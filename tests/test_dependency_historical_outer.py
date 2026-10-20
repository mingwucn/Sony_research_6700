"""Full captured preflight with a real v6 gate and invented complete records.

Only test policy constants are replaced inside captured authored validator text.
No accepted real records, firmware inputs or dependency runtime are involved.
"""
import ast
import base64
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import dependency_historical_gate as gate
from tools import dependency_observation_outer as outer
from tools import dependency_observation_contract as c
from test_dependency_historical_gate import fixtures, fixture_repair
from test_dependency_observation_outer import fixture as outer_fixture
from test_dependency_observation_contract import change, decided, reseal
from test_dependency_producer import refresh


def fixture(root):
    a = outer_fixture()
    proposal = a['proposal_arguments']
    f = fixtures.Fixture(root, role_names=outer.RETAINED)
    p = f.p
    p['dependency_config']['operation_id'] = '3'*32
    p['source_manifest'].update(bytes=1024017848, sha256='a'*64)
    p['basis']['prior_stream'].update(input_package_bytes=1024017848, input_package_sha256='a'*64)
    p['prerequisites']['constants_sha256'] = 'c'*64
    rows = {}
    for key, row in p['source_cache']['sources'].items():
        if not key.startswith(('role:', 'bootstrap:')):
            continue
        old = Path(row['path']).relative_to(f.root/f.c['legacy_session']).as_posix()
        current = f.c['legacy_session']+'/activation/'+old
        row['path'] = str(f.root/current)
        p['source_receipts']['receipts'][key]['path'] = row['path']
        if key.startswith('role:'):
            p['role_authority']['roles'][key[5:]]['path'] = current
        if key in p['repair_overlay']['repairs']:
            p['repair_overlay']['repairs'][key]['path'] = current
        rows[key] = dict(current_path=current, historical_key=old,
            historical_sha256=p['q_old_seal']['sources_sha256'][old], current_sha256=row['sha256'])
    documents, seal = f.pack()
    policy = dict(schema='gdt_explicit_source_ancestry_v1',legacy_session=f.c['legacy_session'],
        historical_seal_sha256=gate.sha(documents['inputs']['q_old_seal']),
        historical_seal_canonical_sha256=gate.sha(gate.encoded(p['q_old_seal'])),
        rows=rows,execution_authorized=False,camera_commands=[])
    proof = gate.encoded(policy)
    constants = dict(SOURCE_ANCESTRY=policy, SOURCE_ANCESTRY_SHA256=gate.sha(proof),
                     REQUIRED_REPAIR_SOURCE_PINS=fixture_repair)
    tree = ast.parse(Path('tools/dependency_historical_gate.py').read_bytes())
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            name=node.targets[0].id
            if name in constants:
                node.value=ast.parse(repr(constants[name]),mode='eval').body
    source = (ast.unparse(tree)+'\n').encode()
    sources = proposal['source_buffers']
    sources['retained_gate'] = source
    for role in sources:
        if role.startswith('bound.'):
            sources[role] = base64.b64decode(p['source_cache']['sources'][role[6:]]['base64'])
    originals = {n:documents['inputs'][n] for n in c.RETAINED}
    proposal['retained_comparison_buffers'] = originals
    proposal['ordinary_buffers'].update(originals)
    change(proposal,'historical_evidence_index',lambda v:v.update(
        original_comparison={n:c.receipt(b) for n,b in originals.items()}))
    manifest = json.loads(proposal['ordinary_buffers']['authored_source_manifest'])
    for role, raw in sources.items():
        manifest['sources'][role].update(c.receipt(raw))
    for role in manifest['prepared_sources']:
        manifest['prepared_sources'][role].update(c.receipt(sources[c.PREPARED_PROCESS_ROLES[role]]))
    proposal['ordinary_buffers']['authored_source_manifest']=c.encoded(manifest)
    change(proposal,'authored_source_receipts',lambda v:v.update(
        receipts={n:c.receipt(b) for n,b in sources.items()}))
    dep=json.loads(proposal['ordinary_buffers']['dependency_packet'])['inputs']
    dep['expectation']['source_sha256']={n:c.sha(c.encoded(manifest['prepared_sources'])
        if role=='closure_manifest' else sources[role]) for n,role in c.DEPENDENCY_SOURCE_ROLES.items()}
    refresh(dep)
    proposal['ordinary_buffers']['dependency_packet']=c.encoded(dict(schema='runtime_dependency_packet_v1',inputs=dep))
    change(proposal,'dependency_fixed',lambda v:v.update(expectation_sha256=c.sha(c.encoded(dep['expectation']))))
    reseal(proposal)
    a['runtime_expectation']=json.loads(proposal['proposal_bytes'])['runtime']
    a.update({n:v for n,v in decided(proposal).items() if n not in proposal})
    a['legacy_documents']=documents
    a['legacy_expected_seal_sha256']=seal
    a['legacy_reference_pins']=f.reference_pins(documents)
    a['capture_buffers']=dict(sources,**{'observation.contract':Path('tools/dependency_observation_contract.py').read_bytes(),
        'observation.outer':Path('tools/dependency_observation_outer.py').read_bytes()})
    a['expected_capture_hashes']={n:c.sha(b) for n,b in a['capture_buffers'].items()}
    context=c.encoded(dict(schema='gdt_historical_context_v1',repository_root=f.c['repository_root'],
        legacy_session=f.c['legacy_session'],operation_id='3'*32,
        dependency_config_sha256=c.sha(documents['inputs']['dependency_config']),
        historical_seal_sha256=c.sha(documents['inputs']['q_old_seal']),
        ancestry_proof_sha256=c.sha(proof),execution_authorized=False,camera_commands=[]))
    a['historical_migration']=dict(context_bytes=context,expected_context_sha256=c.sha(context),
        ancestry_proof_bytes=proof,expected_ancestry_proof_sha256=c.sha(proof))
    return a


