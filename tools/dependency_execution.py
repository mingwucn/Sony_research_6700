"""Prospective dependency input transition and pure saved-record verification.

Runtime activation requires a separately reviewed exact-buffer child packet.
Caller records establish consistency only, never execution permission or truth.
"""
import copy
import json

from tools import dependency_evidence as core
from tools import dependency_producer as producer


ARTIFACTS = ('expectation.json', 'binding.json', 'journal.jsonl', 'raw.json',
             'audit-acknowledgement.json', 'result.json')


def prepare_texts(*, operation_id, vectors, sources):
    """Explicit prospective text inputs, not an implicit historical-cache adapter.

    Original text encoding/digests are the caller's separate evidence. These new
    canonical documents do not inherit historical approval or observation status.
    """
    vectors = core._bounded_copy(vectors)
    core._need(core._hash(vectors) == producer.PUBLIC_PLAN_SHA256, 'public_plan')
    core._shape(sources, producer.ALIASES)
    total = 0; escaped_size = len(core._canonical(dict(schema='prospective_dependency_source_cache_v1',sources={})))+1
    for index,(alias,value) in enumerate(sources.items()):
        core._need(type(value) is str, 'source_text')
        core._need(len(value) <= 1024**2, 'cache_bound')
        byte_size=0; string_size=2
        for char in value:
            point=ord(char)
            core._need(not 0xD800<=point<=0xDFFF,'source_text')
            byte_size+=1 if point<128 else 2 if point<2048 else 3 if point<65536 else 4
            string_size+=2 if char in '\"\\\b\f\n\r\t' else 6 if point<32 or 127<=point<=65535 else 12 if point>65535 else 1
        total+=byte_size
        escaped_size+=len(core._canonical(alias))+1+string_size+(1 if index else 0)
        core._need(byte_size<=1024**2 and total<=4*1024**2 and escaped_size<=4*1024**2,'cache_bound')
    # Validate the operation using the same predicate as the closed policy.
    core._need(type(operation_id) is str and 1 <= len(operation_id) <= 96 and
               all(c.isascii() and (c.isalnum() or c in '_-') for c in operation_id), 'operation')
    config = producer.encoded(dict(schema='prospective_dependency_config_v1',
        operation_id=operation_id, vectors=vectors)).decode('ascii')
    cache = producer.encoded(dict(schema='prospective_dependency_source_cache_v1',
        sources=sources)).decode('ascii')
    core._text_bytes(config); core._text_bytes(cache)
    return dict(config_json=config, cache_json=cache,
        config_file_sha256=producer.sha(config.encode('utf-8')),
        cache_file_sha256=producer.sha(cache.encode('utf-8')),
        config_object_sha256=core._hash(core._json_text(config)),
        cache_object_sha256=core._hash(core._json_text(cache)))


