"""Concrete GDT call bindings; public activation remains disabled.

The prepared request binds already captured authored sources and ordinary
dependency inputs. It is neither an executable launcher nor a rights decision.
Private runtime seams can perform work: only source/spied-call review is
qualified here. Invented execution uses a separate, explicit observer route.
"""
import hashlib
import json
import math
from pathlib import Path, PurePosixPath

if __name__ == '__main__':
    raise SystemExit(2)

from tools import dependency_operational_scope as policy


ADAPTER_PATH = 'tools/dependency_adapter_binding.py'
ENTRIES = dict(outer_contract='validate_request', outer_gate='check_sources',
    outer_entry='bind_child', outer_child='_continue_runtime',
    successor_entry='_saved_runtime', host_parent_adapter='reconcile_runtime')
EXTRA_SOURCES = frozenset(('adapter.scope_policy', 'adapter.comparison_contract'))
SOURCE_ROLES = policy.SOURCE_ROLES | {'host_parent_adapter'} | EXTRA_SOURCES
REQUEST_FIELDS = frozenset(('schema', 'operation_id', 'scope', 'sources',
    'dependency_packet', 'dependency_fixed', 'dependency_review_sha256',
    'folder', 'decisions', 'execution_authorized', 'camera_commands'))
PROCESS_BOOLS = frozenset(('timed_out', 'launch_failed', 'log_cap_exceeded',
    'log_reader_failed', 'kill_succeeded', 'exit_observed', 'reader_threads_joined',
    'collector_stop_requested', 'pipe_close_complete'))
PROCESS_FIELDS = PROCESS_BOOLS | {'launch_attempts', 'child_exit_code',
    'deadline_seconds', 'kill_attempts', 'wait_attempts', 'elapsed_seconds'}


def need(ok, code):
    if not ok:
        raise ValueError(code)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    need(type(value) is str and len(value) == 64 and
         all(c in '0123456789abcdef' for c in value), 'adapter_digest')


def check_sources(sources, checked_sources):
    """Hash captured buffers only; never open or execute their path labels.

    Six explicit function roles share one source file. Two additional import
    sources account for this module's policy import and its comparison import.
    This is byte binding, not live-function ownership or a complete launcher.
    """
    need(type(sources) is dict and type(checked_sources) is dict and
         set(sources) == set(checked_sources) == SOURCE_ROLES, 'adapter_sources')
    total = 0
    aliases = {}
    for role, row in sources.items():
        need(type(row) is dict and set(row) == {'path', 'bytes', 'sha256', 'entry'},
             'adapter_source_row')
        name = row['path']
        need(type(name) is str and 0 < len(name) <= 1024 and
             not any(c in name for c in ('\\', ':')) and
             all(ord(c) >= 32 for c in name), 'adapter_source_path')
        path = PurePosixPath(name)
        need(not path.is_absolute() and '..' not in path.parts and
             path.suffix == '.py' and str(path) == name and
             path.parts[0] in ('tools', 'private'), 'adapter_source_path')
        raw = checked_sources[role]
        need(type(raw) is bytes and 0 < len(raw) <= 2 * 1024**2 and
             type(row['bytes']) is int and row['bytes'] == len(raw), 'adapter_source_size')
        digest(row['sha256'])
        need(sha(raw) == row['sha256'], 'adapter_source_hash')
        entry = ENTRIES.get(role)
        need(row['entry'] == entry, 'adapter_source_entry')
        if role in ENTRIES:
            need(name == ADAPTER_PATH, 'adapter_source_entry_path')
        if role in EXTRA_SOURCES:
            expected = ('tools/dependency_operational_scope.py' if role == 'adapter.scope_policy'
                        else 'tools/dependency_outer_contract.py')
            need(name == expected, 'adapter_source_import_path')
        key = name.casefold()
        if key in aliases:
            old_role, old_row = aliases[key]
            need(role in ENTRIES and old_role in ENTRIES and name == old_row['path'] and
                 (row['bytes'], row['sha256']) == (old_row['bytes'], old_row['sha256']),
                 'adapter_source_alias')
        else:
            aliases[key] = (role, row)
            total += len(raw)
        need(total <= 16 * 1024**2, 'adapter_source_total')
    return sha(encoded(sources))


