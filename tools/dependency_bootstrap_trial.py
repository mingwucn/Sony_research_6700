"""Synthetic-only original-method trial; ordinary invocation refuses.

This cooperatively source-bound child is not executable authentication or a
native sandbox. All module origins and native events are invented declarations.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import types

FILES={'trial':'dependency_bootstrap_trial.py','journal':'dependency_bootstrap_journal.py',
       'core':'dependency_evidence.py','producer':'dependency_producer.py'}
TRUSTED=('ctypes','_ctypes','ctypes.util','ctypes._endian','platform')
SCENARIOS=('complete','no_native_events','reversed_native_events','duplicate_native_event',
    'unexpected_native_event','origin_drift','extra_import','actual_native_event','package_import',
    'stdout_flood','stderr_flood','stall','nonzero','journal_flood','bad_serialization')
SUCCESS=('complete','no_native_events','reversed_native_events')
FLAGS=('original_native_bootstrap_executed','installed_dependency_activated','actual_runtime_verified',
       'producer_execution_authenticated','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed')

def need(value,code):
    if not value:raise ValueError(code)

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',', ':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def write_new(path,raw):
    need(type(raw) is bytes and len(raw)<=65536,'trial_output_bound')
    with Path(path).open('xb',buffering=0) as stream:
        need(stream.write(raw)==len(raw),'trial_short_write');os.fsync(stream.fileno())

def origins():return {name:'X:/invented-runtime/'+name.replace('.','/')+'.py' for name in TRUSTED}

def native_plan(scenario):
    if scenario=='no_native_events':return []
    if scenario=='reversed_native_events':return ['kernel32',None]
    if scenario=='duplicate_native_event':return [None,None]
    if scenario=='unexpected_native_event':return ['unapproved-invented-library']
    return [None,'kernel32']

def validate_request(request):
    need(type(request) is dict and set(request)=={'schema','invented','operation_id','scenario','folder','sources','source_roots',
         'execution_authorized','camera_commands'},'trial_request_shape')
    need(request['schema']=='invented_bootstrap_only_request_v1' and request['invented'] is True and
         request['execution_authorized'] is False and request['camera_commands']==[],'trial_request_mode')
    op=request['operation_id']
    need(type(op) is str and len(op)==32 and all(c in '0123456789abcdef' for c in op),'trial_operation')
    need(type(request['scenario']) is str and request['scenario'] in SCENARIOS,'trial_scenario')
    need(type(request['folder']) is str and Path(request['folder']).is_absolute() and '..' not in Path(request['folder']).parts,'trial_folder')
    need(type(request['sources']) is dict and set(request['sources'])==set(FILES),'trial_sources')
    paths=set()
    for role,row in request['sources'].items():
        need(type(row) is dict and set(row)=={'path','size','sha256','lstat','fstat'} and type(row['path']) is str and
            0<len(row['path'])<=1024 and Path(row['path']).is_absolute() and
            Path(row['path'])==Path(__file__).parent/FILES[role] and '..' not in Path(row['path']).parts and
            row['path'].casefold() not in paths,'trial_source_path')
        paths.add(row['path'].casefold())
        need(type(row['size']) is int and 0<row['size']<=2*1024**2 and type(row['sha256']) is str and
            len(row['sha256'])==64 and all(c in '0123456789abcdef' for c in row['sha256']),'trial_source_receipt')
        for kind in ('lstat','fstat'):
            need(type(row[kind]) is list and len(row[kind])==8 and all(type(v) is int for v in row[kind]),'trial_source_stamp')
    need(type(request['source_roots']) is list and 1<=len(request['source_roots'])<=64,'trial_source_roots')
    for row in request['source_roots']:
        need(type(row) is list and len(row)==5 and type(row[0]) is str and
            all(type(v) is int for v in row[1:]),'trial_source_roots')
    return request


BOOTSTRAP=r'''
import hashlib,json,os,stat,sys,types
from pathlib import Path
def need(x):
 if not x:raise ValueError('invented_trial_bootstrap_binding')
def read(path,limit):
 with open(path,'rb') as f:data=f.read(limit+1)
 need(len(data)<=limit);return data
def stamp(v):return [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns,getattr(v,'st_file_attributes',0)]
def roots(path):
 rows=[]
 for p in reversed((path,*path.parents)):
  v=os.lstat(p);need(stat.S_ISDIR(v.st_mode) and not getattr(v,'st_file_attributes',0)&0x400)
  rows.append([str(p),v.st_dev,v.st_ino,v.st_mode,getattr(v,'st_file_attributes',0)])
 return rows
def source(row):
 path=row['path'];before=os.lstat(path)
 need(stat.S_ISREG(before.st_mode) and before.st_nlink==1 and not getattr(before,'st_file_attributes',0)&0x400 and stamp(before)==row['lstat'])
 fd=os.open(path,os.O_RDONLY|getattr(os,'O_BINARY',0)|getattr(os,'O_NOFOLLOW',0))
 try:
  opened=os.fstat(fd);need(stamp(opened)==row['fstat']);chunks=[];size=0
  while True:
   raw=os.read(fd,min(65536,2*1024**2+1-size))
   if not raw:break
   size+=len(raw);need(size<=2*1024**2);chunks.append(raw)
  need(stamp(os.fstat(fd))==row['fstat'])
 finally:os.close(fd)
 need(stamp(os.lstat(path))==row['lstat']);data=b''.join(chunks)
 need(len(data)==row['size'] and hashlib.sha256(data).hexdigest()==row['sha256']);return data
try:
 raw=read(sys.argv[1],65536);need(hashlib.sha256(raw).hexdigest()==sys.argv[2]);request=json.loads(raw)
 need(json.dumps(request,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')==raw)
 need(request['schema']=='invented_bootstrap_only_request_v1' and request['invented'] is True and request['execution_authorized'] is False and request['camera_commands']==[])
 names={'trial':'dependency_bootstrap_trial.py','journal':'dependency_bootstrap_journal.py','core':'dependency_evidence.py','producer':'dependency_producer.py'}
 need(set(request['sources'])==set(names));buffers={};source_parent=Path(request['sources']['trial']['path']).parent
 need(roots(source_parent)==request['source_roots'])
 for role,row in request['sources'].items():
  need(Path(row['path']).is_absolute() and Path(row['path'])==source_parent/names[role] and '..' not in Path(row['path']).parts)
  buffers[role]=source(row)
 need(roots(source_parent)==request['source_roots'])
 folder=Path(request['folder']);allowed={str(Path(v['path'])) for v in request['sources'].values()}
 def audit(event,args):
  if event.startswith(('socket.','ctypes.','subprocess.','os.spawn','os.posix_spawn','os.exec')) or event=='os.system':raise ValueError('synthetic_native_network_process_denied')
  if event=='import' and args[0].split('.')[0] in ('ctypes','_ctypes','Crypto','Cryptodome','cffi','_cffi_backend','pycparser'):raise ValueError('synthetic_installed_import_denied')
  if event=='open' and type(args[0]) is str:
   path=Path(args[0]);need(str(path) in allowed or path.is_relative_to(folder) or path.is_relative_to(Path(sys.base_prefix)))
 sys.addaudithook(audit)
 package=types.ModuleType('tools');package.__path__=[];sys.modules['tools']=package;modules={}
 for role in ('core','producer','journal','trial'):
  alias='tools.'+Path(names[role]).stem;module=types.ModuleType(alias);module.__file__=request['sources'][role]['path']
  sys.modules[alias]=module;setattr(package,Path(names[role]).stem,module)
  exec(compile(buffers[role],'<captured:'+role+'>','exec',dont_inherit=True,optimize=0),vars(module));modules[role]=module
 modules['trial'].validate_request(request)
 modules['trial']._child(request,modules,sys.argv[2])
except BaseException:
 os.write(2,b'invented_bootstrap_needs_review\n');raise SystemExit(2)
'''


def _child(request,modules,request_sha256):
    scenario=request['scenario'];folder=Path(request['folder']);producer=modules['producer']
    need(tuple(producer.TRUSTED)==TRUSTED,'trial_original_roster')
    if scenario=='stdout_flood':os.write(1,b'x'*131072)
    if scenario=='stderr_flood':os.write(2,b'x'*131072)
    if scenario=='stall':
        import time
        time.sleep(60)
    if scenario=='nonzero':raise ValueError('invented_nonzero')
    journal=modules['journal'].Journal(folder/'journal.jsonl')
    original=producer.importlib;method=producer.RuntimeOps.bootstrap;seen=[];count={None:0,'kernel32':0}
    class Adapter:
        def import_module(self,name):
            need(name in TRUSTED and name not in seen,'trial_inert_import')
            seen.append(name);journal.emit('invented.import',(name,))
            if name=='ctypes':
                for argument in native_plan(scenario):
                    need(argument in count and count[argument]==0,'trial_inert_native_policy')
                    count[argument]+=1;journal.emit('invented.native',(argument,))
            module=types.ModuleType(name);module.__file__=origins()[name]
            if scenario=='origin_drift' and name=='platform':module.__file__='X:/wrong.py'
            return module
    adapter=Adapter();old_profile=sys.getprofile();trace=[];primary=None
    def profile(frame,event,arg):
        if event=='call' and frame.f_code.co_filename=='<captured:producer>':
            need(frame.f_code.co_name in ('bootstrap','<dictcomp>'),'trial_forbidden_continuation')
            trace.append(frame.f_code.co_name)
    try:
        journal.emit('trial.started',('invented_adapter',request['operation_id']))
        if scenario=='journal_flood':
            for i in range(257):journal.emit('invented.flood',(str(i),))
        if scenario=='bad_serialization':journal.emit('invented.bad',(object(),))
        producer.importlib=adapter;sys.setprofile(profile)
        observer=producer.RuntimeOps();returned=observer.bootstrap()
        sys.setprofile(old_profile)
        need(producer.RuntimeOps.bootstrap is method and observer.__dict__=={},'trial_method_ownership')
        need(tuple(seen)==TRUSTED and set(returned)==set(TRUSTED),'trial_import_roster')
        for name in TRUSTED:
            need(returned[name].__file__==origins()[name],'trial_origin')
            journal.emit('invented.origin',(name,returned[name].__file__))
        if scenario=='extra_import':adapter.import_module('not_in_roster')
        if scenario=='package_import':adapter.import_module('Cryptodome')
        if scenario=='actual_native_event':sys.audit('ctypes.dlopen',None)
        journal.emit('bootstrap.only_stop',('before_package_imports',))
    except BaseException as error:
        primary=error
        raise
    finally:
        sys.setprofile(old_profile)
        owned=producer.importlib is adapter or producer.importlib is original
        if owned:producer.importlib=original
        try:journal.close()
        except BaseException:
            if primary is None:raise
        need(owned and producer.importlib is original,'trial_adapter_ownership')
    need(trace.count('bootstrap')==1,'trial_method_count')
    data=(folder/'journal.jsonl').read_bytes()
    result=dict(schema='invented_bootstrap_only_result_v1',status='complete_invented_bootstrap_only',
        request_sha256=request_sha256,source_sha256={k:v['sha256'] for k,v in request['sources'].items()},
        pid=os.getpid(),isolated=sys.flags.isolated,no_site=sys.flags.no_site,no_user_site=sys.flags.no_user_site,
        no_bytecode=sys.dont_write_bytecode,optimize=sys.flags.optimize,imports=seen,origins=origins(),
        bootstrap_calls=trace.count('bootstrap'),adapter_restored=True,stop='before_package_imports',
        events_are_invented_adapter_declarations=True,journal_sha256=sha(data),journal_events=len(data.splitlines()),
        camera_commands=[],**{k:False for k in FLAGS})
    write_new(folder/'result.json',canonical(result))


def prepare_invented(folder,*,scenario='complete'):
    from tools import dependency_child_entry as entry
    import uuid
    need(scenario in SCENARIOS,'trial_scenario');folder=Path(folder)
    need(folder.is_absolute() and '..' not in folder.parts,'trial_folder')
    rows={role:entry.read_source(str(Path(__file__).parent/name))[1] for role,name in FILES.items()}
    request=dict(schema='invented_bootstrap_only_request_v1',invented=True,operation_id=uuid.uuid4().hex,
        scenario=scenario,folder=str(folder),sources=rows,source_roots=entry.roots(str(Path(__file__).parent)),
        execution_authorized=False,camera_commands=[])
    validate_request(request);raw=canonical(request);need(len(raw)<=65536,'trial_request_bound')
    folder.mkdir(exist_ok=False);write_new(folder/'request.json',raw)
    return dict(request=request,request_bytes=raw,folder=folder)


def _expected_journal(request):
    # Independent fixed grammar: trial events use tuples containing str/None.
    rows=[]
    def event(name,args):
        typed=dict(type='tuple',items=[dict(type='none') if x is None else dict(type='str',value=x) for x in args])
        rows.append(dict(sequence=len(rows)+1,event=name,arguments=typed))
    event('trial.started',('invented_adapter',request['operation_id']))
    for name in TRUSTED:
        event('invented.import',(name,))
        if name=='ctypes':
            for arg in native_plan(request['scenario']):event('invented.native',(arg,))
    for name in TRUSTED:event('invented.origin',(name,origins()[name]))
    event('bootstrap.only_stop',('before_package_imports',))
    return b''.join(canonical(row)+b'\n' for row in rows)


def verify_invented(*,request,journal,result,process):
    validate_request(request);need(request['scenario'] in SUCCESS,'trial_fault_cannot_complete')
    need(process['status']=='complete' and process['returncode']==0 and process['stdout']==process['stderr']==b'','trial_process')
    need(type(journal) is bytes and len(journal)<=262144 and all(len(line)+1<=4096 for line in journal.splitlines()) and
        len(journal.splitlines())<=256 and journal==_expected_journal(request),'trial_journal')
    need(type(result) is bytes and len(result)<=65536,'trial_result_bound')
    row=json.loads(result)
    expected=dict(schema='invented_bootstrap_only_result_v1',status='complete_invented_bootstrap_only',
        request_sha256=sha(canonical(request)),source_sha256={k:v['sha256'] for k,v in request['sources'].items()},
        pid=process['pid'],isolated=1,no_site=1,no_user_site=1,no_bytecode=True,optimize=0,
        imports=list(TRUSTED),origins=origins(),bootstrap_calls=1,adapter_restored=True,stop='before_package_imports',
        events_are_invented_adapter_declarations=True,journal_sha256=sha(journal),journal_events=len(journal.splitlines()),
        camera_commands=[],**{k:False for k in FLAGS})
    need(canonical(row)==result==canonical(expected),'trial_result')
    return dict(status='consistent_invented_bootstrap_only',journal_events=len(journal.splitlines()),
        journal_sha256=sha(journal),result_sha256=sha(result),**{k:False for k in FLAGS},camera_commands=[])


def run_prepared(prepared,*,timeout=30):
    from tools import dependency_bootstrap_supervisor as supervisor
    from tools import dependency_child_entry as entry
    request=prepared['request'];validate_request(request);folder=Path(request['folder'])
    need(prepared['request_bytes']==canonical(request) and (folder/'request.json').read_bytes()==prepared['request_bytes'],'trial_saved_request')
    def intact():
        need(entry.roots(str(Path(__file__).parent))==request['source_roots'],'trial_roots_changed')
        for row in request['sources'].values():
            need(entry.read_source(row['path'])[1]==row,'trial_source_changed')
    intact()
    write_new(folder/'started.json',canonical(dict(request_sha256=sha(prepared['request_bytes']),automatic_retry=False,camera_commands=[])))
    argv=[sys.executable,'-I','-S','-B','-X','utf8','-c',BOOTSTRAP,str(folder/'request.json'),sha(prepared['request_bytes'])]
    process=supervisor.run_once(argv,timeout=timeout)
    answer=dict(status='needs_review',process=process,verification=None,automatic_retry=False,camera_commands=[])
    if process['status']=='complete' and process['returncode']==0:
        try:
            intact()
            need({p.name for p in folder.iterdir()}=={'request.json','started.json','journal.jsonl','result.json'},'trial_artifact_roster')
            def bounded(name,limit):
                with (folder/name).open('rb') as stream:data=stream.read(limit+1)
                need(len(data)<=limit,'trial_artifact_bound');return data
            answer['verification']=verify_invented(request=request,journal=bounded('journal.jsonl',262144),
                result=bounded('result.json',65536),process=process)
            answer['status']='complete_invented_bootstrap_only'
        except (ValueError,OSError):pass
    facts={k:v for k,v in process.items() if k not in ('stdout','stderr')}
    write_new(folder/'stdout.bin',process['stdout'])
    write_new(folder/'stderr.bin',process['stderr'])
    facts.update(stdout_bytes=len(process['stdout']),stderr_bytes=len(process['stderr']),
        stdout_sha256=sha(process['stdout']),stderr_sha256=sha(process['stderr']),trial_status=answer['status'])
    write_new(folder/'supervision.json',canonical(facts))
    return answer


def run_runtime(**kwargs):raise ValueError('real_activation_pending')
if __name__=='__main__':raise SystemExit(2)
