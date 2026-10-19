"""Pure invented legacy/successor metadata comparison, never an activation API.

Legacy records have no operation/cache/root/bootstrap fields. A caller's explicit
supplement pins successor context but cannot create missing historical authority.
"""
if __name__ == '__main__':
    raise SystemExit(2)

from tools import dependency_activity_metadata as activity

e = activity.e
core = activity.composed.evidence
ORDINARY = frozenset(('binding_plan','prerequisites','dependency_packet','dependency_fixed'))
ABSENT_CONTEXT = ('operation_id','source_mapping','cache_bytes','root_identity','loader_kwargs','bootstrap_boundary')


def project_native_policy(policy, manifest, trusted_receipts):
    """Explicit relative-path-only projection; receipt tokens are canonical JSON.

    Retain original absolute receipts outside this view. Projection is a chosen
    comparison representation, not evidence of original legacy token provenance.
    """
    e.shape(trusted_receipts, policy['trusted_origins'], 'bridge_trusted_roster')
    backend = {}
    for alias, expected in policy['trusted_origins'].items():
        value = trusted_receipts[alias]
        path = policy['roots']['runtime']['path'].rstrip('/')+'/'+expected['relative_path']
        core._receipt(value,path,expected['sha256'],expected['size'],expected['identity'])
        projected = dict(value,path=expected['relative_path'])
        backend[alias] = dict(path=expected['relative_path'],sha256=expected['sha256'],
            open_identity_sha256=core._hash(projected))
    groups = {name:{alias:dict(path=row['relative_path'],sha256=row['sha256'])
                   for alias,row in policy[name].items()} for name in ('python_origins','native_libraries')}
    # Two disjoint absolute roots can collapse into ambiguous relative labels.
    core._unique([row['path'] for rows in (*groups.values(),backend) for row in rows.values()])
    return dict(schema='activation_native_policy_v1',version=manifest['version'],backend=policy['backend'],
        extension_suffix=policy['extension_suffix'],record_sha256=manifest['record_sha256'],
        backend_origins=backend,no_fallback=policy['no_fallback'],**groups)


def compare_invented_metadata(*, legacy, prerequisites_dependency, packet, fixed,
        source_buffers, dependency_anchor, trusted_receipts, successor_context):
    """Compare already supplied records, validating successor with retained binder.

    This lower-level helper does not validate the full four-document envelope,
    external anchors or frozen legacy binding source. The full API below does.
    """
    e.shape(legacy, ('schema','version','wheel_sha256','record_sha256','expected_files','native_policy'),
        'bridge_legacy_shape')
    e.need(legacy['schema']=='activation_dependency_plan_v1' and type(legacy['version']) is str,
        'bridge_legacy_schema')
    activity.same(legacy,prerequisites_dependency,'bridge_legacy_prerequisites')
    e.shape(dependency_anchor, ('schema','invented','operation_id','fixed_file_sha256','prior_review_sha256','source_roles'),
        'bridge_dependency_anchor_shape')
    e.need(dependency_anchor['schema']=='invented_dependency_input_anchor_v1' and
        dependency_anchor['invented'] is True,'bridge_dependency_anchor_mode')
    e.digest(dependency_anchor['prior_review_sha256']);e.digest(dependency_anchor['fixed_file_sha256'])
    mapping = dependency_anchor['source_roles']
    e.need(type(packet) is dict and type(packet.get('inputs')) is dict and
        type(packet['inputs'].get('expectation')) is dict and
        type(packet['inputs']['expectation'].get('source_sha256')) is dict,'bridge_packet_policy')
    e.shape(mapping,packet['inputs']['expectation']['source_sha256'],'bridge_source_roster')
    e.need(0<len(mapping)<=32 and
        all(type(role) is str and role in source_buffers and role in e.SOURCE_ROLES for role in mapping.values()) and
        len(set(mapping.values()))==len(mapping),
        'bridge_source_mapping')
    bound = activity.composed.dependency.execution.bind_runtime_packet(packet,fixed,
        {alias:source_buffers[role] for alias,role in mapping.items()},dependency_anchor['prior_review_sha256'])
    policy=bound['expectation'];manifest=bound['package']['manifest']
    e.need(legacy['version']==manifest['version']=='3.24.1','bridge_version')
    e.need(legacy['wheel_sha256']==manifest['wheel_sha256'],'bridge_wheel')
    expected_context = dict(operation_id=policy['operation_id'],source_roles=mapping,
        source_sha256=policy['source_sha256'],config_text_sha256=policy['config_sha256'],
        cache_text_sha256=policy['cache_sha256'],root_sha256=fixed['root_sha256'],
        loader_kwargs=policy['loader_kwargs'],bootstrap_boundary=policy['bootstrap_boundary'],
        manifest_sha256=policy['manifest_sha256'],installed_proof_sha256=policy['installed_proof_sha256'])
    activity.same(successor_context,expected_context,'bridge_successor_context')
    e.need(dependency_anchor['operation_id']==policy['operation_id'],'bridge_operation')
    native=project_native_policy(policy,manifest,trusted_receipts)
    missing=[]
    for key,expected in (('record_sha256',manifest['record_sha256']),('expected_files',manifest['files']),
                         ('native_policy',native)):
        if legacy[key] is None:
            missing.append(key)
        else:
            activity.same(legacy[key],expected,'bridge_'+key)
    return dict(schema='invented_legacy_dependency_comparison_v1',
        shared_fields_consistent=True,shared_plan_metadata_complete=not missing,
        missing_legacy_fields=missing,legacy_absent_context=list(ABSENT_CONTEXT),
        projected_native_policy_sha256=core._hash(native),
        legacy_context_binding_present=False,successor_context_claims_match=True,
        original_legacy_token_provenance_verified=False,source_mapping_observed=False,
        cache_freshness_verified=False,dependency_bridge_verified=False,actual_startup_verified=False,
        actual_inputs_accessed=False,execution_authorized=False,feature_supported=False,
        recovery_proven=False,device_write_gate_passed=False,camera_commands=[])


