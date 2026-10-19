# A6700 Powerful: owner-requested reference recheck

2026-10-19. Branch `codex/a6700-reference-recheck-20261019`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

GitHub main still resolves to **`0c6294a83988f196adfc980de59f9a1d0b92e8e2`**, the already pinned and audited revision. No newer code was adopted. The [earlier 33-file static audit](20261019-RA-003-a6700-powerful-audit.md) remains applicable. This session fetched commit metadata, the complete recursive tree (39 blobs), and four immutable text documents. Their sizes and Git blob identities matched the tree; SHA-256 receipts remain private. The source lock is unchanged.

| Owner goal | Finding | Remaining prerequisite |
|---|---|---|
| Native English, primary | No unlock located in the earlier inspected code or refreshed documents | Mainland language-resource/configuration evidence and a reversible, exact-target method |
| Native Wi-Fi FTP, primary | Author reports settings and RAW+JPEG transfer physically verified on a6700 2.00 | Public implementation, exact build identities, onboard Wi-Fi/no-relay proof, server integrity and failure/reversal evidence; no independent reproduction here |
| FL2/FL3, deferred | Author reports offline validation in progress, physical validation pending | Target implementation and physical still/preview validation |
| Rollback before writing | Complete backup/restore and official-firmware recovery explicitly unfinished | Coverage of every changed object, independent backup copies and demonstrated recovery limitations |

The currently documented public route uses Pico-triggered RAM Fastboot and bounded readback. Although its storage commands are described as read-only, entering the route executes native code on the camera: project R2, requiring its own exact-step approval. It is not an ordinary USB identity query. The reported environment is a6700 2.00/macOS; that does not prove this Windows/mainland body's compatibility. Ordinary-USB unlock code and the complete new write framework remain pending publication/acceptance. The proposed bundled feature release also requires review against our separately gated goals.

The [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md) supplies the author claims. The [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md) limits backup coverage and says complete restoration is unverified. [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE) labels authored code/docs GPL-3.0-only but excludes relicensing inherited Pico portions from an upstream commit without an attached licence. Adoption of that chain remains blocked on rights/provenance review. No implementation or payload was copied into this project.

## Commands and results

Host: Windows AMD64, CPython **3.13.12**, `C:\ProgramData\miniconda3\python.exe`.

- `git status --short --branch`: clean tracked tree on `codex/ra003-stream-contract-binding`.
- `git switch -c codex/a6700-reference-recheck-20261019`: exit **0**.
- Host-authored standard-library acquisition via `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -`: exit **0**. GET `https://api.github.com/repos/xyzhangxin/sony-a6700-powerful/commits/main`, then `/git/trees/0c6294a83988f196adfc980de59f9a1d0b92e8e2?recursive=1` under the same repository API prefix. GET only `README.md`, `开发计划与进展.md`, `操作手册.md`, `NOTICE` under `https://raw.githubusercontent.com/xyzhangxin/sony-a6700-powerful/0c6294a83988f196adfc980de59f9a1d0b92e8e2/`. Verified size and `sha1(b'blob '+size+b'\0'+bytes)` against tree, recorded SHA-256, exclusively created a new private session folder. Public web reader initially failed on `/tree/main`; repository-root/raw-text reads succeeded. No upstream script or binary execution/download.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));raise SystemExit(not r.wasSuccessful())"
```

**228 cases: 225 passed, three skipped, exit 0; 17.324s suite / 17.81431899999734s wrapper.** These are this project's standard-library host tests, not upstream, actual-server or camera qualification. Raw logs and interpreter/command receipt are private. Historical private gate suites were not replayed.

Reviewed changes: this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `docs/CODEX_HANDOFF.md`, `research/STATE.json`. Private session/feature notes updated with exclusive backups. JSON and whitespace checks accompany exact-path staging; no push.

Camera commands: **none**. No firmware/constants/native payload reads, dependency installation, private uploads, device changes or writes. English/FTP support, operational acceptance, recovery and device-write gates remain unpassed. This reference check does not change the shared RA-003 dependency/native-policy blockers or supersede its stored next package.

## Next single work package

**FT-101: prepare a source-only FTP evidence checklist for this pinned revision, specifying the missing implementation, exact build identities, onboard Wi-Fi/no-relay transfer, server-side RAW/JPEG integrity, failure handling and reversal evidence.** No camera operation or author contact is included.
