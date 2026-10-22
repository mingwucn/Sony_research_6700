# RA-003: isolated current-context preparation handoff

2026-10-22. Branch `codex/ra003-isolated-current-handoff-20261022`, baseline
`19d4c88a996ab2f4b253f84e321740b4652ed864`. Evidence: **static-inference**, **offline-tested**.
Previous goal turn: **progress**, finite current-binding audit and repair.
This turn: **progress**, a source-owned child preparation seam and fresh isolated
synthetic handoff. The overall pre-camera goal remains active/incomplete.

Native English and native camera-to-server Wi-Fi FTP remain first. FL2/FL3
is deferred; calibrated looks and optional host-assisted bridge remain separate.
**Camera commands: none.** No feature, recovery, actual runtime or device-write
gate passed. No new owner facts or legal questions are required.

## Implementation and observed boundary

`tools/dependency_operational_child.py` adds `prepare_synthetic_owned`, parallel
to the existing host synthetic preparation. It checks startup/49-role roster,
canonical original request bytes, detached metadata, source-owned adapter
projection, full v6 gate/pending preflight and all 29 retained byte/size/hash/path
bindings. It constructs the current context before acquiring genuine child
helpers, then returns an unstarted `Preparation` and explicit owner handoff.
Failure closes acquired owners. It neither launches a process nor dispatches
runtime. Exact bootstrap, captured source receipts, saved bytes and observed
argv remain caller preconditions, rather than claims authenticated by this API.

The **unchanged** bootstrap ran with `-I -S -B -X utf8`, observed runtime profile
and actual argv. The successful subprocess transported exact current child
source **plus a separately pinned test-only suffix** that calls this new
synthetic seam. This is not successful execution of the unchanged production
child entry. No production request selector or bootstrap byte was added.

The new fixture in `tests/test_dependency_isolated_handoff.py` replaces the old
in-memory source registry with an invented disk reader. Tiny optional fixture
hooks in `test_dependency_preparation_migration.py` and
`test_dependency_joined_handoff.py` leave their default behavior unchanged.
All target/input metadata and data fixtures are invented; source locations are
temporary. Captured authored modules are real except the explicitly identified
test substitutions. Retained checker/control bytes are unchanged and pinned. The v6 gate
algorithm is real; its ancestry/evidence policy is regenerated for the invented
records. No actual frozen candidate or private firmware metadata is used as an
executable input.

| Requirement | Observed evidence and limit |
|---|---|
| Fresh startup | Separate PID; isolated/no-site/no-user-site/no-bytecode, optimization zero; no `tools`, ctypes or third-party crypto/native dependency aliases at entry. Interpreter/stdlib remain trusted, not attested. |
| Source and metadata ownership | Exact 49-role capture and 46-role prepared projection, full source-owned v6 gate/pending preflight; no predicate mocks. The test suffix is separately identified. |
| Current context | Parent and fresh child produce the same complete context hash; unchanged retained control accepts its ordinary bindings and parent marker. |
| Actual preparation refresh | Exactly **29 successful temporary disk reads**, each with expected path/hash/size. Dedicated audit events occur only inside the invented reader after its own successful read; later context-checker opens cannot supply these receipts. |
| Ownership and reservations | Genuine `HelperSources`, unchanged retained control, exclusive parent/child records and callback lease participate. Parent handles remain open while child works. Forwarded `Path.open` instrumentation observes child/partial reservation handles closed **before** the child receipt/exit. |
| Final runtime boundary | Callback factory, dispatch and collection are explicitly inert test implementations. Genuine controller/collector, installed dependencies and observer are not invoked. Parent uses standard `subprocess.run`, not the retained supervisor/reconciliation chain. |
| Negative cases | Saved source/packet drift, observed-profile mismatch, rehashed operation/ordinary-metadata mismatch, post-transport retained-source drift, partial child-reservation collision, dispatch/callback interruption, incomplete return and callback-close failure refuse and preserve the relevant evidence. Cleanup is attempted once; no automatic retry. |
| Production refusal | The unappended production child refuses before child records. Its generic bootstrap result alone does not identify why. A separately pinned diagnostic suffix calls the unchanged child function and records exact `operational_process_v6_execution_pending`. Direct CLI/public refusals remain covered by the regression suite. |

Production `child`, `refuse_v6_execution`, child `run_runtime`, parent
`_prepare_pending`, parent `bootstrap` and parent `run_runtime` are AST-identical
to baseline. Their line positions changed; behavior was not relaxed. Actual
parent/child paths still use the historical constructor after their deliberate
v6 refusal. Source/gate/record migration and actual-runtime readiness remain
incomplete. This package closes the combined **synthetic** startup/context/
preparation/control/helper handoff gap only.

Source identities for the accepted synthetic success:

- Exact authored child prefix: `58b6d62fc66cdb68ce45d8c67e05de8ea50c75b4c43fa489aac2ab5a88a047b6`.
- Test-only appended adapter: `8eed0ae2c82334256dee93b76197528d28c40452ea8899be5970fa684c9b98f8`.
- Transported combined child: `3958017961ecccb79cb2ac338103d7c4762635eeeca812046515ca8b3ad444af`.
- Unchanged bootstrap: `9fc839f17e6c2ff316b88421af3d0d0719838d83a6113b65fdfcdc2743c99c86`.

## Failures, correction and qualification

Three early one-case smoke attempts failed: two test-suffix literal/syntax
errors, then a bare assertion in the invented disk reader. The fourth smoke
passed after diagnostic assertion messages were added; this was insufficient
qualification. The first full focused run then recorded **9 cases and six
failure entries** (four subtest failures plus two individual case failures),
all early stops at the invented reader's cross-API identity predicate.

