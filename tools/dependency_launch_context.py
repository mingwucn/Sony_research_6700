"""Compose existing invented metadata checks with a prepared launch request.

No files, observer, process or runtime are opened here. Reviewed caller and
checked-buffer owners are trusted. Original comparison records remain intact.
"""
import hashlib
import json

if __name__ == '__main__':
    raise SystemExit(2)

VALIDATORS = dict(envelope='dependency_authority_grammar',
    source_receipts='dependency_source_receipts', basis='dependency_basis_recompute',
    dependency='dependency_input_semantics', activity='dependency_activity_metadata')


def need(ok, code):
    if not ok:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def strict(raw):
    need(type(raw) is bytes and 0 < len(raw) <= 2 * 1024**2, 'launch_request_bound')
    def pairs(rows):
        out = {}
        for key, value in rows:
            need(key not in out, 'launch_duplicate_key')
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda _: need(False, 'launch_nonfinite'))


def same(left, right, code):
    need(encoded(left) == encoded(right), code)


def checked_metadata_sources(owner):
    owner.intact()
    need(type(owner.buffers) is dict and type(owner.hashes) is dict and
         len(owner.buffers) == 14 and set(owner.buffers) == set(owner.hashes) == set(owner.modules),
         'launch_metadata_source_roster')
    need(all(type(raw) is bytes and 0 < len(raw) <= 2*1024**2 and
             sha(raw) == owner.hashes[name] for name, raw in owner.buffers.items()),
         'launch_metadata_loaded_source')
    return dict(owner.hashes)


