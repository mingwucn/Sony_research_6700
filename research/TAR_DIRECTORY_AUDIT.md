# RA-003: private metadata-only tar directory inventory

## Before-read scope

Recorded 2026-10-18 UTC (2026-10-19 Europe/Paris) on `codex/ra003-tar-directory`, parent
`1accd029cc900573199a320e924b64cb1a230af4`. English and native Wi-Fi FTP
remain first. Previous goal turn: progress. Camera commands: **none**.

The [bounded prefix experiment](COMPONENT_PREFIX_AUDIT.md) identified a ustar
header candidate in the declared firmware extent. A directory inventory is
necessary to select relevant children for later English-resource and FTP-binary
research. Names alone do not prove those features or a child format.

Use only the already acquired private package and single previously tested
experimental hypothesis. Copy the seven pinned authored foundation/test files
unchanged. No upstream launcher, extractor, firmware code or camera command.
No new download, installation, agreement or private upload.

The existing [necessary private format-study rationale](FDAT_DECODING_PLAN.md)
extends to bounded directory metadata and streaming identity hashes. Accepted
contract interaction and independent constants derivation remain unresolved.
This act retains transient header/extension bytes and private directory metadata,
without member payload copies. It supplies no clearance for later component
files, decompression, disassembly, distribution, modification or device work.

Selected extent: **decoded-FDAT file offset 1,253,888**, length
**1,018,763,264**, end exclusive **1,020,017,152**. These are declared decoded
file positions checked against the measured stream, never camera storage,
virtual or process addresses. Revalidate both previous 4,096-byte prefixes,
complete parent and logical-stream identities, fresh header and every declared
span before accepting any directory result.

## Fixed parser and resource policy

Authored streaming parser, sequential logical callbacks of at most 1,020 bytes.
Observe exact intersections with the selected extent. Hash its complete bytes
and regular member payloads without retaining payloads or following member
paths. Keep only safe private names/link text, type/size, explicitly labelled tar
relative and decoded-FDAT file spans, header/payload hashes and bounded counts.
Public summaries contain aggregate observations; detailed names remain private.

Predeclared limits: 512-byte header, 1,024-byte UTF-8 name/link, 64 KiB per
extension payload, 4,096 actual members, 8,192 physical headers and 2 MiB aggregate
compact UTF-8 directory JSON metadata. Existing lineage/journal fields are
separate small fixed-shape metadata; this encoded directory bound does not cap
Python object or JSON pretty-print overhead. Global PAX state is bounded. Refuse invalid types, booleans as
integers, noncontiguous/oversized callbacks, unsafe paths and canonical duplicate
members. Permit a conventional `./` directory entry as metadata only.

Supported subset: POSIX ustar and reviewed GNU magic; unsigned header checksum;
nonnegative ASCII-octal fields; regular files, directories, hard links and symbolic
links. Links are recorded, never resolved or materialized. GNU L/K long name/link
and POSIX x/g PAX records are bounded and validated. Only explicit path/linkpath/
size overrides and reviewed benign identity/time fields are allowed. Unknown
semantic keys, GNU sparse/base-256 numeric forms, devices/FIFO/contiguous and
unknown type flags are refused. No format fallback or automatic decompression.
Require at least one record in each x/g extension. Reject empty/deletion PAX values, duplicate keys, conflicting GNU/PAX overrides
and size overrides on nonregular members. Extension payload length always uses
its own raw header size, never a pending/global override. Interpret POSIX prefix
only for POSIX magic; GNU timestamp fields are not name prefixes. Require the
unsupported GNU sparse/offset tail to be zero. Record link metadata without
asserting resolution or target existence.

Check each header, effective-size padded bounds and zero member padding. Require
two consecutive 512-byte zero end blocks and all remaining extent bytes zero.
Dangling extensions, truncated headers/payloads, missing end blocks, nonzero tail,
overflow, unsafe/duplicate metadata and unsupported variants stop the pipeline.
These are fixed conservative acceptance policies, not universal Sony/tar rules.
Do not adjust them after observing failure without recording a new package.

Managed I/O/crypto/observer/metadata design budget: **8 MiB**, including the
unchanged nested stream reader's 5 MiB budget, 8,192 prefix bytes, extension
buffer and bounded directory metadata. This does not measure or cap total Python/
native memory, guarantee secure erasure or create an OS sandbox.

## Qualification and acceptance

Qualify parser, observer composition and lineage acceptance on synthetic archives
before any real source read. Tests must cover callbacks crossing boundaries,
zero/odd lengths, normal/extended names, framing/checksum/numeric failures,
unsafe/duplicate paths, links, extension/metadata/member/header caps, truncated
data/end/tail, poisoned/sealed state and late full-stream/lineage failure after
directory completion. No operational constants or firmware in synthetic fixtures.

Journal exclusively and fsync before actual source I/O. One pipeline, two
predeclared complete-parent hash passes on the same ordinary read-only single-link
non-reparse descriptor. Preliminary framing captures the IV; the decoding pass
rechecks IV, complete parent, all envelope/terminal checks, logical length/hash,
header and spans. No retry or key/parser fallback. Any error enters needs_review;
preserve its generic reason and existing journal, without raw input in exceptions.

Prefix and directory observers remain tentative. After full stream validation,
require exact previous parent/stream/header/span/prefix evidence, then finish the
tar observer. A failure discards buffered observations without a secure-erasure
claim. Directory framing and hashes cannot establish full child formats, signatures,
package authenticity, body applicability, resources/backend semantics, ABI,
recoverability, feature support or a device-write gate.

Status at scope creation: implementation, qualification and real inventory pending.
Preserve these scope bytes privately before source I/O; append actual observations
and exact source/test/runner identities separately.

## Primary format source review

Source-only review: [CPython v3.13.12 tarfile.py](https://raw.githubusercontent.com/python/cpython/v3.13.12/Lib/tarfile.py),
matching installed standard-library source, **114,407 bytes**, SHA-256
`e741d0f405b82bdb99f3c9f3604add700d47a1a5ec819b237c1f488259e1f005`;
[GNU basic tar format](https://www.gnu.org/software/tar/manual/html_node/Standard.html)
and [GNU tar manual](https://www.gnu.org/software/tar/manual/tar.pdf), official
indexed format text. No upstream implementation is imported or run by this
parser. The [current POSIX pax page](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/pax.html)
returned browser HTTP 403; its full text was not directly inspected. PAX record
framing and effective-size handling were checked in the pinned CPython source.
Source descriptions are distinct from observed package facts.


## Observed refusal

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

The guard combines several member-name and link-target checks. This receipt does
not identify which predicate or field failed. A legitimate link can use syntax
that an extraction-oriented path guard rejects, but that cause was not observed
here. No accepted child names, hashes, complete extent digest or inventory are
retained. The earlier stream/prefix observations retain their original scope.

Do not rerun this implementation or relax its threshold. A new synthetic-first
diagnostic must retain one bounded fixed-shape field-role/category/length/hash
event before discard, stop semantic directory parsing, and complete source/stream
lineage before exposing that diagnostic. It accepts no directory.

Next single package: **RA-003: qualify and run one bounded tar path/link diagnostic that records the first refusal category privately, completes source/stream lineage validation, and accepts no directory or child files**.
See [exact session commands/results](sessions/20261018-RA-003-tar-directory.md).
