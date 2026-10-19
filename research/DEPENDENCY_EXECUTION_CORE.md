# Dependency execution core: proof transition and record verification

2026-10-19. Evidence: **static-inference**, **offline-tested**.
English/native Wi-Fi FTP remain primary; FL2/FL3 deferred.

This implements required pieces of the complete noninjected route described in
[the activation packet](DEPENDENCY_ACTIVATION_PACKET.md). It does not finish that
route or make the non-runnable activation packet executable. Actual installed
dependency observation and all feature/recovery/write authority remain absent.

## New prospective texts and digest domains

`tools/dependency_execution.py:prepare_texts` takes an explicit operation identifier,
the fixed public vector plan, and eleven exact source strings. It emits new
prospective configuration/cache documents and separate raw UTF-8-file and
canonical-object digests. It does not silently convert a historical cache or
inherit its authorization. Independently observed original source/file receipts
and rights/scope evidence remain necessary for actual use.

The vector structure is bounded and detached before hashing. Source values must
be exact strings; character, UTF-8 and escaped JSON byte budgets precede
serialization. Per-source UTF-8 bytes remain bounded to one MiB, combined source
bytes to four MiB, and serialized documents to four MiB. Surrogate code points
are refused. Non-ASCII/control/DEL escaping is counted explicitly; output-size
guards remain in place after serialization too.

## Revalidated complete collection and fresh-proof transition

`bind_collection` independently checks the complete invented collection's closed
schema, all 351 absolute receipts, separate relative projections and their
hashes, five trusted receipts, source roster/cache binding, root identities,
strict counts/flags, unchanged manifest and newly recomputed installed proof.
The input package and policy remain intact. Returned inputs are detached.

| Preserved domain | Derived domain |
|---|---|
| Original policy/package/binding hashes | Newly observed proof/package hashes |
| Original review digest | Same digest, explicitly no new independent approval |
| Manifest, source/config/cache/root/native expectations | Only installed-proof binding may differ |
| Absolute opened receipt | Separate path-only relative projection |

The transition records actual differing policy fields, including an empty list
when receipts/proof are unchanged. It cannot promote the existing invented
collector's records into actual observations. A future actual branch needs a
separate explicit collection grammar and appropriate exact runtime/input bindings.

## Integrated invented path and strict saved-record verifier

`produce_collected_invented` checks and detaches bounded inputs, exclusively
reserves one output folder, then runs:

1. Complete invented package/trusted collection.
2. Independent pure collection verification and proof transition.
3. Publication of collection/transition metadata before producer bootstrap.
4. Existing producer with invented reader, audit, native loader and cipher.
5. Exact six-file producer artifact roster and pure saved-record verification.
6. Exclusive completion publication; one callback only, no automatic retry.

Failures retain existing artifacts and identify the failed stage. A failure while
publishing a refusal keeps the primary exception and exposes the publication
exception as its cause. Completion publication is never retried. This is ordinary
host output handling, not a camera transaction/recovery implementation.

`verify_records` takes supplied byte buffers only. It checks exact artifact and
result rosters, policy/binding equality, transcript/journal hashes and event
projections, nested source execution trace and completion order, and audit
acknowledgement. Both invented and saved-record grammars are covered, but all new
tests use invented data. Grammar flags cannot authenticate actual historical
events, producer source, interpreter, OS-mapped bytes or CPU results.

This verifier returns false historical-truth/runtime/producer authentication and
execution/feature/recovery/write authority. It performs no file read, bootstrap
or native load. The qualification composition reads only its newly generated
invented metadata. It refuses `RuntimeOps`/subclasses; ordinary CLI also refuses.

## Remaining complete-route work

The disposable child must still bind every executing helper and input buffer;
validate runtime/optimization/module-resolution and preloaded-module rules;
separately represent actual collection and prospective derivation; recheck the
execution freshness interval; supervise one process with bounded wait/reap and
uncertain-state reconciliation; and independently verify its saved result in the
parent. Current ordinary parent imports are not an authenticated executing-parent
contract. There is no actual activation entry or prepared activation command.

Sequential collection remains non-atomic, transitive DLLs and mapped bytes remain
unattested, and initial public-vector use precedes final guard completion. The
strict eleven-Python/five-native roster, including AES-NI, stays unchanged.

[Session commands/results and independent review](sessions/20261019-RA-003-execution-core.md).
No camera commands, firmware/constants/native-body inputs or private uploads.
