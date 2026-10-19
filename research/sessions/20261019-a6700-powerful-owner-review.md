# A6700 Powerful: owner-requested reference review

2026-10-19. Branch `codex/a6700-powerful-owner-review`, starting HEAD `d25117a`, clean tracked tree. Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh main resolves to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from our [33-text source audit](20261019-RA-003-a6700-powerful-audit.md). Recursive tree metadata has 51 entries. README, development plan, manual and NOTICE were fetched at the exact commit; all four byte sizes and Git blob identities verified. SHA-256 receipts are private. This refresh does not repeat the full code audit. Source lock unchanged.

| Goal | Finding | Missing evidence |
|---|---|---|
| Native English, primary | No unlock found in earlier audited source; refreshed documents add none. | Matching mainland resources/restriction analysis and reversible implementation. |
| Native Wi-Fi FTP, primary | Author reports FTP settings and RAW+JPEG transfers physically working on a6700 2.00. | Published patch/backend, direct Wi-Fi/no-relay receipts, regional applicability, integrity and lifecycle behavior. |
| Rollback prerequisite | Published backup route covers bounded storage ranges. Full restoration remains explicitly unverified. | Exact-body backup coverage and demonstrated recovery envelope before writes. |
| FL2/FL3, deferred | Offline work reported, device validation pending. | No validated installable result established. |

Sources: [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

The public route uses Pico hardware and executes an injected program in camera RAM, even for storage reads. Under this project's rules it requires R2 authorization. Upstream records are scoped to 2.00/macOS, without proof of this mainland body's binary identity or Windows readiness. No route adopted or executed. A claimed successful feature does not establish a safe installation or a proven rollback system.

NOTICE grants GPL-3.0-only for authored material while expressly declining to relicense inherited Pico portions from an upstream revision lacking an attached licence. Whole-chain permissions and source/binary correspondence remain unresolved. No third-party implementation or payload integrated or redistributed.

## Commands and results

Interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12, Windows AMD64.

- `git status --short` and `git branch --show-current`: exit 0; clean tracked tree on `codex/ra003-v6-saved-reconciliation`.
- `git switch -c codex/a6700-powerful-owner-review`: exit 0.
- Host-authored stdin script under `C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -`: GET `https://api.github.com/repos/xyzhangxin/sony-a6700-powerful/commits/main`, then `/git/trees/0c6294a83988f196adfc980de59f9a1d0b92e8e2?recursive=1`, then the four texts from `https://raw.githubusercontent.com/xyzhangxin/sony-a6700-powerful/0c6294a83988f196adfc980de59f9a1d0b92e8e2/` with UTF-8-escaped filenames. Size/blob checks passed; exit 0. Metadata and source text only. Initial web tree view failed; repository-root/raw views and host requests succeeded.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));raise SystemExit(not r.wasSuccessful())" *> private/sessions/20261019-a6700-powerful-owner-review/host-tests.log
```

Exit **0**: **228 tests, 225 passes, three skips**, **18.695s**. Ordinary authored host synthetic regressions only, not upstream behavior, private gate qualification or camera validation. No executable source changed. JSON/link checks and `git diff --check` passed before staging.

Changed tracked files: this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `research/STATE.json`. Private session/feature notes updated after exclusive byte-preserving backups. Unfinished separate RA-003 private work and its publication state are not promoted by this refresh.

Camera commands: **none**. No private input upload, firmware/native payload download or execution, driver change, camera contact, or feature/recovery/device-write gate passed.

Next single reference package: **FT-101: review published FTP implementation and direct camera-to-server Wi-Fi evidence against the [saved checklist](20261019-a6700-powerful-recheck.md#ftp-evidence-checklist-for-the-next-source-only-package) when available.** Missing publication/evidence remains a blocker. No author contact performed or authorized.
