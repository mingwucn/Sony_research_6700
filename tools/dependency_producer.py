"""Prospective dependency-only producer; ordinary CLI always refuses.

The engine performs real source-hook, native-wrapper and durable-output steps.
Only invented operations are exposed for qualification. A separately reviewed
outer entry and disposable-child activation remain required for a real run.
No firmware, GDT, camera or arbitrary continuation API is provided.
"""
import hashlib
import importlib
import importlib.abc
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys

from tools import dependency_evidence as core


PUBLIC_PLAN_SHA256 = 'a914aca415d20a87a56440f36944f7ac6082ecbc36387b68694175a579bc43b5'
ALIASES = ('Cryptodome', 'Cryptodome.Cipher', 'Cryptodome.Cipher.AES',
    'Cryptodome.Cipher._mode_ecb', 'Cryptodome.Cipher._mode_cbc', 'Cryptodome.Random',
    'Cryptodome.Util', 'Cryptodome.Util._raw_api', 'Cryptodome.Util._cpu_features',
    'Cryptodome.Util._file_system', 'Cryptodome.Util.py3compat')
NATIVES = {'cpuid':'Cryptodome/Util/_cpuid_c.pyd','aes':'Cryptodome/Cipher/_raw_aes.pyd',
    'aesni':'Cryptodome/Cipher/_raw_aesni.pyd','ecb':'Cryptodome/Cipher/_raw_ecb.pyd',
    'cbc':'Cryptodome/Cipher/_raw_cbc.pyd'}
TRUSTED = ('ctypes', '_ctypes', 'ctypes.util', 'ctypes._endian', 'platform')
PROBE_EVENT = 'a6700.dependency.guard_probe'


def encoded(value): return core._canonical(value) + b'\n'
def sha(data): return hashlib.sha256(data).hexdigest()
def need(condition, code): core._need(condition, code)
def target(policy, row):
    return policy['roots'][row['root']]['path'].rstrip('/')+'/'+row['relative_path']
def stamp(value):
    return dict(zip(core.STAMP,(value.st_dev,value.st_ino,value.st_mode,value.st_nlink,
        value.st_size,value.st_mtime_ns,value.st_ctime_ns,getattr(value,'st_file_attributes',0))))


def directory_receipt(path):
    """Directory identities are actual stat/ancestor observations, not path labels."""
    rows=[]
    for item in reversed((Path(path), *Path(path).parents)):
        value=os.lstat(item)
        need(stat.S_ISDIR(value.st_mode) and not getattr(value,'st_file_attributes',0)&0x400,
             'directory_kind')
        rows.append(dict(path=str(item),device=value.st_dev,inode=value.st_ino,
            mode=value.st_mode,file_attributes=getattr(value,'st_file_attributes',0)))
    return dict(schema='dependency_directory_identity_v1',path=path,ancestors=rows)


def read_verified(path, expected=None, limit=8*1024**2):
    """Bounded ordinary descriptor read; cooperative filesystem, not a sandbox."""
    need(type(limit) is int and 0 < limit <= 8*1024**2, 'read_bound')
    parents=directory_receipt(str(Path(path).parent));before=os.lstat(path)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink==1 and
         not getattr(before,'st_file_attributes',0)&0x400 and before.st_size<=limit,'file_kind')
    fd=os.open(path,os.O_RDONLY|getattr(os,'O_BINARY',0)|getattr(os,'O_NOFOLLOW',0))
    try:
        opened=os.fstat(fd)
        need(stat.S_ISREG(opened.st_mode) and opened.st_nlink==1 and
             not getattr(opened,'st_file_attributes',0)&0x400, 'file_kind')
        need(all(stamp(before)[k]==stamp(opened)[k] for k in core.CROSS),'file_identity')
        chunks=[];total=0
        while True:
            data=os.read(fd,min(65536,limit+1-total))
            if not data: break
            total+=len(data);need(total<=limit,'read_bound');chunks.append(data)
        final=os.fstat(fd)
    finally:
        os.close(fd)
    after=os.lstat(path);raw=b''.join(chunks)
    need(stamp(before)==stamp(after) and stamp(opened)==stamp(final) and
         len(raw)==before.st_size and parents==directory_receipt(str(Path(path).parent)),'file_changed')
    receipt=dict(path=path,size=len(raw),sha256=sha(raw),opened_read_only=True,
        lstat_before=stamp(before),fstat_before=stamp(opened),fstat_after=stamp(final),lstat_after=stamp(after))
    core._receipt(receipt,path,sha(raw) if expected is None else expected['sha256'],
        len(raw) if expected is None else expected['size'],
        None if expected is None else expected['identity'])
    return raw,receipt


