"""Delegate invented-file observations to exact RuntimeOps.reader/root methods.

Startup, dispatch, collection, producer and parent code are unchanged. The
remaining bootstrap, native loader, audit delivery and cipher are inert doubles.
No installed dependency, native executable payload or protected input is read.
"""
from dependency_runtime_route_fixture import route_fixture_source


MODES=('complete','unused_bytes','same_byte_replacement','missing_member',
       'hardlink','trusted_bytes','root_replacement','late_native')


def filesystem_runtime_source(mode='complete'):
    if type(mode) is not str or mode not in MODES:
        raise ValueError('synthetic_filesystem_runtime_mode')
    raw=route_fixture_source('complete')
    old=b'            self.ops = _synthetic_route_ops(self.package, self.inputs)'
    new=old+b'\n            _install_filesystem_observer(self)'
    if raw.count(old)!=1:raise AssertionError('synthetic filesystem constructor drift')
    raw=raw.replace(old,new)
    old=b'        self.closed = True\n        # Each owned binding'
    new=b'        self.closed = True\n        _close_filesystem_trace(self)\n        # Each owned binding'
    if raw.count(old)!=1:raise AssertionError('synthetic filesystem close drift')
    raw=raw.replace(old,new)
    suffix=rb'''
import os
from pathlib import Path

def _filesystem_owned_path(owner,path):
 path=Path(path);base=Path(owner.inputs['expectation']['roots']['package']['path']).parent
 assert base.name=='invented-dependency-files' and path.is_absolute() and path.is_relative_to(base)
 assert path!=base,'synthetic filesystem root ownership'
 return path

class _FilesystemTrace:
 def __init__(self,owner):
  self.owner=owner;self.events=[];self.live=set();self.closed=False
  self.paths=set()
  policy=owner.inputs['expectation']
  self.paths.update(policy['roots']['package']['path']+'/'+r for r in owner.inputs['package']['manifest']['files'])
  self.paths.update(owner.producer.target(policy,row) for row in policy['trusted_origins'].values())
  self.original={n:getattr(os,n) for n in ('open','read','close')}
  def opened(path,flags,*args,**kw):
   tracked=isinstance(path,(str,bytes,os.PathLike)) and Path(path).as_posix() in self.paths
   if tracked:self.events.append(dict(op='open_attempt',flags=flags))
   fd=self.original['open'](path,flags,*args,**kw)
   if tracked:self.live.add(fd);self.events.append(dict(op='open_returned',fd=fd,flags=flags))
   return fd
  def read(fd,size):
   data=self.original['read'](fd,size)
   if fd in self.live:self.events.append(dict(op='read_returned',fd=fd,requested=size,returned=len(data)))
   return data
  def close(fd):
   tracked=fd in self.live
   if tracked:self.events.append(dict(op='close_attempt',fd=fd))
   answer=self.original['close'](fd)
   if tracked:self.live.remove(fd);self.events.append(dict(op='close_returned',fd=fd))
   return answer
  self.installed=dict(open=opened,read=read,close=close)
  for name,value in self.installed.items():setattr(os,name,value)
 def close(self):
  self.closed=True;changed=[]
  for name in reversed(tuple(self.installed)):
   if getattr(os,name) is self.installed[name]:setattr(os,name,self.original[name])
   else:changed.append(name)
  if changed:raise ValueError('synthetic_filesystem_trace_ownership')

def _install_filesystem_observer(owner):
 ops=owner.ops;policy=owner.inputs['expectation'];producer=owner.producer
 owner.filesystem_reads=[];owner.filesystem_roots=[];owner.filesystem_faults=[]
 owner.filesystem_trace=_FilesystemTrace(owner)
 owner.filesystem_original_reader=owner.original_class.reader
 owner.filesystem_original_root=owner.original_class.root
 # Remove all fallback bytes/receipts. Every observer read must delegate to the
 # exact original class method on a newly authored file, never FakeOps.reader.
 ops.contents=ops.observed=ops.roots=None
 owner.filesystem_unused=next(policy['roots']['package']['path']+'/'+r
  for r in sorted(owner.inputs['package']['manifest']['files']) if '/data/item' in r)
 owner.filesystem_trusted=producer.target(policy,policy['trusted_origins']['ctypes'])
 owner.filesystem_native=producer.target(policy,policy['native_libraries']['cpuid'])
 def reader(path,row):
  ops.reads.append(path);event=dict(path=path,expected_sha256=row['sha256'],completed=False)
  owner.filesystem_reads.append(event)
  try:raw,receipt=owner.filesystem_original_reader(ops,path,row)
  except BaseException as error:
   event.update(error_type=type(error).__name__,error_code=str(error));raise
  event.update(completed=True,bytes=len(raw),sha256=producer.sha(raw),receipt_sha256=producer.core._hash(receipt))
  if (_FILESYSTEM_MODE=='late_native' and path==owner.filesystem_native and
      not owner.filesystem_faults):
   # The collector receives the verified old bytes/receipt. The following
   # original producer reread must reject the changed invented native bytes.
   target=_filesystem_owned_path(owner,path)
   target.write_bytes(raw+b'invented late drift')
   owner.filesystem_faults.append('late_native_after_original_read')
  return raw,receipt
 def root(path):
  ops.root_calls+=1
  value=owner.filesystem_original_root(ops,path)
  owner.filesystem_roots.append(dict(path=path,receipt_sha256=producer.core._hash(value)))
  return value
 ops.reader=reader;ops.root=root
 mode=_FILESYSTEM_MODE
 target=_filesystem_owned_path(owner,owner.filesystem_unused)
 if mode in ('unused_bytes','trusted_bytes'):
  if mode=='trusted_bytes':target=_filesystem_owned_path(owner,owner.filesystem_trusted)
  with target.open('ab') as stream:stream.write(b'invented drift')
  owner.filesystem_faults.append(mode)
 elif mode in ('same_byte_replacement','missing_member'):
  retained=_filesystem_owned_path(owner,str(target)+'.retained-before')
  assert not retained.exists()
  raw=target.read_bytes();target.rename(retained)
  if mode=='same_byte_replacement':
   with target.open('xb') as stream:stream.write(raw)
  owner.filesystem_faults.append(mode)
 elif mode=='hardlink':
  link=_filesystem_owned_path(owner,str(target)+'.invented-link')
  assert not link.exists();os.link(target,link);owner.filesystem_faults.append(mode)
 elif mode=='root_replacement':
  package=_filesystem_owned_path(owner,policy['roots']['package']['path'])
  retained=_filesystem_owned_path(owner,str(package)+'.retained-before')
  assert not retained.exists();package.rename(retained);package.mkdir(exist_ok=False)
  owner.filesystem_faults.append(mode)

def _close_filesystem_trace(owner):
 trace=getattr(owner,'filesystem_trace',None)
 if trace is not None:
  try:trace.close()
  except BaseException as error:owner.cleanup_errors.append(str(error))

def _filesystem_observation(owner):
 trace=getattr(owner,'filesystem_trace',None)
 reads=getattr(owner,'filesystem_reads',[]);roots=getattr(owner,'filesystem_roots',[])
 return dict(schema='synthetic_filesystem_runtime_observation_v1',mode=_FILESYSTEM_MODE,
  original_reader_delegated=True,original_root_delegated=True,reads=reads,roots=roots,
  faults=getattr(owner,'filesystem_faults',[]),events=[] if trace is None else trace.events,
  live_fds=[] if trace is None else sorted(trace.live),trace_restored=trace is not None and trace.closed,
  fallback_bytes_and_receipts_removed=owner.ops is not None and owner.ops.contents is owner.ops.observed is owner.ops.roots is None,
  installed_dependency_observed=False,native_execution_performed=False,real_cryptography_performed=False,
  actual_runtime_verified=False,execution_authorized=False,feature_supported=False,recovery_proven=False,
  device_write_gate_passed=False,camera_commands=[])

_SyntheticRuntimeOwner.filesystem_observation=_filesystem_observation
'''
    return raw+b'\n_FILESYSTEM_MODE='+repr(mode).encode()+b'\n'+suffix
