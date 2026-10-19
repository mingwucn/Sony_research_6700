"""Exact-buffer dependency graph with neutral module ownership.

The copied per-module import hook changes authored import semantics explicitly.
This is invented-child infrastructure, not a sandbox or execution permission.
It never removes a preexisting tools alias to make a source plan pass.
"""
import ast
import builtins
import hashlib
import importlib.machinery
from pathlib import Path
import sys
import types


NAMESPACE = '_a6700_collected'
ORDER = ('dependency_evidence', 'dependency_producer',
         'dependency_package_preflight', 'dependency_execution',
         'dependency_invented', 'dependency_controller')


def need(ok, code):
    if not ok:
        raise ValueError(code)


class ClosedSources:
    def __init__(self, *, buffers, origins, hashes):
        need(type(buffers) is dict and type(origins) is dict and type(hashes) is dict and
             set(buffers) == set(origins) == set(hashes) == set(ORDER), 'source_roster')
        self.buffers = dict(buffers); self.origins = dict(origins); self.hashes = dict(hashes)
        self.compiled = {}; self.owned = {}; self.modules = {}
        self.started = False; self.closed = False; self.failed = False
        total = 0
        # Validate and compile the entire roster before executing any member.
        for name in ORDER:
            raw = self.buffers[name]; origin = self.origins[name]
            need(type(raw) is bytes and 0 < len(raw) <= 2*1024**2, 'source_bound')
            total += len(raw); need(total <= 8*1024**2, 'source_bound')
            need(type(origin) is str and Path(origin).is_absolute() and len(origin) <= 2048,
                 'source_origin')
            need(type(self.hashes[name]) is str and
                 hashlib.sha256(raw).hexdigest() == self.hashes[name], 'source_hash')
            tree = ast.parse(raw, filename=origin)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    need(not any(a.name == 'tools' or a.name.startswith('tools.')
                                 for a in node.names), 'authored_import')
                if isinstance(node, ast.ImportFrom) and node.module and (
                        node.module == 'tools' or node.module.startswith('tools.')):
                    need(node.level == 0 and node.module == 'tools' and
                         all(a.name in ORDER for a in node.names), 'authored_import')
            self.compiled[name] = compile(tree, origin, 'exec', dont_inherit=True, optimize=0)

    def intact(self):
        need(not self.closed and not self.failed, 'namespace_inactive')
        need(all(sys.modules.get(alias) is module for alias, module in self.owned.items()),
             'namespace_ownership')
        if hasattr(self, 'package'):
            need(all(vars(self.package).get(name) is module
                     for name, module in self.modules.items()), 'namespace_attribute')

    def import_authored(self, name, globals=None, locals=None, fromlist=(), level=0):
        if name == 'tools' or name.startswith('tools.'):
            try:
                self.intact()
                need(name == 'tools' and level == 0 and type(fromlist) in (tuple, list)
                     and bool(fromlist) and all(item in self.modules for item in fromlist),
                     'authored_import')
                return self.package
            except BaseException:
                self.failed = True
                raise
        return builtins.__import__(name, globals, locals, fromlist, level)

    def load(self):
        need(not self.started and not self.closed, 'namespace_reentry')
        self.started = True
        need(not any(n == NAMESPACE or n.startswith(NAMESPACE+'.') or
                     n == 'tools' or n.startswith('tools.') for n in sys.modules),
             'namespace_preloaded')
        try:
            self.package = types.ModuleType(NAMESPACE)
            self.package.__path__ = []
            self.package.__spec__ = importlib.machinery.ModuleSpec(NAMESPACE, self, is_package=True)
            self.owned[NAMESPACE] = self.package; sys.modules[NAMESPACE] = self.package
            for name in ORDER:
                self.intact()
                alias = NAMESPACE+'.'+name
                module = types.ModuleType(alias); module.__file__ = self.origins[name]
                module.__package__ = NAMESPACE; module.__loader__ = self
                module.__spec__ = importlib.machinery.ModuleSpec(alias, self, origin=module.__file__)
                module.__builtins__ = dict(vars(builtins), __import__=self.import_authored)
                self.modules[name] = module; self.owned[alias] = module
                sys.modules[alias] = module; setattr(self.package, name, module)
                exec(self.compiled[name], module.__dict__)
                self.intact()
            return self.package
        except BaseException as primary:
            self.failed = True
            try:
                self.close()
            except BaseException as cleanup:
                raise primary from cleanup
            raise

    def close(self):
        need(not self.closed, 'namespace_reclose')
        self.closed = True
        intact = True; primary = None
        for alias, module in reversed(tuple(self.owned.items())):
            try:
                if sys.modules.get(alias) is module:
                    del sys.modules[alias]
                else:
                    intact = False
            except BaseException as error:
                if primary is None:
                    primary = error
        if primary is not None:
            raise primary
        need(intact, 'namespace_cleanup_ownership')
        return True


def main():
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