def validate_request(request, *, expected_request_sha256, checked_sources):
    """Prepared call mapping only; pending decisions cannot become approvals."""
    need(type(request) is dict and set(request) == REQUEST_FIELDS, 'adapter_request')
    digest(expected_request_sha256)
    need(sha(encoded(request)) == expected_request_sha256, 'adapter_request_hash')
    need(request['schema'] == 'prepared_gdt_adapter_request_v1', 'adapter_mode')
    operation = request['operation_id']
    need(type(operation) is str and len(operation) == 32 and
         all(c in '0123456789abcdef' for c in operation), 'adapter_operation')
    need(encoded(request['scope']) == encoded(policy.SCOPE), 'adapter_scope')
    need(request['execution_authorized'] is False and request['camera_commands'] == [],
         'adapter_authority')
    need(type(request['decisions']) is dict and set(request['decisions']) == policy.RIGHTS and
         all(v == 'pending' for v in request['decisions'].values()), 'adapter_decisions')
    digest(request['dependency_review_sha256'])
    need(type(request['folder']) is str, 'adapter_folder')
    folder = Path(request['folder'])
    need(folder.is_absolute() and '..' not in folder.parts and
         folder.name not in ('', '.', '..'), 'adapter_folder')
    return check_sources(request['sources'], checked_sources)


def bind_child(*, request, expected_request_sha256, checked_sources, helpers,
               dependency_source_buffers, context, identity):
    """Map a prepared request to the existing closed dependency packet binder.

    Caller supplies checked helper ownership and an already prepared controller
    context. Neither live helper ownership nor ordinary role semantics is
    inferred from the source hashes. No record reservation or I/O occurs here.
    """
    validate_request(request, expected_request_sha256=expected_request_sha256,
                     checked_sources=checked_sources)
    need(helpers.mode == 'child', 'adapter_helper_mode')
    helpers.intact()
    need(type(context) is dict and type(identity) is dict and
         request['operation_id'] == context.get('operation_id') == identity.get('operation_id'),
         'adapter_operation')
    need(type(context.get('deadline_seconds')) is int and
         context['deadline_seconds'] == policy.SCOPE['child_deadline_seconds'] and
         encoded(context.get('limits')) == encoded({'poll_seconds': 0.05}), 'adapter_context_limits')
    inputs = helpers.package.dependency_execution.bind_runtime_packet(
        request['dependency_packet'], request['dependency_fixed'], dependency_source_buffers,
        request['dependency_review_sha256'])
    need(inputs['expectation']['operation_id'] == request['operation_id'], 'adapter_operation')
    # The five dependency helper texts and manifest must be the same buffers
    # reviewed by the outer source map, not an independently substituted set.
    names = policy.outer.CHILD
    need(type(dependency_source_buffers) is dict and
         set(dependency_source_buffers) == set(names) | {'closure_manifest'}, 'adapter_dependency_sources')
    for name in names:
        need(dependency_source_buffers[name] == checked_sources['dependency.' + name],
             'adapter_dependency_source_binding')
    need(dependency_source_buffers['closure_manifest'] == encoded(request['sources']),
         'adapter_dependency_closure')
    helpers.intact()
    return inputs


def _continue_runtime(*, request, expected_request_sha256, checked_sources, helpers,
                      dependency_source_buffers, runtime_wiring, context, identity,
                      control, records, make_callbacks_after_receipt,
                      release_callbacks_after_controller, monotonic):
    """Future trusted engine seam, NOT a permission check or public activation.

    Never accepts an injected observer, cipher, backend or invented selector.
    Runtime construction remains inside the existing execution/controller seam.
    """
    bind_child(request=request, expected_request_sha256=expected_request_sha256,
        checked_sources=checked_sources, helpers=helpers,
        dependency_source_buffers=dependency_source_buffers, context=context, identity=identity)
    return runtime_wiring._dispatch_runtime(helpers=helpers,
        packet=request['dependency_packet'], fixed=request['dependency_fixed'],
        source_buffers=dependency_source_buffers, review_sha256=request['dependency_review_sha256'],
        folder=Path(request['folder']), control=control, context=context, identity=identity,
        records=records, make_callbacks_after_receipt=make_callbacks_after_receipt,
        release_callbacks_after_controller=release_callbacks_after_controller, monotonic=monotonic)


def run_invented(*, request, expected_request_sha256, checked_sources, helpers,
                 dependency_source_buffers, context, identity, ops, control,
                 records, make_callbacks_after_receipt, release_callbacks_after_controller,
                 monotonic):
    """Real authored controller, explicit invented observer, no runtime dispatch."""
    inputs = bind_child(request=request, expected_request_sha256=expected_request_sha256,
        checked_sources=checked_sources, helpers=helpers,
        dependency_source_buffers=dependency_source_buffers, context=context, identity=identity)
    return helpers.package.dependency_controller.run_invented(inputs=inputs, ops=ops,
        folder=Path(request['folder']), control=control, context=context, identity=identity,
        records=records, make_callbacks_after_receipt=make_callbacks_after_receipt,
        release_callbacks_after_controller=release_callbacks_after_controller, monotonic=monotonic)


