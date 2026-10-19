# RA-003: selected-member prefix identification

## Before-read scope

Recorded 2026-10-18 UTC / 2026-10-19 Europe/Paris on topic branch
`codex/ra003-member-prefix`, parent `e1f421f10da8d85ea20775f8a3abb774b8a302c5`.
Previous goal turn: progress; consecutive no-progress count **0**.
Native English and native camera-to-server Wi-Fi FTP remain primary.
Camera commands: **none**.

The [accepted private tar directory](TAR_LINK_INVENTORY.md) contains 137 entries.
This package uses its metadata to select a minimal set of regular, nonempty
members for child-format discovery. The private selection review records exact
member identities, file spans and name-based rationale. Names are selection leads,
not evidence of application contents, English resources or an FTP backend.
No symlink or hard-link target is followed; no selected name becomes a host path.
Boot/recovery/loader, settings/region tables and unrelated assets are excluded.

The reviewed selection is **five image-category regular members**, **4,096 bytes
each**, **20,480 bytes total**. This covers the image-named category without
choosing an arbitrary subset from names alone; it is not a claim of globally
minimal English/FTP contents. All 132 other entries have private exclusion
rationales. Exact accepted records and selection-review provenance stay private.

The necessary private format-study rationale from the
[decoding plan](FDAT_DECODING_PLAN.md) continues within this bounded step.
Accepted-contract interaction and independent constants derivation remain
unresolved. This is not blanket clearance for member files, decompression,
disassembly, distribution, modified firmware or device work. No new download,
dependency installation, agreement, private upload or upstream execution.

## Selection, bounds and acceptance

Select at most **eight regular members**, with at most **4,096 bytes** from each
member's payload start, maximum **32,768 raw prefix bytes**. If a selected member
is shorter, retain only its declared length; explicitly count prefixes that
transiently cover an entire member. No accepted output retains raw member bytes.
Exact selection, rationale, indices,
complete original directory records and source-result hash are frozen privately
before source I/O. Opaque sequential labels identify probes; do not publish names,
targets, member positions, member/prefix hashes or raw bytes.

Every selected record must exactly match the accepted prior directory, including
regular type, size, labelled file positions, header and complete-payload hashes.
Keep type-aware validation, strict built-in metadata types, unique indices/labels,
non-overlapping payload spans and bounds. Deep-copy caller state so later mutation
cannot alter the selection. Prior directory compact UTF-8 JSON remains bounded to
**2 MiB**. Existing tar member guards and opaque-link metadata policy are unchanged.
All offsets are **decoded-FDAT file offsets** or explicitly tar-relative file
positions; none is a camera storage, virtual or runtime address.

Qualify the exact authored sources with synthetic bytes before the new experiment.
The combined suite must pass **202 cases**: the unchanged 171 plus 17 collector
and 14 coordinator/pipeline cases. Freeze all **23 qualified sources plus the
reviewed runner (24)** and the four authored dependency hashes.
Cover selection/type/label/index/record/bounds failures, cap enforcement, chunk
edges and short members, mutation isolation, incomplete observations, classifier
failure, single-use state and cleanup. Integration must inject late envelope and
parent-hash failures after tentative selected-prefix capture and tar end. A failed
pipeline must expose no accepted selected metadata or raw prefixes. A changed
fresh directory, including payload hashes, must refuse before member classification.

One pipeline, two planned complete-parent passes on the same original ordinary
read-only, single-link, non-reparse descriptor. Recheck the complete package,
logical stream, header, declared spans, both original component prefixes, tar
directory and full member/extent hashes. Only after the fresh accepted directory
exactly matches the prior private directory may selected-prefix classification
run. Capture all prefixes in bounded memory during that same decoding pass;
never reopen a child file or rerun on failure. Existing lineage and tar checks
remain intact. An exclusive/fsynced journal precedes input I/O; a failure enters
**needs_review** and clears tentative observers. No retry, key/parser fallback or
changed experimental acceptance threshold during the run.

Use only the unchanged bounded signature/header classifier. Its closed output
has format/status and `container_validated=false`, `abi_verified=false`.
No strings search, offset following, decompression, disassembly or firmware code
execution. A header candidate cannot establish a mountable/complete child format,
AP/CP ownership, resource semantics, executable ABI, English availability, native
FTP, authenticity, exact-body correspondence or recovery. Unknown/malformed
results remain negative observations within the fixed probe, not proof of absence.

Retain private selection and metadata only; release raw prefix buffers on both
success and failure. No member/decoded-stream/raw-prefix files. The managed
pipeline **design allowance is 16 MiB**, including the former 8 MiB design and
additional prior/working/encoded metadata allowance; it is not a measured or
enforced whole-process cap. Python objects, native crypto allocation and pretty
JSON overhead are not bounded by compact JSON lengths. Clearing references does
not guarantee secure erasure; observable source checks are not an atomic snapshot.

Freeze this scope, selected-plan hash, exact qualified source/test/runner hashes
and qualification receipt before the single actual read. Existing firmware and
crypto inputs stay private; no target profile, feature or device-write gate passes.

Status at scope creation: selection finalization, implementation and qualification
pending. Append actual observations separately; preserve frozen scope privately.


## Observed result

One selected-member prefix experiment completed, script and host exit **0**, **32.470943s**.
Synthetic qualification **202/202 passed**, zero skipped, exit **0**, **1.317s**.
**Five regular image-category candidates**, **4,096 bytes each / 20,480 bytes total**;
all five returned **unknown / unsupported_opaque** under the fixed classifier.
Complete fresh source/stream/header/span/original-prefix lineage and exact whole
directory equality passed before selected classification. No complete member
was covered by these prefixes; raw buffers discarded, no child files or links followed.
Classifier coverage is limited; this does not establish missing formats, English
resources or FTP code. No decompression/disassembly, camera or feature/write gate.

