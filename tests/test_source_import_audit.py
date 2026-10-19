"""Invented source buffers only; AST parsing never imports supplied code."""
import copy
import hashlib
import sys
import unittest
from unittest.mock import patch

from tools import source_import_audit as subject


def invoke(buffers=None, **kwargs):
    buffers = {'owned.entry':b'from owned import helper as h\nimport json\nh.f()\n',
        'owned.helper':b'def f():\n return 1\n'} if buffers is None else buffers
    args=dict(roots=('owned.entry',),expected_hashes={n:hashlib.sha256(v).hexdigest() for n,v in buffers.items()},
        stdlib_roots=frozenset(('json','sys')),namespace_packages=('owned',))
    args.update(kwargs)
    return subject.audit_imports(buffers,**args)


class ImportAuditTests(unittest.TestCase):
    def test_static_dag_and_authority_boundary(self):
        r=invoke();self.assertEqual(r['dependency_order'],['owned.helper','owned.entry'])
        self.assertEqual(r['authored_edges']['owned.entry'],['owned.helper'])
        self.assertEqual(r['external_imports'][0]['module'],'json')
        self.assertTrue(r['complete_static_import_roster'])
        for key in ('execution_closure_verified','source_origin_authenticated','namespace_origin_authenticated',
            'external_import_closure_verified','interpreter_startup_verified','validator_execution_owned',
            'execution_authorized','actual_inputs_accessed','feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(r[key],False)

    def test_missing_import_and_unknown_external_refuse(self):
        for raw in (b'from owned import absent',b'import unlisted'):
            with self.subTest(raw=raw),self.assertRaisesRegex(ValueError,'unresolved_import'):
                invoke({'owned.entry':raw})

    def test_conditional_and_nested_imports_still_included(self):
        r=invoke({'owned.entry':b'if False:\n import json\ndef f():\n import sys\n'})
        self.assertEqual({v['module'] for v in r['external_imports']},{'json','sys'})

    def test_source_bytes_do_not_execute(self):
        before=dict(sys.modules)
        with patch('builtins.exec',side_effect=AssertionError('execution forbidden')):
            r=invoke({'owned.entry':b'raise RuntimeError("must not run")\nimport json\n'})
        self.assertTrue(all(sys.modules[n] is v for n,v in before.items()));self.assertFalse(r['execution_authorized'])

    def test_hash_mismatch_refuses_before_parsing(self):
        with patch.object(subject.ast,'parse',side_effect=AssertionError('must not parse')):
            with self.assertRaisesRegex(ValueError,'source_hash'):
                invoke({'owned.entry':b'!'},expected_hashes={'owned.entry':'0'*64})

    def test_exact_hash_roster(self):
        for hashes in ({},{'owned.entry':'0'*64,'extra':'0'*64}):
            with self.subTest(hashes=hashes),self.assertRaisesRegex(ValueError,'hash_roster'):
                invoke({'owned.entry':b'pass'},expected_hashes=hashes)

    def test_relative_star_and_bare_namespace_refuse(self):
        for raw,code in ((b'from . import helper','relative_import'),(b'from json import *','star_import'),
            (b'import owned','bare_namespace_import')):
            with self.subTest(raw=raw),self.assertRaisesRegex(ValueError,code):invoke({'owned.entry':raw})

    def test_module_alias_and_stdlib_shadow_refuse(self):
        for buffers,code in (({'owned.entry':b'pass','Owned.Entry':b'pass'},'module_alias'),
            ({'json':b'pass'},'namespace_parents')):
            with self.subTest(code=code),self.assertRaisesRegex(ValueError,code):invoke(buffers)

    def test_cycle_refuses(self):
        with self.assertRaisesRegex(ValueError,'import_cycle'):
            invoke({'owned.entry':b'from owned import helper','owned.helper':b'from owned import entry'})

    def test_unreachable_supplied_source_refuses(self):
        with self.assertRaisesRegex(ValueError,'unreachable_source'):
            invoke({'owned.entry':b'pass','owned.extra':b'pass'})

    def test_dynamic_calls_are_inventory_only_including_alias_use(self):
        r=invoke({'owned.entry':b'f=exec\nf("import missing")\ngetattr(obj,"load")()\n'})
        self.assertEqual([v['expression'] for v in r['syntactic_calls']],['f','getattr(obj, \'load\')','getattr'])
        self.assertFalse(r['dynamic_alias_dataflow_analyzed']);self.assertFalse(r['embedded_code_strings_analyzed'])
        self.assertFalse(r['execution_closure_verified'])

    def test_decorators_and_class_bases_calls_inventory(self):
        r=invoke({'owned.entry':b'@decorate()\nclass C(base()):\n pass\n'})
        self.assertEqual({v['expression'] for v in r['syntactic_calls']},{'decorate','base'})

    def test_bounds_and_syntax(self):
        for raw,code in ((b'','source_bound'),(b'x'*(subject.MAX_SOURCE+1),'source_bound'),
            (b'if','source_syntax')):
            with self.subTest(code=code),self.assertRaisesRegex(ValueError,code):invoke({'owned.entry':raw})
        with patch.object(subject,'MAX_TOTAL',1):
            with self.assertRaisesRegex(ValueError,'source_total_bound'):invoke({'owned.entry':b'pass'})
        with patch.object(subject,'MAX_NODES',1):
            with self.assertRaisesRegex(ValueError,'source_node_bound'):invoke({'owned.entry':b'pass'})

    def test_inputs_unchanged(self):
        buffers={'owned.entry':b'import json'};before=copy.deepcopy(buffers);invoke(buffers);self.assertEqual(buffers,before)

    def test_root_and_namespace_rosters(self):
        for key,value in (('roots',()),('roots',('absent',)),('roots',('owned.entry','owned.entry')),
            ('namespace_packages',('owned','owned')),('namespace_packages',('bad/path',))):
            with self.subTest(key=key,value=value),self.assertRaises(ValueError):invoke({'owned.entry':b'pass'},**{key:value})

    def test_runtime_refuses(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):subject.run_runtime()

    def test_authored_from_leaf_symbol_import_is_ambiguous(self):
        with self.assertRaisesRegex(ValueError,'authored_symbol_import'):
            invoke({'owned.entry':b'from owned.helper import f','owned.helper':b'def f(): pass'})

    def test_missing_namespace_and_leaf_package_overlap_refuse(self):
        with self.assertRaisesRegex(ValueError,'namespace_parents'):invoke(namespace_packages=())
        with self.assertRaisesRegex(ValueError,'namespace_parents'):
            invoke({'owned.entry':b'pass','owned.entry.child':b'pass'})

    def test_stdlib_shadow_explicit_and_nonstring_rosters(self):
        with self.assertRaisesRegex(ValueError,'stdlib_shadow'):
            invoke({'json':b'pass'},roots=('json',),namespace_packages=())
        for key,value in (('roots',([],)),('namespace_packages',([],))):
            with self.subTest(key=key),self.assertRaises(ValueError):invoke(**{key:value})
