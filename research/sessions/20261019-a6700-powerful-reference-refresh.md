# A6700 Powerful reference refresh

2026-10-19. Branch `codex/a6700-powerful-reference-refresh`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

The user requested a check of `xyzhangxin/sony-a6700-powerful`. GitHub main resolves to the already audited `0c6294a83988f196adfc980de59f9a1d0b92e8e2`; no new revision was adopted. The previous [33-text-file source audit](20261019-RA-003-a6700-powerful-audit.md) remains applicable. This refresh retrieved only commit metadata and four commit-pinned text documents: README, development plan, manual and NOTICE. Each received a private size/SHA-256 receipt. No launcher, upstream Python, build, native payload or firmware was executed or downloaded.

| Goal | Current evidence and limit |
|---|---|
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG transfers physically verified on a6700 2.00. Public implementation and reproducible transfer/backend evidence remain absent from the inspected revision. This is a promising source-report, not our validated native Wi-Fi/relay-independent result. |
| Native English | No English unlock located in the previously inspected tree; the refreshed documents add none. Mainland build compatibility remains unproved. |
| FL2/FL3 | Upstream reports offline validation in progress and physical validation pending. Deferred locally. |
| Rollback | Complete backup/restoration and official-firmware recovery explicitly remain future work. Published partial readback does not establish recovery after a failed write. |

The ordinary USB route and full write-loop framework are still awaiting publication/completion. README's recorded camera environment is a6700 2.00/macOS; it does not establish our Windows/mainland body compatibility. Upstream's all-feature incremental release plan also differs from our separately gated features; adopt no bundle without per-feature evidence.

Authored code/docs are labelled GPL-3.0-only. NOTICE excludes relicensing the inherited Pico source, whose pinned upstream lacks a licence. No code/payload is adopted or redistributed. Component rights and source/binary equivalence remain prerequisites.

## Commands and results

Host: Windows AMD64; CPython 3.13.12 at `C:\ProgramData\miniconda3\python.exe`.

- `git status --short`: clean tracked tree before work.
- `git branch --show-current`: `codex/ra003-parent-child-composition` before this narrowly scoped refresh. Existing ignored research evidence preserved.
- `git switch -c codex/a6700-powerful-reference-refresh`: exit 0.
- Host-authored standard-library Python via `python.exe -I -S -B -X utf8 -`: GET GitHub API `/repos/xyzhangxin/sony-a6700-powerful/commits/main`, then four raw text URLs pinned to the returned commit; save exclusive new private session directory and hash bytes. Exit 0. The reviewed SHA is unchanged. Web reader also checked README, plan and NOTICE; the initial GitHub tree web open failed, then raw text reads succeeded. No binary request or camera action.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));raise SystemExit(not r.wasSuccessful())"
```

**228 cases: 225 passed, 3 skipped; exit 0; 20.080s suite / 20.600405399978627s wrapper.** These are our ordinary synthetic tests, not upstream tests or hardware validation. Private raw logs preserve skip reasons. No implementation changed. Source lock is unchanged. JSON parsing, document diff review and `git diff --check` validate the documentation changes.

Changed tracked files: this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `research/STATE.json`. Private receipt/logs and an additive continuity entry are ignored; existing private state is backed up before updating.

Camera commands: **none**. No private input upload, firmware/native input read, device transition, driver change, write, or automatic follow-up schedule. English/native FTP support, recovery and device-write gates remain false.

## Next single work package

**FT-101: prepare a source-only FTP evidence checklist against this pinned revision, covering the unpublished implementation, exact firmware identities, native Wi-Fi transport without a relay, server-side RAW/JPEG integrity, failure behavior and reversal.** No camera operation or author message is authorized by that package. Existing RA-003 composition work remains separate and its stored status is not promoted by this reference refresh.