All five unknown results are preserved. No parser/key fallback or acceptance-rule
change occurred. No format or feature absence follows from these predicates.

Next single package: **RA-003: audit pinned image-format parser sources and reuse rights, then design and synthetically qualify bounded structural header predicates for the five opaque candidates before another actual read**.
See [exact commands/results](sessions/20261018-RA-003-member-prefix.md).


## Later source-only image-header design (2026-10-19 local / 2026-10-18 UTC)

Earlier next-package recommendations are historical. See [header design](IMAGE_HEADER_DESIGN.md)
and [commands/results](sessions/20261018-RA-003-image-header-design.md).
Four public parser blobs (**16,708 bytes**) verified at the existing immutable pin;
published MIT notice reviewed and preserved with private source copies.
Separate bounded AXFS/ext-family/legacy-FAT/LZPT header predicates qualified
with **251/251 synthetic passes** (49 new plus 202 retained),
zero skipped, exit **0**, **1.271s**. All 23 baseline files unchanged.
The new API remains standalone and unintegrated. **No actual firmware, member
prefix or operational-constants read**; prior five unknown observations unchanged.
No filesystem, English, native FTP, body-match, recovery or device-write gate.

Next single package: **RA-003: implement and qualify an all-prefix reconciliation gate, then run one frozen expanded-header comparison on the same five members with full prior lineage**.


## Later refused expanded trial (2026-10-19 local / 2026-10-18 UTC)

Earlier next-package recommendations are historical. See [trial](EXPANDED_PREFIX_AUDIT.md)
and [commands/results](sessions/20261018-RA-003-expanded-prefix.md).
One frozen same-five expanded-header trial stopped **needs_review**, script exit **2**, host exit **1**, **38.945781s**.
Qualification **278/278 passed**, zero skipped, exit **0**, **2.001s**; 27 new cases plus 251 retained, all 27 foundation files unchanged.
Failure code **expanded_prefix_acceptance_failed**; no accepted expanded candidates, fresh directory or persisted stream-validation result.
Static source/metadata review finds float timing fields in prior summaries rejected by the new freezer; this is a sufficient blocker, not a logged precise runtime stage.
Observer cleanup reported no failures. No retry, fallback, changed threshold, child files or raw-prefix output.
Earlier five unknown classifications and all prior evidence remain unchanged. No decompression/disassembly, upstream/firmware execution, camera or feature/write gate.

Next single package: **RA-003: design and synthetically qualify exact prior-metadata preflight using preserved production summaries, resolving the timing-field schema mismatch before any new actual prefix read**.


## Later metadata-only preflight qualification (2026-10-19)

Earlier next-package recommendations are historical. See [preflight](METADATA_PREFLIGHT.md)
and [commands/results](sessions/20261019-RA-003-metadata-preflight.md).
Metadata-only qualification **320/320 passed**, zero skipped, exit **0**, **7.649s**; **42 new + 278 retained** cases.
**30** retained source/test files and all **32** historical failed-trial source/runner pins remain unchanged.
Only the new session gate copy is revised; its preflight preserves every field and exact type, with a narrow allowance for finite nonnegative built-in timing floats at two root keys in two prior-summary roles.
Production metadata shapes, signed zero, bounded trees, fixed role/stage diagnostics, mutation isolation and cleanup flags are qualified offline.
No firmware/key/raw-prefix input, actual replay, new download, upstream execution, camera or feature/write gate.
The earlier expanded trial remains **needs_review**, script **2** / host **1**; its precise runtime refusal stage stays unrecorded.
Earlier five unknown classifications and all other actual results remain unchanged. A future pre-I/O runner is still to be frozen and reviewed.

Next single package: **RA-003: freeze and review a runner with pre-I/O metadata preflight and bounded stage diagnostics, then run one separately scoped same-five expanded-header comparison with complete prior lineage**.


## Later separately frozen preflight comparison (2026-10-19)

Earlier recommendations are historical. See [comparison](PREFLIGHT_COMPARISON.md) and
[commands/results](sessions/20261019-RA-003-preflight-comparison.md).
Qualification **346/346 passed**, zero skipped, exit **0**, **12.080s**; **26 new + 320 retained** cases; all **35** predecessor files and **32** historical failed-trial pins preserved.
Actual terminal **complete_private_preflight_expanded_member_comparison**, script **0** / host **0**, **37.595937s**; pipeline attempts **1**, expanded callback attempts **5**.
Source observation **source_read_confirmed**; protected callback attempts are separate and missing preliminary verification does not establish no I/O.
One separately frozen same-five comparison passed its complete lineage and original-outcome checks; limited expanded header leads were recorded after pre-I/O metadata preflight.
No retry, fallback, child/decoded/raw-prefix files, decompression/disassembly, upstream/firmware execution, camera or feature/write gate.
Earlier five unknown outcomes and prior refusal remain unchanged; no retroactive runtime-stage claim.
Sanitized header-lead counts: ext_family_header_candidate/header_only: 2; fat_legacy_header_candidate/malformed_header: 2; unknown/unsupported_opaque: 1.
Selected raw retention remains bounded separately from metadata copies. Six retained prior trees and seven gate snapshots may coexist, each with a 2MiB serialized-role limit, plus caller objects/overhead/other buffers. Historical20MiB pipeline allowance is not an aggregate managed/process memory cap.

Next single package: **RA-003: design and synthetically qualify a bounded ext-family superblock capability and geometry gate using pinned authoritative format sources; no actual replay or directory traversal**.