class Outputs:
    """Exclusive files, stepwise publication and sticky failure; no retry."""
    def __init__(self, folder):
        self.folder=Path(folder);self.journal=None;self.raw=None;self.failed=False;self.events=[]
    def reserve(self, expectation, binding):
        self.folder.mkdir(exist_ok=False)
        self.small('expectation.json',expectation);self.small('binding.json',binding)
        self.journal=(self.folder/'journal.jsonl').open('xb',buffering=0)
        self.raw=(self.folder/'raw.json').open('xb',buffering=0)
    def small(self, name, value):
        handle=(self.folder/name).open('xb',buffering=0)
        try:
            raw=encoded(value);need(len(raw)<=8*1024**2,'output_bound')
            need(handle.write(raw)==len(raw),'short_write');handle.flush();os.fsync(handle.fileno())
        finally: handle.close()
    def emit(self, event, data):
        need(not self.failed,'sticky_failure');self.failed=True
        row=dict(sequence=len(self.events)+1,event=event,data=json.loads(encoded(data)))
        raw=encoded(row);need(len(raw)<=32768 and len(self.events)<1024,'event_bound')
        need(self.journal.write(raw)==len(raw),'journal_write');self.journal.flush();os.fsync(self.journal.fileno())
        self.events.append(row);self.failed=False
    def publish(self, value, operation):
        raw=encoded(value);need(len(raw)<=4*1024**2,'output_bound')
        anchor=dict(raw_receipt_sha256=sha(raw),operation_id=operation)
        need(not self.failed and self.raw is not None,'sticky_failure')
        # On any uncertain operation no later marker or callback may occur.
        self.failed=True;need(self.raw.write(raw)==len(raw),'raw_write');self.failed=False
        self.emit('raw_written',anchor)
        self.failed=True;self.raw.flush();self.failed=False;self.emit('raw_flushed',anchor)
        self.failed=True;os.fsync(self.raw.fileno());self.failed=False;self.emit('raw_fsynced',anchor)
        self.failed=True;closing=self.raw;self.raw=None;need(closing.close() is None,'raw_close')
        self.failed=False;self.emit('raw_closed',anchor)
        self.verify_raw(raw);self.emit('raw_reverified',anchor)
        return raw,anchor
    def verify_raw(self, raw):
        need(not self.failed,'sticky_failure');self.failed=True
        observed,_=read_verified(str(self.folder/'raw.json'),limit=4*1024**2)
        need(observed==raw,'raw_readback');self.failed=False
    def close(self):
        failed=False
        for name in ('raw','journal'):
            handle=getattr(self,name);setattr(self,name,None)
            if handle is not None:
                try: need(handle.close() is None,'output_close')
                except BaseException: self.failed=True;failed=True
        need(not failed,'output_close')


