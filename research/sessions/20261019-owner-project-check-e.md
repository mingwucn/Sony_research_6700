# Owner-requested A6700 Powerful check e

2026-10-19. Branch: codex/a6700-reference-check-20261019e. Starting HEAD: e05f1f1.
Evidence: source-report, static-inference, offline-tested. Camera commands: none.

Fresh main resolves to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the locked
[33-text / 12-Python source audit](20261019-RA-003-a6700-powerful-audit.md).
Complete recursive tree: 51 entries, 39 blobs. Four immutable documents
were verified by size and Git blob SHA-1; SHA-256 receipts retained privately.
This refresh does not repeat the prior whole-source audit or independently reproduce device claims.

| Owner priority | Finding |
|---|---|
| Native English | No unlock located in unchanged audited sources or refreshed documents. Mainland resources, restrictions and feasibility remain unresolved. |
| Native Wi-Fi FTP | Author reports a6700 2.00 FTP settings and RAW+JPEG transfer physically tested. Implementation is not published in this tree. Direct Wi-Fi without a relay, exact build hashes, server equality, security, persistence and failure handling remain unverified by us. |
| Rollback before firmware writes | Manual explicitly leaves physical eMMC size and complete restoration unverified. Partial range readback is not a proven rollback system. |
| FL2/FL3 | Offline validation ongoing; device validation pending. Deferred behind English and FTP. |

Sources at this immutable revision:
[README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md),
[development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md),
[manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md),
[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

The published hardware route uses Pico to inject and execute a temporary RAM program.
It is R2 here even though its storage operations are described as read-only.
Public device records are a6700 2.00/macOS; this does not prove our exact mainland
body/build or a Windows route. Ordinary USB unlocking remains unpublished; the
new write framework's full loop and complete backup/restoration remain unfinished.
The roadmap plans bundled features without individual selection, requiring a future scope review.

NOTICE labels authored material GPL-3.0-only but expressly excludes relicensing
inherited Pico portions from a pinned upstream without an attached licence.
Whole-chain reuse rights and source/binary correspondence remain unresolved.
No code or payload adopted, no agreement accepted and no new legal conclusion.

Commands and results, all host-side:

- `git status --short --branch`: six existing staged RA-003 documentation/state paths on codex/ra003-operational-delta; preserved.
- `git log -1 --oneline`: e05f1f1 feat: qualify invented clean child and parent reconciliation.
- `git switch -c codex/a6700-reference-check-20261019e`: exit 0; existing index carried unchanged.
- `New-Item -ItemType Directory -Path private/sessions/20261019-owner-project-check-e -ErrorAction Stop`: exclusive evidence folder, success.
- `Copy-Item -LiteralPath private/sessions/20261019-owner-project-check-d/check.py -Destination private/sessions/20261019-owner-project-check-e/check.py -ErrorAction Stop`: reviewed host-authored harness, success.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-e/check.py`: exit 0. Seven bounded HTTPS GETs, no redirects/retries, 30-second timeout and 2 MiB response bound. Ref, commit, complete tree and four immutable texts verified. No binary download.
- Same harness: standard-library `unittest.defaultTestLoader.discover('tests', pattern='test_ftps_client_policy.py')`: 17/17 passed, zero skips/errors/failures, 1.772284s. CPython 3.13.12 / Windows AMD64. Mocked host policy tests prohibit sockets; they do not validate upstream FTP, radio transport or a camera. Full historical suites not rerun for this source/documentation refresh.
- Web tree/main fetch failed; repository root and raw immutable texts succeeded. Host API requests supplied the fresh revision pin.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-e/record.py`: create this report, append external/internal progress and a new STATE observation with exclusive original-byte backups; all prior JSON values preserved.
- `git diff --check`; `git add -- research/sessions/20261019-owner-project-check-e.md`; `git diff --cached --check`: review/check new report only. Prior staged blobs preserved; new shared-note changes remain unstaged to avoid mixing the unfinished RA-003 package. No commit or push.

Changed public files: this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md,
docs/FEATURE_PROGRESS.md and research/STATE.json. Private session/feature notes
updated with backups. Source lock and source code unchanged; existing RA-003
phase/next package, staged content and all previous state observations preserved.
No camera contact, author message, upstream execution, driver/firmware change,
private upload, protected-input read or feature/recovery/write gate passed.

Next single reference work package: FT-101: source-only audit of the FTP implementation and direct camera-to-server Wi-Fi test evidence when published; establish exact build identity, source/payload correspondence, transfer equality, failure handling and reversal/recovery coverage before considering any device step.
Blocker: implementation and reproducible evidence are not yet published.
