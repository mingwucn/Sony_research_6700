"""Invented clean outer child; no runtime/protected-input entry exists."""
if __name__=='__main__':
    raise SystemExit(2)

import builtins,base64,hashlib,json,os,pathlib,sys,time,types

def need(ok,code):
 if not ok:raise ValueError(code)
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def sha(v):return hashlib.sha256(v).hexdigest()
def module(alias,raw,path,importer=None):
 need(alias not in sys.modules,'outer_alias')
 m=types.ModuleType(alias);m.__file__=path;sys.modules[alias]=m
 if importer is not None:m.__builtins__=dict(vars(builtins),__import__=importer)
 try:exec(compile(raw,path,'exec',dont_inherit=True,optimize=0),m.__dict__)
 except BaseException:
  if sys.modules.get(alias) is m:del sys.modules[alias]
  raise
 return m

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

def child(request,packet,buffers,receipts):
 need(packet['scope']=='invented_only_no_operational_authority','invented_only')
 need(not any(n=='tools' or n.startswith('tools.') or n.split('.')[0] in ('ctypes','_ctypes','Crypto','Cryptodome','cffi','_cffi_backend') for n in sys.modules),'unclean_start')
 if packet['mode']=='slow_child':time.sleep(30)
 if packet['mode']=='log_overflow':
  sys.stdout.buffer.write(b'x'*(2097152+1));sys.stdout.buffer.flush();time.sleep(30)
 contract=module('_successor_contract',buffers['outer_contract'],receipts['outer_contract']['path'])
 contract.validate_request(request)
 ns=module('_outer_neutral_source',buffers['namespace'],receipts['namespace']['path'])
 entry=module('_outer_checked_entry',buffers['outer_entry'],receipts['outer_entry']['path'])
 gate=module('_outer_checked_gate',buffers['outer_gate'],receipts['outer_gate']['path'])
 io=module('_outer_checked_io',buffers['ordinary_io'],receipts['ordinary_io']['path'])
 docs={k:base64.b64decode(v,validate=True) for k,v in packet['documents'].items() if k!='inputs'}
 docs['inputs']={k:base64.b64decode(v,validate=True) for k,v in packet['documents']['inputs'].items()}
 v=gate.validate_bundle(docs,expected_seal_sha256=packet['seal_sha256'],reference_pins=packet['reference_pins'])
 need(v['candidate']['operation_id']==request['operation_id'],'operation')
 need(v['inputs']['source_manifest']['sha256']=='b3ff4fd1ebb621f4c2be4b104e11b395ea315f1fbf580dd6b403bb2a091de541','invented_stream_only')
 literal=("key_aes="+repr(bytes(range(16)))+"\nkey_cxd90057_k8="+repr(bytes(range(32)))+'\n'+''.join('unused_'+str(i)+"=b'invented'\n" for i in range(13))).encode()
 need(v['inputs']['prerequisites']['constants_sha256']==sha(literal),'invented_constants_only')
 for key,row in v['inputs']['source_cache']['sources'].items():
  if not (key.startswith('role:') or key in ('bootstrap:activation_binding','bootstrap:io_entry','integration:prospective_child')):continue
  need(buffers['bound.'+key]==v['source_buffers'][key] and receipts['bound.'+key]['path']==row['path'],'bound_source')
 # Source planning occurs before any tools/crypto/native alias exists.
 fresh,_=entry.refresh_sources(v,io)
 need(all(fresh[k]==buffers['bound.'+k] for k in fresh),'fresh_sources')
 callbacks=owner=records=ops=adapter_owner=preparation=None;owned_helpers={};installed=set()
 record_closes=[];cipher_calls=[];opens=[];closes=[];releases=[];factory_calls=[]
 primary=None;answer=None
 try:
  adapter_loader=module('_outer_adapter_loader',buffers['adapter_loader'],receipts['adapter_loader']['path'])
  adapter_sources={n:buffers[k] for n,k in adapter_loader.BUFFER_KEYS.items()}
  adapter_owner=adapter_loader.AdapterSources(buffers=adapter_sources,hashes={n:sha(raw) for n,raw in adapter_sources.items()}).load()
  adapter_rows,adapter_buffers=adapter_owner.project(process_sources=receipts,process_buffers=buffers,repository_root=packet['adapter_repository_root'])
  need(adapter_rows==packet['adapter_request']['sources'],'adapter_projection')
  original_load=entry.HostPreparation._load_current
  original_validate=entry.HostPreparation._validate_current
  def load_current(self,loader,sources):
   real_exec=loader.__builtins__['exec']
   def interrupt_exec(code,*args,**kwargs):
    if self.metadata_owner is not None and code is self.metadata_owner.compiled[self.metadata_owner.entry]:
     raise KeyboardInterrupt('invented current load interrupt')
    return real_exec(code,*args,**kwargs)
   try:
    if packet['mode']=='metadata_load_interrupt':loader.__builtins__['exec']=interrupt_exec
    return original_load(self,loader,sources)
   finally:loader.__builtins__['exec']=real_exec
  def validate_current(self,**kwargs):
   if packet['mode']=='metadata_interrupt':raise KeyboardInterrupt('invented metadata interrupt')
   if packet['mode']=='metadata_current_mutation':
    self.metadata_owner.modules['dependency_outer_metadata'].validate_invented_outer.__code__=(lambda **kw:{}).__code__
   if packet['mode']=='metadata_compare_source':self.comparison_owner.buffers['dependency_evidence']+=b'\n'
   return original_validate(self,**kwargs)
  entry.HostPreparation._load_current=load_current
  entry.HostPreparation._validate_current=validate_current
  preparation=entry.HostPreparation(request=request,packet=packet,buffers=buffers,receipts=receipts,
      contract=contract,documents=docs,validated=v,fresh=fresh,gate=gate,io=io,
      adapter_owner=adapter_owner,adapter_buffers=adapter_buffers)
  try:modules,_,callbacks=preparation.prepare()
  finally:
   entry.HostPreparation._load_current=original_load
   entry.HostPreparation._validate_current=original_validate
  need(not any(n=='tools' or n.startswith('tools.') for n in sys.modules),'tools_before_dependency')
  neutral={n:buffers['dependency.'+n] for n in ns.CHILD_ORDER}
  owner=ns.HelperSources(mode='child',buffers=neutral,origins={n:receipts['dependency.'+n]['path'] for n in ns.CHILD_ORDER},hashes={n:sha(raw) for n,raw in neutral.items()})
  package=owner.load();producer=package.dependency_producer
  invented=types.ModuleType('_successor_invented_fixture')
  invented.__file__=receipts['invented_fixture']['path']
  invented.__builtins__=dict(vars(builtins),__import__=owner.import_authored)
  exec(compile(buffers['invented_fixture'],invented.__file__,'exec',dont_inherit=True,optimize=0),invented.__dict__)
  if packet['mode']=='setup_unpack':raise KeyboardInterrupt('invented unpack setup')
  source_buffers=dict(neutral,closure_manifest=canonical(adapter_rows))
  data,ops=invented.unpack(packet['dependency'],packet['fixed'],source_buffers,request['review_sha256'],complete=True)
  context=entry.make_context(v);context['child_argv']=request['argv_prefix']+sys.argv[1:]
  need(context['operation_id']==data['expectation']['operation_id'],'operation')
  control=modules['control'];records=control.reserve_child(context=context)
  original_close=records.close
  def close_records():record_closes.append(True);return original_close()
  records.close=close_records
  if packet['mode']=='setup_records':raise KeyboardInterrupt('invented records setup')
  original_new=ops.new
  def new(key,mode,**kw):
   if any(bytes.fromhex(v['key_hex'])==key for v in ops.vectors):return original_new(key,mode,**kw)
   need(key in (bytes(range(16)),bytes(range(32))),'invented_cipher_key')
   need(ops.modules['ctypes'].CDLL is not ops.original and 'Cryptodome.Cipher.AES' in sys.modules,'guard_lifetime')
   cipher_calls.append(mode)
   class IdentityCipher:
    def encrypt(self,value):return value
    def decrypt(self,value):return value
   return IdentityCipher()
  helper=types.ModuleType(invented.HELPER);helper.new=new
  need(invented.HELPER not in sys.modules and 'ctypes' not in sys.modules,'helper_preloaded')
  owned_helpers={invented.HELPER:helper,'ctypes':ops.modules['ctypes']}
  sys.modules[invented.HELPER]=helper;installed.add(invented.HELPER)
  if packet['mode']=='setup_helper':raise KeyboardInterrupt('invented helper setup')
  sys.modules['ctypes']=ops.modules['ctypes'];installed.add('ctypes')
  source=context['repository_root']/context['source_manifest']['relative_path']
  def opened(path,flags):
   need(pathlib.Path(path)==source and not flags&(os.O_RDWR|os.O_WRONLY|os.O_CREAT|os.O_TRUNC),'stream_open')
   need(ops.modules['ctypes'].CDLL is not ops.original,'guard_lifetime')
   opens.append(str(path));return os.open(path,flags)
  def read(fd,n):
   if packet['mode']=='phase2_failure' and len(opens)==2:raise OSError('invented phase2')
   return os.read(fd,n)
  def closed(fd):closes.append(fd);return os.close(fd)
  modules['factory'].os=types.SimpleNamespace(open=opened,read=read,close=closed,fstat=os.fstat,lseek=os.lseek)
  def factory(controller,stage_source,dependency):
   factory_calls.append(True);owner.intact()
   if packet['mode']=='missing_raw':
    raw=pathlib.Path(dependency['provenance']['path']);raw.rename(raw.with_name('preserved-raw.json'))
   if packet['mode']=='adapter_live_mutation':
    adapter_owner.modules['dependency_adapter_binding'].need.__code__=(lambda *a,**kw:None).__code__
   need(not any(n=='tools' or n.startswith('tools.') for n in sys.modules),'tools_before_factory')
   if packet['mode']=='interrupt_cleanup':
    sys.modules[ns.NAMESPACE]=types.ModuleType(ns.NAMESPACE)
    raise KeyboardInterrupt('invented factory plus foreign owner')
   if packet['mode']=='interrupt_factory':raise KeyboardInterrupt('invented factory interrupt')
   return callbacks(controller,stage_source,dependency)
  def release():
   releases.append(True)
   error=None
   try:need(ops.modules['ctypes'].CDLL is not ops.original,'guard_lifetime');owner.intact()
   except BaseException as e:error=e
   try:callbacks.close()
   except BaseException as cleanup:
    if error is not None:raise error from cleanup
    raise
   if error is not None:raise error
  wiring=module('_outer_successor_wiring',buffers['successor_wiring'],receipts['successor_wiring']['path'])
  answer=entry.run_invented(helpers=owner,runtime_wiring=wiring,inputs=data,ops=ops,folder=pathlib.Path(request['folder'])/'composition',control=control,context=context,records=records,
    adapter_owner=adapter_owner,adapter_request=packet['adapter_request'],adapter_request_sha256=packet['adapter_request_sha256'],adapter_buffers=adapter_buffers,
    make_callbacks_after_receipt=factory,release_callbacks_after_controller=release,monotonic=time.monotonic,
    identity=dict(operation_id=context['operation_id'],isolated=True,optimized=False,camera_commands=[]))
  owner.intact()
  artifacts=package.dependency_execution.validate_saved_composition(pathlib.Path(request['folder'])/'composition'/'collected',data,invented=True)
  bridge={name:sha(producer.read_verified(str(pathlib.Path(request['folder'])/'composition'/name),limit=2*1024**2)[0]) for name in ('completion.json','controller-result.json')}
  summary=answer['callback_result'][1];summary_hash=sha(control.encoded(summary,16384))
 except BaseException as e:primary=e
 finally:
  if records is not None and not record_closes:
   try:records.close()
   except BaseException as e:
    if primary is None:primary=e
  if callbacks is not None and not releases:
   releases.append(True)
   try:callbacks.close()
   except BaseException as e:
    if primary is None:primary=e
  for alias,expected in owned_helpers.items():
   try:
    current=sys.modules.get(alias)
    if current is expected:del sys.modules[alias]
    else:need(current is None and alias not in installed,'helper_ownership')
   except BaseException as e:
    if primary is None:primary=e
  if owner is not None and not owner.closed:
   try:owner.close()
   except BaseException as e:
    if primary is None:primary=e
  if adapter_owner is not None and not adapter_owner.closed:
   try:adapter_owner.close()
   except BaseException as e:
    if primary is None:primary=e
  if preparation is not None:
   try:preparation.close()
   except BaseException as e:
    if primary is None:primary=e
 cleanup_check_failed=False
 try:
  need(not any(n in sys.modules for n in ('_successor_binding','_successor_control','_successor_factory')),'bootstrap_cleanup')
  need(not any(n=='tools' or n.startswith('tools.') or n=='Cryptodome' or n.startswith('Cryptodome.') or n==ns.NAMESPACE or n.startswith(ns.NAMESPACE+'.') for n in sys.modules),'namespace_cleanup')
  if ops is not None:need(ops.modules['ctypes'].CDLL is ops.original,'guard_cleanup')
 except BaseException as e:
  cleanup_check_failed=True
  if primary is None:primary=e
 metrics=dict(stream_opens=len(opens),stream_closes=len(closes),stream_cipher_calls=len(cipher_calls),record_close_attempts=len(record_closes),role_release_attempts=len(releases),factory_calls=len(factory_calls))
 complete=primary is None
 result=dict(schema='invented_successor_outer_child_v1',operation_id=request['operation_id'],status='invented_outer_child_complete' if complete else 'needs_review',source_closure_sha256=sha(canonical(request['sources'])),neutral_namespace=ns.NAMESPACE,source_roles=list(ns.CHILD_ORDER),namespace_closed=owner is None or owner.closed,role_loader_closed=callbacks is None or callbacks.closed,metrics=metrics,test_injection_used=True,production_runtime_qualified=False,execution_authorized=False,feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])
 result.update(adapter_closed=adapter_owner is None or adapter_owner.closed,adapter_request_sha256=packet['adapter_request_sha256'])
 result.update(preparation.snapshot() if preparation is not None else dict(
     metadata_preflight_sha256=None,metadata_attempts=0,preparation_calls=0,
     comparison_closed=True,metadata_closed=True,metadata_close_attempts=dict(current=0,comparison=0)))
 if complete:
  need(answer['callback_result'][0]==0 and metrics==dict(stream_opens=2,stream_closes=2,stream_cipher_calls=4,record_close_attempts=1,role_release_attempts=1,factory_calls=1),'complete_metrics')
  result['dependency_artifact_sha256']=artifacts
  result['bridge_artifact_sha256']=bridge
  result['summary_sha256']=summary_hash
 if primary is not None:
  result['failure_type']=type(primary).__name__
  result['failure_code']=str(primary)[:160]
  result['cleanup_check_failed']=cleanup_check_failed
 try:
  contract.validate_terminal(result,request)
  io.write_new(pathlib.Path(request['folder'])/'outer-result.json',result)
 except BaseException as publication:
  if primary is not None:raise primary from publication
  raise
 if primary is not None:raise primary
 if packet['mode']=='malformed_stdout':sys.stdout.buffer.write(b'invented malformed stdout\n')
 else:sys.stdout.buffer.write(control.encoded(summary,16384))
 sys.stdout.buffer.flush();return 0


def run_runtime(**kwargs):
 raise ValueError("real_activation_pending")
