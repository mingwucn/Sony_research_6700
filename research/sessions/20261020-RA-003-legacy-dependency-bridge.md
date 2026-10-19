# RA-003: retained legacy and successor dependency comparison

2026-10-20; branch `codex/ra003-legacy-dependency-bridge`, base `7604346`.
Evidence: **static-inference**, **offline-tested**.

## Finding and implementation

The preceding fourteen-role full invented fixture passes its separate contracts despite differing legacy and successor wheel hashes. The new cross-comparison refuses it at `bridge_wheel`. This is an inconsistency in invented qualification records, not an observation of an actual installation. No previously recorded test result is erased or relabeled: its earlier scope lacked this cross-check.

New pure `tools/dependency_legacy_bridge.py` composes all fourteen retained role checks, a separate externally pinned bridge anchor and a retained successor packet binder. It requires exact equality of the legacy plan and prerequisite dependency records, version and wheel identity, and any non-null RECORD, file-roster and native-policy fields. Missing legacy RECORD/files/native fields are reported, never inferred or silently populated. Mismatching supplied values refuse. Deliberately aligned invented fixtures show partial diagnostics and full common-plan comparison; these are not changes to actual dependency records.

The explicit native-policy projection retains package-relative Python/native origins and maps trusted runtime origins to legacy backend origins using a relative-path-only copy of each full receipt. The token is the canonical JSON SHA-256 of that projected receipt; original absolute receipt bytes remain externally pinned and unchanged. Projection rejects relative-label collisions across otherwise distinct roots. Read-only/regular-file/no-hardlink/no-reparse/stable-identity predicates reuse the retained receipt checker. This selected representation is not evidence that any historical legacy token used that domain.

The bridge anchor binds original binding plan/prerequisites/dependency packet/fixed record bytes, original source/dependency/activity anchor bytes, all five trusted receipt buffers and explicit successor operation/source map/source hashes/config/cache/root/loader/bootstrap/manifest/proof context. It has a closed invented schema and matching operation. Trusted buffers are metadata JSON, not actual runtime files. The lower comparison helper checks the fixed expectation object via the retained binder but only format-checks the dependency anchor's original fixed-file digest; its documented boundary is tested. Full API separately revalidates original fixed bytes and all prior external anchors via the fourteen-role checker. Neither API grants authority.

**Legacy format cannot express operation ID, source mapping, cache bytes, root identity, loader kwargs or bootstrap boundary.** The successor supplement pins these claims but cannot backfill absent historical bindings. Even complete shared metadata leaves legacy-context binding, original token provenance, source mapping observation, cache freshness, full bridge verification, startup, execution, recovery and feature/write authority false. The new comparison does not replace the frozen legacy source guard or modify a legacy schema to make it proceed. Runtime entry remains disabled.

## Verification

Accepted focused run: **181/181 passed**, zero failures/errors/skips, exit **0**; **156 retained + 19 new public + six private integration cases**, **39.99450319999596s wrapper / 39.973s suite**. All **102** source/test/fixture/scope/lock pins stable. Installed Cryptodome/Crypto/cffi alias list empty. The previous three invented-file reader tests remain historical evidence and were not rerun here.

Integration covers original full fourteen-role wheel-conflict refusal, explicitly matched wheel with three missing fields, fully populated common metadata passing both the pinned legacy preflight and successor binder, stale/cross anchors, closed projection/operation/absent-context labels, raw trusted receipt drift, rebound cache context and rebound read-write claims. Public tests cover individual missing fields, all shared identities, native groups/backend/suffix/no-fallback, relative token domain, relative-root collision, trusted receipt identity/type/read-only predicates, source alias injectivity and exact successor contexts. All original records remain unmodified by the pure API. Independent source-only review accepted code/tests/evidence and checked all pins/log counts.

The qualifier loads prior authored qualification code from one captured buffer after checking fixed SHA-256 `c7259c50fd267d1d1f13b2e7f73c39b2c87070f321d9ac494b255124732f52f6`. It reads authored `.py` texts and the pinned invented basis JSON only. Protected-role source texts are hashed/AST inspected; protected validator/capture/core code is not executed. No installed package, native file, firmware/constants or raw stream is read.

Log SHA-256: `831e8571bd708d472dcc82d1e8d954890f278c942c3f69b00600f2d76aa230ca`.
Module SHA-256: `225743426bf7ac03ebc5dd47840b579e0b984e65d9e7e5ce688f1eb193be8d0e`.
Public tests SHA-256: `e535852d16ef00b6abded5e832e3cbf6ddfbb8f66825d09a23781612befb9044`.
Qualifier SHA-256: `42111307d9274c34fd97d80e92cb1a0c6a0995b492b147c70dc17bd57ed8bb63`.
Result SHA-256: `7aebf4cea99e74b09d8d2a7a4e7b9670c30e74317010695cef99e9725019a95f`.

## Exact commands and results

Host: Windows AMD64, CPython 3.13.12 at `C:/ProgramData/miniconda3/python.exe`.

```powershell
git status --short --branch
git switch -c codex/ra003-legacy-dependency-bridge
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_legacy_bridge'));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_legacy_bridge'));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-legacy-dependency-bridge/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import subprocess,sys;r=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','tools/dependency_legacy_bridge.py']);print('CLI child exit:',r.returncode);raise SystemExit(0 if r.returncode==2 else 1)"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-legacy-dependency-bridge/record.py
git diff --check
```

Branch/status commands exit 0. Initial public run: 16 cases, one pass and **15 errors**, exit 1, because its public skeletal basis-link fixture has no dependency field. Corrected the test constructor to supply an explicit invented legacy plan; no production guard or acceptance threshold changed. Corrected preliminary run: 16/16, exit 0, 7.072s. Three more targeted public cases were then added and the final 181-case run passed as above. CLI child intentionally exits 2; checking wrapper exits 0. Standard-library stdin verifier recomputed all 102 pins and log digest, exit 0. Qualification logs/results created exclusively; full historical suites not repeated.

Changed public files: new module, new public tests, this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md and research/STATE.json. Private session/feature notes updated after exclusive backups. Only seven reviewed public paths staged. Previous goal turn was progress (fourteen invented contracts); this turn is progress (cross-comparison detects a previously untested fixture conflict and qualifies explicit common-field compatibility). Overall pre-camera goal remains active.

## Remaining prerequisites

Current candidate-to-operation binding, complete interpreter/bootstrap/helper closure and owned execution, independent expectation/review/owner authority, actual source/dependency freshness and activity-specific rights remain unresolved. Inspection rights remain **No / unknown**; no legal conclusion is introduced. Exact-body correspondence, native English, native Wi-Fi FTP, backup coverage and usable rollback/recovery remain unverified. A source comparison cannot close device gates.

Camera commands: **none**. No camera, protected input, saved raw stream, installed dependency/native payload, upstream execution, download/upload, driver or firmware change. English/native FTP first; FL2/FL3 and calibrated looks deferred; optional bridge remains host-assisted.

Next single package: **RA-003: implement and independently qualify a versioned invented candidate envelope that binds an explicit operation ID and current dependency/source/activity/bridge context anchors across candidate, review, decision and seal. Keep the legacy envelope comparison-only; do not infer authority from a matching digest. Exact bootstrap/source ownership, freshness, rights and actual runtime remain separate prerequisites. Authored texts/invented records only; runtime disabled, no protected inputs or camera.**
