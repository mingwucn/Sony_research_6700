"""Pending proposal and historical comparison review; no activation path.

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
    ('dependency_observation_contract', 'review.contract',
        ('dependency_operational_scope', 'dependency_outer_contract', 'dependency_adapter_binding', 'dependency_execution')),
    ('retained_gate', 'retained_gate', ()),
    ('dependency_legacy_comparison', 'review.legacy', ()),
    ('ancestry_comparison_gate', 'review.ancestry', ()),
)
ADDED = frozenset(('review.contract', 'review.legacy', 'review.ancestry', 'review.entry'))
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
             'pending_review_capture_roster')
        self.buffers = dict(buffers)
        self.hashes = dict(expected_hashes)
        total = 0
        for name, raw in buffers.items():
            need(type(raw) is bytes and 0 < len(raw) <= 4*1024**2 and
                 sha(raw) == expected_hashes[name], 'pending_review_capture_hash')
            total += len(raw)
        need(total <= 20*1024**2, 'pending_review_capture_bound')
        trees = {}
        for name, role, edges in GRAPH:
            need(role in buffers, 'pending_review_graph_roster')
            tree = ast.parse(buffers[role], filename='<observation-validator:'+name+'>')
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    need(all(a.name.split('.')[0] in STDLIB for a in node.names),
                         'pending_review_import')
                elif isinstance(node, ast.ImportFrom):
                    need(node.level == 0, 'pending_review_import')
                    if node.module == 'tools':
                        imports.extend(a.name for a in node.names)
                    else:
                        need(node.module and node.module.split('.')[0] in STDLIB,
                             'pending_review_import')
            need(tuple(imports) == edges, 'pending_review_edges')
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
        need(self.started and not self.closed and not self.failed, 'pending_review_inactive')
        hashes, codes = self.policy
        need(tuple(self.hashes.items()) == hashes and set(self.buffers) == set(self.hashes) and
             all(type(self.buffers[n]) is bytes and sha(self.buffers[n]) == h for n,h in hashes) and
             set(self.compiled) == {n for n,_ in codes} and
             all(self.compiled[n] is c for n,c in codes), 'pending_review_source_changed')
        need(set(self.modules) == set(vars(self.package)) and
             all(vars(self.package)[n] is m for n,m in self.modules.items()) and
             all(n in self.modules and stamp(vars(self.modules[n])) == s for n,s in self.frozen.items()),
             'pending_review_live_changed')
        if self.loaded:
            need(set(self.modules) == {n for n,_,_ in GRAPH}, 'pending_review_loaded_roster')

    def _import(self, name, globals=None, locals=None, fromlist=(), level=0):
        self.intact()
        need(level == 0, 'pending_review_import')
        if name == 'tools':
            need(fromlist and all(n in self.modules for n in fromlist), 'pending_review_import')
            return self.package
        need(name.split('.')[0] in STDLIB, 'pending_review_import')
        return builtins.__import__(name, globals, locals, fromlist, level)

    def load(self):
        need(not self.started and not self.closed, 'pending_review_reentry')
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
        need(not self.closed, 'pending_review_reclose')
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


def _check(*, owner, proposal_arguments, historical_buffers, reference_map_bytes,
        expected_reference_map_sha256, expected_proposal_sha256,
        expected_request_sha256, ancestry_proof_bytes, expected_ancestry_proof_sha256,
        historical_context, runtime_expectation):
    owner.intact()
    c=owner.modules['dependency_observation_contract']
    comparison=owner.modules['dependency_legacy_comparison']
    gate=owner.modules['retained_gate'];ancestry=owner.modules['ancestry_comparison_gate']
    need(CAPTURE_ROLES==c.SOURCE_ROLES|ADDED,'pending_review_source_roster')
    need({n:owner.buffers[n] for n in c.SOURCE_ROLES}==proposal_arguments['source_buffers'],
         'pending_review_original_sources')
    result=c.validate_proposal(**proposal_arguments);owner.intact()
    need(len(result['pending_decisions'])==5 and not result['denied_decisions'],
         'pending_review_dispositions')
    proposal=c.decode(proposal_arguments['proposal_bytes'])
    c.equal(proposal['runtime'],runtime_expectation,'pending_review_runtime_expectation')
    compared=comparison.compare(historical_buffers=historical_buffers,
        reference_map_bytes=reference_map_bytes,expected_reference_map_sha256=expected_reference_map_sha256,
        proposal_bytes=proposal_arguments['proposal_bytes'],expected_proposal_sha256=expected_proposal_sha256,
        request_bytes=proposal_arguments['request_bytes'],expected_request_sha256=expected_request_sha256,
        ordinary_buffers=proposal_arguments['ordinary_buffers'],
        retained_source_buffers={n:b for n,b in proposal_arguments['source_buffers'].items() if n.startswith('bound.')})
    need(compared['operation_ids_differ'] is True,'pending_review_distinct_contexts');owner.intact()
    c.digest(expected_ancestry_proof_sha256);c.raw_bytes(ancestry_proof_bytes)
    need(sha(ancestry_proof_bytes)==expected_ancestry_proof_sha256 and
         encoded(ancestry.SOURCE_ANCESTRY)==ancestry_proof_bytes,'pending_review_ancestry_proof')
    c.shape(historical_context,('repository_root','legacy_session','operation_id'),'pending_review_context')
    need(historical_context['operation_id']==compared['historical_operation_id'],
         'pending_review_historical_operation')
    p={n:gate.parse(b) for n,b in historical_buffers.items() if n!='q_snapshot_log'}
    stages=[]
    gate.parent_evidence(p);stages.append('historical_parent_evidence');owner.intact()
    gate._qualifications(p,historical_buffers);stages.append('historical_qualifications');owner.intact()
    effective=ancestry.effective_sources(p,historical_context,
        repair_result_sha256=sha(historical_buffers['q_repair_result']),
        historical_seal_sha256=sha(historical_buffers['q_old_seal']))
    stages.append('historical_source_ancestry_repairs');owner.intact()
    integration=ancestry.integration_sources(p);stages.append('historical_factory_sources');owner.intact()
    cached=ancestry._source_cache(p,historical_context,effective,integration)
    need(len(cached)==47 and all(cached[n.removeprefix('bound.')]==b
         for n,b in proposal_arguments['source_buffers'].items() if n.startswith('bound.')),
         'pending_review_cached_originals')
    stages.append('historical_cached_receipts_qualification');owner.intact()
    need(set(p['basis'])==gate.BASIS_ROLES and
         p['basis']['prior_stream']['input_package_bytes']==p['source_manifest']['bytes'] and
         p['basis']['prior_stream']['input_package_sha256']==p['source_manifest']['sha256'] and
         p['prerequisites']['qualified_roles']==p['role_authority']['roles']==p['prerequisites']['binding_input']['roles'] and
         p['binding_plan']['dependency']==p['prerequisites']['binding_input']['dependency'] and
         p['binding_plan']['load_order']==p['binding_schema']['load_order'] and
         p['binding_plan']['protected_order']==p['binding_schema']['protected_order'],
         'pending_review_original_relationships')
    missing=[n for n in ('record_sha256','expected_files','native_policy') if p['binding_plan']['dependency'][n] is None]
    need(not p['historical_rights']['conclusions']['actual_execution_authorized_by_this_review'],
         'pending_review_historical_rights')
    stages.append('historical_basis_roles_orders_dependency_plan');owner.intact()
    return dict(schema='pending_observation_review_preflight_v1',status='pending_review_consistency_only',
        proposal=result,comparison=compared,historical_stages=stages,
        capture_receipts={n:c.receipt(b) for n,b in owner.buffers.items()},
        ancestry_proof_sha256=expected_ancestry_proof_sha256,
        runtime_expectation_sha256=sha(encoded(runtime_expectation)),
        historical_dependency_null_fields=missing,historical_contexts_separate=True,
        validator_owner_closed=True,operational_source_roster_changed=False,
        full_legacy_bundle_validated=False,decided_outer_preflight_performed=False,
        accepted_authority=False,launch_transport_assembled=False,
        **dict.fromkeys(FALSE,False),camera_commands=[])


def preflight(*, capture_buffers, expected_capture_hashes, **arguments):
    """Run the pending review and close source ownership exactly once.

    Caller-selected pins establish technical consistency, not authority. No
    historical cache text, observer, runtime continuation or launcher executes.
    """
    owner=Validators(buffers=capture_buffers,expected_hashes=expected_capture_hashes)
    owner.load()
    primary=None;result=None
    try:result=_check(owner=owner,**arguments)
    except BaseException as error:primary=error
    try:owner.close()
    except BaseException as cleanup:
        if primary is not None:raise primary from cleanup
        raise
    if primary is not None:raise primary
    return result


def verify_saved(*, raw, expected_sha256, **arguments):
    need(type(raw) is bytes and 0<len(raw)<=4*1024**2 and sha(raw)==expected_sha256,
         'pending_review_saved_hash')
    need(raw==encoded(preflight(**arguments)),'pending_review_saved_original')
    return True
