# RA-003: pure observation contract session

2026-10-20, branch `codex/ra003-observation-contract`, base `00df33d`.
Previous goal turn: **progress**; reviewed activity packet committed. Current goal
turn: **progress**; separate pure contract implemented and independently reviewed,
with final invented qualification. Goal remains active.

[Assessment](../OBSERVATION_CONTRACT.md) records the new schema/role semantics,
exact immutable-request/argv and external evidence bindings. Existing pending
launcher/source graph and the prior private packet remain unchanged. New code
expresses decided-scope consistency without operational execution or consent.

Reviewed SHA-256:

- Source: `c4d2d0b3bd52f05e946411d300991c6564dac12b02743dfda346c88e0b21563b`
- Tests: `c3e21ed289ec9c3166be6a8259e55bd715689288f2848cbff638f2dff45d6cf1`

Independent reviewer `activity_packet_review` performed static source/test reads,
no imports/tests/processes/protected reads. One substantive alias-contract gap was
fixed despite initial passing tests: exact five-helper+closure mapping now matches
the intended adapter. Prepared/process projection, anchor bounds and dual-parser
traversal checks were repaired before the accepted review/final run.

## Exact commands and results

```powershell
git status --short --branch
# exit 0; clean at 00df33d
git switch -c codex/ra003-observation-contract
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-observation-contract -ErrorAction Stop | Out-Null
# both exit 0
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_observation_contract'));raise SystemExit(not r.wasSuccessful())" 2>&1 | Tee-Object -FilePath private/sessions/20261020-RA-003-observation-contract/exploratory-tests.log
# exit 0; initial 20/20, 11.199s; not final source/fixture qualification
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_observation_contract'));raise SystemExit(not r.wasSuccessful())" 2>&1 | Tee-Object -FilePath private/sessions/20261020-RA-003-observation-contract/review-tests.log
# exit 0; corrected 23/23, 10.759s
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-observation-contract/qualify.py
# exit 0; frozen final 98/98, no failures/errors/skips, 138 stable pins
```

Final exact child command:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');s=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in ('test_dependency_observation_contract', 'test_dependency_authority_grammar', 'test_dependency_input_semantics', 'test_dependency_operational_scope', 'test_dependency_operational_launcher'));r=unittest.TextTestRunner(verbosity=2).run(s);print('RESULT',r.testsRun,len(r.failures),len(r.errors),len(r.skipped));raise SystemExit(not r.wasSuccessful())"
# exit 0; 18.706s suite / 19.720849s qualification wrapper
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_observation_contract.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_operational_launcher.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_operational_child.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_operational_metadata.py
# each expected exit 2, empty stdout/stderr; no operational dispatch
```

Interpreter: CPython 3.13.12 Anaconda, Windows AMD64; isolated/no-site/no-user-site,
no-bytecode, UTF-8, optimize 0. Final suite = 23 new + 75 retained standard-library
synthetic tests. All fixtures are invented metadata/source text; no actual crypto,
firmware/constants/native payload or installed dependency bodies. Tests prove
pure consistency/refusal and unchanged pending contracts, not actual execution,
human/legal authority, history truth, host attestation or target support. Historical
full/process suites not rerun because their implementation stayed byte-identical.
Source receipts are not an execution allowlist or complete dynamic closure.

Raw logs, qualification script/results, source snapshots and reviewer receipt stay
private. stdout SHA-256 `23e91666e61a1749aa1cb4d3080cc69d10cb3b7d137af0ac88280596473cbc1f`;
stderr SHA-256 `41576275ab392a54a8e0e4866918eebcfc5ca4f34a5c1d586883d70f9c6ae9e5`.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-observation-contract/record.py
git diff --check
git add -- tools/dependency_observation_contract.py tests/test_dependency_observation_contract.py research/OBSERVATION_CONTRACT.md research/sessions/20261020-RA-003-observation-contract.md research/STATE.json docs/BACKLOG.md docs/FEATURE_PROGRESS.md docs/CODEX_HANDOFF.md research/PRE_CAMERA_READINESS.md research/ACTIVITY_REVIEW_PACKET.md
git diff --cached --check
git diff --cached --stat
git commit -m "feat: add pure observation contract with external decision binding"
git status --short --branch
```

The initial whitespace check returned exit 2: the note recorder doubled CR in
ACTIVITY_REVIEW_PACKET.md while appending its continuation. Byte-level newline
normalization repaired that document, and the recorder now normalizes existing
CRLF before writing. Source/tests and qualification pins remained unchanged.
The repeated whitespace check and staged check passed with exit 0.

Publication results are retained separately in the ignored publication receipt
and final response. Changed public files are the ten explicitly staged paths.
Nine existing public/private note before-images are saved before updating.
No old consent/observation deleted, source lock changed, private input uploaded,
download performed, actual record assembled, dependency activated or camera
contacted. Camera commands: **none**. Native English/FTP first; FL2/FL3 deferred;
no feature, recovery or device-write gate passed. Actual decisions stay pending.

Next single work package: **RA-003: integrate the reviewed pure observation contract into a separate disabled source-captured outer preflight and saved-parent validation path. Derive the explicit source-roster delta, immutable request-core and separately supplied authority-record bindings; preserve original comparison inputs, exact dependency projection, fixed I/O/supervision limits and the pending route. Qualify complete, changed-anchor/source/argv, undecided and cleanup/refusal cases with invented records and intercepted runtime only; independently review before actual record assembly. Keep public activation disabled and all actual activity decisions pending; no firmware/constants/native payload reads, installed dependency activation, downloads/uploads or camera contact.**
