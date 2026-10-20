"""Host-entry migration: invented data, lifecycle and saved-result boundaries."""
import base64
import copy
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace, ModuleType
import unittest
from unittest.mock import Mock, patch
from tools import dependency_host_entry as s


def owner(**changes):
    args=dict.fromkeys(('request','packet','buffers','receipts','contract','documents',
        'validated','fresh','gate','io','adapter_owner','adapter_buffers'),None)
    args.update(changes)
    return s.HostPreparation(**args)


def fixture():
    current=('dependency_launch_context','dependency_current_metadata','dependency_outer_metadata')
    ordinary={n:'a'*64 for n in ('basis','config')}
    packet=dict(adapter_request_sha256='b'*64,
        metadata=dict(comparison_context_seal_sha256='c'*64,current_ordinary_sha256=ordinary,
            expected_outer_receipts={'candidate':dict(sha256='d'*64)}),
        documents=dict(candidate=base64.b64encode(s.canonical(dict(repository_root='D:/invented/old'))).decode()))
    request=dict(operation_id='1'*32,sources={'current.'+n:dict(sha256='e'*64) for n in current})
    mr=dict(schema='invented_outer_metadata_binding_v1',operation_id=request['operation_id'],
        prepared_request_bytes_sha256=packet['adapter_request_sha256'],
        outer_original_sha256={'candidate':'d'*64},current_ordinary_sha256=ordinary,
        source_frames=dict(comparison_root='D:/invented/old',prepared_root=Path.cwd().as_posix()),
        comparison_context_seal_sha256='c'*64,checked_current_roles=sorted(ordinary),
        current_source_roles=46,unique_source_paths=41,camera_commands=[])
    mr.update(dict.fromkeys(('derived_closure_is_file','source_reads_observed','source_freshness_verified',
        'rights_established','actual_inputs_accessed','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed'),False))
    saved=dict(schema='invented_checked_public_metadata_result_v1',metadata_result=mr,
        checked_public_buffer_execution=True,public_source_count=3,
        source_hashes={n:'e'*64 for n in current},camera_commands=[])
    saved.update(dict.fromkeys(('interpreter_startup_verified','stdlib_origins_verified','validator_execution_owned',
        'actual_inputs_accessed','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed'),False))
    args=dict(request=request,packet=packet,contract=SimpleNamespace(CURRENT=current),prepared_repository_root=Path.cwd())
    return saved,args


