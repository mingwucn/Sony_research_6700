"""Invented metadata recomputation using pinned, trusted authored source buffers.

No disk imports of authored modules, sys.modules aliases, payload reads or runtime
activation. This executes reviewed host validators, not a hostile-code sandbox.
An empty invented namespace below is a planning input, never a startup observation.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import ast
import builtins
import sys
import types

from tools import dependency_authority_grammar as envelope
from tools import dependency_basis_links as links

SCOPE_SHA256 = '928027b9f240aa114c9ae03fd5e0d852435c8911299c5ce9c671f8632d60c44d'
PREFLIGHT_ORDER = ('acceptance', 'link_acceptance', 'member_acceptance',
    'metadata_preflight', 'expanded_gate', 'ext_superblock', 'ext_preflight',
    'ext_read_planner', 'ext_gate', 'gdt_preflight')


def _stamp(value, active=None):
    """Detect replacement, mutable constants and authored function-code changes."""
    active = set() if active is None else active
    kind = type(value)
    if value is None or kind in (str, int, bool, bytes):
        return kind, value
    if kind is float:
        return kind, value.hex()
    if kind is types.FunctionType:
        # functools wrappers keep the function they call in a closure and in
        # __wrapped__; changing that function must not evade the global check.
        if id(value) in active:
            return kind, id(value), 'recursive_function'
        active.add(id(value))
        try:
            return (kind, id(value), id(value.__code__), _stamp(value.__defaults__, active),
                _stamp(value.__kwdefaults__, active), _stamp(vars(value), active),
                tuple(_stamp(cell.cell_contents, active) for cell in (value.__closure__ or ())))
        finally:
            active.remove(id(value))
    if kind in (classmethod, staticmethod):
        return kind, id(value), _stamp(value.__func__, active)
    if kind is type and value.__module__.startswith('_a6700_owned_'):
        if id(value) in active:
            return kind, id(value), 'recursive_class'
        active.add(id(value))
        try:
            return kind, id(value), tuple((k, _stamp(v, active)) for k,v in vars(value).items())
        finally:
            active.remove(id(value))
    if kind in (dict, list, tuple, set, frozenset):
        envelope.need(id(value) not in active, 'recomputer_global_cycle')
        active.add(id(value))
        try:
            if kind is dict:
                content = tuple((_stamp(k, active), _stamp(v, active)) for k, v in value.items())
            elif kind in (set, frozenset):
                content = frozenset(_stamp(v, active) for v in value)
            else:
                content = tuple(_stamp(v, active) for v in value)
            return kind, id(value), content
        finally:
            active.remove(id(value))
    # Imported modules/classes and builtin objects retain identity. This is not
    # authentication against a hostile thread mutating the Python interpreter.
    return kind, id(value)


class _OwnedPreflight:
    """Detached exact-source graph; never installs or deletes process aliases."""
    def __init__(self, buffers):
        self.modules = {}; self.frozen = {}; self.closed = False; self.failed = False
        self.order = ('binding',) + PREFLIGHT_ORDER
        envelope.shape(buffers, self.order, 'recomputer_roster')
        # Entire graph compiles before the first execution. Buffers were pinned
        # by the caller against the frozen review packet before construction.
        self.compiled = {n: compile(ast.parse(buffers[n], filename='<owned:'+n+'>'),
            '<owned:'+n+'>', 'exec', dont_inherit=True, optimize=0) for n in self.order}

    def intact(self):
        envelope.need(not self.closed and not self.failed, 'recomputer_inactive')
        if self.frozen:
            envelope.need(set(self.modules) == set(self.order), 'recomputer_module_roster')
            for name, module in self.modules.items():
                envelope.need(_stamp(vars(module)) == self.frozen[name], 'recomputer_globals_changed')

    def _import(self, name, globals=None, locals=None, fromlist=(), level=0):
        try:
            self.intact()
            envelope.need(level == 0, 'recomputer_relative_import')
            if name in PREFLIGHT_ORDER:
                envelope.need(name in self.modules, 'recomputer_import_order')
                return self.modules[name]
            envelope.need(name.split('.')[0] in sys.stdlib_module_names and
                name.split('.')[0] not in ('ctypes', '_ctypes'), 'recomputer_import_refused')
            return builtins.__import__(name, globals, locals, fromlist, level)
        except BaseException:
            self.failed = True
            raise

    def load(self):
        envelope.need(not self.modules and not self.closed and not self.failed, 'recomputer_reentry')
        try:
            for name in self.order:
                module = types.ModuleType('_a6700_owned_' + name)
                module.__file__ = '<owned:'+name+'>'
                module.__builtins__ = dict(vars(builtins), __import__=self._import)
                self.modules[name] = module
                exec(self.compiled[name], vars(module))
            self.frozen = {n: _stamp(vars(m)) for n, m in self.modules.items()}
            self.intact()
            return self
        except BaseException as primary:
            self.failed = True
            try:
                self.close()
            except BaseException as cleanup:
                raise primary from cleanup
            raise

    def call(self, role, name, **kwargs):
        self.intact()
        try:
            answer = getattr(self.modules[role], name)(**kwargs)
        except BaseException as primary:
            try:
                self.intact()
            except BaseException as cleanup:
                self.failed = True
                raise primary from cleanup
            raise
        self.intact()
        return answer

    def close(self):
        envelope.need(not self.closed, 'recomputer_reclose')
        try:
            if not self.failed:
                self.intact()
        finally:
            self.closed = True
            self.modules.clear(); self.compiled.clear(); self.frozen.clear()
        return True


def validate_invented_basis_roles(documents, *, external_seal_sha256, scope_bytes,
        source_buffers, ordinary_buffers, historical_buffers):
    """Validate the envelope, then recompute plan and nine-role metadata preflight.

    Frozen source identity establishes which authored validators ran here. It
    does not authenticate caller approval, metadata truth/freshness, interpreter
    startup or compatibility with the successor dependency packet/fixed roles.
    """
    envelope.validate_invented_chain(documents, external_seal_sha256=external_seal_sha256,
        scope_bytes=scope_bytes, source_buffers=source_buffers,
        ordinary_buffers=ordinary_buffers, historical_buffers=historical_buffers)
    envelope.need(envelope.sha(scope_bytes) == SCOPE_SHA256, 'recomputer_frozen_scope')
    scope = envelope.decode(scope_bytes)
    # Pin all 26 role texts, including three protected texts that are only
    # hashed and AST-parsed by prepare_bindings. No protected code is compiled.
    selected = ['bound.bootstrap:activation_binding'] + ['bound.role:'+n for n in links.ROLES]
    for key in selected:
        row = scope['source_inventory'][key]; raw = source_buffers[key]
        envelope.need(len(raw) == row['bytes'] and envelope.sha(raw) == row['sha256'], 'recomputer_source_pin')
    prerequisites = envelope.decode(ordinary_buffers['prerequisites'])
    envelope.shape(prerequisites, ('qualified_roles','binding_input','constants_relative_path',
        'constants_sha256','constants_assignment_count','selected_literal_lengths','crypto_python_relative_path'),
        'prerequisite_shape')
    envelope.shape(prerequisites['qualified_roles'], links.ROLES, 'role_roster')
    for row in prerequisites['qualified_roles'].values():
        envelope.shape(row, ('path','sha256'), 'role_shape')
        links.private_path(row['path']); envelope.digest(row['sha256'])
    candidate = envelope.decode(documents['candidate'])
    buffers = {'binding': source_buffers['bound.bootstrap:activation_binding']}
    buffers.update({n: source_buffers['bound.role:'+n] for n in PREFLIGHT_ORDER})
    owned = _OwnedPreflight(buffers).load()
    try:
        binding = owned.modules['binding']
        retained = {k: binding.CONTRACT[k] for k in ('aliases','load_order','protected_order')}
        roles = prerequisites['qualified_roles']
        plan = owned.call('binding', 'prepare_bindings',
            binding_input=prerequisites['binding_input'], qualified_roles=roles,
            qualified_sources={row['path']: row['sha256'] for row in roles.values()},
            authored_sources={n:source_buffers['bound.role:'+n] for n in links.ROLES},
            preexisting_aliases=())
        basis = envelope.decode(ordinary_buffers['basis'])
        frozen = owned.call('gdt_preflight', 'freeze_basis', **basis)
        result = links.validate_invented_basis_links(candidate=candidate,
            ordinary_buffers=ordinary_buffers, source_buffers=source_buffers,
            recomputed_plan=plan, frozen_basis=frozen, retained_schema=retained)
        result.update(schema='invented_basis_role_recomputation_v1',
            recomputation_authenticated=False, pinned_authored_validators_executed=True,
            executed_validator_roles=list(owned.order), role_sources_ast_checked=26,
            protected_role_code_executed=False, ordinary_roles_checked=sorted(links.INPUTS),
            pending_ordinary_roles=sorted(envelope.policy.ORDINARY_INPUTS-links.INPUTS),
            dependency_roles_not_revalidated_here=['dependency_fixed','dependency_packet'],
            dependency_bridge_verified=False, metadata_freshness_verified=False,
            actual_startup_verified=False)
    except BaseException as primary:
        try:
            owned.close()
        except BaseException as cleanup:
            raise primary from cleanup
        raise
    owned.close()
    return result


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
