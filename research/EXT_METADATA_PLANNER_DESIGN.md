# RA-003: bounded ext metadata read-planner design

2026-10-19 UTC / Europe/Paris. Topic branch
`codex/ra003-ext-planner-design`, parent
`e0075d93711f15a72e3eb888f327d2dab0633049`.
Native English and native camera-to-server Wi-Fi FTP remain first. FL2/FL3 is
deferred; calibrated custom still looks remain later and separately gated.
The optional bridge is **HOST-ASSISTED**. Camera commands: **none**.

## Before-code scope

The [previous observation](EXT_SUPERBLOCK_OBSERVATION.md) recorded two fixed
superblock metadata leads with matching classic feature masks. It did not
establish usable read plans. This package designs and qualifies the next pure
metadata planning layer with **invented inputs only**. No actual observation is
replayed, no saved actual numeric fields are evaluated by the planner, and no
descriptor, inode, directory or file is read from firmware.

Read the already pinned local Linux v6.6 source/documentation as reference text.
Preserve their GPL notices and pin their existing hashes. Author separate code
from documented facts and explicit policy; do not copy upstream implementation,
execute upstream source, infer a new licence or change the source lock. Make no
new download, installation, agreement acceptance or legal conclusion. Previous
analysis acts, accepted and refused trials, source seals and protected inputs
remain unchanged. Do not open firmware, operational constants or saved raw
prefixes, import an actual runner, or use device/network/USB/service interfaces.

## Proposed planning boundary

Use exact built-in bytes and integers, bounded lengths and fixed errors. The
unchanged pinned observer must recompute its fields from the supplied invented
prefix; a caller's old status, derived geometry or feature-mask boolean is not
trusted. Reapply and extend the geometry and feature policy before proposing a
primary contiguous group-descriptor table. All addresses are explicitly
**logical-member-relative file-byte offsets**, never firmware-package offsets,
runtime addresses or camera targets.

Freeze an exact API, closed output schema, reason-code vocabulary, resource
limits and all predicates before implementation, after independent source and
contract review. Model only classic 32-byte descriptors, rejecting unmodeled
features including journal/recovery, checksums, extents, 64-bit, meta/flex groups
and bigalloc. A project cap of **1,024 groups / 32,768 descriptor bytes** bounds
work before any count-dependent loop or allocation. This cap is a policy limit,
not a format maximum or evidence about the observed leads.

After stricter superblock counter, inode, primary-group and table-fit checks,
the first stage may propose the exact primary descriptor-byte span. A second
stage accepts only caller-supplied invented descriptors of the exact required
length. Validate every group's actual extent, bitmap/table bounds and overlap,
including primary/backup superblock, GDT and reserved-GDT occupancy. The sparse
backup pattern comes from the pinned documentation; stronger eligibility rules
must be labelled project policy. Do not treat a reserve allocation count as
disjoint from the free-block count. Ignore inactive raw high-count/descriptor
fields consistently with the preceding observer; do not manufacture corruption
from them.

Only after the complete descriptor set passes may the model propose the fixed
root inode-2 record span. The slot proposal proves neither allocation nor
directory type nor contents. It reads no inode or allocation bitmap and does not
follow an inode pointer or traverse a directory. Counter consistency and
metadata-placement checks are prerequisite models, not complete filesystem or
kernel acceptance. Dirty/error/orphan state, inactive descriptor fields and
unsupported combinations need explicit conservative handling rather than
unjustified corruption labels.

## Qualification and completion

Use only standard-library Python and invented prefixes/descriptors. Include
the unchanged 52 observer cases and meaningful new developer and independent
adversarial cases. Cover exact types, truncation and caps, exponent guards,
every feature-policy boundary, raw/effective distinctions, independent scalar
invariants, reserved/free overlap, group count and final-group arithmetic,
inode alignment and root-record bounds, descriptor length/count, sparse backup
groups, metadata overlaps and sums, deterministic detached closed outputs,
mutation/privacy and no I/O. Historical larger suites are historical evidence,
not a claimed fresh rerun.

Preserve development failures and exact commands, interpreter, exits, test IDs,
times and source hashes. Freeze reviewed sources for authoritative qualification;
do not adjust a threshold after evaluating actual data, which is excluded here.
Independently review the source, meaningful negative tests and final sanitized
publication. No generated firmware or table payload enters Git.

Every observer claim, actual-read authorization, filesystem/content/checksum,
authentication, backend/ABI, English/native FTP, device-write and recovery claim
remains false. Any returned range is a synthetic model proposal only. A future
actual descriptor observation requires its own scope, rights review, lineage,
source seal and non-retryable operation review; this design authorizes none.

Update STATE, backlog, handoff, artifact intake and external/private per-function
progress, private session/intake history and a sanitized session report. Review
only eight public paths (the six current documentation/state entry points, this
design and its report) before explicit staging and local commit. No push.
Select one next package from qualification/review; RA-003 and the overall
pre-camera goal remain incomplete while exact-target evidence is missing.

Scope status: detailed contract, independent review, implementation and synthetic
qualification pending. Preserve this before-code text; append outcomes below.


## Qualified synthetic outcome

Bounded ext metadata planner design: **174/174 synthetic passes**, zero skipped, exit **0**, **0.154s**; **52 retained + 122 new** cases; **8** qualified source/test pins. Invented buffers exercise primary-GDT and root-record proposals with counter, inode and group/reserved-metadata placement checks. All **13** retained ordinary source pins, prior actual results, analysis acts and source lock remain unchanged; no new source acquisition or historical full-suite rerun.

Limits: **1,024 groups**, **32,768 descriptor bytes**, **4,096 prefix bytes** (project budgets). No actual metadata/firmware application, traversal, raw output or camera; planning authorization and all filesystem/content, native English/FTP, recovery and device-write claims remain false.

See [exact commands/results](sessions/20261019-RA-003-ext-planner-design.md).
Next single package: **RA-003: review and freeze the rights, lineage and byte limits for a bounded primary-GDT descriptor-metadata observation using the qualified planner; no inode/content traversal**.
