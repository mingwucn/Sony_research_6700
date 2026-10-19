"""Invented role records, with no I/O or actual qualification execution."""
import copy
import unittest
from unittest.mock import patch

from tools import dependency_activity_metadata as subject
from tests.test_dependency_source_receipts import fixture as source_fixture
from tests.test_dependency_authority_grammar import raw, chain

e = subject.e


def records(c, args, dep, source, validators=None):
    operation = dep['operation_id']
    validators = validators or {k:('# invented validator '+k).encode() for k in subject.VALIDATORS}
    def rec(schema, **kwargs):
        return dict(schema=schema,invented=True,operation_id=operation,camera_commands=[],**kwargs)
    o = args['ordinary_buffers']
    o['activity_scope'] = raw(rec('invented_activity_scope_v1',
        purpose='offline_metadata_contract_qualification',scope_file_sha256=e.sha(args['scope_bytes']),
        limits=copy.deepcopy(e.policy.SCOPE),source_manifest_sha256=e.sha(o['authored_source_manifest']),
        source_receipts_sha256=e.sha(o['authored_source_receipts']),source_anchor_sha256=e.sha(raw(source)),
        dependency_anchor_sha256=e.sha(raw(dep)),protected=copy.deepcopy(c['protected']),
        historical_blockers=list(e.policy.HISTORY)))
    o['activity_rights'] = raw(rec('invented_activity_rights_v1',scope_file_sha256=e.sha(args['scope_bytes']),
        activity_scope_sha256=e.sha(o['activity_scope']),owner_facts=copy.deepcopy(e.policy.OWNER),
        uncertainties={k:'unresolved' for k in e.policy.RIGHTS},decision='pending',
        legal_basis_established=False,execution_authorized=False))
    source_rows = {k:e.receipt(v) for k,v in args['source_buffers'].items()}
    validator_rows = {k:e.receipt(v) for k,v in validators.items()}
    qualifications = dict(log=b'invented qualification log: all cases claimed passed\n')
    qualifications['result'] = raw(rec('invented_qualification_result_v1',total=7,passed=7,
        failures=0,errors=0,skipped=0,exit_code=0,sources=source_rows,validators=validator_rows,
        log_sha256=e.sha(qualifications['log']),claimed_checked_roles=sorted(e.policy.ORDINARY_INPUTS),
        actual_inputs_accessed=False,execution_authorized=False))
    o['qualification_index'] = raw(rec('invented_qualification_index_v1',purpose='invented_claims_only',
        ordinary={k:e.receipt(o[k]) for k in e.policy.ORDINARY_INPUTS-{'qualification_index'}},
        sources=source_rows,validators=validator_rows,artifacts={k:e.receipt(v) for k,v in qualifications.items()},
        claimed_checked_roles=sorted(e.policy.ORDINARY_INPUTS),execution_authenticated=False,freshness_verified=False))
    anchor = rec('invented_activity_anchor_v1',ordinary={k:e.receipt(o[k]) for k in subject.ROLES},
        source_anchor_sha256=e.sha(raw(source)),dependency_anchor_sha256=e.sha(raw(dep)),
        validators=validator_rows,qualification={k:e.receipt(v) for k,v in qualifications.items()},expected_test_count=7)
    return validators,qualifications,anchor


def fixture():
    c,args,dep,source=source_fixture()
    return c,args,dep,source,*records(c,args,dep,source)


def invoke(c,args,dep,source,validators,qualifications,anchor,*,all_roles=False,external=None):
    c=copy.deepcopy(c)
    c['sources']={k:e.receipt(v) for k,v in args['source_buffers'].items()}
    c['ordinary']={k:e.receipt(v) for k,v in args['ordinary_buffers'].items()}
    docs=chain(c)
    common=dict(**args,external_seal_sha256=e.sha(docs['seal']),source_anchor_bytes=raw(source),
        external_source_anchor_sha256=e.sha(raw(source)),dependency_anchor_bytes=raw(dep),
        external_dependency_anchor_sha256=e.sha(raw(dep)),activity_anchor_bytes=raw(anchor),
        external_activity_anchor_sha256=external or e.sha(raw(anchor)),validator_buffers=validators,
        qualification_buffers=qualifications)
    return (subject.validate_invented_all_metadata if all_roles else subject.validate_invented_activity_roles)(docs,**common)


def change(args,role,mutate):
    value=e.decode(args['ordinary_buffers'][role]);mutate(value);args['ordinary_buffers'][role]=raw(value)


def rebind(args,anchor,qualifications):
    """Rebind caller claims without repairing semantic fields under test."""
    o=args['ordinary_buffers'];index=e.decode(o['qualification_index'])
    index['ordinary']={k:e.receipt(o[k]) for k in e.policy.ORDINARY_INPUTS-{'qualification_index'}}
    index['artifacts']={k:e.receipt(v) for k,v in qualifications.items()}
    o['qualification_index']=raw(index)
    anchor['ordinary']={k:e.receipt(o[k]) for k in subject.ROLES}
    anchor['qualification']={k:e.receipt(v) for k,v in qualifications.items()}


