"""Invented transport/preflight; pending runtime child explicitly intercepted.

These cases do not qualify the entire retained supervisor/engine composition.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import types
from unittest.mock import patch, Mock

from tools import dependency_observation_launcher as s
from tools import dependency_observation_contract as c
from tools import dependency_operational_launcher as pending
from test_dependency_observation_legacy import fixture as legacy_fixture
from test_dependency_observation_contract import reseal,decided,change
from test_dependency_producer import refresh


def fixture(root,bootstrap=None):
    arguments=legacy_fixture();a=arguments['proposal_arguments'];sources=a['source_buffers']
    for role,name in (('host.launcher','dependency_operational_launcher'),
                      ('host.bootstrap_and_supervisor','dependency_child_entry'),
                      ('process_child','dependency_operational_child')):
        sources[role]=Path('tools',name+'.py').read_bytes()
    manifest=json.loads(a['ordinary_buffers']['authored_source_manifest'])
    rows={}
    for i,(role,raw) in enumerate(sorted(sources.items())):
        fixed={'adapter':'dependency_adapter_binding','adapter_scope':'dependency_operational_scope',
               'adapter_comparison':'dependency_outer_contract'}
        if role in fixed:
            path=Path.cwd()/'tools'/(fixed[role]+'.py')
            assert path.read_bytes()==raw
        else:
            path=root/('source'+str(i)+'.py');path.write_bytes(raw)
        manifest['sources'][role].update(path=path.relative_to(Path.cwd()).as_posix(),**c.receipt(raw))
        if role in pending.process.ROSTER:
            _,rows[role]=pending.entry.read_source(str(path))
    for role,row in manifest['prepared_sources'].items():
        source_role=c.PREPARED_PROCESS_ROLES[role]
        row.update(manifest['sources'][source_role])
    a['ordinary_buffers']['authored_source_manifest']=c.encoded(manifest)
    change(a,'authored_source_receipts',lambda v:v.update(receipts={n:c.receipt(b) for n,b in sources.items()}))
    dep=json.loads(a['ordinary_buffers']['dependency_packet'])['inputs']
    dep['expectation']['source_sha256']={n:c.sha(c.encoded(manifest['prepared_sources']) if r=='closure_manifest' else sources[r])
                                       for n,r in c.DEPENDENCY_SOURCE_ROLES.items()}
    refresh(dep)
    a['ordinary_buffers']['dependency_packet']=c.encoded(dict(schema='runtime_dependency_packet_v1',inputs=dep))
    fixed=json.loads(a['ordinary_buffers']['dependency_fixed'])
    fixed['expectation_sha256']=c.sha(c.encoded(dep['expectation']))
    a['ordinary_buffers']['dependency_fixed']=c.encoded(fixed)
    result=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',pending.PROFILE],capture_output=True,check=True,timeout=15)
    profile=json.loads(result.stdout)
    request=json.loads(a['request_bytes']);request['result_folder']=str(root/'review')
    a['request_bytes']=c.encoded(request)
    proposal=json.loads(a['proposal_bytes'])
    boot=s.bootstrap() if bootstrap is None else bootstrap
    proposal['runtime']=dict(interpreter=sys.executable,profile_sha256=s.sha(s.encoded(profile)),bootstrap=boot,
        argv=[sys.executable,'-I','-S','-B','-X','utf8','-c',boot,str(root/'review/request.json'),c.sha(a['request_bytes'])])
    a['proposal_bytes']=c.encoded(proposal)
    reseal(a)
    arguments.update({n:v for n,v in decided(a).items() if n not in a})
    arguments['runtime_expectation']=json.loads(a['proposal_bytes'])['runtime']
    arguments['capture_buffers'].update(sources)
    arguments['expected_capture_hashes']={n:c.sha(b) for n,b in arguments['capture_buffers'].items()}
    buffers=dict(arguments['capture_buffers']);buffers[s.ADDED]=Path('tools/dependency_observation_launcher.py').read_bytes()
    return dict(arguments=arguments,buffers=buffers,expected={n:c.sha(b) for n,b in buffers.items()},
        rows=rows,folder=root,repository_root=Path.cwd(),profile=profile)


def transport(value):
    result,packet=s.check(**value)
    root=value['folder'];root.joinpath('review').mkdir()
    lib=s.Library(value['buffers']).load()
    try:
        old=lib.pending
        bootstrap=old.bootstrap()
        pending_request=dict(schema='disabled_operational_outer_request_v1',operation_id=result['operation_id'],
            sources=value['rows'],packet=dict(path=str(root/'packet.json'),size=len(s.encoded(packet)),sha256=s.sha(s.encoded(packet))),folder=str(root),
            argv_prefix=[sys.executable,'-I','-S','-B','-X','utf8','-c',bootstrap],expected_runtime=value['profile'],
            bootstrap_sha256=s.sha(bootstrap.encode()),execution_authorized=False,camera_commands=[])
    finally:lib.close()
    body=s.build_transport(**value,pending_request=pending_request)
    core=value['arguments']['proposal_arguments']['request_bytes']
    (root/'review/request.json').write_bytes(core);(root/'review/transport.json').write_bytes(body)
    env=dict(os.environ);env[s.ENV]=s.sha(body)
    return body,env


def owned_harness(value,mode='complete',cleanup_failure=False,publication_failure=False):
    """Unit seams only: controller, process and reconciliation are invented."""
    events=[]
    class Owner:
        def __init__(self,name):self.name=name;self.closed=False
        def close(self):
            events.append('close:'+self.name);self.closed=True
            if self in sys.meta_path:sys.meta_path.remove(self)
            if cleanup_failure and self.name=='helpers':raise OSError('invented_cleanup')
            return True
    owners={n:Owner(n) for n in ('helpers','validation','bootstrap','adapter','outer')}
    core=value['arguments']['proposal_arguments']['request_bytes'];preflight=dict(operation_id='1'*32)
    raw=b'invented transport'
    context=dict(child_argv=['invented argv'],repository_root=Path.cwd())
    def supervise(*,context,records,spawn,**kwargs):
        spawn(context['child_argv'],Path.cwd())
        if mode=='supervisor_error':raise RuntimeError('invented_supervisor')
        return None,dict(process_observation=dict(launch_attempts=1,child_pids=[12345],child_exit_code=0,
            exit_observed=True,disposition='exited'),host_exit_code=0,terminal_records_agree=True)
    control=types.SimpleNamespace(reserve_parent=lambda **kw:Owner('records'),run_parent_reserved=supervise)
    oldplan=dict(owners,control=control)
    child=dict(schema='disabled_observation_child_v1',operation_id='1'*32,core_sha256=s.sha(core),transport_sha256=s.sha(raw),
        preflight=preflight,pending_child_completed=True,actual_runtime_verified=False,**dict.fromkeys(s.FALSE,False),camera_commands=[])
    def write(path,raw):
        events.append('publish')
        if publication_failure:raise PermissionError('invented_publication')
    def reconcile(*args):
        events.append('reconcile')
        if mode=='operation_error':raise ValueError('invented_reconcile')
        return {'invented_engine':True}
    old=types.SimpleNamespace(Records=pending.Records,entry=types.SimpleNamespace(read_source=lambda *args:(s.encoded(child),{})),
        write=write,_reconcile=reconcile)
    library=Owner('library');library.pending=old
    plan=dict(library=library,pending=oldplan,folder=value['folder'],preflight=preflight,
        core=core,transport=raw,context=context,environment={s.ENV:s.sha(raw)},started=False)
    return plan,events


class ObservationLauncherTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=Path.cwd()/'private')
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.a=fixture(self.root)

    def test_complete_capture_and_exact_pending_projection(self):
        result,packet=s.check(**self.a)
        self.assertEqual(len(self.a['buffers']),54)
        self.assertEqual(len(packet['ordinary']),14)
        self.assertTrue(result['retained_comparison_semantics_revalidated'])
        self.assertFalse(result['execution_authorized'])
        decoded=pending.process.decode_packet(packet)
        request=decoded[2];ordinary=decoded[4]
        for role in c.RETAINED:
            self.assertEqual(ordinary[role],self.a['arguments']['proposal_arguments']['ordinary_buffers'][role])
        self.assertEqual(set(request['sources']),set(c.PREPARED_PROCESS_ROLES))
        self.assertEqual(set(json.loads(ordinary['activity_rights'])['decisions'].values()),{'pending'})
        self.assertEqual(set(packet['documents']['inputs']),set(self.a['arguments']['legacy_documents']['inputs']))
        from test_dependency_operational_preparation import build_records
        docs,_,_,checked,_=pending.process.decode_packet(packet)
        outer={n:c.receipt(self.a['buffers'][role]) for n,role in pending.process.OUTER.items()}
        expected,originals=build_records(request,checked,docs,outer)
        self.assertEqual(ordinary,expected)
        self.assertEqual(packet['original_receipts'],originals)

    def test_same_count_capture_substitution_refuses_before_any_execution(self):
        buffers=dict(self.a['buffers']);expected=dict(self.a['expected'])
        buffers['invented.role']=buffers.pop('process_child')
        expected['invented.role']=expected.pop('process_child')
        with patch('builtins.exec',side_effect=AssertionError('executed')):
            with self.assertRaisesRegex(ValueError,'observation_launch_capture'):
                s.validate_capture(buffers,expected)

    def test_saved_transport_must_be_reconstructed_from_parent_checked_inputs(self):
        result,packet=s.check(**self.a)
        request={'invented':'frozen pending request'}
        raw=s.build_transport(**self.a,pending_request=request)
        old=types.SimpleNamespace(check_saved=Mock(),entry=types.SimpleNamespace(read_source=Mock()))
        plan=dict(self.a,library=types.SimpleNamespace(pending=old),pending=dict(packet=packet,request=request),
            preflight=result,transport=raw,core=self.a['arguments']['proposal_arguments']['request_bytes'],
            context=dict(child_argv=self.a['arguments']['runtime_expectation']['argv']),environment={s.ENV:s.sha(raw)})
        for kind in ('stale_packet','core','pending_request'):
            changed=dict(plan,pending=dict(plan['pending']))
            if kind=='stale_packet':
                parsed=s.strict(raw);parsed['inputs']['profile']['version_text']='substituted'
                changed['transport']=s.encoded(parsed)
                changed['environment']={s.ENV:s.sha(changed['transport'])}
            elif kind=='core':changed['core']=b'{}'
            else:changed['pending']['request']={'invented':'changed pending request'}
            with self.subTest(kind=kind),patch.object(s,'check',return_value=(result,packet)):
                with self.assertRaisesRegex(ValueError,'saved_transport_binding'):s.check_saved(changed)
        old.entry.read_source.assert_not_called()

    def test_prepare_attempts_all_cleanup_preserving_primary(self):
        events=[]
        class Owner:
            closed=False
            def __init__(self,name):self.name=name
            def close(self):
                events.append(self.name);self.closed=True
                if self.name=='helpers':raise OSError('invented helper close')
        fakeplan={n:Owner(n) for n in ('helpers','validation','bootstrap','adapter','outer')}
        fakeplan['request']={'expected_runtime':{}}
        old=types.SimpleNamespace(process=pending.process,_prepare_pending=Mock(return_value=fakeplan))
        class Lib:
            pending=old
            def load(self):return self
            def close(self):events.append('library');raise RuntimeError('invented library close')
        with patch.object(s,'Library',return_value=Lib()),patch.object(s,'check',return_value=({},{})):
            with self.assertRaisesRegex(ValueError,'prepared_profile') as caught:s.prepare(**self.a)
        self.assertIsInstance(caught.exception.__cause__,OSError)
        self.assertEqual(events,['helpers','validation','bootstrap','adapter','outer','library'])

    def test_supervisor_exception_retains_unknown_completion_without_retry(self):
        plan,events=owned_harness(self.a,mode='supervisor_error')
        with patch.object(s,'check_saved'),patch.object(s.subprocess,'Popen',return_value=types.SimpleNamespace(pid=12345)) as spawn:
            result=s.run_disabled(plan)
            self.assertEqual(spawn.call_count,1)
            with self.assertRaisesRegex(ValueError,'reentry'):s.run_disabled(plan)
        self.assertEqual(result['status'],'needs_review')
        self.assertEqual(result['process']['disposition'],'unknown_after_supervisor_exception')
        self.assertEqual(result['process']['child_pids'],[12345])
        self.assertFalse(result['process']['exit_observed'])
        self.assertNotIn('reconcile',events)
        self.assertTrue(result['library_closed'] and result['owners_closed'] and result['records_closed'])

    def test_publication_failure_preserves_primary_and_disposition(self):
        for mode,cleanup_failure,expected in (('operation_error',True,ValueError),('complete',True,OSError),
                                             ('complete',False,PermissionError)):
            plan,events=owned_harness(self.a,mode=mode,cleanup_failure=cleanup_failure,publication_failure=True)
            with self.subTest(mode=mode,cleanup=cleanup_failure),patch.object(s,'check_saved'),\
                    patch.object(s.subprocess,'Popen',return_value=types.SimpleNamespace(pid=12345)):
                with self.assertRaises(expected) as caught:s.run_disabled(plan)
            result=caught.exception.operational_disposition
            self.assertEqual(result['launch_attempts'],1)
            self.assertTrue(result['library_closed'] and result['owners_closed'])
            self.assertEqual(events[-1],'publish')
            if expected is not PermissionError:self.assertIsInstance(caught.exception.__cause__,PermissionError)

    def test_successful_owned_sequence_with_explicit_supervisor_and_engine_seams(self):
        plan,events=owned_harness(self.a)
        with patch.object(s,'check_saved') as check,patch.object(s.subprocess,'Popen',return_value=types.SimpleNamespace(pid=12345)) as spawn:
            result=s.run_disabled(plan)
        self.assertEqual(result['status'],'consistent_disabled_observation')
        self.assertEqual(check.call_count,2)
        self.assertEqual(spawn.call_count,1)
        self.assertIs(spawn.call_args.kwargs['shell'],False)
        self.assertEqual(spawn.call_args.kwargs['stdin'],subprocess.DEVNULL)
        self.assertIs(spawn.call_args.kwargs['env'],plan['environment'])
        self.assertTrue(all(result[n] for n in ('owners_closed','records_closed','library_closed')))
        self.assertEqual(events.count('reconcile'),1)
        self.assertEqual(len(events),len(set(events)))
        for n in s.FALSE:self.assertIs(result[n],False)

    def test_hash_cycle_is_avoided_by_separate_transport(self):
        boot=s.bootstrap()
        self.assertNotIn(self.a['arguments']['expected_external_anchor_sha256'],boot)
        core=self.a['arguments']['proposal_arguments']['request_bytes']
        argv=self.a['arguments']['runtime_expectation']['argv']
        self.assertEqual(argv[-1],s.sha(core))
        self.assertEqual(argv[-2],str(self.root/'review/request.json'))
        self.assertNotIn('transport_sha256',json.loads(core))

    def test_retained_bootstrap_is_identical_across_isolated_processes(self):
        command=[sys.executable,'-I','-S','-B','-X','utf8','-c',
            "import sys;sys.path.insert(0,"+repr(str(Path.cwd()))+");from tools import dependency_operational_launcher as p;print(p.sha(p.bootstrap().encode()))"]
        for _ in range(3):
            result=subprocess.run(command,capture_output=True,check=True,timeout=15)
            self.assertEqual(result.stdout.decode().strip(),s.sha(pending.bootstrap().encode()))

    def test_capture_and_row_changes_refuse(self):
        for kind in ('hash','roster','row','origin','profile','folder'):
            a=copy.deepcopy(self.a)
            if kind=='hash':a['buffers']['host.launcher']+=b'\n'
            elif kind=='roster':a['buffers'].pop('process_child')
            elif kind=='row':a['rows']['process_child']['sha256']='f'*64
            elif kind=='origin':a['rows']['process_child']['path']+= '.py'
            elif kind=='profile':a['profile']['version_text']+='changed'
            else:a['folder']=a['folder']/'other'
            with self.subTest(kind=kind),self.assertRaises(ValueError):s.check(**a)

    def test_reserved_environment_collision_refuses_before_source_work(self):
        with patch.dict(os.environ,{s.ENV:''}),patch.object(s,'check',side_effect=AssertionError('source')):
            with self.assertRaisesRegex(ValueError,'environment_collision'):s.prepare(**self.a)

    def test_wire_duplicate_nonfinite_and_tag_refusals(self):
        for raw in (b'{"a":1,"a":2}',b'{"a":NaN}'):
            with self.assertRaises(ValueError):s.strict(raw)
        for value in ({'$bytes':None},{'$bytes':'a','extra':True}):
            with self.assertRaises(ValueError):s.unwire(value)
        with self.assertRaises(ValueError):s.wire({'$bytes':'reserved'})
        value={'original':b'ordinary bytes','nested':[{'bytes':b'authored'}]}
        self.assertEqual(s.unwire(s.strict(s.encoded(s.wire(value)))),value)

    def test_public_runtime_and_cli_disabled(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):s.run_runtime()
        r=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','tools/dependency_observation_launcher.py','--activate'],capture_output=True,timeout=10)
        self.assertEqual((r.returncode,r.stdout,r.stderr),(2,b'',b''))

    def test_bootstrap_packet_and_environment_refuse_before_authored_execution(self):
        body,env=transport(self.a)
        argv=self.a['arguments']['runtime_expectation']['argv']
        for kind in ('missing','syntax','hash','core'):
            use=dict(env)
            command=list(argv)
            if kind=='missing':use.pop(s.ENV)
            elif kind=='syntax':use[s.ENV]='BAD'
            elif kind=='hash':use[s.ENV]='f'*64
            else:command[-1]='f'*64
            with self.subTest(kind=kind):
                r=subprocess.run(command,cwd=Path.cwd(),env=use,capture_output=True,timeout=15)
                self.assertEqual(r.returncode,2)
                self.assertFalse((self.root/'review/child-observation.json').exists())

    def test_bootstrap_launcher_crosscheck_precedes_authored_execution(self):
        body,env=transport(self.a)
        import base64
        for kind in ('buffer','expected'):
            doc=s.strict(body)
            # If this launcher were executed it would leave this sentinel.
            raw=("from pathlib import Path\nPath("+repr(str(self.root/'executed'))+").write_text('bad')\n").encode()
            doc['launcher']=dict(bytes=base64.b64encode(raw).decode(),sha256=s.sha(raw))
            if kind=='expected':doc['inputs']['buffers'][s.ADDED]={'$bytes':base64.b64encode(raw).decode()}
            changed=s.encoded(doc);(self.root/'review/transport.json').write_bytes(changed)
            env[s.ENV]=s.sha(changed)
            r=subprocess.run(self.a['arguments']['runtime_expectation']['argv'],cwd=Path.cwd(),env=env,
                capture_output=True,timeout=15)
            self.assertEqual(r.returncode,2)
            self.assertFalse((self.root/'executed').exists())

    def test_bootstrap_revalidates_source_file_before_launcher_execution(self):
        _,env=transport(self.a)
        source=Path(self.a['rows']['process_child']['path'])
        source.write_bytes(source.read_bytes()+b'\n# changed after capture\n')
        r=subprocess.run(self.a['arguments']['runtime_expectation']['argv'],cwd=Path.cwd(),env=env,
            capture_output=True,timeout=15)
        self.assertEqual(r.returncode,2)
        self.assertFalse((self.root/'review/child-observation.json').exists())

    def test_real_bootstrap_and_child_check_with_explicit_engine_substitution(self):
        boot=s.bootstrap()
        setup=""" original=worker.Library.load
 def load(self):
  result=original(self)
  def invented_child(request,packet,buffers,rows):
   with (Path(request['folder'])/'invented-engine.json').open('x') as stream:
    json.dump(dict(roles=len(buffers),argv_prefix=request['argv_prefix'],camera_commands=[]),stream)
   return 0
  result.pending.process.child=invented_child
  return result
 worker.Library.load=load
