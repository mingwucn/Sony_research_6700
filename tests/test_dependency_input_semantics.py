"""Invented records and inert source strings; no dependency activation."""
import copy
import json
import unittest
from unittest.mock import patch

from tools import dependency_input_semantics as subject
from tools import dependency_producer as producer
from tools import dependency_evidence as core
from tests.test_dependency_authority_grammar import fixture as envelope_fixture, chain, raw
from test_dependency_producer import fixture as dependency_fixture, refresh


def fixture():
    candidate, args = envelope_fixture()
    data, _ = dependency_fixture()
    mapping = dict(runtime='dependency.dependency_producer', continuation='bound.integration:prospective_child')
    for alias, role in mapping.items():
        args['source_buffers'][role] = data['source_buffers'][alias]
    packet = dict(schema='runtime_dependency_packet_v1', inputs={k:v for k,v in data.items() if k!='source_buffers'})
    args['ordinary_buffers']['dependency_packet'] = raw(packet)
    args['ordinary_buffers']['dependency_fixed'] = raw(dict(expectation_sha256=core._hash(data['expectation']),
        package_sha256=core._hash(data['package']),
        root_sha256={k:v['identity_sha256'] for k,v in data['expectation']['roots'].items()}))
    anchor = dict(schema='invented_dependency_input_anchor_v1', invented=True,
        operation_id=data['expectation']['operation_id'],
        fixed_file_sha256=subject.envelope.sha(args['ordinary_buffers']['dependency_fixed']),
        prior_review_sha256=data['binding']['review_sha256'], source_roles=mapping)
    return candidate, args, anchor


def bind(candidate, args, anchor):
    candidate=copy.deepcopy(candidate)
    candidate['sources']={r:subject.envelope.receipt(v) for r,v in args['source_buffers'].items()}
    candidate['ordinary']={r:subject.envelope.receipt(v) for r,v in args['ordinary_buffers'].items()}
    documents=chain(candidate)
    return subject.validate_invented_dependency_roles(documents,
        external_seal_sha256=subject.envelope.sha(documents['seal']), **args,
        dependency_anchor_bytes=raw(anchor),external_dependency_anchor_sha256=subject.envelope.sha(raw(anchor)))


