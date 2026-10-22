"""Genuine child preparation/callback/collection over invented I/O and crypto.

Unlike the earlier replay join, every terminal and dependency output is absent
before launch and is generated in the isolated child. Exact retained factory,
control, engine and parent remain intact. Captured synthetic IoAdapter/wiring
replace protected source I/O and installed dependencies; records retain the
invented=True grammar. No actual runtime or producer authentication is claimed.
"""
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from tools import dependency_operational_launcher as parent
from dependency_terminal_fixture import FreshTerminal
from dependency_child_fixture import synthetic_io_adapter_source
from dependency_child_runtime_fixture import wiring_source
import test_dependency_joined_handoff as joined
import test_dependency_parent_handoff as supervised
from test_dependency_isolated_handoff import DISK_IO

CHILD_IO=DISK_IO+b'''
def write_new(path,value):
 import json
 raw=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
 with Path(path).open('xb') as stream:
  stream.write(raw);stream.flush();os.fsync(stream.fileno())
 return {'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
'''

RELEASE_INTERRUPT=rb'''
_synthetic_original_dispatch=_dispatch_runtime
def _dispatch_runtime(**kw):
 release=kw['release_callbacks_after_controller']
 def release_once():
  release()
  raise OSError('invented release completion interruption')
 kw['release_callbacks_after_controller']=release_once
 return _synthetic_original_dispatch(**kw)
'''


