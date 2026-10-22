"""Retained I/O and protected-preparation over invented physical source files.

The genuine factory/IoAdapter operate on disposable files. Capture, decoding,
header validation and dependency operations remain explicit invented doubles.
No actual protected source/input, installed dependency or device is accessed.
"""
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import unittest
from unittest.mock import patch

from tools import dependency_operational_launcher as parent
from dependency_terminal_fixture import FreshTerminal
from dependency_io_boundary_fixture import invented_boundary
from dependency_child_runtime_fixture import wiring_source
from test_dependency_child_callbacks import CHILD_IO, CHILD_SUFFIX
import test_dependency_joined_handoff as joined
import test_dependency_parent_handoff as supervised


CONSTANTS_READER=rb'''
def read_ordinary(path,root):
 path=Path(path);root=Path(root)
 assert path==root/'private/invented-constants.py','invented constants path'
 before=path.lstat()
 assert stat.S_ISREG(before.st_mode) and before.st_nlink==1 and not getattr(before,'st_file_attributes',0)&0x400
 with path.open('rb') as stream:
  opened=os.fstat(stream.fileno());raw=stream.read(4097);final=os.fstat(stream.fileno())
 after=path.lstat();stamp=lambda s:(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
 assert 0<len(raw)<=4096 and stamp(before)==stamp(after) and stamp(opened)==stamp(final) and stamp(before)[:-1]==stamp(opened)[:-1]
 sys.audit('a6700.synthetic.constants_read',hashlib.sha256(raw).hexdigest(),len(raw))
 return raw
'''


IO_TRACE=rb'''
import os
class _InventedIoTrace:
 def __init__(self,path,mode):
  self.path=path;self.mode=mode;self.events=[];self.live=set();self.installed={};self.original={}
  self.closed=False
  for name in ('open','read','lseek','close'):self.original[name]=getattr(os,name)
  def traced_open(path,flags,*args,**kwargs):
   target=isinstance(path,(str,bytes,os.PathLike)) and Path(path)==self.path
   fd=self.original['open'](path,flags,*args,**kwargs)
   if target:
    self.live.add(fd);self.events.append(dict(op='open',fd=fd,flags=flags))
   return fd
  def traced_read(fd,n):
   raw=self.original['read'](fd,n)
   if fd in self.live:self.events.append(dict(op='read',fd=fd,requested=n,returned=len(raw)))
   return raw
  def traced_seek(fd,offset,whence):
   value=self.original['lseek'](fd,offset,whence)
   if fd in self.live:self.events.append(dict(op='seek',fd=fd,offset=offset,whence=whence,result=value))
   return value
  def traced_close(fd):
   tracked=fd in self.live
   if tracked:self.events.append(dict(op='close_attempt',fd=fd))
   value=self.original['close'](fd)
   if tracked:
    self.live.remove(fd);self.events.append(dict(op='close_returned',fd=fd))
    if self.mode=='close_completion_error':raise OSError('invented post-close completion error')
   return value
  self.installed=dict(open=traced_open,read=traced_read,lseek=traced_seek,close=traced_close)
  for name,value in self.installed.items():setattr(os,name,value)
 def restore(self):
  assert not self.closed
  self.closed=True;changed=[]
  for name in reversed(tuple(self.installed)):
   if getattr(os,name) is self.installed[name]:setattr(os,name,self.original[name])
   else:changed.append(name)
  if changed:raise AssertionError('invented I/O trace ownership changed')

def _boundary_observation(loader,trace,constants):
 loaded={} if loader is None else loader.loaded
 observations={name:module.SYNTHETIC_PROTECTED_OBSERVATIONS for name,module in loaded.items()
  if hasattr(module,'SYNTHETIC_PROTECTED_OBSERVATIONS')}
 return dict(events=[] if trace is None else trace.events,
  source_fds_live=[] if trace is None else sorted(trace.live),
  tracing_restored=None if trace is None else trace.closed,
  constants_reads=constants,protected_doubles=observations,
  live_owned_aliases=sorted(n for n in loaded if n in sys.modules),
  original_io_adapter=True,original_factory=True,actual_inputs_accessed=False,
  real_cryptography_performed=False,camera_commands=[])
'''


