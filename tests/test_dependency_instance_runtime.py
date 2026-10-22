"""Genuine RuntimeOps instances with explicit inert dependency adapters.

All filesystem data, native events, cipher and protected inputs are invented.
The bootstrap adapter is not evidence of actual dependency initialization.
"""
import sys
import unittest

from dependency_audit_runtime_fixture import audit_runtime_source
from dependency_instance_runtime_fixture import instance_runtime_source
import test_dependency_audit_runtime as audit
import test_dependency_filesystem_runtime as filesystem
import test_dependency_runtime_route as route


def instance_child_suffix(mode):
    previous=audit_runtime_source('complete')
    raw=audit.audit_child_suffix('complete')
    if not raw.startswith(previous):raise AssertionError('synthetic instance audit source drift')
    raw=instance_runtime_source(mode)+raw[len(previous):]
    old=b"\nSYNTHETIC_MODE='complete'\n"
    if raw.count(old)!=1:raise AssertionError('synthetic instance mode source drift')
    raw=raw.replace(old,b'\nSYNTHETIC_MODE='+repr(mode).encode()+b'\n')
    old=b'audit_runtime=None if runtime_owner is None else runtime_owner.audit_observation(),'
    if raw.count(old)!=1:raise AssertionError('synthetic instance diagnostic source drift')
    return raw.replace(old,old+b'\n  instance_runtime=None if runtime_owner is None else runtime_owner.instance_observation(),')


OBSERVATIONS=[]


