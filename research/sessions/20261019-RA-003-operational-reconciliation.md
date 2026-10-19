# RA-003: saved operational packet reconciliation

2026-10-19. Branch `codex/ra003-reconciliation-repair`, starting HEAD `a445e64`, tracked tree clean. Evidence: **static-inference**, **offline-tested**. English and native Wi-Fi FTP remain first; no camera contact.

## Result

The source-reviewed saved-metadata diagnostic **refused**, exit **1**, after accepting historical parent evidence and the old/integration/snapshot/current qualification records. It stopped in the source-repair binding stage, before source-cache validation, dependency completion comparison or basis semantic checks. No operational packet was accepted.

All 22 fixed historical document references, current qualification pair and observed dependency config were located (25 ordinary input documents). Fixed bootstrap reads and nine supplementary saved metadata/review reads were bounded and recorded. This establishes read identities, not acceptance of the complete packet. No protected path in a manifest was followed.

The failure is a source namespace mismatch: the current gate computes source paths relative to the repaired session, retaining `activation/`, while the old seal stores paths relative to its activation subtree. All 29 role/bootstrap lookups consequently miss historical keys. A separate saved-metadata comparison finds all 29 original hashes match under an explicit ancestor-subtree mapping, including the old hashes for the three reviewed replacements. This is a **static mapping candidate**, not a changed gate or accepted migration. No address, offset, target byte or firmware was involved. The gate and historical evidence were left unchanged.

## Repairs and review

The original unexecuted diagnostic and reviews remain preserved privately. Two independent source reviewers identified unanchored helper execution, a late allowlist check and overly broad dependency completion linkage. A successor embeds the existing authored bounded reader, fixes six bootstrap and nine supplemental raw hashes, checks the entire pinned manifest before document reads, and reconciles saved result/journal/native receipts plus the exact eleven-source cache digest. Cached sources are never executed.

Both reviewers found the successor's review-key handling incompatible with the saved Windows separator convention. R2 was preserved and never run. R3 normalizes separator/case keys with collision refusal; evidence bytes remain unchanged. Both reviewers accepted R3 for this narrow diagnostic, with no operational authority. One R3 execution then produced the refusal above. No automatic retry or replay occurred.

Independent saved-output review confirms the refusal and all 40 read receipts closed once with stable identities. Its source comparison confirms the direct historical-key lookup explains the mismatch; the 29 proposed ancestry mappings are unique. Review SHA-256: `a7a0c672099d6cddd1ad04a7824c1cde98cbc2a088c5264b6bb2854f2858d4be`. This review establishes a precise blocker, not permission to bypass it.

New regressions: **24 passed, zero skipped**: eleven invented-file boundary cases (**0.084s**) and thirteen invented completion metadata cases (**0.025s**). Cases cover changed pins/lengths, pre-open bounds/hard links, interruption cleanup, bootstrap tampering before helper execution, extra/missing roles, failed callback/cleanup/audit, cache substitution, boolean/nonzero exits, altered result/review and normalized-key collisions. These prove the diagnostic's scoped guards, not complete production composition. Earlier retained 232-unit evidence remains private and was not rerun in this repair turn; historical 253-case and 81-case qualifications are unchanged.

## Exact commands and results

Interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython **3.13.12**, Windows AMD64. All following commands ran on the host.

```powershell
git status --short
git branch --show-current
git switch -c codex/ra003-reconciliation-repair
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-operational-reconciliation/prepare_revision.py
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-operational-reconciliation/test_reconciliation_boundary.py
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-operational-reconciliation/test_completion_metadata.py
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-operational-reconciliation/reconcile-r3.py
git diff --check
```

Git inspection/branch creation and source preparation: exit **0**. Test commands: exit **0**, counts/times above. Diagnostic: exit **1**, `needs_review`, `GateError`, stage `contract`; only the first two named stages passed. Test/diagnostic stdout and stderr were redirected to distinct private logs. Source R3 SHA-256: `1152e29a021f429479860600d39a3da1aff8bb25164c17657872af974e1bf35b`. Gate source SHA-256 remains `faa196abe6dbea4ef141deab810558f8f0e03fdda9bc0b9d9c4b6acda2f25172`.

Authored standard-library stdin scripts under the same interpreter/flags prepared the preserved R3 normalization and compared only saved source-row/seal/overlay metadata. Both exited **0**. The latter wrote `source-binding-diagnosis.json` and `ancestor-mapping-diagnosis.json` privately; no source/native/target paths in their rows were opened. Final JSON parsing and staged diff checks pass. Earlier ad hoc profile diagnostic's LF mismatch is retained as an initial diagnostic failure; it did not change any gate or evidence.

Changed tracked files: this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `docs/CODEX_HANDOFF.md`, `research/STATE.json`. Private continuity files were backed up byte-for-byte before updates. Source revisions, initial findings, tests, logs and read receipts remain ignored; no private source/cache/basis/native payload staged. Previous goal turn: **no progress toward the operational chain** (unchanged public-reference refresh); current goal turn: **progress** (reviewed repairs and precise actual refusal diagnosis).

Camera commands: **none**. No network request, dependency/native execution, firmware/constants/raw-prefix read, proprietary unpacking, upload, driver or firmware change in this package. Saved structured metadata was processed. Native-load evidence refers only to the earlier dependency-only observation; this diagnostic did not reach its comparison stage. English/native FTP, recovery, full operational acceptance and device-write gates remain false.

## Next single work package

**RA-003: implement and independently review an explicit historical source-namespace migration in a successor gate, qualify it against all 29 archived identities and negative collision/substitution cases, and bind the successor source/qualification chain before a fresh saved-metadata diagnostic.** Preserve the historical seal, cache and old gate. Complete binding-plan recomputation, saved-basis semantic validation, activity-specific scope/rights decision, external review/seal and fixed-policy parent/child composition remain prerequisites before any real metadata act. Goal remains active.
