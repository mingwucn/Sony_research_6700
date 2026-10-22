"""Exact transport with a separately identified synthetic child adapter.

The successful process runs current child source plus the test-only suffix
below, not the unchanged operational child entry. The unchanged bootstrap,
source owners, v6 gate/metadata, current context, helpers, retained checker and
record reservations are real. All metadata/files and the disk reader are
invented. Callbacks, dispatch and collection remain inert. No installed
dependencies, firmware, constants, upstream tools or camera are involved.
"""
import base64
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from tools import dependency_operational_launcher as parent
import test_dependency_joined_handoff as joined_fixture

OBSERVATIONS=[]

DISK_IO=b'''import hashlib,os,stat,sys
from pathlib import Path
def read(path,*,expected_sha256,expected_bytes):
 path=Path(path);before=path.lstat()
 assert stat.S_ISREG(before.st_mode) and before.st_nlink==1,'invented_disk_kind'
 assert not getattr(before,'st_file_attributes',0)&0x400,'invented_disk_reparse'
 with path.open('rb') as stream:
  opened=os.fstat(stream.fileno());raw=stream.read(expected_bytes+1);final=os.fstat(stream.fileno())
 after=path.lstat()
 stamp=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
 # Windows lstat/fstat can expose different ctime semantics. Preserve full
 # stability within each API, plus dev/inode/size/mtime across the open.
 assert stamp(before)==stamp(after) and stamp(opened)==stamp(final) and stamp(before)[:-1]==stamp(opened)[:-1],'invented_disk_identity'
 assert len(raw)==expected_bytes,'invented_disk_size:'+str(path)
 assert hashlib.sha256(raw).hexdigest()==expected_sha256,'invented_disk_hash:'+str(path)
 sys.audit('a6700.synthetic.refresh_read',str(path),expected_sha256,len(raw))
 return raw,{'invented_disk_reader':True,'sha256':expected_sha256,'bytes':len(raw)}
def read_ordinary(*a,**kw):raise AssertionError('invented ordinary callback forbidden')
'''


