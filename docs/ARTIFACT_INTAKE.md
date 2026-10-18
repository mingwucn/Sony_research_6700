# RA-003 artifact intake and bounded inspection

Status: host tooling available; exact-target acquisition and extraction **BLOCKED**.
Current intake (2026-10-18, **source-report**): the owner reports α6700
firmware **2.00**, current **简体中文**, **Chinese mainland version**, and
**English unavailable**. The full list is not supplied; exact SKU and binary
identity remain unverified. This is an owner report, not a target resource or
restriction-field finding. See [latest intake](../research/sessions/20261018-owner-mainland-english.md).
No official target package, body program, resource, settings or calibration object
has been supplied. Earlier private-directory checks were not a whole-computer
search. See [owner intake](../research/sessions/20261018-owner-ui-intake.md).
Owner additionally requires verified rollback/recovery before any firmware write;
offline package inspection does not establish that recovery system.

The [version 2.00 provenance/rights review](../research/OFFICIAL_PACKAGE_INTAKE.md)
now identifies official package metadata, but one asset GET stopped at an
unreviewed redirect with zero firmware bytes and no file. Owner inspection
permission is **No / unknown**; proprietary firmware analysis remains blocked.
Sony separately lists 34 open-source packages. The owner approved two BusyBox
source downloads under its notice; their licences, supplied FTP-enabled configs
and client source were reviewed privately as data. No downloaded source was
executed. Neither route establishes exact-body correspondence or recovery.

## Available host commands

Both tools use only the standard library and explicitly supplied ordinary local
files. Paths and content prefixes are omitted from their JSON. Model, firmware,
kind and aliases remain user-supplied labels, not authenticated observations.
Write output only to a new private file; never redirect over any input.

```text
python tools/offline_inventory.py --help
python tools/artifact_probe.py --help
python -m unittest discover -s tests -p test_artifact_probe.py -v
```

After a legitimate input has been supplied, the probe accepts
`--kind official-package --artifact package=ACTUAL_PRIVATE_PATH`. Substitute a real
existing path; the placeholder is not an acquisition command. It hashes the entire
file and inspects at most 4096 bytes from that same validated read. It reports
bounded ELF/PE header candidates, ZIP/gzip/Sony-UFU signature candidates, malformed
headers, a PE header outside the probe, or opaque unsupported data. File extensions
do not select a parser. An opaque input is not automatically encrypted.

The probe does not unpack archives, recursively traverse input directories, follow
embedded offsets beyond the prefix, invoke a loader or extract a Sony component.
It does not verify archive checksums, signing chains, encryption, compression,
incremental-update dependencies or omitted per-body state. Numeric machine codes
describe header bytes; they do not establish the target's ABI or storage layout.
The [inventory portability note](INVENTORY_PORTABILITY.md) records filesystem limits.

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

RA-003 remains incomplete: suitable firmware inspection rights, independent
exact-build evidence, matching official input bytes and a reviewed applicable
extractor are absent. The reported
2.00 version label is recorded above. Consequently
there is no target component inventory or private extraction manifest to validate.
A private acquisition-failure journal now records the zero-byte stopped attempt;
it is not an unsupported-format diagnosis of an unseen package. The synthetic
probe's passing tests establish only the documented local behavior. Camera
commands: **none**.
