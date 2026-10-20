"""Authored host preparation and parent reconciliation; invented inputs only.

The ordinary CLI and operational runtime refuse. Trusted interpreter/stdlib and
bootstrap are assumptions, not attested or sandboxed by this module. Metadata
owners and bootstrap aliases live until explicit close; observer callbacks remain
caller-owned and must be released before closing a successful preparation.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import base64, builtins, hashlib, json, types
import importlib,importlib.util,sys
from pathlib import Path
from types import SimpleNamespace,ModuleType
def need(condition, code="outer_entry_v2_refused"):
    if not condition:
        raise ValueError(code)


def cached_module(alias, raw, path):
    need(alias not in sys.modules)
    module=ModuleType(alias);module.__file__=str(path);module.__package__=''
    # Retained bootstrap modules use their checked AuthoredSources importer.
    # Do not accidentally inherit a detached caller's tools-only importer when
    # exec inserts builtins into a fresh namespace.
    module.__builtins__=dict(vars(builtins))
    module.__spec__=importlib.machinery.ModuleSpec(alias,loader=None,origin=str(path))
    sys.modules[alias]=module
    try:exec(compile(raw,str(path),'exec'),module.__dict__)
    except BaseException:
        if sys.modules.get(alias) is module:del sys.modules[alias]
        raise
    return module


def refresh_sources(validated, io):
    """Fresh in this process; saved receipts never replace these reads."""
    rows=validated['inputs']['source_cache']['sources'];buffers={};receipts={}
    for key,row in rows.items():
        if not (key.startswith('role:') or key in ('bootstrap:activation_binding','bootstrap:io_entry','integration:prospective_child')): continue
        raw,proof=io.read(row['path'],expected_sha256=row['sha256'],expected_bytes=row['bytes'])
        need(raw==validated['source_buffers'][key]);buffers[key]=raw;receipts[key]=proof
    return buffers,{'schema':'gdt_outer_fresh_sources_v3',
                    'operation_id':validated['candidate']['operation_id'],
                    'seal_sha256':validated['seal_sha256'],'receipts':receipts,'camera_commands':[]}


def _prepare_modules(validated, buffers, gate, io, modules):
    """Concrete production bindings; not invoked on saved inputs by this package."""
    c=validated['candidate'];p=validated['inputs'];root=Path(c['repository_root'])
    # Legacy runtime_entry/gdt_wiring remain historical metadata, never executed.
    for name,key in [('binding','bootstrap:activation_binding'),('control','bootstrap:io_entry'),
                     ('factory','integration:prospective_child')]:
        row=p['source_cache']['sources'][key]
        need(gate.sha(buffers[key])==row['sha256'])
        modules[name]=cached_module('_successor_'+name,buffers[key],row['path'])
    adapter=SimpleNamespace(require=gate.require,relative=gate.relative,sha=gate.sha,read_ordinary=io.read_ordinary)
    roles=p['role_authority']['roles']
    qualified=validated['effective_qualified_sources']
    role_buffers={name:buffers['role:'+name] for name in roles}
    binding=modules['binding']
    plan=binding.prepare_bindings(binding_input=p['prerequisites']['binding_input'],
        qualified_roles=roles,qualified_sources=qualified,authored_sources=role_buffers,
        preexisting_aliases=tuple(sys.modules))
    need(plan==p['binding_plan']
         and plan['load_order']==p['binding_schema']['load_order']
         and plan['protected_order']==p['binding_schema']['protected_order'])
    # Preserve old false flags/blockers; only its source graph is reused.
    need(plan['execution_authorized'] is False and plan['actual_binding_ready'] is False)
    loader=modules['factory'].AuthoredSources(adapter)
    for name,row in roles.items():
        loader.add(p['binding_schema']['aliases'][name],root/row['path'],role_buffers[name])
    freeze_owned(loader,p['basis'])
    factory_arguments={'validated':{'qualified_roles':roles,'qualified_sources':qualified,
                                  'binding_input':p['prerequisites']['binding_input'],
                                  'prerequisite_plan':p['prerequisites']},
                       'source_plan':plan,'source_buffers':role_buffers,
                       'aliases':p['binding_schema']['aliases'],'gate':adapter,'control':modules['control']}
    callbacks=modules['factory'].ScopedCallbacks(**factory_arguments)
    return modules,None,callbacks


def freeze_owned(loader,basis):
    """One cleanup attempt even if mounting stores then raises."""
    primary=None
    try:
        sys.meta_path.insert(0,loader)
        importlib.import_module('gdt_preflight').freeze_basis(**basis)
    except BaseException as error:
        primary=error
    finally:
        try:loader.close()
        except BaseException as cleanup:
            if primary is not None:raise primary from cleanup
            raise
    if primary is not None:raise primary


def make_context(validated):
    c=validated['candidate'];p=validated['inputs'];root=Path(c['repository_root']);here=root/c['session']
    ordinary={row['path']:row['sha256'] for row in c['inputs'].values()}
    for row in p['source_cache']['sources'].values():
        path=Path(row['path'])
        if path.is_relative_to(root):ordinary[path.relative_to(root).as_posix()]=row['sha256']
    for role,name in [('candidate','activation-candidate.json'),('review','activation-review.json'),('decision','act-decision.json')]:
        # Exact linked bytes are rehashed in ordinary context checks; seal binds them.
        field=role+'_sha256'
        # Hash values were already reconciled by validate_bundle; derive from the
        # trusted seal data freshly read under the inherited context checker.
        ordinary[c['session']+'/'+name]=validated['document_sha256'][role]
    return {'schema':'gdt_io_context_v1','session_dir':here,'repository_root':root,
            'operation_id':c['operation_id'],'execution_seal_sha256':validated['seal_sha256'],
            'basis':p['basis'],'source_manifest':p['source_manifest'],
            'implementation_sha256':{name+'.py':row['sha256'] for name,row in c['bootstrap'].items()},
            'ordinary_sha256':ordinary,'child_argv':validated['child_argv'],
            'deadline_seconds':300,'limits':{'poll_seconds':0.05}}


def run_invented(*,helpers,runtime_wiring,inputs,ops,folder,control,context,records,
                 adapter_owner,adapter_request,adapter_request_sha256,adapter_buffers,
                 make_callbacks_after_receipt,release_callbacks_after_controller,monotonic,identity):
    # Exercise actual startup and runtime packet grammar, but retain invented
    # observation/cipher mode throughout the controller. No runtime observer.
    runtime_wiring._startup()
    helpers.intact()
    package=helpers.package
    policy=inputs['expectation']; core=package.dependency_evidence
    fixed=dict(expectation_sha256=core._hash(policy),package_sha256=core._hash(inputs['package']),
               root_sha256={k:r['identity_sha256'] for k,r in policy['roots'].items()})
    packet=dict(schema='runtime_dependency_packet_v1',inputs={k:v for k,v in inputs.items() if k!='source_buffers'})
    bound=package.dependency_execution.bind_runtime_packet(packet,fixed,inputs['source_buffers'],inputs['binding']['review_sha256'])
    need(policy['operation_id']==context['operation_id']==identity['operation_id'])
    need(str(folder)==adapter_request['folder'])
    answer=adapter_owner.call('run_invented',request=adapter_request,
        expected_request_sha256=adapter_request_sha256,checked_sources=adapter_buffers,
        helpers=helpers,dependency_source_buffers=bound['source_buffers'],ops=ops,control=control,
        context=context,records=records,make_callbacks_after_receipt=make_callbacks_after_receipt,
        release_callbacks_after_controller=release_callbacks_after_controller,monotonic=monotonic,identity=identity)
    helpers.intact()
    return answer


def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def sha(v):return hashlib.sha256(v).hexdigest()
def _module(raw, path, importer=None):
    result=types.ModuleType('_checked_host_metadata')
    result.__file__=str(path)
    if importer is not None:
        result.__builtins__=dict(vars(builtins),__import__=importer)
    exec(compile(raw,str(path),'exec',dont_inherit=True,optimize=0),vars(result))
    return result

def unwire(value):
 count=0
 def visit(row,depth):
  nonlocal count
  count+=1;need(count<=200000 and depth<=100,'metadata_wire_bound')
  need(type(row) is list and len(row)==2 and type(row[0]) is str,'metadata_wire_shape')
  kind,payload=row
  if kind=='bytes':
   need(type(payload) is str and len(payload)<=3*1024**2,'metadata_wire_bytes')
   raw=base64.b64decode(payload,validate=True);need(len(raw)<=2*1024**2,'metadata_wire_bytes');return raw
  if kind=='scalar':
   need(payload is None or type(payload) in (str,int,bool,float),'metadata_wire_scalar');return payload
  need(type(payload) is list,'metadata_wire_sequence')
  if kind=='list':return [visit(v,depth+1) for v in payload]
  need(kind=='dict','metadata_wire_kind');result={}
  for pair in payload:
   need(type(pair) is list and len(pair)==2 and type(pair[0]) is str and pair[0] not in result,'metadata_wire_key')
   result[pair[0]]=visit(pair[1],depth+1)
  return result
 return visit(value,0)



class HostPreparation:
    """One preparation attempt; independent once-only metadata cleanup."""
    def __init__(self, *, request, packet, buffers, receipts, contract, documents,
                 validated, fresh, gate, io, adapter_owner, adapter_buffers):
        self.request=request; self.packet=packet; self.buffers=buffers
        self.receipts=receipts; self.contract=contract; self.documents=documents
        self.validated=validated; self.fresh=fresh; self.gate=gate; self.io=io
        self.adapter_owner=adapter_owner; self.adapter_buffers=adapter_buffers
        self.metadata_owner=None; self.comparison_owner=None
        self.bootstrap_modules={}
        self.metadata_attempts=0; self.preparation_calls=0; self.metadata_hash=None
        self.close_attempts=dict(comparison=0,current=0)
        self.started=False; self.closed=False

    def _track(self, owner, name):
        original=owner.close
        def close():
            self.close_attempts[name]+=1
            return original()
        owner.close=close
        return owner

    def _load_current(self, loader, sources):
        self.metadata_owner=self._track(loader.DetachedMetadata(
            buffers=sources,expected_hashes={n:sha(raw) for n,raw in sources.items()},
            purpose='current'),'current')
        self.metadata_owner.load()

    def _validate_current(self, **kwargs):
        return self.metadata_owner.call(**kwargs)

    def snapshot(self):
        return dict(metadata_preflight_sha256=self.metadata_hash,
            metadata_attempts=self.metadata_attempts,preparation_calls=self.preparation_calls,
            comparison_closed=self.comparison_owner is None or self.comparison_owner.closed,
            metadata_closed=self.metadata_owner is None or self.metadata_owner.closed,
            metadata_close_attempts=dict(self.close_attempts))

    def prepare(self):
        need(not self.started and not self.closed,'host_preparation_reentry')
        self.started=True
        try:
            return self._prepare()
        except BaseException as primary:
            try:self.close()
            except BaseException as cleanup:raise primary from cleanup
            raise

    def close(self):
        if self.closed:return False
        self.closed=True
        primary=None
        for owner in (self.metadata_owner,self.comparison_owner):
            if owner is not None and not owner.closed:
                try:owner.close()
                except BaseException as error:
                    if primary is None:primary=error
        for module in self.bootstrap_modules.values():
            alias=module.__name__
            try:
                if sys.modules.get(alias) is module:
                    del sys.modules[alias]
                else:
                    need(alias not in sys.modules,'host_bootstrap_alias_ownership')
            except BaseException as error:
                if primary is None:primary=error
        if primary is not None:raise primary
        return True

    def _prepare(self):
        request=self.request;packet=self.packet;buffers=self.buffers
        receipts=self.receipts;contract=self.contract;docs=self.documents
        v=self.validated;io=self.io;adapter_buffers=self.adapter_buffers
        adapter_owner=self.adapter_owner
        need(packet['scope']=='invented_only_no_operational_authority','invented_only')
        need(v['inputs']['source_manifest']['sha256']=='b3ff4fd1ebb621f4c2be4b104e11b395ea315f1fbf580dd6b403bb2a091de541','invented_stream_only')
        literal=("key_aes="+repr(bytes(range(16)))+"\nkey_cxd90057_k8="+repr(bytes(range(32)))+'\n'+''.join('unused_'+str(i)+"=b'invented'\n" for i in range(13))).encode()
        need(v['inputs']['prerequisites']['constants_sha256']==sha(literal),'invented_constants_only')
        self.metadata_attempts+=1
        audit=_module(buffers['metadata_audit'],receipts['metadata_audit']['path'])
        audit_package=types.SimpleNamespace(source_import_audit=audit)
        def import_loader(name,globals=None,locals=None,fromlist=(),level=0):
         need(level==0,'metadata_loader_relative_import')
         if name=='tools':
          need(tuple(fromlist)==('source_import_audit',),'metadata_loader_import');return audit_package
         need(name in ('builtins','hashlib','json','math','sys','types'),'metadata_loader_stdlib')
         return builtins.__import__(name,globals,locals,fromlist,level)
        metadata_loader=_module(buffers['metadata_loader'],receipts['metadata_loader']['path'],import_loader)
        mp=packet['metadata']
        need(mp['shared_sources']==contract.METADATA_SHARED,'metadata_shared_sources')
        need(sha(canonical(mp['arguments']))==mp['arguments_sha256'],'metadata_argument_binding')
        arguments=unwire(mp['arguments'])
        need(arguments['checked_sources']==adapter_buffers,'metadata_prepared_source_buffers')
        comparison_sources={n:buffers[k] for n,k in contract.METADATA_SHARED.items()}
        comparison_sources.update({n:buffers['metadata.'+n] for n in contract.METADATA_EXTRA})
        self.comparison_owner=self._track(metadata_loader.DetachedMetadata(buffers=comparison_sources,expected_hashes={n:sha(raw) for n,raw in comparison_sources.items()}),'comparison')
        self.comparison_owner.load()
        current_sources={n:buffers['current.'+n] for n in contract.CURRENT}
        self._load_current(metadata_loader,current_sources)
        metadata_result=self._validate_current(outer_documents=docs,expected_outer_receipts=mp['expected_outer_receipts'],validated=v,
            prepared_request_bytes=base64.b64decode(mp['prepared_request_base64'],validate=True),prepared_request_sha256=packet['adapter_request_sha256'],
            prepared_repository_root=packet['adapter_repository_root'],arguments=arguments,metadata_owner=self.comparison_owner,adapter_owner=adapter_owner)
        io.write_new(Path(request['folder'])/'metadata-preflight.json',metadata_result)
        self.metadata_hash=sha(canonical(metadata_result))
        self.preparation_calls+=1
        return _prepare_modules(v,self.fresh,self.gate,io,self.bootstrap_modules)


def strict_json(raw):
    need(type(raw) is bytes and len(raw)<=2*1024**2,'metadata_saved_bound')
    def pairs(rows):
        result={}
        for key,value in rows:
            need(key not in result,'metadata_duplicate_key')
            result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=pairs)


def verify_saved_preflight(*,raw,expected_sha256,request,packet,contract,prepared_repository_root):
    """Compare bounded saved metadata against original parent-held records."""
    from pathlib import PureWindowsPath
    need(sha(raw)==expected_sha256,'metadata_saved_result_hash')
    checked=strict_json(raw);mr=checked['metadata_result'];mp=packet['metadata']
    need(set(checked)=={'schema','metadata_result','checked_public_buffer_execution','public_source_count','source_hashes',
        'interpreter_startup_verified','stdlib_origins_verified','validator_execution_owned','actual_inputs_accessed',
        'execution_authorized','feature_supported','recovery_proven','device_write_gate_passed','camera_commands'},'metadata_saved_wrapper_shape')
    need(type(mr) is dict and set(mr)=={'schema','operation_id','prepared_request_bytes_sha256','outer_original_sha256',
        'current_ordinary_sha256','source_frames','comparison_context_seal_sha256','checked_current_roles','current_source_roles',
        'unique_source_paths','derived_closure_is_file','source_reads_observed','source_freshness_verified','rights_established',
        'actual_inputs_accessed','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed','camera_commands'},
        'metadata_saved_inner_shape')
    need(checked['schema']=='invented_checked_public_metadata_result_v1' and
        checked['checked_public_buffer_execution'] is True and type(checked['public_source_count']) is int and
        checked['public_source_count']==3,'metadata_saved_wrapper')
    need(mr['comparison_context_seal_sha256']==mp['comparison_context_seal_sha256'],'metadata_saved_comparison_seal')
    need(checked['source_hashes']=={n:request['sources']['current.'+n]['sha256'] for n in contract.CURRENT},'metadata_saved_sources')
    need(mr['schema']=='invented_outer_metadata_binding_v1' and mr['operation_id']==request['operation_id'] and
        mr['prepared_request_bytes_sha256']==packet['adapter_request_sha256'],'metadata_saved_request')
    need(mr['outer_original_sha256']=={n:row['sha256'] for n,row in mp['expected_outer_receipts'].items()} and
        mr['current_ordinary_sha256']==mp['current_ordinary_sha256'],'metadata_saved_originals')
    candidate=strict_json(base64.b64decode(packet['documents']['candidate'],validate=True))
    need(mr['source_frames']==dict(comparison_root=PureWindowsPath(candidate['repository_root']).as_posix(),
        prepared_root=Path(prepared_repository_root).as_posix()),'metadata_saved_frames')
    need(mr['checked_current_roles']==sorted(mp['current_ordinary_sha256']) and
        type(mr['current_source_roles']) is int and mr['current_source_roles']==46 and
        type(mr['unique_source_paths']) is int and mr['unique_source_paths']==41,'metadata_saved_roster')
    need(mr['camera_commands']==[] and checked['camera_commands']==[] and
        all(mr[n] is False for n in ('derived_closure_is_file','source_reads_observed','source_freshness_verified',
            'rights_established','actual_inputs_accessed','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed')) and
        all(checked[n] is False for n in ('interpreter_startup_verified','stdlib_origins_verified','validator_execution_owned',
            'actual_inputs_accessed','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed')),'metadata_saved_authority')
    return True


def verify_child_completion(*, verifier, folder, inputs, operation_id, stdout,
                            stdout_sha256, dependency_sha256, bridge_sha256,
                            adapter_owner,adapter_request,adapter_request_sha256,adapter_buffers,process):
    if str(folder)!=adapter_request['folder'] or operation_id!=adapter_request['operation_id']:
        raise ValueError('adapter_parent_binding')
    return adapter_owner.call('reconcile_invented',request=adapter_request,
        expected_request_sha256=adapter_request_sha256,checked_sources=adapter_buffers,
        helpers=verifier,inputs=inputs,process=process,stdout=stdout,stdout_sha256=stdout_sha256,
        dependency_sha256=dependency_sha256,bridge_sha256=bridge_sha256)


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
