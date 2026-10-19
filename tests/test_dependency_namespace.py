"""Fresh-process qualification; never conceal preloaded tools modules."""
import hashlib
from pathlib import Path
import subprocess
import sys
import unittest


SOURCE = Path(__file__).resolve().parents[1]/'tools/dependency_namespace.py'
PREFIX = '''
import hashlib,pathlib,sys,types
raw=pathlib.Path(SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN
subject=types.ModuleType('namespace_subject');exec(compile(raw,SOURCE,'exec'),subject.__dict__)
buffers={name:b'x=1\\n' for name in subject.ORDER}
buffers['dependency_producer']=b'from tools import dependency_evidence as core\\n'
buffers['dependency_execution']=b'def lazy():\\n from tools import dependency_producer as producer\\n return producer\\n'
def owner():
 return subject.ClosedSources(buffers=buffers,origins={n:SOURCE for n in buffers},hashes={n:hashlib.sha256(v).hexdigest() for n,v in buffers.items()})
def refuse(fn,code):
 try:fn()
 except ValueError as e:assert str(e)==code,(str(e),code)
 else:raise AssertionError('expected refusal: '+code)
'''


class NamespaceTests(unittest.TestCase):
    def child(self, code):
        prefix = 'SOURCE='+repr(str(SOURCE))+'\nPIN='+repr(hashlib.sha256(SOURCE.read_bytes()).hexdigest())+'\n'
        result = subprocess.run([sys.executable, '-I', '-S', '-B', '-X', 'utf8', '-c', prefix+PREFIX+code],
                                capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8', 'replace'))
        self.assertEqual(result.stdout, b'')

    def test_shared_instances_and_lazy_import_with_role_owned_tools(self):
        self.child("o=owner();p=o.load();assert p.dependency_producer.core is p.dependency_evidence\n"
                   "foreign=types.ModuleType('tools');sys.modules['tools']=foreign\n"
                   "assert p.dependency_execution.lazy() is p.dependency_producer\n"
                   "assert o.close() is True;assert sys.modules['tools'] is foreign\n"
                   "assert not any(n.startswith(subject.NAMESPACE) for n in sys.modules)\n")

    def test_preexisting_tools_refused_without_removal(self):
        self.child("m=types.ModuleType('tools');sys.modules['tools']=m;o=owner()\n"
                   "refuse(o.load,'namespace_preloaded');assert sys.modules['tools'] is m\n")

    def test_preexisting_neutral_child_refused_without_removal(self):
        self.child("a=subject.NAMESPACE+'.foreign';m=types.ModuleType(a);sys.modules[a]=m;o=owner()\n"
                   "refuse(o.load,'namespace_preloaded');assert sys.modules[a] is m\n")

    def test_hash_failure_before_any_module_execution(self):
        self.child("kw=dict(buffers=buffers,origins={n:SOURCE for n in buffers},hashes={n:'0'*64 for n in buffers})\n"
                   "refuse(lambda:subject.ClosedSources(**kw),'source_hash')\n"
                   "assert subject.NAMESPACE not in sys.modules\n")

    def test_unknown_tools_member_refused_before_any_execution(self):
        self.child("buffers['dependency_controller']=b'from tools import missing\\n'\n"
                   "refuse(owner,'authored_import');assert subject.NAMESPACE not in sys.modules\n")

    def test_direct_tools_import_refused_before_execution(self):
        self.child("buffers['dependency_controller']=b'import tools.dependency_producer\\n'\n"
                   "refuse(owner,'authored_import')\n")

    def test_tools_subpackage_from_import_refused_before_execution(self):
        self.child("buffers['dependency_controller']=b'from tools.other import missing\\n'\n"
                   "refuse(owner,'authored_import')\n")

    def test_forward_member_import_is_not_filled_from_disk(self):
        self.child("buffers['dependency_evidence']=b'from tools import dependency_controller\\n'\n"
                   "o=owner();refuse(o.load,'authored_import');assert o.closed\n"
                   "assert not any(n.startswith(subject.NAMESPACE) for n in sys.modules)\n")

    def test_partial_execution_interrupt_releases_all_owned_aliases(self):
        self.child("buffers['dependency_controller']=b'raise KeyboardInterrupt(\"invented\")\\n'\n"
                   "o=owner()\ntry:o.load()\nexcept KeyboardInterrupt:pass\nelse:raise AssertionError()\n"
                   "assert o.closed;assert not any(n.startswith(subject.NAMESPACE) for n in sys.modules)\n")

    def test_foreign_replacement_preserved_and_other_aliases_released(self):
        self.child("o=owner();o.load();a=subject.NAMESPACE+'.dependency_producer';m=types.ModuleType(a);sys.modules[a]=m\n"
                   "refuse(o.close,'namespace_cleanup_ownership');assert sys.modules[a] is m\n"
                   "assert all(n==a for n in sys.modules if n.startswith(subject.NAMESPACE))\n"
                   "refuse(o.close,'namespace_reclose')\n")

    def test_missing_alias_blocks_lazy_import_and_failure_is_sticky(self):
        self.child("o=owner();p=o.load();a=subject.NAMESPACE+'.dependency_producer';m=sys.modules.pop(a)\n"
                   "refuse(p.dependency_execution.lazy,'namespace_ownership');sys.modules[a]=m\n"
                   "refuse(p.dependency_execution.lazy,'namespace_inactive');o.close()\n")

    def test_package_attribute_substitution_blocks_lazy_import(self):
        self.child("o=owner();p=o.load();p.dependency_producer=None\n"
                   "refuse(p.dependency_execution.lazy,'namespace_attribute');o.close()\n")

    def test_dynamic_unknown_tools_import_never_falls_back(self):
        self.child("o=owner();o.load()\n"
                   "refuse(lambda:o.import_authored('tools',fromlist=('missing',)),'authored_import');o.close()\n")

    def test_source_map_is_detached_before_external_mutation(self):
        self.child("o=owner();buffers['dependency_evidence']=b'raise RuntimeError()';p=o.load()\n"
                   "assert p.dependency_evidence.x==1;o.close()\n")

    def test_missing_source_roster_not_accepted(self):
        self.child("buffers.pop('dependency_controller');refuse(owner,'source_roster')\n")

    def test_execution_and_close_are_single_attempts(self):
        self.child("o=owner();o.load();refuse(o.load,'namespace_reentry');o.close();refuse(o.close,'namespace_reclose')\n")

    def test_cleanup_interruption_does_not_abandon_other_owned_aliases(self):
        self.child("o=owner();o.load();a=subject.NAMESPACE+'.dependency_controller';original=sys.modules\n"
                   "class InterruptOnce(dict):\n def __delitem__(self,k):\n  if k==a:raise KeyboardInterrupt('invented close')\n  return super().__delitem__(k)\n"
                   "sys.modules=InterruptOnce(original)\n"
                   "try:\n try:o.close()\n except KeyboardInterrupt:pass\n else:raise AssertionError()\n"
                   " assert all(n==a for n in sys.modules if n.startswith(subject.NAMESPACE))\n"
                   " refuse(o.close,'namespace_reclose')\nfinally:sys.modules=original\n")

    def test_package_registration_interruption_closes_partial_owner(self):
        self.child("o=owner();original=sys.modules\n"
                   "class InterruptRegistration(dict):\n def __setitem__(self,k,v):\n  super().__setitem__(k,v)\n  if k==subject.NAMESPACE:raise KeyboardInterrupt('invented registration')\n"
                   "sys.modules=InterruptRegistration(original)\n"
                   "try:\n try:o.load()\n except KeyboardInterrupt:pass\n else:raise AssertionError()\n"
                   " assert o.closed;assert subject.NAMESPACE not in sys.modules\nfinally:sys.modules=original\n")


if __name__ == '__main__':
    unittest.main()
