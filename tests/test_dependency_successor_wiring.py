"""Closed runtime-shaped dispatch with invented packets and observers forbidden."""
import copy
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

from tools import dependency_successor_wiring as subject
from tools import dependency_controller as controller
from tools import dependency_execution as execution
from tools import dependency_evidence as core
from test_dependency_package_preflight import complete_fixture


class SuccessorWiringTests(unittest.TestCase):
    def setUp(self):
        self.data, _ = complete_fixture()
        self.call = Mock(return_value=object())
        self.helpers = types.SimpleNamespace(mode='child', intact=Mock(),
            package=types.SimpleNamespace(dependency_execution=execution,
                                          dependency_controller=types.SimpleNamespace(_run=self.call)))
        self.packet = dict(schema='runtime_dependency_packet_v1', inputs={k:v for k,v in self.data.items() if k!='source_buffers'})
        policy = self.data['expectation']
        self.fixed = dict(expectation_sha256=core._hash(policy),package_sha256=core._hash(self.data['package']),
                          root_sha256={k:r['identity_sha256'] for k,r in policy['roots'].items()})
        self.closes = Mock(return_value=True)
        self.kw = dict(helpers=self.helpers,packet=self.packet,fixed=self.fixed,
            source_buffers=self.data['source_buffers'],review_sha256=self.data['binding']['review_sha256'],
            folder=object(),control=object(),context=dict(operation_id=policy['operation_id']),
            records=types.SimpleNamespace(close=self.closes),make_callbacks_after_receipt=Mock(),
            release_callbacks_after_controller=Mock(),monotonic=Mock(),identity=dict(operation_id=policy['operation_id']))
        # Startup grammar qualification only; no runtime activation on any host.
        self.profile = types.SimpleNamespace(implementation=types.SimpleNamespace(name='cpython'),platform='win32',
            flags=types.SimpleNamespace(isolated=1,no_site=1,no_user_site=1,optimize=0),dont_write_bytecode=True,modules={})
        self.profile_patch = patch.object(subject,'sys',self.profile)
        self.profile_patch.start(); self.addCleanup(self.profile_patch.stop)

    def dispatch(self):
        return subject._dispatch_runtime(**self.kw)

    def test_exact_internal_runtime_call_no_ops_or_second_owner(self):
        answer = self.dispatch()
        args = self.call.call_args.kwargs
        self.assertIs(answer,self.call.return_value)
        self.assertIs(args['records'],self.kw['records'])
        self.assertIs(args['make_callbacks_after_receipt'],self.kw['make_callbacks_after_receipt'])
        self.assertIs(args['invented'],False)
        self.assertNotIn('ops',args)
        self.assertEqual(args['inputs'],self.data)
        self.closes.assert_not_called()

    def test_completion_uses_fixed_saved_runtime_grammar_without_activating(self):
        producer=types.SimpleNamespace(read_verified=Mock(return_value=(b'invented bridge',{})))
        saved=Mock(return_value={'invented':'dependency hashes'})
        helpers=types.SimpleNamespace(mode='child',intact=Mock(),package=types.SimpleNamespace(
            dependency_execution=types.SimpleNamespace(validate_saved_composition=saved),
            dependency_producer=producer))
        control=types.SimpleNamespace(encoded=Mock(return_value=b'{"script_exit_code":0}\n'))
        result=subject._collect_completion(helpers=helpers,folder=Path('invented'),inputs=self.data,
            answer={'callback_result':(0,{'script_exit_code':0})},control=control)
        saved.assert_called_once_with(Path('invented/collected'),self.data,invented=False)
        self.assertEqual(producer.read_verified.call_count,2)
        self.assertEqual(set(result['bridge_sha256']),{'completion.json','controller-result.json'})
        self.assertEqual(result['stdout'],b'{"script_exit_code":0}\n')
        self.assertEqual(helpers.intact.call_count,2)

    def test_completion_rejects_parent_before_saved_reads(self):
        helpers=types.SimpleNamespace(mode='parent',package=Mock())
        with self.assertRaisesRegex(ValueError,'successor_helper_mode'):
            subject._collect_completion(helpers=helpers,folder=None,inputs=None,answer=None,control=None)
        self.assertEqual(helpers.package.mock_calls,[])

    def test_primary_or_unknown_controller_failure_not_retried_or_closed_by_wiring(self):
        error = KeyboardInterrupt('unknown completion')
        self.call.side_effect = error
        with self.assertRaises(KeyboardInterrupt) as caught:self.dispatch()
        self.assertIs(caught.exception,error);self.call.assert_called_once();self.closes.assert_not_called()
        self.kw['release_callbacks_after_controller'].assert_not_called()

    def test_observer_and_mode_injection_rejected_by_signature(self):
        for extra in ('ops','invented','continuation','backend'):
            with self.subTest(extra=extra),self.assertRaises(TypeError):
                subject._dispatch_runtime(**self.kw,**{extra:object()})
        self.call.assert_not_called();self.closes.assert_not_called()

    def test_startup_mismatch_before_helper_or_packet_access(self):
        for attr,value in (('platform','linux'),('dont_write_bytecode',False)):
            with self.subTest(attr=attr),patch.object(self.profile,attr,value),self.assertRaisesRegex(ValueError,'^successor_startup$'):
                self.dispatch()
        for name in ('isolated','no_site','no_user_site','optimize'):
            with self.subTest(name=name),patch.object(self.profile.flags,name,1 if name=='optimize' else 0),self.assertRaisesRegex(ValueError,'^successor_startup$'):
                self.dispatch()
        self.helpers.intact.assert_not_called();self.call.assert_not_called()

    def test_preloaded_crypto_alias_refused(self):
        for name in ('Crypto','Crypto.Cipher','Cryptodome','Cryptodome.Cipher.AES'):
            self.profile.modules={name:object()}
            with self.assertRaisesRegex(ValueError,'^successor_preloaded$'):self.dispatch()
        self.call.assert_not_called()

    def test_parent_helper_refused_before_packet_binding(self):
        self.helpers.mode='parent'
        with self.assertRaisesRegex(ValueError,'^successor_helper_mode$'):self.dispatch()
        self.call.assert_not_called()

    def test_packet_mode_extra_observer_or_wrong_review_refused_before_records(self):
        mutations=[lambda:self.packet.update(schema='invented_dependency_packet_v1'),
            lambda:self.packet['inputs'].update(ops={}),lambda:self.kw.update(review_sha256='0'*64)]
        for change in mutations:
            self.packet=copy.deepcopy(dict(schema='runtime_dependency_packet_v1',inputs={k:v for k,v in self.data.items() if k!='source_buffers'}))
            self.kw['packet']=self.packet;self.kw['review_sha256']=self.data['binding']['review_sha256'];change()
            with self.assertRaises(ValueError):self.dispatch()
        self.call.assert_not_called();self.closes.assert_not_called()

    def test_fixed_root_or_package_mismatch_refused(self):
        for key in ('root_sha256','package_sha256','expectation_sha256'):
            fixed=copy.deepcopy(self.fixed)
            if key=='root_sha256':fixed[key][next(iter(fixed[key]))]='0'*64
            else:fixed[key]='0'*64
            self.kw['fixed']=fixed
            with self.assertRaisesRegex(ValueError,'fixed_expectations'):self.dispatch()
        self.call.assert_not_called();self.closes.assert_not_called()

    def test_operation_mismatch_keeps_caller_ownership(self):
        self.kw['identity']['operation_id']='different'
        with self.assertRaisesRegex(ValueError,'^successor_operation$'):self.dispatch()
        self.call.assert_not_called();self.closes.assert_not_called()

    def test_real_controller_pre_reservation_failure_keeps_records(self):
        self.helpers.package.dependency_controller=controller
        self.kw['control']=types.SimpleNamespace(verify_context=lambda context:False)
        with self.assertRaisesRegex(ValueError,'controller_context'):self.dispatch()
        self.closes.assert_not_called()

    def test_real_controller_post_reservation_failure_closes_once_without_observer(self):
        self.helpers.package.dependency_controller=controller
        self.kw['control']=types.SimpleNamespace(verify_context=lambda context:True)
        with tempfile.TemporaryDirectory() as folder:
            self.kw['folder']=Path(folder)/'attempt'
            with patch.object(execution,'_produce_collected_runtime',side_effect=KeyboardInterrupt('synthetic stop')) as collect:
                with self.assertRaises(KeyboardInterrupt):self.dispatch()
                collect.assert_called_once()
                self.assertEqual(set(collect.call_args.kwargs),{'inputs','folder','continuation'})
            self.closes.assert_called_once_with()
            completion=json.loads((self.kw['folder']/'completion.json').read_text())
            self.assertEqual(completion['status'],'needs_review')
            self.assertIs(completion['actual_dependency_observation_completed'],False)
            self.assertIs(completion['automatic_retry'],False)

    def test_parent_saved_record_mode_has_no_invented_selector(self):
        verify=Mock(return_value=object())
        helper=types.SimpleNamespace(mode='parent',verify=verify)
        args={k:object() for k in ('folder','inputs','operation_id','stdout','stdout_sha256','dependency_sha256','bridge_sha256')}
        answer=subject._verify_saved_runtime(helpers=helper,**args)
        verify.assert_called_once_with(**args,invented=False)
        self.assertIs(answer,verify.return_value)

    def test_public_runtime_always_refuses(self):
        with self.assertRaisesRegex(ValueError,'^real_activation_pending$'):subject.run_runtime(helpers=object())
        self.assertEqual(subject.main(),2)


if __name__ == '__main__':
    unittest.main()