"""
        boot=boot.replace(' raise SystemExit(worker.child(',setup+' raise SystemExit(worker.child(')
        boot=boot.replace('except BaseException:\n print(',
            "except BaseException as error:\n print(type(error).__name__,str(error),file=sys.stderr)\n print(")
        # The exact substituted bootstrap is bound in the invented proposal.
        root=self.root/'positive';root.mkdir()
        value=fixture(root,bootstrap=boot)
        _,env=transport(value)
        r=subprocess.run(value['arguments']['runtime_expectation']['argv'],cwd=Path.cwd(),env=env,
            capture_output=True,timeout=30)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        observed=json.loads((root/'invented-engine.json').read_bytes())
        self.assertEqual(observed['roles'],49)
        self.assertEqual(observed['argv_prefix'],value['arguments']['runtime_expectation']['argv'][:-2])
        receipt=json.loads((root/'review/child-observation.json').read_bytes())
        self.assertFalse(receipt['execution_authorized'])
        self.assertFalse(receipt['actual_runtime_verified'])

    def test_library_does_not_publish_tools_aliases_and_closes_once(self):
        before=dict(sys.modules)
        lib=s.Library(self.a['buffers']).load()
        self.assertEqual(len(lib.modules),3)
        self.assertTrue(all(sys.modules[n] is m for n,m in before.items()))
        self.assertNotIn('_observation_tools',sys.modules)
        lib.close()
        self.assertFalse(lib.modules)
        with self.assertRaisesRegex(ValueError,'library_reclose'):lib.close()

    def test_library_executes_nested_captured_owner_graph_with_stdlib_imports(self):
        buffers=dict(self.a['buffers'])
        aliases=dict(namespace='dependency_successor_sources',successor_wiring='dependency_successor_wiring',
            host_entry='dependency_host_entry',operational_metadata='dependency_operational_metadata',
            operational_entry='dependency_operational_entry',operational_preparation='dependency_operational_preparation',
            adapter_loader='dependency_adapter_sources',outer_loader='dependency_operational_sources')
        for role,name in aliases.items():buffers[role]=Path('tools',name+'.py').read_bytes()
        buffers['ordinary_io']=Path('private/sessions/20261019-RA-003-parent-evidence-v5/outer/ordinary_io.py').read_bytes()
        for name in pending.process.DEPENDENCIES:
            buffers['dependency.'+name]=Path('tools',name+'.py').read_bytes()
        lib=s.Library(buffers).load();outer=adapter=helper=None
        before=dict(sys.modules)
        try:
            outer,adapter=lib.pending.process.owners(buffers)
            helper=lib.pending.process.helper_owner(outer,buffers,self.a['rows'],'parent')
            self.assertEqual(helper.mode,'parent')
            self.assertTrue(all(sys.modules.get(n) is m for n,m in before.items()))
            self.assertFalse(any(n.startswith('_a6700_successor') for n in sys.modules))
        finally:
            lib.pending.process.close_owned((helper,adapter,outer))
            lib.close()


if __name__=='__main__':unittest.main()
