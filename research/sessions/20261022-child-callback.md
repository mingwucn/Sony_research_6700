# RA-003: synthetic runtime checker and child preparation integration

2026-10-22. Evidence: **static-inference**, **offline-tested**. English and native
camera-to-server Wi-Fi FTP remain first. FL2/FL3 and calibrated looks remain
deferred; a bridge remains an optional host-assisted result. Camera commands:
**none**. No new legal questions or research.

## Result and limits

The genuine child preparation/callback and collected-result path now joins the
parent using synthetic inputs without precomputed terminal replay. The positive
case reaches `consistent_pending_composition` and `consistent_saved_controller`.
Seven new cases pass, comprising six single child launches and one prelaunch
refusal; 113 unchanged regression cases also pass. These are host-side integration
results, not evidence of English menus, native FTP or actual firmware runtime.

The isolated child executes genuine `Preparation.prepare`, the exact retained
`ScopedCallbacks` factory, genuine runner/gates/classifier, controller, collector
and producer around explicitly invented I/O and dependency operations. The
successful path begins with no terminal, dependency, bridge or outer-child
outputs; the child generates them afresh. Two collision cases deliberately
introduce an existing output at different reservation boundaries. No saved basis
or terminal result is replayed by the new child path.

The captured synthetic `IoAdapter` replaces the original I/O adapter and never
retains or calls the protected preparation closure or supplied I/O operations.
Its logical data, source events, digest claims and event-derived snapshot are
invented. The zero protected/I/O call fields are source-traced declarations,
not instrumentation of actual protected inputs or OS I/O. The real factory
therefore runs, but actual I/O and protected preparation remain unexecuted.

Separate captured wiring overrides route the genuine dependency/controller
algorithms through `FakeOps`, inert package contents/public vectors and the
`invented=True` record grammar. Original runtime dispatch/producer routing and
`RuntimeOps` do not execute; the captured original prefix and startup checks do.
Runtime verification, producer authentication and operational acceptance
remain false. The child's PID, isolation flags, refresh receipts, output writes
and owner closure are observed synthetic process facts. They do not establish
any camera behavior. [Layer-by-layer boundaries](../CHILD_CALLBACK_INTEGRATION.md).

The new tests cover interrupted adapter preparation, fresh ordinary-source drift,
preserved output collisions before parent launch and after parent reservation,
interrupted callback release completion, and coherently rehashed collected raw
data after narrow terminal success. Refusals remain `needs_review`, with no
automatic process retry. Narrow zero-exit/terminal success cannot override full
saved-result validation. Callback leases, child/parent owners, modules and pipes
close in the observed cases.

Two independent read-only source reviews found no blocking issue. Scope remains
trusted test composition; pinned/stat-checked ordinary sources do not establish
hostile-filesystem/import isolation. An audit allowing the standard-library
prefix alone would not exclude installed-package paths; captured source maps
and inert operations define that boundary. Cleanup-fault coverage is not
exhaustive, including the preceding helper's untested ownership-capture exception.

All 16 frozen ordinary records, five historical pending dispositions and three
dependency nulls remain unchanged. Production tools and v6/public runtime
refusals remain unchanged. No actual executable bundle or source migration was
created. No actual firmware, constants, raw-prefix or native payload was read;
no installed dependency, upstream launcher/service, camera, network, download,
upload, driver or firmware action occurred.

## Exact commands and results

Working directory: `D:/LocalWork/Sony_research_6700`; PowerShell 7.6.5.
Interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython 3.13.12.
The standard-library runner uses `-I -S -B -X utf8`. Logs, observations, source
pins and before-images stay in the ignored private session folder.

| Exact command | Exit | Result |
|---|---|---|
| `git status --short --branch` | 0 | Clean baseline on `codex/ra003-terminal-validation-20261022` |
| `git switch -c codex/ra003-child-callback-20261022` | 0 | Topic branch from `755214896d2323ce7f87574b51e692f9a00ec231` |
| `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/setup.py` | 0 | Exclusive session setup |
| `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/snapshot.py` | 0 | Eleven note before-images and production function AST pins |
| `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/qualify.py smoke-01` | 1 | 1 failed positive case; 10.027 s; classifier-lineage fixture mismatch |
| `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/preserve_smoke.py` | 0 | Five smoke source before-images preserved |
| `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/qualify.py smoke-02` | 0 | 1/1 positive case; 29.955 s |
| `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/qualify.py focused-01` | 1 | 6 cases: 4 passed, 1 failure, 1 error; 104.927 s; incorrect collision/interruption test expectations |
| `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/qualify.py regression-01` | 0 | 113/113 regressions; 354.974 s |
| `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/qualify.py focused-02` | 0 | Corrected complete seven-case module, 7/7; 104.623 s |

Initial smoke failure: the old fixture lineage used an always-opaque classifier,
while the genuine callback factory supplied a classifier recognizing the invented
tar prefix. Parent and child fixture builders now regenerate the complete
invented lineage consistently with the genuine classifier. The classifier and
all acceptance predicates remain unchanged.

