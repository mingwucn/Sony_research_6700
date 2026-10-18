# RA-003 artifact intake and bounded inspection

Status: official mainland 2.00 package acquired; UFU framing inventoried.
The bounded-memory FDAT stream trial measured logical length/SHA and checked
declared extents against measured EOF. No component files retained or formats
validated. Later bounded prefixes match SquashFS v4 and ustar header predicates;
these are candidates, with directory contents, body correspondence and later
copying/analysis scope still open.
Current intake (2026-10-18, **source-report**): the owner reports α6700
firmware **2.00**, current **简体中文**, **Chinese mainland version**, and
**English unavailable**. The full list is not supplied; exact SKU and binary
identity remain unverified. This is an owner report, not a target resource or
restriction-field finding. See [latest intake](../research/sessions/20261018-owner-mainland-english.md).
The later ordinary download supplies an official version-labelled package,
without proving exact-body applicability. No body program/resource/settings/
calibration readback has been supplied. Earlier private-directory checks were not a whole-computer
search. See [owner intake](../research/sessions/20261018-owner-ui-intake.md).
Owner additionally requires verified rollback/recovery before any firmware write;
offline package inspection does not establish that recovery system.

Earlier snapshot: the [version 2.00 provenance/rights review](../research/OFFICIAL_PACKAGE_INTAKE.md)
now identifies official package metadata, but one asset GET stopped at an
unreviewed redirect with zero firmware bytes and no file. Owner inspection
permission is **No / unknown**; proprietary firmware analysis remains blocked.
Sony separately lists 34 open-source packages. The owner approved two BusyBox
source downloads under its notice; their licences, supplied FTP-enabled configs
and client source were reviewed privately as data. No downloaded source was
executed. Neither route establishes exact-body correspondence or recovery.

Latest continuation: [image-parser/header design](../research/IMAGE_HEADER_DESIGN.md),
[commands/results](../research/sessions/20261018-RA-003-image-header-design.md).
Four public parser blobs (**16,708 bytes**) verified at the existing immutable pin;
published MIT notice reviewed and preserved with private source copies.
Separate bounded AXFS/ext-family/legacy-FAT/LZPT header predicates qualified
with **251/251 synthetic passes** (49 new plus 202 retained),
zero skipped, exit **0**, **1.271s**. All 23 baseline files unchanged.
The new API remains standalone and unintegrated. **No actual firmware, member
prefix or operational-constants read**; prior five unknown observations unchanged.
No filesystem, English, native FTP, body-match, recovery or device-write gate.
Next single work package: **RA-003: implement and qualify an all-prefix reconciliation gate, then run one frozen expanded-header comparison on the same five members with full prior lineage**.

Earlier continuation: [selected-member prefix study](../research/MEMBER_PREFIX_AUDIT.md),
[commands/results](../research/sessions/20261018-RA-003-member-prefix.md).
One selected-member prefix experiment completed, script and host exit **0**, **32.470943s**.
Synthetic qualification **202/202 passed**, zero skipped, exit **0**, **1.317s**.
**Five regular image-category candidates**, **4,096 bytes each / 20,480 bytes total**;
all five returned **unknown / unsupported_opaque** under the fixed classifier.
Complete fresh source/stream/header/span/original-prefix lineage and exact whole
directory equality passed before selected classification. No complete member
was covered by these prefixes; raw buffers discarded, no child files or links followed.
Classifier coverage is limited; this does not establish missing formats, English
resources or FTP code. No decompression/disassembly, camera or feature/write gate.
Historical next single work package: **RA-003: audit pinned image-format parser sources and reuse rights, then design and synthetically qualify bounded structural header predicates for the five opaque candidates before another actual read**.

Earlier continuation: [opaque-link metadata inventory](../research/TAR_LINK_INVENTORY.md),
[commands/results](../research/sessions/20261018-RA-003-tar-link-inventory.md).
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
Historical next single work package: **RA-003: review the private directory to select minimal English/FTP-relevant members, then document, qualify and run bounded in-memory prefix identification with full lineage and no child files**.

Earlier continuation: [bounded path/link diagnostic](../research/TAR_PATH_DIAGNOSTIC.md),
[commands/results](../research/sessions/20261018-RA-003-tar-path-diagnostic.md).
One bounded first-refusal diagnostic completed, script and host exit **0**, **28.299963s**.
Synthetic qualification **171/171 passed**, zero skipped, exit **0**, **0.916s**.
The first refused field is **link_target**, origin **header**,
predicate **empty_or_parent_component**. Combined categories retain their stated ambiguity.
Complete parent/logical-stream identities, header, declared spans and both prior
prefixes agree. Semantic tar parsing stopped permanently at the unchanged guard;
no directory accepted or tar-end/tail validation. One private bounded event,
no path text/raw bytes in it. No retry/fallback, child files, decompression,
disassembly, camera contact or feature/write gate. Earlier failed evidence is preserved.
Historical next single work package: **RA-003: review the observed path/link predicate, qualify an explicit metadata-only policy and run one bounded directory inventory with complete lineage and no child files**.