def bind_collection(*, collection, inputs, evidence_mode='invented', test_injection_used=True):
    """Pure revalidation and deterministic proof transition, no file observation.

    A declared record mode never proves actual observation. Retain original input
    and receipt hashes; changing a proof binding creates no independent approval.
    """
    policy, package, binding, _, _ = producer.bind_inputs(**inputs)
    core._need(type(test_injection_used) is bool and (evidence_mode,test_injection_used) in
               (('invented',True),('saved_records',False)), 'collection_mode')
    core._shape(collection, ('schema','status','evidence_mode','prior_package_sha256',
        'observed_package_sha256','package','absolute_receipts','relative_projection',
        'trusted_origins','root_before','root_after','source_aliases','raw_cache_sha256',
        'package_reads','trusted_reads','test_injection_used','dependency_bootstrap_performed',
        'actual_installation_observed','atomic_snapshot_proven','operational_acceptance',
        'execution_authorized','feature_supported','recovery_proven','device_write_gate_passed','camera_commands'))
    # Detach groups with independently bounded contracts instead of one oversized
    # aggregate node budget for both absolute and projected 351-file rosters.
    fresh = core._bounded_copy(collection['package'])
    absolute = core._bounded_copy(collection['absolute_receipts'])
    projected = core._bounded_copy(collection['relative_projection'])
    trusted = core._bounded_copy(collection['trusted_origins'])
    roots = core._bounded_copy([collection['root_before'], collection['root_after']])
    core._need(collection['schema']=='dependency_package_collection_v1' and
               collection['status']==('complete_invented_package_collection' if test_injection_used else 'complete_package_collection') and
               collection['evidence_mode']==evidence_mode and collection['test_injection_used'] is test_injection_used,
               'collection_mode')
    core._need(collection['actual_installation_observed'] is (not test_injection_used), 'collection_authority')
    for key in ('dependency_bootstrap_performed','atomic_snapshot_proven',
                'operational_acceptance','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed'):
        core._need(collection[key] is False, 'collection_authority')
    core._need(collection['camera_commands']==[], 'collection_authority')
    core._need(type(collection['package_reads']) is int and collection['package_reads']==351 and
               type(collection['trusted_reads']) is int and collection['trusted_reads']==5, 'collection_counts')
    core._need(collection['source_aliases']==sorted(producer.ALIASES) and
               collection['raw_cache_sha256']==policy['cache_sha256'], 'collection_sources')
    core._need(collection['prior_package_sha256']==core._hash(package) and
               collection['observed_package_sha256']==core._hash(fresh), 'collection_binding')
    manifest, receipts = core._package(fresh)
    core._need(core._canonical(manifest)==core._canonical(package['manifest']), 'manifest_changed')
    core._shape(absolute, manifest['files']); core._shape(projected, manifest['files'])
    core._need(all(row['size']<=8*1024**2 for group in
               (manifest['files'],policy['trusted_origins']) for row in group.values()), 'package_read_bound')
    for relative, expected in manifest['files'].items():
        identity = {k:package['installed_receipts'][relative]['lstat_before'][k] for k in core.CROSS}
        path = policy['roots']['package']['path'].rstrip('/')+'/'+relative
        row = absolute[relative]
        core._receipt(row,path,expected['sha256'],expected['size'],identity)
        core._need(core._canonical(dict(receipts[relative],path=path))==core._canonical(row), 'receipt_projection')
        core._need(core._canonical(projected[relative])==core._canonical(dict(
            absolute_receipt_sha256=core._hash(row),relative_receipt_sha256=core._hash(receipts[relative]))), 'projection_hash')
    core._shape(trusted, producer.TRUSTED)
    for name, expected in policy['trusted_origins'].items():
        core._receipt(trusted[name],producer.target(policy,expected),expected['sha256'],expected['size'],expected['identity'])
    for rootset in roots:
        core._shape(rootset,policy['roots'])
        core._need({k:core._hash(v) for k,v in rootset.items()}==
                   {k:v['identity_sha256'] for k,v in policy['roots'].items()}, 'root_identity')
    observed_policy = copy.deepcopy(policy)
    observed_policy['installed_proof_sha256'] = core._hash(fresh['installed_proof'])
    observed_binding = dict(binding,expectation_sha256=core._hash(observed_policy),package_sha256=core._hash(fresh))
    observed_inputs = dict(copy.deepcopy(inputs),expectation=observed_policy,package=fresh,binding=observed_binding)
    producer.bind_inputs(**observed_inputs)
    transition = dict(schema='dependency_fresh_proof_transition_v1',
        original_expectation_sha256=core._hash(policy),original_package_sha256=core._hash(package),
        original_binding_sha256=core._hash(binding),collection_sha256=core._hash(collection),
        observed_expectation_sha256=core._hash(observed_policy),observed_package_sha256=core._hash(fresh),
        observed_binding_sha256=core._hash(observed_binding),review_sha256=binding['review_sha256'],
        changed_policy_fields=[k for k in policy if policy[k]!=observed_policy[k]],test_injection_used=test_injection_used,
        independent_approval_created=False,execution_authorized=False,camera_commands=[])
    return observed_inputs, transition


def produce_collected_invented(*, inputs, ops, folder):
    """Qualification of collector→transition→producer→saved verifier composition.

    No real observer accepted. The eventual bound child must execute the complete
    source closure and preserve this ordering with a separately qualified route.
    """
    core._need(not isinstance(ops,producer.RuntimeOps),'real_activation_pending')
    return _produce_collected(inputs=inputs,ops=ops,folder=folder,invented=True)


