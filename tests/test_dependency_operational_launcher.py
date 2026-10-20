"""Invented source capture and intercepted supervisor boundaries only."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock,patch
from tools import dependency_operational_launcher as s


class LauncherTests(unittest.TestCase):
    def test_public_runtime_and_direct_clis_refuse(self):
        for name in ('dependency_operational_launcher','dependency_operational_child'):
            with self.subTest(name=name):
                r=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8',str(Path('tools',name+'.py')),'--activate'],capture_output=True,timeout=10)
                self.assertEqual((r.returncode,r.stdout,r.stderr),(2,b'',b''))
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):s.run_runtime()
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):s.process.run_runtime()

    def test_minimal_roster_excludes_old_fixture_and_comparison_graphs(self):
        self.assertEqual(len(s.process.ROSTER),49)
        self.assertEqual(len([n for n in s.process.ROSTER if n.startswith('bound.')]),29)
        self.assertNotIn('invented_fixture',s.process.ROSTER)
        self.assertNotIn('host_launcher',s.process.ROSTER)
        self.assertFalse(any(n.startswith(('metadata.','current.')) for n in s.process.ROSTER))

    def test_changed_roster_refuses_before_directory_or_source_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/'new'
            with patch.object(s.entry,'read_source',side_effect=AssertionError('read')):
                with self.assertRaisesRegex(ValueError,'operational_launch_roster'):
                    s.capture_sources(named={},sourcefolder=folder,validated={},expected_hashes={})
            self.assertFalse(folder.exists())

    def test_capture_checks_review_hash_before_writing_source_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);src=p/'source.py';src.write_bytes(b'pass\n')
            named={n:src for n in s.process.ROSTER};expected={n:'0'*64 for n in named}
            with self.assertRaisesRegex(ValueError,'operational_launch_source'):
                s.capture_sources(named=named,sourcefolder=p/'capture',validated={},expected_hashes=expected)
            self.assertEqual(list((p/'capture').iterdir()),[])

    def test_retained_source_rebinding_refuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);src=p/'source.py';src.write_bytes(b'pass\n')
            named={n:src for n in sorted(s.process.ROSTER)}
            expected={n:s.sha(src.read_bytes()) for n in named}
            rows={n.removeprefix('bound.'):dict(path=str(src),sha256='0'*64,bytes=5) for n in named if n.startswith('bound.')}
            validated=dict(inputs=dict(source_cache=dict(sources=rows)),source_buffers={k:b'pass\n' for k in rows})
            with self.assertRaisesRegex(ValueError,'operational_launch_retained'):
                s.capture_sources(named=named,sourcefolder=p/'capture',validated=validated,expected_hashes=expected)
            self.assertEqual(src.read_bytes(),b'pass\n')

    def test_capture_hash_and_size_rosters(self):
        buffers={n:b'pass\n' for n in s.process.ROSTER}
        rows={n:dict(path=str(Path.cwd()/(n+'.py')),size=5,sha256=s.sha(b'pass\n'),lstat=[],fstat=[]) for n in buffers}
        expected={n:r['sha256'] for n,r in rows.items()}
        s.validate_capture(buffers,rows,expected)
        for kind in ('buffer','size','hash','roster'):
            b=copy.deepcopy(buffers);r=copy.deepcopy(rows);e=dict(expected);key=next(iter(b))
            if kind=='buffer':b[key]+=b'\n'
            elif kind=='size':r[key]['size']+=1
            elif kind=='hash':e[key]='0'*64
            else:b.pop(key)
            with self.subTest(kind=kind),self.assertRaises(ValueError):s.validate_capture(b,r,e)

    def bootstrap_fixture(self,p):
        marker=p/'executed.txt'
        child=("from pathlib import Path\nPath("+repr(str(marker))+ ").write_text('entered')\ndef child(*a):return 0\n").encode()
        rows={}
        for i,n in enumerate(sorted(s.process.ROSTER)):
            path=p/(str(i)+'.py');path.write_bytes(child if n=='process_child' else b'pass\n')
            _,rows[n]=s.entry.read_source(str(path))
        packet=p/'packet.json';packet.write_bytes(b'{}');_,packetrow=s.entry.read_source(str(packet))
        profile=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',s.PROFILE],capture_output=True,check=True)
        request=dict(schema='disabled_operational_outer_request_v1',operation_id='1'*32,sources=rows,
            packet=packetrow,folder=str(p),expected_runtime=json.loads(profile.stdout),
            argv_prefix=[sys.executable,'-I','-S','-B','-X','utf8','-c',s.bootstrap()],
            bootstrap_sha256=s.sha(s.bootstrap().encode()),execution_authorized=False,camera_commands=[])
        return request,marker

    def test_unmodified_bootstrap_checks_before_executing_child(self):
        for kind in ('complete','source','packet','syntax','profile','authority','roster'):
            with tempfile.TemporaryDirectory() as tmp:
                p=Path(tmp);request,marker=self.bootstrap_fixture(p)
                if kind=='source':Path(request['sources']['adapter']['path']).write_bytes(b'changed\n')
                elif kind=='packet':(p/'packet.json').write_bytes(b'{"changed":1}')
                elif kind=='syntax':
                    path=Path(request['sources']['adapter']['path']);path.write_bytes(b'if broken\n')
                    _,request['sources']['adapter']=s.entry.read_source(str(path))
                elif kind=='profile':request['expected_runtime']['platform']='other'
                elif kind=='authority':request['execution_authorized']=True
                elif kind=='roster':request['sources'].pop('adapter')
                raw=s.encoded(request);(p/'request.json').write_bytes(raw)
                r=subprocess.run(request['argv_prefix']+[str(p/'request.json'),s.sha(raw)],capture_output=True,timeout=15)
                with self.subTest(kind=kind):
                    self.assertEqual(r.returncode,0 if kind=='complete' else 2)
                    self.assertEqual(marker.exists(),kind=='complete')

    def test_packet_duplicate_and_authority_shapes_refuse_without_observer(self):
        for raw in (b'{"a":1,"a":2}',b'{"a":NaN}'):
            with self.assertRaises(ValueError):s.process.strict(raw)
        for packet in ({},{'schema':'actual','ops':{}}):
            with self.assertRaisesRegex(ValueError,'operational_process_packet'):s.process.decode_packet(packet)

    def test_preparation_checks_capture_before_loading_any_source(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(s.process,'owners',side_effect=AssertionError('execute')) as owner:
            with self.assertRaisesRegex(ValueError,'operational_launch_roster'):
                s._prepare_pending(folder=Path(tmp),packet={},buffers={},rows={},expected_hashes={})
            owner.assert_not_called()

    def test_supervisor_reservation_interrupt_closes_loader_without_spawn(self):
        closed=[]
        loader=SimpleNamespace(closed=False)
        def close():loader.closed=True;closed.append('loader')
        loader.close=close
        control=Mock();control.reserve_parent.side_effect=KeyboardInterrupt('reserve')
        plan=dict(control=control,context={},validation=loader)
        with patch.object(s,'check_saved'),patch.object(s.subprocess,'Popen',side_effect=AssertionError('spawn')) as spawn:
            result,ownership=s._supervise(plan)
        spawn.assert_not_called();self.assertEqual(closed,['loader'])
        self.assertEqual(result['process_observation']['disposition'],'not_launched')
        self.assertEqual(ownership['failure_type'],'KeyboardInterrupt')

    def test_close_owners_does_not_let_one_failure_suppress_other_cleanup(self):
        one=SimpleNamespace(closed=False,close=Mock(side_effect=OSError('cleanup')))
        two=SimpleNamespace(closed=False,close=Mock())
        primary=KeyboardInterrupt('primary')
        with self.assertRaises(KeyboardInterrupt) as got:s.process.close_owned((one,two),primary)
        self.assertIs(got.exception,primary);one.close.assert_called_once();two.close.assert_called_once()

    def test_run_keeps_process_disposition_and_closes_all_on_reconcile_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan=dict(folder=Path(tmp))
            calls=[]
            for key in ('helpers','validation','bootstrap','adapter','outer'):
                owner=SimpleNamespace(closed=False)
                def close(owner=owner,key=key):owner.closed=True;calls.append(key)
                owner.close=close;plan[key]=owner
            narrow=dict(process_observation=dict(launch_attempts=1,exit_observed=True,child_exit_code=2))
            ownership=dict(failure_type=None,cleanup_failure_type=None,parent_records_closed=True,parent_validation_closed=True)
            with patch.object(s,'_supervise',return_value=(narrow,ownership)),patch.object(s,'_reconcile',side_effect=ValueError('refused')):
                r=s._run_pending(plan)
            self.assertEqual(r['status'],'needs_review');self.assertEqual(r['process'],narrow['process_observation'])
            self.assertEqual(calls,['helpers','validation','bootstrap','adapter','outer'])
            self.assertIs(r['automatic_retry'],False)

    def test_records_never_retries_unknown_close(self):
        records=s.Records();records.value=SimpleNamespace(close=Mock(side_effect=OSError('unknown')))
        with self.assertRaises(OSError):records.close()
        with self.assertRaisesRegex(ValueError,'records_reclose'):records.close()
        records.value.close.assert_called_once()

    def test_retained_binding_is_required_even_with_self_consistent_new_review_hashes(self):
        keys=[n for n in s.process.ROSTER if n.startswith('bound.')]
        buffers={n:b'pass\n' for n in keys};rows={n:dict(path=str(Path.cwd()/(n+'.py'))) for n in keys}
        cached={n.removeprefix('bound.'):dict(path=rows[n]['path'],bytes=5,sha256=s.sha(b'pass\n')) for n in keys}
        validated=dict(inputs=dict(source_cache=dict(sources=cached)),source_buffers={n.removeprefix('bound.'):b'pass\n' for n in keys})
        s.check_retained(validated,buffers,rows)
        for kind in ('bytes','origin'):
            b=dict(buffers);r=copy.deepcopy(rows);key='bound.bootstrap:io_entry'
            if kind=='bytes':b[key]+=b'\n'
            else:r[key]['path']+='changed.py'
            with self.subTest(kind=kind),self.assertRaisesRegex(ValueError,'operational_launch_retained'):s.check_retained(validated,b,r)

    def test_parent_partial_validation_loader_closes_once_preserving_interrupt(self):
        ordinary=[str(i) for i in range(23)];protected=['a','b','c'];raw=b'pass\n'
        rows={n:dict(path=n+'.py',sha256=s.sha(raw)) for n in ordinary+protected}
        v=dict(candidate=dict(repository_root=str(Path.cwd())),inputs=dict(binding_schema=dict(load_order=ordinary,protected_order=protected,aliases={n:n for n in rows}),role_authority=dict(roles=rows)),
            source_buffers={'role:'+n:raw for n in rows},effective_qualified_sources={n+'.py':s.sha(raw) for n in rows})
        primary=KeyboardInterrupt('add');loader=SimpleNamespace(add=Mock(side_effect=primary),close=Mock())
        factory=SimpleNamespace(AuthoredSources=Mock(return_value=loader));gate=SimpleNamespace(require=None,relative=None,sha=s.sha)
        with self.assertRaises(KeyboardInterrupt) as got:s.parent_validation_sources(v,gate,SimpleNamespace(read_ordinary=None),factory)
        self.assertIs(got.exception,primary);loader.close.assert_called_once()

    def test_publication_failure_preserves_primary_and_known_process(self):
        for error in (RuntimeError('reconcile'),KeyboardInterrupt('interrupted')):
            plan=dict(folder=Path.cwd())
            for n in ('helpers','validation','bootstrap','adapter','outer'):plan[n]=SimpleNamespace(closed=True)
            narrow=dict(process_observation=dict(launch_attempts=1,exit_observed=True,child_exit_code=0))
            with patch.object(s,'_supervise',return_value=(narrow,dict(failure_type=None,cleanup_failure_type=None,parent_records_closed=True,parent_validation_closed=True))),patch.object(s,'_reconcile',side_effect=error),patch.object(s,'write',side_effect=OSError('publication')) as write:
                with self.subTest(error=type(error).__name__),self.assertRaises(type(error)) as got:s._run_pending(plan)
                self.assertIs(got.exception,error);self.assertIsInstance(error.__cause__,OSError)
                self.assertEqual(error.operational_disposition['process'],narrow['process_observation']);write.assert_called_once()

    def test_retained_drift_refuses_before_parent_bootstrap_or_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            outer=SimpleNamespace(closed=False,close=Mock(),modules={'retained_gate':SimpleNamespace(validate_bundle=Mock(return_value={'candidate':{'operation_id':'1'*32}})),'ordinary_io':object(),'dependency_host_entry':object()})
            adapter=SimpleNamespace(closed=False,close=Mock())
            packet=dict.fromkeys(s.process.PACKET_FIELDS)
            packet.update(schema='pending_operational_outer_packet_v1',seal_sha256='0'*64,reference_pins={})
            decoded=({},b'{}',dict(operation_id='1'*32,folder=str(Path(tmp)/'composition')),{}, {})
            with patch.object(s,'validate_capture'),patch.object(s.process,'owners',return_value=(outer,adapter)),patch.object(s.process,'check_packet',return_value=decoded),patch.object(s,'check_retained',side_effect=ValueError('operational_launch_retained')),patch.object(s,'BootstrapOwner') as boot,patch.object(s,'write') as write,patch.object(s.subprocess,'run') as profile:
                with self.assertRaisesRegex(ValueError,'operational_launch_retained'):
                    s._prepare_pending(folder=Path(tmp),packet=packet,buffers={},rows={},expected_hashes={})
                boot.assert_not_called();write.assert_not_called();profile.assert_not_called()
                outer.close.assert_called_once();adapter.close.assert_called_once()

    def test_terminal_unknown_fields_and_wrong_digest_types_refuse_before_saved_reads(self):
        terminal=dict(schema='disabled_operational_outer_child_v1',operation_id='1'*32,
            status='complete_pending_composition',preflight_sha256='0'*64,request_sha256='1'*64,
            evidence=dict(dependency_sha256=dict.fromkeys(s.process.DEPENDENCY_ARTIFACTS,'2'*64),
                bridge_sha256=dict.fromkeys(('completion.json','controller-result.json'),'3'*64),stdout_sha256='4'*64),
            preparation_closed=True,helpers_closed=True,adapter_closed=True,callback_closed=True,
            execution_authorized=False,feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])
        for kind in ('extra_terminal','extra_evidence','extra_dependency','hash_type'):
            value=copy.deepcopy(terminal)
            if kind=='extra_terminal':value['authority_granted']=True
            elif kind=='extra_evidence':value['evidence']['authority_granted']=True
            elif kind=='extra_dependency':value['evidence']['dependency_sha256']['unexpected']='5'*64
            else:value['evidence']['stdout_sha256']=True
            control=SimpleNamespace(read_ordinary=Mock(side_effect=AssertionError('saved read')))
            plan=dict(folder=Path.cwd(),outer=object(),packet={'request_sha256':'1'*64},prepared={'operation_id':'1'*32},context={},control=control)
            narrow=dict(host_exit_code=0,terminal_records_agree=True)
            with self.subTest(kind=kind),patch.object(s,'check_saved'),patch.object(s.entry,'read_source',return_value=(s.encoded(value),{})):
                with self.assertRaises(ValueError):s._reconcile(plan,narrow)
                control.read_ordinary.assert_not_called()

if __name__=='__main__':unittest.main()
