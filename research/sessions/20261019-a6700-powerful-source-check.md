# A6700 Powerful: source and feature check

2026-10-19. Branch `codex/a6700-powerful-source-check`; starting HEAD `3ffbab5`, clean tracked tree. Evidence: **source-report**, **static-inference**, **offline-tested**.

Live main resolves to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the [33-text-file audit](20261019-RA-003-a6700-powerful-audit.md). Complete recursive tree metadata has 51 entries. Fresh commit-pinned README, development plan, manual and NOTICE all match their Git blob identities and sizes. Private acquisition receipts retain exact URLs and SHA-256. The source lock is unchanged; this refresh does not repeat the full code audit.

| Owner goal | Finding | Remaining blocker |
|---|---|---|
| Native English, primary | Earlier audited source contains no located unlock; refreshed documents add none. | Matching mainland resources/restriction evidence and a reversible candidate. |
| Native Wi-Fi FTP, primary | Author reports FTP settings and RAW+JPEG transfer physically working on a6700 2.00. | Implementation remains unpublished in this tree; direct Wi-Fi/no-relay evidence, integrity, regional applicability and lifecycle behavior remain unverified here. |
| Rollback before writes | Manual describes bounded backup reads; full restoration is explicitly unverified. | Exact-body backup coverage and demonstrated recovery envelope. |
| FL2/FL3, deferred | Author reports offline validation, physical validation pending. | No validated installation inferred. |

Sources: [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

The published route uses Pico hardware to inject temporary camera RAM code. Read-only storage operations still require temporary native execution (R2). The recorded platform is a6700 2.00/macOS; this does not establish this mainland body's binary identity or Windows readiness. No route adopted or executed.

NOTICE states GPL-3.0-only for authored material but expressly excludes relicensing inherited Pico portions from an upstream revision without an attached licence. Whole-chain reuse and source/binary correspondence remain unresolved. No implementation or payload copied into tracked files.

## Commands and results

Host interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12, Windows AMD64.

- `git status --short --branch`, `git log -3 --oneline`: exit 0; tracked tree initially clean.
- `git switch -c codex/a6700-powerful-source-check`: exit 0.
- Host-authored standard-library stdin script under `python.exe -I -S -B -X utf8 -`: HTTPS GET `/repos/xyzhangxin/sony-a6700-powerful/commits/main`, then `/git/trees/<resolved-commit>?recursive=1` at `api.github.com`; four raw documents fetched at the resolved commit. Size/Git-blob checks pass, exit 0. Metadata and text only; no binary request. Initial web `/tree/main` failed; repository-root/raw views succeeded.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));raise SystemExit(not r.wasSuccessful())" *> private/sessions/20261019-a6700-powerful-source-check/host-tests.log
```

Exit **0**, **228 cases: 225 passes, three skips**, **21.596s**. Ordinary host synthetic regressions only; no upstream or camera behavioral tests, private chain qualification or new executable code. JSON parsing and `git diff --check` pass.

Changed tracked files: this report, `research/STATE.json`, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`. Internal session/feature notes updated after exclusive byte-preserving backups. Prior RA-003 phase and next package remain unchanged; its unfinished private work is not promoted.

Camera commands: **none**. No upstream execution, private upload, camera/driver/firmware change or feature/recovery/write gate passed.

Next single reference work package: **FT-101: assess published FTP implementation and direct-transfer evidence against the [saved checklist](20261019-a6700-powerful-recheck.md#ftp-evidence-checklist-for-the-next-source-only-package) when available.** Publication is missing; no author contact performed or authorized.
