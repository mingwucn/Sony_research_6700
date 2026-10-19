# RA-003: shared internal controller continuation

2026-10-19. Branch codex/ra003-internal-continuation; starting HEAD 70ca363.
Evidence: static-inference, offline-tested. Camera commands: none.

The [internal continuation](../DEPENDENCY_INTERNAL_CONTINUATION.md) repairs the
specific callback gap identified in the operational delta. The bridge no longer
substitutes an observer wrapper: the producer owns a distinct continuation slot.
The runtime construction seam always constructs RuntimeOps internally; its public
dependency-only API has no observer/callback/continuation parameter. Public
controller runtime entry and CLI still refuse. Private authored functions are not
a Python sandbox, permission record or an approved operational entry.

Same-operation/context and AES ownership are checked before the factory and after
controller release. Factory handoff must complete once; caught failure/reentry is
sticky. Durable current raw receipts are rechecked before/after continuation.
Single-attempt record close/release, primary error retention, existing-folder
refusal and uncertain-publication behavior are retained. Ordinary observer vectors
are now preserved separately; bridge fixtures perform 72 simulated cipher comparisons.

Two independent source reviewers found and then accepted repairs for missing or
swallowed factory handoff, a runtime-mode-derived false observation claim on early
failure, and late context/operation mutation. Failure now reports incomplete or
unknown observation with completed=false; it does not claim a performed observation
from mode. Source review receipts and original findings remain private.

## Qualification and limits

- Full public host suite: **679 total, 676 passed, 3 skipped**, zero failures/errors, exit **0**, **270.649937s**.
- Real invented parent/child/controller suite: **18/18 passed**, zero skips/failures/errors, exit **0**, **246.067326s**. Both controller phases, one stream/record owner, dependency/bridge parent verification, setup interruption, changed receipts, source mismatch, terminal cleanup and bounded timeout/reaping are exercised by the retained fixture.
- Terminal fallback: **3/3 passed**, zero skips/failures/errors, exit **0**, **25.054357s**. Two stub-handle unknown-completion/cleanup-failure cases prohibit extra poll/kill/wait and retain known PID plus primary error; one additional real invented child success. Seven original fixture pins stable; derived test differs only in its exclusive folder label, with both byte hashes retained. No actual PID is acted upon in the stub cases.
- Both final runs retained **107** authored source pins unchanged; raw logs, source inventories, process dispositions and hashes remain private. The three full-suite platform skips are explicit limitations, not passes.
- Nominal runtime dispatch tests stop at a mocked engine; concrete observer construction is inspected without installed dependency activation. Actual crypto/native loaders are simulated. No actual firmware/constants, dependency installation, camera, upstream launchers or protected inputs accessed/uploaded.
- Historical seventeen blockers and exact-target/recovery limits remain. This is host composition qualification, not English/native FTP support, a runtime activation packet or a device-write gate.

## Exact commands and reconciled attempts

Interpreter for all qualifications: C:/ProgramData/miniconda3/python.exe,
CPython 3.13.12, Windows AMD64, flags `-I -S -B -X utf8`.

