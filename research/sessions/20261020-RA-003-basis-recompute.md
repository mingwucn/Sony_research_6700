# RA-003: retained basis and binding-plan recomputation

2026-10-20 local date. Topic branch: `codex/ra003-basis-recompute`.
Starting HEAD: `507b300`; existing untracked `tools/dependency_basis_links.py` was inspected and completed as part of this package.
Evidence: **static-inference**, **offline-tested**. English and native camera-to-server Wi-Fi FTP remain primary; FL2/FL3 deferred, calibrated custom looks later and separately gated, optional bridge HOST-ASSISTED.

## Result and scope

The previous [two dependency-role checks](20261019-RA-003-dependency-input-semantics.md) remain separate. This continuation adds checks for six ordinary roles: `basis`, `source_manifest`, `prerequisites`, `role_authority`, `binding_schema`, `binding_plan`. It compares the complete retained binding plan, including blockers, namespace bindings, lazy imports and false readiness flags, and recomputes the nine-role basis with the retained pure GDT preflight.

`tools/dependency_basis_links.py` is pure consistency checking. It intentionally cannot authenticate caller-supplied recomputations. `tools/dependency_basis_recompute.py` first validates the invented four-document envelope, requires the exact frozen review packet, and verifies byte sizes/SHA-256 of the retained binding validator and all 26 authored role sources before executing any owned source.

Only the binding validator plus ten preflight modules execute: acceptance, link acceptance, member acceptance, metadata preflight, expanded gate, ext superblock, ext preflight, ext read planner, ext gate and GDT preflight. All 26 source import graphs are AST-checked against the retained contract. The three protected roles (`validator`, `capture`, `core`) are hashed and AST-inspected only; their code is never compiled or executed. The remaining ordinary modules need not execute to recompute these two pure contracts.

Modules are detached Python objects with checked-buffer import redirection. No authored module is imported from disk and no process `sys.modules` alias is installed or removed. Full graph compilation precedes execution. Integrity checks cover owned globals, mutable constants, function replacements/code/defaults/closures/wrappers and authored class methods. Cleanup clears owned references, preserves foreign aliases, refuses reuse and preserves the primary exception if cleanup also fails. This is trusted reviewed source composition, not a hostile-code sandbox or authentication of the Python interpreter/standard library.

Manifest size/hash agree with the basis's package identity and candidate's protected package record. Constants hash and metadata shape agree without opening constants. All 26 role hashes agree across qualified roles, binding input and authority records; unsafe/aliased private path labels refuse. These labels do not establish observed file origins or current filesystem receipts.

The exact scope packet remains SHA-256 `928027b9f240aa114c9ae03fd5e0d852435c8911299c5ce9c671f8632d60c44d`. It is a frozen comparison authority for these host validators, not an operational allowlist. Source lock and inherited source files remain unchanged. The integration fixture uses the existing explicitly invented nine-role JSON, pinned at `2c89e2958a68b3bf937427494279663e3691f9e7a45a3e217c041b5e620fb167`; its hypothetical package is 95,554 bytes. No associated stream file is read.

## Qualification and independent review

Final **96/96 passed**, zero failures/errors/skips, exit **0**: **66 retained + 12 new public linkage + 18 new private composition tests**. Suite **10.464s**, wrapper **10.482354000036139s**, CPython **3.13.12**, Windows AMD64. All **93** source/test/scope/lock/invented-fixture pins stayed stable. No installed Crypto/Cryptodome/cffi aliases loaded. Log SHA-256: `b8fa07447a1507125ce8ac4594dcb14463f2ccaeaa2f29ac0382ae721df748f1`.

Negatives include all 26 changed role sources, changed binding bootstrap/frozen packet, changed full-plan blockers/hidden fields, relaxed schema, malformed basis, rebound source/protected identities, wrong role authority, protected/unknown imports, protected loader roster, function/wrapper/class-method mutation, compile-before-execute, partial-load interruption, cleanup failure, preserved foreign aliases and unused dependency inputs explicitly remaining pending. The public linkage-only positive deliberately accepts fabricated recomputations while returning `recomputation_authenticated=false`; the integration independently recomputes the retained contracts.

