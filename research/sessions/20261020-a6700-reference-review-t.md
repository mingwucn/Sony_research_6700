# A6700 Powerful: current source review

2026-10-20; topic branch `codex/a6700-reference-check-20261020-t`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh GitHub API resolution pins main at `2de85f1cca89b0e20ee25a70f93e04c3d34e10e5`. The full recursive tree matches review s: **51 entries, 39 blobs, zero changed paths**. README, development plan, manual and NOTICE were freshly fetched as text and verified against their pinned Git blob IDs and sizes. Source lock already matches; it is unchanged. Earlier [full source audit](20261019-RA-003-a6700-powerful-audit.md) remains applicable to unchanged implementation blobs. This is a fresh delta/document review, not a new complete source audit.

| Priority | Finding | Remaining evidence |
|---|---|---|
| Native English | No unlock found in reviewed source/docs; no implementation delta | Exact mainland language policy/resource mapping and reversible candidate |
| Native Wi-Fi FTP | Author reports a6700 2.00 FTP settings and RAW+JPEG double transfer physically tested | Implementation unpublished; direct camera-to-server Wi-Fi, file equality, security, lifecycle and failure behavior unverified by us |
| Rollback prerequisite | Public route provides a temporary RAM Fastboot reader and known-range backup | Full physical storage coverage, complete restore and official firmware rescue unproved |
| FL2/FL3, deferred | Author describes offline validation, physical validation pending | No verified install; keep English/FTP first |

Published physical records are scoped to macOS; neither our Windows host nor this owner's exact mainland body/build is independently qualified. Displayed 2.00 does not prove binary identity. Public hardware access involves temporary native camera execution, not ordinary USB identification. The ordinary USB unlock tool remains under preparation, and the new execution framework's complete write loop awaits acceptance. Planned bundled feature updates do not establish separately gated feature safety.

The [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/开发计划与进展.md) supplies the FTP claim and explicitly leaves complete backup/restore unfinished. The [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/操作手册.md) describes the RAM route. [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/NOTICE) assigns GPL-3.0-only to authored work but excludes relicensing inherited Pico code from the named upstream commit without an attached licence. Whole-chain reuse rights and source/binary correspondence remain unresolved. No code, target offsets or payload adopted.

## Exact host commands and results

```powershell
git status --short
git branch --show-current
git switch -c codex/a6700-reference-check-20261020-t
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-t -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-s/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-t/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-t/check_reference.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-t/record_review.py
```

Acquisition: exit **0**, six bounded public metadata/text GETs, four documents blob/size verified. No binary download. The web tree URL returned a cache miss; repository/raw/document views and host API/text GETs succeeded. A local lookup used a nonexistent historical filename before the correct report was selected; no device or upstream operation was retried. The acquisition receipt's legacy `unchanged_from_prior_audit` compares with older 0c6294a; private `delta.json` is the explicit comparison with review s.

Recording/qualification: exit **0**, **17/17** standard-library mocked host FTPS policy tests pass, zero failures/errors/skips, **2.050s** wrapper. Interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython **3.13.12**, Windows AMD64, isolated flags above. The authored recorder inserts repository/tests paths, uses `unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy')` and TextTestRunner verbosity 2; raw log/result retained privately. No socket/listener, no upstream behavioral qualification and no camera validation. No broad historical suite rerun for this documentation-only change. Seven existing public/private notes were backed up before updates; internal feature/session notes synchronized.

Changed public files: this report, `research/STATE.json`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`. The two pre-existing untracked `research/OBSERVATION_GO_NO_GO.md` and `research/sessions/20261020-RA-003-observation-go-no-go.md` were preserved and excluded from staging. No production/test implementation changed. Explicit staging/publication commands:

```powershell
git diff --check
git add -- research/sessions/20261020-a6700-reference-review-t.md research/STATE.json docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md
git diff --cached --stat
git diff --cached --check
git diff --cached
git commit -m "docs: review current a6700 reference FTP and recovery claims"
git status --short --branch
```

Camera commands: **none**. No private input upload, firmware/constants/native payload read, upstream execution, dependency installation or driver/firmware change. No feature marked supported and no recovery or device-write gate passed.

Next single reference work package: **FT-101: audit the published FTP implementation and direct camera-to-server Wi-Fi evidence when available, including exact target/region identity, file equality, security, persistence, failure handling and reversal.** Existing RA-003 continuation remains pending; this reference check does not complete that engineering package.
