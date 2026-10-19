"""Disposable Python with authored helpers and invented metadata only."""
import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch, Mock

from tools import isolated_metadata_entry as subject
from test_detached_metadata_loader import fixture

ROOT = Path(__file__).resolve().parents[1]


def runtime():
    value = subject.runtime_profile()
    value['path'] = [p for p in value['path'] if p not in
        ('', '.', 'tests', str(ROOT), str(ROOT/'tests'))]
    return value


def packet(*, body="return {'rows':VALUE['rows']}", arguments=None, extra=''):
    public, hashes = fixture(body=body, extra=extra)
    helpers = {n:(ROOT/'tools'/ (n+'.py')).read_bytes() for n in subject.HELPERS}
    return subject.make_packet(helpers=helpers, helper_hashes={n:subject.sha(v) for n,v in helpers.items()},
        public=public, public_hashes=hashes, arguments={} if arguments is None else arguments,
        runtime=runtime())


def run(raw, **kwargs):
    return subject.run_invented(packet=raw, expected_packet_sha256=subject.sha(raw), **kwargs)


def altered(raw, change):
    value=json.loads(raw);change(value);return subject.canonical(value)


class IsolatedMetadataTests(unittest.TestCase):
    def assert_refused(self, raw):
        result=run(raw)
        self.assertEqual(result['status'],'needs_review');self.assertEqual(result['exit_code'],2)
        self.assertIsNone(result['result']);self.assertTrue(result['process_reaped'])
        self.assertFalse(result['automatic_retry']);self.assertEqual(result['camera_commands'],[])
        return result

    def test_fresh_child_checks_helpers_and_composes_fake_graph(self):
        raw=packet();before=dict(sys.modules);result=run(raw)
        self.assertEqual(result['status'],'complete',result)
        value=result['result'];self.assertEqual(value['metadata_result']['metadata_result'],{'rows':[1]})
        self.assertTrue(value['no_site_observed']);self.assertTrue(value['argv_flags_bound'])
        self.assertTrue(value['loader_closed']);self.assertEqual(value['authored_aliases_after'],[])
        self.assertEqual(value['startup'],runtime());self.assertEqual(result['stderr_bytes'],0)
        self.assertTrue(all(sys.modules[n] is v for n,v in before.items()))
        self.assertFalse(value['review_authenticated']);self.assertFalse(value['stdlib_origins_verified'])

    def test_typed_wire_bytes_and_tag_like_dict_round_trip(self):
        args={'raw':b'\x00\xff', 'nested':{'bytes':'not a tag','list':[None,True,7,1.25,'字']}}
        saved=copy.deepcopy(args)
        raw=packet(body="return {'hex':kwargs['raw'].hex(),'nested':kwargs['nested']}",arguments=args)
        result=run(raw);self.assertEqual(result['status'],'complete',result)
        self.assertEqual(result['result']['metadata_result']['metadata_result'],dict(hex='00ff',nested=args['nested']))
        self.assertEqual(args,saved)

    def test_external_packet_digest_required_before_launch(self):
        with patch.object(subject.subprocess,'Popen',side_effect=AssertionError('must not launch')):
            with self.assertRaisesRegex(ValueError,'packet_digest'):
                subject.run_invented(packet=packet(),expected_packet_sha256='0'*64)

    def test_child_independently_checks_external_packet_digest(self):
        process=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',subject.BOOTSTRAP,'0'*64],
            input=packet(),capture_output=True,timeout=10)
        self.assertEqual(process.returncode,2);self.assertEqual(json.loads(process.stdout)['status'],'needs_review')
        self.assertEqual(process.stderr,b'')

    def test_helper_hash_mismatch_refuses_before_helper_execution(self):
        raw=packet()
        def change(value):
            value['helpers']['source_import_audit']['base64']='cmFpc2UgS2V5Ym9hcmRJbnRlcnJ1cHQ='
        result=self.assert_refused(altered(raw,change));self.assertEqual(result['stderr_bytes'],0)

    def test_helper_roster_origin_and_invalid_base64_refuse(self):
        changes=(lambda v:v['helpers'].pop('source_import_audit'),
            lambda v:v['helpers']['source_import_audit'].update(origin='C:/untrusted.py'),
            lambda v:v['helpers']['source_import_audit'].update(base64='!'))
        for change in changes:
            with self.subTest(change=change):self.assert_refused(altered(packet(),change))

    def test_public_roster_hash_and_origin_refuse(self):
        changes=(lambda v:v['public'].pop('dependency_candidate_context'),
            lambda v:v['public']['dependency_candidate_context'].update(sha256='0'*64),
            lambda v:v['public']['dependency_candidate_context'].update(origin='ambient'))
        for change in changes:
            with self.subTest(change=change):self.assert_refused(altered(packet(),change))

    def test_wrong_startup_path_version_and_flags_refuse(self):
        changes=(lambda v:v['runtime'].update(path=['.']),lambda v:v['runtime'].update(version=[0,0,0]),
            lambda v:v['runtime'].update(isolated=0),lambda v:v.update(bootstrap_sha256='0'*64))
        for change in changes:
            with self.subTest(change=change):self.assert_refused(altered(packet(),change))

    def test_closed_packet_mode_and_camera_refuse(self):
        changes=(lambda v:v.update(invented=False),lambda v:v.update(camera_commands=['forbidden']),
            lambda v:v.update(schema='runtime'),lambda v:v.update(path='forbidden'))
        for change in changes:
            with self.subTest(change=change):self.assert_refused(altered(packet(),change))

    def test_duplicate_key_json_refuses(self):
        raw=packet();raw=b'{"invented":true,'+raw[1:]
        with self.assertRaisesRegex(ValueError,'duplicate_key'):run(raw)
        process=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','-c',subject.BOOTSTRAP,subject.sha(raw)],
            input=raw,capture_output=True,timeout=10)
        self.assertEqual(process.returncode,2)

    def test_duplicate_argument_keys_refuse(self):
        def change(value):value['arguments']=['dict',[[['str','x'],['none',None]],[['str','x'],['none',None]]]]
        self.assert_refused(altered(packet(),change))

    def test_malformed_argument_tags_and_types_refuse(self):
        for node in (['pickle','abc'],['int',True],['bytes','!'],['none',False],['dict',[[['int',1],['none',None]]]],['list','x']):
            with self.subTest(node=node):self.assert_refused(altered(packet(),lambda v:v.update(arguments=node)))

    def test_source_exception_refuses_and_reaps(self):
        self.assert_refused(packet(body='raise KeyboardInterrupt'))

    def test_timeout_kills_and_reaps_without_retry(self):
        raw=packet(body='while True:pass')
        result=run(raw,timeout=.5)
        self.assertEqual(result['status'],'needs_review');self.assertEqual(result['termination'],'terminated_after_timeout')
        self.assertTrue(result['process_reaped']);self.assertFalse(result['automatic_retry'])

    def test_output_overflow_kills_and_reaps(self):
        raw=packet(body="while True:print('x'*65536,flush=True)")
        result=run(raw,timeout=10)
        self.assertEqual(result['status'],'needs_review');self.assertIn('output_bound',result['pipe_errors'])
        self.assertEqual(result['termination'],'terminated_after_pipe_failure')
        self.assertLessEqual(result['stdout_bytes'],subject.MAX_OUTPUT);self.assertTrue(result['process_reaped'])

    def test_strict_json_and_encoder_refuse_nonbuiltin_inputs(self):
        for value in ((1,),set(),object(),float('nan'),{1:'x'},2**4097):
            with self.subTest(kind=type(value)):
                with self.assertRaises(ValueError):subject.encode_arguments(value)
        cyclic=[];cyclic.append(cyclic)
        with self.assertRaisesRegex(ValueError,'argument_cycle'):subject.encode_arguments(cyclic)
        with self.assertRaises(ValueError):subject.strict_json(b'{"x":NaN}')
        with self.assertRaises(ValueError):subject.strict_json(b'{"x":1e999}')

    def test_oversized_and_deep_arguments_refuse(self):
        with self.assertRaises(ValueError):subject.encode_arguments('x'*(2*1024**2+1))
        with self.assertRaises(ValueError):subject.encode_arguments(['x'*1024]*1500)
        deep=[];top=deep
        for _ in range(82):next_value=[];deep.append(next_value);deep=next_value
        with self.assertRaisesRegex(ValueError,'argument_tree_bound'):subject.encode_arguments(top)

    def test_runtime_and_cli_refuse(self):
        with self.assertRaisesRegex(ValueError,'real_activation_pending'):subject.run_runtime()
        process=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8',str(ROOT/'tools/isolated_metadata_entry.py')],
            capture_output=True,timeout=10)
        self.assertEqual(process.returncode,2);self.assertEqual(process.stdout+process.stderr,b'')

    def test_timeout_bounds_refuse_without_launch(self):
        raw=packet()
        with patch.object(subject.subprocess,'Popen',side_effect=AssertionError('must not launch')):
            for timeout in (0,-1,31,True,float('nan'),float('inf')):
                with self.assertRaisesRegex(ValueError,'timeout_bound'):run(raw,timeout=timeout)

    def test_runtime_schema_bounds_and_exact_boolean_integer_types(self):
        changes=(lambda v:v.update(isolated=True),lambda v:v.update(no_bytecode=1),
            lambda v:v.update(optimize=False),lambda v:v.update(version=[True,1,2]),
            lambda v:v.update(path=['x'*4097]),lambda v:v.update(extra='x'),
            lambda v:v.update(path=['x']*65))
        for change in changes:
            value=runtime();change(value)
            with self.subTest(value=value):
                with self.assertRaises(ValueError):subject.checked_runtime(value)
        self.assert_refused(altered(packet(),lambda v:v['runtime'].update(isolated=True)))

    def test_closed_result_and_inner_loader_authority_are_checked(self):
        raw=packet();request=json.loads(raw);base=run(raw)['result'];self.assertIsNotNone(base)
        changes=(lambda v:v.update(extra=1),lambda v:v.update(metadata_result={}),
            lambda v:v['metadata_result'].update(execution_authorized=True),
            lambda v:v['metadata_result'].update(schema='unknown'),
            lambda v:v['metadata_result']['source_hashes'].update(dependency_candidate_context='0'*64),
            lambda v:v['metadata_result'].update(public_source_count=True),
            lambda v:v['startup'].update(isolated=True),
            lambda v:v['metadata_result'].update(metadata_result={'bad':float('inf')}))
        for change in changes:
            value=copy.deepcopy(base);change(value)
            with self.subTest(change=change):
                with self.assertRaises(ValueError):subject.validate_result(value,request,subject.sha(raw))


