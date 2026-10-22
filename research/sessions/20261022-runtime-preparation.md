# RA-003: retained runtime checker and synthetic command preparation

2026-10-22. Branch `codex/ra003-synthetic-runtime-preparation-20261022`,
baseline `c2f280f`. Evidence: **offline-tested** and **static-inference**.
Native English and native camera-to-server Wi-Fi FTP remain first. Camera
commands: **none**. No feature, recovery or device-write gate passed.

The constructed current context now passes the genuine retained `verify_context`
over invented ordinary files. Packet/request saving is shared with the existing
launcher, and a data-only synthetic preparation entry applies the capture,
retained-source, request and saved-file checks before returning the context.
The unchanged isolated bootstrap transports that saved request and all **49**
source entries to an explicitly invented, inert child.

## What changed and what this establishes

- `tools/dependency_operational_launcher.py`: extracted `_save_command` from
  the existing preparation path. It writes packet/request files exclusively,
  detaches caller metadata and preserves the existing request/bootstrap grammar.
  The legacy path now obtains its interpreter profile before the shared writer;
  a profile failure therefore creates no packet file. Its v6 refusal still
  occurs before either action.
- `prepare_synthetic_context` checks the complete capture roster, retained source
  bindings, current operation/folder and original document hashes against the
  already-validated gate result; it constructs the current context and calls
  `check_saved`. Its returned data has no control, helper, callback or source
  owner and is not an operational `_run_pending` plan.
- `tests/test_dependency_retained_context.py`: **12** cases run the pinned,
  unchanged authored checker. Changed documents, current/retained source bytes,
  implementation bytes, missing files, directories, hard links, malformed
  context and traversal refuse. Reads during checker verification are observed
  inside the invented temporary tree; the fixture's source manifest is not
  opened. The inactive loader still refuses.
- `tests/test_dependency_preparation_context.py`: **14** cases qualify the
  shared preparation path, real checker acceptance, exact bootstrap transport,
  caller detachment, source/packet/request changes, retained rebinding and
  no-overwrite failures. Existing-request collisions and fresh-source failures
  preserve partial files for inspection, return no plan and do not retry.

The retained checker is **58,942 bytes**, SHA-256
`70a2ed3a0265894adace48e5285c0eb8962c666975f7df1a8e4f6141b918bb43`.
The test loads this authored private source without copying it into Git or
replacing its predicates. Its active checker uses standard-library ordinary-file
and hash operations. A dormant `gdt_preflight` import elsewhere in the module is
accounted for statically and remains blocked by the test loader's import guard.

The checker establishes ordinary-file consistency. It does **not** independently
validate command/basis/source-manifest semantics or authorize execution; a test
demonstrates this boundary. The complete roster, reviewed bootstrap and current
request checks remain separate responsibilities of the preparation code.
Caller-provided gate results and runtime profiles are trusted fixture inputs,
not newly authenticated observations. The synthetic entry is a trusted
authored-code seam, not a sandbox for arbitrary caller-selected paths or source.

Actual parent/child v6 refusals and public runtime/CLI refusals remain in place.
The child source and current-context constructor are unchanged. The current
synthetic preparation entry does not perform source-owned adapter projection or
full metadata preflight, instantiate operational helpers, reserve/run the
retained supervisor, or call `_continue_child`. Those stages are covered by
separate existing synthetic tests; their complete joined current-context
handoff is the next package. No actual firmware analysis result follows here.

## Commands and results

Host: Windows, PowerShell **7.6.5**, CPython **3.13.12** at
`C:/ProgramData/miniconda3/python.exe`.

```powershell
git status --short --branch
git log -1 --oneline
git switch -c codex/ra003-synthetic-runtime-preparation-20261022
New-Item -ItemType Directory -Path private/sessions/20261022-runtime-preparation -ErrorAction Stop | Out-Null
$PSVersionTable.PSVersion.ToString()
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys; print(sys.version); print(sys.executable)"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-runtime-preparation/qualify.py qualification-01
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-runtime-preparation/record.py
git diff --check
```

