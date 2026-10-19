# RA-003: isolated invented adapter qualification

2026-10-20; branch `codex/ra003-isolated-adapter-repair`, starting HEAD `7ce0dd1`.

[Assessment](../ISOLATED_ADAPTER_INTEGRATION.md). 76/76 focused cases passed (64 public regressions, 10 invented process cases, 2 isolated preparation-cleanup cases), zero failures/errors/skips, exit 0. Main suite 178.054891s; cleanup 4.210653s; 153 main-suite pins stable. Checked-buffer adapter loading and existing 300/5/1-second, 2MiB-per-pipe supervision now compose through the full two-phase invented reader and saved-parent verification. Actual observation and complete ordinary-role launch binding remain unqualified. English/native FTP first; FL2/FL3 deferred. Camera commands: none; no feature, recovery or device-write gate passed.

```powershell
git status --short --branch
git switch -c codex/ra003-isolated-adapter-repair
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path[:0]=['.','tests'];r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_adapter_sources'));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-adapter/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-adapter/qualify_cleanup.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-adapter/qualify_cleanup_v2.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_adapter_sources.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import subprocess,sys; p=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','tools/dependency_adapter_sources.py'],capture_output=True); print({'child_exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)});raise SystemExit(0 if p.returncode==2 and not p.stdout and not p.stderr else 1)"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-adapter/record.py
git diff --check
```

Interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython 3.13.12, Windows AMD64,
isolated/no-site/no-bytecode, UTF-8, optimization 0. Initial focused loader test:
16/16 pass, 0.618s, exit 0. Main qualification: 74/74, exit 0, zero skips;
16 loader + 21 binding + 14 scope + 13 wiring + 10 real invented-process cases.
Cleanup v2: 2/2, both fresh worker subprocesses exit 0. Historical full suites
were not repeated; no upstream, real server or camera validation.

Preserved negative evidence: cleanup v1 exits 1 with one pass and one alias_occupied
error because its second prepare reused an already-imported process. V2 isolates
each test in a fresh worker; production code/thresholds unchanged. The direct CLI
child exits 2 with no output, as confirmed by subprocess measurement; the outer
PowerShell tool reported that initial native invocation as exit 1. The confirming
measurement wrapper exits 0. An exploratory read of absent
research/OPERATIONAL_EXECUTABLE_PATH.md failed; the actual assessment is
research/OPERATIONAL_PATH_ASSESSMENT.md. No missing file was fabricated.

The previous turn's initial-complete run remains pre-review evidence; final
qualification uses new exclusive operation folders. No evidence overwritten.
The prior goal turn was progress as a pinned reference refresh with saved findings;
this turn is implementation and qualification progress. The overall goal remains
active; operational and camera prerequisites are not complete.

Main log SHA-256: `9876195a719407411a44640f3ece52ba854f762c31d850ae10056ef18f47118c`.

Reviewed source pins:

- `tools/dependency_adapter_sources.py`: `f618fd079e4c144c08df67c80f94a75db68b2d472cd448bc4bc0e30664d20de8`
- `tests/test_dependency_adapter_sources.py`: `1cd6c0a09dd0ecf57f0784895bb146743cbcba7460a9319e073aacccfad1cb7a`

Changed public paths: loader, loader tests, this report, assessment, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md, research/PRE_CAMERA_READINESS.md and research/STATE.json.
Private authored harness, logs, exclusive source/receipt files and backed-up private session/feature notes remain ignored. Only reviewed public paths are staged.

Camera commands: **none**. No actual firmware/constants/native payload or saved actual raw input reads, dependency activation, download/upload, upstream execution, driver/firmware change, camera access or target offset adoption.

Next single package: **RA-003: compose the existing checked fourteen-role ordinary metadata validation with the migrated prepared-adapter launch request. Bind original candidate/context bytes, operation, frozen scope, current source receipts and dependency anchors to the same supplied invented records; reconcile the legacy comparison and successor role inventories explicitly. Independently review and qualify mismatched/stale/refused cases. Keep public runtime disabled and activity decisions pending; no actual activation records, installed dependency activation, firmware/constants/native payload reads or camera contact.**
