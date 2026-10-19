"""Complete invented producer in exact-buffer children; no installed inputs."""
import copy
import inspect
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from tools import dependency_child_entry as entry
from tools import dependency_invented as invented
from test_dependency_producer import fixture


class CompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        code = 'import sys,json\n'+inspect.getsource(entry.runtime_profile)+'\nprint(json.dumps(runtime_profile()))'
        run = subprocess.run([sys.executable, '-I', '-S', '-B', '-X', 'utf8', '-c', code],
                             capture_output=True, text=True, timeout=15)
        if run.returncode: raise AssertionError(run.stderr)
        cls.profile = json.loads(run.stdout)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'authored'; self.root.mkdir()
        for name in entry.COMPOSITION_FILES.values():
            shutil.copyfile(Path(entry.__file__).parent/name, self.root/name)
        self.folder = Path(self.temp.name)/'attempt'
        self.path = Path(self.temp.name)/'invented-packet.json'
        self.buffers = {k: (self.root/v).read_bytes() for k, v in entry.COMPOSITION_FILES.items()}
        self.data, self.ops = fixture()
        self.value = invented.packet(self.data, self.ops, self.buffers, 'c'*64)
        self.fixed = invented.expectations(self.value)

    def freeze(self):
        raw = entry.canonical(self.value)
        with self.path.open('xb') as out: out.write(raw)
        return entry.freeze_composition(source_root=self.root, expected_runtime=self.profile,
            review_sha256='c'*64, packet_path=self.path, packet_sha256=entry.sha(raw), fixed=self.fixed)

    def run_child(self, request):
        return entry.run_preflight(request=request, folder=self.folder)

    def assert_refused(self, request, *, no_producer=True):
        receipt = self.run_child(request)
        self.assertEqual(receipt['status'], 'needs_review'); self.assertIsNone(receipt['result'])
        self.assertTrue((self.folder/'completion.json').exists())
        if no_producer: self.assertFalse((self.folder/'producer').exists())
        return receipt

    def test_complete_invented_sequence_real_audit_and_saved_contract(self):
        request = self.freeze(); before = copy.deepcopy(request)
        receipt = self.run_child(request)
        self.assertEqual(request, before)
        self.assertEqual((receipt['status'], receipt['exit_code'], receipt['termination']),
                         ('invented_child_producer_complete', 0, 'reaped'))
        result = receipt['result']
        self.assertEqual((result['simulated_native_loads'], result['callback_calls'], result['simulated_cipher_calls']), (5, 1, 48))
        self.assertIs(result['test_injection_used'], True)
        self.assertIs(result['audit_hook_acknowledged'], True)
        self.assertIs(result['audit_hook_retained_inert'], True)
        self.assertEqual(set(result['artifact_sha256']), set(invented.ARTIFACTS))
        for name in ('installed_dependency_bootstrap_performed', 'actual_dependency_observation_performed',
                     'parent_execution_authenticated', 'prior_review_proven', 'execution_authorized',
                     'operational_acceptance', 'feature_supported', 'recovery_proven', 'device_write_gate_passed'):
            self.assertIs(result[name], False)
        self.assertEqual(result['camera_commands'], [])
        journal = [json.loads(line)['event'] for line in (self.folder/'producer/journal.jsonl').read_text().splitlines()]
        self.assertEqual(journal[-8:], ['raw_written', 'raw_flushed', 'raw_fsynced', 'raw_closed',
            'raw_reverified', 'callback_claimed', 'callback_returned', 'cleanup_complete'])
        self.assertEqual(journal.count('callback_claimed'), 1)
        self.assertEqual(invented.validate_saved(self.folder/'producer', self.value, self.fixed,
                         self.buffers, 'c'*64), result['artifact_sha256'])

    def sentinel_entry(self):
        sentinel = Path(self.temp.name)/'unexpected-entry'
        with (self.root/entry.FILES['entry']).open('a', encoding='utf8') as out:
            out.write('\nPath('+repr(str(sentinel))+').write_text("unexpected")\n')
        return sentinel

    def test_packet_is_checked_before_any_entry_execution(self):
        sentinel = self.sentinel_entry(); request = self.freeze()
        with self.path.open('ab') as out: out.write(b' ')
        self.assert_refused(request); self.assertFalse(sentinel.exists())

    def test_fourth_source_is_checked_before_any_entry_execution(self):
        sentinel = self.sentinel_entry(); request = self.freeze()
        with (self.root/entry.COMPOSITION_FILES['invented']).open('ab') as out: out.write(b'\n# changed\n')
        self.assert_refused(request); self.assertFalse(sentinel.exists())

    def test_runtime_is_checked_before_any_entry_execution(self):
        sentinel = self.sentinel_entry(); request = self.freeze()
        request['expected_runtime']['optimize'] = 1
        self.assert_refused(request); self.assertFalse(sentinel.exists())

    def test_wrong_packet_digest_refuses_without_launch(self):
        self.path.write_bytes(entry.canonical(self.value))
        with self.assertRaisesRegex(ValueError, '^packet_hash$'):
            entry.freeze_composition(source_root=self.root, expected_runtime=self.profile,
                review_sha256='c'*64, packet_path=self.path, packet_sha256='0'*64, fixed=self.fixed)
        self.assertFalse(self.folder.exists())

    def test_package_expectation_cannot_be_derived_from_substituted_packet(self):
        self.value['inputs']['package']['manifest']['wheel_sha256'] = '0'*64
        self.assert_refused(self.freeze())

    def test_independent_root_expectation_cannot_be_substituted(self):
        self.fixed['root_sha256']['package'] = '0'*64
        self.assert_refused(self.freeze())

    def test_independent_policy_expectation_cannot_be_substituted(self):
        self.fixed['expectation_sha256'] = '0'*64
        self.assert_refused(self.freeze())

    def test_claimed_source_identity_must_be_exact_executing_buffers(self):
        self.value['inputs']['expectation']['source_sha256']['producer'] = '0'*64
        self.value['inputs']['binding']['expectation_sha256'] = invented.core._hash(self.value['inputs']['expectation'])
        self.fixed = invented.expectations(self.value)
        self.assert_refused(self.freeze())

    def test_review_declaration_must_match_packet(self):
        self.value['inputs']['binding']['review_sha256'] = 'b'*64
        self.assert_refused(self.freeze())

    def test_saved_records_mode_is_not_an_activation_mode(self):
        self.value['schema'] = 'actual_dependency_packet_v1'
        self.assert_refused(self.freeze())

    def test_invented_reader_has_no_filesystem_fallback(self):
        key = next(iter(self.value['contents'])); del self.value['contents'][key]
        self.assert_refused(self.freeze())

    def test_invented_source_partial_execution_never_reports_success(self):
        data, ops = fixture({'Cryptodome.Random': "raise ValueError('invented partial')\n"})
        self.value = invented.packet(data, ops, self.buffers, 'c'*64)
        self.fixed = invented.expectations(self.value)
        self.assert_refused(self.freeze(), no_producer=False)
        self.assertFalse((self.folder/'producer/result.json').exists())

    def test_suppressed_real_audit_install_refuses_before_simulated_load(self):
        suffix = "\nimport sys\ndef suppress(event,args):\n if event=='sys.addaudithook':raise RuntimeError('invented suppression')\nsys.addaudithook(suppress)\n"
        with (self.root/entry.COMPOSITION_FILES['invented']).open('a', encoding='utf8') as out: out.write(suffix)
        self.buffers = {k: (self.root/v).read_bytes() for k, v in entry.COMPOSITION_FILES.items()}
        self.value = invented.packet(self.data, self.ops, self.buffers, 'c'*64)
        self.fixed = invented.expectations(self.value)
        self.assert_refused(self.freeze(), no_producer=False)
        journal = (self.folder/'producer/journal.jsonl').read_text()
        self.assertNotIn('native_intent', journal); self.assertNotIn('callback_claimed', journal)

    def mutate_after_wait(self, action):
        original = entry.subprocess.Popen
        def spawn(*args, **kwargs):
            process = original(*args, **kwargs); wait = process.wait
            def mutated_wait(*args, **kwargs):
                code = wait(*args, **kwargs)
                if code == 0: action()
                return code
            process.wait = mutated_wait
            return process
        return patch.object(entry.subprocess, 'Popen', spawn)

    def test_parent_rechecks_saved_journal_after_child_success(self):
        request = self.freeze()
        def tamper():
            p = self.folder/'producer/journal.jsonl'; p.write_bytes(p.read_bytes()+b'{}\n')
        with self.mutate_after_wait(tamper): self.assert_refused(request, no_producer=False)

    def test_parent_rejects_promoted_child_claim_after_real_success(self):
        request = self.freeze()
        def tamper():
            p = self.folder/'stdout.json'; value = json.loads(p.read_bytes())
            value['actual_dependency_observation_performed'] = True
            p.write_bytes(entry.canonical(value))
        with self.mutate_after_wait(tamper): self.assert_refused(request, no_producer=False)

    def test_parent_rejects_saved_result_promoted_claim(self):
        request = self.freeze()
        def tamper():
            p = self.folder/'producer/result.json'; value = json.loads(p.read_bytes())
            value['test_injection_used'] = False
            p.write_bytes(entry.canonical(value))
        with self.mutate_after_wait(tamper): self.assert_refused(request, no_producer=False)

    def test_parent_rechecks_original_packet_after_child_success(self):
        request = self.freeze()
        def tamper():
            with self.path.open('ab') as out: out.write(b' ')
        with self.mutate_after_wait(tamper): self.assert_refused(request, no_producer=False)

    def tamper_trace(self, reorder):
        request = self.freeze()
        def tamper():
            p = self.folder/'producer/result.json'; value = json.loads(p.read_bytes())
            value['source_execution_trace'] = reorder(value['source_execution_trace'])
            raw = entry.canonical(value); p.write_bytes(raw)
            # Rebind the outer artifact digest so semantic correlation, rather
            # than an incidental stale digest, must detect the inconsistency.
            p = self.folder/'stdout.json'; outer = json.loads(p.read_bytes())
            outer['artifact_sha256']['result.json'] = entry.sha(raw); p.write_bytes(entry.canonical(outer))
        with self.mutate_after_wait(tamper): self.assert_refused(request, no_producer=False)

    def test_parent_correlates_trace_completion_order_with_journal(self):
        def reorder(trace):
            return [row for alias in reversed(sorted(invented.subject.ALIASES))
                    for row in trace if row['alias'] == alias]
        self.tamper_trace(reorder)

    def test_parent_rejects_impossible_trace_nesting(self):
        def reorder(trace):
            return ([row for row in trace if row['stage'] == 'source_execute_intent'] +
                    [row for row in trace if row['stage'] == 'source_execute_complete'])
        self.tamper_trace(reorder)

    def test_parent_rechecks_source_receipts_after_child_success(self):
        request = self.freeze()
        def tamper():
            with (self.root/entry.COMPOSITION_FILES['invented']).open('ab') as out: out.write(b'\n# changed\n')
        with self.mutate_after_wait(tamper): self.assert_refused(request, no_producer=False)

    def cleanup_case(self, alias, *, primary=False, remove=False):
        # Unit seam for cleanup faults; no producer/hook/native execution here.
        foreign = types.ModuleType('foreign')
        def produce(**kwargs):
            if remove: sys.modules.pop(alias)
            else: sys.modules[alias] = foreign
            if primary: raise ValueError('invented_primary_failure')
        with patch.dict(sys.modules):
            sys.modules.pop('ctypes', None); sys.modules.pop(invented.HELPER, None)
            with patch.object(invented.subject, 'produce_invented', side_effect=produce):
                code = '^invented_primary_failure$' if primary else '^invented_cleanup_ownership$'
                with self.assertRaisesRegex(ValueError, code):
                    invented.execute(self.value, self.fixed, self.buffers, 'c'*64, self.folder)
            other = 'ctypes' if alias == invented.HELPER else invented.HELPER
            self.assertNotIn(other, sys.modules)
            if remove: self.assertNotIn(alias, sys.modules)
            else: self.assertIs(sys.modules[alias], foreign)

    def test_helper_replacement_preserves_foreign_and_releases_owned_ctypes(self):
        self.cleanup_case(invented.HELPER)

    def test_ctypes_replacement_preserves_foreign_and_releases_owned_helper(self):
        self.cleanup_case('ctypes')

    def test_primary_error_survives_helper_cleanup_failure(self):
        self.cleanup_case(invented.HELPER, primary=True)

    def test_primary_error_survives_ctypes_deletion(self):
        self.cleanup_case('ctypes', primary=True, remove=True)

    def test_existing_attempt_is_preserved_without_spawn(self):
        request = self.freeze(); self.folder.mkdir(); (self.folder/'sentinel').write_bytes(b'preserve')
        with patch.object(entry.subprocess, 'Popen') as spawn:
            with self.assertRaises(FileExistsError): self.run_child(request)
            spawn.assert_not_called()
        self.assertEqual((self.folder/'sentinel').read_bytes(), b'preserve')


if __name__ == '__main__': unittest.main()
