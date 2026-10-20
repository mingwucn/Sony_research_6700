"""Invented-only host source capture, launch and supervision.

No fixture generation, camera adapter or real activation path. Interpreter,
stdlib and initial authored bootstrap are trusted assumptions, not a sandbox.
"""
if __name__=='__main__':
    raise SystemExit(2)

import base64,hashlib,json,os,pathlib,subprocess,sys,time
from pathlib import Path
from types import SimpleNamespace
from tools import dependency_child_entry as entry
from tools import dependency_host_entry as host
from tools import dependency_host_process_contract as contract
from tools import dependency_invented as invented


def need(ok,code='invented_parent_refused'):
    if not ok:raise ValueError(code)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')

def write(path,raw):
    with path.open('xb') as stream:
        stream.write(raw);stream.flush();os.fsync(stream.fileno())

def require_invented(packet):
    need(type(packet) is dict and packet.get('scope')=='invented_only_no_operational_authority','invented_only')
    # The child independently checks the fixed invented source/constants identity
    # before observer preparation. A caller statement is not operational consent.

class BootstrapOwner:
    def __init__(self):self.modules={};self.closed=False
    def load(self,alias,raw,path):
        need(not self.closed,'parent_bootstrap_closed')
        module=host.cached_module(alias,raw,path)
        self.modules[alias]=module
        return module
    def close(self):
        if self.closed:return False
        self.closed=True;primary=None
        for alias,module in self.modules.items():
            try:
                if sys.modules.get(alias) is module:del sys.modules[alias]
                else:need(alias not in sys.modules,'parent_bootstrap_ownership')
            except BaseException as error:
                if primary is None:primary=error
        if primary is not None:raise primary
        return True


def capture_sources(*,named,sourcefolder,validated):
    """Exclusive authored-text copies plus fresh retained source receipts."""
    sources={};buffers={}
    need(set(named)=={n for n in contract.SOURCE_ROLES if not n.startswith('bound.')},'capture_named_roster')
    sourcefolder.mkdir(parents=True,exist_ok=False)
    for key,path in named.items():
        raw,proof=entry.read_source(str(path))
        target=sourcefolder/(key+'.py')
        write(target,raw)
        buffers[key],sources[key]=entry.read_source(str(target))
        need(buffers[key]==raw,'capture_changed')
    for key,row in validated['inputs']['source_cache']['sources'].items():
        if not (key.startswith('role:') or key in ('bootstrap:activation_binding','bootstrap:io_entry','integration:prospective_child')):continue
        raw,receipt=entry.read_source(row['path'])
        need(raw==validated['source_buffers'][key] and sha(raw)==row['sha256'] and
            len(raw)==row['bytes'],'capture_retained_changed')
        buffers['bound.'+key],sources['bound.'+key]=raw,receipt
    need(set(sources)==contract.SOURCE_ROLES,'capture_source_roster')
    return buffers,sources

PROFILE = "import sys,json\nprint(json.dumps(dict(implementation=sys.implementation.name,version=list(sys.version_info[:3]),version_text=sys.version,cache_tag=sys.implementation.cache_tag,executable=sys.executable,base_executable=getattr(sys,'_base_executable',sys.executable),prefix=sys.prefix,base_prefix=sys.base_prefix,platform=sys.platform,maxsize=sys.maxsize,path=list(sys.path),isolated=sys.flags.isolated,no_site=sys.flags.no_site,no_user_site=sys.flags.no_user_site,no_bytecode=sys.dont_write_bytecode,optimize=sys.flags.optimize)))\n"

