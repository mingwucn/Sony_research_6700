"""Current prepared-source/dependency semantics on invented records only.

No acquisition, source opens, dependency activation or runtime observer. Original
comparison records stay separate. Checked owners and this caller are trusted.
"""
if __name__ == '__main__':
    raise SystemExit(2)

from tools import dependency_launch_context as launch

BASIS = frozenset(('basis','source_manifest','prerequisites','binding_plan','role_authority','binding_schema'))
RETAINED = BASIS | {'historical_evidence_index'}


def record(raw, schema, fields, operation):
    value = launch.strict(raw)
    launch.need(type(value) is dict and set(value) == set(fields) |
        {'schema','invented','operation_id','camera_commands'}, 'current_record_shape')
    launch.need(value['schema'] == schema and value['invented'] is True and
        value['operation_id'] == operation and value['camera_commands'] == [], 'current_record_mode')
    return value


def receipts(rows, buffers):
    launch.need(type(rows) is dict and type(buffers) is dict and set(rows) == set(buffers), 'current_receipt_roster')
    for name, raw in buffers.items():
        launch.need(type(raw) is bytes and 0 < len(raw) <= 2*1024**2, 'current_buffer_bound')
        launch.same(rows[name], dict(bytes=len(raw),sha256=launch.sha(raw)), 'current_original_bytes')


