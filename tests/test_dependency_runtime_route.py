"""Original runtime routing over invented dependency and protected inputs.

Only the child RuntimeOps constructor binding is replaced. Dispatch, collector,
controller, producer and frozen parent verification remain original. Runtime
record grammar is explicitly synthetic evidence, never an actual observation.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from tools import dependency_operational_launcher as parent
from dependency_terminal_fixture import REPOSITORY, _pinned_source
from dependency_runtime_route_fixture import route_fixture_source
import test_dependency_binding_integration as binding
import test_dependency_io_boundary as io_boundary


WIRING_SHA256='9bb5b33f37f5cf6e5231afdae87b230281423c058a852b8977de2fc754eeb31d'


def route_child_suffix(mode):
    raw=io_boundary.child_suffix(mode)
    replacements={
      b'refresh=[];constants=[];io_trace=None':
       b'refresh=[];constants=[];io_trace=None;runtime_owner=None',
      b'io_trace=_InventedIoTrace(source_path,SYNTHETIC_MODE)':
       b'''io_trace=_InventedIoTrace(source_path,SYNTHETIC_MODE)
  runtime_inputs=owned['helpers'].package.dependency_execution.bind_runtime_packet(
   owned['prepared']['dependency_packet'],owned['prepared']['dependency_fixed'],
   owned['dependency_source_buffers'],owned['prepared']['dependency_review_sha256'])
  runtime_owner=_SyntheticRuntimeOwner(owned['helpers'],runtime_inputs)
  runtime_owner.install()''',
      b'if io_trace is not None:':
       b'''if runtime_owner is not None:
  try:runtime_owner.close()
  except BaseException as error:
   if cleanup is None:cleanup=error
 if io_trace is not None:''',
      b'io_boundary=_boundary_observation(callback_loader,io_trace,constants),':
       b'''io_boundary=_boundary_observation(callback_loader,io_trace,constants),
  runtime_route=None if runtime_owner is None else runtime_owner.observation(),
  synthetic_saved_metadata=_route_saved_metadata(owned),''',
    }
    for old,new in replacements.items():
        if raw.count(old)!=1:raise AssertionError('synthetic route diagnostic source drift')
        raw=raw.replace(old,new)
    metadata=rb'''
def _route_saved_metadata(owned):
 if owned is None:return {}
 folder=Path(owned['prepared']['folder']);values={}
 keys=('status','evidence_mode','test_injection_used','actual_installation_observed',
  'actual_dependency_observation_performed','audit_acknowledgement_is_invented')
 for name in ('completion.json','collected/collection.json','collected/completion.json',
              'collected/producer/raw.json','collected/producer/audit-acknowledgement.json',
              'collected/producer/result.json'):
  path=folder/name
  if path.exists():
   raw=path.read_bytes()
   if not raw:
    values[name]=dict(empty_partial_record=True)
    continue
   value=json.loads(raw);values[name]={k:value[k] for k in keys if k in value}
   if 'observation' in value:values[name]['observation_evidence_mode']=value['observation']['evidence_mode']
 return dict(fields=values,all_fields_are_synthetic_grammar=True,
  actual_dependency_observation_performed=False,actual_runtime_verified=False)
'''
    return route_fixture_source(mode)+metadata+raw


OBSERVATIONS=[]


@unittest.skipUnless(sys.platform=='win32','retained readonly guard requires Windows file attributes')
class RuntimeRouteTests(unittest.TestCase):
    setUpClass=classmethod(io_boundary.IoBoundaryTests.setUpClass.__func__)
    emergency_reap=io_boundary.IoBoundaryTests.emergency_reap
    fixture=io_boundary.IoBoundaryTests.fixture

    def configure_case(self,case,inputs,terminal,mode):
        binding.BindingIntegrationTests.configure_case(self,case,inputs,terminal,mode)
        # No binder result wrapper or wiring override is used in this package.
        case.fixture_binding_source=self.captured['binding_source']
        case.fixture_wiring=_pinned_source(REPOSITORY/'tools/dependency_successor_wiring.py',WIRING_SHA256)
        case.fixture_child_suffix=route_child_suffix(mode)

    def run_route(self,mode='complete',*,tamper_saved=False):
        case,plan,inputs=self.fixture(mode)
        expected=copy.deepcopy(case.validated['inputs']['binding_plan'])
        processes=[];real_popen=subprocess.Popen;reconciliations=[]
        def spawn(*args,**kwargs):
            self.assertFalse(processes,'automatic retry')
            process=real_popen(*args,**kwargs);processes.append(process)
            self.addCleanup(self.emergency_reap,process);return process
        real_reconcile=parent._reconcile
        def reconcile(current,narrow):
            reconciliations.append(dict(tamper_saved=tamper_saved))
            if tamper_saved:
                path=Path(current['prepared']['folder'])/'collected/producer/raw.json'
                raw=path.read_bytes();path.write_bytes(raw+b' ')
                # Updating the outer digest must not hide inner saved-record drift.
                terminal_path=current['folder']/'outer-child.json'
                terminal=json.loads(terminal_path.read_bytes())
                terminal['evidence']['dependency_sha256']['producer/raw.json']=parent.sha(path.read_bytes())
                terminal_path.write_bytes(parent.encoded(terminal))
            return real_reconcile(current,narrow)
        with patch.object(parent.subprocess,'Popen',side_effect=spawn), \
             patch.object(parent,'_reconcile',side_effect=reconcile):
            answer=parent._run_pending(plan)
        diag=json.loads((plan['folder']/'synthetic-child-observation.json').read_bytes())
        narrow_path=plan['context']['session_dir']/'host-result.json'
        narrow=json.loads(narrow_path.read_bytes()) if narrow_path.exists() else None
        row=dict(test=self.id(),mode=mode,answer=answer,diagnostic=diag,narrow=narrow,
            expected_plan=expected,contract_sha256=self.captured['expected_contract_sha256'],
            wiring_sha256=WIRING_SHA256,reconciliations=reconciliations,
            outer_digest_updated_for_saved_drift=tamper_saved,camera_commands=[])
        OBSERVATIONS.append(row)
        self.assertEqual(len(processes),1);self.assertIsNotNone(processes[0].poll())
        self.assertTrue(processes[0].stdout.closed and processes[0].stderr.closed)
        for name in ('helpers','validation','bootstrap','adapter','outer'):self.assertTrue(plan[name].closed,name)
        self.assertTrue(all(diag['owners_closed'].values()));self.assertEqual(diag['leaked_aliases'],[])
        self.assertIsNone(diag['cleanup_failure_type']);self.assertEqual(diag['camera_commands'],[])
        self.assertEqual(diag['io_boundary']['source_fds_live'],[])
        self.assertTrue(diag['io_boundary']['tracing_restored'])
        self.assertEqual(diag['io_boundary']['live_owned_aliases'],[])
        for key in ('actual_runtime_verified','producer_execution_authenticated','execution_authorized',
                    'feature_supported','recovery_proven','device_write_gate_passed','terminal_replay'):
            self.assertIs(diag[key],False,key)
        route=diag['runtime_route']
        self.assertEqual((route['install_attempts'],route['close_attempts']),(1,1))
        for key in ('closed','original_class_restored','original_class_and_producer_functions_intact',
                    'fake_loader_restored','runtime_shaped_saved_fields_are_synthetic'):
            self.assertIs(route[key],True,key)
        self.assertEqual(route['live_owned_aliases'],[])
        self.assertEqual(route['foreign_alias_replacements'],[]);self.assertEqual(route['cleanup_errors'],[])
        self.assertIs(route['actual_dependency_observation_performed'],False)
        self.assertEqual(json.loads((plan['folder']/'final-receipt.json').read_bytes()),answer)
        self.assertEqual([expected['dependency'][k] for k in ('record_sha256','expected_files','native_policy')],[None]*3)
        for key in ('execution_authorized','actual_runtime_verified','actual_binding_ready'):
            self.assertIs(expected[key],False,key)
        return plan,answer,diag,narrow,inputs

    def assert_complete_child(self,diag,narrow,inputs):
        self.assertIsNone(diag['failure_type']);self.assertFalse(diag['preparation_failed'])
        self.assertTrue(diag['callbacks_claimed'] and diag['callbacks_closed'] and diag['callback_lease_closed'])
        self.assertEqual(narrow['host_exit_code'],0)
        self.assertEqual(narrow['adapter_snapshot']['status'],'complete')
        route=diag['runtime_route']
        self.assertEqual(route['constructor_calls'],1);self.assertEqual(route['constructor_preloaded_roots'],[])
        self.assertEqual((route['fake_loader_calls'],route['fake_callback_calls']),(5,1))
        self.assertGreater(route['fake_cipher_calls'],0)
        self.assertEqual(len(diag['protected_aliases_loaded']),3)
        self.assertEqual(len(diag['io_boundary']['constants_reads']),1)
        events=diag['io_boundary']['events'];ops=[v['op'] for v in events]
        self.assertEqual((ops.count('open'),ops.count('seek'),ops.count('close_returned')),(2,2,2))
        self.assertEqual(sum(v['returned'] for v in events if v['op']=='read'),4*len(inputs['source_raw']))
        saved=diag['synthetic_saved_metadata']
        self.assertTrue(saved['all_fields_are_synthetic_grammar'])
        self.assertIs(saved['actual_runtime_verified'],False)
        fields=saved['fields']
        self.assertIs(fields['collected/collection.json']['actual_installation_observed'],True)
        for name in ('completion.json','collected/completion.json'):
            self.assertIs(fields[name]['actual_dependency_observation_performed'],True)
            self.assertIs(fields[name]['test_injection_used'],False)
        self.assertIs(fields['collected/producer/result.json']['audit_acknowledgement_is_invented'],False)
        self.assertEqual(fields['collected/producer/result.json']['observation_evidence_mode'],'saved_records')
        self.assertIs(fields['collected/producer/audit-acknowledgement.json']['test_injection_used'],False)

    def test_original_runtime_route_and_parent_join(self):
        plan,answer,diag,narrow,inputs=self.run_route()
        self.assert_complete_child(diag,narrow,inputs)
        self.assertEqual(answer['status'],'consistent_pending_composition',answer)
        saved=answer['engine_result']['engine_result']
        self.assertEqual(saved['status'],'consistent_saved_controller')
        for key in ('actual_runtime_verified','producer_execution_authenticated','execution_authorized',
                    'feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(saved[key],False,key)

    def assert_route_refused(self,mode):
        plan,answer,diag,narrow,inputs=self.run_route(mode)
        self.assertEqual(answer['status'],'needs_review',answer)
        self.assertFalse((plan['folder']/'outer-child.json').exists())
        self.assertTrue(diag['preparation_started']);self.assertFalse(diag['preparation_failed'])
        self.assertFalse(diag['callbacks_claimed']);self.assertTrue(diag['callbacks_closed'])
        self.assertEqual(diag['io_boundary']['events'],[])
        self.assertEqual(diag['io_boundary']['constants_reads'],[])
        route=diag['runtime_route'];self.assertEqual(route['fake_loader_calls'],0)
        self.assertEqual(route['fake_callback_calls'],0)
        self.assertTrue((Path(plan['prepared']['folder'])/'started.json').exists())
        return diag,route

    def test_constructor_interruption_closes_reserved_owners(self):
        diag,route=self.assert_route_refused('constructor_error')
        self.assertEqual(route['constructor_calls'],1)
        self.assertEqual(diag['failure_code'],'synthetic_runtime_constructor_error')

    def test_reader_interruption_refuses_before_loader(self):
        diag,route=self.assert_route_refused('reader_error')
        self.assertEqual(route['constructor_calls'],1)
        self.assertIn('synthetic_runtime_reader_error',diag['failure_code'])

    def test_preloaded_origin_refuses_before_constructor(self):
        diag,route=self.assert_route_refused('preloaded')
        self.assertEqual(route['constructor_calls'],0)
        self.assertEqual(diag['failure_code'],'preloaded_runtime_origin')

    def test_unlisted_simulated_native_intent_refuses_before_fake_loader(self):
        diag,route=self.assert_route_refused('native_intent')
        self.assertEqual(route['constructor_calls'],1)
        self.assertEqual(route['native_intent_requests'],1)
        self.assertIn('native_arguments',diag['failure_code'])

    def test_parent_rejects_saved_drift_after_outer_digest_update(self):
        plan,answer,diag,narrow,inputs=self.run_route(tamper_saved=True)
        self.assert_complete_child(diag,narrow,inputs)
        self.assertEqual(answer['status'],'needs_review',answer)
        self.assertIsNotNone(answer['failure_type'])
        self.assertTrue((plan['folder']/'outer-child.json').exists())


if __name__=='__main__':unittest.main(verbosity=2)
