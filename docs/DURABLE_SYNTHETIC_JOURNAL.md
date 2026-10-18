# Durable synthetic transaction journal

RA-007 host-only foundation; no camera transport, device executor, automatic
retry, inverse, rollback or hardware eligibility. The original
[in-memory simulator](OFFLINE_GUARDS.md) and FTP queue remain separate modules.
This journal records caller-supplied synthetic observations; it does not read,
modify, authenticate or restore a camera or a synthetic object's contents.

## Implemented contract and API

`tools/durable_transaction.py` exposes `DurableTransaction` for immutable
synthetic plans using `Operation` from `transaction_model.py`. The API is:

- `create(journal_path, lock_path, session_id, initial_objects, operations)`:
  exclusive creation; existing evidence is never overwritten.
- `reopen(...)`: validate the complete original plan/history under ownership,
  append a reopened boundary and enter `needs_review`, even after completion.
- `prepare_next(complete_observed_map)`: verify the complete confirmed boundary,
  persist the prepared record, then return an immutable operation description.
- `record_result(outcome, complete_observed_map)` and `interrupt_boundary()`:
  record caller claims; ambiguous, partial or mismatched results require review.
- `reconcile(complete_observed_map, evidence_identifier)`, then `resume()`:
  classify known before/after/boundary states; mixed states remain unresolved.
- `close()`: release handles in any state without repair or optimistic success.
  Context-manager exit has the same meaning. Read-only properties expose state,
  completed count, detached journal snapshots and `device_eligible == False`.

Only the `synthetic_mutation` category is accepted. Prepared records bind the
operation, component, category, attempt, boundary, whole before/after hashes and
complete observation metadata. A confirmed non-application needs reconciliation,
explicit resume and a new prepared attempt. Confirmed application advances once.

| Requirement | Implemented behavior and observed host evidence |
|---|---|
| Source/plan binding | Complete initial-object identities and ordered operation identities must match on reopen; include unselected objects. Device eligibility is always false. |
| Preparation before advancement | Append the complete prepared record, flush and fsync before returning the operation to the caller. A failed or partial append poisons that handle. |
| Append-only evidence | Bound record/file sizes, reject duplicate keys, unknown records, broken sequence/hash links and illegal transitions. Never truncate, repair or rewrite a malformed history. |
| Exclusive cooperative ownership | Competing real subprocesses cannot hold the same stable OS lock simultaneously. Bind the journal to the lock identity; never unlink the lock file or infer ownership from PID/age. |
| Conservative reopen | Every reopen begins in needs_review. A released OS lock is not permission to replay, rollback or continue a mutation. |
| Explicit reconciliation | Require the complete observed object set; classify exact expected before/after/boundary or unresolved mixed state. Successful reconciliation still needs explicit resume. |
| Interruption boundaries | Test prepared-before-send, applied-before-result, between objects and after the final result. Earlier completed and unselected objects remain preserved. |
| Persistence failures | Inject incomplete append and failed fsync, retain existing bytes, stop the handle, and refuse mutation/append until a separately reconciled reopen where possible. |
| Honest limits | Corruption detection is not authentication; caller observations are fixture claims; cooperative locks and fsync do not prove camera ownership or physical power-loss durability. |

## Evidence boundary

Bounds are 32 components, 128 operations, 1 MiB per object, 8 MiB aggregate,
64 KiB per record, 4 MiB per journal and 4096 records. Canonical ASCII JSONL
rejects duplicate keys, non-finite values, boolean/float substitutes for integer
facts, unknown events, invalid transitions and incorrect sequence/hash links.
Initial payload hashes are cached for bounded metadata-only history replay;
fresh caller observation bytes are hashed at preparation/result/reconciliation.
Short writes are attempted once and retained. Append, fsync or post-append state
adoption failure poisons that handle; no progression is permitted. A torn history
cannot be reopened or repaired by this API. A surviving complete history still
requires a separately reviewed reopen and explicit reconciliation/resume.

The stable lock uses Windows `msvcrt` or POSIX `flock`. It is never unlinked and
the canonical lock path is journal-bound. All cooperating users of one resource
must choose the same lock path. Handles are creator-PID-bound; a fork child must
not explicitly unlock the parent's shared open-file description. Plain single-link
files and ordinary directory parents are required. Windows UNC/device/stream
paths are refused before filesystem inspection. Path/descriptor checks detect
ordinary replacement; these are not protection against a hostile filesystem.

On Windows AMD64 / CPython 3.13.12, the focused command
`python -B -X utf8 -m unittest tests.test_durable_transaction -v` passed
**23 tests with one POSIX-fork skip**, exit 0. Real subprocess exclusion and five
crash boundaries, corruption, append/fsync failures, bounds and actual hard-link
refusal passed. The final complete standard-library suite passed **152 tests
with two skips**, exit 0. The other skip is unavailable real-symlink creation.
A retained private demonstration reconciled an applied-before-result crash and
completed only the next operation, preserving the earlier journal prefix and an
unselected fixture. [Exact commands, failures and results](../research/sessions/20261018-RA-007-durable-journal.md).

That focused result is `offline-tested` evidence on the owner Windows host.
Later qualification at `fb32370052a0ffe5d8a529edba971f962ce57654` passed a NEW
63-file clean export (152 passed/two skipped), plus four observed Ubuntu/Windows
CI jobs on Python 3.10/3.13 (153 passed/one platform skip per job). Ubuntu passed
the POSIX inherited-lock test and actual symlink refusal; hosted Windows also
passed actual symlink refusal. The local owner-host symlink gap remains.
[Exact run/job evidence](../research/sessions/20261018-IN-102-final.md) is retained.
Recorded host coverage does not qualify other filesystems or physical durability.
Caller observations are unauthenticated fixture claims. A hash
chain provides no authentication or anti-rollback guarantee. Cooperative OS locks
do not establish exclusive camera access. Flush/fsync and process-crash tests do
not prove power-loss or directory-entry durability. Journal/lock paths,
observations and raw logs stay private; Git contains authored code, invented
fixtures and sanitized findings only.

No real body/source identity, target offset, firmware or resource mapping can be
inferred from this work. It does not complete RA-007's target-specific review or
OFF-08/10/11. No device-write gate is passed. This is preparation for a possible
future separately reviewed executor; it adds no new gate before ordinary
separately approved UI observation.
