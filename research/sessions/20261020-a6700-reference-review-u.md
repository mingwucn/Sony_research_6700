# A6700 Powerful reference recheck

2026-10-20, branch `codex/a6700-reference-check-20261020-u`.
Evidence: **source-report**, **static-inference**. Validation below checks reference metadata only.

Main now resolves to `c8e2aa100cfb02523d06cc6fc767d25a63cf943d`, a parentless commit. The complete recursive tree equals our previous `2de85f1cca89b0e20ee25a70f93e04c3d34e10e5` pin: **51 entries, 39 blobs, zero changed paths**. This is an observed history replacement, not new implementation evidence. Prior pin and earlier delta review are preserved in the source lock. No upstream instructions adopted. Four documents freshly fetched and verified by size, Git blob ID and SHA-256. This delta review relies on the earlier unchanged-source audit; no new complete implementation audit claimed.

| Priority | Finding | Remaining prerequisite |
|---|---|---|
| Native English | No unlock located in reviewed material | Exact mainland resource/policy mapping and reversible candidate |
| Native Wi-Fi FTP | Author reports a6700 2.00 FTP settings and RAW+JPEG physical success | Published implementation, direct Wi-Fi transfer evidence, file equality, security and failure/reversal testing |
| Rollback | Public Pico route temporarily executes camera RAM code and reads known ranges | Complete storage coverage and restoration remain unproved; backup alone is insufficient |
| FL2/FL3, deferred | Author lists offline work with physical validation pending | No usable feature accepted here |

Physical records are scoped to macOS; this Windows host and owner's exact mainland build are unqualified. Ordinary USB tools and full write-loop acceptance remain unfinished. Bundled feature plans do not satisfy our separate feature gates. GPL-3.0-only covers authored material; NOTICE explicitly excludes relicensing inherited Pico portions from its unlicensed upstream. No code, offsets or payload adopted.

Pinned primary documents: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/README.md), [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/c8e2aa100cfb02523d06cc6fc767d25a63cf943d/NOTICE).

## Exact commands and results

```powershell
git status --short --branch
git remote -v
git switch -c codex/a6700-reference-check-20261020-u
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-u -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-t/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-u/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-u/check_reference.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-u/record_review.py
```

Acquisition exit **0**: six bounded public metadata/text requests, four document size/blob checks. Web tree/API views failed; root/document views and host API requests succeeded. No binary download. The acquisition receipt's inherited `unchanged_from_prior_audit` refers to older 0c6294a; this report and validation explicitly compare the immediately preceding pin.

Recording/metadata validation exit **0**: exact tree equality, 51/39 inventory counts, parentless commit, four document size/blob/SHA-256 checks, lock consistency, original JSON fields preserved and appended text history unchanged. Interpreter `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12, isolated flags above. No behavioral tests rerun for this documentation/pin change; existing synthetic tests do not validate these upstream camera claims. Before-images and acquisition/validation receipts retained privately. Initial Git state clean; engineering branch retained.

Changed public files: this report, `references/sources.lock.json`, `research/STATE.json`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`. Internal session/function notes updated, private originals preserved. Production and test code unchanged.

Publication commands, after reviewing each diff:

```powershell
git diff --check
git add -- references/sources.lock.json research/STATE.json docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/sessions/20261020-a6700-reference-review-u.md
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "docs: review a6700 reference history replacement and feature evidence"
git status --short --branch
```

The recorder initially reformatted unrelated source-lock objects; a checked formatting-only cleanup restored their original layout and asserted identical parsed JSON. Both intermediate bytes and original before-image remain private. Diff checks exit 0; only the six named public paths are staged.

Camera commands: **none**. No firmware/constants/native payload reads, upstream execution, private upload, camera contact, driver/firmware change, feature support or recovery/device-write gate pass.

Next single reference package: **FT-101: audit the FTP implementation and direct camera-to-server Wi-Fi evidence when published, including exact target identity, file equality, security, persistence, failures and reversal.** Existing RA-003 engineering continuation and its pending decisions are unchanged.