The initial tree was clean. Branch creation, qualification, recording and diff
checks exited **0**. Final combined suite: **139 cases, 138 passed, 0 failures,
0 errors, 1 skipped**; **76.915s** unittest / **78.212s** runner. The sole skip
is real symlink creation: Windows privilege error **1314**. Hard-link refusal
passed. No elevation or system change was attempted. The six measured source/test
files remained byte-identical during qualification.

The exact runner is retained privately and loads these modules explicitly,
with the repository and `tests` directories inserted into `sys.path` under
`-I -S -B -X utf8`; it does not perform broad test discovery:

```text
test_dependency_current_context
test_dependency_retained_context
test_dependency_preparation_context
test_dependency_host_entry
test_dependency_migration_transport
test_dependency_operational_launcher
test_dependency_preparation_migration
test_dependency_operational_preparation
test_dependency_operational_entry
```

Earlier focused checks passed **55/55** preparation/launcher/migration/context
cases, then **2/2** added failure cases. Retained-checker qualification ran
**12 cases: 11 passed, 1 skipped**. Its initial attempt stopped before tests on
the incomplete import inventory; after reviewing the dormant import, the test
inventory was corrected without changing retained source or allowing that import.
Independent review found no remaining blocking issue and separately passed
the checker suite, **14/14** initial preparation/refusal cases and the **2/2**
added failure cases. These overlap the final combined suite and are not added
to its total. No full historical suite, remote CI or hardware test was run.

Raw final log: `private/sessions/20261022-runtime-preparation/qualification-01.log`,
SHA-256 `b75e45793f3ace33551bac0ae755f73f3c96776d622d0cbdd805bda4a1af5da6`.
The private directory also retains the runner, qualification receipt, progress
updater, before-images and final verification. Focused integration logs remain
in `private/sessions/20261022-synthetic-runtime-preparation/`.
An export lacking the private authored checker explicitly skips the retained
checker class and the integration case requiring it; a changed checker fails
its identity pin. This is a reproducibility prerequisite, not a feature pass.

## Scope deviation and preserved state

An initial source-location search was broader than intended: it searched private
Python text for checker names, excluding `constants.py`, `source-*.py` and
`selected-*.py`, and returned filenames only. It did not search binary firmware,
native payloads or raw-prefix files. Those filename exclusions cannot prove that
no differently named constants text was opened. Further private source inspection
was restricted to the exact authored checker. All test inputs were invented.

No upstream launcher/service tool, firmware program, installed crypto runtime,
camera operation, private upload or external request occurred. No legal inquiry
or owner question was made. Historical frozen operation records and reference
source locks were not edited. Public and private feature progress now agree on
the next technical work; the stale internal FTP next step requesting camera
inventory has been corrected. Camera contact remains on explicit hold, including
Windows PnP inventory. English/FTP feasibility, exact-body correspondence and
rollback/recovery remain unvalidated. FL2/FL3 stay deferred.

## Reviewed files and completion

Public changes: the launcher and two tests listed above; this report;
`research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`,
`research/PRE_CAMERA_GAP_AUDIT.md`, `research/ANALYSIS_PREREQUISITES.md`,
`research/PRE_CONTACT_DECISION.md`; `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`
and `docs/FEATURE_PROGRESS.md`.
Ignored internal updates: `private/session-state.json`,
`private/feature-progress.json`, `private/feature-progress.md` and session
logs/scripts/receipts. Before-images preserve the previous notes.

After content review and synchronized-state verification, stage these named
public files only, check the staged paths/content, and commit locally:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-runtime-preparation/verify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-runtime-preparation/verify.py final-state
git add -- tools/dependency_operational_launcher.py tests/test_dependency_retained_context.py tests/test_dependency_preparation_context.py research/sessions/20261022-runtime-preparation.md research/STATE.json research/PRE_CAMERA_GAP_LEDGER.json research/PRE_CAMERA_GAP_AUDIT.md research/ANALYSIS_PREREQUISITES.md research/PRE_CONTACT_DECISION.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "feat: qualify synthetic runtime context preparation"
git status --short --branch
```

No push or external submission is part of this package.

Next single work package: **RA-003: qualify the source-owned full preflight to
current-context and retained control/helper ownership handoff using invented
callbacks, including failure cleanup and partial-result reconciliation. Reuse
the qualified command transport and checker; keep actual v6 execution refused
and camera contact on hold. English/native FTP stay first.**
