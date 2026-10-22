"""Genuine retained parent supervision of the isolated synthetic child adapter.

Current preparation, saved-file checks, parent reservation, pipe collection,
watchdog, termination, retained reconciliation and handle closure are real.
The child adapter/callbacks/collection and parent validation finder are explicitly
inert. Its diagnostic is not GDT terminal evidence: even a successful child
handoff must leave the genuine retained receipt at needs_review. All target
files and metadata are invented. Private reads are limited to the existing
fixture's pinned authored control, outer gate and ordinary-I/O snapshots;
no private target or installed inputs. The timeout case injects time, not a
five-minute wait.
"""
import json
from pathlib import Path
import subprocess
import sys
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools import dependency_operational_launcher as parent
import test_dependency_isolated_handoff as isolated
import test_dependency_joined_handoff as joined


OBSERVATIONS = []
TIMEOUT_SUFFIX = rb'''
_completed_synthetic_child=child
def child(request,packet,buffers,rows):
 result=_completed_synthetic_child(request,packet,buffers,rows)
 if result==0:
  with (Path(request['folder'])/'supervisor-timeout-ready').open('xb') as stream:
   stream.write(b'invented child handoff finished; waiting for watchdog')
  sys.stdout.flush()
  time.sleep(60)
 return result
'''


class InertValidationFinder:
    """No core validator is supplied or called for the inert child outcome."""
    def __init__(self):
        self.closed = False
        self.close_attempts = 0
        self.lookups = []

    def find_spec(self, fullname, path=None, target=None):
        self.lookups.append(fullname)
        return None

    def close(self):
        if self.closed:
            raise AssertionError('inert finder closed twice')
        self.close_attempts += 1
        if self in sys.meta_path:
            sys.meta_path.remove(self)
        self.closed = True
        return True


class ParentHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        observed = subprocess.run([sys.executable, '-I', '-S', '-B', '-X', 'utf8',
                                   '-c', parent.PROFILE],
                                  capture_output=True, check=True, timeout=15)
        if observed.stderr:
            raise AssertionError(observed.stderr)
        cls.profile = json.loads(observed.stdout)

    def emergency_reap(self, process):
        """Bound test cleanup after failed supervision; never success evidence."""
        if process.poll() is not None:
            return
        observation = dict(test=self.id(), test_emergency_cleanup=True,
                           child_pid=process.pid, kill_attempts=1, wait_attempts=0)
        try:
            try:
                process.kill()
                observation['kill_succeeded'] = True
            except BaseException as error:
                observation['kill_failure'] = type(error).__name__
            observation['wait_attempts'] = 1
            try:
                observation['child_exit_code'] = process.wait(timeout=5)
            except BaseException as error:
                observation['wait_failure'] = type(error).__name__
            if process.poll() is not None:
                process.stdout.close()
                process.stderr.close()
        finally:
            OBSERVATIONS.append(observation)
        self.fail('test emergency cleanup required; genuine supervisor did not reap child')

    def fixture(self, mode='complete', *, actual_child=False):
        case = joined.JoinedHandoffTests('test_joined_real_preflight_context_control_and_helper_handoff')
        self.addCleanup(case.doCleanups)
        case.fixture_ordinary_io = isolated.DISK_IO
        child_mode = 'complete' if mode == 'timeout' else mode
        case.fixture_child_suffix = (b'' if actual_child else b'\nSYNTHETIC_MODE=' +
                                     repr(child_mode).encode() + b'\n' + isolated.SYNTHETIC_SUFFIX)
        if mode == 'timeout':
            case.fixture_child_suffix += TIMEOUT_SUFFIX
        case.setUp()
        plan = parent.prepare_synthetic_owned(folder=case.folder, packet=case.packet,
            buffers=case.buffers, rows=case.rows, expected_hashes=case.expected,
            runtime_profile=self.profile)
        self.addCleanup(lambda: parent.process.close_owned((plan['adapter'], plan['outer'])))
        plan['control'] = case.checker
        plan['validation'] = InertValidationFinder()
        self.addCleanup(lambda: None if plan['validation'].closed else plan['validation'].close())
        self.assertEqual(plan['context']['child_argv'][7], parent.bootstrap())
        self.assertIs(case.checker.verify_context(plan['context']), True)
        plan['qualification_sources'] = dict(
            bootstrap_sha256=plan['request']['bootstrap_sha256'],
            authored_child_sha256=parent.sha(Path('tools/dependency_operational_child.py').read_bytes()),
            test_adapter_sha256=None if actual_child else parent.sha(case.fixture_child_suffix),
            transported_child_sha256=case.rows['process_child']['sha256'])
        return case, plan

    def supervise(self, case, plan, *, before_spawn=None, spawn_failure=False,
                  partial_parent_failure=False, simulated_deadline=False):
        processes = []
        attempts = []
        handles = []
        open_failures = []
        real_popen = subprocess.Popen
        real_open = Path.open
        session = plan['context']['session_dir']

        def spawn(*args, **kwargs):
            attempts.append((args, kwargs))
            if len(attempts) != 1:
                raise AssertionError('automatic retry attempted')
            if before_spawn is not None:
                before_spawn()
            if spawn_failure:
                raise OSError('invented process creation failure')
            process = real_popen(*args, **kwargs)
            processes.append(process)
            self.addCleanup(self.emergency_reap, process)
            return process

        def tracked_open(path, *args, **kwargs):
            if path.parent == session and args and args[0] == 'xb':
                if partial_parent_failure and path.name == case.checker.PARENT_FILES[1]:
                    open_failures.append(path)
                    raise OSError('invented exclusive output failure')
                handle = real_open(path, *args, **kwargs)
                if path.name in case.checker.PARENT_FILES:
                    handles.append(handle)
                return handle
            return real_open(path, *args, **kwargs)

        marker = plan['folder'] / 'supervisor-timeout-ready'
        def monotonic():
            return time.monotonic() + (301 if simulated_deadline and marker.exists() else 0)
        clock = SimpleNamespace(monotonic=monotonic, sleep=time.sleep)
        with patch.object(parent.subprocess, 'Popen', side_effect=spawn), \
             patch.object(Path, 'open', tracked_open), patch.object(parent, 'time', clock):
            narrow, ownership = parent._supervise(plan)
        # The actual process object and all owned handles are inspected after
        # the genuine supervisor returns; no wait/kill/retry is supplied here.
        self.assertTrue(all(process.poll() is not None for process in processes))
        self.assertTrue(all(process.stdout.closed and process.stderr.closed for process in processes))
        self.assertTrue(all(handle.closed for handle in handles))
        self.assertTrue(plan['validation'].closed)
        self.assertEqual(plan['validation'].close_attempts, 1)
        self.assertNotIn(plan['validation'], sys.meta_path)
        self.assertNotIn('gdt_preflight', plan['validation'].lookups)
        self.assertNotIn('gdt_preflight', sys.modules)
        result = dict(narrow=narrow, ownership=ownership, launch_calls=len(attempts),
                      process_count=len(processes), parent_handle_count=len(handles),
                      exclusive_open_failures=len(open_failures), simulated_deadline=simulated_deadline)
        OBSERVATIONS.append(dict(test=self.id(), sources=plan['qualification_sources'], **result))
        return result

    def assert_incomplete(self, result):
        self.assertEqual(result['narrow']['status'], 'needs_review')
        self.assertEqual(result['narrow']['host_exit_code'], 1)
        self.assertIs(result['narrow']['terminal_records_agree'], False)
        self.assertIs(result['ownership']['parent_validation_closed'], True)
        self.assertIsNone(result['ownership']['cleanup_failure_type'])

    def assert_saved(self, case, plan, result):
        session = plan['context']['session_dir']
        self.assertEqual(json.loads((session / 'host-result.json').read_bytes()), result['narrow'])
        marker = json.loads((session / 'actual-started.json').read_bytes())
        self.assertEqual(marker['operation_id'], plan['context']['operation_id'])
        self.assertEqual(marker['child_argv'], plan['context']['child_argv'])
        events = [json.loads(row) for row in (session / 'host-journal.jsonl').read_bytes().splitlines()]
        self.assertEqual([row['seq'] for row in events], list(range(len(events))))
        self.assertEqual(events[-1]['status'], 'needs_review')
        self.assertEqual((session / 'actual-stderr.txt').read_bytes(), b'')
        self.assertTrue(all((session / name).exists() for name in case.checker.PARENT_FILES))
        self.assertIs(result['narrow']['automatic_retry'], False)
        self.assertEqual(result['narrow']['camera_commands'], [])
        return events

    def test_successful_handoff_is_supervised_without_inventing_terminal_acceptance(self):
        case, plan = self.fixture()
        result = self.supervise(case, plan)
        self.assert_incomplete(result)
        process = result['narrow']['process_observation']
        self.assertEqual((result['launch_calls'], process['launch_attempts'], process['child_exit_code']), (1, 1, 0))
        self.assertEqual((process['kill_attempts'], process['wait_attempts']), (0, 0))
        for field in ('exit_observed', 'reader_threads_joined', 'pipe_close_complete'):
            self.assertIs(process[field], True)
        self.assertIs(process['timed_out'], False)
        self.assertIsNone(result['ownership']['failure_type'])
        self.assertIs(result['ownership']['parent_records_closed'], True)
        self.assertEqual(result['parent_handle_count'], 4)
        self.assert_saved(case, plan, result)
        child = json.loads((plan['context']['session_dir'] / 'actual-stdout.txt').read_bytes())
        self.assertEqual(child['status'], 'synthetic_handoff_complete')
        self.assertEqual(len(child['fresh_refresh_receipts']), 29)
        self.assertEqual(child['record_handles_closed_before_exit'], [True, True])
        self.assertEqual(child['leaked_aliases'], [])
        self.assertEqual(child['events'], ['inert_dispatch', 'inert_collection'])

    def test_current_command_identity_mismatch_refuses_before_reservation(self):
        case, plan = self.fixture()
        plan['context']['operation_id'] = '9' * 32
        before = plan['request_path'].read_bytes()
        with patch.object(parent.subprocess, 'Popen', side_effect=AssertionError('unexpected launch')), \
             self.assertRaisesRegex(ValueError, 'operational_launch_operation'):
            parent._supervise(plan)
        self.assertEqual(plan['request_path'].read_bytes(), before)
        self.assertTrue(all(not (plan['context']['session_dir'] / name).exists()
                            for name in (*case.checker.PARENT_FILES, *case.checker.CHILD_FILES, 'actual-started.json')))

    def test_existing_parent_output_is_preserved_without_launch(self):
        case, plan = self.fixture()
        path = plan['context']['session_dir'] / case.checker.PARENT_FILES[0]
        path.write_bytes(b'invented existing parent evidence')
        result = self.supervise(case, plan)
        self.assert_incomplete(result)
        self.assertEqual(path.read_bytes(), b'invented existing parent evidence')
        self.assertEqual((result['launch_calls'], result['parent_handle_count']), (0, 0))
        self.assertEqual(result['ownership']['failure_type'], 'IoEntryError')
        self.assertIs(result['ownership']['parent_records_closed'], False)
        self.assertFalse((plan['context']['session_dir'] / 'actual-started.json').exists())

    def test_partial_parent_reservation_closes_handle_and_preserves_output(self):
        case, plan = self.fixture()
        result = self.supervise(case, plan, partial_parent_failure=True)
        self.assert_incomplete(result)
        self.assertEqual((result['launch_calls'], result['parent_handle_count'], result['exclusive_open_failures']), (0, 1, 1))
        self.assertEqual(result['ownership']['failure_type'], 'IoEntryError')
        self.assertEqual((plan['context']['session_dir'] / case.checker.PARENT_FILES[0]).read_bytes(), b'')
        self.assertFalse((plan['context']['session_dir'] / 'actual-started.json').exists())

    def test_child_collision_after_parent_reservation_is_preserved(self):
        case, plan = self.fixture()
        path = plan['context']['session_dir'] / case.checker.CHILD_FILES[1]
        def collision():
            with path.open('xb') as stream:
                stream.write(b'invented child collision')
        result = self.supervise(case, plan, before_spawn=collision)
        self.assert_incomplete(result)
        self.assertEqual(result['launch_calls'], 1)
        self.assertEqual(result['narrow']['process_observation']['child_exit_code'], 2)
        self.assertEqual(path.read_bytes(), b'invented child collision')
        child = json.loads((plan['context']['session_dir'] / 'actual-stdout.txt').read_bytes())
        self.assertEqual((child['failure_stage'], child['failure_reason']),
                         ('record_reservation', 'exclusive_reservation_failed'))
        self.assertEqual(child['record_handles_closed_before_exit'], [True])
        self.assertTrue((plan['context']['session_dir'] / case.checker.CHILD_FILES[0]).exists())
        self.assert_saved(case, plan, result)

    def test_child_callback_interrupt_preserves_failure_and_closes_records(self):
        case, plan = self.fixture('callback_interrupt')
        result = self.supervise(case, plan)
        self.assert_incomplete(result)
        self.assertEqual(result['narrow']['process_observation']['child_exit_code'], 2)
        self.assertEqual(result['launch_calls'], 1)
        child = json.loads((plan['context']['session_dir'] / 'actual-stdout.txt').read_bytes())
        self.assertEqual(child['failure_type'], 'KeyboardInterrupt')
        self.assertEqual(child['callback_close_attempts'], 1)
        self.assertEqual(child['record_handles_closed_before_exit'], [True, True])
        self.assertEqual(child['leaked_aliases'], [])
        self.assertIs(result['ownership']['parent_records_closed'], True)
        self.assert_saved(case, plan, result)

    def test_simulated_deadline_kills_and_waits_once_for_real_child(self):
        case, plan = self.fixture('timeout')
        result = self.supervise(case, plan, simulated_deadline=True)
        self.assert_incomplete(result)
        process = result['narrow']['process_observation']
        self.assertTrue((plan['folder'] / 'supervisor-timeout-ready').exists())
        self.assertEqual((result['launch_calls'], process['launch_attempts'], process['kill_attempts'], process['wait_attempts']), (1, 1, 1, 1))
        for field in ('timed_out', 'kill_succeeded', 'exit_observed', 'reader_threads_joined', 'pipe_close_complete'):
            self.assertIs(process[field], True)
        self.assertEqual(process['deadline_seconds'], 300)
        self.assertGreaterEqual(process['elapsed_seconds'], 301)
        self.assertNotEqual(process['child_exit_code'], 0)
        events = self.assert_saved(case, plan, result)
        self.assertEqual([row['status'] for row in events],
                         ['reserved', 'before_spawn', 'spawned', 'deadline', 'before_kill', 'reaped', 'needs_review'])

    def test_unchanged_production_child_is_refused_under_supervision(self):
        case, plan = self.fixture(actual_child=True)
        result = self.supervise(case, plan)
        self.assert_incomplete(result)
        self.assertEqual((result['launch_calls'], result['narrow']['process_observation']['child_exit_code']), (1, 2))
        self.assertEqual(json.loads((plan['context']['session_dir'] / 'actual-stdout.txt').read_bytes()),
                         {'status': 'needs_review', 'camera_commands': []})
        self.assertTrue(all(not (plan['context']['session_dir'] / name).exists() for name in case.checker.CHILD_FILES))
        self.assert_saved(case, plan, result)
        # This generic bootstrap diagnostic proves refusal here. The exact v6
        # reason is covered by the separate isolated REFUSAL_SUFFIX diagnostic.

    def test_spawn_failure_is_single_attempt_and_preserves_parent_journal(self):
        case, plan = self.fixture()
        result = self.supervise(case, plan, spawn_failure=True)
        self.assert_incomplete(result)
        process = result['narrow']['process_observation']
        self.assertEqual((result['launch_calls'], process['launch_attempts'], result['process_count']), (1, 1, 0))
        self.assertIs(process['launch_failed'], True)
        self.assertIs(process['exit_observed'], False)
        self.assertEqual((process['kill_attempts'], process['wait_attempts']), (0, 0))
        self.assertIs(result['ownership']['parent_records_closed'], True)
        self.assert_saved(case, plan, result)

    def test_run_pending_records_incomplete_supervision_and_closes_owned_graph(self):
        case, plan = self.fixture()
        plan['helpers'] = parent.process.helper_owner(plan['outer'], case.buffers, case.rows, 'parent')
        plan['bootstrap'] = parent.BootstrapOwner(plan['outer'].modules['dependency_host_entry'])
        self.addCleanup(lambda: parent.process.close_owned((plan['helpers'], plan['bootstrap'])))
        real_popen = subprocess.Popen
        processes = []
        attempts = []

        def spawn(*args, **kwargs):
            attempts.append((args, kwargs))
            if len(attempts) != 1:
                raise AssertionError('automatic retry attempted')
            process = real_popen(*args, **kwargs)
            processes.append(process)
            self.addCleanup(self.emergency_reap, process)
            return process

        # Neither _supervise nor _reconcile is replaced. The latter must refuse
        # the genuine incomplete terminal result before saved success decoding.
        with patch.object(parent.subprocess, 'Popen', side_effect=spawn):
            result = parent._run_pending(plan)
        self.assertEqual(len(attempts), 1)
        self.assertEqual(len(processes), 1)
        self.assertIsNotNone(processes[0].poll())
        self.assertTrue(processes[0].stdout.closed and processes[0].stderr.closed)
        self.assertEqual(result['status'], 'needs_review')
        self.assertEqual(result['failure_type'], 'ValueError')
        self.assertEqual(result['failure_code'], 'operational_launch_supervision_incomplete')
        self.assertIsNone(result['cleanup_failure_type'])
        self.assertIsNone(result['engine_result'])
        self.assertEqual((result['process']['launch_attempts'], result['process']['child_exit_code']), (1, 0))
        self.assertIs(result['process']['exit_observed'], True)
        self.assertEqual((result['process']['kill_attempts'], result['process']['wait_attempts']), (0, 0))
        for key in ('helpers_closed', 'validation_closed', 'bootstrap_closed', 'adapter_closed', 'outer_closed'):
            self.assertIs(result[key], True, key)
        self.assertEqual(result['supervision'], dict(parent_records_closed=True, parent_validation_closed=True,
                                                    failure_type=None, cleanup_failure_type=None))
        self.assertEqual(plan['validation'].close_attempts, 1)
        self.assertNotIn(plan['validation'], sys.meta_path)
        for key in ('automatic_retry', 'execution_authorized', 'feature_supported', 'recovery_proven', 'device_write_gate_passed'):
            self.assertIs(result[key], False, key)
        self.assertEqual(result['camera_commands'], [])
        self.assertEqual(json.loads((plan['folder'] / 'final-receipt.json').read_bytes()), result)
        host_result = json.loads((plan['context']['session_dir'] / 'host-result.json').read_bytes())
        self.assertIs(host_result['terminal_records_agree'], False)
        self.assertEqual(host_result['process_observation'], result['process'])
        self.assertFalse((plan['folder'] / 'outer-child.json').exists())
        OBSERVATIONS.append(dict(test=self.id(), sources=plan['qualification_sources'],
                                 joined_run_pending=True, launch_calls=len(attempts), result=result))


if __name__ == '__main__':
    unittest.main(verbosity=2)
