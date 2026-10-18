# RA-003: bounded identification of declared component prefixes

## Before-read scope

Recorded before this experiment on 2026-10-18, topic branch
`codex/ra003-component-prefix`, parent
`e1f3c41827b58c1f13c5e136d2ea337d15ed8886`. English and native Wi-Fi FTP are
primary. Camera commands: **none**.

The [previous measured stream](FDAT_STREAM_VALIDATION.md) establishes logical
length/SHA and declared span bounds, but does not identify formats needed to
choose language-resource or FTP-binary parsers. The necessary next observation
is a bounded prefix at each nonempty declared component start. The empty P slot
is excluded. No component is presumed to contain English resources or FTP.

Predeclared logical decoded-FDAT file spans, not runtime/storage addresses:

| Label | Declared start | Declared bytes | Prefix limit |
|---|---:|---:|---:|
| U slot 0 | 512 | 1,253,376 | 4,096 |
| Firmware extent | 1,253,888 | 1,018,763,264 | 4,096 |

At most 4,096 logical bytes are retained per selected extent, clipped to its
declared length. Transient in-memory copies are necessary; no raw-prefix,
decoded-stream or component files/output are permitted. Preserve metadata only:
parent and measured-stream hashes, labelled spans, inspected lengths/prefix hashes,
implementation/probe identity and candidate classification. A prefix hash is not
a whole-component hash. No secure memory erasure is claimed.

The existing [act-specific format-study rationale](FDAT_DECODING_PLAN.md) applies
to this necessary private observation; accepted-contract interaction and independent
constants derivation remain unresolved. This is not a new agreement, general
permission request or clearance for component copying, decompression, disassembly,
distribution, modification or device work.

Copy the previously qualified authored stream reader and add only an optional
validated-payload observer. Keep the exact same single experimental hypothesis;
no key/parser fallback or automatic retry. Qualify changes and collector/classifier
synthetically and independently review the actual runner before source I/O.
Journal first; use one fresh ordinary single-link non-reparse read-only descriptor.
Preliminary full-parent hash/framing captures the IV; rewind that descriptor for
the full decoding pass, including another complete parent hash. Recheck encountered
IV, all envelope sums/capacities/terminal positions, measured length/SHA, source
observations, header SHA and freshly validated declarations against prior lineage.

The observer receives logical offset before advancement and exact validated
payload. Enforce contiguous logical callbacks, including zero/odd payloads;
collect exact intersections across physical-block/crypto-batch boundaries.
Require both expected prefixes complete. Observer failure ends the pipeline.
Filled prefixes remain tentative until every source/stream/header/extent/lineage
check passes. No classifier invocation or accepted prefix result on a later failure.

Managed I/O/crypto/observer buffer design budget: **5 MiB**, including **8,192**
retained prefix bytes and the 512-byte header; source requests at most 1 MiB,
crypto batches at most 64 KiB. This does not cap/measure interpreter/native heap
or create an OS sandbox. No upstream launcher/tool/module or firmware code runs.

Use a fixed reviewed allowlist: existing authored ELF/PE, ZIP, gzip, UFU and
decoded-FDAT prefix predicates, plus conservative cramfs, SquashFS v4, newc/crc
CPIO and ustar header predicates. No offset following, member walk, magic scan,
decompression or target mapping. Validate bounded numeric/header consistency
where defined; a match remains a candidate. Unknown stays unknown. Invalid or
unsupported forms do not establish feature absence. No raw bytes, filenames or
arbitrary strings may enter exceptions, stdout, journals or persisted results.

Status at scope recording: implementation, synthetic qualification and actual
prefix experiment pending. Preserve these original scope bytes privately before
the real run; append observations separately afterward. No body/profile,
authentication, recovery, feature or device-write gate follows from this package.

## Fixed classifier subset and sources

These public format descriptions are source reports, not observations about this
package. The actual classifier is authored privately and pinned by hash.

| Additional candidate | Bounded predicates | Unchecked |
|---|---|---|
| Little-endian cramfs | 76-byte superblock; magic/signature; declared size within extent | Flags, root inode, fsid CRC, contents |
| Little-endian SquashFS 4.0 | 96-byte superblock; block size/log 4 KiB–1 MiB; compressor code 1–6; bounded bytes-used | Tables, inodes, compressor/payload validity |
| Newc/crc CPIO | 110-byte header; thirteen hex fields; positive name length; aligned first-data bounds; newc check field zero | Names, payload/checksum, members, end marker |
| Ustar | 512-byte header; reviewed magic variants; unsigned checksum; ASCII-octal size/checksum; first padded member bounds | Names, member traversal/extensions, archive end |

References: [Linux v6.12 cramfs definitions](https://github.com/torvalds/linux/blob/v6.12/include/uapi/linux/cramfs_fs.h),
[Linux v6.12 SquashFS definitions](https://github.com/torvalds/linux/blob/v6.12/fs/squashfs/squashfs_fs.h),
[official SquashFS documentation](https://docs.kernel.org/filesystems/squashfs.html),
[official CPIO/initramfs format](https://docs.kernel.org/driver-api/early-userspace/buffer-format.html),
[CPython v3.13.12 tar implementation](https://raw.githubusercontent.com/python/cpython/v3.13.12/Lib/tarfile.py).
No upstream source implementation is imported/executed. Public format predicates
do not establish an applicable extractor. Other versions, endian forms, GNU
base-256 or signed-checksum tar forms are outside this conservative subset.


## Observed result

**Offline-tested:** one pipeline, two predeclared source-hashed passes, exit **0**,
**23.899888s**. All 1,000,017 physical blocks and parent/stream/header/span checks
passed again; measured logical length/SHA agree with the earlier stream result.
Exactly **8,192 prefix bytes** were observed, 4,096 per selected extent.

| Declared extent | Prefix candidate | Bounded status | Prefix SHA-256 |
|---|---|---|---|
| U slot 0 | SquashFS v4, little-endian | header_only | `dca812aa192ba01f9ae956b8b1b07fba575b7bec62749ae9265723856023f9b0` |
| Firmware | ustar | header_only | `515c8394b754f22ce3af56957f051ef7f75942a71adac61e234ddb56bb6ed9e2` |

These are prefix digests, **not whole-component hashes**. No mountable filesystem,
complete archive, member names/contents, English resources/restriction or FTP binary
is established. Classification occurred only after complete lineage revalidation.

Final combined synthetic suite: **93/93 passed**, zero skipped, exit **0**,
unittest **0.441s**. Includes 45 unchanged stream cases, seven observer cases,
24 collector/acceptance cases and 17 classifier cases. Collector tests include
variable/empty/odd lengths, exact intersections, retention/callback refusals,
changed evidence/spans, poisoned/sealed state, safe classifier metadata and a
late corrupt envelope after both prefixes filled with the classifier uncalled.

The 5 MiB buffer design budget does not cap/measure whole-process memory. No raw
prefix/stream/component file, decompression, disassembly, upstream/firmware
execution or camera contact occurred. Previous observations remain unchanged.
Contract/provenance limitations and all body/profile/feature/recovery gates remain.

Next single package: **RA-003: document and qualify a bounded-memory, metadata-only tar-directory inventory of the candidate ustar firmware extent, then run it with full source/stream lineage checks and no child files**.
The directory inventory must establish supported tar variants, framing/checksums,
bounded metadata and parent-child lineage before any child copy is selected.
No automatic decompression or fallback parser. See [session commands/results](sessions/20261018-RA-003-component-prefix.md).
