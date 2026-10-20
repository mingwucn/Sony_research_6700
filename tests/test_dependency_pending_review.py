"""Invented full review composition; historical semantic calls intercepted.

Actual saved metadata is exercised only by the separately reviewed private host
collector. No cache text, installed dependency or protected payload executes.
"""
import base64
import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from tools import dependency_pending_review as review
from tools import dependency_observation_contract as c
from tools import dependency_legacy_comparison as legacy
from test_dependency_observation_outer import fixture as outer_fixture
from test_dependency_observation_contract import reseal, change


def fixture():
    a=outer_fixture()['proposal_arguments'];sources=a['source_buffers']
    stub=b'''import json
BASIS_ROLES=frozenset(('prior_stream','prior_prefix','prior_directory','prior_member_identification','prior_selection','prior_measured','prior_accepted_inventory','lead_plan','prior_ext_superblock_observation'))
def parse(raw):return json.loads(raw)
def parent_evidence(p):return None
def _qualifications(p,raw):return None
'''
    sources['retained_gate']=stub
    names=[n.removeprefix('bound.role:') for n in sources if n.startswith('bound.role:')]
    roles={n:dict(path='private/invented/'+n+'.py') for n in names}
    old={n:dict(role=n) for n in legacy.HISTORICAL}
    old['role_authority']=dict(roles=roles)
    old['dependency_config']=dict(operation_id='3'*32,source_rows={'alias'+str(i):{} for i in range(11)},trusted_origins={'trusted'+str(i):dict(path='C:/invented/trusted'+str(i)+'.py') for i in range(4)})
    texts={n.removeprefix('bound.'):b for n,b in sources.items() if n.startswith('bound.')}
    texts.update({n:b'# invented, never execute\n' for n in ('bootstrap:activation_gate','integration:runtime_entry','integration:gdt_wiring')})
    texts.update({'dependency:'+n:b'# cached dependency never execute\n' for n in old['dependency_config']['source_rows']})
    texts.update({'trusted:'+n:b'# cached trusted never execute\n' for n in old['dependency_config']['trusted_origins']})
    rows={n:dict(path='C:/invented/cache'+str(i)+'.py',bytes=len(b),sha256=c.sha(b),base64=base64.b64encode(b).decode()) for i,(n,b) in enumerate(sorted(texts.items()))}
    old['source_cache']=dict(schema='ordinary_python_source_cache_v1',sources=rows)
    identity=json.loads(a['proposal_bytes'])['protected_identities']
    old['source_manifest']=dict(identity['firmware_package'])
    old['prerequisites']=dict(constants_sha256=identity['operational_constants']['sha256'],qualified_roles=roles,binding_input=dict(roles=roles,dependency=dict(record_sha256=None,expected_files=None,native_policy=None)))
    old['binding_plan']=dict(dependency=old['prerequisites']['binding_input']['dependency'],load_order=['invented'],protected_order=['invented'])
    old['binding_schema']=dict(load_order=['invented'],protected_order=['invented'])
    basis_names=('prior_stream','prior_prefix','prior_directory','prior_member_identification','prior_selection','prior_measured','prior_accepted_inventory','lead_plan','prior_ext_superblock_observation')
    old['basis']={n:dict(role=n) for n in basis_names}
    old['basis']['prior_stream'].update(input_package_bytes=old['source_manifest']['bytes'],input_package_sha256=old['source_manifest']['sha256'])
    old['historical_rights']=dict(conclusions=dict(actual_execution_authorized_by_this_review=False))
    historical={n:c.encoded(v) for n,v in old.items()}
    for n in c.RETAINED:a['ordinary_buffers'][n]=historical[n];a['retained_comparison_buffers'][n]=historical[n]
    change(a,'historical_evidence_index',lambda v:v.update(original_comparison={n:c.receipt(b) for n,b in a['retained_comparison_buffers'].items()}))
    change(a,'activity_rights',lambda v:v.update(decisions={n:dict(disposition='pending',evidence=[]) for n in c.policy.RIGHTS}))
    manifest=json.loads(a['ordinary_buffers']['authored_source_manifest']);manifest['sources']['retained_gate'].update(c.receipt(stub))
    a['ordinary_buffers']['authored_source_manifest']=c.encoded(manifest)
    change(a,'authored_source_receipts',lambda v:v.update(receipts={n:c.receipt(b) for n,b in sources.items()}));reseal(a)
    refs={n:dict(path='private/sessions/invented/'+n+'.json',**c.receipt(b)) for n,b in historical.items()}
    profile=c.sha(c.encoded({k:v for k,v in old['dependency_config'].items() if k!='operation_id'}))
    mapping=c.encoded(dict(references=refs,reference_pins={n:refs[n]['sha256'] for n in legacy.FIXED}|dict(dependency_profile=profile),dependency_profile_sha256=profile,raw_fixed_references=22,ordinary_input_documents=25,execution_authorized=False,camera_commands=[]))
    captures=dict(sources)
    captures.update({'review.contract':Path('tools/dependency_observation_contract.py').read_bytes(),'review.legacy':Path('tools/dependency_legacy_comparison.py').read_bytes(),'review.entry':Path('tools/dependency_pending_review.py').read_bytes()})
    captures['review.ancestry']=b'''import base64
SOURCE_ANCESTRY={'invented':True}
def effective_sources(p,context,**kwargs):return {}
def integration_sources(p):return {}
def _source_cache(p,context,effective,integration):
 return {n:base64.b64decode(r['base64']) for n,r in p['source_cache']['sources'].items()}
'''
    proof=c.encoded(dict(invented=True))
    return dict(capture_buffers=captures,expected_capture_hashes={n:c.sha(b) for n,b in captures.items()},proposal_arguments=a,historical_buffers=historical,reference_map_bytes=mapping,expected_reference_map_sha256=c.sha(mapping),expected_proposal_sha256=c.sha(a['proposal_bytes']),expected_request_sha256=c.sha(a['request_bytes']),ancestry_proof_bytes=proof,expected_ancestry_proof_sha256=c.sha(proof),historical_context=dict(repository_root='C:/invented',legacy_session='private/sessions/invented',operation_id='3'*32),runtime_expectation=json.loads(a['proposal_bytes'])['runtime'])


