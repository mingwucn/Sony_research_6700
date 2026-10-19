# RA-003: saved dependency-policy gap audit

2026-10-19. Branch `codex/ra003-dependency-policy-gap-audit`.
Evidence: **static-inference**, **offline-tested**. Previous goal turn: **progress** (reference revision/evidence limits verified and committed). Current goal turn: **progress** (saved manifest/proof reconciled and concrete native-contract gaps established).

## Findings

The [predicate matrix and closed successor proposal](../DEPENDENCY_POLICY_GAP_AUDIT.md) distinguish missing inputs in the historical plan from evidence acquired later. One source-reviewed saved-record comparison completed, exit **0**, **0.243941199965775s**, without retry. The unchanged pure validator accepts the saved manifest and all **351** installed receipts. The saved installed proof passes its own exact schema and equals the canonical recomputation. No wheel, installed package, firmware, constants or native payload was opened.

The later continuation has **11** package Python origins, **11** historically fresh source receipt rows, and **5** native intents/completions. All **5** trusted external origin paths are refused by the old relative-path predicate. Its raw native receipt is a different schema: the old closed receipt shape refuses it with `native_receipt:invalid_shape`. These are contract differences, not evidence of faulty dependency execution or a reason to strip paths/rename fields. The expected policy, trusted bootstrap, package membership, event ordering and durability bindings need an explicit successor design.

Static inspection also finds the continuation's public-vector loop precedes `guard.finish()` (reviewed `runtime_entry.py` lines 287–300). Durable completion before its callback therefore does not establish the old `complete_before_cipher_use` assertion. The successor must preserve this distinction rather than manufacture a true flag.

Both old blockers (`dependency_manifest_unobserved`, `native_policy_unobserved`) remain in the historical binding plan; no plan was rewritten or blocker cleared. Operational readiness and full historical-event authenticity remain false. The six saved input hashes were checked again after comparison; both historical pure source copies remain unchanged. Actual runtime behavior was not repeated.

An existing six-item FTP reference checklist was located in [the earlier recheck](20261019-a6700-powerful-recheck.md). Its implementation/evidence prerequisite remains unpublished in the pinned tree; this session did not duplicate it or re-fetch unchanged upstream material. Shared RA-003 work can proceed offline while that reference lead waits. English/native FTP remain primary; FL2/FL3/custom looks remain deferred and the optional bridge separate.

## Review and qualification

The initial **14/14** invented tests passed, zero skipped, exit **0**, **0.278s** (wrapper **0.49197229999117553s**). A local source-only reviewer found two real gaps before saved-record application: Python equality admitted type-equivalent but schema-invalid saved proof values; unbounded file reads did not enforce the ordinary-file boundary. The initial source/test snapshots and logs are preserved privately.

The revised script validates the saved proof itself before canonical comparison. Six fixed JSON paths are pinned/closed as a roster; each read is bounded to **8 MiB**, the pure source to **1 MiB**. It checks ancestor directory/type/reparse state, ordinary regular single-link files, before/open identity, same-API stability, EOF/length and unchanged ancestor identities. Reads use read-only descriptors, with `O_NOFOLLOW` where available. These checks are not a hostile-filesystem sandbox, OS-mapped-byte attestation or a process-memory cap.

Final qualification: **22/22 tests passed**, zero skipped, exit **0**, **0.527s** (wrapper **0.8430001999950036s**). Eight additional cases cover the saved-proof composition and bounded ordinary-file helper. Independent source re-review accepted the narrow comparison with no remaining scoped findings. Tests do not cover complete `main()` substitutions, active filesystem races or close failures, and do not implement/qualify the proposed successor contract. Historical full suites were not rerun; no production source changed.

## Exact substantive commands and results

Working directory: `D:\LocalWork\Sony_research_6700`. Host: Windows AMD64, CPython **3.13.12**, `C:\ProgramData\miniconda3\python.exe`.

```powershell
git status --short --branch
git switch -c codex/ft101-reference-evidence-checklist
git branch -m codex/ra003-dependency-policy-gap-audit
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-dependency-policy-gap-audit/test_contract.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-dependency-policy-gap-audit/check_saved.py
git diff --check
```

Starting tracked tree clean on `codex/a6700-reference-recheck-20261019`, commit `459e6d8`. Branch commands and final commands exit **0**. The test command ran during development (14 cases, 0.275s), final initial qualification (14, 0.278s), revised development (22, 0.489s) and final qualification (22, 0.527s); all exited **0**. Only **one** saved comparison ran, after review. Standard-library stdin wrappers under the same interpreter/flags saved exact argv, raw output, elapsed times and source/result SHA-256 receipts exclusively. A separate stdin output verification checked six unchanged input hashes, two historical pure copies and all false-authority claims, exit **0**; it did not replay validators or load dependencies.

- Comparison source SHA-256: `11d9b0f208c319429814c5d4a24f55890a98546eefa4bd9bdc02891a93aafc51`.
- Test source SHA-256: `be2e6f00dc0d9ccbe5e8918bc01ce3a0624c7b190602c7875ec1643e69d01e2e`.
- Unchanged authored pure snapshot SHA-256: `22558080636f15300590c22b9987216216f650b4edc58d7df89092643722de74`, bound by the previous 114-pin freeze.

Reviewed tracked changes: this report, `research/DEPENDENCY_POLICY_GAP_AUDIT.md`, `research/STATE.json`, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `docs/CODEX_HANDOFF.md`. Private session/feature JSON and feature prose updated after exclusive backups. Stage only these six reviewed paths; no push. Source lock unchanged. JSON and whitespace checks pass.

Unresolved prerequisites: implementation/qualification/review of the successor expectation/observation contract, complete operational chain acceptance and separate activity decision before protected-input work; exact body/build/feature correspondence; backup coverage and demonstrated rollback/recovery before any eventual device write. No additional owner fact is needed for the next offline package. No private upload, download/install, agreement acceptance, dependency/native execution, firmware read or camera operation occurred. Camera commands: **none**. Feature/recovery/write gates remain unpassed.

Next single work package: **RA-003: implement the closed successor dependency/native-evidence contract on invented inputs, preserving root domains, bootstrap boundaries and event/durability ordering; independently review it before applying it to saved actual receipts or authorizing any runtime/protected-input act.**
