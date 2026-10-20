"""Fresh-process checked helper graphs; only authored Python or invented bytes."""
import hashlib
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'tools/dependency_successor_sources.py'
PREFIX = '''
import hashlib,pathlib,sys,types
raw=pathlib.Path(SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN
s=types.ModuleType('subject');exec(compile(raw,SOURCE,'exec'),s.__dict__)
def owner(mode='child',real=False):
 order=s.CHILD_ORDER if mode=='child' else s.PARENT_ORDER
 buffers={n:(pathlib.Path(ROOT)/'tools'/(n+'.py')).read_bytes() if real else b'x=1\\n' for n in order}
 if not real:
  buffers['dependency_producer']=b'from tools import dependency_evidence as core\\n'
  buffers['dependency_execution']=b'def lazy():\\n from tools import dependency_producer as p\\n return p\\n'
 return buffers,dict(mode=mode,buffers=buffers,origins={n:SOURCE for n in order},hashes={n:hashlib.sha256(v).hexdigest() for n,v in buffers.items()})
def make(mode='child',real=False):
 return s.HelperSources(**owner(mode,real)[1])
def refuse(fn,code):
 try:fn()
 except ValueError as e:assert str(e)==code,(str(e),code)
 else:raise AssertionError(code)
def changed(kw,name,raw):
 kw['buffers'][name]=raw;kw['hashes'][name]=hashlib.sha256(raw).hexdigest()
'''


