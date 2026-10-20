"""Disabled operational engine composition; no launcher or permission check.

Only invented/intercepted calls are qualified. The trusted outer owner must
provide checked adapter/helper/wiring sources and a separately reviewed metadata
preparation. Existing HostPreparation remains invented-only and is not promoted
here. This module does not assemble records, spawn a process, open inputs or
authenticate its callers. Private engine calls can perform work if invoked.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import hashlib
import json
import time


def need(ok, code):
    if not ok:
        raise ValueError(code)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


class OnceClose:
    """Own one attempt even when close raises or returns an uncertain result."""
    def __init__(self, value, *, strict=False):
        self.value = value
        self.strict = strict
        self.attempted = self.closed = False
        self.failed = False

    def __getattr__(self, name):
        return getattr(self.value, name)

    def close(self):
        try:
            need(not self.attempted, 'operational_reclose')
            self.attempted = True
            answer = self.value.close()
            self.closed = answer is True or (not self.strict and answer is None)
            need(self.closed, 'operational_close_unknown')
            return True
        except BaseException:
            self.failed = True
            raise


def _binding(*, request, request_sha256, checked_sources, adapter_owner, helpers,
             helper_source_buffers):
    """Prepared mapping only; never infer authority from matching bytes."""
    adapter_owner.intact()
    helpers.intact()
    adapter = adapter_owner.modules['dependency_adapter_binding']
    adapter.validate_request(request, expected_request_sha256=request_sha256,
                             checked_sources=checked_sources)
    for name, role in (('dependency_adapter_binding', 'outer_child'),
                       ('dependency_operational_scope', 'adapter.scope_policy'),
                       ('dependency_outer_contract', 'adapter.comparison_contract')):
        need(adapter_owner.buffers[name] == checked_sources[role], 'operational_adapter_sources')
    # Parent uses dependency_parent rather than dependency_controller. That
    # fifth parent source is a separate outer-source binding, not a child role.
    common = ('dependency_evidence', 'dependency_producer',
              'dependency_package_preflight', 'dependency_execution')
    need(helpers.mode in ('child', 'parent'), 'operational_helper_mode')
    names = common + (('dependency_controller',) if helpers.mode == 'child'
                      else ('dependency_parent',))
    need(helpers.order == names and type(helper_source_buffers) is dict and
         set(helper_source_buffers) == set(names) and
         helpers.buffers == helper_source_buffers, 'operational_helper_roster')
    for name in names:
        need(type(helper_source_buffers[name]) is bytes and
             0 < len(helper_source_buffers[name]) <= 2*1024**2,
             'operational_helper_bound')
        key = 'dependency.' + name
        if key in checked_sources:
            need(helpers.buffers[name] == checked_sources[key], 'operational_helper_sources')
    return adapter


def _finish(primary, owners):
    cleanup = None
    for owner in owners:
        if owner is None:
            continue
        if owner.attempted:
            if (owner.failed or not owner.closed) and cleanup is None:
                cleanup = ValueError('operational_close_unknown')
            continue
        try:
            owner.close()
        except BaseException as error:
            if cleanup is None:
                cleanup = error
    if primary is not None:
        if cleanup is not None:
            raise primary from cleanup
        raise primary
    if cleanup is not None:
        raise cleanup


def _result(side, value):
    # An engine return is not a saved/process/physical completion assertion.
    return dict(schema='disabled_operational_engine_result_v1', side=side,
        engine_result=value, production_runtime_qualified=False,
        execution_authorized=False, feature_supported=False, recovery_proven=False,
        device_write_gate_passed=False, camera_commands=[])


def _continue_child(*, request, request_sha256, checked_sources, adapter_owner,
                    helpers, dependency_source_buffers, runtime_wiring,
                    preparation, context, identity, records):
    """Trusted future child engine, qualified with intercepted calls only.

    The outer owner must bind preparation/wiring/entry source bytes before this
    call. There is no packet-supplied observer, cipher, mode or callback factory.
    Ownership transfers on entry, including validation/preparation failures.
    """
    prep = OnceClose(preparation)
    helper = OnceClose(helpers)
    owner = OnceClose(adapter_owner)
    record = OnceClose(records, strict=True)
    callbacks = None
    primary = None
    result = None
    claimed = False
    completed = failed = False
    try:
        adapter = _binding(request=request, request_sha256=request_sha256,
            checked_sources=checked_sources, adapter_owner=adapter_owner, helpers=helpers,
            helper_source_buffers={n:raw for n,raw in dependency_source_buffers.items()
                                   if n != 'closure_manifest'})
        need(helpers.mode == 'child', 'operational_helper_mode')
        modules, _, raw_callbacks = preparation.prepare()
        callbacks = OnceClose(raw_callbacks)
        # Metadata preparation precedes observer/controller dispatch. The
        # controller invokes this factory only after its durable raw receipt.
        def factory(controller, stage_source, dependency):
            nonlocal claimed, completed, failed
            try:
                need(not claimed, 'operational_factory_reentry')
                claimed = True
                adapter_owner.intact()
                helpers.intact()
                answer = raw_callbacks(controller, stage_source, dependency)
                completed = True
                return answer
            except BaseException:
                failed = True
                raise

        def release():
            return callbacks.close()

        adapter_owner.intact()
        helpers.intact()
        need(hashlib.sha256(encoded(request)).hexdigest() == request_sha256,
             'operational_request_changed')
        result = adapter._continue_runtime(request=request,
            expected_request_sha256=request_sha256, checked_sources=checked_sources,
            helpers=helpers, dependency_source_buffers=dependency_source_buffers,
            runtime_wiring=runtime_wiring, context=context, identity=identity,
            control=modules['control'], records=record,
            make_callbacks_after_receipt=factory,
            release_callbacks_after_controller=release, monotonic=time.monotonic)
        adapter_owner.intact()
        helpers.intact()
        need(hashlib.sha256(encoded(request)).hexdigest() == request_sha256,
             'operational_request_changed')
        need(claimed and completed and not failed and callbacks.attempted and callbacks.closed and
             not callbacks.failed and record.attempted and record.closed and not record.failed,
             'operational_child_incomplete')
    except BaseException as error:
        primary = error
    # Callback cleanup precedes helper/adapter/metadata cleanup. A failed close
    # attempt is never retried, and one failing owner cannot suppress the rest.
    _finish(primary, (callbacks, record, helper, owner, prep))
    return _result('child', result)


def _reconcile_parent(*, request, request_sha256, checked_sources, adapter_owner,
                      helpers, parent_source_buffers, runtime_wiring, inputs, process, stdout,
                      stdout_sha256, dependency_sha256, bridge_sha256):
    """Saved-runtime engine only; owned supervisor integration is still required.

    Caller process facts are not authenticated by this function. The separate
    outer parent must derive them from its own supervised process and bind the
    saved preflight/original records before invoking this composition.
    """
    helper = OnceClose(helpers)
    owner = OnceClose(adapter_owner)
    primary = None
    result = None
    try:
        adapter = _binding(request=request, request_sha256=request_sha256,
            checked_sources=checked_sources, adapter_owner=adapter_owner, helpers=helpers,
            helper_source_buffers=parent_source_buffers)
        need(helpers.mode == 'parent', 'operational_helper_mode')
        result = adapter.reconcile_runtime(request=request,
            expected_request_sha256=request_sha256, checked_sources=checked_sources,
            helpers=helpers, runtime_wiring=runtime_wiring, inputs=inputs,
            process=process, stdout=stdout, stdout_sha256=stdout_sha256,
            dependency_sha256=dependency_sha256, bridge_sha256=bridge_sha256)
        adapter_owner.intact()
        helpers.intact()
        need(hashlib.sha256(encoded(request)).hexdigest() == request_sha256,
             'operational_request_changed')
    except BaseException as error:
        primary = error
    _finish(primary, (helper, owner))
    return _result('parent', result)


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