def validate_invented_launch(*, request_bytes, expected_request_bytes_sha256,
        checked_sources, context_arguments, metadata_owner, adapter_owner):
    """Validate the same operation and explicit old-to-new source projection.

    Owner creation/cleanup remains the caller's responsibility, including failed
    calls. A matching digest is not approval, freshness or source provenance.
    """
    need(type(expected_request_bytes_sha256) is str and
         sha(request_bytes) == expected_request_bytes_sha256, 'launch_original_request')
    request = strict(request_bytes)
    metadata_hashes = checked_metadata_sources(metadata_owner)
    adapter_owner.intact()
    adapter = adapter_owner.modules['dependency_adapter_binding']
    # Use owned adapter call dispatch, never an ambient tools module.
    adapter_owner.call('validate_request', request=request,
        expected_request_sha256=sha(encoded(request)), checked_sources=checked_sources)
    need(type(context_arguments) is dict, 'launch_arguments')
    operation = request['operation_id']
    need(context_arguments['expected_operation_id'] == operation, 'launch_operation')
    scope = strict(context_arguments['scope_bytes'])
    same(scope['scope'], request['scope'], 'launch_scope')
    old_sources = context_arguments['source_buffers']
    comparison = adapter.policy.SOURCE_ROLES | {'host_parent_adapter'}
    need(type(old_sources) is dict and set(old_sources) == comparison, 'launch_comparison_roster')
    replaced = set(adapter.ENTRIES)
    retained = comparison - replaced
    for role in retained:
        need(old_sources[role] == checked_sources[role], 'launch_retained_source')
    # These are labels for old supplied source/receipt records, not fresh opens.
    source_manifest = strict(context_arguments['ordinary_buffers']['authored_source_manifest'])
    for role in retained:
        need(request['sources'][role]['path'] == source_manifest['sources'][role]['path'],
             'launch_retained_origin')
    for role, name in VALIDATORS.items():
        need(context_arguments['validator_buffers'][role] == metadata_owner.buffers[name],
             'launch_validator_source')
    # Bind the shared executable dependency helpers to the actual metadata owner.
    for name in ('dependency_execution', 'dependency_producer', 'dependency_package_preflight', 'dependency_evidence'):
        need(checked_sources['dependency.' + name] == metadata_owner.buffers[name],
             'launch_execution_source')
    for name, role in (('dependency_operational_scope', 'adapter.scope_policy'),
                       ('dependency_outer_contract', 'adapter.comparison_contract')):
        need(metadata_owner.buffers[name] == checked_sources[role], 'launch_shared_policy_source')
    ordinary = context_arguments['ordinary_buffers']
    old_packet = strict(ordinary['dependency_packet'])
    old_fixed = strict(ordinary['dependency_fixed'])
    anchor = strict(context_arguments['dependency_anchor_bytes'])
    current = request['dependency_packet']['inputs']
    previous = old_packet['inputs']
    need(anchor['operation_id'] == operation == current['expectation']['operation_id'], 'launch_operation')
    need(request['dependency_review_sha256'] == anchor['prior_review_sha256'], 'launch_dependency_review')
    for key in ('package', 'config_json', 'cache_json'):
        same(previous[key], current[key], 'launch_dependency_' + key)
    # The source roster is intentionally replaced; all other expectation fields
    # (including roots, native/library policy and original config/cache hashes)
    # must agree. The retained binders validate both sets of source digests.
    same({k:v for k,v in previous['expectation'].items() if k != 'source_sha256'},
         {k:v for k,v in current['expectation'].items() if k != 'source_sha256'}, 'launch_expectation')
    same({k:v for k,v in previous['binding'].items() if k != 'expectation_sha256'},
         {k:v for k,v in current['binding'].items() if k != 'expectation_sha256'}, 'launch_binding')
    same({k:v for k,v in old_fixed.items() if k != 'expectation_sha256'},
         {k:v for k,v in request['dependency_fixed'].items() if k != 'expectation_sha256'}, 'launch_fixed')
    dependency_sources = {n:checked_sources['dependency.' + n] for n in adapter.policy.outer.CHILD}
    dependency_sources['closure_manifest'] = encoded(request['sources'])
    for name, key in (('dependency_adapter_binding','outer_child'),
                      ('dependency_operational_scope','adapter.scope_policy'),
                      ('dependency_outer_contract','adapter.comparison_contract')):
        need(checked_sources[key] == adapter_owner.buffers[name], 'launch_loaded_adapter_source')
    metadata_owner.intact()
    # The already owned pure packet binder makes no runtime observer or I/O.
    metadata_owner.modules['dependency_execution'].bind_runtime_packet(
        request['dependency_packet'], request['dependency_fixed'], dependency_sources,
        request['dependency_review_sha256'])
    metadata_owner.intact()
    metadata = metadata_owner.call(**context_arguments)
    adapter_owner.intact()
    need(checked_metadata_sources(metadata_owner) == metadata_hashes, 'launch_metadata_loaded_source')
    result = metadata['metadata_result']
    need(result['phase'] == 'prepared' and result['operation_id'] == operation and
         result['retained_sidecar_contracts_checked'] is True, 'launch_metadata_result')
    checked = result['legacy_comparison_result']['metadata_contract_result']['checked_roles']
    need(set(checked) == adapter.policy.ORDINARY_INPUTS and len(checked) == 14, 'launch_metadata_coverage')
    return dict(schema='invented_launch_context_binding_v1', operation_id=operation,
        request_original_bytes_sha256=sha(request_bytes),
        context_document_sha256={n:sha(raw) for n,raw in context_arguments['documents'].items()},
        legacy_document_sha256={n:sha(raw) for n,raw in context_arguments['legacy_documents'].items()},
        source_receipts_sha256=sha(ordinary['authored_source_receipts']),
        comparison_roles=len(comparison), retained_roles=sorted(retained),
        replacement_roles=sorted(replaced), additional_roles=sorted(adapter.EXTRA_SOURCES),
        checked_ordinary_roles=sorted(checked), checked_metadata_source_hashes=dict(metadata_owner.hashes),
        metadata_result=result, source_freshness_verified=False, actual_startup_verified=False,
        rights_established=False, actual_inputs_accessed=False, execution_authorized=False,
        feature_supported=False, recovery_proven=False, device_write_gate_passed=False, camera_commands=[])


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
