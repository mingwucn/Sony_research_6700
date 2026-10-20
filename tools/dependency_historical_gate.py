"""Versioned historical-context preflight; authored-source successor, no activation.

Derived from the pinned comparison validator; original v5 API remains comparison-only.
The v6 entry separates historical cached records from the current proposed act.
"""
import base64
import hashlib
import json
import math
from pathlib import Path
MIB = 1024 ** 2
PURPOSE = 'one_private_two_phase_primary_gdt_metadata_observation'
INPUTS = frozenset(('basis', 'source_manifest', 'prerequisites', 'binding_plan', 'dependency_config', 'source_cache', 'source_receipts', 'role_authority', 'binding_schema', 'historical_scope', 'historical_rights', 'activity_scope', 'activity_rights', 'q_old_result', 'q_old_seal', 'q_old_review', 'q_integration_result', 'q_integration_review', 'q_snapshot_result', 'q_snapshot_log', 'q_outer_result', 'q_outer_review', 'repair_overlay', 'q_repair_result', 'q_repair_review', 'factory_evidence', 'parent_evidence'))
BASIS_ROLES = frozenset(('prior_stream', 'prior_prefix', 'prior_directory', 'prior_member_identification', 'prior_selection', 'prior_measured', 'prior_accepted_inventory', 'lead_plan', 'prior_ext_superblock_observation'))
UNCERTAINTIES = frozenset(('accepted_contract_interaction', 'accompanying_component_terms', 'constants_provenance', 'narrow_research_hypothesis_scope', 'distinct_operational_act_decision'))
OWNER = {'country': 'China', 'personal': True, 'noncommercial': True, 'existing_inspection_rights': 'No / unknown', 'download_consent_alone_clears_inspection': False}
FLAGS = ['-I', '-S', '-B', '-X', 'utf8']
REFERENCE_ROLES = frozenset(('historical_scope', 'historical_rights', 'role_authority', 'binding_schema', 'q_old_result', 'q_old_seal', 'q_old_review', 'q_integration_result', 'q_integration_review', 'q_snapshot_result', 'q_snapshot_log', 'source_cache', 'source_receipts', 'basis', 'source_manifest', 'prerequisites', 'binding_plan', 'repair_overlay', 'q_repair_result', 'q_repair_review', 'factory_evidence', 'parent_evidence'))

class GateError(ValueError):

    def __init__(self, stage='contract'):
        self.stage = stage
        super().__init__('outer_v2_refused:' + stage)

def require(condition, stage='contract'):
    if not condition:
        raise GateError(stage)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def digest(value, length=64):
    require(type(value) is str and len(value) == length and all((c in '0123456789abcdef' for c in value)))
    return value

def closed(value, fields):
    require(type(value) is dict and set(value) == set(fields))
    return value

def relative(value):
    require(type(value) is str and 0 < len(value) <= 1024 and (':' not in value) and ('\\' not in value) and ('\x00' not in value) and (not value.startswith('/')) and all((part not in ('', '.', '..') for part in value.split('/'))))
    return value

def absolute(value):
    require(type(value) is str and 0 < len(value) <= 1024 and ('\x00' not in value))
    path = Path(value)
    require(path.is_absolute() and '..' not in path.parts and (str(path) == value))
    return path

def parse(raw):
    require(type(raw) is bytes and 0 < len(raw) <= 8 * MIB, 'document_bound')

    def pairs(items):
        answer = {}
        for key, value in items:
            require(key not in answer, 'duplicate_key')
            answer[key] = value
        return answer
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=lambda _: require(False, 'nonfinite'))
    except GateError:
        raise
    except Exception:
        raise GateError('json') from None
    count = [0]

    def walk(item, depth=0):
        count[0] += 1
        require(depth <= 32 and count[0] <= 500000, 'json_bound')
        kind = type(item)
        require(kind in (dict, list, str, int, float, bool, type(None)), 'json_type')
        if kind is dict:
            require(len(item) <= 8192 and all((type(k) is str and len(k) <= 2048 for k in item)))
            for nested in item.values():
                walk(nested, depth + 1)
        elif kind is list:
            require(len(item) <= 8192)
            for nested in item:
                walk(nested, depth + 1)
        elif kind is str:
            require(len(item) <= 4 * MIB, 'text_bound')
        elif kind is int:
            require(abs(item) <= 2 ** 128, 'integer_bound')
        elif kind is float:
            require(math.isfinite(item), 'nonfinite')
    walk(value)
    return value

def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def same(left, right):
    return encoded(left) == encoded(right)

def zero(value):
    return type(value) is int and value == 0

def _ref(row):
    closed(row, ('path', 'bytes', 'sha256'))
    relative(row['path'])
    digest(row['sha256'])
    require(type(row['bytes']) is int and 0 < row['bytes'] <= 8 * MIB)

def startup_shape(config, startup):
    closed(startup, ('implementation', 'version', 'platform', 'os_name', 'maxsize', 'isolated', 'no_site', 'dont_write_bytecode', 'optimize', 'executable', 'base_executable', 'prefix', 'base_prefix', 'path'))
    require(startup['implementation'] == 'cpython' and startup['platform'] == 'win32' and (startup['os_name'] == 'nt') and (type(startup['version']) is list) and all((type(v) is int for v in startup['version'])) and (startup['version'] == [3, 13, 12]) and (type(startup['maxsize']) is int) and (startup['maxsize'] == 2 ** 63 - 1) and (type(startup['isolated']) is int) and (startup['isolated'] == 1) and (type(startup['no_site']) is int) and (startup['no_site'] == 1) and (startup['dont_write_bytecode'] is True) and (type(startup['optimize']) is int) and (startup['optimize'] == 0), 'startup_profile')
    venv = absolute(config['package_root']).parents[2]
    base = absolute(config['trusted_origins']['platform']['path']).parents[1]
    for key, path in [('executable', venv / 'Scripts' / 'python.exe'), ('base_executable', base / 'python.exe'), ('prefix', base), ('base_prefix', base)]:
        require(str(absolute(startup[key])).casefold() == str(path).casefold(), 'startup_profile')
    require(type(startup['path']) is list and len(startup['path']) == 4, 'startup_profile')
    for name, path in zip(startup['path'], [base / 'python313.zip', base / 'DLLs', base / 'Lib', base]):
        require(str(absolute(name)).casefold() == str(path).casefold(), 'startup_profile')
