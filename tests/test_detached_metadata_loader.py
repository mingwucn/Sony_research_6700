"""Invented reviewed host sources only; no payload/native/camera operations."""
import hashlib
import sys
import types
import unittest
from unittest.mock import patch

from tools import detached_metadata_loader as subject

ENTRY='dependency_candidate_context'
SUPPORT='''
VALUE={'rows':[1]}
def helper(x=1,*,y=2):return x+y
helper.__annotations__={'x':'invented'}
def build():
 cell=[1]
 def inner():return cell[0]
 return inner
closed=build()
helper.__wrapped__=closed
class BaseOne:pass
class BaseTwo:pass
class Thing(BaseOne):
 def method(self):return 1
 @property
 def prop(self):return 1
 @staticmethod
 def static():return 1
 @classmethod
 def klass(cls):return 1
bound=Thing().method
'''


def fixture(body="return {'rows':VALUE['rows']}",extra=''):
    order=sorted(subject.ROSTER-{ENTRY})+[ENTRY];buffers={}
    for i,name in enumerate(order):
        source=('from tools import '+order[i-1]+' as prior\n') if i else ''
        if name==ENTRY:
            source+=SUPPORT+'\ndef validate_invented_context_composition(**kwargs):\n'+''.join(' '+line+'\n' for line in body.splitlines())+extra
        else:source+='TOKEN='+repr(name)+'\n'
        buffers[name]=source.encode()
    return buffers,{n:hashlib.sha256(raw).hexdigest() for n,raw in buffers.items()}


def make(**kwargs):
    buffers,hashes=fixture(**kwargs)
    return subject.DetachedMetadata(buffers=buffers,expected_hashes=hashes)