def produce_collected_runtime(*, inputs, folder):
    """Bound-child runtime branch. Calling this API is not consent or authority.

    No custom observer or callback accepted. A reviewed exact activation packet
    and independent current expectations are prerequisites, not supplied here.
    """
    return _produce_collected_runtime(inputs=inputs, folder=folder)


def _produce_collected_runtime(*, inputs, folder, continuation=None):
    """Internal composition seam; the concrete observer is always constructed here.

    A continuation belongs to reviewed authored code, not a runtime packet or
    observer supplied by an entry caller. This function is not an authority check.
    The controller's public runtime entry remains disabled.
    """
    core._need(continuation is None or callable(continuation), 'controller_continuation')
    core._need(producer.os.name=='nt' and producer.sys.implementation.name=='cpython','runtime_platform')
    core._need(producer.sys.flags.isolated==1 and producer.sys.flags.no_site==1 and
        producer.sys.flags.no_user_site==1 and producer.sys.dont_write_bytecode is True and
        producer.sys.flags.optimize==0,'runtime_flags')
    core._need(not any(n.split('.')[0] in ('ctypes','_ctypes','platform','cffi','_cffi_backend','pycparser','Cryptodome')
        for n in producer.sys.modules),'preloaded_runtime_origin')
    kwargs = {} if continuation is None else dict(continuation=continuation)
    return _produce_collected(inputs=inputs,ops=producer.RuntimeOps(),folder=folder,invented=False,**kwargs)


def _produce_collected(*, inputs, ops, folder, invented, continuation=None):
    from tools import dependency_package_preflight as collector
    core._need(type(invented) is bool,'collection_mode')
    core._need(continuation is None or callable(continuation), 'controller_continuation')
    mode='invented' if invented else 'saved_records'
    core._shape(inputs,('expectation','package','binding','config_json','cache_json','source_buffers'))
    policy,package,binding,_,_=producer.bind_inputs(**inputs)
    inputs=dict(expectation=policy,package=package,binding=binding,
        config_json=inputs['config_json'],cache_json=inputs['cache_json'],source_buffers=dict(inputs['source_buffers']))
    output=producer.Outputs(folder);output.folder.mkdir(exist_ok=False)
    stage='collection'
    output.small('started.json',dict(schema='dependency_collection_producer_started_v1',
        expectation_sha256=core._hash(inputs['expectation']),package_sha256=core._hash(inputs['package']),
        test_injection_used=invented,automatic_retry=False,execution_authorized=False,camera_commands=[]))
    try:
        collection=collector._collect(ops=ops,inputs=inputs,invented=invented)
        stage='transition';observed,transition=bind_collection(collection=collection,inputs=inputs,
            evidence_mode=mode,test_injection_used=invented)
        output.small('collection.json',collection);output.small('transition.json',transition)
        stage='producer'
        producer._produce(**observed,ops=ops,folder=str(output.folder/'producer'),invented=invented,
                          continuation=continuation)
        stage='verification'
        core._need(set(p.name for p in (output.folder/'producer').iterdir())==set(ARTIFACTS),'artifact_roster')
        artifacts={name:producer.read_verified(str(output.folder/'producer'/name),limit=4*1024**2)[0]
                   for name in ARTIFACTS}
        verification=verify_records(artifacts=artifacts,inputs=observed,
            evidence_mode=mode,test_injection_used=invented)
        output.small('verification.json',verification)
        completion=completion_record(collection,transition,verification,invented=invented)
        stage='completion';output.small('completion.json',completion)
        return completion
    except BaseException as primary:
        # Do not overwrite a possibly completed outcome, replay a callback or
        # attempt recovery. A failed publication requires existing-state review.
        if stage!='completion':
            try:
                output.small('completion.json',dict(schema='dependency_collection_producer_completion_v1',
                    status='needs_review',failed_stage=stage,test_injection_used=invented,automatic_retry=False,
                    execution_authorized=False,camera_commands=[]))
            except BaseException as publication:
                raise primary from publication
        raise


