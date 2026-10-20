"""Invented host launcher: pre-execution binding and lifecycle failures."""
import copy
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
from tools import dependency_host_launcher as s


def captured():
    raw=b'pass\n'
    buffers={n:raw for n in s.contract.SOURCE_ROLES}
    sources={n:dict(path='D:/invented/'+str(i)+'.py',size=len(raw),sha256=s.sha(raw)) for i,n in enumerate(sorted(buffers))}
    original={n.removeprefix('bound.'):raw for n in buffers if n.startswith('bound.')}
    rows={n:dict(path=sources['bound.'+n]['path'],bytes=len(raw),sha256=s.sha(raw)) for n in original}
    validated=dict(inputs=dict(source_cache=dict(sources=rows)),source_buffers=original)
    request=dict(sources=copy.deepcopy(sources))
    packet=dict(scope='invented_only_no_operational_authority',adapter_request=dict(sources={'invented':True}))
    deps={n:raw for n in s.contract.CHILD};deps['closure_manifest']=s.canonical(packet['adapter_request']['sources'])
    return dict(request=request,buffers=buffers,sources=sources,validated=validated,source_buffers=deps,packet=packet)


def launch(folder):
    packet=dict(scope='invented_only_no_operational_authority',adapter_request=dict(operation_id='1'*32))
    packet_path=folder/'packet.json';s.write(packet_path,s.canonical(packet))
    _,receipt=s.entry.read_source(str(packet_path))
    request=dict(folder=str(folder),operation_id='1'*32,packet=receipt,argv_prefix=['invented'])
    request_path=folder/'request.json';s.write(request_path,s.canonical(request))
    context=dict(operation_id='1'*32,repository_root=folder,session_dir=folder/'session',
        child_argv=request['argv_prefix']+[str(request_path),s.sha(s.canonical(request))])
    return dict(request=request,request_path=request_path,folder=folder,packet=packet,context=context,
        validated=dict(candidate=dict(operation_id='1'*32,repository_root=str(folder),session='session')))


