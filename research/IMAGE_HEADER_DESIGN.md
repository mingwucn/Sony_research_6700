# RA-003: image-parser coverage and bounded header design

2026-10-18 UTC / 2026-10-19 Europe/Paris. Host R0, topic branch
`codex/ra003-image-header-design`, parent
`b030355a47e7fc42b4e2688a30e9bddd02de9bd9`.
Native English and native camera-to-server Wi-Fi FTP remain first.
Camera commands: **none**. This package reads source and metadata and tests
authored synthetic bytes; **no actual firmware or member-prefix read**.

## Evidence and reuse

The [previous five prefixes](MEMBER_PREFIX_AUDIT.md) remain **unknown /
unsupported_opaque** under their frozen classifier. Its finite coverage omitted
four parser categories present in the already pinned reference tree. That is a
reason to study additional predicates; neither names nor missing classifier
coverage identifies the actual images or an English/FTP implementation.

Reference: `DavidBuchanan314/fwtool.py`, commit
`3955d7890fc38daf942bb52827599bfe35de4a14`, complete tree
`63801fd484c6e089f2363095b1c90968c6ee9c0d`. The earlier local subset did not
include these four blobs. Four separately scoped public-source GETs returned
HTTP **200**, **16,708 bytes total**, with exact tree-record sizes and Git blob
identities. Each source was UTF-8 decoded and syntax parsed only. No redirects,
retries, dependency installation, import, launcher, decoder or writer execution.
The browser reader's four GitHub-page fetches failed; direct immutable raw-source
acquisition independently succeeded. The private receipt preserves per-file
SHA-256, exact URLs and journal; [source lock](../references/sources.lock.json)
records the public-source identities.

