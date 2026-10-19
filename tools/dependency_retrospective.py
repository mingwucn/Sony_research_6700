"""Pure retrospective comparison; observations never become prior approval.

This module has no saved-file reader or executable source loader. Source hashes
are declarations supplied by the caller, not authenticated executing buffers.
"""
import hashlib

from tools import dependency_evidence as core
from tools import dependency_legacy as legacy


PRODUCERS = {
    'runtime': '4a64bd6c63ff6e43b56ab7298e5fb84a6304e3576990eaa4aa020c551aeba8f1',
    'continuation': '75ab70f9445ee9d1f072252fabaab8d0dca54c576b8b3b5b6ec874005a609592',
}
EXTRA_BLOCKERS = (
    'expectations_derived_after_historical_observation',
    'root_tokens_are_path_labels_not_directory_observations',
    'executing_source_buffers_not_authenticated',
    'cache_digest_declaration_not_content_revalidation',
)


def _origin(relative, row, domain):
    return dict(root=domain, relative_path=relative, sha256=row['sha256'],
        size=row['size'], identity={key:row['lstat_before'][key] for key in core.CROSS})


def _root(path, domain):
    # The old expectation schema requires a digest here. It is deliberately a
    # deterministic path LABEL, with an explicit blocker, never a stat identity.
    token = dict(schema='retrospective_path_label_v1', domain=domain, path=path)
    return dict(path=path, identity_sha256=core._hash(token))


def reconcile_legacy_metadata(*, package, config, completion, raw_receipt_json,
                              journal_jsonl, producer_sha256, cache_sha256):
    """Derive a labeled retrospective expectation and apply the legacy adapter.

    Caller data consistency only. No source/cache/installation observation,
    historical authentication, file reading or runtime activation is performed.
    Original transcript bytes (UTF-8 encoding of supplied text) are preserved.
    """
    try:
        core._text_bytes(raw_receipt_json)
        core._text_bytes(journal_jsonl)
        lines = journal_jsonl.splitlines()
        core._need(1 <= len(lines) <= 1024 and all(lines), 'journal_lines')
        raw = core._json_text(raw_receipt_json)
        journal = [core._json_text(line) for line in lines]
        package, config, completion, raw, journal, producer_sha256 = core._bounded_copy(
            [package, config, completion, raw, journal, producer_sha256])
        core._shape(producer_sha256, PRODUCERS)
        legacy._same(producer_sha256, PRODUCERS, 'retrospective_producer')
        core._digest(cache_sha256)
        manifest, receipts = core._package(package)
        core._shape(config, ('schema', 'operation_id', 'package_root', 'source_rows',
            'native_rows', 'trusted_origins', 'vectors'))
        core._shape(raw, legacy.RAW_KEYS)
        first = journal[0]
        core._shape(first, ('sequence', 'event', 'data'))
        core._need(first['event'] == 'integrated_entry_started', 'retrospective_startup')
        startup = first['data']['startup']
        package_path, leaf = legacy._origin_path(config['package_root']).rsplit('/', 1)
        core._need(leaf.casefold() == 'cryptodome', 'retrospective_package_root')
        runtime_path = legacy._origin_path(startup['base_prefix'])
        roots = dict(package=_root(package_path, 'package'), runtime=_root(runtime_path, 'runtime'))
        python_origins = {}
        for alias in legacy.ALIASES:
            tail = alias.replace('.', '/')
            relative = tail + ('/__init__.py' if alias in legacy.PACKAGES else '.py')
            python_origins[alias] = _origin(relative, receipts[relative], 'package')
        natives = {alias:_origin('Cryptodome/' + path, receipts['Cryptodome/' + path], 'package')
            for alias, path in legacy.NATIVE.items()}
        core._shape(raw['trusted_origins'], legacy.TRUSTED)
        trusted = {}
        for alias, relative in legacy.TRUSTED_PATHS.items():
            row = raw['trusted_origins'][alias]
            trusted[alias] = _origin(relative, dict(row, size=row['bytes']), 'runtime')
        expectation = dict(schema='dependency_expectation_v1', operation_id=config['operation_id'],
            platform='windows', backend='ctypes', extension_suffix='.pyd', roots=roots,
            python_origins=python_origins, native_libraries=natives, trusted_origins=trusted,
            source_sha256=producer_sha256,
            config_sha256=hashlib.sha256(core._canonical(config) + b'\n').hexdigest(),
            cache_sha256=cache_sha256, manifest_sha256=core._hash(manifest),
            installed_proof_sha256=core._hash(package['installed_proof']),
            vector_plan_sha256=legacy.PUBLIC_VECTOR_PLAN_SHA256, loader_kwargs={},
            no_fallback=True, bootstrap_boundary=['interpreter', 'stdlib', '_ctypes', 'os_loader'])
        envelope = legacy.adapt_legacy_dependency_records(expectation=expectation,
            package=package, config=config, completion=completion,
            raw_receipt_json=raw_receipt_json, journal_jsonl=journal_jsonl)
        # Retain every legacy blocker, even when this caller has declared the
        # reviewed producer hashes. A declaration does not bind executing code.
        return dict(schema='retrospective_legacy_comparison_v1',
            status='retrospective_consistency_with_blockers', envelope=envelope,
            expectation_basis=dict(
                package_origins='saved_installed_receipts_and_recomputed_proof',
                trusted_origins='saved_raw_trusted_origin_receipts',
                package_root='saved_configuration_path', runtime_root='saved_entry_startup_base_prefix',
                root_tokens='retrospective_path_label_v1_not_directory_identity',
                config_digest='canonical_configuration_plus_newline_not_input_file_digest',
                cache_digest='caller_declared_digest_only', producer_digests='caller_declared_reviewed_profile'),
            blockers=list(envelope['blockers']) + list(EXTRA_BLOCKERS),
            source_buffers_bound=False, source_cache_read=False, actual_records_observed=False,
            prior_expectation_approval_proven=False, historical_events_authenticated=False,
            execution_authorized=False, operational_acceptance=False, feature_supported=False,
            recovery_proven=False, device_write_gate_passed=False, camera_commands=[])
    except core.EvidenceError:
        raise
    except Exception:
        raise core.EvidenceError('retrospective_shape') from None
