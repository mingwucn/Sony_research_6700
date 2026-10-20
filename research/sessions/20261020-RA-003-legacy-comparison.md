# RA-003: historical/successor comparison

2026-10-20; branch `codex/ra003-legacy-comparison`, base `ab7ad16`.
Previous goal turn: **progress**, proposal/core/argv checked. Current turn:
**progress**, full original 25-input reference inventory, distinct operation
comparison and six limited historical stages reconciled. Overall goal active.

See the [assessment](../LEGACY_SUCCESSOR_COMPARISON.md) for scope and blockers.
No full historical act bundle or current authority records were created. The
new public comparator is disconnected from operational launch paths.

## Commands and results

Interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython **3.13.12**,
Anaconda Windows AMD64; isolated/no-site/no-bytecode flags below.

```powershell
git status --short --branch
git switch -c codex/ra003-legacy-comparison
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-legacy-comparison -ErrorAction Stop | Out-Null
```

Preliminary isolated-interpreter stdin metadata inspection listed the original
map roles and cached text field names only; no cached text was output/executed.
An explicit current-turn sixteen-artifact proposal comparison baseline was
saved and literal-pinned. It is a technical selection, not retrospective
attestation. All 25 actual read paths are explicitly authored and must match
the separately literal-pinned historical map before reads.

Initial new-test check used an authored PowerShell here-string piped to:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -
```

It loaded `test_dependency_legacy_comparison` through unittest: **16/16 passed**,
zero failures/errors/skips, exit **0**, **0.247s** suite. The broader final
qualification then ran:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-legacy-comparison/qualify.py
```

Exact inner argv rendered as a command:

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path[:0]=['.','tests'];s=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in ('test_dependency_legacy_comparison','test_dependency_observation_contract','test_dependency_execution.TextPreparationTests'));r=unittest.TextTestRunner(verbosity=2).run(s);print('RESULT',r.testsRun,len(r.failures),len(r.errors),len(r.skipped));raise SystemExit(not r.wasSuccessful())"
```

**50/50 passed**, 16 new + 23 retained observation-contract + 11 retained
text-preparation cases; zero failures/errors/skips, child and wrapper exit **0**,
**13.634s** suite / **14.177369s** wrapper. Six source/test
pins stable. Raw stdout/stderr and exact argv saved privately. Invented
metadata/cache texts only; no broad historical suite rerun.

The direct isolated CLI was run through an authored stdin subprocess wrapper:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_legacy_comparison.py
```

Expected refusal **2**, empty stdout/stderr; wrapper **0**. No activation API.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-legacy-comparison/collect.py
```

First revision: exit **1**, preserved `comparison-1` and helper before-image.
Proposal and byte comparison passed; original retained gate parent evidence and
qualifications passed, then its `effective_sources` old namespace lookup refused
`outer_v2_refused:contract`. This reproduces a documented historical defect;
no source fallback, protected read or runtime retry was attempted.

After diagnosis and independent source review, the corrected helper ran once
to exclusive `comparison-2`, exit **0**. It uses the separately literal-pinned
ancestry comparison validator and verifies its embedded proof against separately
pinned original proof bytes. The original 51-role operational source map/gate
is not replaced. All 25 records, 47 cache text receipts and 29 retained source
copies match; six limited historical stages pass. Fourteen-role successor
proposal validates again with all five decisions pending. Input pins rechecked.
This is a reviewed successor metadata diagnostic, not a retry of any protected act.

Independent authored-source review accepted new module/tests and both collector
revisions. Final helper SHA-256 `7fb73e613e9c29bb203ee45dac06319b9ee1de186b5f425de9c912da7d52b7e9`.
Review did not read data/cache/proof or run tests. Captured authored imports
avoid normal tools/package/bytecode imports. Interpreter/stdlib/OS remain trusted;
this is no hostile-code sandbox, atomic snapshot or full host attestation.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-legacy-comparison/record.py
```

Recorder exit **0**, eight exclusive existing-note before-images, synchronized
private session/function notes, all selected input and qualification pins checked.

Changed public files: `tools/dependency_legacy_comparison.py`,
`tests/test_dependency_legacy_comparison.py`, `research/LEGACY_SUCCESSOR_COMPARISON.md`,
this report, `research/STATE.json`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`,
`docs/FEATURE_PROGRESS.md`, `research/PRE_CAMERA_READINESS.md`. No original
comparison record, execution source/launcher, source lock or upstream code changed.
Private metadata, cached source and proof remain ignored.

Camera commands: **none**. No firmware/constants/installed payload read,
dependency/native activation, network/download/upload, driver/firmware change,
accepted authority/transport, full legacy bundle or full outer preflight. Native
English/FTP, recovery and device-write gates remain unproved. Three historical
dependency null fields remain unchanged; all five current decisions pending.

Next single package: **RA-003: integrate the pending proposal and historical comparison into one captured-source, non-executing review preflight. Bind comparison-only validators separately from the unchanged operational source roster, preserve original records and both operation contexts, and qualify source drift, cleanup and saved-result tamper refusals. Keep all five activity decisions pending; no accepted authority, launch transport, dependency activation, protected-input read or camera contact.**

Reviewed publication commands:

```powershell
git diff --check
git add -- tools/dependency_legacy_comparison.py tests/test_dependency_legacy_comparison.py research/LEGACY_SUCCESSOR_COMPARISON.md research/sessions/20261020-RA-003-legacy-comparison.md research/STATE.json docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/PRE_CAMERA_READINESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git commit -m "feat: compare pending successor with preserved historical records"
git status --short --branch
```
