# RA-003: late child-record reservation

2026-10-20. Topic branch `codex/ra003-late-record-reservation`.
Evidence: static-inference and offline-tested. Camera commands: **none**.

Previous goal turn was progress: requested reference check `a75cf6e` in a separate worktree. In this continuation the previously staged engine package was completed as commit `654f79b` after revalidating its four independently reviewed source/test hashes, staged contents and retained 243-case result/log. The reference worktree and its notes remain separate. The full pre-camera goal stays active.

Independent integration review found that the existing preparation creates the control needed for child record reservation, whereas the new engine expected records already reserved. The engine now calls preparation once, validates the complete prepared dependency packet and context using the checked adapter, then reserves child journals once through that prepared control. It accepts no caller-supplied records. Runtime dispatch repeats its own pure checks. Callback/helper/adapter/preparation cleanup remains independent and ordered.

The first implementation acquired the records before constructing their close wrapper. Review identified that a constructor interruption could lose the acquired owner. The repaired implementation allocates the strict proxy first, then acquires its handle, rejects an empty return, and skips record close when acquisition did not return a handle. The control owns partial reservation failure cleanup; the engine does not retry it. These are ordinary trusted Python lifetime guarantees, not process-crash recovery or a hostile-interpreter sandbox.

Qualification covers metadata interruption, source/request drift, invalid operation/dependency binding, reservation exception or empty return, wrapper-constructor interruption before reservation, post-acquisition dispatch interruption, callback failure/reentry/reclose, uncertain close and parent refusal/cleanup. Successful ordering is metadata → reservation → dispatch, with one preparation, one reservation and one record close. No actual record was reserved by the tests; the control and runtime/saved dispatch are intercepted and inputs invented. The real RuntimeOps constructor is blocked throughout suite loading/execution.

## Exact commands and results

```powershell
git diff --cached --check
git diff --cached --stat
# Read retained review.txt and source/test diff; revalidate four hashes and final log/result.
git commit -m "feat: compose disabled operational engines with owned cleanup"
git status --short --branch
git switch -c codex/ra003-late-record-reservation
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-late-record-reservation -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-RA-003-operational-entry/qualify.py -Destination private/sessions/20261020-RA-003-late-record-reservation/qualify.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-late-record-reservation/qualify.py initial-v1
Copy-Item -LiteralPath tools/dependency_operational_entry.py -Destination private/sessions/20261020-RA-003-late-record-reservation/entry-initial.py -ErrorAction Stop
Copy-Item -LiteralPath tests/test_dependency_operational_entry.py -Destination private/sessions/20261020-RA-003-late-record-reservation/tests-initial.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-late-record-reservation/qualify.py repaired-v1
```

All above commands exit 0. Initial 87/87 focused cases passed before the independent acquisition finding; initial sources and logs are preserved and do not supersede that finding. Final **90/90 tests pass**, zero failures/errors/skips, exit **0**, **48.215046s**, six source pins stable. Interpreter: CPython 3.13.12 Windows AMD64, `C:/ProgramData/miniconda3/python.exe`, isolated/no-site/no-bytecode and optimize 0. Final raw log SHA-256: `a5c4ee0c74aa8ccd881e30a85445cf688969e45006653483cca32f56d94a539c`.

Five focused modules: test_dependency_operational_entry, test_dependency_successor_sources, test_dependency_adapter_binding, test_dependency_successor_wiring and test_dependency_host_launcher. Shared helper/launcher sources are unchanged; the only production delta is the separate disabled engine, whose source callers are its tests. The 16 historical full invented-process cases were not rerun for this private engine-only change. The prior 243-case result is historical, not qualification of this new ordering. No installed/native dependency activation or actual firmware/constants/saved raw input reads occurred.

Ordinary source inspection used Get-Content and rg. Exploratory reads of three absent guessed source filenames returned exit 1; `rg --files` located the authored host child, detached metadata loader and retained control instead. No executing operation was lost or restarted. Review was local/source-only under the owner's existing authorization. No network, downloads/uploads, upstream execution or camera contact occurred in this continuation.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-late-record-reservation/record.py
git diff --check
git add -- tools/dependency_operational_entry.py tests/test_dependency_operational_entry.py research/DISABLED_OPERATIONAL_ENGINE.md research/sessions/20261020-RA-003-late-record-reservation.md research/STATE.json research/PRE_CAMERA_READINESS.md docs/BACKLOG.md docs/FEATURE_PROGRESS.md docs/CODEX_HANDOFF.md
git diff --cached --check
git diff --cached --stat
git diff --cached -- tools/dependency_operational_entry.py tests/test_dependency_operational_entry.py research/STATE.json
git commit -m "fix: reserve child records after prepared control binding"
git status --short --branch
```

Changed public files: engine source and test, engine assessment, this report, STATE, pre-camera ledger, backlog, feature progress and handoff. Existing public/private notes were backed up before updating private/session-state.json and both private feature notes. Frozen scope, source lock, inherited records and prior evidence remain unchanged. English/native FTP stay first; FL2/FL3 remains deferred. No feature, recovery or device-write gate passed.

Remaining prerequisites: separately source-owned outer preparation and saved-result verification; operational ordinary/preflight/result semantics; OS-derived parent supervision facts; the five activity-specific decisions and fresh in-act dependency provenance. Exact-body correspondence and usable rollback remain unproved for later camera work. Existing invented checks remain invented-only; matching source bytes do not authenticate permission or observations.

Next single work package: **RA-003: bind the disabled operational engine composition into a separately source-owned outer parent/child preparation and saved-result path. Derive its exact source map and operational ordinary/preflight/result contracts, preserving frozen supervision and observation limits. Reserve child journals through the prepared control only once; collect child completion evidence before engine-owned teardown and derive parent process facts through the owned supervisor. Qualify with invented records and intercepted runtime calls only; independently review before actual record assembly or activation. Keep five decisions pending; no installed dependency activation, firmware/constants/native payload reads, downloads/uploads or camera contact.**
