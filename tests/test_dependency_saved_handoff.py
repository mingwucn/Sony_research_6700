"""Real saved-reconciliation chain, invented disk records and process facts.

The nominal saved-record grammar is produced with FakeOps over invented package
bytes, cipher vectors and import sources. No installed/native input is opened.
No genuine supervisor success is asserted: process facts and the terminal child
envelope are explicit fixture data. This qualifies rereads/bindings/ownership,
not producer truth, target execution or acceptance of actual GDT observations.
"""
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

from tools import dependency_operational_launcher as parent
from tools import dependency_producer as producer
from tools import dependency_execution as execution
from tools import dependency_evidence as evidence
from tools import dependency_invented as invented
import test_dependency_joined_handoff as joined
from test_dependency_isolated_handoff import DISK_IO
from test_dependency_package_preflight import complete_fixture


OBSERVATIONS=[]


class SavedHandoffTests(unittest.TestCase):
    def setUp(self):
        self.case=getattr(self,'fixture_case',None) or joined.JoinedHandoffTests(
            'test_joined_real_preflight_context_control_and_helper_handoff')
        self.case.fixture_ordinary_io=DISK_IO
        self.case.setUp();self.addCleanup(self.case.doCleanups)
        case=self.case
        self.plan=parent.prepare_synthetic_owned(folder=case.folder,packet=case.packet,
            buffers=case.buffers,rows=case.rows,expected_hashes=case.expected,
            runtime_profile=getattr(self,'fixture_runtime_profile',{'executable':sys.executable}))
        plan=self.plan
        helpers=parent.process.helper_owner(plan['outer'],case.buffers,case.rows,'parent')
        plan.update(helpers=helpers,control=case.checker)
        self.addCleanup(lambda:parent.process.close_owned((helpers,plan['adapter'],plan['outer'])))
        dep={name:case.buffers['dependency.'+name] for name in parent.process.DEPENDENCIES[:-1]}
        dep['closure_manifest']=parent.encoded(plan['prepared']['sources'])
        inputs=helpers.package.dependency_execution.bind_runtime_packet(
            plan['prepared']['dependency_packet'],plan['prepared']['dependency_fixed'],dep,
            plan['prepared']['dependency_review_sha256'])
        plan['inputs']=inputs
        _,ops=complete_fixture()
        ops.policy=inputs['expectation']
        helper=types.ModuleType(invented.HELPER);helper.new=ops.new
        folder=Path(plan['prepared']['folder']);folder.mkdir()
        # No concrete RuntimeOps object, native loader or actual package exists.
        with patch.dict(sys.modules,{invented.HELPER:helper,'ctypes':ops.modules['ctypes']}), \
             patch.object(producer.RuntimeOps,'__init__',side_effect=AssertionError('actual observer')):
            execution._produce_collected(inputs=inputs,ops=ops,folder=folder/'collected',invented=False)
        self.fake_ops=ops
        self.stdout=producer.encoded(dict(script_exit_code=0,invented_saved_handoff=True))
        operation=plan['prepared']['operation_id']
        self.write(folder/'started.json',dict(schema='collected_controller_started_v1',operation_id=operation,
            expectation_sha256=evidence._hash(inputs['expectation']),test_injection_used=False,
            automatic_retry=False,protected_input_authorized=False,camera_commands=[]))
        self.write(folder/'controller-result.json',dict(code=0,summary=json.loads(self.stdout),
            test_injection_used=False,camera_commands=[]))
        completion=json.loads((folder/'collected/completion.json').read_bytes())
        self.write(folder/'completion.json',dict(schema='collected_controller_completion_v1',
            status='collected_controller_complete',controller_entered=True,callback_released=True,
            dependency_completion_sha256=evidence._hash(completion),test_injection_used=False,
            automatic_retry=False,actual_dependency_observation_performed=True,
            execution_authorized=False,feature_supported=False,recovery_proven=False,
            device_write_gate_passed=False,camera_commands=[]))
        self.write(plan['context']['session_dir']/'actual-stdout.txt',self.stdout)
        self.preflight=parent.encoded(plan['preflight'])
        self.write(plan['folder']/'pending-preflight.json',self.preflight)
        dependency=execution.validate_saved_composition(folder/'collected',inputs,invented=False)
        bridge={name:producer.sha((folder/name).read_bytes()) for name in ('completion.json','controller-result.json')}
        self.terminal=dict(schema='disabled_operational_outer_child_v1',operation_id=operation,
            status='complete_pending_composition',preflight_sha256=parent.sha(self.preflight),
            request_sha256=plan['packet']['request_sha256'],
            evidence=dict(dependency_sha256=dependency,bridge_sha256=bridge,stdout_sha256=parent.sha(self.stdout)),
            preparation_closed=True,helpers_closed=True,adapter_closed=True,callback_closed=True,
            execution_authorized=False,feature_supported=False,recovery_proven=False,
            device_write_gate_passed=False,camera_commands=[])
        self.write(plan['folder']/'outer-child.json',self.terminal)
        # Exact process grammar, but not observed OS facts in these tests.
        from tools import dependency_adapter_binding as adapter
        process=dict.fromkeys(adapter.PROCESS_BOOLS,False)
        process.update(launch_attempts=1,child_exit_code=0,deadline_seconds=300,
            kill_attempts=0,wait_attempts=0,elapsed_seconds=0.125,
            exit_observed=True,reader_threads_joined=True,pipe_close_complete=True)
        self.narrow=dict(host_exit_code=0,terminal_records_agree=True,
            process_observation=process,stdout_sha256=parent.sha(self.stdout))

    def write(self,path,value):
        self.assertTrue(Path(path).is_relative_to(self.case.root))
        raw=value if type(value) is bytes else parent.encoded(value)
        with Path(path).open('xb') as stream:stream.write(raw)

    def rewrite(self,path,value):
        self.assertTrue(Path(path).is_relative_to(self.case.root))
        Path(path).write_bytes(value if type(value) is bytes else parent.encoded(value))

    def reconcile(self):
        with patch.object(producer.RuntimeOps,'__init__',side_effect=AssertionError('actual observer')):
            answer=parent._reconcile(self.plan,self.narrow)
        OBSERVATIONS.append(dict(test=self.id(),result=answer,fake_loader_calls=self.fake_ops.loader_calls,
            process_facts_injected=True,genuine_supervisor_success=False,camera_commands=[]))
        return answer

    def test_full_saved_chain_rereads_original_preflight_and_real_helper_metadata(self):
        answer=self.reconcile()
        self.assertEqual(answer['side'],'parent')
        self.assertEqual(answer['engine_result']['status'],'consistent_saved_controller')
        for key in ('actual_runtime_verified','historical_truth_verified','producer_execution_authenticated',
                    'operational_acceptance','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(answer['engine_result'][key],False,key)
        self.assertTrue(self.plan['helpers'].closed);self.assertTrue(self.plan['adapter'].closed)
        self.assertFalse(self.plan['outer'].closed);self.plan['outer'].intact()

    def test_genuine_supervisor_needs_review_cannot_be_promoted_to_saved_success(self):
        self.narrow.update(host_exit_code=1,terminal_records_agree=False)
        read_source=parent.entry.read_source;seen=[]
        forbidden={self.plan['folder']/'outer-child.json',self.plan['folder']/'pending-preflight.json'}
        def guarded_read(path,*args,**kwargs):
            self.assertNotIn(Path(path),forbidden,'terminal evidence read after incomplete supervision')
            seen.append(Path(path))
            return read_source(path,*args,**kwargs)
        with patch.object(parent.entry,'read_source',side_effect=guarded_read), \
             patch.object(self.plan['control'],'read_ordinary',side_effect=AssertionError('saved stdout read')):
            with self.assertRaisesRegex(ValueError,'operational_launch_supervision_incomplete'):
                self.reconcile()
        expected=[self.plan['request_path'],Path(self.plan['request']['packet']['path'])]
        expected.extend(Path(row['path']) for row in self.plan['request']['sources'].values())
        self.assertEqual(seen,expected)
        self.assertFalse(self.plan['helpers'].closed);self.assertFalse(self.plan['adapter'].closed)

    def test_changed_stdout_refuses_before_parent_ownership_transfer(self):
        self.rewrite(self.plan['context']['session_dir']/'actual-stdout.txt',self.stdout+b' ')
        with self.assertRaisesRegex(ValueError,'operational_launch_stdout'):self.reconcile()
        self.assertFalse(self.plan['helpers'].closed);self.assertFalse(self.plan['adapter'].closed)

    def test_rehashed_false_preflight_claim_refuses_and_closes_transferred_owners(self):
        saved=json.loads(self.preflight);saved['execution_authorized']=True
        altered=parent.encoded(saved);self.rewrite(self.plan['folder']/'pending-preflight.json',altered)
        self.terminal['preflight_sha256']=parent.sha(altered)
        self.rewrite(self.plan['folder']/'outer-child.json',self.terminal)
        with self.assertRaisesRegex(ValueError,'operational_saved_preflight'):self.reconcile()
        self.assertTrue(self.plan['helpers'].closed);self.assertTrue(self.plan['adapter'].closed)
        self.plan['outer'].intact()

    def test_changed_collected_metadata_refuses_in_real_parent_helper(self):
        path=Path(self.plan['prepared']['folder'])/'collected/producer/raw.json'
        self.rewrite(path,path.read_bytes()+b' ')
        with self.assertRaises(ValueError):self.reconcile()
        self.assertTrue(self.plan['helpers'].closed);self.assertTrue(self.plan['adapter'].closed)
        self.plan['outer'].intact()

    def test_incomplete_process_cleanup_refuses_in_joined_adapter_and_closes_owners(self):
        self.narrow['process_observation']['pipe_close_complete']=False
        with self.assertRaisesRegex(ValueError,'adapter_process_incomplete'):self.reconcile()
        self.assertTrue(self.plan['helpers'].closed);self.assertTrue(self.plan['adapter'].closed)
        self.plan['outer'].intact()

    def test_saved_bridge_authority_promotion_refuses_after_coherent_hash_update(self):
        folder=Path(self.plan['prepared']['folder']);path=folder/'completion.json'
        value=json.loads(path.read_bytes());value['execution_authorized']=True
        self.rewrite(path,value)
        self.terminal['evidence']['bridge_sha256']['completion.json']=parent.sha(path.read_bytes())
        self.rewrite(self.plan['folder']/'outer-child.json',self.terminal)
        with self.assertRaisesRegex(ValueError,'parent_completion'):self.reconcile()
        self.assertTrue(self.plan['helpers'].closed);self.assertTrue(self.plan['adapter'].closed)


if __name__=='__main__':unittest.main()
