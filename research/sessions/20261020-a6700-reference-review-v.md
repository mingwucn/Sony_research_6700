# A6700 Powerful: repeated reference check

2026-10-20. Branch `codex/a6700-reference-recheck-v`. Evidence: **source-report**, **static-inference**.

The requested repository remains at the existing locked revision **c8e2aa100cfb02523d06cc6fc767d25a63cf943d**. Its complete recursive tree matches review u: **51 entries, 39 blobs, no changed paths**. Four freshly retrieved ordinary documents match the previous size, Git blob identity and SHA-256. No new complete source audit or independent hardware reproduction is claimed; the earlier unchanged-source audit remains applicable. Source lock unchanged.

| Owner priority | Finding | Unresolved prerequisite |
|---|---|---|
| Native English | No English-menu unlock located in the reviewed material | Mainland resource/policy mapping and a reversible exact-target candidate |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG physical success on a6700 2.00 | Published implementation; direct camera-to-server Wi-Fi evidence, file equality, security, persistence and failure/reversal tests |
| Rollback | Public route reads known ranges through code temporarily executed in camera RAM | Complete storage coverage and full restoration remain unproved |
| FL2/FL3, deferred | Offline work reported; physical validation pending | No feature accepted here |

Primary documents at the pinned revision: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/README.md), [progress](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/NOTICE).

Physical records are scoped to macOS; this Windows host and the owner's exact mainland build remain unqualified. A public read-only route still changes camera execution state. The reported ordinary USB route and complete write loop are not a released, validated installation path. GPL-3.0-only covers authored material; NOTICE excludes relicensing inherited Pico material from an upstream revision without a licence. No implementation, offsets or payload adopted. No contact with the author or camera.

## Exact commands and results

```powershell
git status --short --branch
git switch -c codex/a6700-reference-recheck-v
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-v -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-u/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-v/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-v/check_reference.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-v/record_review.py
git diff --check
git diff --stat
```

Acquisition exit **0**: six bounded public metadata/text requests, four size/blob checks, no binary download. Web tree view failed; root/raw views and host metadata acquisition succeeded. The inherited receipt field `unchanged_from_prior_audit` compares an older revision; the recorder explicitly verifies equality against review u instead.

Recorder/metadata validation exit **0**: same locked commit, entire tree equality, four document hashes and original JSON fields preserved with an appended review entry. Before-images and receipts retained privately. Interpreter: **CPython 3.13.12**, `C:/ProgramData/miniconda3/python.exe`, isolated flags above. Behavioral tests were not rerun for this reference-only update; synthetic tests cannot verify upstream camera claims. An incidental local read returned exit 1 because the new recorder did not yet exist; the requested saved manual was read successfully. No upstream command was executed.

Changed public files: this report, `research/STATE.json`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`. Private session and per-function notes appended with before-images. Four pre-existing authored tool/test changes on the engineering branch are preserved, excluded from reference staging, and remain unfinished engineering work; their reviewer results are not FTP/English evidence.

Publication commands after reviewing the five public file diffs:

```powershell
git add -- research/sessions/20261020-a6700-reference-review-v.md research/STATE.json docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "docs: recheck a6700 reference FTP English and recovery evidence"
git status --short --branch
```

Camera commands: **none**. No firmware/constants/native payload reads, private upload, dependency activation, driver/firmware change, feature support or recovery/device-write gate pass.

Next single reference work package: **FT-101: audit the published FTP implementation and direct camera-to-server Wi-Fi evidence when available**, including exact target identity, file equality, security, persistence, failures and reversal. Existing RA-003 continuation remains recorded separately.
