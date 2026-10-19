# Owner-requested A6700 Powerful source check d

2026-10-19. Topic branch: codex/a6700-reference-check-20261019d.
Starting HEAD: 28610f4. Evidence: source-report, static-inference, offline-tested.

Fresh GitHub main resolves to 0c6294a83988f196adfc980de59f9a1d0b92e8e2, unchanged from the
[33-text / 12-Python static audit](20261019-RA-003-a6700-powerful-audit.md).
Complete recursive tree metadata: 51 entries, 39 blobs. Four immutable documents
match tree byte sizes and Git blob SHA-1 identities; private SHA-256 receipts retained.
No upstream code, installers, launchers or firmware executed; no binaries downloaded.

| Owner priority | Finding |
|---|---|
| Native English | No unlock located in unchanged audited sources or refreshed documents; mainland resource/configuration feasibility remains unresolved. |
| Native Wi-Fi FTP | Author reports completed a6700 2.00 FTP settings and RAW+JPEG transfer. FTP implementation remains unpublished; direct Wi-Fi/no-relay behavior, exact build hashes, server equality, security, persistence and failure handling remain unverified by us. |
| Rollback before firmware writes | Complete physical storage coverage and full restoration explicitly remain unverified. Range readback is insufficient to prove recovery. |
| FL2/FL3 | Offline validation underway; device validation pending. Deferred behind English and FTP. |

Sources at this immutable revision:
[README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md),
[roadmap](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md),
[manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md),
[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

Published device records are a6700 2.00/macOS, without independent confirmation
of our exact mainland body/build or Windows route. The public backup path injects
temporary native camera code using Pico; it is R2 under our policy despite being
described as read-only. No device step is approved by this source review.
The roadmap says features will be deployed as a bundle without individual selection;
that scope would require review before considering any future package.

NOTICE marks authored code/docs GPL-3.0-only and explicitly excludes relicensing
original inherited Pico portions from a pinned upstream lacking an attached licence.
No reuse grant for the whole chain is established; no code or payload adopted.
No legal determination or new agreement acceptance was performed.

Commands and results (all host-side):

- git status --short --branch: codex/ra003-clean-outer-child, two untracked namespace source/test files preserved.
- git log -1 --oneline: 28610f4 feat: qualify invented collected dependency controller composition.
- git switch -c codex/a6700-reference-check-20261019d: exit 0.
- New-Item -ItemType Directory -Path private/sessions/20261019-owner-project-check-d -ErrorAction Stop: exclusive folder, exit 0.
- Copy-Item -LiteralPath private/sessions/20261019-owner-project-check-c/check.py -Destination private/sessions/20261019-owner-project-check-d/check.py -ErrorAction Stop: reviewed host harness copied, exit 0.
- C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-d/check.py: exit 0. Seven bounded HTTPS GETs, no redirects/retries, 2 MiB per response and 30-second timeout; four documents verified. CPython 3.13.12, Windows AMD64.
- Harness unittest.defaultTestLoader.discover('tests', pattern='test_ftps_client_policy.py'): 17/17 passed, zero skips/errors/failures, 1.721332s wrapper. Mocked host policy tests prohibit sockets; they do not qualify upstream FTP or any camera. Full historical suites were not rerun.
- Web tree/main fetch failed; repository root and raw documents succeeded. The host GitHub API harness supplied the fresh immutable pin.
- C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-owner-project-check-d/record.py: creates this report and updates external/internal notes, with exclusive private backups and prior STATE values preserved.
- git diff --check; explicit staging of only the five documentation/state paths; git diff --cached --check and staged content inspection before commit.

Changed public files: this report; docs/BACKLOG.md; docs/CODEX_HANDOFF.md;
docs/FEATURE_PROGRESS.md; research/STATE.json. Private session/feature notes updated
after byte backups. Existing source lock, RA-003 phase/next package, unfinished
namespace source/test and private outer-child work preserved.

Camera commands: none. No author contact, private upload, native payload read,
driver/firmware change, camera operation, feature support claim or recovery/write gate.

Next single reference work package: FT-101, source-only review of published FTP
implementation, direct camera-to-server Wi-Fi evidence and reversal/recovery coverage
when available. Missing prerequisite: publication of implementation and reproducible evidence.
