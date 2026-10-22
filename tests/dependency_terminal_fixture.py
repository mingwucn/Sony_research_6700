"""Fresh invented GDT terminal inputs through the genuine authored source graph.

Read only the finite pinned ordinary Python closure below. The six historical
fixture builders generate new logical data and metadata; no saved basis, stream,
firmware, constants or installed dependency is read. Genuine v5 AuthoredSources,
runner, gates and retained control remain unchanged. Source stamps/hash claims
and adapter snapshots are explicit inventions, not observations of source I/O.
Private-source absence skips; an identity change fails. This is a trusted test
composition, not a sandbox or an operational entry point.
"""
import copy
import hashlib
import importlib
import importlib.util
from pathlib import Path
import stat
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tools import dependency_historical_gate as policy
from tools import dependency_host_entry as host
from tools import dependency_operational_launcher as parent
from test_dependency_parent_loader import (
    selected_bootstrap_sources, FACTORY_PATH, CONTROL_PATH,
)


REPOSITORY = Path(__file__).resolve().parents[1]
ROLE_ROOT = REPOSITORY / 'private/sessions/20261019-RA-003-parent-evidence-v5/roles'
GENERATOR_ROOT = REPOSITORY / 'private/sessions/20261019-RA-003-gdt-runner-design'
ROLE_NAMES = parent.process.RETAINED[:23]
GENERATOR_PINS = {
    'gdt_dev_fixtures.py': (5820, 'e38330df9e27166f103f466287e03bbae50e7f84f308dc164e467421a342c18a'),
    'test_gdt_runner.py': (20966, 'fe5c2f303a87940742ca2840fe65efc3ede2825aad46783f36e6af2219c007fb'),
    'inherited/test_expanded_gate.py': (18537, '936139cd403e1db698eaf684207b32d437ae5ad6d3ac500052c6d41acb727556'),
    'inherited/test_member_acceptance.py': (13681, 'e573de0323c5149989185439b1ce1736103a1404ffe29dbd1ceb01c93218e4a9'),
    'inherited/test_link_acceptance.py': (17051, '5cb6e89f685e746c9cecfe811f06bf24f72384896499ec769d9c12a138a52994'),
    'inherited/test_prefix.py': (19250, 'bbdcb2a587b76f0c9dd5f6258306337d2bc8387a3d2750210b03ce42a7ce2eb2'),
}
_MISSING = object()


def _require(value):
    if not value:
        raise AssertionError('fresh terminal fixture contract')


def _pinned_source(path, digest, size=None):
    try:
        before = path.lstat()
    except FileNotFoundError:
        raise unittest.SkipTest('private authored terminal fixture unavailable in this export')
    _require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
             not getattr(before, 'st_file_attributes', 0) & 0x400)
    raw = path.read_bytes()
    after = path.lstat()
    stamp = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    _require(stamp(before) == stamp(after) and 0 < len(raw) <= 2 * 1024**2 and
             hashlib.sha256(raw).hexdigest() == digest and
             (size is None or len(raw) == size))
    return raw


def selected_terminal_sources():
    """Exactly 23 ordinary roles, six builders and two bootstrap sources."""
    _require(len(ROLE_NAMES) == 23 and not set(ROLE_NAMES) & {'capture', 'core', 'validator'})
    roles = {name: _pinned_source(ROLE_ROOT / (name + '.py'),
             policy.PARENT_EVIDENCE_POLICY['source_sha256']['roles/' + name + '.py'])
             for name in ROLE_NAMES}
    generators = {name: _pinned_source(GENERATOR_ROOT / name, digest, size)
                  for name, (size, digest) in GENERATOR_PINS.items()}
    return roles, generators, selected_bootstrap_sources()


def _empty_snapshot():
    def phase(name):
        def source_pass():
            return dict(read_attempts=0, read_calls=0, bytes_returned=0,
                        eof_probes=0, last_read='not_started',
                        failed_read_returned_bytes_unknown=False, verified=False)
        return dict(phase=name, status='not_started', open_attempts=0,
                    open_succeeded=False, rewind_attempts=0, rewind_succeeded=False,
                    close_attempts=0, close_succeeded=False,
                    capture=source_pass(), decode=source_pass())
    return dict(schema='gdt_io_snapshot_v1', status='not_started',
                preparation_attempts=0, phase_a=phase('A'), phase_b=phase('B'))


