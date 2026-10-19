"""Saved invented metadata only; no operational loader or actual input paths."""
import json
import unittest
from unittest.mock import patch

from tools import dependency_parent as subject
from tools import dependency_evidence as core
from tools import dependency_execution as execution
from tools import dependency_producer as producer
import test_dependency_controller as controller_fixture


class ParentTests(unittest.TestCase):
    def setUp(self):
        self.fixture = controller_fixture.ControllerTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.execute()
        self.folder = self.fixture.folder
        self.stdout = producer.encoded(self.fixture.result[1])
        self.dependency = execution.validate_saved_composition(self.folder/'collected', self.fixture.data, invented=True)
        self.bridge = {name:producer.sha((self.folder/name).read_bytes()) for name in subject.BRIDGE}

    def execute(self, **changes):
        kwargs = dict(folder=self.folder, inputs=self.fixture.data,
            operation_id=self.fixture.data['expectation']['operation_id'], stdout=self.stdout,
            stdout_sha256=producer.sha(self.stdout), dependency_sha256=self.dependency,
            bridge_sha256=self.bridge, invented=True)
        kwargs.update(changes)
        return subject.validate_saved_controller(**kwargs)

    def change_bridge(self, name, change):
        path = self.folder/name
        value = json.loads(path.read_bytes()); change(value)
        path.write_bytes(producer.encoded(value))
        self.bridge[name] = producer.sha(path.read_bytes())

    def test_complete_bridge_and_dependency_metadata_recomputed(self):
        with patch.object(producer.RuntimeOps, 'reader', side_effect=AssertionError('actual reader')):
            result = self.execute()
        self.assertEqual(result['dependency_sha256'], self.dependency)
        self.assertEqual(result['bridge_sha256'], self.bridge)
        self.assertEqual(result['start_sha256'], producer.sha((self.folder/'started.json').read_bytes()))
        for name in ('actual_runtime_verified','historical_truth_verified','operational_acceptance',
                     'execution_authorized','feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(result[name], False)

    def test_boolean_mode_refused_before_any_read(self):
        with patch.object(producer, 'read_verified', side_effect=AssertionError('read')):
            with self.assertRaisesRegex(core.EvidenceError, '^collection_mode$'): self.execute(invented=1)

    def test_operation_substitution_refused(self):
        with self.assertRaisesRegex(core.EvidenceError, '^parent_operation$'): self.execute(operation_id='other')

    def test_exact_stdout_hash_required(self):
        with self.assertRaisesRegex(core.EvidenceError, '^parent_stdout_hash$'): self.execute(stdout=self.stdout+b' ')

    def test_changed_summary_is_not_authorized_by_rehashed_stdout(self):
        raw = producer.encoded(dict(script_exit_code=0, changed=True))
        with self.assertRaisesRegex(core.EvidenceError, '^parent_summary$'):
            self.execute(stdout=raw, stdout_sha256=producer.sha(raw))

    def test_boolean_summary_exit_code_refused(self):
        raw = producer.encoded(dict(script_exit_code=False))
        with self.assertRaisesRegex(core.EvidenceError, '^parent_summary$'):
            self.execute(stdout=raw, stdout_sha256=producer.sha(raw))

    def test_duplicate_stdout_keys_refused(self):
        raw = b'{"script_exit_code":2,"script_exit_code":0}'
        with self.assertRaises(core.EvidenceError): self.execute(stdout=raw, stdout_sha256=producer.sha(raw))

    def test_empty_stdout_refused(self):
        with self.assertRaisesRegex(core.EvidenceError, '^parent_stdout_bound$'): self.execute(stdout=b'')

    def test_oversized_stdout_refused(self):
        with self.assertRaisesRegex(core.EvidenceError, '^parent_stdout_bound$'): self.execute(stdout=b' '*16385)

    def test_extra_bridge_artifact_refused(self):
        (self.folder/'unexpected.json').write_bytes(b'{}')
        with self.assertRaisesRegex(core.EvidenceError, '^parent_bridge_roster$'): self.execute()

    def test_start_operation_changed_refused(self):
        path = self.folder/'started.json'; value = json.loads(path.read_bytes())
        value['operation_id'] = 'other'; path.write_bytes(producer.encoded(value))
        with self.assertRaisesRegex(core.EvidenceError, '^parent_start$'): self.execute()

    def test_start_authority_flag_changed_refused(self):
        path = self.folder/'started.json'; value = json.loads(path.read_bytes())
        value['protected_input_authorized'] = True; path.write_bytes(producer.encoded(value))
        with self.assertRaisesRegex(core.EvidenceError, '^parent_start$'): self.execute()

    def test_changed_dependency_bytes_refused(self):
        path = self.folder/'collected/producer/raw.json'; path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaises(core.EvidenceError): self.execute()

    def test_dependency_hash_map_cannot_omit_artifact(self):
        self.dependency.pop('producer/raw.json')
        with self.assertRaisesRegex(core.EvidenceError, '^shape$'): self.execute()

    def test_dependency_hash_map_substitution_refused(self):
        self.dependency['producer/raw.json'] = '0'*64
        with self.assertRaisesRegex(core.EvidenceError, '^parent_dependency_hashes$'): self.execute()

    def test_changed_bridge_bytes_refused(self):
        path = self.folder/'completion.json'; path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaisesRegex(core.EvidenceError, '^parent_bridge_hashes$'): self.execute()

    def test_rehashed_boolean_result_code_refused(self):
        self.change_bridge('controller-result.json', lambda value:value.update(code=False))
        with self.assertRaisesRegex(core.EvidenceError, '^parent_result$'): self.execute()

    def test_rehashed_summary_substitution_refused(self):
        self.change_bridge('controller-result.json', lambda value:value['summary'].update(changed=True))
        with self.assertRaisesRegex(core.EvidenceError, '^parent_summary$'): self.execute()

    def test_rehashed_authority_promotion_refused(self):
        self.change_bridge('completion.json', lambda value:value.update(execution_authorized=True))
        with self.assertRaisesRegex(core.EvidenceError, '^parent_completion$'): self.execute()

    def test_rehashed_release_failure_refused(self):
        self.change_bridge('completion.json', lambda value:value.update(callback_released=False))
        with self.assertRaisesRegex(core.EvidenceError, '^parent_completion$'): self.execute()

    def test_rehashed_dependency_anchor_substitution_refused(self):
        self.change_bridge('completion.json', lambda value:value.update(dependency_completion_sha256='0'*64))
        with self.assertRaisesRegex(core.EvidenceError, '^parent_completion$'): self.execute()

    def test_unknown_bridge_hash_role_refused(self):
        self.bridge['extra.json'] = '0'*64
        with self.assertRaisesRegex(core.EvidenceError, '^shape$'): self.execute()

    def test_retained_controller_timing_float_round_trip(self):
        summary = dict(script_exit_code=0, source_observation=dict(elapsed_seconds=0.125))
        self.change_bridge('controller-result.json', lambda value:value.update(summary=summary))
        raw = producer.encoded(summary)
        self.assertEqual(self.execute(stdout=raw, stdout_sha256=producer.sha(raw))['status'],
                         'consistent_saved_controller')

    def test_nonfinite_negative_or_unlabelled_float_refused(self):
        for raw in (b'{"script_exit_code":0,"elapsed_seconds":NaN}',
                    b'{"script_exit_code":0,"elapsed_seconds":1e999}',
                    b'{"script_exit_code":0,"elapsed_seconds":-0.5}',
                    b'{"script_exit_code":0,"count":0.5}',
                    b'{"script_exit_code":0,"elapsed_seconds":[0.5]}'):
            with self.subTest(raw=raw), self.assertRaisesRegex(core.EvidenceError, '^json_number$'):
                self.execute(stdout=raw, stdout_sha256=producer.sha(raw))


if __name__ == '__main__':
    unittest.main()