class HostLauncherTests(unittest.TestCase):
    def test_direct_clis_and_runtime_refuse(self):
        for name in ('dependency_host_launcher','dependency_host_child','dependency_host_process_contract'):
            r=subprocess.run([sys.executable,'-I','-S','-B',str(Path('tools')/(name+'.py')),'--activate'],capture_output=True,timeout=10)
            self.assertEqual((r.returncode,r.stdout,r.stderr),(2,b'',b''))
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):s.run_runtime()

    def test_complete_captured_bytes_check(self):s.check_capture(**captured())

    def test_changed_buffers_refuse_before_any_bootstrap_execution(self):
        for name in ('bound.bootstrap:io_entry','namespace','successor_entry'):
            args=captured();args['buffers'][name]+=b'\n'
            with self.subTest(name=name),patch.object(s.contract,'validate_request'),patch.object(s.BootstrapOwner,'load',side_effect=AssertionError('executed')) as load:
                with self.assertRaisesRegex(ValueError,'parent_buffer_binding'):
                    s.prepare_parent(**args,gate=None,io=None,folder=None,request_path=None,context=None,
                        adapter_owner=None,adapter_buffers={},repository_root=None)
                load.assert_not_called()

    def test_rebound_receipts_cannot_replace_validated_retained_source(self):
        args=captured();name='bound.bootstrap:io_entry';raw=args['buffers'][name]+b'\n'
        args['buffers'][name]=raw
        args['sources'][name].update(size=len(raw),sha256=s.sha(raw))
        args['request']['sources']=copy.deepcopy(args['sources'])
        with self.assertRaisesRegex(ValueError,'parent_retained_binding'):s.check_capture(**args)

    def test_changed_roster_receipts_and_dependency_buffers_refuse(self):
        for mode in ('roster','receipts','dependency','closure'):
            args=captured()
            if mode=='roster':args['buffers'].pop('namespace')
            elif mode=='receipts':args['sources']['namespace']['sha256']='f'*64
            elif mode=='dependency':args['source_buffers'][s.contract.CHILD[0]]+=b'\n'
            else:args['source_buffers']['closure_manifest']=b'{}'
            with self.subTest(mode=mode),self.assertRaises(ValueError):s.check_capture(**args)

    def test_bad_capture_roster_refuses_before_creating_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'capture'
            with self.assertRaisesRegex(ValueError,'capture_named_roster'):
                s.capture_sources(named={'../outside':Path(tmp)},sourcefolder=target,validated={})
            self.assertFalse(target.exists())

    def test_retained_capture_drift_rejected_against_original_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);path=folder/'source.py';path.write_bytes(b'pass\n')
            named={n:path for n in s.contract.SOURCE_ROLES if not n.startswith('bound.')}
            v=dict(inputs=dict(source_cache=dict(sources={'bootstrap:io_entry':dict(path=str(path),bytes=4,sha256=s.sha(b'pass'))})),
                source_buffers={'bootstrap:io_entry':b'pass'})
            with self.assertRaisesRegex(ValueError,'capture_retained_changed'):
                s.capture_sources(named=named,sourcefolder=folder/'capture',validated=v)
            self.assertEqual(path.read_bytes(),b'pass\n')

    def test_launch_original_records_match(self):
        with tempfile.TemporaryDirectory() as tmp:s.check_launch(**launch(Path(tmp)))

    def test_packet_operation_paths_or_argv_substitution_refuses_before_spawn(self):
        for mode in ('packet','operation','folder','request_path','argv','root','session'):
            with tempfile.TemporaryDirectory() as tmp:
                args=launch(Path(tmp))
                if mode=='packet':args['packet']['extra']=True
                elif mode=='operation':args['context']['operation_id']='2'*32
                elif mode=='folder':args['folder']=Path(tmp)/'other'
                elif mode=='request_path':args['request_path']=Path(tmp)/'other.json'
                elif mode=='argv':args['context']['child_argv']=['unrelated-command']
                elif mode=='root':args['context']['repository_root']=Path(tmp)/'other'
                else:args['context']['session_dir']=Path(tmp)/'other'
                plan=dict(args,control=Mock(),validation_loader=Mock())
                with self.subTest(mode=mode),patch.object(s.contract,'validate_request'),patch.object(s.subprocess,'Popen',side_effect=AssertionError('spawn')) as spawn:
                    with self.assertRaises(ValueError):s.supervise(plan)
                    spawn.assert_not_called();plan['control'].reserve_parent.assert_not_called()

    def test_saved_request_and_packet_changes_refuse_before_spawn(self):
        for name in ('request.json','packet.json'):
            with tempfile.TemporaryDirectory() as tmp:
                args=launch(Path(tmp));path=Path(tmp)/name;path.write_bytes(path.read_bytes()+b' ')
                with self.subTest(name=name),patch.object(s.subprocess,'Popen',side_effect=AssertionError('spawn')):
                    with self.assertRaisesRegex(ValueError,'parent_saved_'):s.check_launch(**args)

    def test_parent_scope_refuses_before_request_write_or_profile(self):
        with patch.object(s,'write',side_effect=AssertionError('write')),patch.object(s.subprocess,'run',side_effect=AssertionError('process')):
            with self.assertRaisesRegex(ValueError,'invented_only'):
                s.prepare_request(folder=Path.cwd(),packet={'scope':'actual'},sources={},operation_id='',review_sha256='',context={})

    def test_reserve_interrupt_closes_unmounted_loader_once_no_process(self):
        with tempfile.TemporaryDirectory() as tmp:
            args=launch(Path(tmp));loader=SimpleNamespace(closed=False);calls=[]
            def close():calls.append('loader');loader.closed=True
            loader.close=close;primary=KeyboardInterrupt('invented reserve')
            control=Mock();control.reserve_parent.side_effect=primary
            plan=dict(args,control=control,validation_loader=loader)
            with patch.object(s.contract,'validate_request'),patch.object(s.subprocess,'Popen',side_effect=AssertionError('spawn')) as spawn:
                narrow,owned=s.supervise(plan)
            self.assertEqual(calls,['loader']);spawn.assert_not_called()
            self.assertEqual(owned['parent_failure_type'],'KeyboardInterrupt')
            self.assertFalse(owned['parent_loader_mount_attempted'])
            self.assertEqual(narrow['process_observation']['launch_attempts'],0)

    def test_reserve_primary_preserved_when_loader_cleanup_also_interrupts(self):
        with tempfile.TemporaryDirectory() as tmp:
            args=launch(Path(tmp));loader=SimpleNamespace(closed=False)
            def close():loader.closed=True;raise RuntimeError('cleanup')
            loader.close=Mock(side_effect=close)
            control=Mock();control.reserve_parent.side_effect=KeyboardInterrupt('reserve')
            with patch.object(s.contract,'validate_request'):
                narrow,owned=s.supervise(dict(args,control=control,validation_loader=loader))
            self.assertEqual(owned['parent_failure_type'],'KeyboardInterrupt');loader.close.assert_called_once()
            self.assertEqual(narrow['host_exit_code'],1)

    def test_bootstrap_ownership_cleanup_preserves_foreign_and_cleans_other(self):
        from types import ModuleType
        o=s.BootstrapOwner();foreign=ModuleType('_invented_parent_a');other=ModuleType('_invented_parent_b')
        o.modules={foreign.__name__:ModuleType(foreign.__name__),other.__name__:other}
        sys.modules[foreign.__name__]=foreign;sys.modules[other.__name__]=other
        try:
            with self.assertRaisesRegex(ValueError,'parent_bootstrap_ownership'):o.close()
            self.assertIs(sys.modules[foreign.__name__],foreign);self.assertNotIn(other.__name__,sys.modules)
            self.assertFalse(o.close())
        finally:del sys.modules[foreign.__name__]
