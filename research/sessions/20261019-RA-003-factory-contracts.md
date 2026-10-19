# RA-003: authored callback factory contracts and cleanup repair

2026-10-19. Branch: `codex/ra003-factory-contracts`.
Evidence: **static-inference**, **offline-tested**. Previous goal turn: no progress toward the pending factory qualification (external-claim refresh only); this turn: progress.

## Outcome and scope

Exercised the actual authored `ScopedCallbacks`, `AuthoredSources`, constants AST parser and `gdt_wiring` functions with entirely invented role source buffers, constants, dependency receipts and controller/runtime adapters. No production role source, installed dependency backend, firmware, operational constants, saved raw prefix or native payload was executed/read by these tests. The suite shares one isolated/no-site child interpreter, with per-case teardown; it is not a separate process per test.

Initial 27 contracts passed. Two independent source reviewers found the same ownership-cleanup defect: an alias identity mismatch aborted the cleanup loop, leaving other owned aliases loaded while sticky closed prevented another attempt. New missing/replaced-alias regressions reproduced it. Cleanup in a new isolated factory revision now visits all owned aliases once, removes only identities it still owns, preserves foreign replacements and reports mismatches after the pass. Repeated close remains a no-op. No cleanup success is reported for mismatched ownership.

Corrected a test docstring that overstated subprocess isolation. No other production source changed. Both reviewers accepted the scoped repair after inspecting the corrected source and 29-test records; they did not execute tests. Full adapter/controller/runtime composition and operational acceptance remain false.

## Commands and results

Interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12, Windows AMD64.

- `git status --short`: exit 0, clean initial tree on `codex/ra003-source-overlay`.
- `git switch -c codex/ra003-factory-contracts`: exit 0.
- Copied the prior authored factory and wiring into a new ignored private session; originals preserved. Added authored invented-input tests and a 45-second subprocess supervisor. Four source/test/helper files have before/after hashes and retained snapshots for each run.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-factory-contracts/qualify.py development-001
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-factory-contracts/qualify.py development-002
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-factory-contracts/qualify.py development-003
```

| Run | Result | Exit | Suite seconds | Wrapper seconds |
|---|---|---|---|---|
| 001 | 27/27 passed, zero skips | 0 | 0.058 | 0.266829 |
| 002 | 29 run, 3 failures and 6 errors | 1 | 0.068 | 0.314756 |
| 003 | 29/29 passed, zero skips | 0 | 0.095 | 0.387254 |

Run 002 includes cascading alias-contamination errors after the first cleanup regression; all failed results/logs remain preserved. The same 29 tests passed after the factory repair. These tests cover delayed protected imports, source hashes, alias collisions, single claim/close behavior, AES identity checks, import interruption/path restoration, constants shape/hash/length/refusals, and wiring cleanup on controller success/failure. Historical suites were not rerun; their prior claims remain scoped to their exact bytes.

Host-authored preservation check: exit 0, all **42** prior source/specification pins unchanged; wiring byte-identical. Two source re-reviews accepted the repair. Exact child argv, case IDs, source hashes, stdout/stderr and review receipts remain private. Exploratory reads also encountered three nonexistent helper paths (PowerShell nonterminating read errors); these were corrected by file inventory and no qualification relied on them.

The qualifier has a 45-second child timeout; its captured stdout/stderr has no byte cap. This is a small authored synthetic suite, not an operational memory-bounded supervisor. Initial review artifacts span edits made during review; only the final source re-reviews bind the four-file successful revision consistently.

Camera commands: **none**. No download, upload, installation, driver/firmware change or device contact. Native English/FTP support, recovery and device-write gates remain false.

## Remaining prerequisites and next single package

The repaired factory is not yet integrated into the outer gate's pinned source chain. Actual production role modules and the real authored adapter/controller were substituted at test boundaries. No complete operational bundle, act, seal or real metadata replay was prepared. Invented receipts do not establish runtime dependency provenance.

**RA-003: compose the repaired callback factory with the real authored adapter and controller on invented byte streams, qualify that composition, and migrate/review its new source pin in the outer gate before preparing any real metadata act.**

English and native camera Wi-Fi FTP remain first; FL2/FL3 and calibrated custom looks remain deferred. Exact-body correspondence and demonstrated rollback remain unresolved device prerequisites.
