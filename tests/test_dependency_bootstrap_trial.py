"""Captured authored sources, invented adapters/events, disposable child files.

One genuine successful child supplies immutable bytes for all pure tamper
checks.  Fault cases each receive a new folder and one child attempt; these
tests never open firmware, native payloads, installed packages or devices.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from tools import dependency_bootstrap_supervisor as supervisor
from tools import dependency_bootstrap_trial as subject


class BootstrapTrialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._temporary = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls._temporary.cleanup)
        cls.root = Path(cls._temporary.name).resolve()
        cls.shared = subject.prepare_invented(cls.root / 'shared-success')
        cls.shared_answer = subject.run_prepared(cls.shared, timeout=10)
        if cls.shared_answer['status'] != 'complete_invented_bootstrap_only':
            raise AssertionError('shared invented bootstrap child did not complete')
        cls.shared_journal = (cls.shared['folder'] / 'journal.jsonl').read_bytes()
        cls.shared_result = (cls.shared['folder'] / 'result.json').read_bytes()
        cls.shared_process = copy.deepcopy(cls.shared_answer['process'])

    def setUp(self):
        self.folder = self.root / self._testMethodName

    def prepare(self, scenario='complete'):
        return subject.prepare_invented(self.folder, scenario=scenario)

    def assert_refused(self, code, function, *args, **kwargs):
        with self.assertRaises(ValueError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.args, (code,))

    def verify(self, *, request=None, journal=None, result=None, process=None):
        return subject.verify_invented(
            request=self.shared['request'] if request is None else request,
            journal=self.shared_journal if journal is None else journal,
            result=self.shared_result if result is None else result,
            process=self.shared_process if process is None else process)

    def tamper_result(self, key, value):
        row = json.loads(self.shared_result)
        row[key] = value
        return subject.canonical(row)

    @staticmethod
    def rewrite_saved_request(prepared):
        # Only invented temporary request metadata is changed, never sources.
        prepared['request_bytes'] = subject.canonical(prepared['request'])
        (prepared['folder'] / 'request.json').write_bytes(prepared['request_bytes'])

    def assert_no_launch(self, prepared, code):
        with patch.object(supervisor.subprocess, 'Popen') as launch:
            self.assert_refused(code, subject.run_prepared, prepared)
            launch.assert_not_called()
        self.assertFalse((prepared['folder'] / 'started.json').exists())

    def assert_success(self, prepared, answer):
        self.assertEqual(answer['status'], 'complete_invented_bootstrap_only')
        process = answer['process']
        self.assertEqual((process['status'], process['returncode']), ('complete', 0))
        self.assertIs(type(process['pid']), int)
        self.assertGreater(process['pid'], 0)
        self.assertNotEqual(process['pid'], os.getpid())
        self.assertTrue(process['process_terminal'])
        self.assertTrue(process['reader_threads_terminal'])
        self.assertTrue(process['stdout_eof'] and process['stderr_eof'])
        self.assertEqual((process['stdout'], process['stderr']), (b'', b''))
        self.assertFalse(process['automatic_retry'] or answer['automatic_retry'])
        self.assertEqual(answer['camera_commands'], [])
        row = json.loads((prepared['folder'] / 'result.json').read_bytes())
        self.assertEqual(row['pid'], process['pid'])
        self.assertEqual((row['isolated'], row['no_site'], row['no_user_site'],
                          row['no_bytecode'], row['optimize']), (1, 1, 1, True, 0))
        self.assertEqual(row['bootstrap_calls'], 1)
        self.assertEqual(row['imports'], list(subject.TRUSTED))
        self.assertEqual(row['origins'], subject.origins())
        self.assertIs(row['adapter_restored'], True)
        self.assertEqual(row['stop'], 'before_package_imports')
        self.assertIs(row['events_are_invented_adapter_declarations'], True)
        self.assertEqual(row['camera_commands'], [])
        for flag in subject.FLAGS:
            self.assertIs(row[flag], False)
            self.assertIs(answer['verification'][flag], False)
        self.assertEqual((prepared['folder'] / 'stdout.bin').read_bytes(), b'')
        self.assertEqual((prepared['folder'] / 'stderr.bin').read_bytes(), b'')
        self.assertEqual({item.name for item in prepared['folder'].iterdir()},
                         {'request.json', 'started.json', 'journal.jsonl', 'result.json',
                          'stdout.bin', 'stderr.bin', 'supervision.json'})
        facts = json.loads((prepared['folder'] / 'supervision.json').read_bytes())
        self.assertEqual(facts['pid'], process['pid'])
        self.assertEqual(facts['trial_status'], answer['status'])
        self.assertEqual((facts['stdout_bytes'], facts['stderr_bytes']), (0, 0))
        self.assertFalse(facts['automatic_retry'])
        return row

    def assert_fault(self, scenario, *, timeout=10):
        prepared = self.prepare(scenario)
        original_launch = supervisor.subprocess.Popen
        with patch.object(supervisor.subprocess, 'Popen', wraps=original_launch) as launch:
            answer = subject.run_prepared(prepared, timeout=timeout)
            self.assertEqual(launch.call_count, 1)
        self.assertEqual(answer['status'], 'needs_review')
        self.assertIsNone(answer['verification'])
        self.assertFalse(answer['automatic_retry'])
        self.assertEqual(answer['camera_commands'], [])
        process = answer['process']
        self.assertEqual(process['status'], 'needs_review')
        self.assertTrue(process['process_terminal'])
        self.assertIs(type(process['pid']), int)
        self.assertGreater(process['pid'], 0)
        self.assertNotEqual(process['pid'], os.getpid())
        self.assertFalse(process['automatic_retry'])
        for stream in ('stdout', 'stderr'):
            self.assertLessEqual(len(process[stream]), 65536)
            self.assertEqual((prepared['folder'] / (stream + '.bin')).read_bytes(), process[stream])
        facts = json.loads((prepared['folder'] / 'supervision.json').read_bytes())
        self.assertEqual(facts['trial_status'], 'needs_review')
        self.assertEqual(facts['pid'], process['pid'])
        self.assertEqual(facts['returncode'], process['returncode'])
        self.assertFalse(facts['automatic_retry'])
        self.assertEqual(facts['stdout_bytes'], len(process['stdout']))
        self.assertEqual(facts['stderr_bytes'], len(process['stderr']))
        self.assertEqual(facts['stdout_sha256'], subject.sha(process['stdout']))
        self.assertEqual(facts['stderr_sha256'], subject.sha(process['stderr']))
        self.assertFalse((prepared['folder'] / 'result.json').exists())
        return prepared, answer

    def assert_partial_journal(self, prepared):
        raw = (prepared['folder'] / 'journal.jsonl').read_bytes()
        self.assertTrue(raw)
        self.assertLessEqual(len(raw), 262144)
        lines = raw.splitlines()
        self.assertLessEqual(len(lines), 256)
        self.assertTrue(all(len(line)+1 <= 4096 for line in lines))
        rows = [json.loads(line) for line in lines]
        self.assertEqual([row['sequence'] for row in rows], list(range(1, len(rows)+1)))
        self.assertNotIn('bootstrap.only_stop', [row['event'] for row in rows])
        self.assertEqual(rows[0]['event'], 'trial.started')
        return rows

    def test_complete_child_is_genuine_isolated_original_method_and_stops(self):
        row = self.assert_success(self.shared, self.shared_answer)
        self.assertEqual(row['journal_events'], 14)
        self.assertEqual(self.verify()['status'], 'consistent_invented_bootstrap_only')
        events = [json.loads(line) for line in self.shared_journal.splitlines()]
        self.assertEqual(events[-1]['event'], 'bootstrap.only_stop')
        self.assertEqual([row['arguments']['items'][0] for row in events
                          if row['event'] == 'invented.native'],
                         [{'type': 'none'}, {'type': 'str', 'value': 'kernel32'}])

    def test_no_native_events_are_optional_invented_declarations(self):
        prepared = self.prepare('no_native_events')
        answer = subject.run_prepared(prepared, timeout=10)
        row = self.assert_success(prepared, answer)
        self.assertEqual(row['journal_events'], 12)
        events = [json.loads(line)['event'] for line in (self.folder/'journal.jsonl').read_bytes().splitlines()]
        self.assertNotIn('invented.native', events)

    def test_reversed_native_events_do_not_claim_a_fixed_observed_order(self):
        prepared = self.prepare('reversed_native_events')
        answer = subject.run_prepared(prepared, timeout=10)
        self.assert_success(prepared, answer)
        events = [json.loads(line) for line in (self.folder/'journal.jsonl').read_bytes().splitlines()]
        self.assertEqual([row['arguments']['items'][0] for row in events
                          if row['event'] == 'invented.native'],
                         [{'type': 'str', 'value': 'kernel32'}, {'type': 'none'}])

    def test_duplicate_native_event_stops_and_preserves_partial_journal(self):
        prepared, _ = self.assert_fault('duplicate_native_event')
        self.assertEqual(len(self.assert_partial_journal(prepared)), 3)

    def test_unexpected_native_argument_stops_and_preserves_partial_journal(self):
        prepared, _ = self.assert_fault('unexpected_native_event')
        self.assertEqual(len(self.assert_partial_journal(prepared)), 2)

    def test_origin_drift_stops_before_stop_record(self):
        prepared, _ = self.assert_fault('origin_drift')
        self.assert_partial_journal(prepared)

    def test_extra_import_stops_before_stop_record(self):
        prepared, _ = self.assert_fault('extra_import')
        self.assert_partial_journal(prepared)

    def test_actual_native_audit_event_is_denied(self):
        prepared, _ = self.assert_fault('actual_native_event')
        self.assert_partial_journal(prepared)

    def test_package_import_is_denied_in_the_inert_adapter(self):
        prepared, _ = self.assert_fault('package_import')
        self.assert_partial_journal(prepared)

    def test_stdout_flood_retains_at_most_cap_and_no_completed_trial(self):
        prepared, answer = self.assert_fault('stdout_flood')
        self.assertTrue(answer['process']['stdout_overflow'])
        self.assertEqual(answer['process']['stdout'], b'x'*65536)
        self.assertFalse((prepared['folder']/'journal.jsonl').exists())

    def test_stderr_flood_retains_at_most_cap_and_no_completed_trial(self):
        prepared, answer = self.assert_fault('stderr_flood')
        self.assertTrue(answer['process']['stderr_overflow'])
        self.assertEqual(answer['process']['stderr'], b'x'*65536)
        self.assertFalse((prepared['folder']/'journal.jsonl').exists())

    def test_stall_timeout_terminates_once_and_records_known_completion(self):
        start = time.monotonic()
        prepared, answer = self.assert_fault('stall', timeout=0.25)
        self.assertTrue(answer['process']['timed_out'])
        self.assertTrue(answer['process']['cleanup']['kill_attempted'])
        self.assertTrue(answer['process']['cleanup']['reap_attempted'])
        self.assertLess(time.monotonic()-start, 6)
        self.assertFalse((prepared['folder']/'journal.jsonl').exists())

    def test_nonzero_child_exit_is_preserved_without_result(self):
        prepared, answer = self.assert_fault('nonzero')
        self.assertEqual(answer['process']['returncode'], 2)
        self.assertEqual(answer['process']['stderr'], b'invented_bootstrap_needs_review\n')
        self.assertFalse((prepared['folder']/'journal.jsonl').exists())

    def test_journal_flood_preserves_exact_cap_without_stop_or_retry(self):
        prepared, _ = self.assert_fault('journal_flood')
        rows = self.assert_partial_journal(prepared)
        self.assertEqual(len(rows), 256)
        self.assertEqual(rows[-1]['event'], 'invented.flood')

    def test_bad_serialization_preserves_started_event_without_object_repr(self):
        prepared, answer = self.assert_fault('bad_serialization')
        self.assertEqual(len(self.assert_partial_journal(prepared)), 1)
        self.assertEqual(answer['process']['stderr'], b'invented_bootstrap_needs_review\n')

    def test_saved_request_tamper_refuses_before_process_and_started_record(self):
        prepared = self.prepare()
        (prepared['folder']/'request.json').write_bytes(prepared['request_bytes']+b' ')
        self.assert_no_launch(prepared, 'trial_saved_request')

    def test_source_hash_drift_refuses_before_process(self):
        prepared = self.prepare()
        prepared['request']['sources']['producer']['sha256'] = '0'*64
        self.rewrite_saved_request(prepared)
        self.assert_no_launch(prepared, 'trial_source_changed')

    def test_source_receipt_identity_drift_refuses_before_process(self):
        prepared = self.prepare()
        prepared['request']['sources']['journal']['fstat'][1] += 1
        self.rewrite_saved_request(prepared)
        self.assert_no_launch(prepared, 'trial_source_changed')

    def test_source_root_drift_refuses_before_process(self):
        prepared = self.prepare()
        prepared['request']['source_roots'][-1][2] += 1
        self.rewrite_saved_request(prepared)
        self.assert_no_launch(prepared, 'trial_roots_changed')

    def test_request_authority_promotion_refuses_before_process(self):
        prepared = self.prepare()
        prepared['request']['execution_authorized'] = True
        self.rewrite_saved_request(prepared)
        self.assert_no_launch(prepared, 'trial_request_mode')

    def test_second_attempt_refuses_existing_started_record_before_process(self):
        with patch.object(supervisor.subprocess, 'Popen') as launch:
            with self.assertRaises(FileExistsError):
                subject.run_prepared(self.shared)
            launch.assert_not_called()
        self.assertEqual((self.shared['folder']/'journal.jsonl').read_bytes(), self.shared_journal)
        self.assertEqual((self.shared['folder']/'result.json').read_bytes(), self.shared_result)

    def test_result_duplicate_keys_cannot_hide_behind_json_decoding(self):
        duplicate = b'{"schema":"invented_bootstrap_only_result_v1",' + self.shared_result[1:]
        self.assert_refused('trial_result', self.verify, result=duplicate)

    def test_result_authority_flags_cannot_be_promoted(self):
        for flag in subject.FLAGS:
            with self.subTest(flag=flag):
                self.assert_refused('trial_result', self.verify, result=self.tamper_result(flag, True))

    def test_result_source_hash_must_match_captured_request(self):
        row = json.loads(self.shared_result)
        row['source_sha256']['producer'] = '0'*64
        self.assert_refused('trial_result', self.verify, result=subject.canonical(row))

    def test_result_pid_must_match_genuinely_observed_child(self):
        self.assert_refused('trial_result', self.verify,
                            result=self.tamper_result('pid', self.shared_process['pid']+1))

    def test_result_origin_drift_is_not_freshness_or_native_evidence(self):
        row = json.loads(self.shared_result)
        row['origins']['platform'] = 'X:/invented-runtime/wrong.py'
        self.assert_refused('trial_result', self.verify, result=subject.canonical(row))

    def test_result_stop_must_precede_package_imports(self):
        self.assert_refused('trial_result', self.verify,
                            result=self.tamper_result('stop', 'after_package_imports'))

    def test_result_import_order_cannot_be_rewritten(self):
        self.assert_refused('trial_result', self.verify,
                            result=self.tamper_result('imports', list(reversed(subject.TRUSTED))))

    def test_missing_journal_event_refuses(self):
        lines = self.shared_journal.splitlines(keepends=True)
        self.assert_refused('trial_journal', self.verify, journal=b''.join(lines[:2]+lines[3:]))

    def test_duplicate_journal_event_refuses(self):
        lines = self.shared_journal.splitlines(keepends=True)
        self.assert_refused('trial_journal', self.verify, journal=b''.join(lines[:2]+[lines[1]]+lines[2:]))

    def test_reordered_journal_events_refuse(self):
        lines = self.shared_journal.splitlines(keepends=True)
        lines[1], lines[2] = lines[2], lines[1]
        self.assert_refused('trial_journal', self.verify, journal=b''.join(lines))

    def test_oversized_journal_line_and_aggregate_refuse(self):
        for raw in (b'x'*4096+b'\n', b'\n'*262145):
            self.assert_refused('trial_journal', self.verify, journal=raw)

    def test_oversized_result_refuses_before_json_decoding(self):
        self.assert_refused('trial_result_bound', self.verify,
                            result=self.shared_result+b' '*65536)

    def test_process_failure_or_output_cannot_be_promoted_by_valid_saved_result(self):
        for key, value in (('status', 'needs_review'), ('returncode', 7),
                           ('stdout', b'ordinary output'), ('stderr', b'ordinary error')):
            process = copy.deepcopy(self.shared_process)
            process[key] = value
            with self.subTest(key=key):
                self.assert_refused('trial_process', self.verify, process=process)

    def test_fault_request_cannot_claim_a_complete_saved_result(self):
        request = copy.deepcopy(self.shared['request'])
        request['scenario'] = 'duplicate_native_event'
        self.assert_refused('trial_fault_cannot_complete', self.verify, request=request)

    def test_public_runtime_refuses_without_effects(self):
        with patch.object(supervisor.subprocess, 'Popen') as launch, \
             patch.object(Path, 'open') as opening:
            self.assert_refused('real_activation_pending', subject.run_runtime,
                                request=self.shared['request'])
            launch.assert_not_called()
            opening.assert_not_called()

    def test_ordinary_cli_refuses_without_output(self):
        result = subprocess.run([sys.executable, '-I', '-S', '-B', '-X', 'utf8',
                                 str(Path(subject.__file__).resolve())],
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((result.stdout, result.stderr), (b'', b''))


if __name__ == '__main__':
    unittest.main()
