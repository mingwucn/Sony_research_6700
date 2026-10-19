# Owner-requested A6700 Powerful source check c

2026-10-19. Branch `codex/a6700-reference-check-20261019c`; starting HEAD `12ff519`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh GitHub metadata pins main to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the [existing 33-text / 12-Python source audit](20261019-RA-003-a6700-powerful-audit.md). Recursive tree: 51 entries, 39 blobs. Four immutable documents match tree sizes and Git blob identities. Private receipts record SHA-256. No binaries acquired or upstream code executed.

| Priority | Finding |
|---|---|
| Native English | No unlock found in previously audited unchanged sources or refreshed documents. Mainland resource/configuration feasibility unresolved. |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG transfer physically verified on a6700 2.00. Implementation remains unpublished. Direct Wi-Fi/no-relay behavior, exact build hashes, server file equality, security, persistence and failure handling unverified by us. |
| Rollback prerequisite | Manual explicitly leaves complete physical storage coverage and restoration unverified. Existing range readback does not establish recovery. |
| FL2/FL3 | Offline validation underway; physical validation pending. Remains deferred. |

Sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md), [roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

Published device records cover a6700 2.00/macOS; our exact mainland body/build and Windows route remain unverified. Pico-assisted RAM Fastboot entails temporary camera execution (R2), requiring separate exact-step authorization. The roadmap says deployment bundles features rather than providing individual selection; any future package needs scope review before use.

Authored material is marked GPL-3.0-only. NOTICE excludes relicensing inherited Pico portions from an upstream commit lacking an attached licence. Whole-chain reuse rights and binary/source correspondence remain unresolved; no code or payload adopted.

## Commands and results

- `git status --short --branch`: inherited branch `codex/ra003-collected-controller`, two untracked unfinished controller files; preserved untouched.
- `git log -1 --oneline`: `12ff519 docs: record complete collected host dependency runtime observation`.
- `git switch -c codex/a6700-reference-check-20261019c`: exit 0.
- `New-Item -ItemType Directory -Path private/sessions/20261019-owner-project-check-c -ErrorAction Stop`: exclusive evidence folder, exit 0.
- `Copy-Item -LiteralPath private/sessions/20261019-owner-project-check-b/check.py -Destination private/sessions/20261019-owner-project-check-c/check.py -ErrorAction Stop`: reviewed host-authored harness copied, exit 0.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-c/check.py`: exit 0. Seven bounded HTTPS GETs; no redirects/retries, 2 MiB per response, 30-second timeout. Four documents verified. CPython 3.13.12 / Windows AMD64. `unittest.defaultTestLoader.discover('tests', pattern='test_ftps_client_policy.py')`: **17/17 passes**, zero skips, 1.598589000001084 seconds wrapper. These mocked host policy tests prohibit sockets; they do not validate upstream FTP or any camera.
- Web tree/API opens failed; raw text retrieval succeeded. The host API harness supplied the immutable pin and verification.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-c/record.py`: this documentation/internal-note update, preserving all prior STATE keys and exclusive private original-byte backups.
- Explicit file staging and `git diff --cached --check` required before commit; no full-suite rerun for this documentation-only check. Earlier full-suite results remain historical.

Changed public files: this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md, research/STATE.json. Private session and feature notes updated after backup. Source lock and existing RA-003 phase/next package unchanged. No author contact, uploads, driver/firmware changes, native payload read/execution or camera contact. Camera commands: **none**. No feature supported, recovery proved or device-write gate passed.

Next single reference work package: **FT-101: assess published FTP implementation, direct camera-to-server Wi-Fi evidence and reversal/recovery coverage when available, source-only**. Publication is the missing prerequisite.
