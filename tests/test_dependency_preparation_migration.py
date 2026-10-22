"""Real preparation/gate/metadata/materializer with wholly invented bootstraps."""
import ast
import base64
import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from tools import dependency_operational_metadata as m
from tools import dependency_operational_sources as sources
from tools import dependency_host_entry as host
from tools import dependency_historical_gate as gate
import test_dependency_operational_preparation as preparation_tests
from test_dependency_historical_outer import fixture
from test_dependency_historical_gate import fixtures
from test_dependency_producer import refresh

FACTORY = b'''import sys, importlib.util
class AuthoredSources:
 def __init__(self,adapter):self.rows={}
 def add(self,name,path,raw):self.rows[name]=(path,raw)
 def find_spec(self,name,path=None,target=None):
  return importlib.util.spec_from_loader(name,self) if name in self.rows else None
 def create_module(self,spec):return None
 def exec_module(self,module):
  path,raw=self.rows[module.__name__];exec(compile(raw,str(path),'exec'),vars(module))
 def close(self):
  if self in sys.meta_path:sys.meta_path.remove(self)
  for name in self.rows:sys.modules.pop(name,None)
  return True
class ScopedCallbacks:
 def __init__(self,**kw):self.close_attempts=0
 def __call__(self,*a,**kw):raise AssertionError('invented callbacks never observe')
 def close(self):self.close_attempts+=1;return True
'''