Initial focused issues: a pre-existing child output correctly stopped the parent
before spawning, contrary to the test expectation; `KeyboardInterrupt` correctly
propagated before a controller-result file existed, contrary to another test
expectation. The failing source was preserved before correcting only the root
test and adding a distinct child-reservation collision case. The seven-case
module was rerun completely. No production subject change or threshold
relaxation was required.

Final effective qualification: **120 distinct cases passed**, zero failures,
errors or skips in the final selections. Preliminary/failed runs are preserved
and are not counted again. Both final runs retained **91 stable source pins**
within each run. The only difference between those runs is the corrected root
test, which was pinned but not imported or selected in the 113-case regression
run; all 90 other source pins are identical. This supports reusing those
regression results without relabeling them as a rerun after the test-only edit.
The original 72 ordinary draft pins were also rechecked.

The regression selects `test_dependency_preparation_migration`,
`test_dependency_joined_handoff`, `test_dependency_saved_handoff`,
`test_dependency_parent_handoff`, `test_dependency_isolated_handoff`,
`test_dependency_operational_preparation`, `test_dependency_operational_launcher`,
`test_dependency_migration_transport`, `test_dependency_terminal_join` and
`test_dependency_parent_loader`. It includes the earlier replay tests; the
private runner's common `terminal_replay=false` summary field describes the
new package path, not every regression case. Per-case observations preserve
the distinction. New cases are in `test_dependency_child_callbacks`.

| Retained log | SHA-256 |
|---|---|
| Initial smoke | `e6560adb00c559993bb714c9ffbd497444a99355f877eba2d82d147d732cb19f` |
| Positive smoke | `090713cecfad7f36ba630f14fa09cee4fcb83f3b33c9ae40748f858d5c89806f` |
| Initial focused | `155cce984324ee9b560a729fca75996b43d18e6acce1199cb0daba31ac211a31` |
| Corrected focused | `108ff4238b935ee3453e58c580571c510b167c1ba7b05a97b54fbae49c8337db` |
| Regression | `ca6ed76b9165ab84948d5766cb3391593e5a879741fec6174f3d5a7b0c68152b` |

## Changed files and review

- `tests/dependency_child_fixture.py`: captured synthetic I/O role with fresh child-side logical generation.
- `tests/dependency_child_runtime_fixture.py`: separate invented wiring, dependency operations and saved verifier.
- `tests/test_dependency_child_callbacks.py`: seven preparation/callback/collection/parent cases.
- `tests/dependency_terminal_fixture.py`: opt-in genuine-classifier fixture lineage; default unchanged.
- `tests/test_dependency_preparation_migration.py`, `tests/test_dependency_joined_handoff.py`: opt-in captured wiring inputs.
- `research/CHILD_CALLBACK_INTEGRATION.md`, `research/sessions/20261022-child-callback.md`: boundaries and this report.
- `research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`: structured progress.
- `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`: current handoff and feature priorities.
- `research/PRE_CAMERA_GAP_AUDIT.md`, `research/ANALYSIS_PREREQUISITES.md`, `research/PRE_CONTACT_DECISION.md`: current gaps and next package.

Ignored internal notes: `private/session-state.json`, `private/feature-progress.json`
and `private/feature-progress.md`. Before-images and execution/review/Git receipts
remain private. Exactly these sixteen public files enter the local commit;
no push or external submission.

Local completion commands, recorded with exit zero on completion:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/record.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/verify.py
git diff --check
git add -- tests/dependency_terminal_fixture.py tests/dependency_child_fixture.py tests/dependency_child_runtime_fixture.py tests/test_dependency_child_callbacks.py tests/test_dependency_preparation_migration.py tests/test_dependency_joined_handoff.py research/CHILD_CALLBACK_INTEGRATION.md research/sessions/20261022-child-callback.md research/STATE.json research/PRE_CAMERA_GAP_LEDGER.json docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/PRE_CAMERA_GAP_AUDIT.md research/ANALYSIS_PREREQUISITES.md research/PRE_CONTACT_DECISION.md
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/staged_review.py
git diff --cached --check
git commit -m "test: join synthetic child preparation and callback collection"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-child-callback/complete.py
```

Private receipts bind exact reviewed file hashes, staged blobs, commit parent,
clean working tree and preserved camera/feature/recovery boundaries.

## Remaining prerequisites and next single package

The retained I/O adapter and protected-preparation boundary remain replaced.
Actual current bindings, installed dependencies/runtime, GDT/content, body
correspondence, English resources/policy, native FTP backend and practical
recovery remain unqualified. The five historical pending dispositions and three
dependency nulls remain recorded; they are not new intake questions. The full
pre-contact goal remains active and incomplete. No owner input is required for
the next synthetic package, and camera contact remains on hold.

Next single package: **RA-003: qualify the retained I/O adapter and
protected-preparation callback boundary using exclusively invented physical
source envelopes, constants and protected-role test doubles through the current
child/parent path.** Keep genuine classifier and acceptance predicates, actual
runtime refusals, frozen records, five historical pending dispositions and
dependency nulls. No actual protected inputs, installed-dependency activation
or camera contact. English/native FTP stay first.

No feature supported, recovery proven, runtime authorized or device-write gate
passed. Camera commands: **none**.
