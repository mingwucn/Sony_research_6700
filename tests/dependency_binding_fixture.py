"""Detached synthetic contract for the genuine retained binding validator.

The caller supplies the exact pinned ordinary validator, the 23 ordinary role
buffers already captured by FreshTerminal, and three newly authored protected
role doubles from invented_boundary. This helper opens or executes nothing.
Capture its result before introducing candidate faults; never recapture an
expected contract from the candidate under test.

The emitted validator preserves the complete original source as a byte prefix.
Only a labelled final CONTRACT assignment changes the three protected doubles'
import records. All validator functions and predicates remain original. This
qualifies an invented import graph, not the original protected implementation,
installed dependencies, firmware decoding, actual runtime or a device gate.
"""
import ast
import copy
import hashlib
import json


BINDING_SHA256 = '22558080636f15300590c22b9987216216f650b4edc58d7df89092643722de74'
PROTECTED = frozenset(('capture', 'core', 'validator'))
CONTRACT_KEYS = frozenset(('aliases', 'source_import_records', 'eager_edges',
    'lazy_imports', 'namespace_bindings', 'load_order', 'protected_order'))
DEPENDENCY_NULLS = ('record_sha256', 'expected_files', 'native_policy')


def _require(value):
    if not value:
        raise AssertionError('independent synthetic binding fixture contract')


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _capture_import_records(raw):
    """Independent AST traversal; no retained visitor or validator is invoked.

    Function bodies, including nested class bodies inside a function, retain
    function scope. Class bodies at module scope retain module scope, matching
    this finite original import grammar. DFS preserves the AST source order.
    """
    _require(type(raw) is bytes and 0 < len(raw) <= 8 * 1024**2)
    result = []

    def visit(node, in_function=False):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            in_function = True
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            from_import = isinstance(node, ast.ImportFrom)
            result.append(dict(kind='from' if from_import else 'import',
                module=node.module if from_import else None,
                level=node.level if from_import else 0,
                names=[[alias.name, alias.asname] for alias in node.names],
                scope='function' if in_function else 'module'))
        for child in ast.iter_child_nodes(node):
            visit(child, in_function)

    visit(ast.parse(raw))
    return result