A separate probe created/read **100 invented disposable files** and preserved
five `lstat`/`fstat` ctime-only mismatches. Each API's before/after stamps remained
stable and cross-API device/inode/size/mtime agreed. The fixture predicate was
therefore explicitly corrected to match the existing authored reader's
structure: full same-API stability, cross-API device/inode/size/mtime, and exact
size/SHA-256. This justified fixture correction is recorded after the failure;
no production guard or feature acceptance threshold was weakened. Raw failed
logs, the diagnostic-bootstrap-only traceback and timestamp observations remain
private. No automatic retry or protected/device action occurred.

Independent static review also required dedicated preparation-read receipts,
before-exit handle observations and a separate exact-reason diagnostic. Those
assertions were added before final qualification.

Focused corrected run: **10/10 passed**, zero failures/errors/skips, exit **0**,
**53.029s** runner, **15 new child observations**.
It overlaps the final suite and is not added to its count.

Final qualification: **205 cases: 204 passed, 1 skipped**,
zero failures/errors, exit **0**, **223.835s** unittest /
**224.419s** runner. The single skip is the existing Windows
symlink privilege error 1314; no elevation or system change. All
**38 source/test pins** stayed unchanged through the final
run, including the exact private authored retained control. This focused suite
is not whole-repository CI, pristine-host proof, real firmware analysis or
target runtime/feature/recovery validation.

## Exact commands and results

Host: Windows, PowerShell 7.6.5, CPython **3.13.12** at
`C:/ProgramData/miniconda3/python.exe`. Baseline working tree was clean.

```powershell
git status --short --branch
git switch -c codex/ra003-isolated-current-handoff-20261022
New-Item -ItemType Directory -Path private/sessions/20261022-isolated-current-handoff -ErrorAction Stop | Out-Null
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-isolated-current-handoff/snapshot.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-isolated-current-handoff/qualify.py focused
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-isolated-current-handoff/qualify.py focused 02
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-isolated-current-handoff/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-isolated-current-handoff/write_report.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-isolated-current-handoff/record.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-isolated-current-handoff/verify.py
git diff --check
```

First focused command exit **1** as described; corrected focused/final commands
exit **0**. Snapshot, report/progress recording and final preservation checks
exit **0**. The smoke and diagnostic stdin scripts and outputs remain in the
private session/tool trace; their final accepted replacement is the explicit
runner above. No failed raw evidence is deleted or overwritten.

Final runner explicitly loads these modules, adding repository/tests paths;
there is no broad discovery:

```text
test_dependency_isolated_handoff
test_dependency_joined_handoff
test_dependency_current_context
test_dependency_retained_context
test_dependency_preparation_context
test_dependency_host_entry
test_dependency_migration_transport
test_dependency_operational_launcher
test_dependency_preparation_migration
test_dependency_operational_preparation
test_dependency_operational_entry
test_dependency_observation_contract
test_dependency_observation_launcher
```

Final log: `private/sessions/20261022-isolated-current-handoff/qualification-01.log`,
SHA-256 `8a820811c00affb1e023ecdca58445c6e53d777acee6609d8220e914b81305b3`. Raw child observations,
source identities, failure history, before-images, static guard comparison,
working/staged review and completion receipts are private.

```powershell
git add -- tools/dependency_operational_child.py tests/test_dependency_isolated_handoff.py tests/test_dependency_joined_handoff.py tests/test_dependency_preparation_migration.py research/sessions/20261022-isolated-current-handoff.md research/STATE.json research/PRE_CAMERA_GAP_LEDGER.json research/PRE_CAMERA_GAP_AUDIT.md research/ANALYSIS_PREREQUISITES.md research/PRE_CONTACT_DECISION.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-isolated-current-handoff/verify.py final-state
git commit -m "feat: qualify isolated synthetic current-context handoff"
git status --short --branch
```

Only reviewed named files are staged. Local commit only; no push or external
submission. Commit identity and clean-tree verification are retained in the
private completion receipt and session response.

## Changed files and unresolved prerequisites

Public: `tools/dependency_operational_child.py`;
`tests/test_dependency_isolated_handoff.py`, `tests/test_dependency_joined_handoff.py`,
`tests/test_dependency_preparation_migration.py`; this report;
`research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`,
`research/PRE_CAMERA_GAP_AUDIT.md`, `research/ANALYSIS_PREREQUISITES.md`,
`research/PRE_CONTACT_DECISION.md`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`,
`docs/FEATURE_PROGRESS.md`. Ignored: session scripts/logs/receipts and internal
`private/session-state.json`, `private/feature-progress.json`,
`private/feature-progress.md`. Before-images are preserved.

Actual runtime remains **not ready**: exact-current source/gate/request records
are unmigrated, production v6 entry still refuses, and genuine parent supervision/
saved reconciliation is not part of this successful join. Actual dependency
freshness/activation and GDT/content observation remain absent. English resources/
locale consumers, resident FTP backend, exact-body correspondence, complete
backup/inverse and recovery remain unverified. The five historical pending
dispositions and three dependency nulls are preserved; they are not new owner
questions. No source-lock, firmware, constants, native payload or frozen actual
input was changed or processed. No network/download/upload, upstream launcher,
driver/firmware change or camera operation occurred. Legal questions stay stopped.

**Next single work package:** RA-003: prepare and independently review a
nonexecuting, pending-only migration draft for the existing GDT route's
exact-current ordinary source/gate/request bindings. Reuse the qualified
host/child context and retained contracts; preserve frozen records, five
historical pending dispositions and dependency nulls. Do not construct an
executable actual bundle, activate dependencies, read protected inputs or
contact the camera. English/native FTP stay first.