def completion_record(collection, transition, verification, *, invented):
    return dict(schema='dependency_collection_producer_completion_v1',
        status='complete_invented_composition' if invented else 'complete_dependency_composition',
        collection_sha256=core._hash(collection),transition_sha256=core._hash(transition),
        verification_sha256=core._hash(verification),test_injection_used=invented,automatic_retry=False,
        actual_dependency_observation_performed=not invented,execution_authorized=False,feature_supported=False,
        recovery_proven=False,device_write_gate_passed=False,camera_commands=[])


def bind_runtime_packet(value, fixed, source_buffers, review_sha256):
    """Closed prospective runtime packet. No invented contents/observers allowed."""
    core._shape(value,('schema','inputs'))
    core._need(value['schema']=='runtime_dependency_packet_v1','packet_mode')
    data=value['inputs']
    core._shape(data,('expectation','package','binding','config_json','cache_json'))
    policy,package,binding,_,_=producer.bind_inputs(**data,source_buffers=source_buffers)
    core._shape(fixed,('expectation_sha256','package_sha256','root_sha256'))
    expected=dict(expectation_sha256=core._hash(policy),package_sha256=core._hash(package),
        root_sha256={k:row['identity_sha256'] for k,row in policy['roots'].items()})
    core._need(core._canonical(fixed)==core._canonical(expected),'fixed_expectations')
    core._need(binding['review_sha256']==review_sha256,'review_binding')
    return dict(expectation=policy,package=package,binding=binding,
        config_json=data['config_json'],cache_json=data['cache_json'],source_buffers=dict(source_buffers))


def validate_saved_composition(folder, inputs, *, invented):
    """Independent parent metadata reread/recomputation; no dependency execution."""
    from pathlib import Path
    core._need(type(invented) is bool,'collection_mode')
    folder=Path(folder)
    names=('started.json','collection.json','transition.json','verification.json','completion.json')
    core._need(set(p.name for p in folder.iterdir())==set(names)|{'producer'},'composition_roster')
    raw={name:producer.read_verified(str(folder/name),limit=4*1024**2)[0] for name in names}
    rows={name:core._json_text(buf.decode('utf-8')) for name,buf in raw.items()}
    expected_start=dict(schema='dependency_collection_producer_started_v1',
        expectation_sha256=core._hash(inputs['expectation']),package_sha256=core._hash(inputs['package']),
        test_injection_used=invented,automatic_retry=False,execution_authorized=False,camera_commands=[])
    core._need(core._canonical(rows['started.json'])==core._canonical(expected_start),'saved_start')
    mode='invented' if invented else 'saved_records'
    observed,transition=bind_collection(collection=rows['collection.json'],inputs=inputs,
        evidence_mode=mode,test_injection_used=invented)
    core._need(core._canonical(rows['transition.json'])==core._canonical(transition),'saved_transition')
    core._need(set(p.name for p in (folder/'producer').iterdir())==set(ARTIFACTS),'artifact_roster')
    producer_raw={name:producer.read_verified(str(folder/'producer'/name),limit=4*1024**2)[0] for name in ARTIFACTS}
    verification=verify_records(artifacts=producer_raw,inputs=observed,evidence_mode=mode,test_injection_used=invented)
    core._need(core._canonical(rows['verification.json'])==core._canonical(verification),'saved_verification')
    expected_completion=completion_record(rows['collection.json'],transition,verification,invented=invented)
    core._need(core._canonical(rows['completion.json'])==core._canonical(expected_completion),'saved_completion')
    return dict({name:producer.sha(buf) for name,buf in raw.items()},
                **{'producer/'+name:producer.sha(buf) for name,buf in producer_raw.items()})


