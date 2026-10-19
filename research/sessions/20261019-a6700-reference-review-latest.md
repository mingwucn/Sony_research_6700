# A6700 Powerful: current public-reference review

2026-10-19. Branch `codex/a6700-reference-review-20261019-latest`.
Evidence: source-report, static-inference, offline-tested.

Main remains **0c6294a83988f196adfc980de59f9a1d0b92e8e2**. No new revision adopted. Commit/tree metadata (39 blobs) and four immutable texts were acquired privately. Byte sizes and Git blob SHA-1 match; SHA-256 receipts are retained. The [earlier 33-file static audit](20261019-RA-003-a6700-powerful-audit.md) remains applicable; source lock unchanged.

| Priority | Finding | Missing evidence |
|---|---|---|
| Native English | No unlock located in earlier inspected source or refreshed documents | Mainland resource/configuration mapping and reversible exact-target method |
| Native Wi-Fi FTP | Author reports settings and RAW+JPEG transfers physically verified on a6700 2.00 | Published implementation, exact build/region identity, direct onboard Wi-Fi/no-relay proof, integrity, security and failure behavior |
| Rollback before writing | Bounded backup route published; full restore and official-firmware rescue explicitly unfinished | Complete coverage and demonstrated recovery envelope for every changed object |
| FL2/FL3, deferred | Offline validation underway, physical validation pending | No validated installable result inferred |

The published route uses Pico-triggered RAM Fastboot: temporary native camera execution (R2), despite describing subsequent storage reads as read-only. Recorded environment is a6700 2.00/macOS; displayed version does not prove mainland binary identity or Windows readiness. The bundled incremental release plan also requires review against our separately gated features.

Authored code/docs carry GPL-3.0-only. NOTICE expressly excludes relicensing inherited Pico portions from an upstream revision without an attached licence. Whole-chain reuse rights and source/binary equivalence remain unresolved. No implementation or payload adopted. This records source notices, not a new legal opinion.

Pinned sources:

- [README.md](https://raw.githubusercontent.com/xyzhangxin/sony-a6700-powerful/0c6294a83988f196adfc980de59f9a1d0b92e8e2/README.md)
- [开发计划与进展.md](https://raw.githubusercontent.com/xyzhangxin/sony-a6700-powerful/0c6294a83988f196adfc980de59f9a1d0b92e8e2/%E5%BC%80%E5%8F%91%E8%AE%A1%E5%88%92%E4%B8%8E%E8%BF%9B%E5%B1%95.md)
- [操作手册.md](https://raw.githubusercontent.com/xyzhangxin/sony-a6700-powerful/0c6294a83988f196adfc980de59f9a1d0b92e8e2/%E6%93%8D%E4%BD%9C%E6%89%8B%E5%86%8C.md)
- [NOTICE](https://raw.githubusercontent.com/xyzhangxin/sony-a6700-powerful/0c6294a83988f196adfc980de59f9a1d0b92e8e2/NOTICE)

## Exact commands and results

Host: Windows AMD64, CPython 3.13.12, C:/ProgramData/miniconda3/python.exe.

- `git status --short`: two pre-existing untracked files, tools/dependency_evidence.py and tests/test_dependency_evidence.py. Preserved; excluded from staging and this test scope.
- `git branch --show-current`: initially codex/ra003-successor-dependency-contract.
- `git log -1 --oneline`: 465c2cb docs: reconcile saved dependency proof and identify native contract gaps.
- `git switch -c codex/a6700-reference-review-20261019-latest`: exit 0.
- Host-authored standard-library acquisition through `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -`: exit 0. GET GitHub API repos/xyzhangxin/sony-a6700-powerful/commits/main, then git/trees/<resolved-commit>?recursive=1 under the same repository prefix; GET only the four linked pinned raw texts. Compare size and Git blob hash against tree; retain SHA-256 receipts. Initial web tree/main failed; repository root and raw text succeeded. No binaries fetched.

Exact generated test child argv (JSON array; retained verbatim in private tests.json):

```json
[
  "C:\\ProgramData\\miniconda3\\python.exe",
  "-I",
  "-S",
  "-B",
  "-X",
  "utf8",
  "-c",
  "import sys,unittest;sys.path.insert(0,'.');s=unittest.TestSuite();l=unittest.defaultTestLoader;s.addTests(l.discover('tests',pattern='test_artifact_probe.py'));s.addTests(l.discover('tests',pattern='test_candidate_guards.py'));s.addTests(l.discover('tests',pattern='test_durable_transaction.py'));s.addTests(l.discover('tests',pattern='test_fdat_header.py'));s.addTests(l.discover('tests',pattern='test_fdat_probe.py'));s.addTests(l.discover('tests',pattern='test_ftps_client_policy.py'));s.addTests(l.discover('tests',pattern='test_offline_inventory.py'));s.addTests(l.discover('tests',pattern='test_prepare_ftps_lab.py'));s.addTests(l.discover('tests',pattern='test_transaction_model.py'));s.addTests(l.discover('tests',pattern='test_transfer_queue.py'));s.addTests(l.discover('tests',pattern='test_ufu_inventory.py'));r=unittest.TextTestRunner(verbosity=2).run(s);raise SystemExit(not r.wasSuccessful())"
]
```

**228 cases: 225 passed, three platform skips, exit 0; 16.068s suite / 16.520155400037766s wrapper.** Discovery uses git ls-files tests/test_*.py, then each tracked test basename; unrelated untracked tests excluded. Skips cover unavailable fork and real symlink cases. These are our standard-library host regressions, not upstream behavior, frozen private gate suites or camera tests. No executable source changed in this review.

Changed files: this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md and research/STATE.json. Private session/feature notes updated with exclusive backups. Only these five public paths staged; no push. Unrelated untracked implementation remains unfinished and untouched.

Camera commands: **none**. No firmware/constants/native payload reads, upstream execution, dependency installation, private upload or device/driver changes. English/native FTP support, operational acceptance, recovery and device-write gates remain unpassed. Shared RA-003 blockers and next package preserved.

## Next single reference work package

**FT-101: assess published FTP implementation and direct camera-to-server Wi-Fi evidence against the existing [source-only checklist](20261019-a6700-powerful-recheck.md) when available.** No author contact or camera action requested. Shared offline RA-003 work can continue independently.
