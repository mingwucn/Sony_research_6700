# A6700 Powerful: owner-requested recheck

2026-10-19. Branch `codex/a6700-powerful-recheck`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

GitHub main still resolves to `0c6294a83988f196adfc980de59f9a1d0b92e8e2`, the revision in our [33-text-file source audit](20261019-RA-003-a6700-powerful-audit.md). This check fetched commit metadata, the complete recursive tree metadata and four commit-pinned texts (README, development plan, manual, NOTICE). All four sizes and Git blob identities match the tree; SHA-256 receipts remain private. No new revision adopted; source lock unchanged. No upstream code, binary payload or firmware downloaded/executed in this check.

| Owner goal | Finding | Evidence limit |
|---|---|---|
| English first | No language unlock located in the earlier audited source; current documents add none. | Mainland English feasibility remains unresolved. |
| Native Wi-Fi FTP first | Author reports FTP settings and RAW+JPEG double transfer completed and physically verified on a6700 2.00. | Public tree contains backup/access tools, not the reported FTP patch. Native Wi-Fi transport, absence of relay, integrity, persistence and failure behavior have not been reproduced here. |
| Rollback before write | Manual describes bounded readback; plan explicitly leaves full backup/restore and official-firmware rescue for later validation. | Partial backup and equal double reads do not prove recoverability. |
| FL2/FL3 later | Offline validation underway; physical validation pending upstream. | No validated installable result inferred. |

Sources at the fixed revision: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md), [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md), [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md), [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

The recorded environment is a6700 2.00/macOS. Displayed version alone does not establish mainland binary/SKU correspondence or Windows readiness. The published read-only route still injects executable code into camera RAM and requires hardware/service access; it is R2 temporary execution under our policy, not ordinary identification. No step in its manual has been executed. Its bundled incremental feature plan must not bypass our separate feature gates.

Authored code/docs are GPL-3.0-only. NOTICE expressly excludes relicensing original inherited Pico material from an upstream revision without an attached licence. Whole-chain reuse rights and source/binary equivalence remain unresolved; reference only, no code adoption or redistribution.

## FTP evidence checklist for the next source-only package

Before considering an exact-target candidate, collect and review:

1. Public implementation revision, relevant component notices and reproducible build/source-to-payload evidence.
2. Exact source firmware hashes, regional applicability, expected bytes, address types and bounded modification/inverse descriptions; no copied offsets without independent target evidence.
3. Camera-resident client/backend and Wi-Fi invocation path, media access and lifecycle; distinguish a menu flag from a working transfer worker.
4. Sanitized author evidence of direct camera-to-server transfer without a host/phone relay, with matching RAW and JPEG sizes/hashes and server receipts.
5. Protocol/security, credential storage, manual versus automatic triggering, reconnect, partial transfer, duplicate and power-state behavior.
6. Reversal on the exact starting state plus separately proved backup coverage and recovery envelope. A working-body reversal does not prove unbootable recovery.

This checklist requests no author contact or camera action. Missing evidence is a blocker, not a negative feasibility proof.

## Commands and results

Host: Windows AMD64, CPython 3.13.12, `C:\ProgramData\miniconda3\python.exe`.

- `git status --short`: clean before work.
- `git branch --show-current`: `codex/ra003-parent-evidence-v5` initially.
- `git rev-parse HEAD`: `2b6856796e7e30f00d1b4b5cabf420f015abdd4f`.
- `git switch -c codex/a6700-powerful-recheck`: exit 0.
- Host-authored standard-library script through `python.exe -I -S -B -X utf8 -`: HTTPS GET GitHub `/commits/main`, `/git/trees/<resolved-sha>?recursive=1`, then four raw documents at that SHA; verify byte sizes/Git blobs and retain SHA-256 receipts in a newly created private directory. Exit 0. Initial web tree/API reader attempts failed; raw web text and the host metadata/text requests succeeded. No binary request.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));raise SystemExit(not r.wasSuccessful())"
```

**228 cases, 225 passed, three skipped; exit 0; 20.149s suite / 20.666756s wrapper.** Skips cover Windows-inapplicable fork and unavailable real symlink cases. These are our synthetic host regressions, not upstream or camera tests. No executable source changed. JSON parsing and `git diff --check` also pass.

Changed tracked files: this report, docs/BACKLOG.md, docs/FEATURE_PROGRESS.md and research/STATE.json. Internal continuity notes updated after byte-preserving private backups. Prior RA-003 phase/next package retained; no production chain promoted.

Camera commands: **none**. No private upload, driver change, firmware/native input read, tool launch, device transition or write. English/native FTP, recovery and device-write gates remain unpassed.

Next single work package for this reference lead: **FT-101: assess any published FTP implementation and transfer evidence against the checklist above, remaining source-only.** Publication/evidence is currently missing. The separate saved RA-003 dependency-composition package remains pending and is unchanged by this check.
