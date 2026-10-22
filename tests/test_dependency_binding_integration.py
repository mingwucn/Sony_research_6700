"""Genuine binding checks in the invented-file preparation/child/parent path.

Expected imports are captured before labelled candidate fault injection. The
retained validator source/function predicates stay intact. No actual protected
source, firmware/constants, installed dependency or camera is accessed.
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
from dependency_binding_fixture import capture_binding_fixture, build_expected_plan
import test_dependency_io_boundary as io_boundary


BINDING_PATH=REPOSITORY/'private/sessions/20261019-RA-003-parent-evidence-v5/activation/activation_binding.py'
BINDING_SHA256='22558080636f15300590c22b9987216216f650b4edc58d7df89092643722de74'

# This labelled caller/result fault adapter delegates to the saved genuine
# validator. It neither replaces its checks nor changes the expected contract.
FAULT_ADAPTER=rb'''
import sys
_synthetic_original_prepare_bindings=prepare_bindings
def prepare_bindings(**kw):
 mode=SYNTHETIC_BINDING_MODE
 sys.audit('a6700.synthetic.binding_begin',mode,SYNTHETIC_CONTRACT_SHA256)
 if mode=='source_hash':
  kw['authored_sources']=dict(kw['authored_sources'])
  kw['authored_sources']['capture']+=b'\n# invented hash drift\n'
 elif mode=='import_drift':
  kw['authored_sources']=dict(kw['authored_sources'])
  raw=kw['authored_sources']['capture']+b'\nimport os\n'
  kw['authored_sources']['capture']=raw
  kw['binding_input']=_copy(kw['binding_input'])
  kw['qualified_roles']=_copy(kw['qualified_roles'])
  kw['qualified_sources']=dict(kw['qualified_sources'])
  for roles in (kw['binding_input']['roles'],kw['qualified_roles']):roles['capture']['sha256']=_sha(raw)
  kw['qualified_sources'][kw['qualified_roles']['capture']['path']]=_sha(raw)
 elif mode=='qualified_role':
  kw['binding_input']=_copy(kw['binding_input'])
  kw['binding_input']['roles']['capture']['sha256']='0'*64
 elif mode in ('occupied_role','occupied_tools','occupied_crypto','duplicate_alias'):
  added={'occupied_role':(CONTRACT['aliases']['capture'],),
   'occupied_tools':('tools.invented_binding_collision',),
   'occupied_crypto':('Cryptodome.invented_binding_collision',),
   'duplicate_alias':('invented_duplicate','invented_duplicate')}[mode]
  kw['preexisting_aliases']=kw['preexisting_aliases']+added
 try:plan=_synthetic_original_prepare_bindings(**kw)
 except BindingError as error:
  sys.audit('a6700.synthetic.binding_refused',error.stage,error.code)
  raise
 sys.audit('a6700.synthetic.binding_validated',json.dumps(plan,sort_keys=True))
 if mode in ('load_order','protected_order'):
  key=mode
  plan[key]=list(reversed(plan[key]))
  sys.audit('a6700.synthetic.binding_result_fault',key)
 return plan
'''


def binding_child_suffix(mode):
    raw=io_boundary.child_suffix(mode)
    changes={
      b'refresh=[];constants=[];io_trace=None':b'refresh=[];constants=[];io_trace=None;binding_events=[]',
      b"if event=='a6700.synthetic.constants_read':constants.append(list(args))":
       b"if event=='a6700.synthetic.constants_read':constants.append(list(args))\n  if event.startswith('a6700.synthetic.binding_'):binding_events.append(dict(event=event,args=list(args)))",
      b'io_boundary=_boundary_observation(callback_loader,io_trace,constants),':
       b'io_boundary=_boundary_observation(callback_loader,io_trace,constants),binding_events=binding_events,',
    }
    for old,new in changes.items():
        if raw.count(old)!=1:raise AssertionError('invented binding diagnostic drift')
        raw=raw.replace(old,new)
    return raw


OBSERVATIONS=[]


@unittest.skipUnless(sys.platform=='win32','retained readonly guard requires Windows file attributes')
class BindingIntegrationTests(unittest.TestCase):
    setUpClass=classmethod(io_boundary.IoBoundaryTests.setUpClass.__func__)
    emergency_reap=io_boundary.IoBoundaryTests.emergency_reap
    fixture=io_boundary.IoBoundaryTests.fixture

    def configure_case(self,case,inputs,terminal,mode):
        raw=_pinned_source(BINDING_PATH,BINDING_SHA256)
        captured=capture_binding_fixture(binding_raw=raw,ordinary_sources=terminal.role_sources,
            protected_sources=inputs['role_sources'])
        # The helper captures exact expected imports before the candidate
        # adapter below can mutate any caller buffers, aliases or output order.
        self.captured=captured
        self.assertEqual(hashlib.sha256(raw).hexdigest(),BINDING_SHA256)
        contract=copy.deepcopy(captured['contract'])
        case.fixture_prerequisites['binding_input']=dict(schema='activation_binding_input_v1',roles={},
            dependency=dict(schema='activation_dependency_plan_v1',version='3.24.1',
                wheel_sha256='b'*64,record_sha256=None,expected_files=None,native_policy=None))
        case.fixture_binding_schema={k:copy.deepcopy(contract[k]) for k in ('aliases','load_order','protected_order')}
        prefix=("\nSYNTHETIC_BINDING_MODE="+repr(mode)+
                "\nSYNTHETIC_CONTRACT_SHA256="+repr(captured['expected_contract_sha256'])+'\n').encode()
        case.fixture_binding_source=captured['binding_source']+prefix+FAULT_ADAPTER
        case.fixture_binding_plan=lambda prerequisites:build_expected_plan(prerequisites,contract)
        case.fixture_child_suffix=binding_child_suffix(mode)

    def run_binding(self,mode='complete'):
        case,plan,inputs=self.fixture(mode)
        expected=copy.deepcopy(case.validated['inputs']['binding_plan'])
        processes=[];real_popen=subprocess.Popen
        def spawn(*args,**kwargs):
            self.assertFalse(processes,'automatic retry')
            process=real_popen(*args,**kwargs);processes.append(process)
            self.addCleanup(self.emergency_reap,process);return process
        with patch.object(parent.subprocess,'Popen',side_effect=spawn):answer=parent._run_pending(plan)
        self.assertEqual(len(processes),1);self.assertIsNotNone(processes[0].poll())
        self.assertTrue(processes[0].stdout.closed and processes[0].stderr.closed)
        diag=json.loads((plan['folder']/'synthetic-child-observation.json').read_bytes())
        narrow=json.loads((plan['context']['session_dir']/'host-result.json').read_bytes()) \
            if (plan['context']['session_dir']/'host-result.json').exists() else None
        row=dict(test=self.id(),mode=mode,answer=answer,diagnostic=diag,narrow=narrow,
            expected_plan=expected,contract_sha256=self.captured['expected_contract_sha256'],
            role_source_pins=self.captured['role_pins'],camera_commands=[])
        OBSERVATIONS.append(row)
        for name in ('helpers','validation','bootstrap','adapter','outer'):self.assertTrue(plan[name].closed,name)
        self.assertTrue(all(diag['owners_closed'].values()));self.assertEqual(diag['leaked_aliases'],[])
        self.assertIsNone(diag['cleanup_failure_type']);self.assertEqual(diag['camera_commands'],[])
        self.assertEqual(diag['io_boundary']['source_fds_live'],[])
        self.assertTrue(diag['io_boundary']['tracing_restored'])
        self.assertEqual(diag['io_boundary']['live_owned_aliases'],[])
        for key in ('actual_runtime_verified','producer_execution_authenticated','execution_authorized',
                    'feature_supported','recovery_proven','device_write_gate_passed','terminal_replay'):
            self.assertIs(diag[key],False,key)
        self.assertEqual(json.loads((plan['folder']/'final-receipt.json').read_bytes()),answer)
        self.assertEqual(diag['binding_events'][0],dict(event='a6700.synthetic.binding_begin',
            args=[mode,self.captured['expected_contract_sha256']]))
        self.assertEqual(expected['dependency']['record_sha256'],None)
        self.assertEqual(expected['dependency']['expected_files'],None)
        self.assertEqual(expected['dependency']['native_policy'],None)
        self.assertEqual(expected['blockers'],['dependency_manifest_unobserved','native_policy_unobserved'])
        for key in ('execution_authorized','actual_runtime_verified','actual_binding_ready'):
            self.assertIs(expected[key],False,key)
        return plan,answer,diag,narrow,expected

    def assert_binding_refused(self,mode,code=None,order=None):
        plan,answer,diag,narrow,expected=self.run_binding(mode)
        self.assertEqual(answer['status'],'needs_review',answer)
        self.assertFalse((plan['folder']/'outer-child.json').exists())
        self.assertTrue(diag['preparation_failed']);self.assertIsNone(diag['callbacks_closed'])
        self.assertIs(diag['callback_lease_attempted'],False)
        self.assertEqual(diag['protected_aliases_loaded'],[])
        self.assertEqual(diag['io_boundary']['constants_reads'],[])
        self.assertEqual(diag['io_boundary']['events'],[])
        events=diag['binding_events']
        if code is not None:
            self.assertEqual(events[1:], [dict(event='a6700.synthetic.binding_refused',args=['binding_plan',code])])
            self.assertEqual(diag['failure_type'],'BindingError')
            self.assertEqual(diag['failure_code'],'binding_plan:'+code)
        else:
            self.assertIsNotNone(order)
            self.assertEqual(json.loads(events[1]['args'][0]),expected)
            self.assertEqual(events[1]['event'],'a6700.synthetic.binding_validated')
            self.assertEqual(events[2:], [dict(event='a6700.synthetic.binding_result_fault',args=[order])])
            self.assertEqual(diag['failure_type'],'ValueError')
            self.assertEqual(diag['failure_code'],'outer_entry_v2_refused')

    def test_genuine_binding_and_complete_io_child_parent_join(self):
        plan,answer,diag,narrow,expected=self.run_binding()
        self.assertEqual(answer['status'],'consistent_pending_composition',answer)
        self.assertEqual(len(diag['binding_events']),2)
        self.assertEqual(diag['binding_events'][1]['event'],'a6700.synthetic.binding_validated')
        self.assertEqual(json.loads(diag['binding_events'][1]['args'][0]),expected)
        self.assertTrue(diag['callbacks_closed'] and diag['callback_lease_closed'])
        self.assertFalse(diag['preparation_failed']);self.assertEqual(narrow['host_exit_code'],0)
        self.assertEqual(narrow['adapter_snapshot']['status'],'complete')
        self.assertEqual(narrow['adapter_snapshot']['preparation_attempts'],1)
        self.assertEqual(len(diag['protected_aliases_loaded']),3)
        self.assertEqual(len(diag['io_boundary']['constants_reads']),1)
        events=diag['io_boundary']['events'];ops=[v['op'] for v in events]
        self.assertEqual((ops.count('open'),ops.count('seek'),ops.count('close_returned')),(2,2,2))
        self.assertEqual(sum(v['returned'] for v in events if v['op']=='read'),4*plan['context']['source_manifest']['bytes'])

    def test_hash_mismatch_reaches_genuine_binding_validator(self):self.assert_binding_refused('source_hash','source_hash_mismatch')
    def test_rebound_import_drift_refuses_against_captured_contract(self):self.assert_binding_refused('import_drift','import_closure_mismatch')
    def test_qualified_role_mismatch_refuses(self):self.assert_binding_refused('qualified_role','qualified_role_mismatch')
    def test_occupied_protected_alias_refuses(self):self.assert_binding_refused('occupied_role','alias_occupied')
    def test_tools_descendant_alias_refuses(self):self.assert_binding_refused('occupied_tools','alias_occupied')
    def test_crypto_descendant_alias_refuses(self):self.assert_binding_refused('occupied_crypto','alias_occupied')
    def test_duplicate_alias_input_refuses(self):self.assert_binding_refused('duplicate_alias','invalid_shape')
    def test_load_order_result_fault_refuses_in_genuine_host(self):self.assert_binding_refused('load_order',order='load_order')
    def test_protected_order_result_fault_refuses_in_genuine_host(self):self.assert_binding_refused('protected_order',order='protected_order')


if __name__=='__main__':unittest.main(verbosity=2)
