"""Authored source buffers only; no installed dependency/cache/firmware inputs."""
import copy
import inspect
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

from tools import dependency_child_entry as subject


class ChildEntryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Independently observe the fresh child's ordinary runtime metadata first;
        # freeze it before the separate authored-source preflight invocation.
        code = 'import sys,json\n'+inspect.getsource(subject.runtime_profile)+'\nprint(json.dumps(runtime_profile()))'
        result = subprocess.run([sys.executable, '-I', '-S', '-B', '-X', 'utf8', '-c', code],
            capture_output=True, text=True, timeout=15)
        if result.returncode: raise AssertionError(result.stderr)
        cls.profile = json.loads(result.stdout)
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'authored'; self.root.mkdir()
        actual = Path(subject.__file__).parent
        for name in subject.FILES.values(): shutil.copyfile(actual/name, self.root/name)
        self.folder = Path(self.temp.name)/'attempt'
    def freeze(self):
        return subject.freeze_request(source_root=str(self.root), expected_runtime=self.profile, review_sha256='c'*64)
    def run_child(self, request): return subject.run_preflight(request=request, folder=self.folder)
    def test_exact_source_buffers_and_runtime_acknowledge_without_dependencies(self):
        request = self.freeze(); before = copy.deepcopy(request); receipt = self.run_child(request)
        self.assertEqual(request, before)
        self.assertEqual((receipt['status'], receipt['exit_code'], receipt['termination']),
                         ('authored_source_child_preflight_complete', 0, 'reaped'))
        result = receipt['result']; self.assertTrue(result['audit_hook_acknowledged'])
        self.assertTrue(result['exact_child_source_buffers_executed'])
        for key in ('parent_execution_authenticated','prior_review_proven','installed_dependency_bootstrap_performed',
                    'actual_dependency_observation_performed','execution_authorized','feature_supported',
                    'recovery_proven','device_write_gate_passed'):
            self.assertIs(result[key], False)
        self.assertEqual(result['camera_commands'], [])
    def test_every_source_is_checked_before_entry_executes(self):
        sentinel = Path(self.temp.name)/'must-not-exist'
        entry = self.root/subject.FILES['entry']
        with entry.open('a', encoding='utf-8') as out: out.write('\nPath('+repr(str(sentinel))+').write_text("unexpected")\n')
        request = self.freeze()
        with (self.root/subject.FILES['producer']).open('a', encoding='utf-8') as out: out.write('\n# changed\n')
        receipt = self.run_child(request)
        self.assertEqual(receipt['status'], 'needs_review'); self.assertEqual(receipt['exit_code'], 2)
        self.assertFalse(sentinel.exists()); self.assertIsNone(receipt['result'])
    def test_runtime_substitution_refuses_before_entry_executes(self):
        sentinel = Path(self.temp.name)/'must-not-exist'
        entry = self.root/subject.FILES['entry']
        with entry.open('a', encoding='utf-8') as out: out.write('\nPath('+repr(str(sentinel))+').write_text("unexpected")\n')
        request = self.freeze(); request['expected_runtime']['optimize'] = 1
        receipt = self.run_child(request)
        self.assertEqual(receipt['status'], 'needs_review'); self.assertFalse(sentinel.exists())
    def test_path_roster_substitution_refuses(self):
        request = self.freeze(); request['sources']['core']['path'] = request['sources']['entry']['path']
        receipt = self.run_child(request); self.assertEqual(receipt['status'], 'needs_review')
    def test_source_identity_substitution_refuses(self):
        request = self.freeze(); request['sources']['core']['lstat'][1] += 1
        receipt = self.run_child(request); self.assertEqual(receipt['status'], 'needs_review')
    def test_root_identity_substitution_refuses(self):
        request = self.freeze(); request['source_root_identity'][-1][2] += 1
        receipt = self.run_child(request); self.assertEqual(receipt['status'], 'needs_review')
    def test_missing_source_role_refuses(self):
        request = self.freeze(); del request['sources']['producer']
        receipt = self.run_child(request); self.assertEqual(receipt['status'], 'needs_review')
    def test_existing_attempt_is_never_overwritten_or_relaunched(self):
        request = self.freeze(); self.folder.mkdir(); sentinel = self.folder/'sentinel'; sentinel.write_bytes(b'preserve')
        with patch.object(subject.subprocess, 'Popen') as popen:
            with self.assertRaises(FileExistsError): self.run_child(request)
        popen.assert_not_called(); self.assertEqual(sentinel.read_bytes(), b'preserve')
    def test_invalid_timeout_refuses_before_output_or_spawn(self):
        request = self.freeze()
        for timeout in (0, True, -1, 31):
            with self.subTest(timeout=timeout), patch.object(subject.subprocess, 'Popen') as popen:
                with self.assertRaisesRegex(ValueError, '^timeout_bound$'):
                    subject.run_preflight(request=request, folder=self.folder, timeout=timeout)
                popen.assert_not_called(); self.assertFalse(self.folder.exists())
    def test_timeout_is_terminated_once_and_not_accepted(self):
        request = self.freeze()
        with patch.object(subject.subprocess, 'Popen') as popen:
            process = popen.return_value; process.pid = 123
            process.wait.side_effect = [subprocess.TimeoutExpired('invented', 1), -9]
            receipt = subject.run_preflight(request=request, folder=self.folder, timeout=1)
        self.assertEqual(receipt['status'], 'needs_review')
        self.assertEqual(receipt['termination'], 'terminated_after_timeout')
        process.kill.assert_called_once(); self.assertEqual(process.wait.call_count, 2); popen.assert_called_once()
    def test_unreaped_process_requires_reconciliation_without_restart(self):
        request = self.freeze()
        with patch.object(subject.subprocess, 'Popen') as popen:
            process = popen.return_value; process.pid = 123
            process.wait.side_effect = subprocess.TimeoutExpired('invented', 1)
            receipt = self.run_child(request)
        self.assertEqual(receipt['termination'], 'needs_process_reconciliation')
        self.assertEqual(receipt['status'], 'needs_review'); self.assertEqual(receipt['child_pid'], 123)
        process.kill.assert_called_once(); popen.assert_called_once()
    def test_spawn_failure_is_preserved_and_not_retried(self):
        with patch.object(subject.subprocess, 'Popen', side_effect=OSError('invented')) as popen:
            receipt = self.run_child(self.freeze())
        self.assertEqual(receipt['status'], 'needs_review'); self.assertIsNone(receipt['child_pid'])
        popen.assert_called_once(); self.assertTrue((self.folder/'completion.json').exists())
    def test_interrupted_wait_terminates_and_reaps_once(self):
        request = self.freeze()
        with patch.object(subject.subprocess, 'Popen') as popen:
            process = popen.return_value; process.pid = 123
            process.wait.side_effect = [KeyboardInterrupt(), -9]
            receipt = self.run_child(request)
        self.assertEqual(receipt['termination'], 'terminated_after_interruption')
        self.assertEqual(receipt['status'], 'needs_review'); process.kill.assert_called_once()
        self.assertEqual(process.wait.call_count, 2); popen.assert_called_once()
    def test_interrupted_cleanup_failure_retains_uncertain_process(self):
        request = self.freeze()
        with patch.object(subject.subprocess, 'Popen') as popen:
            process = popen.return_value; process.pid = 123
            process.wait.side_effect = KeyboardInterrupt(); process.kill.side_effect = OSError('invented kill failure')
            receipt = self.run_child(request)
        self.assertEqual(receipt['termination'], 'needs_process_reconciliation')
        self.assertEqual(receipt['status'], 'needs_review'); self.assertEqual(receipt['child_pid'], 123)
        process.kill.assert_called_once(); process.wait.assert_called_once(); popen.assert_called_once()
    def fake_process(self, raw, stderr_raw=b''):
        def popen(argv, **kwargs):
            kwargs['stdout'].write(raw); kwargs['stderr'].write(stderr_raw)
            process = MagicMock(); process.pid = 123; process.wait.return_value = 0
            return process
        return popen
    def valid_result(self, request):
        return dict(schema='dependency_child_preflight_result_v1', status='authored_source_child_preflight_complete',
            request_sha256=subject.sha(subject.canonical(request)),
            source_sha256={role: row['sha256'] for role, row in request['sources'].items()},
            runtime_profile=request['expected_runtime'], audit_hook_acknowledged=True, audit_hook_retained_inert=True,
            exact_child_source_buffers_executed=True, parent_execution_authenticated=False, prior_review_proven=False,
            installed_dependency_bootstrap_performed=False, actual_dependency_observation_performed=False,
            operational_acceptance=False, execution_authorized=False, feature_supported=False,
            recovery_proven=False, device_write_gate_passed=False, camera_commands=[])
    def test_promoted_flags_extra_fields_wrong_runtime_or_ack_are_not_accepted(self):
        request = self.freeze()
        for key, value in [('execution_authorized', True), ('feature_supported', True),
            ('installed_dependency_bootstrap_performed', True), ('audit_hook_acknowledged', False),
            ('runtime_profile', {}), ('extra', False), ('parent_execution_authenticated', 0)]:
            with self.subTest(key=key):
                self.folder = Path(self.temp.name)/key
                result = self.valid_result(request); result[key] = value
                with patch.object(subject.subprocess, 'Popen', self.fake_process(subject.canonical(result))):
                    receipt = self.run_child(request)
                self.assertEqual(receipt['status'], 'needs_review'); self.assertIsNone(receipt['result'])
    def test_invalid_duplicate_or_oversized_output_retains_completion_receipt(self):
        request = self.freeze(); valid = subject.canonical(self.valid_result(request))
        cases = [b'{invalid', valid[:-1]+b',"execution_authorized":false}', b'x'*65537,
                 b'['*2000+b']'*2000]
        for index, raw in enumerate(cases):
            with self.subTest(index=index):
                self.folder = Path(self.temp.name)/str(index)
                with patch.object(subject.subprocess, 'Popen', self.fake_process(raw)):
                    receipt = self.run_child(request)
                self.assertEqual(receipt['status'], 'needs_review'); self.assertIsNone(receipt['result'])
                self.assertTrue((self.folder/'completion.json').exists())
    def test_missing_output_is_recorded_as_needs_review(self):
        request = self.freeze(); original = subject.read_source
        def read(path, **kwargs):
            if Path(path).name == 'stdout.json': raise FileNotFoundError('invented disappearance')
            return original(path, **kwargs)
        with patch.object(subject.subprocess, 'Popen', self.fake_process(b'{}')), patch.object(subject, 'read_source', read):
            receipt = self.run_child(request)
        self.assertEqual(receipt['status'], 'needs_review'); self.assertTrue((self.folder/'completion.json').exists())
    def test_review_digest_is_declaration_but_must_be_well_formed(self):
        with self.assertRaisesRegex(ValueError, '^review_digest$'):
            subject.freeze_request(source_root=str(self.root), expected_runtime=self.profile, review_sha256='invalid')
    def test_hardlinked_source_is_refused(self):
        path = self.root/subject.FILES['core']; os.link(path, self.root/'second-name')
        with self.assertRaisesRegex(ValueError, '^source_kind$'): self.freeze()
    def test_cli_refuses_without_reading_any_inputs(self):
        with patch('builtins.print') as out: self.assertEqual(subject.main(), 2)
        self.assertEqual(json.loads(out.call_args.args[0])['code'], 'real_activation_pending')


if __name__ == '__main__': unittest.main()