def bootstrap(entry):
    prefix = entry.BOOTSTRAP.split('try:\n need(len(sys.argv)==3', 1)[0]
    body = "\ntry:\n need(len(sys.argv)==3,'arguments')\n raw,_=read(sys.argv[1],65536);need(digest(raw)==sys.argv[2],'request_hash')\n request=json.loads(raw,object_pairs_hook=pairs)\n need(type(request) is dict and set(request)=={'schema','operation_id','sources','packet','argv_prefix','expected_runtime','bootstrap_sha256','review_sha256','folder'},'request_shape')\n need(request['schema']=='invented_clean_outer_request_v1','invented_only')\n actual=sys.orig_argv[sys.orig_argv.index('-c')+1]\n need(digest(actual.encode())==request['bootstrap_sha256'],'bootstrap_binding')\n need(sys.orig_argv==request['argv_prefix']+sys.argv[1:],'argv_binding')\n observed=dict(implementation=sys.implementation.name,version=list(sys.version_info[:3]),version_text=sys.version,cache_tag=sys.implementation.cache_tag,executable=sys.executable,base_executable=getattr(sys,'_base_executable',sys.executable),prefix=sys.prefix,base_prefix=sys.base_prefix,platform=sys.platform,maxsize=sys.maxsize,path=list(sys.path),isolated=sys.flags.isolated,no_site=sys.flags.no_site,no_user_site=sys.flags.no_user_site,no_bytecode=sys.dont_write_bytecode,optimize=sys.flags.optimize)\n def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')\n need(canon(observed)==canon(request['expected_runtime']) and sys.flags.isolated==1 and sys.flags.no_site==1 and sys.dont_write_bytecode is True and sys.flags.optimize==0,'runtime_binding')\n need(type(request['sources']) is dict and 1<=len(request['sources'])<=80,'source_roster')\n buffers={};receipts={};total=0\n for role,row in request['sources'].items():\n  need(type(row) is dict and set(row)=={'path','size','sha256','lstat','fstat'} and Path(row['path']).suffix=='.py','source_shape')\n  buf,receipt=read(row['path'],2*1024**2);need(canon(receipt)==canon(row),'source_binding')\n  total+=len(buf);need(total<=16*1024**2,'source_bound');buffers[role]=buf;receipts[role]=receipt\n packet_raw,packet_receipt=read(request['packet']['path'],8*1024**2)\n need(canon(packet_receipt)==canon(request['packet']),'packet_binding')\n packet=json.loads(packet_raw,object_pairs_hook=pairs)\n entry=types.ModuleType('_clean_outer_child');entry.__file__=receipts['outer_child']['path']\n exec(compile(buffers['outer_child'],entry.__file__,'exec',dont_inherit=True,optimize=0),entry.__dict__)\n raise SystemExit(entry.child(request,packet,buffers,receipts))\nexcept SystemExit:raise\nexcept BaseException:\n print(json.dumps(dict(status='needs_review',code='invented_outer_refused',camera_commands=[])))\n raise SystemExit(2)\n"
    body=body.replace("'review_sha256','folder'}", "'review_sha256','folder','authority'}")
    body=body.replace('invented_clean_outer_request_v1','invented_successor_outer_request_v1')
    body=body.replace("need(type(request['sources']) is dict and 1<=len(request['sources'])<=80,'source_roster')",
        "need(type(request['sources']) is dict and set(request['sources'])=="+repr(set(contract.SOURCE_ROLES))+",'source_roster')")
    body=body.replace(" buffers={};receipts={};total=0", " for row in list(request['sources'].values())+[request['packet']]:\n  need(type(row) is dict and set(row)=={'path','size','sha256','lstat','fstat'} and Path(row['path']).is_absolute() and '..' not in Path(row['path']).parts and Path(row['path']).is_relative_to(Path(request['folder'])),'source_path')\n buffers={};receipts={};total=0")
    body=body.replace(" entry=types.ModuleType('_clean_outer_child')", " import ast\n compiled={key:compile(ast.parse(raw,filename=receipts[key]['path']),receipts[key]['path'],'exec',dont_inherit=True,optimize=0) for key,raw in buffers.items()}\n contract=types.ModuleType('_checked_contract');exec(compiled['outer_contract'],contract.__dict__);contract.validate_request(request)\n entry=types.ModuleType('_clean_outer_child')")
    body=body.replace("exec(compile(buffers['outer_child'],entry.__file__,'exec',dont_inherit=True,optimize=0),entry.__dict__)","exec(compiled['outer_child'],entry.__dict__)")
    return prefix + body

