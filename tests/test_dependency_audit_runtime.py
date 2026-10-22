"""Original audit/startup/callback methods in disposable invented-file children.

Python audit delivery is genuine. Bootstrap, native events/loader, vector cipher
and protected processing stay simulated; no installed input or camera is read.
"""
import sys
import unittest

from dependency_audit_runtime_fixture import audit_runtime_source
from dependency_filesystem_runtime_fixture import filesystem_runtime_source
import test_dependency_filesystem_runtime as filesystem
import test_dependency_runtime_route as route


def audit_child_suffix(mode):
    original=filesystem_runtime_source('complete')
    raw=filesystem.filesystem_child_suffix('complete')
    if not raw.startswith(original):raise AssertionError('synthetic audit source drift')
    raw=audit_runtime_source(mode)+raw[len(original):]
    old=b"\nSYNTHETIC_MODE='complete'\n"
    if raw.count(old)!=1:raise AssertionError('synthetic audit mode source drift')
    raw=raw.replace(old,b'\nSYNTHETIC_MODE='+repr(mode).encode()+b'\n')
    old=b'filesystem_runtime=None if runtime_owner is None else runtime_owner.filesystem_observation(),'
    if raw.count(old)!=1:raise AssertionError('synthetic audit diagnostic source drift')
    return raw.replace(old,old+b'\n  audit_runtime=None if runtime_owner is None else runtime_owner.audit_observation(),')


OBSERVATIONS=[]


