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
