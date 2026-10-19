"""Invented-only checked-buffer metadata calls; no operational activation.

Trusted reviewed authored code, not a sandbox. Interpreter, stdlib objects and
this loader/audit bootstrap are assumed; matching caller hashes grant no rights.
No process module aliases are installed, replaced or deleted.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import builtins
import json
import math
import sys
import types

from tools import source_import_audit as audit

ROSTER = frozenset(('dependency_outer_contract','dependency_operational_scope',
    'dependency_authority_grammar','dependency_basis_links','dependency_basis_recompute',
    'dependency_evidence','dependency_producer','dependency_package_preflight',
    'dependency_execution','dependency_input_semantics','dependency_source_receipts',
    'dependency_activity_metadata','dependency_legacy_bridge','dependency_candidate_context'))


def need(condition, code):
    if not condition:
        raise ValueError(code)


def detached_result(value):
    """Copy only bounded exact builtin JSON data; no owned objects escape."""
    active=set();count=0;serialized=0
    def charge(size):
        nonlocal serialized
        serialized+=size;need(serialized<=8*1024**2,'result_serialized_bound')
    def string(item):
        need(len(item)<=2*1024**2,'result_scalar_bound');charge(2)
        for char in item:
            code=ord(char)
            need(not 0xd800<=code<=0xdfff,'result_string_encoding')
            if char in ('"','\\','\b','\f','\n','\r','\t'):charge(2)
            elif code<32:charge(6)
            else:charge(1 if code<128 else 2 if code<2048 else 3 if code<65536 else 4)
    def copy(item,depth):
        nonlocal count
        count+=1;need(count<=200000 and depth<=100,'result_bound')
        kind=type(item)
        if item is None or kind in (str,bool,int):
            if kind is str:string(item)
            elif kind is int:
                need(item.bit_length()<=4096,'result_scalar_bound');charge(len(str(item)))
            else:charge(4 if item is None or item is True else 5)
            return item
        if kind is float:
            need(math.isfinite(item),'result_nonfinite');charge(len(repr(item)));return item
        need(kind in (dict,list),'result_type')
        need(id(item) not in active,'result_cycle');active.add(id(item))
        try:
            charge(2+max(0,len(item)-1))
            if kind is list:
                return [copy(v,depth+1) for v in item]
            need(all(type(k) is str for k in item),'result_key')
            result={}
            for key,value in item.items():
                count+=1;need(count<=200000,'result_bound');string(key);charge(1)
                result[key]=copy(value,depth+1)
            return result
        finally:
            active.remove(id(item))
    result=copy(value,0)
    # Only serialize after exact compact-JSON byte accounting has passed.
    need(len(json.dumps(result,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode('utf-8'))==serialized,
        'result_serialized_accounting')
    return result


class DetachedMetadata:
    """One-owner lifecycle; sole qualified call is invented context composition."""
    def __init__(self,*,buffers,expected_hashes):
        need(type(buffers) is dict and type(expected_hashes) is dict and
            set(buffers)==set(expected_hashes)==ROSTER,'metadata_source_roster')
        self.buffers=dict(buffers);self.hashes=dict(expected_hashes)
        self.modules={};self.frozen={};self.started=False;self.closed=False;self.failed=False;self.loaded=False
        self.policy_hashes=tuple(sorted(self.hashes.items()))
        self.package=types.SimpleNamespace()
        self.foreign={n:m for n,m in sys.modules.items() if n=='tools' or n.startswith('tools.')}
        self.names={'_a6700_metadata.'+n for n in ROSTER}
        graph=audit.audit_imports({'tools.'+n:v for n,v in self.buffers.items()},
            roots=('tools.dependency_candidate_context',),
            expected_hashes={'tools.'+n:h for n,h in self.hashes.items()},
            namespace_packages=('tools',),stdlib_roots=frozenset(sys.stdlib_module_names))
        self.order=tuple(n.split('.')[1] for n in graph['dependency_order'])
        self.external=frozenset(v['module'] for v in graph['external_imports'])
        # All sources were copied, parsed and hash checked before first compile;
        # all bytecode is prepared before any supplied authored member executes.
        self.compiled={n:compile(self.buffers[n],'<checked-public:'+n+'>','exec',
            dont_inherit=True,optimize=0) for n in self.order}
        self.construction=(self.order,self.external,tuple(self.compiled.items()))

    def _check_construction(self):
        order,external,compiled=self.construction
        need(type(self.order) is tuple and self.order==order and type(self.external) is frozenset and
            self.external==external and set(self.compiled)==set(order) and
            all(self.compiled[n] is code for n,code in compiled),'metadata_compiled_policy_changed')

    def _stamp(self,value,active=None):
        active=set() if active is None else active
        kind=type(value)
        if value is None or kind in (str,int,bool,bytes):return kind,value
        if kind is float:return kind,value.hex()
        if id(value) in active:return kind,id(value),'recursive_reference'
        active.add(id(value))
        try:
            if kind is types.FunctionType and any(value.__globals__ is vars(m) for m in self.modules.values()):
                cells=[]
                for cell in value.__closure__ or ():
                    try:cells.append(self._stamp(cell.cell_contents,active))
                    except ValueError:cells.append(('empty_cell',id(cell)))
                return (kind,id(value),id(value.__code__),value.__name__,value.__qualname__,value.__module__,
                    self._stamp(value.__defaults__,active),self._stamp(value.__kwdefaults__,active),
                    self._stamp(value.__annotations__,active),self._stamp(vars(value),active),tuple(cells))
            if kind is types.MethodType:
                return kind,id(value),id(value.__self__),self._stamp(value.__func__,active)
            if kind in (classmethod,staticmethod):return kind,id(value),self._stamp(value.__func__,active)
            if kind is property:
                return kind,id(value),tuple(self._stamp(v,active) for v in (value.fget,value.fset,value.fdel)),value.__doc__
            if isinstance(value,type) and value.__module__ in self.names:
                return (kind,id(value),tuple(id(c) for c in value.__bases__),tuple(id(c) for c in value.__mro__),
                    tuple((k,self._stamp(v,active)) for k,v in vars(value).items()))
            if kind is dict:return kind,id(value),tuple((self._stamp(k,active),self._stamp(v,active)) for k,v in value.items())
            if kind in (list,tuple):return kind,id(value),tuple(self._stamp(v,active) for v in value)
            if kind in (set,frozenset):return kind,id(value),frozenset(self._stamp(v,active) for v in value)
            # Borrowed stdlib objects and other instances retain identity only.
            # Their internal mutation is outside this authored-code check.
            return kind,id(value)
        finally:
            active.remove(id(value))

    def _check(self):
        need(self.started and not self.closed and not self.failed,'metadata_inactive')
        self._check_construction()
        need(tuple(sorted(self.hashes.items()))==self.policy_hashes,'metadata_policy_changed')
        need(all(sys.modules.get(n) is m for n,m in self.foreign.items()),'metadata_foreign_alias_changed')
        need(set(vars(self.package))==set(self.modules) and
            all(vars(self.package)[n] is m for n,m in self.modules.items()),'metadata_namespace_changed')
        if self.frozen:
            need(set(self.frozen)<=set(self.modules),'metadata_module_roster')
            for name,stamp in self.frozen.items():
                need(self._stamp(vars(self.modules[name]))==stamp,'metadata_live_code_changed')
        if self.loaded:need(set(self.modules)==set(self.frozen)==ROSTER,'metadata_module_roster')

    def intact(self):
        try:self._check()
        except BaseException:
            self.failed=True;raise

    def _import(self,name,globals=None,locals=None,fromlist=(),level=0):
        try:
            self.intact();need(level==0,'metadata_relative_import')
            if name=='tools' or name.startswith('tools.'):
                need(name=='tools' and type(fromlist) in (tuple,list) and fromlist and
                    all(type(n) is str and n in self.modules for n in fromlist),'metadata_authored_import')
                return self.package
            need(name in self.external,'metadata_external_import')
            return builtins.__import__(name,globals,locals,fromlist,level)
        except BaseException:
            self.failed=True;raise

    def load(self):
        try:
            need(not self.started and not self.closed and not self.failed,'metadata_reentry')
            self._check_construction()
            self.started=True
            for name in self.order:
                module=types.ModuleType('_a6700_metadata.'+name)
                module.__file__='<checked-public:'+name+'>';module.__package__='_a6700_metadata'
                module.__builtins__=dict(vars(builtins),__import__=self._import)
                self.modules[name]=module;setattr(self.package,name,module)
                exec(self.compiled[name],vars(module))
                self.frozen[name]=self._stamp(vars(module));self.intact()
            self.loaded=True
            self.intact();return self
        except BaseException as primary:
            self._failure_cleanup(primary);raise

    def _failure_cleanup(self,primary):
        self.failed=True
        try:
            if not self.closed:self.close()
        except BaseException as cleanup:
            raise primary from cleanup

    def call(self,**kwargs):
        try:
            self.intact()
            need(self.loaded,'metadata_not_loaded')
            result=self.modules['dependency_candidate_context'].validate_invented_context_composition(**kwargs)
            self.intact();copied=detached_result(result);self.intact()
            return dict(schema='invented_checked_public_metadata_result_v1',metadata_result=copied,
                checked_public_buffer_execution=True,public_source_count=len(self.modules),
                source_hashes=dict(self.hashes),interpreter_startup_verified=False,
                stdlib_origins_verified=False,validator_execution_owned=False,
                actual_inputs_accessed=False,execution_authorized=False,
                feature_supported=False,recovery_proven=False,device_write_gate_passed=False,camera_commands=[])
        except BaseException as primary:
            self._failure_cleanup(primary);raise

    def close(self):
        need(not self.closed,'metadata_reclose')
        try:
            if self.started and not self.failed:self.intact()
        finally:
            self.closed=True;self.modules.clear();self.compiled.clear();self.buffers.clear();self.frozen.clear()
            self.construction=();self.foreign.clear()
            vars(self.package).clear()
        return True


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