@unittest.skipUnless(sys.platform=='win32','retained Windows filesystem contract')
class InstanceRuntimeTests(unittest.TestCase):
    setUpClass=classmethod(filesystem.FilesystemRuntimeTests.setUpClass.__func__)
    emergency_reap=filesystem.FilesystemRuntimeTests.emergency_reap
    fixture=filesystem.FilesystemRuntimeTests.fixture

    def configure_case(self,case,inputs,terminal,mode):
        filesystem.FilesystemRuntimeTests.configure_case(self,case,inputs,terminal,'complete')
        case.fixture_child_suffix=instance_child_suffix(mode)

    def run_instance(self,mode='complete'):
        before=len(audit.OBSERVATIONS)
        values=audit.AuditRuntimeTests.run_audit(self,mode)
        row=audit.OBSERVATIONS.pop();self.assertEqual(len(audit.OBSERVATIONS),before)
        OBSERVATIONS.append(row)
        plan,answer,diag,narrow,inputs=values
        observed=diag['instance_runtime']
        for key in ('exact_original_type','no_class_inheritance','no_fake_ops_observer',
                    'no_fallback_attributes','original_class_methods_intact',
                    'original_delegates_use_exact_instance'):
            self.assertIs(observed[key],True,key)
        names=sorted(('reader','root','startup','audit_install','audit_probe','callback','bootstrap'))
        self.assertEqual(observed['ops_instance_attributes'],names)
        self.assertEqual(observed['expected_instance_attributes'],names)
        self.assertEqual(observed['bootstrap_calls'],1)
        self.assertFalse(observed['bootstrap_original_method_called'])
        self.assertFalse(observed['callback_active'])
        for key in ('explicit_inert_adapter','native_events_are_direct_simulation',
                    'vector_cipher_is_lookup','constructor_binding_remains_synthetic','class_source_unchanged'):
            self.assertIs(observed[key],True,key)
        delegates=observed['original_delegations']
        self.assertTrue(all(row['bound_original_instance'] for row in delegates))
        self.assertNotIn('bootstrap',[row['method'] for row in delegates])
        counts={name:sum(row['method']==name for row in delegates) for name in names}
        self.assertEqual(counts['reader'],observed['reads'])
        self.assertEqual(counts['root'],observed['root_calls'])
        self.assertEqual(counts['reader'],len(diag['filesystem_runtime']['reads']))
        self.assertEqual(counts['root'],len(diag['filesystem_runtime']['roots']))
        self.assertEqual((counts['startup'],counts['audit_install'],counts['audit_probe']),(1,1,2))
        self.assertEqual(counts['callback'],diag['audit_runtime']['callback_delegations'])
        self.assertEqual(observed['callback_calls'],diag['audit_runtime']['callback_calls'])
        self.assertEqual(observed['camera_commands'],[])
        for key in ('actual_runtime_verified','installed_dependency_observed','native_execution_performed',
                    'real_cryptography_performed','execution_authorized','feature_supported',
                    'recovery_proven','device_write_gate_passed'):
            self.assertIs(observed[key],False,key)
        self.assertEqual(diag['audit_runtime']['guard_final']['probe_count'],1)
        self.assertEqual(diag['audit_runtime']['cleanup_errors'],[])
        self.assertEqual(diag['runtime_route']['cleanup_errors'],[])
        return values

    def test_original_instance_and_parent_join(self):
        plan,answer,diag,narrow,inputs=self.run_instance()
        route.RuntimeRouteTests.assert_complete_child(self,diag,narrow,inputs)
        self.assertEqual(answer['status'],'consistent_pending_composition',answer)
        observed=diag['instance_runtime']
        self.assertEqual(observed['bootstrap_returns'],1)
        self.assertEqual((observed['loader_calls'],observed['cipher_calls'],observed['callback_calls']),(5,72,1))
        self.assertEqual((observed['direct_native_audit_calls'],observed['skipped_native_audit_calls']),(5,0))
        self.assertEqual(observed['corrupted_cipher_lookups'],0)
        self.assertEqual(observed['callback_state'],'complete')
        self.assertEqual(len(diag['filesystem_runtime']['reads']),398)
        self.assertEqual(len(diag['filesystem_runtime']['roots']),10)
        self.assertEqual(diag['audit_runtime']['callback_delegations'],1)

    def assert_instance_refused(self,mode,code):
        plan,answer,diag,narrow,inputs=self.run_instance(mode)
        self.assertEqual(answer['status'],'needs_review',answer)
        self.assertEqual(diag['failure_code'],code)
        self.assertFalse((plan['folder']/'outer-child.json').exists())
        self.assertTrue(diag['preparation_started']);self.assertFalse(diag['preparation_failed'])
        self.assertFalse(diag['callbacks_claimed']);self.assertTrue(diag['callbacks_closed'])
        self.assertEqual(diag['io_boundary']['events'],[])
        self.assertEqual(diag['io_boundary']['constants_reads'],[])
        return diag

    def test_bootstrap_interruption_closes_owners(self):
        diag=self.assert_instance_refused('bootstrap_error','synthetic_instance_bootstrap_error')
        self.assertEqual(diag['instance_runtime']['bootstrap_returns'],0)
        self.assertEqual(diag['instance_runtime']['loader_calls'],0)
        self.assertEqual(diag['audit_runtime']['callback_calls'],0)

    def test_missing_bootstrap_module_refuses(self):
        diag=self.assert_instance_refused('missing_module','shape')
        self.assertEqual(diag['instance_runtime']['bootstrap_returns'],1)
        self.assertEqual(diag['instance_runtime']['loader_calls'],0)
        self.assertEqual(diag['audit_runtime']['callback_calls'],0)

    def test_wrong_trusted_origin_refuses(self):
        diag=self.assert_instance_refused('wrong_origin','trusted_origin')
        self.assertEqual(diag['instance_runtime']['loader_calls'],0)
        self.assertEqual(diag['audit_runtime']['callback_calls'],0)

    def test_missing_simulated_native_audit_refuses(self):
        diag=self.assert_instance_refused('missing_native_audit','missing_audit')
        self.assertEqual(diag['instance_runtime']['loader_calls'],1)
        self.assertEqual(diag['instance_runtime']['direct_native_audit_calls'],0)
        self.assertEqual(diag['instance_runtime']['skipped_native_audit_calls'],1)
        self.assertEqual(diag['audit_runtime']['callback_calls'],0)

    def test_wrong_producer_cipher_result_refuses(self):
        diag=self.assert_instance_refused('wrong_cipher','vector_mismatch')
        self.assertEqual(diag['instance_runtime']['cipher_calls'],1)
        self.assertEqual(diag['instance_runtime']['cipher_fault_stage'],'producer_vectors')
        self.assertEqual(diag['instance_runtime']['corrupted_cipher_lookups'],1)
        self.assertEqual(diag['audit_runtime']['callback_calls'],0)

    def test_wrong_original_callback_cipher_result_refuses(self):
        diag=self.assert_instance_refused('callback_cipher','vector_mismatch')
        self.assertEqual(diag['audit_runtime']['callback_delegations'],1)
        self.assertEqual(diag['audit_runtime']['callback_returns'],0)
        self.assertEqual(diag['instance_runtime']['cipher_calls'],25)
        self.assertEqual(diag['instance_runtime']['cipher_fault_stage'],'original_callback')
        self.assertEqual(diag['instance_runtime']['corrupted_cipher_lookups'],1)
        self.assertEqual(diag['instance_runtime']['callback_state'],'failed')

    def test_callback_interruption_preserves_delegation_count(self):
        diag=self.assert_instance_refused('callback_error','synthetic_instance_callback_error')
        self.assertEqual(diag['audit_runtime']['callback_calls'],1)
        self.assertEqual(diag['audit_runtime']['callback_delegations'],0)
        self.assertEqual(diag['audit_runtime']['callback_returns'],0)
        self.assertEqual(diag['instance_runtime']['cipher_calls'],24)
        self.assertEqual(diag['instance_runtime']['callback_state'],'not_entered')


if __name__=='__main__':unittest.main(verbosity=2)
