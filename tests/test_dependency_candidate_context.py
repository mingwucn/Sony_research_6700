"""Invented context DAGs; no actual files, sidecar execution or camera."""
import copy
import unittest
from unittest.mock import patch

from tools import dependency_candidate_context as subject
from tests.test_dependency_authority_grammar import fixture as legacy_fixture, chain, raw

e=subject.e


def context_chain(candidate):
    common=dict(invented=True,operation_id=candidate['operation_id'],camera_commands=[])
    docs=dict(candidate=raw(candidate))
    docs['review']=raw(dict(schema='invented_context_review_v2',**common,
        candidate_sha256=e.sha(docs['candidate']),outcome='accepted_shape'))
    docs['decision']=raw(dict(schema='invented_context_decision_v2',**common,
        candidate_sha256=e.sha(docs['candidate']),review_sha256=e.sha(docs['review']),
        outcome='pending' if candidate['phase']=='prepared' else 'accepted_shape'))
    docs['seal']=raw(dict(schema='invented_context_seal_v2',**common,
        **{n+'_sha256':e.sha(docs[n]) for n in ('candidate','review','decision')}))
    return docs


def candidate(legacy,scope,anchors,operation,phase='prepared'):
    return dict(schema='invented_context_candidate_v2',invented=True,operation_id=operation,camera_commands=[],
        purpose='non_executable_context_comparison',phase=phase,scope_file_sha256=e.sha(scope),
        legacy_documents={k:e.receipt(v) for k,v in legacy.items()},anchors={k:e.receipt(v) for k,v in anchors.items()})


def fixture(phase='prepared'):
    c,args=legacy_fixture(phase);legacy=chain(c);operation='invented_context_operation'
    anchors={k:raw(dict(operation_id=operation,tag=k)) for k in subject.ANCHORS}
    return candidate(legacy,args['scope_bytes'],anchors,operation,phase),dict(
        expected_operation_id=operation,legacy_documents=legacy,scope_bytes=args['scope_bytes'],anchor_buffers=anchors)


def invoke(c,args):
    docs=context_chain(c)
    return subject.validate_invented_context_documents(docs,external_seal_sha256=e.sha(docs['seal']),**args)


def reseal(docs):
    review=e.decode(docs['review']);review['candidate_sha256']=e.sha(docs['candidate']);docs['review']=raw(review)
    decision=e.decode(docs['decision']);decision.update(candidate_sha256=e.sha(docs['candidate']),review_sha256=e.sha(docs['review']))
    docs['decision']=raw(decision)
    seal=e.decode(docs['seal']);seal.update({n+'_sha256':e.sha(docs[n]) for n in ('candidate','review','decision')});docs['seal']=raw(seal)


