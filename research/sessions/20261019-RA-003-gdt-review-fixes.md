# RA-003: isolated source review repairs

2026-10-19. Branch: `codex/ra003-gdt-review-fixes`. Evidence: **static-inference**, **offline-tested**.

Six scoped source issues are repaired in a new private revision and accepted by three source-only reviewers. The original 38 sources remain byte-identical. Operational binding migration and complete operational review remain pending; this is not activation authority.

| Finding | Repair and evidence |
|---|---|
| GR-001 (also RUNTIME-001) | Match dependency producer JSON encoding, including UTF-8 escaping and final LF; test producer-format receipts against the actual consumer. |
| GR-002 | Require the exact 162-case roster and source roster with nine fixed non-self source pins; refuse resealed downgrade, substituted IDs and changed fixtures. External seals remain necessary. |
| RUNTIME-002 | Track child record close ownership and uncertainty; close once across caught interruption and never retry an uncertain close. |
| IO-001 | Write inherited canonical bytes to binary stdout, require a full write and flush; exercise the inherited reconciliation byte comparison. |
| IO-002 | Return descriptor metadata with an empty root proposal; remove root-offset arithmetic and require this scope in the validator. |
| RUNTIME-003 (found during rereview) | Bound host interruption cleanup to one kill and one wait attempt, preserve unknown completion, and track parent record closure. Journal failure cannot consume the kill attempt. |

The 162 cases comprise 124 retained cases with necessary fixture/ownership updates and 38 new cases. Invented buffers, documents and inert child objects were used. Selected real function definitions were AST-extracted into test namespaces; protocol surroundings and factories were injected. These tests do not exercise the full saved-input/native operational composition. The reviewers inspected source/specification only and did not execute it. No new scoped blockers were identified; source-delta acceptance does not establish operational acceptance.

## Exact commands and results

Interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12. Each test run used the host-authored runner below, supervised by authored standard-library Python with stdin closed, captured output and a 60-second timeout. Raw logs, argv and source snapshots are retained privately.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 D:\LocalWork\Sony_research_6700\private\sessions\20261019-RA-003-gdt-review-fixes\outer\qualify_review.py
```

| Preserved run | Result | Exit | Suite seconds | Explanation |
|---|---|---|---|---|
| development-001 | 149 passes, one failure / 150 | 1 | 5.536 | An unrelated host close expectation was changed too early; corrected. Source inspection also caught and repaired an unintended validator key rename before the next run. |
| development-002 | 154/154 pass, zero skips | 0 | 3.298 | Original five repairs qualified. Rereview then found RUNTIME-003. Exact sources and reviews preserved. |
| development-003 | 160 passes, two errors / 162 | 1 | 3.405 | Two new fixtures omitted a required seal field; fixtures corrected without lowering thresholds. |
| development-004 | 162/162 pass, zero skips | 0 | 3.277 | Final wrapper 3.6534459000104107 seconds; all frozen sources stable. |

Final text/hash verification: 38 original pins unchanged, 41 current source/specification pins and 12 qualification pins matched. Forty Python files were syntax/AST checked. `git status --short` initially clean; `git branch --show-current` returned the topic branch above. No full historical suites were rerun for these isolated repairs.

## Changed files and limits

Private revised copies: `activation/gdt_gate.py`, `activation/ext_read_planner.py`, `activation/io_entry.py`, `outer/outer_gate.py`, `outer/entry_v2.py`, `outer/outer_fixtures.py`, `outer/test_outer_v2.py`, and `outer/scope.md`. New private tests/runner: `outer/test_review_fixes.py`, `outer/qualify_review.py`. Baseline, snapshots, failed runs, review records and final qualification stay in the ignored session directory. The copied historical runner was not run. No original source or historical review record was overwritten.

Sanitized public changes: this report, README, handoff, backlog, feature progress and research/STATE.json. Private state/feature notes receive additive entries. Only reviewed public paths are staged.

No firmware, operational constants, saved raw prefix or native payload read; no actual factory/entry activation, download, upstream execution, private upload or camera contact. Camera commands: **none**. English and native FTP remain first priorities; no feature, recovery or device-write gate passed.

Unresolved prerequisites: operational role/cache/reference migration and full composition review; exact-body/SKU/binary correspondence; English resource/restriction and native FTP backend evidence; proven recovery and separately approved device steps. The public a6700 Powerful FTP claim remains an author report, not our reproduction.

## Next single work package

RA-003: migrate and independently review the ordinary source-cache, role, reference and qualification chain to the repaired revision, with fresh bounded source receipts and invented host/child composition checks; no actual activation or GDT replay.
