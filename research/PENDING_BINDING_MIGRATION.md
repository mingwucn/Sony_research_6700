# Pending source and request migration

2026-10-22. Evidence: **static-inference**, **offline-tested** with invented
metadata. English and native camera-to-server Wi-Fi FTP remain first. Camera
contact remains on owner hold.

The private draft records an exact proposed source selection and the order in
which a future request's hash links would need rebuilding. It has its own
review-only schema. It contains no current candidate, review, decision, seal,
executable packet or runnable command. The frozen proposal remains unchanged.

## Proposed source selection

The comparison has 51 roles: 49 child and two host roles. Contract and outer
validators extend this to 53; the observation launcher extends it to 54. The
46 prepared roles are derived through the existing explicit alias map. Their
byte identities are unchanged.

Five authored roles changed since the frozen proposal. A sixth replacement is
the explicit gate selection below; that selection has not been applied.

| Role | Proposed ordinary source | SHA-256 |
|---|---|---|
| host.launcher | tools/dependency_operational_launcher.py | `8ff194d6a954904c0e0345edf4f0ae3f375213372d98421e90a7620e64bb09a1` |
| host_entry | tools/dependency_host_entry.py | `78be04ce3bc3532a44162feb801b5e95525431f3986256ddd26fe39525d774ae` |
| operational_metadata | tools/dependency_operational_metadata.py | `c539ab4a5592627b4c8bef069a9ff9567910f5842cf2fdfd07a9e387afefce14` |
| operational_preparation | tools/dependency_operational_preparation.py | `25e8f3ebd2a2d050e6a3e9a3b311b98709aaf08a12225167dd0431e384e895ba` |
| process_child | tools/dependency_operational_child.py | `58b6d62fc66cdb68ce45d8c67e05de8ea50c75b4c43fa489aac2ab5a88a047b6` |
| retained_gate | tools/dependency_historical_gate.py | `25663aadb151d0cf9fe4b287accda99a52153bd7b12895f5b233bdee4db44459` |

The old selected gate does not declare `validate_bundle_v6`; the proposed gate
does. Declaration and matching source hashes do not establish gate compatibility
or runtime qualification. No actual gate validation was performed.

## Request preparation order

1. Preserve the six original comparison buffers, all 16 frozen assembly records
   and historical cache/config identities. Do not rewrite their operation IDs.
2. Review the current 51-role source selection and unchanged 46-role projection.
   Future source expectations must remain `freshness_verified=false`.
3. Build separate current dependency packet/fixed bindings before selecting a
   current request. Preserve the historical comparison's `record_sha256`,
   `expected_files` and `native_policy` nulls. No fresh dependency observation is
   claimed.
4. Bind a future request core to final source-manifest and dependency-fixed
   bytes, a separately chosen current operation and result folder, and the
   unchanged scope-policy semantics. None of these actual records is emitted.
5. Follow the acyclic hash chain: request → scope → pending dispositions →
   qualification index → proposal. Preserve every pending disposition and empty
   evidence list. Retain exact original-comparison receipts.
6. Bind the proposal's exact ten-element argv to its core path and whole-byte
   hash. The observation request and nested prepared-adapter request are separate
   objects and hash domains. No operational folder, packet or command is created.

Historical migration is a separate four-field handoff: context bytes/hash and
ancestry-proof bytes/hash, bounded to 16 KiB and 64 KiB. It must bind unchanged
historical config/seal identities while the current operation remains distinct.
No actual migration context or proof was selected or opened here.

## Checker limits

The pure proposal checker can establish internal consistency while all five
dispositions remain pending. Its decided-scope entry must still refuse such a
proposal. The outer observation preflight requires separately decided scope;
the nested projection also needs complete current candidate/review/decision/seal
inputs. None was invented for the actual research route.

The synthetic migration fixture uses exact current bytes for the six proposed
outer replacements. All remaining source strings and records are invented.
Preserving nulls in opaque comparison buffers does not validate their semantics.
The checker does not inspect a gate's implementation: a consistently reanchored
inert gate can pass proposal consistency. Independent source selection and gate
qualification therefore remain necessary.

The operational parent and child still refuse v6. The earlier isolated success
used a separate inert test adapter and `subprocess.run`; genuine retained parent
supervision and saved-result reconciliation remain unqualified. No actual
dependencies, GDT contents, English resources or FTP backend were observed.

[Exact qualification, commands and remaining work](sessions/20261022-pending-binding-draft.md).