class DetachedLoaderTests(unittest.TestCase):
    def current(self):
        names=('dependency_launch_context','dependency_current_metadata','dependency_outer_metadata')
        buffers={}
        for index,name in enumerate(names):
            source=('from tools import '+names[index-1]+' as prior\n') if index else ''
            source+='TOKEN='+repr(name)+'\n'
            if index==2:source+='def validate_invented_outer(**kwargs):return {"invented":True}\n'
            buffers[name]=source.encode()
        return subject.DetachedMetadata(buffers=buffers,expected_hashes={n:hashlib.sha256(v).hexdigest() for n,v in buffers.items()},purpose='current')

    def test_current_closed_graph_dispatches_three_members(self):
        owner=self.current().load()
        try:
            result=owner.call()
            self.assertEqual(result['metadata_result'],{'invented':True})
            self.assertEqual(result['public_source_count'],3)
            self.assertIs(result['execution_authorized'],False)
        finally:owner.close()

    def test_unknown_graph_purpose_is_refused(self):
        for purpose in ('runtime','',None):
            with self.subTest(purpose=purpose),self.assertRaisesRegex(ValueError,'metadata_purpose'):
                subject.DetachedMetadata(buffers={},expected_hashes={},purpose=purpose)

    def test_mutated_graph_dispatch_is_refused_and_closed(self):
        for field,value in (('purpose','comparison'),('purpose','other'),('entry','dependency_launch_context'),('method','run_runtime')):
            owner=self.current().load();setattr(owner,field,value)
            with self.subTest(field=field,value=value),self.assertRaisesRegex(ValueError,'metadata_graph_changed'):owner.call()
            self.assertTrue(owner.closed)

    def test_loaded_buffer_mutation_is_refused_and_closed(self):
        for maker in (make,self.current):
            owner=maker().load();name=next(iter(owner.buffers));owner.buffers[name]+=b'\n'
            with self.assertRaisesRegex(ValueError,'metadata_source_buffer_changed'):owner.call()
            self.assertTrue(owner.closed)

    def test_complete_graph_executes_and_authority_stays_false(self):
        loader=make().load();result=loader.call()
        self.assertEqual(result['metadata_result'],{'rows':[1]})
        self.assertEqual(result['public_source_count'],14);self.assertTrue(result['checked_public_buffer_execution'])
        for key in ('validator_execution_owned','interpreter_startup_verified','stdlib_origins_verified',
            'actual_inputs_accessed','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(result[key],False)
        loader.close();self.assertFalse(loader.modules);self.assertFalse(loader.compiled)
        self.assertFalse(loader.construction);self.assertFalse(loader.foreign)

    def test_bad_roster_or_hash_never_executes_supplied_code(self):
        buffers,hashes=fixture();hashes[ENTRY]='0'*64
        with patch('builtins.exec',side_effect=AssertionError('must not execute')):
            with self.assertRaisesRegex(ValueError,'source_hash'):
                subject.DetachedMetadata(buffers=buffers,expected_hashes=hashes)
            hashes.pop(ENTRY)
            with self.assertRaisesRegex(ValueError,'metadata_source_roster'):
                subject.DetachedMetadata(buffers=buffers,expected_hashes=hashes)

    def test_syntax_refuses_before_any_execution(self):
        buffers,hashes=fixture();buffers[ENTRY]=b'if';hashes[ENTRY]=hashlib.sha256(b'if').hexdigest()
        with patch('builtins.exec',side_effect=AssertionError('must not execute')):
            with self.assertRaisesRegex(ValueError,'source_syntax'):
                subject.DetachedMetadata(buffers=buffers,expected_hashes=hashes)

    def test_constructor_copies_source_and_policy(self):
        buffers,hashes=fixture();loader=subject.DetachedMetadata(buffers=buffers,expected_hashes=hashes)
        buffers[ENTRY]=b'raise KeyboardInterrupt';hashes[ENTRY]='0'*64
        self.assertEqual(loader.load().call()['metadata_result'],{'rows':[1]});loader.close()

    def test_all_bytecode_prepared_before_first_execution(self):
        loader=make()
        with patch('builtins.compile',side_effect=AssertionError('late compile forbidden')):
            loader.load();loader.call();loader.close()

    def test_foreign_process_modules_preserved_and_not_resolved(self):
        foreign=types.ModuleType('foreign');foreign.TOKEN='foreign'
        with patch.dict(sys.modules,{'tools.dependency_outer_contract':foreign,'tools.unrelated_owner':foreign}):
            before={n:m for n,m in sys.modules.items() if n=='tools' or n.startswith('tools.')}
            loader=make().load();self.assertIsNot(loader.modules['dependency_outer_contract'],foreign)
            loader.call();loader.close()
            self.assertTrue(all(sys.modules[n] is m for n,m in before.items()))
            self.assertFalse(any(n.startswith('_a6700_metadata') for n in sys.modules))

    def tamper(self,callback):
        loader=make().load();callback(loader,loader.modules[ENTRY])
        with self.assertRaises(ValueError):loader.call()
        self.assertTrue(loader.failed);self.assertTrue(loader.closed);self.assertFalse(loader.modules)
        with self.assertRaisesRegex(ValueError,'metadata_inactive'):loader.call()

    def test_namespace_binding_tamper(self):
        self.tamper(lambda l,m:setattr(l.package,ENTRY,object()))

    def test_module_alias_tamper(self):
        self.tamper(lambda l,m:setattr(m,'prior',object()))

    def test_function_code_tamper(self):
        self.tamper(lambda l,m:setattr(m.helper,'__code__',(lambda:0).__code__))

    def test_function_defaults_tamper(self):
        self.tamper(lambda l,m:setattr(m.helper,'__defaults__',(4,)))

    def test_function_kwdefaults_tamper(self):
        self.tamper(lambda l,m:m.helper.__kwdefaults__.update(y=4))

    def test_function_annotations_tamper(self):
        self.tamper(lambda l,m:m.helper.__annotations__.update(x='changed'))

    def test_function_closure_tamper(self):
        self.tamper(lambda l,m:m.closed.__closure__[0].cell_contents.append(2))

    def test_wrapped_function_attribute_tamper(self):
        self.tamper(lambda l,m:setattr(m.helper,'__wrapped__',lambda:0))

    def test_class_method_code_tamper(self):
        self.tamper(lambda l,m:setattr(m.Thing.method,'__code__',(lambda self:0).__code__))

    def test_property_getter_code_tamper(self):
        self.tamper(lambda l,m:setattr(m.Thing.prop.fget,'__code__',(lambda self:0).__code__))

    def test_staticmethod_code_tamper(self):
        self.tamper(lambda l,m:setattr(m.Thing.static,'__code__',(lambda:0).__code__))

    def test_classmethod_code_tamper(self):
        self.tamper(lambda l,m:setattr(m.Thing.klass.__func__,'__code__',(lambda cls:0).__code__))

    def test_class_inheritance_tamper(self):
        self.tamper(lambda l,m:setattr(m.Thing,'__bases__',(m.BaseTwo,)))

    def test_bound_method_function_tamper(self):
        self.tamper(lambda l,m:setattr(m.bound.__func__,'__code__',(lambda self:0).__code__))

    def test_result_is_detached_from_owned_globals(self):
        loader=make().load();result=loader.call();result['metadata_result']['rows'].append(9)
        self.assertEqual(loader.call()['metadata_result'],{'rows':[1]});loader.close()

    def test_returned_owned_function_is_refused(self):
        loader=make(body="return {'callback':helper}").load()
        with self.assertRaisesRegex(ValueError,'result_type'):loader.call()
        self.assertTrue(loader.closed)

    def test_result_cycle_types_and_size_limits(self):
        cycle=[];cycle.append(cycle)
        for value,code in ((cycle,'result_cycle'),({'x':object()},'result_type'),({1:0},'result_key'),
            ({'x':float('nan')},'result_nonfinite'),({'x':'x'*(2*1024**2+1)},'result_scalar_bound'),
            ({'x':1<<4097},'result_scalar_bound')):
            with self.subTest(code=code),self.assertRaisesRegex(ValueError,code):subject.detached_result(value)

    def test_mutation_during_call_refuses_before_return(self):
        loader=make(body="VALUE['rows'].append(2)\nreturn {}",extra='').load()
        with self.assertRaisesRegex(ValueError,'metadata_live_code_changed'):loader.call()
        self.assertTrue(loader.closed)

    def test_keyboardinterrupt_call_cleans_only_owned_references(self):
        marker=types.ModuleType('marker')
        with patch.dict(sys.modules,{'tools.other_owner':marker}):
            loader=make(body='raise KeyboardInterrupt').load()
            with self.assertRaises(KeyboardInterrupt):loader.call()
            self.assertTrue(loader.closed);self.assertFalse(loader.modules)
            self.assertIs(sys.modules['tools.other_owner'],marker)

    def test_partial_load_interrupt_cleans_owned_references(self):
        buffers,hashes=fixture();name=sorted(subject.ROSTER-{ENTRY})[1]
        buffers[name]+=b'raise KeyboardInterrupt\n';hashes[name]=hashlib.sha256(buffers[name]).hexdigest()
        loader=subject.DetachedMetadata(buffers=buffers,expected_hashes=hashes)
        with self.assertRaises(KeyboardInterrupt):loader.load()
        self.assertTrue(loader.closed);self.assertFalse(loader.modules);self.assertFalse(vars(loader.package))

    def test_swallowed_import_failure_still_poisoned(self):
        loader=make(body="try:\n __import__('tools',fromlist=('absent',))\nexcept ValueError:\n pass\nreturn {}").load()
        with self.assertRaisesRegex(ValueError,'metadata_inactive'):loader.call()
        self.assertTrue(loader.failed);self.assertTrue(loader.closed)

    def test_reentry_reclose_and_call_before_load_refuse(self):
        loader=make().load()
        with self.assertRaisesRegex(ValueError,'metadata_reentry'):loader.load()
        self.assertTrue(loader.closed)
        with self.assertRaisesRegex(ValueError,'metadata_reclose'):loader.close()
        loader=make()
        with self.assertRaisesRegex(ValueError,'metadata_inactive'):loader.call()
        self.assertTrue(loader.closed)

    def test_foreign_replacement_detected_but_not_deleted(self):
        original=types.ModuleType('original');replacement=types.ModuleType('replacement')
        with patch.dict(sys.modules,{'tools.other_owner':original}):
            loader=make().load();sys.modules['tools.other_owner']=replacement
            with self.assertRaisesRegex(ValueError,'metadata_foreign_alias_changed'):loader.call()
            self.assertIs(sys.modules['tools.other_owner'],replacement)

    def test_later_module_cannot_modify_frozen_previous_module(self):
        buffers,hashes=fixture();buffers[ENTRY]+=b'prior.TOKEN="changed"\n'
        hashes[ENTRY]=hashlib.sha256(buffers[ENTRY]).hexdigest()
        loader=subject.DetachedMetadata(buffers=buffers,expected_hashes=hashes)
        with self.assertRaisesRegex(ValueError,'metadata_live_code_changed'):loader.load()
        self.assertTrue(loader.closed)

    def test_primary_failure_preserved_if_cleanup_also_fails(self):
        loader=make(body='raise KeyboardInterrupt').load();close=loader.close
        def broken_close():
            close();raise RuntimeError('cleanup example')
        with patch.object(loader,'close',broken_close):
            with self.assertRaises(KeyboardInterrupt) as caught:loader.call()
        self.assertIsInstance(caught.exception.__cause__,RuntimeError);self.assertTrue(loader.closed)

    def test_policy_mutation_refuses(self):
        self.tamper(lambda l,m:l.hashes.update({ENTRY:'0'*64}))

    def test_runtime_refuses(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):subject.run_runtime()

    def test_late_from_tools_resolves_owned_module(self):
        foreign=types.ModuleType('foreign');foreign.TOKEN='foreign'
        with patch.dict(sys.modules,{'tools.dependency_outer_contract':foreign}):
            loader=make(body="from tools import dependency_outer_contract as late\nreturn {'token':late.TOKEN}").load()
            self.assertEqual(loader.call()['metadata_result'],{'token':'dependency_outer_contract'});loader.close()

    def test_relative_bare_dotted_and_undeclared_import_calls_poison_loader(self):
        for name,fromlist,level in (('tools',(),0),('tools.missing',('x',),0),
            ('os',(),1),('ctypes',(),0)):
            loader=make().load()
            with self.subTest(name=name,level=level),self.assertRaises(ValueError):loader._import(name,fromlist=fromlist,level=level)
            self.assertTrue(loader.failed);loader.close()

    def test_close_detects_mutation_and_still_clears_owned_references(self):
        loader=make().load();loader.modules[ENTRY].VALUE['rows'].append(2)
        with self.assertRaisesRegex(ValueError,'metadata_live_code_changed'):loader.close()
        self.assertTrue(loader.closed);self.assertFalse(loader.modules)

    def test_result_nesting_count_and_serialized_bound(self):
        nested=[];leaf=nested
        for _ in range(101):child=[];leaf.append(child);leaf=child
        for value,code in ((nested,'result_bound'),([0]*200001,'result_bound'),
            (['x'*(2*1024**2)]*5,'result_serialized_bound')):
            with self.subTest(code=code),self.assertRaisesRegex(ValueError,code):subject.detached_result(value)

    def test_constructor_compile_interrupt_runs_no_source(self):
        compile_real=compile
        def interrupted(source,filename,mode,*args,**kwargs):
            if filename.startswith('<checked-public:'):raise KeyboardInterrupt
            return compile_real(source,filename,mode,*args,**kwargs)
        with patch('builtins.compile',interrupted),patch('builtins.exec',side_effect=AssertionError('must not execute')):
            with self.assertRaises(KeyboardInterrupt):make()

    def test_compiled_order_and_external_policy_mutation_refuse_before_exec(self):
        for mutation in (lambda l:l.compiled.update({ENTRY:compile('raise KeyboardInterrupt','<replacement>','exec')}),
            lambda l:setattr(l,'order',tuple(reversed(l.order))),
            lambda l:setattr(l,'external',l.external|{'ctypes'})):
            loader=make();mutation(loader)
            with patch('builtins.exec',side_effect=AssertionError('must not execute')):
                with self.assertRaisesRegex(ValueError,'metadata_compiled_policy_changed'):loader.load()
            self.assertTrue(loader.failed);self.assertTrue(loader.closed)

    def test_aggregate_keys_escapes_and_values_refuse_before_whole_serialization(self):
        cases=[(['x'*(2*1024**2)]*5,'result_serialized_bound'),
            ({'x'*(2*1024**2+1):0},'result_scalar_bound'),
            ({str(i)+'\x01'*1000000:0 for i in range(2)},'result_serialized_bound'),
            (['\x01'*1000000]*2,'result_serialized_bound'),
            ({'\ud800':0},'result_string_encoding'),({'x':'\udfff'},'result_string_encoding')]
        for value,code in cases:
            with self.subTest(code=code),patch.object(subject.json,'dumps',side_effect=AssertionError('oversized serialization forbidden')):
                with self.assertRaisesRegex(ValueError,code):subject.detached_result(value)

    def test_compact_serialized_accounting_for_unicode_escapes_and_numbers(self):
        value={'unicode':'汉字😀','escape':'"\\\n\x00','values':[None,True,False,-5,0.0,-0.0,1.23e50]}
        self.assertEqual(subject.detached_result(value),value)
