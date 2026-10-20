"""Pure closed schemas for invented successor process qualification only.

These synthetic review records bind bytes; they confer no human permission.
Ordinary runtime activation and the CLI remain disabled.
"""
if __name__=='__main__':
    raise SystemExit(2)

import hashlib
import json
from pathlib import Path


ROLES = ('acceptance','link_acceptance','member_acceptance','metadata_preflight',
         'expanded_gate','ext_superblock','ext_preflight','ext_read_planner','ext_gate',
         'gdt_preflight','gdt_cleanup','gdt_gate','gdt_adapter','gdt_runner','prefix',
         'offline_inventory','artifact_probe','classifier','tar_inventory','metadata_tar',
         'member_prefix','header_candidates','io_adapter','validator','capture','core')
SHARED = ('dependency_evidence','dependency_producer','dependency_package_preflight',
          'dependency_execution','dependency_controller','dependency_parent')
CHILD = SHARED[:-1]
SOURCE_ROLES = frozenset({'bound.role:'+n for n in ROLES} |
    {'bound.bootstrap:activation_binding','bound.bootstrap:io_entry','bound.integration:prospective_child'} |
    {'dependency.'+n for n in SHARED} |
    {'namespace','outer_child','outer_entry','outer_gate','ordinary_io',
     'invented_fixture','successor_entry','successor_wiring','outer_contract'})
SOURCE_ROLES = SOURCE_ROLES | {'adapter_loader', 'adapter', 'adapter_scope', 'adapter_comparison'}
METADATA_SHARED = dict(dependency_outer_contract='adapter_comparison',dependency_operational_scope='adapter_scope',
    **{n:'dependency.'+n for n in ('dependency_evidence','dependency_producer','dependency_package_preflight','dependency_execution')})
METADATA_EXTRA = ('dependency_authority_grammar','dependency_basis_links','dependency_basis_recompute',
    'dependency_input_semantics','dependency_source_receipts','dependency_activity_metadata',
    'dependency_legacy_bridge','dependency_candidate_context')
CURRENT = ('dependency_launch_context','dependency_current_metadata','dependency_outer_metadata')
SOURCE_ROLES = SOURCE_ROLES | {'host_launcher'}
SOURCE_ROLES = SOURCE_ROLES | {'metadata_loader','metadata_audit'} | {'metadata.'+n for n in METADATA_EXTRA} | {'current.'+n for n in CURRENT}
REQUEST_FIELDS = frozenset(('schema','operation_id','sources','packet','argv_prefix',
    'expected_runtime','bootstrap_sha256','review_sha256','folder','authority'))
FLAGS = ('production_runtime_qualified','execution_authorized','feature_supported',
         'recovery_proven','device_write_gate_passed')
METRICS = ('stream_opens','stream_closes','stream_cipher_calls','record_close_attempts',
           'role_release_attempts','factory_calls')
DEPENDENCY_ARTIFACTS = frozenset(('started.json','collection.json','transition.json','verification.json','completion.json',
    'producer/expectation.json','producer/binding.json','producer/journal.jsonl','producer/raw.json',
    'producer/audit-acknowledgement.json','producer/result.json'))
BASE_TERMINAL = frozenset(('schema','operation_id','status','source_closure_sha256',
    'neutral_namespace','source_roles','namespace_closed','role_loader_closed',
    'metrics','test_injection_used','camera_commands') + FLAGS)
BASE_TERMINAL = BASE_TERMINAL | {'adapter_closed', 'adapter_request_sha256'}
BASE_TERMINAL = BASE_TERMINAL | {'metadata_preflight_sha256','comparison_closed','metadata_closed','preparation_calls','metadata_attempts'}
BASE_TERMINAL = BASE_TERMINAL | {'metadata_close_attempts'}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def sha(value):
    return hashlib.sha256(value).hexdigest()


def authority(request):
    """Deterministic invented binding; never a permission or source-review claim."""
    return dict(schema='invented_successor_authority_v1',operation_id=request['operation_id'],
        source_manifest_sha256=sha(canonical(request['sources'])),packet_sha256=request['packet']['sha256'],
        profile_sha256=sha(canonical(request['expected_runtime'])),argv_prefix_sha256=sha(canonical(request['argv_prefix'])),
        bootstrap_sha256=request['bootstrap_sha256'],dependency_review_sha256=request['review_sha256'],
        status='invented_binding_only',execution_authorized=False,feature_supported=False,
        recovery_proven=False,device_write_gate_passed=False,camera_commands=[])


