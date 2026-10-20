# RA-003: disabled captured observation preflight

2026-10-20, branch `codex/ra003-observation-outer`, base `0f56f0e`.
Previous goal turn: **progress** (requested reference check `f07f6ab` on its separate
worktree). Current: **progress**; finished contract commit `0f56f0e`, then added
captured-validator preflight and saved-parent comparison. Goal remains active.

[Assessment](../OBSERVATION_OUTER.md) documents exact bindings and material limits.
Positive legacy gate is an invented source stub; real-gate qualification is refusal
only. This is partial outer integration with no runtime/engine/supervisor wiring.
The initial outer loader is trusted, not authenticated by its captured source;
dynamic import closure and operational execution roster are not attested.

Reviewed SHA-256:

- Source: `0f26c9059cf78b3bf244724511f1a5085681b19bd04b93ed855627f9bd94b446`
- Tests: `a3f712a509a166520fe6000f9672b822fc39c458af04d82f5b1ab2d172db62c7`

Independent source reviewer accepted after an exact53-before-execution fix.
The earlier count-only roster check allowed non-graph role substitution to reach
validator execution. New same-count replacement test intercepts exec and requires
refusal before any execution. No acceptance threshold was relaxed.

## Exact commands and results

```powershell
git status --short --branch
# clean after contract commit 0f56f0e
git switch -c codex/ra003-observation-outer
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-observation-outer -ErrorAction Stop | Out-Null
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_observation_outer'));raise SystemExit(not r.wasSuccessful())"
```

This exploratory command ran three times: first exit 1, 14 cases/4 failures/5
errors, 2.783s; second exit 1 with same counts, 2.525s; third exit 0, 14/14 passed,
13.328s. Fixed closed graph omissions: execution's local package-preflight import
and that helper's producer edge. The helper is captured, not left to a disk import.
No firmware/native or installed dependency ran. Negative summaries remain private.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-observation-outer/qualify.py
# exit 0; superseded before exact-roster review fix: 112/112, 29.709s / 30.208285s
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-observation-outer/qualify-reviewed.py
# final exit 0; 112/112, 29.152s suite / 29.640268s wrapper, 141 stable pins
```

A shell-quoted inline command to create qualify-reviewed.py first failed with
SyntaxError; the absent-driver invocation exited 2. An exclusive corrected copy
used explicit character quoting, then the command above succeeded. No existing
evidence was overwritten. Both qualification directories remain private.

Final child command (CPython 3.13.12 Anaconda Windows AMD64; isolated/no-site,
no-bytecode, UTF-8, optimize 0):

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');s=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in ('test_dependency_observation_outer', 'test_dependency_observation_contract', 'test_dependency_authority_grammar', 'test_dependency_input_semantics', 'test_dependency_operational_scope', 'test_dependency_operational_launcher'));r=unittest.TextTestRunner(verbosity=2).run(s);print('RESULT',r.testsRun,len(r.failures),len(r.errors),len(r.skipped));raise SystemExit(not r.wasSuccessful())"
# exit 0; 14 new + 98 retained, zero failures/errors/skips
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_observation_outer.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_observation_contract.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_operational_launcher.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_operational_child.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_operational_metadata.py
# each expected exit 2, empty stdout/stderr
```

Raw stdout SHA-256 `71e4e1f92241e83f576e8598a1ee7de4036969e9ddb1dbfb39140c387dd3f26c`;
stderr `11dc6568ed7c3907328c4c6caed2853f2b3513a33e8e8ba17a4937e941c601c5`. Logs, snapshots, exact commands, reviewer receipt
and original public/private note before-images stay private. Tests exercise
authored validators with invented inputs/intercepted legacy success; no actual
protected/dependency observation, external permission or camera result.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-observation-outer/record.py
git diff --check
git add -- tools/dependency_observation_outer.py tests/test_dependency_observation_outer.py research/OBSERVATION_OUTER.md research/sessions/20261020-RA-003-observation-outer.md research/STATE.json docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/PRE_CAMERA_READINESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git commit -m "feat: add disabled captured observation preflight"
git status --short --branch
```

Only the nine reviewed paths above change publicly. Private continuity notes are
backed up before updating; earlier evidence and actual pending decisions remain.
The source lock and existing contract/launcher/child stay unchanged. Camera
commands: **none**. No downloads/uploads, actual firmware/constants/native
payload reads, installed dependency activation or actual record assembly.
English/native FTP remain first; no feature, recovery or device-write gate passed.

Next single work package: **RA-003: qualify successful end-to-end captured observation preflight and saved-parent comparison through the unchanged retained gate using a complete wholly invented legacy bundle, without intercepting that gate. Cover changed original records, source/anchor/runtime bindings and cleanup/refusal. Independently review before any actual record assembly. Keep activation disabled and actual activity decisions pending; no firmware/constants/native payload reads, installed dependency activation, downloads/uploads or camera contact.**
