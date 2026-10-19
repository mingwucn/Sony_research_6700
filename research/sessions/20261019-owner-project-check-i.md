# Owner-requested A6700 Powerful check i

2026-10-19. Topic branch: codex/a6700-reference-check-20261019i. Starting HEAD: 971c160.
Evidence: source-report, static-inference, offline-tested. Camera commands: none.

Fresh main remains `0c6294a83988f196adfc980de59f9a1d0b92e8e2`: unchanged from references/sources.lock.json and
the [previous whole-source audit](20261019-RA-003-a6700-powerful-audit.md).
Complete recursive tree: 51 entries, 39 blobs. Four immutable documents
verified against tree sizes and Git blob SHA-1; SHA-256 receipts retained privately.
This is a reference refresh, not a repeat source audit or independent device reproduction.

| Owner priority | Finding |
|---|---|
| English | No unlock found in the unchanged audited source or refreshed documentation. Mainland enablement remains unresolved. |
| Native FTP | Author reports settings and RAW+JPEG transfer tested on a6700 2.00. FTP implementation remains unpublished; direct Wi-Fi without a host relay, exact build, server-side equality and failure handling need evidence. |
| Rollback | Known-range backups are documented; full physical coverage and restoration explicitly remain unverified. |
| FL2/FL3 | Offline validation ongoing, device validation pending. Deferred behind English and FTP. |

Sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md),
[roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md),
[manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md),
[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

Published hardware access executes temporary camera RAM code: R2 under our policy,
even when subsequent storage commands only read. Documented target/platform is
a6700 2.00/macOS; exact mainland-body identity and Windows compatibility are unproved.
Ordinary USB unlock code remains unpublished; the new writer's complete write loop
and full restore remain pending. Bundled feature changes require separate scope review.
Authored material is GPL-3.0-only; NOTICE states that inherited Pico portions from
an upstream without a licence are not relicensed. Reuse rights and source/binary
correspondence remain unresolved. No code or payload adopted.

Exact host commands and results:

- `git status --short --branch`; `git log -1 --oneline`: exit 0. Initial branch codex/ra003-operational-scope, HEAD 971c160, nine previously staged files preserved.
- `git switch -c codex/a6700-reference-check-20261019i`: exit 0.
- `New-Item -ItemType Directory -Path private/sessions/20261019-owner-project-check-i -ErrorAction Stop`: success, exclusive folder.
- `Copy-Item -LiteralPath private/sessions/20261019-owner-project-check-h/check.py -Destination private/sessions/20261019-owner-project-check-i/check.py -ErrorAction Stop`: success; authored harness read before reuse.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-i/check.py`: exit 0. Seven bounded HTTPS GETs, no redirects/retries, 30-second timeout and 2 MiB response bound. Four immutable documents verified. CPython 3.13.12 / Windows AMD64. Mocked host FTP policy tests: 17/17 passed, zero failures/errors/skips, 1.837267s. These tests prohibit sockets; they do not test upstream FTP or a camera. Historical full suites not rerun.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-i/record.py`: saves this report and appends public/private notes with exclusive backups; all existing JSON values preserved.

The supplied main-tree browser URL failed; repository-root/raw browser reads and
the independent bounded API/raw harness succeeded. No binaries downloaded,
upstream tools executed, firmware/constants read, private inputs uploaded,
drivers changed or camera contacted. No feature, recovery or device-write gate passed.

Changed files: this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md,
docs/FEATURE_PROGRESS.md and research/STATE.json; ignored private session and feature
notes/receipts updated. Existing staged RA-003 work is preserved. Only this new report
is newly staged; appended shared-file notes remain unstaged to avoid restaging prior
work. No commit or push is made by this refresh. The source lock and active RA-003
phase/next implementation package remain unchanged.

Next single reference package: **FT-101: audit the FTP implementation and direct camera-to-server Wi-Fi evidence when published, including exact build identity, transfer equality, failure handling and reversal/recovery coverage.**
Prerequisite: publication of that implementation and reproducible evidence.
