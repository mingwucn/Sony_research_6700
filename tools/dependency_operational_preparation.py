"""Source-owned preparation for the disabled operational engine.

Private preparation may read authored sources and construct retained metadata
validators. Public activation refuses. Pending records establish no new consent.
The outer caller must capture/pin this complete source owner before use.
"""
if __name__ == '__main__':
    raise SystemExit(2)

import sys
from pathlib import Path
from tools import dependency_operational_metadata as metadata
from tools import dependency_host_entry as host


class CallbackLease:
    """Preparation retains cleanup responsibility until engine release."""
    def __init__(self):
        self.value = None
        self.attempted = self.closed = False

    def __call__(self, *args, **kwargs):
        metadata.need(self.value is not None and not self.attempted,
                      'operational_callbacks_inactive')
        return self.value(*args, **kwargs)

    def close(self):
        metadata.need(not self.attempted, 'operational_callbacks_reclose')
        self.attempted = True
        outcome = self.value.close()
        metadata.need(outcome is True or outcome is None, 'operational_callbacks_close_unknown')
        self.closed = True
        return True


class Preparation:
    def __init__(self, *, source_owner, adapter_owner, request_bytes,
                 request_sha256, checked_sources, documents, original_receipts,
                 ordinary, ordinary_receipts, legacy_seal_sha256, reference_pins,
                 prepared_repository_root, historical_migration=None):
        self.source_owner = source_owner
        self.adapter_owner = adapter_owner
        # Copy mutable containers; buffers themselves are immutable.
        self.request_bytes = request_bytes
        self.request_sha256 = request_sha256
        self.checked_sources = dict(checked_sources)
        self.documents = {n:documents[n] for n in ('candidate','review','decision','seal')}
        self.documents['inputs'] = dict(documents['inputs'])
        self.ordinary = dict(ordinary)
        self.original_receipts = metadata.strict(metadata.encoded(original_receipts))
        self.ordinary_receipts = metadata.strict(metadata.encoded(ordinary_receipts))
        self.reference_pins = metadata.strict(metadata.encoded(reference_pins))
        self.legacy_seal_sha256 = legacy_seal_sha256
        self.prepared_repository_root = prepared_repository_root
        # Buffers/pins are immutable; no caller-owned nested container survives.
        if historical_migration is not None:
            metadata.migration_receipts(historical_migration)
        self.historical_migration = None if historical_migration is None else dict(historical_migration)
        self.bootstrap_modules = {}
        self.callback_lease = CallbackLease()
        self.started = self.closed = self.failed = False
        self.preflight = self.validated = None

    def arguments(self, validated):
        arguments = dict(documents=self.documents, original_receipts=self.original_receipts,
            validated=validated, request_bytes=self.request_bytes,
            request_sha256=self.request_sha256, checked_sources=self.checked_sources,
            adapter_owner=self.adapter_owner, ordinary=self.ordinary,
            ordinary_receipts=self.ordinary_receipts,
            outer_source_receipts=self.source_owner.receipts(),
            prepared_repository_root=self.prepared_repository_root)
        if self.historical_migration is not None:
            arguments['historical_migration'] = dict(self.historical_migration)
        return arguments

    def _validate_gate(self):
        gate = self.source_owner.modules['retained_gate']
        if self.historical_migration is None:
            return gate.validate_bundle(self.documents,
                expected_seal_sha256=self.legacy_seal_sha256, reference_pins=self.reference_pins)
        metadata.need(metadata.sha(self.request_bytes) == self.request_sha256,
                      'operational_original_request')
        metadata.migration_receipts(self.historical_migration)
        return gate.validate_bundle_v6(self.documents,
            expected_seal_sha256=self.legacy_seal_sha256, reference_pins=self.reference_pins,
            expected_operation_id=metadata.strict(self.request_bytes)['operation_id'],
            **self.historical_migration)

    def _refresh(self, validated):
        return host.refresh_sources(validated, self.source_owner.modules['ordinary_io'])

    def _materialize(self, validated, fresh):
        # No call to invented HostPreparation or its invented metadata grammar.
        return host._prepare_modules(validated, fresh,
            self.source_owner.modules['retained_gate'],
            self.source_owner.modules['ordinary_io'], self.bootstrap_modules)

    def prepare(self):
        metadata.need(not self.started and not self.closed, 'operational_preparation_reentry')
        self.started = True
        try:
            self.source_owner.intact()
            validated = self._validate_gate()
            # Legacy accepted documents are checked only as retained comparison
            # inputs. The new activity record still requires all five pending.
            self.preflight = metadata.validate_pending(**self.arguments(validated))
            for name, role in (('dependency_successor_wiring','successor_wiring'),
                               ('dependency_successor_sources','namespace'),
                               ('ordinary_io','ordinary_io'),
                               ('parent_verifier','dependency.dependency_parent')):
                metadata.need(self.source_owner.buffers[name] == self.checked_sources[role],
                              'operational_outer_prepared_source')
            request = metadata.strict(self.request_bytes)
            rows = validated['inputs']['source_cache']['sources']
            selected = {n for n in rows if n.startswith('role:') or n in (
                'bootstrap:activation_binding','bootstrap:io_entry','integration:prospective_child')}
            metadata.need(len(selected) == 29, 'operational_retained_source_roster')
            for key in selected:
                role = 'bound.'+key
                metadata.need(self.checked_sources[role] == validated['source_buffers'][key],
                              'operational_retained_source_bytes')
                metadata.need((Path(self.prepared_repository_root) /
                    request['sources'][role]['path']) == Path(rows[key]['path']),
                    'operational_retained_source_origin')
            self.source_owner.intact()
            fresh, _ = self._refresh(validated)
            metadata.need(set(fresh) == selected and all(
                fresh[n] == self.checked_sources['bound.'+n] for n in selected),
                'operational_fresh_source_binding')
            self.source_owner.intact()
            self.validated = validated
            modules, auxiliary, callbacks = self._materialize(validated, fresh)
            self.callback_lease.value = callbacks
            self.source_owner.intact()
            return modules, auxiliary, self.callback_lease
        except BaseException:
            self.failed = True
            # Engine owns preparation teardown, including failed prepare. Do
            # not self-close and force its caller to reclose an uncertain owner.
            raise

    def close(self):
        metadata.need(not self.closed, 'operational_preparation_reclose')
        self.closed = True
        primary = None
        lease = self.callback_lease
        if lease.value is not None:
            try:
                if not lease.attempted:
                    lease.close()
                else:
                    metadata.need(lease.closed, 'operational_callbacks_close_unknown')
            except BaseException as error:
                primary = error
        for module in reversed(tuple(self.bootstrap_modules.values())):
            alias = module.__name__
            try:
                metadata.need(sys.modules.get(alias) is module, 'operational_bootstrap_ownership')
                del sys.modules[alias]
            except BaseException as error:
                if primary is None:
                    primary = error
        if primary is not None:
            raise primary
        return True