def validate_invented_bridge(documents, *, bridge_anchor_bytes, external_bridge_anchor_sha256,
        trusted_receipt_buffers, **common):
    """Compose fourteen role checks and explicitly anchored shared-field checks."""
    # The bridge record is separate from the retained fourteen ordinary roles.
    result=activity.validate_invented_all_metadata(documents,**common)
    anchor=activity.record(bridge_anchor_bytes,'invented_legacy_bridge_anchor_v1',
        ('ordinary','source_anchor_sha256','dependency_anchor_sha256','activity_anchor_sha256',
         'trusted_receipts','projection','successor_context','legacy_absent_context'), 'bridge_anchor')
    e.digest(external_bridge_anchor_sha256)
    e.need(e.sha(bridge_anchor_bytes)==external_bridge_anchor_sha256,'bridge_external_anchor')
    o=common['ordinary_buffers']
    e.receipts(anchor['ordinary'],{k:o[k] for k in ORDINARY},ORDINARY)
    dep=e.decode(common['dependency_anchor_bytes'])
    packet=e.decode(o['dependency_packet']);fixed=e.decode(o['dependency_fixed'])
    policy=packet['inputs']['expectation']
    e.receipts(anchor['trusted_receipts'],trusted_receipt_buffers,policy['trusted_origins'])
    for field,raw in (('source_anchor_sha256',common['source_anchor_bytes']),
                      ('dependency_anchor_sha256',common['dependency_anchor_bytes']),
                      ('activity_anchor_sha256',common['activity_anchor_bytes'])):
        e.digest(anchor[field]);e.need(anchor[field]==e.sha(raw),'bridge_cross_anchor')
    e.need(anchor['projection']=='relative_path_only_canonical_receipt_v1','bridge_projection')
    activity.same(anchor['legacy_absent_context'],list(ABSENT_CONTEXT),'bridge_absent_context')
    e.need(anchor['operation_id']==result['activity_result']['operation_id']==dep['operation_id'],'bridge_operation')
    legacy=e.decode(o['binding_plan'])['dependency']
    prerequisites=e.decode(o['prerequisites'])['binding_input']['dependency']
    compared=compare_invented_metadata(legacy=legacy,prerequisites_dependency=prerequisites,packet=packet,
        fixed=fixed,source_buffers=common['source_buffers'],dependency_anchor=dep,
        trusted_receipts={k:e.decode(v) for k,v in trusted_receipt_buffers.items()},
        successor_context=anchor['successor_context'])
    compared.update(metadata_contract_result=result,bridge_anchor_file_sha256=external_bridge_anchor_sha256)
    return compared


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