class RecordOwner:
    """One close attempt across inherited control and abrupt interruption."""
    def __init__(self, records):
        self.original=records;self.attempted=False;self.closed=False
    def __getattr__(self, name):return getattr(self.original,name)
    def close(self):
        need(not self.attempted)
        self.attempted=True
        self.closed=self.original.close() is True
        return self.closed


def parent_validation_sources(validated, gate, io, modules):
    """Own only ordinary role aliases needed by parent core reconciliation."""
    root=Path(validated['candidate']['repository_root']);p=validated['inputs']
    ordinary=p['binding_schema']['load_order'];protected=p['binding_schema']['protected_order']
    need(type(ordinary) is list and type(protected) is list
         and len(ordinary)==len(set(ordinary))==23 and len(protected)==len(set(protected))==3
         and not set(ordinary)&set(protected)
         and set(ordinary)|set(protected)==set(p['role_authority']['roles']))
    adapter=SimpleNamespace(require=gate.require,relative=gate.relative,sha=gate.sha,read_ordinary=io.read_ordinary)
    loader=modules['factory'].AuthoredSources(adapter)
    for role in ordinary:
        row=p['role_authority']['roles'][role];raw=validated['source_buffers']['role:'+role]
        need(gate.sha(raw)==row['sha256']==validated['effective_qualified_sources'][row['path']])
        loader.add(p['binding_schema']['aliases'][role],root/row['path'],raw)
    return loader


def prepare_request(*,folder,packet,sources,operation_id,review_sha256,context):
    require_invented(packet)
    folder=Path(folder)
    need(folder.is_absolute(),'launch_folder')
    packet_path=folder/'packet.json'
    write(packet_path,canonical(packet))
    _,packet_receipt=entry.read_source(str(packet_path),limit=8*1024**2)
    profile=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',PROFILE],capture_output=True,timeout=15)
    need(profile.returncode==0 and not profile.stderr,'profile_refused')
    boot=bootstrap(entry)
    argv=[sys.executable,'-I','-S','-B','-X','utf8','-c',boot]
    request=dict(schema='invented_successor_outer_request_v1',operation_id=operation_id,sources=sources,
        packet=packet_receipt,argv_prefix=argv,expected_runtime=entry.strict_json(profile.stdout),
        bootstrap_sha256=sha(boot.encode()),review_sha256=review_sha256,folder=str(folder))
    request['authority']=contract.authority(request)
    contract.validate_request(request)
    raw=canonical(request);need(len(raw)<=65536,'request_bound')
    request_path=folder/'request.json';write(request_path,raw)
    context['child_argv']=argv+[str(request_path),sha(raw)]
    return request,request_path


def check_capture(*,request,buffers,sources,validated,source_buffers,packet):
    """Every executable buffer must match both the request and original gate."""
    need(type(buffers) is dict and type(sources) is dict and
        set(buffers)==set(sources)==contract.SOURCE_ROLES,'parent_buffer_roster')
    need(canonical(sources)==canonical(request['sources']),'parent_receipt_binding')
    for role,raw in buffers.items():
        row=sources[role]
        need(type(raw) is bytes and len(raw)==row['size'] and sha(raw)==row['sha256'],'parent_buffer_binding')
    for key,row in validated['inputs']['source_cache']['sources'].items():
        role='bound.'+key
        if role not in contract.SOURCE_ROLES:continue
        need(buffers[role]==validated['source_buffers'][key] and
            sha(buffers[role])==row['sha256'] and len(buffers[role])==row['bytes'] and
            sources[role]['path']==row['path'],'parent_retained_binding')
    need(type(source_buffers) is dict and set(source_buffers)==set(contract.CHILD)|{'closure_manifest'},'parent_dependency_roster')
    need(all(source_buffers[n]==buffers['dependency.'+n] for n in contract.CHILD) and
        source_buffers['closure_manifest']==canonical(packet['adapter_request']['sources']),'parent_dependency_binding')


