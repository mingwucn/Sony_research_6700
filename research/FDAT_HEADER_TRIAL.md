# RA-003: one bounded private FDAT header trial

Reviewed 2026-10-18 on `codex/ra003-header-trial`, basis
`1c952fd160cfeaa66bc239a5a23dd15c142cc9a0`. English and native Wi-Fi FTP remain
primary. Camera commands: **none**.

## Result and evidence scope

**Offline-tested:** the one predeclared `CXD90057_k8` hypothesis passed its
declared first-block envelope and logical-header predicates, exit **0**, in
**6.517645 seconds**. Exactly one hypothesis was attempted; no fallback or
retry occurred. This is the first real bounded decoding observation. It is not
an accepted target profile, authenticated key selection or complete firmware decode.

The original official package again matched **1,024,017,848 bytes** and SHA-256
`d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c`.
Fresh framing matched all five prior spans; the one FDAT has 1,000,017 physical
ciphertext blocks under the experimental shape. Same-read full-source hashing,
ordinary/single-link/non-reparse checks, fresh read-only descriptor and stable
before/after observations passed. The original read-only attribute stayed set.
Trusted intermediate directories and observable-change checks are not an atomic
snapshot or an OS sandbox.

Only the first 1,024 FDAT bytes and 16 IV bytes were retained for decoding.
Each source read requests at most 1 MiB. The authored reader budgets **3 MiB for
managed source buffers**, including at most two transient input chunks and
1,040 retained bytes; it does not cap total interpreter/native-process memory.
No raw cipher/plaintext, stream or component file was written or published.

The full 1,024-byte first plaintext block passed its unsigned LE16 envelope sum,
declared payload length **1020** and nonterminal requirement. The logical header
at physical plaintext `[4:516]` passed identifier/version, U/N flags, final-zero
predicate and CRC32. These positions describe FDAT format, never target addresses.
CRC and additive sum provide consistency checks, not authentication.

Header-only metadata includes two declared slot records. Their forms and extents
remain **unvalidated declarations at decoded-FDAT file offsets**. No actual decoded
stream length was measured, and `tools/fdat_header.py` was deliberately not called
with an estimated size. No component presence/format, payload integrity, signature,
container semantics, installed-body correspondence, architecture or ABI is proved.
The remaining 256 trailer bytes are uninterpreted and unauthenticated.

## Qualification and implementation review

The authored implementation and tests stay in ignored private storage. They do
not import or run fwtool, firmware assets or an upstream launcher. Required
operational constants were parsed solely as data from the previously pinned
AST-only source. Values and a working decoding implementation remain unpublished.
The isolated private crypto environment and **351 installed wheel hashes** were
checked against the pinned artifact before decoding; third-party AES/native code
did execute. Dependency isolation is not a security sandbox.

Corrected synthetic run: **45 passed, zero skipped**, exit **0**, unittest
**0.428 seconds**. Tests cover min/odd/max lengths, malformed length/terminal
fields, whole-first-block checksum coverage including padding, CRC and the four-byte
cipher-boundary overlap, wrong keys/IV/layout, fresh state, malformed inputs,
whole-parent hashing, short reads, framing/range errors and source-file mutations.
An independent bitwise CRC oracle and exact cipher-call spy strengthen the
fixture checks. Actual NTFS hardlink refusal was exercised.

The initial run was **36 passed / one failed out of 37**, exit **1**. Its relocated
span fixture exceeded parent bounds before the expected framing check; adding a
dummy final chunk made that fixture test the intended condition. No acceptance
threshold was weakened. Original sources/logs are preserved. Buffering was also
refined after independent review; six wrapper cases and two oracle/call cases
were added. Two independent source reviews found no remaining trial blocker.

## Basis, limitations and next package

The existing [narrow statutory format-study assessment](FDAT_DECODING_PLAN.md)
and [source/dependency provenance review](FDAT_CRYPTO_PROVENANCE.md) remain the
documented basis. This experiment did not resolve accepted-contract interaction
or independently derive the constants. It clears no distribution, component
extraction, decompression, disassembly, modification or device operation.

English resources/restriction mechanisms and a native FTP binary/invocation/
media/network lifecycle remain unmapped. No requested function, rollback system
or device-write gate passed. FL2/FL3 remains deferred; calibrated custom looks
follow separately; a bridge remains optional and **HOST-ASSISTED**.

Next single package: **RA-003: assess and document the necessary private full-stream format-study scope, implement and synthetically qualify bounded FDAT stream validation, then measure decoded length and SHA-256 through bounded memory without retaining decoded-stream or component files**.
Document necessity/acts/retention before the read. Keep the same single hypothesis;
validate every envelope and terminal state before accepting a measured length/hash.
Only then can the existing extent validator check declared bounds/non-overlap.
No child files, decompression, disassembly or camera contact belong in that package.
See the [session report](sessions/20261018-RA-003-header-trial.md) for exact commands,
interpreter, failures and changed files.