class MigrationPreparation(unittest.TestCase):
    def setUp(self):
        seed=preparation_tests.PreparationTests('test_owned_graph_and_pending_preflight_recompute_from_originals')
        seed.setUp();self.addCleanup(seed.doCleanups)
        seed.prep.close();seed.owner.close()
        root=getattr(self,'fixture_root',Path.cwd())
        a=fixture(root)
        f=fixtures.Fixture.__new__(fixtures.Fixture)
        f.root=root
        f.p={n:(raw if n=='q_snapshot_log' else json.loads(raw)) for n,raw in a['legacy_documents']['inputs'].items()}
        for attr,role in (('c','candidate'),('d','decision'),('r','review'),('s','seal')):
            setattr(f,attr,json.loads(a['legacy_documents'][role]))
        p=f.p
        for value in (f.c,f.d,f.r,f.s,p['activity_scope']):
            value['operation_id']=seed.case.request['operation_id']
        p['binding_plan']=dict(load_order=p['binding_schema']['load_order'],
            protected_order=p['binding_schema']['protected_order'],dependency={},
            execution_authorized=False,actual_binding_ready=False)
        replacements={
            'role:gdt_preflight':b'def freeze_basis(**kw):return None\n',
            'bootstrap:activation_binding':('def prepare_bindings(**kw):return '+repr(p['binding_plan'])+'\n').encode(),
            'bootstrap:io_entry':getattr(self,'fixture_control',b'# invented control; no device or observer\n'),
            'integration:prospective_child':getattr(self,'fixture_factory',FACTORY),
        }
        for key,raw in replacements.items():
            row=p['source_cache']['sources'][key]
            row.update(bytes=len(raw),sha256=m.sha(raw),base64=base64.b64encode(raw).decode())
            receipt=p['source_receipts']['receipts'][key]
            receipt.update(bytes=len(raw),sha256=m.sha(raw))
            for field in ('lstat_before','lstat_after','fstat_before','fstat_after'):
                receipt[field]['st_size']=len(raw)
            if key.startswith('role:'):p['role_authority']['roles'][key[5:]]['sha256']=m.sha(raw)
        tree=ast.parse(a['capture_buffers']['retained_gate'])
        constants={n.targets[0].id:ast.literal_eval(n.value) for n in tree.body
            if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)
            and n.targets[0].id in ('SOURCE_ANCESTRY','REQUIRED_REPAIR_SOURCE_PINS')}
        policy=constants['SOURCE_ANCESTRY'];repair=constants['REQUIRED_REPAIR_SOURCE_PINS']
        for key,row in policy['rows'].items():
            now=p['source_cache']['sources'][key]['sha256'];row['current_sha256']=now
            if key in p['repair_overlay']['repairs']:
                p['repair_overlay']['repairs'][key]['new_sha256']=now
                repair[gate.REPAIR_SOURCE_NAMES[key]]=now
            else:
                row['historical_sha256']=now
                for name in ('q_old_result','q_old_seal','q_old_review'):
                    p[name]['sources_sha256'][row['historical_key']]=now
        p['q_repair_result']['source_sha256']=repair
        p['q_repair_review']['source_sha256']=repair
        p['prerequisites']['qualified_roles']=p['role_authority']['roles']
        p['prerequisites']['binding_input']['roles']=p['role_authority']['roles']
        factory=p['factory_evidence'];factory['new_factory_sha256']=m.sha(replacements['integration:prospective_child'])
        for group in ('contract','composition'):
            factory[group]['source_sha256']['prospective_child.py']=m.sha(replacements['integration:prospective_child'])
        factory['composition']['source_sha256']['roles/gdt_preflight.py']=m.sha(replacements['role:gdt_preflight'])
        factory['composition']['source_sha256']['io_entry.py']=m.sha(replacements['bootstrap:io_entry'])
        docs,seal=f.pack()
        policy['historical_seal_sha256']=m.sha(docs['inputs']['q_old_seal'])
        policy['historical_seal_canonical_sha256']=m.sha(m.encoded(p['q_old_seal']))
        proof=m.encoded(policy);constants['SOURCE_ANCESTRY_SHA256']=m.sha(proof)
        for node in tree.body:
            if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name):
                name=node.targets[0].id
                if name in constants:node.value=ast.parse(repr(constants[name]),mode='eval').body
        texts=dict(seed.texts,retained_gate=(ast.unparse(tree)+'\n').encode())
        raw_sources={k:base64.b64decode(v['base64']) for k,v in p['source_cache']['sources'].items()}
        registry={v['path']:raw_sources[k] for k,v in p['source_cache']['sources'].items()}
        texts['ordinary_io']=('DATA='+repr(registry)+'''\ndef read(path,*,expected_sha256,expected_bytes):
 raw=DATA[str(path)]
 assert len(raw)==expected_bytes
 return raw,{'invented':True}
def read_ordinary(*a,**kw):raise AssertionError('invented ordinary callback forbidden')
''').encode()
        self.owner=sources.OuterSources(buffers=texts,hashes={n:m.sha(b) for n,b in texts.items()}).load()
        self.addCleanup(lambda:None if self.owner.closed else self.owner.close())
        case=seed.case
        if hasattr(self,'fixture_root'):
            case.request['folder']=str(root/'command'/'composition')
        for role,row in case.request['sources'].items():
            if role.startswith('bound.'):
                key=role[6:];raw=raw_sources[key];row.update(path=Path(p['source_cache']['sources'][key]['path']).relative_to(root).as_posix())
                case.buffers[role]=raw;row.update(bytes=len(raw),sha256=m.sha(raw))
        for name,role in (('dependency_successor_wiring','successor_wiring'),
                          ('dependency_successor_sources','namespace'),('ordinary_io','ordinary_io'),
                          ('parent_verifier','dependency.dependency_parent')):
            case.buffers[role]=texts[name]
            case.request['sources'][role].update(bytes=len(texts[name]),sha256=m.sha(texts[name]))
        case.data['source_buffers']['closure_manifest']=m.encoded(case.request['sources'])
        case.data['expectation']['source_sha256']={n:m.sha(b) for n,b in case.data['source_buffers'].items()}
        refresh(case.data)
        case.request['dependency_packet']['inputs']={n:v for n,v in case.data.items() if n!='source_buffers'}
        case.request['dependency_fixed']['expectation_sha256']=m.sha(m.encoded(case.data['expectation']))
        ordinary,originals=preparation_tests.build_records(case.request,case.buffers,docs,self.owner.receipts())
        context=json.loads(a['historical_migration']['context_bytes'])
        context.update(dependency_config_sha256=m.sha(docs['inputs']['dependency_config']),
            historical_seal_sha256=m.sha(docs['inputs']['q_old_seal']),ancestry_proof_sha256=m.sha(proof))
        raw=m.encoded(context)
        self.migration=dict(context_bytes=raw,expected_context_sha256=m.sha(raw),
                            ancestry_proof_bytes=proof,expected_ancestry_proof_sha256=m.sha(proof))
        cls=self.owner.modules['dependency_operational_preparation'].Preparation
        self.prep=cls(source_owner=self.owner,adapter_owner=case.owner,
            request_bytes=m.encoded(case.request),request_sha256=m.sha(m.encoded(case.request)),
            checked_sources=case.buffers,documents=docs,original_receipts=originals,
            ordinary=ordinary,ordinary_receipts=m.receipts(ordinary),legacy_seal_sha256=seal,
            reference_pins=f.reference_pins(docs),prepared_repository_root=str(root),
            historical_migration=self.migration)
        self.addCleanup(lambda:None if self.prep.closed else self.prep.close())

    def test_real_gate_metadata_refresh_and_materializer_complete(self):
        before=set(sys.modules)
        with patch('builtins.open',side_effect=AssertionError('no file opens')), \
             patch.object(Path,'open',side_effect=AssertionError('no file opens')), \
             patch('ctypes.CDLL',side_effect=AssertionError('no native')):
            modules,aux,lease=self.prep.prepare()
        self.assertEqual(set(modules),{'binding','control','factory'})
        self.assertIsNone(aux)
        self.assertEqual(self.prep.preflight['schema'],'pending_operational_preflight_v2')
        self.assertFalse(self.prep.preflight['execution_bootstrap_qualified'])
        for flag in m.FLAGS:self.assertIs(self.prep.preflight[flag],False)
        raw=m.encoded(self.prep.preflight)
        self.assertTrue(self.owner.modules['dependency_operational_preparation'].verify_saved_preflight(
            source_owner=self.owner,raw=raw,expected_sha256=m.sha(raw),arguments=self.prep.arguments(self.prep.validated)))
        callbacks=lease.value
        self.prep.close();self.assertEqual(callbacks.close_attempts,1)
        self.assertFalse(any(n in sys.modules for n in ('_successor_binding','_successor_control','_successor_factory','gdt_preflight')))
        self.owner.intact()

    def test_request_hash_refuses_before_gate(self):
        self.prep.request_sha256='0'*64
        with self.assertRaisesRegex(ValueError,'operational_original_request'):self.prep.prepare()

    def test_caller_container_is_detached(self):
        self.migration['expected_context_sha256']='0'*64
        self.assertNotEqual(self.migration,self.prep.historical_migration)
        self.prep.prepare()

    def test_migration_mutation_refuses_before_refresh(self):
        self.prep.historical_migration['context_bytes']+=b' '
        with self.assertRaisesRegex(ValueError,'migration_anchor'):self.prep.prepare()
        self.assertFalse(self.prep.bootstrap_modules)

    def test_legacy_gate_route_keeps_cross_operation_refusal(self):
        self.prep.historical_migration=None
        with self.assertRaisesRegex(ValueError,'operation_binding'):self.prep.prepare()

    def test_consistency_result_cannot_build_execution_context(self):
        validated=self.prep._validate_gate()
        with self.assertRaisesRegex(ValueError,'separate_execution_qualification'):
            host.make_context(validated)

    def test_saved_migration_receipts_and_false_claims_recomputed(self):
        self.prep.prepare();arguments=self.prep.arguments(self.prep.validated)
        result=copy.deepcopy(self.prep.preflight)
        result['historical_migration']['context']['sha256']='0'*64
        raw=m.encoded(result)
        with self.assertRaisesRegex(ValueError,'saved_preflight'):
            m.verify_saved(raw=raw,expected_sha256=m.sha(raw),**arguments)
        bad=copy.deepcopy(self.prep.validated);bad['execution_authorized']=True
        with self.assertRaisesRegex(ValueError,'migration_result'):
            m.validate_pending(**self.prep.arguments(bad))

    def test_omitting_context_cannot_downgrade_v6_saved_preflight(self):
        self.prep.prepare();args=self.prep.arguments(self.prep.validated)
        args.pop('historical_migration')
        with self.assertRaisesRegex(ValueError,'migration_required'):m.validate_pending(**args)

    def test_rehashed_context_still_binds_original_config_and_root(self):
        self.prep.prepare()
        for field,value in (('dependency_config_sha256','0'*64),('operation_id','5'*32),
                            ('repository_root',str(Path.cwd()/'wrong'))):
            args=self.prep.arguments(copy.deepcopy(self.prep.validated))
            migration=dict(args['historical_migration']);context=json.loads(migration['context_bytes'])
            context[field]=value;raw=m.encoded(context)
            migration.update(context_bytes=raw,expected_context_sha256=m.sha(raw))
            args['historical_migration']=migration
            args['validated'].update(historical_context_sha256=m.sha(raw),historical_operation_id=context['operation_id'])
            with self.subTest(field=field),self.assertRaisesRegex(ValueError,'migration_context'):
                m.validate_pending(**args)

    def test_public_runtime_remains_disabled(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):
            self.owner.modules['dependency_operational_preparation'].run_runtime()


if __name__=='__main__':unittest.main(verbosity=2)
