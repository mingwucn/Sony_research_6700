# Owner-requested A6700 Powerful source check

2026-10-19. Branch: `codex/a6700-reference-refresh-20261019`.
Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh public ref/commit/tree metadata resolves main to
`0c6294a83988f196adfc980de59f9a1d0b92e8e2`, unchanged from the source lock and
[prior 33-text / 12-Python static audit](20261019-RA-003-a6700-powerful-audit.md).
The recursive tree has 51 entries / 39 blobs. Four immutable documents were
downloaded privately and matched against tree sizes and Git blob identities;
SHA-256 receipts are retained privately. This refresh checks identity and current
published claims; it does not repeat the unchanged implementation audit.

| Owner goal | Finding | Evidence still required |
|---|---|---|
| Native English, primary | No unlock found in the prior audit or current documents | Mainland language-resource/configuration mapping and narrow reversible enablement |
| Native Wi-Fi FTP, primary | Author reports working FTP settings and RAW+JPEG transfer on a6700 2.00 | Published implementation, exact-target hashes, direct Wi-Fi/server evidence without relay, file equality, persistence and failure/security behavior |
| Rollback prerequisite | Documented partial storage readback | Full storage coverage, demonstrated restoration and recovery envelope; the author explicitly leaves full restore/rescue unfinished |
| FL2/FL3, deferred | Offline validation underway; physical validation pending | Later separate work; no present usable installation established |

The [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md)
limits device records to a6700 2.00/macOS. The
[roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md)
includes unpublished work and bundled feature deployment; these claims do not
establish this body's compatibility or our individually gated English/FTP scope.
Its normal-USB write tooling is not published as a qualified ready-to-use route.

The [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md)
uses a Pico to launch temporary Fastboot code in camera RAM before USB reads.
This is R2 temporary native execution under our policy; calling subsequent reads
read-only does not turn entry into R1 ordinary identification. The documented
backup covers a partition-table range plus portions of two boot areas; physical
storage capacity and full restoration remain unverified. No target addresses,
identities or binaries were adopted.

[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE)
labels authored code/docs GPL-3.0-only but expressly declines to relicense inherited
Pico portions from an upstream revision without an attached licence. Whole-chain
reuse rights and source/binary correspondence remain unresolved; no implementation
was integrated, no licence changed and no binary downloaded.

## Exact commands and results

- `git status --short`, `git branch --show-current`, `git log -1 --format="%h %s"`: HEAD `b9ad979`, inherited branch `codex/ra003-dependency-activation-packet`; three unrelated untracked activation-packet files preserved, unstaged.
- `git switch -c codex/a6700-reference-refresh-20261019`: exit 0.
- `& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-reference-refresh-owner/check.py`: exit 0. Authored standard-library script makes seven bounded HTTPS GETs: GitHub API `git/ref/heads/main`, `git/commits/<resolved SHA>`, `git/trees/<tree SHA>?recursive=1`, then README, roadmap, manual and NOTICE from immutable raw URLs. Each response bounded to 2 MiB, timeout 30 seconds, redirects refused, no retries. Exact URLs, sizes and hashes retained in ignored `receipt.json`. Initial web `/tree/main` failed; repository-root and document views succeeded.
- Same isolated interpreter adds repository root to `sys.path`, then `unittest.defaultTestLoader.discover('tests', pattern='test_ftps_client_policy.py')` through `unittest.TextTestRunner(stream=log, verbosity=2)`: **17/17 passed**, zero skips, exit **0**, **1.6700068999780342 seconds** wrapper. CPython **3.13.12**, Windows AMD64. These are our mocked host policy tests, with socket creation prohibited; they do not qualify upstream implementation, camera FTP or recovery. No full-suite rerun for this documentation-only check.
- JSON validation, explicit staged-path/content review and `git diff --cached --check` are performed before commit. Only this report, BACKLOG, HANDOFF, FEATURE_PROGRESS and STATE belong to the public change.

Public and internal progress notes updated. Existing private notes backed up
exclusively before modification; owner intake and the shared RA-003 phase/next
package remain unchanged. Source lock unchanged because upstream is unchanged.
Unrelated untracked code and design files remain untouched and unstaged.

Camera commands: **none**. No upstream execution, dependency/native activation,
firmware/private-input inspection or upload, driver/firmware change or device
contact. No feature support, recovery or device-write gate passed.

Next single reference work package: **FT-101: assess the published FTP implementation,
direct camera-to-server Wi-Fi transfer evidence and reversal/recovery coverage
when available; source-only, no camera contact.** Shared RA-003 work remains separate.
