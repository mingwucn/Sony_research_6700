"""Real authored parent finder/bootstrap ownership over invented role sources.

Only the two explicitly pinned private authored bootstrap files are read.
Registration uses the real parent_validation_sources function and unmodified
AuthoredSources. The minimal invented validation/context records test these
consumers; they are not a historical gate result or an executable actual bundle.
The loader executes cached ordinary text. Fresh disk checks belong to the
separate retained verify_context call, not to AuthoredSources itself.
"""
import copy
import hashlib
import importlib
from pathlib import Path
import stat
import sys
import tempfile
from types import ModuleType
import unittest
from unittest.mock import patch

from tools import dependency_historical_gate as gate
from tools import dependency_host_entry as host
from tools import dependency_operational_launcher as parent


REPOSITORY = Path(__file__).resolve().parents[1]
FACTORY_PATH = REPOSITORY / 'private/sessions/20261019-RA-003-parent-evidence-v5/integration/prospective_child.py'
CONTROL_PATH = REPOSITORY / 'private/sessions/20261019-RA-003-parent-evidence-v5/activation/io_entry.py'
BOOTSTRAP_SOURCES = {
    'factory': (FACTORY_PATH, 8861, '3cd438eb42db7d64c18752fab3580b47915de8ccd2d95efc431fd67fe3b0e08c'),
    'control': (CONTROL_PATH, 58942, '70a2ed3a0265894adace48e5285c0eb8962c666975f7df1a8e4f6141b918bb43'),
}


def selected_bootstrap_sources():
    """Read exactly the selected authored files, refusing changed identities."""
    buffers = {}
    for name, (path, size, digest) in BOOTSTRAP_SOURCES.items():
        try:
            before = path.lstat()
        except FileNotFoundError:
            raise unittest.SkipTest('selected private authored bootstrap unavailable in this export')
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or getattr(before, 'st_file_attributes', 0) & 0x400:
            raise AssertionError('selected bootstrap is not an ordinary single-link file')
        raw = path.read_bytes()
        after = path.lstat()
        stamp = lambda value: (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns, value.st_ctime_ns)
        if stamp(before) != stamp(after) or len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
            raise AssertionError('selected authored bootstrap identity changed')
        buffers[name] = raw
    return buffers


class ParentLoaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bootstrap_buffers = selected_bootstrap_sources()
        cls.before_pins = {name: parent.sha(raw) for name, raw in cls.bootstrap_buffers.items()}

    @classmethod
    def tearDownClass(cls):
        cls.after_pins = {name: parent.sha(raw) for name, raw in selected_bootstrap_sources().items()}
        if cls.after_pins != cls.before_pins:
            raise AssertionError('authored bootstrap changed during qualification')

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.boot = parent.BootstrapOwner(host)
        self.addCleanup(lambda: None if self.boot.closed else self.boot.close())
        self.control_alias = '_qualified_parent_loader_control'
        self.factory_alias = '_qualified_parent_loader_factory'
        self.control = self.boot.load(self.control_alias, self.bootstrap_buffers['control'], CONTROL_PATH)
        self.factory = self.boot.load(self.factory_alias, self.bootstrap_buffers['factory'], FACTORY_PATH)
        self.ordinary = ['ordinary_' + str(index) for index in range(23)]
        self.protected = ['protected_' + str(index) for index in range(3)]
        self.aliases = {name: '_qualified_parent_loader_' + name for name in self.ordinary + self.protected}
        rows = {}
        buffers = {}
        effective = {}
        for index, name in enumerate(self.ordinary + self.protected):
            raw = ('VALUE = ' + str(index) + '\n').encode() if name in self.ordinary else b'raise AssertionError("protected role must not execute")\n'
            path = 'invented_roles/' + name + '.py'
            rows[name] = dict(path=path, sha256=parent.sha(raw))
            buffers['role:' + name] = raw
            effective[path] = parent.sha(raw)
            if name in self.ordinary:
                target = self.root / path
                target.parent.mkdir(exist_ok=True)
                with target.open('xb') as stream:
                    stream.write(raw)
        self.validated = dict(candidate=dict(repository_root=str(self.root)),
            inputs=dict(binding_schema=dict(load_order=self.ordinary, protected_order=self.protected,
                                           aliases=self.aliases), role_authority=dict(roles=rows)),
            source_buffers=buffers, effective_qualified_sources=effective)
        session = self.root / 'session'
        session.mkdir()
        seal = b'{"invented_read_guard_fixture":true}\n'
        (session / 'execution-seal.json').write_bytes(seal)
        self.context = dict(schema='gdt_io_context_v1', session_dir=session, repository_root=self.root,
            operation_id='a' * 32, execution_seal_sha256=parent.sha(seal), basis={}, source_manifest={},
            implementation_sha256={}, ordinary_sha256={rows[name]['path']: rows[name]['sha256'] for name in self.ordinary},
            child_argv=[], deadline_seconds=300, limits={'poll_seconds': .05})

    def loader(self, validated=None):
        result = parent.parent_validation_sources(self.validated if validated is None else validated,
            gate, self.control, self.factory)
        self.addCleanup(lambda: None if result.closed else result.close())
        return result

    def activate(self, loader):
        sys.meta_path.insert(0, loader)

    def replace_ordinary(self, name, raw):
        row = self.validated['inputs']['role_authority']['roles'][name]
        row['sha256'] = parent.sha(raw)
        self.validated['effective_qualified_sources'][row['path']] = parent.sha(raw)
        self.validated['source_buffers']['role:' + name] = raw
        (self.root / row['path']).write_bytes(raw)

    def test_real_registration_loads_23_ordinary_excludes_three_protected_and_closes_bootstraps(self):
        self.assertIs(self.control.verify_context(self.context), True)
        loader = self.loader()
        self.assertIs(type(loader), self.factory.AuthoredSources)
        self.assertEqual(loader.__class__.exec_module.__code__.co_filename, str(FACTORY_PATH))
        self.assertEqual(set(loader.entries), {self.aliases[name] for name in self.ordinary})
        self.assertEqual(len(loader.entries), 23)
        self.assertTrue(all(self.aliases[name] not in loader.entries and not (
            self.root / self.validated['inputs']['role_authority']['roles'][name]['path']).exists()
            for name in self.protected))
        self.activate(loader)
        loaded = [importlib.import_module(self.aliases[name]) for name in self.ordinary]
        self.assertEqual([module.VALUE for module in loaded], list(range(23)))
        self.assertEqual(set(loader.loaded), set(loader.entries))
        self.assertTrue(all(sys.modules[module.__name__] is module for module in loaded))
        self.assertIs(sys.modules[self.control_alias], self.control)
        self.assertIs(sys.modules[self.factory_alias], self.factory)
        loader.close()
        self.assertTrue(loader.closed)
        self.assertNotIn(loader, sys.meta_path)
        self.assertTrue(all(module.__name__ not in sys.modules for module in loaded))
        self.assertIs(self.boot.close(), True)
        self.assertTrue(self.boot.closed)
        self.assertNotIn(self.control_alias, sys.modules)
        self.assertNotIn(self.factory_alias, sys.modules)

    def test_wrong_ordinary_protected_partition_refuses(self):
        for kind in ('missing_ordinary', 'duplicate_ordinary', 'missing_protected', 'overlap', 'extra_authority'):
            args = copy.deepcopy(self.validated)
            schema = args['inputs']['binding_schema']
            if kind == 'missing_ordinary':
                schema['load_order'].pop()
            elif kind == 'duplicate_ordinary':
                schema['load_order'][-1] = schema['load_order'][0]
            elif kind == 'missing_protected':
                schema['protected_order'].pop()
            elif kind == 'overlap':
                schema['protected_order'][0] = schema['load_order'][0]
            else:
                args['inputs']['role_authority']['roles']['extra'] = dict(path='invented_roles/extra.py', sha256='f' * 64)
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, 'operational_launch_parent_roles'):
                self.loader(args)
        self.assertTrue(all(alias not in sys.modules for alias in self.aliases.values()))

    def test_cached_role_authority_and_effective_hashes_must_all_match(self):
        name = self.ordinary[2]
        for kind in ('buffer', 'authority', 'effective'):
            args = copy.deepcopy(self.validated)
            row = args['inputs']['role_authority']['roles'][name]
            if kind == 'buffer':
                args['source_buffers']['role:' + name] += b'# drift\n'
            elif kind == 'authority':
                row['sha256'] = 'f' * 64
            else:
                args['effective_qualified_sources'][row['path']] = 'f' * 64
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, 'operational_launch_parent_role_hash'):
                self.loader(args)
        self.assertTrue(all(alias not in sys.modules for alias in self.aliases.values()))

    def test_preexisting_and_duplicate_role_aliases_are_not_overwritten(self):
        alias = self.aliases[self.ordinary[3]]
        foreign = ModuleType(alias)
        sys.modules[alias] = foreign
        self.addCleanup(lambda: sys.modules.pop(alias, None))
        with self.assertRaises(gate.GateError):
            self.loader()
        self.assertIs(sys.modules[alias], foreign)
        del sys.modules[alias]
        args = copy.deepcopy(self.validated)
        args['inputs']['binding_schema']['aliases'][self.ordinary[1]] = self.aliases[self.ordinary[0]]
        with self.assertRaises(gate.GateError):
            self.loader(args)
        self.assertTrue(all(alias not in sys.modules for alias in self.aliases.values()))
        # A loaded bootstrap alias is likewise never replaced or re-owned.
        with self.assertRaises(ValueError):
            self.boot.load(self.control_alias, self.bootstrap_buffers['control'], CONTROL_PATH)
        self.assertIs(sys.modules[self.control_alias], self.control)

    def test_disk_drift_is_rejected_by_context_guard_but_cannot_replace_cached_execution(self):
        self.assertIs(self.control.verify_context(self.context), True)
        loader = self.loader()
        name = self.ordinary[0]
        path = self.root / self.validated['inputs']['role_authority']['roles'][name]['path']
        path.write_bytes(b'raise AssertionError("drifted disk source must not execute")\n')
        with self.assertRaises(self.control.IoEntryError):
            self.control.verify_context(self.context)
        self.activate(loader)
        # Demonstrate the loader boundary explicitly: it does not revalidate
        # disk freshness, and executes the already checked cached bytes only.
        with patch.object(Path, 'open', side_effect=AssertionError('unexpected source disk read')):
            module = importlib.import_module(self.aliases[name])
        self.assertEqual(module.VALUE, 0)

    def test_source_sys_path_mutation_is_refused_and_restored(self):
        name = self.ordinary[0]
        self.replace_ordinary(name, b'import sys\nsys.path.append("invented unwanted path")\n')
        loader = self.loader()
        self.activate(loader)
        before = list(sys.path)
        with self.assertRaises(gate.GateError):
            importlib.import_module(self.aliases[name])
        self.assertEqual(sys.path, before)
        self.assertNotIn(self.aliases[name], sys.modules)
        self.assertNotIn(self.aliases[name], loader.loaded)
        self.assertEqual(importlib.import_module(self.aliases[self.ordinary[1]]).VALUE, 1)

    def test_source_exception_removes_failed_alias_and_preserves_owned_cleanup(self):
        name = self.ordinary[1]
        self.replace_ordinary(name, b'raise RuntimeError("invented role failure")\n')
        loader = self.loader()
        self.activate(loader)
        first = importlib.import_module(self.aliases[self.ordinary[0]])
        with self.assertRaisesRegex(RuntimeError, 'invented role failure'):
            importlib.import_module(self.aliases[name])
        self.assertNotIn(self.aliases[name], sys.modules)
        self.assertIs(sys.modules[first.__name__], first)
        loader.close()
        self.assertNotIn(first.__name__, sys.modules)
        self.assertNotIn(loader, sys.meta_path)

    def test_real_finder_blocks_unbound_authored_helpers_and_defers_dependency_policy(self):
        loader = self.loader()
        for name, error in (('tools.invented_unbound', 'unbound_authored_import'),
                            ('invented_nonstdlib_helper', 'unbound_authored_helper'),
                            (self.aliases[self.protected[0]], 'unbound_authored_helper')):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, error):
                loader.find_spec(name)
        self.assertIsNone(loader.find_spec('os'))
        self.assertIsNone(loader.find_spec('Cryptodome'))
        self.assertIsNone(loader.find_spec('Cryptodome.Cipher'))
        self.assertEqual(loader.loaded, {})
        self.assertTrue(all(alias not in sys.modules for alias in self.aliases.values()))

    def test_role_alias_replacement_is_preserved_and_other_aliases_are_released(self):
        loader = self.loader()
        self.activate(loader)
        first = importlib.import_module(self.aliases[self.ordinary[0]])
        second = importlib.import_module(self.aliases[self.ordinary[1]])
        foreign = ModuleType(first.__name__)
        sys.modules[first.__name__] = foreign
        self.addCleanup(lambda: sys.modules.pop(first.__name__, None))
        with self.assertRaises(gate.GateError):
            loader.close()
        self.assertTrue(loader.closed)
        self.assertNotIn(loader, sys.meta_path)
        self.assertIs(sys.modules[first.__name__], foreign)
        self.assertNotIn(second.__name__, sys.modules)
        self.assertIsNone(loader.close())
        self.assertIs(sys.modules[first.__name__], foreign)

    def test_bootstrap_alias_replacement_preserves_foreign_owner_and_releases_other_bootstrap(self):
        foreign = ModuleType(self.factory_alias)
        sys.modules[self.factory_alias] = foreign
        self.addCleanup(lambda: sys.modules.pop(self.factory_alias, None))
        with self.assertRaisesRegex(ValueError, 'operational_launch_bootstrap_ownership'):
            self.boot.close()
        self.assertTrue(self.boot.closed)
        self.assertIs(sys.modules[self.factory_alias], foreign)
        self.assertNotIn(self.control_alias, sys.modules)
        with self.assertRaisesRegex(ValueError, 'operational_launch_bootstrap_reclose'):
            self.boot.close()
        self.assertIs(sys.modules[self.factory_alias], foreign)


if __name__ == '__main__':
    unittest.main(verbosity=2)
