"""Invented activity/qualification consistency only; never an authority API.

All anchors and reports are supplied claims. No reads, rights adjudication,
qualification execution or operational activation occur in this module.
"""
if __name__ == '__main__':
    raise SystemExit(2)

from tools import dependency_source_receipts as composed

e = composed.envelope
ROLES = frozenset(('activity_scope', 'activity_rights', 'historical_evidence_index', 'qualification_index'))
VALIDATORS = frozenset(('envelope', 'source_receipts', 'basis', 'dependency', 'activity'))
ARTIFACTS = frozenset(('result', 'log'))


def same(left, right, code):
    e.need(composed.links.equal(left, right), code)


def record(raw, schema, fields, code):
    value = e.decode(raw)
    e.shape(value, ('schema', 'invented', 'operation_id', 'camera_commands') + fields, code+'_shape')
    e.need(value['schema'] == schema and value['invented'] is True and value['camera_commands'] == [], code+'_mode')
    composed._operation(value['operation_id'])
    return value


def validate_invented_activity_roles(documents, *, activity_anchor_bytes,
        external_activity_anchor_sha256, validator_buffers, qualification_buffers, **common):
    """Check four remaining contracts; supplied source digests are not ownership.

    Qualification result/log buffers are invented, bounded and externally pinned.
    Passing claims do not authenticate who ran the tests or which code executed.
    """
    e.validate_invented_chain(documents, **{k:common[k] for k in
        ('external_seal_sha256','scope_bytes','source_buffers','ordinary_buffers','historical_buffers')})
    e.digest(external_activity_anchor_sha256)
    anchor = record(activity_anchor_bytes, 'invented_activity_anchor_v1',
        ('ordinary', 'source_anchor_sha256', 'dependency_anchor_sha256', 'validators',
         'qualification', 'expected_test_count'), 'activity_anchor')
    e.need(e.sha(activity_anchor_bytes) == external_activity_anchor_sha256, 'activity_external_anchor')
    ordinary = common['ordinary_buffers']
    e.receipts(anchor['ordinary'], {k:ordinary[k] for k in ROLES}, ROLES)
    e.receipts(anchor['validators'], validator_buffers, VALIDATORS)
    e.receipts(anchor['qualification'], qualification_buffers, ARTIFACTS)
    e.need(type(anchor['expected_test_count']) is int and 0 < anchor['expected_test_count'] <= 1000000,
        'qualification_expected_count')
    for field, raw_name in (('source_anchor_sha256','source_anchor_bytes'),
                            ('dependency_anchor_sha256','dependency_anchor_bytes')):
        e.digest(anchor[field])
        e.need(anchor[field] == e.sha(common[raw_name]), 'activity_cross_anchor')
    # All expectations are outside the forward four-document authority DAG.
    current_hashes = {e.sha(v) for v in documents.values()}
    digests = [anchor[k] for k in ('source_anchor_sha256','dependency_anchor_sha256')]
    digests += [row['sha256'] for group in ('ordinary','validators','qualification') for row in anchor[group].values()]
    e.need(not current_hashes.intersection(digests), 'activity_anchor_cycle')
    activity = record(ordinary['activity_scope'], 'invented_activity_scope_v1',
        ('purpose','scope_file_sha256','limits','source_manifest_sha256','source_receipts_sha256',
         'source_anchor_sha256','dependency_anchor_sha256','protected','historical_blockers'), 'activity_scope')
    e.need(activity['purpose'] == 'offline_metadata_contract_qualification', 'activity_purpose')
    e.need(activity['scope_file_sha256'] == e.sha(common['scope_bytes']), 'activity_scope_bytes')
    same(activity['limits'], e.policy.SCOPE, 'activity_limits')
    for field, name in (('source_manifest_sha256','authored_source_manifest'),
                        ('source_receipts_sha256','authored_source_receipts')):
        e.need(activity[field] == e.sha(ordinary[name]), 'activity_source_binding')
    for field in ('source_anchor_sha256','dependency_anchor_sha256'):
        e.need(activity[field] == anchor[field], 'activity_anchor_binding')
    candidate = e.decode(documents['candidate'])
    same(activity['protected'], candidate['protected'], 'activity_protected_binding')
    same(activity['historical_blockers'], list(e.policy.HISTORY), 'activity_historical_blockers')
    rights = record(ordinary['activity_rights'], 'invented_activity_rights_v1',
        ('scope_file_sha256','activity_scope_sha256','owner_facts','uncertainties',
         'decision','legal_basis_established','execution_authorized'), 'activity_rights')
    e.need(rights['scope_file_sha256'] == e.sha(common['scope_bytes']) and
        rights['activity_scope_sha256'] == e.sha(ordinary['activity_scope']), 'rights_scope_binding')
    same(rights['owner_facts'], e.policy.OWNER, 'rights_owner_facts')
    same(rights['uncertainties'], {k:'unresolved' for k in e.policy.RIGHTS}, 'rights_uncertainties')
    e.need(rights['decision'] == 'pending' and rights['legal_basis_established'] is False and
        rights['execution_authorized'] is False, 'rights_authority')
    # The retained envelope already checks the exact comparison-only historical
    # index schema, roster and all original historical byte receipts.
    history = e.decode(ordinary['historical_evidence_index'])
    e.need(history['purpose'] == 'comparison_only', 'history_authority')
    index = record(ordinary['qualification_index'], 'invented_qualification_index_v1',
        ('purpose','ordinary','sources','validators','artifacts','claimed_checked_roles',
         'execution_authenticated','freshness_verified'), 'qualification_index')
    e.need(index['purpose'] == 'invented_claims_only' and index['execution_authenticated'] is False and
        index['freshness_verified'] is False, 'qualification_authority')
    other_roles = e.policy.ORDINARY_INPUTS - {'qualification_index'}
    e.receipts(index['ordinary'], {k:ordinary[k] for k in other_roles}, other_roles)
    e.receipts(index['sources'], common['source_buffers'], e.SOURCE_ROLES)
    e.receipts(index['validators'], validator_buffers, VALIDATORS)
    e.receipts(index['artifacts'], qualification_buffers, ARTIFACTS)
    same(index['claimed_checked_roles'], sorted(e.policy.ORDINARY_INPUTS), 'qualification_coverage')
    result = record(qualification_buffers['result'], 'invented_qualification_result_v1',
        ('total','passed','failures','errors','skipped','exit_code','sources','validators',
         'log_sha256','claimed_checked_roles','actual_inputs_accessed','execution_authorized'), 'qualification_result')
    for key in ('total','passed','failures','errors','skipped','exit_code'):
        e.need(type(result[key]) is int, 'qualification_count_type')
    e.need(result['total'] == result['passed'] == anchor['expected_test_count'] and
        result['failures'] == result['errors'] == result['skipped'] == result['exit_code'] == 0,
        'qualification_failed_or_partial')
    e.need(result['actual_inputs_accessed'] is False and result['execution_authorized'] is False,
        'qualification_result_authority')
    e.receipts(result['sources'], common['source_buffers'], e.SOURCE_ROLES)
    e.receipts(result['validators'], validator_buffers, VALIDATORS)
    e.need(result['log_sha256'] == e.sha(qualification_buffers['log']), 'qualification_log_binding')
    same(result['claimed_checked_roles'], index['claimed_checked_roles'], 'qualification_result_coverage')
    operation = anchor['operation_id']
    for value in (activity, rights, index, result, e.decode(common['source_anchor_bytes']),
                  e.decode(common['dependency_anchor_bytes'])):
        e.need(value.get('operation_id') == operation, 'activity_operation_binding')
    return dict(schema='invented_activity_metadata_consistency_v1', operation_id=operation,
        checked_roles=sorted(ROLES), claims_match_supplied_buffers=True,
        qualification_execution_authenticated=False, validator_execution_owned=False,
        rights_established=False, history_freshness_verified=False, actual_inputs_accessed=False,
        execution_authorized=False, feature_supported=False, recovery_proven=False,
        device_write_gate_passed=False, camera_commands=[])


