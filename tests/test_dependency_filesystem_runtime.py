"""Original filesystem readers in the isolated synthetic preparation path.

Independent parent expectations precede filesystem fault injection. Bootstrap,
native loading, guard delivery, cipher and protected processing stay invented.
No installed dependency, real native payload, firmware or camera is accessed.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest

from dependency_filesystem_fixture import materialize_filesystem_fixture
from dependency_filesystem_runtime_fixture import filesystem_runtime_source
from dependency_runtime_route_fixture import route_fixture_source
from test_dependency_package_preflight import complete_fixture
import test_dependency_runtime_route as route


def filesystem_child_suffix(mode):
    original=route_fixture_source('complete')
    raw=route.route_child_suffix('complete')
    if not raw.startswith(original):raise AssertionError('synthetic filesystem route source drift')
    raw=filesystem_runtime_source(mode)+raw[len(original):]
    old=b"\nSYNTHETIC_MODE='complete'\n"
    if raw.count(old)!=1:raise AssertionError('synthetic filesystem mode source drift')
    raw=raw.replace(old,b'\nSYNTHETIC_MODE='+repr(mode).encode()+b'\n')
    old=b'runtime_route=None if runtime_owner is None else runtime_owner.observation(),'
    if raw.count(old)!=1:raise AssertionError('synthetic filesystem observation source drift')
    return raw.replace(old,old+b'\n  filesystem_runtime=None if runtime_owner is None else runtime_owner.filesystem_observation(),')


OBSERVATIONS=[]


@unittest.skipUnless(sys.platform=='win32','retained Windows filesystem receipt contract')
class FilesystemRuntimeTests(unittest.TestCase):
    setUpClass=classmethod(route.RuntimeRouteTests.setUpClass.__func__)
    emergency_reap=route.RuntimeRouteTests.emergency_reap
    fixture=route.RuntimeRouteTests.fixture

    def configure_case(self,case,inputs,terminal,mode):
        route.RuntimeRouteTests.configure_case(self,case,inputs,terminal,'complete')
        case.fixture_child_suffix=filesystem_child_suffix(mode)
        def dependency_data(root,data):
            _,ops=complete_fixture();before=copy.deepcopy(data)
            rebound,summary=materialize_filesystem_fixture(root/'invented-dependency-files',data,ops)
            self.assertEqual(data,before)
            self.filesystem_fixture=summary
            self.expected_filesystem=copy.deepcopy(rebound)
            return rebound
        case.fixture_dependency_data=dependency_data

    def run_filesystem(self,mode='complete'):
        # Reuse real process/parent ownership and false-authority checks. The
        # shared observation is moved here so suites do not relabel each other.
        before=len(route.OBSERVATIONS)
        values=route.RuntimeRouteTests.run_route(self,mode)
        row=route.OBSERVATIONS.pop()
        self.assertEqual(len(route.OBSERVATIONS),before)
        row.update(filesystem_fixture=self.filesystem_fixture)
        OBSERVATIONS.append(row)
        plan,answer,diag,narrow,inputs=values
        observed=diag['filesystem_runtime'];runtime=diag['runtime_route']
        self.assertEqual(runtime['constructor_calls'],1)
        self.assertEqual(runtime['constructor_preloaded_roots'],[])
        for key in ('original_reader_delegated','original_root_delegated','trace_restored','fallback_bytes_and_receipts_removed'):
            self.assertIs(observed[key],True,key)
        self.assertEqual(observed['live_fds'],[])
        for key in ('installed_dependency_observed','native_execution_performed','real_cryptography_performed',
                    'actual_runtime_verified','execution_authorized','feature_supported','recovery_proven','device_write_gate_passed'):
            self.assertIs(observed[key],False,key)
        fixture=self.filesystem_fixture
        self.assertEqual((fixture['authored_files'],fixture['package_files'],fixture['trusted_files']),(356,351,5))
        self.assertEqual(len(fixture['absolute_receipts']),356)
        counters=fixture['capture_counters']
        for key in ('write_opens','write_calls','write_close_attempts','write_close_returns',
                    'read_opens','eof_returns','read_close_attempts','read_close_returns'):
            self.assertEqual(counters[key],356,key)
        self.assertEqual(counters['read_bytes'],counters['written_bytes'])
        self.assertEqual(counters['read_bytes'],fixture['total_authored_bytes'])
        for event in observed['reads']:
            path=event['path'];self.assertIn(path,fixture['absolute_receipts'])
            if event['completed']:
                expected=fixture['absolute_receipts'][path]
                self.assertEqual(event['sha256'],expected['sha256'])
                # All actual four-stamp observations must agree with the
                # independent capture; no candidate receipt is its own oracle.
                encoded=json.dumps(expected,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')
                self.assertEqual(event['receipt_sha256'],hashlib.sha256(encoded).hexdigest())
        if mode!='root_replacement':
            expected_roots={v['path']:v for v in fixture['root_receipts'].values()}
            for event in observed['roots']:
                self.assertIn(event['path'],expected_roots)
                encoded=json.dumps(expected_roots[event['path']],sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')
                self.assertEqual(event['receipt_sha256'],hashlib.sha256(encoded).hexdigest())
        events=observed['events'];ops=[v['op'] for v in events]
        self.assertEqual(ops.count('open_returned'),ops.count('close_attempt'))
        self.assertEqual(ops.count('open_returned'),ops.count('close_returned'))
        self.assertTrue(all(v['flags']&3==0 for v in events if v['op']=='open_returned'))
        return values

    def test_original_filesystem_readers_and_parent_join(self):
        plan,answer,diag,narrow,inputs=self.run_filesystem()
        route.RuntimeRouteTests.assert_complete_child(self,diag,narrow,inputs)
        self.assertEqual(answer['status'],'consistent_pending_composition',answer)
        observed=diag['filesystem_runtime'];events=observed['events']
        self.assertEqual(len(observed['reads']),398);self.assertEqual(len(observed['roots']),10)
        self.assertTrue(all(v['completed'] for v in observed['reads']))
        self.assertEqual(sum(v['op']=='open_returned' for v in events),398)
        self.assertEqual(sum(v['op']=='read_returned' and v['returned']==0 for v in events),398)
        self.assertEqual(observed['faults'],[])

    def assert_filesystem_refused(self,mode,code=None,error_type=None):
        plan,answer,diag,narrow,inputs=self.run_filesystem(mode)
        self.assertEqual(answer['status'],'needs_review',answer)
        self.assertFalse((plan['folder']/'outer-child.json').exists())
        self.assertTrue(diag['preparation_started']);self.assertFalse(diag['preparation_failed'])
        self.assertFalse(diag['callbacks_claimed']);self.assertTrue(diag['callbacks_closed'])
        self.assertEqual(diag['io_boundary']['events'],[])
        self.assertEqual(diag['io_boundary']['constants_reads'],[])
        self.assertEqual(diag['runtime_route']['fake_loader_calls'],0)
        self.assertEqual(diag['runtime_route']['fake_callback_calls'],0)
        if code is not None:self.assertEqual(diag['failure_code'],code)
        if error_type is not None:self.assertEqual(diag['failure_type'],error_type)
        self.assertEqual(len(diag['filesystem_runtime']['faults']),1)
        return diag

    def test_unused_package_bytes_drift_refuses(self):
        self.assert_filesystem_refused('unused_bytes','receipt_binding')

    def test_same_byte_replacement_refuses_identity(self):
        self.assert_filesystem_refused('same_byte_replacement','expected_identity')

    def test_missing_member_refuses_without_retry(self):
        self.assert_filesystem_refused('missing_member',error_type='FileNotFoundError')

    def test_hardlink_refuses_before_open(self):
        self.assert_filesystem_refused('hardlink','file_kind')

    def test_trusted_bytes_drift_refuses_before_bootstrap(self):
        self.assert_filesystem_refused('trusted_bytes','receipt_binding')

    def test_replaced_root_refuses_before_file_reads(self):
        diag=self.assert_filesystem_refused('root_replacement','root_identity')
        self.assertEqual(diag['filesystem_runtime']['reads'],[])
        self.assertEqual(diag['filesystem_runtime']['events'],[])

    def test_late_native_drift_refuses_on_producer_reread(self):
        diag=self.assert_filesystem_refused('late_native','receipt_binding')
        self.assertGreater(len(diag['filesystem_runtime']['reads']),356)


if __name__=='__main__':unittest.main(verbosity=2)
