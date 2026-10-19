# A6700 Powerful: requested project check

2026-10-19. Topic branch `codex/a6700-powerful-review-refresh`; starting HEAD `a64402901b4169bd734a67490bba06ff92835190`, clean tracked tree. Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh GitHub main resolves to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the [earlier 33-text source audit](20261019-RA-003-a6700-powerful-audit.md). Recursive tree metadata has 51 entries. Four commit-pinned texts (README, development plan, manual, NOTICE) passed byte-size and Git blob identity checks; SHA-256 receipts remain private. No new full code audit was needed for this unchanged revision. No upstream code was imported or executed, and no binary payload was downloaded.

| Owner goal | Finding | Remaining prerequisite |
|---|---|---|
| Native English, primary | No English unlock found in the earlier audited implementation; refreshed documents add none. | Matching mainland resources/restriction analysis and reversible implementation. |
| Native Wi-Fi FTP, primary | Author reports FTP settings and RAW+JPEG transfer physically verified on a6700 2.00. | Public implementation, matching build/region, direct camera-to-server Wi-Fi evidence, file integrity, persistence and failure behavior. |
| Rollback before writes | Public route covers bounded storage reads; complete restore remains explicitly unverified. | Exact-body backup coverage, independent copies, inverse and demonstrated recovery envelope. |
| FL2/FL3, deferred | Offline validation reported; physical validation pending. | No validated installable result established. |

The [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md) distinguishes unpublished development from installable releases. Ordinary-USB tools and complete write-loop acceptance remain pending. Its FTP report is a useful exact-model/version lead, not independently reproduced support on this mainland body.

The [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md) scopes records to 2.00/macOS. Its read route temporarily executes an injected RAM program, requiring separate R2 approval here. Published storage coverage does not establish whole-device backup or rollback. No route was adopted or attempted.

[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE) states GPL-3.0-only for authored material and expressly excludes relicensing inherited Pico portions from an upstream revision without an attached licence. Whole-chain reuse permissions and source/binary correspondence remain unresolved. No implementation or payload was integrated or redistributed; source lock remains unchanged.

## Exact commands and results

Interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython 3.13.12, Windows AMD64.

```powershell
git status --short
git branch --show-current
git rev-parse HEAD
git switch -c codex/a6700-powerful-review-refresh
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-a6700-powerful-review-refresh/check_reference.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));raise SystemExit(not r.wasSuccessful())" *> private/sessions/20261019-a6700-powerful-review-refresh/host-tests.log
git diff --check
```

All exited **0**. Initial branch was `codex/ra003-binding-basis-diagnostic`; its unfinished private work was preserved. The reference script GETs GitHub `/commits/main`, the commit's recursive tree and the four commit-pinned texts; it saves new files exclusively. Metadata/identity checks passed. Initial browser tree/API opens failed; raw text and host API requests succeeded.

Host suite: **228 tests, 225 passes, three skips**, **18.019s**, exit **0**. These are authored synthetic host regressions, not upstream behavioral tests, private diagnostic qualification or camera validation. Skips cover POSIX fork inheritance and two Windows symlink cases. No executable source changed.

JSON/report/gate checks passed. An auxiliary saved-log reader initially used UTF-16 and refused the UTF-8 log (exit 1); correcting the reader verified the same saved 228-case result without repeating tests. Reviewed staged paths/content and `git diff --cached --check` passed.

Changed tracked files: this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `research/STATE.json`. Internal session/feature notes updated after exclusive byte-preserving backups. Separate RA-003 phase and its next package remain unchanged; its diagnostic was not run in this reference review.

Camera commands: **none**. No private upload, camera contact, driver/firmware change, target offsets, feature support, recovery proof or device-write gate passed.

Next single reference work package: **FT-101: assess published FTP implementation and direct camera-to-server Wi-Fi evidence against the [saved checklist](20261019-a6700-powerful-recheck.md#ftp-evidence-checklist-for-the-next-source-only-package) when available.** Missing publication/evidence remains a blocker. No author contact performed.
