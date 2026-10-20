# A6700 Powerful: owner-requested source review

2026-10-20. Branch `codex/a6700-reference-check-20261020-q`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh main resolution: `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the existing 33-text-file source audit. Six bounded public metadata/text GETs obtained the commit, complete 51-entry tree and four documents. Document bytes and Git blob IDs verified. No reason to repeat the unchanged full source audit or execute upstream tools.

| Priority | Finding | Remaining prerequisite |
|---|---|---|
| Native English | No unlock in reviewed material or unchanged prior code audit. | Exact mainland resources/restrictions and reversible narrow change. |
| Native Wi-Fi FTP | Author reports FTP/settings and RAW+JPEG double transfer physically tested on a6700 2.00; implementation not published. | Source plus direct Wi-Fi evidence, exact binary/region match, file equality, credentials/security, persistence and failure handling. |
| Rollback | Public Pico-assisted route temporarily executes camera RAM code and reads known storage ranges; complete physical coverage/full restore explicitly unverified. | Demonstrated recovery envelope and independently verified backups. |
| FL2/FL3 | Offline validation underway; physical tests pending. | Deferred; no verified installable result. |

Physical records are scoped to macOS; they do not qualify our Windows host or this mainland body. A version string is not binary compatibility evidence. The planned bundled feature changes differ from our separately gated features. The public readback route is an R2 temporary native-execution route, not ordinary USB identification. No offsets, identifiers, code or payloads were adopted.

NOTICE assigns GPL-3.0-only to authored material and expressly excludes relicensing inherited Pico portions from an upstream revision without an attached licence. Whole-chain reuse rights and binary/source correspondence remain unresolved. No code reuse or new legal clearance.

Pinned sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md), [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

## Exact commands and results

Initial tree clean at `0748209`, branch `codex/ra003-observation-outer`. Existing reference worktree left unchanged. Broad initial documentation output truncated; focused reads followed. Browser `/tree/main` failed; repository/document pages and host acquisition succeeded.

```powershell
git status --short
git branch --show-current
git worktree list
git ls-remote https://github.com/xyzhangxin/sony-a6700-powerful.git refs/heads/main
# exit 0; pinned revision above
git switch -c codex/a6700-reference-check-20261020-q
# exit 0
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-q -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-o/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-q/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-q/check_reference.py
# exit 0; 51 entries, four verified documents, unchanged main
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy'));raise SystemExit(not r.wasSuccessful())" 2>&1 | Tee-Object -FilePath private/sessions/20261020-a6700-reference-review-q/tests.log
# child exit 0; 17/17, zero failures/errors/skips, 1.469s
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-q/record.py
# exit 0; exclusive before-images of all six existing notes
```

CPython 3.13.12 Anaconda Windows AMD64; isolated, standard-library mocked policy tests. These test our host FTP policy, not upstream code or camera FTP; no sockets/listeners. Historical broad suites not rerun for unchanged reference text.

Changed public files: this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `research/STATE.json`. Ignored private session/feature notes backed up and supplemented. Source lock unchanged because upstream revision unchanged. No private firmware/constants/native payload reads, private uploads, upstream execution or device modification. Camera commands: **none**. No feature supported, recovery proved or device-write gate passed.

Next single reference work package: **FT-101: audit the published FTP implementation and direct camera-to-server Wi-Fi evidence when available; require exact target/region identity, file equality, security, persistence, failure handling and reversal.** Existing RA-003 engineering continuation remains unchanged.

Reviewed publication commands (all exit 0):
```powershell
git diff --check
git add -- docs/BACKLOG.md docs/FEATURE_PROGRESS.md research/STATE.json research/sessions/20261020-a6700-reference-review-q.md
git diff --cached --check
git diff --cached --stat
git diff --cached -- research/sessions/20261020-a6700-reference-review-q.md
git commit -m "docs: refresh requested a6700 project assessment"
git status --short --branch
```
