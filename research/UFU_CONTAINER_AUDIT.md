# RA-003: bounded UFU directory and act assessment

Reviewed 2026-10-18. English and native camera-to-server Wi-Fi FTP remain
primary. This is an R0 host-file inspection, with no camera command.

## Activity-specific basis

The owner reports China and personal/noncommercial research. Legitimate input
provenance and separate download consents are recorded in the
[source dossier](MAINLAND_FIRMWARE_SOURCE.md). The original **No / unknown**
answer about existing Sony inspection permission remains historical evidence.

| Act | Assessment and boundary |
|---|---|
| A: local structural directory | Proceed within the existing ordinary-local-read authorization. Read and hash the acquired file; retain only chunk types, sizes and zero-based **package file offsets**. No component contents are written or output. This studies underlying design and is narrower than extraction. |
| B: private extraction/decompression | Assess the selected components, additional copies, private retention, exact operations and any applicable component terms before use. Compression alone does not establish a protective measure. A does not authorize every possible B operation. |
| C: static disassembly | Assess the actual program and research purpose separately; no firmware execution or device modification follows. No disassembly is performed in this package. |
| D: publication/reuse | Publish authored explanations and sanitized factual metadata. Do not publish extracted programs/resources, disassembly listings or generated patches under a presumed research grant. Apply each reused component's rights. |

**Static-inference:** [Software Protection Regulations Article 17](https://xzfg.moj.gov.cn/front/law/detail?LawID=581)
provides a documented basis for A's narrow study of software design/principles.
Article 6 distinguishes underlying methods from protected expression. This is
an activity-specific assessment, not a ruling about every later analysis act.
[Copyright Law Article 24](https://www.ncac.gov.cn/xxfb/flfg/flfg_532/202103/t20210309_50530.html)
also addresses personal study/research subject to attribution, normal-use and
legitimate-interest conditions. Article 50(5) becomes relevant if a later act
actually avoids a technical measure; ordinary directory reading requires no
such avoidance. No interoperability-only restriction is invented.

The [accepted Sony agreement](https://service.sony.com.cn/download/firm/00003046.html)
has broad decomposition/reverse-engineering wording in section 3 and anticipates
accompanying EULAs in section 4. Their enforceability and interaction with the
statutory route are not adjudicated here. A's narrow factual inspection proceeds
on the documented assessment; separate Sony permission is not made the only
possible basis. Full proprietary extraction/disassembly and redistribution are
not declared cleared. No protection bypass is proposed or performed.

## Pinned parser audit

Existing local Git objects were read with lazy fetch disabled and Git protocols
denied. No reference module was imported or executed.

Pin: `ma1co/Sony-PMCA-RE` commit
`a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0`.

| Source | Git blob | Finding |
|---|---|---|
| `pmca/firmware/__init__.py` | `a136d25c68e8cae340405e5237163038b7467745` | Eight-byte UFU magic, then unsigned big-endian 32-bit payload length and four type bytes; returns the first FDAT payload offset/declared size |
| `pmca/util/__init__.py` | `b2ee7d939661150ebb4c0c15f2b8a6eb0d96847e` | Short struct input returns None; the locator's outer-header access does not handle that result |
| `LICENSE.txt` | `77b0378407be242b5537f8dca3ed6402c91ba676` | MIT, copyright 2015 ma1co; grants no rights in Sony firmware |

The locator does not check declared spans against EOF, duplicate/empty FDAT,
all subsequent chunks, trailing bytes or a work limit. It is unsuitable as a
trusted extractor. No reviewed code establishes CRC, signing, terminal-chunk,
padding or ordering semantics; absence of those checks is not evidence that
the actual format lacks them. No implementation was copied or dependency
adopted. The authored reader uses the observed framing facts only.

## Authored reader

[`tools/ufu_inventory.py`](../tools/ufu_inventory.py) accepts one ordinary local
file, an expected whole-file SHA-256 and expected byte count. It streams the
entire file for hashing while interpreting only eight-byte framing fields.
Payload buffers are hashed and discarded. Reads are at most 1 MiB, input is
limited to 2 GiB and metadata to 4,096 chunks. Zero-length payloads still advance
past an eight-byte header. These are host resource limits, not target support
entries or undocumented format rules.

It rejects wrong magic/hash/size, truncated fields/payloads, out-of-file extents,
uninterpretable trailing bytes and count-limit violations. It reports absent,
empty or duplicate FDAT explicitly rather than selecting one. A successful
scan means only that this framing interpretation covers the file. Checksums,
signatures, chunk semantics, model/build identity and full container validity
remain unverified. File metadata checks detect observable changes; the trusted
workspace assumption and filesystem limitations in
[inventory portability](../docs/INVENTORY_PORTABILITY.md) still apply.

Output omits the input path, raw payloads and raw headers. Four-byte type labels
are factual directory metadata. All numeric positions have address type
`package_file_offset`; no runtime/flash addresses are inferred. No extraction,
decompression, decryption, loaders, reference imports, network or device adapter
exists in the reader.

## Actual package directory

After synthetic tests and code review, the real inventory exited **0** in
**1.617467 seconds**. Its whole-file SHA-256 matches acquisition:
`d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c`.
The original size, modification time and Windows read-only attribute were
unchanged. The private manifest retains exact argv, directory and tool hash.

| Chunk label | Header file offset | Payload file offset | Payload bytes | Exclusive end file offset |
|---|---:|---:|---:|---:|
| DATV | 8 | 16 | 4 | 20 |
| PROV | 20 | 28 | 4 | 32 |
| UDID | 32 | 40 | 108 | 148 |
| FDAT | 148 | 156 | 1,024,017,680 | 1,024,017,836 |
| DEND | 1,024,017,836 | 1,024,017,844 | 4 | 1,024,017,848 |

These are observed package FILE offsets and labels, not target addresses or
decoded field meanings. In particular, UDID is not interpreted as an observed
body identity, and DEND is not treated as a validated checksum/end marker.
Five bounded spans cover the input under this framing interpretation, with one
nonempty FDAT. No chunk payload contents were interpreted or output. This is
**offline-tested metadata evidence**, not a component inventory or full format
validation. [Exact commands/results](sessions/20261018-RA-003-ufu-inventory.md).

Next single package: **RA-003 bounded FDAT format identification and applicable
extractor audit**, before any component copying or decompression. No native
English/FTP, recovery or device-write claim follows.
