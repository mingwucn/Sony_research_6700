# RA-003 primary-GDT runner session

2026-10-19; topic branch `codex/ra003-gdt-runner-design`. Evidence: **static-inference / offline-tested**.
Camera commands: **none**.

**547/547 synthetic cases passed**, zero skipped, exit **0**. The suite took **280.109s** and the wrapper **280.948s**, using CPython **3.13.12**. The ordered suite contains **441 retained + 106 new cases**, and the sealed candidate pins **67 source files**.

Run from the repository root; the authoritative invocation was:

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-runner-design/qualify-gdt.py
```

Preparation and qualification commands used the same interpreter flags:

| Command (repository root) | Observed result |
| --- | --- |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-runner-design/bootstrap.py` | exit **0**; 119 tracked files, four private snapshots, 285 ordinary dependencies, 53 immutable copies |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-runner-design/copy-supplements.py` | exit **0**; two ordinary supplemental copies |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-runner-design/freeze-qualification-candidate.py` | exit **0**; 67 sealed sources, 547 ordered case IDs |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-runner-design/finalize-qualification-seal.py` | exit **0**; reviewed candidate sealed |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-runner-design/qualify-gdt.py` | exit **0**; 547/547 passed, zero skipped; 280.109s suite / 280.948s wrapper |

Later publication, staging and commit results are recorded separately after execution.

The isolated child command is the same interpreter with `-I -B -X utf8` and `private/sessions/20261019-RA-003-gdt-runner-design/run-suite.py`. The final central result records child exit 0, stable sealed sources, no timeout, zero failures/errors/skips/expected failures/unexpected successes, and the exact ordered case IDs. Three historical cases were excluded before execution: two crypto-dependent cases and one saved-actual-metadata case. They are not skipped tests. No development run substitutes for this final qualification.

The package implements detached nine-role preflight, an owned phase-A ticket, a bounded primary descriptor collector, full inherited A/B lineage gates, descriptor-only projection, sticky cleanup ownership, fixed event/counter schemas and an injected synthetic source-transcript protocol. It preserves 53 immutable copies, the inert historical qualification helper and 285 ordinary dependency pins. The complete five historical inventory blocks are compared rather than replaced by selected summaries. All raw A references are released before B; a second-lead refusal clears the pending aggregate result.

Preserved development outcomes include:

- Gate/preflight developer run 001 passed 32/32; run 002 passed the two added boundary cases. Their receipts retain exact commands, interpreter, source pins and logs.
- Runner developer run 001 passed 35/36. One test expectation about journaling failure and cleanup was corrected; production policy was unchanged.
- Independent run 001 passed 24/27, with three fixture/assertion errors. Independent run 002 passed 31/34, with one failure and two errors. These negative outcomes remain preserved. Fixture/assertion corrections did not change production policy. An edited test file is not evidence of an unobserved focused pass; the central qualification above supplies the final result.
- Earlier contract revisions and proposal bytes were preserved before the final reviewed freeze. Ordinary display/search failures are retained locally and did not access protected inputs.

The public publication set is exactly eight reviewed files:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`
- `research/GDT_RUNNER_DESIGN.md`
- `research/sessions/20261019-RA-003-gdt-runner-design.md`

The four private notes are updated locally with prior histories/bytes preserved:

- `private/session-state.json`
- `private/feature-progress.json`
- `private/feature-progress.md`
- `private/owner-intake.md`

Public staging uses explicit paths and reviewed byte hashes; prior evidence, source locks and unrelated tracked files are preserved. Private source, synthetic fixtures, command logs, source pins, seals and receipts remain local. No private inputs are uploaded or staged. Publication and commit-pointer controls receive separate reviews and reconcile the exact reviewed commit before advancing private pointers.

No actual firmware, operational constants or saved raw prefixes were opened. The planner was not applied to actual fields. No camera contact, upstream launcher execution, download, agreement acceptance or input upload occurred. Native English, native FTP, checksums/authenticity, recovery and all device-write gates remain unproved. The actual scope remained inactive; the legal refresh was not repeated and no new actual analysis act was added.

The actual-I/O adapter, exclusive actual entry, independently instrumented source transcript and an actual-source watchdog remain unimplemented. A future actual run needs its own reviewed scope and prerequisites. No resource/content mapping, language implementation or native FTP backend was observed. Rollback and recovery remain unproved; this package does not replace exact-body evidence, fresh current-state capture or independently verified backup copies on separate storage before any eventual write.

English and native FTP remain the priorities; support for either feature has not been established. Recovery remains unproved. The [design report](../GDT_RUNNER_DESIGN.md) explains the two-phase bounds. The [handoff](../../docs/CODEX_HANDOFF.md), [backlog](../../docs/BACKLOG.md) and [feature progress](../../docs/FEATURE_PROGRESS.md) carry the continuation.

Next single package: **RA-003: implement and synthetically qualify a separately reviewed actual-I/O adapter and exclusive entry for the two-phase GDT scope, including source telemetry and watchdog; no actual execution**.