class SuccessorSourceTests(unittest.TestCase):
    def child(self, code):
        bindings = 'SOURCE='+repr(str(SOURCE))+'\nROOT='+repr(str(ROOT))+'\nPIN='+repr(hashlib.sha256(SOURCE.read_bytes()).hexdigest())+'\n'
        result = subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',bindings+PREFIX+code],
                                capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8','replace'))
        self.assertEqual(result.stdout, b'')

    def test_real_child_graph_loads_exact_five_without_invented(self):
        self.child("o=make(real=True);p=o.load();o.intact();assert len(o.modules)==5\n"
                   "assert p.dependency_controller.execution is p.dependency_execution\n"
                   "assert p.dependency_execution.producer is p.dependency_producer\n"
                   "assert not any(n=='tools' or n.startswith('tools.') for n in sys.modules)\n"
                   "assert 'dependency_invented' not in o.modules;o.close()\n")

    def test_real_parent_graph_uses_no_aliases_or_controller(self):
        self.child("before=dict(sys.modules);o=make('parent',True);p=o.load();o.intact()\n"
                   "assert len(o.modules)==5 and not o.owned\n"
                   "assert 'dependency_controller' not in o.modules\n"
                   "assert p.dependency_parent.execution is p.dependency_execution\n"
                   "assert all(sys.modules.get(n) is m for n,m in before.items());o.close()\n")

    def test_parent_existing_tools_remains_untouched(self):
        self.child("foreign=types.ModuleType('tools');sys.modules['tools']=foreign\n"
                   "o=make('parent');p=o.load();assert p.dependency_execution.lazy() is p.dependency_producer\n"
                   "assert sys.modules['tools'] is foreign;o.close()\n")

    def test_child_existing_tools_refused_preserved_and_closed(self):
        self.child("m=types.ModuleType('tools');sys.modules['tools']=m;o=make()\n"
                   "refuse(o.load,'helper_preloaded');assert o.closed;assert sys.modules['tools'] is m\n")

    def test_foreign_neutral_alias_is_not_removed(self):
        self.child("a=s.NAMESPACE+'.other';m=types.ModuleType(a);sys.modules[a]=m;o=make()\n"
                   "refuse(o.load,'helper_preloaded');assert sys.modules[a] is m\n")

    def test_invented_extra_role_and_wrong_graph_refused_before_load(self):
        self.child("b,k=owner();b['dependency_invented']=b'x=1';k['origins']['dependency_invented']=SOURCE;k['hashes']['dependency_invented']='0'*64\n"
                   "refuse(lambda:s.HelperSources(**k),'helper_roster')\n"
                   "b,k=owner();k['mode']='parent';refuse(lambda:s.HelperSources(**k),'helper_roster')\n")

    def test_missing_role_refused(self):
        self.child("b,k=owner();b.pop('dependency_controller');refuse(lambda:s.HelperSources(**k),'helper_roster')\n")

    def test_bad_hash_origin_and_source_bound_refused(self):
        self.child("b,k=owner();k['hashes']['dependency_controller']='0'*64;refuse(lambda:s.HelperSources(**k),'helper_hash')\n"
                   "b,k=owner();k['origins']['dependency_controller']='relative.py';refuse(lambda:s.HelperSources(**k),'helper_origin')\n"
                   "b,k=owner();b['dependency_controller']=b'';refuse(lambda:s.HelperSources(**k),'helper_bound')\n")

    def test_complete_compilation_before_execution(self):
        self.child("b,k=owner();changed(k,'dependency_evidence',b'raise AssertionError(\"must not execute\")');changed(k,'dependency_controller',b'if:')\n"
                   "try:s.HelperSources(**k)\nexcept SyntaxError:pass\nelse:raise AssertionError()\n"
                   "assert s.NAMESPACE not in sys.modules\n")

    def test_import_of_missing_role_direct_tools_and_subpackage_refused(self):
        self.child("for raw in (b'from tools import dependency_invented',b'import tools',b'from tools.other import x'):\n"
                   " b,k=owner();changed(k,'dependency_controller',raw);refuse(lambda:s.HelperSources(**k),'helper_import')\n")

    def test_forward_import_refused_and_partial_graph_closed(self):
        self.child("b,k=owner();changed(k,'dependency_evidence',b'from tools import dependency_controller');o=s.HelperSources(**k)\n"
                   "refuse(o.load,'helper_import');assert o.closed;assert s.NAMESPACE not in sys.modules\n")

    def test_lazy_import_uses_same_objects_with_later_foreign_tools(self):
        self.child("o=make();p=o.load();m=types.ModuleType('tools');sys.modules['tools']=m\n"
                   "assert p.dependency_execution.lazy() is p.dependency_producer;o.close();assert sys.modules['tools'] is m\n")

    def test_foreign_replacement_survives_close_other_aliases_released(self):
        self.child("o=make();o.load();a=s.NAMESPACE+'.dependency_producer';m=types.ModuleType(a);sys.modules[a]=m\n"
                   "refuse(o.close,'helper_cleanup_ownership');assert sys.modules[a] is m\n"
                   "assert all(n==a for n in sys.modules if n.startswith(s.NAMESPACE));refuse(o.close,'helper_reclose')\n")

    def test_lazy_import_loss_is_sticky(self):
        self.child("o=make();p=o.load();a=s.NAMESPACE+'.dependency_producer';m=sys.modules.pop(a)\n"
                   "refuse(p.dependency_execution.lazy,'helper_alias_ownership');sys.modules[a]=m\n"
                   "refuse(p.dependency_execution.lazy,'helper_inactive');o.close()\n")

    def test_parent_global_mutation_refused(self):
        self.child("o=make('parent');p=o.load();p.dependency_producer.core=None\n"
                   "refuse(o.intact,'helper_global_ownership');o.close()\n")

    def test_callback_after_close_and_reentry_refused(self):
        self.child("o=make();p=o.load();refuse(o.load,'helper_reentry');o.close()\n"
                   "refuse(p.dependency_execution.lazy,'helper_inactive');refuse(o.close,'helper_reclose')\n")

    def test_module_execution_interrupt_closes_graph(self):
        self.child("b,k=owner();changed(k,'dependency_controller',b'raise KeyboardInterrupt()');o=s.HelperSources(**k)\n"
                   "try:o.load()\nexcept KeyboardInterrupt:pass\nelse:raise AssertionError()\n"
                   "assert o.closed;assert not any(n.startswith(s.NAMESPACE) for n in sys.modules)\n")

    def test_replaced_compiled_code_refuses_before_any_execution(self):
        self.child("o=make();o.compiled['dependency_evidence']=compile('raise AssertionError(\"must not execute\")',SOURCE,'exec')\n"
                   "refuse(o.load,'helper_policy_changed');assert o.closed;assert not o.modules\n")

    def test_rebound_buffer_hash_policy_refuses_before_load(self):
        self.child("o=make();o.buffers['dependency_controller']=b'raise AssertionError()'\n"
                   "o.source_hashes=tuple((n,hashlib.sha256(o.buffers[n]).hexdigest()) for n in o.order)\n"
                   "refuse(o.load,'helper_policy_changed');assert o.closed;assert not o.modules\n")

    def test_changed_mode_order_and_origin_refuse_before_load(self):
        self.child("for field,value in (('mode','parent'),('order',tuple(reversed(s.CHILD_ORDER))),('origins',{})):\n"
                   " o=make();setattr(o,field,value);refuse(o.load,'helper_policy_changed');assert o.closed;assert not o.modules\n")

    def test_post_load_buffer_and_compiled_mutations_refuse(self):
        self.child("o=make();o.load();o.buffers['dependency_controller']=b'changed';refuse(o.intact,'helper_buffer_changed');o.close()\n"
                   "o=make();o.load();o.compiled['dependency_controller']=compile('pass',SOURCE,'exec');refuse(o.intact,'helper_policy_changed');o.close()\n")

    def test_parent_verification_failure_preserves_primary(self):
        self.child("b,k=owner('parent');changed(k,'dependency_parent',b'def validate_saved_controller(**kw):\\n raise KeyboardInterrupt(\"primary\")');o=s.HelperSources(**k);o.load()\n"
                   "try:o.verify()\nexcept KeyboardInterrupt as e:assert str(e)=='primary'\nelse:raise AssertionError()\n"
                   "o.intact();o.close()\n")


if __name__ == '__main__':
    unittest.main()
