"""Captured synthetic I/O role for the genuine child callback factory.

Only the same 31 pinned ordinary authored sources as FreshTerminal are read.
The returned role replaces IoAdapter explicitly: its logical bytes, source
events and snapshot are inventions. It never calls the supplied protected
preparation closure or I/O operations. The six original builder modules execute
from captured bytes in a short owned import scope inside the child; no terminal
result or saved basis is embedded. Production sources and entry guards are not
changed by this test helper.
"""
from dependency_terminal_fixture import selected_terminal_sources


_ADAPTER = rb'''
import copy
import importlib
import importlib.abc
import importlib.machinery
import importlib.util
from pathlib import Path
import sys

import gdt_preflight


SYNTHETIC_IO_OBSERVATIONS = []


def _require(value):
    if not value:
        raise AssertionError('synthetic child I/O fixture contract')


class _BuilderSources(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, root):
        self.root = root
        self.loaded = {}
        self.spec_owned = {}
        self.closed = False
        self.before = dict(sys.modules)
        self.entries = {Path(name).stem: (root / Path(name).name, raw)
                        for name, raw in _GENERATOR_SOURCES.items()}
        self.paths = {root / (name + '.py'): raw for name, raw in _ROLE_SOURCES.items()}
        self.paths.update({path: raw for path, raw in self.entries.values()})
        _require(len(self.entries) == 6 and len(self.paths) == 29)
        _require(not any(name in sys.modules for name in self.entries))

    def find_spec(self, fullname, path=None, target=None):
        if fullname in self.entries:
            _require(not self.closed)
            return importlib.machinery.ModuleSpec(fullname, self,
                origin=str(self.entries[fullname][0]))
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        _require(not self.closed and module.__name__ in self.entries)
        path, raw = self.entries[module.__name__]
        module.__file__ = str(path)
        module.__package__ = ''
        exec(compile(raw, str(path), 'exec', dont_inherit=True, optimize=0), vars(module))
        self.loaded[module.__name__] = module

    def source_spec(self, name, location, *args, **kwargs):
        # Old builders use detached sibling specs. Preserve their exact source
        # and object construction while replacing filesystem reads with this
        # closed captured map. A path label cannot add another import source.
        path = Path(location)
        _require(not self.closed and not args and not kwargs and path in self.paths)
        _require(name not in self.before)
        owner = self
        raw = self.paths[path]

        class CapturedSource(importlib.abc.Loader):
            def create_module(self, spec):
                return None

            def exec_module(self, module):
                _require(not owner.closed)
                module.__file__ = str(path)
                module.__package__ = ''
                exec(compile(raw, str(path), 'exec', dont_inherit=True, optimize=0), vars(module))
                # These builders normally leave spec-created modules detached.
                # If one registers itself, own only that exact new identity.
                current = sys.modules.get(name)
                if current is not None:
                    _require(current is module)
                    owner.spec_owned[name] = module

        return importlib.machinery.ModuleSpec(name, CapturedSource(), origin=str(path))

    def close(self):
        _require(not self.closed)
        self.closed = True
        primary = None
        if self in sys.meta_path:
            sys.meta_path.remove(self)
        for name, module in reversed(tuple(self.loaded.items()) + tuple(self.spec_owned.items())):
            if sys.modules.get(name) is module:
                del sys.modules[name]
            elif primary is None:
                primary = AssertionError('synthetic generator alias ownership changed')
        if primary is not None:
            raise primary


def _fresh_harness(source_path):
    _require(type(source_path) is type(Path()) and source_path.is_absolute())
    # This is only a filename namespace under the invented source's directory;
    # captured builders are compiled directly and create no source files.
    owner = _BuilderSources(source_path.parent / 'synthetic-child-generators')
    before_path = list(sys.path)
    original_spec = importlib.util.spec_from_file_location
    ours = owner.source_spec
    primary = cleanup = None
    harness = None
    try:
        importlib.util.spec_from_file_location = ours
        sys.meta_path.insert(0, owner)
        builder = importlib.import_module('test_gdt_runner')
        # Its prefix fixtures are a detached sibling-spec module, not the
        # optional test_prefix import alias. Build the entire fresh lineage
        # with the genuine classifier that ScopedCallbacks will later supply.
        # Restore only our own temporary binding; foreign changes are preserved
        # and reported, including when the builder raises.
        fixtures = builder.old.fixtures
        original_classifier = fixtures.classifier
        genuine_classifier = sys.modules['classifier'].classify
        fixtures.classifier = genuine_classifier
        construction_error = None
        try:
            harness = builder.Harness()
        except BaseException as error:
            construction_error = error
        if fixtures.classifier is genuine_classifier:
            fixtures.classifier = original_classifier
        else:
            changed = AssertionError('synthetic builder classifier ownership changed')
            if construction_error is not None:
                raise construction_error from changed
            raise changed
        if construction_error is not None:
            raise construction_error
        _require(sys.path == before_path)
    except BaseException as error:
        primary = error
    finally:
        # Report foreign replacement without overwriting it or abandoning the
        # other owned aliases. There is one close attempt and no retry.
        if importlib.util.spec_from_file_location is ours:
            importlib.util.spec_from_file_location = original_spec
        else:
            cleanup = AssertionError('synthetic generator spec ownership changed')
        try:
            owner.close()
        except BaseException as error:
            if cleanup is None:
                cleanup = error
        if sys.path != before_path:
            if cleanup is None:
                cleanup = AssertionError('synthetic generator sys.path changed')
        if primary is not None and cleanup is not None:
            raise primary from cleanup
        if cleanup is not None:
            raise cleanup
    if primary is not None:
        raise primary
    _require(harness is not None and owner.closed and
             all(name not in sys.modules for name in owner.loaded))
    return harness


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


class IoAdapter:
    """Invented event adapter; genuine callback factory remains unchanged."""
    def __init__(self, *, basis, source_path, prepare_protected, io_ops, stage_source):
        _require(callable(prepare_protected) and callable(stage_source) and
                 type(io_ops) is dict)
        self.harness = _fresh_harness(source_path)
        _require(gdt_preflight.exact(self.harness.fixture.basis, basis))
        self.basis = copy.deepcopy(basis)
        self.stage_source = stage_source
        self.state = _empty_snapshot()
        self.observation = dict(generator_built_in_child=True,
            generator_aliases_released=True, generator_source_files_written=False,
            genuine_classifier_used_to_generate_basis=True,
            source_events_and_snapshot_invented=True, terminal_replay=False,
            protected_prepare_calls=0, io_ops_calls=0, preparation_calls=0,
            inspect_phases=[], discard_phases=[], camera_commands=[])
        SYNTHETIC_IO_OBSERVATIONS.append(self.observation)
        # Retain neither the protected closure nor OS operations. They have no
        # call path from this explicit replacement role.

    def snapshot(self):
        return copy.deepcopy(self.state)

    def prepare(self, basis, resources):
        _require(gdt_preflight.exact(basis, self.basis) and
                 self.observation['preparation_calls'] == 0)
        self.observation['preparation_calls'] += 1
        self.state.update(status='incomplete', preparation_attempts=1)
        if _SYNTHETIC_MODE == 'prepare_interrupt':
            raise KeyboardInterrupt('invented child adapter preparation interruption')
        return self.harness.prepare(basis, resources)

    def _source_snapshot(self, phase, record):
        value = self.state['phase_' + phase.lower()]
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
        self.state['status'] = ('complete' if all(self.state[key]['status'] == 'complete'
            for key in ('phase_a', 'phase_b')) else 'incomplete')

    def inspect(self, phase, basis, resources, descriptors, source_event):
        _require(gdt_preflight.exact(basis, self.basis))
        self.observation['inspect_phases'].append(phase)
        def emit(record):
            self._source_snapshot(phase, record)
            self.stage_source(phase, record)
            return source_event(record)
        return self.harness.inspect(phase, basis, resources, descriptors, emit)

    def discard(self, resources, phase):
        self.observation['discard_phases'].append(phase)
        return self.harness.discard(resources, phase)
'''


def synthetic_io_adapter_source(mode='complete'):
    """Return a closed captured role; no private bytes are written by this API."""
    if mode not in ('complete', 'prepare_interrupt'):
        raise ValueError('unsupported synthetic child I/O mode')
    roles, generators, _ = selected_terminal_sources()
    prefix = ('_SYNTHETIC_MODE = ' + repr(mode) + '\n_ROLE_SOURCES = ' + repr(roles) + '\n_GENERATOR_SOURCES = ' +
              repr(generators) + '\n').encode('ascii')
    raw = prefix + _ADAPTER
    if not 0 < len(raw) <= 2 * 1024**2:
        raise AssertionError('synthetic child role source bound')
    return raw
