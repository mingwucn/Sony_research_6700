# RA-003 artifact intake and bounded inspection

Status: official mainland 2.00 package acquired; bounded identification and
authored UFU directory inventory and bounded opaque FDAT identification recorded,
without component extraction or decoding.
Exact-body correspondence and the full extraction/analysis scope remain unresolved.
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

Latest continuation: [crypto/public-constant provenance](../research/FDAT_CRYPTO_PROVENANCE.md)
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

RA-003 remains incomplete. Official input size/hash and bounded directory metadata
are recorded; no component contents have been extracted. Full proposed analysis
scope, component-format/extractor suitability, independent exact-build evidence
and body applicability remain open. Earlier stopped-download journals are retained
as history. The bounded prefix remains opaque; the later narrow research rationale
and synthetic validator do not decode it. Next: **RA-003: implement, synthetically qualify and run one bounded private FDAT header trial for the predeclared CXD90057_k8 hypothesis**. Synthetic tests and framing coverage establish only
their documented host behaviour. Camera commands: **none**.