@unittest.skipUnless(sys.platform=='win32','retained Windows filesystem contract')
class AuditRuntimeTests(unittest.TestCase):
    setUpClass=classmethod(filesystem.FilesystemRuntimeTests.setUpClass.__func__)
    emergency_reap=filesystem.FilesystemRuntimeTests.emergency_reap
    fixture=filesystem.FilesystemRuntimeTests.fixture

    def configure_case(self,case,inputs,terminal,mode):
        filesystem.FilesystemRuntimeTests.configure_case(self,case,inputs,terminal,'complete')
        case.fixture_child_suffix=audit_child_suffix(mode)

    def run_audit(self,mode='complete'):
        before=len(filesystem.OBSERVATIONS)
        values=filesystem.FilesystemRuntimeTests.run_filesystem(self,mode)
        row=filesystem.OBSERVATIONS.pop();self.assertEqual(len(filesystem.OBSERVATIONS),before)
        OBSERVATIONS.append(row)
        plan,answer,diag,narrow,inputs=values
        observed=diag['audit_runtime'];guard=observed['guard_final']
        self.assertTrue(observed['original_methods_intact'])
        self.assertEqual((observed['startup_calls'],observed['startup_returns']),(1,1))
        self.assertTrue(observed['original_startup_delegated'])
        startup=observed['startup_value'];independent=diag['observed']
        for name in ('isolated','no_site','no_user_site','no_bytecode'):
            self.assertIs(startup[name],True,name);self.assertEqual(startup[name],bool(independent[name]))
        self.assertEqual(startup['preloaded_package_aliases'],[])
        self.assertEqual(startup['bootstrap_boundary'],['interpreter','stdlib','_ctypes','os_loader'])
        self.assertEqual((observed['observer_install_attempts'],observed['observer_install_returns']),(1,1))
        self.assertFalse(observed['observer_enabled']);self.assertTrue(observed['observer_retained_inert'])
        self.assertFalse(observed['suppression_enabled']);self.assertFalse(observed['hooks_removed'])
        self.assertFalse(guard['active']);self.assertTrue(guard['finished'])
        self.assertEqual(observed['cleanup_errors'],[])
        post=observed['after_cleanup_probe']
        self.assertEqual((post['attempts'],post['delegations']),(1,1))
        self.assertTrue(post['returned'] and post['count_unchanged'])
        self.assertEqual(post['count_before'],post['count_after']);self.assertIsNone(post['error_type'])
        self.assertEqual(post['count_after'],guard['probe_count'])
        monitor=observed['probe_monitor'];after=[v for v in monitor if v['phase']=='after_cleanup']
        self.assertEqual(len(after),1)
        self.assertFalse(after[0]['active']);self.assertTrue(after[0]['finished'])
        self.assertFalse(after[0]['token_matches'])
        self.assertEqual(after[0]['count_before'],guard['probe_count'])
        for label,count in (('audit_install',observed['install_delegations']),
                            ('audit_probe',observed['probe_delegations']),
                            ('callback',observed['callback_delegations'])):
            self.assertEqual(observed['original_'+label+'_delegated'],count>0,label)
        self.assertEqual(observed['camera_commands'],[])
        for key in ('actual_runtime_verified','installed_dependency_observed','native_execution_performed',
                    'real_cryptography_performed','execution_authorized','feature_supported',
                    'recovery_proven','device_write_gate_passed'):
            self.assertIs(observed[key],False,key)
        self.assertEqual(diag['filesystem_runtime']['faults'],[])
        return values

    def test_original_audit_startup_callback_and_parent_join(self):
        plan,answer,diag,narrow,inputs=self.run_audit()
        route.RuntimeRouteTests.assert_complete_child(self,diag,narrow,inputs)
        self.assertEqual(answer['status'],'consistent_pending_composition',answer)
        observed=diag['audit_runtime'];guard=observed['guard_final']
        self.assertEqual((observed['install_calls'],observed['install_delegations'],observed['install_returns']),(1,1,1))
        self.assertEqual((observed['probe_calls'],observed['probe_delegations'],observed['probe_returns']),(1,1,1))
        self.assertEqual((observed['callback_calls'],observed['callback_delegations'],observed['callback_returns']),(1,1,1))
        self.assertEqual(guard['probe_count'],1);self.assertFalse(guard['failed'])
        self.assertFalse(guard['bootstrap']);self.assertEqual(observed['suppression_count'],0)
        production=[v for v in observed['probe_monitor'] if v['phase']=='production']
        self.assertEqual(len(production),1);self.assertTrue(production[0]['token_matches'])
        self.assertEqual(production[0]['count_before'],0);self.assertTrue(production[0]['active'])
        self.assertEqual(len(diag['filesystem_runtime']['reads']),398)

    def assert_audit_refused(self,mode,code,*,count=0,failed=False,delegations=1,install=1):
        plan,answer,diag,narrow,inputs=self.run_audit(mode)
        observed=diag['audit_runtime'];guard=observed['guard_final']
        self.assertEqual(answer['status'],'needs_review',answer)
        self.assertEqual(diag['failure_code'],code)
        self.assertFalse((plan['folder']/'outer-child.json').exists())
        self.assertTrue(diag['preparation_started']);self.assertFalse(diag['preparation_failed'])
        self.assertFalse(diag['callbacks_claimed']);self.assertTrue(diag['callbacks_closed'])
        self.assertEqual(diag['io_boundary']['events'],[]);self.assertEqual(diag['io_boundary']['constants_reads'],[])
        self.assertEqual(diag['runtime_route']['fake_loader_calls'],0)
        self.assertEqual(diag['runtime_route']['fake_callback_calls'],0)
        self.assertEqual((observed['callback_calls'],observed['callback_delegations'],observed['callback_returns']),(0,0,0))
        self.assertEqual(observed['install_calls'],1);self.assertEqual(observed['install_delegations'],install)
        self.assertEqual(observed['probe_delegations'],delegations)
        self.assertEqual(guard['probe_count'],count);self.assertIs(guard['failed'],failed)
        self.assertTrue(guard['bootstrap'])
        self.assertEqual(len(diag['filesystem_runtime']['reads']),361)
        sequences={
            'suppressed_install':[(True,0,False)],
            'missing_probe':[], 'install_error':[], 'probe_error':[],
            'wrong_probe':[(False,0,False)],
            'duplicate_probe':[(True,0,False),(True,1,False)],
            'swallowed_probe':[(False,0,False),(True,0,True)],
        }
        production=[v for v in observed['probe_monitor'] if v['phase']=='production']
        self.assertEqual([(v['token_matches'],v['count_before'],v['failed']) for v in production],sequences[mode])
        self.assertTrue(all(v['active'] and v['bootstrap'] and not v['finished'] for v in production))
        return observed

    def test_suppressed_original_registration_refuses(self):
        observed=self.assert_audit_refused('suppressed_install','audit_not_acknowledged')
        self.assertEqual(observed['suppression_count'],1)
        self.assertEqual(observed['install_returns'],1)
        self.assertTrue(observed['suppressor_retained_inert'])

    def test_missing_probe_refuses(self):
        self.assert_audit_refused('missing_probe','audit_not_acknowledged',delegations=0)

    def test_wrong_token_refuses(self):
        self.assert_audit_refused('wrong_probe','audit_probe',failed=True)

    def test_duplicate_probe_refuses(self):
        self.assert_audit_refused('duplicate_probe','audit_probe',count=1,failed=True,delegations=2)

    def test_swallowed_invalid_then_valid_probe_stays_failed(self):
        self.assert_audit_refused('swallowed_probe','audit_not_acknowledged',count=1,failed=True,delegations=2)

    def test_install_interruption_refuses(self):
        self.assert_audit_refused('install_error','synthetic_audit_install_error',delegations=0,install=0)

    def test_probe_interruption_refuses(self):
        self.assert_audit_refused('probe_error','synthetic_audit_probe_error',delegations=0)


if __name__=='__main__':unittest.main(verbosity=2)
