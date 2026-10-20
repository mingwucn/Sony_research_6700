"""Pure pending-operation records; consistency is not authority or freshness.

Original gate documents remain comparison evidence. These separate records do
not promote invented checks, historical consent or source receipts into a new
approved act. No source, dependency, protected input or process is opened here.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import hashlib
import json
from pathlib import Path

RETAINED = frozenset(('basis', 'source_manifest', 'prerequisites', 'binding_plan',
                     'role_authority', 'binding_schema'))
FLAGS = ('source_reads_observed', 'source_freshness_verified', 'rights_established',
         'actual_inputs_accessed', 'execution_authorized', 'feature_supported',
         'recovery_proven', 'device_write_gate_passed')


def need(ok, code):
    if not ok:
        raise ValueError(code)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def strict(raw):
    need(type(raw) is bytes and 0 < len(raw) <= 2*1024**2, 'operational_metadata_bound')
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, 'operational_metadata_duplicate')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda _: need(False, 'operational_metadata_nonfinite'))


def same(left, right, code):
    need(encoded(left) == encoded(right), code)


def receipts(buffers):
    need(type(buffers) is dict, 'operational_metadata_buffers')
    total = 0
    result = {}
    for name, raw in buffers.items():
        need(type(name) is str and type(raw) is bytes and 0 < len(raw) <= 2*1024**2,
             'operational_metadata_bound')
        total += len(raw)
        need(total <= 32*1024**2, 'operational_metadata_total')
        result[name] = dict(bytes=len(raw), sha256=sha(raw))
    return result


def record(raw, schema, fields, operation):
    value = strict(raw)
    need(type(value) is dict and set(value) == set(fields) |
         {'schema', 'operation_id', 'camera_commands'}, 'operational_record_shape')
    need(value['schema'] == schema and value['operation_id'] == operation and
         value['camera_commands'] == [], 'operational_record_mode')
    return value


def migration_receipts(migration):
    """Closed captured-byte handoff; pins establish consistency only."""
    need(type(migration) is dict and set(migration) == {'context_bytes',
         'expected_context_sha256', 'ancestry_proof_bytes',
         'expected_ancestry_proof_sha256'}, 'operational_migration_shape')
    selected = {}
    for name, limit in (('context', 16384), ('ancestry_proof', 65536)):
        raw = migration[name+'_bytes']
        pin = migration['expected_'+name+'_sha256']
        need(type(raw) is bytes and 0 < len(raw) <= limit and type(pin) is str and
             len(pin) == 64 and all(c in '0123456789abcdef' for c in pin) and
             sha(raw) == pin, 'operational_migration_anchor')
        selected[name] = dict(bytes=len(raw), sha256=pin)
    return selected


def validate_pending(*, documents, original_receipts, validated, request_bytes,
                     request_sha256, checked_sources, adapter_owner, ordinary,
                     ordinary_receipts, outer_source_receipts, prepared_repository_root,
                     historical_migration=None):
    """Check fourteen pending records after the separately owned legacy gate.

    Gate qualification and retained preflight remain separate responsibilities.
    These schemas bind original bytes and pending decisions, never approvals.
    Source receipt rows below are byte claims, not filesystem-read observations.
    """
    need(type(documents) is dict and set(documents) ==
         {'candidate', 'review', 'decision', 'seal', 'inputs'}, 'operational_original_roster')
    originals = {n: documents[n] for n in ('candidate', 'review', 'decision', 'seal')}
    need(type(documents['inputs']) is dict, 'operational_original_inputs')
    originals.update({'input:'+n: raw for n, raw in documents['inputs'].items()})
    same(receipts(originals), original_receipts, 'operational_original_bytes')
    need(sha(request_bytes) == request_sha256, 'operational_original_request')
    request = strict(request_bytes)
    adapter_owner.intact()
    adapter = adapter_owner.modules['dependency_adapter_binding']
    adapter.validate_request(request, expected_request_sha256=sha(encoded(request)),
                             checked_sources=checked_sources)
    for name, role in (('dependency_adapter_binding','outer_child'),
                       ('dependency_operational_scope','adapter.scope_policy'),
                       ('dependency_outer_contract','adapter.comparison_contract')):
        need(adapter_owner.buffers[name] == checked_sources[role], 'operational_loaded_adapter')
    operation = request['operation_id']
    candidate = strict(documents['candidate'])
    same(candidate, validated['candidate'], 'operational_original_candidate')
    same({n:sha(documents[n]) for n in ('candidate','review','decision','seal')},
         validated['document_sha256'], 'operational_original_gate')
    need(validated['seal_sha256'] == sha(documents['seal']) and
         candidate['operation_id'] == operation, 'operational_original_operation')
    root = Path(prepared_repository_root)
    comparison_root = Path(candidate['repository_root'])
    need(root.is_absolute() and comparison_root.is_absolute() and
         '..' not in root.parts and '..' not in comparison_root.parts and
         comparison_root.is_relative_to(root), 'operational_source_frames')
    need(set(documents['inputs']) == set(candidate['inputs']) and
         set(validated['inputs']) == set(documents['inputs']) - {'q_snapshot_log'},
         'operational_original_input_roster')
    for name, raw in documents['inputs'].items():
        row = candidate['inputs'][name]
        need(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'operational_original_input')
        if name != 'q_snapshot_log':
            same(strict(raw), validated['inputs'][name], 'operational_original_parsed')
    policy = adapter.policy
    need(type(ordinary) is dict and set(ordinary) == policy.ORDINARY_INPUTS,
         'operational_ordinary_roster')
    same(receipts(ordinary), ordinary_receipts, 'operational_ordinary_originals')
    for name in RETAINED:
        need(ordinary[name] == documents['inputs'][name], 'operational_retained_original')
    manifest = record(ordinary['authored_source_manifest'], 'pending_operational_sources_v1',
        ('prepared_sources', 'outer_sources', 'derived'), operation)
    same(manifest['prepared_sources'], request['sources'], 'operational_prepared_map')
    same(manifest['outer_sources'], outer_source_receipts, 'operational_outer_map')
    closure = encoded(request['sources'])
    same(manifest['derived'], dict(closure_manifest=dict(kind='canonical_prepared_source_map_v1',
        bytes=len(closure), sha256=sha(closure))), 'operational_derived_closure')
    claims = record(ordinary['authored_source_receipts'], 'pending_operational_source_byte_claims_v1',
        ('manifest_sha256', 'prepared', 'outer', 'source_reads_observed'), operation)
    need(claims['manifest_sha256'] == sha(ordinary['authored_source_manifest']) and
         claims['source_reads_observed'] is False, 'operational_source_claim_mode')
    same(claims['prepared'], receipts(checked_sources), 'operational_prepared_bytes')
    same(claims['outer'], outer_source_receipts, 'operational_outer_bytes')
    same(strict(ordinary['dependency_packet']), request['dependency_packet'], 'operational_dependency_packet')
    same(strict(ordinary['dependency_fixed']), request['dependency_fixed'], 'operational_dependency_fixed')
    scope = record(ordinary['activity_scope'], 'pending_operational_scope_v1',
        ('purpose', 'request_bytes_sha256', 'limits', 'originals', 'sources_sha256', 'historical_blockers'), operation)
    same({k:scope[k] for k in scope if k not in ('schema','operation_id','camera_commands')},
        dict(purpose='prepare_only_no_operational_act', request_bytes_sha256=request_sha256,
             limits=policy.SCOPE, originals=original_receipts,
             sources_sha256=sha(ordinary['authored_source_manifest']),
             historical_blockers=list(policy.HISTORY)), 'operational_scope')
    rights = record(ordinary['activity_rights'], 'pending_operational_rights_v1',
        ('scope_sha256', 'owner_facts', 'decisions', 'legal_basis_established', 'execution_authorized'), operation)
    same({k:rights[k] for k in rights if k not in ('schema','operation_id','camera_commands')},
        dict(scope_sha256=sha(ordinary['activity_scope']), owner_facts=policy.OWNER,
             decisions=dict.fromkeys(policy.RIGHTS, 'pending'), legal_basis_established=False,
             execution_authorized=False), 'operational_rights_pending')
    history = record(ordinary['historical_evidence_index'], 'pending_operational_history_v1',
        ('purpose', 'original_inputs'), operation)
    need(history['purpose'] == 'comparison_only', 'operational_history_purpose')
    same(history['original_inputs'], receipts(documents['inputs']), 'operational_history_originals')
    index = record(ordinary['qualification_index'], 'pending_operational_consistency_index_v1',
        ('ordinary', 'checked_roles', 'execution_authenticated', 'freshness_verified'), operation)
    same(index['ordinary'], receipts({n:b for n,b in ordinary.items() if n != 'qualification_index'}),
         'operational_index_originals')
    need(index['execution_authenticated'] is False and index['freshness_verified'] is False,
         'operational_index_authority')
    same(index['checked_roles'], sorted(policy.ORDINARY_INPUTS), 'operational_index_roles')
    adapter_owner.intact()
    result = dict(schema='pending_operational_preflight_v1', operation_id=operation,
        request_bytes_sha256=request_sha256, original_receipts=original_receipts,
        ordinary_receipts=ordinary_receipts, outer_source_receipts=outer_source_receipts,
        prepared_source_map_sha256=sha(encoded(request['sources'])),
        source_frames=dict(comparison_root=comparison_root.as_posix(), prepared_root=root.as_posix()),
        checked_roles=sorted(policy.ORDINARY_INPUTS), derived_closure_is_file=False,
        **dict.fromkeys(FLAGS, False), camera_commands=[])
    need(historical_migration is not None or validated.get('schema') != 'gdt_outer_consistency_v6',
         'operational_migration_required')
    if historical_migration is not None:
        selected = migration_receipts(historical_migration)
        context = strict(historical_migration['context_bytes'])
        same(context, dict(schema='gdt_historical_context_v1',
             repository_root=candidate['repository_root'],legacy_session=candidate['legacy_session'],
             operation_id=validated['inputs']['dependency_config']['operation_id'],
             dependency_config_sha256=sha(documents['inputs']['dependency_config']),
             historical_seal_sha256=sha(documents['inputs']['q_old_seal']),
             ancestry_proof_sha256=selected['ancestry_proof']['sha256'],
             execution_authorized=False,camera_commands=[]), 'operational_migration_context')
        need(validated['schema'] == 'gdt_outer_consistency_v6' and
             validated['consistency_only'] is True and
             all(validated[n] is False for n in ('execution_authorized','actual_entry_ready',
                 'feature_supported','recovery_proven','device_write_gate_passed','actual_inputs_accessed')) and
             'child_argv' not in validated and validated['current_operation_id'] == operation and
             validated['historical_operation_id'] == context['operation_id'] != operation and
             validated['historical_context_sha256'] == selected['context']['sha256'] and
             validated['ancestry_proof_sha256'] == selected['ancestry_proof']['sha256'],
             'operational_migration_result')
        result.update(schema='pending_operational_preflight_v2',
            historical_operation_id=context['operation_id'], historical_migration=selected,
            execution_bootstrap_qualified=False)
    return result


def verify_saved(*, raw, expected_sha256, **arguments):
    need(sha(raw) == expected_sha256, 'operational_saved_hash')
    expected = validate_pending(**arguments)
    same(strict(raw), expected, 'operational_saved_preflight')
    return True


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
