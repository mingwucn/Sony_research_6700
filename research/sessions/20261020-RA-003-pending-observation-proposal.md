# RA-003: pending observation proposal

2026-10-20; branch `codex/ra003-pending-observation-proposal`, base `1091d04`.
Previous goal turn: **progress**, dependency draft committed. Current turn:
**progress**, fourteen-role proposal/core/argv checked and a concrete legacy
identity incompatibility verified. The full pre-camera goal remains active.

The [assessment](../PENDING_OBSERVATION_PROPOSAL.md) describes the scope and
remaining prerequisites. Assembly exit **0**: 14 ordinary roles, 51 source roles,
46 prepared roles, eight captured authored validators, six original comparison
records, five pending dispositions. Pure proposal validation passes. No complete
legacy bundle, decided-scope validation or full outer preflight was attempted.

The selected seven-artifact baseline was created before assembly and literal-pinned
after source review found that the prior recorder had no complete output receipt.
Its selection is explicitly current-turn, not retrospective derivation attestation.
The package separately matches the original literal-pinned audit. Baseline and
helper receipts remain private; all original files are retained.

Independent source-only review accepted helper SHA-256
`bbbdc282ec40b2de39f443f53fb8b4288bf6f49aa56fb61826026bf7deddbd90`. No remaining required source findings; reviewer read no data and
performed no execution/reproduction. Interpreter/stdlib/OS remain trusted; the
captured importer is not a hostile-code sandbox or full host attestation.

## Exact commands and results

Interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython **3.13.12**,
Anaconda Windows AMD64. Commands:

```powershell
git status --short --branch
git switch -c codex/ra003-pending-observation-proposal
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-pending-observation-proposal -ErrorAction Stop | Out-Null
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-pending-observation-proposal/assemble.py
```

Assembly ran once, exit **0**, exclusive `assembly-1` output; no retries. Saved
source and selected draft pins rechecked at completion. The private recorder
rechecks every selected input pin again before publication.

Qualification used two authored PowerShell here-strings piped to
`C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -`. Each ran:

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path[:0]=['.','tests'];s=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in ('test_dependency_observation_contract','test_dependency_execution.TextPreparationTests'));r=unittest.TextTestRunner(verbosity=2).run(s);print('RESULT',r.testsRun,len(r.failures),len(r.errors),len(r.skipped));raise SystemExit(not r.wasSuccessful())"
```

Both inner suites passed **34/34**, zero failures/errors/skips, exit **0**.
The first wrapper exited **1** after saving the passing receipt: a file-handle
variable shadowed the numeric failure count in its final assertion. Logs and
receipt are preserved. Corrected wrapper exit **0**: **14.145s** suite /
**14.687360s** wrapper. This is retained invented metadata/text
coverage, not firmware/runtime/native feature validation. No production/test
source changed and no broad historical suite was rerun.

A separate isolated-interpreter stdin diagnostic read only the explicitly
selected original config (literal SHA-256 checked) and new request metadata. It
asserted `old['operation_id'] != request['operation_id']`, then saved the two
static equality predicates and incompatibility conclusion, exit **0**. No
complete legacy validator or old authority decision was executed/promoted.
One local lookup used a nonexistent historical composition-helper path; it
failed without executing anything and was not treated as authoritative evidence.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-pending-observation-proposal/record.py
```

Recorder exit **0**, eight exclusive existing-note before-images; private session
and function progress synchronized. Public changes: this report,
`research/PENDING_OBSERVATION_PROPOSAL.md`, `research/STATE.json`,
`docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`,
`research/PRE_CAMERA_READINESS.md`. Source lock and implementation unchanged.

Camera commands: **none**. No protected firmware/constants read, installed
payload open/import/activation, network/download/upload, driver/firmware change,
feature support, recovery or device-write gate. Draft cached Python texts are
read as data only; no current payload freshness or complete proposal authority
is asserted.

Remaining: complete original legacy graph, operation-ID compatibility design,
old null dependency fields, all five activity dispositions, external evidence
and accepted anchors, fresh runtime qualification and separately reviewed
transport. Exact-target English/FTP behavior and recovery remain unproved.

Next single package: **RA-003: design and qualify a pending-only successor/legacy comparison contract that preserves historical operation/config bytes while explicitly binding the new proposal. Inventory the complete original legacy reference graph through an explicit metadata/source-cache allowlist; distinguish historical authority from current activity decisions. Resolve the observed operation-ID incompatibility without fabricating allow records, rewriting originals, accepting operational anchors, assembling transport, activating dependencies, reading protected inputs or contacting the camera.**

Reviewed publication commands:

```powershell
git diff --check
git add -- research/PENDING_OBSERVATION_PROPOSAL.md research/sessions/20261020-RA-003-pending-observation-proposal.md research/STATE.json docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/PRE_CAMERA_READINESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git commit -m "docs: bind pending observation proposal and record legacy identity gap"
git status --short --branch
```
