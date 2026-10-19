# Requested A6700 Powerful source review

2026-10-20 local date. Branch `codex/a6700-reference-review-20261020-d`, starting HEAD `f9aca58`. Evidence: source-report, static-inference, offline-tested.

Fresh GitHub commit/tree lookup confirms main remains `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, identical to the locked prior audit. All 51 tree entries were inventoried; README, development plan, manual and NOTICE were fetched at this exact revision and matched Git blob identities and sizes. SHA-256 receipts remain private. This is a source refresh against the prior implementation audit, not a new full code audit.

| Priority | Finding | Unresolved prerequisite |
|---|---|---|
| Native English | No unlock in the unchanged audited source or current documents. | Mainland restriction/resource mapping and reversible implementation. |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG transfers physically tested on a6700 2.00. | Public implementation; direct Wi-Fi/server evidence without a relay; exact build/region match; transfer integrity and failure handling. |
| Recovery before writes | Public backup route executes temporary RAM Fastboot code through Pico. | Complete physical storage coverage, restoration and official-firmware rescue remain unverified. |
| FL2/FL3, deferred | Roadmap says offline validation in progress. | Physical validation pending. |

Primary sources at the checked revision: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md), [roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

The manual's physical records cover a6700 2.00/macOS, not verified correspondence with this owner's mainland body or Windows host. Its read-only storage interface requires camera-side RAM execution (R2 here), not ordinary passive USB identification. No device instructions were executed. The roadmap's ordinary USB unlock tool remains unpublished; complete write-loop acceptance is pending. Planned bundled feature releases do not establish independently gated English/FTP changes.

NOTICE covers authored material under GPL-3.0-only and explicitly leaves inherited Pico material from an unlicensed upstream outside that grant. Whole-chain reuse rights and source/binary equivalence remain unresolved. No implementation, offset or payload adopted. Owner firmware-inspection rights answer remains No / unknown; this review makes no new legal conclusion.

## Commands and results

```powershell
git status --short --branch
git switch -c codex/a6700-reference-review-20261020-d
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-d -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-c/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-d/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-d/check_reference.py
```

All exited 0. Public text acquisition caps responses and exclusively creates receipts; no upstream execution or binary retrieval. Web tree/main failed; repository root, document pages and local GitHub API requests succeeded. The current remote commit matches the existing source lock, which remains unchanged. No source changes were adopted.

A standard-library stdin wrapper under `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -` added `.` and `tests` to sys.path, ran `unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy')`, exclusively saved tests.log/tests-result.json, measured time and propagated success. Equivalent exact suite command:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path[:0]=['.','tests'];r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy'));raise SystemExit(not r.wasSuccessful())"
```

CPython 3.13.12: 17/17 passed, zero failures/errors/skips, exit 0; 1.5992487999610603 seconds wrapper. Log SHA-256 `59be4eb6af9d1950bd68fc1a90b6380055b0ac1be2ea38cb0d470f54d5bfe62b`. Mocked host protocol tests establish no upstream, camera, real-server or native FTP result. No historical full suite rerun.

Recording command: `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-d/record.py`. Review checks: `git diff --check`, explicit four-path `git add`, `git diff --cached --check`, staged content/path inspection, and topic-branch commit. Results recorded in final response.

Changed public files: this report, docs/BACKLOG.md, docs/FEATURE_PROGRESS.md, research/STATE.json. Private session/feature notes updated after exclusive backups. Starting tree was clean. No implementation files were changed. Shared RA-003 phase, latest qualification and next implementation package remain unchanged.

Camera commands: **none**. No firmware/constants/private payload reads, uploads, upstream launchers, driver/firmware changes or feature/recovery/device-write gate passed.

Next single reference package: **FT-101: audit the public FTP implementation and direct camera-to-server Wi-Fi evidence when published**, including exact target/build, no-relay operation, file equality, interruption handling and reversible changes. No author contact or monitoring scheduled.