class ActivityMetadataTests(unittest.TestCase):
    def test_four_roles_match_but_do_not_authenticate(self):
        f=fixture();before=copy.deepcopy(f);r=invoke(*f)
        self.assertEqual(len(r['checked_roles']),4);self.assertEqual(f,before)
        self.assertTrue(r['claims_match_supplied_buffers'])
        for key in ('qualification_execution_authenticated','validator_execution_owned','rights_established',
            'history_freshness_verified','actual_inputs_accessed','execution_authorized','feature_supported',
            'recovery_proven','device_write_gate_passed'):
            self.assertIs(r[key],False)

    def test_external_anchor_mismatch(self):
        with self.assertRaisesRegex(ValueError,'activity_external_anchor'):invoke(*fixture(),external='0'*64)

    def test_roles_and_artifacts_have_exact_rosters(self):
        for target in ('ordinary','validators','qualification'):
            f=fixture();f[-1][target]['extra']=dict(bytes=1,sha256='a'*64)
            with self.subTest(target=target),self.assertRaisesRegex(ValueError,'receipt_roster'):invoke(*f)

    def test_changed_raw_scope_not_repaired_by_claim_rebinding(self):
        f=fixture();f[1]['ordinary_buffers']['activity_scope']+=b' '
        with self.assertRaisesRegex(ValueError,'original_bytes_mismatch'):invoke(*f)

    def test_scope_limits_do_not_widen(self):
        for key in ('content_reads','source_opens','camera_operations','child_deadline_seconds'):
            f=fixture();change(f[1],'activity_scope',lambda v:v['limits'].update({key:v['limits'][key]+1}))
            rebind(f[1],f[-1],f[-2])
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'activity_limits'):invoke(*f)

    def test_bool_cannot_replace_numeric_scope_value(self):
        f=fixture();change(f[1],'activity_scope',lambda v:v['limits'].update(camera_operations=False));rebind(f[1],f[-1],f[-2])
        with self.assertRaisesRegex(ValueError,'activity_limits'):invoke(*f)

    def test_source_and_protected_identity_bindings(self):
        for key,value in (('scope_file_sha256','0'*64),('source_manifest_sha256','0'*64),
            ('source_receipts_sha256','0'*64),('source_anchor_sha256','0'*64),('protected',{}),
            ('historical_blockers',[])):
            f=fixture();change(f[1],'activity_scope',lambda v:v.update({key:value}));rebind(f[1],f[-1],f[-2])
            with self.subTest(key=key),self.assertRaises(ValueError):invoke(*f)

    def test_rights_owner_unknown_and_all_uncertainties_preserved(self):
        for key,value in (('owner_facts',dict(e.policy.OWNER,existing_inspection_rights='granted')),
            ('uncertainties',{}),('decision','accepted'),('legal_basis_established',True),
            ('execution_authorized',True),('activity_scope_sha256','0'*64)):
            f=fixture();change(f[1],'activity_rights',lambda v:v.update({key:value}));rebind(f[1],f[-1],f[-2])
            with self.subTest(key=key),self.assertRaises(ValueError):invoke(*f)

    def test_no_historical_promotion_or_missing_original(self):
        for mutate in (lambda v:v.update(purpose='fresh_current_basis'),lambda v:v['receipts'].pop(next(iter(v['receipts'])))):
            f=fixture();change(f[1],'historical_evidence_index',mutate);rebind(f[1],f[-1],f[-2])
            with self.assertRaises(ValueError):invoke(*f)

    def test_result_counts_and_failures_are_strict(self):
        for key,value in (('total',True),('passed',6),('failures',1),('errors',1),('skipped',1),('exit_code',1)):
            f=fixture();v=e.decode(f[-2]['result']);v[key]=value;f[-2]['result']=raw(v);rebind(f[1],f[-1],f[-2])
            with self.subTest(key=key),self.assertRaises(ValueError):invoke(*f)

    def test_result_expected_count_is_external_and_strict(self):
        for value in (True,0,8,1000001):
            f=fixture();f[-1]['expected_test_count']=value
            with self.subTest(value=value),self.assertRaises(ValueError):invoke(*f)

    def test_current_source_drift_refuses_even_when_envelope_rebound(self):
        f=fixture();f[1]['source_buffers']['host_parent_adapter']+=b'#drift'
        with self.assertRaisesRegex(ValueError,'original_bytes_mismatch'):invoke(*f)

    def test_validator_drift_refuses(self):
        f=fixture();f[-3]['activity']+=b'# drift'
        with self.assertRaisesRegex(ValueError,'original_bytes_mismatch'):invoke(*f)

    def test_log_drift_cannot_hide_behind_artifact_rebinding(self):
        f=fixture();f[-2]['log']+=b'drift';rebind(f[1],f[-1],f[-2])
        with self.assertRaisesRegex(ValueError,'qualification_log_binding'):invoke(*f)

    def test_qualification_source_validator_and_coverage_claims(self):
        for key,value in (('sources',{}),('validators',{}),('claimed_checked_roles',[]),
            ('execution_authenticated',True),('freshness_verified',True)):
            f=fixture();change(f[1],'qualification_index',lambda v:v.update({key:value}));rebind(f[1],f[-1],f[-2])
            with self.subTest(key=key),self.assertRaises(ValueError):invoke(*f)

    def test_cross_operation_refuses(self):
        for name in ('activity_scope','activity_rights','qualification_index'):
            f=fixture();change(f[1],name,lambda v:v.update(operation_id='different'));rebind(f[1],f[-1],f[-2])
            with self.subTest(name=name),self.assertRaises(ValueError):invoke(*f)

    def test_unknown_fields_and_actual_mode_refuse(self):
        for name in ('activity_scope','activity_rights','qualification_index'):
            for key,value in (('extra',True),('invented',False),('camera_commands',['operation'])):
                f=fixture();change(f[1],name,lambda v:v.update({key:value}));rebind(f[1],f[-1],f[-2])
                with self.subTest(name=name,key=key),self.assertRaises(ValueError):invoke(*f)

    def test_refusal_before_retained_owned_execution(self):
        f=fixture();f[-1]['expected_test_count']=0
        with patch.object(subject.composed,'validate_invented_composed_inputs') as retained:
            with self.assertRaises(ValueError):invoke(*f,all_roles=True)
            retained.assert_not_called()

    def test_runtime_refuses(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):subject.run_runtime()

    def test_index_cannot_include_itself_or_omit_other_ordinary_roles(self):
        for extra in (True,False):
            f=fixture();index=e.decode(f[1]['ordinary_buffers']['qualification_index'])
            if extra:index['ordinary']['qualification_index']=dict(bytes=1,sha256='0'*64)
            else:index['ordinary'].pop('basis')
            f[1]['ordinary_buffers']['qualification_index']=raw(index)
            f[-1]['ordinary']['qualification_index']=e.receipt(raw(index))
            with self.subTest(extra=extra),self.assertRaisesRegex(ValueError,'receipt_roster'):invoke(*f)

    def test_unknown_anchor_result_fields_and_modes(self):
        for name in ('anchor','result'):
            for key,value in (('extra',True),('invented',False),('operation_id','different')):
                f=fixture()
                if name=='anchor':f[-1][key]=value
                else:
                    result=e.decode(f[-2]['result']);result[key]=value;f[-2]['result']=raw(result)
                    rebind(f[1],f[-1],f[-2])
                with self.subTest(name=name,key=key),self.assertRaises(ValueError):invoke(*f)

    def test_result_source_validator_coverage_and_authority_claims(self):
        for key,value in (('sources',{}),('validators',{}),('claimed_checked_roles',[]),
            ('actual_inputs_accessed',True),('execution_authorized',True)):
            f=fixture();result=e.decode(f[-2]['result']);result[key]=value;f[-2]['result']=raw(result)
            rebind(f[1],f[-1],f[-2])
            with self.subTest(key=key),self.assertRaises(ValueError):invoke(*f)

    def test_rebound_source_or_dependency_anchor_operation_refuses(self):
        for offset in (2,3):
            c,args,dep,source,*_=fixture()
            (dep if offset==2 else source)['operation_id']='different'
            validators,qualifications,anchor=records(c,args,dep,source)
            with self.subTest(offset=offset),self.assertRaisesRegex(ValueError,'activity_operation_binding'):
                invoke(c,args,dep,source,validators,qualifications,anchor)

    def test_caller_can_reanchor_inert_validator_and_log_without_proving_execution(self):
        c,args,dep,source,*_=fixture()
        validators,qualifications,anchor=records(c,args,dep,source,
            validators={k:b'not executable source' for k in subject.VALIDATORS})
        qualifications['log']=b'opaque invented log, not parsed as proof'
        result=e.decode(qualifications['result']);result['log_sha256']=e.sha(qualifications['log'])
        qualifications['result']=raw(result);rebind(args,anchor,qualifications)
        result=invoke(c,args,dep,source,validators,qualifications,anchor)
        self.assertFalse(result['qualification_execution_authenticated'])
        self.assertFalse(result['validator_execution_owned'])

    def test_raw_qualification_and_validator_buffers_are_bounded(self):
        for group,name in ((-2,'log'),(-3,'activity')):
            f=fixture();f[group][name]=b'x'*(e.MAX_BYTES+1)
            with self.subTest(group=group),self.assertRaises(ValueError):invoke(*f)