# This adapter is captured and hashed separately from the unmodified prefix.
# It selects only the explicitly synthetic API; no production request selector
# or bootstrap byte is changed. The real child entry is tested independently.
SYNTHETIC_SUFFIX=rb'''
def child(request,packet,buffers,rows):
 import os
 from types import SimpleNamespace
 observed=dict(pid=os.getpid(),isolated=sys.flags.isolated,no_site=sys.flags.no_site,
  no_user_site=sys.flags.no_user_site,no_bytecode=sys.dont_write_bytecode,optimize=sys.flags.optimize,
  forbidden_modules=sorted(n for n in sys.modules if n=='tools' or n.startswith('tools.') or
   n.split('.')[0] in ('ctypes','_ctypes','Crypto','Cryptodome','cffi','_cffi_backend')))
 root=Path(packet['repository_root']);reads=[];refreshes=[];events=[];record_handles=[]
 owned=None;records=None;answer=None;primary=None;original_open=Path.open
 def tracked_open(path,*args,**kwargs):
  handle=original_open(path,*args,**kwargs)
  if args and args[0]=='xb' and path.name in ('observation-journal.jsonl','observation-result.json'):
   record_handles.append(handle)
  return handle
 def audit(event,args):
  if event=='a6700.synthetic.refresh_read':refreshes.append(list(args))
  if event.startswith(('socket.','ctypes.')) or event=='subprocess.Popen':
   raise AssertionError('synthetic child forbids external execution/network/native loading')
  if event=='import' and args[0].split('.')[0] in ('tools','ctypes','_ctypes','Crypto','Cryptodome','cffi','_cffi_backend'):
   raise AssertionError('synthetic child forbids installed dependency import')
  if event=='open' and isinstance(args[0],str):
   path=Path(args[0])
   if path.is_relative_to(root):reads.append(str(path))
   else:
    assert path.is_relative_to(Path(sys.base_prefix)), 'unexpected read outside invented tree/stdlib'
 sys.addaudithook(audit)
 def dispatch(**kw):
  nonlocal records
  events.append('inert_dispatch');owned['helpers'].intact()
  records=kw['records'].value
  assert not records.closed and all(not h.closed for h in records.handles.values())
  callback=owned['preparation'].callback_lease.value
  callback.fail=SYNTHETIC_MODE=='callback_interrupt'
  callback.close_fail=SYNTHETIC_MODE=='callback_close_interrupt'
  if SYNTHETIC_MODE=='dispatch_interrupt':raise KeyboardInterrupt('invented dispatch interruption')
  assert kw['make_callbacks_after_receipt'](None,None,None)==('invented callback token',)
  if SYNTHETIC_MODE=='partial_return':return {'inert':'incomplete'}
  kw['release_callbacks_after_controller']();kw['records'].close()
  return {'inert':'completed isolated handoff'}
 def collect(**kw):
  events.append('inert_collection');owned['helpers'].intact();assert records.closed
  return {'invented_completion_only':True}
 try:
  assert observed['forbidden_modules']==[]
  owned=prepare_synthetic_owned(request=request,packet=packet,buffers=buffers,rows=rows,
   request_bytes=encoded(request),expected_request_sha256=sys.argv[2],request_path=sys.argv[1])
  Path.open=tracked_open
  if SYNTHETIC_MODE=='refresh_drift':
   key='bound.role:acceptance';Path(rows[key]['path']).write_bytes(b'# invented post-transport drift\n')
  outer=owned['outer']
  answer=outer.modules['dependency_operational_entry']._continue_child(
   request=owned['prepared'],request_sha256=packet['request_sha256'],checked_sources=owned['checked'],
   adapter_owner=owned['adapter'],helpers=owned['helpers'],dependency_source_buffers=owned['dependency_source_buffers'],
   runtime_wiring=SimpleNamespace(_dispatch_runtime=dispatch,_collect_completion=collect),
   preparation=owned['preparation'],context=owned['context'],
   identity={'operation_id':request['operation_id'],'isolated':True,'optimized':False,'camera_commands':[]})
 except BaseException as error:primary=error
 cleanup=None
 if owned is not None:
  try:close_owned((owned['preparation'],owned['helpers'],owned['adapter'],owned['outer']))
  except BaseException as error:cleanup=error
 Path.open=original_open
 context=None if owned is None else dict(owned['context'])
 if context is not None:
  context['session_dir']=str(context['session_dir']);context['repository_root']=str(context['repository_root'])
 prep=None if owned is None else owned['preparation']
 callback=None if prep is None else prep.callback_lease.value
 report=dict(schema='invented_isolated_current_handoff_v1',observed=observed,events=events,
  status='synthetic_handoff_complete' if primary is None and cleanup is None else 'needs_review',
  context_sha256=None if context is None else sha(encoded(context)),answer=answer,
  fresh_retained_reads=sorted(row[0] for row in refreshes),fresh_refresh_receipts=refreshes,
  record_handles_closed_before_exit=[handle.closed for handle in record_handles],
  helpers_closed=None if owned is None else owned['helpers'].closed,
  preparation_closed=None if prep is None else prep.closed,
  adapter_closed=None if owned is None else owned['adapter'].closed,
  outer_closed=None if owned is None else owned['outer'].closed,
  child_records_closed=None if records is None else records.closed,
  callback_calls=None if callback is None else callback.calls,
  callback_close_attempts=None if callback is None else callback.close_attempts,
  callback_closed=None if prep is None else prep.callback_lease.closed,
  leaked_aliases=sorted(n for n in sys.modules if n.startswith('_a6700_successor') or
   n in ('_successor_binding','_successor_control','_successor_factory','gdt_preflight')),
  failure_type=None if primary is None else type(primary).__name__,
  failure_code=None if primary is None else str(primary),
  failure_stage=None if primary is None else getattr(primary,'stage',None),
  failure_reason=None if primary is None else getattr(primary,'reason',None),
  cleanup_failure_type=None if cleanup is None else type(cleanup).__name__,
  execution_authorized=False,feature_supported=False,recovery_proven=False,device_write_gate_passed=False,
  automatic_retry=False,camera_commands=[])
 print(encoded(report).decode('ascii'))
 return 0 if primary is None and cleanup is None else 2
'''

