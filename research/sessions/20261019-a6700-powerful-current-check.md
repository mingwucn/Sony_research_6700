# A6700 Powerful: current reference check

2026-10-19. Branch `codex/a6700-powerful-current-check`, starting HEAD `adae041` and clean tracked tree. Evidence: **source-report**, **static-inference**, **offline-tested**. No independently reproduced camera result.

GitHub main still resolves to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`. Complete tree metadata (51 entries) and four commit-pinned documents were retrieved: README, development plan, manual and NOTICE. Each text's byte size and Git blob identity matches the tree; private SHA-256 receipts retained. No revision or source-lock change. The earlier [33-text source audit](20261019-RA-003-a6700-powerful-audit.md) and [FTP evidence checklist](20261019-a6700-powerful-recheck.md) remain applicable. This check did not repeat the complete source audit.

| Owner priority | Finding | Remaining prerequisite |
|---|---|---|
| English | No English unlock found in the earlier audited source; current documents add none. | Mainland-specific resource/configuration evidence and reversible implementation. |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG double transfer physically working on a6700 2.00. | Published implementation, direct camera-to-server Wi-Fi evidence, exact firmware/region bindings, integrity/security and lifecycle behavior. |
| Rollback | Public manual describes bounded backup reads; complete restoration is explicitly unverified. | Verified backup coverage and demonstrated recovery envelope before any write. |
| FL2/FL3, deferred | Author describes offline work with physical validation pending. | No available validated installation established. |

Sources: [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

The documented route runs injected camera RAM code through Pico/service access. A read-only storage command still involves temporary native execution; it does not become ordinary identification. Device records are scoped upstream to 2.00/macOS, without proof of this mainland body's binary identity or Windows readiness. No route adopted or executed here.

NOTICE covers authored code/docs with GPL-3.0-only, while expressly declining to relicense original inherited Pico material from an upstream revision without an attached licence. Whole-chain reuse rights and source-to-binary correspondence remain unresolved. No third-party implementation or payload copied into tracked files.

## Commands and results

Host: Windows AMD64, CPython 3.13.12 at `C:\ProgramData\miniconda3\python.exe`.

- `git status --porcelain`: clean initially; exit 0.
- `git switch -c codex/a6700-powerful-current-check`: exit 0.
- Host-authored standard-library stdin script under `C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -`: GET `https://api.github.com/repos/xyzhangxin/sony-a6700-powerful/commits/main`, then `/git/trees/0c6294a83988f196adfc980de59f9a1d0b92e8e2?recursive=1`, then raw commit-pinned README, development plan, manual and NOTICE. Exit 0; exact URLs, sizes and hashes saved privately. No binary requests. Initial web-reader tree/API attempts failed; root/raw document views and host metadata requests succeeded.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));raise SystemExit(not r.wasSuccessful())" *> private/sessions/20261019-a6700-powerful-current-check/host-tests.log
```

Exit **0**; **228 cases, 225 passes, three skips**, **18.382s**. These are ordinary synthetic host regressions, not upstream behavioral tests, private gate composition or camera validation. No executable code changed. JSON parsing and `git diff --check` pass.

Changed tracked files: this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `research/STATE.json`. Private session and feature continuity updated after preserving their original bytes. Separate RA-003 operational reconciliation remains pending; its diagnostic was not run during this reference check. Previously received review findings remain unresolved and no chain authority was promoted.

Camera commands: **none**. No private upload, camera contact, driver/firmware change, upstream execution, native payload download or feature/write/recovery gate passed.

Next single work package for this lead: **FT-101: assess published FTP implementation and direct transfer evidence against the saved source-only checklist when available**. Publication/evidence remains missing; no author contact authorized or performed.
