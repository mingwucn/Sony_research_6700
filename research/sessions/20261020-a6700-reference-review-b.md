# Requested A6700 Powerful source recheck

2026-10-20 local date; branch `codex/a6700-reference-review-20261020-b`.
Evidence: source-report, static-inference, offline-tested.

Fresh public GitHub commit/tree lookup confirms main remains `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, matching the source lock and prior static audit. Tree: 51 entries. README, development plan, manual and NOTICE were fetched at that exact revision and verified against Git blob SHA-1 and sizes; SHA-256 receipts retained privately. This refresh is not a repeated full implementation audit. No upstream code or binary was executed or acquired as an executable input.

| Owner priority | Finding | Blocker |
|---|---|---|
| Native English | No unlock identified in the prior source audit or refreshed documents. | Exact mainland resource/restriction analysis and reversible implementation. |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG transfers physically tested on a6700 2.00. | Public implementation and direct Wi-Fi/server evidence, exact build/region correspondence, integrity and failure handling. |
| Rollback before writes | Public backup route injects and executes a RAM Fastboot program; its host scripts read storage. | Whole physical storage coverage, complete restore and official-firmware rescue are not verified. |
| FL2/FL3, deferred | Author reports offline validation in progress. | Physical validation remains pending. |

Primary sources at the pinned revision: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md), [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

The manual scopes physical records to a6700 2.00/macOS. Version text alone does not establish this owner's mainland body compatibility. Temporary camera RAM execution is R2 here, requiring separate exact-command approval. No suggested device command was run. The roadmap says feature releases are bundled rather than independently selectable; that does not meet our separate feature acceptance requirement without further work. The ordinary USB tool and FTP implementation are not yet published in the reviewed revision. Complete write-loop acceptance and full backup/restore remain pending.

NOTICE grants GPL-3.0-only for authored material but explicitly does not relicense inherited Pico portions from its unlicensed pinned upstream. Whole-chain reuse permission and source/binary equivalence remain unresolved. No code, payload or target offset was adopted; no legal conclusion or licence change follows.

## Commands and results

Host: Windows, CPython 3.13.12, `C:/ProgramData/miniconda3/python.exe`.

```powershell
git status --short --branch
git switch -c codex/a6700-reference-review-20261020-b
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-reference-review-b -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-powerful-check/check_reference.py -Destination private/sessions/20261020-a6700-reference-review-b/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-b/check_reference.py
```

All exited 0. The source-only acquisition script caps public text responses, verifies four Git blobs, saves new receipts exclusively and executes no upstream code. Web tree/main fetch failed; raw documents and host GitHub API succeeded. One diagnostic attempted an absent `tests/test_ftp_host_protocol.py`; corrected by discovering the existing test module, with no source changes.

Focused tests were run by a standard-library stdin wrapper under `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -`, loading `unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy')` after adding repository root and tests to sys.path. The wrapper wrote a new private tests.log and tests-result.json, measured elapsed time, hashed the log and propagated the unittest result. Exact equivalent suite invocation:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_ftps_client_policy'));raise SystemExit(not r.wasSuccessful())"
```

17/17 passed, no errors/failures/skips; exit 0; 1.5778669000137597 seconds. Log SHA-256: `a15c1f55b0720a74af338687814770c5e155c2ebce7e2dea338e020605ea4604`. The exact `-c` command above was also run successfully: 17/17, exit 0, 1.537s suite time. These are mocked host protocol-policy tests, not upstream, camera or real-server validation. Historical full suites were not repeated for a document refresh.

`C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-reference-review-b/record_review.py` recorded these notes and exclusive private backups, exit 0. `git diff --check` passed; explicit four-path staging and staged whitespace/content inspection followed.

Changed public files: this report, docs/BACKLOG.md, docs/FEATURE_PROGRESS.md and research/STATE.json. Private session and feature notes updated after exclusive backups. Starting HEAD `c8b5ec5`; unrelated existing untracked tools/dependency_source_receipts.py and tests/test_dependency_source_receipts.py remain untouched and unstaged. Shared RA-003 phase, latest qualification and next package remain unchanged by this source review.

Camera commands: **none**. No firmware/constants/native payload inspection, private input upload, drivers/firmware change, upstream launcher, feature support claim or passed device-write gate.

Next single reference work package: **FT-101: assess the public FTP implementation and direct camera-to-server Wi-Fi evidence against the existing [evidence checklist](20261019-a6700-powerful-recheck.md#ftp-evidence-checklist-for-the-next-source-only-package) when published.** No author contact performed.