Earlier continuation: [tar-directory refusal](../research/TAR_DIRECTORY_AUDIT.md),
[commands/results](../research/sessions/20261018-RA-003-tar-directory.md).
One newly scoped tar-directory experiment stopped at the fixed **unsafe_path**
guard, **needs_review**, script exit **2**, host-tool exit **1**, **28.603684s**.
Combined synthetic qualification **133/133 passed**, zero skipped, exit **0**,
**0.749s**. Preliminary complete-parent hash passed; actual-pass final hashes,
fresh lineage acceptance and tar end/tail checks did not complete. No directory
accepted. Tentative header counter 114 is not a member inventory; post-discard
member count 0 does not mean an empty archive. Both observers cleared.
The offending member-name/link-target category is unknown. No retry, parser
fallback, threshold relaxation, child files, decompression/disassembly, camera
contact or feature/write gate. Prior measured observations remain unchanged.
Historical next single package: **RA-003: qualify and run one bounded tar path/link diagnostic that records the first refusal category privately, completes source/stream lineage validation, and accepts no directory or child files**.

Earlier continuation: [component-prefix identification](../research/COMPONENT_PREFIX_AUDIT.md),
[commands/results](../research/sessions/20261018-RA-003-component-prefix.md): 93/93 synthetic passes and one real
pipeline passed, exit 0. Exactly 4,096 bytes per selected extent; U-slot SquashFS
v4 and firmware ustar header candidates. No raw prefix files or child inventory.
Historical next single package: **RA-003: document and qualify a bounded-memory, metadata-only tar-directory inventory of the candidate ustar firmware extent, then run it with full source/stream lineage checks and no child files**.

Earlier continuation: [stream validation](../research/FDAT_STREAM_VALIDATION.md) and
[commands/results](../research/sessions/20261018-RA-003-stream-validation.md): 45/45 synthetic passes; one real pipeline
passed all 1,000,017 blocks, measured 1,020,017,152 logical bytes and checked
declared bounds/non-overlap. No component files, format/body/feature verification.
Historical next single package: **RA-003: document the necessary private selected-component scope, then synthetically qualify and run bounded in-memory identification of the declared U-slot and firmware extent prefixes, retaining lineage metadata only**.

Earlier continuation: [bounded header trial](../research/FDAT_HEADER_TRIAL.md)
passed first-block/header predicates only. That session did not measure the stream.

Earlier continuation: [crypto/public-constant provenance](../research/FDAT_CRYPTO_PROVENANCE.md)
records eight isolated AES passes and pinned private public-source/artifact inputs,
with no real firmware read or key/profile acceptance.

Earlier continuation: [bounded decoding basis/design](../research/FDAT_DECODING_PLAN.md)
and [commands/results](../research/sessions/20261018-RA-003-decoding-design.md). A pure standard-library header
validator passed synthetic CRC/extent cases; the real opaque payload was not read
or decoded in this continuation. Narrow statutory rationale is documented, with
contract interaction and actual decoding implementation/provenance still open.

Earlier continuation: [bounded FDAT identification/extractor audit](../research/FDAT_EXTRACTOR_AUDIT.md)
and [commands/results](../research/sessions/20261018-RA-003-fdat-identification.md).
The classifier interpreted 4,096 prefix bytes in memory and returned unknown /
unsupported_opaque; no prefix contents were output or saved. A source-only
extractor candidate is pinned, with no adoption/execution or exact-package support
claim. Decryption, component copying and full semantics remain unestablished.

Earlier continuation: [scoped UFU directory/parser audit](../research/UFU_CONTAINER_AUDIT.md)
and [commands/results](../research/sessions/20261018-RA-003-ufu-inventory.md).
Five chunk spans cover the file under the reviewed framing; one nonempty FDAT
is bounded. No chunk payload contents were interpreted or output. Full format
semantics and component formats remain unverified. The narrow statutory
assessment for local structural reading does not clear all later extraction.

Earlier continuation: [package acquisition, bounded identification and statutory route](../research/sessions/20261018-RA-003-package-law.md).
The separately approved destination GET succeeded; size and two acquisition
hashes agree. Existing authored probe reports a UFU signature candidate only.
Copyright Law Article 50(5) is an express research exception; full proposed
analysis acts and accepted terms still require assessment.

Earlier China-scope snapshot: [China scope, limited acquisition consent and results](../research/sessions/20261018-RA-003-cn-scope.md).
Country/purpose facts, download acceptance and proprietary-analysis rights are
separate records; consult STATE for acquired bytes/hash and current blockers.

Earlier source/terms snapshot: [Sony China source and inspection-rights review](../research/MAINLAND_FIRMWARE_SOURCE.md)
identifies the mainland 2.00 offer and published asset reference. No agreement
was accepted or firmware requested. Resolve a documented basis for proprietary
unpacking/static disassembly before that analysis; ordinary public-document
reads and hashing are distinct activities. The unsent inquiry is prepared.

