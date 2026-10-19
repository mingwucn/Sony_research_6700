# RA-003: complete saved binding plan and nine-role preflight

2026-10-19. Branch `codex/ra003-binding-diagnostic-repairs`; starting HEAD `d8af5c2`, tracked tree clean. Evidence: **offline-tested**, **static-inference**. The preceding external-reference refresh did not advance this pre-camera gate; this package makes concrete progress. The broader pre-camera goal remains active and incomplete.

One reviewed host-only diagnostic completed with **child 0 / supervisor 0**, **0.68248560000211s**, one launch and one main wait, no kill, cleanup wait or retry. The **complete binding plan was recomputed and matched**, and the **existing nine-role preflight/cross-bindings passed**. All **17 stages** passed. Saved stdout agrees with the result; stderr is empty; a separate durable host-completion receipt records the child exit.

The diagnostic made **53 ordinary reads / 2,397,309 bytes**: **17 fixed bootstrap + nine supplemental + 27 mapped documents**. Receipts record stable pathname and descriptor identities under the qualified reader policy, one EOF probe and one close each. Its 47 cached source buffers contain 814,219 bytes; the effective qualification map has 29 identities. The actual namespace snapshot contained 97 aliases and remained unchanged through checks; no conflicts were removed or replaced to pass.

Unlike the earlier component-only reconciliation, this run **executed eleven exact reviewed cached pure helpers** plus the composition and qualified gate/reader. All 26 role buffers were checked as source; the remaining role implementations were not executed. No dependency/native backend, firmware, operational constants or saved raw prefixes were opened or executed. Ordinary saved native-provenance metadata is distinct from the native payload itself.

## Review findings, repairs and qualification

The first source revision passed 54 invented tests, but runtime review found two blockers. Both original reviews, source snapshots and failed/superseded logs remain preserved.

| Finding | Repair and evidence |
|---|---|
| DIAG-RUNTIME-001: interruption lacks authored bounded cleanup/completion evidence | New supervisor owns `Popen`, redirects output to exclusive files, catches `BaseException`, attempts at most one kill and one five-second cleanup wait, and records known/unknown completion. Start journal prevents automatic retry. Tests cover real harmless success/nonzero/timeout and modeled interruptions, cleanup and journal failures. |
| DIAG-RUNTIME-002: downstream refusal can falsely report no cached-source execution | Execution trace changes at composition/helper boundaries; partial loading stays unknown and completed loading records eleven helpers before plan/preflight checks. Tests cover alias, basis, whole-plan and hash refusals. |

The supervisor now binds both diagnostic and supervisor hashes to the two source reviews. Its direct-child ownership is not a process-tree guarantee, disk quota, bounded OS-call guarantee or power-loss durability proof. A failed completion journal remains a review condition; it does not authorize repeating the act. The reference-count field was corrected from a stale constant to the actual 26 fixed/supplemental documents.

Final **76/76 invented-data tests passed**, zero skips, five exits **0**: **11 + 13 + 16 + 19 + 17**, with suite times **0.093 / 0.041 / 0.157 / 2.316 / 0.867s**. This is 54 retained cases plus 22 new cases, not a sum of repeated runs. Historical larger suites were not rerun. Fifteen final source/log pins match their snapshots; twelve original snapshot pins remain intact.

Two independent source-only saved-outcome reviews accepted the narrow result with no findings. Reviewers inspected saved outputs and authored sources without execution, input reopening or independent physical reproduction. Source-review hashes: gate `165247e6baada6adc48024ca7fca015dbfae2d515ccdf34a520a53ba0afcf73d`, runtime `974489c793dde8b86a43883d9864177cf10f4becd8751302efdce8cf8059bd04`. Outcome-review hashes: gate `7262251974f2b8cd5b8676d1f9566ae72769f7b131f030bafbf9b5e80e33bfb1`, runtime `e31119ebcaedf88d2fa79dbee2956c29829131af381db8f2e4787c45cceeb4cc`.

During development, one 19-case run had 18 passes/one error because a test expected `TypeError`; the inherited preflight correctly raised `GdtPreflightError`. The corrected test asserts that exact exception name, with unchanged implementation and acceptance predicates. An earlier 17-case supervisor run passed. Both source reviewers accepted the frozen final revision before execution; saved-outcome review is recorded below.

## Exact commands and results

Interpreter: `C:/ProgramData/miniconda3/python.exe`, **CPython 3.13.12**, Windows AMD64. All commands are host-side.