def verify_saved_preflight(*, source_owner, raw, expected_sha256, arguments):
    """Recompute from the parent's original bytes, never trust saved coverage."""
    source_owner.intact()
    result = metadata.verify_saved(raw=raw, expected_sha256=expected_sha256, **arguments)
    source_owner.intact()
    return result


def reconcile_saved_parent(*, source_owner, raw, expected_sha256, preflight_arguments,
        request, request_sha256, checked_sources, adapter_owner, helpers,
        parent_source_buffers, inputs, process, stdout, stdout_sha256,
        dependency_sha256, bridge_sha256):
    """Bind original preflight before the fixed source-owned parent engine.

    Supplied process facts remain caller-owned: this is not an OS supervisor or
    completion receipt. The future launcher must obtain them from its process.
    Helper/adapter ownership transfers here even on preflight refusal. The
    separate outer source owner remains caller-owned after engine teardown.
    """
    transferred = False
    try:
        source_owner.intact()
        engine = source_owner.modules['dependency_operational_entry']
        metadata.need(preflight_arguments['adapter_owner'] is adapter_owner and
            preflight_arguments['checked_sources'] == checked_sources,
            'operational_parent_preflight_owner')
        metadata.same(request, metadata.strict(preflight_arguments['request_bytes']),
                      'operational_parent_original_request')
        metadata.need(request_sha256 == metadata.sha(metadata.encoded(request)),
                      'operational_parent_request_hash')
        metadata.same(preflight_arguments['outer_source_receipts'], source_owner.receipts(),
                      'operational_parent_outer_sources')
        metadata.need(parent_source_buffers['dependency_parent'] ==
            source_owner.buffers['parent_verifier'] and checked_sources['successor_wiring'] ==
            source_owner.buffers['dependency_successor_wiring'] and checked_sources['namespace'] ==
            source_owner.buffers['dependency_successor_sources'], 'operational_parent_source_binding')
        verify_saved_preflight(source_owner=source_owner, raw=raw,
            expected_sha256=expected_sha256, arguments=preflight_arguments)
        source_owner.intact()
        transferred = True
        result = engine._reconcile_parent(request=request, request_sha256=request_sha256,
            checked_sources=checked_sources, adapter_owner=adapter_owner, helpers=helpers,
            parent_source_buffers=parent_source_buffers,
            runtime_wiring=source_owner.modules['dependency_successor_wiring'],
            inputs=inputs, process=process, stdout=stdout, stdout_sha256=stdout_sha256,
            dependency_sha256=dependency_sha256, bridge_sha256=bridge_sha256)
        source_owner.intact()
        return result
    except BaseException as primary:
        if not transferred:
            # This function is already trusted by its caller. Do not execute an
            # unvalidated engine just to acquire or tear down these owners.
            cleanup = None
            for owner in (helpers, adapter_owner):
                try:
                    outcome = owner.close()
                    metadata.need(outcome is True or outcome is None,
                                  'operational_parent_close_unknown')
                except BaseException as error:
                    if cleanup is None:
                        cleanup = error
            if cleanup is not None:
                raise primary from cleanup
        raise


def run_runtime(**kwargs):
    raise ValueError('real_activation_pending')