def child_suffix(mode):
    raw=CHILD_SUFFIX
    replacements={
      b"root=Path(packet['repository_root']);refresh=[]":
       b"root=Path(packet['repository_root']);refresh=[];constants=[];io_trace=None",
      b"if event=='a6700.synthetic.refresh_read':refresh.append(list(args))":
       b"if event=='a6700.synthetic.refresh_read':refresh.append(list(args))\n  if event=='a6700.synthetic.constants_read':constants.append(list(args))",
      b"outer=owned['outer'];wiring=outer.modules['dependency_successor_wiring']":
       b"outer=owned['outer'];wiring=outer.modules['dependency_successor_wiring']\n  source_path=root/owned['context']['source_manifest']['relative_path']\n  io_trace=_InventedIoTrace(source_path,SYNTHETIC_MODE)",
      b"prep=None if owned is None else owned['preparation']":
       b"if io_trace is not None:\n  try:io_trace.restore()\n  except BaseException as error:\n   if cleanup is None:cleanup=error\n prep=None if owned is None else owned['preparation']",
      b"synthetic_io=[] if io_module is None else io_module.SYNTHETIC_IO_OBSERVATIONS,":
       b"io_boundary=_boundary_observation(callback_loader,io_trace,constants),",
    }
    for old,new in replacements.items():
        if raw.count(old)!=1:raise AssertionError('invented child diagnostic source drift')
        raw=raw.replace(old,new)
    # The unchanged retained controller saves the real adapter snapshot.
    return b'\nSYNTHETIC_MODE='+repr(mode).encode()+b'\n'+IO_TRACE+raw


OBSERVATIONS=[]


