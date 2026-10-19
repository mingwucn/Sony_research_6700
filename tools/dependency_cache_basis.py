"""Separate historical cache-file and producer JSON digest declarations.

The producer digest is taken from the same saved raw record being compared.
It is never an independent expectation or cache-content observation.
"""
import hashlib

from tools import dependency_evidence as core
from tools import dependency_digest_diagnostic as diagnostic


BLOCKERS = (
    'cache_expectation_is_same_saved_raw_record_self_report',
    'cache_file_and_canonical_content_relationship_unproved',
    'cache_contents_not_independently_revalidated',
)


def declare_cache_digest_domains(*, config_json, raw_json, localization_json,
                                core_sha256, diagnostic_sha256,
                                original_failure_sha256, cache_file_sha256):
    """Bind the earlier localization, then label the two declared quantities.

    Recomputing its four comparisons authenticates no historic event or source.
    Hashes of sources/failure remain caller declarations in this pure function.
    """
    try:
        for value in (core_sha256, diagnostic_sha256, original_failure_sha256,
                      cache_file_sha256):
            core._digest(value)
        config_bytes = core._text_bytes(config_json)
        raw_bytes = core._text_bytes(raw_json)
        core._text_bytes(localization_json)
        saved = core._bounded_copy(core._json_text(localization_json))
        core._shape(saved, ('schema', 'status', 'failed_attempt_sha256', 'input_sha256',
            'localization', 'legacy_adapter_executed', 'cache_body_read',
            'firmware_read', 'installed_dependency_executed', 'camera_commands'))
        core._need(saved['schema'] == 'saved_digest_diagnostic_v1' and
                   saved['status'] == 'digest_localization_recorded', 'cache_basis_schema')
        for key in ('legacy_adapter_executed', 'cache_body_read', 'firmware_read',
                    'installed_dependency_executed'):
            core._need(saved[key] is False, 'cache_basis_authority')
        core._need(saved['camera_commands'] == [], 'cache_basis_authority')
        expected = dict(core=core_sha256, diagnostic=diagnostic_sha256,
            failure=original_failure_sha256,
            config=hashlib.sha256(config_bytes).hexdigest(),
            raw=hashlib.sha256(raw_bytes).hexdigest())
        core._need(core._canonical(saved['input_sha256']) == core._canonical(expected)
            and saved['failed_attempt_sha256'] == original_failure_sha256, 'cache_basis_binding')
        measured = diagnostic.compare_saved_dependency_digests(
            config_json=config_json, raw_json=raw_json,
            declared_cache_file_sha256=cache_file_sha256)
        core._need(core._canonical(saved['localization']) == core._canonical(measured),
                   'cache_basis_localization')
        core._need(measured['first_failing_digest_predicate'] ==
            'raw_cache_equals_declared_cache_file_digest' and
            [row['equal'] for row in measured['comparisons']] == [True, True, False, True],
            'cache_basis_scope')
        producer_digest = measured['comparisons'][2]['left']
        return dict(schema='retrospective_cache_digest_domains_v1',
            status='declared_domains_separated_with_blockers',
            file_bytes=dict(sha256=cache_file_sha256, basis='prior_file_digest_declaration'),
            producer_canonical_json_plus_newline=dict(sha256=producer_digest,
                basis='same_saved_raw_record_self_report'),
            legacy_cache_expectation_sha256=producer_digest,
            localization_sha256=hashlib.sha256(localization_json.encode('utf-8')).hexdigest(),
            relationship='different_domains_content_relationship_unproved',
            blockers=list(BLOCKERS), independent_cache_expectation=False,
            cache_content_revalidated=False, cache_content_change_proven=False,
            historical_events_authenticated=False, prior_approval_proven=False,
            execution_authorized=False, feature_supported=False, recovery_proven=False,
            device_write_gate_passed=False, camera_commands=[])
    except core.EvidenceError:
        raise
    except Exception:
        raise core.EvidenceError('cache_basis_shape') from None
