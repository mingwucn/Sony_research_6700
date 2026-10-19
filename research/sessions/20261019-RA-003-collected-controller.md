# RA-003: collected dependency/controller composition

2026-10-19. Branch `codex/ra003-controller-qualification`, starting HEAD `8464ae3`.
Starting tracked tree clean, with inherited untracked bridge and unit-test files.
This package completes and qualifies those files; it does not discard prior work.
Evidence: **offline-tested**, **static-inference**. Camera commands: **none**.

## Outcome and boundary

The [design](../DEPENDENCY_CONTROLLER_COMPOSITION.md) reconciles the current
collector/producer with the real authored GDT controller, callback factory and
runner. The immutable factory receipt references the newly published producer raw
bytes and callback-claim journal. The same AES owner/native guard remains live
through both controller phases, cleanup and final public-vector checks. Operation
IDs are checked against the captured policy; controller and summary exit codes
require exact integers. Reserved records close at most once across interruption;
uncertain publication is never retried. Primary failure survives cleanup failure.

There is only an invented API; RuntimeOps is rejected before collection, and the
CLI returns 2. Neither source review nor callback/hash inputs authorize execution.
The private integration uses newly invented read-only stream/constants and a
modeled identity cipher for its non-public invented keys. Native loading is
simulated. Four cases use the actual authored factory/controller/source-role
loader/runner: success, second-phase read failure, factory interruption and a
caught forbidden load. Success performs two stream opens/two closes/four cipher
constructions; each case attempts record close and callback release exactly once.

Temporary tools-namespace isolation is an explicit fixture accommodation. It is
not a production clean bootstrap or a qualification of the actual parent/child
chain. Old dependency-config/cache validation is only source-graph setup, never
fresh dependency evidence or execution authority. No actual installed dependency,
firmware, operational constants, native payload, camera or protected continuation
was accessed this turn. No new upstream source was acquired or executed.

## Reviews and qualification

Two existing owner-authorized reviewers accepted the final authored sources.
Resolved findings: boolean/float summary acceptance, mutable cross-operation
substitution, completion-publication retry after uncertain outcome, record leaks
on BaseException, and interruption during output construction after reservation.
The last repair moves ownership/state/class setup before directory reservation
and output construction inside the cleanup boundary, with its own regression.
No test threshold was relaxed. Review source hashes and saved-output hashes are
retained privately and in the new STATE record.

- Focused: **24/24 passed**, zero skips/failures/errors, exit 0,
  **82.79413829999976s** wrapper; 20 bridge cases + four real-controller
  integration cases on invented data. All **103** authored Python pins unchanged.
- Full public host: **639 cases**, **636 passed**,
  **3 platform skips**, no failures/errors, exit 0,
  **234.2584512999747s** wrapper; same103 pins unchanged.
- Saved focused log and result independently reviewed: 24 unique passes and four
  case metrics consistent; no actual input paths followed or execution repeated.
- Saved full-suite result/log independently reviewed: 639 cases, 636 passes and
  three platform skips consistent; no replay or actual input access.
- Full suite is ordinary authored host regression, not the historical private
  frozen gate suite, actual dependency activation or physical-camera validation.

Source SHA-256:

- Bridge: `c19bfec63559028f07eed52a1eb18c808b25346bff5c995cb4fbf8e281e7836c`
- Unit tests: `90a7890546ed76558f8378a24e5f3a8b7a89c7ce9c03d1e6e6860054ace50557`
- Focused log: `877c214e2a5566aadbc027baa94d39c86b5a04de94fe10cd10c941b33a1fdc7f`
- Full log: `1793e76a2722b130720a9b9ce6655cee8b7d1da4aeee1b751ccd4e722b7a8fb6`

## Exact host commands and results

Interpreter for all Python commands: `C:/ProgramData/miniconda3/python.exe`,
CPython 3.13.12, Anaconda MSC v1942 64-bit Windows AMD64. Isolated startup flags
`-I -S -B -X utf8`; no environment/dependency/driver changes.