def _saved_runtime(*, helpers, runtime_wiring, **saved):
    """Ordinary saved-runtime verifier only; never activates an observer."""
    return runtime_wiring._verify_saved_runtime(helpers=helpers, **saved)


def _parent_binding(*, request, expected_request_sha256, checked_sources, helpers,
                    inputs, process):
    validate_request(request, expected_request_sha256=expected_request_sha256,
                     checked_sources=checked_sources)
    need(helpers.mode == 'parent', 'adapter_helper_mode')
    helpers.intact()
    need(type(process) is dict and set(process) == PROCESS_FIELDS, 'adapter_process')
    need(all(type(process[n]) is bool for n in PROCESS_BOOLS) and
         all(type(process[n]) is int and 0 <= process[n] <= 1
             for n in ('launch_attempts', 'kill_attempts', 'wait_attempts')) and
         type(process['deadline_seconds']) is int and process['deadline_seconds'] == 300 and
         type(process['elapsed_seconds']) in (int, float) and
         math.isfinite(process['elapsed_seconds']) and process['elapsed_seconds'] >= 0,
         'adapter_process_shape')
    need(type(process['launch_attempts']) is int and process['launch_attempts'] == 1 and
         type(process['child_exit_code']) is int and process['child_exit_code'] == 0 and
         process['exit_observed'] is True and process['reader_threads_joined'] is True and
         process['pipe_close_complete'] is True and
         all(process[n] is False for n in ('timed_out', 'launch_failed',
             'log_cap_exceeded', 'log_reader_failed', 'kill_succeeded')) and
         process['kill_attempts'] == 0 and process['wait_attempts'] == 0,
         'adapter_process_incomplete')
    expected = dict(request['dependency_packet']['inputs'])
    need(type(inputs) is dict and set(inputs) == set(expected) | {'source_buffers'} and
         encoded({k: v for k, v in inputs.items() if k != 'source_buffers'}) == encoded(expected),
         'adapter_parent_inputs')
    need(inputs['expectation']['operation_id'] == request['operation_id'], 'adapter_operation')
    # Saved verifier revalidates the dependency binding and source digests.
    need(type(inputs['source_buffers']) is dict and
         set(inputs['source_buffers']) == set(policy.outer.CHILD) | {'closure_manifest'},
         'adapter_dependency_sources')
    for name in policy.outer.CHILD:
        need(inputs['source_buffers'].get(name) == checked_sources['dependency.' + name],
             'adapter_dependency_source_binding')
    need(inputs['source_buffers'].get('closure_manifest') == encoded(request['sources']),
         'adapter_dependency_closure')
    rebound = helpers.package.dependency_execution.bind_runtime_packet(
        request['dependency_packet'], request['dependency_fixed'], inputs['source_buffers'],
        request['dependency_review_sha256'])
    need(rebound == inputs, 'adapter_parent_inputs')


def reconcile_runtime(*, request, expected_request_sha256, checked_sources, helpers,
                      runtime_wiring, inputs, process, stdout, stdout_sha256,
                      dependency_sha256, bridge_sha256):
    """Require observed terminal cleanup before ordinary saved-record checks.

    Caller-owned process facts are not authenticated OS observations. Failure
    raises to the parent's existing needs_review path; no retry or cleanup here.
    """
    _parent_binding(request=request, expected_request_sha256=expected_request_sha256,
        checked_sources=checked_sources, helpers=helpers, inputs=inputs, process=process)
    result = _saved_runtime(helpers=helpers, runtime_wiring=runtime_wiring,
        folder=Path(request['folder']), inputs=inputs, operation_id=request['operation_id'],
        stdout=stdout, stdout_sha256=stdout_sha256, dependency_sha256=dependency_sha256,
        bridge_sha256=bridge_sha256)
    helpers.intact()
    return result


def reconcile_invented(*, request, expected_request_sha256, checked_sources, helpers,
                       inputs, process, stdout, stdout_sha256, dependency_sha256, bridge_sha256):
    _parent_binding(request=request, expected_request_sha256=expected_request_sha256,
        checked_sources=checked_sources, helpers=helpers, inputs=inputs, process=process)
    result = helpers.verify(folder=Path(request['folder']), inputs=inputs,
        operation_id=request['operation_id'], stdout=stdout, stdout_sha256=stdout_sha256,
        dependency_sha256=dependency_sha256, bridge_sha256=bridge_sha256, invented=True)
    helpers.intact()
    return result


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
