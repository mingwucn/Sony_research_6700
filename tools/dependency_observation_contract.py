"""Pure proposed-observation and separately decided-scope consistency.

Bytes in, consistency out. No open, import hook, process, observer or permission
API. An externally supplied digest is a consistency anchor, not proof of consent.
The disabled operational launcher is deliberately not connected to this module.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import hashlib
import json
import math
from pathlib import PurePosixPath, PureWindowsPath

from tools import dependency_operational_scope as policy
from tools import dependency_outer_contract as comparison
from tools import dependency_adapter_binding as adapter
from tools import dependency_execution as dependency

MAX_BYTES = 4 * 1024**2
RETAINED = frozenset(('basis', 'source_manifest', 'prerequisites', 'binding_plan',
                      'role_authority', 'binding_schema'))
CHILD_ROLES = frozenset({'bound.role:'+n for n in comparison.ROLES} |
    {'bound.bootstrap:activation_binding','bound.bootstrap:io_entry','bound.integration:prospective_child'} |
    {'dependency.'+n for n in comparison.SHARED} |
    {'adapter','adapter_scope','adapter_comparison','namespace','successor_wiring',
     'host_entry','retained_gate','ordinary_io','operational_metadata','operational_entry',
     'operational_preparation','adapter_loader','outer_loader','process_child'})
HOST_ROLES = frozenset(('host.launcher', 'host.bootstrap_and_supervisor'))
SOURCE_ROLES = CHILD_ROLES | HOST_ROLES
PREPARED_PROCESS_ROLES = {n:n for n in adapter.SOURCE_ROLES}
PREPARED_PROCESS_ROLES.update({n:'adapter' for n in adapter.ENTRIES})
PREPARED_PROCESS_ROLES.update({'adapter.scope_policy':'adapter_scope',
                               'adapter.comparison_contract':'adapter_comparison'})
DEPENDENCY_SOURCE_ROLES = {n:'dependency.'+n for n in comparison.CHILD}
DEPENDENCY_SOURCE_ROLES['closure_manifest'] = 'closure_manifest'
EFFECTS = dict(hypothesis='same_two_primary_gdt_structural_metadata',
    firmware_package_bytes=1024017848, zero_byte_eof_probes=4,
    physical_fdat_envelopes=2000034, logical_decoded_bytes=2040034304,
    dependency_payload_files=351, trusted_origins=5, basis_roles=list(policy.BASIS_ROLES),
    whole_process_memory_cap=False, root_proposals_suppressed=True,
    complete_lineage_before_acceptance=True, automatic_retry=False,
    decompression=False, disassembly=False, secure_erasure_claim=False)
STOP = ['unresolved_decision_no_launch','unknown_role_or_identity_refuse',
        'collision_preserve','dependency_or_cleanup_failure_needs_review',
        'phase_a_failure_no_phase_b','phase_b_failure_no_partial_acceptance',
        'unknown_completion_no_retry_reboot_or_rollback']
FALSE_FLAGS = ('authority_verified','rights_established','execution_authorized',
    'fresh_observation_verified','runtime_qualified','actual_inputs_accessed',
    'feature_supported','recovery_proven','device_write_gate_passed')


def need(ok, code):
    if not ok:
        raise ValueError(code)


def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,
                      allow_nan=False).encode('ascii')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def raw_bytes(raw):
    need(type(raw) is bytes and 0 < len(raw) <= MAX_BYTES, 'observation_buffer_bound')


def decode(raw):
    raw_bytes(raw)
    def pairs(rows):
        result = {}
        for k,v in rows:
            need(k not in result,'observation_duplicate_key');result[k]=v
        return result
    def constant(_):
        raise ValueError('observation_nonfinite')
    try:
        value=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=constant)
        stack=[(value,0)];count=0
        while stack:
            v,depth=stack.pop();count+=1
            need(depth<=32 and count<=200000,'observation_json_bound')
            if type(v) is float:need(math.isfinite(v),'observation_nonfinite')
            if type(v) is dict:stack.extend((x,depth+1) for x in v.values())
            elif type(v) is list:stack.extend((x,depth+1) for x in v)
        return value
    except (UnicodeError,RecursionError) as error:
        raise ValueError('observation_json_encoding_depth') from error


def shape(value, fields, code):
    need(type(value) is dict and set(value)==set(fields),code)


def digest(value):
    need(type(value) is str and len(value)==64 and
         all(c in '0123456789abcdef' for c in value),'observation_digest')


def receipt(raw):
    raw_bytes(raw)
    return dict(bytes=len(raw),sha256=sha(raw))


def check_receipt(value, raw=None):
    shape(value,('bytes','sha256'),'observation_receipt_shape')
    need(type(value['bytes']) is int and 0<value['bytes']<=MAX_BYTES,'observation_receipt_size')
    digest(value['sha256'])
    if raw is not None:need(value==receipt(raw),'observation_original_bytes')


def buffers(value, roles, total=32*1024**2):
    shape(value,roles,'observation_buffer_roster')
    for raw in value.values():raw_bytes(raw)
    need(sum(map(len,value.values()))<=total,'observation_total_bound')


def record(raw, schema, fields, operation):
    value=decode(raw)
    shape(value,set(fields)|{'schema','operation_id','camera_commands'},'observation_record_shape')
    need(value['schema']==schema and value['operation_id']==operation and
         value['camera_commands']==[],'observation_record_mode')
    return value


def equal(left,right,code):
    need(encoded(left)==encoded(right),code)


def absolute(path):
    need(type(path) is str and 0<len(path)<=4096 and
         all(ord(c)>=32 for c in path),'observation_path')
    interpretations=(PurePosixPath(path),PureWindowsPath(path))
    need(any(p.is_absolute() for p in interpretations) and
         all('..' not in p.parts for p in interpretations),'observation_absolute_path')


def evidence(rows):
    need(type(rows) is list and 1<=len(rows)<=16,'observation_evidence')
    for row in rows:check_receipt(row)


def validate_proposal(*, proposal_bytes, request_bytes, ordinary_buffers,
                      source_buffers, retained_comparison_buffers,
                      expected_source_manifest_sha256):
    """Validate roles/expectations, not actual execution or historical truth.

    The six retained buffers are original comparison evidence. Their historical
    gate semantics are NOT rerun here. Dependency config/cache/proof semantics
    use the existing pure binder, never RuntimeOps or an installed dependency.
    The expected source-manifest hash must be selected outside this proposal;
    provenance of that selection is not authenticated by this function.
    """
    buffers(ordinary_buffers,policy.ORDINARY_INPUTS)
    buffers(source_buffers,SOURCE_ROLES,16*1024**2)
    buffers(retained_comparison_buffers,RETAINED)
    request=decode(request_bytes)
    shape(request,('schema','operation_id','source_manifest_sha256','dependency_fixed_sha256',
                   'scope_policy_sha256','result_folder'),'observation_request_shape')
    operation=request['operation_id']
    need(type(operation) is str and len(operation)==32 and
         all(c in '0123456789abcdef' for c in operation),'observation_operation')
    need(request['schema']=='gdt_observation_request_core_v1','observation_request_mode')
    absolute(request['result_folder'])
    for key in ('source_manifest_sha256','dependency_fixed_sha256','scope_policy_sha256'):digest(request[key])
    digest(expected_source_manifest_sha256)
    manifest_raw=ordinary_buffers['authored_source_manifest']
    need(sha(manifest_raw)==request['source_manifest_sha256']==expected_source_manifest_sha256,
         'observation_source_anchor')
    manifest=record(manifest_raw,'gdt_observation_sources_v1',
        ('sources','prepared_sources','dependency_source_roles','prior_dependency_review_sha256'),operation)
    shape(manifest['sources'],SOURCE_ROLES,'observation_source_roster')
    by_path={}
    for role,row in manifest['sources'].items():
        shape(row,('path','bytes','sha256'),'observation_source_row')
        path=row['path']
        need(type(path) is str and 0<len(path)<=1024 and '\\' not in path and ':' not in path
             and all(ord(c)>=32 for c in path),'observation_source_path')
        p=PurePosixPath(path)
        need(not p.is_absolute() and '..' not in p.parts and p.suffix=='.py' and str(p)==path
             and p.parts[0] in ('tools','private') and path.casefold() not in by_path,'observation_source_path')
        check_receipt({k:row[k] for k in ('bytes','sha256')},source_buffers[role])
        by_path[path.casefold()]=(row,source_buffers[role])
    prepared=manifest['prepared_sources'];shape(prepared,adapter.SOURCE_ROLES,'observation_prepared_roster')
    projected={}
    for role,row in prepared.items():
        shape(row,('path','bytes','sha256','entry'),'observation_prepared_row')
        need(type(row['path']) is str and row['path'].casefold() in by_path,'observation_prepared_origin')
        original,raw=by_path[row['path'].casefold()]
        equal({k:row[k] for k in ('path','bytes','sha256')},original,'observation_prepared_identity')
        equal(original,manifest['sources'][PREPARED_PROCESS_ROLES[role]],'observation_prepared_process_role')
        projected[role]=raw
    adapter.check_sources(prepared,projected)
    aliases=manifest['dependency_source_roles']
    equal(aliases,DEPENDENCY_SOURCE_ROLES,'observation_dependency_aliases')
    dep_sources={a:encoded(prepared) if r=='closure_manifest' else projected[r] for a,r in aliases.items()}
    digest(manifest['prior_dependency_review_sha256'])
    fixed_raw=ordinary_buffers['dependency_fixed']
    need(request['dependency_fixed_sha256']==sha(fixed_raw),'observation_fixed_original')
    bound=dependency.bind_runtime_packet(decode(ordinary_buffers['dependency_packet']),decode(fixed_raw),
                                         dep_sources,manifest['prior_dependency_review_sha256'])
    need(bound['expectation']['operation_id']==operation,'observation_dependency_operation')
    for role in RETAINED:
        need(ordinary_buffers[role]==retained_comparison_buffers[role],'observation_retained_original')
    claims=record(ordinary_buffers['authored_source_receipts'],'gdt_observation_source_expectations_v1',
        ('manifest_sha256','receipts','stage','freshness_verified'),operation)
    equal(claims,dict(schema='gdt_observation_source_expectations_v1',operation_id=operation,camera_commands=[],
        manifest_sha256=sha(manifest_raw),receipts={n:receipt(b) for n,b in source_buffers.items()},
        stage='review_expectations_only',freshness_verified=False),'observation_source_expectations')
    scope=record(ordinary_buffers['activity_scope'],'gdt_observation_scope_v1',
        ('request_sha256','limits','effects','stop','historical_blockers'),operation)
    equal(scope,dict(schema='gdt_observation_scope_v1',operation_id=operation,camera_commands=[],
        request_sha256=sha(request_bytes),limits=policy.SCOPE,effects=EFFECTS,stop=STOP,
        historical_blockers=list(policy.HISTORY)),'observation_scope')
    need(request['scope_policy_sha256']==sha(encoded(dict(limits=policy.SCOPE,effects=EFFECTS,stop=STOP))),
         'observation_request_scope')
    rights=record(ordinary_buffers['activity_rights'],'gdt_observation_activity_dispositions_v1',
        ('scope_sha256','owner_facts','decisions'),operation)
    need(rights['scope_sha256']==sha(ordinary_buffers['activity_scope']),'observation_rights_scope')
    equal(rights['owner_facts'],policy.OWNER,'observation_owner')
    shape(rights['decisions'],policy.RIGHTS,'observation_decision_roster')
    for row in rights['decisions'].values():
        shape(row,('disposition','evidence'),'observation_disposition_shape')
        need(type(row['disposition']) is str and row['disposition'] in
             ('pending','allow_scope','deny_scope'),'observation_disposition')
        if row['disposition']=='pending':
            need(row['evidence']==[],'observation_pending_evidence')
        else:evidence(row['evidence'])
    history=record(ordinary_buffers['historical_evidence_index'],'gdt_observation_history_v1',
        ('purpose','original_comparison','basis_roles','historical_blockers'),operation)
    equal(history,dict(schema='gdt_observation_history_v1',operation_id=operation,camera_commands=[],
        purpose='comparison_only',original_comparison={n:receipt(b) for n,b in retained_comparison_buffers.items()},
        basis_roles=list(policy.BASIS_ROLES),historical_blockers=list(policy.HISTORY)),'observation_history')
    index=record(ordinary_buffers['qualification_index'],'gdt_observation_qualification_v1',
        ('ordinary','source_manifest_sha256','evidence','stage','freshness_verified','actual_runtime_verified'),operation)
    expected_rows={n:receipt(b) for n,b in ordinary_buffers.items() if n!='qualification_index'}
    equal(index['ordinary'],expected_rows,'observation_qualification_bytes')
    need(index['source_manifest_sha256']==sha(manifest_raw) and index['stage']=='source_and_synthetic_only'
         and index['freshness_verified'] is False and index['actual_runtime_verified'] is False,'observation_qualification_mode')
    evidence(index['evidence'])
    proposal=record(proposal_bytes,'gdt_observation_proposal_v1',
        ('request_sha256','ordinary','protected_identities','runtime'),operation)
    need(proposal['request_sha256']==sha(request_bytes),'observation_request_bytes')
    equal(proposal['ordinary'],{n:receipt(b) for n,b in ordinary_buffers.items()},'observation_proposal_bytes')
    shape(proposal['protected_identities'],('firmware_package','operational_constants'),'observation_protected_roster')
    for name,row in proposal['protected_identities'].items():
        shape(row,('bytes','sha256'),'observation_protected_identity');digest(row['sha256'])
        need(type(row['bytes']) is int and (row['bytes']==EFFECTS['firmware_package_bytes']
             if name=='firmware_package' else 0<row['bytes']<=65536),'observation_protected_size')
    runtime=proposal['runtime']
    shape(runtime,('interpreter','profile_sha256','bootstrap','argv'),'observation_runtime_shape')
    absolute(runtime['interpreter']);digest(runtime['profile_sha256'])
    need(type(runtime['bootstrap']) is str and 0<len(runtime['bootstrap'])<=128*1024,'observation_bootstrap')
    argv=runtime['argv']
    need(type(argv) is list and len(argv)==10 and all(type(x) is str and 0<len(x)<=128*1024 for x in argv),
         'observation_argv')
    need(argv[:8]==[runtime['interpreter'],'-I','-S','-B','-X','utf8','-c',runtime['bootstrap']]
         and argv[9]==sha(request_bytes),'observation_argv_binding')
    # Acyclic core: no proposal/decision/seal hashes inside the request. Authority
    # is supplied separately, never inserted into a request whose hash it binds.
    win=PureWindowsPath(request['result_folder']).is_absolute()
    path_type=PureWindowsPath if win else PurePosixPath
    absolute(argv[8])
    need(path_type(argv[8])==path_type(request['result_folder'])/'request.json','observation_request_path')
    return dict(schema='gdt_observation_proposal_consistency_v1',operation_id=operation,
        proposal_sha256=sha(proposal_bytes),request_sha256=sha(request_bytes),
        source_manifest_sha256=sha(manifest_raw),
        pending_decisions=sorted(n for n,r in rights['decisions'].items() if r['disposition']=='pending'),
        denied_decisions=sorted(n for n,r in rights['decisions'].items() if r['disposition']=='deny_scope'),
        retained_semantics_revalidated=False,source_roster_completeness_attested=False,
        **dict.fromkeys(FALSE_FLAGS,False),camera_commands=[])


def validate_decided_scope(*, review_bytes, decision_bytes, external_anchor_bytes,
                           expected_external_anchor_sha256, **proposal_arguments):
    """Agree with caller-selected external evidence; do not authenticate it.

    Accepted dispositions can be represented without invented/pending-only
    schemas. This is NOT operational acceptance and cannot dispatch execution.
    """
    result=validate_proposal(**proposal_arguments);operation=result['operation_id']
    need(not result['pending_decisions'] and not result['denied_decisions'],'observation_undecided')
    review=record(review_bytes,'gdt_observation_review_v1',('proposal_sha256','outcome','evidence'),operation)
    need(review['proposal_sha256']==result['proposal_sha256'] and review['outcome']=='accepted_scope',
         'observation_review_binding');evidence(review['evidence'])
    decision=record(decision_bytes,'gdt_observation_decision_v1',
        ('proposal_sha256','review_sha256','activity_rights_sha256','outcome'),operation)
    equal(decision,dict(schema='gdt_observation_decision_v1',operation_id=operation,camera_commands=[],
        proposal_sha256=result['proposal_sha256'],review_sha256=sha(review_bytes),
        activity_rights_sha256=sha(proposal_arguments['ordinary_buffers']['activity_rights']),
        outcome='allow_scope'),'observation_decision_binding')
    digest(expected_external_anchor_sha256)
    raw_bytes(external_anchor_bytes)
    need(sha(external_anchor_bytes)==expected_external_anchor_sha256,'observation_external_anchor')
    anchor=record(external_anchor_bytes,'gdt_observation_external_decision_v1',
        ('proposal_sha256','request_sha256','review_sha256','decision_sha256','outcome','evidence'),operation)
    for name,value in (('proposal_sha256',result['proposal_sha256']),('request_sha256',result['request_sha256']),
                       ('review_sha256',sha(review_bytes)),('decision_sha256',sha(decision_bytes))):
        need(anchor[name]==value,'observation_external_binding')
    need(anchor['outcome']=='allow_scope','observation_external_outcome');evidence(anchor['evidence'])
    return dict(result,schema='gdt_observation_decided_consistency_v1',
        status='decided_scope_consistency_only',external_anchor_sha256=expected_external_anchor_sha256)


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