class FreshTerminal:
    """One fresh builder/callback scope; exit before installing a parent loader.

    Metadata and captured role bytes remain available after close. Runner and
    callback use belong inside this scope. The snapshot is generated from the
    invented Harness events; it does not instrument actual file handles.
    """
    def __init__(self, *, genuine_classifier=False):
        self.genuine_classifier = genuine_classifier
        self.active = self.claimed = False
        self.loader = self.boot = self.temporary = self.spec_patch = None
        self.harness = self.runner = None
        self.snapshot_value = _empty_snapshot()
        self._spec_paths = {}
        self._spec_owned = {}
        self._tools = None
        self._tools_before = {}

    def __enter__(self):
        _require(not self.active and self.boot is None)
        self.role_sources, generators, bootstrap = selected_terminal_sources()
        self.factory_raw = bootstrap['factory']
        self.control_raw = bootstrap['control']
        self.aliases = {n: ('tools.' + n if n in ('artifact_probe', 'offline_inventory') else n)
                        for n in ROLE_NAMES}
        self.source_pins = {str(ROLE_ROOT / (n + '.py')): hashlib.sha256(b).hexdigest()
                            for n, b in self.role_sources.items()}
        self.source_pins.update({str(GENERATOR_ROOT / n): hashlib.sha256(b).hexdigest()
                                 for n, b in generators.items()})
        self.source_pins.update({str(FACTORY_PATH): hashlib.sha256(bootstrap['factory']).hexdigest(),
                                 str(CONTROL_PATH): hashlib.sha256(bootstrap['control']).hexdigest()})
        self.temporary = tempfile.TemporaryDirectory(prefix='a6700-invented-terminal-')
        self.root = Path(self.temporary.name)
        self._tools = sys.modules.get('tools')
        self._tools_before = {name: getattr(self._tools, name, _MISSING)
                              for name in ('artifact_probe', 'offline_inventory')}
        self._modules_before = dict(sys.modules)
        self.boot = parent.BootstrapOwner(host)
        try:
            self.control = self.boot.load('_invented_terminal_control', bootstrap['control'], CONTROL_PATH)
            self.factory = self.boot.load('_invented_terminal_factory', bootstrap['factory'], FACTORY_PATH)
            self.loader = self.factory.AuthoredSources(SimpleNamespace(require=_require))
            staged = {}
            for name, raw in self.role_sources.items():
                path = self.root / (name + '.py')
                with path.open('xb') as stream:
                    stream.write(raw)
                staged[path] = raw
                self.loader.add(self.aliases[name], path, raw)
            for name, raw in generators.items():
                path = self.root / Path(name).name
                with path.open('xb') as stream:
                    stream.write(raw)
                staged[path] = raw
                self.loader.add(path.stem, path, raw)

            # The unmodified old builders use explicit sibling module specs.
            # Their only disk import targets are these exact temporary copies.
            original_spec = importlib.util.spec_from_file_location
            def source_spec(name, location, *args, **kwargs):
                path = Path(location).resolve()
                _require(path in staged and path.read_bytes() == staged[path])
                _require(name not in self._modules_before)
                self._spec_paths[name] = path
                return original_spec(name, location, *args, **kwargs)
            self.spec_patch = patch.object(importlib.util, 'spec_from_file_location', source_spec)
            self.spec_patch.start()
            sys.meta_path.insert(0, self.loader)
            builder = importlib.import_module('test_gdt_runner')
            original_classifier = builder.old.fixtures.classifier
            classifier = importlib.import_module('classifier').classify if self.genuine_classifier else original_classifier
            try:
                # Regenerate the invented lineage consistently; acceptance
                # predicates and the captured classifier source stay intact.
                builder.old.fixtures.classifier = classifier
                self.harness = builder.Harness()
            finally:
                _require(builder.old.fixtures.classifier is classifier)
                builder.old.fixtures.classifier = original_classifier
            self.runner = importlib.import_module('gdt_runner')
            self.basis = copy.deepcopy(self.harness.fixture.basis)
            measured = self.harness.fixture.measured['stream_measurement']
            self.source_manifest = dict(bytes=measured['actual_decoding_pass_parent_bytes'],
                                        sha256=measured['actual_decoding_pass_parent_sha256'])
            # Revalidate the fresh basis through the exact loaded ordinary role.
            importlib.import_module('gdt_preflight').freeze_basis(**self.basis)
            self._capture_spec_modules()
            self.active = True
            return self
        except BaseException:
            self._capture_spec_modules()
            self.close()
            raise

    def _capture_spec_modules(self):
        # These six fixed builders normally leave explicit spec modules
        # detached. Account for registration if their import path does so.
        for name, path in self._spec_paths.items():
            module = sys.modules.get(name)
            if module is not None and name not in self._modules_before:
                _require(Path(getattr(module, '__file__', '')).resolve() == path)
                self._spec_owned[name] = module

    def _source_snapshot(self, phase, record):
        value = self.snapshot_value['phase_' + phase.lower()]
        kind = record['kind']
        if kind == 'source_open_attempt':
            value.update(status='incomplete', open_attempts=1)
        elif kind == 'source_opened':
            value['open_succeeded'] = True
        elif kind == 'source_pass_attempt' and record['pass'] == 'decode':
            value.update(rewind_attempts=1, rewind_succeeded=True)
        elif kind in ('source_pass_progress', 'source_pass_verified'):
            result = value[record['pass']]
            result.update(read_attempts=record['read_calls'], read_calls=record['read_calls'],
                          bytes_returned=record['bytes_returned'], eof_probes=record['eof_probes'],
                          last_read='eof' if record['eof_probes'] else 'positive',
                          verified=kind == 'source_pass_verified')
        elif kind == 'source_stable':
            value.update(status='complete', close_attempts=1, close_succeeded=True)
        self.snapshot_value['status'] = ('complete' if all(self.snapshot_value[k]['status'] == 'complete'
                                        for k in ('phase_a', 'phase_b')) else 'incomplete')

    def make_callbacks(self, controller, stage_source):
        _require(self.active and not self.claimed)
        self.claimed = True
        _require(self.control.exact(self.control.context_copy(controller.ordinary)['basis'], self.basis))
        controller.bind_snapshot(lambda: copy.deepcopy(self.snapshot_value))
        def prepare(basis, resources):
            _require(self.active)
            self.snapshot_value.update(status='incomplete', preparation_attempts=1)
            return self.harness.prepare(basis, resources)
        def inspect(phase, basis, resources, descriptors, source_event):
            _require(self.active)
            def emit(record):
                self._source_snapshot(phase, record)
                stage_source(phase, record)
                return source_event(record)
            return self.harness.inspect(phase, basis, resources, descriptors, emit)
        old = sys.modules['test_expanded_gate']
        return dict(runner=self.runner, basis=copy.deepcopy(self.basis), prepare=prepare,
                    inspect=inspect, discard=self.harness.discard,
                    original_classifier=(sys.modules['classifier'].classify if self.genuine_classifier else old.fixtures.classifier),
                    expanded_classifier=sys.modules['header_candidates'].classify)

    def close(self):
        self.active = False
        first = None
        # MetaPathFinder.close handles aliases, but ordinary package attributes
        # can survive an alias removal. Restore only attributes still ours.
        for name, before in self._tools_before.items():
            current = getattr(self._tools, name, _MISSING)
            owned = None if self.loader is None else self.loader.loaded.get('tools.' + name)
            if current is before:
                continue
            if owned is not None and current is owned and sys.modules.get('tools') is self._tools:
                if before is _MISSING:
                    delattr(self._tools, name)
                else:
                    setattr(self._tools, name, before)
            elif first is None:
                first = AssertionError('fresh terminal tools attribute ownership changed')
        for owner in (self.loader, self.boot):
            if owner is not None and not owner.closed:
                try:
                    owner.close()
                except BaseException as error:
                    if first is None:
                        first = error
        for name, module in reversed(tuple(self._spec_owned.items())):
            current = sys.modules.get(name)
            if current is module:
                del sys.modules[name]
            elif current is not None and first is None:
                first = AssertionError('fresh terminal explicit module ownership changed')
        if self.spec_patch is not None:
            self.spec_patch.stop()
            self.spec_patch = None
        self.harness = self.runner = None
        if self.temporary is not None:
            self.temporary.cleanup()
            self.temporary = None
        if first is not None:
            raise first

    def __exit__(self, exc_type, exc, traceback):
        try:
            self.close()
        except BaseException as cleanup:
            if exc is not None:
                raise exc from cleanup
            raise
        return False
