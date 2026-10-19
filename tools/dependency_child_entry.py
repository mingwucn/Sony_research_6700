"""Bound-buffer disposable child with separately gated dependency collection.

Authored helpers execute only from checked buffers. The refusing ordinary CLI
does not activate this API. Caller pins/review declarations are not consent.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import types


FILES = {'entry': 'dependency_child_entry.py', 'core': 'dependency_evidence.py',
         'producer': 'dependency_producer.py'}
COMPOSITION_FILES = dict(FILES, invented='dependency_invented.py')
COLLECTION_FILES = dict(FILES, collector='dependency_package_preflight.py', execution='dependency_execution.py')


def require(condition, code):
    if not condition: raise ValueError(code)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def sha(raw): return hashlib.sha256(raw).hexdigest()


def strict_json(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            require(key not in result, 'duplicate_key'); result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs)


def roots(path):
    rows = []
    for item in reversed((Path(path), *Path(path).parents)):
        value = os.lstat(item)
        require(stat.S_ISDIR(value.st_mode) and not getattr(value, 'st_file_attributes', 0) & 0x400, 'directory_kind')
        rows.append([str(item), value.st_dev, value.st_ino, value.st_mode, getattr(value, 'st_file_attributes', 0)])
    return rows


def stamp(value):
    return [value.st_dev, value.st_ino, value.st_mode, value.st_nlink, value.st_size,
            value.st_mtime_ns, value.st_ctime_ns, getattr(value, 'st_file_attributes', 0)]


def read_source(path, limit=2*1024**2):
    ancestors = roots(str(Path(path).parent)); before = os.lstat(path)
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
            not getattr(before, 'st_file_attributes', 0) & 0x400 and before.st_size <= limit, 'source_kind')
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_BINARY', 0) | getattr(os, 'O_NOFOLLOW', 0))
    try:
        opened = os.fstat(fd)
        require(stamp(before)[:6] == stamp(opened)[:6] and
                not getattr(opened, 'st_file_attributes', 0) & 0x400, 'source_identity')
        chunks = []; size = 0
        while True:
            raw = os.read(fd, min(65536, limit+1-size))
            if not raw: break
            size += len(raw); require(size <= limit, 'source_bound'); chunks.append(raw)
        final = os.fstat(fd)
    finally: os.close(fd)
    after = os.lstat(path); raw = b''.join(chunks)
    require(stamp(before) == stamp(after) and stamp(opened) == stamp(final) and len(raw) == before.st_size
            and ancestors == roots(str(Path(path).parent)), 'source_changed')
    return raw, dict(path=path, size=len(raw), sha256=sha(raw), lstat=stamp(before), fstat=stamp(opened))


def runtime_profile():
    """Ordinary runtime observations, not interpreter binary authentication."""
    return dict(implementation=sys.implementation.name, version=list(sys.version_info[:3]),
        version_text=sys.version, cache_tag=sys.implementation.cache_tag,
        executable=sys.executable, base_executable=getattr(sys, '_base_executable', sys.executable),
        prefix=sys.prefix, base_prefix=sys.base_prefix, platform=sys.platform,
        maxsize=sys.maxsize, path=list(sys.path), isolated=sys.flags.isolated,
        no_site=sys.flags.no_site, no_user_site=sys.flags.no_user_site,
        no_bytecode=sys.dont_write_bytecode, optimize=sys.flags.optimize)


# This standalone bootstrap verifies every source buffer before executing any
# authored module. Stdlib/interpreter startup remains the trusted boundary.
BOOTSTRAP = r'''
import hashlib,json,os,stat,sys,types
from pathlib import Path
def need(ok,code):
 if not ok:raise ValueError(code)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def stamp(v):return [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns,getattr(v,'st_file_attributes',0)]
def roots(path):
 rows=[]
 for p in reversed((Path(path),*Path(path).parents)):
  v=os.lstat(p);need(stat.S_ISDIR(v.st_mode) and not getattr(v,'st_file_attributes',0)&0x400,'directory_kind')
  rows.append([str(p),v.st_dev,v.st_ino,v.st_mode,getattr(v,'st_file_attributes',0)])
 return rows
def read(path,limit):
 ancestors=roots(str(Path(path).parent));a=os.lstat(path)
 need(stat.S_ISREG(a.st_mode) and a.st_nlink==1 and not getattr(a,'st_file_attributes',0)&0x400 and a.st_size<=limit,'source_kind')
 fd=os.open(path,os.O_RDONLY|getattr(os,'O_BINARY',0)|getattr(os,'O_NOFOLLOW',0))
 try:
  b=os.fstat(fd);need(stamp(a)[:6]==stamp(b)[:6] and not getattr(b,'st_file_attributes',0)&0x400,'source_identity');chunks=[];total=0
  while True:
   raw=os.read(fd,min(65536,limit+1-total))
   if not raw:break
   total+=len(raw);need(total<=limit,'source_bound');chunks.append(raw)
  c=os.fstat(fd)
 finally:os.close(fd)
 d=os.lstat(path);raw=b''.join(chunks)
 need(stamp(a)==stamp(d) and stamp(b)==stamp(c) and len(raw)==a.st_size and ancestors==roots(str(Path(path).parent)),'source_changed')
 return raw,dict(path=path,size=len(raw),sha256=digest(raw),lstat=stamp(a),fstat=stamp(b))
def pairs(rows):
 result={}
 for k,v in rows:
  need(k not in result,'duplicate_key');result[k]=v
 return result
try:
 need(len(sys.argv)==3,'arguments')
 raw,_=read(sys.argv[1],65536);need(digest(raw)==sys.argv[2],'request_hash')
 request=json.loads(raw,object_pairs_hook=pairs)
 need(type(request) is dict,'request_shape')
 composed=request.get('schema')=='dependency_child_invented_request_v1'
 collected=request.get('schema')=='dependency_child_collection_request_v1'
 keys={'schema','sources','source_root','source_root_identity','expected_runtime','bootstrap_sha256','review_sha256'}
 need(set(request)==(keys|{'collection'} if collected else keys|{'composition'} if composed else keys),'request_shape')
 need(collected or composed or request['schema']=='dependency_child_preflight_request_v1','request_schema')
 def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
 need(canonical(request['source_root_identity'])==canonical(roots(request['source_root'])),'root_identity')
 buffers={};receipts={};total=0
 names={'entry':'dependency_child_entry.py','core':'dependency_evidence.py','producer':'dependency_producer.py'}
 if composed:names['invented']='dependency_invented.py'
 if collected:
  c=request['collection'];need(type(c) is dict and set(c)=={'mode','packet','fixed'},'collection_shape')
  need(c['mode'] in ('invented','runtime'),'collection_mode')
  names.update(collector='dependency_package_preflight.py',execution='dependency_execution.py')
  if c['mode']=='invented':names['invented']='dependency_invented.py'
 need(type(request['sources']) is dict and set(request['sources'])==set(names),'source_roster')
 for role,row in request['sources'].items():
  need(type(row) is dict and set(row)=={'path','size','sha256','lstat','fstat'},'source_shape')
  need(row['path']==str(Path(request['source_root'])/names[role]),'source_path')
  buf,receipt=read(row['path'],2*1024**2);need(canonical(receipt)==canonical(row),'source_binding')
  total+=len(buf);need(total<=4*1024**2,'source_bound');buffers[role]=buf;receipts[role]=receipt
 need(canonical(request['source_root_identity'])==canonical(roots(request['source_root'])),'root_changed')
 packet=None
 if composed or collected:
  c=request['collection'] if collected else request['composition']
  if composed:need(type(c) is dict and set(c)=={'packet','fixed'},'composition_shape')
  packet_raw,packet_receipt=read(c['packet']['path'],4*1024**2)
  need(canonical(packet_receipt)==canonical(c['packet']),'packet_binding')
  packet=json.loads(packet_raw,object_pairs_hook=pairs)
 observed=dict(implementation=sys.implementation.name,version=list(sys.version_info[:3]),version_text=sys.version,
  cache_tag=sys.implementation.cache_tag,executable=sys.executable,base_executable=getattr(sys,'_base_executable',sys.executable),
  prefix=sys.prefix,base_prefix=sys.base_prefix,platform=sys.platform,maxsize=sys.maxsize,path=list(sys.path),
  isolated=sys.flags.isolated,no_site=sys.flags.no_site,no_user_site=sys.flags.no_user_site,
  no_bytecode=sys.dont_write_bytecode,optimize=sys.flags.optimize)
 need(canonical(observed)==canonical(request['expected_runtime']),'runtime_binding')
 need(observed['implementation']=='cpython' and observed['isolated']==1 and observed['no_site']==1 and
  observed['no_user_site']==1 and observed['no_bytecode'] is True and observed['optimize']==0,'runtime_flags')
 entry=types.ModuleType('__dependency_child_bound__');entry.__file__=receipts['entry']['path']
 exec(compile(buffers['entry'],entry.__file__,'exec',dont_inherit=True,optimize=0),entry.__dict__)
 result=entry.child_preflight(request,buffers,receipts,packet=packet,folder=str(Path(sys.argv[1]).parent))
 print(json.dumps(result,sort_keys=True,separators=(',',':')))
except BaseException:
 print(json.dumps(dict(status='needs_review',code='child_preflight_refused',camera_commands=[])))
 raise SystemExit(2)
'''


def freeze_request(*, source_root, expected_runtime, review_sha256):
    """Capture authored source identities before the child. This is not approval."""
    source_root = str(Path(source_root).absolute())
    require(type(review_sha256) is str and len(review_sha256) == 64 and
            all(c in '0123456789abcdef' for c in review_sha256), 'review_digest')
    before = roots(source_root)
    sources = {role: read_source(str(Path(source_root)/name))[1] for role, name in FILES.items()}
    require(before == roots(source_root), 'root_changed')
    request = dict(schema='dependency_child_preflight_request_v1', sources=sources,
        source_root=source_root, source_root_identity=before, expected_runtime=expected_runtime,
        bootstrap_sha256=sha(BOOTSTRAP.encode('utf-8')), review_sha256=review_sha256)
    require(len(canonical(request)) <= 65536, 'request_bound')
    return json.loads(canonical(request))


def freeze_composition(*, source_root, expected_runtime, review_sha256, packet_path, packet_sha256, fixed):
    """Invented-only successor. Caller fixes package/root expectations beforehand."""
    request = freeze_request(source_root=source_root, expected_runtime=expected_runtime, review_sha256=review_sha256)
    source_root = request['source_root']
    request['sources']['invented'] = read_source(str(Path(source_root)/COMPOSITION_FILES['invented']))[1]
    require(request['source_root_identity'] == roots(source_root), 'root_changed')
    raw, receipt = read_source(str(Path(packet_path).absolute()), limit=4*1024**2)
    require(sha(raw) == packet_sha256, 'packet_hash')
    request.update(schema='dependency_child_invented_request_v1', composition=dict(packet=receipt, fixed=fixed))
    require(len(canonical(request)) <= 65536, 'request_bound')
    return json.loads(canonical(request))


def freeze_collection(*, source_root, expected_runtime, review_sha256, packet_path, packet_sha256, fixed, mode):
    """Freeze exact authored/input identities. This does not authorize a launch."""
    require(mode in ('invented','runtime'),'collection_mode')
    request=freeze_request(source_root=source_root,expected_runtime=expected_runtime,review_sha256=review_sha256)
    names=dict(COLLECTION_FILES)
    if mode=='invented':names['invented']='dependency_invented.py'
    request['sources']={k:read_source(str(Path(request['source_root'])/v))[1] for k,v in names.items()}
    require(request['source_root_identity']==roots(request['source_root']),'root_changed')
    raw,receipt=read_source(str(Path(packet_path).absolute()),limit=4*1024**2)
    require(sha(raw)==packet_sha256,'packet_hash')
    request.update(schema='dependency_child_collection_request_v1',collection=dict(mode=mode,packet=receipt,fixed=fixed))
    require(len(canonical(request))<=65536,'request_bound')
    return json.loads(canonical(request))


def child_preflight(request, buffers, receipts, *, packet=None, folder=None):
    """Bound child body, called only after every source/input buffer is checked."""
    observed = runtime_profile()
    require(canonical(observed) == canonical(request['expected_runtime']), 'runtime_binding')
    require(observed['implementation'] == 'cpython' and observed['isolated'] == 1 and
            observed['no_site'] == 1 and observed['no_user_site'] == 1 and
            observed['no_bytecode'] is True and observed['optimize'] == 0, 'runtime_flags')
    original_argv = sys.orig_argv
    bootstrap = original_argv[original_argv.index('-c')+1]
    require(sha(bootstrap.encode('utf-8')) == request['bootstrap_sha256'] == sha(BOOTSTRAP.encode('utf-8')), 'bootstrap_binding')
    require(not any(name == 'tools' or name.startswith('tools.') or name == 'Cryptodome' or
                    name.startswith('Cryptodome.') for name in sys.modules), 'preloaded_alias')
    package = types.ModuleType('tools'); package.__path__ = []; sys.modules['tools'] = package
    roles = [('core', 'dependency_evidence'), ('producer', 'dependency_producer')]
    composed = request['schema'] == 'dependency_child_invented_request_v1'
    collected = request['schema'] == 'dependency_child_collection_request_v1'
    if collected:
        # Ordinary trusted origins must not be preloaded before their fresh
        # collection/bootstrap interval. Interpreter/stdlib remain trusted.
        require(not any(n.split('.')[0] in ('ctypes','_ctypes','platform','cffi','_cffi_backend','pycparser')
                        for n in sys.modules),'preloaded_runtime_origin')
        roles.extend([('collector','dependency_package_preflight'),('execution','dependency_execution')])
        if request['collection']['mode']=='invented':roles.append(('invented','dependency_invented'))
    if composed: roles.append(('invented', 'dependency_invented'))
    for role, alias in roles:
        module = types.ModuleType('tools.'+alias); module.__file__ = receipts[role]['path']
        module.__package__ = 'tools'; sys.modules[module.__name__] = module; setattr(package, alias, module)
        exec(compile(buffers[role], module.__file__, 'exec', dont_inherit=True, optimize=0), module.__dict__)
    producer = package.dependency_producer
    if collected:
        require(not any(n.split('.')[0] in ('ctypes','_ctypes','platform','cffi','_cffi_backend','pycparser')
                        for n in sys.modules),'preloaded_runtime_origin')
        c=request['collection'];target=str(Path(folder)/'collected')
        if c['mode']=='invented':
            artifacts=package.dependency_invented.execute(packet,c['fixed'],buffers,request['review_sha256'],target,collected=True)
        else:
            data=package.dependency_execution.bind_runtime_packet(packet,c['fixed'],buffers,request['review_sha256'])
            package.dependency_execution.produce_collected_runtime(inputs=data,folder=target)
            artifacts=package.dependency_execution.validate_saved_composition(target,data,invented=False)
        return collection_result(request,artifacts)
    if composed:
        artifacts = package.dependency_invented.execute(packet, request['composition']['fixed'],
            buffers, request['review_sha256'], str(Path(folder)/'producer'))
        return composition_result(request, artifacts)
    guard = producer.Guard({'native_libraries': {}}, None, lambda *args: None)
    try:
        operations = producer.RuntimeOps(); operations.audit_install(guard.audit); operations.audit_probe(guard.probe_token)
        require(guard.probe_count == 1 and not guard.failed, 'audit_not_acknowledged')
    finally: guard.active = False
    sys.audit(producer.PROBE_EVENT, 'inert_after_cleanup')
    return dict(schema='dependency_child_preflight_result_v1', status='authored_source_child_preflight_complete',
        request_sha256=sha(canonical(request)), source_sha256={role: sha(raw) for role, raw in buffers.items()},
        runtime_profile=observed, audit_hook_acknowledged=True, audit_hook_retained_inert=True,
        exact_child_source_buffers_executed=True, parent_execution_authenticated=False,
        prior_review_proven=False, installed_dependency_bootstrap_performed=False,
        actual_dependency_observation_performed=False, operational_acceptance=False,
        execution_authorized=False, feature_supported=False, recovery_proven=False,
        device_write_gate_passed=False, camera_commands=[])


def composition_result(request, artifacts):
    return dict(schema='dependency_child_invented_result_v1', status='invented_child_producer_complete',
        request_sha256=sha(canonical(request)), source_sha256={k: v['sha256'] for k, v in request['sources'].items()},
        runtime_profile=request['expected_runtime'], packet_sha256=request['composition']['packet']['sha256'],
        fixed=request['composition']['fixed'], artifact_sha256=artifacts,
        simulated_native_loads=5, callback_calls=1, simulated_cipher_calls=48,
        test_injection_used=True, audit_hook_acknowledged=True, audit_hook_retained_inert=True,
        exact_child_source_buffers_executed=True, parent_execution_authenticated=False, prior_review_proven=False,
        installed_dependency_bootstrap_performed=False, actual_dependency_observation_performed=False,
        operational_acceptance=False, execution_authorized=False, feature_supported=False,
        recovery_proven=False, device_write_gate_passed=False, camera_commands=[])


def collection_result(request, artifacts):
    invented=request['collection']['mode']=='invented'
    return dict(schema='dependency_child_collection_result_v1',
        status='invented_collected_child_complete' if invented else 'runtime_collected_child_complete',
        request_sha256=sha(canonical(request)),source_sha256={k:r['sha256'] for k,r in request['sources'].items()},
        runtime_profile=request['expected_runtime'],packet_sha256=request['collection']['packet']['sha256'],
        fixed=request['collection']['fixed'],artifact_sha256=artifacts,test_injection_used=invented,
        audit_hook_acknowledged=True,audit_hook_retained_inert=True,exact_child_source_buffers_executed=True,
        parent_execution_authenticated=False,prior_review_proven=False,
        actual_dependency_observation_performed=not invented,installed_dependency_bootstrap_performed=not invented,
        operational_acceptance=False,execution_authorized=False,feature_supported=False,recovery_proven=False,
        device_write_gate_passed=False,camera_commands=[])


def run_preflight(*, request, folder, timeout=15):
    """Once-only bound child; actual activation requires its own reviewed packet."""
    require(type(timeout) in (int, float) and 0 < timeout <= 30, 'timeout_bound')
    raw = canonical(request); require(len(raw) <= 65536, 'request_bound')
    folder = Path(folder); folder.mkdir(exist_ok=False)
    with (folder/'request.json').open('xb') as out: out.write(raw); out.flush(); os.fsync(out.fileno())
    argv = [sys.executable, '-I', '-S', '-B', '-X', 'utf8', '-c', BOOTSTRAP,
            str((folder/'request.json').absolute()), sha(raw)]
    with (folder/'started.json').open('xb') as out:
        out.write(canonical(dict(schema='dependency_child_preflight_started_v1',request_sha256=sha(raw),
            interpreter=sys.executable,bootstrap_sha256=sha(BOOTSTRAP.encode()),automatic_retry=False)))
        out.flush(); os.fsync(out.fileno())
    status = 'needs_review'; result = None; process = None; exit_code = None; termination = 'not_started'
    kill_attempted = False
    with (folder/'stdout.json').open('xb', buffering=0) as stdout, (folder/'stderr.log').open('xb', buffering=0) as stderr:
        try:
            process = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr)
            termination = 'running'
            try: exit_code = process.wait(timeout=timeout); termination = 'reaped'
            except subprocess.TimeoutExpired:
                # Host-only disposable process. Never restart after timeout.
                kill_attempted = True
                process.kill(); exit_code = process.wait(timeout=10); termination = 'terminated_after_timeout'
        except BaseException:
            termination = 'needs_process_reconciliation'
            if process is not None and not kill_attempted:
                kill_attempted = True
                try:
                    process.kill(); exit_code = process.wait(timeout=10); termination = 'terminated_after_interruption'
                except BaseException: pass
    if termination == 'reaped' and exit_code == 0:
        try:
            stdout_raw, _ = read_source(str(folder/'stdout.json'), limit=65536)
            stderr_raw, _ = read_source(str(folder/'stderr.log'), limit=65536)
            result = strict_json(stdout_raw)
            composed = request.get('schema') == 'dependency_child_invented_request_v1'
            collected = request.get('schema') == 'dependency_child_collection_request_v1'
            accepted = (('invented_collected_child_complete' if request['collection']['mode']=='invented'
                         else 'runtime_collected_child_complete') if collected else
                        'invented_child_producer_complete' if composed else 'authored_source_child_preflight_complete')
            require(not stderr_raw and result['status'] == accepted and
                    result['request_sha256'] == sha(raw) and result['source_sha256'] ==
                    {role: row['sha256'] for role, row in request['sources'].items()}, 'child_result_binding')
            expected_result = dict(schema='dependency_child_preflight_result_v1',
                status='authored_source_child_preflight_complete', request_sha256=sha(raw),
                source_sha256={role: row['sha256'] for role, row in request['sources'].items()},
                runtime_profile=request['expected_runtime'], audit_hook_acknowledged=True,
                audit_hook_retained_inert=True, exact_child_source_buffers_executed=True,
                parent_execution_authenticated=False, prior_review_proven=False,
                installed_dependency_bootstrap_performed=False, actual_dependency_observation_performed=False,
                operational_acceptance=False, execution_authorized=False, feature_supported=False,
                recovery_proven=False, device_write_gate_passed=False, camera_commands=[])
            if composed:
                # Independent parent read/contract recomputation of newly created
                # invented records. This parent import does not authenticate its
                # own executing source; no authority flag is promoted.
                from tools import dependency_invented as invented
                packet_raw, packet_receipt = read_source(request['composition']['packet']['path'], limit=4*1024**2)
                require(canonical(packet_receipt) == canonical(request['composition']['packet']), 'packet_binding')
                source_buffers = {}
                for role, row in request['sources'].items():
                    source_buffers[role], current = read_source(row['path'])
                    require(canonical(current) == canonical(row), 'source_binding')
                artifacts = invented.validate_saved(folder/'producer', strict_json(packet_raw),
                    request['composition']['fixed'], source_buffers, request['review_sha256'])
                expected_result = composition_result(request, artifacts)
            if collected:
                from tools import dependency_execution as execution
                c=request['collection'];packet_raw,current=read_source(c['packet']['path'],limit=4*1024**2)
                require(canonical(current)==canonical(c['packet']),'packet_binding')
                source_buffers={}
                for role,row in request['sources'].items():
                    source_buffers[role],current=read_source(row['path'])
                    require(canonical(current)==canonical(row),'source_binding')
                value=strict_json(packet_raw);invented_mode=c['mode']=='invented'
                if invented_mode:
                    from tools import dependency_invented as invented
                    data,_=invented.unpack(value,c['fixed'],source_buffers,request['review_sha256'],complete=True)
                else:data=execution.bind_runtime_packet(value,c['fixed'],source_buffers,request['review_sha256'])
                artifacts=execution.validate_saved_composition(folder/'collected',data,invented=invented_mode)
                expected_result=collection_result(request,artifacts)
            require(canonical(result) == canonical(expected_result), 'child_result_binding')
            status = accepted
        except BaseException:
            # Child completion is already known. Preserve its PID/exit record
            # even if parent reconciliation is interrupted; never replay it.
            result = None
    receipt = dict(schema='dependency_child_preflight_completion_v1', status=status,
        request_sha256=sha(raw), exit_code=exit_code, termination=termination,
        child_pid=process.pid if process is not None else None, result=result,
        automatic_retry=False, execution_authorized=False, feature_supported=False,
        recovery_proven=False, device_write_gate_passed=False, camera_commands=[])
    with (folder/'completion.json').open('xb') as out:
        out.write(canonical(receipt)); out.flush(); os.fsync(out.fileno())
    return receipt


def main():
    print(json.dumps(dict(status='needs_review', code='real_activation_pending', camera_commands=[])))
    return 2


if __name__ == '__main__': raise SystemExit(main())
