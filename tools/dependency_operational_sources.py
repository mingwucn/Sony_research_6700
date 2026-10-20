"""Detached checked-buffer graph for disabled operational preparation engines.

No disk imports, aliases, observers or permission decisions. Initial loader,
interpreter and stdlib are trusted. Private engine calls remain capable APIs.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import ast
import builtins
import hashlib
import sys
import types

ORDER = ('dependency_operational_metadata', 'dependency_host_entry',
         'dependency_operational_entry', 'dependency_successor_wiring',
         'dependency_successor_sources', 'dependency_adapter_sources',
         'retained_gate', 'ordinary_io', 'dependency_operational_preparation')
EDGES = {n:() for n in ORDER}
EDGES['dependency_operational_preparation'] = ('dependency_operational_metadata', 'dependency_host_entry')
DATA_ONLY = ('parent_verifier',)
ROSTER = ORDER + DATA_ONLY


def need(ok, code):
    if not ok:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def stamp(value, active=None):
    active = set() if active is None else active
    kind = type(value)
    if value is None or kind in (str, bytes, int, bool):
        return kind, value
    if kind is float:
        return kind, value.hex()
    if id(value) in active:
        return kind, id(value), 'recursive'
    active.add(id(value))
    try:
        if kind is types.FunctionType:
            return (kind, id(value), id(value.__code__), stamp(value.__defaults__, active),
                stamp(value.__kwdefaults__, active), stamp(vars(value), active),
                tuple(stamp(c.cell_contents, active) for c in (value.__closure__ or ())))
        if kind is type and value.__module__.startswith('_disabled_outer.'):
            return kind, id(value), stamp(dict(vars(value)), active)
        if kind in (classmethod, staticmethod):
            return kind, stamp(value.__func__, active)
        if kind is dict:
            return kind, tuple((stamp(k,active),stamp(v,active)) for k,v in value.items())
        if kind in (tuple,list):
            return kind, tuple(stamp(v,active) for v in value)
        if kind in (set,frozenset):
            return kind, frozenset(stamp(v,active) for v in value)
        return kind, id(value)
    finally:
        active.remove(id(value))


class OuterSources:
    def __init__(self, *, buffers, hashes):
        need(type(buffers) is dict and type(hashes) is dict and
             set(buffers) == set(hashes) == set(ROSTER), 'operational_outer_roster')
        self.buffers = dict(buffers)
        self.hashes = dict(hashes)
        self.modules = {}
        self.frozen = {}
        self.started = self.closed = self.failed = False
        self.loaded = False
        self.package = types.SimpleNamespace()
        trees = {}
        total = 0
        for name in ROSTER:
            raw = buffers[name]
            need(type(raw) is bytes and 0 < len(raw) <= 2*1024**2 and sha(raw) == hashes[name],
                 'operational_outer_hash')
            total += len(raw)
            need(total <= 16*1024**2, 'operational_outer_bound')
            tree = ast.parse(raw, filename='<disabled-outer:'+name+'>')
            if name in DATA_ONLY:
                # Executed only through the separate five-helper parent owner.
                # This owner binds the bytes; it neither compiles nor imports it.
                continue
            edges = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    need(all(a.name.split('.')[0] in sys.stdlib_module_names and
                        a.name.split('.')[0] not in ('ctypes','_ctypes') for a in node.names),
                        'operational_outer_import')
                elif isinstance(node, ast.ImportFrom):
                    need(node.level == 0, 'operational_outer_import')
                    if node.module == 'tools':
                        edges.extend(a.name for a in node.names)
                    else:
                        need(node.module and node.module.split('.')[0] in sys.stdlib_module_names and
                             node.module.split('.')[0] not in ('ctypes','_ctypes'), 'operational_outer_import')
            need(tuple(edges) == EDGES[name], 'operational_outer_edges')
            trees[name] = tree
        self.compiled = {n:compile(trees[n], '<disabled-outer:'+n+'>', 'exec',
                                  dont_inherit=True, optimize=0) for n in ORDER}
        self.policy = (tuple(self.hashes.items()), tuple(self.compiled.items()))

    def intact(self):
        need(self.started and not self.closed and not self.failed, 'operational_outer_inactive')
        hashes, compiled = self.policy
        need(tuple(self.hashes.items()) == hashes and set(self.buffers) == set(ROSTER) and
             all(type(self.buffers[n]) is bytes and sha(self.buffers[n]) == h for n,h in hashes) and
             set(self.compiled) == set(ORDER) and all(self.compiled[n] is c for n,c in compiled),
             'operational_outer_policy')
        need(set(self.modules) == set(vars(self.package)) and
             all(getattr(self.package,n) is m for n,m in self.modules.items()), 'operational_outer_package')
        need(all(n in self.modules and stamp(vars(self.modules[n])) == s for n,s in self.frozen.items()),
             'operational_outer_live_code')
        if self.loaded:
            need(set(self.modules) == set(self.frozen) == set(ORDER), 'operational_outer_loaded_roster')

    def _import(self, name, globals=None, locals=None, fromlist=(), level=0):
        try:
            self.intact()
            need(level == 0, 'operational_outer_import')
            if name == 'tools':
                need(fromlist and all(n in self.modules for n in fromlist), 'operational_outer_import')
                return self.package
            need(name.split('.')[0] in sys.stdlib_module_names and
                 name.split('.')[0] not in ('ctypes','_ctypes'), 'operational_outer_import')
            return builtins.__import__(name, globals, locals, fromlist, level)
        except BaseException:
            self.failed = True
            raise

    def load(self):
        need(not self.started and not self.closed, 'operational_outer_reentry')
        self.started = True
        try:
            for name in ORDER:
                self.intact()
                module = types.ModuleType('_disabled_outer.'+name)
                module.__file__ = '<disabled-outer:'+name+'>'
                module.__builtins__ = dict(vars(builtins), __import__=self._import)
                self.modules[name] = module
                setattr(self.package, name, module)
                exec(self.compiled[name], vars(module))
                self.frozen[name] = stamp(vars(module))
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

    def receipts(self):
        self.intact()
        return {n:dict(bytes=len(self.buffers[n]),sha256=self.hashes[n]) for n in ROSTER}

    def close(self):
        need(not self.closed, 'operational_outer_reclose')
        try:
            if not self.failed:
                self.intact()
        finally:
            self.closed = True
            self.modules.clear()
            self.frozen.clear()
            vars(self.package).clear()
            self.buffers.clear()
            self.hashes.clear()
            self.compiled.clear()
            self.policy = None
        return True


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
