# Owner-requested A6700 Powerful recheck

2026-10-19. Branch `codex/a6700-source-check-20261019`; starting HEAD `dd9bf3c`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh main-ref, commit and recursive-tree metadata confirm
`0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the source lock and
[earlier 33-text / 12-Python source audit](20261019-RA-003-a6700-powerful-audit.md).
The tree has 51 entries / 39 blobs. Four freshly acquired immutable documents
(README, roadmap, manual, NOTICE) match tree sizes and Git blob identities.
Private SHA-256 receipts retain exact requests and results. This is an identity
and claims refresh, not a repeated full implementation audit or reproduction.

| Owner goal | Current assessment |
|---|---|
| Native English, primary | No unlock found in the unchanged audited source/current documents. Mainland resources and language configuration remain unresolved. |
| Native Wi-Fi FTP, primary | Author reports FTP settings and RAW+JPEG transfer physically verified on a6700 2.00. Implementation remains unpublished; direct Wi-Fi/no-relay evidence, exact-target identities, file equality, persistence, security and failure behavior remain to assess. |
| Rollback before writes | Public route reads selected storage ranges after temporary camera RAM execution. Physical storage coverage and complete restoration remain explicitly unverified. This does not satisfy the owner's rollback prerequisite. |
| FL2/FL3, deferred | Roadmap reports offline validation underway, physical validation pending. |

The [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md)
limits device records to a6700 2.00/macOS. Matching version text does not establish
the owner's mainland build or Windows-host compatibility. The
[manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md)
describes Pico-assisted RAM Fastboot execution: R2 under this project's policy,
requiring a separate exact-step decision. Subsequent read-only operations do not
make that entry ordinary identification. No instructions were executed.

The [roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md)
includes unpublished work, bundled feature deployment and an unfinished complete
write/restore workflow. These require review against our separate English/FTP
and recovery gates. [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE)
assigns GPL-3.0-only to authored material but explicitly excludes relicensing
inherited Pico portions from an upstream revision without an attached licence.
Whole-chain reuse rights and binary/source correspondence remain unresolved;
no implementation adopted or redistributed.

## Commands and results

- `git status --short --branch`: four inherited modified dependency modules and
  one untracked dependency test preserved; no staged paths. HEAD `dd9bf3c`.
- `git switch -c codex/a6700-source-check-20261019`: exit 0.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-source-recheck/check.py`:
  exit 0. Existing host-authored source-check script copied into a new exclusive
  ignored session directory. Seven HTTPS GETs (main ref, commit, tree, four
  immutable documents), 2 MiB per-response limit, 30-second timeout, redirects
  refused, no retries. Four documents verified; no binaries acquired.
- The same script inserts the repository root, then runs
  `unittest.defaultTestLoader.discover('tests', pattern='test_ftps_client_policy.py')`
  with `unittest.TextTestRunner(stream=log, verbosity=2)`:
  **17/17 passed**, zero skips, exit **0**, **1.6672659000032581s** wrapper,
  CPython **3.13.12**, Windows AMD64. These mocked host policy tests prohibit
  socket creation; they do not validate upstream FTP or camera behavior.
  Full suite not rerun for this documentation-only refresh. Inherited unfinished
  dependency edits are not qualified by this test run.
- JSON preservation validation and `git diff --cached --check`: exit 0 before
  commit. Explicit paths and staged content reviewed; no inherited code staged.

Changed public files: this report, BACKLOG, HANDOFF, FEATURE_PROGRESS and STATE.
Internal private session notes updated after exclusive byte-for-byte backup.
Source lock, RA-003 phase/next package, feature gates and latest full-suite result
remain unchanged. Initial web `/tree/main` failed; repository-root, raw text and
GitHub API retrieval succeeded. An initial PowerShell `rg` wildcard-path query
refused invalid path syntax; source lock was read directly afterward.

Camera commands: **none**. No upstream execution, dependency/native activation,
firmware/private-input inspection or upload, author contact, driver/firmware
change, feature-support claim or recovery/device-write gate passed.

Next single reference work package: **FT-101: assess published FTP implementation,
direct camera-to-server Wi-Fi evidence and reversal/recovery coverage when
available; source-only, no camera contact.** Publication remains a prerequisite.
Separate unfinished RA-003 dependency work remains preserved.
