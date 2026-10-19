# RA-003: v6 saved-metadata reconciliation

2026-10-19. Preparation and diagnostic on `codex/ra003-v6-saved-reconciliation`; publication on `codex/ra003-v6-reconciliation-record`, starting HEAD `b1b3fd1`, clean tracked tree. Evidence: **offline-tested**, **static-inference**. Previous goal turn: progress; this turn: progress. The broader pre-camera objective remains active and incomplete.

## Accepted result

The once-only saved ordinary-metadata diagnostic returned exit **0** with **16 component stages passed**. The historical source-namespace mismatch is resolved through the previously reviewed ancestry mapping. Source identities, earlier dependency-only completion, startup/profile records, runtime identity, limited basis identity/digests, prerequisite roles and binding orders reconcile. This is component reconciliation; complete binding-plan recomputation and complete saved-basis semantic validation remain pending.

Final qualification: **40/40 invented tests**, zero skips, each invocation exit **0**: 11 boundary cases in **0.067s**, 13 completion cases in **0.027s**, 16 new qualification/manifest cases in **0.147s**. These are three separate suite times, not a measured combined wall time. The historical 305-case qualification was consumed as pinned evidence and was not rerun.

The map retains 23 prior input rows unchanged, updates two qualification rows and adds ancestry map/evidence: **27 mapped documents**, **24 fixed raw references**, alongside the separately normalized dependency-profile authority. The diagnostic recorded **47 ordinary reads**: 11 fixed bootstrap/evidence/map, nine supplemental saved records and 27 mapped documents, totaling **2,357,805 bytes**, including repeated records. Receipts record approved hashes/lengths, stable file identities, one EOF probe and one close per opened file. They are software receipts, not an independent OS access trace.

The source cache contained **47 decoded source buffers totaling 814,219 bytes**, processed as data, with 29 effective qualified source identities. Nine basis roles and 26 role entries reconciled under the limited checks. Only pinned authored pure gate/reader helpers executed. Cached implementations, installed dependencies, native payloads, firmware, operational constants and saved actual prefixes were not executed or opened as protected inputs. Metadata paths were not followed to those inputs. Earlier dependency-only observation was compared as saved metadata, not repeated.

## Independent review and publication checks

Two owner-authorized local source-only reviewers accepted final source and the saved narrow outcome with no findings. They did not execute or independently reproduce the diagnostic. Both recorded that exit 0 and one launch are parent-reported and consistent with the source/result/journal; no separate OS wrapper completion receipt was retained. The original host tool observed terminal exit 0. No script-only elapsed time was instrumented. The diagnostic was not rerun to create missing evidence.

Publication checks rehashed all nine final source/test/map/log pairs against their snapshots and verified every local artifact hash in both outcome reviews. Saved stdout JSON equals the result. All authority flags remain false. Verification exit 0; private publication receipt retained.

| Artifact | SHA-256 |
|---|---|
| Diagnostic | `da7959993f253a682c1c68d9b3179d4b334b70154199d11d86915ced397694fa` |
| Reference map | `23eec6786a01a26d6b5872f206a8bcfce3b4428479e6d225623c4ddce15a7038` |
| Saved result | `69bdbe72b4055c8ce9c899ced5a54f5041f7b27493f2728a0f9e75f0d75620c7` |
| Read ledger | `de0b5354a8cf6c3296a740aa51636339d30607e063c20b7a125fb5db1cc800ba` |
| Gate outcome review | `3dd40bfea5967fe922e10a61d7fbb064c6d0809ee58966d5560c4cfeadf78cde` |
| Runtime outcome review | `5b3f26d749b7acd3b37cbc5605abdf70b10eca280054795c5c420fb3d73c2bc7` |

During preparation, a case-alias negative was strengthened to exercise collision detection specifically. Two stale descriptive map counters were corrected from 22/25 to 24/27 and the map hash refreshed; function ASTs were unchanged. Initial versions/logs were preserved. All 40 final tests were rerun after the corrections, before the single diagnostic. No acceptance threshold was relaxed. The earlier failed historical diagnostic remains unchanged.

## Exact commands and results

Interpreter: `C:ProgramDataminiconda3python.exe`, CPython **3.13.12**, Windows AMD64. The following historical commands completed during preparation; publication only rechecked their saved evidence.

```powershell
C:ProgramDataminiconda3python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-v6-saved-reconciliation/test_reconciliation_boundary.py *> private/sessions/20261019-RA-003-v6-saved-reconciliation/boundary-tests-final.log
C:ProgramDataminiconda3python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-v6-saved-reconciliation/test_completion_metadata.py *> private/sessions/20261019-RA-003-v6-saved-reconciliation/completion-tests-final.log
C:ProgramDataminiconda3python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-v6-saved-reconciliation/test_v6_evidence.py *> private/sessions/20261019-RA-003-v6-saved-reconciliation/v6-tests-r2-final.log
C:ProgramDataminiconda3python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-v6-saved-reconciliation/reconcile-v6.py *> private/sessions/20261019-RA-003-v6-saved-reconciliation/diagnostic.log
```

All four exit **0**. No automatic retry. Preparation and publication metadata/hash scripts used `C:ProgramDataminiconda3python.exe -I -S -B -X utf8 -`. Publication `git status --short --branch`, `git switch -c codex/ra003-v6-reconciliation-record`, JSON/link/hash checks and `git diff --check`: exit 0. No new operational diagnostic or historical test replay during publication.

Changed tracked files: this report, `research/STATE.json`, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `docs/CODEX_HANDOFF.md`. Private session and feature continuity updated after exclusive byte-preserving backups. Only reviewed documentation is staged; authored diagnostic and raw evidence remain private.

## Remaining prerequisites

Complete binding plan and basis semantics; activity-specific scope/rights decision; independent operational review; externally anchored candidate/review/seal; complete fixed-policy parent/child qualification; exact-body correspondence and proved recovery. No operational candidate or rights decision is produced here. Proprietary inspection rights remain No/unknown; earlier limited acts are not blanket authority.

English and native camera-to-server Wi-Fi FTP remain first and unvalidated. FL2/FL3 is deferred; calibrated custom looks later; optional HOST-ASSISTED bridge separate. No feature, recovery or device-write gate passed.

Camera commands: **none**. No camera/USB contact, driver or firmware change, upstream launcher/service execution, private upload, download or invented target offsets in this package.

Next single work package: **RA-003: prepare source-only complete binding-plan recomputation and complete saved-basis semantic validation against the frozen ordinary authority graph; qualify invented mismatch tests and obtain independent review before any new saved-metadata diagnostic.**
