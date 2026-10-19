"""Detached checked-buffer adapter graph for invented integration only.

No process aliases, disk import, runtime activation or source-path reads.
The reviewed loader, interpreter and stdlib are trusted. This is not a sandbox.
"""
import ast
import builtins
import hashlib
from pathlib import Path
import sys
import types

if __name__ == '__main__':
    raise SystemExit(2)

ORDER = ('dependency_outer_contract', 'dependency_operational_scope', 'dependency_adapter_binding')
BUFFER_KEYS = dict(zip(ORDER, ('adapter_comparison', 'adapter_scope', 'adapter')))
EDGES = {'dependency_outer_contract': (),
         'dependency_operational_scope': ('dependency_outer_contract',),
         'dependency_adapter_binding': ('dependency_operational_scope',)}
EXTERNAL = frozenset(('hashlib', 'json', 'math', 'pathlib'))
CALLS = frozenset(('validate_request', 'check_sources', 'run_invented', 'reconcile_invented'))


def need(ok, code):
    if not ok:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class AdapterSources:
    def __init__(self, *, buffers, hashes):
        need(type(buffers) is dict and type(hashes) is dict and
             set(buffers) == set(hashes) == set(ORDER), 'adapter_loader_roster')
        self.buffers = dict(buffers)
        self.hashes = dict(hashes)
        self.modules = {}
        self.frozen = {}
        self.package = types.SimpleNamespace()
        self.started = self.loaded = self.closed = self.failed = False
        self.foreign = {n: m for n, m in sys.modules.items() if n == 'tools' or n.startswith('tools.')}
        total = 0
        trees = {}
        for name in ORDER:
            raw = self.buffers[name]
            need(type(raw) is bytes and 0 < len(raw) <= 2 * 1024**2, 'adapter_loader_bound')
            total += len(raw)
            need(total <= 4 * 1024**2 and type(self.hashes[name]) is str and
                 sha(raw) == self.hashes[name], 'adapter_loader_hash')
            tree = ast.parse(raw, filename='<checked-adapter:' + name + '>')
            authored = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    need(all(a.name in EXTERNAL for a in node.names), 'adapter_loader_import')
                elif isinstance(node, ast.ImportFrom):
                    need(node.level == 0, 'adapter_loader_import')
                    if node.module == 'tools':
                        authored.extend(a.name for a in node.names)
                    else:
                        need(node.module in EXTERNAL, 'adapter_loader_import')
            need(tuple(authored) == EDGES[name], 'adapter_loader_edges')
            trees[name] = tree
        # Complete hash/import validation precedes any compilation or execution.
        self.compiled = {n: compile(trees[n], '<checked-adapter:' + n + '>', 'exec',
                                   dont_inherit=True, optimize=0) for n in ORDER}
        self.construction = tuple(self.compiled.items())
        self.expected_hashes = tuple(self.hashes.items())

    def _stamp(self, value, active=None):
        active = set() if active is None else active
        kind = type(value)
        if value is None or kind in (str, int, bool, bytes):
            return kind, value
        if kind is float:
            return kind, value.hex()
        if id(value) in active:
            return kind, id(value), 'recursive'
        active.add(id(value))
        try:
            if kind is types.FunctionType and any(value.__globals__ is vars(m) for m in self.modules.values()):
                cells = []
                for cell in value.__closure__ or ():
                    try:
                        cells.append(self._stamp(cell.cell_contents, active))
                    except ValueError:
                        cells.append(('empty', id(cell)))
                return (kind, id(value), id(value.__code__), value.__module__,
                    self._stamp(value.__defaults__, active), self._stamp(value.__kwdefaults__, active),
                    self._stamp(value.__annotations__, active), self._stamp(vars(value), active), tuple(cells))
            if kind is dict:
                return kind, id(value), tuple((self._stamp(k, active), self._stamp(v, active)) for k, v in value.items())
            if kind in (list, tuple):
                return kind, id(value), tuple(self._stamp(v, active) for v in value)
            if kind in (set, frozenset):
                return kind, id(value), frozenset(self._stamp(v, active) for v in value)
            return kind, id(value)  # Borrowed stdlib objects are trusted by identity.
        finally:
            active.remove(id(value))

    def intact(self):
        try:
            need(self.started and not self.closed and not self.failed, 'adapter_loader_inactive')
            need(tuple(self.hashes.items()) == self.expected_hashes and
                 set(self.compiled) == {n for n, code in self.construction} and
                 all(self.compiled[n] is code for n, code in self.construction), 'adapter_loader_policy_changed')
            need(set(self.buffers) == set(ORDER) and all(
                type(self.buffers[n]) is bytes and 0 < len(self.buffers[n]) <= 2 * 1024**2 and
                sha(self.buffers[n]) == self.hashes[n] for n in ORDER), 'adapter_loader_buffer_changed')
            current = {n: m for n, m in sys.modules.items() if n == 'tools' or n.startswith('tools.')}
            need(current.keys() == self.foreign.keys() and
                 all(current[n] is m for n, m in self.foreign.items()), 'adapter_loader_foreign_alias')
            need(set(vars(self.package)) == set(self.modules) and
                 all(vars(self.package)[n] is m for n, m in self.modules.items()), 'adapter_loader_namespace')
            need(set(self.frozen) <= set(self.modules), 'adapter_loader_roster')
            for name, stamp in self.frozen.items():
                need(self._stamp(vars(self.modules[name])) == stamp, 'adapter_loader_live_code')
            if self.loaded:
                need(set(self.modules) == set(self.frozen) == set(ORDER), 'adapter_loader_roster')
        except BaseException:
            self.failed = True
            raise

    def _import(self, name, globals=None, locals=None, fromlist=(), level=0):
        try:
            self.intact()
            need(level == 0, 'adapter_loader_import')
            if name == 'tools':
                need(type(fromlist) in (tuple, list) and fromlist and
                     all(n in self.modules for n in fromlist), 'adapter_loader_import')
                return self.package
            need(name in EXTERNAL, 'adapter_loader_import')
            return builtins.__import__(name, globals, locals, fromlist, level)
        except BaseException:
            self.failed = True
            raise

    def load(self):
        need(not self.started and not self.closed, 'adapter_loader_reentry')
        self.started = True
        try:
            for name in ORDER:
                self.intact()
                module = types.ModuleType('_a6700_adapter.' + name)
                module.__file__ = '<checked-adapter:' + name + '>'
                module.__package__ = '_a6700_adapter'
                module.__builtins__ = dict(vars(builtins), __import__=self._import)
                self.modules[name] = module
                setattr(self.package, name, module)
                exec(self.compiled[name], vars(module))
                self.frozen[name] = self._stamp(vars(module))
                self.intact()
            self.loaded = True
            self.intact()
            return self
        except BaseException as primary:
            self.failed = True
            try:
                self.close()
            except BaseException as cleanup:
                raise primary from cleanup
            raise

    def call(self, name, **kwargs):
        self.intact()
        need(self.loaded and name in CALLS, 'adapter_loader_call')
        try:
            result = getattr(self.modules['dependency_adapter_binding'], name)(**kwargs)
        except BaseException as primary:
            try:
                self.intact()
            except BaseException as changed:
                raise primary from changed
            raise
        self.intact()
        return result

    def project(self, *, process_sources, process_buffers, repository_root):
        """Explicitly map harness receipts to prepared role labels, without I/O.

        Six function roles share the adapter buffer. Other process harness code,
        this loader and invented fixture stay bound in the outer process map;
        they are not silently counted as operational role replacements.
        """
        self.intact()
        for name, key in BUFFER_KEYS.items():
            need(process_buffers[key] == self.buffers[name] and
                 process_sources[key]['sha256'] == self.hashes[name] and
                 process_sources[key]['size'] == len(self.buffers[name]),
                 'adapter_projection_loaded_source')
        binding = self.modules['dependency_adapter_binding']
        root = Path(repository_root)
        sources, buffers = {}, {}
        for role in binding.SOURCE_ROLES:
            key = ('adapter' if role in binding.ENTRIES else
                   'adapter_scope' if role == 'adapter.scope_policy' else
                   'adapter_comparison' if role == 'adapter.comparison_contract' else role)
            row, raw = process_sources[key], process_buffers[key]
            need(type(raw) is bytes and sha(raw) == row['sha256'] and len(raw) == row['size'],
                 'adapter_projection_source')
            if role in binding.ENTRIES:
                path = binding.ADAPTER_PATH
            elif role == 'adapter.scope_policy':
                path = 'tools/dependency_operational_scope.py'
            elif role == 'adapter.comparison_contract':
                path = 'tools/dependency_outer_contract.py'
            else:
                path = Path(row['path']).relative_to(root).as_posix()
            sources[role] = dict(path=path, bytes=len(raw), sha256=sha(raw), entry=binding.ENTRIES.get(role))
            buffers[role] = raw
        binding.check_sources(sources, buffers)
        self.intact()
        return sources, buffers

    def close(self):
        need(not self.closed, 'adapter_loader_reclose')
        try:
            if self.started and not self.failed:
                self.intact()
        finally:
            self.closed = True
            self.modules.clear()
            self.frozen.clear()
            self.compiled.clear()
            self.buffers.clear()
            self.construction = ()
            self.expected_hashes = ()
            self.hashes.clear()
            self.foreign.clear()
            vars(self.package).clear()
        return True


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
