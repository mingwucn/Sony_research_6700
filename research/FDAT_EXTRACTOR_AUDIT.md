# RA-003: bounded FDAT identification and extractor candidate

Reviewed 2026-10-18. English and native camera-to-server Wi-Fi FTP remain primary.
This work reads an ordinary private host file; camera commands: **none**.

## Narrow inspection scope

The [preceding act assessment](UFU_CONTAINER_AUDIT.md#activity-specific-basis)
supports ordinary local structural study under the recorded China/personal-
research facts. This extension retains **at most 4,096 bytes in memory** from
the single bounded FDAT span during the same whole-file hash/framing pass.
It reports candidate labels/counts and package metadata, with no prefix bytes,
hex or strings in output, logs or files. It performs no transformation,
extraction, decompression, decryption, disassembly, firmware execution or bypass.

This run does interpret a bounded payload prefix. The earlier directory-only
run's statement that payload contents were not interpreted remains its historical
description. No new owner approval is needed for this ordinary local read within
the existing R0 research task. The narrow statutory assessment and unresolved
Sony contract interaction do not clear every later extraction/decryption act.

## Public candidate and pin

The pinned A7CR README names `ma1co/fwtool.py` as an extraction reference. The
inspected local PMCA subset provides only a UFU locator and a call to an external
`fwtool.sony.fdat` dependency. Some other PMCA Git blobs were unavailable with
lazy fetch disabled; this is not a complete-tree absence claim.

The [upstream project](https://github.com/ma1co/fwtool.py) and its open
[PR #52](https://github.com/ma1co/fwtool.py/pull/52) are distinct revisions:

| Reference | Immutable revision | Review status |
|---|---|---|
| Upstream master observed | `cdba742b73eed5981480c326aeb30033aabf0223` | Baseline reference; not adopted or executed |
| DavidBuchanan314 fork / PR #52 head | `3955d7890fc38daf942bb52827599bfe35de4a14` | Selected text-only audit candidate; open/unmerged when checked |

The PR author reports ILCE-6700 among tested models. No exact 2.00 version,
mainland variant or input hash is provided. This is **source-report**, not
independent reproduction or proof that this package is supported. Neither a
processor-family match nor another model's success establishes an ABI or body
access/recovery route. The candidate is pinned in
[`sources.lock.json`](../references/sources.lock.json), with no runtime adoption.

## Format facts and hazards

The reviewed [fixed-revision `fdat.py`](https://github.com/DavidBuchanan314/fwtool.py/blob/3955d7890fc38daf942bb52827599bfe35de4a14/fwtool/sony/fdat.py)
has Git blob `3236a4292b933c38766952ec31ef887a3b90eaad`, 9,791 bytes, SHA-256
`ea1feccdc115fa46cdb29061cfa6cd1bb7277bb454892c0c7f8e9f6257c6d628`.
It defines decoded FDAT magic **UDTRFIRM**, a 512-byte little-endian header,
version marker `0100`, a header CRC32 and filesystem-slot fields. Magic-only
recognition is a signature candidate; the CRC covers header bytes, not the
payload or a signing chain. The source defines no encrypted-FDAT magic.

**Static-inference from reviewed source:** direct use is unsuitable as a trusted
extractor. `readFdat` does not establish component EOF bounds, header/segment
non-overlap, uniqueness of the selected usermode slot or expected model/build.
Short headers can reach a None dereference. `FilePart.seek` computes a clamp
without applying it. Block decryption has incomplete declared-size and malformed-
input handling, and the later CBC path does not authenticate the full omitted
trailer. These limitations do not establish a safe decryption or write route.

The CLI creates output files and invokes decoding/extraction. It was not run.
Only source text and metadata were obtained; no firmware assets, device helpers,
key/constant files or runtime dependencies were acquired for this audit. MIT
licence provenance applies to the reviewed code and grants no Sony firmware
rights. No upstream implementation or key was integrated or implicitly relicensed.

## Authored probe

The optional `--probe-fdat` mode in
[`ufu_inventory.py`](../tools/ufu_inventory.py) retains one bounded prefix while
hashing, then calls the authored
[`artifact_probe.py`](../tools/artifact_probe.py) only after framing and the
expected whole-file hash pass. It refuses ambiguous duplicate FDAT spans. Default
directory-only behaviour remains available. The generic classifier now recognizes
the public UDTRFIRM identifier as a **candidate**, using 512 bytes as the source-
described header minimum. It does not validate that header's fields or checksum.

An unknown result means **unsupported opaque prefix**, not proof of encryption,
compression, a particular cipher/key or absent English/FTP functionality. No
classifier output can establish extractor applicability, exact-body identity or
native feature support.

## Actual bounded result

The one local pass exited **0**, with empty stderr, in **1.486305 seconds**.
Its same-pass whole-file SHA-256 agrees with the recorded acquisition, and the
five directory spans agree with the preceding inventory. The classifier inspected
4,096 FDAT prefix bytes in memory and returned **unknown / unsupported_opaque**.
It did not recognize the decoded UDTRFIRM identifier or another supported prefix.
The outer probe status `signature_only` describes the limited operation, not a
positive format match. No raw prefix was saved or output.

This negative result does not establish encryption, a cipher, compression or a
decoder/key choice. The audited PR remains a lead requiring validation. Original
size, modification time and read-only attribute were unchanged; these observable
checks are not a backup or an adversarial-filesystem guarantee.

The local standard-library suite passed **195 tests, three skipped, 198 total**,
exit **0**. Independent focused tests passed **19/19**. See the
[session report](sessions/20261018-RA-003-fdat-identification.md) for commands,
test scope, private lineage and limitations. Evidence: public code/author claim
**source-report**; audit **static-inference**; synthetic tests and actual bounded
result **offline-tested**. No device evidence exists.

Next single work package: **RA-003: establish an act-specific FDAT decoding basis
and bounded decoder design before real decryption or component copying**. Define
the actual copies/transformations, dependency and licence scope, accepted-contract
interaction, size/extent/checksum limits and malformed-input rejection criteria.
Real decoding has not been cleared or attempted. English and native FTP remain
primary, with exact-body/build correspondence and recovery unresolved.


## Later crypto-provenance continuation (2026-10-18)

The [crypto/source audit](FDAT_CRYPTO_PROVENANCE.md) and
[session result](sessions/20261018-RA-003-crypto-provenance.md) supersede
the preceding next-step statement. The private AES wheel and public constants
source are pinned; eight authored primitive tests passed. No actual firmware
read/decoding or camera action occurred. Constants origin and accepted-contract
interaction remain unresolved, alongside exact-body correspondence/recovery.
One predeclared experimental hypothesis is not a target support profile.
Next single package: **RA-003: implement, synthetically qualify and run one bounded private FDAT header trial for the predeclared CXD90057_k8 hypothesis**. No feature/write gate passed.