def verify_records(*, artifacts, inputs, evidence_mode, test_injection_used):
    """Pure strict parent-side records check; runtime observations not replayed.

    The saved_records grammar is qualified with invented records only. Matching
    flags cannot authenticate the executing producer or historical observations.
    """
    core._need((evidence_mode,test_injection_used) in (('invented',True),('saved_records',False)) and
               type(test_injection_used) is bool, 'record_mode')
    policy,package,binding,_,_ = producer.bind_inputs(**inputs)
    core._shape(artifacts,ARTIFACTS)
    for raw in artifacts.values():
        core._need(type(raw) is bytes and len(raw)<=4*1024**2,'artifact_bound')
    rows={name:core._json_text(raw.decode('utf-8')) for name,raw in artifacts.items() if name!='journal.jsonl'}
    core._need(core._canonical(rows['expectation.json'])==core._canonical(policy) and
               core._canonical(rows['binding.json'])==core._canonical(binding),'saved_binding')
    result=rows['result.json']
    core._shape(result,('schema','status','observation','consistency','source_execution_trace',
        'test_injection_used','audit_hook_retained_inert','audit_hook_acknowledged',
        'audit_acknowledgement_is_invented','source_buffers_are_caller_supplied',
        'executing_producer_authenticated','prior_binding_is_caller_declaration',
        'operational_acceptance','execution_authorized','feature_supported','recovery_proven',
        'device_write_gate_passed','camera_commands'))
    expected=dict(result,schema='prospective_dependency_producer_result_v1',status='produced_consistent_dependency_records',
        test_injection_used=test_injection_used,audit_hook_retained_inert=True,audit_hook_acknowledged=True,
        audit_acknowledgement_is_invented=test_injection_used,source_buffers_are_caller_supplied=True,
        executing_producer_authenticated=False,prior_binding_is_caller_declaration=True,
        operational_acceptance=False,execution_authorized=False,feature_supported=False,recovery_proven=False,
        device_write_gate_passed=False,camera_commands=[])
    core._need(core._canonical(result)==core._canonical(expected),'result_flags')
    core._need(result['observation']['evidence_mode']==evidence_mode,'record_mode')
    consistency=core.validate_dependency_records(expectation=policy,package=package,
        observation=result['observation'],raw_receipt_json=artifacts['raw.json'].decode('utf-8'),
        journal_jsonl=artifacts['journal.jsonl'].decode('utf-8'))
    core._need(core._canonical(result['consistency'])==core._canonical(consistency),'saved_consistency')
    trace=result['source_execution_trace']; starts={}; ends={};stack=[]
    core._need(type(trace) is list and len(trace)==22,'source_trace')
    for row in trace:
        core._shape(row,('alias','stage','sha256'));alias=row['alias']
        core._need(type(alias) is str and alias in policy['python_origins'] and
                   row['sha256']==policy['python_origins'][alias]['sha256'],'source_trace')
        if row['stage']=='source_execute_intent':
            core._need(alias not in starts,'source_trace');starts[alias]=row;stack.append(alias)
        else:
            core._need(row['stage']=='source_execute_complete' and stack and stack[-1]==alias and alias not in ends,'source_trace')
            stack.pop();ends[alias]=row
    core._need(not stack and set(starts)==set(ends)==set(producer.ALIASES),'source_trace')
    core._need(list(ends)==[r['data']['alias'] for r in result['observation']['events'] if r['event']=='python_import'],'source_trace_order')
    ack=rows['audit-acknowledgement.json']
    core._shape(ack,('schema','operation_id','probe_event','probe_token','acknowledged','test_injection_used'))
    token=ack['probe_token']
    core._need(type(token) is str and len(token)==32 and all(c in '0123456789abcdef' for c in token),'audit_token')
    core._need(core._canonical(ack)==core._canonical(dict(schema='dependency_audit_acknowledgement_v1',
        operation_id=policy['operation_id'],probe_event=producer.PROBE_EVENT,probe_token=token,
        acknowledged=True,test_injection_used=test_injection_used)),'audit_acknowledgement')
    return dict(schema='dependency_saved_records_verification_v1',status='consistent_caller_records',
        artifact_sha256={name:producer.sha(raw) for name,raw in artifacts.items()},
        expectation_sha256=core._hash(policy),package_sha256=core._hash(package),
        evidence_mode=evidence_mode,test_injection_used=test_injection_used,
        producer_execution_authenticated=False,actual_runtime_verified=False,
        historical_truth_verified=False,execution_authorized=False,feature_supported=False,
        recovery_proven=False,device_write_gate_passed=False,camera_commands=[])


def main():
    print(json.dumps(dict(status='needs_review',code='real_activation_pending',camera_commands=[])))
    return 2


if __name__=='__main__':raise SystemExit(main())
