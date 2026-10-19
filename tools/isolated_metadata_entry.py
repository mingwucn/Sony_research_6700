"""Disposable, no-site invented-metadata entry. Not an operational activation.

Reviewed authored code and the interpreter/stdlib are trusted, not sandboxed.
Caller digests bind bytes, not review, permission, provenance or freshness.
No filesystem input paths or native/package callbacks are accepted by this API.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import base64
import hashlib
import json
import math
import subprocess
import sys
import threading
import time

MAX_PACKET = 16 * 1024**2
MAX_OUTPUT = 8 * 1024**2
HELPERS = ('source_import_audit', 'detached_metadata_loader')


def need(condition, code):
    if not condition:
        raise ValueError(code)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, allow_nan=False,
                      separators=(',', ':')).encode('ascii')


def strict_json(raw):
    def pairs(rows):
        value = {}
        for key, item in rows:
            need(key not in value, 'duplicate_key'); value[key] = item
        return value
    def finite_float(value):
        result = float(value); need(math.isfinite(result), 'nonfinite'); return result
    return json.loads(raw, object_pairs_hook=pairs, parse_float=finite_float,
                      parse_constant=lambda value: need(False, 'nonfinite'))


def checked_runtime(value):
    keys = {'executable','version','implementation','isolated','no_site','no_user_site',
            'no_bytecode','optimize','utf8_mode','path'}
    need(type(value) is dict and set(value) == keys, 'runtime_shape')
    for name in ('executable','implementation'):
        need(type(value[name]) is str and 0 < len(value[name]) <= 4096, 'runtime_string')
    need(type(value['version']) is list and len(value['version']) == 3 and
         all(type(n) is int and 0 <= n <= 10000 for n in value['version']), 'runtime_version')
    for name in ('isolated','no_site','no_user_site','optimize','utf8_mode'):
        need(type(value[name]) is int and value[name] == (0 if name=='optimize' else 1), 'runtime_flag')
    need(value['no_bytecode'] is True, 'runtime_flag')
    need(type(value['path']) is list and len(value['path']) <= 64 and
         all(type(p) is str and len(p) <= 4096 for p in value['path']), 'runtime_path')
    need(value['implementation'] == 'cpython', 'runtime_implementation')
    return strict_json(canonical(value))


def encode_arguments(value):
    """Typed builtin-only wire tree; bytes cannot collide with user dictionaries."""
    active = set(); nodes = 0; budget = 0
    def visit(item, depth):
        nonlocal nodes, budget
        nodes += 1; budget += 32
        need(nodes <= 100000 and depth <= 80, 'argument_tree_bound')
        kind = type(item)
        if kind in (bytes, str):
            need(len(item) <= 2*1024**2, 'argument_scalar_bound')
            budget += len(item)* (2 if kind is bytes else 12)
        need(budget <= MAX_PACKET, 'argument_budget')
        if item is None: return ['none', None]
        if kind is bool: return ['bool', item]
        if kind is int:
            need(item.bit_length() <= 4096, 'argument_integer_bound')
            budget += 1234; return ['int', item]
        if kind is float:
            need(math.isfinite(item), 'argument_nonfinite'); return ['float', item]
        if kind is str: return ['str', item]
        if kind is bytes: return ['bytes', base64.b64encode(item).decode('ascii')]
        need(kind in (dict, list), 'argument_type')
        need(id(item) not in active, 'argument_cycle'); active.add(id(item))
        try:
            if kind is list: return ['list', [visit(v, depth+1) for v in item]]
            need(all(type(k) is str for k in item), 'argument_key')
            return ['dict', [[visit(k, depth+1), visit(v, depth+1)] for k,v in item.items()]]
        finally:
            active.remove(id(item))
    result = visit(value, 0)
    need(len(canonical(result)) <= MAX_PACKET, 'argument_budget')
    return result


# This fixed text, not a disk module or caller-selected entry, is the child entry.
BOOTSTRAP = r'''
import base64,builtins,hashlib,json,math,sys,types
def need(ok,code):
 if not ok:raise ValueError(code)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,ensure_ascii=True,allow_nan=False,separators=(',',':')).encode('ascii')
def pairs(rows):
 d={}
 for k,v in rows:
  need(k not in d,'duplicate_key');d[k]=v
 return d
def forbidden():
 return sorted(n for n in sys.modules if n=='tools' or n.startswith(('tools.','Crypto','Cryptodome','cffi','_cffi','_a6700_metadata.')))
def profile():
 return dict(executable=sys.executable,version=list(sys.version_info[:3]),implementation=sys.implementation.name,
  isolated=sys.flags.isolated,no_site=sys.flags.no_site,no_user_site=sys.flags.no_user_site,
  no_bytecode=sys.dont_write_bytecode,optimize=sys.flags.optimize,utf8_mode=sys.flags.utf8_mode,path=list(sys.path))
owner=None
try:
 need(len(sys.argv)==2 and len(sys.orig_argv)==9,'argv_shape')
 need(sys.orig_argv[:7]==[sys.executable,'-I','-S','-B','-X','utf8','-c'] and sys.orig_argv[8]==sys.argv[1],'argv_policy')
 raw=sys.stdin.buffer.read(16*1024**2+1);need(len(raw)<=16*1024**2,'packet_bound')
 need(sha(raw)==sys.argv[1],'packet_digest')
 packet=json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:need(False,'nonfinite'))
 need(type(packet) is dict and set(packet)=={'schema','invented','helpers','public','arguments','bootstrap_sha256','runtime','camera_commands'},'packet_shape')
 need(packet['schema']=='invented_isolated_metadata_request_v1' and packet['invented'] is True and packet['camera_commands']==[],'packet_mode')
 need(packet['bootstrap_sha256']==sha(sys.orig_argv[7].encode('utf-8')),'bootstrap_binding')
 startup=profile();need(canonical(startup)==canonical(packet['runtime']),'runtime_binding')
 need(startup['implementation']=='cpython' and all(startup[k]==1 for k in ('isolated','no_site','no_user_site','utf8_mode')) and startup['no_bytecode'] is True and startup['optimize']==0,'startup_flags')
 need(not forbidden() and 'site' not in sys.modules,'startup_imports')
 before_aliases=forbidden()
 helpers=packet['helpers'];need(type(helpers) is dict and set(helpers)=={'source_import_audit','detached_metadata_loader'},'helper_roster')
 buffers={};pins={};origins={};total=0
 for name,row in helpers.items():
  need(type(row) is dict and set(row)=={'base64','sha256','origin'},'helper_shape')
  need(row['origin']=='<checked-helper:'+name+'>','helper_origin')
  need(type(row['base64']) is str and len(row['base64'])<=3*1024**2,'helper_bound')
  buf=base64.b64decode(row['base64'],validate=True)
  need(0<len(buf)<=2*1024**2 and sha(buf)==row['sha256'],'helper_digest')
  buffers[name]=buf;pins[name]=row['sha256'];origins[name]=row['origin'];total+=len(buf)
 # Both helper byte buffers verified and compiled before either is executed.
 compiled={n:compile(buf,origins[n],'exec',dont_inherit=True,optimize=0) for n,buf in buffers.items()}
 namespace=types.SimpleNamespace()
 permitted=frozenset(('ast','hashlib','re','builtins','json','math','sys','types'))
 def helper_import(name,globals=None,locals=None,fromlist=(),level=0):
  need(level==0,'helper_relative_import')
  if name=='tools':
   need(tuple(fromlist)==('source_import_audit',) and hasattr(namespace,'source_import_audit'),'helper_authored_import')
   return namespace
  need(name in permitted,'helper_external_import')
  return builtins.__import__(name,globals,locals,fromlist,level)
 for name in ('source_import_audit','detached_metadata_loader'):
  module=types.ModuleType('_a6700_bootstrap.'+name);module.__file__=origins[name]
  module.__builtins__=dict(vars(builtins),__import__=helper_import)
  exec(compiled[name],vars(module));setattr(namespace,name,module)
 loader=namespace.detached_metadata_loader
 public=packet['public'];need(type(public) is dict and set(public)==loader.ROSTER,'public_roster')
 sources={};source_hashes={}
 for name,row in public.items():
  need(type(row) is dict and set(row)=={'base64','sha256','origin'},'public_shape')
  need(row['origin']=='<checked-public:'+name+'>','public_origin')
  need(type(row['base64']) is str and len(row['base64'])<=3*1024**2,'public_bound')
  buf=base64.b64decode(row['base64'],validate=True);total+=len(buf)
  need(0<len(buf)<=2*1024**2 and total<=8*1024**2 and sha(buf)==row['sha256'],'public_digest')
  sources[name]=buf;source_hashes[name]=row['sha256']
 count=0
 def decode(node,depth=0):
  global count
  count+=1;need(count<=100000 and depth<=80,'argument_tree_bound')
  need(type(node) is list and len(node)==2 and type(node[0]) is str,'argument_node')
  tag,v=node
  if tag=='none':need(v is None,'argument_none');return None
  if tag=='bool':need(type(v) is bool,'argument_bool');return v
  if tag=='int':need(type(v) is int and v.bit_length()<=4096,'argument_int');return v
  if tag=='float':need(type(v) is float and math.isfinite(v),'argument_float');return v
  if tag=='str':need(type(v) is str and len(v)<=2*1024**2,'argument_str');return v
  if tag=='bytes':
   need(type(v) is str and len(v)<=3*1024**2,'argument_bytes')
   b=base64.b64decode(v,validate=True);need(len(b)<=2*1024**2,'argument_bytes');return b
  need(type(v) is list,'argument_container')
  if tag=='list':return [decode(x,depth+1) for x in v]
  need(tag=='dict','argument_tag');d={}
  for row in v:
   need(type(row) is list and len(row)==2,'argument_pair')
   k=decode(row[0],depth+1);need(type(k) is str and k not in d,'argument_key')
   d[k]=decode(row[1],depth+1)
  return d
 arguments=decode(packet['arguments']);need(type(arguments) is dict,'argument_keywords')
 owner=loader.DetachedMetadata(buffers=sources,expected_hashes=source_hashes).load()
 result=owner.call(**arguments);owner.close()
 need(owner.closed and not owner.modules and not owner.compiled and not owner.buffers and not owner.construction,'loader_cleanup')
 need(not forbidden() and 'site' not in sys.modules and profile()==startup,'final_imports_or_startup_changed')
 output=dict(schema='invented_isolated_metadata_result_v1',status='complete',packet_sha256=sha(raw),
  bootstrap_sha256=packet['bootstrap_sha256'],helper_sha256=pins,helper_origins=origins,
  public_sha256=source_hashes,startup=startup,argv_flags_bound=True,no_site_observed=True,
  checked_helper_buffers_executed=True,loader_closed=True,authored_aliases_before=before_aliases,
  authored_aliases_after=forbidden(),metadata_result=result,
  stdlib_origins_verified=False,review_authenticated=False,execution_authorized=False,
  actual_inputs_accessed=False,feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])
 # Bounded UTF-8 accounting precedes whole-result serialization, including keys.
 output=loader.detached_result(output)
 encoded=json.dumps(output,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode('utf-8')
 need(len(encoded)<=8*1024**2,'output_bound')
 sys.stdout.buffer.write(encoded);sys.stdout.buffer.flush()
except BaseException:
 if owner is not None and not owner.closed:
  try:owner.close()
  except BaseException:pass
 sys.stdout.write('{"status":"needs_review","code":"metadata_child_refused","camera_commands":[]}')
 raise SystemExit(2)
'''


def make_packet(*, helpers, helper_hashes, public, public_hashes, arguments, runtime):
    """Capture supplied bytes once. Expected hashes are external caller inputs."""
    need(type(helpers) is dict and type(helper_hashes) is dict and
         set(helpers) == set(helper_hashes) == set(HELPERS), 'helper_roster')
    need(type(public) is dict and type(public_hashes) is dict and
         set(public) == set(public_hashes) and len(public) == 14, 'public_roster')
    total = 0
    def rows(buffers, hashes, prefix):
        nonlocal total
        result = {}
        for name, raw in buffers.items():
            need(type(name) is str and name.isidentifier() and name.isascii(), 'source_label')
            need(type(raw) is bytes and 0 < len(raw) <= 2*1024**2, 'source_bound')
            total += len(raw); need(total <= 8*1024**2, 'source_total_bound')
            need(type(hashes[name]) is str and sha(raw) == hashes[name], 'source_digest')
            result[name] = dict(base64=base64.b64encode(raw).decode('ascii'),
                                sha256=hashes[name], origin='<checked-'+prefix+':'+name+'>')
        return result
    helper_rows = rows(dict(helpers), dict(helper_hashes), 'helper')
    public_rows = rows(dict(public), dict(public_hashes), 'public')
    packet = dict(schema='invented_isolated_metadata_request_v1', invented=True,
        helpers=helper_rows, public=public_rows, arguments=encode_arguments(arguments),
        bootstrap_sha256=sha(BOOTSTRAP.encode('utf-8')), runtime=checked_runtime(runtime), camera_commands=[])
    raw = canonical(packet); need(len(raw) <= MAX_PACKET, 'packet_bound')
    return raw


def runtime_profile():
    """Expected child profile; caller must supply the isolated no-site sys.path."""
    return dict(executable=sys.executable, version=list(sys.version_info[:3]),
        implementation=sys.implementation.name, isolated=sys.flags.isolated,
        no_site=sys.flags.no_site, no_user_site=sys.flags.no_user_site,
        no_bytecode=sys.dont_write_bytecode, optimize=sys.flags.optimize,
        utf8_mode=sys.flags.utf8_mode, path=list(sys.path))


def validate_result(value, request, expected_packet_sha256):
    """Closed outer observation and retained-loader contract, never authority."""
    keys = ('schema status packet_sha256 bootstrap_sha256 helper_sha256 helper_origins public_sha256 startup '
        'argv_flags_bound no_site_observed checked_helper_buffers_executed loader_closed authored_aliases_before '
        'authored_aliases_after metadata_result stdlib_origins_verified review_authenticated execution_authorized '
        'actual_inputs_accessed feature_supported recovery_proven device_write_gate_passed camera_commands').split()
    need(type(value) is dict and set(value)==set(keys), 'result_shape')
    count = 0
    def check(item, depth=0):
        nonlocal count
        count += 1; need(count<=200000 and depth<=100, 'result_bound')
        if type(item) is dict:
            for k,v in item.items(): check(k,depth+1); check(v,depth+1)
        elif type(item) is list:
            for v in item: check(v,depth+1)
        elif type(item) is str:
            need(len(item)<=2*1024**2 and not any(0xd800<=ord(c)<=0xdfff for c in item), 'result_string')
        elif type(item) is int: need(item.bit_length()<=4096, 'result_integer')
        elif type(item) is float: need(math.isfinite(item), 'result_nonfinite')
        else: need(item is None or type(item) is bool, 'result_type')
    check(value)
    need(value['schema']=='invented_isolated_metadata_result_v1' and value['status']=='complete', 'result_schema')
    need(value['packet_sha256']==expected_packet_sha256 and
        value['bootstrap_sha256']==sha(BOOTSTRAP.encode('utf-8')) and
        value['helper_sha256']=={n:r['sha256'] for n,r in request['helpers'].items()} and
        value['helper_origins']=={n:r['origin'] for n,r in request['helpers'].items()} and
        value['public_sha256']=={n:r['sha256'] for n,r in request['public'].items()} and
        canonical(checked_runtime(value['startup']))==canonical(checked_runtime(request['runtime'])), 'result_binding')
    need(all(value[k] is True for k in ('argv_flags_bound','no_site_observed','checked_helper_buffers_executed','loader_closed')) and
        value['authored_aliases_before']==value['authored_aliases_after']==value['camera_commands']==[], 'result_observation')
    need(all(value[k] is False for k in ('stdlib_origins_verified','review_authenticated','execution_authorized',
        'actual_inputs_accessed','feature_supported','recovery_proven','device_write_gate_passed')), 'result_authority')
    inner=value['metadata_result']
    inner_flags=('interpreter_startup_verified','stdlib_origins_verified','validator_execution_owned',
        'actual_inputs_accessed','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed')
    need(type(inner) is dict and set(inner)==set(inner_flags)|{'schema','metadata_result',
        'checked_public_buffer_execution','public_source_count','source_hashes','camera_commands'}, 'inner_shape')
    need(inner['schema']=='invented_checked_public_metadata_result_v1' and
        inner['checked_public_buffer_execution'] is True and type(inner['public_source_count']) is int and
        inner['public_source_count']==14 and inner['source_hashes']==value['public_sha256'] and
        inner['camera_commands']==[] and all(inner[k] is False for k in inner_flags), 'inner_binding')
    return value


def run_invented(*, packet, expected_packet_sha256, timeout=20):
    """One child, bounded pipes, deadline, kill/reap; never retries or activates."""
    need(type(packet) is bytes and 0 < len(packet) <= MAX_PACKET, 'packet_bound')
    need(type(expected_packet_sha256) is str and sha(packet) == expected_packet_sha256, 'packet_digest')
    need(type(timeout) in (int,float) and math.isfinite(timeout) and 0 < timeout <= 30, 'timeout_bound')
    request = strict_json(packet)
    argv = [sys.executable,'-I','-S','-B','-X','utf8','-c',BOOTSTRAP,expected_packet_sha256]
    stdout = bytearray(); stderr = bytearray(); stop = threading.Event(); errors = []
    process = None; threads = []; reason = 'reaped'; exit_code = None
    reaped=False; kill_attempted=False; wait_attempted=False; primary=None; cleanup_errors=[]
    close_lock=threading.Lock()
    closes={name:dict(attempted=False,completed=False,error=None) for name in ('stdin','stdout','stderr')}
    def close_once(pipe,name):
        with close_lock:
            if closes[name]['attempted']: return
            closes[name]['attempted']=True
        try:
            pipe.close(); closes[name]['completed']=True
        except BaseException as error:
            closes[name]['error']=type(error).__name__; raise
    def read(pipe, sink):
        try:
            while True:
                chunk = pipe.read(65536)
                if not chunk: break
                if len(sink)+len(chunk) > MAX_OUTPUT:
                    errors.append('output_bound'); stop.set(); break
                sink.extend(chunk)
        except BaseException:
            errors.append('pipe_read'); stop.set()
    def write(pipe):
        try:
            pipe.write(packet); pipe.flush()
        except BaseException as error:
            errors.append('pipe_write:'+type(error).__name__); stop.set()
        finally:
            try: close_once(pipe,'stdin')
            except BaseException: errors.append('stdin_close'); stop.set()
    try:
        process = subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        for target,args in ((read,(process.stdout,stdout)),(read,(process.stderr,stderr)),(write,(process.stdin,))):
            thread = threading.Thread(target=target,args=args,daemon=True); threads.append(thread); thread.start()
        deadline = time.monotonic()+timeout
        while True:
            exit_code=process.poll()
            if exit_code is not None:
                reaped=True; break
            if stop.wait(min(.02,max(0,deadline-time.monotonic()))):
                reason='terminated_after_pipe_failure'; break
            if time.monotonic() >= deadline:
                reason='terminated_after_timeout'; break
        if not reaped:
            kill_attempted=True; process.kill()
            wait_attempted=True; exit_code=process.wait(timeout=10); reaped=True
    except BaseException as error:
        primary=error; reason='supervision_exception'
    finally:
        if process is not None:
            if not reaped and not kill_attempted:
                kill_attempted=True
                try: process.kill()
                except BaseException as error: cleanup_errors.append('kill:'+type(error).__name__)
            if not reaped and not wait_attempted:
                wait_attempted=True
                try: exit_code=process.wait(timeout=10); reaped=True
                except BaseException as error: cleanup_errors.append('wait:'+type(error).__name__)
            for thread in threads:
                try: thread.join(timeout=2)
                except BaseException as error: cleanup_errors.append('join:'+type(error).__name__)
            # A live reader/writer may own a pipe lock. Do not block on its close.
            for name,pipe in (('stdin',process.stdin),('stdout',process.stdout),('stderr',process.stderr)):
                if any(t.is_alive() for t in threads):
                    cleanup_errors.append('pipe_retained_live_thread'); continue
                try: close_once(pipe,name)
                except BaseException as error: cleanup_errors.append('close:'+type(error).__name__)
    threads_stopped=not any(t.is_alive() for t in threads)
    result = None
    if reason == 'reaped' and reaped and threads_stopped and exit_code == 0 and not errors and not cleanup_errors and not stderr:
        try:
            result=validate_result(strict_json(bytes(stdout)),request,expected_packet_sha256)
        except (ValueError,KeyError,TypeError,RecursionError):
            pass
    receipt=dict(status='complete' if result is not None else 'needs_review',result=result,
        child_pid=process.pid if process is not None else None,exit_code=exit_code,termination=reason,process_reaped=reaped,
        kill_attempted=kill_attempted,wait_attempted=wait_attempted,threads_stopped=threads_stopped,cleanup_errors=cleanup_errors,
        pipe_closes=closes,
        stdout_bytes=len(stdout),stderr_bytes=len(stderr),stdout_sha256=sha(bytes(stdout)),
        stderr_sha256=sha(bytes(stderr)),pipe_errors=list(errors),automatic_retry=False,
        execution_authorized=False,actual_inputs_accessed=False,camera_commands=[])
    if primary is not None:
        primary.metadata_completion=receipt
        raise primary
    return receipt


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