REFUSAL_SUFFIX=rb'''
_unchanged_operational_child=child
def child(request,packet,buffers,rows):
 try:return _unchanged_operational_child(request,packet,buffers,rows)
 except BaseException as error:
  print(encoded(dict(schema='invented_unchanged_child_refusal_diagnostic_v1',
   failure_type=type(error).__name__,failure_code=str(error),camera_commands=[])).decode('ascii'))
  return 2
'''


class IsolatedHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        observed=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',parent.PROFILE],
            capture_output=True,check=True,timeout=15)
        if observed.stderr:raise AssertionError(observed.stderr)
        cls.profile=json.loads(observed.stdout)

    def fixture(self,mode='complete',*,actual_child=False,refusal_diagnostic=False):
        case=joined_fixture.JoinedHandoffTests('test_joined_real_preflight_context_control_and_helper_handoff')
        self.addCleanup(case.doCleanups)
        case.fixture_ordinary_io=DISK_IO
        case.fixture_child_suffix=b'' if actual_child else b'\nSYNTHETIC_MODE='+repr(mode).encode()+b'\n'+SYNTHETIC_SUFFIX
        if refusal_diagnostic:case.fixture_child_suffix=REFUSAL_SUFFIX
        case.setUp()
        compile(case.buffers['process_child'],'<synthetic-process-child>','exec',dont_inherit=True,optimize=0)
        plan=parent.prepare_synthetic_owned(folder=case.folder,packet=case.packet,buffers=case.buffers,
            rows=case.rows,expected_hashes=case.expected,runtime_profile=self.profile)
        self.addCleanup(lambda:parent.process.close_owned((plan['adapter'],plan['outer'])))
        self.assertEqual(plan['request']['argv_prefix'][-1],parent.bootstrap())
        self.assertEqual(plan['request']['bootstrap_sha256'],parent.sha(parent.bootstrap().encode()))
        records=case.checker.reserve_parent(context=plan['context'])
        self.addCleanup(records.close)
        self.assertFalse(records.closed)
        plan['qualification_sources']=dict(authored_child_sha256=parent.sha(
            Path('tools/dependency_operational_child.py').read_bytes()),
            test_adapter_sha256=None if actual_child else parent.sha(case.fixture_child_suffix),
            transported_child_sha256=case.rows['process_child']['sha256'],
            bootstrap_sha256=plan['request']['bootstrap_sha256'])
        return case,plan,records

    def run_child(self,plan):
        argv=plan['context']['child_argv']
        result=subprocess.run(argv,cwd=plan['context']['repository_root'],stdin=subprocess.DEVNULL,
            capture_output=True,timeout=30,shell=False,close_fds=True)
        self.assertEqual(result.stderr,b'',result.stderr.decode('utf-8','replace'))
        self.assertTrue(result.stdout,result)
        receipt=json.loads(result.stdout)
        OBSERVATIONS.append(dict(test=self.id(),exit_code=result.returncode,
            sources=plan['qualification_sources'],receipt=receipt))
        return result,receipt

    def save_changed_request(self,plan,request):
        raw=parent.encoded(request);plan['request_path'].write_bytes(raw)
        plan['context']['child_argv'][-1]=parent.sha(raw)

    def assert_closed(self,receipt):
        for key in ('helpers_closed','preparation_closed','adapter_closed','outer_closed'):
            self.assertIs(receipt[key],True,(key,receipt))
        self.assertEqual(receipt['leaked_aliases'],[])
        for key in ('execution_authorized','feature_supported','recovery_proven','device_write_gate_passed','automatic_retry'):
            self.assertIs(receipt[key],False)
        self.assertEqual(receipt['camera_commands'],[])

    def test_fresh_isolated_current_context_and_genuine_retained_handoff(self):
        case,plan,records=self.fixture()
        result,receipt=self.run_child(plan)
        self.assertEqual(result.returncode,0,receipt)
        self.assertEqual(receipt['status'],'synthetic_handoff_complete')
        context=dict(plan['context'],session_dir=str(plan['context']['session_dir']),
            repository_root=str(plan['context']['repository_root']))
        self.assertEqual(receipt['context_sha256'],parent.sha(parent.encoded(context)))
        self.assertEqual(receipt['fresh_retained_reads'],sorted(str(Path(row['path']))
            for name,row in case.rows.items() if name.startswith('bound.')))
        self.assertEqual(len(receipt['fresh_refresh_receipts']),29)
        expected={row['path']:(row['sha256'],row['size']) for name,row in case.rows.items() if name.startswith('bound.')}
        self.assertEqual({path:(digest,size) for path,digest,size in receipt['fresh_refresh_receipts']},expected)
        observed=receipt['observed'];self.assertNotEqual(observed['pid'],__import__('os').getpid())
        self.assertEqual([observed[n] for n in ('isolated','no_site','no_user_site','no_bytecode','optimize')],[1,1,1,True,0])
        self.assertEqual(observed['forbidden_modules'],[])
        self.assertEqual(receipt['events'],['inert_dispatch','inert_collection'])
        self.assertEqual(receipt['answer']['engine_result'],{'inert':'completed isolated handoff'})
        self.assertEqual((receipt['callback_calls'],receipt['callback_close_attempts'],receipt['callback_closed']),(1,1,True))
        self.assertIs(receipt['child_records_closed'],True);self.assert_closed(receipt)
        self.assertEqual(receipt['record_handles_closed_before_exit'],[True,True])
        self.assertFalse(records.closed);self.assertTrue(all(not h.closed for h in records.handles.values()))

    def test_unchanged_operational_child_still_refuses_v6_before_records(self):
        case,plan,records=self.fixture(actual_child=True)
        result,receipt=self.run_child(plan)
        self.assertEqual(result.returncode,2)
        self.assertEqual(receipt,{'status':'needs_review','camera_commands':[]})
        self.assertTrue(all(not (plan['context']['session_dir']/n).exists() for n in case.checker.CHILD_FILES))
        self.assertFalse(records.closed)

    def test_diagnostic_adapter_identifies_unchanged_child_v6_refusal(self):
        case,plan,_=self.fixture(refusal_diagnostic=True)
        result,receipt=self.run_child(plan)
        self.assertEqual(result.returncode,2)
        self.assertEqual(receipt,dict(schema='invented_unchanged_child_refusal_diagnostic_v1',
            failure_type='ValueError',failure_code='operational_process_v6_execution_pending',camera_commands=[]))
        self.assertTrue(all(not (plan['context']['session_dir']/n).exists() for n in case.checker.CHILD_FILES))

    def test_bootstrap_rejects_saved_source_and_packet_drift_before_adapter(self):
        for kind in ('source','packet'):
            with self.subTest(kind=kind):
                case,plan,_=self.fixture()
                path=Path(case.rows['process_child']['path']) if kind=='source' else case.folder/'packet.json'
                with path.open('ab') as stream:stream.write(b' ')
                result,receipt=self.run_child(plan)
                self.assertEqual(result.returncode,2)
                self.assertEqual(receipt,{'status':'needs_review','camera_commands':[]})

    def test_current_ordinary_drift_refuses_genuine_reservation_before_dispatch(self):
        case,plan,_=self.fixture()
        path=case.root/next(iter(plan['validated']['candidate']['inputs'].values()))['path']
        with path.open('ab') as stream:stream.write(b' ')
        result,receipt=self.run_child(plan)
        self.assertEqual(result.returncode,2,receipt);self.assertEqual(receipt['events'],[])
        self.assertEqual(receipt['failure_type'],'IoEntryError');self.assert_closed(receipt)
        self.assertTrue(all(not (plan['context']['session_dir']/n).exists() for n in case.checker.CHILD_FILES))

    def test_observed_profile_and_rehashed_current_operation_mismatch_refuse(self):
        for kind in ('profile','operation'):
            with self.subTest(kind=kind):
                case,plan,_=self.fixture();request=copy.deepcopy(plan['request'])
                if kind=='profile':request['expected_runtime']['platform']='invented-other-platform'
                else:request['operation_id']='8'*32
                self.save_changed_request(plan,request)
                result,receipt=self.run_child(plan);self.assertEqual(result.returncode,2,receipt)
                if kind=='profile':self.assertEqual(receipt,{'status':'needs_review','camera_commands':[]})
                else:
                    self.assertEqual(receipt['failure_code'],'operational_process_operation')
                    self.assertEqual(receipt['events'],[]);self.assertIsNone(receipt['helpers_closed'])
                self.assertTrue(all(not (plan['context']['session_dir']/n).exists() for n in case.checker.CHILD_FILES))

    def test_rehashed_ordinary_metadata_mismatch_reaches_full_preflight_and_refuses(self):
        case,plan,_=self.fixture();packet=copy.deepcopy(plan['packet']);raw=b'{"invented":"changed activity scope"}'
        packet['ordinary']['activity_scope']=base64.b64encode(raw).decode('ascii')
        packet['ordinary_receipts']['activity_scope']={'bytes':len(raw),'sha256':parent.sha(raw)}
        (case.folder/'packet.json').write_bytes(parent.encoded(packet))
        request=copy.deepcopy(plan['request'])
        _,request['packet']=parent.entry.read_source(str(case.folder/'packet.json'),8*1024**2)
        self.save_changed_request(plan,request)
        result,receipt=self.run_child(plan)
        self.assertEqual(result.returncode,2,receipt);self.assertEqual(receipt['events'],[])
        self.assertEqual(receipt['failure_type'],'ValueError');self.assertIsNone(receipt['helpers_closed'])
        self.assertNotIn(receipt['failure_code'],('operational_process_projection','operational_process_operation'))

    def test_fresh_disk_refresh_refuses_post_transport_retained_source_drift(self):
        _,plan,_=self.fixture('refresh_drift')
        result,receipt=self.run_child(plan)
        self.assertEqual(result.returncode,2,receipt);self.assertEqual(receipt['events'],[])
        self.assertEqual(receipt['failure_type'],'AssertionError');self.assert_closed(receipt)
        self.assertIsNone(receipt['callback_calls'])

    def test_partial_child_reservation_preserves_collision_and_closes_handles(self):
        case,plan,_=self.fixture()
        path=plan['context']['session_dir']/case.checker.CHILD_FILES[1]
        path.write_bytes(b'invented existing evidence')
        result,receipt=self.run_child(plan)
        self.assertEqual(result.returncode,2,receipt);self.assertEqual(receipt['events'],[])
        self.assertEqual((receipt['failure_stage'],receipt['failure_reason']),('record_reservation','exclusive_reservation_failed'))
        self.assertEqual(path.read_bytes(),b'invented existing evidence');self.assert_closed(receipt)
        self.assertEqual(receipt['record_handles_closed_before_exit'],[True])
        # Also retain the partial file and check availability after reaping.
        first=plan['context']['session_dir']/case.checker.CHILD_FILES[0]
        self.assertTrue(first.exists());first.unlink()

    def test_engine_interrupt_partial_return_and_callback_close_clean_once(self):
        for mode,kind in (('dispatch_interrupt','KeyboardInterrupt'),('callback_interrupt','KeyboardInterrupt'),
                          ('partial_return','ValueError'),('callback_close_interrupt','OSError')):
            with self.subTest(mode=mode):
                _,plan,_=self.fixture(mode)
                result,receipt=self.run_child(plan)
                self.assertEqual(result.returncode,2,receipt);self.assertEqual(receipt['failure_type'],kind)
                self.assert_closed(receipt);self.assertIs(receipt['child_records_closed'],True)
                self.assertEqual(receipt['callback_close_attempts'],1)
                self.assertEqual(receipt['callback_closed'],mode!='callback_close_interrupt')
                self.assertNotIn('inert_collection',receipt['events'])


if __name__=='__main__':unittest.main(verbosity=2)
