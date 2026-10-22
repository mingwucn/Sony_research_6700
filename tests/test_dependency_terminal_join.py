"""Real validator/supervisor/saved join over fresh generated, replayed terminals.

The generator executes genuine authored pure runner/gates over invented logical
bytes and source events. An isolated, separately pinned adapter replays those
records; dependency/bridge records and outer-child flags are fixture data. The
child checks synthetic preparation but does not execute its callback factory or
Preparation.prepare. This is contract integration, not authenticated producer
execution or actual firmware/dependency observation.
"""
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

from tools import dependency_operational_launcher as parent
import test_dependency_joined_handoff as joined
import test_dependency_saved_handoff as saved
import test_dependency_parent_handoff as parent_handoff
from dependency_terminal_fixture import FreshTerminal


REPLAY_SUFFIX=rb'''
def child(request,packet,buffers,rows):
 import os
 root=Path(packet['repository_root']);owned=None;records=None;control=None;primary=None
 def audit(event,args):
  if event.startswith(('socket.','ctypes.')) or event=='subprocess.Popen':
   raise AssertionError('synthetic terminal replay forbids network/native/execution')
  if event=='import' and args[0].split('.')[0] in ('tools','ctypes','_ctypes','Crypto','Cryptodome','cffi','_cffi_backend'):
   raise AssertionError('synthetic terminal replay forbids installed imports')
  if event=='open' and isinstance(args[0],str):
   path=Path(args[0])
   assert path.is_relative_to(root) or path.is_relative_to(Path(sys.base_prefix)), 'outside invented tree/stdlib'
 sys.addaudithook(audit)
 try:
  owned=prepare_synthetic_owned(request=request,packet=packet,buffers=buffers,rows=rows,
   request_bytes=encoded(request),expected_request_sha256=sys.argv[2],request_path=sys.argv[1])
  host=owned['outer'].modules['dependency_host_entry']
  control=host.cached_module('_synthetic_terminal_control',buffers['bound.bootstrap:io_entry'],rows['bound.bootstrap:io_entry']['path'])
  records=control.reserve_child(context=owned['context'])
  replay=Path(request['folder'])/'synthetic-terminal'
  for name in control.CHILD_FILES:
   raw=control.read_ordinary(replay/name,root,control.CHILD_RESULT_BYTE_CAP)
   control.durable(records.handles[name],raw)
  assert records.close() is True
  stdout=control.read_ordinary(replay/'summary.json',root,16384)
 except BaseException as error:primary=error
 finally:
  cleanup=None
  try:
   if records is not None and not records.closed:records.close()
  except BaseException as error:cleanup=error
  try:
   if control is not None:
    assert sys.modules.get('_synthetic_terminal_control') is control,'control ownership changed'
    del sys.modules['_synthetic_terminal_control']
  except BaseException as error:
   if cleanup is None:cleanup=error
  try:
   if owned is not None:close_owned((owned['preparation'],owned['helpers'],owned['adapter'],owned['outer']))
  except BaseException as error:
   if cleanup is None:cleanup=error
  if primary is not None and cleanup is not None:raise primary from cleanup
  if cleanup is not None:raise cleanup
 if primary is not None:raise primary
 sys.stdout.buffer.write(stdout);sys.stdout.buffer.flush()
 return 0
'''

OBSERVATIONS=[]


class GeneratorRecords:
    """Fresh ordinary files, independent of the later exclusive child outputs."""
    def __init__(self,folder,names):
        self.handles={};self.closed=False
        try:
            for name in names:self.handles[name]=(folder/name).open('xb')
        except BaseException:
            self.close();raise
    def close(self):
        if self.closed:return True
        self.closed=True
        for stream in self.handles.values():stream.close()
        return True


class TerminalJoinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        observed=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',parent.PROFILE],
            capture_output=True,check=True,timeout=15)
        if observed.stderr:raise AssertionError(observed.stderr)
        cls.profile=json.loads(observed.stdout)

    emergency_reap=parent_handoff.ParentHandoffTests.emergency_reap

    def fixture(self,mode='complete'):
        with FreshTerminal() as terminal:
            case=joined.JoinedHandoffTests('test_joined_real_preflight_context_control_and_helper_handoff')
            case.fixture_basis=terminal.basis;case.fixture_source_manifest=terminal.source_manifest
            case.fixture_role_sources=terminal.role_sources;case.fixture_role_aliases=terminal.aliases
            case.fixture_factory=terminal.factory_raw
            case.fixture_child_suffix=REPLAY_SUFFIX
            fixture=saved.SavedHandoffTests('test_full_saved_chain_rereads_original_preflight_and_real_helper_metadata')
            fixture.fixture_case=case;fixture.fixture_runtime_profile=self.profile
            self.addCleanup(fixture.doCleanups);fixture.setUp()
            plan=fixture.plan;control=terminal.control;folder=plan['folder']/'synthetic-terminal';folder.mkdir()
            records=GeneratorRecords(folder,control.CHILD_FILES);self.addCleanup(records.close)
            code,summary=control.run_child_reserved(context=plan['context'],records=records,
                make_callbacks=terminal.make_callbacks,monotonic=time.monotonic,
                identity=dict(operation_id=plan['request']['operation_id'],isolated=True,optimized=False,camera_commands=[]))
            self.assertEqual(code,0,summary)
            self.assertEqual(summary['status'],'complete_private_gdt_descriptor_metadata_observation')
            self.assertTrue(records.closed)
            raw=control.encoded(summary,16384)
            if mode in ('core_claim','snapshot'):
                result=json.loads((folder/'observation-result.json').read_bytes())
                if mode=='core_claim':
                    key=next(iter(result['runner_result']['claims']));result['runner_result']['claims'][key]=True
                else:
                    result['adapter_snapshot']['phase_a']['capture']['read_calls']+=1
                    result['adapter_snapshot']['phase_a']['capture']['read_attempts']+=1
                result_raw=control.encoded(result);fixture.rewrite(folder/'observation-result.json',result_raw)
                summary['result_sha256']=parent.sha(result_raw);raw=control.encoded(summary,16384)
                lines=(folder/'observation-journal.jsonl').read_bytes().splitlines()
                last=json.loads(lines[-1]);last['summary']=summary
                fixture.rewrite(folder/'observation-journal.jsonl',b''.join(line+b'\n' for line in lines[:-1])+control.encoded(last))
            if mode=='stdout':raw+=b'\n'
            fixture.write(folder/'summary.json',raw)
            self.assertFalse(any(n in sys.modules for n in ('_disabled_parent_control','_disabled_parent_factory')))
        # Fresh generator closes its role imports before the genuine parent
        # finder owns those aliases; no preloaded validator is accepted here.
        self.assertNotIn('gdt_preflight',sys.modules)
        plan['bootstrap']=parent.BootstrapOwner(plan['outer'].modules['dependency_host_entry'])
        self.addCleanup(lambda:None if plan['bootstrap'].closed else plan['bootstrap'].close())
        plan['control']=plan['bootstrap'].load('_disabled_parent_control',case.buffers['bound.bootstrap:io_entry'],
            case.rows['bound.bootstrap:io_entry']['path'])
        factory=plan['bootstrap'].load('_disabled_parent_factory',case.buffers['bound.integration:prospective_child'],
            case.rows['bound.integration:prospective_child']['path'])
        plan['validation']=parent.parent_validation_sources(plan['validated'],plan['outer'].modules['retained_gate'],
            plan['outer'].modules['ordinary_io'],factory)
        self.addCleanup(lambda:None if plan['validation'].closed else plan['validation'].close())
        self.assertEqual(len(plan['validation'].entries),23)
        # Preserve initial invented fixture outputs before rebinding canonical
        # terminal stdout. These files were never observed parent logs.
        original=plan['context']['session_dir']/'actual-stdout.txt'
        original.rename(plan['folder']/'fixture-stdout-before-terminal.txt')
        controller=Path(plan['prepared']['folder'])/'controller-result.json'
        value=json.loads(controller.read_bytes());value['summary']=json.loads(raw)
        if mode=='bridge':value['code']=True
        controller.rename(plan['folder']/'fixture-controller-before-terminal.json')
        fixture.write(controller,value)
        fixture.terminal['evidence']['bridge_sha256']['controller-result.json']=parent.sha(controller.read_bytes())
        fixture.terminal['evidence']['stdout_sha256']=parent.sha(raw)
        child=plan['folder']/'outer-child.json';child.rename(plan['folder']/'fixture-outer-child-before-terminal.json')
        fixture.write(child,fixture.terminal)
        return fixture,plan

    def run_join(self,mode):
        fixture,plan=self.fixture(mode);real_popen=subprocess.Popen;processes=[]
        def spawn(*args,**kwargs):
            self.assertFalse(processes,'automatic retry')
            process=real_popen(*args,**kwargs);processes.append(process)
            self.addCleanup(self.emergency_reap,process)
            return process
        with patch.object(parent.subprocess,'Popen',side_effect=spawn), \
             patch.object(plan['control'],'_validate_core',wraps=plan['control']._validate_core) as core_check:
            answer=parent._run_pending(plan)
        self.assertEqual(core_check.call_count,0 if mode=='stdout' else 1)
        self.assertEqual('gdt_preflight' in plan['validation'].loaded,mode!='stdout')
        self.assertEqual(len(processes),1)
        self.assertIsNotNone(processes[0].poll())
        self.assertTrue(processes[0].stdout.closed and processes[0].stderr.closed)
        for name in ('helpers','validation','bootstrap','adapter','outer'):self.assertTrue(plan[name].closed,name)
        self.assertEqual(set(plan['bootstrap'].modules),{'_disabled_parent_control','_disabled_parent_factory'})
        self.assertFalse(any(n in sys.modules for n in ('gdt_preflight','_disabled_parent_control','_disabled_parent_factory')))
        self.assertEqual(json.loads((plan['folder']/'final-receipt.json').read_bytes()),answer)
        narrow=json.loads((plan['context']['session_dir']/'host-result.json').read_bytes())
        self.assertEqual(narrow['process_observation'],answer['process'])
        for key in ('execution_authorized','feature_supported','recovery_proven','device_write_gate_passed','automatic_retry'):
            self.assertIs(answer[key],False,key)
        self.assertEqual(answer['camera_commands'],[])
        OBSERVATIONS.append(dict(test=self.id(),mode=mode,answer=answer,narrow=narrow,
            terminal_replay=True,source_events_and_snapshot_invented=True,camera_commands=[]))
        return answer,narrow

    def test_genuine_loaded_validator_supervisor_and_saved_chain_join(self):
        answer,narrow=self.run_join('complete')
        self.assertEqual(narrow['host_exit_code'],0)
        self.assertIs(narrow['terminal_records_agree'],True)
        self.assertEqual(answer['status'],'consistent_pending_composition')
        self.assertIsNone(answer['failure_type']);self.assertIsNone(answer['cleanup_failure_type'])
        result=answer['engine_result']['engine_result']
        self.assertEqual(result['status'],'consistent_saved_controller')
        for key in ('actual_runtime_verified','producer_execution_authenticated','historical_truth_verified','operational_acceptance'):
            self.assertIs(result[key],False,key)

    def test_noncanonical_stdout_refuses_even_when_decoded_summary_matches(self):
        answer,narrow=self.run_join('stdout')
        self.assertEqual((narrow['host_exit_code'],answer['status']),(1,'needs_review'))
        self.assertEqual(answer['failure_code'],'operational_launch_supervision_incomplete')

    def test_coherently_rehashed_core_authority_claim_refuses(self):
        answer,narrow=self.run_join('core_claim')
        self.assertEqual((narrow['host_exit_code'],answer['status']),(1,'needs_review'))
        self.assertIs(narrow['terminal_records_agree'],False)

    def test_coherently_rehashed_snapshot_transcript_mismatch_refuses(self):
        answer,narrow=self.run_join('snapshot')
        self.assertEqual((narrow['host_exit_code'],answer['status']),(1,'needs_review'))

    def test_narrow_terminal_success_does_not_override_bridge_refusal(self):
        answer,narrow=self.run_join('bridge')
        self.assertEqual(narrow['host_exit_code'],0)
        self.assertEqual(answer['status'],'needs_review')
        self.assertEqual(answer['failure_code'],'parent_result')


if __name__=='__main__':unittest.main(verbosity=2)