class HistoricalOuter(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        self.a=fixture(Path(temp.name))

    def test_full_captured_gate_and_contract_with_distinct_operations(self):
        before=copy.deepcopy(self.a)
        with patch('builtins.open',side_effect=AssertionError('no opens')), \
             patch.object(Path,'open',side_effect=AssertionError('no opens')), \
             patch('subprocess.Popen',side_effect=AssertionError('no process')), \
             patch('ctypes.CDLL',side_effect=AssertionError('no native')):
            result=outer.preflight(**self.a)
        self.assertEqual(before,self.a)
        self.assertEqual(result['schema'],'disabled_observation_outer_preflight_v2')
        self.assertEqual(result['operation_id'],'1'*32)
        self.assertEqual(result['historical_operation_id'],'3'*32)
        for field in outer.FALSE:
            self.assertIs(result[field],False)
        raw=outer.encoded(result)
        self.assertTrue(outer.verify_saved(raw=raw,expected_sha256=c.sha(raw),**self.a))

    def test_pending_decision_refuses_before_gate(self):
        proposal=self.a['proposal_arguments']
        change(proposal,'activity_rights',lambda v:v['decisions']['constants_provenance'].update(
            disposition='pending',evidence=[]))
        reseal(proposal)
        self.a.update({n:v for n,v in decided(proposal).items() if n not in proposal})
        # Even a deliberately invalid migration must not be reached first.
        self.a['historical_migration']={}
        with self.assertRaisesRegex(ValueError,'undecided'):
            outer.preflight(**self.a)

    def test_legacy_route_still_refuses_cross_operation(self):
        self.a.pop('historical_migration')
        with self.assertRaisesRegex(ValueError,'operation_binding'):
            outer.preflight(**self.a)

    def test_closed_migration_envelope(self):
        self.a['historical_migration']['extra']=True
        with self.assertRaisesRegex(ValueError,'migration_shape'):
            outer.preflight(**self.a)

    def test_current_candidate_guard_remains(self):
        # All current v5 documents remain internally bound; expected outer act differs.
        migration=self.a['historical_migration']
        context=json.loads(migration['context_bytes']);context['operation_id']='1'*32
        migration['context_bytes']=c.encoded(context)
        migration['expected_context_sha256']=c.sha(migration['context_bytes'])
        with self.assertRaisesRegex(ValueError,'historical_operation_binding'):
            outer.preflight(**self.a)

    def test_saved_migration_claim_cannot_be_rehashed_into_success(self):
        result=outer.preflight(**self.a);result['historical_operation_id']='4'*32
        raw=outer.encoded(result)
        with self.assertRaisesRegex(ValueError,'saved_original'):
            outer.verify_saved(raw=raw,expected_sha256=c.sha(raw),**self.a)


if __name__=='__main__':unittest.main(verbosity=2)
