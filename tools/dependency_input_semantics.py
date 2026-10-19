"""Pure dependency-role checks on invented envelopes; runtime always disabled.

Caller anchors establish byte consistency, not who approved them or freshness.
No payload/source text is executed and no installed files are read.
"""
if __name__ == '__main__':
    raise SystemExit(2)

from tools import dependency_authority_grammar as envelope
from tools import dependency_execution as execution

CHECKED_ROLES = frozenset(('dependency_packet', 'dependency_fixed'))


def validate_invented_dependency_roles(documents, *, external_seal_sha256,
        scope_bytes, source_buffers, ordinary_buffers, historical_buffers,
        dependency_anchor_bytes, external_dependency_anchor_sha256):
    """Check two roles using the retained binder and separately anchored inputs.

    The dependency anchor is prior caller-selected expectation metadata, outside
    the four-document graph. Its digest/claimed prior review are not signatures.
    No current review digest may replace the dependency's earlier review ID.
    Source alias mapping is explicit in this anchor; no production map is inferred.
    """
    envelope.validate_invented_chain(documents, external_seal_sha256=external_seal_sha256,
        scope_bytes=scope_bytes, source_buffers=source_buffers,
        ordinary_buffers=ordinary_buffers, historical_buffers=historical_buffers)
    anchor = envelope.decode(dependency_anchor_bytes)
    envelope.digest(external_dependency_anchor_sha256)
    envelope.need(envelope.sha(dependency_anchor_bytes) == external_dependency_anchor_sha256,
                  'dependency_external_anchor')
    envelope.shape(anchor, ('schema', 'invented', 'operation_id', 'fixed_file_sha256',
                            'prior_review_sha256', 'source_roles'), 'dependency_anchor_shape')
    envelope.need(anchor['schema'] == 'invented_dependency_input_anchor_v1' and
                  anchor['invented'] is True, 'dependency_anchor_mode')
    for key in ('fixed_file_sha256', 'prior_review_sha256'):
        envelope.digest(anchor[key])
    envelope.need(anchor['prior_review_sha256'] not in
                  {envelope.sha(value) for value in documents.values()}, 'dependency_review_cycle')
    envelope.need(anchor['fixed_file_sha256'] == envelope.sha(ordinary_buffers['dependency_fixed']),
                  'dependency_fixed_original_bytes')
    packet = envelope.decode(ordinary_buffers['dependency_packet'])
    fixed = envelope.decode(ordinary_buffers['dependency_fixed'])
    # Validate the outer packet before looking at its expectation or alias map.
    envelope.shape(packet, ('schema', 'inputs'), 'dependency_packet_shape')
    envelope.need(packet['schema'] == 'runtime_dependency_packet_v1', 'dependency_packet_mode')
    envelope.shape(packet['inputs'], ('expectation', 'package', 'binding', 'config_json', 'cache_json'),
                   'dependency_input_roster')
    policy = packet['inputs']['expectation']
    envelope.need(type(policy) is dict and type(policy.get('source_sha256')) is dict,
                  'dependency_source_policy')
    mapping = anchor['source_roles']
    envelope.shape(mapping, policy['source_sha256'], 'dependency_source_mapping')
    envelope.need(0 < len(mapping) <= 32 and all(type(role) is str and role in envelope.SOURCE_ROLES
                  for role in mapping.values()), 'dependency_source_role')
    envelope.need(len(set(mapping.values())) == len(mapping), 'dependency_source_alias')
    selected = {alias: source_buffers[role] for alias, role in mapping.items()}
    # This existing pure function checks package/proof/root policy, original
    # config/cache text hashes, cache-to-origin equality and source byte hashes.
    bound = execution.bind_runtime_packet(packet, fixed, selected, anchor['prior_review_sha256'])
    envelope.need(type(anchor['operation_id']) is str and
                  anchor['operation_id'] == bound['expectation']['operation_id'], 'dependency_operation')
    return dict(schema='invented_dependency_role_consistency_v1',
        checked_roles=sorted(CHECKED_ROLES),
        pending_roles=sorted(envelope.policy.ORDINARY_INPUTS - CHECKED_ROLES),
        dependency_anchor_file_sha256=external_dependency_anchor_sha256,
        packet_file_sha256=envelope.sha(ordinary_buffers['dependency_packet']),
        fixed_file_sha256=envelope.sha(ordinary_buffers['dependency_fixed']),
        config_text_sha256=bound['expectation']['config_sha256'],
        cache_text_sha256=bound['expectation']['cache_sha256'],
        expectation_object_sha256=fixed['expectation_sha256'],
        package_object_sha256=fixed['package_sha256'],
        declared_source_aliases=sorted(mapping),
        current_metadata_freshness_verified=False, producer_execution_authenticated=False,
        interpreter_identity_verified=False, actual_inputs_accessed=False,
        execution_authorized=False, feature_supported=False, recovery_proven=False,
        device_write_gate_passed=False, camera_commands=[])


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
