# RA-003: disabled observation launcher, partial qualification

2026-10-20. Branch `codex/ra003-observation-launcher-review`, base `a64916e`.
Evidence: **static-inference**, **offline-tested**.

Added the [disabled observation launcher](../OBSERVATION_LAUNCHER.md), its 18 invented-data tests, and a deterministic-bootstrap correction in the retained launcher. Actual preparation/full owned-engine qualification remains pending; this is progress within the original package, not completion of that requirement.

## Commands and results

```powershell
git status --short --branch
# a64916e; two pre-existing untracked launcher/test drafts, no tracked changes
git switch -c codex/ra003-observation-launcher-review
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path[:0]=['.','tests'];r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_observation_launcher'));raise SystemExit(not r.wasSuccessful())"
# Final exploratory: 18/18, zero failures/errors/skips, exit 0, 23.046s
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-observation-launcher/qualify.py
# Frozen final: 145/145, zero failures/errors/skips, exit 0;
# 66.884s suite / 67.404895s wrapper; 149 stable pins
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-observation-launcher/record.py
```

Interpreter: **CPython 3.13.12**, Anaconda Windows AMD64, `C:/ProgramData/miniconda3/python.exe`, isolated/no-site/no-bytecode. Final suite: 18 new launcher cases + unchanged 127-case selection (complete legacy gate, observation outer/contract, authority/input/scope and retained launcher). Driver preserves exact child argv, stdout/stderr, source snapshots, hashes and six CLI refusal results privately. It explicitly permits only the reviewed retained launcher delta among prior pins. These are invented record/source/ordinary-file tests; no installed crypto/native code, actual protected inputs or camera. Full repository/hardware suites not run for this scoped change.

Exploratory findings: fixed three adapter source origins in the inherited draft fixture; eight initial cases passed in 8.460s. Four review defects (canonical transport, roster-before-exec, preparation cleanup, publication disposition) received targeted regressions. A 13-case run failed one positive child in 14.691s; diagnostic singleton confirmed `operational_launch_bootstrap` caused by unordered set literals. Sorted literals fixed this without changing membership rules; singleton then passed (2.547s), expanded 14 passed (15.947s), expanded 18 passed (23.046s). One intermediate exploration lost its PTY handle in output formatting; its Python PID was checked absent before rerun, with no result claimed for that attempt. No production retry policy changed.

Independent reviewer accepted source hashes:

- observation launcher `193ef9c6b3dbe6b81f0deac288ac9b689213d2470b6e9db0227d4ecfbf437f07`
- retained launcher `25e854807853cc2ea180cffd498c8395b769a53927a713917c0bb817c64d15ba`
- tests `6b3c6585851308b3b0d86f1929eaa47cc29f9b5405463f1f6444ed874ad8b81a`

Review was source-only. Positive subprocess substitutes the engine child through an explicitly modified/bound test bootstrap; successful supervision/ownership unit cases substitute the controller, process and reconciliation. No production `prepare()` success or complete supervisor/engine qualification claim. Current invented legacy cache uses inert roles; historical small-stream operational fixture does not satisfy the fixed protected-size contract. Those are remaining qualification requirements, not permission to relax guards.

Private evidence: `private/sessions/20261020-RA-003-observation-launcher/final/result.json`, raw stdout/stderr and three source snapshots; `independent-review.json`; exclusive before-images of eight continuity files. Public changes: launcher, retained launcher, test file, assessment, this report, STATE, backlog, handoff, feature progress and pre-camera readiness. Private session/feature notes synchronized; prior consents/evidence preserved. No feature status promoted.

Camera commands: **none**. No actual firmware/constants/native payload reads, downloads/uploads, installed dependency activation, actual activation records or driver/firmware changes. All five actual activity decisions pending; no feature, recovery or device-write gate passed.

Next single work package: **RA-003: qualify the new disabled observation launcher through real preparation and one owned supervised engine composition using complete invented legacy/source/metadata records and explicit runtime substitutions. Preserve the fixed protected-size contract, source freshness and original pending route; do not weaken guards to fit the small historical fixture. Cover saved-result tamper, drift-before-spawn and unknown completion, and independently review before actual records. Keep actual activity decisions pending and public activation disabled; no actual firmware/constants/native payload reads, installed dependency activation, downloads/uploads or camera contact.** Goal remains active.

Reviewed publication commands:

```powershell
git diff --check
git add -- tools/dependency_observation_launcher.py tools/dependency_operational_launcher.py tests/test_dependency_observation_launcher.py research/OBSERVATION_LAUNCHER.md research/sessions/20261020-RA-003-observation-launcher.md research/STATE.json docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/PRE_CAMERA_READINESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git commit -m "Add disabled observation transport and deterministic bootstrap"
git status --short --branch
```