REQUIRED_OUTER_TEST_IDS = ('factory_migration_cases.MigrationTests.test_changed_composed_role_source', 'factory_migration_cases.MigrationTests.test_changed_contract_factory_source', 'factory_migration_cases.MigrationTests.test_changed_controller_source', 'factory_migration_cases.MigrationTests.test_changed_runtime_source', 'factory_migration_cases.MigrationTests.test_changed_wiring_source', 'factory_migration_cases.MigrationTests.test_extra_proof_field', 'factory_migration_cases.MigrationTests.test_loader_rejects_changed_factory_before_any_module_executes', 'factory_migration_cases.MigrationTests.test_loader_requires_complete_integration_map_before_execution', 'factory_migration_cases.MigrationTests.test_missing_review', 'factory_migration_cases.MigrationTests.test_new_factory_identity_substitution', 'factory_migration_cases.MigrationTests.test_old_bundle_schema_refused', 'factory_migration_cases.MigrationTests.test_old_factory_lineage_substitution', 'factory_migration_cases.MigrationTests.test_operational_promotion', 'factory_migration_cases.MigrationTests.test_qualification_boolean_exit', 'factory_migration_cases.MigrationTests.test_qualification_case_swap', 'factory_migration_cases.MigrationTests.test_qualification_count_downgrade', 'factory_migration_cases.MigrationTests.test_qualification_unstable_sources', 'factory_migration_cases.MigrationTests.test_reviewed_successor_factory_has_distinct_shared_pin', 'outer_cases.BootstrapReaderTests.test_directory_refuses', 'outer_cases.BootstrapReaderTests.test_duplicate_bootstrap_json_key_refuses', 'outer_cases.BootstrapReaderTests.test_empty_file_refuses', 'outer_cases.BootstrapReaderTests.test_hardlink_refuses', 'outer_cases.BootstrapReaderTests.test_nonfinite_bootstrap_json_refuses', 'outer_cases.BootstrapReaderTests.test_oversized_file_refuses', 'outer_cases.BootstrapReaderTests.test_parent_traversal_refuses', 'outer_cases.BootstrapReaderTests.test_read_regular_invented_file', 'outer_cases.BootstrapReaderTests.test_relative_path_refuses', 'outer_cases.CachedModuleTests.test_compile_and_execute_only_supplied_invented_bytes', 'outer_cases.CachedModuleTests.test_compile_failure_removes_owned_alias', 'outer_cases.CachedModuleTests.test_execution_failure_removes_owned_alias', 'outer_cases.CachedModuleTests.test_occupied_alias_is_preserved', 'outer_cases.CompletionReceiptTests.test_boolean_native_sequence', 'outer_cases.CompletionReceiptTests.test_complete_invented_receipt_chain', 'outer_cases.CompletionReceiptTests.test_duplicate_native_intent', 'outer_cases.CompletionReceiptTests.test_duplicate_vector_case', 'outer_cases.CompletionReceiptTests.test_journal_claim_before_persistence', 'outer_cases.CompletionReceiptTests.test_journal_wrong_receipt_anchor', 'outer_cases.CompletionReceiptTests.test_missing_native_receipt', 'outer_cases.CompletionReceiptTests.test_native_aesni_claim_mismatch', 'outer_cases.CompletionReceiptTests.test_native_before_after_mismatch', 'outer_cases.CompletionReceiptTests.test_native_false_audit', 'outer_cases.CompletionReceiptTests.test_native_wrong_arguments', 'outer_cases.CompletionReceiptTests.test_native_wrong_audit_path', 'outer_cases.CompletionReceiptTests.test_source_not_closed', 'outer_cases.CompletionReceiptTests.test_source_wrong_operation', 'outer_cases.CompletionReceiptTests.test_substituted_python_origin', 'outer_cases.CompletionReceiptTests.test_substituted_trusted_origin', 'outer_cases.CompletionReceiptTests.test_unclosed_trusted_read', 'outer_cases.CompletionReceiptTests.test_wrong_native_sequence', 'outer_cases.CompletionReceiptTests.test_wrong_vector_branch', 'outer_cases.CompletionReceiptTests.test_wrong_vector_identifier', 'outer_cases.GateTests.test_context_contains_exact_gate_and_metadata_pins', 'outer_cases.GateTests.test_deep_json_refused', 'outer_cases.GateTests.test_duplicate_json_key', 'outer_cases.GateTests.test_matching_version_does_not_make_body_supported', 'outer_cases.GateTests.test_nonfinite_json_refused', 'outer_cases.GateTests.test_reject_changed_interpreter', 'outer_cases.GateTests.test_reject_constants_assignment_count_float', 'outer_cases.GateTests.test_reject_constants_read_as_source', 'outer_cases.GateTests.test_reject_download_misrepresented_as_inspection', 'outer_cases.GateTests.test_reject_extra_candidate_field', 'outer_cases.GateTests.test_reject_float_version', 'outer_cases.GateTests.test_reject_integer_not_boolean_owner_fact', 'outer_cases.GateTests.test_reject_integration_case_duplicate', 'outer_cases.GateTests.test_reject_integration_changed_source', 'outer_cases.GateTests.test_reject_missing_basis_role', 'outer_cases.GateTests.test_reject_new_bootstrap_unqualified', 'outer_cases.GateTests.test_reject_new_qualification_authorizes_actual', 'outer_cases.GateTests.test_reject_new_qualification_pending', 'outer_cases.GateTests.test_reject_no_site_false', 'outer_cases.GateTests.test_reject_old_case_count_changed', 'outer_cases.GateTests.test_reject_old_case_count_float', 'outer_cases.GateTests.test_reject_old_exit_false_not_zero', 'outer_cases.GateTests.test_reject_old_schema', 'outer_cases.GateTests.test_reject_old_session_reused', 'outer_cases.GateTests.test_reject_old_site_enabled_argv', 'outer_cases.GateTests.test_reject_old_summary_failed', 'outer_cases.GateTests.test_reject_owner_rights_changed', 'outer_cases.GateTests.test_reject_pending_activity', 'outer_cases.GateTests.test_reject_reviewer_same_as_author', 'outer_cases.GateTests.test_reject_snapshot_failed_exit', 'outer_cases.GateTests.test_reject_snapshot_failure_log', 'outer_cases.GateTests.test_reject_source_cache_hash_mismatch', 'outer_cases.GateTests.test_reject_source_receipt_boolean_count', 'outer_cases.GateTests.test_reject_source_receipt_cross_identity', 'outer_cases.GateTests.test_reject_source_receipt_unclosed', 'outer_cases.GateTests.test_reject_source_roster_missing_role', 'outer_cases.GateTests.test_reject_true_is_not_integer_version', 'outer_cases.GateTests.test_reject_unreviewed_import_path', 'outer_cases.GateTests.test_reject_wrong_basis_source', 'outer_cases.GateTests.test_reject_wrong_operation', 'outer_cases.GateTests.test_retained_rights_uncertainties_cannot_disappear', 'outer_cases.GateTests.test_tampered_bound_input', 'outer_cases.GateTests.test_valid_complete_invented_chain_and_no_hash_cycle', 'outer_cases.GateTests.test_validation_has_no_file_or_source_execution', 'outer_cases.GateTests.test_wrong_external_anchor', 'outer_cases.HostBoundaryTests.test_cli_bad_arguments_refuse_before_bootstrap', 'outer_cases.HostBoundaryTests.test_complete_requires_outer_reconciliation', 'outer_cases.HostBoundaryTests.test_narrow_success_cannot_hide_dependency_failure', 'outer_cases.HostBoundaryTests.test_source_publication_failure_closes_pre_controller_records_once', 'outer_cases.HostBoundaryTests.test_terminal_uncertainty_is_not_retried', 'outer_cases.InventedBootstrapTests.test_changed_helper_refuses_before_module_execution', 'outer_cases.InventedBootstrapTests.test_complete_invented_file_bootstrap', 'outer_cases.InventedBootstrapTests.test_missing_input_refuses', 'outer_cases.InventedBootstrapTests.test_resealed_noncanonical_final_input_opens_no_inputs', 'outer_cases.InventedBootstrapTests.test_resealed_wrong_archival_hash_opens_no_inputs', 'outer_cases.InventedBootstrapTests.test_wrong_external_anchor_reads_no_inputs', 'outer_cases.OrdinaryTests.test_failed_fsync_keeps_output_and_does_not_retry', 'outer_cases.OrdinaryTests.test_hardlink_refuses', 'outer_cases.OrdinaryTests.test_hash_change_refuses_after_one_close', 'outer_cases.OrdinaryTests.test_json_write_readback_and_collision_preserve_original', 'outer_cases.OwnershipTests.test_failure_after_controller_does_not_close_again', 'outer_cases.OwnershipTests.test_failure_before_controller_closes_once', 'outer_cases.OwnershipTests.test_second_controller_attempt_refuses', 'outer_cases.OwnershipTests.test_success_does_not_close_controller_owned_records_again', 'outer_cases.OwnershipTests.test_success_without_controller_refuses', 'outer_cases.OwnershipTests.test_uncertain_close_never_retried', 'outer_cases.OwnershipTests.test_wrong_callback_code_cannot_succeed', 'outer_cases.ReferencePolicyTests.test_extra_policy_key_refuses', 'outer_cases.ReferencePolicyTests.test_frozen_reference_policy_accepts_original', 'outer_cases.ReferencePolicyTests.test_missing_policy_refuses', 'outer_cases.ReferencePolicyTests.test_missing_reference_policy_argument_has_no_fallback', 'outer_cases.ReferencePolicyTests.test_native_profile_substitution_refuses_after_resealing', 'outer_cases.ReferencePolicyTests.test_new_operation_is_only_dependency_profile_normalization', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_basis', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_binding_plan', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_binding_schema', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_factory_evidence', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_historical_rights', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_historical_scope', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_parent_evidence', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_prerequisites', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_integration_result', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_integration_review', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_old_result', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_old_review', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_old_seal', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_repair_result', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_repair_review', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_snapshot_log', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_snapshot_result', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_repair_overlay', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_role_authority', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_source_cache', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_source_manifest', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_source_receipts', 'outer_cases.ReferencePolicyTests.test_vector_profile_substitution_refuses_after_resealing', 'overlay_cases.OverlayTests.test_gate_returns_one_effective_map', 'overlay_cases.OverlayTests.test_gate_to_real_loader_passes_same_effective_map', 'overlay_cases.OverlayTests.test_loader_refuses_authority_promotion', 'overlay_cases.OverlayTests.test_loader_refuses_changed_graph_beyond_orders', 'overlay_cases.OverlayTests.test_loader_refuses_changed_role_graph', 'overlay_cases.OverlayTests.test_loader_refuses_missing_blocker', 'overlay_cases.OverlayTests.test_nested_path_cannot_fall_back_to_historical_basename', 'overlay_cases.OverlayTests.test_nested_traversal_is_not_a_historical_key', 'overlay_cases.OverlayTests.test_nested_unchanged_sources_use_full_historical_keys', 'overlay_cases.OverlayTests.test_new_hash_substitution', 'overlay_cases.OverlayTests.test_operational_review_claim_refused', 'overlay_cases.OverlayTests.test_overlay_does_not_authorize_execution', 'overlay_cases.OverlayTests.test_overlay_path_substitution', 'overlay_cases.OverlayTests.test_prior_hash_substitution', 'overlay_cases.OverlayTests.test_qualification_schema_does_not_alias_v2_bundle', 'overlay_cases.OverlayTests.test_repair_case_swap', 'overlay_cases.OverlayTests.test_repair_count_downgrade', 'overlay_cases.OverlayTests.test_repair_overlay_extra', 'overlay_cases.OverlayTests.test_repair_overlay_missing', 'overlay_cases.OverlayTests.test_repair_review_roster_missing', 'overlay_cases.OverlayTests.test_repair_scope_pin_swap', 'overlay_cases.OverlayTests.test_stale_repair_result_review_binding', 'overlay_cases.OverlayTests.test_unchanged_source_cannot_be_added_to_overlay', 'parent_evidence_cases.ParentEvidenceTests.test_boolean_exit', 'parent_evidence_cases.ParentEvidenceTests.test_bootstrap_promotion', 'parent_evidence_cases.ParentEvidenceTests.test_camera_command', 'parent_evidence_cases.ParentEvidenceTests.test_changed_raw_log_hash', 'parent_evidence_cases.ParentEvidenceTests.test_changed_raw_result_hash', 'parent_evidence_cases.ParentEvidenceTests.test_changed_review', 'parent_evidence_cases.ParentEvidenceTests.test_changed_source', 'parent_evidence_cases.ParentEvidenceTests.test_complete_evidence_preserves_historical_identity_and_false_flags', 'parent_evidence_cases.ParentEvidenceTests.test_count_downgrade', 'parent_evidence_cases.ParentEvidenceTests.test_duplicate_case', 'parent_evidence_cases.ParentEvidenceTests.test_execution_promotion', 'parent_evidence_cases.ParentEvidenceTests.test_extra_evidence_field', 'parent_evidence_cases.ParentEvidenceTests.test_extra_source', 'parent_evidence_cases.ParentEvidenceTests.test_float_exit', 'parent_evidence_cases.ParentEvidenceTests.test_missing_evidence_field', 'parent_evidence_cases.ParentEvidenceTests.test_missing_review', 'parent_evidence_cases.ParentEvidenceTests.test_missing_source', 'parent_evidence_cases.ParentEvidenceTests.test_noninjected_promotion', 'parent_evidence_cases.ParentEvidenceTests.test_old_v4_candidate_refused', 'parent_evidence_cases.ParentEvidenceTests.test_operational_promotion', 'parent_evidence_cases.ParentEvidenceTests.test_predecessor_identity_cannot_be_relabelled_current', 'parent_evidence_cases.ParentEvidenceTests.test_reference_policy_promotion', 'parent_evidence_cases.ParentEvidenceTests.test_same_count_case_swap', 'parent_evidence_cases.ParentEvidenceTests.test_unstable_sources', 'repair_cases.DependencyReceiptTests.test_legacy_no_LF_config_refused', 'repair_cases.DependencyReceiptTests.test_producer_hashes_accepted_by_consumer', 'repair_cases.DependencyReceiptTests.test_tampered_dependency_hash_refused', 'repair_cases.DescriptorOnlyTests.test_actual_gate_slice_accepts_descriptor_only_result', 'repair_cases.DescriptorOnlyTests.test_actual_gate_slice_refuses_root_proposal', 'repair_cases.DescriptorOnlyTests.test_descriptor_pass_has_no_root_proposal', 'repair_cases.DescriptorOnlyTests.test_invalid_descriptor_still_refuses', 'repair_cases.DescriptorOnlyTests.test_no_root_offset_calculation_in_planner_AST', 'repair_cases.DescriptorOnlyTests.test_outside_group_descriptor_refuses', 'repair_cases.DescriptorOnlyTests.test_phase_A_still_only_proposes_GDT', 'repair_cases.EncodingTests.test_dependency_nonfinite_refused', 'repair_cases.EncodingTests.test_emitted_bytes_pass_real_reconcile_wire_boundary', 'repair_cases.EncodingTests.test_legacy_spaced_stdout_fails_real_reconcile_wire_boundary', 'repair_cases.EncodingTests.test_producer_dependency_contract_ascii', 'repair_cases.EncodingTests.test_producer_dependency_contract_unicode', 'repair_cases.EncodingTests.test_stdout_exact_inherited_wire_contract', 'repair_cases.EncodingTests.test_stdout_flush_failure_refuses', 'repair_cases.EncodingTests.test_stdout_short_write_refuses', 'repair_cases.EncodingTests.test_successful_child_main_uses_binary_wire', 'repair_cases.OwnershipRepairTests.test_false_close_cannot_succeed', 'repair_cases.OwnershipRepairTests.test_inherited_success_close_once', 'repair_cases.OwnershipRepairTests.test_keyboard_interrupt_after_inherited_close_no_retry', 'repair_cases.OwnershipRepairTests.test_keyboard_interrupt_closes_once', 'repair_cases.OwnershipRepairTests.test_system_exit_closes_once', 'repair_cases.OwnershipRepairTests.test_uncertain_close_after_system_exit_no_retry', 'repair_cases.ParentInterruptionTests.test_before_kill_journal_failure_cannot_consume_kill', 'repair_cases.ParentInterruptionTests.test_keyboard_interrupt_kills_reaps_closes_once', 'repair_cases.ParentInterruptionTests.test_kill_interruption_still_waits_without_retry', 'repair_cases.ParentInterruptionTests.test_outer_parent_false_close_cannot_succeed', 'repair_cases.ParentInterruptionTests.test_outer_parent_interrupt_closes_owned_records', 'repair_cases.ParentInterruptionTests.test_sleep_interruption_terminates_once', 'repair_cases.ParentInterruptionTests.test_system_exit_kills_reaps_closes_once', 'repair_cases.ParentInterruptionTests.test_wait_interruption_stays_unknown_without_retry', 'repair_cases.QualificationPolicyTests.test_changed_fixture_pin_refused', 'repair_cases.QualificationPolicyTests.test_count_downgrade_refused_after_resealing', 'repair_cases.QualificationPolicyTests.test_extra_qualification_source_refused', 'repair_cases.QualificationPolicyTests.test_missing_fixture_pin_refused', 'repair_cases.QualificationPolicyTests.test_same_count_case_substitution_refused')
REQUIRED_OUTER_SOURCE_PINS = {'outer_fixtures.py': 'fd1c6e34c706a58dcc4bbabdd6afe9e6f47f0580be4d202ad2a182572e7e303c', 'test_outer_v2.py': '3a63ead3e8b68688e47a7c7cf5f1a8587d0a1af156f46c82643b6bcebafea2d1', 'scope.md': '72881d5cf695bed07315517b3d08c594f90b7914a7e6cfff10423534c347ff9f', 'qualify_review.py': 'ad7de2f895428ff6128d7141f79cebccd94e861b0f8d51d50a7755d548b90392', 'test_review_fixes.py': 'a4aa522ccf7240fcade49ab41a2055077f4910085f37ca112b62e932779e7d74', 'test_source_overlay.py': '2aeb17f5e9f1ffea85fd3cce069dd5536078c8560be2f46fc386118bab0bdd3c', 'activation/gdt_gate.py': '917c88b52b954d25920b44c83ae397ca1debe36491c19d0e3e0149458010b65c', 'activation/ext_read_planner.py': '7ea688107813156e4bdd43a78d0b8f88e9bd8279fcd81885b7bc39f7e0cf886b', 'activation/io_entry.py': '70a2ed3a0265894adace48e5285c0eb8962c666975f7df1a8e4f6141b918bb43', 'integration/runtime_entry.py': '4a64bd6c63ff6e43b56ab7298e5fb84a6304e3576990eaa4aa020c551aeba8f1', 'test_factory_migration.py': '9dfdb2f102fa3dc158da903f4b3e33b8f5b6155c6de7d01bd8a47f8124dccc43', 'integration/prospective_child.py': '3cd438eb42db7d64c18752fab3580b47915de8ccd2d95efc431fd67fe3b0e08c', 'outer/test_parent_evidence.py': 'd495dfdb039d4b7ed8f59199c87320f9c3ce87948e8fe21484a3b6ed549032db', 'lab.py': 'd65ab782a7e56bf485f0835b8feaf47f5a69a43152d345558ae836b6603b0777', 'test_bootstrap.py': 'a83bedde3980a62c3c41bdb91b6abf1aebb16d8f130e08695c9c87e9a8ec2818', 'test_parent_child.py': 'a39446c53da910a9b62688c50889509af15f73db27b664ce56057da41173f717', 'successor_runner.py': '0bdac6386fc9a586ee8c4cf07fab0f84e0161b5f80e937c93dad89ccfdf201ac', 'qualify_successor.py': '7eb7cae4f320116d41a7ec00d91eecb6fa6668c381413dc282c945dd293d7274', 'parent-evidence.json': '8b9dc7a70894802799a66cc747cd171ddaf9f0e565c04cb2cc0a3e9ad7975b24'}
REQUIRED_OUTER_SOURCE_NAMES = frozenset(('activation/ext_read_planner.py', 'activation/gdt_gate.py', 'activation/io_entry.py', 'entry_v2.py', 'integration/prospective_child.py', 'integration/runtime_entry.py', 'lab.py', 'ordinary_io.py', 'outer/test_parent_evidence.py', 'outer_fixtures.py', 'outer_gate.py', 'parent-evidence.json', 'qualify_review.py', 'qualify_successor.py', 'scope.md', 'successor_runner.py', 'test_bootstrap.py', 'test_factory_migration.py', 'test_outer_v2.py', 'test_parent_child.py', 'test_review_fixes.py', 'test_source_overlay.py'))
PARENT_EVIDENCE_POLICY = {'schema': 'gdt_parent_composition_evidence_v1', 'tested_entry_sha256': 'd6100e5fbd3374e5da07c44881bda41288f0bbff170be6ca30f576fbcb4b5a83', 'test_ids': ['__main__.ParentChildTests.test_changed_integration_source_refused_before_loader', '__main__.ParentChildTests.test_malformed_stdout_refuses_parent_reconciliation', '__main__.ParentChildTests.test_missing_outer_receipt_dominates_narrow_child_success', '__main__.ParentChildTests.test_real_child_complete_narrow_parent_success_outer_refuses_injection', '__main__.ParentChildTests.test_real_child_deadline_accelerated_test_clock', '__main__.ParentChildTests.test_real_child_second_phase_failure_no_retry', '__main__.ParentChildTests.test_source_mutation_before_child_is_not_retried'], 'source_sha256': {'activation/activation_binding.py': '22558080636f15300590c22b9987216216f650b4edc58d7df89092643722de74', 'activation/activation_gate.py': '21505f2583de8f5d26f7ccd959903ec964ed39b21ea6df1e400e8bc11b66750b', 'activation/activation_reference/artifact_probe.py': '54fbda68197b54547793b72aae1afececb92422dc3f29362c6515f8f86384071', 'activation/activation_reference/fdat_header.py': '6d78dc186355919d5457d8cb01b765422d24aca354519f1a76a1554368cdf117', 'activation/activation_reference/offline_inventory.py': '3bd0a8eddb4cc9f3aa9589bf625f6ad14daace386180a97332385f7fbd8fa3c7', 'activation/ext_gate.py': 'df2fbdeb9ab44d2cee23d41a7e4da9e63dcef7139194edb848b43b321109976d', 'activation/ext_preflight.py': 'e6106e6c72b6aee7d16c4db67e03803d22b5108199f644641b539721daa36775', 'activation/ext_read_planner.py': '7ea688107813156e4bdd43a78d0b8f88e9bd8279fcd81885b7bc39f7e0cf886b', 'activation/ext_superblock.py': 'b838b2fe8f4f3af18ddd4d8f3609acbe51e1aa992343615c84ec8119879750f5', 'activation/gdt_adapter.py': '531dd53fa5bd60cefcb99976b6914ecf5a7b45e592975b3121cba463c533a95d', 'activation/gdt_cleanup.py': 'c85bc84c055874e6fc06f338d5856c1a5d78ee373a7bf9a097f8ff7f0906397e', 'activation/gdt_gate.py': '917c88b52b954d25920b44c83ae397ca1debe36491c19d0e3e0149458010b65c', 'activation/gdt_preflight.py': '9f984f8c26437e2000492c4014372334e506ea67bdd6f3cf93ffebff69cf4368', 'activation/gdt_runner.py': '73c03899e3a44a1ce586ef32d2e620275bc1bede3643a55824e6d20fab89bafa', 'activation/inherited/acceptance.py': 'e2ee49ee8a419946947ce266a1959d4206b3cb99a3ad6d7ee4f9152a1ec901da', 'activation/inherited/classifier.py': '662036ae5966319621fc359191b59784c6b411777aece1034c21db95601c758a', 'activation/inherited/expanded_gate.py': 'bc598272b37b46e1230db286e5c4494de088f299b139301a89a99f8554490687', 'activation/inherited/fdat_stream.py': 'c1f7072c975c94044b43a1ffa31b1c7acb01008e9078b1841867b85e7c2523a1', 'activation/inherited/header_candidates.py': '522bf2d978454240e6e4c72994f9ef46fc44e47ea93711964d8432406c7ad507', 'activation/inherited/link_acceptance.py': '56ee869b40b59900bfb0452653175895ed7be1d1e97f1db6579db008ff4ad8d1', 'activation/inherited/member_acceptance.py': 'e1e717554d21546fb4a2c0aede8473ff0debc8b4b9680210b3dc2e900c408809', 'activation/inherited/member_prefix.py': '6e4b3ff43815a1b89150ff0b2abd4a8d9c579abc69ed32f9f89cd4d648fce431', 'activation/inherited/metadata_preflight.py': 'b92b8064bc234ed138bc084040d0206ba879219edc8f4efa15431847cc16fa32', 'activation/inherited/metadata_tar.py': 'f2494afc74384bfe34d52bc2fd892464c8669eac86cbddb47a9c588f6cc429cb', 'activation/inherited/prefix.py': 'e385fa70dd9fe91513b756d4256f38efc450acd1244f0114bc9c97983a1dd623', 'activation/inherited/tar_inventory.py': 'edb92477ab6ca4b164ff9964644a201b8711f4f76aa88361baf7bfe3261c8ed6', 'activation/io_adapter.py': '6dc64ce25a4c43185e5b2660fc802e314a6451908dba369beffd54ce4d097f81', 'activation/io_entry.py': '70a2ed3a0265894adace48e5285c0eb8962c666975f7df1a8e4f6141b918bb43', 'activation/reference_source/fdat_trial.py': '57e8b894e9ec1293b9780d1dfa0a64fde1c7a634b03b1dca4251b2427e55fa7c', 'baseline.json': 'cc1c758897a502f078b54f0491548261441bf5f31c9284a3830c2cee6ea651cb', 'dependency_fixture.py': 'd7732516339507308da931ce0cacd299fcea205da06e3b9e025c182aa439fa9d', 'factory-evidence.json': '9c1162d0279d3f85b13321e94527682ce684c993c2192519babab1ad286aca40', 'integration/gdt_wiring.py': 'c1117307de2c6a0230b0bf848472dce30eaa766535cf498d4b945becbdb07d85', 'integration/prospective_child.py': '3cd438eb42db7d64c18752fab3580b47915de8ccd2d95efc431fd67fe3b0e08c', 'integration/runtime_entry.py': '4a64bd6c63ff6e43b56ab7298e5fb84a6304e3576990eaa4aa020c551aeba8f1', 'invented-v2/aliases.json': '46be4bee4bdb959a9669b4eec4f645eb56c570cad54331531ee6dc301dda89cb', 'invented-v2/basis.json': '2c89e2958a68b3bf937427494279663e3691f9e7a45a3e217c041b5e620fb167', 'invented-v2/plan.json': '78ff5a2e7226d06c1dd51c6d7f4687cae9468f6f482ef456674ad1824633c7c1', 'invented-v2/roles.json': 'b984d6eb3eeca85b5eb9c485d0e15961cf353ca02065e3de99111f25ba883383', 'invented-v2/stream.bin': 'b3ff4fd1ebb621f4c2be4b104e11b395ea315f1fbf580dd6b403bb2a091de541', 'lab.py': '3275c1171f6f7eb572c4694e9461aee490de7075739b95c706144e728a092b91', 'outer/entry_v2.py': 'd6100e5fbd3374e5da07c44881bda41288f0bbff170be6ca30f576fbcb4b5a83', 'outer/ordinary_io.py': '9ff5c852603d7cc115d53fc1296d21892dafa460400e08698440c1367205231d', 'outer/outer_fixtures.py': '0404c49b1b887248108189915119c11536c6cadc82a9a19d52b7c17ea46b7d43', 'outer/outer_gate.py': '499a9b85761b6d4ad24b0dfa55011613b54020fd6adfa295d40d741ec4759559', 'outer/qualify_002.py': '507f4d6f139af900154417d88bbe9ee454e3f155094cd4626533cd5dcb58b74b', 'outer/qualify_review.py': 'ad7de2f895428ff6128d7141f79cebccd94e861b0f8d51d50a7755d548b90392', 'outer/scope.md': '72881d5cf695bed07315517b3d08c594f90b7914a7e6cfff10423534c347ff9f', 'outer/test_factory_migration.py': '9dfdb2f102fa3dc158da903f4b3e33b8f5b6155c6de7d01bd8a47f8124dccc43', 'outer/test_outer_v2.py': 'eb83f69299a6009904f1d4812cce67bf99efa2af6a97169010a898aa33b0e5c2', 'outer/test_review_fixes.py': 'a4aa522ccf7240fcade49ab41a2055077f4910085f37ca112b62e932779e7d74', 'outer/test_source_overlay.py': '1148dedf4e35ad25b23288e6b7d3e909f5ca5709251eab3e64eadc605ec3ada4', 'qualify.py': 'ae29a28f064987b6dc50738727b383e360694b2f052a4cdca01ee2e2b38c0dba', 'roles/acceptance.py': 'e2ee49ee8a419946947ce266a1959d4206b3cb99a3ad6d7ee4f9152a1ec901da', 'roles/artifact_probe.py': '54fbda68197b54547793b72aae1afececb92422dc3f29362c6515f8f86384071', 'roles/capture.py': '57e8b894e9ec1293b9780d1dfa0a64fde1c7a634b03b1dca4251b2427e55fa7c', 'roles/classifier.py': '662036ae5966319621fc359191b59784c6b411777aece1034c21db95601c758a', 'roles/core.py': 'c1f7072c975c94044b43a1ffa31b1c7acb01008e9078b1841867b85e7c2523a1', 'roles/expanded_gate.py': 'bc598272b37b46e1230db286e5c4494de088f299b139301a89a99f8554490687', 'roles/ext_gate.py': 'df2fbdeb9ab44d2cee23d41a7e4da9e63dcef7139194edb848b43b321109976d', 'roles/ext_preflight.py': 'e6106e6c72b6aee7d16c4db67e03803d22b5108199f644641b539721daa36775', 'roles/ext_read_planner.py': '7ea688107813156e4bdd43a78d0b8f88e9bd8279fcd81885b7bc39f7e0cf886b', 'roles/ext_superblock.py': 'b838b2fe8f4f3af18ddd4d8f3609acbe51e1aa992343615c84ec8119879750f5', 'roles/gdt_adapter.py': '531dd53fa5bd60cefcb99976b6914ecf5a7b45e592975b3121cba463c533a95d', 'roles/gdt_cleanup.py': 'c85bc84c055874e6fc06f338d5856c1a5d78ee373a7bf9a097f8ff7f0906397e', 'roles/gdt_gate.py': '917c88b52b954d25920b44c83ae397ca1debe36491c19d0e3e0149458010b65c', 'roles/gdt_preflight.py': '9f984f8c26437e2000492c4014372334e506ea67bdd6f3cf93ffebff69cf4368', 'roles/gdt_runner.py': '73c03899e3a44a1ce586ef32d2e620275bc1bede3643a55824e6d20fab89bafa', 'roles/header_candidates.py': '522bf2d978454240e6e4c72994f9ef46fc44e47ea93711964d8432406c7ad507', 'roles/io_adapter.py': '6dc64ce25a4c43185e5b2660fc802e314a6451908dba369beffd54ce4d097f81', 'roles/link_acceptance.py': '56ee869b40b59900bfb0452653175895ed7be1d1e97f1db6579db008ff4ad8d1', 'roles/member_acceptance.py': 'e1e717554d21546fb4a2c0aede8473ff0debc8b4b9680210b3dc2e900c408809', 'roles/member_prefix.py': '6e4b3ff43815a1b89150ff0b2abd4a8d9c579abc69ed32f9f89cd4d648fce431', 'roles/metadata_preflight.py': 'b92b8064bc234ed138bc084040d0206ba879219edc8f4efa15431847cc16fa32', 'roles/metadata_tar.py': 'f2494afc74384bfe34d52bc2fd892464c8669eac86cbddb47a9c588f6cc429cb', 'roles/offline_inventory.py': '3bd0a8eddb4cc9f3aa9589bf625f6ad14daace386180a97332385f7fbd8fa3c7', 'roles/prefix.py': 'e385fa70dd9fe91513b756d4256f38efc450acd1244f0114bc9c97983a1dd623', 'roles/tar_inventory.py': 'edb92477ab6ca4b164ff9964644a201b8711f4f76aa88361baf7bfe3261c8ed6', 'roles/validator.py': '6d78dc186355919d5457d8cb01b765422d24aca354519f1a76a1554368cdf117', 'runtime_entry.py': '4a64bd6c63ff6e43b56ab7298e5fb84a6304e3576990eaa4aa020c551aeba8f1', 'test_parent_child.py': 'a39446c53da910a9b62688c50889509af15f73db27b664ce56057da41173f717'}, 'result_sha256': '0f9393137b88e3078ca8db531bd256fd6e9f501c158f0422a6b4ca617fbc331a', 'stderr_sha256': '1aa63516c631377aea8067d18904b3bb702060a262b1fef60d9b074b46593e1b', 'review_artifact_sha256': {'runtime-rereview.json': '659b07a72e25a22f8b9e25c5f1b38bd3d292b2dcc8e156bfc8775a6005cda77b', 'io-review.json': 'db8014f4a49966f759bdde2fd572538440ebdd29bbac3a06db272d44b8f4553e'}, 'tests_run': 7, 'passed': 7, 'failed': 0, 'errors': 0, 'skipped': 0, 'child_exit_code': 0, 'sources_stable': True, 'positive_reference_policy': 'invented_test_override', 'production_bootstrap_qualified': False, 'noninjected_dependency_qualified': False, 'operational_acceptance': False, 'execution_authorized': False, 'camera_commands': []}