class PendingReviewTests(unittest.TestCase):
    def setUp(self):self.a=fixture()

    def test_composition_and_saved_comparison_close_without_authority(self):
        before=copy.deepcopy(self.a);r=review.preflight(**self.a);self.assertEqual(self.a,before)
        self.assertTrue(r['validator_owner_closed']);self.assertEqual(len(r['capture_receipts']),55)
        self.assertEqual(len(r['historical_stages']),6)
        for field in review.FALSE:self.assertIs(r[field],False)
        self.assertFalse(r['full_legacy_bundle_validated']);self.assertFalse(r['decided_outer_preflight_performed'])
        raw=review.encoded(r);self.assertTrue(review.verify_saved(raw=raw,expected_sha256=c.sha(raw),**self.a))

    def test_capture_drift_and_roster_fail_before_execution(self):
        for mode in ('hash','missing','extra','swap'):
            a=copy.deepcopy(self.a)
            if mode=='hash':a['capture_buffers']['review.legacy']+=b'\n'
            elif mode=='missing':a['capture_buffers'].pop('bound.role:core')
            elif mode=='extra':a['capture_buffers']['extra']=b'# extra'
            else:
                for key in ('capture_buffers','expected_capture_hashes'):a[key]['unknown']=a[key].pop('bound.role:core')
            with self.subTest(mode=mode),patch('builtins.exec',side_effect=AssertionError('exec')),self.assertRaises(ValueError):review.preflight(**a)

    def test_import_and_syntax_changes_fail_before_execution(self):
        for raw in (b'import ctypes\n',b'if invalid\n',b'from tools import missing\n'):
            a=copy.deepcopy(self.a);a['capture_buffers']['review.legacy']=raw;a['expected_capture_hashes']['review.legacy']=c.sha(raw)
            with self.subTest(raw=raw),patch('builtins.exec',side_effect=AssertionError('exec')),self.assertRaises((ValueError,SyntaxError)):review.preflight(**a)

    def test_saved_hash_and_rehashed_claim_tamper_refuse(self):
        result=review.preflight(**self.a);result['execution_authorized']=True;raw=review.encoded(result)
        with self.assertRaisesRegex(ValueError,'saved_hash'):review.verify_saved(raw=raw,expected_sha256='f'*64,**self.a)
        with self.assertRaisesRegex(ValueError,'saved_original'):review.verify_saved(raw=raw,expected_sha256=c.sha(raw),**self.a)

    def test_selected_input_pins_proof_and_runtime_are_separate(self):
        for name,value in (('expected_reference_map_sha256','f'*64),('expected_proposal_sha256','f'*64),('expected_request_sha256','f'*64),('expected_ancestry_proof_sha256','f'*64),('runtime_expectation',{}),('ancestry_proof_bytes',b'{}')):
            a=copy.deepcopy(self.a);a[name]=value
            with self.subTest(name=name),self.assertRaises(ValueError):review.preflight(**a)

    def test_pending_decisions_refuse_promotions(self):
        a=self.a['proposal_arguments'];change(a,'activity_rights',lambda v:v['decisions']['constants_provenance'].update(disposition='allow_scope',evidence=[c.receipt(b'invented')]))
        reseal(a)
        with self.assertRaisesRegex(ValueError,'dispositions'):review.preflight(**self.a)

    def test_live_function_class_and_source_drift_refuse_and_close(self):
        for mode in ('function','class','source'):
            owner=review.Validators(buffers=self.a['capture_buffers'],expected_hashes=self.a['expected_capture_hashes']).load()
            if mode=='function':owner.modules['dependency_legacy_comparison'].compare=lambda **kw:None
            elif mode=='class':owner.modules['dependency_producer'].RuntimeOps.extra=True
            else:owner.buffers['review.legacy']+=b'\n'
            with self.subTest(mode=mode),self.assertRaises(ValueError):owner.intact()
            with self.assertRaises(ValueError):owner.close()
            self.assertTrue(owner.closed);self.assertEqual(owner.modules,{})

    def test_close_occurs_once_on_success_and_validation_failure(self):
        original=review.Validators.close;calls=[]
        def close(owner):calls.append(owner);return original(owner)
        with patch.object(review.Validators,'close',close):review.preflight(**self.a)
        self.assertEqual(len(calls),1);self.assertTrue(calls[0].closed)
        calls.clear();a=copy.deepcopy(self.a);a['expected_request_sha256']='f'*64
        with patch.object(review.Validators,'close',close),self.assertRaises(ValueError):review.preflight(**a)
        self.assertEqual(len(calls),1);self.assertTrue(calls[0].closed)

    def test_cleanup_failure_prevents_success_and_preserves_primary(self):
        original=review.Validators.close
        def fail(owner):original(owner);raise RuntimeError('invented cleanup failure')
        with patch.object(review.Validators,'close',fail),self.assertRaisesRegex(RuntimeError,'cleanup failure'):review.preflight(**self.a)
        a=copy.deepcopy(self.a);a['expected_request_sha256']='f'*64
        with patch.object(review.Validators,'close',fail),self.assertRaisesRegex(ValueError,'selected_anchor') as raised:review.preflight(**a)
        self.assertIsInstance(raised.exception.__cause__,RuntimeError)

    def test_load_failure_closes_once_and_publishes_no_tool_alias(self):
        a=copy.deepcopy(self.a);raw=a['capture_buffers']['review.legacy']+b'\nraise ValueError("invented load failure")\n'
        a['capture_buffers']['review.legacy']=raw;a['expected_capture_hashes']['review.legacy']=c.sha(raw)
        calls=[];original=review.Validators.close
        def close(owner):calls.append(owner);return original(owner)
        with patch.object(review.Validators,'close',close),self.assertRaisesRegex(ValueError,'load failure'):review.preflight(**a)
        self.assertEqual(len(calls),1);self.assertTrue(calls[0].closed);self.assertEqual(calls[0].modules,{})

    def test_mismatched_historical_context_refuses(self):
        self.a['historical_context']['operation_id']='4'*32
        with self.assertRaisesRegex(ValueError,'historical_operation'):review.preflight(**self.a)
