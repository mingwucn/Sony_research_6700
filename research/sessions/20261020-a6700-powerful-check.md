# Requested A6700 Powerful project check

2026-10-20 local date. Branch: `codex/a6700-powerful-check-20261020`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh GitHub API lookup resolves main to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the [earlier source audit](20261019-RA-003-a6700-powerful-audit.md). Recursive tree: 51 entries. Four pinned texts (README, development plan, manual, NOTICE) passed Git blob SHA-1 and size checks; SHA-256 receipts are private. This is a document refresh against the previously audited revision, not a new full implementation audit. No upstream execution or binary acquisition.

| Goal | Finding | Remaining evidence |
|---|---|---|
| Native English, primary | No English unlock in the earlier audited source; refreshed documents add none. | Matching mainland resource/restriction analysis and reversible implementation. |
| Native Wi-Fi FTP, primary | Author reports FTP settings and RAW+JPEG transfer physically verified on a6700 2.00. | Public FTP implementation, matching build/region, direct camera-to-server Wi-Fi evidence, integrity, persistence and failure behavior. |
| Rollback before firmware writes | Public backup route temporarily executes a RAM program. Full physical storage coverage and complete restore remain unverified. | Exact-body backup coverage, independent copies, exact inverse and demonstrated recovery envelope. |
| FL2/FL3, deferred | Offline validation reported; physical validation pending. | No independently validated installable result. |

The [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md) distinguishes unpublished development from released code and leaves full write-loop acceptance and complete recovery pending. The [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md) scopes device records to a6700 2.00/macOS. Its read route is R2 temporary native execution here, requiring its own device approval. A version-label match does not establish this mainland body's compatibility.

[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE) assigns GPL-3.0-only to authored material but excludes relicensing inherited Pico portions from an upstream without an attached licence. Whole-chain permissions and source/binary correspondence remain unresolved. No code adopted, offsets copied or project licence changed.

## Commands and results

Host: Windows AMD64, CPython 3.13.12 at `C:/ProgramData/miniconda3/python.exe`.

```powershell
git status --short --branch
git rev-parse HEAD
git switch -c codex/a6700-powerful-check-20261020
New-Item -ItemType Directory -Path private/sessions/20261020-a6700-powerful-check -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261019-a6700-powerful-review-refresh/check_reference.py -Destination private/sessions/20261020-a6700-powerful-check/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-a6700-powerful-check/check_reference.py
```

All exited 0. Starting HEAD: `ee6903ff3754418d7b47a2b93bc89094f8e63ef6`, branch `codex/ra003-basis-links`, with one existing untracked `tools/dependency_basis_links.py`; preserved and excluded from staging. API script fetches only public commit/tree metadata and four pinned UTF-8 texts with exclusive file creation. Initial web `/tree/main` open failed; repository root and host API succeeded. Source lock remains unchanged.

Focused standard-library tests used this exact PowerShell pipeline, exit **0**:

```powershell
@'
import hashlib,json,pathlib,sys,time,unittest
root=pathlib.Path.cwd(); sys.path.insert(0,str(root)); sys.path.insert(0,str(root/'tests'))
out=root/'private/sessions/20261020-a6700-powerful-check'
suite=unittest.defaultTestLoader.loadTestsFromNames(['test_offline_inventory','test_artifact_probe'])
start=time.perf_counter()
with (out/'host-tests.log').open('x',encoding='utf-8') as log:
 result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
record={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skips':len(result.skipped),'seconds':time.perf_counter()-start,'exit_code':0 if result.wasSuccessful() else 1,'interpreter':sys.executable,'version':sys.version,'log_sha256':hashlib.sha256((out/'host-tests.log').read_bytes()).hexdigest(),'camera_commands':[]}
with (out/'tests-result.json').open('x',encoding='utf-8') as f: json.dump(record,f,indent=2)
print(json.dumps(record)); raise SystemExit(record['exit_code'])
'@ | C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -
```

**36 cases: 35 passed, one Windows symlink skip, zero failures/errors; 0.1542345000198111 seconds.** Log SHA-256: `b7dc36db28d7d5b5907197ad4a9d21a5702b35fe72cd19b1961a7e2836b3c3c5`. These test our invented-input inventory/probe behavior, not upstream code or camera features. Full historical suites were not repeated for this documentation review.

Changed tracked files: this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `research/STATE.json`. Private session/feature notes updated after exclusive backups. Separate RA-003 implementation and next package are preserved. Explicit staged path/content review and diff whitespace checks required before commit.

Camera commands: **none**. No private upload, firmware/constants/native payload read, camera contact, driver or firmware change. No feature supported, recovery proven or device-write gate passed.

Next single reference work package: **FT-101: assess published FTP implementation and direct camera-to-server Wi-Fi evidence against the [saved checklist](20261019-a6700-powerful-recheck.md#ftp-evidence-checklist-for-the-next-source-only-package) when available.** Publication remains a blocker; no author contact performed.
