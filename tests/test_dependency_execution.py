"""Invented metadata/texts only; no installed dependency or actual observations."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from tools import dependency_execution as subject
from tools import dependency_package_preflight as collector
from tools import dependency_producer as producer
from tools import dependency_evidence as core
from test_dependency_package_preflight import complete_fixture


class TransitionTests(unittest.TestCase):
    def setUp(self):
        self.inputs,self.ops=complete_fixture()
        self.collection=collector.collect_invented(ops=self.ops,**self.inputs)

    def execute(self):return subject.bind_collection(collection=self.collection,inputs=self.inputs)

    def test_transition_retains_prior_and_only_changes_derived_proof_binding(self):
        before=copy.deepcopy(self.inputs); previous=copy.deepcopy(self.collection)
        path=next(p for p in self.ops.observed if '/data/item' in p)
        for name in ('fstat_before','fstat_after'):self.ops.observed[path][name]['ctime_ns']+=1
        self.collection=collector.collect_invented(ops=self.ops,**self.inputs)
        data,transition=self.execute()
        self.assertEqual(self.inputs,before)
        oldpolicy=before['expectation'];newpolicy=dict(data['expectation'])
        self.assertNotEqual(newpolicy['installed_proof_sha256'],oldpolicy['installed_proof_sha256'])
        newpolicy['installed_proof_sha256']=oldpolicy['installed_proof_sha256'];self.assertEqual(newpolicy,oldpolicy)
        self.assertEqual(data['binding']['review_sha256'],before['binding']['review_sha256'])
        self.assertNotEqual(transition['original_package_sha256'],transition['observed_package_sha256'])
        self.assertIs(transition['independent_approval_created'],False)
        producer.bind_inputs(**data)
        self.assertEqual(previous['prior_package_sha256'],core._hash(before['package']))

    def test_returned_proof_is_detached_from_collection(self):
        data,_=self.execute();self.collection['package']['installed_proof']['files'].clear()
        self.assertEqual(len(data['package']['installed_proof']['files']),351)

    def test_returned_source_buffers_are_detached_in_both_directions(self):
        data,_=self.execute();before=dict(self.inputs['source_buffers'])
        data['source_buffers']['runtime']=b'changed'
        self.assertEqual(self.inputs['source_buffers'],before)
        self.inputs['source_buffers']['continuation']=b'caller changed'
        self.assertEqual(data['source_buffers']['continuation'],before['continuation'])

    def test_unchanged_proof_does_not_claim_policy_change(self):
        _,transition=self.execute()
        self.assertEqual(transition['changed_policy_fields'],[])

    def test_rejects_projected_path_only_without_absolute_record(self):
        relative=next(iter(self.collection['absolute_receipts']))
        self.collection['absolute_receipts'][relative]['path']=relative
        with self.assertRaisesRegex(core.EvidenceError,'^receipt_binding$'):self.execute()

    def test_rejects_forged_projection_hash(self):
        relative=next(iter(self.collection['relative_projection']))
        self.collection['relative_projection'][relative]['absolute_receipt_sha256']='0'*64
        with self.assertRaisesRegex(core.EvidenceError,'^projection_hash$'):self.execute()

    def test_rejects_changed_source_alias_roster(self):
        self.collection['source_aliases'].pop()
        with self.assertRaisesRegex(core.EvidenceError,'^collection_sources$'):self.execute()

    def test_rejects_wrong_original_package_binding(self):
        self.collection['prior_package_sha256']='0'*64
        with self.assertRaisesRegex(core.EvidenceError,'^collection_binding$'):self.execute()

    def test_rejects_rebound_manifest_even_with_self_consistent_collection(self):
        self.collection['package']['manifest']['wheel_sha256']='0'*64
        self.collection['observed_package_sha256']=core._hash(self.collection['package'])
        with self.assertRaisesRegex(core.EvidenceError,'^manifest_changed$'):self.execute()

    def test_rejects_changed_root(self):
        self.collection['root_after']['package']['path']='Z:/changed'
        with self.assertRaisesRegex(core.EvidenceError,'^root_identity$'):self.execute()

    def test_rejects_extra_absolute_receipt(self):
        self.collection['absolute_receipts']['extra']={}
        with self.assertRaisesRegex(core.EvidenceError,'^shape$'):self.execute()

    def test_false_authority_flags_are_strict_booleans(self):
        for name in ('execution_authorized','actual_installation_observed','atomic_snapshot_proven'):
            old=self.collection[name];self.collection[name]=0
            with self.subTest(name=name),self.assertRaisesRegex(core.EvidenceError,'^collection_authority$'):self.execute()
            self.collection[name]=old

    def test_counts_cannot_be_booleans(self):
        self.collection['package_reads']=True
        with self.assertRaisesRegex(core.EvidenceError,'^collection_counts$'):self.execute()

    def test_no_actual_record_promotion(self):
        self.collection['evidence_mode']='saved_records'
        with self.assertRaisesRegex(core.EvidenceError,'^collection_mode$'):self.execute()

    def test_raw_cache_digest_is_not_canonical_digest(self):
        self.collection['raw_cache_sha256']=core._hash(core._json_text(self.inputs['cache_json']))
        with self.assertRaisesRegex(core.EvidenceError,'^collection_sources$'):self.execute()


class TextPreparationTests(unittest.TestCase):
    def setUp(self):
        self.data,_=complete_fixture()
        self.kw=dict(operation_id=self.data['expectation']['operation_id'],
            vectors=core._json_text(self.data['config_json'])['vectors'],sources=core._json_text(self.data['cache_json'])['sources'])

    def test_explicit_canonical_texts_keep_raw_and_object_hash_domains(self):
        before=copy.deepcopy(self.kw);value=subject.prepare_texts(**self.kw)
        self.assertEqual(self.kw,before)
        for label in ('config','cache'):
            text=value[label+'_json'];self.assertTrue(text.endswith('\n'))
            self.assertEqual(value[label+'_file_sha256'],producer.sha(text.encode()))
            self.assertEqual(value[label+'_object_sha256'],core._hash(core._json_text(text)))
            self.assertNotEqual(value[label+'_file_sha256'],value[label+'_object_sha256'])

    def test_missing_alias_refuses(self):
        self.kw['sources'].pop(producer.ALIASES[0])
        with self.assertRaisesRegex(core.EvidenceError,'^shape$'):subject.prepare_texts(**self.kw)

    def test_arbitrary_vector_plan_refuses(self):
        self.kw['vectors']=[]
        with self.assertRaisesRegex(core.EvidenceError,'^public_plan$'):subject.prepare_texts(**self.kw)

    def test_source_text_bound(self):
        self.kw['sources'][producer.ALIASES[0]]='x'*(1024**2+1)
        with patch.object(producer,'encoded',side_effect=AssertionError('serialization entered')), \
             self.assertRaisesRegex(core.EvidenceError,'^cache_bound$'):subject.prepare_texts(**self.kw)

    def test_escaped_document_budget_precedes_serialization(self):
        self.kw['sources']={alias:'\x00'*70000 for alias in producer.ALIASES}
        with patch.object(producer,'encoded',side_effect=AssertionError('serialization entered')), \
             self.assertRaisesRegex(core.EvidenceError,'^cache_bound$'):subject.prepare_texts(**self.kw)

    def test_del_escaped_budget_precedes_serialization(self):
        self.kw['sources']={alias:'\x7f'*70000 for alias in producer.ALIASES}
        with patch.object(producer,'encoded',side_effect=AssertionError('serialization entered')), \
             self.assertRaisesRegex(core.EvidenceError,'^cache_bound$'):subject.prepare_texts(**self.kw)

    def test_deep_vectors_refuse_before_hash(self):
        value=[]
        for _ in range(20):value=[value]
        self.kw['vectors']=value
        with patch.object(core,'_hash',side_effect=AssertionError('hash entered')), \
             self.assertRaisesRegex(core.EvidenceError,'^bound$'):subject.prepare_texts(**self.kw)

    def test_source_subclass_is_never_encoded(self):
        class Source(str):
            def encode(self,*a,**kw):raise AssertionError('subclass encode')
        self.kw['sources'][producer.ALIASES[0]]=Source('text')
        with self.assertRaisesRegex(core.EvidenceError,'^source_text$'):subject.prepare_texts(**self.kw)

    def test_surrogates_refuse_before_serialization(self):
        self.kw['sources'][producer.ALIASES[0]]='\ud800'
        with patch.object(producer,'encoded',side_effect=AssertionError('serialization entered')), \
             self.assertRaisesRegex(core.EvidenceError,'^source_text$'):subject.prepare_texts(**self.kw)

    def test_unicode_and_escapes_keep_exact_document_hashes(self):
        self.kw['sources'][producer.ALIASES[0]]='中\U0001f600\n\\"\x01\x7f'
        value=subject.prepare_texts(**self.kw)
        self.assertEqual(core._json_text(value['cache_json'])['sources'],self.kw['sources'])

    def test_operation_cannot_be_path(self):
        self.kw['operation_id']='../bad'
        with self.assertRaisesRegex(core.EvidenceError,'^operation$'):subject.prepare_texts(**self.kw)


class RecordVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs,ops=complete_fixture()
        value=collector.collect_invented(ops=ops,**cls.inputs)
        cls.inputs,_=subject.bind_collection(collection=value,inputs=cls.inputs)
        helper=types.ModuleType('_invented_dependency_probe');helper.new=ops.new
        additions={'_invented_dependency_probe':helper,'ctypes':ops.modules['ctypes']}
        original={name:sys.modules.get(name) for name in additions}
        try:
            sys.modules.update(additions)
            with tempfile.TemporaryDirectory() as directory:
                folder=Path(directory)/'producer'
                producer.produce_invented(**cls.inputs,ops=ops,folder=folder)
                cls.saved={name:(folder/name).read_bytes() for name in subject.ARTIFACTS}
        finally:
            for name,module in original.items():
                if module is None:sys.modules.pop(name,None)
                else:sys.modules[name]=module

    def setUp(self):self.artifacts=copy.deepcopy(self.saved)

    def rewrite(self,name,mutator):
        value=core._json_text(self.artifacts[name].decode());mutator(value)
        self.artifacts[name]=producer.encoded(value)

    def verify(self,mode='invented',injected=True):
        return subject.verify_records(artifacts=self.artifacts,inputs=self.inputs,
            evidence_mode=mode,test_injection_used=injected)

    def test_complete_invented_saved_artifacts_and_false_authority(self):
        value=self.verify()
        self.assertEqual(value['artifact_sha256'],{k:producer.sha(v) for k,v in self.artifacts.items()})
        for name in ('historical_truth_verified','producer_execution_authenticated','execution_authorized','actual_runtime_verified'):
            self.assertIs(value[name],False)

    def test_saved_record_grammar_on_explicitly_invented_metadata(self):
        # Parser qualification only. No runtime observation is claimed by this test.
        def change(row):
            row['test_injection_used']=False;row['audit_acknowledgement_is_invented']=False
            row['observation']['evidence_mode']='saved_records'
            row['consistency']=core.validate_dependency_records(expectation=self.inputs['expectation'],package=self.inputs['package'],
                observation=row['observation'],raw_receipt_json=self.artifacts['raw.json'].decode(),journal_jsonl=self.artifacts['journal.jsonl'].decode())
        self.rewrite('result.json',change)
        self.rewrite('audit-acknowledgement.json',lambda row:row.update(test_injection_used=False))
        value=self.verify('saved_records',False)
        self.assertIs(value['actual_runtime_verified'],False);self.assertIs(value['historical_truth_verified'],False)

    def test_mode_mismatch_refuses(self):
        with self.assertRaisesRegex(core.EvidenceError,'^result_flags$'):self.verify('saved_records',False)

    def test_unknown_artifact_refuses(self):
        self.artifacts['extra.json']=b'{}'
        with self.assertRaisesRegex(core.EvidenceError,'^shape$'):self.verify()

    def test_missing_artifact_refuses(self):
        del self.artifacts['raw.json']
        with self.assertRaisesRegex(core.EvidenceError,'^shape$'):self.verify()

    def test_unknown_result_field_refuses(self):
        self.rewrite('result.json',lambda row:row.update(extra=True))
        with self.assertRaisesRegex(core.EvidenceError,'^shape$'):self.verify()

    def test_promoted_authority_refuses(self):
        self.rewrite('result.json',lambda row:row.update(execution_authorized=True))
        with self.assertRaisesRegex(core.EvidenceError,'^result_flags$'):self.verify()

    def test_forged_callback_transcript_refuses(self):
        self.artifacts['journal.jsonl']=self.artifacts['journal.jsonl'].replace(b'callback_claimed',b'callback_renamed')
        with self.assertRaises(core.EvidenceError):self.verify()

    def test_trace_sha_substitution_refuses(self):
        self.rewrite('result.json',lambda row:row['source_execution_trace'][0].update(sha256='0'*64))
        with self.assertRaisesRegex(core.EvidenceError,'^source_trace$'):self.verify()

    def test_trace_nesting_refuses(self):
        def change(row):row['source_execution_trace'][0],row['source_execution_trace'][1]=row['source_execution_trace'][1],row['source_execution_trace'][0]
        self.rewrite('result.json',change)
        with self.assertRaisesRegex(core.EvidenceError,'^source_trace$'):self.verify()

    def test_wrong_audit_operation_refuses(self):
        self.rewrite('audit-acknowledgement.json',lambda row:row.update(operation_id='wrong'))
        with self.assertRaisesRegex(core.EvidenceError,'^audit_acknowledgement$'):self.verify()

    def test_exact_binding_must_match(self):
        self.rewrite('binding.json',lambda row:row.update(review_sha256='0'*64))
        with self.assertRaisesRegex(core.EvidenceError,'^saved_binding$'):self.verify()

    def test_duplicate_keys_refuse(self):
        self.artifacts['result.json']=b'{"schema":"x","schema":"y"}'
        with self.assertRaisesRegex(core.EvidenceError,'^duplicate_key$'):self.verify()

    def test_oversized_artifact_refuses(self):
        self.artifacts['result.json']=b'x'*(4*1024**2+1)
        with self.assertRaisesRegex(core.EvidenceError,'^artifact_bound$'):self.verify()

    def test_verification_uses_no_reader_bootstrap_or_loader(self):
        with patch.object(producer.RuntimeOps,'reader',side_effect=AssertionError('actual read')), \
             patch.object(producer.RuntimeOps,'bootstrap',side_effect=AssertionError('actual bootstrap')):
            self.verify()


class CollectedCompositionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name)/'attempt';self.inputs,self.ops=complete_fixture()

    def execute(self):
        helper=types.ModuleType('_invented_dependency_probe');helper.new=self.ops.new
        with patch.dict(sys.modules,{'_invented_dependency_probe':helper,'ctypes':self.ops.modules['ctypes']}):
            return subject.produce_collected_invented(inputs=self.inputs,ops=self.ops,folder=self.folder)

    def completion(self):return core._json_text((self.folder/'completion.json').read_text())

    def test_complete_collection_precedes_bootstrap_and_saved_verification(self):
        before=copy.deepcopy(self.inputs);seen=[];original=self.ops.bootstrap
        def bootstrap():
            seen.append(len(self.ops.reads))
            self.assertTrue((self.folder/'collection.json').exists())
            self.assertTrue((self.folder/'transition.json').exists())
            return original()
        self.ops.bootstrap=bootstrap
        result=self.execute()
        self.assertGreaterEqual(seen[0],361)
        self.assertEqual(self.inputs,before)
        self.assertEqual(result['status'],'complete_invented_composition')
        self.assertEqual((self.ops.loader_calls,self.ops.callback_calls,self.ops.cipher_calls),(5,1,48))
        self.assertEqual(result,self.completion())
        for name in ('collection','transition','verification'):
            value=core._json_text((self.folder/(name+'.json')).read_text())
            self.assertEqual(core._hash(value),result[name+'_sha256'])
        self.assertIs(result['actual_dependency_observation_performed'],False)

    def test_missing_unused_file_refuses_before_bootstrap(self):
        path=next(p for p in self.ops.contents if '/data/item' in p);del self.ops.contents[path]
        with patch.object(self.ops,'bootstrap',side_effect=AssertionError('bootstrap entered')),self.assertRaises(KeyError):self.execute()
        self.assertEqual(self.completion()['failed_stage'],'collection')
        self.assertEqual((self.ops.loader_calls,self.ops.callback_calls),(0,0))
        self.assertFalse((self.folder/'producer').exists())

    def test_callback_failure_preserves_partial_outputs_and_needs_review(self):
        def fail(op,AES):raise RuntimeError('invented callback')
        self.ops.callback_action=fail
        with self.assertRaisesRegex(RuntimeError,'invented callback'):self.execute()
        self.assertEqual(self.completion()['failed_stage'],'producer')
        self.assertEqual(self.ops.callback_calls,1)
        self.assertTrue((self.folder/'producer/raw.json').exists())
        self.assertFalse((self.folder/'producer/result.json').exists())
        self.assertIs(self.completion()['automatic_retry'],False)

    def test_unknown_saved_artifact_is_not_ignored(self):
        def extra(op,AES):(self.folder/'producer/extra.json').write_text('{}')
        self.ops.callback_action=extra
        with self.assertRaisesRegex(core.EvidenceError,'^artifact_roster$'):self.execute()
        self.assertEqual(self.completion()['failed_stage'],'verification')
        self.assertEqual(self.ops.callback_calls,1)

    def test_existing_attempt_is_not_overwritten(self):
        self.folder.mkdir();(self.folder/'sentinel').write_bytes(b'keep')
        with self.assertRaises(FileExistsError):self.execute()
        self.assertEqual((self.folder/'sentinel').read_bytes(),b'keep')
        self.assertEqual(self.ops.reads,[])

    def test_concrete_runtime_is_refused_without_output(self):
        with self.assertRaisesRegex(core.EvidenceError,'^real_activation_pending$'):
            subject.produce_collected_invented(inputs=self.inputs,ops=producer.RuntimeOps(),folder=self.folder)
        self.assertFalse(self.folder.exists())

    def test_invalid_deep_inputs_are_bounded_before_cloning_or_output(self):
        value=[]
        for _ in range(20):value=[value]
        self.inputs['expectation']['source_sha256']=value
        with patch.object(subject.copy,'deepcopy',side_effect=AssertionError('deepcopy entered')), \
             self.assertRaisesRegex(core.EvidenceError,'^bound$'):self.execute()
        self.assertFalse(self.folder.exists())

    def test_failure_completion_publication_retains_primary_exception(self):
        path=next(p for p in self.ops.contents if '/data/item' in p);del self.ops.contents[path]
        original=producer.Outputs.small;writes=[]
        def write(output,name,value):
            writes.append(name)
            if name=='completion.json':raise OSError('invented publication uncertainty')
            return original(output,name,value)
        with patch.object(producer.Outputs,'small',write),self.assertRaises(KeyError) as caught:self.execute()
        self.assertIsInstance(caught.exception.__cause__,OSError)
        self.assertEqual(writes.count('completion.json'),1)
        self.assertFalse((self.folder/'producer').exists())


if __name__=='__main__':unittest.main()
