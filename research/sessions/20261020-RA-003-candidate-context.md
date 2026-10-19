# RA-003: invented candidate operation/context composition

2026-10-20. Final branch `codex/ra003-candidate-context-final`, baseline `2c9e5b6`. Source and test work began on `codex/ra003-candidate-context`; the intervening requested reference refresh preserved these two untracked files. Evidence: static-inference, offline-tested.

The new pure V2 candidate/review/decision/seal envelope binds one caller-supplied operation ID to the four original legacy documents, original scope bytes and source/dependency/activity/bridge sidecar bytes. All four V2 records and all four sidecars must carry the same operation ID. The dependency graph runs forward from candidate to review to decision to seal, with an external caller seal digest. Closed schemas, original-byte receipts, legacy/current phase equality and prepared-versus-operational-shaped decision outcomes are checked. Legacy V1 records remain unmodified comparison payloads.

This is operation consistency, not authentication. A caller who replaces and reanchors all operation claims can pass under a new expected operation; an explicit test preserves operation-origin and execution flags as false. The lower API allows opaque sidecar dictionaries carrying the operation ID and explicitly reports retained_sidecar_contracts_checked=false. It does not claim sidecar semantics, full legacy validation or runtime authority. The composed API checks V2 context before calling the retained fourteen-role validator and legacy/successor shared-metadata comparison; its checked-contract flag means those validators ran, not that their claims became independently true. The original invented wheel conflict still refuses bridge_wheel without a stub. A fully populated aligned shared plan still leaves legacy-context provenance and bridge verification false.

No actual activation packet is prepared. Runtime refuses real_activation_pending; direct CLI exits 2 before imports. Reviewer/owner/operation identity, full executing-source ownership, freshness, rights, startup, features and recovery remain unverified. Hash equality never supplies these missing authorities. The protected validator/capture/core source texts are hashed or AST inspected, never executed; detached binding plus ten ordinary preflight validators execute as authored host validators. No installed crypto/native dependency is activated.

Independent source-only reviewer accepted the final source, public tests and preserved qualification in this invented consistency scope, verified all 105 current pins and counted 203 individual successful log outcomes (42.698s suite). No material finding; reviewer performed no execution or protected-input reads. Remaining source/bootstrap ownership and caller-authority limits were explicitly retained.

## Qualification and exact results

Preserved completed run: **203/203 passed**, zero failures/errors/skips, exit **0**, **42.71936300001107s wrapper**. Composition: **181 retained + 18 public + four private integration tests**. All **105** source/test/fixture/scope/lock pins remain unchanged on current revalidation. Log SHA-256 `44e23c97827b03ce80eefa51efe3beb358b5e7319531bee1dcd645b7201f8736`. Installed Crypto/Cryptodome/cffi aliases empty. The process is terminal: result.json and completed unittest log exist and agree; it was not restarted. Historical three invented-file reader cases and full historical suites were not rerun.

Tests cover all eight original legacy/sidecar buffer drifts, scope drift, all four document operation mismatches after resealing, independently rebound wrong sidecar operations, both legacy phase mismatches and both decision-mode mismatches, exact rosters/closed fields, duplicate keys/size bounds, original DAG digests, external seal refusal before retained validation, opaque lower-API limits and caller-reanchored operation limits. Nonstub integration covers both phases, fourteen retained contracts, common-field completeness without provenance, preserved wheel conflict, input immutability and foreign sys.modules preservation.

Preliminary public run before the last two cases: 16/16, exit 0, 0.061s. No preliminary failure. Final qualifier reads the prior authored qualifier once and verifies fixed SHA-256 `42111307d9274c34fd97d80e92cb1a0c6a0995b492b147c70dc17bd57ed8bb63` before detached compilation of that captured buffer. It reads authored source texts and the pinned invented basis, not private firmware or constants. This qualification does not authenticate the ambient Python import/bootstrap chain.

Module SHA-256: `c37ef3e898877c2c47434246850748b686b29f04f5e548735474e4d0decc5439`.
Public tests: `6174e08874b7979ed71ea6a40e056aaec3198ae98a58bedcd5922b7d3013faa3`.
Qualifier: `0ff0be73e6ac97f7e5cd3c0a36864eabae5e34283b20f4a2c88bd15c6829feac`.
Result: `7389544d1d773548fae74bc63b0b39d489f8583385c3e19ba5bdf554aac39581`.

Host: Windows AMD64, CPython 3.13.12, `C:/ProgramData/miniconda3/python.exe`.

```powershell
git status --short --branch
git switch -c codex/ra003-candidate-context-final
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-candidate-context/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import subprocess,sys;r=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','tools/dependency_candidate_context.py'],capture_output=True,text=True);print('CLI child exit:',r.returncode);raise SystemExit(0 if r.returncode==2 and not r.stdout and not r.stderr else 1)"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-candidate-context/record.py
git diff --check
```

Qualification command above records the prior completed invocation; it was not repeated during reconciliation. Branch/status and checking wrappers exit 0; direct CLI child intentionally exits 2 with empty output. Standard-library stdin verifier recomputed all 105 pins, log and the four hashes above, exit 0. Recording preserves exclusive backups before updating private/public state. Explicit staging and staged content/path/whitespace inspection precede commit.

Changed public files: tools/dependency_candidate_context.py, tests/test_dependency_candidate_context.py, this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md, research/PRE_CAMERA_READINESS.md and research/STATE.json. Private session and feature notes updated after exclusive backups. No source lock changes.

## Objective audit and remaining work

This closes the current invented candidate-to-operation consistency subtask only. The pre-camera ledger is reconciled with current evidence rather than treating more synthetic tests as target discovery. The next necessary host step is exact executing-source/bootstrap ownership and complete helper closure. Independent authority/freshness and activity-specific rights remain separate blockers; owner inspection-rights answer remains **No / unknown**. No new legal conclusion.

Rights-cleared exact-build resource/restriction mapping for English, native FTP backend and direct Wi-Fi evidence, exact-body correspondence, storage backup coverage and practical rollback/recovery remain incomplete. No English resource or FTP backend was discovered by this package. The external project's unchanged FTP claim remains author-reported and its implementation unpublished. Native English/FTP first; FL2/FL3 deferred; calibrated looks separately later; optional bridge remains HOST-ASSISTED.

Previous goal turn was a completed requested reference refresh, with no new shared implementation evidence. This turn is progress: preserved qualification and source bytes reconciled, operation/context implementation finalized and objective ledger updated. Overall goal remains active; no completion or blocked claim.

Camera commands: **none**. No downloads/uploads, upstream launchers, firmware/constants/native payload or saved raw stream reads, installed dependency activation, driver/firmware change, camera contact or feature/recovery/device-write gate passed.

Next single package: **RA-003: derive and independently qualify the complete authored validator/helper import closure and exact bootstrap ownership requirements for the candidate-context path. Account for ordinary imports, detached retained sources, interpreter/stdlib trust and dynamic import/compile/exec seams; reject missing or ambiguous source ownership using authored text and invented fixtures only. Keep runtime disabled; no actual activation records, dependency activation, firmware/constants/native payload reads or camera.**