class HostEntryTests(unittest.TestCase):
    def test_direct_cli_refuses_even_garbage_arguments(self):
        r=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8',s.__file__,'--activate'],capture_output=True,timeout=10)
        self.assertEqual((r.returncode,r.stdout,r.stderr),(2,b'',b''))

    def test_runtime_stays_disabled(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):s.run_runtime()

    def test_invented_scope_required_before_module_execution(self):
        x=owner(packet={'scope':'actual'})
        with patch.object(s,'_module',side_effect=AssertionError('must not load')):
            with self.assertRaisesRegex(ValueError,'invented_only'):x.prepare()
        self.assertTrue(x.closed)
        self.assertEqual(x.snapshot()['metadata_attempts'],0)

    def test_invented_manifest_and_constants_required_before_module_execution(self):
        for stage in ('manifest','constants'):
            v={'inputs':{'source_manifest':{'sha256':'0'*64},'prerequisites':{'constants_sha256':'0'*64}}}
            if stage=='constants':v['inputs']['source_manifest']['sha256']='b3ff4fd1ebb621f4c2be4b104e11b395ea315f1fbf580dd6b403bb2a091de541'
            x=owner(packet={'scope':'invented_only_no_operational_authority'},validated=v)
            with patch.object(s,'_module',side_effect=AssertionError('must not load')):
                with self.assertRaisesRegex(ValueError,'invented_'+('stream' if stage=='manifest' else 'constants')+'_only'):x.prepare()
            self.assertTrue(x.closed)

    def test_close_independent_after_first_baseexception_and_once_only(self):
        x=owner();calls=[]
        def child(name,error=None):
            o=SimpleNamespace(closed=False)
            def close():
                calls.append(name);o.closed=True
                if error:raise error
            o.close=close
            return x._track(o,name)
        primary=KeyboardInterrupt('current cleanup')
        x.metadata_owner=child('current',primary);x.comparison_owner=child('comparison')
        with self.assertRaises(KeyboardInterrupt) as caught:x.close()
        self.assertIs(caught.exception,primary)
        self.assertEqual(calls,['current','comparison'])
        self.assertFalse(x.close())
        self.assertEqual(x.close_attempts,dict(current=1,comparison=1))

    def test_prepare_preserves_primary_with_cleanup_cause_and_refuses_reentry(self):
        x=owner();primary=KeyboardInterrupt('prepare');cleanup=RuntimeError('cleanup')
        with patch.object(x,'_prepare',side_effect=primary),patch.object(x,'close',side_effect=cleanup) as close:
            with self.assertRaises(KeyboardInterrupt) as caught:x.prepare()
            self.assertIs(caught.exception,primary);self.assertIs(caught.exception.__cause__,cleanup)
            close.assert_called_once()
        with self.assertRaisesRegex(ValueError,'host_preparation_reentry'):x.prepare()

    def test_prepare_after_close_refuses(self):
        x=owner();self.assertTrue(x.close())
        with self.assertRaisesRegex(ValueError,'host_preparation_reentry'):x.prepare()

    def test_loader_internal_close_not_repeated(self):
        x=owner();o=SimpleNamespace(closed=False)
        def close():o.closed=True
        o.close=close;x.metadata_owner=x._track(o,'current')
        o.close();x.close()
        self.assertEqual(x.close_attempts['current'],1)

    def test_complete_saved_preflight_pure(self):
        saved,args=fixture();raw=s.canonical(saved)
        self.assertTrue(s.verify_saved_preflight(raw=raw,expected_sha256=s.sha(raw),**args))

    def test_rebound_digest_does_not_admit_changed_originals_or_authority(self):
        changes=(('comparison_context_seal_sha256','f'*64),('operation_id','2'*32),
            ('prepared_request_bytes_sha256','f'*64),('outer_original_sha256',{}),
            ('current_ordinary_sha256',{}),('source_frames',{}),('checked_current_roles',[]),
            ('current_source_roles',True),('unique_source_paths',40),('rights_established',True),
            ('source_reads_observed',True),('camera_commands',['invented command']),('extra',False))
        for name,value in changes:
            saved,args=fixture();saved['metadata_result'][name]=value;raw=s.canonical(saved)
            with self.subTest(name=name),self.assertRaises(ValueError):
                s.verify_saved_preflight(raw=raw,expected_sha256=s.sha(raw),**args)

    def test_wrapper_rebinding_does_not_admit_changed_source_or_authority(self):
        for name,value in (('source_hashes',{}),('public_source_count',True),('extra',False),
            ('stdlib_origins_verified',True),('execution_authorized',True),('camera_commands',['invented'])):
            saved,args=fixture();saved[name]=value;raw=s.canonical(saved)
            with self.subTest(name=name),self.assertRaises(ValueError):
                s.verify_saved_preflight(raw=raw,expected_sha256=s.sha(raw),**args)

    def test_saved_hash_drift_refuses(self):
        saved,args=fixture();raw=s.canonical(saved)
        with self.assertRaisesRegex(ValueError,'metadata_saved_result_hash'):
            s.verify_saved_preflight(raw=raw+b' ',expected_sha256=s.sha(raw),**args)

    def test_duplicate_and_overbound_saved_json_refuse(self):
        for raw,code in ((b'{"a":0,"a":1}','metadata_duplicate_key'),(b' '*(2*1024**2+1),'metadata_saved_bound')):
            with self.assertRaisesRegex(ValueError,code):s.strict_json(raw)

    def test_wire_bytes_duplicates_and_depth_bounds(self):
        self.assertEqual(s.unwire(['bytes',base64.b64encode(b'invented').decode()]),b'invented')
        with self.assertRaisesRegex(ValueError,'metadata_wire_key'):s.unwire(['dict',[['x',['scalar',1]],['x',['scalar',2]]]])
        raw=['scalar',1]
        for i in range(102):raw=['list',[raw]]
        with self.assertRaisesRegex(ValueError,'metadata_wire_bound'):s.unwire(raw)

    def test_parent_adapter_identity_mismatch_before_call(self):
        adapter=Mock()
        with self.assertRaisesRegex(ValueError,'adapter_parent_binding'):
            s.verify_child_completion(verifier=None,folder='invented',inputs={},operation_id='wrong',
                stdout=b'',stdout_sha256='0'*64,dependency_sha256={},bridge_sha256={},adapter_owner=adapter,
                adapter_request=dict(folder='invented',operation_id='1'*32),adapter_request_sha256='a'*64,
                adapter_buffers={},process={})
        adapter.call.assert_not_called()

    def test_bootstrap_aliases_removed_after_later_preparation_failure(self):
        x=owner();primary=KeyboardInterrupt('after bootstrap load')
        def prepare():
            for name in ('binding','control','factory'):
                module=ModuleType('_invented_host_'+name)
                x.bootstrap_modules[name]=module;sys.modules[module.__name__]=module
            raise primary
        with patch.object(x,'_prepare',side_effect=prepare):
            with self.assertRaises(KeyboardInterrupt) as caught:x.prepare()
            self.assertIs(caught.exception,primary)
        self.assertTrue(all(m.__name__ not in sys.modules for m in x.bootstrap_modules.values()))

    def test_bootstrap_foreign_alias_preserved_and_other_aliases_removed(self):
        x=owner();foreign=ModuleType('_invented_host_foreign')
        owned=ModuleType(foreign.__name__);other=ModuleType('_invented_host_other')
        x.bootstrap_modules=dict(binding=owned,control=other)
        sys.modules[owned.__name__]=foreign;sys.modules[other.__name__]=other
        try:
            with self.assertRaisesRegex(ValueError,'host_bootstrap_alias_ownership'):x.close()
            self.assertIs(sys.modules[owned.__name__],foreign)
            self.assertNotIn(other.__name__,sys.modules)
            self.assertFalse(x.close())
        finally:
            del sys.modules[owned.__name__]

    def test_real_preparation_failure_stages_release_every_published_bootstrap(self):
        for stage in ('binding','control','factory','plan','freeze','callbacks'):
            plan=dict(load_order=[],protected_order=[],execution_authorized=False,actual_binding_ready=False)
            binding=('def prepare_bindings(**kwargs):\n    return '+repr(plan)+'\n').encode()
            factory=b"class AuthoredSources:\n def __init__(self, adapter):pass\n def add(self,*args):pass\nclass ScopedCallbacks:\n def __init__(self,**kwargs):raise RuntimeError('invented callbacks')\n"
            buffers={'bootstrap:activation_binding':binding,'bootstrap:io_entry':b'pass\n',
                'integration:prospective_child':factory}
            names=dict(binding='bootstrap:activation_binding',control='bootstrap:io_entry',factory='integration:prospective_child')
            if stage in names:buffers[names[stage]]=b"raise RuntimeError('invented module')\n"
            sources={key:dict(path='D:/invented/'+str(i)+'.py',sha256=s.sha(raw)) for i,(key,raw) in enumerate(buffers.items())}
            inputs=dict(source_cache=dict(sources=sources),role_authority=dict(roles={}),
                prerequisites=dict(binding_input={}),binding_plan=copy.deepcopy(plan),
                binding_schema=dict(load_order=[],protected_order=[],aliases={}),basis={})
            if stage=='plan':inputs['binding_plan']['load_order']=['invented']
            v=dict(candidate=dict(repository_root='D:/invented'),inputs=inputs,effective_qualified_sources={})
            gate=SimpleNamespace(sha=s.sha,require=s.need,relative=lambda *args:None)
            io=SimpleNamespace(read_ordinary=lambda *args:None)
            x=owner()
            def prepare():return s._prepare_modules(v,buffers,gate,io,x.bootstrap_modules)
            freeze_error=RuntimeError('invented freeze') if stage=='freeze' else None
            with self.subTest(stage=stage),patch.object(x,'_prepare',side_effect=prepare),patch.object(s,'freeze_owned',side_effect=freeze_error):
                with self.assertRaises((ValueError,RuntimeError)):x.prepare()
                self.assertTrue(x.closed)
                self.assertTrue(all('_successor_'+n not in sys.modules for n in names))
