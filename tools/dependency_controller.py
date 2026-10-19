"""Invented collector/producer/controller composition; ordinary CLI refuses.

The public runtime entry refuses activation. A future
entry must bind a new source closure, current inputs and activity-specific scope.
Caller callbacks and review hashes are not an authorization or security sandbox.
"""
from pathlib import Path
import sys
from types import MappingProxyType, ModuleType

from tools import dependency_evidence as core
from tools import dependency_execution as execution
from tools import dependency_producer as producer


def run_invented(*, inputs, ops, folder, control, context, records,
                 make_callbacks_after_receipt, release_callbacks_after_controller,
                 monotonic, identity):
    """Invented qualification only; never accepts a concrete runtime observer."""
    producer.need(not isinstance(ops, producer.RuntimeOps), 'real_activation_pending')
    return _run(inputs=inputs, ops=ops, folder=folder, control=control, context=context,
        records=records, make_callbacks_after_receipt=make_callbacks_after_receipt,
        release_callbacks_after_controller=release_callbacks_after_controller,
        monotonic=monotonic, identity=identity, invented=True)


def run_runtime(**kwargs):
    """No activation route until an exact successor packet is separately reviewed."""
    raise core.EvidenceError('real_activation_pending')


def _run(*, inputs, folder, control, context, records,
         make_callbacks_after_receipt, release_callbacks_after_controller,
         monotonic, identity, invented, ops=None):
    """Shared internal engine, qualified only with invented data.

    Caller owns records until the exclusive folder reservation succeeds. Then
    this engine owns at most one close attempt. The runtime branch receives no
    observer: execution constructs RuntimeOps internally. Leading underscores
    describe a trusted authored-code boundary, not a Python security sandbox.
    """
    producer.need(type(invented) is bool, 'collection_mode')
    producer.need((invented and not isinstance(ops, producer.RuntimeOps)) or
                  (not invented and ops is None), 'controller_observer')
    producer.need(callable(make_callbacks_after_receipt) and
                  callable(release_callbacks_after_controller) and callable(monotonic), 'controller_callbacks')
    policy, _, _, _, _ = producer.bind_inputs(**inputs)
    producer.need(type(context) is dict and type(identity) is dict and
                  policy['operation_id'] == context.get('operation_id') == identity.get('operation_id'),
                  'controller_operation')
    producer.need(control.verify_context(context) is True, 'controller_context')
    prefix = 'invented_' if invented else ''
    folder = Path(folder)
    output = None
    state = dict(claimed=False, entered=False, factory_claimed=False, factory_completed=False,
                 factory_failed=False, release_attempted=False, released=False,
                 callback_result=None, anchor=None)
    completion_attempted = False

    class RecordOwner:
        attempted = False
        closed = False

        def __getattr__(self, name):
            return getattr(records, name)

        def close(self):
            producer.need(not self.attempted, 'controller_records_reclose')
            self.attempted = True
            self.closed = records.close() is True
            return self.closed

    owned_records = RecordOwner()

    def continue_controller(AES, vectors):
        producer.need(not state['claimed'], 'controller_reentry')
        state['claimed'] = True
        producer.need(type(AES) is ModuleType and sys.modules.get('Cryptodome.Cipher.AES') is AES,
                      'controller_aes_owner')
        producer.need(control.verify_context(context) is True, 'controller_context')
        producer.need(policy['operation_id'] == context.get('operation_id') == identity.get('operation_id'),
                      'controller_operation')
        # The existing producer has durably published this raw record and
        # journaled its single callback claim before entering this method.
        raw_path = folder/'collected'/'producer'/'raw.json'
        raw, _ = producer.read_verified(str(raw_path), limit=4*1024**2)
        transcript = core._json_text(raw.decode('utf-8'))
        producer.need(transcript.get('operation_id') == policy['operation_id'], 'controller_receipt')
        journal, _ = producer.read_verified(str(raw_path.parent/'journal.jsonl'), limit=4*1024**2)
        events = [core._json_text(line) for line in journal.decode('utf-8').splitlines()]
        producer.need(len(events) >= 2 and events[-2]['event'] == 'raw_reverified' and
                      events[-1]['event'] == 'callback_claimed' and
                      events[-1]['data'] == dict(raw_receipt_sha256=producer.sha(raw),
                                               operation_id=policy['operation_id']), 'controller_receipt')
        anchor = dict(path=str(raw_path), sha256=producer.sha(raw), bytes=len(raw))
        dependency = MappingProxyType(dict(AES=AES, provenance=MappingProxyType(anchor)))
        state['anchor'] = anchor
        # This new boundary does not accept legacy raw/config/cache as a
        # fresh proof. Its anchor references the current producer's bytes.
        def factory(controller, stage_source):
            try:
                producer.need(not state['factory_claimed'], 'controller_factory_reentry')
                state['factory_claimed'] = True
                producer.need(control.verify_context(context) is True and
                              policy['operation_id'] == context.get('operation_id') == identity.get('operation_id'),
                              'controller_context')
                producer.need(not owned_records.attempted, 'controller_records')
                producer.need(sys.modules.get('Cryptodome.Cipher.AES') is AES, 'controller_aes_owner')
                current, _ = producer.read_verified(str(raw_path), limit=4*1024**2)
                producer.need(current == raw, 'controller_receipt')
                callbacks = make_callbacks_after_receipt(controller, stage_source, dependency)
                state['factory_completed'] = True
                return callbacks
            except BaseException:
                state['factory_failed'] = True
                raise

        primary = None
        state['entered'] = True
        try:
            producer.need(policy['operation_id'] == context.get('operation_id') == identity.get('operation_id'),
                          'controller_operation')
            answer = control.run_child_reserved(context=context, records=owned_records,
                make_callbacks=factory, monotonic=monotonic, identity=identity)
            producer.need(state['factory_completed'] and not state['factory_failed'], 'controller_factory')
            producer.need(type(answer) is tuple and len(answer) == 2 and type(answer[0]) is int and
                          answer[0] in (0, 2) and type(answer[1]) is dict and
                          type(answer[1].get('script_exit_code')) is int and
                          answer[1].get('script_exit_code') == answer[0], 'controller_result')
            state['callback_result'] = answer
            output.small('controller-result.json', dict(code=answer[0], summary=answer[1],
                test_injection_used=invented, camera_commands=[]))
            producer.need(answer[0] == 0, 'controller_refused')
        except BaseException as error:
            primary = error
        finally:
            try:
                if not owned_records.attempted:
                    owned_records.close()
                producer.need(owned_records.closed, 'controller_records')
            except BaseException as error:
                if primary is None:
                    primary = error
            state['release_attempted'] = True
            try:
                release_callbacks_after_controller()
                state['released'] = True
            except BaseException as error:
                if primary is None:
                    primary = error
        if primary is not None:
            raise primary
        producer.need(control.verify_context(context) is True, 'controller_context')
        producer.need(policy['operation_id'] == context.get('operation_id') == identity.get('operation_id'),
                      'controller_operation')
        producer.need(sys.modules.get('Cryptodome.Cipher.AES') is AES, 'controller_aes_owner')
        # Retain the public-vector callback after the controller, while the
        # same guard/finder/AES session is still live. No alternate backend.
        producer.run_vectors(AES, vectors)

    folder.mkdir(exist_ok=False)
    try:
        output = producer.Outputs(folder)
        output.small('started.json', dict(schema=prefix+'collected_controller_started_v1',
            operation_id=policy['operation_id'], expectation_sha256=core._hash(policy),
            test_injection_used=invented, automatic_retry=False, protected_input_authorized=False, camera_commands=[]))
        if invented:
            result = execution._produce_collected(inputs=inputs, ops=ops,
                folder=folder/'collected', invented=True, continuation=continue_controller)
        else:
            result = execution._produce_collected_runtime(inputs=inputs,
                folder=folder/'collected', continuation=continue_controller)
        producer.need(state['entered'] and state['released'] and state['callback_result'] is not None,
                      'controller_incomplete')
        completion_attempted = True
        output.small('completion.json', dict(schema=prefix+'collected_controller_completion_v1',
            status=prefix+'collected_controller_complete', controller_entered=True,
            callback_released=True, dependency_completion_sha256=core._hash(result),
            test_injection_used=invented, automatic_retry=False, actual_dependency_observation_performed=not invented,
            execution_authorized=False, feature_supported=False, recovery_proven=False,
            device_write_gate_passed=False, camera_commands=[]))
        return dict(schema=prefix+'collected_controller_result_v1', status='protected_callback_returned',
            callback_result=state['callback_result'], provenance=state['anchor'],
            dependency=result, test_injection_used=invented, execution_authorized=False,
            feature_supported=False, recovery_proven=False, device_write_gate_passed=False, camera_commands=[])
    except BaseException as primary:
        # A failed/unknown close or publication is never retried.
        if not owned_records.attempted:
            try:
                owned_records.close()
            except BaseException:
                pass
        try:
            if output is not None and not completion_attempted:
                completion_attempted = True
                output.small('completion.json', dict(schema=prefix+'collected_controller_completion_v1',
                status='needs_review', controller_entered=state['entered'],
                release_attempted=state['release_attempted'], callback_released=state['released'],
                record_close_attempted=owned_records.attempted, records_closed=owned_records.closed,
                test_injection_used=invented, automatic_retry=False,
                dependency_observation_status='incomplete_or_unknown', actual_dependency_observation_completed=False,
                execution_authorized=False, feature_supported=False, recovery_proven=False,
                device_write_gate_passed=False, camera_commands=[]))
        except BaseException as publication:
            raise primary from publication
        raise


def main():
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