```powershell
git status --short
git branch --show-current
git switch -c codex/ra003-binding-diagnostic-repairs
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-binding-basis-diagnostic/test_reconciliation_boundary.py *> private/sessions/20261019-RA-003-binding-basis-diagnostic/test_reconciliation_boundary-final.log
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-binding-basis-diagnostic/test_completion_metadata.py *> private/sessions/20261019-RA-003-binding-basis-diagnostic/test_completion_metadata-final.log
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-binding-basis-diagnostic/test_v6_evidence.py *> private/sessions/20261019-RA-003-binding-basis-diagnostic/test_v6_evidence-final.log
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-binding-basis-diagnostic/test_diagnostic_bindings.py *> private/sessions/20261019-RA-003-binding-basis-diagnostic/test_diagnostic_bindings-final.log
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-binding-basis-diagnostic/test_supervisor.py *> private/sessions/20261019-RA-003-binding-basis-diagnostic/test_supervisor-final.log
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-binding-basis-diagnostic/freeze_final.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-binding-basis-diagnostic/verify_before_act.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-binding-basis-diagnostic/run_once_r2.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-binding-basis-diagnostic/verify_outcome.py
git diff --check
```

Final commands above exited **0**. The initial development commands used the same interpreter/flags with `test_diagnostic_bindings.py` redirected to `binding-tests-r2.log` (exit **1**, erroneous test expectation) and `test_supervisor.py` to `supervisor-tests-r2.log` (exit **0**). The diagnostic command itself ran **once only**.

The first saved-output verifier incorrectly required all four stat dictionaries to be identical (exit **1**). Twenty-nine receipts differ only in pathname-versus-descriptor `st_ctime_ns`; each channel stays stable. The existing, already-qualified Windows reader explicitly excludes ctime/attributes from cross-channel equality while requiring equality within each channel. Correcting the auxiliary verifier to that unchanged policy verified the same saved outputs (exit **0**); it did not repeat the diagnostic or change its thresholds. The original verifier is preserved privately.

## Pinned evidence and limits

| Artifact | SHA-256 |
|---|---|
| Diagnostic | `360e2fa4690cf4e7766ce5708c46ce014a01c910d0b308aa8a4c94b288f154bb` |
| R2 supervisor | `1ec59955e7d519cf45920e9637e00fde44af80cd98b3697bff54cc5ccfb617bf` |
| Final freeze | `d33ef44a2c228b3e7f4e71d59b76f8eedfe5eb3bf18949d75d919ad01022ceb7` |
| Result | `e7ddef7a3321f6d0e9ae85bf9dead888f7acebf0a996722563a628b1a5bbbec1` |
| Read ledger | `535757cf33e7a78422e9d9620b52077ec939c8ef6616af00cd22ba25cec3f4e0` |
| Host completion | `338c8e86bbd30a0ec8a0a74347bbbb171efa3048fe4ffe6566c318628cf6556d` |

The retained plan still reports `dependency_manifest_unobserved` and `native_policy_unobserved`. Earlier dependency-only observations are separate evidence; no policy, candidate or operational seal was changed to clear these blockers.

**Nine-role preflight is not complete saved-basis semantic revalidation.** Stream/member classifications, saved measurement semantics and EXT feature/geometry claims still need precise saved-only predicates or the separately scoped fresh observations they require. No saved-field facades may substitute for fresh parser/observer state. Full fixed-policy parent/child qualification, activity-specific rights/scope review, independent operational review and externally anchored candidate/review seal remain unresolved. The owner's historical firmware-inspection rights answer remains **No / unknown**; prior limited acts do not establish blanket permission.

English and native Wi-Fi FTP remain primary and unvalidated; FL2/FL3 is deferred. Exact-body binary identity, practical rollback/recovery and all device-write gates remain unproved. The optional host-assisted bridge stays separate. No feature-support or device-write gate passed.

Camera commands: **none**. No download/upload, upstream launcher, firmware/native execution, driver change, camera contact or device write occurred in this package.

Changed tracked files: this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `docs/CODEX_HANDOFF.md`, `research/STATE.json` and a four-occurrence interpreter-path rendering correction in the prior binding-basis design report. Its original bytes are preserved privately. Internal continuity notes were backed up before updating; private sources and evidence are not staged.

Next single work package: **RA-003: implement and qualify comprehensive saved-only semantic predicates for the nine-role basis, explicitly retaining claims requiring fresh observation as blockers; obtain independent source review before any new actual metadata or protected-input act.** This is preparation for the English/FTP feasibility work, not another camera operation.