def validate_invented_current(*, ordinary_buffers, expected_ordinary_receipts, **launch_arguments):
    """Check fourteen current roles, reusing six retained basis contracts.

    The source-read/qualification records remain supplied claims. Matching their
    bytes does not observe freshness or authenticate who produced them.
    """
    adapter_owner = launch_arguments['adapter_owner']
    metadata_owner = launch_arguments['metadata_owner']
    adapter_owner.intact()
    policy = adapter_owner.modules['dependency_adapter_binding'].policy
    launch.need(type(ordinary_buffers) is dict and set(ordinary_buffers) == policy.ORDINARY_INPUTS,
        'current_ordinary_roster')
    receipts(expected_ordinary_receipts, ordinary_buffers)
    comparison = launch.validate_invented_launch(**launch_arguments)
    request = launch.strict(launch_arguments['request_bytes'])
    operation = request['operation_id']
    previous = launch_arguments['context_arguments']['ordinary_buffers']
    for name in RETAINED:
        launch.need(ordinary_buffers[name] == previous[name], 'current_retained_original_bytes')
    manifest = record(ordinary_buffers['authored_source_manifest'], 'invented_current_source_manifest_v1',
        ('root_path','sources','derived'), operation)
    evidence = metadata_owner.modules['dependency_evidence']
    root = evidence._absolute(manifest['root_path'])
    launch.need(not root.endswith('/'), 'current_source_root')
    launch.same(manifest['sources'],request['sources'],'current_source_map')
    closure = launch.encoded(request['sources'])
    launch.same(manifest['derived'], dict(closure_manifest=dict(
        kind='canonical_prepared_source_map_v1',bytes=len(closure),sha256=launch.sha(closure))), 'current_derived_closure')
    source_receipts = record(ordinary_buffers['authored_source_receipts'], 'invented_current_source_receipts_v1',
        ('manifest_file_sha256','rows'), operation)
    launch.need(source_receipts['manifest_file_sha256'] == launch.sha(ordinary_buffers['authored_source_manifest']),
        'current_receipt_manifest')
    rows = source_receipts['rows']
    launch.need(type(rows) is dict and set(rows) == set(request['sources']), 'current_source_receipt_roster')
    identities, aliases = {}, {}
    for role, row in request['sources'].items():
        item = rows[role]
        launch.need(type(item) is dict and set(item) == {'receipt','close_attempts','eof_probes','read_calls','closed'},
            'current_source_read_shape')
        launch.need(item['closed'] is True and all(type(item[n]) is int and item[n] == 1
            for n in ('close_attempts','eof_probes')) and type(item['read_calls']) is int and
            2 <= item['read_calls'] <= row['bytes']+1, 'current_source_read_completion')
        evidence._receipt(item['receipt'],root+'/'+row['path'],row['sha256'],row['bytes'])
        identity = item['receipt']['fstat_before']
        key = identity['device'],identity['inode']
        path = row['path']
        if key in identities:
            launch.need(identities[key] == path, 'current_source_identity_alias')
        identities[key] = path
        if path in aliases:
            launch.same(item,aliases[path],'current_source_shared_receipt')
        aliases[path] = item
    packet = launch.strict(ordinary_buffers['dependency_packet'])
    fixed = launch.strict(ordinary_buffers['dependency_fixed'])
    launch.same(packet,request['dependency_packet'],'current_dependency_packet')
    launch.same(fixed,request['dependency_fixed'],'current_dependency_fixed')
    # The owned pure packet binder was called above with the five captured
    # helper buffers plus this same derived closure. Neither is opened as a file.
    scope = record(ordinary_buffers['activity_scope'], 'invented_current_activity_scope_v1',
        ('purpose','request_bytes_sha256','limits','source_manifest_sha256','source_receipts_sha256',
         'comparison_context_seal_sha256','protected','historical_blockers'), operation)
    expected = dict(purpose='invented_current_metadata_qualification',
        request_bytes_sha256=launch.sha(launch_arguments['request_bytes']), limits=policy.SCOPE,
        source_manifest_sha256=launch.sha(ordinary_buffers['authored_source_manifest']),
        source_receipts_sha256=launch.sha(ordinary_buffers['authored_source_receipts']),
        comparison_context_seal_sha256=launch_arguments['context_arguments']['external_context_seal_sha256'],
        protected=launch.strict(launch_arguments['context_arguments']['legacy_documents']['candidate'])['protected'],
        historical_blockers=list(policy.HISTORY))
    launch.same({k:scope[k] for k in expected},expected,'current_activity_binding')
    rights = record(ordinary_buffers['activity_rights'], 'invented_current_activity_rights_v1',
        ('activity_scope_sha256','owner_facts','uncertainties','decision','legal_basis_established','execution_authorized'),operation)
    launch.same({k:rights[k] for k in ('activity_scope_sha256','owner_facts','uncertainties','decision',
        'legal_basis_established','execution_authorized')}, dict(
        activity_scope_sha256=launch.sha(ordinary_buffers['activity_scope']),owner_facts=policy.OWNER,
        uncertainties={k:'unresolved' for k in policy.RIGHTS},decision='pending',
        legal_basis_established=False,execution_authorized=False), 'current_rights')
    index = record(ordinary_buffers['qualification_index'], 'invented_current_qualification_index_v1',
        ('purpose','ordinary','current_sources_sha256','comparison_index_sha256','declared_checked_roles',
         'execution_authenticated','freshness_verified'), operation)
    launch.need(index['purpose'] == 'invented_current_contract_claims_only' and
        index['execution_authenticated'] is False and index['freshness_verified'] is False, 'current_qualification_authority')
    receipts(index['ordinary'],{k:v for k,v in ordinary_buffers.items() if k != 'qualification_index'})
    launch.need(index['current_sources_sha256'] == launch.sha(launch.encoded(request['sources'])) and
        index['comparison_index_sha256'] == launch.sha(previous['qualification_index']), 'current_qualification_binding')
    launch.same(index['declared_checked_roles'],sorted(policy.ORDINARY_INPUTS),'current_qualification_coverage')
    adapter_owner.intact()
    launch.checked_metadata_sources(metadata_owner)
    return dict(schema='invented_current_metadata_consistency_v1',operation_id=operation,
        checked_roles=sorted(policy.ORDINARY_INPUTS),retained_roles=sorted(RETAINED),
        current_source_roles=len(rows),unique_source_paths=len(aliases),derived_closure_is_file=False,
        current_ordinary_sha256={k:launch.sha(v) for k,v in ordinary_buffers.items()},comparison_result=comparison,
        source_reads_observed=False,source_freshness_verified=False,qualification_execution_authenticated=False,
        rights_established=False,actual_startup_verified=False,actual_inputs_accessed=False,
        execution_authorized=False,feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
