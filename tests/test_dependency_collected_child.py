"""Exact-buffer collected children; all dependency bytes/loads are invented.

Valid runtime packets are never launched. Runtime grammar/engine seams below use
explicitly invented data or mocked construction, not installed observations.
"""
import copy
import contextlib
import inspect
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from tools import dependency_child_entry as entry
from tools import dependency_execution as execution
from tools import dependency_invented as invented
from tools import dependency_package_preflight as collector
from tools import dependency_producer as producer
from tools import dependency_evidence as core
from test_dependency_package_preflight import complete_fixture


class CollectedChildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        code='import sys,json\n'+inspect.getsource(entry.runtime_profile)+'\nprint(json.dumps(runtime_profile()))'
        run=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',code],capture_output=True,text=True,timeout=15)
        if run.returncode:raise AssertionError(run.stderr)
        cls.profile=json.loads(run.stdout)

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'authored';self.root.mkdir()
        self.names=dict(entry.COLLECTION_FILES,invented='dependency_invented.py')
        for name in self.names.values():shutil.copyfile(Path(entry.__file__).parent/name,self.root/name)
        self.buffers={k:(self.root/v).read_bytes() for k,v in self.names.items()}
        self.data,self.ops=complete_fixture()
        self.value=invented.packet(self.data,self.ops,self.buffers,'c'*64)
        self.fixed=invented.expectations(self.value)
        self.path=Path(self.temp.name)/'invented-input.json';self.folder=Path(self.temp.name)/'attempt'

    def freeze(self):
        raw=entry.canonical(self.value);self.path.write_bytes(raw)
        return entry.freeze_collection(source_root=self.root,expected_runtime=self.profile,
            review_sha256='c'*64,packet_path=self.path,packet_sha256=entry.sha(raw),fixed=self.fixed,mode='invented')

    def run_child(self,request,**kwargs):return entry.run_preflight(request=request,folder=self.folder,**kwargs)

    def assert_refused(self,request,*,no_outputs=True):
        value=self.run_child(request)
        self.assertEqual(value['status'],'needs_review');self.assertIsNone(value['result'])
        if no_outputs:self.assertFalse((self.folder/'collected').exists())
        return value

    def sentinel(self):
        marker=Path(self.temp.name)/'entry-ran'
        with (self.root/self.names['entry']).open('a',encoding='utf-8') as out:out.write('\nPath('+repr(str(marker))+').write_text("unexpected")\n')
        return marker

    def test_complete_six_buffer_child_and_parent_saved_verification(self):
        request=self.freeze();before=copy.deepcopy(request);value=self.run_child(request)
        self.assertEqual(request,before)
        self.assertEqual((value['status'],value['termination'],value['exit_code']),('invented_collected_child_complete','reaped',0))
        result=value['result'];self.assertEqual(len(result['source_sha256']),6)
        self.assertEqual(len(result['artifact_sha256']),11)
        self.assertIs(result['test_injection_used'],True)
        for name in ('actual_dependency_observation_performed','installed_dependency_bootstrap_performed',
                     'execution_authorized','parent_execution_authenticated','prior_review_proven','feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(result[name],False)
        collection=json.loads((self.folder/'collected/collection.json').read_bytes())
        self.assertEqual((collection['package_reads'],collection['trusted_reads']),(351,5))
        data,_=invented.unpack(self.value,self.fixed,self.buffers,'c'*64,complete=True)
        self.assertEqual(execution.validate_saved_composition(self.folder/'collected',data,invented=True),result['artifact_sha256'])

    def test_collector_substitution_refuses_before_entry(self):
        marker=self.sentinel();request=self.freeze()
        with (self.root/self.names['collector']).open('ab') as out:out.write(b'\n# changed\n')
        self.assert_refused(request);self.assertFalse(marker.exists())

    def test_execution_substitution_refuses_before_entry(self):
        marker=self.sentinel();request=self.freeze()
        with (self.root/self.names['execution']).open('ab') as out:out.write(b'\n# changed\n')
        self.assert_refused(request);self.assertFalse(marker.exists())

    def test_packet_substitution_refuses_before_entry(self):
        marker=self.sentinel();request=self.freeze()
        with self.path.open('ab') as out:out.write(b' ')
        self.assert_refused(request);self.assertFalse(marker.exists())

    def test_runtime_optimization_refuses_before_entry(self):
        marker=self.sentinel();request=self.freeze();request['expected_runtime']['optimize']=1
        self.assert_refused(request);self.assertFalse(marker.exists())

    def test_missing_source_role_refuses(self):
        request=self.freeze();del request['sources']['collector'];self.assert_refused(request)

    def test_extra_source_role_refuses(self):
        request=self.freeze();request['sources']['unexpected']=request['sources']['collector'];self.assert_refused(request)

    def test_fixed_original_policy_substitution_refuses(self):
        self.fixed['expectation_sha256']='0'*64;self.assert_refused(self.freeze())

    def test_fixed_package_substitution_refuses(self):
        self.fixed['package_sha256']='0'*64;self.assert_refused(self.freeze())

    def test_fixed_root_substitution_refuses(self):
        self.fixed['root_sha256']['package']='0'*64;self.assert_refused(self.freeze())

    def test_missing_unused_invented_file_has_no_filesystem_fallback(self):
        path=next(p for p in self.value['contents'] if '/data/item' in p)
        del self.value['contents'][path];self.assert_refused(self.freeze())

    def test_changed_unused_bytes_refuse(self):
        path=next(p for p in self.value['contents'] if '/data/item' in p)
        self.value['contents'][path]='00';self.assert_refused(self.freeze())

    def test_review_binding_substitution_refuses(self):
        self.value['inputs']['binding']['review_sha256']='b'*64;self.assert_refused(self.freeze())

    def test_declared_source_hash_must_match_exact_child_buffers(self):
        self.value['inputs']['expectation']['source_sha256']['execution']='0'*64
        self.value['inputs']['binding']['expectation_sha256']=core._hash(self.value['inputs']['expectation'])
        self.fixed=invented.expectations(self.value);self.assert_refused(self.freeze())

    def test_unknown_collection_mode_refuses_before_authored_entry(self):
        request=self.freeze();request['collection']['mode']='other';self.assert_refused(request)

    def test_runtime_mode_cannot_accept_invented_packet(self):
        request=self.freeze();request['collection']['mode']='runtime';del request['sources']['invented']
        self.assert_refused(request)

    def test_preloaded_trusted_origin_refuses_before_observation(self):
        # Qualification helper runs after all sources are checked; it must not
        # bootstrap a preloaded trusted module into a successful observation.
        with (self.root/self.names['producer']).open('a',encoding='utf-8') as out:out.write('\nimport platform\n')
        self.buffers={k:(self.root/v).read_bytes() for k,v in self.names.items()}
        self.value=invented.packet(self.data,self.ops,self.buffers,'c'*64);self.fixed=invented.expectations(self.value)
        self.assert_refused(self.freeze())

    def after_wait(self, action):
        original=entry.subprocess.Popen
        class Process:
            def __init__(self,*a,**kw):self.process=original(*a,**kw);self.pid=self.process.pid
            def wait(self,*a,**kw):
                result=self.process.wait(*a,**kw)
                if result==0:action()
                return result
            def kill(self):return self.process.kill()
        return patch.object(entry.subprocess,'Popen',Process)

    def tamper(self,relative,change):
        request=self.freeze()
        def action():
            path=self.folder/'collected'/relative;value=json.loads(path.read_bytes());change(value)
            raw=entry.canonical(value);path.write_bytes(raw)
            stdout=self.folder/'stdout.json';result=json.loads(stdout.read_bytes())
            result['artifact_sha256'][relative]=entry.sha(raw);stdout.write_bytes(entry.canonical(result))
        with self.after_wait(action):self.assert_refused(request,no_outputs=False)

    def test_parent_rejects_rebound_collection_original_hash(self):
        self.tamper('collection.json',lambda row:row.update(prior_package_sha256='0'*64))

    def test_parent_recomputes_transition(self):
        self.tamper('transition.json',lambda row:row.update(review_sha256='0'*64))

    def test_parent_recomputes_verification_flags(self):
        self.tamper('verification.json',lambda row:row.update(actual_runtime_verified=True))

    def test_parent_recomputes_completion(self):
        self.tamper('completion.json',lambda row:row.update(actual_dependency_observation_performed=True))

    def test_parent_rejects_unknown_result_fields(self):
        self.tamper('producer/result.json',lambda row:row.update(unreviewed=True))

    def test_parent_rechecks_source_after_child(self):
        request=self.freeze()
        def change():
            with (self.root/self.names['collector']).open('ab') as out:out.write(b'\n# changed\n')
        with self.after_wait(change):self.assert_refused(request,no_outputs=False)

    def test_parent_rechecks_packet_after_child(self):
        request=self.freeze()
        def change():
            with self.path.open('ab') as out:out.write(b' ')
        with self.after_wait(change):self.assert_refused(request,no_outputs=False)

    def test_parent_rejects_extra_outer_artifact(self):
        request=self.freeze()
        with self.after_wait(lambda:(self.folder/'collected/extra.json').write_bytes(b'{}')):
            self.assert_refused(request,no_outputs=False)

    def test_parent_rejects_extra_producer_artifact(self):
        request=self.freeze()
        with self.after_wait(lambda:(self.folder/'collected/producer/extra.json').write_bytes(b'{}')):
            self.assert_refused(request,no_outputs=False)

    def test_parent_interruption_records_known_child_completion_without_replay(self):
        request=self.freeze();original=entry.subprocess.Popen
        with patch.object(entry.subprocess,'Popen',wraps=original) as spawn,patch.object(
                execution,'validate_saved_composition',side_effect=KeyboardInterrupt('invented interruption')):
            result=self.run_child(request)
        self.assertEqual(spawn.call_count,1)
        self.assertEqual((result['status'],result['termination'],result['exit_code']),('needs_review','reaped',0))
        self.assertIsNone(result['result']);self.assertIs(result['automatic_retry'],False)
        saved=json.loads((self.folder/'completion.json').read_bytes())
        self.assertEqual(saved,result)

    def test_timeout_is_reaped_without_restart(self):
        with (self.root/self.names['execution']).open('a',encoding='utf-8') as out:out.write('\nimport time\ntime.sleep(3)\n')
        self.buffers={k:(self.root/v).read_bytes() for k,v in self.names.items()}
        self.value=invented.packet(self.data,self.ops,self.buffers,'c'*64);self.fixed=invented.expectations(self.value)
        original=entry.subprocess.Popen
        with patch.object(entry.subprocess,'Popen',wraps=original) as spawn:
            result=self.run_child(self.freeze(),timeout=0.1)
        self.assertEqual(spawn.call_count,1);self.assertEqual(result['status'],'needs_review')
        self.assertEqual(result['termination'],'terminated_after_timeout');self.assertIs(result['automatic_retry'],False)

    def test_uncertain_kill_wait_is_not_retried(self):
        class Process:
            pid=12345
            def wait(self,timeout):raise subprocess.TimeoutExpired('invented',timeout)
            def kill(self):raise OSError('invented uncertain termination')
        with patch.object(entry.subprocess,'Popen',return_value=Process()) as spawn:
            result=self.run_child(self.freeze())
        self.assertEqual(spawn.call_count,1);self.assertEqual(result['status'],'needs_review')
        self.assertEqual(result['termination'],'needs_process_reconciliation')

    def test_existing_attempt_is_not_overwritten_or_launched(self):
        request=self.freeze();self.folder.mkdir();(self.folder/'sentinel').write_bytes(b'keep')
        with patch.object(entry.subprocess,'Popen') as spawn,self.assertRaises(FileExistsError):self.run_child(request)
        spawn.assert_not_called();self.assertEqual((self.folder/'sentinel').read_bytes(),b'keep')


class RuntimeGrammarTests(unittest.TestCase):
    def setUp(self):
        self.data,self.ops=complete_fixture();self.sources=self.data['source_buffers']
        inputs={k:v for k,v in self.data.items() if k!='source_buffers'}
        self.value=dict(schema='runtime_dependency_packet_v1',inputs=inputs)
        self.fixed=dict(expectation_sha256=core._hash(inputs['expectation']),package_sha256=core._hash(inputs['package']),
            root_sha256={k:r['identity_sha256'] for k,r in inputs['expectation']['roots'].items()})

    def bind(self):return execution.bind_runtime_packet(self.value,self.fixed,self.sources,'b'*64)

    @contextlib.contextmanager
    def modeled_runtime(self):
        flags=types.SimpleNamespace(isolated=1,no_site=1,no_user_site=1,optimize=0)
        with patch.object(producer.os,'name','nt'),patch.object(producer.sys,'implementation',types.SimpleNamespace(name='cpython')),patch.object(
                producer.sys,'flags',flags),patch.object(producer.sys,'dont_write_bytecode',True),patch.object(producer.sys,'modules',{}):
            yield

    def test_closed_packet_grammar_only_never_reads_installed_files(self):
        with patch.object(producer.RuntimeOps,'reader',side_effect=AssertionError('actual read')):
            result=self.bind()
        producer.bind_inputs(**result)

    def test_simulated_bytes_are_not_permitted_in_runtime_packet(self):
        self.value['contents']={}
        with self.assertRaisesRegex(core.EvidenceError,'^shape$'):self.bind()

    def test_runtime_packet_cannot_supply_ops_or_callback(self):
        self.value['inputs']['ops']={}
        with self.assertRaisesRegex(core.EvidenceError,'^shape$'):self.bind()

    def test_substituted_fixed_policy_refuses(self):
        self.fixed['expectation_sha256']='0'*64
        with self.assertRaisesRegex(core.EvidenceError,'^fixed_expectations$'):self.bind()

    def test_bound_runtime_packet_detaches_mutable_input_groups(self):
        result=self.bind();before=copy.deepcopy(result)
        self.value['inputs']['expectation']['operation_id']='changed'
        self.value['inputs']['package']['manifest']['version']='changed'
        self.value['inputs']['binding']['review_sha256']='0'*64
        self.sources.clear()
        self.assertEqual(result,before)

    def test_mutating_bound_runtime_packet_does_not_change_caller(self):
        before=copy.deepcopy((self.value,self.sources));result=self.bind()
        result['expectation']['operation_id']='changed'
        result['package']['manifest']['version']='changed'
        result['binding']['review_sha256']='0'*64
        result['source_buffers'].clear()
        self.assertEqual((self.value,self.sources),before)

    def test_saved_verifier_rejects_non_boolean_mode_before_read(self):
        with patch.object(producer,'read_verified',side_effect=AssertionError('unexpected read')):
            with self.assertRaisesRegex(core.EvidenceError,'^collection_mode$'):
                execution.validate_saved_composition('unused',self.data,invented=1)

    def test_review_substitution_refuses(self):
        self.value['inputs']['binding']['review_sha256']='c'*64
        with self.assertRaisesRegex(core.EvidenceError,'^review_binding$'):self.bind()

    def test_runtime_api_constructs_only_concrete_ops_without_execution(self):
        # Empty modeled module roster: no installed module imported or removed.
        with self.modeled_runtime(),patch.object(execution,'_produce_collected',return_value='not executed') as run:
            value=execution.produce_collected_runtime(inputs=self.data,folder='unused')
        self.assertEqual(value,'not executed');self.assertIs(type(run.call_args.kwargs['ops']),producer.RuntimeOps)
        self.assertIs(run.call_args.kwargs['invented'],False)

    def test_unsupported_runtime_refuses_before_ops_or_outputs(self):
        for change in ('platform','implementation','flags','preloaded'):
            with self.subTest(change=change),self.modeled_runtime(),patch.object(producer,'RuntimeOps') as ops,patch.object(
                    execution,'_produce_collected') as run:
                if change=='platform':context=patch.object(producer.os,'name','posix')
                elif change=='implementation':context=patch.object(producer.sys,'implementation',types.SimpleNamespace(name='other'))
                elif change=='flags':context=patch.object(producer.sys,'flags',types.SimpleNamespace(isolated=0))
                else:context=patch.object(producer.sys,'modules',{'platform':object()})
                with context,self.assertRaises(core.EvidenceError):
                    execution.produce_collected_runtime(inputs=self.data,folder='unused')
                ops.assert_not_called();run.assert_not_called()

    def test_actual_collection_grammar_with_invented_reader(self):
        value=collector._collect(ops=self.ops,inputs=self.data,invented=False)
        self.assertEqual(value['evidence_mode'],'saved_records')
        data,transition=execution.bind_collection(collection=value,inputs=self.data,evidence_mode='saved_records',test_injection_used=False)
        self.assertIs(transition['test_injection_used'],False);producer.bind_inputs(**data)
        with self.assertRaisesRegex(core.EvidenceError,'^collection_mode$'):
            execution.bind_collection(collection=value,inputs=self.data)

    def test_shared_runtime_record_engine_with_explicitly_simulated_ops(self):
        helper=types.ModuleType(invented.HELPER);helper.new=self.ops.new
        with tempfile.TemporaryDirectory() as directory,patch.dict(sys.modules,{invented.HELPER:helper,'ctypes':self.ops.modules['ctypes']}):
            folder=Path(directory)/'synthetic-runtime-grammar'
            result=execution._produce_collected(inputs=self.data,ops=self.ops,folder=folder,invented=False)
            self.assertEqual(result['status'],'complete_dependency_composition')
            self.assertEqual(len(execution.validate_saved_composition(folder,self.data,invented=False)),11)
            self.assertEqual((self.ops.loader_calls,self.ops.callback_calls),(5,1))
        # Source/data/ops remain invented. Nominal record flags prove no truth.
        self.assertIs(result['execution_authorized'],False)


if __name__=='__main__':unittest.main()