def check_launch(*,request,request_path,folder,packet,context,validated):
    require_invented(packet)
    folder=Path(folder);request_path=Path(request_path)
    need(folder==Path(request['folder']) and request_path==folder/'request.json','parent_launch_paths')
    raw=canonical(packet)
    need(len(raw)==request['packet']['size'] and sha(raw)==request['packet']['sha256'],'parent_packet_binding')
    need(context['operation_id']==request['operation_id']==packet['adapter_request']['operation_id']==
        validated['candidate']['operation_id'],'parent_operation_binding')
    root=Path(validated['candidate']['repository_root'])
    need(Path(context['repository_root'])==root and
        Path(context['session_dir'])==root/validated['candidate']['session'],'parent_context_binding')
    need(context['child_argv']==request['argv_prefix']+[str(request_path),sha(canonical(request))],'parent_supervisor_argv')
    saved,_=entry.read_source(str(request_path),limit=65536)
    need(saved==canonical(request),'parent_saved_request_binding')
    saved,receipt=entry.read_source(request['packet']['path'],limit=8*1024**2)
    need(saved==raw and canonical(receipt)==canonical(request['packet']),'parent_saved_packet_binding')


def prepare_parent(*,validated,gate,io,folder,request,request_path,context,buffers,sources,
                   packet,source_buffers,adapter_owner,adapter_buffers,repository_root):
    require_invented(packet)
    contract.validate_request(request)
    check_capture(request=request,buffers=buffers,sources=sources,validated=validated,source_buffers=source_buffers,packet=packet)
    check_launch(request=request,request_path=request_path,folder=folder,packet=packet,context=context,validated=validated)
    bootstrap_owner=BootstrapOwner();verifier=validation_loader=None
    try:
        control=bootstrap_owner.load('clean_outer_parent_control',buffers['bound.bootstrap:io_entry'],sources['bound.bootstrap:io_entry']['path'])
        factory=bootstrap_owner.load('clean_outer_parent_factory',buffers['bound.integration:prospective_child'],sources['bound.integration:prospective_child']['path'])
        validation_loader=parent_validation_sources(validated,gate,io,dict(factory=factory))
        source_loader=bootstrap_owner.load('successor_parent_sources',buffers['namespace'],sources['namespace']['path'])
        order=source_loader.PARENT_ORDER
        parent_buffers={n:buffers['dependency.'+n] for n in order}
        verifier=source_loader.HelperSources(mode='parent',buffers=parent_buffers,
            origins={n:sources['dependency.'+n]['path'] for n in order},hashes={n:sha(raw) for n,raw in parent_buffers.items()})
        verifier.load()
        successor=bootstrap_owner.load('successor_parent_entry',buffers['successor_entry'],sources['successor_entry']['path'])
        return dict(verifier=verifier,successor=successor,validation_loader=validation_loader,
            bootstrap_owner=bootstrap_owner,folder=Path(folder),request=request,request_path=request_path,
            context=context,entry=entry,invented=invented,control=control,packet=packet,
            source_buffers=source_buffers,adapter_owner=adapter_owner,adapter_buffers=adapter_buffers,
            repository_root=Path(repository_root),validated=validated)
    except BaseException as primary:
        cleanup=None
        for owner in (verifier,validation_loader,adapter_owner,bootstrap_owner):
            if owner is not None and not owner.closed:
                try:owner.close()
                except BaseException as error:
                    if cleanup is None:cleanup=error
        if cleanup is not None:raise primary from cleanup
        raise


