"""Real retained authored context checker over invented ordinary files only.

The private authored source is identity-pinned, never copied into Git. An export
without that source skips explicitly; a changed source fails. This does not run
its loader, supervisor, callbacks or any protected-input path. The real checker
proves ordinary-file consistency only, not execution permission or target support.
"""
import ast
import builtins
import copy
import hashlib
from pathlib import Path
import stat
from types import ModuleType
import unittest
from unittest.mock import patch

from tools import dependency_host_entry as host
import test_dependency_current_context as current_fixture


REPOSITORY = Path(__file__).resolve().parents[1]
RETAINED_PATH = REPOSITORY / 'private/sessions/20261019-RA-003-parent-evidence-v5/activation/io_entry.py'
RETAINED_SHA256 = '70a2ed3a0265894adace48e5285c0eb8962c666975f7df1a8e4f6141b918bb43'
RETAINED_BYTES = 58942
IMPORTS = frozenset(('datetime', 'hashlib', 'json', 'math', 'os', 'pathlib',
                     'stat', 'threading', 'types'))


def load_retained_checker():
    """Load exactly the reviewed authored source; no source rewriting or mocks."""
    try:
        status = RETAINED_PATH.lstat()
    except FileNotFoundError:
        raise unittest.SkipTest('private authored retained checker unavailable in this export')
    if not stat.S_ISREG(status.st_mode) or status.st_nlink != 1:
        raise AssertionError('retained checker must be an ordinary single-link file')
    raw = RETAINED_PATH.read_bytes()
    if len(raw) != RETAINED_BYTES or hashlib.sha256(raw).hexdigest() != RETAINED_SHA256:
        raise AssertionError('retained authored checker identity changed')
    tree = ast.parse(raw, filename=str(RETAINED_PATH))
    imports = {n.module if isinstance(n, ast.ImportFrom) else a.name
               for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))
               for a in (n.names if isinstance(n, ast.Import) else [None])}
    # gdt_preflight is a dormant callback import outside verify_context's call
    # graph. Keep it statically accounted for and refuse any runtime activation.
    if imports != IMPORTS | {'gdt_preflight'}:
        raise AssertionError('retained import set changed')
    importer = builtins.__import__
    def checked_import(name, *args, **kwargs):
        if name not in IMPORTS:
            raise AssertionError('unexpected retained import: ' + name)
        return importer(name, *args, **kwargs)
    module = ModuleType('_qualified_retained_context_checker')
    module.__file__ = str(RETAINED_PATH)
    module.__builtins__ = dict(vars(builtins), __import__=checked_import)
    exec(compile(tree, str(RETAINED_PATH), 'exec', dont_inherit=True), vars(module))
    return module


def materialize_invented_context(fixture):
    """Write only the existing fixture's invented metadata and inert source text."""
    v = fixture.validated
    root = fixture.root
    documents = fixture.original['legacy_documents']
    def write(path, raw):
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            if path.read_bytes() != raw:
                raise AssertionError('invented fixture path conflict')
        else:
            with path.open('xb') as stream:
                stream.write(raw)
    for name, row in v['candidate']['inputs'].items():
        write(root / row['path'], documents['inputs'][name])
    for name, row in v['inputs']['source_cache']['sources'].items():
        write(Path(row['path']), v['source_buffers'][name])
    here = root / v['candidate']['session']
    for name, filename in (('candidate', 'activation-candidate.json'),
                           ('review', 'activation-review.json'),
                           ('decision', 'act-decision.json'),
                           ('seal', 'execution-seal.json')):
        write(here / filename, documents[name])
    for name, row in v['candidate']['bootstrap'].items():
        # Historical fixture pins name.encode(); these are data, never imported.
        write(root / row['path'], name.encode())
    write(fixture.request_path, fixture.arguments()['request_bytes'])
    return fixture.construct()


class RetainedContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checker = load_retained_checker()

    def setUp(self):
        self.fixture = current_fixture.CurrentContextTests()
        self.addCleanup(self.fixture.doCleanups)
        self.fixture.setUp()
        self.context = materialize_invented_context(self.fixture)

    def verify(self, context=None):
        return self.checker.verify_context(self.context if context is None else context)

    def test_exact_retained_function_accepts_constructed_context(self):
        self.assertEqual(self.checker.verify_context.__code__.co_filename, str(RETAINED_PATH))
        self.assertEqual(self.checker.verify_context.__code__.co_firstlineno, 202)
        before = copy.deepcopy(self.context)
        self.assertIs(self.verify(), True)
        self.assertEqual(self.context, before)

    def test_reads_stay_in_invented_tree_and_do_not_follow_source_manifest(self):
        opened = []
        original = Path.open
        root = self.fixture.root
        def observed(path, *args, **kwargs):
            self.assertTrue(path.is_relative_to(root), str(path))
            opened.append(path)
            return original(path, *args, **kwargs)
        with patch.object(Path, 'open', observed):
            self.assertIs(self.verify(), True)
        self.assertGreater(len(opened), 40)
        forbidden = root / self.context['source_manifest']['relative_path']
        self.assertNotIn(forbidden, opened)
        self.assertFalse(forbidden.exists())

    def test_each_current_document_tamper_is_rejected(self):
        here = self.context['session_dir']
        paths = [here / n for n in ('execution-seal.json', 'activation-candidate.json',
                                    'activation-review.json', 'act-decision.json')]
        paths += [self.fixture.request_path, self.fixture.folder / 'packet.json']
        for path in paths:
            original = path.read_bytes()
            try:
                path.write_bytes(original + b' ')
                with self.subTest(path=path.name), self.assertRaises(self.checker.IoEntryError):
                    self.verify()
            finally:
                path.write_bytes(original)

    def test_current_and_retained_source_tamper_are_rejected(self):
        for bound in (False, True):
            name = next(n for n in self.fixture.rows if n.startswith('bound.') == bound)
            path = Path(self.fixture.rows[name]['path'])
            original = path.read_bytes()
            try:
                path.write_bytes(original + b'# drift\n')
                with self.subTest(bound=bound), self.assertRaises(self.checker.IoEntryError):
                    self.verify()
            finally:
                path.write_bytes(original)

    def test_implementation_bytes_are_checked_separately(self):
        path = self.context['session_dir'] / next(iter(self.context['implementation_sha256']))
        path.write_bytes(b'invented changed implementation')
        with self.assertRaises(self.checker.IoEntryError):
            self.verify()

    def test_missing_ordinary_file_is_not_accepted(self):
        self.fixture.request_path.unlink()
        with self.assertRaises(FileNotFoundError):
            self.verify()

    def test_directory_cannot_replace_an_ordinary_file(self):
        self.fixture.request_path.unlink()
        self.fixture.request_path.mkdir()
        with self.assertRaises(self.checker.IoEntryError):
            self.verify()

    def test_hard_link_is_rejected_when_supported(self):
        linked = self.fixture.root / 'invented-hardlink.json'
        try:
            linked.hardlink_to(self.fixture.request_path)
        except OSError as error:
            self.skipTest('host cannot create an invented hard link; errno=' + str(error.errno))
        with self.assertRaises(self.checker.IoEntryError):
            self.verify()

    def test_symlink_is_rejected_when_supported(self):
        target = self.fixture.root / 'invented-symlink-target.json'
        target.write_bytes(self.fixture.request_path.read_bytes())
        self.fixture.request_path.unlink()
        try:
            self.fixture.request_path.symlink_to(target)
        except OSError as error:
            self.skipTest('host cannot create an invented symlink; winerror=' +
                          str(getattr(error, 'winerror', None)) + '; errno=' + str(error.errno))
        with self.assertRaises(self.checker.IoEntryError):
            self.verify()

    def test_bad_context_shape_deadline_operation_and_relative_name_refuse(self):
        changes = [('schema', 'other'), ('deadline_seconds', True),
                   ('operation_id', 'not-a-hex-operation'), ('extra', None)]
        for name, value in changes:
            context = copy.deepcopy(self.context); context[name] = value
            with self.subTest(name=name), self.assertRaises(self.checker.IoEntryError):
                self.verify(context)
        context = copy.deepcopy(self.context)
        context['ordinary_sha256']['../outside.json'] = '0' * 64
        with self.assertRaises(self.checker.IoEntryError):
            self.verify(context)

    def test_checker_is_consistency_only_not_argv_or_basis_authority(self):
        context = copy.deepcopy(self.context)
        context.update(child_argv=['inert never executed'], basis={'invented': True},
                       source_manifest={'invented': True}, limits={'invented': True})
        self.assertIs(self.verify(context), True)
        self.assertIs(self.fixture.validated['execution_authorized'], False)
        self.assertIs(self.fixture.request['execution_authorized'], False)

    def test_inactive_retained_loader_still_refuses(self):
        with self.assertRaises(self.checker.IoEntryError) as caught:
            self.checker.load_ordinary_context(session_dir=self.context['session_dir'],
                expected_seal_sha256=self.context['execution_seal_sha256'])
        self.assertEqual(caught.exception.reason, 'future_activation_semantic_review_required')


if __name__ == '__main__':
    unittest.main(verbosity=2)