class Guard:
    def __init__(self, policy, reader, emit):
        self.policy=policy;self.reader=reader;self.emit=emit;self.loads={};self.pending=None
        self.failed=False;self.active=True;self.bootstrap=True;self.finished=False;self.bootstrap_seen=set()
        self.probe_token=os.urandom(16).hex();self.probe_count=0
        self.paths={target(policy,row).casefold():name for name,row in policy['native_libraries'].items()}
    def audit(self, event, args):
        if not self.active: return
        try:
            if event==PROBE_EVENT:
                need(args==(self.probe_token,) and self.probe_count==0 and self.bootstrap,'audit_probe')
                self.probe_count+=1;return
            need(event not in ('subprocess.Popen','os.system','os.posix_spawn','os.spawn'),'process_forbidden')
            if event!='ctypes.dlopen':return
            if self.bootstrap and args in ((None,),('kernel32',)):
                need(args not in self.bootstrap_seen,'bootstrap_duplicate');self.bootstrap_seen.add(args);return
            need(not self.failed and not self.finished and self.pending is not None,'unexpected_audit')
            name,load=self.pending
            need(type(args) is tuple and len(args)==1 and type(args[0]) is str and
                 core._loader_path(args[0]).casefold()==target(self.policy,self.policy['native_libraries'][name]).casefold()
                 and load['audit'] is None,'unexpected_audit')
            load['audit']=dict(api='ctypes.dlopen',argument=args[0])
            self.emit('native_audit',dict(name=name,sha256=core._hash(load['audit'])))
        except BaseException:
            self.failed=True;raise
    def wrap(self, original):
        def call(path,*args,**kwargs):
            owns_pending=False
            try:
                need(not self.failed and not self.finished and self.pending is None,'native_closed')
                normalized=core._loader_path(path).casefold()
                need(normalized in self.paths and not args and
                     core._canonical(kwargs)==core._canonical(self.policy['loader_kwargs']),'native_arguments')
                name=self.paths[normalized];need(name not in self.loads,'native_duplicate')
                expected=self.policy['native_libraries'][name];absolute=target(self.policy,expected)
                before_bytes,before=self.reader(absolute,expected)
                load=dict(intent=dict(api='ctypes.CDLL',arguments=[path],keyword_arguments=kwargs,before=before),audit=None,after=None)
                self.loads[name]=load;self.pending=(name,load);owns_pending=True
                self.emit('native_intent',dict(name=name,sha256=core._hash(load['intent'])))
                answer=original(path,**kwargs)
                need(load['audit'] is not None and not self.failed,'missing_audit')
                after_bytes,load['after']=self.reader(absolute,expected)
                need(before_bytes==after_bytes and core._canonical(before)==core._canonical(load['after']),'native_changed')
                self.emit('native_complete',dict(name=name,sha256=core._hash(load['after'])))
                return answer
            except BaseException:
                self.failed=True;raise
            finally:
                if owns_pending:self.pending=None
        return call


class Sources(importlib.abc.MetaPathFinder,importlib.abc.Loader):
    def __init__(self, policy, buffers, reader, emit):
        self.policy=policy;self.buffers=buffers;self.reader=reader;self.emit=emit
        self.owned={};self.completed={};self.failed=False;self.trace=[]
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in ('cffi','_cffi_backend','pycparser'):
            # Unavailable optional-backend probes may fall through to ImportError.
            # A reachable fallback is a sticky refusal, never loaded.
            if importlib.machinery.PathFinder.find_spec(fullname,path) is not None:
                self.failed=True;raise core.EvidenceError('fallback_reachable')
            # Stop the complete meta-path traversal. Returning None would let a
            # later custom finder execute a fallback hidden from PathFinder.
            raise ModuleNotFoundError(name=fullname)
        if fullname=='Cryptodome' or fullname.startswith('Cryptodome.'):
            if fullname not in self.buffers:
                self.failed=True;raise core.EvidenceError('unexpected_source')
            row=self.policy['python_origins'][fullname]
            return importlib.util.spec_from_loader(fullname,self,
                origin=globals()['target'](self.policy,row),is_package=row['relative_path'].endswith('/__init__.py'))
        return None
    def create_module(self,spec): return None
    def exec_module(self,module):
        alias=module.__name__;self.owned[alias]=module
        try:
            need(alias not in self.completed,'source_duplicate')
            row=self.policy['python_origins'][alias];path=target(self.policy,row);raw=self.buffers[alias]
            before_bytes,before=self.reader(path,row);need(before_bytes==raw,'executing_buffer')
            module.__file__=path;module.__cached__=None
            package=row['relative_path'].endswith('/__init__.py')
            if package: module.__path__=[path.rsplit('/',1)[0]]
            self.trace.append(dict(alias=alias,stage='source_execute_intent',sha256=sha(raw)))
            exec(compile(raw,path,'exec'),module.__dict__)
            after_bytes,after=self.reader(path,row)
            need(before_bytes==after_bytes and core._canonical(before)==core._canonical(after),'source_changed')
            need(module.__file__==path and module.__loader__ is self and sys.modules.get(alias) is module
                 and (not package or module.__path__==[path.rsplit('/',1)[0]]),'source_ownership')
            self.completed[alias]=after;self.trace.append(dict(alias=alias,stage='source_execute_complete',sha256=sha(raw)))
            self.emit('python_import',dict(alias=alias,receipt_sha256=core._hash(after)))
        except BaseException:
            self.failed=True;raise