def reconcile(plan, narrow):
    folder=plan['folder'];request=plan['request'];entry=plan['entry'];control=plan['control']
    artifacts=None;source_verified=False;outcome='unknown';failure=None;metadata_verified=False
    try:
        # Bind the saved request as well as every source and the packet anew.
        raw,_=entry.read_source(str(plan['request_path']),limit=65536)
        need(sha(raw)==plan['context']['child_argv'][-1] and canonical(entry.strict_json(raw))==canonical(request),'saved_request_changed')
        contract.validate_request(request)
        for row in request['sources'].values():
            _,seen=entry.read_source(row['path'])
            need(canonical(seen)==canonical(row),'saved_source_changed')
        _,seen=entry.read_source(request['packet']['path'],limit=8*1024**2)
        need(canonical(seen)==canonical(request['packet']),'saved_packet_changed')
        source_verified=True
        process=narrow['process_observation']
        need(process['launch_attempts']==1 and process['exit_observed'] is True and
             process['reader_threads_joined'] is True and process['pipe_close_complete'] is True and
             process['timed_out'] is False and process['kill_attempts']==0 and process['wait_attempts']==0,'process_unknown')
        raw,_=entry.read_source(str(folder/'outer-result.json'))
        result=entry.strict_json(raw)
        need(result['adapter_request_sha256']==plan['packet']['adapter_request_sha256'],'adapter_result_binding')
        terminal=contract.validate_terminal(result,request)
        if result['metadata_preflight_sha256'] is not None:
            raw,_=entry.read_source(str(folder/'metadata-preflight.json'))
            metadata_verified=plan['successor'].verify_saved_preflight(raw=raw,
                expected_sha256=result['metadata_preflight_sha256'],request=request,packet=plan['packet'],
                contract=contract,prepared_repository_root=plan["repository_root"])
        if terminal=='refused':
            need(process['child_exit_code']==2 and narrow['host_exit_code']==1,'refusal_process_mismatch')
            outcome='refused'
            failure=result['failure_type']
        else:
            need(metadata_verified,'metadata_success_missing')
            need(process['child_exit_code']==0 and narrow['host_exit_code']==0 and narrow['terminal_records_agree'] is True,'success_process_mismatch')
            need(result['summary_sha256']==narrow['stdout_sha256'],'summary_mismatch')
            data,_=plan['invented'].unpack(plan['packet']['dependency'],plan['packet']['fixed'],plan['source_buffers'],request['review_sha256'],complete=True)
            stdout=control.read_ordinary(plan['context']['session_dir']/'actual-stdout.txt',plan['context']['repository_root'],16384)
            verification=plan['successor'].verify_child_completion(verifier=plan['verifier'],folder=folder/'composition',inputs=data,
                operation_id=request['operation_id'],stdout=stdout,stdout_sha256=narrow['stdout_sha256'],
                dependency_sha256=result['dependency_artifact_sha256'],bridge_sha256=result['bridge_artifact_sha256'],
                adapter_owner=plan['adapter_owner'],adapter_request=plan['packet']['adapter_request'],
                adapter_request_sha256=plan['packet']['adapter_request_sha256'],adapter_buffers=plan['adapter_buffers'],process=process)
            artifacts=verification['dependency_sha256'];outcome='success'
    except BaseException as error:
        failure=type(error).__name__
    complete=outcome=='success'
    return dict(schema='invented_successor_outer_host_v1',status='invented_outer_complete' if complete else 'needs_review',
        completion_outcome=outcome,reconciliation_failure_type=failure,host_exit_code=0 if complete else 1,
        operation_id=request['operation_id'],process=narrow['process_observation'],narrow_controller_status=narrow['status'],
        dependency_artifacts_verified=11 if artifacts is not None else 0,source_closure_verified=source_verified,current_preflight_verified=metadata_verified,
        automatic_retry=False,test_injection_used=True,production_runtime_qualified=False,execution_authorized=False,
        feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])

