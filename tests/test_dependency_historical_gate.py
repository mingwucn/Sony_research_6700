"""Invented complete bundles; cached Python text is never executed."""
import base64, copy, hashlib, json
from pathlib import Path
import tempfile, unittest
from unittest.mock import patch
from tools import dependency_historical_gate as gate
import dependency_historical_fixture as fixtures

for name in ('REQUIRED_OUTER_TEST_IDS','REQUIRED_OUTER_SOURCE_PINS','REQUIRED_OUTER_SOURCE_NAMES','REQUIRED_REPAIR_TEST_IDS','REQUIRED_REPAIR_SOURCE_PINS','REQUIRED_FACTORY_TEST_IDS','REQUIRED_CHILD_TEST_IDS','PARENT_EVIDENCE_POLICY'):
    setattr(fixtures,name,getattr(gate,name))
fixture_repair=dict(gate.REQUIRED_REPAIR_SOURCE_PINS)
for key,name in gate.REPAIR_SOURCE_NAMES.items():
    fixture_repair[name]=gate.sha(('raise AssertionError("never execute invented source") # '+key+'\n').encode())
fixtures.REQUIRED_REPAIR_SOURCE_PINS=fixture_repair

class Ancestry(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.f=fixtures.Fixture(Path(self.tmp.name));p=self.f.p;legacy=self.f.c['legacy_session']
  # Distinct nested historical keys intentionally have the same basename.
  for role,nested in [('role:role2','nested-a/shared.py'),('role:role3','nested-b/shared.py')]:
   row=p['source_cache']['sources'][role];old=Path(row['path']).name
   for name in ('q_old_seal','q_old_result','q_old_review'):
    values=p[name]['sources_sha256']
    if old in values:values[nested]=values.pop(old)
   row['path']=str(self.f.root/legacy/nested)
  rows={}
  for key,row in p['source_cache']['sources'].items():
   if not key.startswith(('role:','bootstrap:')):continue
   old=Path(row['path']).relative_to(self.f.root/legacy).as_posix()
   current=legacy+'/activation/'+old
   row['path']=str(self.f.root/current);p['source_receipts']['receipts'][key]['path']=row['path']
   if key.startswith('role:'):p['role_authority']['roles'][key[5:]]['path']=current
   if key in p['repair_overlay']['repairs']:p['repair_overlay']['repairs'][key]['path']=current
   rows[key]={'current_path':current,'historical_key':old,'historical_sha256':p['q_old_seal']['sources_sha256'][old],'current_sha256':row['sha256']}
  docs,_=self.f.pack();self.raw_seal_sha=gate.sha(docs['inputs']['q_old_seal'])
  self.policy={'schema':'gdt_explicit_source_ancestry_v1','legacy_session':legacy,
   'historical_seal_sha256':self.raw_seal_sha,'historical_seal_canonical_sha256':gate.sha(gate.encoded(p['q_old_seal'])),
   'rows':rows,'execution_authorized':False,'camera_commands':[]}
  self.stack=[]
  for key,value in [('SOURCE_ANCESTRY',self.policy),('SOURCE_ANCESTRY_SHA256',gate.sha(gate.encoded(self.policy))),('REQUIRED_REPAIR_SOURCE_PINS',fixture_repair)]:
   cm=patch.object(gate,key,value);cm.start();self.addCleanup(cm.stop)
 def reseal_test_policy(self):gate.SOURCE_ANCESTRY_SHA256=gate.sha(gate.encoded(self.policy))
 def ancestry(self):return gate.source_ancestry(self.f.p,self.f.c,self.raw_seal_sha)
 def effective(self):
  docs,_=self.f.pack()
  return gate.effective_sources(self.f.p,self.f.c,repair_result_sha256=gate.sha(docs['inputs']['q_repair_result']),historical_seal_sha256=self.raw_seal_sha)
 def refused(self,call=None):
  with self.assertRaises(gate.GateError):(call or self.effective)()
 def test_all29_migrated_full_paths(self):
  found=self.effective();self.assertEqual(len(found),29)
  self.assertEqual(set(found),{r['current_path'] for r in self.policy['rows'].values()})
 def test_full_pure_bundle_uses_migration(self):
  docs,seal=self.f.pack();v=gate.validate_bundle(docs,expected_seal_sha256=seal,reference_pins=self.f.reference_pins(docs))
  self.assertEqual(len(v['effective_qualified_sources']),29);self.assertEqual(len(v['source_buffers']),47)
  self.assertFalse(v['actual_entry_ready'])
 def test_pure_no_file_opens(self):
  with patch('builtins.open',side_effect=AssertionError('no filesystem')):self.assertEqual(len(self.effective()),29)
 def test_nested_same_basename_stays_distinct(self):
  found=self.effective();self.assertIn(self.f.c['legacy_session']+'/activation/nested-a/shared.py',found)
  self.assertIn(self.f.c['legacy_session']+'/activation/nested-b/shared.py',found)
 def test_removed_role(self):self.policy['rows'].pop('role:role2');self.reseal_test_policy();self.refused()
 def test_extra_role(self):self.policy['rows']['role:extra']={};self.reseal_test_policy();self.refused()
 def test_wrong_ancestor(self):self.policy['legacy_session']='private/sessions/wrong';self.reseal_test_policy();self.refused()
 def test_wrong_candidate_root(self):self.f.c['legacy_session']='private/sessions/wrong';self.refused()
 def test_wrong_raw_seal(self):self.raw_seal_sha='0'*64;self.refused()
 def test_changed_parsed_seal(self):self.f.p['q_old_seal']['unexpected']=True;self.refused()
 def test_changed_mapping_without_policy_pin(self):self.policy['rows']['role:role2']['current_sha256']='0'*64;self.refused()
 def test_old_hash_substitution(self):self.policy['rows']['role:role2']['historical_sha256']='0'*64;self.reseal_test_policy();self.refused()
 def test_current_hash_substitution(self):self.policy['rows']['role:role2']['current_sha256']='0'*64;self.reseal_test_policy();self.refused()
 def test_current_path_substitution(self):self.policy['rows']['role:role2']['current_path']=self.f.c['legacy_session']+'/other.py';self.reseal_test_policy();self.refused()
 def test_no_basename_fallback(self):self.policy['rows']['role:role2']['historical_key']='shared.py';self.reseal_test_policy();self.refused()
 def test_no_prefix_fallback(self):self.policy['rows']['role:role2']['historical_key']='activation/nested-a/shared.py';self.reseal_test_policy();self.refused()
 def test_historical_traversal(self):self.policy['rows']['role:role2']['historical_key']='nested-a/../shared.py';self.reseal_test_policy();self.refused()
 def test_current_traversal(self):self.policy['rows']['role:role2']['current_path']=self.f.c['legacy_session']+'/activation/../role2.py';self.reseal_test_policy();self.refused()
 def test_absolute_historical_key(self):self.policy['rows']['role:role2']['historical_key']='/tmp/shared.py';self.reseal_test_policy();self.refused()
 def test_duplicate_historical_path(self):self.policy['rows']['role:role3']['historical_key']=self.policy['rows']['role:role2']['historical_key'];self.reseal_test_policy();self.refused()
 def test_casefold_historical_alias(self):self.policy['rows']['role:role3']['historical_key']=self.policy['rows']['role:role2']['historical_key'].upper();self.reseal_test_policy();self.refused()
 def test_duplicate_current_path(self):self.policy['rows']['role:role3']['current_path']=self.policy['rows']['role:role2']['current_path'];self.reseal_test_policy();self.refused()
 def test_removed_cached_source(self):self.f.p['source_cache']['sources'].pop('role:role2');self.refused()
 def test_extra_cached_source(self):self.f.p['source_cache']['sources']['role:extra']={};self.refused()
 def test_missing_bootstrap(self):self.policy['rows'].pop('bootstrap:io_entry');self.reseal_test_policy();self.refused()
 def test_changed_overlay_old(self):self.f.p['repair_overlay']['repairs']['role:gdt_gate']['old_sha256']='0'*64;self.refused()
 def test_changed_overlay_new(self):self.f.p['repair_overlay']['repairs']['role:gdt_gate']['new_sha256']='0'*64;self.refused()
 def test_changed_overlay_path(self):self.f.p['repair_overlay']['repairs']['role:gdt_gate']['path']='private/other.py';self.refused()
 def test_added_overlay(self):self.f.p['repair_overlay']['repairs']['role:role2']={};self.refused()
 def test_authority_promotion(self):self.policy['execution_authorized']=True;self.reseal_test_policy();self.refused()
 def test_extra_row_field(self):self.policy['rows']['role:role2']['extra']=True;self.reseal_test_policy();self.refused()
 def test_extra_policy_field(self):self.policy['extra']=True;self.reseal_test_policy();self.refused()
 def test_live_mapping_file_not_followed(self):
  with patch.object(Path,'read_bytes',side_effect=AssertionError('no map file reads')):self.assertEqual(len(self.ancestry()),29)


class HistoricalContext(unittest.TestCase):
 def setUp(self):
  Ancestry.setUp(self)
  # Change current act only. Saved dependency_config operation remains untouched.
  for v in (self.f.c,self.f.d,self.f.r,self.f.s,self.f.p['activity_scope']):
   v['operation_id']='2'*32
  self.docs,self.seal=self.f.pack()
  self.context=dict(schema='gdt_historical_context_v1',
   repository_root=self.f.c['repository_root'],legacy_session=self.f.c['legacy_session'],
   operation_id='1'*32,dependency_config_sha256=gate.sha(self.docs['inputs']['dependency_config']),
   historical_seal_sha256=gate.sha(self.docs['inputs']['q_old_seal']),
   ancestry_proof_sha256=gate.SOURCE_ANCESTRY_SHA256,execution_authorized=False,camera_commands=[])
 def args(self):
  raw=gate.encoded(self.context)
  return dict(expected_seal_sha256=self.seal,reference_pins=self.f.reference_pins(self.docs),
   context_bytes=raw,expected_context_sha256=gate.sha(raw),
   ancestry_proof_bytes=gate.encoded(self.policy),
   expected_ancestry_proof_sha256=gate.SOURCE_ANCESTRY_SHA256,expected_operation_id='2'*32)
 def check(self,**changes):
  a=self.args();a.update(changes)
  return gate.validate_bundle_v6(self.docs,**a)
 def test_full_distinct_operations_pass_all_inherited_guards(self):
  original=copy.deepcopy(self.docs)
  with patch('builtins.open',side_effect=AssertionError('no opens')), \
       patch.object(Path,'open',side_effect=AssertionError('no opens')):
   result=self.check()
  self.assertEqual(self.docs,original)
  self.assertEqual(result['schema'],'gdt_outer_consistency_v6')
  self.assertEqual(result['historical_operation_id'],'1'*32)
  self.assertEqual(result['current_operation_id'],'2'*32)
  self.assertEqual(len(result['source_buffers']),47)
  self.assertEqual(len(result['effective_qualified_sources']),29)
  self.assertNotIn('child_argv',result)
  for n in ('execution_authorized','actual_entry_ready','feature_supported','recovery_proven',
            'device_write_gate_passed','actual_inputs_accessed'):
   self.assertIs(result[n],False)
 def test_legacy_entry_still_refuses_cross_operation(self):
  with self.assertRaisesRegex(gate.GateError,'operation_binding'):
   gate.validate_bundle(self.docs,expected_seal_sha256=self.seal,
                        reference_pins=self.f.reference_pins(self.docs))
 def test_changed_context_without_pin_refuses(self):
  with self.assertRaisesRegex(gate.GateError,'historical_context_anchor'):
   self.check(context_bytes=self.args()['context_bytes']+b' ')
 def test_changed_proof_without_pin_refuses(self):
  with self.assertRaisesRegex(gate.GateError,'historical_ancestry_anchor'):
   self.check(ancestry_proof_bytes=self.args()['ancestry_proof_bytes']+b' ')
 def test_rehashed_wrong_context_sources_refuse(self):
  for field in ('dependency_config_sha256','historical_seal_sha256','ancestry_proof_sha256'):
   context=copy.deepcopy(self.context);context[field]='0'*64;raw=gate.encoded(context)
   with self.subTest(field=field),self.assertRaisesRegex(gate.GateError,'historical_context_sources'):
    self.check(context_bytes=raw,expected_context_sha256=gate.sha(raw))
 def test_rehashed_wrong_context_root_refuses(self):
  for field,value in (('repository_root',str(self.f.root/'wrong')),('legacy_session','private/sessions/wrong')):
   context=copy.deepcopy(self.context);context[field]=value;raw=gate.encoded(context)
   with self.subTest(field=field),self.assertRaisesRegex(gate.GateError,'historical_context_root'):
    self.check(context_bytes=raw,expected_context_sha256=gate.sha(raw))
 def test_rehashed_wrong_historical_operation_refuses(self):
  self.context['operation_id']='3'*32
  with self.assertRaisesRegex(gate.GateError,'historical_operation_binding'):self.check()
 def test_wrong_current_operation_refuses(self):
  with self.assertRaisesRegex(gate.GateError,'historical_operation_binding'):
   self.check(expected_operation_id='3'*32)
 def test_same_operation_is_not_migration(self):
  for v in (self.f.c,self.f.d,self.f.r,self.f.s,self.f.p['activity_scope']):v['operation_id']='1'*32
  self.docs,self.seal=self.f.pack()
  with self.assertRaisesRegex(gate.GateError,'historical_operation_binding'):
   self.check(expected_operation_id='1'*32)
 def test_current_decision_refusal_preserved_after_resealing(self):
  self.f.d['execution_authorized']=False;self.docs,self.seal=self.f.pack()
  with self.assertRaisesRegex(gate.GateError,'activity_decision'):self.check()
 def test_current_review_identity_guard_preserved_after_resealing(self):
  self.f.r['reviewer']=self.f.c['author'];self.docs,self.seal=self.f.pack()
  with self.assertRaisesRegex(gate.GateError,'review_identity'):self.check()
 def test_source_bytes_change_cannot_be_hidden_by_rehashing_documents(self):
  row=self.f.p['source_cache']['sources']['role:role2'];row['base64']=base64.b64encode(b'wrong').decode()
  self.docs,self.seal=self.f.pack()
  with self.assertRaisesRegex(gate.GateError,'source_hash'):self.check()
 def test_closed_context_and_flags_refuse(self):
  for field,value in (('extra',True),('execution_authorized',True),('camera_commands',['invented'])):
   context=copy.deepcopy(self.context);context[field]=value;raw=gate.encoded(context)
   with self.subTest(field=field),self.assertRaises(gate.GateError):
    self.check(context_bytes=raw,expected_context_sha256=gate.sha(raw))
 def test_external_seal_and_reference_pins_still_bind(self):
  with self.assertRaisesRegex(gate.GateError,'external_anchor'):self.check(expected_seal_sha256='0'*64)
  pins=self.args()['reference_pins'];pins['basis']='0'*64
  with self.assertRaisesRegex(gate.GateError,'reference_authority'):self.check(reference_pins=pins)


if __name__=='__main__':unittest.main(verbosity=2)
