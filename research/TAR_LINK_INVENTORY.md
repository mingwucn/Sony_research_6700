# RA-003: tar directory with opaque link-target metadata

## Before-read scope and policy decision

Recorded 2026-10-18 UTC / 2026-10-19 Europe/Paris on
`codex/ra003-tar-link-inventory`, parent
`0f193f706d356b13dd5d3f9f894842f7efbe5c2f`. Previous goal turn: progress.
English and native Wi-Fi FTP remain first. Camera commands: **none**.

The [previous trial](TAR_DIRECTORY_AUDIT.md) refused a conservative path guard.
The [separate full-lineage diagnostic](TAR_PATH_DIAGNOSTIC.md) identifies a
header-supplied link target and the combined `empty_or_parent_component`
predicate. It does not distinguish empty components from `..` or prove link
validity. Both experiments and their original rules remain preserved.

This package deliberately changes **link-target metadata policy only**, before
its new experiment. The former extraction-oriented path rule unnecessarily
constrained lexical link text for an observer that never creates files or
resolves links. A tar link target may be recorded as uninterpreted metadata;
its syntax does not become a host destination or a claim of a valid/resolvable
target. The need is a bounded directory inventory to choose later English/FTP
research inputs, not an extraction path or a permissive device profile.

Member names retain the original conservative `safe_name` guards, canonical
NFC/dot handling and duplicate checks. For hard/symbolic links **only**, retain
exact UTF-8 target text, **1..1,024 bytes**, with the original strict UTF-8 and
Cc/Cf/Cs control/format/surrogate rejection. Do not normalize or interpret it.
Absolute, backslash, drive-like, parent, empty-component, trailing-slash and dot
syntax may be metadata; empty target bytes remain rejected. GNU/PAX effective
link selection and all other extension/header/member guards remain unchanged.

Every link record and accepted directory must explicitly identify the opaque
metadata policy, no resolution/following/normalization/materialization and no
extraction-path-validation claim. Names/targets are never used for host I/O.
Future extraction would need its own path/link policy and scope; this inventory
cannot be passed off as a list of safe extraction destinations.

## Input, scope and fixed bounds

Use only the existing private official package, previously tested experimental
hypothesis and pinned private crypto dependency. Twelve qualified authored
foundation/test files copied unchanged; a narrow authored observer fork and
acceptance wrapper are separately reviewed and qualified. No download,
installation, new agreement, private upload, upstream launcher, firmware code
execution or camera/USB command.

Necessary private directory-format study follows the previously documented
[narrow research rationale](FDAT_DECODING_PLAN.md). Accepted-contract interaction
and independent constants derivation remain unresolved. No blanket clearance
for member copies, decompression, disassembly, distribution or device work.

Selected declared firmware extent: decoded-FDAT file offset **1,253,888**, length
**1,018,763,264**, end exclusive **1,020,017,152**. These are file positions,
never camera storage, virtual or process addresses. Revalidate fresh complete
parent/logical-stream identities, header, all declared spans and both prior
4,096-byte prefixes before any directory is accepted.

Keep the previous parser subset and caps: 512-byte headers; POSIX ustar/ordinary
GNU; regular files/directories/hard links/symbolic links; bounded GNU L/K and PAX
x/g; 64 KiB extension payload; 4,096 members; 8,192 physical headers; bounded
global PAX; **2 MiB compact UTF-8 directory JSON**, including new policy fields.
Keep unsigned checksums, nonnegative octal, raw extension size, effective member
bounds, zero member padding, two zero end blocks, zero remainder and no dangling
extensions. Unknown/sparse/base-256/special forms still refuse. No new fallback.

Retain private names, opaque link text, types/sizes, labelled tar-relative and
decoded-FDAT file spans, header/payload hashes and counts. Hash regular payloads
and the complete extent without retaining payloads. No member, decoded-stream
or raw prefix files. Publish aggregate observations and identities already
appropriate to sanitized provenance; private names/targets/member hashes stay
local. No later member-prefix classification is included in this experiment.

Managed pipeline design budget remains **8 MiB**, including the unchanged nested
stream reader's 5 MiB budget. This is not a measured/capped whole-process memory
or secure-erasure guarantee. Fixed JSON limits exclude Python object and pretty
printing overhead; no OS sandbox or atomic filesystem snapshot is claimed.

## Qualification and one new experiment

Synthetically qualify the exact sources before real source I/O. Test intentional
link-policy differences, verbatim link text, hard/symbolic and GNU/PAX origins,
unchanged unsafe/duplicate member refusal, UTF-8/control/size/caps, framing/end/
tail and cleanup. Verify the header fork's unaffected code matches its original.
Test exact class/selected-extent/policy/schema binding, complete prior lineage,
late source/envelope/parent/prefix mismatches after tentative directory end and
no accepted metadata on failure. No firmware or operational constants in tests.

Freeze this scope, source/test/runner hashes and qualification receipt before
actual source I/O. Exclusive/fsynced journal first. One pipeline with two planned
complete-parent passes on the same ordinary local read-only, single-link,
non-reparse descriptor: preliminary framing/hash, then decoding with full parent,
envelope/terminal, logical-stream/header/spans and observable source-state checks.
Only after source/stream/prefix lineage succeeds may the tar observer finish;
validate exact opaque-policy/schema/counts/bounds before releasing its metadata.
Any failure discards tentative observers and enters **needs_review**. No automatic
retry, key/parser fallback or acceptance-policy change during the experiment.

Framing and hashes cannot establish child formats, signatures/authenticity,
exact-body correspondence, AP/CP architecture, resources/backend/ABI semantics,
recovery, a requested feature or a device-write gate. A package is not a body
backup. No feature support or device gate passes from this directory inventory.

Status at scope creation: implementation, qualification and inventory pending.
Preserve these scope bytes privately; append actual observations separately.


## Observed inventory

One bounded opaque-link directory inventory completed, script and host exit **0**, **29.409064s**.
Synthetic qualification **171/171 passed**, zero skipped, exit **0**, **1.060s**.
Private inventory: **137 members** (97 regular files, 39 directories,
0 hard links, 1 symbolic link); **80182** compact UTF-8 JSON bytes.
Complete source/stream/header/span/prefix lineage, tar framing, member padding,
two end blocks and zero remainder checked. Link targets are opaque private
metadata, never followed/resolved/materialized or claimed safe for extraction.
Member-path guards unchanged; the link-policy change was documented before
this trial. No child files, decompression/disassembly, camera or feature/write gate.
Member formats and English/FTP mapping remain unverified; earlier evidence preserved.

The accepted directory proves only the declared metadata/framing/hash policy.
Detailed names/targets/member identities remain private. No link resolution,
complete child format, resources/backend semantics, body or recovery result follows.

Next single package: **RA-003: review the private directory to select minimal English/FTP-relevant members, then document, qualify and run bounded in-memory prefix identification with full lineage and no child files**.
See [exact session commands/results](sessions/20261018-RA-003-tar-link-inventory.md).