def parent_evidence(p):
    """Historical invented qualification only; exact closed content grants no act."""
    value = closed(p['parent_evidence'], tuple(PARENT_EVIDENCE_POLICY))
    require(same(value, PARENT_EVIDENCE_POLICY), 'parent_evidence')
    require(all((type(value[k]) is int for k in ('tests_run', 'passed', 'failed', 'errors', 'skipped', 'child_exit_code'))), 'parent_evidence')
    require(type(value['test_ids']) is list and len(value['test_ids']) == len(set(value['test_ids'])) == 7, 'parent_evidence')
    return value

def _qualifications(p, raw):
    old, seal, review = (p[k] for k in ('q_old_result', 'q_old_seal', 'q_old_review'))
    require(old['status'] == 'qualified_invented_activation_preparation_only' and type(old['passed']) is int and (type(old['tests_run']) is int) and (old['passed'] == old['tests_run'] == 811) and zero(old['child_exit_code']) and zero(old['skipped']) and (old['sources_stable'] is True) and (old['timed_out'] is False), 'old_qualification')
    ids = old['summary']['test_ids']
    require(old['summary']['was_successful'] is True and all((zero(old['summary'][key]) for key in ('failures', 'errors', 'skipped', 'expected_failures', 'unexpected_successes'))), 'old_qualification')
    require(len(ids) == len(set(ids)) == 811 and ids == seal['test_ids'], 'old_qualification')
    require(old['sources_sha256'] == seal['sources_sha256'] == review['sources_sha256'] and len(old['sources_sha256']) == 95 and (review['status'] == 'passed') and (review['tests_result_sha256'] == sha(raw['q_old_result'])) and (review['qualification_seal_sha256'] == sha(raw['q_old_seal'])), 'old_qualification')
    integration = p['q_integration_result']
    require(type(integration['passed']) is int and type(integration['tests_run']) is int and (integration['passed'] == integration['tests_run'] == 51) and zero(integration['skipped']) and zero(integration['child_exit_code']) and (integration['sources_and_predecessors_stable'] is True) and (integration['timed_out'] is False), 'integration_qualification')
    require(len(integration['test_ids']) == len(set(integration['test_ids'])) == len(integration['observed_pass_ids']) == 51 and set(integration['test_ids']) == set(integration['observed_pass_ids']) and (len(integration['source_sha256']) == 12), 'integration_qualification')
    reviewed = p['q_integration_review']
    require(reviewed['status'] == 'accepted_preparation_only_invented_core_composition_and_source_reviewed_factory' and reviewed['qualification_result_sha256'] == sha(raw['q_integration_result']) and (reviewed['qualified_source_sha256'] == integration['source_sha256']), 'integration_qualification')
    snapshot = p['q_snapshot_result']
    log = raw['q_snapshot_log']
    require(type(snapshot['exit_code']) is int and snapshot['exit_code'] == 0 and (snapshot['source_stable'] is True) and (snapshot['timed_out'] is False) and (snapshot['stderr_sha256'] == sha(log)), 'snapshot_qualification')
    lines = log.decode('utf-8').splitlines()
    passed = [line for line in lines if line.startswith('test_') and line.endswith(' ... ok')]
    require(len(passed) == len(set(passed)) == 20 and any((line.startswith('Ran 20 tests in ') for line in lines)) and (lines[-1] == 'OK'), 'snapshot_qualification')
    outer = p['q_outer_result']
    outer_review = p['q_outer_review']
    require(outer['status'] == 'qualified_invented_outer_gate_v5' and type(outer['tests_run']) is int and (outer['tests_run'] == len(REQUIRED_OUTER_TEST_IDS)) and (type(outer['passed']) is int) and (outer['passed'] == outer['tests_run']) and zero(outer['child_exit_code']) and zero(outer['skipped']) and (outer['timed_out'] is False) and (outer['sources_stable'] is True) and (outer['execution_authorized'] is False) and (outer['actual_entry_ready'] is False) and (len(outer['test_ids']) == len(set(outer['test_ids'])) == outer['tests_run']) and (set(outer['test_ids']) == set(REQUIRED_OUTER_TEST_IDS)) and (set(outer['source_sha256']) == REQUIRED_OUTER_SOURCE_NAMES) and all((outer['source_sha256'].get(k) == v for k, v in REQUIRED_OUTER_SOURCE_PINS.items())), 'outer_qualification')
    require(outer_review['status'] == 'reviewed_invented_outer_gate_v5' and outer_review['result_sha256'] == sha(raw['q_outer_result']) and (outer_review['source_sha256'] == outer['source_sha256']), 'outer_qualification')
