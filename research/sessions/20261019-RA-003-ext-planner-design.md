# RA-003 session: bounded ext metadata planner design

2026-10-19 UTC / Europe/Paris. Topic branch `codex/ra003-ext-planner-design`,
parent `e0075d93711f15a72e3eb888f327d2dab0633049`. Host R0 only. Native English and native camera-to-server
Wi-Fi FTP remain first; FL2/FL3 deferred, calibrated custom still looks later
and separately gated; optional bridge **HOST-ASSISTED**. Camera commands: **none**.

## Outcome

Bounded ext metadata planner design: **174/174 synthetic passes**, zero skipped, exit **0**, **0.154s**; **52 retained + 122 new** cases; **8** qualified source/test pins. Invented buffers exercise primary-GDT and root-record proposals with counter, inode and group/reserved-metadata placement checks. All **13** retained ordinary source pins, prior actual results, analysis acts and source lock remain unchanged; no new source acquisition or historical full-suite rerun.

Limits: **1,024 groups**, **32,768 descriptor bytes**, **4,096 prefix bytes** (project budgets). No actual metadata/firmware application, traversal, raw output or camera; planning authorization and all filesystem/content, native English/FTP, recovery and device-write claims remain false.

This package independently authors and qualifies a pure planner on invented
prefixes and invented exact-length GDT buffers. It is not applied to saved
actual observations, member bytes or firmware. Before-code scope, source audit,
contract review, implementation review, qualification seal and raw synthetic
logs are retained privately. All earlier actual outcomes and analysis-act
records remain unchanged; no new firmware-inspection act is recorded.
No saved actual metadata is evaluated by this design.

## What the design establishes

The planner recomputes the unchanged fixed-superblock observer before applying
stricter eligibility policies. It checks the reviewed classic feature subset,
bounded counts, inode alignment/capacity, canonical primary placement, complete
per-group descriptor/table bounds and reserved superblock/GDT spans. It rejects
unmodeled features and produces no partial accepted proposal on a failure.
Source facts and stricter project refusal policies are distinguished in the
[design audit](../EXT_METADATA_PLANNER_DESIGN.md).

With no descriptor buffer it may propose the bounded primary classic GDT range;
with an exact capped synthetic descriptor buffer passing the modeled checks it
may also propose the root inode record. Proposed addresses are logical
member-relative file bytes. No target patch offset, virtual address or runtime
address is established. A proposal is not execution authority: planning
authorization remains **false**, as do all feature, content, filesystem,
checksum, authentication, exact-body, recovery and device-write claims.
No inode or directory contents are read or traversed. The design does not prove
allocation bits, metadata freshness, backup consistency or a working backend.

## Qualification and retained evidence

The new qualification passed **174/174** cases, zero skipped,
child exit **0**, **0.154s** unittest time and
**0.484898s** wrapper time. Composition: **52 retained** pure
observer cases plus **122 new** planner and independent-review cases.
There are **8 qualified source/test pins** and
**34 sealed original-file pins**. Exact ordered,
unique test IDs and closed zero-failure/zero-error/zero-skip summaries reconcile
with the frozen seal; captured logs are hashed and retained privately.

All **13 retained ordinary source pins**, including eight Linux v6.6 texts
(398,478 bytes), remain unchanged. Those sources and GPL-2.0-only notices remain
reference material; no upstream implementation is imported, executed or copied.
Signed-release authentication is not established. The source lock is byte-identical.
Historically broader suites and actual pipelines were not rerun; prior test and
observation counts remain historical evidence. Project resource caps do not
establish an aggregate managed-memory or whole-process memory cap.

## Host and exact commands/results

Shell: PowerShell 7.6.5. OS: Windows 11 build 26300, AMD64.
Interpreter: `C:/ProgramData/miniconda3/python.exe`; Python CPython 3.13.12 (Anaconda, MSC v.1942 AMD64).
The commands below reproduce the observed command ledger. They do not instruct
execution of any upstream launcher or actual firmware runner.

```powershell
git status --short --branch
```

Exit **0**; tool chunks: `056c83`. Clean on codex/ra003-ext-observation at the recorded parent before this package.

```powershell
git switch -c codex/ra003-ext-planner-design
```

Exit **0**; tool chunks: `54424f`. New topic branch; no push or history rewrite.

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261019-RA-003-ext-planner-design/bootstrap.py
```

Exit **0**; tool chunks: `b4bd29`. 115 tracked baseline files and 13 ordinary source/reference pins saved; unchanged observer/test copies.

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261019-RA-003-ext-planner-design/freeze-scope.py
```