def validate_request(request):
    need(type(request) is dict and set(request)==REQUEST_FIELDS,'successor_request_shape')
    need(request['schema']=='invented_successor_outer_request_v1','successor_mode')
    need(type(request['operation_id']) is str and len(request['operation_id'])==32 and
         all(c in '0123456789abcdef' for c in request['operation_id']),'successor_operation')
    need(type(request['sources']) is dict and set(request['sources'])==SOURCE_ROLES,'successor_source_roster')
    folder=Path(request['folder'])
    need(folder.is_absolute() and '..' not in folder.parts,'successor_folder')
    paths=set()
    for row in list(request['sources'].values())+[request['packet']]:
        need(type(row) is dict and set(row)=={'path','size','sha256','lstat','fstat'},'successor_receipt_shape')
        path=Path(row['path'])
        need(path.is_absolute() and '..' not in path.parts and path.is_relative_to(folder) and
             path != folder and str(path).casefold() not in paths,'successor_source_path')
        paths.add(str(path).casefold())
        need(type(row['size']) is int and 0<row['size']<=8*1024**2,'successor_receipt_size')
        need(type(row['sha256']) is str and len(row['sha256'])==64 and
             all(c in '0123456789abcdef' for c in row['sha256']),'successor_receipt_hash')
    need(all(Path(r['path']).suffix=='.py' for r in request['sources'].values()) and
         Path(request['packet']['path'])==folder/'packet.json','successor_source_path')
    need(type(request['argv_prefix']) is list and len(request['argv_prefix'])==8 and
         request['argv_prefix'][1:7]==['-I','-S','-B','-X','utf8','-c'],'successor_argv')
    need(request['argv_prefix'][0]==request['expected_runtime']['executable'] and
         sha(request['argv_prefix'][-1].encode('utf-8'))==request['bootstrap_sha256'],'successor_bootstrap')
    need(type(request['review_sha256']) is str and len(request['review_sha256'])==64 and
         all(c in '0123456789abcdef' for c in request['review_sha256']),'successor_review')
    need(canonical(request['authority'])==canonical(authority(request)),'successor_authority')
    return request


def validate_terminal(result, request):
    validate_request(request)
    need(type(result) is dict,'successor_terminal_shape')
    success=result.get('status')=='invented_outer_child_complete'
    extras={'dependency_artifact_sha256','bridge_artifact_sha256','summary_sha256'} if success else {'failure_type','failure_code','cleanup_check_failed'}
    need(set(result)==BASE_TERMINAL|extras,'successor_terminal_shape')
    need(result['schema']=='invented_successor_outer_child_v1' and
         result['operation_id']==request['operation_id'] and
         result['source_closure_sha256']==sha(canonical(request['sources'])),'successor_terminal_binding')
    need(result['neutral_namespace']=='_a6700_successor' and result['source_roles']==list(CHILD), 'successor_terminal_roles')
    need(result['test_injection_used'] is True and result['camera_commands']==[] and
         all(result[n] is False for n in FLAGS),'successor_terminal_authority')
    need(type(result['metrics']) is dict and set(result['metrics'])==set(METRICS) and
         all(type(v) is int and 0<=v<=8 for v in result['metrics'].values()),'successor_terminal_metrics')
    need(type(result['namespace_closed']) is bool and type(result['role_loader_closed']) is bool,'successor_terminal_cleanup')
    need(type(result['comparison_closed']) is bool and type(result['metadata_closed']) is bool and
         all(type(result[n]) is int and 0<=result[n]<=1 for n in ('preparation_calls','metadata_attempts')),'metadata_terminal_cleanup')
    need(type(result['metadata_close_attempts']) is dict and set(result['metadata_close_attempts'])=={'comparison','current'} and
         all(type(v) is int and 0<=v<=1 for v in result['metadata_close_attempts'].values()),'metadata_close_attempts')
    digest=result['metadata_preflight_sha256']
    need(digest is None or type(digest) is str and len(digest)==64 and all(c in '0123456789abcdef' for c in digest),'metadata_terminal_hash')
    need(result['preparation_calls']==0 or digest is not None and result['metadata_attempts']==1,'metadata_before_preparation')
    need(type(result['adapter_closed']) is bool and type(result['adapter_request_sha256']) is str and
         len(result['adapter_request_sha256'])==64 and all(c in '0123456789abcdef' for c in result['adapter_request_sha256']),
         'adapter_terminal_binding')
    if success:
        need(digest is not None and result['comparison_closed'] is result['metadata_closed'] is True and
             result['preparation_calls']==result['metadata_attempts']==1 and
             result['metadata_close_attempts']==dict(comparison=1,current=1),'metadata_terminal_success')
        need(result['adapter_closed'] is True,'adapter_terminal_cleanup')
        need(result['namespace_closed'] is result['role_loader_closed'] is True and
             result['metrics']==dict(stream_opens=2,stream_closes=2,stream_cipher_calls=4,
                record_close_attempts=1,role_release_attempts=1,factory_calls=1),'successor_terminal_success')
        for field,roster in (('dependency_artifact_sha256',DEPENDENCY_ARTIFACTS),
                             ('bridge_artifact_sha256',{'completion.json','controller-result.json'})):
            need(type(result[field]) is dict and set(result[field])==roster,'successor_terminal_artifacts')
            need(all(type(v) is str and len(v)==64 and all(c in '0123456789abcdef' for c in v)
                     for v in result[field].values()),'successor_terminal_hash')
        need(type(result['summary_sha256']) is str and len(result['summary_sha256'])==64 and
             all(c in '0123456789abcdef' for c in result['summary_sha256']),'successor_terminal_hash')
    else:
        need(type(result['failure_code']) is str and len(result['failure_code'])<=160,'metadata_failure_code')
        need(result['status']=='needs_review' and type(result['failure_type']) is str and
             0<len(result['failure_type'])<=80 and type(result['cleanup_check_failed']) is bool,'successor_terminal_refusal')
    return 'success' if success else 'refused'


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')


def main():
    return 2


if __name__=='__main__':
    raise SystemExit(main())
