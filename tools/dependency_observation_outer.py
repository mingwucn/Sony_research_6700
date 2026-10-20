"""Disabled observation preflight and saved-parent comparison.

Only source-owned validators execute. There is no observer/process/activation
continuation. Initial loader, interpreter and stdlib are trusted; reviewed source
capture is not a hostile-code sandbox or authentication of outside decisions.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import ast
import builtins
import hashlib
import json
import sys
import types

GRAPH = (
    ('dependency_outer_contract', 'adapter_comparison', ()),
    ('dependency_operational_scope', 'adapter_scope', ('dependency_outer_contract',)),
    ('dependency_adapter_binding', 'adapter', ('dependency_operational_scope',)),
    ('dependency_evidence', 'dependency.dependency_evidence', ()),
    ('dependency_producer', 'dependency.dependency_producer', ('dependency_evidence',)),
    ('dependency_package_preflight', 'dependency.dependency_package_preflight',
        ('dependency_evidence', 'dependency_producer')),
    ('dependency_execution', 'dependency.dependency_execution',
        ('dependency_evidence', 'dependency_producer', 'dependency_package_preflight')),
    ('dependency_observation_contract', 'observation.contract',
        ('dependency_operational_scope', 'dependency_outer_contract', 'dependency_adapter_binding', 'dependency_execution')),
    ('retained_gate', 'retained_gate', ()),
)
ADDED = frozenset(('observation.contract', 'observation.outer'))
# Fixed host review policy, available before any captured source executes.
# The captured contract independently checks the same comparison roster later.
RETAINED = ('acceptance','link_acceptance','member_acceptance','metadata_preflight',
    'expanded_gate','ext_superblock','ext_preflight','ext_read_planner','ext_gate',
    'gdt_preflight','gdt_cleanup','gdt_gate','gdt_adapter','gdt_runner','prefix',
    'offline_inventory','artifact_probe','classifier','tar_inventory','metadata_tar',
    'member_prefix','header_candidates','io_adapter','validator','capture','core')
DEPENDENCIES = ('dependency_evidence','dependency_producer','dependency_package_preflight',
    'dependency_execution','dependency_controller','dependency_parent')
CAPTURE_ROLES = frozenset({'bound.role:'+n for n in RETAINED} |
    {'bound.bootstrap:activation_binding','bound.bootstrap:io_entry','bound.integration:prospective_child'} |
    {'dependency.'+n for n in DEPENDENCIES} |
    {'adapter','adapter_scope','adapter_comparison','namespace','successor_wiring',
     'host_entry','retained_gate','ordinary_io','operational_metadata','operational_entry',
     'operational_preparation','adapter_loader','outer_loader','process_child',
     'host.launcher','host.bootstrap_and_supervisor'}) | ADDED
STDLIB = frozenset(('hashlib', 'json', 'math', 'pathlib', 'copy', 'ntpath',
    'stat', 'unicodedata', 'importlib', 'os', 'sys', 'base64'))
FALSE = ('authority_verified', 'rights_established', 'execution_authorized',
    'fresh_observation_verified', 'runtime_qualified', 'actual_inputs_accessed',
    'feature_supported', 'recovery_proven', 'device_write_gate_passed')


def need(ok, code):
    if not ok:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


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
                stamp(value.__kwdefaults__, active), stamp(vars(value), active))
        if kind is type and value.__module__.startswith('_observation_preflight.'):
            return kind, id(value), stamp(dict(vars(value)), active)
        if kind in (staticmethod, classmethod):
            return kind, stamp(value.__func__, active)
        if kind is dict:
            return kind, tuple((stamp(k, active), stamp(v, active)) for k, v in value.items())
        if kind in (tuple, list):
            return kind, tuple(stamp(v, active) for v in value)
        if kind in (set, frozenset):
            return kind, frozenset(stamp(v, active) for v in value)
        return kind, id(value)
    finally:
        active.remove(id(value))


class Validators:
    """Own captured validator modules without publishing tools aliases."""
    def __init__(self, *, buffers, expected_hashes):
        need(type(buffers) is dict and type(expected_hashes) is dict and
             set(buffers) == set(expected_hashes) == CAPTURE_ROLES,
             'observation_outer_capture_roster')
        self.buffers = dict(buffers)
        self.hashes = dict(expected_hashes)
        total = 0
        for name, raw in buffers.items():
            need(type(raw) is bytes and 0 < len(raw) <= 4*1024**2 and
                 sha(raw) == expected_hashes[name], 'observation_outer_capture_hash')
            total += len(raw)
        need(total <= 20*1024**2, 'observation_outer_capture_bound')
        trees = {}
        for name, role, edges in GRAPH:
            need(role in buffers, 'observation_outer_graph_roster')
            tree = ast.parse(buffers[role], filename='<observation-validator:'+name+'>')
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    need(all(a.name.split('.')[0] in STDLIB for a in node.names),
                         'observation_outer_import')
                elif isinstance(node, ast.ImportFrom):
                    need(node.level == 0, 'observation_outer_import')
                    if node.module == 'tools':
                        imports.extend(a.name for a in node.names)
                    else:
                        need(node.module and node.module.split('.')[0] in STDLIB,
                             'observation_outer_import')
            need(tuple(imports) == edges, 'observation_outer_edges')
            trees[name] = tree
        # Verify all sources and import edges before executing any of them.
        self.compiled = {n:compile(t, '<observation-validator:'+n+'>', 'exec',
            dont_inherit=True, optimize=0) for n,t in trees.items()}
        self.policy = (tuple(self.hashes.items()), tuple(self.compiled.items()))
        self.modules = {}
        self.frozen = {}
        self.package = types.SimpleNamespace()
        self.started = self.loaded = self.closed = self.failed = False

    def intact(self):
        need(self.started and not self.closed and not self.failed, 'observation_outer_inactive')
        hashes, codes = self.policy
        need(tuple(self.hashes.items()) == hashes and set(self.buffers) == set(self.hashes) and
             all(type(self.buffers[n]) is bytes and sha(self.buffers[n]) == h for n,h in hashes) and
             set(self.compiled) == {n for n,_ in codes} and
             all(self.compiled[n] is c for n,c in codes), 'observation_outer_source_changed')
        need(set(self.modules) == set(vars(self.package)) and
             all(vars(self.package)[n] is m for n,m in self.modules.items()) and
             all(n in self.modules and stamp(vars(self.modules[n])) == s for n,s in self.frozen.items()),
             'observation_outer_live_changed')
        if self.loaded:
            need(set(self.modules) == {n for n,_,_ in GRAPH}, 'observation_outer_loaded_roster')

    def _import(self, name, globals=None, locals=None, fromlist=(), level=0):
        self.intact()
        need(level == 0, 'observation_outer_import')
        if name == 'tools':
            need(fromlist and all(n in self.modules for n in fromlist), 'observation_outer_import')
            return self.package
        need(name.split('.')[0] in STDLIB, 'observation_outer_import')
        return builtins.__import__(name, globals, locals, fromlist, level)

    def load(self):
        need(not self.started and not self.closed, 'observation_outer_reentry')
        self.started = True
        try:
            for name,_,_ in GRAPH:
                self.intact()
                module = types.ModuleType('_observation_preflight.'+name)
                module.__builtins__ = dict(vars(builtins), __import__=self._import)
                self.modules[name] = module
                setattr(self.package, name, module)
                exec(self.compiled[name], vars(module))
                self.frozen[name] = stamp(vars(module))
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

    def close(self):
        need(not self.closed, 'observation_outer_reclose')
        try:
            if self.started and not self.failed:
                self.intact()
        finally:
            self.closed = True
            self.modules.clear()
            self.frozen.clear()
            self.compiled.clear()
            self.buffers.clear()
            self.hashes.clear()
            vars(self.package).clear()
            self.policy = None
        return True


def _preflight(*, owner, proposal_arguments, review_bytes, decision_bytes,
        external_anchor_bytes, expected_external_anchor_sha256, runtime_expectation,
        legacy_documents, legacy_expected_seal_sha256, legacy_reference_pins,
        historical_migration=None):
    owner.intact()
    c = owner.modules['dependency_observation_contract']
    need(set(owner.buffers) == c.SOURCE_ROLES | ADDED, 'observation_outer_capture_roster')
    need({n:owner.buffers[n] for n in c.SOURCE_ROLES} == proposal_arguments['source_buffers'],
         'observation_outer_original_sources')
    result = c.validate_decided_scope(**proposal_arguments, review_bytes=review_bytes,
        decision_bytes=decision_bytes, external_anchor_bytes=external_anchor_bytes,
        expected_external_anchor_sha256=expected_external_anchor_sha256)
    proposal = c.decode(proposal_arguments['proposal_bytes'])
    c.equal(proposal['runtime'], runtime_expectation, 'observation_outer_runtime_expectation')
    need(type(legacy_documents) is dict and set(legacy_documents) ==
         {'candidate','review','decision','seal','inputs'}, 'observation_outer_legacy_roster')
    originals = {n:legacy_documents[n] for n in ('candidate','review','decision','seal')}
    need(type(legacy_documents['inputs']) is dict, 'observation_outer_legacy_inputs')
    originals.update({'input:'+n:b for n,b in legacy_documents['inputs'].items()})
    c.buffers(originals, set(originals))
    for role in c.RETAINED:
        need(legacy_documents['inputs'].get(role) == proposal_arguments['retained_comparison_buffers'][role],
             'observation_outer_original_comparison')
    gate = owner.modules['retained_gate']
    if historical_migration is None:
        validated = gate.validate_bundle(legacy_documents,
            expected_seal_sha256=legacy_expected_seal_sha256, reference_pins=legacy_reference_pins)
    else:
        need(type(historical_migration) is dict and set(historical_migration) ==
             {'context_bytes', 'expected_context_sha256', 'ancestry_proof_bytes',
              'expected_ancestry_proof_sha256'}, 'observation_outer_migration_shape')
        validated = gate.validate_bundle_v6(legacy_documents,
            expected_seal_sha256=legacy_expected_seal_sha256, reference_pins=legacy_reference_pins,
            expected_operation_id=result['operation_id'], **historical_migration)
        need(validated['schema'] == 'gdt_outer_consistency_v6' and
             validated['consistency_only'] is True and validated['execution_authorized'] is False and
             validated['historical_operation_id'] != result['operation_id'] and
             validated['current_operation_id'] == result['operation_id'],
             'observation_outer_migration_result')
    need(validated['candidate']['operation_id'] == result['operation_id'], 'observation_outer_operation')
    selected = {n for n in owner.buffers if n.startswith('bound.')}
    need(len(selected) == 29 and all(owner.buffers[n] ==
         validated['source_buffers'].get(n.removeprefix('bound.')) for n in selected),
         'observation_outer_retained_sources')
    manifest = validated['inputs']['source_manifest']
    identity = proposal['protected_identities']
    need(identity['firmware_package'] == dict(bytes=manifest['bytes'], sha256=manifest['sha256']) and
         identity['operational_constants']['sha256'] == validated['inputs']['prerequisites']['constants_sha256'],
         'observation_outer_protected_identity')
    owner.intact()
    output = dict(schema='disabled_observation_outer_preflight_v1',
        status='decided_scope_preflight_consistency_only', operation_id=result['operation_id'],
        contract=result, capture_receipts={n:c.receipt(b) for n,b in owner.buffers.items()},
        source_roster_delta=dict(retained_comparison_roles=51, added_validator_roles=sorted(ADDED),
            operational_execution_roster_derived=False),
        legacy_original_receipts={n:c.receipt(b) for n,b in originals.items()},
        legacy_seal_sha256=legacy_expected_seal_sha256,
        legacy_reference_pins_sha256=sha(encoded(legacy_reference_pins)),
        authority_record_receipts={n:c.receipt(b) for n,b in dict(review=review_bytes,
            decision=decision_bytes, external_anchor=external_anchor_bytes).items()},
        runtime_expectation_sha256=sha(encoded(runtime_expectation)),
        retained_comparison_semantics_revalidated=True, legacy_authority_promoted=False,
        source_owner_closed=True, execution_integration_performed=False,
        **dict.fromkeys(FALSE, False), camera_commands=[])
    if historical_migration is not None:
        output.update(schema='disabled_observation_outer_preflight_v2',
            historical_operation_id=validated['historical_operation_id'],
            historical_context_sha256=validated['historical_context_sha256'],
            ancestry_proof_sha256=validated['ancestry_proof_sha256'])
    return output


def preflight(*, capture_buffers, expected_capture_hashes, **arguments):
    """Validate original records with captured validators and close once.

    Expected source/runtime/anchor identities are caller-selected review inputs,
    not inferred from this proposal. No actual observation can start here.
    """
    owner = Validators(buffers=capture_buffers, expected_hashes=expected_capture_hashes)
    owner.load()
    primary = None
    result = None
    try:
        result = _preflight(owner=owner, **arguments)
    except BaseException as error:
        primary = error
    try:
        owner.close()
    except BaseException as cleanup:
        if primary is not None:
            raise primary from cleanup
        raise
    if primary is not None:
        raise primary
    return result


def verify_saved(*, raw, expected_sha256, **arguments):
    """Recompute parent comparison from original bytes; never trust saved flags."""
    need(type(raw) is bytes and 0 < len(raw) <= 4*1024**2 and
         sha(raw) == expected_sha256, 'observation_outer_saved_hash')
    expected = encoded(preflight(**arguments))
    need(raw == expected, 'observation_outer_saved_original')
    return True


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
