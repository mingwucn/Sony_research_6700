"""Bind invented current contracts to original gate inputs before preparation.

No I/O, observer construction or activation. The caller owns the gate result,
captured-buffer loaders and process bootstrap; hashes do not establish consent.
"""
if __name__ == '__main__':
    raise SystemExit(2)

from pathlib import PureWindowsPath
from tools import dependency_current_metadata as current

e = current.launch


def validate_invented_outer(*, outer_documents, expected_outer_receipts, validated,
        prepared_request_bytes, prepared_request_sha256, prepared_repository_root,
        arguments, metadata_owner, adapter_owner):
    e.need(type(outer_documents) is dict and set(outer_documents)=={'candidate','review','decision','seal','inputs'},
           'outer_metadata_documents')
    docs={n:outer_documents[n] for n in ('candidate','review','decision','seal')}
    inputs=outer_documents['inputs']
    e.need(type(inputs) is dict,'outer_metadata_inputs')
    current.receipts(expected_outer_receipts,dict(docs,**{'input:'+n:v for n,v in inputs.items()}))
    e.same({n:e.sha(raw) for n,raw in docs.items()},validated['document_sha256'],
        'outer_metadata_document_binding')
    e.need(e.sha(docs['seal'])==validated['seal_sha256'],'outer_metadata_seal_binding')
    candidate=e.strict(docs['candidate'])
    e.same(candidate,validated['candidate'],'outer_metadata_candidate')
    e.need(set(inputs)==set(candidate['inputs']) and
        set(validated['inputs'])==set(inputs)-{'q_snapshot_log'},'outer_metadata_input_roster')
    for name,raw in inputs.items():
        e.need(len(raw)==candidate['inputs'][name]['bytes'] and
            e.sha(raw)==candidate['inputs'][name]['sha256'],'outer_metadata_gate_input_bytes')
        if name!='q_snapshot_log':
            e.same(e.strict(raw),validated['inputs'][name],'outer_metadata_validated_input')
    e.need(type(arguments) is dict and 'source_frames' not in arguments,'outer_metadata_arguments')
    e.need(arguments['request_bytes']==prepared_request_bytes and
        arguments['expected_request_bytes_sha256']==prepared_request_sha256==e.sha(prepared_request_bytes),
        'outer_metadata_prepared_request')
    request=e.strict(prepared_request_bytes)
    e.need(request['operation_id']==candidate['operation_id'],'outer_metadata_operation')
    comparison=arguments['context_arguments']
    ordinary=arguments['ordinary_buffers']
    for name in current.BASIS:
        e.need(ordinary[name]==comparison['ordinary_buffers'][name]==inputs[name],
               'outer_metadata_retained_input')
    history=metadata_owner.modules['dependency_authority_grammar'].HISTORY_ROLES
    e.need(set(comparison['historical_buffers'])==history,'outer_metadata_history_roster')
    for name in history:
        e.need(comparison['historical_buffers'][name]==inputs[name],'outer_metadata_history_original')
    frames=dict(comparison_root=PureWindowsPath(candidate['repository_root']).as_posix(),
        prepared_root=PureWindowsPath(prepared_repository_root).as_posix())
    manifest=e.strict(ordinary['authored_source_manifest'])
    e.need(manifest['root_path']==frames['prepared_root'],'outer_metadata_prepared_root')
    result=current.validate_invented_current(**arguments,metadata_owner=metadata_owner,
        adapter_owner=adapter_owner,source_frames=frames)
    return dict(schema='invented_outer_metadata_binding_v1',operation_id=request['operation_id'],
        prepared_request_bytes_sha256=e.sha(prepared_request_bytes),
        outer_original_sha256={n:e.sha(v) for n,v in dict(docs,**{'input:'+n:v for n,v in inputs.items()}).items()},
        current_ordinary_sha256=result['current_ordinary_sha256'],source_frames=frames,
        comparison_context_seal_sha256=comparison['external_context_seal_sha256'],
        checked_current_roles=result['checked_roles'],current_source_roles=result['current_source_roles'],
        unique_source_paths=result['unique_source_paths'],derived_closure_is_file=False,
        source_reads_observed=False,source_freshness_verified=False,rights_established=False,
        actual_inputs_accessed=False,execution_authorized=False,feature_supported=False,
        recovery_proven=False,device_write_gate_passed=False,camera_commands=[])


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
