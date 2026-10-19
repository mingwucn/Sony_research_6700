# RA-003: source receipt consistency and composed preflight

2026-10-20; finalized on `codex/ra003-source-receipt-finalize` from `973dd7f`.
Evidence: **offline-tested**, **static-inference**. English and native Wi-Fi FTP remain primary; FL2/FL3 deferred. No feature support or device-write gate follows.

## Result and limitations

New `tools/dependency_source_receipts.py` checks the two invented authored-source manifest/receipt roles and composes them with the existing six basis-role and two dependency-role validators using the same source, ordinary and historical buffers. The full integration test uses the actual retained validators without stubs. Ten ordinary contracts are checked; four remain: activity_rights, activity_scope, historical_evidence_index and qualification_index.

The closed manifest and receipt rosters contain 44 authored source roles, including the host and protected-role source texts. Source sizes/hashes bind exact buffers; the 26 role path/hash identities bind prerequisites. Paths and physical identity pairs must be distinct and avoid protected-input labels. Each source is capped at 2 MiB, aggregate 32 MiB. Receipt checks reuse existing regular-file, read-only, no-hardlink/reparse, stable lstat/fstat and cross-identity predicates. One close and one EOF are required as claims. Cross-API ctime/attribute equality is not required by the retained contract.

The caller's external source anchor binds original manifest, receipt and dependency-anchor bytes, with matching sidecar operation IDs. Receipts also bind original manifest bytes. Unknown fields, wrong mode/rosters, stale hashes, operation mismatches, source aliases, incomplete reads, unknown close completion and anchor cycles refuse. Caller-selected anchors establish consistency, not independent prior review, owner permission, authenticity or freshness. The root path remains a label, not an observed directory ancestry.

The metadata API explicitly reports source_reads_observed=False and source_freshness_verified=False. It also leaves dependency bridging, complete saved semantics, actual startup and candidate-operation authority false. A self-consistent invented timestamp rebind can pass without establishing freshness. The 44-role comparison inventory is not a complete operational runtime closure or allowlist. Retained plan/successor dependency compatibility remains unproved. Protected validator/capture/core source texts are hashed and AST-checked, never executed; only the retained binding and ten ordinary preflight modules execute. Runtime entry refuses; direct CLI exits 2 before imports.

## Qualification and evidence reconciliation

Accepted final qualification: **130/130 passed**, zero failures/errors/skips, exit **0**; **96 retained + 24 new public + 10 private integration/reader cases**. Wrapper 16.237161699973512s, suite 16.217s. All **96** source/test/scope/lock/fixture pins remain unchanged when reverified at finalization. Log SHA-256 `a2778849ad8b7d86ba6df02527d8b8cbdd37593796eda05936e3f305b5042e8b`. Installed dependency alias list empty.

Three private reader tests operate only on newly created invented temporary `.py` files. The full reader case observes 44 read-only opens, 88 reads, 44 EOFs and 44 closes, checks returned buffer equality and feeds converted receipts to the pure API. Short reads and unknown close completion refuse without retry or publication. These observed invented-file operations are separate from the API's unobserved metadata claims; no actual protected input is opened.

Earlier 125-case and 130-case runs passed. Independent review identified a qualification-loader ownership gap: prior code was hashed then reloaded by path. The accepted `buffer-owned` qualifier captures the prior authored qualifier once, checks its fixed SHA-256 and compiles/executes those exact bytes in a detached module. Earlier evidence is preserved and is not relabeled as proving this stronger property. No failed tests or acceptance-threshold changes were concealed. Independent source-only review accepted final code, tests, all pins, log and result. Historical full suites were not repeated.

Public module SHA-256: `6c2112dcb9a2529156c8815f7c9970cb6c8c2a84fd4718496f4845c41a53e71e`.
Public tests SHA-256: `76c87f34f2afafa62e3578ccfe3c171333ce2d566da0561e4601acb7654c721e`.
Accepted qualifier SHA-256: `ede0f0781efe3344359b1da9aed8f67954f20822be5e20c3540568303b35fdeb`.
Accepted result SHA-256: `413dca80c749a4a2dc28940c0538368d0fccc78bc83aa708aa15b9e06ad14acd`.

## Commands and results

Interpreter: CPython 3.13.12, Windows AMD64, `C:/ProgramData/miniconda3/python.exe`; isolation flags `-I -S -B -X utf8`.

```powershell
git switch -c codex/ra003-source-receipt-compose
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-source-receipt-compose/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-source-receipt-compose/final/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-source-receipt-compose/buffer-owned/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_source_receipts.py
git switch -c codex/ra003-source-receipt-finalize
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_source_receipts'));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-source-receipt-compose/finalize_notes.py
git diff --check
```

Branch commands exit 0. Qualification commands exit 0 with 125/130/130 cases respectively; CLI intentionally exits 2. Finalization public regression: 24/24, exit 0, 2.697s. A separate standard-library stdin verifier recomputed every saved source pin and log SHA, checked accepted total/exit code and printed 96 verified pins, 130 passes and invented I/O counts; exit 0. Saved qualifiers use exclusive output creation and are not rerun over existing evidence. Initial diagnostic reads of absent dependency_ordinary_io.py/dependency_outer_io.py were corrected by finding the pinned authored reader; no upstream tool ran.

Changed public files: new source module, new public test module, this report, docs/BACKLOG.md, docs/FEATURE_PROGRESS.md and research/STATE.json. Private session and feature notes updated after exclusive original-byte backups. Source refresh commit 973dd7f is preserved. Only six reviewed public paths are staged.

Previous goal turn completed an unchanged reference refresh without new shared implementation evidence. Current turn is **progress**: reconciled and finalized the qualified ten-role composition. Full pre-camera objective remains active.

## Remaining prerequisites

The four remaining ordinary contracts, legacy bridge, complete semantics/truth/freshness, independent reviewer/owner authority, current interpreter/bootstrap ownership and actual startup remain unresolved. Existing owner inspection-rights answer remains **No / unknown**; this package establishes no activity-specific legal basis. No actual activation packet is prepared. Exact-body correspondence, native English, native Wi-Fi FTP and practical recovery remain unverified.

Camera commands: **none**. No firmware/constants/native payload/saved stream reads, installed dependency activation, upstream execution, downloads/uploads or camera contact in this package. Earlier source refresh is separately recorded.

Next single work package: **RA-003: implement, review and qualify the remaining four ordinary metadata contracts (activity scope/rights, historical-evidence index and qualification index), binding exact current authored sources and qualification evidence. Preserve unresolved rights, authority, freshness, startup and legacy dependency bridge gaps. Invented records only; runtime disabled; no actual firmware/constants/native payload reads or camera.**
