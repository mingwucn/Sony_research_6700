"""Separate checked-buffer helper graphs; no runtime activation or disk imports.

The child owns neutral sys.modules aliases; parent verification owns no aliases.
This is trusted authored-source composition, not a hostile-code sandbox.
"""
import ast
import builtins
import hashlib
import importlib.machinery
from pathlib import Path
import sys
import types


COMMON = ('dependency_evidence', 'dependency_producer',
          'dependency_package_preflight', 'dependency_execution')
CHILD_ORDER = COMMON + ('dependency_controller',)
PARENT_ORDER = COMMON + ('dependency_parent',)
NAMESPACE = '_a6700_successor'


def need(ok, code):
    if not ok:
        raise ValueError(code)


class HelperSources:
    def __init__(self, *, mode, buffers, origins, hashes):
        need(type(mode) is str and mode in ('child', 'parent'), 'helper_mode')
        self.mode = mode
        self.order = CHILD_ORDER if mode == 'child' else PARENT_ORDER
        need(all(type(x) is dict for x in (buffers, origins, hashes)) and
             set(buffers) == set(origins) == set(hashes) == set(self.order), 'helper_roster')
        self.compiled = {}; self.origins = dict(origins)
        self.modules = {}; self.owned = {}; self.frozen = {}
        self.started = False; self.closed = False; self.failed = False
        self.package = types.SimpleNamespace()
        total = 0
        # Compile the complete graph before any authored module executes.
        for name in self.order:
            raw = buffers[name]; origin = origins[name]
            need(type(raw) is bytes and 0 < len(raw) <= 2*1024**2, 'helper_bound')
            total += len(raw)
            need(total <= 8*1024**2, 'helper_bound')
            need(type(origin) is str and len(origin) <= 2048 and
                 Path(origin).is_absolute(), 'helper_origin')
            need(type(hashes[name]) is str and
                 hashlib.sha256(raw).hexdigest() == hashes[name], 'helper_hash')
            tree = ast.parse(raw, filename=origin)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    need(not any(a.name == 'tools' or a.name.startswith('tools.')
                                 for a in node.names), 'helper_import')
                if isinstance(node, ast.ImportFrom) and node.module and (
                        node.module == 'tools' or node.module.startswith('tools.')):
                    need(node.level == 0 and node.module == 'tools' and
                         all(a.name in self.order for a in node.names), 'helper_import')
            self.compiled[name] = compile(tree, origin, 'exec', dont_inherit=True, optimize=0)

    def intact(self):
        need(self.started and not self.closed and not self.failed, 'helper_inactive')
        need(all(sys.modules.get(alias) is module for alias, module in self.owned.items()),
             'helper_alias_ownership')
        need(all(getattr(self.package, name, None) is module for name, module in self.modules.items()),
             'helper_attribute_ownership')
        if self.mode == 'parent' and self.frozen:
            for name, module in self.modules.items():
                old = self.frozen[name]
                need(set(vars(module)) == set(old) and
                     all(vars(module)[k] is value for k, value in old.items()), 'helper_global_ownership')

    def import_authored(self, name, globals=None, locals=None, fromlist=(), level=0):
        try:
            self.intact()
            if name == 'tools' or name.startswith('tools.'):
                need(name == 'tools' and level == 0 and type(fromlist) in (tuple, list) and
                     bool(fromlist) and all(n in self.modules for n in fromlist), 'helper_import')
                return self.package
            return builtins.__import__(name, globals, locals, fromlist, level)
        except BaseException:
            self.failed = True
            raise

    def load(self):
        need(not self.started and not self.closed, 'helper_reentry')
        self.started = True
        try:
            if self.mode == 'child':
                need(not any(n == NAMESPACE or n.startswith(NAMESPACE+'.') or
                             n == 'tools' or n.startswith('tools.') for n in sys.modules), 'helper_preloaded')
                self.package = types.ModuleType(NAMESPACE)
                self.package.__path__ = []
                self.package.__spec__ = importlib.machinery.ModuleSpec(NAMESPACE, self, is_package=True)
                self.owned[NAMESPACE] = self.package
                sys.modules[NAMESPACE] = self.package
            for name in self.order:
                self.intact()
                alias = NAMESPACE+'.'+name
                module = types.ModuleType(alias)
                module.__file__ = self.origins[name]
                module.__package__ = NAMESPACE; module.__loader__ = self
                module.__spec__ = importlib.machinery.ModuleSpec(alias, self, origin=module.__file__)
                module.__builtins__ = dict(vars(builtins), __import__=self.import_authored)
                self.modules[name] = module
                setattr(self.package, name, module)
                if self.mode == 'child':
                    self.owned[alias] = module
                    sys.modules[alias] = module
                exec(self.compiled[name], vars(module))
                self.intact()
            if self.mode == 'parent':
                self.frozen = {n: dict(vars(m)) for n, m in self.modules.items()}
            return self.package
        except BaseException as primary:
            self.failed = True
            try:
                self.close()
            except BaseException as cleanup:
                raise primary from cleanup
            raise

    def verify(self, **kwargs):
        need(self.mode == 'parent', 'helper_mode')
        self.intact()
        try:
            answer = self.package.dependency_parent.validate_saved_controller(**kwargs)
        except BaseException as primary:
            try:
                self.intact()
            except BaseException as cleanup:
                raise primary from cleanup
            raise
        self.intact()
        return answer

    def close(self):
        need(not self.closed, 'helper_reclose')
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
        need(intact, 'helper_cleanup_ownership')
        return True


def main():
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