| Pinned source | Git blob | Bounded evidence | Important limitation |
|---|---|---|---|
| [AXFS](https://github.com/DavidBuchanan314/fwtool.py/blob/3955d7890fc38daf942bb52827599bfe35de4a14/fwtool/archive/axfs.py) | `8b1d3b35f7f977ca7868f7fc076b0a66e1d10dc2` | Big-endian 253-byte header, magic, signature, block/image/mmap sizes | No region descriptors, tables, digest, inode or payload verification |
| [ext2](https://github.com/DavidBuchanan314/fwtool.py/blob/3955d7890fc38daf942bb52827599bfe35de4a14/fwtool/archive/ext2.py) | `de2180a837cf1929af3fb1c7a2dab775016944b3` | Little-endian 2,048-byte structure; magic and block/group geometry | Shared ext-family evidence; no ext2/3/4 distinction or feature compatibility |
| [legacy FAT](https://github.com/DavidBuchanan314/fwtool.py/blob/3955d7890fc38daf942bb52827599bfe35de4a14/fwtool/archive/fat.py) | `4612f25ecc1a5c5bf4d24a41eae396ee76a34596` | 512-byte boot-header layout, legacy labels/signatures and geometry | Conservative FAT12/16 subset; no FAT32 parser, cluster chains or directory verification |
| [LZPT](https://github.com/DavidBuchanan314/fwtool.py/blob/3955d7890fc38daf942bb52827599bfe35de4a14/fwtool/archive/lzpt.py) | `9ce8db2ffa15e236c5ded6413a8bc5553decaf49` | Little-endian 16-byte header, magic and table span/entry width | No table read, exponent evaluation, decompression or decoded-size assertion |

The already pinned utility helper establishes packed standard widths and default
little endian; AXFS explicitly selects big endian. Source field positions are
**member-relative file positions**, never device, virtual or runtime addresses.

The published [root MIT notice](https://github.com/DavidBuchanan314/fwtool.py/blob/3955d7890fc38daf942bb52827599bfe35de4a14/LICENSE.txt)
names Copyright (c) 2015 ma1co and requires copyright and permission notice in
copies or substantial portions. The complete notice and disclaimer accompany
private source copies. No per-file licence override was found in the four files.
This package authors small predicates and fixtures from inspected field facts;
it does not adopt the upstream extractor or implicitly license this project.
LZPT comments name two kernel-header paths without a pinned version or licence;
those are provenance leads, not permission to copy a kernel implementation.
No proprietary firmware or device permission follows from MIT source availability.
Existing accepted-contract and independent-constants issues remain unresolved.

## Separate experimental classifier

Keep all **23** copied baseline source/test files byte-identical, retaining the
**202** earlier tests and all earlier observations. The original classifier and
acceptance helpers have closed format allowlists; replacing their callback with
new format labels would change or fail the qualified contract. The new module
therefore remains standalone and **unintegrated** in this source-only package.

Accept exact built-in `bytes` of at most **4,096 bytes**, and a positive exact
integer member extent at least as large as the prefix. Inspect only fixed header
positions present in this input. Return fixed metadata without raw bytes, names,
positions, hashes, text or numeric header values. Evaluate categories separately
and retain ambiguity if more than one candidate passes. Every result keeps
`container_validated=false` and `abi_verified=false`. `header_only` means only the
documented header predicates passed; other statuses record refused or unsupported
leads. No filesystem validity, authenticity,
mountability, executable ABI, feature support or exact-body match follows.

The independently authored predicates use these explicit conservative rules:

- AXFS: complete 253-byte header, exact magic and signature, positive block size,
  declared size between 253 and measured extent, and mmap size no larger than
  declared size. Region offsets, digest, file/block counts and other fields are
  unread; no universal block-size or alignment rule is asserted.
- ext family: complete 2,048-byte structure, magic at member-relative 1,080,
  little-endian block exponent at 1,048 at most six, nonzero block count and
  blocks/inodes-per-group. Derived byte size must cover 2,048 bytes and fit the
  measured extent. Revision, feature flags, inode size/count, groups and payload
  remain unverified; this is not an ext2-specific compatibility decision.
- Legacy FAT: complete 512-byte header, extended/end signatures, exact padded
  FAT12/FAT16 label and 512-byte sectors, as in the inspected writer. Require
  positive cluster/reserved/FAT-copy/root-entry/FAT-sector/32-bit-total-sector
  fields; derived image and fixed root area must fit the measured extent, and
  one cluster must fit the declared image size. The skipped 16-bit total-sector
  field, conflicting totals, cluster-count/type relationship, legal cluster
  ranges, chains and directories are **unvalidated**. A positive cluster value
  alone is not FAT validity. Other labels/sector sizes are unsupported variants
  within this probe; no general FAT absence follows.
- LZPT: complete 16-byte header, exact magic, nonempty table size divisible by
  its eight-byte entry width, and a table span starting at or after the header
  and wholly inside the measured extent. Header/table separation is an authored
  conservative rule. The block exponent is uninterpreted and never shifted or
  exponentiated; neither its range nor decoded size is validated. Table entries
  are not read, even when they happen to fall inside the supplied prefix.

Missing leading indicators return unknown. Recognized truncated or inconsistent
headers return malformed; unsupported legacy-FAT variants are distinguished.
These are observations about fixed predicates, not complete format diagnoses.

Qualify valid, malformed, truncated, wrong-endian, misleading-signature, measured
extent and ambiguous synthetic cases. No upstream source is imported by tests.
Preserve qualification failures and explain any pre-qualification design changes;
do not silently replace the five historical unknown outcomes.

## Later actual-comparison prerequisites

Any later actual comparison requires a separately reviewed and frozen runner,
source hashes, synthetic integration qualification and journal before I/O. Keep
the same five exact prior regular members and **4,096 bytes each / 20,480 total**.
Retain the existing maximum of eight members / 32,768 raw bytes; no additional
selection or larger prefix is justified by this design alone.

Before any expanded predicate is called, reconcile **all five** prior prefix
hashes, exact selection metadata, original classifications, full fresh parent/
stream/header/span/original-component lineage and exact whole private directory.
The old collector hashes and classifies each row immediately; substituting a
callback does not prove this stronger all-prefix preflight. Use a separate
reviewed coordinator and fail closed before new classification on a mismatch.
Keep prior outcomes separate from additive candidate observations. No scanning,
offset following, child files, link following, decompression, disassembly or
upstream/firmware execution. Failure enters `needs_review`; no automatic retry
or parser/key fallback. This design does not authorize device contact or writes.

Status at design creation: source acquisition and rights/coverage audit complete;
implementation, independent review and synthetic qualification pending.


## Qualification result

Four public parser blobs (**16,708 bytes**) verified at the existing immutable pin;
published MIT notice reviewed and preserved with private source copies.
Separate bounded AXFS/ext-family/legacy-FAT/LZPT header predicates qualified
with **251/251 synthetic passes** (49 new plus 202 retained),
zero skipped, exit **0**, **1.271s**. All 23 baseline files unchanged.
The new API remains standalone and unintegrated. **No actual firmware, member
prefix or operational-constants read**; prior five unknown observations unchanged.
No filesystem, English, native FTP, body-match, recovery or device-write gate.

See [exact commands/results](sessions/20261018-RA-003-image-header-design.md).
Next single package: **RA-003: implement and qualify an all-prefix reconciliation gate, then run one frozen expanded-header comparison on the same five members with full prior lineage**.
