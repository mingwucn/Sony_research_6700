# Owner-requested A6700 Powerful check g

2026-10-19. Branch: codex/a6700-reference-check-20261019g. Starting HEAD: b4210a8.
Evidence: source-report, static-inference, offline-tested. Camera commands: none.

Fresh main remains `0c6294a83988f196adfc980de59f9a1d0b92e8e2`. Its complete recursive tree contains 51 entries,
39 blobs. Four immutable documents verified by size and Git blob SHA-1;
SHA-256 receipts retained privately. This refresh confirms the unchanged
[previous whole-source audit](20261019-RA-003-a6700-powerful-audit.md), without
repeating that audit or reproducing the author's device claims.

| Priority | Finding |
|---|---|
| English | No unlock found in the unchanged audited sources or refreshed documents. Mainland-language feasibility remains unresolved. |
| Native FTP | Author reports FTP settings and RAW+JPEG transfer physically tested on a6700 2.00. Implementation remains unpublished. Direct Wi-Fi without a relay, exact build identity, server equality, security and failure handling need evidence. |
| Rollback | Complete physical storage coverage and full restoration explicitly remain unverified. A partial backup does not establish recovery. |
| FL2/FL3 | Offline validation ongoing; device validation pending. Deferred behind English and FTP. |

Immutable sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md),
[roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md),
[manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md),
[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

The published Pico route injects and executes a temporary RAM program: R2 under
our policy, even when storage access is read-only. Public records concern 2.00
and macOS; exact mainland-body compatibility and our Windows route are unproved.
Ordinary USB unlock code is not published. The new writer's complete write loop
and full restoration remain unfinished. Planned bundled features require scope
review before any adoption. Authored material is GPL-3.0-only; NOTICE excludes
relicensing inherited Pico portions whose pinned upstream lacks a licence.
Reuse rights for that chain and source/binary correspondence remain unresolved.
No code/payload adopted, no binaries downloaded, no upstream code executed.

The browser fetch of the supplied main-tree URL failed; the bounded GitHub API/raw-text harness below succeeded.

Exact commands and results, all host-side:

- `git status --short --branch`; `git log -1 --oneline`: exit 0; initial branch codex/ra003-operational-binding-spec, HEAD b4210a8; two untracked operational-binding specification files preserved.
- `git switch -c codex/a6700-reference-check-20261019g`: exit 0.
- `New-Item -ItemType Directory -Path private/sessions/20261019-owner-project-check-g -ErrorAction Stop`: exclusive evidence folder, success.
- `Copy-Item -LiteralPath private/sessions/20261019-owner-project-check-f/check.py -Destination private/sessions/20261019-owner-project-check-g/check.py -ErrorAction Stop`: reviewed authored harness copied, success.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-g/check.py`: exit 0; seven HTTPS GETs, no redirects/retries, 30-second timeout and 2 MiB per-response bound; ref, commit, complete tree and four immutable texts verified. Standard-library mocked host FTP policy tests: 17/17 passed, zero skips/errors/failures, 1.643500s. Interpreter CPython 3.13.12 / Windows AMD64. These tests prohibit sockets and do not validate upstream FTP or camera operation. Full historical suites not rerun for this reference refresh.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-g/record.py`: save report and append external/internal observations with exclusive backups; preserve all previous JSON values.
- `git diff --check`; `git diff --cached --check`: review whitespace and staged changes. Explicit staging uses only the five public report/note/state paths listed below.

Changed public files: this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md,
docs/FEATURE_PROGRESS.md, research/STATE.json. Ignored private session/feature
notes and source receipts updated. Existing untracked research/OPERATIONAL_BINDING_SPEC.md
and research/OPERATIONAL_BINDING_SPEC.json remain untouched and unstaged. Source lock,
RA-003 phase and next implementation package are preserved. No camera contact,
private upload, firmware/constants read, driver/firmware change or feature,
recovery or device-write gate passed.

Next single reference package: FT-101: audit the FTP implementation and direct camera-to-server Wi-Fi evidence when published, including exact build identity, transfer equality, failure handling and reversal/recovery coverage.
Blocker: implementation and reproducible evidence are not yet published.
