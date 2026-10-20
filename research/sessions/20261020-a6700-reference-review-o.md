# Requested A6700 Powerful reference check

2026-10-20. Branch `codex/a6700-reference-check-20261020-o`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

Main was freshly resolved to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the existing [33-text-file source audit](20261019-RA-003-a6700-powerful-audit.md). A fresh recursive tree contains 51 entries. README, development plan, operating manual and NOTICE were fetched at that immutable revision and checked against Git blob IDs and byte counts. Private receipts retain URLs/SHA-256 and UTC acquisition time. No upstream instructions were adopted and no upstream code or binary executed.

| Priority | Finding | What this establishes |
|---|---|---|
| Native English | No language unlock found in the inspected material or previous unchanged source audit. | No new English feasibility evidence. |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG double transfer physically tested on a6700 2.00. Public tree has no FTP implementation. | Useful exact-model/version lead; no independently verified direct Wi-Fi transfer, target binary/region match, security, persistence or failure behavior. |
| Rollback | Public Pico-assisted route runs a temporary camera RAM program and reads known storage ranges. Manual explicitly says complete physical storage coverage and full restore are unverified. | Partial readback lead, not a proven rollback/recovery system. |
| FL2/FL3 | Development plan says offline validation underway, awaiting physical tests. | Deferred; no installable verified result. |

Published physical records are scoped to macOS. Displayed version 2.00 does not prove this mainland body's binary compatibility or Windows host qualification. Storage reads require temporary camera execution (R2), not ordinary USB identification. The feature bundle plan also differs from our individually gated changes. No offsets, identifiers, code or payloads were adopted.

NOTICE labels authored code/documents GPL-3.0-only and explicitly declines to relicense inherited Pico portions from an upstream commit without an attached licence. Whole-chain reuse rights and source/binary correspondence remain unresolved. This is a source-notice finding, not a new legal clearance.

Pinned sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md), [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

## Commands and results

Initial working tree was clean at `9e2f5a8` on `codex/ra003-activity-review-packet`. An attempted branch name already existed; Git refused without changing branch. A unique topic branch was then created. Initial broad document output was truncated; targeted reads followed. The browser `/tree/main` URL failed; repository/raw pages and host API acquisition succeeded.

```powershell
git status --short --branch
git worktree list
git ls-remote https://github.com/xyzhangxin/sony-a6700-powerful.git refs/heads/main
# exit 0: 0c6294a83988f196adfc980de59f9a1d0b92e8e2 refs/heads/main
git switch -c codex/a6700-reference-owner-check
# exit 128: branch already exists; no branch switch
git switch -c codex/a6700-reference-check-20261020-o
# exit 0
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-o -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-n/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-o/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-o/check_reference.py
# exit 0: six bounded public metadata/text GETs; 4 documents verified, 51 tree entries
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy'));raise SystemExit(not r.wasSuccessful())" 2>&1 | Tee-Object -FilePath private/sessions/20261020-a6700-reference-review-o/tests.log
# 17 tests, zero failures/errors/skips, 1.501s, OK / exit 0
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-o/record.py
# exit 0; saves before-images of existing notes, then adds this review
```

Interpreter: CPython 3.13.12, Anaconda, Windows AMD64; isolated startup, standard-library-only mocked tests. Tests exercise our host policy, not upstream FTP or camera behavior; no sockets/listener created. No need to rerun historical broad suites for unchanged reference text. Source lock remains unchanged.

Changed public files: this report, `research/STATE.json`, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`. Private session/feature notes were backed up and supplemented without removing prior observations or changing the RA-003 phase/next package. No firmware, native payload or private input acquisition/upload; no upstream launcher execution. Camera commands: **none**. No requested feature supported, recovery proved or device-write gate passed.

Next single reference work package: **FT-101: audit the FTP implementation and direct camera-to-server Wi-Fi evidence when published**, including exact binary/region identity, file integrity, security, persistence, failure handling and reversal. The pre-existing RA-003 activity-review packet remains the separate local engineering continuation.

Reviewed publication commands (all exit 0):

```powershell
git diff --check
git add -- docs/BACKLOG.md docs/FEATURE_PROGRESS.md research/STATE.json research/sessions/20261020-a6700-reference-review-o.md
git diff --cached --check
git diff --cached --stat
git diff --cached -- docs/BACKLOG.md docs/FEATURE_PROGRESS.md research/STATE.json research/sessions/20261020-a6700-reference-review-o.md
git commit -m "docs: record owner-requested a6700 project review"
git status --short --branch
```
