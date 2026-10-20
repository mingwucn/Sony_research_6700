"""Disabled pending-operation host launcher; fixture generation stays separate.

Private APIs can construct retained callbacks. Public activation always refuses.
Host imports, interpreter and stdlib are trusted, not authenticated by child pins.
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
from types import SimpleNamespace
from tools import dependency_child_entry as entry
from tools import dependency_operational_child as process

PROFILE = "import sys,json\nprint(json.dumps(dict(implementation=sys.implementation.name,version=list(sys.version_info[:3]),version_text=sys.version,cache_tag=sys.implementation.cache_tag,executable=sys.executable,base_executable=getattr(sys,'_base_executable',sys.executable),prefix=sys.prefix,base_prefix=sys.base_prefix,platform=sys.platform,maxsize=sys.maxsize,path=list(sys.path),isolated=sys.flags.isolated,no_site=sys.flags.no_site,no_user_site=sys.flags.no_user_site,no_bytecode=sys.dont_write_bytecode,optimize=sys.flags.optimize)))\n"
REQUEST_FIELDS=frozenset(('schema','operation_id','sources','packet','folder','argv_prefix',
    'expected_runtime','bootstrap_sha256','execution_authorized','camera_commands'))

def need(ok,code):
    if not ok:raise ValueError(code)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def encoded(value):return process.encoded(value)

def write(path,raw):
    with Path(path).open('xb') as stream:
        stream.write(raw);stream.flush();os.fsync(stream.fileno())

def validate_capture(buffers,rows,expected_hashes):
    need(type(buffers) is dict and type(rows) is dict and type(expected_hashes) is dict and
        set(buffers)==set(rows)==set(expected_hashes)==process.ROSTER,'operational_launch_roster')
    total=0
    for n,raw in buffers.items():
        row=rows[n]
        need(type(row) is dict and set(row)=={'path','size','sha256','lstat','fstat'} and
            type(raw) is bytes and 0<len(raw)<=2*1024**2 and
            type(row['size']) is int and row['size']==len(raw) and row['sha256']==sha(raw)==expected_hashes[n],
            'operational_launch_source')
        need(Path(row['path']).is_absolute() and Path(row['path']).suffix=='.py',
            'operational_launch_source_path')
        total+=len(raw)
    need(total<=16*1024**2,'operational_launch_bound')

def capture_sources(*,named,sourcefolder,validated,expected_hashes):
    """Capture fresh authored Python; external review hashes are not consent."""
    need(set(named)==process.ROSTER and set(expected_hashes)==process.ROSTER,
        'operational_launch_roster')
    sourcefolder=Path(sourcefolder);sourcefolder.mkdir(parents=True,exist_ok=False)
    buffers={};rows={}
    for n,path in named.items():
        path=Path(path)
        need(path.is_absolute() and path.suffix=='.py','operational_launch_source_path')
        raw,_=entry.read_source(str(path))
        need(sha(raw)==expected_hashes[n],'operational_launch_source')
        if n.startswith('bound.'):
            key=n.removeprefix('bound.');original=validated['inputs']['source_cache']['sources'][key]
            need(raw==validated['source_buffers'][key] and sha(raw)==original['sha256'] and
                len(raw)==original['bytes'] and str(path)==original['path'],
                'operational_launch_retained')
            # Retained origins must stay unchanged for the prepared map.
            buffers[n],rows[n]=entry.read_source(str(path))
        else:
            target=sourcefolder/(n+'.py');write(target,raw)
            buffers[n],rows[n]=entry.read_source(str(target))
    validate_capture(buffers,rows,expected_hashes)
    return buffers,rows

def bootstrap():
    prefix=entry.BOOTSTRAP.split('try:\n need(len(sys.argv)==3',1)[0]
    body=r'''
try:
 need(len(sys.argv)==3,'arguments')
 raw,_=read(sys.argv[1],65536);need(digest(raw)==sys.argv[2],'request_hash')
 request=json.loads(raw,object_pairs_hook=pairs)
 need(type(request) is dict and set(request)==REQUEST_FIELDS,'operational_launch_request')
 need(request['schema']=='disabled_operational_outer_request_v1' and request['execution_authorized'] is False and request['camera_commands']==[],'operational_launch_mode')
 need(sys.orig_argv==request['argv_prefix']+sys.argv[1:],'operational_launch_argv')
 need(digest(sys.orig_argv[sys.orig_argv.index('-c')+1].encode())==request['bootstrap_sha256'],'operational_launch_bootstrap')
 observed=dict(implementation=sys.implementation.name,version=list(sys.version_info[:3]),version_text=sys.version,cache_tag=sys.implementation.cache_tag,executable=sys.executable,base_executable=getattr(sys,'_base_executable',sys.executable),prefix=sys.prefix,base_prefix=sys.base_prefix,platform=sys.platform,maxsize=sys.maxsize,path=list(sys.path),isolated=sys.flags.isolated,no_site=sys.flags.no_site,no_user_site=sys.flags.no_user_site,no_bytecode=sys.dont_write_bytecode,optimize=sys.flags.optimize)
 def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
 need(canon(observed)==canon(request['expected_runtime']) and sys.flags.isolated==sys.flags.no_site==sys.flags.no_user_site==1 and sys.dont_write_bytecode is True and sys.flags.optimize==0,'operational_launch_profile')
 need(type(request['sources']) is dict and set(request['sources'])==SOURCE_ROLES,'operational_launch_roster')
 folder=Path(request['folder']);need(folder.is_absolute() and '..' not in folder.parts,'operational_launch_folder')
 need(Path(sys.argv[1])==folder/'request.json' and Path(request['packet']['path'])==folder/'packet.json','operational_launch_path')
 buffers={};receipts={};total=0
 for name,row in request['sources'].items():
  need(type(row) is dict and set(row)=={'path','size','sha256','lstat','fstat'} and Path(row['path']).is_absolute() and '..' not in Path(row['path']).parts and Path(row['path']).suffix=='.py','operational_launch_source_path')
  data,seen=read(row['path'],2*1024**2);need(canon(seen)==canon(row),'source_binding')
  total+=len(data);need(total<=16*1024**2,'source_bound');buffers[name]=data;receipts[name]=seen
 import ast
 compiled={n:compile(ast.parse(data),'<captured:'+n+'>','exec',dont_inherit=True,optimize=0) for n,data in buffers.items()}
 raw,seen=read(request['packet']['path'],8*1024**2);need(canon(seen)==canon(request['packet']),'packet_binding')
 packet=json.loads(raw,object_pairs_hook=pairs)
 child=types.ModuleType('_disabled_operational_child')
 exec(compiled['process_child'],vars(child))
 raise SystemExit(child.child(request,packet,buffers,receipts))
except SystemExit:raise
except BaseException:
 print(json.dumps(dict(status='needs_review',camera_commands=[])))
 raise SystemExit(2)
'''
    return prefix+body.replace('REQUEST_FIELDS',repr(set(REQUEST_FIELDS))).replace('SOURCE_ROLES',repr(set(process.ROSTER)))

def validate_request(request):
    need(type(request) is dict and set(request)==REQUEST_FIELDS and
        request['schema']=='disabled_operational_outer_request_v1' and
        request['execution_authorized'] is False and request['camera_commands']==[],
        'operational_launch_request')
    need(type(request['operation_id']) is str and len(request['operation_id'])==32 and
        all(c in '0123456789abcdef' for c in request['operation_id']),'operational_launch_operation')
    need(request['argv_prefix']==[request['expected_runtime']['executable'],'-I','-S','-B','-X','utf8','-c',bootstrap()] and
        request['bootstrap_sha256']==sha(bootstrap().encode()),'operational_launch_bootstrap')
    folder=Path(request['folder'])
    need(folder.is_absolute() and '..' not in folder.parts and
        request['packet']['path']==str(folder/'packet.json'),'operational_launch_folder')
    return request

def check_saved(plan):
    validate_request(plan['request'])
    request=plan['request']
    need(encoded(request)==plan['request_bytes'] and encoded(plan['packet'])==plan['packet_bytes'],
        'operational_launch_memory_changed')
    raw,_=entry.read_source(str(plan['request_path']),65536)
    need(raw==plan['request_bytes'],'operational_launch_saved_request')
    raw,row=entry.read_source(request['packet']['path'],8*1024**2)
    need(raw==plan['packet_bytes'] and row==request['packet'],'operational_launch_saved_packet')
    for row in request['sources'].values():
        _,seen=entry.read_source(row['path'])
        need(seen==row,'operational_launch_saved_source')
    need(plan['context']['child_argv']==request['argv_prefix']+[str(plan['request_path']),sha(plan['request_bytes'])],
        'operational_launch_supervisor_argv')
    need(plan['context']['operation_id']==request['operation_id']==plan['prepared']['operation_id'],
        'operational_launch_operation')

class Records:
    def __init__(self):self.value=None;self.attempted=self.closed=False
    def __getattr__(self,name):return getattr(self.value,name)
    def close(self):
        need(not self.attempted,'operational_launch_records_reclose')
        self.attempted=True;self.closed=self.value.close() is True
        need(self.closed,'operational_launch_records_close_unknown')
        return True

class BootstrapOwner:
    def __init__(self,host):self.host=host;self.modules={};self.closed=False
    def load(self,n,raw,path):
        result=self.host.cached_module(n,raw,path);self.modules[n]=result;return result
    def close(self):
        need(not self.closed,'operational_launch_bootstrap_reclose');self.closed=True;primary=None
        for n,m in reversed(tuple(self.modules.items())):
            try:
                need(sys.modules.get(n) is m,'operational_launch_bootstrap_ownership');del sys.modules[n]
            except BaseException as error:
                if primary is None:primary=error
        if primary is not None:raise primary
        return True

def parent_validation_sources(validated,gate,io,factory):
    p=validated['inputs'];root=Path(validated['candidate']['repository_root'])
    ordinary=p['binding_schema']['load_order'];protected=p['binding_schema']['protected_order']
    need(len(ordinary)==len(set(ordinary))==23 and len(protected)==len(set(protected))==3 and
        not set(ordinary)&set(protected) and set(ordinary)|set(protected)==set(p['role_authority']['roles']),
        'operational_launch_parent_roles')
    adapter=SimpleNamespace(require=gate.require,relative=gate.relative,sha=gate.sha,read_ordinary=io.read_ordinary)
    loader=factory.AuthoredSources(adapter)
    try:
        for name in ordinary:
            row=p['role_authority']['roles'][name];raw=validated['source_buffers']['role:'+name]
            need(sha(raw)==row['sha256']==validated['effective_qualified_sources'][row['path']],
                'operational_launch_parent_role_hash')
            loader.add(p['binding_schema']['aliases'][name],root/row['path'],raw)
    except BaseException as primary:
        try:loader.close()
        except BaseException as cleanup:raise primary from cleanup
        raise
    return loader

def check_retained(validated,buffers,rows):
    retained={n for n in process.ROSTER if n.startswith('bound.')}
    need(len(retained)==29,'operational_launch_retained_roster')
    for role in retained:
        key=role.removeprefix('bound.');row=validated['inputs']['source_cache']['sources'][key]
        need(buffers[role]==validated['source_buffers'][key] and sha(buffers[role])==row['sha256'] and
            len(buffers[role])==row['bytes'] and rows[role]['path']==row['path'],
            'operational_launch_retained')

def _prepare_pending(*,folder,packet,buffers,rows,expected_hashes):
    """Source-owned private composition only, not an authorization check."""
    folder=Path(folder)
    need(folder.is_absolute() and folder.is_dir(),'operational_launch_folder')
    validate_capture(buffers,rows,expected_hashes)
    outer=adapter=helpers=boot=validation=None
    try:
        outer,adapter=process.owners(buffers)
        decoded=process.check_packet(packet,buffers,rows,adapter)
        docs,raw,prepared,checked,ordinary=decoded
        need(Path(prepared['folder'])==folder/'composition','operational_launch_composition')
        gate=outer.modules['retained_gate'];io=outer.modules['ordinary_io'];host=outer.modules['dependency_host_entry']
        validated=gate.validate_bundle(docs,expected_seal_sha256=packet['seal_sha256'],reference_pins=packet['reference_pins'])
        need(validated['candidate']['operation_id']==prepared['operation_id'],'operational_launch_operation')
        check_retained(validated,buffers,rows)
        arguments=process.preflight_arguments(packet,decoded,outer,adapter,validated)
        outer.modules['dependency_operational_metadata'].validate_pending(**arguments)
        packet_raw=encoded(packet);need(len(packet_raw)<=8*1024**2,'operational_launch_packet_bound')
        write(folder/'packet.json',packet_raw)
        _,packet_row=entry.read_source(str(folder/'packet.json'),8*1024**2)
        profile=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',PROFILE],capture_output=True,timeout=15)
        need(profile.returncode==0 and not profile.stderr,'operational_launch_profile')
        argv=[sys.executable,'-I','-S','-B','-X','utf8','-c',bootstrap()]
        request=dict(schema='disabled_operational_outer_request_v1',operation_id=prepared['operation_id'],
            sources=rows,packet=packet_row,folder=str(folder),argv_prefix=argv,
            expected_runtime=entry.strict_json(profile.stdout),bootstrap_sha256=sha(bootstrap().encode()),
            execution_authorized=False,camera_commands=[])
        validate_request(request);request_raw=encoded(request)
        need(len(request_raw)<=65536,'operational_launch_request_bound')
        path=folder/'request.json';write(path,request_raw)
        context=host.make_context(validated);context['child_argv']=argv+[str(path),sha(request_raw)]
        boot=BootstrapOwner(host)
        control=boot.load('_disabled_parent_control',buffers['bound.bootstrap:io_entry'],rows['bound.bootstrap:io_entry']['path'])
        factory=boot.load('_disabled_parent_factory',buffers['bound.integration:prospective_child'],rows['bound.integration:prospective_child']['path'])
        validation=parent_validation_sources(validated,gate,io,factory)
        helpers=process.helper_owner(outer,buffers,rows,'parent')
        dep={n:buffers['dependency.'+n] for n in process.DEPENDENCIES[:-1]}
        dep['closure_manifest']=encoded(prepared['sources'])
        inputs=helpers.package.dependency_execution.bind_runtime_packet(prepared['dependency_packet'],
            prepared['dependency_fixed'],dep,prepared['dependency_review_sha256'])
        plan=dict(folder=folder,packet=packet,packet_bytes=packet_raw,request=request,request_bytes=request_raw,
            request_path=path,outer=outer,adapter=adapter,helpers=helpers,bootstrap=boot,validation=validation,
            control=control,context=context,prepared=prepared,checked=checked,preflight_arguments=arguments,inputs=inputs)
        check_saved(plan)
        return plan
    except BaseException as primary:
        process.close_owned((helpers,validation,boot,adapter,outer),primary)

def _supervise(plan):
    check_saved(plan)
    control=plan['control'];context=plan['context'];loader=plan['validation'];records=Records()
    primary=None;narrow=None;launched=[]
    def spawn(argv,cwd):
        proc=subprocess.Popen(argv,cwd=cwd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            bufsize=0,shell=False,close_fds=True)
        launched.append(proc);return proc
    try:
        records.value=control.reserve_parent(context=context)
        sys.meta_path.insert(0,loader)
        _,narrow=control.run_parent_reserved(context=context,records=records,spawn=spawn,
            monotonic=time.monotonic,sleep=time.sleep)
    except BaseException as error:primary=error
    cleanup=None
    for owner in (loader,records if records.value is not None and not records.attempted else None):
        if owner is not None and not owner.closed:
            try:owner.close()
            except BaseException as error:
                if cleanup is None:cleanup=error
    ownership=dict(parent_records_closed=records.closed,parent_validation_closed=loader.closed,
        failure_type=None if primary is None else type(primary).__name__,
        cleanup_failure_type=None if cleanup is None else type(cleanup).__name__)
    if narrow is None:
        narrow=dict(status='needs_review',host_exit_code=1,terminal_records_agree=False,
            process_observation=dict(launch_attempts=len(launched),child_pids=[p.pid for p in launched],
                exit_observed=False,disposition='not_launched' if not launched else 'unknown_after_supervisor_exception'))
    return narrow,ownership

def _reconcile(plan,narrow):
    check_saved(plan)
    need(narrow['host_exit_code']==0 and narrow['terminal_records_agree'] is True,
        'operational_launch_supervision_incomplete')
    folder=plan['folder'];outer=plan['outer'];packet=plan['packet'];request=plan['prepared']
    raw,_=entry.read_source(str(folder/'outer-child.json'),2*1024**2)
    result=process.strict(raw)
    need(type(result) is dict and set(result)==process.TERMINAL_FIELDS and result.get('schema')=='disabled_operational_outer_child_v1' and
        result.get('status')=='complete_pending_composition' and result.get('operation_id')==request['operation_id'] and
        result.get('request_sha256')==packet['request_sha256'],'operational_launch_child_result')
    need(all(result.get(n) is True for n in ('preparation_closed','helpers_closed','adapter_closed','callback_closed')) and
        all(result.get(n) is False for n in ('execution_authorized','feature_supported','recovery_proven','device_write_gate_passed')) and
        result.get('camera_commands')==[],'operational_launch_child_flags')
    evidence=result['evidence'];context=plan['context']
    need(type(evidence) is dict and set(evidence)==process.EVIDENCE_FIELDS and
        type(evidence['dependency_sha256']) is dict and set(evidence['dependency_sha256'])==process.DEPENDENCY_ARTIFACTS and
        type(evidence['bridge_sha256']) is dict and set(evidence['bridge_sha256'])=={'completion.json','controller-result.json'},
        'operational_launch_evidence')
    hashes=[result['preflight_sha256'],result['request_sha256'],evidence['stdout_sha256']]+list(evidence['dependency_sha256'].values())+list(evidence['bridge_sha256'].values())
    need(all(type(h) is str and len(h)==64 and all(c in '0123456789abcdef' for c in h) for h in hashes),
        'operational_launch_evidence_hash')
    stdout=plan['control'].read_ordinary(context['session_dir']/'actual-stdout.txt',context['repository_root'],16384)
    need(sha(stdout)==evidence['stdout_sha256']==narrow['stdout_sha256'],'operational_launch_stdout')
    preflight,_=entry.read_source(str(folder/'pending-preflight.json'),2*1024**2)
    return outer.modules['dependency_operational_preparation'].reconcile_saved_parent(
        source_owner=outer,raw=preflight,expected_sha256=result['preflight_sha256'],
        preflight_arguments=plan['preflight_arguments'],request=request,
        request_sha256=packet['request_sha256'],checked_sources=plan['checked'],adapter_owner=plan['adapter'],
        helpers=plan['helpers'],parent_source_buffers=plan['helpers'].buffers,inputs=plan['inputs'],
        process=narrow['process_observation'],stdout=stdout,stdout_sha256=evidence['stdout_sha256'],
        dependency_sha256=evidence['dependency_sha256'],bridge_sha256=evidence['bridge_sha256'])

def _run_pending(plan):
    """One supervised attempt; preserve unknown disposition and never retry."""
    narrow=None;ownership=None;answer=None;primary=None
    try:
        narrow,ownership=_supervise(plan)
        need(ownership['failure_type'] is None and ownership['cleanup_failure_type'] is None and
            ownership['parent_records_closed'] is True and ownership['parent_validation_closed'] is True,
            'operational_launch_supervisor_failure')
        answer=_reconcile(plan,narrow)
    except BaseException as error:primary=error
    cleanup=None
    for owner in (plan['helpers'],plan['validation'],plan['bootstrap'],plan['adapter'],plan['outer']):
        if not owner.closed:
            try:owner.close()
            except BaseException as error:
                if cleanup is None:cleanup=error
    result=dict(schema='disabled_operational_outer_host_v1',status='consistent_pending_composition' if primary is None and cleanup is None else 'needs_review',
        process=None if narrow is None else narrow['process_observation'],supervision=ownership,
        engine_result=answer,failure_type=None if primary is None else type(primary).__name__,
        failure_code=None if primary is None else str(primary)[:200],
        cleanup_failure_type=None if cleanup is None else type(cleanup).__name__,
        helpers_closed=plan['helpers'].closed,validation_closed=plan['validation'].closed,
        bootstrap_closed=plan['bootstrap'].closed,adapter_closed=plan['adapter'].closed,outer_closed=plan['outer'].closed,
        automatic_retry=False,execution_authorized=False,feature_supported=False,recovery_proven=False,
        device_write_gate_passed=False,camera_commands=[])
    try:write(plan['folder']/'final-receipt.json',encoded(result))
    except BaseException as publication:
        failure=primary if primary is not None else cleanup
        publication.operational_disposition=result
        if failure is not None:
            failure.operational_disposition=result
            raise failure from publication
        raise
    return result

def run_runtime(**kwargs):raise ValueError('real_activation_pending')
