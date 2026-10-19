"""Pure non-executable migration-review packet; never an activation validator.

Source hashes describe comparison texts, including sources needing replacement.
This packet intentionally has no operation/session, argv, input paths or seal.
"""
import hashlib
import json
from pathlib import PurePosixPath

# Refuse the direct CLI before package imports, including isolated file mode.
if __name__=='__main__':
    raise SystemExit(2)

from tools import dependency_outer_contract as outer


SOURCE_ROLES = outer.SOURCE_ROLES - {'invented_fixture'}
ORDINARY_INPUTS = frozenset(('basis','source_manifest','prerequisites','binding_plan',
    'role_authority','binding_schema','authored_source_manifest','authored_source_receipts',
    'dependency_packet','dependency_fixed','activity_scope','activity_rights',
    'historical_evidence_index','qualification_index'))
BASIS_ROLES = ('prior_stream','prior_prefix','prior_directory','prior_member_identification',
    'prior_selection','prior_measured','prior_accepted_inventory','lead_plan',
    'prior_ext_superblock_observation')
RIGHTS = frozenset(('accepted_contract_interaction','accompanying_component_terms',
    'constants_provenance','narrow_research_hypothesis_scope','distinct_operational_act_decision'))
LEGACY_INPUTS = frozenset(('basis','source_manifest','prerequisites','binding_plan',
    'dependency_config','source_cache','source_receipts','role_authority','binding_schema',
    'historical_scope','historical_rights','activity_scope','activity_rights',
    'q_old_result','q_old_seal','q_old_review','q_integration_result','q_integration_review',
    'q_snapshot_result','q_snapshot_log','q_outer_result','q_outer_review','repair_overlay',
    'q_repair_result','q_repair_review','factory_evidence','parent_evidence'))
HISTORY = (
    'legacy_raw_is_not_successor_guard_transcript','legacy_events_are_not_successor_event_grammar',
    'individual_durability_steps_not_journaled','guard_install_and_finish_not_explicit_events',
    'cleanup_claim_not_journaled','read_only_open_mode_not_explicit_in_legacy_receipts',
    'pre_execution_expectation_approval_unestablished','producer_source_authority_not_bound',
    'source_cache_content_not_revalidated','fresh_runtime_observation_not_performed',
    'expectations_derived_after_historical_observation','root_tokens_are_path_labels_not_directory_observations',
    'executing_source_buffers_not_authenticated','cache_digest_declaration_not_content_revalidation',
    'cache_expectation_is_same_saved_raw_record_self_report','cache_file_and_canonical_content_relationship_unproved',
    'cache_contents_not_independently_revalidated')
SCOPE = dict(source_opens=2,full_source_passes=4,source_bytes_on_success=4096071392,
    metadata_leads=2,basis_roles=9,historical_blocks=5,descriptor_bytes_per_lead=32768,
    descriptor_bytes_total=65536,selected_raw_allowance_phase_a=73728,
    selected_raw_allowance_phase_b=139264,preparation_attempts=1,pipeline_calls=2,
    child_deadline_seconds=300,log_bytes_per_pipe=2097152,termination_wait_seconds=5,
    reader_join_seconds=1,inode_reads=0,bitmap_reads=0,directory_reads=0,content_reads=0,
    raw_component_files=0,network_operations=0,camera_operations=0)
OWNER = dict(country='China',personal=True,noncommercial=True,
    existing_inspection_rights='No / unknown',download_consent_alone_clears_inspection=False)
FLAGS = ('operational_roster_complete','activation_request_assembled','source_roster_is_execution_allowlist',
    'actual_inputs_accessed','dependency_activation_performed','execution_authorized',
    'feature_supported','recovery_proven','device_write_gate_passed')
