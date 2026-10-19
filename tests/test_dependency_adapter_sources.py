"""Checked adapter graph ownership only; no runtime or protected inputs."""
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

from tools import dependency_adapter_sources as subject


def sources():
    return {n: (Path('tools') / (n + '.py')).read_bytes() for n in subject.ORDER}


class AdapterSourceTests(unittest.TestCase):
    def make(self, buffers=None, hashes=None):
        buffers = sources() if buffers is None else buffers
        return subject.AdapterSources(buffers=buffers,
            hashes={n: subject.sha(raw) for n, raw in buffers.items()} if hashes is None else hashes)

    def loaded(self):
        owner = self.make().load()
        self.addCleanup(lambda: None if owner.closed else owner.close())
        return owner

    def test_exact_graph_detached_no_process_aliases(self):
        before = dict(sys.modules)
        owner = self.loaded()
        self.assertEqual(set(owner.modules), set(subject.ORDER))
        self.assertTrue(all(sys.modules[n] is m for n, m in before.items()))
        self.assertFalse(any(n.startswith('_a6700_adapter') for n in sys.modules))
        binding = owner.modules['dependency_adapter_binding']
        self.assertIs(binding.policy, owner.modules['dependency_operational_scope'])
        self.assertIs(binding.policy.outer, owner.modules['dependency_outer_contract'])
        owner.intact()

    def test_all_hashes_checked_before_any_execution(self):
        buffers = sources()
        hashes = {n: subject.sha(raw) for n, raw in buffers.items()}
        buffers[subject.ORDER[-1]] += b'\n# change\n'
        with patch('builtins.exec', side_effect=AssertionError('execution')):
            with self.assertRaisesRegex(ValueError, 'adapter_loader_hash'):
                self.make(buffers, hashes)

    def test_incomplete_and_extra_source_roster_refuse(self):
        for extra in (False, True):
            buffers = sources()
            if extra:
                buffers['anything'] = b'pass\n'
            else:
                buffers.pop(subject.ORDER[-1])
            with self.assertRaisesRegex(ValueError, 'adapter_loader_roster'):
                self.make(buffers)

    def test_unreviewed_import_edge_refuses_before_execution(self):
        for raw in (b'import socket\n', b'from tools import dependency_execution\n',
                    b'from . import x\n', b'import tools.dependency_operational_scope\n'):
            buffers = sources()
            buffers[subject.ORDER[-1]] += raw
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, 'adapter_loader_'):
                self.make(buffers)

    def test_code_replacement_detected_even_same_function_object(self):
        owner = self.loaded()
        original = owner.modules['dependency_adapter_binding'].need
        original.__code__ = (lambda *a: None).__code__
        with self.assertRaisesRegex(ValueError, 'adapter_loader_live_code'):
            owner.intact()
        self.assertTrue(owner.failed)

    def test_defaults_and_nested_policy_changes_detected(self):
        for mutate in (lambda m: setattr(m.validate_request, '__kwdefaults__', {'x': True}),
                       lambda m: m.ENTRIES.update(outer_child='run_invented')):
            owner = self.loaded()
            mutate(owner.modules['dependency_adapter_binding'])
            with self.assertRaisesRegex(ValueError, 'adapter_loader_live_code'):
                owner.intact()

    def test_dependency_policy_module_mutation_detected(self):
        owner = self.loaded()
        owner.modules['dependency_operational_scope'].SCOPE['source_opens'] = 3
        with self.assertRaisesRegex(ValueError, 'adapter_loader_live_code'):
            owner.intact()

    def test_package_attribute_substitution_refuses(self):
        owner = self.loaded()
        owner.package.dependency_operational_scope = types.SimpleNamespace()
        with self.assertRaisesRegex(ValueError, 'adapter_loader_namespace'):
            owner.intact()

    def test_compiled_buffer_substitution_refuses(self):
        owner = self.make()
        key = subject.ORDER[-1]
        owner.compiled[key] = compile(sources()[key], '<other>', 'exec')
        with self.assertRaisesRegex(ValueError, 'adapter_loader_policy_changed'):
            owner.load()
        self.assertTrue(owner.closed)

    def test_foreign_tools_alias_preserved_and_change_detected(self):
        owner = self.loaded()
        alias = 'tools.invented_foreign'
        foreign = types.ModuleType(alias)
        with patch.dict(sys.modules, {alias: foreign}):
            with self.assertRaisesRegex(ValueError, 'adapter_loader_foreign_alias'):
                owner.intact()
            self.assertIs(sys.modules[alias], foreign)

    def test_public_call_cannot_select_runtime_capable_functions(self):
        owner = self.loaded()
        for name in ('_continue_runtime', 'run_runtime', 'reconcile_runtime', '_saved_runtime'):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'adapter_loader_call'):
                owner.call(name)

    def test_close_once_clears_owned_references_and_preserves_aliases(self):
        owner = self.loaded()
        before = {n: m for n, m in sys.modules.items() if n == 'tools' or n.startswith('tools.')}
        self.assertTrue(owner.close())
        self.assertEqual(owner.modules, {})
        self.assertEqual(owner.compiled, {})
        self.assertEqual(owner.construction, ())
        self.assertEqual(owner.expected_hashes, ())
        self.assertEqual(owner.buffers, {})
        self.assertEqual(owner.hashes, {})
        self.assertEqual(vars(owner.package), {})
        self.assertTrue(all(sys.modules[n] is m for n, m in before.items()))
        with self.assertRaisesRegex(ValueError, 'adapter_loader_reclose'):
            owner.close()

    def test_projection_refuses_independently_reanchored_source(self):
        for changed in subject.ORDER:
            with self.subTest(changed=changed):
                owner = self.loaded()
                buffers = {key: owner.buffers[name] for name, key in subject.BUFFER_KEYS.items()}
                buffers[subject.BUFFER_KEYS[changed]] += b'\n# independently rebound valid source\n'
                rows = {key: dict(sha256=subject.sha(raw), size=len(raw)) for key, raw in buffers.items()}
                with self.assertRaisesRegex(ValueError, 'adapter_projection_loaded_source'):
                    owner.project(process_sources=rows, process_buffers=buffers, repository_root=Path.cwd())

    def test_owned_source_buffer_mutation_refuses(self):
        owner = self.loaded()
        owner.buffers[subject.ORDER[-1]] += b'\n# changed\n'
        with self.assertRaisesRegex(ValueError, 'adapter_loader_buffer_changed'):
            owner.intact()

    def test_refused_call_preserves_primary_without_automatic_cleanup(self):
        owner = self.loaded()
        with self.assertRaisesRegex(TypeError, 'request'):
            owner.call('validate_request')
        self.assertFalse(owner.closed)
        owner.intact()

    def test_public_runtime_always_refuses(self):
        with self.assertRaisesRegex(ValueError, '^real_activation_pending$'):
            subject.run_runtime(unknown=object())


if __name__ == '__main__':
    unittest.main()