class SupervisionFaultTests(unittest.TestCase):
    class Thread:
        def __init__(self,**kwargs):pass
        def start(self):pass
        def join(self,timeout=None):pass
        def is_alive(self):return False

    def process(self):
        return Mock(pid=123,stdin=io.BytesIO(),stdout=io.BytesIO(),stderr=io.BytesIO())

    def supervise(self,process,**kwargs):
        with patch.object(subject.subprocess,'Popen',return_value=process),\
             patch.object(subject.threading,'Thread',self.Thread):
            return run(packet(),**kwargs)

    def test_main_poll_interruption_preserves_primary_and_reaps_once(self):
        process=self.process();primary=KeyboardInterrupt();process.poll.side_effect=primary;process.wait.return_value=9
        with self.assertRaises(KeyboardInterrupt) as raised:self.supervise(process)
        self.assertIs(raised.exception,primary);process.kill.assert_called_once();process.wait.assert_called_once()
        self.assertTrue(primary.metadata_completion['process_reaped']);self.assertIsNone(primary.metadata_completion['result'])

    def test_failed_main_wait_is_not_retried_or_claimed_reaped(self):
        process=self.process();process.poll.return_value=None;primary=RuntimeError('main wait');process.wait.side_effect=primary
        with self.assertRaises(RuntimeError) as raised:self.supervise(process,timeout=.001)
        self.assertIs(raised.exception,primary);process.kill.assert_called_once();process.wait.assert_called_once()
        self.assertFalse(primary.metadata_completion['process_reaped'])

    def test_kill_failure_keeps_primary_and_one_wait_observation(self):
        process=self.process();process.poll.return_value=None;primary=OSError('kill failed');process.kill.side_effect=primary
        process.wait.side_effect=subprocess.TimeoutExpired('invented',10)
        with self.assertRaises(OSError) as raised:self.supervise(process,timeout=.001)
        self.assertIs(raised.exception,primary);process.kill.assert_called_once();process.wait.assert_called_once()
        receipt=primary.metadata_completion;self.assertFalse(receipt['process_reaped']);self.assertTrue(receipt['cleanup_errors'])

    def test_cleanup_wait_timeout_and_each_close_failure_do_not_replace_primary(self):
        process=self.process();primary=KeyboardInterrupt();process.poll.side_effect=primary
        process.wait.side_effect=subprocess.TimeoutExpired('invented',10)
        pipes=[Mock() for _ in range(3)];process.stdin,process.stdout,process.stderr=pipes
        for pipe in pipes:pipe.close.side_effect=OSError('close')
        with self.assertRaises(KeyboardInterrupt) as raised:self.supervise(process)
        self.assertIs(raised.exception,primary);process.kill.assert_called_once();process.wait.assert_called_once()
        for pipe in pipes:pipe.close.assert_called_once()
        receipt=primary.metadata_completion;self.assertFalse(receipt['process_reaped'])
        self.assertEqual(len(receipt['cleanup_errors']),4)

    def test_each_thread_join_failure_is_recorded_and_other_joins_continue(self):
        process=self.process();process.poll.return_value=0
        class BadJoin(self.Thread):
            joins=0
            def join(self,timeout=None):
                type(self).joins+=1;raise RuntimeError('join')
        with patch.object(subject.subprocess,'Popen',return_value=process),\
             patch.object(subject.threading,'Thread',BadJoin):
            result=run(packet())
        self.assertEqual(BadJoin.joins,3);self.assertEqual(result['status'],'needs_review')
        self.assertTrue(result['process_reaped']);process.wait.assert_not_called();process.kill.assert_not_called()

    def test_normal_polled_exit_has_no_second_process_action(self):
        process=self.process();process.poll.return_value=2
        result=self.supervise(process)
        self.assertTrue(result['process_reaped']);process.wait.assert_not_called();process.kill.assert_not_called()

    def test_running_writer_close_failure_is_never_retried(self):
        class ImmediateThread(self.Thread):
            def __init__(self,target,args,**kwargs):self.target=target;self.args=args
            def start(self):self.target(*self.args)
        for complete_before_error in (False,True):
            process=self.process();process.poll.return_value=2
            class Pipe:
                attempts=0;closed=False
                def write(self,raw):return len(raw)
                def flush(self):pass
                def close(self):
                    self.attempts+=1
                    if complete_before_error:self.closed=True
                    raise OSError('uncertain close')
            pipe=Pipe();process.stdin=pipe
            with patch.object(subject.subprocess,'Popen',return_value=process),\
                 patch.object(subject.threading,'Thread',ImmediateThread):
                result=run(packet())
            self.assertEqual(pipe.attempts,1);self.assertEqual(result['status'],'needs_review')
            self.assertEqual(result['pipe_closes']['stdin'],dict(attempted=True,completed=False,error='OSError'))
            self.assertTrue(result['pipe_closes']['stdout']['completed']);self.assertTrue(result['pipe_closes']['stderr']['completed'])

    def test_writer_close_failure_preserves_main_interruption(self):
        class ImmediateThread(self.Thread):
            def __init__(self,target,args,**kwargs):self.target=target;self.args=args
            def start(self):self.target(*self.args)
        process=self.process();primary=KeyboardInterrupt();process.poll.side_effect=primary;process.wait.return_value=9
        process.stdin=Mock();process.stdin.close.side_effect=OSError('unknown completion')
        with patch.object(subject.subprocess,'Popen',return_value=process),\
             patch.object(subject.threading,'Thread',ImmediateThread):
            with self.assertRaises(KeyboardInterrupt) as raised:run(packet())
        self.assertIs(raised.exception,primary);process.stdin.close.assert_called_once()
        self.assertFalse(primary.metadata_completion['pipe_closes']['stdin']['completed'])

    def test_writer_failure_after_delivery_refuses_even_with_valid_child_result(self):
        raw=packet();valid=run(raw)['result'];self.assertIsNotNone(valid)
        class ImmediateThread(self.Thread):
            def __init__(self,target,args,**kwargs):self.target=target;self.args=args
            def start(self):self.target(*self.args)
        for error in (RuntimeError('flush'),KeyboardInterrupt()):
            process=self.process();process.poll.return_value=0
            process.stdout=io.BytesIO(subject.canonical(valid))
            process.stdin=Mock();process.stdin.flush.side_effect=error
            with patch.object(subject.subprocess,'Popen',return_value=process),\
                 patch.object(subject.threading,'Thread',ImmediateThread):
                result=run(raw)
            self.assertEqual(result['status'],'needs_review');self.assertIsNone(result['result'])
            self.assertIn('pipe_write:'+type(error).__name__,result['pipe_errors'])
            process.stdin.close.assert_called_once();process.kill.assert_not_called();process.wait.assert_not_called()
