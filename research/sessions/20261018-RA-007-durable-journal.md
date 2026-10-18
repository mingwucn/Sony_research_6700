# Session report: 2026-10-18 / RA-007 durable synthetic journal

Status: **durable synthetic host foundation passed on Windows; RA-007 remains
PARTIAL for exact-target evidence and any future executor qualification**.

## Context and scope

Starting commit: `7324fee9185aedc95e6ed50b60ea7a4acecfc856`.
Topic branch: `codex/ra-007-durable-journal`. The starting revision records
feature-progress notes and clean authored-tree reproduction. This continuation
implements the next recorded host package and updates feature continuity.

Host: Windows AMD64 build 26300.9711, CPython **3.13.12** at
`C:\ProgramData\miniconda3\python.exe`; PowerShell 7.6.5 and
Git 2.53.0.windows.2. Windows `msvcrt` is available; POSIX `fcntl` is absent.
No other platform or interpreter result is inferred.

Scope: R0, authored standard-library code and invented local fixture bytes only.
Camera commands: **none**. No USB identification, network/server, driver or
firmware change, upstream launcher/service program, private upload or device
executor is involved. Firmware, region and owner intake remain Unknown.
No feature support, backup completeness or device-write gate is established.

Original source locks, host-lab lock, UNVERIFIED profile, AGENTS and VALIDATION
are protected against changes. MASTER_PLAN changes only to record the owner's
explicit English/FTP priority update below. Existing private continuity
notes/state and owner intake have NEW snapshots in the private session directory.

## Acceptance defined before testing

The [contract](../../docs/DURABLE_SYNTHETIC_JOURNAL.md) requires complete plan/source
binding, a durable prepared record before advancement, bounded strict append-only
evidence, cooperative OS exclusion, conservative reopen, explicit complete
observation/reconciliation/resume and permanent device ineligibility.

Fault tests must preserve earlier completed/unselected objects and distinguish
prepared-only, applied-before-result, between-object and confirmed-complete
boundaries. Corrupt/torn records must be refused without repair; uncertain
append/fsync must poison the active handle. No automatic replay, retry, rollback,
inverse, stale-lock takeover or optimistic completion is accepted. Caller-supplied
fixture observations remain claims; no authenticated device read is implied.

## Commands and results

All Python commands below used CPython 3.13.12. Private capture records contain
prepared/result records, argv, cwd, stdout/stderr and exit status, in newly named
files without overwriting previous attempts. The capture wrapper was:

```powershell
python -I -S -B -X utf8 private/sessions/20261018-RA-007-durable-journal/capture.py LABEL C:/ProgramData/miniconda3/python.exe CHILD_ARGUMENTS
```

| Capture label | Child command / result |
|---|---|
| branch-01 | `git switch -c codex/ra-007-durable-journal`; exit 0 |
| focused-durable-01 | `python -B -X utf8 -m unittest tests.test_durable_transaction -v`; 17 total, 13 passed, 1 failure, 2 errors, 1 POSIX skip; exit 1; 1.820 s |
| focused-durable-02 | Same focused command after fixes; 20 total, 19 passed, 1 skip; exit 0; 2.312 s |
| focused-durable-03 | Same focused command after metadata-replay optimization; 20 total, 19 passed, 1 skip; exit 0; 2.509 s |
| focused-durable-04 | Same focused command with bounds and actual hard-link checks; 24 total, 23 passed, 1 skip; exit 0; 2.918 s |
| focused-durable-05 | Same focused command after scoping Windows path-syntax checks to Windows; 24 total, 23 passed, 1 skip; exit 0; 2.406 s |
| standard-suite-01 | `C:/ProgramData/miniconda3/python.exe -B -X utf8 -m unittest discover -s tests -v`; 150 total, 148 passed, 2 skips; exit 0; 18.487 s |
| standard-suite-02 | Same full command after bounds/hard-link additions; 154 total, 152 passed, 2 skips; exit 0; 18.799 s |
| standard-suite-03 | Same full command after the Windows-test scope correction; **154 total, 152 passed, 2 skips; exit 0; 16.893 s** |
| retained-demo-01 | `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261018-RA-007-durable-journal/retained_demo.py`; exit 0; intentional fixture child exit 23 |

`python` resolves to the interpreter recorded above. Isolated child interpreters
use `-I -S -B -X utf8`; `-B` is explicit because `-I` ignores environment-only
bytecode suppression. The full suite opens no network peer; optional FTPS lab
execution was not repeated. The historical clean 58-file export at `9d5f4ba`
does not qualify these new files.

Both final skips are explicit: POSIX fork inheritance is unavailable on Windows,
and the older inventory real-symlink fixture cannot be created here. The new
actual hard-link fixture succeeded and both linked names were refused with their
bytes preserved. Bounds were tested by lowering constants with small invented
fixtures, avoiding large allocations. No Linux/Unix, alternate interpreter,
independent host or remote CI result is inferred.

## Failures, review corrections and retained evidence

The first focused run found a raw existing-file exception instead of the API's
JournalError, and incomplete confirmed observations could leave a prepared state.
The implementation now wraps exclusive-create failure and records interruption
on invalid result observations. A test also tried to read the locked byte via
another Windows handle; that assertion now reads after ownership is released.
The Windows lock behavior was preserved. The failed output remains private.