REQUIRED_REPAIR_TEST_IDS = ('outer_cases.BootstrapReaderTests.test_directory_refuses', 'outer_cases.BootstrapReaderTests.test_duplicate_bootstrap_json_key_refuses', 'outer_cases.BootstrapReaderTests.test_empty_file_refuses', 'outer_cases.BootstrapReaderTests.test_hardlink_refuses', 'outer_cases.BootstrapReaderTests.test_nonfinite_bootstrap_json_refuses', 'outer_cases.BootstrapReaderTests.test_oversized_file_refuses', 'outer_cases.BootstrapReaderTests.test_parent_traversal_refuses', 'outer_cases.BootstrapReaderTests.test_read_regular_invented_file', 'outer_cases.BootstrapReaderTests.test_relative_path_refuses', 'outer_cases.CachedModuleTests.test_compile_and_execute_only_supplied_invented_bytes', 'outer_cases.CachedModuleTests.test_compile_failure_removes_owned_alias', 'outer_cases.CachedModuleTests.test_execution_failure_removes_owned_alias', 'outer_cases.CachedModuleTests.test_occupied_alias_is_preserved', 'outer_cases.CompletionReceiptTests.test_boolean_native_sequence', 'outer_cases.CompletionReceiptTests.test_complete_invented_receipt_chain', 'outer_cases.CompletionReceiptTests.test_duplicate_native_intent', 'outer_cases.CompletionReceiptTests.test_duplicate_vector_case', 'outer_cases.CompletionReceiptTests.test_journal_claim_before_persistence', 'outer_cases.CompletionReceiptTests.test_journal_wrong_receipt_anchor', 'outer_cases.CompletionReceiptTests.test_missing_native_receipt', 'outer_cases.CompletionReceiptTests.test_native_aesni_claim_mismatch', 'outer_cases.CompletionReceiptTests.test_native_before_after_mismatch', 'outer_cases.CompletionReceiptTests.test_native_false_audit', 'outer_cases.CompletionReceiptTests.test_native_wrong_arguments', 'outer_cases.CompletionReceiptTests.test_native_wrong_audit_path', 'outer_cases.CompletionReceiptTests.test_source_not_closed', 'outer_cases.CompletionReceiptTests.test_source_wrong_operation', 'outer_cases.CompletionReceiptTests.test_substituted_python_origin', 'outer_cases.CompletionReceiptTests.test_substituted_trusted_origin', 'outer_cases.CompletionReceiptTests.test_unclosed_trusted_read', 'outer_cases.CompletionReceiptTests.test_wrong_native_sequence', 'outer_cases.CompletionReceiptTests.test_wrong_vector_branch', 'outer_cases.CompletionReceiptTests.test_wrong_vector_identifier', 'outer_cases.GateTests.test_context_contains_exact_gate_and_metadata_pins', 'outer_cases.GateTests.test_deep_json_refused', 'outer_cases.GateTests.test_duplicate_json_key', 'outer_cases.GateTests.test_matching_version_does_not_make_body_supported', 'outer_cases.GateTests.test_nonfinite_json_refused', 'outer_cases.GateTests.test_reject_changed_interpreter', 'outer_cases.GateTests.test_reject_constants_assignment_count_float', 'outer_cases.GateTests.test_reject_constants_read_as_source', 'outer_cases.GateTests.test_reject_download_misrepresented_as_inspection', 'outer_cases.GateTests.test_reject_extra_candidate_field', 'outer_cases.GateTests.test_reject_float_version', 'outer_cases.GateTests.test_reject_integer_not_boolean_owner_fact', 'outer_cases.GateTests.test_reject_integration_case_duplicate', 'outer_cases.GateTests.test_reject_integration_changed_source', 'outer_cases.GateTests.test_reject_missing_basis_role', 'outer_cases.GateTests.test_reject_new_bootstrap_unqualified', 'outer_cases.GateTests.test_reject_new_qualification_authorizes_actual', 'outer_cases.GateTests.test_reject_new_qualification_pending', 'outer_cases.GateTests.test_reject_no_site_false', 'outer_cases.GateTests.test_reject_old_case_count_changed', 'outer_cases.GateTests.test_reject_old_case_count_float', 'outer_cases.GateTests.test_reject_old_exit_false_not_zero', 'outer_cases.GateTests.test_reject_old_schema', 'outer_cases.GateTests.test_reject_old_session_reused', 'outer_cases.GateTests.test_reject_old_site_enabled_argv', 'outer_cases.GateTests.test_reject_old_summary_failed', 'outer_cases.GateTests.test_reject_owner_rights_changed', 'outer_cases.GateTests.test_reject_pending_activity', 'outer_cases.GateTests.test_reject_reviewer_same_as_author', 'outer_cases.GateTests.test_reject_snapshot_failed_exit', 'outer_cases.GateTests.test_reject_snapshot_failure_log', 'outer_cases.GateTests.test_reject_source_cache_hash_mismatch', 'outer_cases.GateTests.test_reject_source_receipt_boolean_count', 'outer_cases.GateTests.test_reject_source_receipt_cross_identity', 'outer_cases.GateTests.test_reject_source_receipt_unclosed', 'outer_cases.GateTests.test_reject_source_roster_missing_role', 'outer_cases.GateTests.test_reject_true_is_not_integer_version', 'outer_cases.GateTests.test_reject_unreviewed_import_path', 'outer_cases.GateTests.test_reject_wrong_basis_source', 'outer_cases.GateTests.test_reject_wrong_operation', 'outer_cases.GateTests.test_retained_rights_uncertainties_cannot_disappear', 'outer_cases.GateTests.test_tampered_bound_input', 'outer_cases.GateTests.test_valid_complete_invented_chain_and_no_hash_cycle', 'outer_cases.GateTests.test_validation_has_no_file_or_source_execution', 'outer_cases.GateTests.test_wrong_external_anchor', 'outer_cases.HostBoundaryTests.test_cli_bad_arguments_refuse_before_bootstrap', 'outer_cases.HostBoundaryTests.test_complete_requires_outer_reconciliation', 'outer_cases.HostBoundaryTests.test_narrow_success_cannot_hide_dependency_failure', 'outer_cases.HostBoundaryTests.test_source_publication_failure_closes_pre_controller_records_once', 'outer_cases.HostBoundaryTests.test_terminal_uncertainty_is_not_retried', 'outer_cases.InventedBootstrapTests.test_changed_helper_refuses_before_module_execution', 'outer_cases.InventedBootstrapTests.test_complete_invented_file_bootstrap', 'outer_cases.InventedBootstrapTests.test_missing_input_refuses', 'outer_cases.InventedBootstrapTests.test_resealed_noncanonical_final_input_opens_no_inputs', 'outer_cases.InventedBootstrapTests.test_resealed_wrong_archival_hash_opens_no_inputs', 'outer_cases.InventedBootstrapTests.test_wrong_external_anchor_reads_no_inputs', 'outer_cases.OrdinaryTests.test_failed_fsync_keeps_output_and_does_not_retry', 'outer_cases.OrdinaryTests.test_hardlink_refuses', 'outer_cases.OrdinaryTests.test_hash_change_refuses_after_one_close', 'outer_cases.OrdinaryTests.test_json_write_readback_and_collision_preserve_original', 'outer_cases.OwnershipTests.test_failure_after_controller_does_not_close_again', 'outer_cases.OwnershipTests.test_failure_before_controller_closes_once', 'outer_cases.OwnershipTests.test_second_controller_attempt_refuses', 'outer_cases.OwnershipTests.test_success_does_not_close_controller_owned_records_again', 'outer_cases.OwnershipTests.test_success_without_controller_refuses', 'outer_cases.OwnershipTests.test_uncertain_close_never_retried', 'outer_cases.OwnershipTests.test_wrong_callback_code_cannot_succeed', 'outer_cases.ReferencePolicyTests.test_extra_policy_key_refuses', 'outer_cases.ReferencePolicyTests.test_frozen_reference_policy_accepts_original', 'outer_cases.ReferencePolicyTests.test_missing_policy_refuses', 'outer_cases.ReferencePolicyTests.test_missing_reference_policy_argument_has_no_fallback', 'outer_cases.ReferencePolicyTests.test_native_profile_substitution_refuses_after_resealing', 'outer_cases.ReferencePolicyTests.test_new_operation_is_only_dependency_profile_normalization', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_basis', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_binding_plan', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_binding_schema', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_historical_rights', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_historical_scope', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_prerequisites', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_integration_result', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_integration_review', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_old_result', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_old_review', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_old_seal', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_snapshot_log', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_q_snapshot_result', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_role_authority', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_source_cache', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_source_manifest', 'outer_cases.ReferencePolicyTests.test_resealed_substitution_source_receipts', 'outer_cases.ReferencePolicyTests.test_vector_profile_substitution_refuses_after_resealing', 'repair_cases.DependencyReceiptTests.test_legacy_no_LF_config_refused', 'repair_cases.DependencyReceiptTests.test_producer_hashes_accepted_by_consumer', 'repair_cases.DependencyReceiptTests.test_tampered_dependency_hash_refused', 'repair_cases.DescriptorOnlyTests.test_actual_gate_slice_accepts_descriptor_only_result', 'repair_cases.DescriptorOnlyTests.test_actual_gate_slice_refuses_root_proposal', 'repair_cases.DescriptorOnlyTests.test_descriptor_pass_has_no_root_proposal', 'repair_cases.DescriptorOnlyTests.test_invalid_descriptor_still_refuses', 'repair_cases.DescriptorOnlyTests.test_no_root_offset_calculation_in_planner_AST', 'repair_cases.DescriptorOnlyTests.test_outside_group_descriptor_refuses', 'repair_cases.DescriptorOnlyTests.test_phase_A_still_only_proposes_GDT', 'repair_cases.EncodingTests.test_dependency_nonfinite_refused', 'repair_cases.EncodingTests.test_emitted_bytes_pass_real_reconcile_wire_boundary', 'repair_cases.EncodingTests.test_legacy_spaced_stdout_fails_real_reconcile_wire_boundary', 'repair_cases.EncodingTests.test_producer_dependency_contract_ascii', 'repair_cases.EncodingTests.test_producer_dependency_contract_unicode', 'repair_cases.EncodingTests.test_stdout_exact_inherited_wire_contract', 'repair_cases.EncodingTests.test_stdout_flush_failure_refuses', 'repair_cases.EncodingTests.test_stdout_short_write_refuses', 'repair_cases.EncodingTests.test_successful_child_main_uses_binary_wire', 'repair_cases.OwnershipRepairTests.test_false_close_cannot_succeed', 'repair_cases.OwnershipRepairTests.test_inherited_success_close_once', 'repair_cases.OwnershipRepairTests.test_keyboard_interrupt_after_inherited_close_no_retry', 'repair_cases.OwnershipRepairTests.test_keyboard_interrupt_closes_once', 'repair_cases.OwnershipRepairTests.test_system_exit_closes_once', 'repair_cases.OwnershipRepairTests.test_uncertain_close_after_system_exit_no_retry', 'repair_cases.ParentInterruptionTests.test_before_kill_journal_failure_cannot_consume_kill', 'repair_cases.ParentInterruptionTests.test_keyboard_interrupt_kills_reaps_closes_once', 'repair_cases.ParentInterruptionTests.test_kill_interruption_still_waits_without_retry', 'repair_cases.ParentInterruptionTests.test_outer_parent_false_close_cannot_succeed', 'repair_cases.ParentInterruptionTests.test_outer_parent_interrupt_closes_owned_records', 'repair_cases.ParentInterruptionTests.test_sleep_interruption_terminates_once', 'repair_cases.ParentInterruptionTests.test_system_exit_kills_reaps_closes_once', 'repair_cases.ParentInterruptionTests.test_wait_interruption_stays_unknown_without_retry', 'repair_cases.QualificationPolicyTests.test_changed_fixture_pin_refused', 'repair_cases.QualificationPolicyTests.test_count_downgrade_refused_after_resealing', 'repair_cases.QualificationPolicyTests.test_extra_qualification_source_refused', 'repair_cases.QualificationPolicyTests.test_missing_fixture_pin_refused', 'repair_cases.QualificationPolicyTests.test_same_count_case_substitution_refused')
REQUIRED_REPAIR_SOURCE_PINS = {'outer_fixtures.py': '93789f0c796ba241d6c9968cfe9e64f32273ebcf78aa90a622740ae57b03e192', 'test_outer_v2.py': '215b6319563286ed66461d9253a9a791847cf93b06b00b7b4b57d6af4a9835b1', 'scope.md': '5757555f79a7c76a182d8ffc869361c53239781b7c2d6365b10f0a2ea76d5615', 'qualify_review.py': '4e99029b3485a9337b858d2583bc2e2b9d63f37858f71755962bcea504c2bf3a', 'test_review_fixes.py': 'a4aa522ccf7240fcade49ab41a2055077f4910085f37ca112b62e932779e7d74', 'activation/gdt_gate.py': '917c88b52b954d25920b44c83ae397ca1debe36491c19d0e3e0149458010b65c', 'activation/ext_read_planner.py': '7ea688107813156e4bdd43a78d0b8f88e9bd8279fcd81885b7bc39f7e0cf886b', 'activation/io_entry.py': '70a2ed3a0265894adace48e5285c0eb8962c666975f7df1a8e4f6141b918bb43', 'integration/runtime_entry.py': '4a64bd6c63ff6e43b56ab7298e5fb84a6304e3576990eaa4aa020c551aeba8f1', 'outer_gate.py': 'eee5fa7ffb3d429ce1eb1888a5a35813ec93fc6d3baabd39d264ecf32b44a71a', 'ordinary_io.py': '07c63ea490ee3997c3fa668fb45d4e2dfb8a9331f6eaa4b6dc0d4ff4b2660f2a', 'entry_v2.py': '41ea6ee57b17660f70b62e57a80b30c4aacf9ffdd205f0efff5a2f967e307276'}
REPAIR_KEYS = frozenset(('role:gdt_gate', 'role:ext_read_planner', 'bootstrap:io_entry'))
REPAIR_SOURCE_NAMES = {'role:gdt_gate': 'activation/gdt_gate.py', 'role:ext_read_planner': 'activation/ext_read_planner.py', 'bootstrap:io_entry': 'activation/io_entry.py'}
SOURCE_ANCESTRY = {'schema': 'gdt_explicit_source_ancestry_v1', 'legacy_session': 'private/sessions/20261019-RA-003-gdt-review-fixes', 'historical_seal_sha256': 'a882024fb5e424259cc29c4982f5832461b8aa7424cbe2366e6b87d055d5ed94', 'historical_seal_canonical_sha256': '6bea53d98a9d8b16d30517ef09a2513d637c74e0c49c5757a935051ae9d059f2', 'rows': {'bootstrap:activation_binding': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/activation_binding.py', 'historical_key': 'activation_binding.py', 'historical_sha256': '22558080636f15300590c22b9987216216f650b4edc58d7df89092643722de74', 'current_sha256': '22558080636f15300590c22b9987216216f650b4edc58d7df89092643722de74'}, 'bootstrap:activation_gate': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/activation_gate.py', 'historical_key': 'activation_gate.py', 'historical_sha256': '21505f2583de8f5d26f7ccd959903ec964ed39b21ea6df1e400e8bc11b66750b', 'current_sha256': '21505f2583de8f5d26f7ccd959903ec964ed39b21ea6df1e400e8bc11b66750b'}, 'bootstrap:io_entry': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/io_entry.py', 'historical_key': 'io_entry.py', 'historical_sha256': 'f9bb023b428cb5375f26417f3199b6b0607e494f713bf4ebddad05a05569ca8e', 'current_sha256': '70a2ed3a0265894adace48e5285c0eb8962c666975f7df1a8e4f6141b918bb43'}, 'role:acceptance': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/acceptance.py', 'historical_key': 'inherited/acceptance.py', 'historical_sha256': 'e2ee49ee8a419946947ce266a1959d4206b3cb99a3ad6d7ee4f9152a1ec901da', 'current_sha256': 'e2ee49ee8a419946947ce266a1959d4206b3cb99a3ad6d7ee4f9152a1ec901da'}, 'role:artifact_probe': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/activation_reference/artifact_probe.py', 'historical_key': 'activation_reference/artifact_probe.py', 'historical_sha256': '54fbda68197b54547793b72aae1afececb92422dc3f29362c6515f8f86384071', 'current_sha256': '54fbda68197b54547793b72aae1afececb92422dc3f29362c6515f8f86384071'}, 'role:capture': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/reference_source/fdat_trial.py', 'historical_key': 'reference_source/fdat_trial.py', 'historical_sha256': '57e8b894e9ec1293b9780d1dfa0a64fde1c7a634b03b1dca4251b2427e55fa7c', 'current_sha256': '57e8b894e9ec1293b9780d1dfa0a64fde1c7a634b03b1dca4251b2427e55fa7c'}, 'role:classifier': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/classifier.py', 'historical_key': 'inherited/classifier.py', 'historical_sha256': '662036ae5966319621fc359191b59784c6b411777aece1034c21db95601c758a', 'current_sha256': '662036ae5966319621fc359191b59784c6b411777aece1034c21db95601c758a'}, 'role:core': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/fdat_stream.py', 'historical_key': 'inherited/fdat_stream.py', 'historical_sha256': 'c1f7072c975c94044b43a1ffa31b1c7acb01008e9078b1841867b85e7c2523a1', 'current_sha256': 'c1f7072c975c94044b43a1ffa31b1c7acb01008e9078b1841867b85e7c2523a1'}, 'role:expanded_gate': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/expanded_gate.py', 'historical_key': 'inherited/expanded_gate.py', 'historical_sha256': 'bc598272b37b46e1230db286e5c4494de088f299b139301a89a99f8554490687', 'current_sha256': 'bc598272b37b46e1230db286e5c4494de088f299b139301a89a99f8554490687'}, 'role:ext_gate': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/ext_gate.py', 'historical_key': 'ext_gate.py', 'historical_sha256': 'df2fbdeb9ab44d2cee23d41a7e4da9e63dcef7139194edb848b43b321109976d', 'current_sha256': 'df2fbdeb9ab44d2cee23d41a7e4da9e63dcef7139194edb848b43b321109976d'}, 'role:ext_preflight': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/ext_preflight.py', 'historical_key': 'ext_preflight.py', 'historical_sha256': 'e6106e6c72b6aee7d16c4db67e03803d22b5108199f644641b539721daa36775', 'current_sha256': 'e6106e6c72b6aee7d16c4db67e03803d22b5108199f644641b539721daa36775'}, 'role:ext_read_planner': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/ext_read_planner.py', 'historical_key': 'ext_read_planner.py', 'historical_sha256': '6e3ae4773e823927300bafead0df199f7b773abbbcd2b5c0c9903524b6be1721', 'current_sha256': '7ea688107813156e4bdd43a78d0b8f88e9bd8279fcd81885b7bc39f7e0cf886b'}, 'role:ext_superblock': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/ext_superblock.py', 'historical_key': 'ext_superblock.py', 'historical_sha256': 'b838b2fe8f4f3af18ddd4d8f3609acbe51e1aa992343615c84ec8119879750f5', 'current_sha256': 'b838b2fe8f4f3af18ddd4d8f3609acbe51e1aa992343615c84ec8119879750f5'}, 'role:gdt_adapter': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/gdt_adapter.py', 'historical_key': 'gdt_adapter.py', 'historical_sha256': '531dd53fa5bd60cefcb99976b6914ecf5a7b45e592975b3121cba463c533a95d', 'current_sha256': '531dd53fa5bd60cefcb99976b6914ecf5a7b45e592975b3121cba463c533a95d'}, 'role:gdt_cleanup': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/gdt_cleanup.py', 'historical_key': 'gdt_cleanup.py', 'historical_sha256': 'c85bc84c055874e6fc06f338d5856c1a5d78ee373a7bf9a097f8ff7f0906397e', 'current_sha256': 'c85bc84c055874e6fc06f338d5856c1a5d78ee373a7bf9a097f8ff7f0906397e'}, 'role:gdt_gate': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/gdt_gate.py', 'historical_key': 'gdt_gate.py', 'historical_sha256': '25ecf78026191f060b353cb54dc9da50708fc5135b90840ff33f2c198c9786e2', 'current_sha256': '917c88b52b954d25920b44c83ae397ca1debe36491c19d0e3e0149458010b65c'}, 'role:gdt_preflight': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/gdt_preflight.py', 'historical_key': 'gdt_preflight.py', 'historical_sha256': '9f984f8c26437e2000492c4014372334e506ea67bdd6f3cf93ffebff69cf4368', 'current_sha256': '9f984f8c26437e2000492c4014372334e506ea67bdd6f3cf93ffebff69cf4368'}, 'role:gdt_runner': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/gdt_runner.py', 'historical_key': 'gdt_runner.py', 'historical_sha256': '73c03899e3a44a1ce586ef32d2e620275bc1bede3643a55824e6d20fab89bafa', 'current_sha256': '73c03899e3a44a1ce586ef32d2e620275bc1bede3643a55824e6d20fab89bafa'}, 'role:header_candidates': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/header_candidates.py', 'historical_key': 'inherited/header_candidates.py', 'historical_sha256': '522bf2d978454240e6e4c72994f9ef46fc44e47ea93711964d8432406c7ad507', 'current_sha256': '522bf2d978454240e6e4c72994f9ef46fc44e47ea93711964d8432406c7ad507'}, 'role:io_adapter': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/io_adapter.py', 'historical_key': 'io_adapter.py', 'historical_sha256': '6dc64ce25a4c43185e5b2660fc802e314a6451908dba369beffd54ce4d097f81', 'current_sha256': '6dc64ce25a4c43185e5b2660fc802e314a6451908dba369beffd54ce4d097f81'}, 'role:link_acceptance': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/link_acceptance.py', 'historical_key': 'inherited/link_acceptance.py', 'historical_sha256': '56ee869b40b59900bfb0452653175895ed7be1d1e97f1db6579db008ff4ad8d1', 'current_sha256': '56ee869b40b59900bfb0452653175895ed7be1d1e97f1db6579db008ff4ad8d1'}, 'role:member_acceptance': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/member_acceptance.py', 'historical_key': 'inherited/member_acceptance.py', 'historical_sha256': 'e1e717554d21546fb4a2c0aede8473ff0debc8b4b9680210b3dc2e900c408809', 'current_sha256': 'e1e717554d21546fb4a2c0aede8473ff0debc8b4b9680210b3dc2e900c408809'}, 'role:member_prefix': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/member_prefix.py', 'historical_key': 'inherited/member_prefix.py', 'historical_sha256': '6e4b3ff43815a1b89150ff0b2abd4a8d9c579abc69ed32f9f89cd4d648fce431', 'current_sha256': '6e4b3ff43815a1b89150ff0b2abd4a8d9c579abc69ed32f9f89cd4d648fce431'}, 'role:metadata_preflight': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/metadata_preflight.py', 'historical_key': 'inherited/metadata_preflight.py', 'historical_sha256': 'b92b8064bc234ed138bc084040d0206ba879219edc8f4efa15431847cc16fa32', 'current_sha256': 'b92b8064bc234ed138bc084040d0206ba879219edc8f4efa15431847cc16fa32'}, 'role:metadata_tar': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/metadata_tar.py', 'historical_key': 'inherited/metadata_tar.py', 'historical_sha256': 'f2494afc74384bfe34d52bc2fd892464c8669eac86cbddb47a9c588f6cc429cb', 'current_sha256': 'f2494afc74384bfe34d52bc2fd892464c8669eac86cbddb47a9c588f6cc429cb'}, 'role:offline_inventory': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/activation_reference/offline_inventory.py', 'historical_key': 'activation_reference/offline_inventory.py', 'historical_sha256': '3bd0a8eddb4cc9f3aa9589bf625f6ad14daace386180a97332385f7fbd8fa3c7', 'current_sha256': '3bd0a8eddb4cc9f3aa9589bf625f6ad14daace386180a97332385f7fbd8fa3c7'}, 'role:prefix': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/prefix.py', 'historical_key': 'inherited/prefix.py', 'historical_sha256': 'e385fa70dd9fe91513b756d4256f38efc450acd1244f0114bc9c97983a1dd623', 'current_sha256': 'e385fa70dd9fe91513b756d4256f38efc450acd1244f0114bc9c97983a1dd623'}, 'role:tar_inventory': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/inherited/tar_inventory.py', 'historical_key': 'inherited/tar_inventory.py', 'historical_sha256': 'edb92477ab6ca4b164ff9964644a201b8711f4f76aa88361baf7bfe3261c8ed6', 'current_sha256': 'edb92477ab6ca4b164ff9964644a201b8711f4f76aa88361baf7bfe3261c8ed6'}, 'role:validator': {'current_path': 'private/sessions/20261019-RA-003-gdt-review-fixes/activation/activation_reference/fdat_header.py', 'historical_key': 'activation_reference/fdat_header.py', 'historical_sha256': '6d78dc186355919d5457d8cb01b765422d24aca354519f1a76a1554368cdf117', 'current_sha256': '6d78dc186355919d5457d8cb01b765422d24aca354519f1a76a1554368cdf117'}}, 'execution_authorized': False, 'camera_commands': []}
SOURCE_ANCESTRY_SHA256 = '8c424160ee6567f436e8259d986092b414be8569eff927f4d6d109ddf7c58f5c'