- `git status --short --branch`: branch `codex/a6700-reference-check-20261019c`,
  the two inherited untracked bridge/test files; tracked tree clean.
- `git switch -c codex/ra003-controller-qualification`: exit 0.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-collected-controller/test_composition.py`:
  first current-turn setup attempt exit 1, four alias-occupied errors (4.905s);
  moved fake ctypes setup after source planning. Second exit 1, four missing
  actual-started marker errors (6.326s); added the real invented parent-record
  reservation/close before child reservation. Third exit 0, **4/4 passed**
  (50.764s). Earlier inherited setup attempt failed at lab.make's tools namespace
  guard; preserved as history. None reached actual inputs or native execution.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests',pattern='test_dependency_controller.py'));raise SystemExit(not r.wasSuccessful())"`:
  exit 0, initial repaired **19/19 passed** (31.833s), before the final
  constructor-interruption regression was added. Not the final qualification.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-collected-controller/qualify.py focused`:
  exit 0, final24-case qualification above; exclusive `qualification-focused-a`
  folder, retained raw log/result and case metrics.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-collected-controller/qualify.py full`:
  exit 0, final full regression above; exclusive `qualification-full-a` folder.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-collected-controller/record.py`:
  writes these notes and state only; preserves unrelated state values and backs
  up original private notes exclusively. Exit 0.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import runpy,sys;sys.path.insert(0,'.');runpy.run_module('tools.dependency_controller',run_name='__main__')"`:
  intentional Python exit **2**, no output or activation. Initial PowerShell
  invocation surfaced shell status1; explicit `$controllerExit = $LASTEXITCODE`,
  `Write-Output "python_exit=$controllerExit"`, `exit $controllerExit` confirmed
  Python and explicit shell exit2. This is authored-entry refusal, not an upstream
  launcher or controller observation.
- `git add -- tools/dependency_controller.py tests/test_dependency_controller.py research/DEPENDENCY_CONTROLLER_COMPOSITION.md research/DEPENDENCY_COLLECTED_RUNTIME.md research/sessions/20261019-RA-003-collected-controller.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/STATE.json`: exit 0.
- `git diff --cached --check`: exit 0. Nine explicit staged paths/content reviewed;
  staged bridge/test hashes match qualification; unrelated prior STATE values
  preserved; no private files staged. No push, upstream launcher, service tool
  or camera command.

One optional source search used an incorrect ordinary authored binding path and
returned file-not-found; the actual activation/activation_binding.py was then
read. Initial test failures were fixture errors, not accepted operational results.

Changed public files: tools/dependency_controller.py,
tests/test_dependency_controller.py, research/DEPENDENCY_CONTROLLER_COMPOSITION.md,
research/DEPENDENCY_COLLECTED_RUNTIME.md, this report, docs/BACKLOG.md,
docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md and research/STATE.json. Private
fixture, qualification/review records and session/feature notes remain ignored.
All historical actual-result and source-lock records remain unchanged. Previous
goal turn was an external-source refresh without shared-path progress; this turn
advances the shared pre-camera dependency/controller integration.

## Unresolved prerequisites and next single package

The operational source closure, clean namespace/bootstrap, independent parent
verification of the new composition and scoped protected activation preparation
remain pending. Parent/mapped-native/transitive authentication and the historical
seventeen blockers are not cleared. Exact body/build identity, English resource
and policy mapping, native FTP backend/transport evidence, backup coverage and
recovery/rollback remain unproved. English/native FTP first; FL2/FL3 deferred.
No feature is marked supported and no recovery/device-write gate passed.

**RA-003: implement and qualify the invented-only exact-buffer outer child with one declared source closure, namespace ownership planned before activation, the current collected dependency contract held through the real controller, and independent parent verification of dependency/controller/close/release results; exercise stop and unknown-completion reconciliation and obtain source review before any protected-input activation preparation. No actual dependency activation, firmware/constants reads or camera.**
