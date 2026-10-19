"""Pure localization of the legacy adapter's four ordered digest comparisons.

Does not apply the adapter, validate cache contents or authorize continuation.
The declared cache *file* digest and producer's canonical-JSON digest are
separate quantities; equality is measured, never assumed to be necessary.
"""
import hashlib

from tools import dependency_evidence as core


VECTOR_PLAN = 'a914aca415d20a87a56440f36944f7ac6082ecbc36387b68694175a579bc43b5'
RAW_KEYS = ('schema','status','operation_id','evidence_class','test_injection_used',
    'config_sha256','cache_sha256','source_origins','trusted_origins','native_receipt',
    'cases','checks','events','gdt_execution_authorized','actual_gdt_entry_ready',
    'feature_supported','camera_commands','limitations')


def compare_saved_dependency_digests(*,config_json,raw_json,declared_cache_file_sha256):
    """Report equality of digest quantities and the earliest digest refusal.

    An identified digest refusal precedes all event comparisons in the frozen
    legacy adapter. If none fails, the historical generic refusal remains
    unlocalized; this function does not compare event/receipt semantics.
    """
    try:
        config_bytes=core._text_bytes(config_json);raw_bytes=core._text_bytes(raw_json)
        config,raw=core._bounded_copy([core._json_text(config_json),core._json_text(raw_json)])
        core._shape(config,('schema','operation_id','package_root','source_rows',
            'native_rows','trusted_origins','vectors'))
        core._shape(raw,RAW_KEYS)
        core._need(config['schema']=='dependency_probe_config_v1' and
            raw['schema']=='dependency_probe_raw_result_v1' and
            raw['status']=='complete_dependency_vectors','digest_diagnostic_schema')
        core._need(type(config['operation_id']) is str and
            len(config['operation_id'])==32 and all(c in '0123456789abcdef' for c in config['operation_id'])
            and raw['operation_id']==config['operation_id'],'digest_diagnostic_operation')
        for key in ('gdt_execution_authorized','actual_gdt_entry_ready','feature_supported','test_injection_used'):
            core._need(raw[key] is False,'authority')
        core._need(raw['camera_commands']==[] and raw['evidence_class']=='runtime-observed','authority')
        for value in (raw['config_sha256'],raw['cache_sha256'],declared_cache_file_sha256):core._digest(value)
        canonical_config=hashlib.sha256(core._canonical(config)+b'\n').hexdigest()
        vector_plan=core._hash(config['vectors'])
        comparisons=[
            dict(predicate='raw_config_equals_canonical_config',left=raw['config_sha256'],right=canonical_config),
            # The retrospective wrapper derives the expectation config digest
            # from that same canonical configuration, rather than its file hash.
            dict(predicate='raw_config_equals_retrospective_expectation',left=raw['config_sha256'],right=canonical_config),
            dict(predicate='raw_cache_equals_declared_cache_file_digest',left=raw['cache_sha256'],right=declared_cache_file_sha256),
            dict(predicate='vector_plan_equals_reviewed_public_plan',left=vector_plan,right=VECTOR_PLAN),
        ]
        for row in comparisons:row['equal']=row['left']==row['right']
        first=next((row['predicate'] for row in comparisons if not row['equal']),None)
        return dict(schema='legacy_digest_localization_v1',
            status='earliest_digest_refusal_localized' if first else 'digest_prefix_equal_event_failure_unlocalized',
            first_failing_digest_predicate=first,comparisons=comparisons,
            config_file_sha256=hashlib.sha256(config_bytes).hexdigest(),
            raw_file_sha256=hashlib.sha256(raw_bytes).hexdigest(),
            config_file_equals_canonical_digest=hashlib.sha256(config_bytes).hexdigest()==canonical_config,
            cache_digest_meaning='raw_is_canonical_json_plus_newline_declared_is_original_file_bytes',
            cache_content_change_proven=False,cache_content_revalidated=False,
            whole_record_semantics_validated=False,legacy_comparison_retried=False,
            historical_events_authenticated=False,execution_authorized=False,
            feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])
    except core.EvidenceError:raise
    except Exception:raise core.EvidenceError('digest_diagnostic_shape') from None
