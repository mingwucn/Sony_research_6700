# Requested A6700 Powerful project review

2026-10-20. Topic branch `codex/a6700-reference-check-20261020-j`.
Evidence: source-report, static-inference, offline-tested.

Fresh GitHub API retrieval resolves main to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the [33-text/12-Python static audit](20261019-RA-003-a6700-powerful-audit.md). Complete recursive tree: 51 entries. README, development plan, manual and NOTICE were freshly fetched at that immutable commit and each verified against its Git blob hash and size. Source lock unchanged. This review does not repeat or independently reproduce the upstream device experiments.

| Priority | Finding | Remaining prerequisite |
|---|---|---|
| Native English | No unlock located in the inspected material. | Exact mainland language restriction/resource mapping and reversible change. |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG transfer physically tested on a6700 2.00. Implementation remains unpublished in the pinned tree. | Published code, exact build/region identities, direct camera-to-server Wi-Fi evidence without a relay, integrity, persistence, security and failure tests. |
| Rollback before writes | Public Pico route runs Fastboot temporarily in camera RAM and reads known storage ranges. | Full storage coverage and complete restoration/recovery remain unverified. |
| FL2/FL3, deferred | Author reports offline validation underway. | Physical qualification and reproducible release. |

Primary sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md), [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

Device records concern macOS/a6700 2.00. A shared displayed version does not establish Windows/mainland-body binary compatibility. The public read route requires temporary native execution (R2), independently gated from ordinary USB identification. The author's complete backup/restore and official-firmware rescue are explicitly unfinished. Bundled feature changes also require review against our separate feature gates.

NOTICE assigns GPL-3.0-only to authored code/docs and expressly declines to relicense inherited Pico material whose pinned upstream revision has no attached licence. Whole-chain reuse rights and source/binary equivalence remain unresolved. No upstream implementation, binary payload, offset or instruction was adopted. Existing inspection-rights answers and all feature/recovery/device-write gates remain unchanged and false.

## Exact commands and results

Starting Git tree clean on `codex/ra003-host-launcher`; host-only inspection. Browser tree retrieval failed; repository/document browsing and bounded host API/raw text retrieval succeeded. A local exploratory read used the nonexistent tests/test_ftp_policy.py; the correct tests/test_ftps_client_policy.py was read and tested, with no source changes. Public text only; no upstream imports/execution, firmware/payload acquisition, dependency installation or private upload.

```powershell
git status --short --branch
git switch -c codex/a6700-reference-check-20261020-j
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-j -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-i/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-j/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-j/check_reference.py
```

All above exit 0. Acquisition script creates exclusive private outputs, caps each response at 4 MiB, and verifies the four public text blobs against the complete tree.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest,time,json,pathlib;sys.path.insert(0,'.');sys.path.insert(0,'tests');t=time.perf_counter();r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy'));d={'total':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'skipped':len(r.skipped),'seconds':time.perf_counter()-t,'interpreter':sys.executable,'version':sys.version,'exit_code':0 if r.wasSuccessful() else 1,'camera_commands':[]};pathlib.Path('private/sessions/20261020-a6700-reference-review-j/tests.json').open('x',encoding='utf-8').write(json.dumps(d,indent=2)+'\n');print(json.dumps(d));raise SystemExit(d['exit_code'])"
```

CPython 3.13.12, isolated/no-site/no-bytecode: **17/17 passed**, zero failures/errors/skips, exit **0**, 1.579s suite / 1.711564s wrapper. These unchanged local mocked-transport tests establish no upstream FTP, server or camera behavior. Historical full suites were not rerun for an unchanged reference.

The host-authored private recording script backs up existing private/public notes before adding this review; original intake and prior evidence are preserved. record.py is copied from the prior reviewed recording script with only the new report path and record key changed. The existing source lock and RA-003 phase/next package are unchanged.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-j/record.py
git diff --check
git add -- docs/BACKLOG.md docs/FEATURE_PROGRESS.md research/STATE.json research/sessions/20261020-a6700-reference-review-j.md
git diff --cached --check
git diff --cached --stat
git diff --cached -- docs/BACKLOG.md docs/FEATURE_PROGRESS.md research/STATE.json research/sessions/20261020-a6700-reference-review-j.md
git commit -m "docs: refresh a6700 project findings for owner priorities"
git status --short --branch
```

Changed public files: this report, docs/BACKLOG.md, docs/FEATURE_PROGRESS.md, research/STATE.json. Private session/feature notes backed up and updated. Source lock and RA-003 global phase/next package preserved.

Camera commands: **none**. No feature support, recovery or device-write gate passed.

Next single reference package: **FT-101: audit published FTP implementation and direct camera-to-server Wi-Fi evidence when available**, including exact target identity, integrity, persistence and failure behavior. This reference finding does not block useful offline RA-003 work.
