# RA-003: independent host-side source review

2026-10-19. Branch `codex/ra003-gdt-independent-review`. Evidence: static-inference and offline-tested.

The owner explicitly authorized local source-only review subagents. Three separate reviewers returned findings on gate/bootstrap authority, runtime/factory ownership and I/O/scope reconciliation. Review acceptance is **false**. This supersedes the earlier pending-authorization blocker, not the unresolved technical prerequisites. No operational decision, candidate or execution seal was created.

All **38 frozen authored source hashes / 767,313 bytes** remain unchanged. Reviewers reported a union of **17 distinct source paths**; this is not a claim that every line of all 38 sources received independent review. The review round has returned; complete accepted operational review remains outstanding. Earlier source files, packet, draft and test logs were preserved.

## Findings and required repairs

| Finding | Evidence and consequence | Required repair/validation |
|---|---|---|
| GR-001 / duplicate RUNTIME-001, P1 | Parent `entry_v2.py:236-237` hashes dependency JSON without LF; runtime producer `runtime_entry.py:58-59,304` hashes JSON with LF. A legitimate successful child receipt is rejected after the protected work. Existing invented fixtures use the consumer encoding, hiding the mismatch. | Explicit producer-compatible canonical dependency encoding; cross-module invented producer receipt passes, wrong encoding and tampered hashes refuse. Preserve separate outer-document hash encoding. |
| IO-001, P1 | Actual entry stdout uses default spaced JSON/text printing; inherited `io_entry.reconcile:773` requires exact compact UTF-8 JSON bytes plus LF. A successful child fails parent reconciliation. | Emit the exact inherited console wire bytes through binary stdout with bounded write/flush; qualify actual CLI-output composition with inherited reconciliation on invented observations. |
| IO-002, scope blocker | Phase-B `gdt_gate.py:307` calls the planner with descriptors. The planner generates a root-inode proposal and the gate validates it before omitting it from output. The draft excludes proposals as well as reads. No root read was observed or executed here. | Suppress root-proposal generation in the descriptor-only path, retaining existing no-root-read scope; test internal calls/results as well as final projection. Do not silently broaden the draft. |
| RUNTIME-002, medium | Inherited controller catches Exception and closes records only after its normal/error tail; outer ownership skips closure once controller entry is marked. BaseException can bypass explicitly accounted closure. Outer outcome remains needs_review, but ownership/finalization evidence is incomplete. | One owner must account for all record handles on interruption; preserve sticky failure and unknown-close semantics, avoid blind retry. Invented KeyboardInterrupt/SystemExit and close-failure cases. |
| GR-002, P2 policy/coverage gap | Current gate accepts self-consistent outer qualification with >=20 cases and three bootstrap pins, weaker than the reviewed 124-case/full qualification-source evidence. The external seal remains required; this is not an external-anchor bypass. | Explicit non-circular qualification case/source policy; test resealed count/case/source-roster downgrade and legitimate updated qualification without circular hashing. |

Reviewer finding files are private, with path/line/trigger/effect/minimal-fix/validation and source-scope limitations. Findings are unresolved. The old 124-case suite cannot establish production compatibility because it misses these producer/consumer and interruption boundaries. Startup/source/native receipt ordering has useful static safeguards, but actual factory/native execution and OS mapped/transitive closure remain unqualified. Child watchdog is not a whole-host deadline; selected-byte allowances are not a whole-process memory cap.

## Exact commands and results

Interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12.

- `git status --short --branch`: clean starting tree on `codex/ra003-a6700-powerful-audit` (prior turn made substantive progress by pinning/auditing that external source).
- `git switch -c codex/ra003-gdt-independent-review`: exit 0.
- Host-authored Python via `python.exe -I -S -B -X utf8 -` checked every packet source against its declared size and SHA-256 before/after review: exit 0, **38/38 unchanged**. Private baseline/review hashes retained.
- Exact synthetic test command:

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 D:\LocalWork\Sony_research_6700\private\sessions\20261019-RA-003-gdt-bootstrap-qualification\test_outer_v2.py
```

Result: exit **0**, **124/124 passed**, zero skips, **2.868s** suite / **3.280s** wrapper. This reruns the unchanged invented-data suite, not actual saved inputs or production entry/factory. Raw stdout/stderr and hashes retained privately. Initial result-parser regex counted zero case lines due to CRLF; a separate parser-view reconciliation counted 124 unique passing IDs without changing raw logs or rerunning tests.

- Pure encoder reproduction: host-authored AST extraction selected only each standalone `encoded` function and executed it on one invented ASCII dictionary with stdlib json. Exit 0; hashes differ, independently confirming GR-001. No module import, actual entry/factory or native dependency was executed. Private `encoder-reproduction.json` preserves paths/lines/bytes/hashes.
- `git diff --check` and staged path/content inspection precede explicit staging; no private records or third-party source are published.

Camera commands: **none**. No firmware/constants/raw-prefix/cached third-party/native-payload reads, download/install/upload, upstream execution, device or driver action. Source-review authorization does not authorize the future metadata act. No filesystem/feature/body/recovery/device-write gate passes.

## Completion and next package

Changed public files: this report, README.md, docs/CODEX_HANDOFF.md, docs/BACKLOG.md, docs/FEATURE_PROGRESS.md and research/STATE.json. Private review records and additive session/feature continuity notes are ignored and unstaged.

English and native FTP remain first. Exact mainland build/body correspondence, English resources/restriction, onboard FTP invocation/network/media/lifecycle, fresh two-copy backups and proved rollback remain unresolved. FL2/FL3 stays deferred; custom looks and any host-assisted bridge remain separate.

RA-003: preserve frozen sources, repair the five review findings in a new revision, add cross-module invented-data regressions and requalify; then obtain source re-review before any activation.

The goal remains active. This is a review result requiring repairs, not successful activation or completion of all pre-camera preparation.
