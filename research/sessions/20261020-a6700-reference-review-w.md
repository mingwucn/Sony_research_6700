# A6700 Powerful: current reference check

2026-10-20. Topic branch: `codex/a6700-reference-recheck-w`. Evidence: **source-report**, **static-inference**.

Fresh GitHub metadata pins main at **c8e2aa100cfb02523d06cc6fc767d25a63cf943d**. The complete recursive tree equals review v: **51 entries, 39 blobs, no changes**. README, progress, manual and NOTICE match their previous sizes, Git blob identities and SHA-256 hashes. Source lock unchanged. This is a reference refresh; no new full source audit or hardware reproduction is claimed.

| Priority | Finding | Remaining evidence |
|---|---|---|
| Native English | No unlock located in reviewed material | Exact mainland resource/policy mapping and reversible candidate |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG physical success on a6700 2.00 | Published implementation and independently checked direct Wi-Fi transfers, file equality, authentication, persistence, failures and reversal |
| Recovery before writes | Public route temporarily executes a RAM Fastboot reader | Full storage coverage and complete restoration remain explicitly unverified |
| Deferred FL2/FL3 | Offline research reported; physical validation pending | No accepted feature result here |

[Progress](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/开发计划与进展.md) distinguishes unpublished development from available releases. Its ordinary USB tool and full write loop are unfinished. [Manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/操作手册.md) scopes physical records to macOS and a6700 2.00; that does not qualify this Windows host or this owner's exact build. A read-only storage protocol still changes camera execution state and requires separate device approval.

[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/NOTICE) grants GPL-3.0-only for authored material but excludes relicensing inherited Pico code from an upstream commit without a licence. No code, offsets or payload adopted; no legal clearance inferred.

## Exact commands and results

PowerShell, CPython 3.13.12, `C:/ProgramData/miniconda3/python.exe`:

```powershell
git status --short
git branch --show-current
git switch -c codex/a6700-reference-recheck-w
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-w -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-v/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-w/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-w/check_reference.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-w/record_review.py
git diff --check
```

Acquisition **exit 0**: six bounded public metadata/text requests, four blob/size/hash checks. Recorder **exit 0**: complete tree/document equality against review v, unchanged locked pin, before-images retained and append-only review fields added to public/private notes. Recorder was derived locally from the previous recorder with only session/review labels changed. Its inherited `unchanged_from_prior_audit` acquisition field compares an older baseline; equality with review v is checked separately. Browser tree retrieval failed; raw documents and GitHub API acquisition succeeded. No behavioral tests rerun for these documentation changes; synthetic tests cannot establish upstream hardware claims.

Changed public files: this report, `research/STATE.json`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`. Private session/function notes synchronized. Five pre-existing engineering edits remain unstaged and excluded from this review commit: three tool files and two test files. Their work is unfinished and supplies no feature evidence.

After reviewing only those five public paths:

```powershell
git add -- research/sessions/20261020-a6700-reference-review-w.md research/STATE.json docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "docs: refresh a6700 reference claims and release limitations"
git status --short --branch
```

Camera commands: **none**. No firmware/constants/native reads, downloads of payloads, upstream execution, private uploads, driver changes, feature support or recovery/device-write gate pass.

Next single reference work package: **FT-101: audit the published FTP implementation and direct camera-to-server Wi-Fi evidence when available**, checking exact target, file equality, security, persistence, failure and reversal. Existing RA-003 engineering continuation remains separate and incomplete.