def capture_binding_fixture(*, binding_raw, ordinary_sources, protected_sources):
    """Freeze expected bytes/imports before mutation; return detached evidence.

    Caller source provenance remains necessary: ordinary_sources must come from
    the pinned FreshTerminal capture and protected_sources from invented_boundary.
    No caller object is retained. The three doubles are additionally required to
    have their declared two-import grammar; original protected sources cannot
    satisfy that grammar. This helper never reads those original sources.
    """
    _require(type(binding_raw) is bytes and _sha(binding_raw) == BINDING_SHA256)
    assignments = [node for node in ast.parse(binding_raw).body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and
        isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'CONTRACT']
    _require(len(assignments) == 1)
    original = ast.literal_eval(assignments[0].value)
    _require(type(original) is dict and set(original) == CONTRACT_KEYS)
    roles = set(original['aliases'])
    _require(len(roles) == 26 and PROTECTED < roles and
             type(ordinary_sources) is dict and type(protected_sources) is dict and
             set(ordinary_sources) == roles - PROTECTED and
             len(ordinary_sources) == 23 and set(protected_sources) == PROTECTED)
    _require(set(original['source_import_records']) == roles and
             set(original['eager_edges']) == roles)
    all_sources = dict(ordinary_sources, **protected_sources)
    _require(sum(len(raw) for raw in all_sources.values() if type(raw) is bytes)
             <= 32 * 1024**2)
    captured = {role: _capture_import_records(raw)
                for role, raw in all_sources.items()}
    for role in ordinary_sources:
        _require(captured[role] == original['source_import_records'][role])
    declared_double_imports = [
        dict(kind='import', module=None, level=0, names=[['copy', None]], scope='module'),
        dict(kind='import', module=None, level=0, names=[['hashlib', None]], scope='module'),
    ]
    expected = copy.deepcopy(original)
    for role in PROTECTED:
        _require(captured[role] == declared_double_imports and
                 captured[role] != original['source_import_records'][role] and
                 original['eager_edges'][role] == [])
        expected['source_import_records'][role] = copy.deepcopy(captured[role])
    for key in CONTRACT_KEYS - {'source_import_records'}:
        _require(expected[key] == original[key])
    changed = sorted(role for role in roles if
        expected['source_import_records'][role] != original['source_import_records'][role])
    _require(changed == sorted(PROTECTED))
    expected_digest = _sha(_canonical(expected))
    original_digest = _sha(_canonical(original))
    pins = {role: dict(bytes=len(raw), sha256=_sha(raw))
            for role, raw in sorted(all_sources.items())}
    label = dict(schema='invented_binding_contract_v1',
        original_binding_sha256=BINDING_SHA256,
        original_contract_sha256=original_digest,
        expected_contract_sha256=expected_digest,
        replaced_import_record_roles=changed, ordinary_roles_changed=[],
        actual_protected_sources_read=False, installed_dependency_used=False,
        actual_runtime_verified=False, feature_supported=False,
        recovery_proven=False, device_write_gate_passed=False, camera_commands=[])
    suffix = ('\n# SYNTHETIC ONLY: independently captured invented-role contract.\n'
              '# Original validator bytes/functions/predicates above are unchanged.\n'
              'SYNTHETIC_BINDING_FIXTURE = ' + repr(label) + '\n'
              'CONTRACT = ' + repr(expected) + '\n').encode('ascii')
    source = binding_raw + suffix
    _require(source[:len(binding_raw)] == binding_raw)
    ast.parse(source)
    return dict(binding_source=source, contract=copy.deepcopy(expected),
        original_contract=copy.deepcopy(original),
        expected_contract_sha256=expected_digest,
        original_contract_sha256=original_digest,
        original_binding_sha256=BINDING_SHA256,
        binding_source_sha256=_sha(source), role_pins=copy.deepcopy(pins),
        captured_import_records=copy.deepcopy(captured), summary=copy.deepcopy(label))


def build_expected_plan(prerequisites, contract):
    """Explicit oracle from previously frozen contract and invented role rows.

    This does not call prepare_bindings or inspect any current candidate source.
    It intentionally supports only this package's three-null dependency state;
    the original validator remains responsible for accepting/refusing candidates.
    Supply prerequisites after the fixture has bound its final invented roles.
    """
    _require(type(prerequisites) is dict and type(contract) is dict and
             set(contract) == CONTRACT_KEYS)
    binding_input = prerequisites['binding_input']
    _require(type(binding_input) is dict and
             set(binding_input) == {'schema', 'roles', 'dependency'} and
             binding_input['schema'] == 'activation_binding_input_v1')
    roles = binding_input['roles']
    _require(type(roles) is dict and set(roles) == set(contract['aliases']) and
             roles == prerequisites['qualified_roles'])
    dependency = binding_input['dependency']
    _require(type(dependency) is dict and set(dependency) == {
        'schema', 'version', 'wheel_sha256', *DEPENDENCY_NULLS} and
        dependency['schema'] == 'activation_dependency_plan_v1' and
        dependency['version'] == '3.24.1' and
        all(dependency[key] is None for key in DEPENDENCY_NULLS))
    # List every output field independently of the function under test.
    return dict(schema='activation_binding_plan_v1',
        status='source_binding_plan_validated', roles=copy.deepcopy(roles),
        load_order=copy.deepcopy(contract['load_order']),
        protected_order=copy.deepcopy(contract['protected_order']),
        dependency=copy.deepcopy(dependency),
        namespace_bindings=copy.deepcopy(contract['namespace_bindings']),
        lazy_imports=copy.deepcopy(contract['lazy_imports']),
        blockers=['dependency_manifest_unobserved', 'native_policy_unobserved'],
        execution_authorized=False, actual_runtime_verified=False,
        actual_binding_ready=False, camera_commands=[])