def source_ancestry(p, candidate, historical_seal_sha256):
    """Closed explicit ancestry; never infer prefixes or search by basename."""
    proof = closed(SOURCE_ANCESTRY, ('schema', 'legacy_session', 'historical_seal_sha256', 'historical_seal_canonical_sha256', 'rows', 'execution_authorized', 'camera_commands'))
    require(sha(encoded(proof)) == SOURCE_ANCESTRY_SHA256, 'ancestry_policy')
    require(proof['schema'] == 'gdt_explicit_source_ancestry_v1' and proof['execution_authorized'] is False and (proof['camera_commands'] == []), 'ancestry_policy')
    digest(historical_seal_sha256)
    require(historical_seal_sha256 == proof['historical_seal_sha256'] and sha(encoded(p['q_old_seal'])) == proof['historical_seal_canonical_sha256'], 'ancestry_seal')
    legacy = relative(proof['legacy_session'])
    root = absolute(candidate['repository_root'])
    require(legacy == candidate['legacy_session'] and legacy.startswith('private/sessions/'), 'ancestry_root')
    expected = {'role:' + name for name in p['role_authority']['roles']} | {'bootstrap:activation_gate', 'bootstrap:activation_binding', 'bootstrap:io_entry'}
    current = {k for k in p['source_cache']['sources'] if k.startswith(('role:', 'bootstrap:'))}
    require(type(proof['rows']) is dict and len(expected) == 29 and (set(proof['rows']) == expected == current), 'ancestry_roster')
    seen_current = set()
    seen_old = set()
    for key, row in proof['rows'].items():
        closed(row, ('current_path', 'historical_key', 'historical_sha256', 'current_sha256'))
        now = relative(row['current_path'])
        old = relative(row['historical_key'])
        require(now.startswith(legacy + '/') and now.endswith('.py') and old.endswith('.py') and (now.casefold() not in seen_current) and (old.casefold() not in seen_old), 'ancestry_path')
        seen_current.add(now.casefold())
        seen_old.add(old.casefold())
        digest(row['historical_sha256'])
        digest(row['current_sha256'])
        require(row['historical_sha256'] == p['q_old_seal']['sources_sha256'].get(old), 'ancestry_old_identity')
        cached = p['source_cache']['sources'][key]
        require(absolute(cached['path']) == root / now and cached['sha256'] == row['current_sha256'], 'ancestry_current_identity')
    return proof['rows']