CHILD_SUFFIX=rb'''
def child(request,packet,buffers,rows):
 import os
 owned=None;answer=None;primary=None;cleanup=None
 root=Path(packet['repository_root']);refresh=[]
 observed=dict(pid=os.getpid(),isolated=sys.flags.isolated,no_site=sys.flags.no_site,
  no_user_site=sys.flags.no_user_site,no_bytecode=sys.dont_write_bytecode,optimize=sys.flags.optimize)
 def audit(event,args):
  if event=='a6700.synthetic.refresh_read':refresh.append(list(args))
  if event.startswith(('socket.','ctypes.')) or event=='subprocess.Popen':
   raise AssertionError('invented child forbids network/native/subprocess')
  if event=='import' and args[0].split('.')[0] in ('ctypes','_ctypes','Crypto','cffi','_cffi_backend'):
   raise AssertionError('invented child forbids installed dependency import')
  if event=='open' and isinstance(args[0],str):
   path=Path(args[0])
   assert path.is_relative_to(root) or path.is_relative_to(Path(sys.base_prefix)),'outside invented tree/stdlib'
 sys.addaudithook(audit)
 try:
  owned=prepare_synthetic_owned(request=request,packet=packet,buffers=buffers,rows=rows,
   request_bytes=encoded(request),expected_request_sha256=sys.argv[2],request_path=sys.argv[1])
  if SYNTHETIC_MODE=='refresh_drift':
   Path(rows['bound.role:acceptance']['path']).write_bytes(b'# explicit invented source drift\n')
  outer=owned['outer'];wiring=outer.modules['dependency_successor_wiring']
  answer=outer.modules['dependency_operational_entry']._continue_child(
   request=owned['prepared'],request_sha256=packet['request_sha256'],checked_sources=owned['checked'],
   adapter_owner=owned['adapter'],helpers=owned['helpers'],dependency_source_buffers=owned['dependency_source_buffers'],
   runtime_wiring=wiring,preparation=owned['preparation'],context=owned['context'],
   identity=dict(operation_id=request['operation_id'],isolated=True,optimized=False,camera_commands=[]))
  evidence=dict(answer['completion_evidence']);stdout=evidence.pop('stdout')
  assert type(stdout) is bytes and sha(stdout)==evidence['stdout_sha256']
  prep=owned['preparation']
  assert all(owned[n].closed for n in ('preparation','helpers','adapter')) and prep.callback_lease.closed
  receipt=outer.modules['ordinary_io'].write_new(Path(request['folder'])/'pending-preflight.json',prep.preflight)
  terminal=dict(schema='disabled_operational_outer_child_v1',operation_id=request['operation_id'],
   status='complete_pending_composition',preflight_sha256=receipt['sha256'],request_sha256=packet['request_sha256'],
   evidence=evidence,preparation_closed=True,helpers_closed=True,adapter_closed=True,callback_closed=True,
   execution_authorized=False,feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])
  outer.intact();outer.modules['ordinary_io'].write_new(Path(request['folder'])/'outer-child.json',terminal)
 except BaseException as error:primary=error
 if owned is not None:
  try:close_owned((owned['preparation'],owned['helpers'],owned['adapter'],owned['outer']))
  except BaseException as error:cleanup=error
 prep=None if owned is None else owned['preparation']
 callback=None if prep is None else prep.callback_lease.value
 callback_loader=None if callback is None else callback.loader
 io_module=None if callback_loader is None else callback_loader.loaded.get('io_adapter')
 report=dict(schema='invented_child_callback_observation_v1',mode=SYNTHETIC_MODE,observed=observed,
  preparation_started=None if prep is None else prep.started,
  preparation_failed=None if prep is None else prep.failed,
  callbacks_claimed=None if callback is None else callback.claimed,
  callbacks_closed=None if callback is None else callback.closed,
  callback_lease_attempted=None if prep is None else prep.callback_lease.attempted,
  callback_lease_closed=None if prep is None else prep.callback_lease.closed,
  owners_closed={} if owned is None else {n:owned[n].closed for n in ('preparation','helpers','adapter','outer')},
  fresh_refresh_receipts=refresh,
  synthetic_io=[] if io_module is None else io_module.SYNTHETIC_IO_OBSERVATIONS,
  controller_result=json.loads((Path(owned['prepared']['folder'])/'controller-result.json').read_bytes())
   if owned is not None and (Path(owned['prepared']['folder'])/'controller-result.json').exists() else None,
  protected_aliases_loaded=[] if callback_loader is None else sorted(
   n for n in callback_loader.loaded if n in {callback.arguments['aliases'][r] for r in callback.arguments['source_plan']['protected_order']}),
  leaked_aliases=sorted(n for n in sys.modules if n in ('tools','gdt_preflight','_successor_binding','_successor_control','_successor_factory') or
   n.startswith(('tools.','_a6700_successor','Cryptodome'))),
  failure_type=None if primary is None else type(primary).__name__,failure_code=None if primary is None else str(primary),
  cleanup_failure_type=None if cleanup is None else type(cleanup).__name__,
  terminal_replay=False,actual_runtime_verified=False,producer_execution_authenticated=False,
  execution_authorized=False,feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])
 with (Path(request['folder'])/'synthetic-child-observation.json').open('xb') as stream:stream.write(encoded(report))
 if primary is not None and cleanup is not None:raise primary from cleanup
 if primary is not None:raise primary
 if cleanup is not None:raise cleanup
 sys.stdout.buffer.write(stdout);sys.stdout.buffer.flush()
 return 0
'''

OBSERVATIONS=[]


class ChildCallbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',parent.PROFILE],
            capture_output=True,check=True,timeout=15)
        if result.stderr:raise AssertionError(result.stderr)
        cls.profile=json.loads(result.stdout)

    emergency_reap=supervised.ParentHandoffTests.emergency_reap

    def fixture(self,mode):
        with FreshTerminal(genuine_classifier=True) as terminal:
            case=joined.JoinedHandoffTests('test_joined_real_preflight_context_control_and_helper_handoff')
            case.fixture_basis=terminal.basis;case.fixture_source_manifest=terminal.source_manifest
            case.fixture_role_sources=dict(terminal.role_sources,io_adapter=synthetic_io_adapter_source(
                'prepare_interrupt' if mode=='prepare_interrupt' else 'complete'))
            case.fixture_role_aliases=terminal.aliases;case.fixture_factory=terminal.factory_raw
            case.fixture_ordinary_io=CHILD_IO
            case.fixture_wiring=wiring_source()+(RELEASE_INTERRUPT if mode=='release_interrupt' else b'')
            case.fixture_child_suffix=b'\nSYNTHETIC_MODE='+repr(mode).encode()+b'\n'+CHILD_SUFFIX
            self.addCleanup(case.doCleanups);case.setUp()
        plan=parent.prepare_synthetic_owned(folder=case.folder,packet=case.packet,buffers=case.buffers,
            rows=case.rows,expected_hashes=case.expected,runtime_profile=self.profile)
        self.addCleanup(lambda:parent.process.close_owned((plan.get('helpers'),plan.get('validation'),
            plan.get('bootstrap'),plan['adapter'],plan['outer'])))
        plan['helpers']=parent.process.helper_owner(plan['outer'],case.buffers,case.rows,'parent')
        dep={n:case.buffers['dependency.'+n] for n in parent.process.DEPENDENCIES[:-1]}
        dep['closure_manifest']=parent.encoded(plan['prepared']['sources'])
        plan['inputs']=plan['helpers'].package.dependency_execution.bind_runtime_packet(
            plan['prepared']['dependency_packet'],plan['prepared']['dependency_fixed'],dep,
            plan['prepared']['dependency_review_sha256'])
        boot=plan['bootstrap']=parent.BootstrapOwner(plan['outer'].modules['dependency_host_entry'])
        plan['control']=boot.load('_disabled_parent_control',case.buffers['bound.bootstrap:io_entry'],case.rows['bound.bootstrap:io_entry']['path'])
        factory=boot.load('_disabled_parent_factory',case.buffers['bound.integration:prospective_child'],case.rows['bound.integration:prospective_child']['path'])
        plan['validation']=parent.parent_validation_sources(plan['validated'],plan['outer'].modules['retained_gate'],
            plan['outer'].modules['ordinary_io'],factory)
        self.assertFalse(Path(plan['prepared']['folder']).exists())
        for name in ('pending-preflight.json','outer-child.json','synthetic-child-observation.json'):
            self.assertFalse((plan['folder']/name).exists())
        for name in plan['control'].CHILD_FILES:self.assertFalse((plan['context']['session_dir']/name).exists())
        if mode=='collision':
            target=plan['context']['session_dir']/plan['control'].CHILD_FILES[1]
            with target.open('xb') as stream:stream.write(b'preserved invented child collision')
        return case,plan

    def run_join(self,mode='complete',*,tamper_saved=False):
        case,plan=self.fixture(mode);real_popen=subprocess.Popen;processes=[]
        def spawn(*args,**kwargs):
            self.assertFalse(processes,'automatic retry')
            if mode=='child_collision':
                # Deterministic collision after parent reservation, before child reservation.
                target=plan['context']['session_dir']/plan['control'].CHILD_FILES[1]
                with target.open('xb') as stream:stream.write(b'preserved invented child collision')
            result=real_popen(*args,**kwargs);processes.append(result)
            self.addCleanup(self.emergency_reap,result);return result
        real_reconcile=parent._reconcile
        def reconcile(current,narrow):
            if tamper_saved:
                raw_path=Path(current['prepared']['folder'])/'collected/producer/raw.json'
                value=json.loads(raw_path.read_bytes());value['operation_id']='f'*32
                raw_path.write_bytes(parent.encoded(value))
                terminal_path=current['folder']/'outer-child.json';terminal=json.loads(terminal_path.read_bytes())
                terminal['evidence']['dependency_sha256']['producer/raw.json']=parent.sha(raw_path.read_bytes())
                terminal_path.write_bytes(parent.encoded(terminal))
            return real_reconcile(current,narrow)
        with patch.object(parent.subprocess,'Popen',side_effect=spawn),patch.object(parent,'_reconcile',side_effect=reconcile):
            answer=parent._run_pending(plan)
        self.assertEqual(len(processes),1)
        self.assertIsNotNone(processes[0].poll())
        self.assertTrue(processes[0].stdout.closed and processes[0].stderr.closed)
        for name in ('helpers','validation','bootstrap','adapter','outer'):self.assertTrue(plan[name].closed,name)
        diagnostic=json.loads((plan['folder']/'synthetic-child-observation.json').read_bytes())
        self.assertTrue(all(diagnostic['owners_closed'].values()))
        self.assertEqual(diagnostic['leaked_aliases'],[])
        self.assertIsNone(diagnostic['cleanup_failure_type'])
        self.assertEqual(diagnostic['protected_aliases_loaded'],[])
        self.assertTrue(diagnostic['preparation_started'])
        self.assertIs(diagnostic['terminal_replay'],False)
        for key in ('actual_runtime_verified','producer_execution_authenticated','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(diagnostic[key],False,key)
        self.assertEqual(diagnostic['camera_commands'],[])
        self.assertEqual(json.loads((plan['folder']/'final-receipt.json').read_bytes()),answer)
        narrow=json.loads((plan['context']['session_dir']/'host-result.json').read_bytes())
        OBSERVATIONS.append(dict(test=self.id(),answer=answer,narrow=narrow,diagnostic=diagnostic,
            terminal_replay=False,dependency_and_source_io_invented=True,camera_commands=[]))
        return case,plan,answer,narrow,diagnostic

    def test_child_preparation_factory_controller_collection_and_parent_join(self):
        case,plan,answer,narrow,diagnostic=self.run_join()
        self.assertEqual(answer['status'],'consistent_pending_composition',answer)
        self.assertEqual(narrow['host_exit_code'],0)
        self.assertIs(narrow['terminal_records_agree'],True)
        self.assertTrue(diagnostic['callbacks_claimed'] and diagnostic['callbacks_closed'])
        self.assertTrue(diagnostic['callback_lease_attempted'] and diagnostic['callback_lease_closed'])
        self.assertEqual(len(diagnostic['synthetic_io']),1)
        observation=diagnostic['synthetic_io'][0]
        self.assertEqual((observation['protected_prepare_calls'],observation['io_ops_calls']),(0,0))
        self.assertEqual(observation['preparation_calls'],1)
        self.assertEqual(observation['inspect_phases'],['A','B'])
        self.assertEqual(observation['discard_phases'],['A','B'])
        for key in ('generator_built_in_child','generator_aliases_released','genuine_classifier_used_to_generate_basis'):
            self.assertIs(observation[key],True,key)
        self.assertIs(observation['generator_source_files_written'],False)
        self.assertIsNone(diagnostic['failure_type'])
        self.assertEqual(len(diagnostic['fresh_refresh_receipts']),29)
        self.assertNotEqual(diagnostic['observed']['pid'],__import__('os').getpid())
        self.assertEqual([diagnostic['observed'][n] for n in ('isolated','no_site','no_user_site','no_bytecode','optimize')],[1,1,1,True,0])
        saved=answer['engine_result']['engine_result'];self.assertEqual(saved['status'],'consistent_saved_controller')
        self.assertIs(saved['test_injection_used'],True)
        for path in ('started.json','controller-result.json','completion.json','collected/collection.json','collected/producer/result.json'):
            value=json.loads((Path(plan['prepared']['folder'])/path).read_bytes())
            self.assertIs(value['test_injection_used'],True,path)

    def test_callback_prepare_interruption_cleans_without_success_envelope(self):
        case,plan,answer,narrow,diagnostic=self.run_join('prepare_interrupt')
        self.assertEqual(answer['status'],'needs_review')
        self.assertTrue(diagnostic['callbacks_claimed'] and diagnostic['callbacks_closed'])
        self.assertEqual(diagnostic['synthetic_io'][0]['preparation_calls'],1)
        self.assertEqual(diagnostic['synthetic_io'][0]['inspect_phases'],[])
        self.assertIsNone(diagnostic['controller_result'])
        self.assertEqual(diagnostic['failure_type'],'KeyboardInterrupt')
        self.assertEqual(diagnostic['failure_code'],'invented child adapter preparation interruption')
        self.assertFalse((plan['folder']/'outer-child.json').exists())

    def test_fresh_source_drift_stops_preparation_before_callback_and_outputs(self):
        case,plan,answer,narrow,diagnostic=self.run_join('refresh_drift')
        self.assertEqual(answer['status'],'needs_review')
        self.assertTrue(diagnostic['preparation_failed'])
        self.assertTrue(diagnostic['failure_code'].startswith('invented_disk_size:'),diagnostic)
        self.assertIsNone(diagnostic['callbacks_claimed'])
        self.assertFalse(Path(plan['prepared']['folder']).exists())
        self.assertFalse((plan['folder']/'outer-child.json').exists())

    def test_existing_child_output_is_preserved_without_dispatch(self):
        case,plan=self.fixture('collision')
        with patch.object(parent.subprocess,'Popen',side_effect=AssertionError('prelaunch collision must not spawn')) as spawn:
            answer=parent._run_pending(plan)
        spawn.assert_not_called()
        self.assertEqual(answer['status'],'needs_review')
        self.assertEqual(answer['failure_code'],'operational_launch_supervisor_failure')
        for name in ('helpers','validation','bootstrap','adapter','outer'):self.assertTrue(plan[name].closed,name)
        for name in ('synthetic-child-observation.json','outer-child.json'):
            self.assertFalse((plan['folder']/name).exists())
        for name in (*plan['control'].PARENT_FILES,'actual-started.json'):
            self.assertFalse((plan['context']['session_dir']/name).exists(),name)
        self.assertEqual(json.loads((plan['folder']/'final-receipt.json').read_bytes()),answer)
        target=plan['context']['session_dir']/plan['control'].CHILD_FILES[1]
        self.assertEqual(target.read_bytes(),b'preserved invented child collision')
        self.assertFalse(Path(plan['prepared']['folder']).exists())
        OBSERVATIONS.append(dict(test=self.id(),answer=answer,prelaunch_refusal=True,
            observed_child_processes=0,terminal_replay=False,dependency_and_source_io_invented=True,camera_commands=[]))

    def test_child_collision_after_parent_reservation_refuses_without_callback(self):
        case,plan,answer,narrow,diagnostic=self.run_join('child_collision')
        self.assertEqual(answer['status'],'needs_review')
        self.assertIs(diagnostic['callbacks_claimed'],False)
        target=plan['context']['session_dir']/plan['control'].CHILD_FILES[1]
        self.assertEqual(target.read_bytes(),b'preserved invented child collision')
        self.assertFalse(Path(plan['prepared']['folder']).exists())

    def test_release_completion_interruption_refuses_without_retry(self):
        case,plan,answer,narrow,diagnostic=self.run_join('release_interrupt')
        self.assertEqual(answer['status'],'needs_review')
        self.assertTrue(diagnostic['callback_lease_attempted'] and diagnostic['callback_lease_closed'])
        self.assertEqual(diagnostic['failure_code'],'invented release completion interruption')
        self.assertFalse((plan['folder']/'outer-child.json').exists())

    def test_rehashed_collected_raw_drift_refuses_after_narrow_success(self):
        case,plan,answer,narrow,diagnostic=self.run_join(tamper_saved=True)
        self.assertEqual(narrow['host_exit_code'],0)
        self.assertEqual(answer['status'],'needs_review')
        self.assertIsNotNone(answer['failure_code'])


if __name__=='__main__':unittest.main(verbosity=2)
