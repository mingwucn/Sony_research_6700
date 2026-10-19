# Requested A6700 Powerful check

2026-10-20 local date. Branch `codex/a6700-reference-check-20261020-c`.
Evidence: source-report, static-inference, offline-tested.

Fresh Git remote and GitHub commit/tree checks agree: main is
`0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the
[prior static code audit](20261019-RA-003-a6700-powerful-audit.md).
All four refreshed documents match their pinned Git blob hashes and sizes;
51 tree entries. This is a document/source refresh, not a repeated full code audit.

| Owner priority | Finding | Remaining prerequisite |
|---|---|---|
| Native English | No unlock identified in the inspected material. | Exact mainland resource/restriction analysis and reversible change. |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG transfers physically tested on a6700 2.00. | Public implementation, direct Wi-Fi/server evidence, exact build/region identity, transfer integrity and failure behavior. |
| Rollback before writes | Public route temporarily executes a RAM Fastboot payload to read known storage ranges. | Whole-storage coverage and complete restore are explicitly unverified. |
| FL2/FL3, deferred | Offline validation in progress according to roadmap. | Physical validation; not a demonstrated installable release. |

Primary pinned sources:
[README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md),
[roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md),
[manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md),
[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

The published hardware route has macOS/a6700 2.00 records, not an established
Windows or exact-mainland-body compatibility result. RAM injection is R2 camera
execution even when subsequent commands only read storage. No such action was run.
The ordinary USB feature tool remains unpublished; complete write-loop acceptance
is pending. The proposed bundled feature release also needs reconciliation with
our independently gated English and FTP requirements.

Authored material is GPL-3.0-only. NOTICE explicitly excludes relicensing inherited
Pico portions from an upstream commit without an attached licence. No code,
payload, offset or licence was adopted. Source/binary equivalence remains unresolved.

Exact commands/results (CPython 3.13.12, Windows):

```powershell
git status --short --branch
git ls-remote https://github.com/xyzhangxin/sony-a6700-powerful.git refs/heads/main
git switch -c codex/a6700-reference-check-20261020-c
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-f -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-b/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-f/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-f/check_reference.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy'));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-f/record.py
git diff --check
```

Acquisition exit 0: four bounded public UTF-8 texts verified against Git tree;
exclusive receipts retained privately. No upstream code imported/executed or binary
downloaded. Browser GitHub page/API fetch failed; raw text and host Git/API succeeded.
Tests exit 0: 17 passes, zero failures/errors/skips, 1.636s. These mocked host FTP
policy regressions do not validate this upstream implementation, camera or server.
Historical full suites were not repeated for a documentation refresh.

Changed public files: this report, docs/BACKLOG.md, docs/FEATURE_PROGRESS.md,
research/STATE.json. Private state backed up before adding the reference result.
Existing untracked tools/dependency_adapter_sources.py and
tests/test_dependency_adapter_sources.py remain untouched and unstaged. Separate
RA-003 work, its pending review findings, phase and next work package are preserved.

Camera commands: **none**. No drivers/firmware changes, private-input upload,
firmware/constants/native payload read, upstream launcher, or device contact.
No feature support or recovery/device-write gate passed.

Next single reference work package: **FT-101: audit the published FTP implementation
and direct camera-to-server Wi-Fi evidence when available**, using the existing
[evidence checklist](20261019-a6700-powerful-recheck.md#ftp-evidence-checklist-for-the-next-source-only-package).
