"""Invented records, real prepared adapter, intercepted engine dispatch only."""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from tools import dependency_operational_entry as subject
from tools import dependency_adapter_sources as sources
from tools import dependency_execution as execution
from tools import dependency_producer as producer
from test_dependency_adapter_binding import fixture
from test_dependency_package_preflight import complete_fixture


class EntryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data, _ = complete_fixture()
        self.request, self.buffers = fixture(self.data, Path(self.tmp.name)/'composition')
        self.digest = hashlib.sha256(subject.encoded(self.request)).hexdigest()
        self.events = []
        texts = {n:Path('tools',n+'.py').read_bytes() for n in sources.ORDER}
        self.owner = sources.AdapterSources(buffers=texts,
            hashes={n:hashlib.sha256(b).hexdigest() for n,b in texts.items()})
        self.owner.load()
        self.addCleanup(lambda: None if self.owner.closed else self.owner.close())
        common = ('dependency_evidence','dependency_producer',
                  'dependency_package_preflight','dependency_execution')
        self.helper_texts = {n:self.buffers['dependency.'+n]
                             for n in common+('dependency_controller',)}
        self.helper = SimpleNamespace(mode='child',order=tuple(self.helper_texts),
            buffers=dict(self.helper_texts),intact=Mock(),close=Mock(return_value=True),
            package=SimpleNamespace(dependency_execution=execution))
        self.callbacks = Mock(return_value=('invented callbacks',))
        self.callbacks.close = Mock(return_value=None)
        self.preparation = SimpleNamespace(prepare=Mock(side_effect=self.prepare),
                                          close=Mock(return_value=True))
        self.records = SimpleNamespace(close=Mock(return_value=True))
        self.control = SimpleNamespace(reserve_child=Mock(side_effect=self.reserve))
        self.wiring = SimpleNamespace(_dispatch_runtime=Mock(side_effect=self.dispatch),
                                     _verify_saved_runtime=Mock(return_value={'saved':'intercepted'}))
        self.context = dict(operation_id=self.request['operation_id'],deadline_seconds=300,
                            limits={'poll_seconds':0.05})
        self.identity = dict(operation_id=self.request['operation_id'])
        self.guard = patch.object(producer.RuntimeOps,'__init__',
                                  side_effect=AssertionError('actual observer forbidden'))
        self.guard.start(); self.addCleanup(self.guard.stop)

    def prepare(self):
        self.events.append('metadata')
        return {'control':self.control},None,self.callbacks

    def reserve(self, *, context):
        self.events.append('reserve')
        self.assertIs(context,self.context)
        return self.records

    def dispatch(self, **kw):
        self.events.append('dispatch')
        self.assertIs(kw['control'],self.control)
        self.assertNotIn('ops',kw)
        self.assertNotIn('invented',kw)
        kw['make_callbacks_after_receipt'](object(),object(),object())
        kw['release_callbacks_after_controller']()
        kw['records'].close()
        return {'engine':'intercepted'}

    def args(self):
        return dict(request=self.request,request_sha256=self.digest,
            checked_sources=self.buffers,adapter_owner=self.owner,helpers=self.helper,
            dependency_source_buffers=self.data['source_buffers'],runtime_wiring=self.wiring,
            preparation=self.preparation,context=self.context,identity=self.identity)

    def assert_closed(self, callbacks=True, reserved=True):
        self.helper.close.assert_called_once_with()
        if reserved:self.records.close.assert_called_once_with()
        else:self.records.close.assert_not_called()
        self.preparation.close.assert_called_once_with()
        self.assertTrue(self.owner.closed)
        if callbacks:self.callbacks.close.assert_called_once_with()

    def test_child_metadata_before_dispatch_and_once_owned_lifetime(self):
        result=subject._continue_child(**self.args())
        self.assertEqual(self.events,['metadata','reserve','dispatch'])
        self.preparation.prepare.assert_called_once_with()
        self.control.reserve_child.assert_called_once_with(context=self.context)
        self.assertEqual(result['side'],'child')
        self.assertEqual(result['engine_result'],{'engine':'intercepted'})
        for key in ('execution_authorized','feature_supported','recovery_proven',
                    'device_write_gate_passed','production_runtime_qualified'):
            self.assertIs(result[key],False)
        self.assert_closed()

    def test_metadata_interrupt_never_reaches_dispatch_and_closes_all(self):
        primary=KeyboardInterrupt('metadata interrupted')
        self.preparation.prepare.side_effect=primary
        with self.assertRaises(KeyboardInterrupt) as got:
            subject._continue_child(**self.args())
        self.assertIs(got.exception,primary)
        self.wiring._dispatch_runtime.assert_not_called()
        self.control.reserve_child.assert_not_called()
        self.assert_closed(False,False)

    def test_primary_preserved_with_cleanup_failures_and_no_reclose(self):
        primary=KeyboardInterrupt('factory interrupted')
        self.callbacks.side_effect=primary
        self.callbacks.close.side_effect=OSError('cleanup')
        self.helper.close.side_effect=RuntimeError('second cleanup')
        with self.assertRaises(KeyboardInterrupt) as got:
            subject._continue_child(**self.args())
        self.assertIs(got.exception,primary)
        self.assertIsInstance(got.exception.__cause__,OSError)
        self.assert_closed()

    def test_no_callback_completion_cannot_be_reported_as_engine_success(self):
        self.wiring._dispatch_runtime.side_effect=None
        with self.assertRaisesRegex(ValueError,'operational_child_incomplete'):
            subject._continue_child(**self.args())
        self.assert_closed()

    def test_duplicate_factory_claim_refuses_and_independent_cleanup_runs(self):
        def dispatch(**kw):
            factory=kw['make_callbacks_after_receipt']
            factory(None,None,None);factory(None,None,None)
        self.wiring._dispatch_runtime.side_effect=dispatch
        with self.assertRaisesRegex(ValueError,'operational_factory_reentry'):
            subject._continue_child(**self.args())
        self.assertEqual(self.callbacks.call_count,1)
        self.assert_closed()

    def test_uncertain_record_close_is_not_retried(self):
        self.records.close.return_value=False
        with self.assertRaisesRegex(ValueError,'operational_close_unknown'):
            subject._continue_child(**self.args())
        self.assert_closed()

    def test_swallowed_callback_failure_remains_sticky(self):
        self.callbacks.side_effect=KeyboardInterrupt('callback failure')
        def dispatch(**kw):
            try:kw['make_callbacks_after_receipt'](None,None,None)
            except KeyboardInterrupt:pass
            kw['release_callbacks_after_controller']()
            kw['records'].close()
            return {'engine':'swallowed callback error'}
        self.wiring._dispatch_runtime.side_effect=dispatch
        with self.assertRaisesRegex(ValueError,'operational_child_incomplete'):
            subject._continue_child(**self.args())
        self.assert_closed()

    def test_swallowed_duplicate_factory_or_release_cannot_complete(self):
        for duplicate in ('factory','release'):
            # Each subcase needs fresh owned adapters and lifecycle state.
            case=EntryTests('test_child_metadata_before_dispatch_and_once_owned_lifetime')
            case.setUp()
            try:
                def dispatch(**kw):
                    kw['make_callbacks_after_receipt'](None,None,None)
                    kw['release_callbacks_after_controller']()
                    try:
                        if duplicate=='factory':kw['make_callbacks_after_receipt'](None,None,None)
                        else:kw['release_callbacks_after_controller']()
                    except ValueError:pass
                    kw['records'].close()
                    return {}
                case.wiring._dispatch_runtime.side_effect=dispatch
                with self.subTest(duplicate=duplicate), self.assertRaisesRegex(ValueError,'operational_child_incomplete'):
                    subject._continue_child(**case.args())
                case.assert_closed()
            finally:case.doCleanups()

    def test_request_mutation_during_metadata_refuses_before_dispatch(self):
        def prepare():
            result=self.prepare();self.request['folder']+='-changed';return result
        self.preparation.prepare.side_effect=prepare
        with self.assertRaisesRegex(ValueError,'operational_request_changed'):
            subject._continue_child(**self.args())
        self.wiring._dispatch_runtime.assert_not_called()
        self.control.reserve_child.assert_not_called()
        self.assert_closed(reserved=False)

    def test_helper_substitution_refuses_before_metadata(self):
        self.helper.buffers['dependency_producer']=b'changed\n'
        with self.assertRaisesRegex(ValueError,'operational_helper_roster'):
            subject._continue_child(**self.args())
        self.preparation.prepare.assert_not_called()
        self.control.reserve_child.assert_not_called()
        self.assert_closed(False,False)

    def test_reservation_failure_preserves_error_and_releases_prepared_callbacks(self):
        primary=OSError('exclusive reservation failed')
        self.control.reserve_child.side_effect=primary
        with self.assertRaises(OSError) as got:
            subject._continue_child(**self.args())
        self.assertIs(got.exception,primary)
        self.preparation.prepare.assert_called_once_with()
        self.control.reserve_child.assert_called_once_with(context=self.context)
        self.wiring._dispatch_runtime.assert_not_called()
        self.assert_closed(reserved=False)

    def test_bad_context_refuses_before_reservation(self):
        self.context['operation_id']='0'*32
        with self.assertRaisesRegex(ValueError,'adapter_operation'):
            subject._continue_child(**self.args())
        self.control.reserve_child.assert_not_called()
        self.wiring._dispatch_runtime.assert_not_called()
        self.assert_closed(reserved=False)

    def test_record_proxy_construction_interrupt_never_acquires_records(self):
        original=subject.OnceClose
        primary=KeyboardInterrupt('record owner allocation interrupted')
        def wrapper(value, *, strict=False):
            if strict:raise primary
            return original(value,strict=strict)
        with patch.object(subject,'OnceClose',side_effect=wrapper):
            with self.assertRaises(KeyboardInterrupt) as got:
                subject._continue_child(**self.args())
        self.assertIs(got.exception,primary)
        self.control.reserve_child.assert_not_called()
        self.wiring._dispatch_runtime.assert_not_called()
        self.assert_closed(reserved=False)

    def test_post_reservation_dispatch_interrupt_closes_acquired_records_once(self):
        primary=KeyboardInterrupt('dispatch interrupted')
        self.wiring._dispatch_runtime.side_effect=primary
        with self.assertRaises(KeyboardInterrupt) as got:
            subject._continue_child(**self.args())
        self.assertIs(got.exception,primary)
        self.control.reserve_child.assert_called_once_with(context=self.context)
        self.assert_closed()

    def test_empty_reservation_refuses_without_dispatch_or_fake_close(self):
        self.control.reserve_child.side_effect=None
        self.control.reserve_child.return_value=None
        with self.assertRaisesRegex(ValueError,'operational_reservation_empty'):
            subject._continue_child(**self.args())
        self.control.reserve_child.assert_called_once_with(context=self.context)
        self.wiring._dispatch_runtime.assert_not_called()
        self.assert_closed(reserved=False)

    def test_bad_dependency_packet_refuses_before_reservation(self):
        self.request['dependency_fixed']['expectation_sha256']='0'*64
        self.digest=hashlib.sha256(subject.encoded(self.request)).hexdigest()
        with self.assertRaises(ValueError):
            subject._continue_child(**self.args())
        self.control.reserve_child.assert_not_called()
        self.wiring._dispatch_runtime.assert_not_called()
        self.assert_closed(reserved=False)

    def parent_args(self):
        names=self.helper.order[:-1]+('dependency_parent',)
        texts={n:Path('tools',n+'.py').read_bytes() for n in names}
        self.helper.mode='parent';self.helper.order=names;self.helper.buffers=texts
        process=dict(launch_attempts=1,exit_observed=True,child_exit_code=0,
            reader_threads_joined=True,pipe_close_complete=True,timed_out=False,
            launch_failed=False,log_cap_exceeded=False,log_reader_failed=False,
            kill_succeeded=False,collector_stop_requested=True,deadline_seconds=300,
            kill_attempts=0,wait_attempts=0,elapsed_seconds=0.1)
        return dict(request=self.request,request_sha256=self.digest,
            checked_sources=self.buffers,adapter_owner=self.owner,helpers=self.helper,
            parent_source_buffers=texts,runtime_wiring=self.wiring,inputs=self.data,
            process=process,stdout=b'invented',stdout_sha256='0'*64,
            dependency_sha256={},bridge_sha256={})

    def test_parent_only_uses_saved_runtime_seam(self):
        result=subject._reconcile_parent(**self.parent_args())
        self.assertEqual(result['side'],'parent')
        self.assertEqual(result['engine_result'],{'saved':'intercepted'})
        self.wiring._dispatch_runtime.assert_not_called()
        self.wiring._verify_saved_runtime.assert_called_once()
        self.helper.close.assert_called_once();self.assertTrue(self.owner.closed)

    def test_parent_unknown_process_refuses_before_saved_record_reads(self):
        args=self.parent_args();args['process']['reader_threads_joined']=False
        with self.assertRaisesRegex(ValueError,'adapter_process_incomplete'):
            subject._reconcile_parent(**args)
        self.wiring._verify_saved_runtime.assert_not_called()
        self.helper.close.assert_called_once();self.assertTrue(self.owner.closed)

    def test_parent_owns_cleanup_even_when_saved_verifier_raises(self):
        primary=OSError('saved mismatch')
        self.wiring._verify_saved_runtime.side_effect=primary
        with self.assertRaises(OSError) as got:
            subject._reconcile_parent(**self.parent_args())
        self.assertIs(got.exception,primary)
        self.helper.close.assert_called_once();self.assertTrue(self.owner.closed)

    def test_public_runtime_and_direct_cli_refuse(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):
            subject.run_runtime(unknown=object())
        result=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8',
            str(Path(subject.__file__).resolve())],capture_output=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(result.stdout,b'')
        self.assertEqual(result.stderr,b'')


if __name__=='__main__':
    unittest.main()
