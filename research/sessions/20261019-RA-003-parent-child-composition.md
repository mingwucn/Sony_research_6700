# RA-003: invented-input parent/child composition

2026-10-19. Branch `codex/ra003-parent-child-records`. Evidence: **offline-tested**, **static-inference**. Previous goal turn: progress (pinned public-reference refresh); this turn: progress (saved qualification reconciled and handoff updated). The complete pre-camera objective remains active and incomplete.

The actual authored gate, source loader, parent controller, real isolated subprocess, child controller, callback factory, 26 roles, adapter and runtime now compose on invented inputs. Seven real-process cases passed. Their complete narrow parent result is accepted by the parent controller, while strict outer acceptance correctly remains `needs_review`: dependency/native evidence explicitly identifies test injection. This is neither actual firmware observation nor operational approval.

## Defect and repair

The child initially completed both phases, but parent reconciliation failed because `gdt_preflight` had been unloaded by preparation. A new private source revision of `outer/entry_v2.py` retains a hash-checked finder for exactly the 23 ordinary roles during parent reconciliation; the three protected roles are excluded. The finder closes in a finally block before outer verification. The repaired factory and all other 75 baseline copies remain unchanged. Source-only runtime and I/O reviewers accepted this scoped repair, with limitations recorded privately. Reviewers did not execute tests or inspect protected inputs.

The final seven cases cover complete child/narrow-parent success with outer rejection, phase-two read failure without retry, missing outer receipt, malformed stdout, source mutation refused before launch, changed integration buffer refused before module execution, and a direct-child timeout using a 600x test clock. The timeout case records one launch/kill/wait and observed exit. It does not test 300 wall-clock seconds or arbitrary process-tree termination.

The harness uses a custom child driver and invented reference policy, stream, constants, trusted/native readers and AES responses. Production bootstrap/main is bypassed. Native audit-required remains false and injection-used true; no test manufactures operational provenance. Temporary environments use standard-library venv without pip/downloads. The parent ordinary-reader spy covers that adapter boundary, not every operating-system file open. Suite capture has no memory cap; the 2,400-second supervisor timeout establishes no descendant termination guarantee if it fires. It did not fire in the accepted run.

## Commands, results and retained failures

Interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12, Windows AMD64. Commands from repository root; all host-side. The first two commands are the recorded qualification invocations from the preceding development session, not new reruns in this reconciliation turn.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-parent-child-composition/qualify.py development-004
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-parent-child-composition/retained_runner.py
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-parent-child-composition/verify_saved.py
```

- Composition: **7/7 passes**, zero skips, exit **0**, **67.528s** suite / **67.90742780000437s** wrapper. All **81** source/fixture pins match before/after, current files and preserved snapshots. Synthetic per-test text/JSON/log records retained.
- Retained unit regressions: **207/207 passes**, zero skips, exit **0**, **5.309s** suite / **5.737711999972817s** wrapper. All **82** pins match. An explicit test-only scope stand-in adapts four pre-existing fake HostBoundaryTests to the new parent validation boundary. Their original assertions and case identities remain; this is adapted unit coverage, not 207 real-process or full operational cases. Production code was not weakened for these fixtures.
- New saved-result verifier: exit **0**, checks exact unique test IDs/counts, raw log outcomes, before/after/current/snapshot hashes, 76-copy baseline delta and current review-source identities. It executes no tested source and opens only authored sources, invented fixtures and qualification records. It does not revalidate real input lineage or grant execution authority.
- Initial direct development: seven cases, six errors, exit 1, 11.763s. Wrong fixture filenames/expectations; raw output exists only in session transcript, not a complete standalone failed-run archive. Source-pair snapshot retained; do not claim complete initial evidence closure.
- development-001: seven cases, five errors, exit 1, 9.205s. Remaining decision filename issue. Runtime records not yet archived.
- development-002: seven cases, three failures, exit 1, 18.176s. Fixture native-policy paths had not been rebased. JSON/text records retained, but `.log` omitted.
- development-003: seven cases, two failures, exit 1, 72.518s. Revealed the real parent module-lifetime defect. Its diagnostic reconstructed the known invented log and verified the saved size/hash because `.log` had not been archived. Final development-004 archives `.log` too.
- retained-regressions-001: 207 cases, one failure/one error, exit 1, 3.587s. Four minimal fake host fixtures lacked the new scope; the explicit unit adapter repairs the fixture boundary. Its outer wrapper printed child failure but did not propagate it; recorded child exit remains 1. Accepted second wrapper propagates exit correctly.

No acceptance threshold was lowered. Failed/superseded records remain private. Earlier source roots are preserved; only the new composition copy is repaired. Documentation validation: JSON parse, reviewed explicit diffs and `git diff --check`.

## State, prerequisites and next work

Changed tracked files: README, BACKLOG, CODEX_HANDOFF, FEATURE_PROGRESS, STATE and this report. Source/test fixtures, raw results, reviews, verifier and backed-up private continuity remain ignored. No third-party/protected material is staged. Previous source-only FTP refresh remains recorded separately.

Production bootstrap with fixed references, the complete successor source/qualification chain and noninjected dependency composition remain unqualified. The current repaired source has no operational activation authority. Exact-body correspondence, English-resource/backend mapping, native Wi-Fi FTP behavior and proven rollback remain unresolved. FL2/FL3 stays deferred; host-assisted bridge remains separate.

Camera commands: **none**. No actual firmware, operational constants, saved actual prefix, cached native payload or installed audited dependency execution; no private upload, new download, driver change, upstream launcher or device write. English/native FTP support, recovery and device-write gates remain false.

Next single package: **RA-003: qualify the production bootstrap on invented inputs and bind/review the repaired parent-loader revision in the complete successor source/qualification chain.** Noninjected dependency qualification and any actual metadata act remain later decisions; no camera contact.

Retained-suite review addendum: a separate source-only review accepted the explicit four-case fixture adapter, excluding real finder/isolation/cleanup coverage from those cases. Root-agent comparison of both preserved logs confirmed identical full 207-case ID sets. The review and comparison hashes are recorded privately and in STATE.