## Available host commands

All three tools use only the standard library and explicitly supplied ordinary local
files. Paths and content prefixes are omitted from their JSON. Model, firmware,
kind and aliases remain user-supplied labels, not authenticated observations.
Write output only to a new private file; never redirect over any input.

```text
python tools/offline_inventory.py --help
python tools/artifact_probe.py --help
python tools/ufu_inventory.py --help
python -m unittest discover -s tests -p test_artifact_probe.py -v
python -m unittest tests.test_ufu_inventory -v
```

After a legitimate input has been supplied, the probe accepts
`--kind official-package --artifact package=ACTUAL_PRIVATE_PATH`. Substitute a real
existing path; the placeholder is not an acquisition command. It hashes the entire
file and inspects at most 4096 bytes from that same validated read. It reports
bounded ELF/PE header candidates, ZIP/gzip/Sony-UFU/decoded-FDAT signature candidates, malformed
headers, a PE header outside the probe, or opaque unsupported data. File extensions
do not select a parser. An opaque input is not automatically encrypted.

The probe does not unpack archives, recursively traverse input directories, follow
embedded offsets beyond the prefix, invoke a loader or extract a Sony component.
It does not verify archive checksums, signing chains, encryption, compression,
incremental-update dependencies or omitted per-body state. Numeric machine codes
describe header bytes; they do not establish the target's ABI or storage layout.
The [inventory portability note](INVENTORY_PORTABILITY.md) records filesystem limits.

The [UFU directory reader](../research/UFU_CONTAINER_AUDIT.md) additionally requires
`--input ACTUAL_PRIVATE_PATH --expect-sha256 EXPECTED_SHA256 --expect-bytes EXPECTED_BYTES`.
These placeholders are explanatory; use the recorded acquisition identity.
By default it streams the whole file for hash verification and interprets framing only,
with 2 GiB / 4,096 chunk / 1 MiB read limits. Optional `--probe-fdat` retains
at most 4,096 bytes of one FDAT prefix in memory and classifies after the full
framing/hash pass; duplicate FDAT is refused in this mode. No raw contents output.

Header references: [ELF gABI](https://gabi.xinuos.com/elf/02-eheader.html) and
[Microsoft PE/COFF](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format).
These standard-format field positions are not alpha6700 target offsets. The first
legacy ELF reference URL timed out; the maintained gABI page was read instead.

## Extractor review, before choosing one

The already pinned PMCA revision
`a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0` contains a small DAT offset locator:

| Source | Git blob | Static finding |
|---|---|---|
| `pmca/firmware/__init__.py` | `a136d25c68e8cae340405e5237163038b7467745` | Checks an eight-byte UFU identifier, scans big-endian size/type chunks and returns an FDAT span; it does not extract/decrypt/validate a complete updater |
| `pmca/util/__init__.py` | `b2ee7d939661150ebb4c0c15f2b8a6eb0d96847e` | Struct helper returns None for short input; callers must handle that failure |

This is **static-inference** from Git object text, never an upstream import or test.
The locator does not establish chunk bounds against total input length, a valid
declared FDAT extent, checksums/signatures, nested formats, encryption, model/build
identity, or alpha6700 applicability. A truncated top header can reach an attribute
access on None. No extractor is adopted, installed or executed. MIT provenance is
recorded in [RA-002](../research/REFERENCE_AUDIT.md); no implementation was copied.
Only the public file-format identifier is recognized by the independently authored
probe. A matching identifier would still be insufficient to select this locator.

## Private lineage required for each real input

Use a new private record for each acquisition. Retain original bytes, source URL or
owner-supplied origin, acquisition time, declared model/build, observed installed
firmware evidence separately, complete size/SHA-256, acquisition category, rights
basis, tool/source revisions and the immutable original's local location. Avoid
authentication-bearing URLs in shareable summaries.

Every extracted child must additionally record parent hash, extractor revision,
parameters, source span/address type where meaningful, output length/hash, validation
results and unsupported fields. Never merge official-package provenance with an
exact-body read or call a package a per-body backup. Preserve failed attempts.

Before extraction, add synthetic cases for every accepted container: truncated
headers/chunks, oversized/overlapping extents, duplicate/absent components, bad
checksums, unsafe archive names and resource limits. An executable updater must
remain data. No firmware upgrade is needed to inspect a matching package.

## Remaining acceptance

RA-003 remains incomplete. Official source identity, bounded directory framing,
complete experimental stream measurement and measured-size declared extent checks
are recorded. No component contents have been retained or their formats validated.
Selected-component necessity/terms/lineage, independent exact-build evidence and
body applicability remain open. Earlier negative/stopped trials stay preserved.
Historical next single package: **RA-003: document and qualify a bounded-memory, metadata-only tar-directory inventory of the candidate ustar firmware extent, then run it with full source/stream lineage checks and no child files**.
Host tests and format consistency do not establish authentication, English/FTP,
recovery or a device-write gate. Camera commands: **none**.