def supervise(plan):
    require_invented(plan['packet'])
    contract.validate_request(plan['request'])
    check_launch(request=plan['request'],request_path=plan['request_path'],folder=plan['folder'],packet=plan['packet'],context=plan['context'],validated=plan['validated'])
    control=plan['control'];context=plan['context'];loader=plan['validation_loader']
    records=RecordOwner(None);primary=None;narrow=None;mount_attempted=False;launched=[]
    def spawn(argv,cwd):
        proc=subprocess.Popen(argv,cwd=cwd,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0,shell=False,close_fds=True)
        launched.append(proc)
        return proc
    try:
        records.original=control.reserve_parent(context=context)
        mount_attempted=True
        sys.meta_path.insert(0,loader)
        code,narrow=control.run_parent_reserved(context=context,records=records,spawn=spawn,monotonic=time.monotonic,sleep=time.sleep)
    except BaseException as error:primary=error
    finally:
        if not loader.closed:
            try:
                loader.close()
            except BaseException as error:
                if primary is None:primary=error
        if records.original is not None and not records.attempted:
            try:records.close()
            except BaseException as error:
                if primary is None:primary=error
    if narrow is None:
        process=dict(launch_attempts=len(launched),child_pids=[proc.pid for proc in launched],exit_observed=False,disposition='not_launched' if not launched else 'unknown_after_supervisor_exception')
        narrow=dict(host_exit_code=1,terminal_records_agree=False,status='needs_review',process_observation=process)
    if primary is not None:
        narrow=dict(narrow,host_exit_code=1,status='needs_review')
    return narrow,dict(parent_records_close_attempted=records.attempted,
        parent_records_closed=records.closed,parent_loader_mount_attempted=mount_attempted,
        parent_failure_type=None if primary is None else type(primary).__name__)

def run_invented(plan):
    """Parent helper ownership spans supervision and reconciliation."""
    owner=plan['verifier'];primary=None;result=None;close_attempted=False;adapter_close_attempted=False
    try:
        require_invented(plan['packet'])
        narrow,ownership=supervise(plan)
        result=reconcile(plan,narrow)
        result.update(ownership)
        owner.intact()
    except BaseException as error:primary=error
    finally:
        if not owner.closed:
            close_attempted=True
            try:owner.close()
            except BaseException as cleanup:
                if primary is None:primary=cleanup
        if not plan['adapter_owner'].closed:
            adapter_close_attempted=True
            try:plan['adapter_owner'].close()
            except BaseException as cleanup:
                if primary is None:primary=cleanup
        if not plan['validation_loader'].closed:
            try:plan['validation_loader'].close()
            except BaseException as cleanup:
                if primary is None:primary=cleanup
        try:plan['bootstrap_owner'].close()
        except BaseException as cleanup:
            if primary is None:primary=cleanup
    if result is None:
        if primary is not None:raise primary
        raise ValueError('missing_parent_result')
    result['parent_validation_loader_closed']=plan['validation_loader'].closed
    result['parent_bootstrap_closed']=plan['bootstrap_owner'].closed
    result['parent_bootstrap_aliases_absent']=all(n not in sys.modules for n in plan['bootstrap_owner'].modules)
    result['parent_helper_close_attempted']=close_attempted
    result['parent_helper_closed']=owner.closed
    result['adapter_parent_close_attempted']=adapter_close_attempted
    result['adapter_parent_closed']=plan['adapter_owner'].closed
    result['parent_helper_failure_type']=None if primary is None else type(primary).__name__
    if primary is not None or result['parent_failure_type'] is not None:
        result.update(status='needs_review',completion_outcome='unknown',host_exit_code=1)
    try:write(plan['folder']/'final-receipt.json',canonical(result))
    except BaseException as publication:
        if primary is not None:raise primary from publication
        raise
    return result



def run_runtime(**kwargs):
    raise ValueError("real_activation_pending")