def effective_sources(p, candidate, *, repair_result_sha256, historical_seal_sha256):
    """One source qualification map shared by cache validation and loader.



    Historical qualification remains exact-byte evidence. Only three pinned,

    separately reviewed repairs can replace it. This is not a new test result.

    """
    ancestry = source_ancestry(p, candidate, historical_seal_sha256)
    repair = p['q_repair_result']
    review = p['q_repair_review']
    require(repair['status'] == 'qualified_invented_outer_gate_v2' and type(repair['tests_run']) is int and (repair['tests_run'] == 162) and (type(repair['passed']) is int) and (repair['passed'] == 162) and zero(repair['child_exit_code']) and zero(repair['skipped']) and (repair['sources_stable'] is True) and (repair['timed_out'] is False) and (repair['execution_authorized'] is False) and (repair['actual_entry_ready'] is False) and (len(repair['test_ids']) == len(set(repair['test_ids'])) == 162) and (set(repair['test_ids']) == set(REQUIRED_REPAIR_TEST_IDS)) and (repair['source_sha256'] == REQUIRED_REPAIR_SOURCE_PINS), 'repair_qualification')
    closed(review, ('schema', 'status', 'result_sha256', 'source_sha256', 'review_artifact_sha256', 'operational_acceptance', 'execution_authorized', 'camera_commands'))
    require(review['schema'] == 'gdt_scoped_repair_review_v1' and review['status'] == 'three_source_reviews_accept_scoped_repairs' and (review['result_sha256'] == repair_result_sha256) and (review['source_sha256'] == repair['source_sha256']) and (set(review['review_artifact_sha256']) == {'gate', 'runtime', 'io'}) and (review['operational_acceptance'] is False) and (review['execution_authorized'] is False) and (review['camera_commands'] == []), 'repair_review')
    for pin in review['review_artifact_sha256'].values():
        digest(pin)
    overlay = closed(p['repair_overlay'], ('schema', 'repairs', 'execution_authorized', 'camera_commands'))
    require(overlay['schema'] == 'gdt_source_repair_overlay_v1' and overlay['execution_authorized'] is False and (overlay['camera_commands'] == []) and (type(overlay['repairs']) is dict) and (set(overlay['repairs']) == REPAIR_KEYS), 'repair_roster')
    root = absolute(candidate['repository_root'])
    legacy = relative(candidate['legacy_session'])
    effective = {}
    seen = set()
    for key, row in p['source_cache']['sources'].items():
        if not key.startswith(('role:', 'bootstrap:')):
            continue
        path = absolute(row['path'])
        rel = path.relative_to(root / legacy).as_posix()
        relative(rel)
        require(rel.endswith('.py') and rel.casefold() not in seen, 'repair_source_path')
        seen.add(rel.casefold())
        prior = p['q_old_seal']['sources_sha256'].get(ancestry[key]['historical_key'])
        digest(prior)
        if key in REPAIR_KEYS:
            replacement = closed(overlay['repairs'][key], ('path', 'old_sha256', 'new_sha256'))
            require(replacement['path'] == legacy + '/' + rel and replacement['old_sha256'] == prior and (replacement['new_sha256'] == row['sha256']) and (row['sha256'] != prior) and (row['sha256'] == repair['source_sha256'][REPAIR_SOURCE_NAMES[key]]), 'repair_identity')
        else:
            require(row['sha256'] == prior, 'source_qualification')
        effective[legacy + '/' + rel] = row['sha256']
    require(len(effective) == 29 and REPAIR_KEYS.issubset(p['source_cache']['sources']), 'repair_roster')
    return effective

