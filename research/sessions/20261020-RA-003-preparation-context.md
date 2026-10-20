# RA-003: preparation context handoff

2026-10-20; branch `codex/ra003-preparation-context-qualified`, base `28a7136`.
Evidence: **offline-tested**, **static-inference**. Previous goal turn: **progress**,
recording a verified reference recheck in `28a7136`; no new feature implementation.
This turn completes the pending authored preparation integration and its invented
qualification. Overall pre-camera goal remains incomplete.

The implementation and limits are described in
[the handoff note](../PREPARATION_CONTEXT_HANDOFF.md). Three existing tools and
one new ten-case test module changed. The optional argument selects the real v6
gate, binds immutable context/proof receipts through pending saved metadata, and
preserves legacy behavior. A consistency-only result cannot build a host execution
context. No new framework, transport or camera adapter was added.

## Exact commands and results

Interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython **3.13.12**,
Windows AMD64; flags `-I -S -B -X utf8`.

```powershell
git status --short --branch
git switch -c codex/ra003-preparation-context-qualified
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-migration/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-migration/check_pending.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-migration/check_pending_r2.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-migration/record.py
```

Qualification exit **0**, **165/165**, zero failures/errors/skips, **76.255s**.
Composition: previous 137 cases + 10 preparation migration cases + 18 host-entry
cases. Fifteen selected source/test hashes stable. Complete invented preparation
uses real gate/metadata/refresh/materializer with invented bootstrap/I/O only;
file opens and native loading are denied during its main path. Three changed
tools invoked directly under isolated flags each refuse with exit **2**, empty
stdout/stderr. These are refusal checks, not operational execution.

Initial pending checker exit **1** at a source-byte assertion: Git's normalized
host-entry blob differs from its historical CRLF working-tree receipt. A bounded
diagnostic showed that converting LF to CRLF for this one archived text restores
the exact saved size/hash; the other two archived texts already match. Original
checker preserved. Reviewed `check_pending_r2.py` applies only that explicit
comparison-byte reconstruction and exits **0**. No record/hash guard was changed.
All 16 original artifacts and 51 source receipts reconcile; five decisions
remain pending, three dependency fields remain null, and the actual pending act
refuses `observation_undecided`. Three current source deltas are recorded. Archived
source buffers were inert; actual preparation and bootstrap were not performed.

Earlier focused fixture development retained these observed outcomes: eight-case
runs exited 1 at operation/prerequisite binding (8.520s), repair-pin keys (10.914s),
Windows path spelling (8.961s), and invented ordinary-I/O interface (9.113s).
All were fixture-wiring corrections, with no guard weakened. Corrected eight-case
run passed (9.176s); expanded ten-case run passed (11.860s). A separate host-entry
selection passed 18 cases (0.087s). The final 165-case run supersedes those narrow
runs for current-code qualification; tool-visible exploratory outputs were not
saved as separate raw files.

Independent authorized authored-source reviewer: no blocking findings;
**48 passed**, exit **0**, **26.485s**. Its first selection had one loader error
for a nonexistent metadata test module; 30 behavioral cases passed. The corrected
selection uses migration, preparation and host-entry modules. Review source pins
are checked against the final qualified files and preserved privately. Reviewer
read no selected private records, camera inputs or installed dependencies.

## Remaining prerequisites

The original 51-source operational and 46-role prepared rosters remain frozen.
Current source qualification does not migrate either manifest or qualify their
bootstrap code. Actual candidate/review/decision/seal and accepted current act
remain absent. All five activity decisions and three dependency fields are
unresolved. Freshness, source authority and the provenance of a supplied validated
dictionary are not established by saved consistency verification. Exact mainland
build, English resource/policy mapping, native FTP implementation and recovery
remain unproved. No feature marked supported and no write gate passed.

Changed public files: `tools/dependency_operational_metadata.py`,
`tools/dependency_operational_preparation.py`, `tools/dependency_host_entry.py`,
`tests/test_dependency_preparation_migration.py`, the handoff note, this report,
`research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`,
`research/PRE_CAMERA_GAP_AUDIT.md`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`,
`docs/FEATURE_PROGRESS.md`. Private before-images, qualification logs/pins,
pending-check result and reviewer receipt retained locally. Acceptance
requirements, validation cases, G0–G6 and R0–R5 definitions unchanged.

Camera commands: **none**. No firmware/constants/native payload read, installed
dependency activation, upstream execution, download/upload or driver change.

Next single package: **RA-003: produce the finite evidence/disposition packet for
the next necessary English/FTP analysis act**, using existing terms/provenance,
the five pending decisions and a concrete research hypothesis; assess whether
the proposed structural GDT observation advances it. Identify missing evidence
without creating approvals, clearing nulls or invoking protected processing.

Publication after reviewing only the named paths: `git diff --check`, explicit
`git add --` with those twelve paths, `git diff --cached --check`,
`git diff --cached --stat`, `git diff --cached`,
`git commit -m "Integrate consistency-only historical context into preparation"`,
`git status --short --branch`. Diff checks and recorder validation exit **0**.