Exit **0**; tool chunks: `391636`. Independently approved before-code scope/contract frozen with 31 ordinary source/lineage pins; no protected I/O.

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261019-RA-003-ext-planner-design/freeze-qualification.py
```

Exit **0**; tool chunks: `885f4e`. 174 exact ordered test identities and eight source/test/harness files frozen; 34 original/control pins.

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261019-RA-003-ext-planner-design/run-qualification.py
```

Exit **0**; tool chunks: `95fb24`. First authoritative invocation: 174/174 passed, zero skipped, child/host exit 0; 0.154s unittest and 0.48489790002349764s wrapper. Invented inputs only.

```powershell
& 'C:\ProgramData\miniconda3\python.exe' -I -B -X utf8 'D:\LocalWork\Sony_research_6700\private\sessions\20261019-RA-003-ext-planner-design\run-suite.py'
```

Exit **0**; tool chunks: `95fb24`. Exact inner isolated synthetic command executed once by the qualification wrapper; 52 retained + 73 developer + 49 independent cases.

Helper incidents and negative results:

- Developer fixture run e49c99 exited 1 (72 pass, one fixture failure, 0.064s): a near-uint32 invented block count caused the observer inode-total guard to reject before the intended planner cap. Corrected only that invented count (0xffffffff to 0xfffffff1); original test revision and both logs are preserved. Production code and frozen contract did not change. Final focused b1875c exited 0, 73/73, zero skipped, 0.069s.
- Independent focused suites ee5927 and 70b0b8 exited 0 (44/44 in 0.053s, then 49/49 in 0.095s after additional cases). The authoritative combined 174-case qualification succeeded on its first invocation; no historical full-suite or actual replay.
- An ordinary source-line display exceeded EOF (c02dfe, exit 1) and was corrected with a bounded display (c1f200, exit 0). A read requested a nonexistent review filename (929e12, exit 1) and the correct ordinary reference audit was then read (2fc4b3, exit 0). No protected input or operation began.
- Before publication-helper execution, source review corrected the expected contract-review status and prose-whitespace check, and aligned staging-diff receipt names and post-commit verification/pointer order. These were helper source fixes before their first use; no qualification, production policy or actual-input result changed.

The first independent publication-review command exited **1** (`48713f`) because
its byte-prefix comparison treated LF-to-CRLF conversion during the normal
Windows text write as a scope change. The decoded frozen scope text was equal.
The original review script and report are preserved privately. A comparator
correction retained the sealed original bytes and compared the public prefix
with universal-newline decoding; the corrected review exited **0** (`a51a75`).
That receipt binds the report before this incident note. A final metadata
verification and review will bind this amended report separately. No planner,
contract, test threshold, qualification or actual-input result changed; no
qualification test or actual pipeline was repeated.

The notes/report/verifier helpers are separate metadata publication operations;
their exact completion exits and commit verification are recorded privately
after the report is generated. No firmware trial, actual metadata application,
camera, USB, driver or service command was used in this package.

## Changed files and privacy

The intended reviewed public scope is exactly these eight paths:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`
- `research/EXT_METADATA_PLANNER_DESIGN.md`
- `research/sessions/20261019-RA-003-ext-planner-design.md`

Ignored local session evidence and four private progress/intake notes are also
updated; private histories are appended and existing owner facts are preserved.
Detailed source/review/seal receipts and synthetic logs remain private. No
firmware, raw member bytes, individual member identities, operational constants,
credentials, target offsets or photos enter Git. This report contains generic
format/policy limits and sanitized test results only.

## Unresolved prerequisites and next single package

Exact body/SKU/build correspondence remains unverified. English resources and
the regional restriction mechanism, native FTP binary/ABI/invocation and
media/network lifecycle are unproven. The accepted Sony contract interaction,
operational-constants provenance and any newly proposed real byte-reading act
need their own bounded assessment; this synthetic design grants no such rights.
Verified current backups, independent storage copies, conditional service access,
rollback/recovery and every device-write gate remain unresolved. No feature is
marked supported and no device step is approved.

Next single work package: **RA-003: review and freeze the rights, lineage and byte limits for a bounded primary-GDT descriptor-metadata observation using the qualified planner; no inode/content traversal**.
The complete pre-camera objective remains active; this package is progress,
with consecutive no-progress count **0**. RA-003 remains partial.