The owner-authorized source-only reviewer accepted final code, tests and result evidence, including all 93 pins and 96 logged outcomes. Review found and corrected overstated pending-role reporting and omitted class-method integrity checks before final qualification. No review agent executed code or accessed actual inputs.

Final code SHA-256:

| File | SHA-256 |
|---|---|
| `tools/dependency_basis_links.py` | `f980777f1b61576dcd1f07790a02c3e09ab26364c1c33a4debfc63d51e54f2a0` |
| `tools/dependency_basis_recompute.py` | `6b6609e21a7421eadb2030cc45cf4f5383a0ebdf500f114e00d1203a346efa46` |
| `tests/test_dependency_basis_links.py` | `7563b4bf8e1ae66eaafcbe4075ec4405abc41a9d173e0d1f033a17811f903f82` |

Initial qualifier failed before tests (exit 1): its fixture reader incorrectly treated the retained CONTRACT literal as a `json.loads` call. It was repaired to `ast.literal_eval` the actual dictionary, without executing it. An intermediate qualification passed 85/85, exit 0, **9.975693899963517s**; final adds nine retained outer-contract cases and two explicit boundary regressions, and renames a misleading output field. Original logs/results are retained; no passing threshold changed. One diagnostic `rg` invocation used an unsupported PowerShell glob and exited 1; a corrected search succeeded. Historical full suites were not rerun.

## Exact principal commands and results

```powershell
git status --short --branch
git switch -c codex/ra003-basis-recompute
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-basis-recompute/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-basis-recompute/final/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_basis_links.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_basis_recompute.py
git diff --check
```

Branch/status commands exit 0. First qualifier invocation exit 1 before tests as recorded above; corrected invocation exit 0 (85 cases). Final qualifier exit 0 (96 cases). Both direct module CLIs intentionally exit **2** before imports. Diff checks exit 0. Private qualification logs/results are created exclusively; prior private session/feature notes are backed up exclusively before updates. Only reviewed authored sources/tests and sanitized notes are staged. No upstream launcher, service tool or camera command runs.

Changed tracked files: two new modules, one new public test module, this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `research/STATE.json`. Private qualification and session/feature notes are not staged.

## Remaining prerequisites and next work

This API reports **eight pending ordinary roles**, including the two dependency roles it does not revalidate. Those two have their own prior API/anchors and are exercised in the retained regressions; this is not a single composed eight-role operational validation. The other six roles are authored-source manifest/receipts, activity scope/rights, historical-evidence index and qualification index (the existing envelope already checks historical index receipts, not freshness). Compatibility of the retained legacy dependency plan with the successor dependency packet remains unproved.

Retained basis preflight is not complete semantic validation of every saved claim, historical truth or freshness. The empty invented alias roster supplied to plan preparation is not this process's actual startup state. Reviewer/owner authority, independent expectation authority, current interpreter/bootstrap identity, actual source-origin receipts and activity-specific operational rights/decision remain unresolved. Existing firmware-inspection rights answer remains **No / unknown**; no rights question is resolved by these tests. Exact-body correspondence, English/native FTP, recovery and device-write gates remain unverified.

Previous goal turn: the requested reference refresh completed, but the unchanged source yielded no new shared pre-camera implementation progress. Current goal turn: **progress**, six-role retained-contract recomputation now implemented, independently reviewed and qualified. Full goal remains active.

Camera commands: **none**. No actual firmware, constants, saved raw prefixes/stream, native payload or installed dependency activation; no camera, download, upload, upstream execution or feature/write/recovery gate.

Next single work package: **RA-003: implement and qualify the current authored-source manifest/receipt binding, then compose the six basis-role and two dependency-role validators against that same checked source inventory and explicit dependency anchors. Reject source rebinding/stale receipts without treating labels as observed origins. Keep legacy-plan/successor-dependency compatibility and remaining activity/qualification authority gaps explicit; runtime stays disabled, with no actual firmware/constants/native payload reads or camera.**
