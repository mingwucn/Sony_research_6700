# RA-003: checked metadata/launch binding

2026-10-20; branch `codex/ra003-launch-context-binding`, clean starting HEAD `5ca186b`.

[Assessment](../LAUNCH_CONTEXT_BINDING.md). 91/91 focused cases pass, zero failures/errors/skips, exit 0; 71 public boundary/retained regressions plus 20 full invented composition/refusal cases, 25.282413s, 137 stable pins. Historical 44-role comparison and current 46-role request share 38 retained source buffers and origin labels; six replacements and two imports remain explicit. Independent source review repaired mutable owner-buffer binding and fixture acquisition cleanup. Current-role ordinary semantics and fresh outer integration remain pending. English/native FTP first; camera commands none; no feature/recovery/write gate.

```powershell
git status --short --branch
git switch -c codex/ra003-launch-context-binding
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests',pattern='test_dependency_launch_context.py'));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-launch-context/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import subprocess,sys;p=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','tools/dependency_launch_context.py'],capture_output=True);print({'child_exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)});raise SystemExit(0 if p.returncode==2 and not p.stdout and not p.stderr else 1)"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-launch-context/record.py
git diff --check
```

Host/interpreter: Windows AMD64, CPython 3.13.12 at
`C:/ProgramData/miniconda3/python.exe`; isolated/no-site/no-bytecode, UTF-8,
optimization 0. Focused boundary suite: 4/4, exit 0, 0.006s.
The exact qualification command was run twice into exclusive folders. V1:
88/89 passed, one assertion failure, exit 1, 24.215070s; changed closure digest
was correctly refused as prior_binding, but the test expected a different error
regex. Initial sources, result and raw log are preserved. Review repairs and the
corrected error assertion preceded V2: 91/91, exit 0, zero failures/errors/skips,
25.28241349995369s wrapper / 25.234s unittest. The two new cases cover the review
repairs; acceptance thresholds and runtime policy were not widened.

Composition: four new boundary tests, sixteen retained adapter-loader tests,
eighteen context tests, nineteen legacy-bridge tests, fourteen scope tests and
twenty new full integration/refusal cases. Actual observer construction was blocked.
Historical full public and GDT process suites were not repeated. Direct CLI child
refused exit 2 without stdout/stderr; its measuring wrapper exited 0.

Early diagnostic runpy commands inspected only authored sources and invented
metadata; a complete composition smoke check returned 44/38/14 and exited 0.
Two exploratory source searches used an absent old directory name and a PowerShell
wildcard path unsupported by rg; corrected existing paths were read. No evidence
or target values were fabricated. No source acquisition/download or legal research
was performed in this package.

Final log SHA-256: `5b9c562b7a26db38955c49d956c418514f0d698bb03b721c28ce330f2ab7bcae`. All 137 pinned ordinary authored/invented metadata files remained unchanged and were reverified before publication.

- `tools/dependency_launch_context.py` SHA-256: `ece52bda6a0b55fdb4816c6837c2a78fa1a4d46c86cb04f550d78a55c5687a44`
- `tests/test_dependency_launch_context.py` SHA-256: `52f21e600ad8e12547410e84205a09d6a046a5325891287fcf6a68a02b5ec7a8`

Changed public paths: new composition module and boundary tests, assessment and this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md, research/PRE_CAMERA_READINESS.md and research/STATE.json. Private state/feature notes were backed up or written exclusively. Only reviewed public paths are staged.

Camera commands: **none**. No actual firmware/constants/native payload/saved actual raw reads, installed dependency activation, upstream execution, download/upload, driver/firmware change or device write. No feature support or recovery/write gate passed. Previous goal turn: implementation/qualification progress; current turn: implementation/qualification progress. Overall goal remains active.

Next single package: **RA-003: implement successor ordinary dependency/source semantics for the current 46-role prepared request, deriving the closure_manifest bytes directly from that same source map and binding the five checked helpers without labelling derived JSON as a Python source. Retain the old 44-role validator as comparison-only; migrate the affected ordinary contracts rather than pretending their old source-alias grammar already covers the successor. Qualify complete invented records and independent source review before connecting the current-role preflight to the isolated launcher. Keep actual observation/public runtime disabled, decisions pending, and no actual activation records, installed dependency activation, firmware/constants/native payload reads or camera contact.**
