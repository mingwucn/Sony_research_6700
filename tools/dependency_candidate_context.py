"""Versioned invented operation/context envelope; no operational authority.

The unchanged v1 documents remain a byte-bound comparison payload. New v2
records bind that payload to a caller-selected operation and four sidecars.
"""
if __name__ == '__main__':
    raise SystemExit(2)

from tools import dependency_legacy_bridge as bridge

e=bridge.e
ANCHORS=frozenset(('source','dependency','activity','bridge'))


def validate_invented_context_documents(documents, *, external_seal_sha256,
        expected_operation_id, legacy_documents, scope_bytes, anchor_buffers):
    """Pure original-byte DAG checks, with no imports/reads of supplied sources.

    This lower-level API authenticates neither the caller's expected operation
    nor sidecar semantics. The full API below also calls retained validators.
    """
    e.shape(documents,e.DOCUMENTS,'context_document_roster')
    e.shape(legacy_documents,e.DOCUMENTS,'context_legacy_roster')
    e.shape(anchor_buffers,ANCHORS,'context_anchor_roster')
    e.receipt(scope_bytes)
    bridge.activity.composed._operation(expected_operation_id)
    e.digest(external_seal_sha256)
    data={n:e.decode(v) for n,v in documents.items()}
    e.need(e.sha(documents['seal'])==external_seal_sha256,'context_external_seal')
    for name,value in data.items():
        e.need(type(value) is dict and value.get('schema')=='invented_context_'+name+'_v2' and
            value.get('invented') is True,'context_invented_mode')
        e.need(value.get('operation_id')==expected_operation_id,'context_operation')
        e.need(value.get('camera_commands')==[],'context_camera_commands')
    candidate,review,decision,seal=(data[n] for n in ('candidate','review','decision','seal'))
    common=('schema','invented','operation_id','camera_commands')
    e.shape(candidate,common+('purpose','phase','scope_file_sha256','legacy_documents','anchors'),'context_candidate_shape')
    e.need(candidate['purpose']=='non_executable_context_comparison' and
        candidate['phase'] in ('prepared','operational_shape'),'context_candidate_mode')
    e.need(candidate['scope_file_sha256']==e.sha(scope_bytes),'context_scope_bytes')
    e.receipts(candidate['legacy_documents'],legacy_documents,e.DOCUMENTS)
    e.receipts(candidate['anchors'],anchor_buffers,ANCHORS)
    legacy_candidate=e.decode(legacy_documents['candidate'])
    e.need(type(legacy_candidate) is dict and legacy_candidate.get('phase')==candidate['phase'],
        'context_legacy_phase')
    for raw in anchor_buffers.values():
        anchor=e.decode(raw)
        e.need(type(anchor) is dict and anchor.get('operation_id')==expected_operation_id,'context_sidecar_operation')
    e.shape(review,common+('candidate_sha256','outcome'),'context_review_shape')
    e.need(review['candidate_sha256']==e.sha(documents['candidate']) and review['outcome']=='accepted_shape',
        'context_review_binding')
    e.shape(decision,common+('candidate_sha256','review_sha256','outcome'),'context_decision_shape')
    e.need(decision['candidate_sha256']==e.sha(documents['candidate']) and
        decision['review_sha256']==e.sha(documents['review']),'context_decision_binding')
    expected='pending' if candidate['phase']=='prepared' else 'accepted_shape'
    e.need(decision['outcome']==expected,'context_decision_phase')
    e.shape(seal,common+('candidate_sha256','review_sha256','decision_sha256'),'context_seal_shape')
    for name in ('candidate','review','decision'):
        e.need(seal[name+'_sha256']==e.sha(documents[name]),'context_seal_binding')
    return dict(schema='invented_context_consistency_v2',operation_id=expected_operation_id,
        phase=candidate['phase'],candidate_operation_consistent=True,
        legacy_records_original_bytes_bound=True,context_anchor_original_bytes_bound=True,
        operation_origin_authenticated=False,reviewer_authenticated=False,owner_permission_authenticated=False,
        retained_sidecar_contracts_checked=False,validator_execution_owned=False,source_freshness_verified=False,
        rights_established=False,dependency_bridge_verified=False,actual_startup_verified=False,actual_inputs_accessed=False,
        execution_authorized=False,feature_supported=False,recovery_proven=False,
        device_write_gate_passed=False,camera_commands=[])


def validate_invented_context_composition(documents, legacy_documents, *,
        external_context_seal_sha256, expected_operation_id, **bridge_inputs):
    """Bind operation/context first, then validate fourteen roles and comparison."""
    anchors={name:bridge_inputs[name+'_anchor_bytes'] for name in ANCHORS}
    context=validate_invented_context_documents(documents,external_seal_sha256=external_context_seal_sha256,
        expected_operation_id=expected_operation_id,legacy_documents=legacy_documents,
        scope_bytes=bridge_inputs['scope_bytes'],anchor_buffers=anchors)
    retained=bridge.validate_invented_bridge(legacy_documents,**bridge_inputs)
    # The v1 record remains comparison-only, irrespective of a v2 shape pass.
    context.update(schema='invented_context_composition_v2',retained_sidecar_contracts_checked=True,
        legacy_comparison_result=retained,actual_inputs_accessed=False,
        complete_basis_semantics_verified=False,legacy_context_binding_present=False)
    return context


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