def integration_sources(p):
    """Exact successor factory evidence; historical qualifications stay immutable."""
    proof = closed(p['factory_evidence'], ('schema', 'old_factory_sha256', 'new_factory_sha256', 'contract', 'composition', 'execution_authorized', 'operational_acceptance', 'camera_commands'))
    require(proof['schema'] == 'gdt_reviewed_factory_migration_v1' and proof['execution_authorized'] is False and (proof['operational_acceptance'] is False) and (proof['camera_commands'] == []), 'factory_evidence')
    for name, expected in (('contract', REQUIRED_FACTORY_TEST_IDS), ('composition', REQUIRED_CHILD_TEST_IDS)):
        q = closed(proof[name], ('test_ids', 'source_sha256', 'result_sha256', 'stderr_sha256', 'review_artifact_sha256', 'child_exit_code', 'skipped', 'sources_stable', 'operational_acceptance'))
        require(type(q['test_ids']) is list and len(q['test_ids']) == len(set(q['test_ids'])) == len(expected) and (set(q['test_ids']) == set(expected)) and zero(q['child_exit_code']) and zero(q['skipped']) and (q['sources_stable'] is True) and (q['operational_acceptance'] is False), 'factory_qualification')
        digest(q['result_sha256'])
        digest(q['stderr_sha256'])
        expected_review = {'runtime-rereview-29.json', 'io-rereview-29.json'} if name == 'contract' else {'runtime-rereview-8.json', 'io-review-8.json'}
        require(type(q['review_artifact_sha256']) is dict and set(q['review_artifact_sha256']) == expected_review, 'factory_review')
        for value in q['review_artifact_sha256'].values():
            digest(value)
        require(type(q['source_sha256']) is dict, 'factory_qualification')
        for value in q['source_sha256'].values():
            digest(value)
    contract = proof['contract']['source_sha256']
    composition = proof['composition']['source_sha256']
    require(set(contract) == {'prospective_child.py', 'gdt_wiring.py', 'test_factory.py', 'qualify.py'}, 'factory_roster')
    require(set(composition) == {'roles/' + role + '.py' for role in p['role_authority']['roles']} | {'prospective_child.py', 'gdt_wiring.py', 'io_entry.py', 'runtime_entry.py', 'dependency_fixture.py', 'test_composition.py', 'prepare_fixture.py', 'prepare_fixture_v2.py', 'qualify.py'}, 'factory_roster')
    old = p['q_integration_result']['source_sha256']
    rows = p['source_cache']['sources']
    digest(proof['old_factory_sha256'])
    digest(proof['new_factory_sha256'])
    require(proof['old_factory_sha256'] == old['prospective_child.py'] and proof['new_factory_sha256'] == contract['prospective_child.py'] == composition['prospective_child.py'] and (proof['old_factory_sha256'] != proof['new_factory_sha256']), 'factory_identity')
    effective = {}
    for name in ('runtime_entry', 'gdt_wiring', 'prospective_child'):
        pin = composition[name + '.py']
        require(rows['integration:' + name]['sha256'] == pin, 'integration_identity')
        if name != 'prospective_child':
            require(old[name + '.py'] == pin, 'integration_identity')
        effective[name] = pin
    require(contract['gdt_wiring.py'] == effective['gdt_wiring'] and rows['bootstrap:io_entry']['sha256'] == composition['io_entry.py'], 'integration_identity')
    for role, row in p['role_authority']['roles'].items():
        require(row['sha256'] == composition['roles/' + role + '.py'], 'integration_role_identity')
    return effective

def _source_cache(p, candidate, effective, integration):
    source = closed(p['source_cache'], ('schema', 'sources'))
    require(source['schema'] == 'ordinary_python_source_cache_v1')
    roles = p['role_authority']['roles']
    require(type(roles) is dict and len(roles) == 26)
    config = p['dependency_config']
    closed(config, ('schema', 'operation_id', 'package_root', 'source_rows', 'native_rows', 'trusted_origins', 'vectors'))
    require(config['schema'] == 'dependency_probe_config_v1' and config['operation_id'] == candidate['operation_id'], 'operation_binding')
    require(type(config['source_rows']) is dict and len(config['source_rows']) == 11 and (set(config['native_rows']) == {'cpuid', 'aes', 'aesni', 'ecb', 'cbc'}) and (set(config['trusted_origins']) == {'ctypes', '_ctypes', 'ctypes.util', 'ctypes._endian', 'platform'}))
    expected = {'role:' + name for name in roles}
    expected |= {'bootstrap:' + name for name in ('activation_gate', 'activation_binding', 'io_entry')}
    expected |= {'integration:' + name for name in ('runtime_entry', 'gdt_wiring', 'prospective_child')}
    expected |= {'dependency:' + name for name in config['source_rows']}
    expected |= {'trusted:' + name for name, row in config['trusted_origins'].items() if Path(row['path']).suffix == '.py'}
    require(type(source['sources']) is dict and set(source['sources']) == expected and (len(expected) == 47), 'source_roster')
    receipts = p['source_receipts']['receipts']
    require(type(receipts) is dict and set(receipts) == expected, 'source_receipts')
    buffers = {}
    total = 0
    paths = set()
    root = absolute(candidate['repository_root'])
    legacy = relative(candidate['legacy_session'])
    for key, row in source['sources'].items():
        closed(row, ('path', 'bytes', 'sha256', 'base64'))
        path = absolute(row['path'])
        digest(row['sha256'])
        require(path.suffix == '.py' and row['path'].casefold() not in paths, 'source_path')
        paths.add(row['path'].casefold())
        require(type(row['bytes']) is int and 0 < row['bytes'] <= 8 * MIB and (type(row['base64']) is str))
        try:
            data = base64.b64decode(row['base64'], validate=True)
        except Exception:
            raise GateError('source_encoding') from None
        total += len(data)
        require(total <= 32 * MIB and len(data) == row['bytes'] and (sha(data) == row['sha256']), 'source_hash')
        proof = receipts[key]
        require(all((proof[k] == row[k] for k in ('path', 'bytes', 'sha256'))) and type(proof['close_attempts']) is int and (proof['close_attempts'] == 1) and (type(proof['eof_probes']) is int) and (proof['eof_probes'] == 1) and (proof['closed'] is True) and (proof['lstat_before'] == proof['lstat_after']) and (proof['fstat_before'] == proof['fstat_after']), 'source_receipts')
        fields = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns', 'st_file_attributes')
        for field in ('lstat_before', 'lstat_after', 'fstat_before', 'fstat_after'):
            closed(proof[field], fields)
            require(all((type(v) is int for v in proof[field].values())), 'source_receipts')
        require(all((proof['lstat_before'][k] == proof['fstat_before'][k] for k in fields if k not in ('st_ctime_ns', 'st_file_attributes'))) and proof['fstat_before']['st_size'] == row['bytes'] and (proof['fstat_before']['st_nlink'] == 1), 'source_receipts')
        if key.startswith('role:'):
            role = roles[key[5:]]
            require(path == root / relative(role['path']) and row['sha256'] == role['sha256'])
        elif key.startswith('bootstrap:'):
            require(key in SOURCE_ANCESTRY['rows'] and path == root / SOURCE_ANCESTRY['rows'][key]['current_path'], 'ancestry_bootstrap_path')
        elif key.startswith('dependency:'):
            require({k: row[k] for k in ('path', 'bytes', 'sha256')} == config['source_rows'][key[11:]])
        elif key.startswith('trusted:'):
            require({k: row[k] for k in ('path', 'bytes', 'sha256')} == config['trusted_origins'][key[8:]])
        if key.startswith(('role:', 'bootstrap:')):
            relative_old = path.relative_to(root / legacy).as_posix()
            require(effective.get(legacy + '/' + relative_old) == row['sha256'], 'source_qualification')
        if key.startswith('integration:'):
            require(integration.get(key[12:]) == row['sha256'], 'source_qualification')
        buffers[key] = data
    return buffers

def validate_bundle(documents, *, expected_seal_sha256, reference_pins):
    """Pure validation only; no output records, source execution or device claims."""
    try:
        return _validate_bundle(documents, expected_seal_sha256, reference_pins)
    except GateError:
        raise
    except Exception:
        raise GateError('shape') from None

