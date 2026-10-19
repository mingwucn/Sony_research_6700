# Legacy dependency receipt adapter

2026-10-19. Evidence: **static-inference**, **offline-tested**. English and native
Wi-Fi FTP remain primary; no new feature mapping. The previous
[successor contract](SUCCESSOR_DEPENDENCY_CONTRACT.md) is a prospective model.
The existing authored producer does not emit that model's transcript or event
grammar. Reconstructing its missing events would invent historical evidence.

`tools/dependency_legacy.py` instead validates and preserves the old format in
a separate `legacy_dependency_envelope_v1`. Success is
`legacy_records_consistent_with_blockers`, never successor-contract success.
This is pure standard-library metadata handling: no file reader, cache loader,
native dependency, subprocess, firmware or camera API.

## Audited producer identities

Ordinary authored Python was read as source only, without importing it:

| Source | SHA-256 |
|---|---|
| Existing runtime_entry.py | 4a64bd6c63ff6e43b56ab7298e5fb84a6304e3576990eaa4aa020c551aeba8f1 |
| Existing continuation_probe.py | 75ab70f9445ee9d1f072252fabaab8d0dca54c576b8b3b5b6ec874005a609592 |
| Shared dependency_evidence.py, unchanged | 63eb311df4c818458edd28dd9853c3c20234460f3cf145eb16886ef0abbb12f3 |

The first two are existing private authored source, not firmware or installed
library files. Their bytes and historical outputs remain unchanged. Inspection
of their schemas informs this adapter; it does not bind those sources into an
accepted operational authority chain.

## Cross-format audit

| Existing record | Adapter treatment | Remaining boundary |
|---|---|---|
| dependency_probe_config_v1 | Exact operation/source/native/trusted rosters, Windows paths, hashes/sizes and public vector plan | Cache content not read or revalidated |
| Manifest/351 installed receipts/proof | Shared closed package and expectation predicates | No fresh installation observation |
| dependency_probe_raw_result_v1 | Exact schema, false feature/GDT flags, expected hashes, source/trusted origins, cases and native receipt | Caller-supplied metadata; runtime label is not authenticated |
| Legacy descriptor read receipt | Closed stamps, sizes, read counts, EOF, close and expected identities | No explicit open-mode field; no read-only assertion manufactured |
| dependency_probe_native_receipt_v1 | Five matched intent/audit/completion records, exact backend, no failures, false transitive attestation | OS-mapped bytes and transitive libraries unproved |
| Raw events | Original numbering, nested source-execution pairs, native triples and vector results checked | No invented guard-install/finish events |
| Outer journal | Same raw-event data with the producer's one-position numbering shift, then exact publication/callback sequence | Publication combines write/flush/fsync/close/readback in one marker |
| Completion result | Public-vector callback, fresh-source receipt claims, cleanup claim and runtime-source digest checked | Cleanup is a completion claim, not a journal event; no producer authenticity |

The adapter receives an explicit expectation, package metadata, configuration,
completion record and two original transcript strings. It does not derive an
allowlist from observed successful loads. Expectations supplied later for a
retrospective comparison cannot establish approval before the historical act.

Windows/ctypes, CPython 3.13.12, version 3.24.1, eleven Python origins, five
trusted origins and all five native loads are the qualified profile. The old
producer allows AESNI absence, but this exact-set expectation profile refuses
that variant; no optional native policy is inferred. Other platforms/backends,
versions or schemas require separate work.

## Specific checks

Original paths and loader spellings remain in the envelope. Configuration/read
paths must have the canonical Windows spelling accepted by the old reader;
loader intent/audit paths are separately normalized only for target comparison.
Raw source origins and descriptor paths bind back to the original configuration.
Common package/runtime roots and expected identities remain distinct.

Source-byte metadata respects the producer's 1 MiB per-source and 4 MiB total
limits. The vector plan is bound to the exact authored public known-answer
metadata, canonical SHA-256
`a914aca415d20a87a56440f36944f7ac6082ecbc36387b68694175a579bc43b5`.
It was derived by AST literal parsing of the pinned source's public test
constants, without executing source or a cipher. The test fixture uses those
public values; their keys are test vectors, not private inputs.

Each vector result requires no unfinished source execution, completed AES and
the relevant mode source, and completed `aes` plus `ecb`/`cbc` native loads.
Lazy CBC import/loading between vector results remains permitted. This checks
specific prerequisites, not complete semantics of the dependency's code.
Startup module lists must agree with the absence of preloaded `_ctypes`;
isolated/no-site flags retain their original integer types. Both startup
snapshots bind the expected interpreter and four-path no-site profile.

The common 4 MiB UTF-8 transcript and 8 MiB bounded canonical-object rules still
apply. In addition, canonical producer raw output plus newline is at most
2 MiB; every raw/journal event plus newline is at most 32,768 bytes. These are
representation limits, not a whole-process memory cap. Exact supplied text,
including whitespace, is preserved and hashed separately from canonical
producer-size checks. This does not attest that the original emitter wrote
that exact representation. Unknown fields/versions refuse; none are silently
discarded. Duplicate JSON keys and float/nonfinite numbers refuse.

## Output and blockers

The envelope contains the detached expectation/package/configuration/completion,
exact original raw and journal text, their hashes, startup projections, counts
and an explicit blocker list. Its complete contents remain private if later
applied to actual records. No text is relabeled as a successor event/transcript.
All historical/operational/execution/feature/recovery/write flags remain false.

Blockers preserve the missing successor transcript/grammar, individual durable
steps, guard events, journaled cleanup, explicit read-only mode, prior
expectation approval, bound producer authority, revalidated cache contents and
fresh runtime observation. Historical null-input blockers in the frozen plan
remain recorded. Envelope consistency does not resolve any of them.

## Qualification and next work

Exact results and review corrections are in the
[session report](sessions/20261019-RA-003-legacy-dependency-adapter.md). Two
independent source-only reviewers accepted the corrected narrow scope. No
actual receipts/configuration/cache or protected inputs were read in this
package, and no independent execution/reproduction is claimed.

Next single work package: **RA-003: bind the adapter, shared validator and exact
producer identities into one saved-metadata diagnostic with explicitly
retrospective expectations; qualify source substitutions and complete input
cross-bindings, then obtain independent source review before a once-only
ordinary saved-record application.** No native dependency loading,
protected-input inspection or camera contact.
