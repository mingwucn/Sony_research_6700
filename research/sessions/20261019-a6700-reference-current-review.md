# A6700 Powerful: owner-requested current review

2026-10-19. Branch: `codex/a6700-reference-current-review`.
Evidence: source-report, static-inference, offline-tested. No independent camera reproduction.

Current main is **0c6294a83988f196adfc980de59f9a1d0b92e8e2**, unchanged from the source lock and [33-text / 12-Python source audit](20261019-RA-003-a6700-powerful-audit.md). Fresh GitHub ref, commit and complete recursive tree metadata identify 51 entries / 39 blobs. README, development plan, operation manual and NOTICE were retrieved at the immutable revision and verified by byte size and Git blob SHA-1; SHA-256 receipts remain private. The earlier static code findings remain applicable; this refresh did not re-audit every source file.

| Owner priority | Published evidence | What it establishes here |
|---|---|---|
| Native English | No English unlock found in the prior text/source audit or refreshed documentation | Unresolved for the mainland body; no change in feasibility status |
| Native Wi-Fi FTP | Author reports FTP settings and RAW+JPEG transfers physically verified on a6700 2.00 | Useful exact-model/version lead; implementation and reproducible transfer evidence are not published in the inspected tree |
| Rollback before writing | Bounded storage reads documented; complete restoration and official-firmware rescue expressly unfinished | Does not meet the owner's recovery prerequisite |
| FL2/FL3, deferred | Offline work reported; physical validation pending | No validated installable result |

The published access route needs Pico/hardware intervention and temporary native Fastboot execution in camera RAM (R2 under our policy), despite describing subsequent storage reads as read-only. Device records are scoped to a6700 2.00/macOS. This does not establish Windows readiness or matching mainland SKU/build/binary identity. No identifiers, addresses or offsets were adopted. The roadmap's proposed bundled incremental feature release also differs from our individually gated English/FTP scope.

FTP remains **source-report**, not our runtime observation. Still needed: published unlock/backend code, exact target/region/build constraints, camera-resident Wi-Fi without a PC/phone relay, server-side file equality, persistence, credential/security handling, interrupted transfer/retry tests, and a reversible change with proved recovery coverage. Existing host FTP mocks cannot supply these facts. A host-assisted bridge remains separate.

NOTICE states GPL-3.0-only for authored code/docs, but expressly excludes relicensing inherited Pico portions from an upstream revision without an attached licence. No blanket whole-chain reuse permission, source/binary equivalence, or payload safety is inferred. No third-party implementation or binary was copied into Git.

Sources at the checked revision:

- [README](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md)
- [Development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/开发计划与进展.md)
- [Operation manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/操作手册.md)
- [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE)

## Commands and results

Host: Windows AMD64, CPython 3.13.12 at `C:/ProgramData/miniconda3/python.exe`.

- `git status --short --branch`: initial branch `codex/ra003-binding-localization`, two unrelated untracked diagnostic source/test files; preserved unstaged. HEAD `2b17c76`.
- `git switch -c codex/a6700-reference-current-review`: exit 0.
- Host-authored acquisition script piped to `& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -`: exit 0. Seven bounded GETs, timeout 30s each, at most 2 MiB per response, no redirects/retries. GitHub API paths: `/repos/xyzhangxin/sony-a6700-powerful/git/ref/heads/main`, `/git/commits/<resolved SHA>`, `/git/trees/<commit tree SHA>?recursive=1`; four raw text URLs at the pinned revision above. No upstream code imported/executed; no binary/payload downloaded. Exact URLs, sizes and hashes: ignored session `receipt.json`.
- Host-authored unittest logging harness piped to the same exact interpreter invocation: exit 0; **17/17 host FTP policy tests passed**, zero skips, **1.579s** suite / **1.7292391999508254s** wrapper. Test selection/execution expression:

```python
sys.path.insert(0, str(pathlib.Path.cwd()))
unittest.TextTestRunner(stream=log, verbosity=2).run(
    unittest.defaultTestLoader.discover('tests', pattern='test_ftps_client_policy.py'))
```

These are our synthetic host policy tests; no server socket or camera connection, upstream behavioral qualification, native camera FTP or recovery test. Raw log and interpreter receipt remain private. The separately running inherited full host suite was allowed to finish on its original handle (403 cases, 400 passes / three skips, exit 0); it includes unrelated pending diagnostic files and is not a reference-project qualification. No diagnostic application was run for this request.

Public changes: this report, STATE, BACKLOG, FEATURE_PROGRESS and CODEX_HANDOFF. Private session-state and feature notes updated after exclusive backups. Source lock, shared RA-003 phase/next package and unrelated untracked work preserved. Only reviewed public documentation is staged. JSON parsing and `git diff --check` passed (exit 0); staged paths/content reviewed explicitly before commit.

Camera commands: **none**. No firmware, cache-body or native-payload access; no private upload, dependency install, upstream launcher or author contact. No feature/recovery/write gate passed.

Next single reference package: **FT-101: assess the published FTP implementation and direct Wi-Fi transfer evidence against the existing checklist when available.** The separate pending RA-003 binding-localization package is unchanged.
