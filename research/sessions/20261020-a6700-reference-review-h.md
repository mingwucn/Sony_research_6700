# Requested A6700 Powerful project check

2026-10-20. Branch `codex/a6700-reference-check-20261020-h`.
Evidence: source-report, static-inference, offline-tested.

GitHub main still resolves to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`.
The complete recursive tree has 51 entries. Four freshly acquired public documents
match their pinned Git blob hashes and sizes. This is a refresh of the
[existing 33-text/12-Python static audit](20261019-RA-003-a6700-powerful-audit.md),
not a new code release or independent reproduction. The source lock is unchanged.

| Owner priority | Finding | Evidence still needed |
|---|---|---|
| Native English | No unlock located in the inspected material. | Exact mainland language restriction/resource mapping and a reversible change. |
| Native Wi-Fi FTP | The author reports FTP settings and RAW+JPEG transfer physically tested on a6700 2.00. | Published implementation, exact target hashes/region, direct camera-to-server Wi-Fi evidence without a relay, integrity and failure tests. |
| Rollback before writes | Public Pico route temporarily executes Fastboot in camera RAM and reads known storage ranges. | Physical storage coverage, complete restoration and recovery for relevant failure states remain unverified. |
| FL2/FL3, deferred | Roadmap reports offline validation underway. | Physical qualification and reproducible release. |

Primary pinned sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md),
[development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md),
[manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md),
[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

Device records cover macOS/a6700 2.00; matching displayed version does not establish
Windows/mainland-body or binary compatibility. The ordinary USB unlock tool and
FTP implementation remain unpublished in this tree. The public read route requires
temporary native execution (R2), separate from ordinary USB identification. No
device procedure was attempted. The planned bundled feature release also requires
review against our separate feature gates.

NOTICE assigns GPL-3.0-only to authored code/docs and explicitly declines to
relicense inherited Pico portions from an upstream commit without an attached
licence. Whole-chain reuse rights and source/binary equivalence remain unresolved.
No code, payload or target offsets were adopted. No new inspection permission is inferred.

## Commands and results

All commands ran on the host. Browser retrieval failed; bounded host GitHub
API/raw text retrieval succeeded. Only public commit/tree metadata and four UTF-8
documents were fetched, with exclusive local output creation. Acquisition exit 0.

```powershell
git status --short
git branch --show-current
git log -3 --oneline
git switch -c codex/a6700-reference-check-20261020-h
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-h -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-g/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-h/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-h/check_reference.py
```

Relevant existing local mocked-transport policy tests, unchanged:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest,time,json,pathlib;sys.path.insert(0,'.');sys.path.insert(0,'tests');t=time.perf_counter();r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy'));d={'total':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'skipped':len(r.skipped),'seconds':time.perf_counter()-t,'interpreter':sys.executable,'version':sys.version,'exit_code':0 if r.wasSuccessful() else 1,'camera_commands':[]};pathlib.Path('private/sessions/20261020-a6700-reference-review-h/tests.json').open('x',encoding='utf-8').write(json.dumps(d,indent=2)+'\n');print(json.dumps(d));raise SystemExit(d['exit_code'])"
```

CPython 3.13.12, isolated/no-site/no-bytecode: **17/17 passed**, zero
failures/errors/skips, exit **0**, 1.414s suite / 1.547210s wrapper.
These tests establish no upstream FTP, real-server or camera behavior.
Historical full suites were not rerun for an unchanged public reference.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-h/record.py
git diff --check
git add -- docs/BACKLOG.md docs/FEATURE_PROGRESS.md research/STATE.json research/sessions/20261020-a6700-reference-review-h.md
git diff --cached --check
git diff --cached --stat
git diff --cached -- docs/BACKLOG.md docs/FEATURE_PROGRESS.md research/STATE.json research/sessions/20261020-a6700-reference-review-h.md
git commit -m "docs: record requested a6700 project check"
git status --short --branch
```

Changed public files: this report, docs/BACKLOG.md, docs/FEATURE_PROGRESS.md,
research/STATE.json. Private session/feature notes backed up before updating.
Pre-existing changes to tools/dependency_launch_context.py,
tools/detached_metadata_loader.py and untracked tools/dependency_outer_metadata.py
remain untouched and unstaged. Shared RA-003 phase/next package remain unchanged.

Camera commands: **none**. No upstream execution, firmware/native payload acquisition,
private-input upload, driver or camera modification. No feature support, recovery
or device-write gate passed.

Next single reference package: **FT-101: audit the FTP implementation and direct
camera-to-server Wi-Fi evidence when published**, including exact target identity,
integrity, persistence and failure behavior. No camera work is needed for that audit.