def run_vectors(AES, vectors):
    comparisons=0
    for vector in vectors:
        for generic in (False,True):
            kw={'use_aesni':False} if generic else {}
            if vector['iv_hex'] is not None:kw['iv']=bytes.fromhex(vector['iv_hex'])
            key=bytes.fromhex(vector['key_hex']);plain=bytes.fromhex(vector['plaintext_hex']);cipher=bytes.fromhex(vector['ciphertext_hex'])
            mode=AES.MODE_ECB if vector['mode']=='ECB' else AES.MODE_CBC
            encrypted=AES.new(key,mode,**kw).encrypt(plain)
            need(type(encrypted) is bytes and encrypted==cipher,'vector_mismatch')
            decrypted=AES.new(key,mode,**kw).decrypt(cipher)
            need(type(decrypted) is bytes and decrypted==plain,'vector_mismatch');comparisons+=2
    need(comparisons==24,'vector_count')


def bind_inputs(expectation, package, binding, config_json, cache_json, source_buffers):
    need(type(config_json) is str and type(cache_json) is str,'input_type')
    config_bytes=core._text_bytes(config_json);cache_bytes=core._text_bytes(cache_json)
    policy,package,binding=core._bounded_copy([expectation,package,binding])
    manifest,receipts=core._package(package);core._policy(policy,package,manifest,receipts)
    core._shape(binding,('schema','expectation_sha256','package_sha256','review_sha256'))
    need(binding['schema']=='prospective_dependency_binding_v1' and
         binding['expectation_sha256']==core._hash(policy) and binding['package_sha256']==core._hash(package),'prior_binding')
    core._digest(binding['review_sha256'])
    need(sha(config_bytes)==policy['config_sha256'] and sha(cache_bytes)==policy['cache_sha256'],'input_hash')
    need(type(source_buffers) is dict and set(source_buffers)==set(policy['source_sha256']),'source_roster')
    total_source=0
    for name,raw in source_buffers.items():
        need(type(raw) is bytes and 0<len(raw)<=1024**2 and sha(raw)==policy['source_sha256'][name],'source_hash')
        total_source+=len(raw);need(total_source<=4*1024**2,'source_bound')
    config=core._bounded_copy(core._json_text(config_json));core._shape(config,('schema','operation_id','vectors'))
    need(config['schema']=='prospective_dependency_config_v1' and config['operation_id']==policy['operation_id']
         and core._hash(config['vectors'])==policy['vector_plan_sha256']==PUBLIC_PLAN_SHA256,'public_plan')
    cache=core._json_text(cache_json);core._shape(cache,('schema','sources'))
    need(cache['schema']=='prospective_dependency_source_cache_v1','cache_schema')
    core._shape(cache['sources'],ALIASES);core._shape(policy['python_origins'],ALIASES)
    core._shape(policy['native_libraries'],NATIVES);core._shape(policy['trusted_origins'],TRUSTED)
    buffers={};total=0
    for alias,text in cache['sources'].items():
        need(type(text) is str and len(text)<=1024**2,'cache_bound');raw=text.encode('utf-8');total+=len(raw)
        row=policy['python_origins'][alias]
        package_alias=alias in ('Cryptodome','Cryptodome.Cipher','Cryptodome.Random','Cryptodome.Util')
        need(row['relative_path']==alias.replace('.','/')+('/__init__.py' if package_alias else '.py'),
             'python_profile')
        need(len(raw)==row['size'] and sha(raw)==row['sha256'] and total<=4*1024**2,'cache_hash');buffers[alias]=raw
    for alias,path in NATIVES.items():need(policy['native_libraries'][alias]['relative_path']==path,'native_profile')
    return policy,package,binding,config,buffers


class RuntimeOps:
    """Concrete future observer. Construction does not execute dependencies."""
    def reader(self,path,row): return read_verified(path,row)
    def root(self,path): return directory_receipt(path)
    def startup(self):
        need(os.name=='nt' and sys.implementation.name=='cpython','runtime_platform')
        return dict(isolated=sys.flags.isolated==1,no_site=sys.flags.no_site==1,
            no_user_site=sys.flags.no_user_site==1,no_bytecode=sys.dont_write_bytecode,
            preloaded_package_aliases=[n for n in sys.modules if n=='Cryptodome' or n.startswith('Cryptodome.')],
            bootstrap_boundary=['interpreter','stdlib','_ctypes','os_loader'])
    def audit_install(self,hook):sys.addaudithook(hook)
    def audit_probe(self,token):sys.audit(PROBE_EVENT,token)
    def bootstrap(self):return {name:importlib.import_module(name) for name in TRUSTED}
    def callback(self,AES,vectors):run_vectors(AES,vectors)


