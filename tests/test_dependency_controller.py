"""Invented callback boundary and failure accounting; no installed dependencies."""
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from tools import dependency_controller as subject
from tools import dependency_producer as producer
from tools import dependency_evidence as core
from tools import dependency_execution as execution
from tools.dependency_invented import HELPER
from test_dependency_package_preflight import complete_fixture


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)/'attempt'
        self.data, self.ops = complete_fixture()
        self.modules = dict(sys.modules); self.meta = list(sys.meta_path); self.path = list(sys.path)
        self.addCleanup(self.restore)
        helper = types.ModuleType(HELPER); helper.new = self.ops.new; sys.modules[HELPER] = helper
        sys.modules['ctypes'] = self.ops.modules['ctypes']
        operation = self.data['expectation']['operation_id']
        self.context = dict(operation_id=operation); self.identity = dict(operation_id=operation)
        self.closes = 0
        self.records = types.SimpleNamespace(close=self.close_records)
        self.releases = 0; self.factories = 0; self.controller_calls = 0
        self.result = (0, dict(script_exit_code=0))
        self.control = types.SimpleNamespace(verify_context=lambda context: True,
                                            run_child_reserved=self.run_controller)

    def restore(self):
        sys.meta_path[:] = self.meta; sys.path[:] = self.path
        for name in tuple(sys.modules):
            if name == HELPER or name == 'ctypes' or name == 'Cryptodome' or name.startswith('Cryptodome.'):
                if name in self.modules: sys.modules[name] = self.modules[name]
                else: sys.modules.pop(name, None)

    def run_controller(self, **kwargs):
        self.controller_calls += 1
        self.assertIsNot(kwargs['records'], self.records)
        kwargs['make_callbacks'](object(), object())
        return self.result

    def close_records(self):
        self.closes += 1
        return True

    def factory(self, controller, stage_source, dependency):
        self.factories += 1
        self.assertIs(dependency['AES'], sys.modules['Cryptodome.Cipher.AES'])
        anchor = dependency['provenance']; raw = Path(anchor['path']).read_bytes()
        self.assertEqual((producer.sha(raw), len(raw)), (anchor['sha256'], anchor['bytes']))
        self.assertEqual(self.ops.loader_calls, 5)
        self.assertIsNot(self.ops.modules['ctypes'].CDLL, self.ops.original)
        with self.assertRaises(TypeError): dependency['AES'] = None
        with self.assertRaises(TypeError): anchor['sha256'] = '0'*64
        return {}

    def release(self):
        self.releases += 1
        self.assertIn('Cryptodome.Cipher.AES', sys.modules)
        self.assertIsNot(self.ops.modules['ctypes'].CDLL, self.ops.original)

    def execute(self, **changes):
        kw = dict(inputs=self.data, ops=self.ops, folder=self.folder, control=self.control,
                  context=self.context, records=self.records, identity=self.identity,
                  make_callbacks_after_receipt=self.factory, release_callbacks_after_controller=self.release,
                  monotonic=lambda: 0.)
        kw.update(changes)
        return subject.run_invented(**kw)

    def test_full_collection_receipt_then_live_controller_then_cleanup(self):
        result = self.execute()
        self.assertEqual((self.controller_calls, self.factories, self.releases), (1, 1, 1))
        self.assertEqual(result['callback_result'][0], 0)
        artifacts = execution.validate_saved_composition(self.folder/'collected', self.data, invented=True)
        self.assertEqual(len(artifacts), 11)
        self.assertNotIn('Cryptodome.Cipher.AES', sys.modules)
        self.assertIs(self.ops.modules['ctypes'].CDLL, self.ops.original)
        completion = json.loads((self.folder/'completion.json').read_bytes())
        for key in ('execution_authorized', 'feature_supported', 'recovery_proven', 'device_write_gate_passed',
                    'actual_dependency_observation_performed'):
            self.assertIs(completion[key], False)

    def test_actual_runtime_ops_rejected_before_any_folder_or_reader(self):
        with self.assertRaisesRegex(core.EvidenceError, '^real_activation_pending$'):
            self.execute(ops=producer.RuntimeOps())
        self.assertFalse(self.folder.exists()); self.assertEqual(self.ops.reads, [])

    def test_operation_mismatch_before_collection(self):
        with self.assertRaisesRegex(core.EvidenceError, '^controller_operation$'):
            self.execute(identity=dict(operation_id='other'))
        self.assertFalse(self.folder.exists()); self.assertEqual(self.ops.reads, [])

    def test_context_must_verify_before_collection(self):
        self.control.verify_context = lambda _: False
        with self.assertRaisesRegex(core.EvidenceError, '^controller_context$'): self.execute()
        self.assertEqual(self.ops.reads, [])

    def test_context_is_rechecked_before_controller(self):
        calls = []
        self.control.verify_context = lambda _: (calls.append(True) or len(calls) == 1)
        with self.assertRaisesRegex(core.EvidenceError, '^controller_context$'): self.execute()
        self.assertEqual(self.controller_calls, 0); self.assertEqual(self.releases, 0)

    def test_unused_package_change_prevents_controller(self):
        path = next(p for p in self.ops.contents if '/data/item' in p)
        self.ops.contents[path] += b'changed'
        with self.assertRaisesRegex(core.EvidenceError, '^fresh_bytes$'): self.execute()
        self.assertEqual(self.controller_calls, 0); self.assertEqual(self.ops.loader_calls, 0)

    def test_controller_refusal_not_promoted_to_success(self):
        self.result = (2, dict(script_exit_code=2))
        with self.assertRaisesRegex(core.EvidenceError, '^controller_refused$'): self.execute()
        self.assertEqual(self.releases, 1)
        self.assertEqual(json.loads((self.folder/'controller-result.json').read_bytes())['code'], 2)
        self.assertEqual(json.loads((self.folder/'completion.json').read_bytes())['status'], 'needs_review')

    def test_boolean_controller_code_rejected(self):
        self.result = (False, dict(script_exit_code=False))
        with self.assertRaisesRegex(core.EvidenceError, '^controller_result$'): self.execute()
        self.assertEqual(self.releases, 1)

    def test_boolean_summary_code_rejected(self):
        self.result = (0, dict(script_exit_code=False))
        with self.assertRaisesRegex(core.EvidenceError, '^controller_result$'): self.execute()

    def test_decimal_summary_code_rejected(self):
        self.result = (0, dict(script_exit_code=0.0))
        with self.assertRaisesRegex(core.EvidenceError, '^controller_result$'): self.execute()

    def test_valid_cross_operation_substitution_refused(self):
        def mutate(op, path):
            self.context['operation_id'] = self.identity['operation_id'] = 'other_valid_operation'
        self.ops.read_action = mutate
        with self.assertRaisesRegex(core.EvidenceError, '^controller_operation$'): self.execute()
        self.assertEqual(self.controller_calls, 0); self.assertEqual(self.closes, 1)

    def test_controller_primary_survives_release_error(self):
        def fail(**kwargs): raise KeyboardInterrupt('invented primary')
        def release(): self.releases += 1; raise OSError('invented release')
        self.control.run_child_reserved = fail
        with self.assertRaisesRegex(KeyboardInterrupt, 'invented primary'):
            self.execute(release_callbacks_after_controller=release)
        self.assertEqual(self.releases, 1)
        self.assertEqual(self.closes, 1)

    def test_release_failure_prevents_completion(self):
        def release(): self.releases += 1; raise OSError('invented release')
        with self.assertRaisesRegex(OSError, 'invented release'):
            self.execute(release_callbacks_after_controller=release)
        self.assertEqual(self.releases, 1)
        self.assertNotIn('Cryptodome.Cipher.AES', sys.modules)

    def test_publication_failure_keeps_primary_exception(self):
        original = producer.Outputs.small
        def small(output, name, value):
            if output.folder == self.folder and name == 'completion.json': raise OSError('publication')
            return original(output, name, value)
        self.result = (2, dict(script_exit_code=2))
        with patch.object(producer.Outputs, 'small', small):
            with self.assertRaisesRegex(core.EvidenceError, '^controller_refused$'): self.execute()

    def test_existing_attempt_blocks_replay(self):
        self.execute(); count = len(self.ops.reads)
        with self.assertRaises(FileExistsError): self.execute()
        self.assertEqual(len(self.ops.reads), count); self.assertEqual(self.controller_calls, 1)

    def test_output_construction_interruption_closes_owned_records(self):
        with patch.object(producer, 'Outputs', side_effect=KeyboardInterrupt('invented pre-start')):
            with self.assertRaisesRegex(KeyboardInterrupt, 'invented pre-start'): self.execute()
        self.assertTrue(self.folder.is_dir())
        self.assertEqual((self.closes, self.releases, self.controller_calls), (1, 0, 0))
        self.assertEqual(self.ops.reads, [])

    def test_success_completion_publication_attempted_once(self):
        original = producer.Outputs.small; calls = []
        def small(output, name, value):
            if output.folder == self.folder and name == 'completion.json':
                calls.append(name)
                raise OSError('uncertain publication')
            return original(output, name, value)
        with patch.object(producer.Outputs, 'small', small):
            with self.assertRaisesRegex(OSError, 'uncertain publication'): self.execute()
        self.assertEqual(len(calls), 1); self.assertEqual(self.closes, 1)

    def test_controller_owned_record_close_not_repeated(self):
        original = self.run_controller
        def run(**kwargs):
            answer = original(**kwargs); self.assertIs(kwargs['records'].close(), True); return answer
        self.control.run_child_reserved = run
        self.execute(); self.assertEqual(self.closes, 1)

    def test_unknown_record_close_not_repeated(self):
        def close(): self.closes += 1; raise OSError('unknown close')
        self.records.close = close
        with self.assertRaisesRegex(OSError, 'unknown close'): self.execute()
        self.assertEqual(self.closes, 1); self.assertEqual(self.releases, 1)

    def test_caught_forbidden_native_load_remains_sticky(self):
        original = self.factory
        def factory(*args):
            result = original(*args)
            try: self.ops.modules['ctypes'].CDLL('C:/invented/forbidden.pyd')
            except core.EvidenceError: pass
            return result
        with self.assertRaisesRegex(core.EvidenceError, '^sticky_guard_failure$'):
            self.execute(make_callbacks_after_receipt=factory)
        self.assertEqual(self.releases, 1)

    def test_observer_callback_is_preserved_before_internal_continuation(self):
        seen = []
        self.ops.callback_action = lambda op, AES: seen.append((self.controller_calls, self.factories))
        self.execute()
        self.assertEqual(seen, [(0, 0)])
        self.assertEqual((self.ops.callback_calls, self.ops.cipher_calls), (1, 72))

    def test_swallowed_observer_load_failure_prevents_controller_entry(self):
        def callback(op, AES):
            try: op.modules['ctypes'].CDLL('C:/invented/forbidden.pyd')
            except core.EvidenceError: pass
        self.ops.callback_action = callback
        with self.assertRaisesRegex(core.EvidenceError, '^sticky_guard_failure$'): self.execute()
        self.assertEqual((self.controller_calls, self.factories, self.releases, self.closes), (0, 0, 0, 1))

    def test_observer_raw_receipt_change_prevents_controller_entry(self):
        def callback(op, AES):
            (self.folder/'collected/producer/raw.json').write_bytes(b'{}')
        self.ops.callback_action = callback
        with self.assertRaisesRegex(core.EvidenceError, '^raw_readback$'): self.execute()
        self.assertEqual((self.controller_calls, self.releases, self.closes), (0, 0, 1))

    def test_source_owner_changed_before_internal_continuation_refuses(self):
        self.ops.callback_action = lambda op, AES: sys.modules.__setitem__('Cryptodome.Random', types.ModuleType('foreign'))
        with self.assertRaisesRegex(core.EvidenceError, '^source_ownership$'): self.execute()
        self.assertEqual((self.controller_calls, self.releases, self.closes), (0, 0, 1))

    def test_internal_factory_can_be_claimed_only_once(self):
        def run(**kwargs):
            kwargs['make_callbacks'](object(), object())
            kwargs['make_callbacks'](object(), object())
            return self.result
        self.control.run_child_reserved = run
        with self.assertRaisesRegex(core.EvidenceError, '^controller_factory_reentry$'): self.execute()
        self.assertEqual((self.factories, self.releases, self.closes), (1, 1, 1))

    def test_controller_success_without_factory_is_refused(self):
        self.control.run_child_reserved = lambda **kwargs: self.result
        with self.assertRaisesRegex(core.EvidenceError, '^controller_factory$'): self.execute()
        self.assertEqual((self.factories, self.releases, self.closes), (0, 1, 1))

    def test_swallowed_factory_failure_cannot_be_promoted_to_success(self):
        def fail(*args): raise ValueError('factory failed')
        def run(**kwargs):
            try: kwargs['make_callbacks'](object(), object())
            except ValueError: pass
            return self.result
        self.control.run_child_reserved = run
        with self.assertRaisesRegex(core.EvidenceError, '^controller_factory$'):
            self.execute(make_callbacks_after_receipt=fail)
        self.assertEqual((self.releases, self.closes), (1, 1))

    def test_swallowed_factory_reentry_cannot_be_promoted_to_success(self):
        def run(**kwargs):
            kwargs['make_callbacks'](object(), object())
            try: kwargs['make_callbacks'](object(), object())
            except core.EvidenceError: pass
            return self.result
        self.control.run_child_reserved = run
        with self.assertRaisesRegex(core.EvidenceError, '^controller_factory$'): self.execute()
        self.assertEqual((self.factories, self.releases, self.closes), (1, 1, 1))

    def test_factory_failure_keeps_primary_and_releases_once(self):
        def fail(*args): raise KeyboardInterrupt('factory failed')
        def release(): self.releases += 1; raise OSError('release failed')
        with self.assertRaisesRegex(KeyboardInterrupt, 'factory failed'):
            self.execute(make_callbacks_after_receipt=fail, release_callbacks_after_controller=release)
        self.assertEqual((self.releases, self.closes), (1, 1))

    def test_factory_refuses_operation_change_after_controller_entry(self):
        def run(**kwargs):
            self.identity['operation_id'] = 'other_valid_operation'
            kwargs['make_callbacks'](object(), object())
            return self.result
        self.control.run_child_reserved = run
        with self.assertRaisesRegex(core.EvidenceError, '^controller_context$'): self.execute()
        self.assertEqual((self.factories, self.releases, self.closes), (0, 1, 1))

    def test_factory_refuses_receipt_change_after_controller_entry(self):
        def run(**kwargs):
            (self.folder/'collected/producer/raw.json').write_bytes(b'{}')
            kwargs['make_callbacks'](object(), object())
            return self.result
        self.control.run_child_reserved = run
        with self.assertRaisesRegex(core.EvidenceError, '^controller_receipt$'): self.execute()
        self.assertEqual((self.factories, self.releases, self.closes), (0, 1, 1))

    def test_release_receipt_change_prevents_completion(self):
        def release():
            self.release()
            (self.folder/'collected/producer/raw.json').write_bytes(b'{}')
        with self.assertRaisesRegex(core.EvidenceError, '^raw_readback$'):
            self.execute(release_callbacks_after_controller=release)
        self.assertEqual((self.releases, self.closes), (1, 1))
        self.assertEqual(json.loads((self.folder/'completion.json').read_bytes())['status'], 'needs_review')

    def test_controller_operation_mutation_after_factory_refuses(self):
        def run(**kwargs):
            kwargs['make_callbacks'](object(), object())
            self.context['operation_id'] = self.identity['operation_id'] = 'other_valid_operation'
            return self.result
        self.control.run_child_reserved = run
        with self.assertRaisesRegex(core.EvidenceError, '^controller_operation$'): self.execute()
        self.assertEqual((self.factories, self.releases, self.closes), (1, 1, 1))

    def test_release_operation_mutation_refuses(self):
        def release():
            self.release()
            self.identity['operation_id'] = 'other_valid_operation'
        with self.assertRaisesRegex(core.EvidenceError, '^controller_operation$'):
            self.execute(release_callbacks_after_controller=release)
        self.assertEqual((self.releases, self.closes), (1, 1))

    def test_release_context_mutation_refuses(self):
        self.control.verify_context = lambda context: not context.get('invalid', False)
        def release():
            self.release()
            self.context['invalid'] = True
        with self.assertRaisesRegex(core.EvidenceError, '^controller_context$'):
            self.execute(release_callbacks_after_controller=release)
        self.assertEqual((self.releases, self.closes), (1, 1))

    def test_public_runtime_entry_refuses_without_inspecting_arguments(self):
        with patch.object(producer, 'bind_inputs', side_effect=AssertionError('inputs inspected')):
            with self.assertRaisesRegex(core.EvidenceError, '^real_activation_pending$'):
                subject.run_runtime(inputs=object(), ops=object(), folder=self.folder)
        self.assertFalse(self.folder.exists())

    def test_internal_runtime_route_cannot_accept_custom_observer(self):
        with self.assertRaisesRegex(core.EvidenceError, '^controller_observer$'):
            subject._run(inputs=self.data, folder=self.folder, control=self.control,
                context=self.context, records=self.records, make_callbacks_after_receipt=self.factory,
                release_callbacks_after_controller=self.release, monotonic=lambda: 0.,
                identity=self.identity, invented=False, ops=self.ops)
        self.assertEqual(self.ops.reads, [])
        self.assertFalse(self.folder.exists())

    def test_internal_runtime_dispatch_has_no_observer_argument_and_owns_cleanup(self):
        # Wiring check only: no runtime observer is constructed or called.
        with patch.object(execution, '_produce_collected_runtime', side_effect=RuntimeError('dispatch stopped')) as run:
            with self.assertRaisesRegex(RuntimeError, 'dispatch stopped'):
                subject._run(inputs=self.data, folder=self.folder, control=self.control,
                    context=self.context, records=self.records, make_callbacks_after_receipt=self.factory,
                    release_callbacks_after_controller=self.release, monotonic=lambda: 0.,
                    identity=self.identity, invented=False)
        self.assertEqual(set(run.call_args.kwargs), {'inputs', 'folder', 'continuation'})
        self.assertTrue(callable(run.call_args.kwargs['continuation']))
        self.assertEqual((self.closes, self.releases, self.controller_calls), (1, 0, 0))
        self.assertEqual(self.ops.reads, [])
        failure = json.loads((self.folder/'completion.json').read_bytes())
        self.assertNotIn('actual_dependency_observation_performed', failure)
        self.assertIs(failure['actual_dependency_observation_completed'], False)
        self.assertEqual(failure['dependency_observation_status'], 'incomplete_or_unknown')

    def test_parent_saved_verifier_refuses_changed_dependency_completion(self):
        self.execute()
        path = self.folder/'collected/completion.json'
        value = json.loads(path.read_bytes()); value['verification_sha256'] = '0'*64
        path.write_text(json.dumps(value), encoding='utf-8')
        with self.assertRaisesRegex(core.EvidenceError, '^saved_completion$'):
            execution.validate_saved_composition(self.folder/'collected', self.data, invented=True)


if __name__ == '__main__':
    unittest.main()