def validate_invented_all_metadata(documents, *, activity_anchor_bytes,
        external_activity_anchor_sha256, validator_buffers, qualification_buffers, **common):
    """Compose all fourteen contract checks, without declaring runtime readiness."""
    activity = validate_invented_activity_roles(documents, activity_anchor_bytes=activity_anchor_bytes,
        external_activity_anchor_sha256=external_activity_anchor_sha256,
        validator_buffers=validator_buffers, qualification_buffers=qualification_buffers, **common)
    retained = composed.validate_invented_composed_inputs(documents, **common)
    e.need(activity['operation_id'] == retained['operation_id'], 'composed_operation')
    return dict(schema='invented_fourteen_metadata_contracts_v1', checked_roles=sorted(ROLES|composed.CHECKED),
        pending_ordinary_role_contracts=[], activity_result=activity, retained_result=retained,
        complete_basis_semantics_verified=False, current_candidate_operation_bound=False,
        validator_execution_owned=False, qualification_execution_authenticated=False,
        history_freshness_verified=False, rights_established=False, dependency_bridge_verified=False,
        actual_startup_verified=False, source_reads_observed=False, actual_inputs_accessed=False,
        execution_authorized=False, feature_supported=False, recovery_proven=False,
        device_write_gate_passed=False, camera_commands=[])


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
