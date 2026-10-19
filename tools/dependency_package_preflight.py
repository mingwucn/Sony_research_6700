"""Complete package freshness collector, qualified with invented inputs only.

No dependency bootstrap, native loader, process, device or output-file API.
The ordinary CLI refuses; an actual observer/entry remains separately gated.
"""
import copy
import json

from tools import dependency_evidence as core
from tools import dependency_producer as producer


def _read(ops, path, row):
    expected = copy.deepcopy(row)
    raw, receipt = ops.reader(path, copy.deepcopy(expected))
    producer.need(type(raw) is bytes and len(raw) == expected['size'] and
                  producer.sha(raw) == expected['sha256'], 'fresh_bytes')
    core._receipt(receipt, path, expected['sha256'], expected['size'], expected['identity'])
    # Detach immediately; a later observer call cannot alter earlier evidence.
    return raw, copy.deepcopy(receipt)


def _collect(*, ops, inputs):
    policy, package, _, _, sources = producer.bind_inputs(**inputs)
    manifest = package['manifest']; original = package['installed_receipts']
    # Apply the concrete ordinary reader's bound before making any observation.
    producer.need(all(row['size'] <= 8*1024**2 for group in
                  (manifest['files'], policy['trusted_origins']) for row in group.values()), 'package_read_bound')
    before = {name: copy.deepcopy(ops.root(row['path'])) for name, row in policy['roots'].items()}
    producer.need({k: core._hash(v) for k, v in before.items()} ==
                  {k: v['identity_sha256'] for k, v in policy['roots'].items()}, 'root_identity')
    absolute = {}; projected = {}; projection = {}; checked = []
    by_path = {row['relative_path']: name for name, row in policy['python_origins'].items()}
    for relative in sorted(manifest['files']):
        path = policy['roots']['package']['path'].rstrip('/')+'/'+relative
        expected = dict(manifest['files'][relative],
            identity={k: original[relative]['lstat_before'][k] for k in core.CROSS})
        raw, receipt = _read(ops, path, expected)
        absolute[relative] = receipt
        # Lossless domain adapter: retain the entire absolute opened receipt,
        # and change only path in the separate manifest-relative projection.
        row = copy.deepcopy(receipt); row['path'] = relative; projected[relative] = row
        projection[relative] = dict(absolute_receipt_sha256=core._hash(receipt),
                                    relative_receipt_sha256=core._hash(row))
        if relative in by_path:
            name = by_path[relative]
            producer.need(raw == sources[name], 'fresh_cache_source')
            checked.append(name)
    producer.need(set(checked) == set(policy['python_origins']), 'fresh_source_roster')
    trusted = {}
    for name, row in policy['trusted_origins'].items():
        _, trusted[name] = _read(ops, producer.target(policy, row), row)
    after = {name: copy.deepcopy(ops.root(row['path'])) for name, row in policy['roots'].items()}
    producer.need(core._canonical(before) == core._canonical(after), 'root_changed')
    proof = dict(schema='activation_installed_proof_v1', status='installed_receipt_set_validated',
        roster_sha256=manifest['roster_sha256'], record_sha256=manifest['record_sha256'],
        files={p: dict(manifest['files'][p], open_identity_sha256=core._hash(row)) for p, row in projected.items()},
        **{k: False for k in core.FLAGS}, camera_commands=[])
    observed = dict(manifest=manifest, installed_receipts=projected, installed_proof=proof)
    core._package(observed)
    return dict(schema='dependency_package_collection_v1', status='complete_invented_package_collection',
        evidence_mode='invented', prior_package_sha256=core._hash(package),
        observed_package_sha256=core._hash(observed), package=observed,
        absolute_receipts=absolute, relative_projection=projection, trusted_origins=trusted,
        root_before=before, root_after=after, source_aliases=sorted(checked),
        raw_cache_sha256=policy['cache_sha256'],
        package_reads=len(absolute), trusted_reads=len(trusted),
        test_injection_used=True, dependency_bootstrap_performed=False,
        actual_installation_observed=False, atomic_snapshot_proven=False,
        operational_acceptance=False, execution_authorized=False,
        feature_supported=False, recovery_proven=False, device_write_gate_passed=False, camera_commands=[])


def collect_invented(*, ops, **inputs):
    """Test seam: never a grant to inspect an actual installation."""
    producer.need(not isinstance(ops, producer.RuntimeOps), 'real_activation_pending')
    return _collect(ops=ops, inputs=inputs)


def main():
    print(json.dumps(dict(status='needs_review', code='real_activation_pending', camera_commands=[])))
    return 2


if __name__ == '__main__': raise SystemExit(main())
