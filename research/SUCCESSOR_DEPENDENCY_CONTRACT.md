# Successor dependency evidence contract

2026-10-19. Evidence: **offline-tested**, **static-inference**. Shared host
preparation for the English/native Wi-Fi FTP priorities; no feature mapping or
camera access. FL2/FL3 remains deferred.

The [previous predicate audit](DEPENDENCY_POLICY_GAP_AUDIT.md) found that the
saved dependency observations cannot be substituted directly into the older
native-policy schema. `tools/dependency_evidence.py` now implements a separate,
closed, pure contract. It validates detached caller-supplied records and
transcript text. It has no file access, loader, import hook, child-process,
camera or activation API. Existing production validators are unchanged.

## Inputs and bindings

`validate_dependency_records` takes keyword-only `expectation`, `observation`,
`package`, `raw_receipt_json`, and `journal_jsonl`. The first three are plain
JSON-shaped data; the last two are UTF-8 text supplied as Python strings.

| Input | Checks and boundary |
|---|---|
| Package | Closed original manifest/proof schemas, version 3.24.1, exactly 351 payload files/RECORD rows and 352 archive entries; recomputed roster and installed proof |
| Installed receipts | Exact per-file path/hash/size and read-only flag; regular, single-link, non-reparse identity; before/after stability within each API; cross-API device/inode/mode/size/mtime agreement |
| Expectation | New `dependency_expectation_v1`; Windows/ctypes only, explicit suffix, source/config/cache/vector-plan hashes, exact origin sets, loader keywords, no fallback, separate package/runtime roots |
| Observation | New `dependency_observation_v1`; operation/policy/source/config/cache/root correspondence, isolated startup, exact Python/trusted/native origins, loader intent/audit/completion and event order |
| Raw text | New `dependency_guard_transcript_v1`; exact UTF-8 SHA-256 and checked startup/origin/load/vector/event projections |
| Journal text | Strict JSONL; exact UTF-8 SHA-256 and equality to the complete checked event sequence |

Package Python/native origins must match the complete manifest and saved
installation identity. External trusted origins belong to a separate runtime
root with independent expected identities. Roots must be distinct and
non-overlapping. Paths reject traversal, reserved names and case-folded
duplicates. Original loader argument and audit spellings remain in the hashed
observation; normalization is used only to compare the target. `ctypes.CDLL`
intent and `ctypes.dlopen` audit are distinct API records. Keywords are either
empty or an explicit integer `winmode`; their presence does not attest its
operating-system effects.

The complete installed proof is compared canonically with its recomputation,
including every per-file open-identity digest. Boolean/integer substitutions
and floating/nonfinite JSON numbers are rejected. Windows cross-API ctime is
deliberately not equated; each API must retain its own stable ctime/attributes.

## Ordering and transcript construction

The event grammar requires expectation binding, bootstrap completion and guard
installation, then exact Python imports and matched native intent/audit/
completion triples. Public-vector results precede guard completion. It then
requires raw written/flushed/fsynced/closed/reverified markers before one
callback claim/return, followed by cleanup. Missing, extra, reordered or
ambiguous outcomes refuse. Bootstrap explicitly covers interpreter, stdlib,
`_ctypes` and OS loader; transitive OS dependencies are not attested.

The raw transcript ends at `guard_finished`. Later durable/callback events bind
its exact text digest; the complete journal text digest belongs to the
observation. This avoids a self-hash cycle. Altering whitespace changes a text
digest even if the parsed projection is unchanged. Duplicate JSON keys refuse.

The vector record requires the configured plan hash, 12 cases, 24 comparisons
and a true result. No vector is executed here. The module cannot prove that a
caller genuinely ran those vectors, wrote/fsynced the text, observed those
paths, or approved the expectation before executing anything.

## Bounds and result meaning

Each transcript is limited to 4 MiB encoded UTF-8; the journal has at most 1,024
nonblank lines. Plain object traversal limits depth to 14, nodes to 100,000,
containers to 2,048 members, keys to 1,024 characters and strings to 2,048.
Accounting for JSON escaping, keys, scalars and containers checks an aggregate
8 MiB canonical representation before whole-container serialization. This is
not an 8 MiB process-memory cap: parsed JSON, detached copies and interpreter
allocations have additional costs. File-roster sizes are separately bounded.

Success is `dependency_record_contract_consistent`. Supplied text hashes and
event projections are checked; historical event authenticity, fresh observation,
operational acceptance, execution authorization, feature support, recovery and
device-write flags remain false. `complete_before_any_cipher_use` is false:
the modeled public vectors precede final guard completion. A record declaring
`saved_records` changes none of these limits.

## Qualification and remaining work

The [session report](sessions/20261019-RA-003-successor-dependency-contract.md)
records exact commands, failures, tests, source hashes and source-only reviews.
Two independent reviewers accepted the final narrow contract. Their reviews
did not reproduce tests, execute dependencies or inspect actual firmware.

This is a **new model schema**. Existing raw runtime receipts do not already
emit it. No existing-format adapter, operational producer, policy-approval
binding or saved-actual-record application has been qualified. The historical
`dependency_manifest_unobserved` and `native_policy_unobserved` blockers remain
recorded in the frozen plan. They must not be erased by assigning this model's
success status to old records.

Next single work package: **RA-003: audit the existing authored dependency
producer and saved-record schemas, then implement and qualify a lossless adapter
on invented old-format receipts, preserving original transcript bytes, unknown
fields and unsupported claims as explicit refusals/blockers; obtain independent
source review before applying it to saved actual records.** No dependency
execution, protected-input inspection or camera contact is part of that package.
