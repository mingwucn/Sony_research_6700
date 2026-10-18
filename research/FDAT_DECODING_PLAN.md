# RA-003: bounded FDAT decoding basis and validation design

Reviewed 2026-10-18. English and native Wi-Fi FTP remain primary. Camera
commands: **none**. The real package remains opaque and is not decoded here.

## Act-specific research basis

The recorded facts are lawful official-package acquisition, inspection in China,
and personal/noncommercial research. The earlier owner answer **No / unknown**
concerns existing permission; it does not erase statutory exceptions.

**Source-report:** [Software Protection Regulations Article 17](https://www.cac.gov.cn/2013-02/08/c_12648744.htm)
addresses studying software's underlying design and principles without copyright
permission/payment. Article 6 distinguishes ideas from expression. Article 16's
backup provision is separate; experimental decoded copies are not body backups.
The MOJ mirror timed out in the root refresh; the official CAC text was read.

[Copyright Law Articles 24, 49–51 and 61](https://www.nsfc.gov.cn/p1/2871/2872/69475.html)
provide personal-study conditions, a specific software reverse-engineering/
encryption research exception for technical measures, restrictions on providing
bypass mechanisms to others, and separate contract liability. Rights-management
information requires preservation. No interoperability-only condition is stated.

**Static-inference:** these provisions supply a usable, documented statutory
rationale for narrowly necessary private in-memory header/block decoding for
format study. Separate Sony permission is not the only possible basis. This
assessment does not establish that every private component copy or later patch
is covered, or that the accepted contract is unenforceable.

The [accepted Sony agreement](https://service.sony.com.cn/download/firm/00003046.html)
§1 allows personal/noncommercial service use; §3 broadly prohibits reverse
engineering, decomposition and copying; §4 anticipates accompanying EULAs and
§7 other applicable terms. The unresolved contract interaction is recorded
separately from the statutory rationale. No new agreement was accepted.

| Proposed act | Current assessment and concrete boundary |
|---|---|
| Synthetic decoded-header validation | Authored standard-library code and synthetic bytes only; performed in this package |
| Bounded private in-memory decoding | Statutory research rationale documented; not operationally ready or performed. Pin/review exact implementation, public constants provenance and bounded trial before use. No device-derived keys, private uploads or publication of a working bypass mechanism. |
| Necessary private component copies | Assess selected component, question, exact bytes/copy count, retention and component terms. A complete component is not automatically prohibited merely because it is complete; unrelated copying is not assumed necessary. Preserve discovered notices/EULAs. Not performed here. |
| Distribution, modification or device work | Separate scope; no proprietary outputs, keys or bypass implementation enter Git. No firmware execution, camera access or write authorization follows. |

No missing country/purpose or ordinary-read approval is being requested again.
The current synthetic validator is not a decryption implementation.

## Fixed source and address vocabulary

Format facts below come from the text-only
[extractor audit](FDAT_EXTRACTOR_AUDIT.md), fork commit
`3955d7890fc38daf942bb52827599bfe35de4a14`, pinned in
[sources.lock.json](../references/sources.lock.json). No upstream code was run,
copied or integrated; no separate cryptographic constant/key file was acquired.

All positions in the following table are **decoded-FDAT file offsets**, never
UFU package offsets, runtime addresses or camera storage offsets. They are
format-description facts, not alpha6700 profile entries.

| Decoded offset | Bytes | Reviewed field |
|---|---:|---|
| 0 | 8 | UDTRFIRM identifier |
| 8 | 4 | Little-endian CRC32 of header bytes 12 through 512 exclusive |
| 12 | 4 | Header version marker 0100 |
| 16 / 20 | 1 each | Update mode / LUW flag; upstream reader accepts U / N |
| 32 / 33 | 1 each | Minor / major version codes; no body-version interpretation |
| 36 / 40 | 4 each | Little-endian model / region fields; no target mapping |
| 48 / 52 | 4 each | Little-endian firmware offset / size |
| 56 | 4 | Declared filesystem count; upstream reader ignores it |
| 64 | 448 | 28 slots of 16 bytes each |

A slot has mode at +0, little-endian offset at +4 and size at +8. Other slot
and header padding remains uninterpreted. The source writer emits two tagged
slots: one U and a zero-sized P at the same offset. It does not require U to be
nonempty. Therefore neither
count = nonempty count nor empty offset = zero is a valid universal assumption.
The source recognizer checks final four header bytes zero; its reader does not.

## Authored decoded-header validator

[`tools/fdat_header.py`](../tools/fdat_header.py) provides only
`validate_header(header, decoded_bytes)`. It accepts exactly 512 bytes and an
integer caller-supplied decoded-stream size, bounded to 2 GiB. It has no CLI,
file opening, cryptography, extraction, network or device API.

It checks identifier/version, U/N mode, the recognizer's final-zero condition,
header CRC, count no greater than 28 and all 28 slots. Its conservative accepted
subset requires exactly one nonempty U, permits tagged P slots and their empty
sentinels, and refuses unknown slot forms. Every nonempty firmware/slot extent
must lie beyond the header, within the claimed decoded size and be disjoint.
Touching spans are allowed. Empty extents may declare offset zero or a position
from 512 through EOF; they are not copied or counted as nonempty spans.

These are explicit host acceptance policies, not proof that all Sony images
must meet them. Nonzero uninterpreted padding is reported, not universally
rejected. Declared and observed slot counts remain separate with count semantics
unverified. Model/region/version fields are integer codes, never support values.
All output positions say `decoded_fdat_file_offset`.

Header CRC success means only those 500 header bytes agree with the stored CRC.
Payload integrity, signatures, full-container validity, identity, ABI and
compatibility remain unverified; output flags cannot open a device gate.
The function does not prove the caller's stream-size claim or that any component
bytes exist. A future real pipeline must supply measured decoded length, not a
ciphertext-derived estimate. Only synthetic inputs are used in this session.

## Decoder requirements before a real trial

The reviewed block envelope has a little-endian 16-bit sum and 16-bit declared
length/last flag before logical payload bytes. The sum covers all following
16-bit words, including metadata and padding. A decoder must reject a declared
length beyond block payload capacity and enforce physical length/alignment,
checksum, position and terminal-flag consistency. Neither sum nor CRC is
cryptographic authentication.

The candidate CBC source uses a 1,024-byte physical block, with a special first
512-byte cipher region and CBC continuation, plus a 272-byte tail containing an
IV. Because the four-byte envelope precedes the logical header, only its first
508 bytes lie in that special region; its last four require the next cipher
region. A first-512-byte-only shortcut is insufficient. The source does not
authenticate the remaining omitted trailer. Preserve that limitation explicitly.

Arithmetic on the already recorded FDAT length gives
`1,024,017,680 - 272 = 1,024 × 1,000,017`. This is compatible with one candidate
shape, **not** an encrypted identifier, algorithm/key selector or exact-package
support proof. No profile is selected from the arithmetic or a processor name.

The next trial design must pin the minimal crypto dependency and inspect the
provenance/applicable terms of any required public constants. Do not install the
upstream project, its launcher or packaging stack, or run automatic key trials.
No cryptographic key material or operational decryption-key constants belong in
public reports or source here. Ordinary format constants remain documented.

Start with an explicitly selected bounded header candidate, not child extraction.
A future journaled host read must verify original size/hash/file identity in the
same operation; retain only the minimal first block and tail needed by the
reviewed candidate, with an explicit memory cap and no raw output. Keep any
decoding code private if its publication would supply a bypass mechanism.
Require independent synthetic known-answer/malformed-input tests first. Record
unsupported/multiple candidates as unresolved; never choose a key from magic
alone. Do not call a candidate authenticated because a header CRC passes.

A header trial does not measure full decoded length or payload integrity. Before
passing real data to the extent validator or copying children, a bounded full
stream must measure actual output, check all blocks and terminal state, retain
the original parent hash and record a decoded-stream hash. Record each selected
child's parent/hash/span/length and rights scope without package-to-runtime
address guesses. Later decompression/archive handling needs separate resource
and path constraints. No real trial or copying is performed now.

## Remaining work

The opaque input and exact body/build correspondence are unresolved. There is no
English resource map, native FTP binary/invocation route, recovery proof or
feature result. FL2/FL3 remains deferred; calibrated looks later; the optional
bridge remains HOST-ASSISTED.

Next single work package: **RA-003: audit and pin the minimal crypto dependency
and public-constant provenance for a bounded private header-decoding trial**.
The narrow statutory rationale is now documented; avoid recycling the general
lack-of-Sony-permission question as the only blocker.


## Later crypto-provenance continuation (2026-10-18)

The [crypto/source audit](FDAT_CRYPTO_PROVENANCE.md) and
[session result](sessions/20261018-RA-003-crypto-provenance.md) supersede
the preceding next-step statement. The private AES wheel and public constants
source are pinned; eight authored primitive tests passed. No actual firmware
read/decoding or camera action occurred. Constants origin and accepted-contract
interaction remain unresolved, alongside exact-body correspondence/recovery.
One predeclared experimental hypothesis is not a target support profile.
Next single package: **RA-003: implement, synthetically qualify and run one bounded private FDAT header trial for the predeclared CXD90057_k8 hypothesis**. No feature/write gate passed.