- `git status --short --branch`; staged/unstaged diff inspection; `git diff --check`; `git diff --cached --check`: pending operational-delta and owner-reference notes reconciled.
- `git add -- docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/STATE.json`; `git commit -m "docs: record operational delta and owner reference findings"`: exit 0, commit 70ca363, seven reviewed documentation/state files including already-staged reports. No private files staged.
- `git switch -c codex/ra003-internal-continuation`; `New-Item -ItemType Directory -Path private/sessions/20261019-RA-003-internal-continuation -ErrorAction Stop`: exit 0, exclusive evidence folder.
- Initial focused standard-library stdin harness: four discovery patterns test_dependency_controller.py, test_dependency_collected_child.py, test_dependency_execution.py, test_dependency_producer.py. **179 tests**, 0 failures, 0 errors, 0 skips, 169.660713s, command exit 0. Source stability **false** because review repairs occurred during this preliminary run; not accepted as final qualification.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-internal-continuation/qualify.py full`: preliminary exit 1, source stability False; crossed source/harness revisions, superseded by the final frozen run, not accepted.
- Same interpreter/script with `outer`: exit 1, **18 fixture refusals**, no child launched by the driver. Harness placed fixtures outside the retained driver's confined root; its existing guard correctly refused. Preserved original script as qualify.initial.py and logs/results. Corrected only placement under the permitted invented-fixture root and added exclusive run labels; did not weaken the guard or change acceptance thresholds.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-internal-continuation/qualify.py full final`: accepted final results above, exit 0. Full standard-library public test discovery.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-internal-continuation/qualify.py outer final`: accepted final results above, exit 0. Retained test_outer.py with fresh confined invented fixtures; existing folders never reused.
- Host-authored stdin script exclusively derives private/sessions/20261019-RA-003-clean-outer-child/test_parent_continuation.py from test_parent_fallback.py with only its fixture folder label changed; preserved source/derived hashes in fallback-derivation.json. `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-clean-outer-child/test_parent_continuation.py`: 3/3 terminal fallback checks above, exit 0.
- CLI refusal: `C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -c "import sys,runpy;sys.path.insert(0,'.');runpy.run_module('tools.dependency_controller',run_name='__main__')"`. Direct shell tool normalized the nonzero status to host 1; a host-authored bounded subprocess capture confirmed actual child exit **2**, empty stdout/stderr (cli-refusal.json), assertion wrapper exit0. No controller or dependency observer invoked.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-internal-continuation/record.py`: verify final source/review pins; update sanitized report, backlog, state and external/internal feature notes after exclusive original-byte backups.
- `git add -- tools/dependency_controller.py tools/dependency_execution.py tools/dependency_producer.py tests/test_dependency_controller.py tests/test_dependency_collected_child.py research/DEPENDENCY_INTERNAL_CONTINUATION.md research/sessions/20261019-RA-003-internal-continuation.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/STATE.json`; `git diff --cached --check`: exit0. Exact eleven staged paths reviewed; all107 final pins current; prior STATE values preserved except intended phase/current report and new entry; source lock unchanged.
- Final Git operations: `git commit -m "feat: qualify shared internal controller continuation"`; `git status --short --branch`; `git log -2 --oneline`. Commit identity and clean-status result are in the final Git output. No push or camera command.

Full log SHA-256: 037224865959a1d7fc0b2581d7b3800bc1db8aa65c73497ab41470a50ebc5b31.
Outer log SHA-256: 37a1a569eace7ba3b151156f28cf6c35400d57e2106a37cd4f32d4df5f4e0a5f.
Fallback log SHA-256: b219e0ece49c1c352f041b3ba0499a2c23803563265f560b2ac1c634aa528f44.

Public changes: tools/dependency_controller.py, tools/dependency_execution.py,
tools/dependency_producer.py, tests/test_dependency_controller.py,
tests/test_dependency_collected_child.py, research/DEPENDENCY_INTERNAL_CONTINUATION.md,
this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md and
research/STATE.json. Private session and feature notes updated with backups.
Source lock, old frozen entry/verifier and all earlier evidence remain unchanged.

Previous goal turn: no progress on the shared pre-camera path (reference refresh
only). Current turn: progress, concrete shared continuation implemented, repaired,
reviewed and qualified with invented inputs. Overall goal remains active.
English/native FTP first, FL2/FL3 deferred, custom looks separately gated and optional
bridge host-assisted. Exact build, feature resources/backend and rollback remain unproved.

Next single work package: **RA-003: migrate the frozen operational parent/wiring to the current collected-controller contract using invented inputs only; derive the exact successor source closure, verify all eleven dependency artifacts and both bridge envelopes, retain ordinary-only parent loading and single-owner cleanup, and qualify refusal/unknown-completion reconciliation. Keep runtime entry disabled; no dependency activation, firmware/constants reads or camera.**
