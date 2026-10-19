# RA-003: required parent evidence and current v5 qualification

2026-10-19. Branch `codex/ra003-parent-evidence-v5`. Evidence: **offline-tested**, **static-inference**. Previous goal turn: progress; current turn: progress. Complete pre-camera work remains active and incomplete.

## Change and result

**BOOT-GR-001 is resolved in the reviewed successor source.** Candidate, decision, review, seal, activity and validated-document schemas advance to v5. Both pure gate and entry require the new `parent_evidence` input/reference. Closed validation requires the exact frozen historical seven-case evidence: all IDs, 81 source hashes, original entry identity, raw result/log hashes, reviews, counts and false authority flags. Re-sealing substituted evidence is insufficient. Old v4 candidates are refused.

The historical tested-entry identity remains historical. The successor entry has a new whole-file hash. After source/reference policy was finalized, the current runner qualified final source, with no result hash embedded inside the entry that produced it. The parent-loader repair and strict completion-verification functions have unchanged ASTs relative to the predecessor; source/schema/reference changes are separately captured.

**253/253 tests passed**, zero skipped, exit **0**, **120.937s** suite / **121.50171929999487s** wrapper:

- **232 gate/unit cases**: 207 retained identities, 24 new parent-evidence cases and one automatic fixed-reference case. Resealed negatives include missing/extra fields/sources/reviews, changed hashes, case substitution/duplication, count downgrade, boolean/float exit, historical identity relabelling, promoted authority and camera commands.
- **14 bootstrap cases** rerun on current source. Positive tests use an explicit invented in-memory reference policy. Actual main launches an unchanged child which refuses the invented bundle under fixed production references.
- **Seven parent/child composition cases** rerun on current source. The real authored controller/factory/26 roles compose with invented AES/native/readers and a custom child driver. Narrow parent success remains distinct from strict outer refusal of injection. Actual phase-two failure, missing receipt, malformed stdout, source mutation and accelerated direct-child deadline cases pass.

All **90 source/fixture pins** agree before/after, current files and preserved snapshots. All **86 predecessor inputs** remain unchanged in their original root. Seven copied predecessor paths changed, plus new successor test/runner/qualifier/baseline files. Two source-only reviewers found no new scoped blocker; exact reviewed pins match current files. They did not execute tests or independently reproduce camera behavior.

The gate requires the 232-case qualification, with **19 fixed source pins plus three candidate/bootstrap self-bindings**. A normalized current result records that subset and explicitly links the actual 253-case raw run and its additional 14+7 cases. Do not describe it as a separate 232-case execution. The historical seven IDs remain distinct from current runner IDs. A pure invented-bundle roundtrip accepts the emitted current result/review summaries with exact final bootstrap hashes. It is not validation of saved actual inputs or an operational activation.

## Commands and evidence

Windows AMD64; CPython **3.13.12** at `C:\ProgramData\miniconda3\python.exe`.

```powershell
git status --short
git branch --show-current
git switch -c codex/ra003-parent-evidence-v5
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-parent-evidence-v5/qualify_successor.py development-001
git diff --check
```

Starting tracked tree clean on `codex/ra003-bootstrap-lab`. Branch creation exit 0. The qualifier launches `python.exe -I -S -B -X utf8 successor_runner.py`, retains exact argv/version, raw stdout/stderr, snapshots and all synthetic per-test text/JSON/log records. One current qualification ran; no failed run or hidden retry. Its predeclared 600-second combined-suite deadline did not fire. It has in-memory uncapped stdout/stderr capture and does not prove whole-descendant termination after a supervisor timeout. The camera-controller deadline remains 300 seconds; its invented timeout test accelerates the clock 600x.

Host-authored standard-library scripts via `python.exe -I -S -B -X utf8 -` returned exit **0** for source-copy verification, current policy construction, AST/source delta checks, exact 253 unique-ID partition and all 90 current/snapshot pins, review-source pin comparison and the emitted-summary invented roundtrip. A pre-test AST check caught and corrected an accidental extra error-stage argument introduced during schema editing before qualification; no failing test result was suppressed. The current source policy fixes 232 unique unit IDs and 22 source names; all 19 fixed file hashes match.

Private normalized result SHA-256: `456d942cabdeb56de557ee17a1561a4cb754520236f2da29d868bd3de7eeeb8b`.
Private review summary SHA-256: `a2b08aeedbf4ee935bb23523d0f90e7f69755428d34f8372b01be3fd02cdb6b1`.
Full verified 253-case record SHA-256: `c4c0264ca92c91acf8e70ae9bd12a9cf164bf93a2756159b6d46ec368e2617dc`.
Original historical parent-evidence bytes/hash are unchanged. Source lock is unchanged; no new public acquisition.

## Limits, state and next package

Four retained fake HostBoundary cases explicitly replace the parent validation scope with an inert stand-in; their assertions remain, while real role-finder behavior is exercised by the separate seven composition cases. Successful composition still uses invented source/dependency authority and native injection. Fixed production references are tested for refusal only. No successful complete production bootstrap/native/actual-input execution is qualified. Cached helper modules and owned role finder aliases are distinct cleanup objects; the recorded role-cleanup result is not a whole-interpreter cleanup proof. Child/host receipt wire v4 remains unchanged and producer/consumer tests agree; this is distinct from activation document schema v5.

Private code/tests, evidence, receipts and backed-up internal continuity remain ignored. Changed tracked files: this report, README, BACKLOG, CODEX_HANDOFF, FEATURE_PROGRESS and STATE. No third-party code or private input is staged.

Native English and native camera-to-server Wi-Fi FTP remain first; FL2/FL3/custom looks remain deferred. Noninjected full dependency composition, actual saved source/basis chain review, exact-body correspondence, feature mappings and proven rollback remain unresolved. Host-assisted transfer remains a separate optional result. No feature support, device-write or recovery gate passed.

Camera commands: **none**. No real firmware/constants/saved-prefix/native payload read, installed audited dependency execution, upstream launcher, private upload, download, driver change or device write.

Next single work package: **RA-003: qualify noninjected dependency-only composition for the frozen v5 revision using public AES vectors and live startup/native receipts, excluding firmware/constants; independently review that scope before any actual metadata act.**