def _produce(*,expectation,package,binding,config_json,cache_json,source_buffers,folder,ops,invented):
    """Internal engine; future real activation needs a separately reviewed outer entry."""
    policy,package,binding,config,buffers=bind_inputs(expectation,package,binding,config_json,cache_json,source_buffers)
    old_meta=list(sys.meta_path);old_path=list(sys.path)
    need(not any(n=='Cryptodome' or n.startswith('Cryptodome.') or n.split('.')[0] in ('cffi','_cffi_backend','pycparser') for n in sys.modules),'preloaded_alias')
    startup=core._bounded_copy(ops.startup())
    core._shape(startup,('isolated','no_site','no_user_site','no_bytecode','preloaded_package_aliases','bootstrap_boundary'))
    need(all(startup[k] is True for k in ('isolated','no_site','no_user_site','no_bytecode')) and
         startup['preloaded_package_aliases']==[] and startup['bootstrap_boundary']==policy['bootstrap_boundary'],'startup')
    roots={name:ops.root(row['path']) for name,row in policy['roots'].items()}
    need({k:core._hash(v) for k,v in roots.items()}=={k:v['identity_sha256'] for k,v in policy['roots'].items()},'root_identity')
    out=Outputs(folder);guard=Guard(policy,ops.reader,out.emit);finder=Sources(policy,buffers,ops.reader,out.emit)
    backend=None;original=None;wrapped=None;primary=None;observation=None;raw=None
    try:
        out.reserve(policy,binding);out.emit('expectation_bound',dict(sha256=core._hash(policy)))
        trusted={name:ops.reader(target(policy,row),row)[1] for name,row in policy['trusted_origins'].items()}
        ops.audit_install(guard.audit);ops.audit_probe(guard.probe_token)
        need(guard.probe_count==1 and not guard.failed,'audit_not_acknowledged')
        out.small('audit-acknowledgement.json',dict(schema='dependency_audit_acknowledgement_v1',
            operation_id=policy['operation_id'],probe_event=PROBE_EVENT,probe_token=guard.probe_token,
            acknowledged=True,test_injection_used=invented))
        modules=ops.bootstrap();core._shape(modules,TRUSTED)
        for name,row in policy['trusted_origins'].items():
            need(core._loader_path(modules[name].__file__)==target(policy,row),'trusted_origin')
            need(core._canonical(ops.reader(target(policy,row),row)[1])==core._canonical(trusted[name]),'trusted_changed')
        backend=modules['ctypes'];original=backend.CDLL;wrapped=guard.wrap(original)
        out.emit('bootstrap_complete',dict(sha256=core._hash(startup)))
        backend.CDLL=wrapped;guard.bootstrap=False;sys.meta_path.insert(0,finder)
        out.emit('guard_installed',dict(backend='ctypes'))
        raw_api=importlib.import_module('Cryptodome.Util._raw_api')
        need(raw_api.backend=='ctypes' and raw_api.CDLL is wrapped,'backend')
        AES=importlib.import_module('Cryptodome.Cipher.AES');run_vectors(AES,config['vectors'])
        need(not guard.failed and not finder.failed and guard.pending is None and
             set(finder.completed)==set(policy['python_origins']) and set(guard.loads)==set(policy['native_libraries']),'incomplete_observation')
        vectors=dict(plan_sha256=policy['vector_plan_sha256'],cases=12,comparisons=24,passed=True)
        out.emit('vectors_complete',vectors);guard.finished=True
        out.emit('guard_finished',dict(native_names=sorted(guard.loads)))
        transcript=dict(schema='dependency_guard_transcript_v1',operation_id=policy['operation_id'],
            expectation_sha256=core._hash(policy),startup=startup,python_origins=finder.completed,
            trusted_origins=trusted,native_loads=guard.loads,vectors=vectors,events=list(out.events))
        raw,anchor=out.publish(transcript,policy['operation_id']);out.verify_raw(raw)
        out.emit('callback_claimed',anchor);ops.callback(AES,config['vectors'])
        need(not guard.failed and not finder.failed and guard.pending is None,'sticky_guard_failure')
        need(sys.meta_path==[finder]+old_meta and sys.path==old_path and backend.CDLL is wrapped,'runtime_changed')
        for alias,module in finder.owned.items():need(sys.modules.get(alias) is module,'source_ownership')
        need(roots=={name:ops.root(row['path']) for name,row in policy['roots'].items()},'root_changed')
        out.emit('callback_returned',dict(success=True))
        observation=dict(schema='dependency_observation_v1',evidence_mode='invented' if invented else 'saved_records',
            operation_id=policy['operation_id'],expectation_sha256=core._hash(policy),
            source_sha256=policy['source_sha256'],config_sha256=policy['config_sha256'],cache_sha256=policy['cache_sha256'],
            root_identities={k:core._hash(v) for k,v in roots.items()},startup=startup,
            python_origins=finder.completed,trusted_origins=trusted,native_loads=guard.loads,vectors=vectors,
            raw_receipt_sha256=anchor['raw_receipt_sha256'],journal_sha256='',events=[],transitive_os_dependencies_attested=False)
    except BaseException as error:primary=error
    finally:
        cleanup=True;guard.finished=True;guard.active=False
        def release(action):
            nonlocal cleanup,primary
            try:action()
            except BaseException as error:
                cleanup=False
                if primary is None:primary=error
        def release_wrapper():
            if backend is not None and wrapped is not None:
                need(getattr(backend,'CDLL',None) is wrapped,'cleanup_ownership')
                backend.CDLL=original
        def release_finder():
            for index,item in enumerate(sys.meta_path):
                if item is finder:
                    del sys.meta_path[index];break
            need(len(sys.meta_path)==len(old_meta) and
                 all(a is b for a,b in zip(sys.meta_path,old_meta)) and sys.path==old_path,'cleanup_ownership')
        def release_alias(alias,module):
            if sys.modules.get(alias) is module:sys.modules.pop(alias)
            else:need(alias not in sys.modules,'cleanup_ownership')
        release(release_wrapper);release(release_finder)
        for alias,module in tuple(finder.owned.items()):
            release(lambda:release_alias(alias,module))
        release(lambda:need(not any(n=='Cryptodome' or n.startswith('Cryptodome.') for n in tuple(sys.modules)),
                            'cleanup_ownership'))
        try:
            need(cleanup,'cleanup_ownership')
            if primary is None:
                out.emit('cleanup_complete',dict(aliases_released=True,finder_removed=True,native_wrapper_removed=True))
        except BaseException as error:
            if primary is None:primary=error
        try:out.close()
        except BaseException as error:
            if primary is None:primary=error
    if primary is not None:raise primary
    journal,_=read_verified(str(Path(folder)/'journal.jsonl'),limit=4*1024**2)
    observation['journal_sha256']=sha(journal);observation['events']=list(out.events)
    consistency=core.validate_dependency_records(expectation=policy,observation=observation,package=package,
        raw_receipt_json=raw.decode('utf-8'),journal_jsonl=journal.decode('utf-8'))
    result=dict(schema='prospective_dependency_producer_result_v1',status='produced_consistent_dependency_records',
        observation=observation,consistency=consistency,source_execution_trace=finder.trace,
        test_injection_used=invented,audit_hook_retained_inert=True,
        audit_hook_acknowledged=True,audit_acknowledgement_is_invented=invented,
        source_buffers_are_caller_supplied=True,executing_producer_authenticated=False,
        prior_binding_is_caller_declaration=True,operational_acceptance=False,
        execution_authorized=False,feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])
    out.small('result.json',result)
    return result


def produce_invented(*,ops,**inputs):
    """Qualification seam only: outputs always identify test injection."""
    need(not isinstance(ops,RuntimeOps),'real_activation_pending')
    return _produce(ops=ops,invented=True,**inputs)


def main():
    print(json.dumps(dict(status='needs_review',code='real_activation_pending',camera_commands=[])))
    return 2


if __name__=='__main__':raise SystemExit(main())
