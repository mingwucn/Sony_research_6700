# Owner-requested A6700 Powerful assessment

2026-10-19. Branch `codex/a6700-reference-assessment`; starting tree clean at
`6566249`. Evidence: **source-report**, **static-inference**, **offline-tested**.

Fresh main-ref and recursive-tree metadata resolve to the existing source-lock
revision `0c6294a83988f196adfc980de59f9a1d0b92e8e2`: 51 entries / 39 blobs.
README, development plan, operation manual and NOTICE match their pinned Git
blob IDs and sizes. The unchanged implementation findings come from the
[earlier 33-text / 12-Python static audit](20261019-RA-003-a6700-powerful-audit.md);
this session is a current identity and document check, not a fresh full-code audit.

| Owner requirement | Finding | Outstanding evidence |
|---|---|---|
| Native English, primary | No English unlock found in prior code audit/current documents | Mainland resources/selection feasibility; exact-body compatibility |
| Native Wi-Fi FTP, primary | Author reports a6700 2.00 FTP settings and RAW+JPEG physically verified | Published implementation; direct Wi-Fi/no relay, full server equality, persistence, authentication and failure behavior |
| Rollback before writes | Partial readback route published | Full backup/restoration and official-firmware rescue explicitly unfinished |
| FL2/FL3, deferred | Offline validation underway | Physical validation pending |

The published route temporarily runs a Fastboot payload in camera RAM using Pico:
project R2, requiring separate exact-step approval. It is not ordinary camera
identification. Device records are scoped to a6700 2.00/macOS; they do not establish
our Windows host, mainland SKU/build or owner's body compatibility. The roadmap
proposes bundled incremental features, which needs separate review against our
individually gated English/FTP scope. No offsets, binaries or target identifiers
were adopted.

NOTICE assigns GPL-3.0-only to authored material while explicitly declining to
relicense inherited Pico portions from an upstream revision without an attached
licence. Whole-chain reuse rights remain unresolved; no implementation adopted
or redistributed. Matching version text alone does not close any target gate.

Sources: [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md),
[development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md),
[manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md),
[NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE).

## Commands and results

- `git status --short --branch`: clean inherited branch `codex/ra003-child-entry-qualification`.
- `git switch -c codex/a6700-reference-assessment`: exit 0.
- Host-authored stdin script: `& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -`: exit 0. Six bounded HTTPS GETs: GitHub main ref, recursive tree at the resolved SHA, four pinned raw text documents. Each limited to 2 MiB and 30 seconds, redirects refused, no retries. Sizes/Git blob SHA-1/SHA-256 verified and saved privately. Initial web `/tree/main` fetch failed; repository root/raw pages and API acquisition succeeded.
- Same interpreter, CPython 3.13.12 on Windows AMD64, ran exactly:

```python
sys.path.insert(0, str(pathlib.Path.cwd()))
unittest.TextTestRunner(stream=log, verbosity=2).run(
    unittest.defaultTestLoader.discover('tests', pattern='test_ftps_client_policy.py'))
```

**17/17 passed**, zero skips, exit **0**, **1.6632565999752842s** wrapper.
Tests mock our host FTP policy and prohibit socket creation; they do not qualify
upstream camera behavior. Full suite not repeated for this documentation-only
assessment. Private log SHA-256:
`7d0883a7430ffd18ff7c3646b17a14141822cfadeddc74445a24390ddf136672`.
JSON parsing, preservation of existing state fields, and staged diff checks passed.
A read of nonexistent `tests/test_offline_guards.py` failed during file discovery;
no test failure or implementation change resulted.

Changed public files: this report, `research/STATE.json`, `docs/BACKLOG.md`,
`docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`. Private session/feature notes
updated after exclusive byte-for-byte backups. Source lock, shared RA-003 phase,
its next package and latest full-suite record remain unchanged. No private input,
third-party implementation or payload staged. No upstream launcher, installed
dependency, firmware or camera operation performed; no upload or author contact.
Camera commands: **none**. No feature, recovery or device-write gate passed.

Next single reference package: **FT-101: assess the published FTP implementation, direct camera-to-server Wi-Fi transfer evidence and reversal/recovery coverage against the existing checklist when available; source-only, no camera contact.**
Publication remains the prerequisite; this assessment does not activate the
separate RA-003 dependency package.
