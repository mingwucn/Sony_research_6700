# Requested A6700 Powerful recheck

2026-10-20 local date; remote receipt UTC 2026-10-19T23:17:11.894961+00:00.
Branch `codex/a6700-reference-review-20261020-e`; starting HEAD `64c04ff` with a clean tree.
Evidence: source-report, static-inference, offline-tested.

Fresh commit/tree lookup confirms main remains `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, identical to the source lock and prior audit. The 51-entry tree was inventoried. Four immutable text documents match their Git blob identities, sizes, SHA-256 values and prior receipt. This is a current-source refresh; unchanged implementation code was not audited again or executed. Source lock unchanged.

| Goal | Current evidence | Remaining requirement |
|---|---|---|
| Native English, primary | No English unlock in the unchanged audited source/documents. | Mainland language policy/resource mapping and reversible exact-target implementation. |
| Native Wi-Fi FTP, primary | Author reports FTP settings and RAW+JPEG transfers physically tested on a6700 2.00. | Public implementation, direct Wi-Fi/server operation without relay, exact build/region match, file integrity and interruption handling. |
| Recovery before writes | Published Pico route injects temporary RAM Fastboot code; manual records limited storage reads. | Full physical storage coverage, restoration and official-firmware rescue remain unverified. A matching double-read is not restore proof. |
| FL2/FL3, deferred | Roadmap says offline validation in progress. | Physical validation pending; does not take priority over English/FTP. |

The published route is R2 temporary camera-side execution, not ordinary passive USB identification. Physical records cover a6700 2.00/macOS; correspondence with this owner's mainland body and Windows host is unproved. The ordinary USB unlock tool and FTP implementation remain unpublished. The roadmap plans bundled incremental features; this does not meet our independently gated feature scope.

NOTICE grants GPL-3.0-only for authored material and explicitly excludes inherited original Pico material from that grant because its pinned upstream lacks a licence. Whole-chain reuse rights and source/binary equivalence remain unresolved. No source, payload, offset or guard change adopted. No new legal conclusion about proprietary firmware inspection.

Sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md), [roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

## Exact commands and results

```powershell
git status --short --branch
git switch -c codex/a6700-reference-review-20261020-e
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-e -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-d/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-e/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-e/check_reference.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-e/record.py
git diff --check
git add -- research/sessions/20261020-a6700-reference-review-e.md research/STATE.json docs/BACKLOG.md docs/FEATURE_PROGRESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached --numstat
git diff --cached
git commit -m "docs: refresh requested a6700 reference findings"
git status --short --branch
```

Acquisition and receipt verification: exit 0, CPython 3.13.12, standard library only; four document checks pass. Public text requests only, capped at 4 MiB per response, exclusively saved into a new private folder. Web tree/main failed; repository root and local GitHub API/raw text requests succeeded. No upstream tests/code or installed dependencies executed. No implementation changed, so historical synthetic suites were not rerun; the prior report's 17 mocked host-policy passes remain historical and establish no native feature. Git review/commit results are reported in the final response.

Changed public files: this report, research/STATE.json, docs/BACKLOG.md and docs/FEATURE_PROGRESS.md. Internal session/feature notes synchronized after exclusive backups. Shared RA-003 phase, qualification and next implementation package retained.

Camera commands: **none**. No firmware/constants/native payload reads, private uploads, launchers, driver or firmware changes. No feature supported; no recovery or device-write gate passed.

Next single reference work package: **FT-101: audit public FTP implementation and direct camera-to-server Wi-Fi evidence when published**. No author contact or monitoring scheduled.
