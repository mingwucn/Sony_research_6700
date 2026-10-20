"""Disabled observation transport and owned retained supervision.

The initial host/interpreter/environment are trusted. Captured source is not
self-authentication, and consistent decision records are not human consent.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import types

ENV = 'A6700_OBSERVATION_PACKET_SHA256'
ADDED = 'observation.launcher'
LIMIT = 32*1024**2
FALSE = ('execution_authorized','feature_supported','recovery_proven','device_write_gate_passed')
# Trusted finite policy, checked before any captured validator executes.
RETAINED = ('acceptance','link_acceptance','member_acceptance','metadata_preflight',
    'expanded_gate','ext_superblock','ext_preflight','ext_read_planner','ext_gate',
    'gdt_preflight','gdt_cleanup','gdt_gate','gdt_adapter','gdt_runner','prefix',
    'offline_inventory','artifact_probe','classifier','tar_inventory','metadata_tar',
    'member_prefix','header_candidates','io_adapter','validator','capture','core')
DEPENDENCIES = ('dependency_evidence','dependency_producer','dependency_package_preflight',
    'dependency_execution','dependency_controller','dependency_parent')
CAPTURE_ROLES = frozenset({'bound.role:'+n for n in RETAINED} |
    {'bound.bootstrap:activation_binding','bound.bootstrap:io_entry','bound.integration:prospective_child'} |
    {'dependency.'+n for n in DEPENDENCIES} |
    {'adapter','adapter_scope','adapter_comparison','namespace','successor_wiring',
     'host_entry','retained_gate','ordinary_io','operational_metadata','operational_entry',
     'operational_preparation','adapter_loader','outer_loader','process_child',
     'host.launcher','host.bootstrap_and_supervisor','observation.contract','observation.outer',ADDED})


def need(ok, code):
    if not ok:raise ValueError(code)


def encoded(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')


def sha(raw):return hashlib.sha256(raw).hexdigest()


def strict(raw):
    need(type(raw) is bytes and 0<len(raw)<=LIMIT,'observation_launch_bound')
    def pairs(rows):
        result={}
        for k,v in rows:
            need(k not in result,'observation_launch_duplicate');result[k]=v
        return result
    value=json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:need(False,'observation_launch_nonfinite'))
    stack=[(value,0)];nodes=0
    while stack:
        v,depth=stack.pop();nodes+=1
        need(depth<=32 and nodes<=200000,'observation_launch_json_bound')
        if type(v) is dict:stack.extend((x,depth+1) for x in v.values())
        elif type(v) is list:stack.extend((x,depth+1) for x in v)
    return value


def wire(value):
    if type(value) is bytes:return {'$bytes':base64.b64encode(value).decode('ascii')}
    if type(value) is dict:
        need('$bytes' not in value,'observation_launch_reserved_tag')
        return {k:wire(v) for k,v in value.items()}
    if type(value) is list:return [wire(v) for v in value]
    return value


def unwire(value):
    if type(value) is dict:
        if '$bytes' in value:
            need(set(value)=={'$bytes'} and type(value['$bytes']) is str,'observation_launch_tag')
            raw=base64.b64decode(value['$bytes'],validate=True)
            need(0<len(raw)<=4*1024**2,'observation_launch_tag_bound')
            return raw
        return {k:unwire(v) for k,v in value.items()}
    if type(value) is list:return [unwire(v) for v in value]
    return value


class Library:
    """Private three-module host/child library, with no tools publication."""
    def __init__(self,buffers):
        self.closed=False;self.modules={};self.package=types.ModuleType('_observation_tools')
        self.buffers=buffers

    def load(self):
        import builtins
        def importer(name,globals=None,locals=None,fromlist=(),level=0):
            need(level==0,'observation_launch_import')
            if name=='tools':
                need(fromlist and all(n in self.modules for n in fromlist),'observation_launch_import')
                return self.package
            need(name.split('.')[0] in {'base64','hashlib','json','os','pathlib','stat','subprocess','sys','time','types'},
                 'observation_launch_import')
            return builtins.__import__(name,globals,locals,fromlist,level)
        try:
            for name,role in (('dependency_child_entry','host.bootstrap_and_supervisor'),
                ('dependency_operational_child','process_child'),('dependency_operational_launcher','host.launcher')):
                module=types.ModuleType('_observation_'+name)
                module.__builtins__=dict(vars(builtins),__import__=importer)
                exec(compile(self.buffers[role],'<observation-library:'+name+'>','exec',dont_inherit=True,optimize=0),vars(module))
                self.modules[name]=module;setattr(self.package,name,module)
            return self
        except BaseException:
            self.close();raise

    @property
    def pending(self):return self.modules['dependency_operational_launcher']

    def close(self):
        need(not self.closed,'observation_launch_library_reclose');self.closed=True
        self.modules.clear();vars(self.package).clear();self.buffers=None
        return True


def observation_module(buffers):
    module=types.ModuleType('_captured_observation_outer')
    exec(compile(buffers['observation.outer'],'<observation-outer>','exec',dont_inherit=True,optimize=0),vars(module))
    return module


def validate_capture(buffers,expected):
    need(type(buffers) is dict and type(expected) is dict and
        set(buffers)==set(expected)==CAPTURE_ROLES,'observation_launch_capture')
    total=0
    for name,raw in buffers.items():
        need(type(raw) is bytes and 0<len(raw)<=4*1024**2 and sha(raw)==expected[name],
             'observation_launch_source')
        total+=len(raw)
    need(total<=20*1024**2,'observation_launch_capture_bound')
    # Outside expected hashes and the initial host are trusted, not self-authenticated.
    outer=observation_module(buffers)
    need(set(buffers)==outer.CAPTURE_ROLES|{ADDED},'observation_launch_capture')
    return outer


def pending_projection(arguments,folder,pending,repository_root):
    """Exact fourteen-role rehearsal projection; never converts rights to consent.

    The operational engine keeps its existing pending grammar. Its pending
    records describe the rehearsal, while observation dispositions remain
    separate original inputs to the captured observation preflight.
    """
    a=arguments['proposal_arguments'];ordinary=a['ordinary_buffers']
    manifest=strict(ordinary['authored_source_manifest']);core=strict(a['request_bytes'])
    scope=strict(ordinary['activity_scope']);rights=strict(ordinary['activity_rights'])
    by_path={r['path']:a['source_buffers'][n] for n,r in manifest['sources'].items()}
    checked={n:by_path[r['path']] for n,r in manifest['prepared_sources'].items()}
    request=dict(schema='prepared_gdt_adapter_request_v1',operation_id=core['operation_id'],
        scope=scope['limits'],sources=manifest['prepared_sources'],
        dependency_packet=strict(ordinary['dependency_packet']),dependency_fixed=strict(ordinary['dependency_fixed']),
        dependency_review_sha256=manifest['prior_dependency_review_sha256'],folder=str(Path(folder)/'composition'),
        decisions=dict.fromkeys(rights['decisions'],'pending'),execution_authorized=False,camera_commands=[])
    docs=arguments['legacy_documents']
    originals={n:docs[n] for n in ('candidate','review','decision','seal')}
    originals.update({'input:'+n:b for n,b in docs['inputs'].items()})
    receipt=lambda b:dict(bytes=len(b),sha256=sha(b))
    receipts=lambda bs:{n:receipt(b) for n,b in bs.items()}
    original_rows=receipts(originals)
    outer_rows={n:receipt(a['source_buffers'][role]) for n,role in pending.process.OUTER.items()}
    def row(schema,**kw):return encoded(dict(schema=schema,operation_id=core['operation_id'],camera_commands=[],**kw))
    result={n:ordinary[n] for n in ('basis','source_manifest','prerequisites','binding_plan','role_authority','binding_schema')}
    closure=encoded(request['sources'])
    result['authored_source_manifest']=row('pending_operational_sources_v1',prepared_sources=request['sources'],
        outer_sources=outer_rows,derived=dict(closure_manifest=dict(kind='canonical_prepared_source_map_v1',**receipt(closure))))
    result['authored_source_receipts']=row('pending_operational_source_byte_claims_v1',
        manifest_sha256=sha(result['authored_source_manifest']),prepared=receipts(checked),outer=outer_rows,source_reads_observed=False)
    result['dependency_packet']=ordinary['dependency_packet'];result['dependency_fixed']=ordinary['dependency_fixed']
    result['activity_scope']=row('pending_operational_scope_v1',purpose='prepare_only_no_operational_act',
        request_bytes_sha256=sha(encoded(request)),limits=scope['limits'],originals=original_rows,
        sources_sha256=sha(result['authored_source_manifest']),historical_blockers=scope['historical_blockers'])
    result['activity_rights']=row('pending_operational_rights_v1',scope_sha256=sha(result['activity_scope']),
        owner_facts=rights['owner_facts'],decisions=dict.fromkeys(rights['decisions'],'pending'),
        legal_basis_established=False,execution_authorized=False)
    result['historical_evidence_index']=row('pending_operational_history_v1',purpose='comparison_only',original_inputs=receipts(docs['inputs']))
    result['qualification_index']=row('pending_operational_consistency_index_v1',ordinary=receipts(result),
        checked_roles=sorted(ordinary),execution_authenticated=False,freshness_verified=False)
    b64=lambda b:base64.b64encode(b).decode('ascii')
    return dict(schema='pending_operational_outer_packet_v1',documents={n:b64(docs[n]) for n in ('candidate','review','decision','seal')}|
        {'inputs':{n:b64(b) for n,b in docs['inputs'].items()}},reference_pins=arguments['legacy_reference_pins'],
        seal_sha256=arguments['legacy_expected_seal_sha256'],request_bytes=b64(encoded(request)),request_sha256=sha(encoded(request)),
        checked={n:b64(b) for n,b in checked.items()},original_receipts=original_rows,
        ordinary={n:b64(b) for n,b in result.items()},ordinary_receipts=receipts(result),
        repository_root=str(repository_root))


def check(arguments,buffers,expected,rows,folder,repository_root,profile):
    outer=validate_capture(buffers,expected)
    captures={n:b for n,b in buffers.items() if n!=ADDED}
    need(arguments['capture_buffers']==captures and arguments['expected_capture_hashes']=={n:expected[n] for n in captures},
         'observation_launch_original_capture')
    result=outer.preflight(**arguments)
    lib=Library(buffers).load()
    try:
        pending=lib.pending
        process_buffers={n:buffers[n] for n in pending.process.ROSTER}
        pending.validate_capture(process_buffers,rows,{n:expected[n] for n in process_buffers})
        a=arguments['proposal_arguments'];core=strict(a['request_bytes']);proposal=strict(a['proposal_bytes'])
        need(Path(core['result_folder'])==Path(folder)/'review','observation_launch_review_folder')
        runtime=proposal['runtime']
        need(runtime['profile_sha256']==sha(encoded(profile)) and runtime['interpreter']==profile['executable'],
             'observation_launch_profile')
        manifest=strict(a['ordinary_buffers']['authored_source_manifest'])
        for n in process_buffers:
            need(process_buffers[n]==a['source_buffers'][n] and
                Path(repository_root)/manifest['sources'][n]['path']==Path(rows[n]['path']),
                 'observation_launch_projection_origin')
        packet=pending_projection(arguments,folder,pending,repository_root)
        return result,packet
    finally:lib.close()


def bootstrap():
    # Independent of every proposal/decision/packet digest: no authority cycle.
    from tools import dependency_child_entry as entry
    prefix=entry.BOOTSTRAP.split('try:\n need(len(sys.argv)==3',1)[0]
    body=r'''
try:
 need(len(sys.argv)==3,'arguments')
 token=os.environ.get('A6700_OBSERVATION_PACKET_SHA256')
 need(type(token) is str and len(token)==64 and all(c in '0123456789abcdef' for c in token),'observation_transport_environment')
 core,_=read(sys.argv[1],4*1024**2);need(digest(core)==sys.argv[2],'observation_core_hash')
 request=json.loads(core,object_pairs_hook=pairs);folder=Path(request['result_folder'])
 need(folder.is_absolute() and '..' not in folder.parts and Path(sys.argv[1])==folder/'request.json','observation_core_path')
 packet,_=read(str(folder/'transport.json'),32*1024**2);need(digest(packet)==token,'observation_transport_hash')
 transport=json.loads(packet,object_pairs_hook=pairs)
 row=transport['launcher'];raw=__import__('base64').b64decode(row['bytes'],validate=True)
 need(0<len(raw)<=4*1024**2 and digest(raw)==row['sha256'],'observation_launcher_hash')
 original=transport['inputs']['buffers']['observation.launcher']
 need(type(original) is dict and set(original)=={'$bytes'},'observation_launcher_original')
 need(raw==__import__('base64').b64decode(original['$bytes'],validate=True) and
  row['sha256']==transport['inputs']['expected']['observation.launcher'],'observation_launcher_original')
 rows=transport['inputs']['rows'];need(type(rows) is dict and set(rows)==set(PROCESS_ROLES),'observation_process_roster')
 def canon(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
 total=0
 for name,source_row in rows.items():
  need(type(source_row) is dict and set(source_row)=={'path','size','sha256','lstat','fstat'},'observation_source_row')
  path=Path(source_row['path']);need(path.is_absolute() and '..' not in path.parts and path.suffix=='.py','observation_source_path')
  data,seen=read(str(path),2*1024**2);need(canon(seen)==canon(source_row),'observation_source_binding')
  tagged=transport['inputs']['buffers'][name]
  need(type(tagged) is dict and set(tagged)=={'$bytes'} and data==__import__('base64').b64decode(tagged['$bytes'],validate=True) and
   digest(data)==transport['inputs']['expected'][name],'observation_source_original')
  total+=len(data);need(total<=16*1024**2,'observation_source_bound')
  compile(data,'<checked-observation-source:'+name+'>','exec',dont_inherit=True,optimize=0)
 worker=types.ModuleType('_observation_worker')
 exec(compile(raw,'<captured-observation-launcher>','exec',dont_inherit=True,optimize=0),vars(worker))
 raise SystemExit(worker.child(core,packet,token,sys.orig_argv))
except SystemExit:raise
except BaseException:
 print(json.dumps(dict(status='needs_review',camera_commands=[])))
 raise SystemExit(2)
'''
    process_roles=CAPTURE_ROLES-{'host.launcher','host.bootstrap_and_supervisor','observation.contract','observation.outer',ADDED}
    return prefix+body.replace('PROCESS_ROLES',repr(sorted(process_roles)))


def child(core,packet_raw,transport_sha,argv):
    need(sha(packet_raw)==transport_sha,'observation_launch_transport')
    transport=strict(packet_raw)
    need(set(transport)=={'schema','launcher','inputs'} and transport['schema']=='disabled_observation_transport_v1',
         'observation_launch_transport_schema')
    value=unwire(transport['inputs'])
    need(set(value)=={'arguments','buffers','expected','rows','folder','repository_root','profile','pending_request'},
         'observation_launch_transport_fields')
    a=value['arguments']['proposal_arguments']
    need(core==a['request_bytes'],'observation_launch_core_original')
    runtime=value['arguments']['runtime_expectation']
    need(argv==runtime['argv'] and os.environ.get(ENV)==transport_sha,'observation_launch_command')
    profile=dict(implementation=sys.implementation.name,version=list(sys.version_info[:3]),version_text=sys.version,
        cache_tag=sys.implementation.cache_tag,executable=sys.executable,base_executable=getattr(sys,'_base_executable',sys.executable),
        prefix=sys.prefix,base_prefix=sys.base_prefix,platform=sys.platform,maxsize=sys.maxsize,path=list(sys.path),
        isolated=sys.flags.isolated,no_site=sys.flags.no_site,no_user_site=sys.flags.no_user_site,
        no_bytecode=sys.dont_write_bytecode,optimize=sys.flags.optimize)
    need(encoded(profile)==encoded(value['profile']),'observation_launch_child_profile')
    result,pending_packet=check(**{k:value[k] for k in ('arguments','buffers','expected','rows','folder','repository_root','profile')})
    lib=Library(value['buffers']).load()
    try:
        pending=lib.pending
        request=value['pending_request']
        pending.validate_request(request)
        need(request['operation_id']==result['operation_id'] and request['sources']==value['rows'] and
            Path(request['folder'])==Path(value['folder']),'observation_launch_pending_request')
        packet_bytes=encoded(pending_packet)
        need(request['packet'].get('size')==len(packet_bytes) and
            request['packet'].get('sha256')==sha(packet_bytes),'observation_launch_pending_packet')
        # Rebind only the host command frame; the retained pending request and
        # all fourteen ordinary records remain original comparison inputs.
        request=dict(request,argv_prefix=runtime['argv'][:-2])
        code=pending.process.child(request,pending_packet,
            {n:value['buffers'][n] for n in pending.process.ROSTER},value['rows'])
        need(code==0,'observation_launch_child_incomplete')
        receipt=dict(schema='disabled_observation_child_v1',operation_id=result['operation_id'],
            core_sha256=sha(core),transport_sha256=transport_sha,preflight=result,
            pending_child_completed=True,actual_runtime_verified=False,**dict.fromkeys(FALSE,False),camera_commands=[])
        pending.write(Path(value['folder'])/'review'/'child-observation.json',encoded(receipt))
        return 0
    finally:lib.close()


def build_transport(*,arguments,buffers,expected,rows,folder,repository_root,profile,pending_request):
    """Single canonical transport derived from the checked original inputs."""
    value=dict(arguments=arguments,buffers=buffers,expected=expected,rows=rows,folder=str(folder),
        repository_root=str(repository_root),profile=profile,pending_request=pending_request)
    transport=dict(schema='disabled_observation_transport_v1',
        launcher=dict(bytes=base64.b64encode(buffers[ADDED]).decode('ascii'),sha256=expected[ADDED]),inputs=wire(value))
    raw=encoded(transport)
    need(len(raw)<=LIMIT,'observation_launch_transport_bound')
    return raw


def prepare(*,arguments,buffers,expected,rows,folder,repository_root,profile):
    """Private disabled preparation; public activation remains unavailable."""
    need(ENV not in os.environ,'observation_launch_environment_collision')
    result,packet=check(arguments,buffers,expected,rows,folder,repository_root,profile)
    runtime=arguments['runtime_expectation']
    need(runtime['bootstrap']==bootstrap(),'observation_launch_bootstrap')
    lib=Library(buffers).load();plan=None
    try:
        pending=lib.pending
        plan=pending._prepare_pending(folder=folder,packet=packet,
            buffers={n:buffers[n] for n in pending.process.ROSTER},rows=rows,
            expected_hashes={n:expected[n] for n in pending.process.ROSTER})
        need(encoded(plan['request']['expected_runtime'])==encoded(profile),'observation_launch_prepared_profile')
        review=Path(folder)/'review';review.mkdir(exist_ok=False)
        core=arguments['proposal_arguments']['request_bytes'];pending.write(review/'request.json',core)
        raw=build_transport(arguments=arguments,buffers=buffers,expected=expected,rows=rows,
            folder=folder,repository_root=repository_root,profile=profile,pending_request=plan['request'])
        pending.write(review/'transport.json',raw)
        context=dict(plan['context'],child_argv=runtime['argv'])
        environment=dict(os.environ);need(ENV not in environment,'observation_launch_environment_collision')
        environment[ENV]=sha(raw)
        return dict(library=lib,pending=plan,arguments=arguments,buffers=buffers,expected=expected,rows=rows,
            folder=Path(folder),repository_root=repository_root,profile=profile,preflight=result,
            core=core,transport=raw,context=context,environment=environment,started=False)
    except BaseException as primary:
        cleanup=None
        if plan is not None:
            try:pending.process.close_owned(tuple(plan[n] for n in ('helpers','validation','bootstrap','adapter','outer')),primary=None)
            except BaseException as error:cleanup=error
        try:lib.close()
        except BaseException as error:
            if cleanup is None:cleanup=error
        if cleanup is not None:raise primary from cleanup
        raise


def check_saved(plan):
    lib=plan['library'];pending=lib.pending
    pending.check_saved(plan['pending'])
    result,packet=check(**{k:plan[k] for k in ('arguments','buffers','expected','rows','folder','repository_root','profile')})
    need(encoded(result)==encoded(plan['preflight']) and packet==plan['pending']['packet'],
         'observation_launch_saved_projection')
    canonical=build_transport(**{k:plan[k] for k in ('arguments','buffers','expected','rows','folder','repository_root','profile')},
        pending_request=plan['pending']['request'])
    need(plan['transport']==canonical and plan['core']==plan['arguments']['proposal_arguments']['request_bytes'],
         'observation_launch_saved_transport_binding')
    need(plan['context']['child_argv']==plan['arguments']['runtime_expectation']['argv'] and
        plan['environment'].get(ENV)==sha(plan['transport']),'observation_launch_saved_command')
    for name,raw in (('request.json',plan['core']),('transport.json',plan['transport'])):
        value,_=pending.entry.read_source(str(plan['folder']/'review'/name),LIMIT)
        need(value==raw,'observation_launch_saved_transport')


def run_disabled(plan):
    """Single existing supervised child; no new timeout/retry policy."""
    need(not plan['started'],'observation_launch_reentry');plan['started']=True
    pending=plan['library'].pending;p=plan['pending'];records=pending.Records()
    narrow=answer=None;primary=cleanup=None;launched=[]
    try:
        check_saved(plan)
        def spawn(argv,cwd):
            need(argv==plan['context']['child_argv'],'observation_launch_spawn_argv')
            proc=subprocess.Popen(argv,cwd=cwd,env=plan['environment'],stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0,shell=False,close_fds=True)
            launched.append(proc);return proc
        records.value=p['control'].reserve_parent(context=plan['context'])
        sys.meta_path.insert(0,p['validation'])
        _,narrow=p['control'].run_parent_reserved(context=plan['context'],records=records,spawn=spawn,
            monotonic=time.monotonic,sleep=time.sleep)
        for owner in (p['validation'],records):
            if not owner.closed:owner.close()
        check_saved(plan)
        raw,_=pending.entry.read_source(str(plan['folder']/'review'/'child-observation.json'),LIMIT)
        child_receipt=strict(raw)
        expected=dict(schema='disabled_observation_child_v1',operation_id=plan['preflight']['operation_id'],
            core_sha256=sha(plan['core']),transport_sha256=sha(plan['transport']),preflight=plan['preflight'],
            pending_child_completed=True,actual_runtime_verified=False,**dict.fromkeys(FALSE,False),camera_commands=[])
        need(encoded(child_receipt)==encoded(expected),'observation_launch_child_receipt')
        answer=pending._reconcile(p,narrow)
    except BaseException as error:primary=error
    for owner in (records if records.value is not None and not records.attempted else None,
                  p['helpers'],p['validation'],p['bootstrap'],p['adapter'],p['outer']):
        if owner is not None and not owner.closed:
            try:owner.close()
            except BaseException as error:
                if cleanup is None:cleanup=error
    # No automatic cleanup action on a child with unknown completion.
    process=(narrow['process_observation'] if narrow is not None else
        dict(launch_attempts=len(launched),child_pids=[p.pid for p in launched],exit_observed=False,
             disposition='not_launched' if not launched else 'unknown_after_supervisor_exception'))
    try:plan['library'].close()
    except BaseException as error:
        if cleanup is None:cleanup=error
    result=dict(schema='disabled_observation_host_v1',status='consistent_disabled_observation' if primary is None and cleanup is None else 'needs_review',
        process=process,launch_attempts=len(launched),
        engine_result=answer,preflight=plan['preflight'],transport_sha256=sha(plan['transport']),
        failure_type=None if primary is None else type(primary).__name__,failure_code=None if primary is None else str(primary)[:200],
        cleanup_failure_type=None if cleanup is None else type(cleanup).__name__,
        owners_closed=all(p[n].closed for n in ('helpers','validation','bootstrap','adapter','outer')),
        library_closed=plan['library'].closed,
        records_closed=records.value is None or records.closed,automatic_retry=False,actual_runtime_verified=False,
        **dict.fromkeys(FALSE,False),camera_commands=[])
    try:pending.write(plan['folder']/'review'/'final-observation.json',encoded(result))
    except BaseException as publication:
        failure=primary if primary is not None else cleanup
        publication.operational_disposition=result
        if failure is not None:
            failure.operational_disposition=result
            raise failure from publication
        raise
    return result


def run_runtime(**kwargs):raise ValueError('real_activation_pending')