def _validate_bundle(documents, expected, reference_pins, *, historical_context=None):
    digest(expected)
    closed(documents, ('candidate', 'decision', 'review', 'seal', 'inputs'))
    require(type(documents['inputs']) is dict and set(documents['inputs']) == INPUTS)
    require(all((type(v) is bytes for k, v in documents.items() if k != 'inputs')))
    require(sum((len(v) for k, v in documents.items() if k != 'inputs')) + sum((len(v) for v in documents['inputs'].values())) <= 32 * MIB, 'aggregate_bound')
    require(sha(documents['seal']) == expected, 'external_anchor')
    c, d, r, s = (parse(documents[k]) for k in ('candidate', 'decision', 'review', 'seal'))
    closed(c, ('schema', 'operation_id', 'repository_root', 'session', 'legacy_session', 'base_commit', 'purpose', 'author', 'child_argv_prefix', 'startup', 'bootstrap', 'inputs', 'camera_commands'))
    closed(d, ('schema', 'operation_id', 'candidate_sha256', 'scope_sha256', 'rights_sha256', 'status', 'execution_authorized', 'assessor', 'preserved_uncertainties', 'camera_commands'))
    closed(r, ('schema', 'operation_id', 'candidate_sha256', 'decision_sha256', 'status', 'reviewer', 'findings', 'camera_commands'))
    closed(s, ('schema', 'operation_id', 'candidate_sha256', 'decision_sha256', 'review_sha256', 'execution_authorized', 'camera_commands'))
    require(c['schema'] == 'gdt_outer_candidate_v5' and d['schema'] == 'gdt_outer_decision_v5' and (r['schema'] == 'gdt_outer_review_v5') and (s['schema'] == 'gdt_outer_seal_v5'), 'schema_version')
    operation = digest(c['operation_id'], 32)
    require(all((v['operation_id'] == operation and v['camera_commands'] == [] for v in (c, d, r, s))), 'operation_binding')
    require(c['purpose'] == PURPOSE and d['execution_authorized'] is True and (s['execution_authorized'] is True) and (d['status'] == 'accepted_one_frozen_host_metadata_act') and (r['status'] == 'reviewed_one_frozen_host_metadata_act') and (r['findings'] == []), 'activity_decision')
    for value in (c['author'], d['assessor'], r['reviewer']):
        require(type(value) is str and 0 < len(value) <= 256)
    require(c['author'] != r['reviewer'], 'review_identity')
    require(d['preserved_uncertainties'] == sorted(UNCERTAINTIES), 'rights_preservation')
    candidate_hash = sha(documents['candidate'])
    decision_hash = sha(documents['decision'])
    require(d['candidate_sha256'] == r['candidate_sha256'] == s['candidate_sha256'] == candidate_hash and r['decision_sha256'] == s['decision_sha256'] == decision_hash and (s['review_sha256'] == sha(documents['review'])), 'document_binding')
    root = absolute(c['repository_root'])
    session = relative(c['session'])
    relative(c['legacy_session'])
    require(session.startswith('private/sessions/') and session != c['legacy_session'])
    digest(c['base_commit'], 40)
    closed(c['bootstrap'], ('outer_gate', 'ordinary_io', 'entry_v2'))
    for name, row in c['bootstrap'].items():
        _ref(row)
        require(row['path'] == session + '/' + name + '.py', 'bootstrap_binding')
    require(type(c['child_argv_prefix']) is list and len(c['child_argv_prefix']) == 7 and all((type(x) is str for x in c['child_argv_prefix'])) and (c['child_argv_prefix'][1:6] == FLAGS) and (c['child_argv_prefix'][6] == str(root / session / 'entry_v2.py')), 'child_argv')
    require(c['child_argv_prefix'][0] == c['startup']['executable'], 'interpreter_binding')
    require(type(c['inputs']) is dict and set(c['inputs']) == INPUTS)
    p = {}
    seen = {row['path'] for row in c['bootstrap'].values()}
    for role, row in c['inputs'].items():
        _ref(row)
        require(row['path'] not in seen, 'path_alias')
        seen.add(row['path'])
        raw = documents['inputs'][role]
        require(type(raw) is bytes and len(raw) == row['bytes'] and (sha(raw) == row['sha256']), 'input_binding')
        if role != 'q_snapshot_log':
            p[role] = parse(raw)
    require(type(reference_pins) is dict and set(reference_pins) == REFERENCE_ROLES | {'dependency_profile'}, 'reference_policy')
    for role in REFERENCE_ROLES:
        digest(reference_pins[role])
        require(sha(documents['inputs'][role]) == reference_pins[role], 'reference_authority')
    digest(reference_pins['dependency_profile'])
    profile = {key: value for key, value in p['dependency_config'].items() if key != 'operation_id'}
    require(sha(encoded(profile)) == reference_pins['dependency_profile'], 'dependency_authority')
    require(set(p['basis']) == BASIS_ROLES, 'basis_roster')
    manifest = p['source_manifest']
    closed(manifest, ('schema', 'relative_path', 'bytes', 'sha256', 'readonly_required', 'existing_private_acquisition', 'no_acquisition_or_download', 'camera_commands'))
    require(manifest['schema'] == 'gdt_io_source_manifest_v1' and relative(manifest['relative_path']).startswith('private/') and (type(manifest['bytes']) is int) and (8 <= manifest['bytes'] <= 2 ** 31) and all((manifest[k] is True for k in ('readonly_required', 'existing_private_acquisition', 'no_acquisition_or_download'))) and (manifest['camera_commands'] == []), 'source_manifest')
    digest(manifest['sha256'])
    prior = p['basis']['prior_stream']
    require(prior['input_package_bytes'] == manifest['bytes'] and prior['input_package_sha256'] == manifest['sha256'], 'basis_source')
    plan = p['prerequisites']
    require(same(plan['qualified_roles'], p['role_authority']['roles']) and same(plan['binding_input']['roles'], p['role_authority']['roles']) and (type(plan['constants_assignment_count']) is int) and (plan['constants_assignment_count'] == 15) and same(plan['selected_literal_lengths'], {'common': 16, 'candidate': 32}), 'prerequisite_binding')
    constants = relative(plan['constants_relative_path'])
    digest(plan['constants_sha256'])
    require(constants.startswith('private/') and constants != manifest['relative_path'], 'protected_paths')
    ordinary_paths = {row['path'] for row in c['inputs'].values()} | {row['path'] for row in c['bootstrap'].values()}
    require(constants not in ordinary_paths and manifest['relative_path'] not in ordinary_paths, 'protected_paths')
    for row in p['source_cache']['sources'].values():
        require(absolute(row['path']) not in (root / constants, root / manifest['relative_path']), 'protected_paths')
    startup_shape(p['dependency_config'], c['startup'])
    scope = p['activity_scope']
    rights = p['activity_rights']
    closed(scope, ('schema', 'operation_id', 'purpose', 'risk', 'basis_sha256', 'source_manifest_sha256', 'historical_scope_sha256', 'camera_commands'))
    require(same(scope, {'schema': 'gdt_outer_scope_v5', 'operation_id': operation, 'purpose': PURPOSE, 'risk': 'R0', 'basis_sha256': sha(documents['inputs']['basis']), 'source_manifest_sha256': sha(documents['inputs']['source_manifest']), 'historical_scope_sha256': sha(documents['inputs']['historical_scope']), 'camera_commands': []}), 'scope_binding')
    closed(rights, ('schema', 'owner_facts', 'activity_scope_sha256', 'historical_rights_sha256', 'preserved_uncertainties', 'camera_commands'))
    require(same(rights, {'schema': 'gdt_outer_rights_v5', 'owner_facts': OWNER, 'activity_scope_sha256': sha(documents['inputs']['activity_scope']), 'historical_rights_sha256': sha(documents['inputs']['historical_rights']), 'preserved_uncertainties': sorted(UNCERTAINTIES), 'camera_commands': []}), 'rights_preservation')
    require(d['scope_sha256'] == sha(documents['inputs']['activity_scope']) and d['rights_sha256'] == sha(documents['inputs']['activity_rights']), 'decision_binding')
    parent_evidence(p)
    _qualifications(p, documents['inputs'])
    for name, row in c['bootstrap'].items():
        require(p['q_outer_result']['source_sha256'].get(name + '.py') == row['sha256'], 'bootstrap_qualification')
    effective = effective_sources(p, c, repair_result_sha256=sha(documents['inputs']['q_repair_result']), historical_seal_sha256=sha(documents['inputs']['q_old_seal']))
    integration = integration_sources(p)
    cache_context = c if historical_context is None else historical_context
    buffers = _source_cache(p, cache_context, effective, integration)
    return {'schema': 'gdt_outer_validated_v5', 'candidate': c, 'inputs': p, 'source_buffers': buffers, 'effective_qualified_sources': effective, 'effective_integration_sources': integration, 'seal_sha256': expected, 'document_sha256': {role: sha(documents[role]) for role in ('candidate', 'decision', 'review', 'seal')}, 'child_argv': c['child_argv_prefix'] + ['child', expected, operation], 'execution_authorized': True, 'actual_entry_ready': False, 'feature_supported': False, 'device_write_gate_passed': False, 'camera_commands': []}

def historical_context(documents, *, context_bytes, expected_context_sha256, ancestry_proof_bytes, expected_ancestry_proof_sha256, expected_operation_id):
    """Bind immutable historical metadata independently of the proposed act.

    All inputs are caller-captured bytes. Digests establish consistency, not
    permission, fresh attestation, or authority to access protected inputs.
    """
    digest(expected_context_sha256)
    digest(expected_ancestry_proof_sha256)
    digest(expected_operation_id, 32)
    require(type(context_bytes) is bytes and 0 < len(context_bytes) <= 16384 and (sha(context_bytes) == expected_context_sha256), 'historical_context_anchor')
    require(type(ancestry_proof_bytes) is bytes and 0 < len(ancestry_proof_bytes) <= 65536 and (sha(ancestry_proof_bytes) == expected_ancestry_proof_sha256 == SOURCE_ANCESTRY_SHA256) and (ancestry_proof_bytes == encoded(SOURCE_ANCESTRY)), 'historical_ancestry_anchor')
    context = closed(parse(context_bytes), ('schema', 'repository_root', 'legacy_session', 'operation_id', 'dependency_config_sha256', 'historical_seal_sha256', 'ancestry_proof_sha256', 'execution_authorized', 'camera_commands'))
    require(context['schema'] == 'gdt_historical_context_v1' and context['execution_authorized'] is False and (context['camera_commands'] == []), 'historical_context_schema')
    digest(context['operation_id'], 32)
    for field in ('dependency_config_sha256', 'historical_seal_sha256', 'ancestry_proof_sha256'):
        digest(context[field])
    candidate = parse(documents['candidate'])
    config = parse(documents['inputs']['dependency_config'])
    require(candidate['operation_id'] == expected_operation_id and context['operation_id'] != expected_operation_id and (config['operation_id'] == context['operation_id']), 'historical_operation_binding')
    absolute(context['repository_root'])
    relative(context['legacy_session'])
    require(context['repository_root'] == candidate['repository_root'] and context['legacy_session'] == candidate['legacy_session'], 'historical_context_root')
    require(context['dependency_config_sha256'] == sha(documents['inputs']['dependency_config']) and context['historical_seal_sha256'] == sha(documents['inputs']['q_old_seal']) and (context['ancestry_proof_sha256'] == expected_ancestry_proof_sha256), 'historical_context_sources')
    return context

def validate_bundle_v6(documents, *, expected_seal_sha256, reference_pins, context_bytes, expected_context_sha256, ancestry_proof_bytes, expected_ancestry_proof_sha256, expected_operation_id):
    """Versioned consistency preflight retaining all inherited v5 predicates.

    The historical config is never rewritten. The current candidate/decision/
    review/seal must still describe one distinct current act. No command or
    authorization for an actual act is returned by this entry.
    """
    try:
        context = historical_context(documents, context_bytes=context_bytes, expected_context_sha256=expected_context_sha256, ancestry_proof_bytes=ancestry_proof_bytes, expected_ancestry_proof_sha256=expected_ancestry_proof_sha256, expected_operation_id=expected_operation_id)
        result = _validate_bundle(documents, expected_seal_sha256, reference_pins, historical_context=context)
        result.pop('child_argv')
        result.update(schema='gdt_outer_consistency_v6', current_operation_id=expected_operation_id, historical_operation_id=context['operation_id'], historical_context_sha256=expected_context_sha256, ancestry_proof_sha256=expected_ancestry_proof_sha256, execution_authorized=False, actual_entry_ready=False, feature_supported=False, recovery_proven=False, device_write_gate_passed=False, actual_inputs_accessed=False, consistency_only=True)
        return result
    except GateError:
        raise
    except Exception:
        raise GateError('shape') from None

def main(argv=None):
    return 2
if __name__ == '__main__':
    raise SystemExit(main())
REQUIRED_FACTORY_TEST_IDS = ('test_factory.FactoryTests.test_aes_identity_before_source_loading', 'test_factory.FactoryTests.test_aes_identity_rechecked_before_constants', 'test_factory.FactoryTests.test_close_removes_owned_aliases_and_preserves_dependency', 'test_factory.FactoryTests.test_closed_factory_cannot_claim', 'test_factory.FactoryTests.test_constants_backward_unused_alias_allowed', 'test_factory.FactoryTests.test_constants_call_never_executed', 'test_factory.FactoryTests.test_constants_chained_assignment', 'test_factory.FactoryTests.test_constants_duplicate_name', 'test_factory.FactoryTests.test_constants_forward_alias', 'test_factory.FactoryTests.test_constants_hash_mismatch', 'test_factory.FactoryTests.test_constants_nonbytes_literal', 'test_factory.FactoryTests.test_constants_statement_count', 'test_factory.FactoryTests.test_constants_wrong_key_length', 'test_factory.FactoryTests.test_context_revalidated_before_constants', 'test_factory.FactoryTests.test_factory_cli_disabled', 'test_factory.FactoryTests.test_factory_single_claim', 'test_factory.FactoryTests.test_keyboard_interrupt_import_cleanup', 'test_factory.FactoryTests.test_missing_alias_does_not_abandon_other_owned_aliases', 'test_factory.FactoryTests.test_path_mutation_restored_on_import_refusal', 'test_factory.FactoryTests.test_protected_import_fault_closes_all_loaded_modules', 'test_factory.FactoryTests.test_replaced_alias_preserved_other_owned_aliases_released', 'test_factory.FactoryTests.test_second_loader_refused', 'test_factory.FactoryTests.test_source_alias_collision_preserves_preexisting_module', 'test_factory.FactoryTests.test_source_hash_mismatch', 'test_factory.FactoryTests.test_success_loads_real_factory_and_delays_protected_sources', 'test_factory.FactoryTests.test_unbound_helper_import_refused', 'test_factory.FactoryTests.test_unbound_tools_child_refused_and_package_cleaned', 'test_factory.WiringFactoryTests.test_real_wiring_calls_real_factory_with_invented_boundaries', 'test_factory.WiringFactoryTests.test_real_wiring_releases_factory_on_controller_exception')
REQUIRED_CHILD_TEST_IDS = ('__main__.CompositionTests.test_changed_context_refuses_before_runtime', '__main__.CompositionTests.test_complete_actual_authored_composition_on_invented_stream', '__main__.CompositionTests.test_constants_AST_rejection_precedes_stream_open', '__main__.CompositionTests.test_constants_change_refuses_before_stream_open', '__main__.CompositionTests.test_second_phase_read_fault_preserves_needs_review_without_retry', '__main__.CompositionTests.test_source_buffer_change_refuses_before_constants_or_stream', '__main__.CompositionTests.test_stream_hash_change_refuses_and_closes_once', '__main__.CompositionTests.test_writable_stream_refuses_before_open')
