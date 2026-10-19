"""Prepared bindings and real controller/saved verifier with invented inputs.

No protected-role code, runtime observer, installed dependency or camera runs.
The process record is an invented terminal record, not OS supervision evidence.
"""
import copy
from pathlib import Path
import types
import unittest
from unittest.mock import Mock, patch

from tools import dependency_adapter_binding as subject
from tools import dependency_controller as controller
from tools import dependency_execution as execution
from tools import dependency_parent as parent
from tools import dependency_producer as producer
from tools import dependency_evidence as core
import test_dependency_controller as controller_fixture
from test_dependency_producer import refresh


def fixture(data, folder):
    sources, buffers = {}, {}
    for index, role in enumerate(sorted(subject.SOURCE_ROLES)):
        path = 'private/invented/role_' + str(index) + '.py'
        raw = ('# inert invented source ' + role + '\n').encode('ascii')
        if role in subject.ENTRIES:
            path = subject.ADAPTER_PATH
        elif role == 'adapter.scope_policy':
            path = 'tools/dependency_operational_scope.py'
        elif role == 'adapter.comparison_contract':
            path = 'tools/dependency_outer_contract.py'
        elif role.startswith('dependency.'):
            path = 'tools/' + role.split('.', 1)[1] + '.py'
        if path.startswith('tools/'):
            raw = Path(path).read_bytes()  # Authored ordinary source text only.
        buffers[role] = raw
        sources[role] = dict(path=path, bytes=len(raw), sha256=subject.sha(raw),
                             entry=subject.ENTRIES.get(role))
    dependency = {name: buffers['dependency.' + name] for name in subject.policy.outer.CHILD}
    dependency['closure_manifest'] = subject.encoded(sources)
    data['source_buffers'] = dependency
    data['expectation']['source_sha256'] = {n: subject.sha(raw) for n, raw in dependency.items()}
    refresh(data)
    request = dict(schema='prepared_gdt_adapter_request_v1',
        operation_id=data['expectation']['operation_id'], scope=dict(subject.policy.SCOPE),
        sources=sources, dependency_packet=dict(schema='runtime_dependency_packet_v1',
            inputs={n: v for n, v in data.items() if n != 'source_buffers'}),
        dependency_fixed=dict(expectation_sha256=core._hash(data['expectation']),
            package_sha256=core._hash(data['package']),
            root_sha256={n: row['identity_sha256'] for n, row in data['expectation']['roots'].items()}),
        dependency_review_sha256=data['binding']['review_sha256'], folder=str(folder),
        decisions=dict.fromkeys(subject.policy.RIGHTS, 'pending'),
        execution_authorized=False, camera_commands=[])
    return request, buffers


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.f = controller_fixture.ControllerTests()
        self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        self.request, self.buffers = fixture(self.f.data, self.f.folder)
        self.f.context.update(deadline_seconds=300, limits=dict(poll_seconds=0.05))
        self.helpers = types.SimpleNamespace(mode='child', intact=Mock(),
            package=types.SimpleNamespace(dependency_execution=execution, dependency_controller=controller))
        self.process = dict(launch_attempts=1, exit_observed=True, child_exit_code=0,
            reader_threads_joined=True, pipe_close_complete=True, timed_out=False,
            launch_failed=False, log_cap_exceeded=False, log_reader_failed=False,
            kill_succeeded=False, collector_stop_requested=True, deadline_seconds=300,
            kill_attempts=0, wait_attempts=0, elapsed_seconds=0.1)

    def binding_args(self):
        return dict(request=self.request, expected_request_sha256=subject.sha(subject.encoded(self.request)),
            checked_sources=self.buffers, helpers=self.helpers,
            dependency_source_buffers=self.f.data['source_buffers'],
            context=self.f.context, identity=self.f.identity)

    def execute(self, **changes):
        args = dict(**self.binding_args(), ops=self.f.ops, control=self.f.control,
            records=self.f.records, make_callbacks_after_receipt=self.f.factory,
            release_callbacks_after_controller=self.f.release, monotonic=lambda: 0.)
        args.update(changes)
        return subject.run_invented(**args)

    def parent_args(self):
        helper = types.SimpleNamespace(mode='parent', intact=Mock(), verify=parent.validate_saved_controller,
            package=types.SimpleNamespace(dependency_execution=execution))
        stdout = producer.encoded(self.f.result[1])
        return dict(request=self.request, expected_request_sha256=subject.sha(subject.encoded(self.request)),
            checked_sources=self.buffers, helpers=helper, inputs=self.f.data, process=self.process,
            stdout=stdout, stdout_sha256=subject.sha(stdout),
            dependency_sha256=execution.validate_saved_composition(
                self.f.folder / 'collected', self.f.data, invented=True),
            bridge_sha256={n: subject.sha((self.f.folder / n).read_bytes()) for n in parent.BRIDGE})

    def test_connected_controller_receipt_callbacks_and_saved_parent(self):
        with patch.object(producer.RuntimeOps, '__init__', side_effect=AssertionError('runtime observer')):
            result = self.execute()
            saved = subject.reconcile_invented(**self.parent_args())
        self.assertEqual(result['callback_result'][0], 0)
        self.assertEqual((self.f.controller_calls, self.f.factories, self.f.releases, self.f.closes), (1, 1, 1, 1))
        self.assertEqual(len(saved['dependency_sha256']), 11)
        self.assertFalse(saved['execution_authorized'])
        self.assertFalse(saved['actual_runtime_verified'])

    def test_controller_failure_preserves_primary_and_one_close(self):
        primary = KeyboardInterrupt('invented controller stop')
        self.f.control.run_child_reserved = Mock(side_effect=primary)
        with self.assertRaises(KeyboardInterrupt) as caught:
            self.execute()
        self.assertIs(caught.exception, primary)
        self.assertEqual((self.f.factories, self.f.releases, self.f.closes), (0, 1, 1))

    def test_closed_request_no_ops_backend_or_mode_selector(self):
        for field in ('ops', 'backend', 'invented', 'continuation'):
            self.request[field] = 'injected'
            with self.assertRaisesRegex(ValueError, 'adapter_request'):
                subject.bind_child(**self.binding_args())
            del self.request[field]
        self.assertEqual(self.f.ops.reads, [])

    def test_external_request_digest_mismatch_before_helpers(self):
        args = self.binding_args()
        args['expected_request_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'adapter_request_hash'):
            subject.bind_child(**args)
        self.helpers.intact.assert_not_called()

    def test_every_frozen_limit_refuses_widening(self):
        for name in subject.policy.SCOPE:
            self.request['scope'][name] += 1
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'adapter_scope'):
                subject.bind_child(**self.binding_args())
            self.request['scope'][name] -= 1
        self.assertEqual(self.f.ops.reads, [])

    def test_no_decision_promotion_even_after_rehash(self):
        for name in self.request['decisions']:
            self.request['decisions'][name] = 'approved'
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'adapter_decisions'):
                subject.bind_child(**self.binding_args())
            self.request['decisions'][name] = 'pending'

    def test_authority_and_camera_operation_refused(self):
        for field, value in (('execution_authorized', True), ('camera_commands', ['anything'])):
            old = self.request[field]
            self.request[field] = value
            with self.assertRaisesRegex(ValueError, 'adapter_authority'):
                subject.bind_child(**self.binding_args())
            self.request[field] = old

    def test_missing_extra_and_invented_fixture_sources_refused(self):
        for name in ('invented_fixture', 'unlisted_helper'):
            self.buffers[name] = b'pass\n'
            with self.assertRaisesRegex(ValueError, 'adapter_sources'):
                subject.bind_child(**self.binding_args())
            del self.buffers[name]
        self.buffers.pop('adapter.scope_policy')
        with self.assertRaisesRegex(ValueError, 'adapter_sources'):
            subject.bind_child(**self.binding_args())

    def test_changed_source_buffer_refused_before_bind_or_reservation(self):
        self.buffers['bound.role:capture'] += b'# changed\n'
        with self.assertRaisesRegex(ValueError, 'adapter_source_size'):
            subject.bind_child(**self.binding_args())
        self.assertEqual(self.f.ops.reads, [])
        self.assertFalse(self.f.folder.exists())

    def test_six_function_roles_have_one_explicit_source_identity(self):
        rows = self.request['sources']
        self.assertEqual(len({rows[n]['sha256'] for n in subject.ENTRIES}), 1)
        self.assertEqual({rows[n]['entry'] for n in subject.ENTRIES}, set(subject.ENTRIES.values()))
        rows['outer_child']['entry'] = 'run_invented'
        with self.assertRaisesRegex(ValueError, 'adapter_source_entry'):
            subject.bind_child(**self.binding_args())

    def test_rebinding_role_path_or_alias_is_not_silently_accepted(self):
        rows = self.request['sources']
        rows['outer_gate']['path'] = 'tools/elsewhere.py'
        with self.assertRaisesRegex(ValueError, 'adapter_source_entry_path'):
            subject.bind_child(**self.binding_args())
        rows['outer_gate']['path'] = subject.ADAPTER_PATH
        rows['bound.role:capture']['path'] = rows['bound.role:core']['path']
        with self.assertRaisesRegex(ValueError, 'adapter_source_alias'):
            subject.bind_child(**self.binding_args())

    def test_operation_or_context_limit_substitution_refused(self):
        for key, value in (('operation_id', '0' * 32), ('deadline_seconds', 20),
                           ('deadline_seconds', 300.0), ('limits', {'poll_seconds': 0.1})):
            original = self.f.context[key]
            self.f.context[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                subject.bind_child(**self.binding_args())
            self.f.context[key] = original

    def test_dependency_helper_buffer_substitution_refused(self):
        name = 'dependency_controller'
        self.f.data['source_buffers'][name] += b'# other controller\n'
        self.f.data['expectation']['source_sha256'][name] = subject.sha(self.f.data['source_buffers'][name])
        refresh(self.f.data)
        self.request['dependency_packet']['inputs']['binding'] = self.f.data['binding']
        self.request['dependency_fixed']['expectation_sha256'] = core._hash(self.f.data['expectation'])
        with self.assertRaisesRegex(ValueError, 'adapter_dependency_source_binding'):
            subject.bind_child(**self.binding_args())

    def test_runtime_dispatch_only_spied_exact_arguments_without_ops(self):
        wiring = types.SimpleNamespace(_dispatch_runtime=Mock(return_value=object()))
        args = dict(**self.binding_args(), runtime_wiring=wiring, control=self.f.control,
            records=self.f.records, make_callbacks_after_receipt=self.f.factory,
            release_callbacks_after_controller=self.f.release, monotonic=lambda: 0.)
        result = subject._continue_runtime(**args)
        call = wiring._dispatch_runtime.call_args.kwargs
        self.assertIs(result, wiring._dispatch_runtime.return_value)
        self.assertIs(call['records'], self.f.records)
        self.assertEqual(call['packet'], self.request['dependency_packet'])
        self.assertEqual(call['folder'], self.f.folder)
        self.assertNotIn('ops', call)
        self.assertNotIn('invented', call)
        self.assertEqual(self.f.ops.reads, [])
        self.assertEqual(self.f.closes, 0)
        for name in ('ops', 'invented', 'backend'):
            with self.assertRaises(TypeError):
                subject._continue_runtime(**args, **{name: object()})

    def test_parent_termination_and_cleanup_unknown_refuse_before_saved_reads(self):
        self.execute()
        args = self.parent_args()
        args['helpers'].verify = Mock(side_effect=AssertionError('saved read'))
        for key, value in (('launch_attempts', 2), ('launch_attempts', True),
                ('exit_observed', False), ('child_exit_code', 2), ('child_exit_code', False),
                ('reader_threads_joined', False), ('pipe_close_complete', False), ('timed_out', True),
                ('log_cap_exceeded', True), ('log_reader_failed', True), ('launch_failed', True),
                ('kill_succeeded', True), ('kill_attempts', 1), ('wait_attempts', 1)):
            old = self.process[key]
            self.process[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'adapter_process_'):
                subject.reconcile_invented(**args)
            self.process[key] = old
        args['helpers'].verify.assert_not_called()

    def test_saved_runtime_verifier_only_spied_no_mode_injection(self):
        self.execute()
        args = self.parent_args()
        wiring = types.SimpleNamespace(_verify_saved_runtime=Mock(return_value=object()))
        answer = subject.reconcile_runtime(**args, runtime_wiring=wiring)
        call = wiring._verify_saved_runtime.call_args.kwargs
        self.assertIs(answer, wiring._verify_saved_runtime.return_value)
        self.assertEqual(call['operation_id'], self.request['operation_id'])
        self.assertEqual(call['folder'], self.f.folder)
        self.assertNotIn('invented', call)
        self.assertNotIn('process', call)

    def test_parent_input_and_stdout_tampering(self):
        self.execute()
        args = self.parent_args()
        args['inputs'] = copy.deepcopy(self.f.data)
        args['inputs']['config_json'] += ' '
        with self.assertRaisesRegex(ValueError, 'adapter_parent_inputs'):
            subject.reconcile_invented(**args)
        args['inputs'] = self.f.data
        args['stdout'] += b' '
        with self.assertRaisesRegex(ValueError, 'parent_stdout_hash'):
            subject.reconcile_invented(**args)

    def test_existing_output_refuses_before_second_collection(self):
        self.execute()
        reads = len(self.f.ops.reads)
        with self.assertRaises(FileExistsError):
            self.execute()
        self.assertEqual(len(self.f.ops.reads), reads)
        self.assertEqual(self.f.controller_calls, 1)

    def test_parent_rebinds_fixed_review_and_packet_schema_before_saved_reads(self):
        self.execute()
        args = self.parent_args()
        verifier = Mock(side_effect=AssertionError('saved read before binding'))
        args['helpers'].verify = verifier
        for field, bad in (('expectation_sha256', '0' * 64), ('package_sha256', '0' * 64),
                            ('root_sha256', {})):
            original = self.request['dependency_fixed'][field]
            self.request['dependency_fixed'][field] = bad
            args['expected_request_sha256'] = subject.sha(subject.encoded(self.request))
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'fixed_expectations'):
                subject.reconcile_invented(**args)
            self.request['dependency_fixed'][field] = original
        original = self.request['dependency_review_sha256']
        self.request['dependency_review_sha256'] = '0' * 64
        args['expected_request_sha256'] = subject.sha(subject.encoded(self.request))
        with self.assertRaisesRegex(ValueError, 'review_binding'):
            subject.reconcile_invented(**args)
        self.request['dependency_review_sha256'] = original
        self.request['dependency_packet']['schema'] = 'invented_dependency_packet_v1'
        args['expected_request_sha256'] = subject.sha(subject.encoded(self.request))
        with self.assertRaisesRegex(ValueError, 'packet_mode'):
            subject.reconcile_invented(**args)
        verifier.assert_not_called()

    def test_parent_process_shape_retains_frozen_deadline_and_finite_time(self):
        self.execute()
        args = self.parent_args()
        verifier = Mock(side_effect=AssertionError('saved read'))
        args['helpers'].verify = verifier
        for key, value in (('deadline_seconds', 20), ('deadline_seconds', 300.0),
                ('elapsed_seconds', float('nan')), ('elapsed_seconds', -1),
                ('elapsed_seconds', True), ('reader_threads_joined', 1), ('wait_attempts', True)):
            old = self.process[key]
            self.process[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'adapter_process_shape'):
                subject.reconcile_invented(**args)
            self.process[key] = old
        verifier.assert_not_called()

    def test_public_runtime_refuses_without_reading_arguments(self):
        with self.assertRaisesRegex(ValueError, '^real_activation_pending$'):
            subject.run_runtime(unknown=object())


if __name__ == '__main__':
    unittest.main()