class CandidateContextTests(unittest.TestCase):
    def test_both_shapes_bind_operation_without_authority(self):
        for phase in ('prepared','operational_shape'):
            c,args=fixture(phase);before=copy.deepcopy((c,args));r=invoke(c,args)
            self.assertEqual((c,args),before);self.assertTrue(r['candidate_operation_consistent'])
            for key in ('operation_origin_authenticated','reviewer_authenticated','owner_permission_authenticated',
                'retained_sidecar_contracts_checked','validator_execution_owned','source_freshness_verified',
                'rights_established','dependency_bridge_verified','actual_startup_verified','actual_inputs_accessed',
                'execution_authorized','feature_supported','recovery_proven','device_write_gate_passed'):
                self.assertIs(r[key],False)

    def test_external_operation_is_strict_and_not_taken_from_documents(self):
        for operation in ('different','',True,'含中文','a'*97):
            c,args=fixture();args['expected_operation_id']=operation
            with self.subTest(operation=operation),self.assertRaises(ValueError):invoke(c,args)

    def test_each_document_operation_must_agree_even_after_resealing(self):
        for name in e.DOCUMENTS:
            c,args=fixture();docs=context_chain(c);v=e.decode(docs[name]);v['operation_id']='other';docs[name]=raw(v);reseal(docs)
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'context_operation'):
                subject.validate_invented_context_documents(docs,external_seal_sha256=e.sha(docs['seal']),**args)

    def test_each_sidecar_operation_cannot_be_rebound_into_current_context(self):
        for name in subject.ANCHORS:
            c,args=fixture();args['anchor_buffers'][name]=raw(dict(operation_id='other'))
            c['anchors'][name]=e.receipt(args['anchor_buffers'][name])
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'context_sidecar_operation'):invoke(c,args)

    def test_sidecar_and_legacy_original_bytes_are_bound(self):
        for group,key in [('anchor_buffers',n) for n in subject.ANCHORS]+[('legacy_documents',n) for n in e.DOCUMENTS]:
            c,args=fixture();args[group][key]+=b' '
            with self.subTest(group=group),self.assertRaisesRegex(ValueError,'original_bytes_mismatch'):invoke(c,args)

    def test_scope_original_bytes_are_bound(self):
        c,args=fixture();args['scope_bytes']+=b' '
        with self.assertRaisesRegex(ValueError,'context_scope_bytes'):invoke(c,args)

    def test_phase_must_match_legacy_payload(self):
        for phase,other in (('prepared','operational_shape'),('operational_shape','prepared')):
            c,args=fixture(phase);c['phase']=other
            with self.subTest(phase=phase),self.assertRaisesRegex(ValueError,'context_legacy_phase'):invoke(c,args)

    def test_external_seal_mismatch_and_old_schema_refuse(self):
        c,args=fixture();docs=context_chain(c)
        with self.assertRaisesRegex(ValueError,'context_external_seal'):
            subject.validate_invented_context_documents(docs,external_seal_sha256='0'*64,**args)
        c['schema']='invented_authority_candidate_v1'
        with self.assertRaisesRegex(ValueError,'context_invented_mode'):invoke(c,args)

    def test_closed_document_fields_and_invented_modes(self):
        for name in e.DOCUMENTS:
            for key,value in (('extra',True),('invented',False),('camera_commands',['operation'])):
                c,args=fixture();docs=context_chain(c);v=e.decode(docs[name]);v[key]=value;docs[name]=raw(v);reseal(docs)
                with self.subTest(name=name,key=key),self.assertRaises(ValueError):
                    subject.validate_invented_context_documents(docs,external_seal_sha256=e.sha(docs['seal']),**args)

    def test_exact_four_document_and_anchor_rosters(self):
        for group in ('documents','legacy_documents','anchor_buffers'):
            c,args=fixture();docs=context_chain(c)
            if group=='documents':docs.pop('review')
            else:args[group].pop(next(iter(args[group])))
            with self.subTest(group=group),self.assertRaises(ValueError):
                subject.validate_invented_context_documents(docs,external_seal_sha256=e.sha(docs['seal']),**args)

    def test_review_decision_and_seal_original_hashes_refuse(self):
        for name,key in (('review','candidate_sha256'),('decision','review_sha256'),('seal','decision_sha256')):
            c,args=fixture();docs=context_chain(c);v=e.decode(docs[name]);v[key]='0'*64;docs[name]=raw(v)
            with self.subTest(name=name),self.assertRaises(ValueError):
                subject.validate_invented_context_documents(docs,external_seal_sha256=e.sha(docs['seal']),**args)

    def test_refused_review_or_wrong_decision_phase_refuse_when_resealed(self):
        for name in ('review','decision'):
            c,args=fixture();docs=context_chain(c);v=e.decode(docs[name]);v['outcome']='refused_shape';docs[name]=raw(v);reseal(docs)
            with self.subTest(name=name),self.assertRaises(ValueError):
                subject.validate_invented_context_documents(docs,external_seal_sha256=e.sha(docs['seal']),**args)

    def test_reanchored_opaque_sidecars_do_not_authenticate_semantics(self):
        c,args=fixture();args['anchor_buffers']['bridge']=raw(dict(operation_id=c['operation_id'],opaque=True))
        c['anchors']['bridge']=e.receipt(args['anchor_buffers']['bridge'])
        r=invoke(c,args);self.assertFalse(r['retained_sidecar_contracts_checked'])
        self.assertFalse(r['execution_authorized'])

    def test_invalid_context_refuses_before_retained_validator_execution(self):
        c,args=fixture();docs=context_chain(c)
        inputs=dict(scope_bytes=args['scope_bytes'],**{name+'_anchor_bytes':args['anchor_buffers'][name] for name in subject.ANCHORS})
        with patch.object(subject.bridge,'validate_invented_bridge') as retained:
            with self.assertRaisesRegex(ValueError,'context_external_seal'):
                subject.validate_invented_context_composition(docs,args['legacy_documents'],
                    external_context_seal_sha256='0'*64,expected_operation_id=c['operation_id'],**inputs)
            retained.assert_not_called()

    def test_duplicate_json_keys_and_oversized_context_refuse(self):
        c,args=fixture();docs=context_chain(c);docs['review']=b'{"schema":1,"schema":2}'
        with self.assertRaisesRegex(ValueError,'duplicate_json_key'):
            subject.validate_invented_context_documents(docs,external_seal_sha256=e.sha(docs['seal']),**args)
        c,args=fixture();args['scope_bytes']=b'x'*(e.MAX_BYTES+1)
        with self.assertRaises(ValueError):invoke(c,args)

    def test_runtime_refuses(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):subject.run_runtime()

    def test_both_decision_phase_mismatches_refuse(self):
        for phase,outcome in (('prepared','accepted_shape'),('operational_shape','pending')):
            c,args=fixture(phase);docs=context_chain(c);v=e.decode(docs['decision']);v['outcome']=outcome
            docs['decision']=raw(v);reseal(docs)
            with self.subTest(phase=phase),self.assertRaisesRegex(ValueError,'context_decision_phase'):
                subject.validate_invented_context_documents(docs,external_seal_sha256=e.sha(docs['seal']),**args)

    def test_caller_can_reanchor_new_operation_without_authenticating_its_origin(self):
        c,args=fixture();c['operation_id']=args['expected_operation_id']='replacement_operation'
        for name in subject.ANCHORS:
            args['anchor_buffers'][name]=raw(dict(operation_id=c['operation_id'],tag=name))
            c['anchors'][name]=e.receipt(args['anchor_buffers'][name])
        result=invoke(c,args);self.assertTrue(result['candidate_operation_consistent'])
        self.assertFalse(result['operation_origin_authenticated']);self.assertFalse(result['execution_authorized'])
