# A6700 Powerful: current source review

2026-10-20; topic branch `codex/a6700-reference-check-20261020-r`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

Main is now `2de85f1cca89b0e20ee25a70f93e04c3d34e10e5`, a direct child of the prior audited `0c6294a83988f196adfc980de59f9a1d0b92e8e2`. Full 51-entry tree comparison: only upstream AGENTS.md changed, adding contributor/commit-description guidance. That text was acquired and blob-verified as reference data, not adopted as local instructions. All 38 other blob entries are identical; README, development plan, manual and NOTICE were freshly size/blob-verified. No new implementation to execute or full code audit to repeat. Source lock advances with its prior audit baseline preserved.

| Goal | Published finding | Remaining evidence |
|---|---|---|
| Native English, priority | No unlock located in current material or unchanged prior source audit. | Exact mainland resource/restriction mapping and reversible change. |
| Native Wi-Fi FTP, priority | Author reports a6700 2.00 FTP/settings with RAW+JPEG double transfer physically tested. Implementation remains unpublished. | Published implementation, direct camera-to-server Wi-Fi evidence, binary/region identity, file equality, security, persistence, failure handling and reversal. |
| Rollback | Public Pico route runs temporary camera RAM code to read known storage ranges. Full physical storage coverage, full restore and official-firmware recovery remain unverified. | Exact-body recovery envelope and independent verified backups. |
| FL2/FL3, deferred | Offline validation underway; physical testing pending. | No verified installable result; keep later than English/FTP. |

Public physical records are scoped to macOS. They do not qualify our Windows host or the owner's mainland body. Firmware display 2.00 alone does not establish binary compatibility. The ordinary-USB feature tool is still being prepared for publication; the currently public Pico backup route requires hardware and temporary native execution (R2), even though storage operations are described as reads. The planned bundled feature release differs from our separately gated changes.

NOTICE applies GPL-3.0-only to authored material and expressly excludes relicensing inherited Pico portions from an upstream commit without an attached licence. Whole-chain reuse rights and binary/source correspondence remain unresolved. No code, target offsets or payloads adopted.

Pinned sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/README.md), [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/NOTICE).

## Commands and results

Initial branch `codex/ra003-observation-launcher`, two untracked draft files (`tools/dependency_observation_launcher.py`, `tests/test_dependency_observation_launcher.py`), no tracked changes. Those drafts were neither executed, staged nor modified. GitHub tree/API browsing failed; raw document browsing and bounded host public-text GETs succeeded.

```powershell
git status --short
git branch --show-current
git switch -c codex/a6700-reference-check-20261020-r
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-r -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-q/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-r/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-r/check_reference.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-r/review_delta.py
```

All above host commands exited 0. Acquisition: six bounded metadata/text GETs plus one changed AGENTS text GET; no binary assets. Exact test command:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest,pathlib,time,json;sys.path[:0]=['.','tests'];out=pathlib.Path('private/sessions/20261020-a6700-reference-review-r');t=time.perf_counter();f=(out/'tests.log').open('x',encoding='utf-8');r=unittest.TextTestRunner(stream=f,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy'));f.close();d=dict(total=r.testsRun,failures=len(r.failures),errors=len(r.errors),skipped=len(r.skipped),seconds=time.perf_counter()-t,exit_code=int(not r.wasSuccessful()),interpreter=sys.executable,version=sys.version);(out/'tests.json').write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2));raise SystemExit(d['exit_code'])"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-r/record.py
```

Tests: **17/17 passed**, zero failures/errors/skips, exit **0**, **1.607s** wrapper. Interpreter: CPython **3.13.12**, Anaconda Windows AMD64, `C:/ProgramData/miniconda3/python.exe`. Standard-library mocked host policy only, no socket/listener/camera or upstream execution. No broad suite rerun for documentation/reference pin changes. Record command preserves exclusive before-images of seven existing notes/lock before updating.

Changed public files: this report, `references/sources.lock.json`, `research/STATE.json`, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`. Private session/feature notes synchronized; private acquisition receipts, tree/delta and test logs retained. No firmware/constants/native payload reads, uploads, driver/firmware changes or device access. Camera commands: **none**. No feature supported, recovery proved or device-write gate passed.

Next single reference work package: **FT-101: audit the FTP implementation and direct camera-to-server Wi-Fi evidence when published, including exact target/region identity, file equality, security, persistence, failure handling and reversal.** Existing RA-003 engineering continuation remains pending and unchanged.

Reviewed publication commands:
```powershell
git diff --check
git add -- references/sources.lock.json research/STATE.json docs/BACKLOG.md docs/FEATURE_PROGRESS.md research/sessions/20261020-a6700-reference-review-r.md
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git commit -m "docs: review new a6700 reference revision"
git status --short --branch
```
