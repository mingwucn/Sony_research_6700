# RA-003: Sony A6700 Powerful public-source audit

2026-10-19. Branch: `codex/ra003-a6700-powerful-audit`.
Evidence: **source-report**, **static-inference**, **offline-tested**. No independent reproduction of upstream camera results.

## Pinned scope and findings

Reviewed [xyzhangxin/sony-a6700-powerful](https://github.com/xyzhangxin/sony-a6700-powerful/tree/0c6294a83988f196adfc980de59f9a1d0b92e8e2) at `0c6294a83988f196adfc980de59f9a1d0b92e8e2`. GitHub API resolved main; 33 selected text files were downloaded privately and their Git blob SHA-1 and byte size verified against the pinned recursive tree. SHA-256 receipts are private. Twelve Python sources parsed with `ast.parse`; no upstream import, launcher, build, syntax workflow or device command executed. Excluded upstream AGENTS instructions, images and both binary payloads. Text source is reference material only; no implementation adopted.

| Priority/result | Public evidence | Assessment for this project |
|---|---|---|
| Native English | No English/language unlock implementation or documentation located in inspected text/tree | Unresolved; no new English feasibility result |
| Native FTP | Development plan reports FTP settings and RAW+JPEG double transfer completed and physically verified on a6700 2.00 | Significant model/version-specific lead, author report only. Public tree lacks FTP patch, backend/invocation evidence, reproducible target hashes and server-side transfer evidence. Wi-Fi transport, relay independence, persistence, security and failure behavior remain unverified by us |
| FL2/FL3 | Development plan says offline validation underway, awaiting device validation | Deferred; not an available verified installation |
| Backup/recovery | Manual reports partition-table-covered user-area range plus first 4 MiB of each boot area; physical eMMC size and complete restoration unverified | Partial readback lead, not the requested proven rollback system |
| Normal USB unlock | Plan reports historical root execution, fixed-range reads/writes/reversal; code publication and complete framework write-loop acceptance pending | No published ready-to-use path adopted |

The README scopes device records to a6700 2.00/macOS; organized host scripts received offline comparison without new device tests. Matching displayed version does not establish matching mainland SKU, binary hashes or this body's compatibility.

## Source audit and boundaries

- `源码/核心/注入入口.py:56-72` validates a fixed payload, requires explicit serial/arm selection for injection and does not automatically resend the stream. `记录协议.py` constructs RAM-loading/execution records. This is temporary native camera execution (project R2), not ordinary R1 identification; no such step is authorized here.
- `源码/核心/设备查询.py:29-74` checks a payload-reported product string and unique USB interface. That string identifies the loaded program, not an independently authenticated stock body/build. USB configuration may be set if missing.
- `源码/核心/扇区备份.py:12-50,53-81` bounds a request to 16 MiB, checks replies/length, offers optional independent double reads and uses exclusive output creation. It explicitly reports not a whole-camera backup. No durable transaction journal, whole-backup recovery proof or separate verified storage-copy manager is established by this code.
- `源码/脚本/构建相机引导.py:32-145` constructs a restricted command dispatcher, stubs CP calls, emits native register writes and checks selected forbidden symbols plus final payload hash. Source restrictions and hashes do not establish binary safety, source/binary equivalence or exact-body compatibility. The referenced upstream native source and shipped binaries were not downloaded/audited in this session. No addresses were transplanted into our target profiles.
- `.github/workflows/check.yml` performs compileall syntax checking on two Python versions; it is not a behavioral or physical-camera qualification suite.

## Reuse rights

[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE) states GPL-3.0-only for authored code/docs. The pinned LICENSE text was inspected. Nontrivial reuse must preserve applicable attribution/notices and comply with GPL obligations when applicable; no project-wide licence was changed. NOTICE separately says inherited Pico sources originate from ILCE-7M4-RE commit `2328d18ce640e6c8cd9341efcf0043ce9042a135`, which has no attached licence, and expressly declines to relicense those original portions. Its own GPL notice is therefore not a blanket grant for the entire dependency/payload chain. Resolve inherited-source and binary distribution permissions before adopting them. No third-party code or payload was staged or redistributed.

## Commands and results

All commands ran on the host. Interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12.

- `git status --short --branch`: starting tracked tree clean on `codex/ra003-independent-review-blocker`.
- `git switch -c codex/ra003-a6700-powerful-audit`: exit 0.
- Host-authored Python via `python.exe -I -S -B -X utf8 -`: urllib GET of GitHub commit/tree and commit-pinned text, Git blob/size/SHA-256 verification and `ast.parse` for 12 Python files: exit 0, 33 text files verified. Exact fetched paths/URLs derivable from private `tree.json` and `manifest.json`; no upstream execution or binary download.
- Initial `python.exe -I -S -B -X utf8 -m unittest discover -s tests -v`: exit 1, 11 module-import errors because isolated startup omits repository root (`tools` unavailable). This was a harness invocation problem; no implementation change.
- Corrected command below: exit 0, **228 tests, 225 passes, 3 skips**, suite **21.534s**, wrapper **22.076s**. These are our ordinary synthetic host tests, not upstream behavioral tests, the frozen private gate suite or camera validation. Raw result/logs retained privately.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));raise SystemExit(not r.wasSuccessful())"
```

Camera commands: **none**. No firmware/private input upload, dependency install, agreement acceptance, native payload read/execution, device contact or write. English/native FTP support, recovery and device-write gates remain false.

## Next single work package

RA-003: independently review the frozen 38-source GDT gate packet and 124-case qualification under the owner-authorized local source-only review boundary; resolve findings before any activation.

The new FTP source lead is recorded for FT-101 follow-up when public implementation and test evidence are available. Existing local-review authorization remains valid; this source audit did not perform or complete that independent review.

## Public-document refresh and current local work

2026-10-19: README, development plan, manual and NOTICE were read again through public web text. Their FTP claim, unfinished complete restore/write workflow and inherited licensing limitation remain consistent with this pinned audit. This refresh did not pin a new code tree or reproduce a camera result. English remains unresolved. Current local next package and exact host-only results are in the [factory source gate continuation](20261019-RA-003-factory-source-gate.md); the older next package above is historical.