Static review additionally found boolean/integer/float equality ambiguity in
rehashed facts, missing durable attempt/category facts, constructor/append
cleanup boundaries and a POSIX inherited-handle unlock hazard. Strict canonical
fact comparison, explicit prepared attempts/category, cleanup/poisoning and
creator-PID ownership address these. Regression tests pass where executable;
the POSIX fork regression remains skipped pending an actual POSIX run. Windows
UNC/device/stream paths are rejected before filesystem inspection. Initial hashes
and operation boundaries are cached so history replay compares bounded metadata;
fresh observations are still independently hashed on each relevant call.

Final portability review found that the Windows UNC/device/stream syntax test
would incorrectly run on POSIX, where that syntax policy does not apply. Its
explicit Windows-only decorator fixes the test scope; the subsequent focused
and complete Windows runs passed. This is a static portability correction,
not a substitute for observing the POSIX CI result.

The retained demonstration uses three newly created invented files. A child
persists preparation, explicitly changes one fixture outside the journal API,
then exits 23 before recording the result. Reopen enters `needs_review`, refuses
preparation/resume and reconciles the complete fixture set as `applied`.
Explicit resume prepares only the next operation. Two operations finish, their
prepared IDs each appear once, seven journal records remain, the crash-time
history is a prefix of the final history, and the unselected fixture is unchanged.
The API itself performs no fixture mutation. Raw argv, before/after observations,
hashes and journal copies remain local.

## Feature notes, changed files and publication review

The owner's requested public and internal function notes continue to track five
separate results: native English, FL2/FL3 stills/preview, separately gated
calibrated custom looks, native Wi-Fi FTP, and the optional HOST-ASSISTED bridge.
Each records progress, blockers, next feature package and evidence. Shared host
progress is updated without promoting it to target feature support. STATE and
both private structured copies have identical requested_features entries.

During this session the owner explicitly reprioritized **English and native FTP
above FL2/FL3**, which can wait for future work. Public and private notes, README,
MASTER_PLAN, hand-off, backlog and STATE now record that priority. Existing looks
evidence remains available; custom looks remain separately gated after FL2/FL3.
This changes scheduling only, not acceptance thresholds or device permissions.

Reviewed authored paths for this package:

- `tools/durable_transaction.py`, `tests/test_durable_transaction.py`:
  synthetic journal implementation and independent fault/subprocess tests.
- `docs/DURABLE_SYNTHETIC_JOURNAL.md`, `docs/OFFLINE_GUARDS.md`:
  API, evidence and limitations; original simulator's contract remains explicit.
- `README.md`, `docs/MASTER_PLAN.md`, `docs/CODEX_HANDOFF.md`, `docs/BACKLOG.md`:
  discovery, continuity and package sequencing.
- `docs/FEATURE_PROGRESS.md`, `research/STATE.json`,
  `research/PRE_CAMERA_READINESS.md`, this report: synchronized progress/evidence.

Ignored updates are limited to private session evidence/demonstration, the
snapshotted continuity state and feature notes. Owner intake and protected files
retain their prior hashes, except the explicitly authorized priority-only
MASTER_PLAN edit. No private/reference/runtime artifacts are staged.
Explicit path staging and complete staged-content review are required before
the topic commit. No project-wide or inherited-code licence is introduced.

Continuity/publication verification command:

```powershell
python -I -S -B -X utf8 private/sessions/20261018-RA-007-durable-journal/capture.py verify-review-01 C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261018-RA-007-durable-journal/verify_review.py
```

Exit **0**: all five function records and their priorities agree across the three
structured copies; owner observations/approvals and intake are preserved; the
five unchanged protected files match; exactly 12 authored paths are proposed;
private evidence is ignored/untracked; links, text checks, final test captures and
whitespace checks pass. This bounded review is not a comprehensive secrets or
rights detector. MASTER_PLAN's scheduling-only diff was reviewed independently.
Only the 12 named paths are staged, followed by `git diff --cached --check`,
`git diff --cached --name-status` and complete staged-content inspection.
The same helper with `--staged` verifies exact staged paths and no unstaged diff.

## Practical limits

Evidence class: **offline-tested**, plus separately labelled static review.
Caller observations are unauthenticated claims. Hash links do not authenticate
history or prevent rollback. Lock ownership covers cooperating processes using
the same caller-chosen stable path; it is not camera ownership or hostile-host
protection. Process exit releases OS handles, not uncertainty. Flush/fsync is not
physical power-loss or directory-entry durability. No repair, stale-lock takeover,
automatic replay, inverse, retry, rollback or device execution exists.

## Remaining prerequisites

Exact firmware/region/languages and remaining owner facts, legitimate matching
inputs, approved access/coverage, mappings, recovery and all physical feature
results remain absent. OFF-08/10/11 remain target-dependent. Remote CI, other
hosts, real-symlink coverage and publication rights remain distinct prerequisites.
The next single work package is **IN-102: qualify the final committed RA-007
revision using a fresh authored-tree/no-pip reproduction and inspect the actual
existing Windows/Linux CI matrix**. Include a final publication/feature-note
consistency review. A prepared workflow is not a passing run; POSIX fork remains
unverified until observed. The next target-specific package remains RA-003 once
the missing installed-firmware fact and matching input provenance exist.
Camera commands: **none**. No feature supported and no device-write gate passed.
