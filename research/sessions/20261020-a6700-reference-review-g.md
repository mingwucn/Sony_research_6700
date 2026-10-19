# Requested A6700 Powerful project check

2026-10-20 local date. Branch `codex/a6700-reference-check-20261020-d`.
Evidence: source-report, static-inference, offline-tested.

GitHub commit API resolved main to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`,
unchanged from the [33-text / 12-Python static audit](20261019-RA-003-a6700-powerful-audit.md).
This refresh verified four public documents against their pinned Git blob hashes
and sizes and checked a complete 51-entry tree. It did not repeat the full code audit.
No change to references/sources.lock.json is needed.

| Priority | Finding | Remaining prerequisite |
|---|---|---|
| Native English | No unlock identified in inspected material. | Exact mainland resource/restriction mapping and a reversible change. |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG double transfer physically tested on a6700 2.00. | Published implementation, direct Wi-Fi/server evidence without a relay, target hashes/region, integrity and failure behavior. |
| Recovery before writes | Public Pico route temporarily runs Fastboot in camera RAM and reads known storage ranges. | Physical storage coverage and complete restoration remain explicitly unverified. |
| FL2/FL3, deferred | Offline validation underway according to roadmap. | Physical validation and a reproducible release. |

Primary pinned sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md),
[roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md),
[manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md),
[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

Published hardware records cover macOS/a6700 2.00. Matching version text does not
verify our Windows host, mainland SKU or binary compatibility. The public read
route requires temporary native execution (R2), even though subsequent storage
operations read data. Ordinary USB feature-tool code remains unpublished and the
complete write loop awaits acceptance. The proposed bundled feature release also
needs reconciliation with our separate feature gates. No target offsets adopted.

Authored code/docs are GPL-3.0-only. NOTICE explicitly does not relicense inherited
Pico portions from an upstream commit lacking an attached licence. Whole-chain
reuse rights and source/binary equivalence remain unresolved; no code or payload
was adopted. No legal conclusion or new firmware-inspection permission is inferred.

Commands and results:

```powershell
git status --short --branch
git log -3 --oneline
git switch -c codex/a6700-reference-check-20261020-d
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-g -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-b/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-g/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-g/check_reference.py
```

Acquisition exit 0; four bounded UTF-8 public documents verified and receipts saved
with exclusive creation. GitHub browser/API fetches failed in the web tool; raw
README and host GitHub API succeeded. Public text/tree only, no binary acquisition.

Exact synthetic test command (host-only, mocked transport):

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest,time,json,pathlib;sys.path.insert(0,'.');sys.path.insert(0,'tests');t=time.perf_counter();r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy'));d={'total':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'skipped':len(r.skipped),'seconds':time.perf_counter()-t,'interpreter':sys.executable,'version':sys.version,'exit_code':0 if r.wasSuccessful() else 1,'camera_commands':[]};p=pathlib.Path('private/sessions/20261020-a6700-reference-review-g/tests.json');p.open('x',encoding='utf-8').write(json.dumps(d,indent=2)+'\n');print(json.dumps(d));raise SystemExit(d['exit_code'])"
```

CPython 3.13.12 (Anaconda Windows AMD64), isolated/no-site/no-bytecode, exit 0:
17/17 passed, zero failures/errors/skips; 1.494s suite, 1.626054s wrapper.
These local policy tests do not validate upstream FTP, a camera, or a real server.
Historical full suites were not rerun for this document refresh.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-g/record.py
git diff --check
git add -- docs/BACKLOG.md docs/FEATURE_PROGRESS.md research/STATE.json research/sessions/20261020-a6700-reference-review-g.md
git diff --cached --check
git diff --cached --stat
git diff --cached -- docs/BACKLOG.md docs/FEATURE_PROGRESS.md research/STATE.json research/sessions/20261020-a6700-reference-review-g.md
git commit -m "docs: refresh a6700 reference FTP and recovery findings"
git status --short --branch
```

Changed public files: this report, docs/BACKLOG.md, docs/FEATURE_PROGRESS.md,
research/STATE.json. Private state and feature notes were backed up before adding
this result. Existing untracked tools/dependency_current_metadata.py and
tests/test_dependency_current_metadata.py were left untouched and unstaged.
The separate RA-003 phase and next work package are preserved.

Camera commands: **none**. No drivers/firmware changes, private-input upload,
actual firmware/constants/native payload read, upstream execution or device contact.
No feature support or recovery/device-write gate passed.

Next single reference work package: **FT-101: audit the published FTP implementation
and direct camera-to-server Wi-Fi evidence when available**, using the existing
[evidence checklist](20261019-a6700-powerful-recheck.md#ftp-evidence-checklist-for-the-next-source-only-package).