class DependencyInputTests(unittest.TestCase):
    def setUp(self):
        self.c,self.args,self.anchor=fixture()

    def packet_change(self, callback):
        packet=json.loads(self.args['ordinary_buffers']['dependency_packet'])
        callback(packet)
        self.args['ordinary_buffers']['dependency_packet']=raw(packet)

    def check(self):
        return bind(self.c,self.args,self.anchor)

    def test_retained_binder_checks_without_runtime_reads_or_bootstrap(self):
        before=copy.deepcopy((self.c,self.args,self.anchor))
        with patch.object(producer,'RuntimeOps',side_effect=AssertionError('no runtime')):
            result=self.check()
        self.assertEqual((self.c,self.args,self.anchor),before)
        self.assertEqual(result['checked_roles'],['dependency_fixed','dependency_packet'])
        self.assertEqual(len(result['pending_roles']),12)
        for key in ('current_metadata_freshness_verified','producer_execution_authenticated',
                    'interpreter_identity_verified','actual_inputs_accessed','execution_authorized',
                    'feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(result[key],False)

    def test_dependency_anchor_cannot_be_replaced_without_external_digest(self):
        candidate=copy.deepcopy(self.c)
        candidate['sources']={r:subject.envelope.receipt(v) for r,v in self.args['source_buffers'].items()}
        candidate['ordinary']={r:subject.envelope.receipt(v) for r,v in self.args['ordinary_buffers'].items()}
        docs=chain(candidate)
        with self.assertRaisesRegex(ValueError,'dependency_external_anchor'):
            subject.validate_invented_dependency_roles(docs,external_seal_sha256=subject.envelope.sha(docs['seal']),
                **self.args,dependency_anchor_bytes=raw(self.anchor),external_dependency_anchor_sha256='0'*64)

    def test_changed_fixed_even_when_outer_chain_rebound_refuses(self):
        value=json.loads(self.args['ordinary_buffers']['dependency_fixed']); value['expectation_sha256']='a'*64
        self.args['ordinary_buffers']['dependency_fixed']=raw(value)
        with self.assertRaisesRegex(ValueError,'dependency_fixed_original_bytes'): self.check()

    def test_self_consistent_changed_policy_and_fixed_cannot_replace_prior_anchor(self):
        def mutate(packet):
            packet['inputs']['expectation']['loader_kwargs']={'winmode':0}
            packet['inputs']['binding']['expectation_sha256']=core._hash(packet['inputs']['expectation'])
        self.packet_change(mutate)
        packet=json.loads(self.args['ordinary_buffers']['dependency_packet'])
        fixed=json.loads(self.args['ordinary_buffers']['dependency_fixed'])
        fixed['expectation_sha256']=core._hash(packet['inputs']['expectation'])
        self.args['ordinary_buffers']['dependency_fixed']=raw(fixed)
        with self.assertRaisesRegex(ValueError,'dependency_fixed_original_bytes'): self.check()

    def test_reformatted_fixed_requires_external_original_byte_rebinding(self):
        self.args['ordinary_buffers']['dependency_fixed']=json.dumps(json.loads(self.args['ordinary_buffers']['dependency_fixed']),indent=2).encode()
        with self.assertRaisesRegex(ValueError,'dependency_fixed_original_bytes'): self.check()

    def test_prior_review_substitution_refuses(self):
        self.anchor['prior_review_sha256']='a'*64
        with self.assertRaisesRegex(ValueError,'review_binding'): self.check()

    def test_current_outer_review_not_permitted_as_prior_id(self):
        candidate=copy.deepcopy(self.c)
        candidate['sources']={r:subject.envelope.receipt(v) for r,v in self.args['source_buffers'].items()}
        candidate['ordinary']={r:subject.envelope.receipt(v) for r,v in self.args['ordinary_buffers'].items()}
        docs=chain(candidate)
        for name in ('candidate','review','decision','seal'):
            self.anchor['prior_review_sha256']=subject.envelope.sha(docs[name])
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'dependency_review_cycle'): self.check()

    def test_operation_cannot_silently_reuse_other_context(self):
        self.anchor['operation_id']='other-operation'
        with self.assertRaisesRegex(ValueError,'dependency_operation'): self.check()

    def test_embedded_config_operation_must_match_policy(self):
        def mutate(packet):
            inputs=packet['inputs']; config=json.loads(inputs['config_json']);config['operation_id']='other-operation'
            inputs['config_json']=producer.encoded(config).decode()
            inputs['expectation']['config_sha256']=producer.sha(inputs['config_json'].encode())
            inputs['binding']['expectation_sha256']=core._hash(inputs['expectation'])
        self.packet_change(mutate)
        fixed=json.loads(self.args['ordinary_buffers']['dependency_fixed'])
        fixed['expectation_sha256']=core._hash(json.loads(self.args['ordinary_buffers']['dependency_packet'])['inputs']['expectation'])
        self.args['ordinary_buffers']['dependency_fixed']=raw(fixed)
        self.anchor['fixed_file_sha256']=subject.envelope.sha(raw(fixed))
        with self.assertRaisesRegex(ValueError,'public_plan'): self.check()

    def test_mapping_roster_unknown_role_and_duplicate_role_refuse(self):
        for mapping in ({'runtime':'outer_gate'},dict(self.anchor['source_roles'],runtime='invented_fixture'),
                        dict.fromkeys(self.anchor['source_roles'],'outer_gate')):
            with self.subTest(mapping=mapping),self.assertRaises(ValueError):
                bind(self.c,self.args,dict(self.anchor,source_roles=mapping))

    def test_changed_mapped_source_bytes_even_when_outer_receipts_rebound(self):
        self.args['source_buffers']['dependency.dependency_producer']=b'# different'
        with self.assertRaisesRegex(ValueError,'source_hash'): self.check()

    def test_raw_config_and_cache_hashes_are_not_canonical_objects(self):
        for name in ('config','cache'):
            c,args,anchor=fixture(); packet=json.loads(args['ordinary_buffers']['dependency_packet']); inputs=packet['inputs']
            inputs['expectation'][name+'_sha256']=core._hash(json.loads(inputs[name+'_json']))
            inputs['binding']['expectation_sha256']=core._hash(inputs['expectation'])
            args['ordinary_buffers']['dependency_packet']=raw(packet)
            fixed=json.loads(args['ordinary_buffers']['dependency_fixed']);fixed['expectation_sha256']=core._hash(inputs['expectation'])
            args['ordinary_buffers']['dependency_fixed']=raw(fixed);anchor['fixed_file_sha256']=subject.envelope.sha(raw(fixed))
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'input_hash'):bind(c,args,anchor)

    def test_packet_cannot_supply_observer_or_protected_input(self):
        for name in ('ops','callback','firmware_package'):
            c,args,anchor=fixture(); value=json.loads(args['ordinary_buffers']['dependency_packet'])
            value['inputs'][name]={};args['ordinary_buffers']['dependency_packet']=raw(value)
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'dependency_input_roster'):bind(c,args,anchor)

    def test_consistent_invented_metadata_passes_without_proving_observations(self):
        # These package receipts, paths and cache strings were invented; passing
        # the retained production-shaped binder does not make them observations.
        result=self.check()
        self.assertFalse(result['current_metadata_freshness_verified'])
        self.assertNotEqual(result['fixed_file_sha256'],result['expectation_object_sha256'])

    def test_changed_root_expectation_cannot_replace_prior_fixed_anchor(self):
        value=json.loads(self.args['ordinary_buffers']['dependency_fixed'])
        value['root_sha256']['runtime']='e'*64
        self.args['ordinary_buffers']['dependency_fixed']=raw(value)
        with self.assertRaisesRegex(ValueError,'dependency_fixed_original_bytes'): self.check()

    def test_changed_package_expectation_cannot_replace_prior_fixed_anchor(self):
        value=json.loads(self.args['ordinary_buffers']['dependency_fixed'])
        value['package_sha256']='e'*64
        self.args['ordinary_buffers']['dependency_fixed']=raw(value)
        with self.assertRaisesRegex(ValueError,'dependency_fixed_original_bytes'): self.check()

    def test_package_proof_mismatch_refuses_even_after_outer_rebinding(self):
        def mutate(packet):
            packet['inputs']['package']['installed_proof']['roster_sha256']='0'*64
        self.packet_change(mutate)
        with self.assertRaises(ValueError): self.check()

    def test_policy_root_change_rebound_binding_still_refuses_old_fixed_expectations(self):
        def mutate(packet):
            inputs=packet['inputs'];inputs['expectation']['roots']['runtime']['identity_sha256']='e'*64
            inputs['binding']['expectation_sha256']=core._hash(inputs['expectation'])
        self.packet_change(mutate)
        with self.assertRaisesRegex(ValueError,'fixed_expectations'): self.check()

    def test_anchor_unknown_field_actual_mode_or_noninvented_refuses(self):
        for change in ({'execution_authorized':True},{'invented':False},{'schema':'actual_dependency_input_anchor_v1'}):
            with self.subTest(change=change),self.assertRaises(ValueError):
                bind(self.c,self.args,dict(self.anchor,**change))

    def test_explicit_new_fixed_byte_anchor_allows_reformat_without_semantic_change(self):
        before=self.check()
        self.args['ordinary_buffers']['dependency_fixed']=json.dumps(json.loads(self.args['ordinary_buffers']['dependency_fixed']),indent=2).encode()
        self.anchor['fixed_file_sha256']=subject.envelope.sha(self.args['ordinary_buffers']['dependency_fixed'])
        after=self.check()
        self.assertNotEqual(before['fixed_file_sha256'],after['fixed_file_sha256'])
        self.assertEqual(before['expectation_object_sha256'],after['expectation_object_sha256'])
        self.assertFalse(after['execution_authorized'])

    def test_runtime_always_disabled(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'): subject.run_runtime()
