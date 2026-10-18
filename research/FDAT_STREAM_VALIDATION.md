# RA-003: bounded-memory full-stream FDAT format validation

## Before-read act and necessity record

Recorded before any full-stream decoding on 2026-10-18, basis
`84e750de41f208d7e0ad6c21c869ca0d9483aeb1`, branch
`codex/ra003-stream-validation`. English and native Wi-Fi FTP remain primary.
Camera commands: **none**.

The successful [first-header experiment](FDAT_HEADER_TRIAL.md) cannot establish
actual logical decoded length, every block's envelope/terminal consistency or
whether declared extents fit that length. These specific format questions require
streaming every physical block. This experiment will retain no decoded-stream or
component files and will not extract, decompress, disassemble or map components.

The exact original remains the privately acquired official package:
1,024,017,848 bytes, SHA-256
`d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c`.
The observed FDAT package-file span starts at 156 and is 1,024,017,680 bytes long.
Those are package-file observations, not target/runtime/storage addresses.
Use only the existing experimental `CXD90057_k8` hypothesis, with no fallback.

The [narrow statutory format-study rationale](FDAT_DECODING_PLAN.md) remains the
documented basis for necessary private decoding. Accepted-contract interaction
and independent constants derivation remain unresolved. This act-specific scope
does not clear later component copying, distribution, modification or device work.
No new agreement or generic permission-only question is introduced.

Before the real run, qualify the authored private implementation synthetically
and review its exact runner. Journal before source I/O. Open one fresh ordinary,
single-link, non-reparse read-only descriptor in trusted private directories.
A preliminary whole-parent hash/framing pass obtains 16 IV bytes; rewind the same
descriptor for streaming decode and hash the entire actual decoding pass again.
Compare the encountered IV to the captured IV; require source identity/size/hash,
framing and same-API before/after file observations to match before accepting results.
The two passes are predeclared reads, not retries. No automatic restart is allowed.

Decode the first physical 512 bytes with ECB, then maintain one continuous CBC
state through the remaining ciphertext. Validate every complete 1,024-byte block:
sum over all trailing LE16 words, payload length 0..1020 and terminal flag exactly
matching physical last position. The first payload must contain the 512-byte header.
Zero or odd later payload lengths are permitted; zero never signals physical EOF.
There is no encoded block ordinal. Hash/count logical payload only, excluding
envelopes and padding. Compare the final physical count to 1,000,017.

Retain only 512 accumulated logical header bytes, digests, counters and bounded
metadata. Source requests are capped at 1 MiB; crypto batches at 64 KiB. Budget 4 MiB
for managed source/cipher/plaintext buffers, separately from interpreter/native
heap and bounded parser metadata; do not claim a total-process memory cap.
No raw decoded header, full stream, child files, operational constants or working
decoder will enter Git or external services. Keep source notices locally.

Only after all stream/parent/identity checks pass may the existing decoded-header
validator receive the **measured** logical length. Keep its result nested: its
pure-API `decryption_performed=false` does not describe the pipeline's actual
decoding. Declared bounds/non-overlap are not component-format validation.

Stop on any mismatch; preserve a terminal negative/needs-review result and do not
change thresholds or try another key. The final 256 trailer bytes remain
uninterpreted/unauthenticated. Sums, CRC and hashes establish consistency/identity,
not authentication, body correspondence, ABI, English resources, native FTP,
recovery or a feature/device-write gate.

Status at scope recording: implementation, qualification and real run pending.
The exact original scope bytes are preserved privately and pinned by the real journal;
minor spacing edits above and the result below were added after completion.


## Observed result

**Offline-tested:** one pipeline passed, exit **0**, **28.836450s**.
Both predeclared parent passes matched the pinned size/hash and fresh five-span
directory; same-descriptor/source observations and encountered IV agreed. All
**1,000,017** physical blocks passed envelope sums and exact terminal
position checks with continuous CBC state. Final payload **832 bytes**; zero empty
blocks and zero short nonterminal blocks. Logical length **1,020,017,152 bytes**;
SHA-256 `e48b05235ddba0d8098fa4d71dd88d85ffe4e5ab440581003c6c3b4d5a813373`.
Header SHA matches the earlier bounded trial. The omitted 256 bytes stay uninterpreted.

The existing header validator received the measured length only after all source
and stream checks. Its `decoded_bytes_is_caller_supplied=true` describes the pure
API boundary; the caller now supplies an actual full-stream measurement. Its
`decryption_performed=false` remains nested beneath the pipeline's true flag.

| Declared object | Decoded-FDAT file offset | Bytes | Exclusive end |
|---|---:|---:|---:|
| Header | 0 | 512 | 512 |
| U filesystem slot 0 | 512 | 1,253,376 | 1,253,888 |
| P filesystem slot 1, empty sentinel | 512 | 0 | 512 |
| Firmware extent | 1,253,888 | 1,018,763,264 | 1,020,017,152 |

Nonempty declared spans do not overlap; firmware ends exactly at measured EOF.
These are **decoded-file declarations**, not runtime/storage/target addresses.
Neither slot-count semantics nor actual child formats are validated.

New private synthetic qualification: **45 passed, zero skipped**, exit **0**,
unittest **0.415s**. Independent fixture CRC, logical digest oracle and cipher-call
spy cover continuous CBC, multi-batch boundaries and late corruption; zero/odd
lengths, exact terminal state, short reads, parent mutations, measured EOF+1,
overlap, nested flags and actual NTFS hardlink refusal are exercised. Progress
callback delivery was observed during the real run, not synthetically qualified.
All 351 installed crypto artifact hashes matched before import. Authored reader,
tests and runner received independent review; no upstream code ran.

Only metadata remains: no raw stream/header/component file, keys or working
decoder enters Git. The 4 MiB managed-buffer budget is a design bound, not a
measurement/cap of whole-process memory. Complete format semantics, authentication,
installed-body/build identity, English resources/restrictions, native FTP,
conditional recovery and feature/device gates remain unverified.

Historical next single package: **RA-003: document the necessary private selected-component scope, then synthetically qualify and run bounded in-memory identification of the declared U-slot and firmware extent prefixes, retaining lineage metadata only**.
Identify bounded prefixes before choosing any component copier/decompressor;
retain parent hash, measured-stream hash, explicitly labelled file spans, probe
revision/limits and classifier metadata. No component extraction, decompression,
disassembly or camera action is cleared by this result. See [session commands/results](sessions/20261018-RA-003-stream-validation.md).

## Later component-prefix continuation (2026-10-18)

Earlier next-package recommendations are historical. The
[bounded prefix audit](COMPONENT_PREFIX_AUDIT.md) and
[session commands/results](sessions/20261018-RA-003-component-prefix.md)
record 93 combined synthetic tests passed, exit 0, 0.441 seconds. One real
pipeline passed with two source-hashed passes, exit 0, 23.899888 seconds.
It observed 4,096 prefix bytes per declared extent (8,192 total): the U-slot
returned a SquashFS header candidate and firmware a ustar header candidate,
both `header_only`. Source/stream lineage and measured extent checks passed.
These are bounded identification leads; component formats, authentication,
body correspondence, features and device-write gates remain unverified.
No raw prefixes or component files were retained. Camera commands: **none**.
English and native FTP remain first.

Next single package: **RA-003: document and qualify a bounded-memory, metadata-only tar-directory inventory of the candidate ustar firmware extent, then run it with full source/stream lineage checks and no child files**.
