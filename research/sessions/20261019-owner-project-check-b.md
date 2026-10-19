# Owner-requested A6700 Powerful project check

2026-10-19. Branch `codex/a6700-project-review-20261019b`; starting HEAD
`0e1277ca8ef9515d74de22cf40e35f527ecc2db8`, tracked tree clean.
Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh GitHub ref/commit/tree metadata confirms main remains
`0c6294a83988f196adfc980de59f9a1d0b92e8e2`: 51 tree entries / 39 blobs.
Four immutable documents match tree sizes and Git blob identities; SHA-256
receipts remain private. This refresh reuses the unchanged implementation's
[existing source audit](20261019-RA-003-a6700-powerful-audit.md), without rerunning
upstream code or claiming independent camera reproduction.

| Owner priority | Finding and implication |
|---|---|
| Native English first | No English unlock located in the unchanged audited source or refreshed documents. Mainland resource/configuration feasibility remains unresolved. |
| Native Wi-Fi FTP first | The author reports FTP settings and RAW+JPEG double transfer physically verified on a6700 2.00. Implementation is not in the public tree. Direct Wi-Fi/no-relay behavior, exact target hashes, file equality, security, persistence and failure handling still require evidence. |
| Rollback prerequisite | The manual explicitly leaves physical storage coverage and complete restoration unverified. Range readback is not a proven rollback system. |
| FL2/FL3 deferred | Roadmap reports offline validation underway and physical validation pending. No ready installation established. |

Sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md),
[roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md),
[manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md),
[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

Published device records are scoped to a6700 2.00/macOS. Displayed version matches
the owner's report, but exact mainland build and Windows compatibility remain
unverified. The public backup route uses Pico-assisted temporary RAM Fastboot
execution: R2 under our policy, requiring a separate exact-step device decision.
No instructions were executed. Bundled feature deployment also needs review
against our separate English/FTP acceptance and recovery requirements.

NOTICE assigns GPL-3.0-only to authored material while excluding relicensing of
inherited Pico portions whose pinned upstream lacks an attached licence. Whole
dependency-chain reuse rights and binary/source correspondence remain unresolved.
No third-party implementation, binary or payload was adopted or redistributed.

## Commands and results

- `git status --short --branch`: clean tracked tree on
  `codex/ra003-runtime-packet-preparation` before this review.
- `git switch -c codex/a6700-project-review-20261019b`: exit 0.
- `New-Item -ItemType Directory -Path private/sessions/20261019-owner-project-check-b -ErrorAction Stop`:
  exclusive new private evidence directory, exit 0.
- `Copy-Item -LiteralPath private/sessions/20261019-owner-source-recheck/check.py -Destination private/sessions/20261019-owner-project-check-b/check.py -ErrorAction Stop`:
  existing host-authored acquisition/test harness copied, exit 0.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-b/check.py`:
  exit 0; seven HTTPS GETs, 2 MiB bound each, 30-second timeout, redirects refused,
  no retries, four documents verified. No binary downloads. CPython 3.13.12,
  Windows AMD64. Existing mocked host FTP policy tests: **17/17 passed**, zero
  skips, **1.7336670000222512s** wrapper. The harness runs
  `unittest.defaultTestLoader.discover('tests', pattern='test_ftps_client_policy.py')`.
  These prohibit socket creation and do not test upstream FTP or the camera.
- Web text retrieval refreshed the same documents; initial GitHub tree/API web
  opens failed, while bounded host API acquisition succeeded. A local optional
  read of nonexistent `research/EXTERNAL_A6700_REVIEW.md` returned no content;
  the existing audit was found using `rg --files`.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-b/record.py`:
  writes only this report and progress notes; verifies all preexisting STATE keys
  remain unchanged. Explicit staged paths/content reviewed and
  `git diff --cached --check` required before commit. No full-suite rerun for this
  documentation-only review; previous 619-case qualification remains historical.

Changed public files: this report, BACKLOG, HANDOFF, FEATURE_PROGRESS and STATE.
Internal session notes updated after an exclusive original-byte backup.
Unfinished private runtime-packet preparation is preserved and not executed.
Source lock, RA-003 phase/next package and all feature/recovery/write gates remain
unchanged. Camera commands: **none**. No author contact, private-input upload,
upstream execution, driver/firmware change or dependency activation.

Next single reference package: **FT-101: assess published FTP implementation,
direct camera-to-server Wi-Fi evidence and reversal/recovery coverage when
available, source-only**. Publication is the outstanding prerequisite.