@unittest.skipUnless(sys.platform=='win32','retained readonly guard requires Windows file attributes')
class IoBoundaryTests(unittest.TestCase):
    setUpClass=classmethod(supervised.ParentHandoffTests.setUpClass.__func__)
    emergency_reap=supervised.ParentHandoffTests.emergency_reap

    def fixture(self,mode):
        double_mode=mode if mode in ('capture_early_eof','decode_exception','measure_bad_hash') else 'complete'
        with FreshTerminal(genuine_classifier=True) as terminal:
            inputs=invented_boundary(terminal,double_mode)
            constants=inputs['constants_raw']
            if mode=='constants_shape':
                constants=constants.replace(repr(b'invented-common!').encode(),repr(b'short').encode())
            case=joined.JoinedHandoffTests('test_joined_real_preflight_context_control_and_helper_handoff')
            case.fixture_basis=inputs['basis'];case.fixture_source_manifest=inputs['source_manifest']
            case.fixture_role_sources=dict(terminal.role_sources,**inputs['role_sources'])
            case.fixture_role_aliases=dict(terminal.aliases,capture='gdt_actual_capture',
                core='gdt_actual_core',validator='gdt_actual_validator')
            case.fixture_factory=terminal.factory_raw
            case.fixture_prerequisites=dict(constants_sha256=parent.sha(constants))
            case.fixture_ordinary_io=CHILD_IO+CONSTANTS_READER
            case.fixture_wiring=wiring_source();case.fixture_child_suffix=child_suffix(mode)
            self.addCleanup(case.doCleanups);case.setUp()
        source=case.root/case.validated['inputs']['source_manifest']['relative_path']
        constants_path=case.root/case.validated['inputs']['prerequisites']['constants_relative_path']
        case.write_new(source,inputs['source_raw']);case.write_new(constants_path,constants)
        if mode=='constants_hash':
            with constants_path.open('ab') as stream:stream.write(b'# invented changed constants\n')
        if mode=='source_hash_drift':
            changed=bytearray(inputs['source_raw']);changed[-1]^=1;source.write_bytes(changed)
        if mode!='source_writable':
            os.chmod(source,stat.S_IREAD)
            self.addCleanup(os.chmod,source,stat.S_IWRITE|stat.S_IREAD)
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
        for name in plan['control'].CHILD_FILES:self.assertFalse((plan['context']['session_dir']/name).exists())
        return case,plan,inputs

    def run_join(self,mode='complete'):
        case,plan,inputs=self.fixture(mode);real_popen=subprocess.Popen;processes=[]
        def spawn(*args,**kwargs):
            self.assertFalse(processes,'automatic retry')
            result=real_popen(*args,**kwargs);processes.append(result)
            self.addCleanup(self.emergency_reap,result);return result
        with patch.object(parent.subprocess,'Popen',side_effect=spawn):answer=parent._run_pending(plan)
        self.assertEqual(len(processes),1);self.assertIsNotNone(processes[0].poll())
        self.assertTrue(processes[0].stdout.closed and processes[0].stderr.closed)
        for name in ('helpers','validation','bootstrap','adapter','outer'):self.assertTrue(plan[name].closed,name)
        diagnostic=json.loads((plan['folder']/'synthetic-child-observation.json').read_bytes())
        narrow=json.loads((plan['context']['session_dir']/'host-result.json').read_bytes())
        child_result=json.loads((plan['context']['session_dir']/plan['control'].CHILD_FILES[1]).read_bytes())
        OBSERVATIONS.append(dict(test=self.id(),mode=mode,answer=answer,narrow=narrow,diagnostic=diagnostic,
            retained_child_result=child_result,invented_input_summary=inputs['summary'],camera_commands=[]))
        self.assertTrue(all(diagnostic['owners_closed'].values()));self.assertEqual(diagnostic['leaked_aliases'],[])
        self.assertIsNone(diagnostic['cleanup_failure_type']);self.assertTrue(diagnostic['callbacks_closed'])
        boundary=diagnostic['io_boundary']
        self.assertEqual(boundary['source_fds_live'],[]);self.assertTrue(boundary['tracing_restored'])
        self.assertEqual(boundary['live_owned_aliases'],[])
        for key in ('actual_runtime_verified','producer_execution_authenticated','execution_authorized',
                    'feature_supported','recovery_proven','device_write_gate_passed','terminal_replay'):
            self.assertIs(diagnostic[key],False,key)
        self.assertEqual(diagnostic['camera_commands'],[])
        self.assertEqual(json.loads((plan['folder']/'final-receipt.json').read_bytes()),answer)
        events=boundary['events'];ops=[v['op'] for v in events]
        self.assertEqual(ops.count('open'),ops.count('close_attempt'))
        self.assertEqual(ops.count('open'),ops.count('close_returned'))
        return plan,answer,narrow,diagnostic,boundary,inputs

    def assert_refused(self,mode):
        values=self.run_join(mode);plan,answer,narrow,diagnostic,boundary,inputs=values
        self.assertEqual(answer['status'],'needs_review',answer)
        self.assertFalse((plan['folder']/'outer-child.json').exists())
        return values

    def test_real_io_factory_preparation_two_phases_and_parent_join(self):
        plan,answer,narrow,diagnostic,boundary,inputs=self.run_join()
        self.assertEqual(answer['status'],'consistent_pending_composition',answer)
        self.assertEqual(narrow['host_exit_code'],0)
        snapshot=narrow['adapter_snapshot']
        self.assertEqual(snapshot['status'],'complete');self.assertEqual(snapshot['preparation_attempts'],1)
        for key in ('phase_a','phase_b'):
            phase=snapshot[key];self.assertEqual(phase['status'],'complete')
            for name in ('open_succeeded','rewind_succeeded','close_succeeded'):self.assertTrue(phase[name],name)
            self.assertEqual((phase['open_attempts'],phase['rewind_attempts'],phase['close_attempts']),(1,1,1))
            for name in ('capture','decode'):
                observed=phase[name];self.assertTrue(observed['verified'])
                self.assertEqual(observed['bytes_returned'],len(inputs['source_raw']))
                self.assertEqual((observed['read_attempts'],observed['read_calls'],observed['eof_probes']),(2,2,1))
                self.assertFalse(observed['failed_read_returned_bytes_unknown'])
        self.assertEqual(len(diagnostic['protected_aliases_loaded']),3)
        self.assertEqual(len(boundary['constants_reads']),1)
        roles={v['role']:v for v in boundary['protected_doubles'].values()}
        self.assertEqual({k:v['calls'] for k,v in roles.items()},{'capture':2,'core':2,'validator':2})
        events=boundary['events'];ops=[v['op'] for v in events]
        self.assertEqual(ops.count('open'),2);self.assertEqual(ops.count('seek'),2)
        self.assertEqual(ops.count('close_attempt'),2);self.assertEqual(ops.count('close_returned'),2)
        self.assertEqual(sum(v['returned'] for v in events if v['op']=='read'),4*len(inputs['source_raw']))
        self.assertEqual(sum(v['returned']==0 for v in events if v['op']=='read'),4)
        self.assertTrue(all(not v['cryptography_performed'] for v in roles.values()))

    def test_constants_hash_drift_refuses_before_protected_imports(self):
        *_,diagnostic,boundary,inputs=self.assert_refused('constants_hash')
        self.assertEqual(len(boundary['constants_reads']),1)
        self.assertEqual(diagnostic['protected_aliases_loaded'],[]);self.assertEqual(boundary['events'],[])

    def test_constants_shape_refuses_before_protected_imports(self):
        *_,diagnostic,boundary,inputs=self.assert_refused('constants_shape')
        self.assertEqual(len(boundary['constants_reads']),1)
        self.assertEqual(diagnostic['protected_aliases_loaded'],[]);self.assertEqual(boundary['events'],[])

    def test_source_hash_drift_refuses_after_real_capture_reads(self):
        *_,boundary,inputs=self.assert_refused('source_hash_drift')
        self.assertEqual(sum(v['returned'] for v in boundary['events'] if v['op']=='read'),len(inputs['source_raw']))

    def test_writable_source_refuses_before_descriptor_open(self):
        *_,boundary,inputs=self.assert_refused('source_writable')
        self.assertEqual(boundary['events'],[])

    def test_short_capture_refuses_and_closes_descriptor_once(self):
        *_,boundary,inputs=self.assert_refused('capture_early_eof')
        self.assertEqual(sum(v['returned'] for v in boundary['events'] if v['op']=='read'),17)
        self.assertEqual([v['op'] for v in boundary['events']].count('close_attempt'),1)

    def test_decoder_exception_refuses_after_rewind_and_closes(self):
        *_,boundary,inputs=self.assert_refused('decode_exception')
        self.assertEqual(sum(v['returned'] for v in boundary['events'] if v['op']=='read'),len(inputs['source_raw'])+19)
        self.assertEqual([v['op'] for v in boundary['events']].count('seek'),1)

    def test_measurement_hash_mismatch_refuses_after_both_real_passes(self):
        *_,boundary,inputs=self.assert_refused('measure_bad_hash')
        self.assertEqual(sum(v['returned'] for v in boundary['events'] if v['op']=='read'),2*len(inputs['source_raw']))

    def test_post_close_completion_error_refuses_without_retry(self):
        *_,boundary,inputs=self.assert_refused('close_completion_error')
        self.assertEqual([v['op'] for v in boundary['events']].count('close_attempt'),1)
        self.assertEqual([v['op'] for v in boundary['events']].count('close_returned'),1)


if __name__=='__main__':unittest.main(verbosity=2)
