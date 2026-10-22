"""Review-only preparation over invented files; no bootstrap/native execution."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import dependency_child_entry as subject


PRODUCER = b'''raise RuntimeError('invented producer must never execute')
TRUSTED = ('ctypes','_ctypes','ctypes.util','ctypes._endian','platform')
class RuntimeOps:
 def bootstrap(self):return {name:importlib.import_module(name) for name in TRUSTED}
'''


class BootstrapReviewTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.buffers = dict(entry=b"raise RuntimeError('invented entry must never execute')\n",
            core=b"raise RuntimeError('invented core must never execute')\n", producer=PRODUCER)
        self.receipts = {}
        for role, filename in subject.FILES.items():
            path = self.root / filename
            path.write_bytes(self.buffers[role])
            raw, self.receipts[role] = subject.read_source(str(path))
            self.assertEqual(raw, self.buffers[role])

    def prepare(self, **kwargs):
        return subject.prepare_bootstrap_review(buffers=self.buffers, receipts=self.receipts, **kwargs)

    def validate(self, packet):
        return subject.validate_bootstrap_review(packet=packet,buffers=self.buffers,receipts=self.receipts)

    def replace_producer(self, raw):
        path = Path(self.receipts['producer']['path']);path.write_bytes(raw)
        self.buffers['producer'],self.receipts['producer'] = subject.read_source(str(path))

    def test_complete_invented_capture_is_only_review_consistency(self):
        packet = self.prepare()
        self.assertEqual(self.validate(packet),'consistent_review_only')
        self.assertEqual(packet['status'],'prepared_not_launchable')
        self.assertEqual(len(packet['unresolved_current_bindings']),8)
        self.assertEqual(packet['entry_contract']['direct_imports'],
            ['ctypes','_ctypes','ctypes.util','ctypes._endian','platform'])
        self.assertFalse(packet['supervisor_reference']['called'])
        self.assertEqual(packet['camera_commands'],[])
        for key in ('execution_authorized','bootstrap_executed','native_loader_executed',
                    'actual_runtime_verified','feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(packet[key],False)

    def test_preparation_has_no_file_profile_or_process_effects(self):
        with patch.object(subject,'runtime_profile',side_effect=AssertionError('profile')), \
             patch.object(subject,'run_preflight',side_effect=AssertionError('supervisor')), \
             patch.object(subject,'read_source',side_effect=AssertionError('read')), \
             patch.object(subject.subprocess,'Popen',side_effect=AssertionError('process')), \
             patch.object(Path,'open',side_effect=AssertionError('open')):
            packet = self.prepare()
            self.assertEqual(self.validate(packet),'consistent_review_only')

    def test_source_roster_is_closed(self):
        for missing in (True,False):
            buffers = dict(self.buffers)
            if missing:buffers.pop('core')
            else:buffers['native']=b'not executable'
            with self.subTest(missing=missing),self.assertRaisesRegex(ValueError,'^bootstrap_review_roster$'):
                subject.prepare_bootstrap_review(buffers=buffers,receipts=self.receipts)

    def test_changed_source_bytes_cannot_use_previous_receipt(self):
        self.buffers['core']+=b'# changed\n'
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_source_binding$'):self.prepare()

    def test_declared_size_and_hash_require_exact_bytes(self):
        for field,value in (('size',True),('sha256','a'*64)):
            with self.subTest(field=field):
                rows=copy.deepcopy(self.receipts);rows['core'][field]=value
                with self.assertRaisesRegex(ValueError,'^bootstrap_review_source_binding$'):
                    subject.prepare_bootstrap_review(buffers=self.buffers,receipts=rows)

    def test_declared_source_identity_rejects_alias_or_cross_open_drift(self):
        for index,value in ((3,2),(4,0),(7,0x400),(1,self.receipts['core']['fstat'][1]+1)):
            rows=copy.deepcopy(self.receipts);rows['core']['fstat'][index]=value
            with self.subTest(index=index),self.assertRaisesRegex(ValueError,'^bootstrap_review_source_identity$'):
                subject.prepare_bootstrap_review(buffers=self.buffers,receipts=rows)

    def test_source_paths_require_absolute_correct_role_basename(self):
        for value in ('dependency_evidence.py',str(self.root/'wrong.py'),str(self.root/'..'/'dependency_evidence.py'),None):
            rows=copy.deepcopy(self.receipts);rows['core']['path']=value
            with self.subTest(value=value),self.assertRaisesRegex(ValueError,'^bootstrap_review_source_path$'):
                subject.prepare_bootstrap_review(buffers=self.buffers,receipts=rows)

    def test_reordered_direct_imports_are_not_original_contract(self):
        self.replace_producer(PRODUCER.replace(b"'ctypes','_ctypes'",b"'_ctypes','ctypes'"))
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_import_roster$'):self.prepare()

    def test_broadened_original_method_is_refused_without_execution(self):
        self.replace_producer(PRODUCER.replace(b'def bootstrap(self):return',
            b"def bootstrap(self):\n  raise RuntimeError('must not execute')\n  return"))
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_original_method$'):self.prepare()

    def test_missing_original_method_is_refused(self):
        self.replace_producer(PRODUCER.replace(b'def bootstrap(self)',b'def other(self)'))
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_original_method$'):self.prepare()

    def test_historical_reference_stays_a_declaration(self):
        refs=dict(package=dict(scope='historical_metadata',path=str(self.root/'package.json'),
            size=2,sha256=hashlib.sha256(b'{}').hexdigest()))
        packet=self.prepare(historical_refs=refs)
        self.assertEqual(self.validate(packet),'consistent_review_only')
        self.assertEqual(len(packet['unresolved_current_bindings']),8)
        self.assertTrue(packet['source_receipts_are_caller_declarations'])
        self.assertFalse(Path(refs['package']['path']).exists())
        refs['package']['sha256']='0'*64
        self.assertNotEqual(packet['historical_descriptor_refs'],refs)

    def test_historical_reference_cannot_be_promoted_or_embedded(self):
        for row in (dict(scope='current',path=str(self.root/'package.json'),size=2,sha256='a'*64),
                    dict(scope='historical_metadata',path=str(self.root/'package.json'),size=2,sha256='a'*64,contents='{}')):
            with self.subTest(row=row),self.assertRaisesRegex(ValueError,'^bootstrap_review_historical_scope$'):
                self.prepare(historical_refs={'package':row})

    def test_historical_references_have_closed_roster_and_distinct_paths(self):
        row=dict(scope='historical_metadata',path=str(self.root/'same.json'),size=2,sha256='a'*64)
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_historical_roster$'):
            self.prepare(historical_refs={'cache':row})
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_historical_path$'):
            self.prepare(historical_refs={'package':row,'expectation':row})

    def test_launch_fields_are_never_part_of_review_schema(self):
        for key,value in (('argv',['python']),('command','anything'),('callback','anything'),
                          ('collection',{'mode':'runtime'}),('expected_runtime',{})):
            packet=self.prepare();packet[key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'^bootstrap_review_changed$'):
                self.validate(packet)

    def test_stop_boundary_cannot_be_widened(self):
        for value in ('after_Cryptodome','after_CDLL_wrapper','after_producer','after_controller'):
            packet=self.prepare();packet['entry_contract']['stop']=value
            with self.subTest(value=value),self.assertRaisesRegex(ValueError,'^bootstrap_review_changed$'):
                self.validate(packet)

    def test_audit_profile_cannot_relax_limits_or_claim_observation(self):
        for key,value in (('event_limit',0),('maximum_attempts',2),('automatic_retry',True),
            ('optional_dlopen_arguments',[None,'kernel32','arbitrary.pyd']),('order_attested',True),
            ('other_native_events_resolved',True),('serialization','repr_any_object')):
            packet=self.prepare();packet['future_audit_proposal'][key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'^bootstrap_review_changed$'):
                self.validate(packet)

    def test_unresolved_bindings_and_false_effects_cannot_be_promoted(self):
        for key,value in (('unresolved_current_bindings',[]),('execution_authorized',True),
            ('actual_runtime_verified',True),('bootstrap_executed',True),('native_loader_executed',True),
            ('feature_supported',True),('recovery_proven',True),('device_write_gate_passed',True),
            ('camera_commands',['invented query'])):
            packet=self.prepare();packet[key]=value
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'^bootstrap_review_changed$'):
                self.validate(packet)

    def test_rehashing_tampered_saved_packet_does_not_make_it_valid(self):
        packet=self.prepare();packet['future_audit_proposal']['journal_bytes_limit']+=1
        raw=subject.canonical(packet)
        self.assertEqual(subject.sha(raw),hashlib.sha256(raw).hexdigest())
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_changed$'):
            self.validate(json.loads(raw))

    def test_validation_rechecks_supplied_source_binding(self):
        packet=self.prepare();self.buffers['core']+=b'# changed\n'
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_source_binding$'):self.validate(packet)

    def test_supervisor_refuses_review_before_any_output_or_process(self):
        packet=self.prepare();folder=self.root/'must-not-exist'
        with patch.object(subject.subprocess,'Popen',side_effect=AssertionError('process')) as start, \
             patch.object(subject,'canonical',side_effect=AssertionError('serialization')), \
             patch.object(Path,'mkdir',side_effect=AssertionError('mkdir')), \
             self.assertRaisesRegex(ValueError,'^bootstrap_review_not_executable$'):
            subject.run_preflight(request=packet,folder=folder)
        start.assert_not_called();self.assertFalse(folder.exists())

    def test_supervisor_refusal_precedes_forged_authority_and_invalid_timeout(self):
        packet=self.prepare();packet['execution_authorized']=True
        with patch.object(subject.subprocess,'Popen',side_effect=AssertionError('process')), \
             patch.object(Path,'mkdir',side_effect=AssertionError('mkdir')), \
             self.assertRaisesRegex(ValueError,'^bootstrap_review_not_executable$'):
            subject.run_preflight(request=packet,folder=self.root/'absent',timeout=-1)

    def test_source_and_packet_bounds_are_checked(self):
        buffers=dict(self.buffers);buffers['core']=b'x'*(2*1024**2+1)
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_source_bound$'):
            subject.prepare_bootstrap_review(buffers=buffers,receipts=self.receipts)
        packet=self.prepare();packet['extra']='x'*65536
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_bound$'):self.validate(packet)

    def test_other_request_schema_is_not_a_bootstrap_review(self):
        packet=self.prepare();packet['schema']='dependency_child_collection_request_v1'
        with self.assertRaisesRegex(ValueError,'^bootstrap_review_schema$'):self.validate(packet)


if __name__=='__main__':unittest.main()