REPLACEMENTS = frozenset(('outer_child','outer_entry','outer_gate','outer_contract','successor_entry'))
FIELDS = frozenset(('schema','purpose','source_inventory','host_source','ordinary_input_roles',
    'historical_input_disposition','protected_input_roles','metadata_basis_roles','scope',
    'owner_facts','rights_uncertainties','historical_blockers','historical_evidence_unchanged',
    'unimplemented_bindings','camera_commands')+FLAGS)


def require(ok, code):
    if not ok:
        raise ValueError(code)


def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def source_row(row, disposition):
    require(type(row) is dict and set(row)=={'path','bytes','sha256','disposition'},'source_shape')
    require(type(row['path']) is str and len(row['path'])<=1024 and
        not any(c in row['path'] for c in ('\\',':')) and
        all(ord(c)>=32 for c in row['path']),'source_path')
    path=PurePosixPath(row['path'])
    require(not path.is_absolute() and '..' not in path.parts and path.suffix=='.py'
        and str(path)==row['path'] and path.parts[0] in ('tools','private'),'source_path')
    require(type(row['bytes']) is int and 0<row['bytes']<=2*1024**2,'source_bytes')
    require(type(row['sha256']) is str and len(row['sha256'])==64 and
        all(c in '0123456789abcdef' for c in row['sha256']),'source_digest')
    require(row['disposition']==disposition,'source_disposition')


def validate_review_packet(value):
    """Return review identity only. This API cannot return execution readiness."""
    require(type(value) is dict and set(value)==FIELDS,'review_shape')
    require(value['schema']=='source_only_operational_scope_v1' and
        value['purpose']=='non_executable_adapter_migration_review','review_mode')
    require(all(value[n] is False for n in FLAGS) and value['camera_commands']==[], 'review_authority')
    inventory=value['source_inventory']
    require(type(inventory) is dict and set(inventory)==SOURCE_ROLES,'source_roster')
    paths=set()
    for role,row in list(inventory.items())+[('host_parent_adapter',value['host_source'])]:
        source_row(row,'requires_successor' if role in REPLACEMENTS or role=='host_parent_adapter' else 'retain_contract_rebind_sources')
        require(row['path'].casefold() not in paths,'source_path_alias');paths.add(row['path'].casefold())
    require(type(value['ordinary_input_roles']) is list and
        value['ordinary_input_roles']==sorted(ORDINARY_INPUTS),'input_roster')
    require(value['protected_input_roles']==['firmware_package','operational_constants'],'protected_roster')
    require(value['metadata_basis_roles']==list(BASIS_ROLES),'basis_roster')
    require(encoded(value['scope'])==encoded(SCOPE),'scope_change')
    require(encoded(value['owner_facts'])==encoded(OWNER),'owner_change')
    require(value['rights_uncertainties']==sorted(RIGHTS),'rights_change')
    require(value['historical_blockers']==list(HISTORY) and value['historical_evidence_unchanged'] is True,'historical_change')
    dispositions=value['historical_input_disposition']
    require(type(dispositions) is dict and set(dispositions)==LEGACY_INPUTS,'legacy_roster')
    for role,status in dispositions.items():
        expected=('fresh_current_metadata' if role in {'basis','source_manifest','prerequisites','binding_plan','role_authority','binding_schema'}
            else 'new_activity_specific_record' if role in {'activity_scope','activity_rights'}
            else 'replace_semantics' if role in {'dependency_config','source_cache','source_receipts'}
            else 'historical_index_only')
        require(status==expected,'legacy_disposition')
    require(type(value['unimplemented_bindings']) is list and value['unimplemented_bindings']==[
        'new_authority_input_grammar','operational_host_child_source_binding',
        'internal_runtime_observer_continuation','saved_runtime_parent_reconciliation',
        'independent_activity_specific_decision_and_external_anchor'],'remaining_bindings')
    return dict(schema='operational_scope_review_identity_v1',status='non_executable_review_only',
        sha256=hashlib.sha256(encoded(value)).hexdigest(),child_comparison_sources=43,
        host_comparison_sources=1,execution_authorized=False,camera_commands=[])


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')


def main():
    return 2
