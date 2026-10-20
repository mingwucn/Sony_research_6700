# A6700 Powerful: owner-requested recheck

2026-10-20; branch `codex/a6700-reference-check-20261020-s`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh GitHub API lookup pins main at `2de85f1cca89b0e20ee25a70f93e04c3d34e10e5`. All 51 recursive tree entries, including 39 blobs, match review r. Four README/plan/manual/NOTICE documents were freshly fetched as text and verified against their Git blob IDs and sizes. No changed implementation to audit. The source lock already pins this revision and remains unchanged. The acquisition script's legacy `unchanged_from_prior_audit` field compares against the older 0c6294a audit; the explicit current-baseline comparison is in private delta.json.

| Owner goal | Findings | Blocker |
|---|---|---|
| Native English, first priority | No unlock located in reviewed source/docs; unchanged from full source audit. | Mainland language restriction/resource mapping and reversible exact-target candidate. |
| Native Wi-Fi FTP, first priority | Author reports FTP settings with RAW+JPEG physically tested on a6700 2.00. | Feature implementation still unpublished; no independent direct Wi-Fi/server evidence, file equality, security, persistence or failure/reversal qualification. |
| Rollback | Public hardware route injects a temporary RAM Fastboot reader, not ordinary identification. Known storage ranges were reportedly read. | Entire physical storage coverage, complete restoration and official-firmware rescue remain unverified. |
| FL2/FL3, deferred | Offline validation underway; physical verification pending. | No validated installation; do not delay English/FTP. |

Physical records are scoped to macOS, not our Windows host or independently identified mainland body. A displayed 2.00 version does not establish binary compatibility. The ordinary USB unlock tool remains in preparation, with complete execution-framework write-loop acceptance pending. Its planned bundled feature release does not satisfy our separately gated change policy by itself.

NOTICE states GPL-3.0-only for authored code/docs and expressly excludes relicensing inherited Pico source from an upstream commit without an attached licence. Whole-chain reuse and source/binary correspondence are unresolved. Reference summaries only; no code, payload or target offsets adopted.

Pinned sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/README.md), [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/2de85f1cca89b0e20ee25a70f93e04c3d34e10e5/NOTICE). Earlier [full source audit](20261019-RA-003-a6700-powerful-audit.md) remains applicable to unchanged source blobs.

Commands/results (host only):

```powershell
git status --short --branch
git switch -c codex/a6700-reference-check-20261020-s
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-s -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-r/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-s/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-s/check_reference.py
```

Acquisition exited 0: six bounded public metadata/text GETs; no binaries. Public web tree fetch failed; raw text and host API/text GETs succeeded. The host-authored comparison/test block and recording block ran through PowerShell here-strings piped to this exact interpreter command:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -
```

Comparison asserted zero changed paths against review r. Test block explicitly inserted `.` and `tests` into sys.path and used `unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy')` with TextTestRunner verbosity 2; raw tests.log/tests.json retained privately. Results: **17/17 pass**, zero failures/errors/skips, exit **0**, **1.976s** wrapper. Interpreter: CPython **3.13.12**, Anaconda Windows AMD64. These standard-library mocked host policy tests create no socket/listener and do not validate upstream camera functionality. No broad historical suite rerun for this documentation-only review. Recording block backed up six existing public/private notes before updating, exit 0.

Initial branch `codex/ra003-observation-composition` contained two tracked edits to `tools/dependency_observation_launcher.py` and `tests/test_dependency_observation_launcher.py`. They were preserved, excluded from staging and neither executed nor qualified in this reference review. Changed public files: this report, research/STATE.json, docs/BACKLOG.md and docs/FEATURE_PROGRESS.md. Internal private session/feature notes synchronized; source lock unchanged.

Camera commands: **none**. No private input upload, actual firmware/constants/native payload read, upstream execution, driver/firmware change or device access. No feature supported, recovery proven or device-write gate passed.

Next single reference work package: **FT-101: audit the published FTP implementation and direct camera-to-server Wi-Fi evidence when available, including exact target/region identity, file equality, security, persistence, failure handling and reversal.** Existing RA-003 engineering continuation remains pending.
