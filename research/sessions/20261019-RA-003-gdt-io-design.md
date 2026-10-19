# RA-003 primary-GDT invented-file I/O session

2026-10-19; branch `codex/ra003-gdt-io-design`; base `e30c4fa966215568b1f61f3b1a9e9be6d69d07e5`.
Evidence: **static-inference / offline-tested**. Camera commands: **none**.

**666/666 synthetic cases passed**, zero failures/errors/skips, exit **0**. CPython **3.13.12**; **800.360s** suite / **801.228s** wrapper. The ordered suite contains **547 retained + 119 new cases** and pins **80 source files**.

The authoritative invocation, from the repository root, was:

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-io-design/qualify-io.py
```

| Exact command (repository root) | Result |
| --- | --- |
| `git switch -c codex/ra003-gdt-io-design` | exit 0; clean topic branch from the base above |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-io-design/bootstrap.py` | exit 0; 121 tracked baseline files, four private snapshots, 329 ordinary originals, 67 source copies |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-io-design/copy-source-references.py` | exit 0; one ordinary pinned source-text copy; no import |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-io-design/freeze-before-code.py` | exit 0; implementation/test/fixture files and actual activation/output files absent at freeze |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-io-design/freeze-qualification-candidate.py` | exit 0; exact ordered case IDs and sources frozen |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-io-design/finalize-qualification-seal.py` | exit 0; independently reviewed candidate sealed |
| `& 'C:/ProgramData/miniconda3/python.exe' -I -B -X utf8 private/sessions/20261019-RA-003-gdt-io-design/qualify-io.py` | exit 0; 666/666 passed; zero skipped; child exit 0 |

Independent saved before-code review: `e165d3`, exit 0; exact argv/cwd was not retained.

The child command is the same interpreter and flags with this session's
`run-io-suite.py`. Exact case IDs, exclusions, source pins, interpreter, timing,
stdout/stderr hashes and zero failure/error/skip counts are preserved privately.
No development run substitutes for this sealed qualification. Publication, explicit
path staging, local commit and commit-pointer reconciliation have separate receipts;
no push is performed in this package.

Preserved development outcomes and corrections:

- Adapter smoke 001 exited 1 because its ad hoc harness omitted the inherited-source search path; corrected smoke 002 passed the full invented A/B chain. Adapter run 003 passed 37/38 with one fixture expectation error, corrected without changing an acceptance predicate. Run 004 passed 43/43; the final four focused checks passed after the exact-None close check. The final adapter module has 44 cases; no unobserved final-source 44-case development pass is claimed.
- Entry developer runs passed 28/28 and 29/29 on their preserved loaded revisions. Later focused runs passed 4/4 for journal-prefix reconciliation and 6/6 for reader ownership, terminal console and deadline behavior. The final developer entry module has 32 cases. An earlier loaded-source pass is not evidence for subsequent corrections.
- Independent run 001 passed 22/23: the progress fixture expected a milestone on the final read, which the frozen protocol replaces with the verified row. Increasing only invented padding to cross the milestone before EOF corrected the fixture. Focused runs 002 and 003 passed 2/2 each.
- Independent run 004 passed 10/15 and exposed a real context-copying bug: a named timing float lost its field context before callback construction. The fix preserved strict output rules. Focused run 005 passed all five affected cases plus the new detachment case, 6/6.
- Independent focused run 006 passed 3/3, including transactional journal replay: a rejected row cannot advance confirmed reads or counters beyond the previous valid prefix. Run 007 passed the blocked-log-write ownership regression, 1/1. The final independent module has 43 cases.
- Source review also corrected late-deadline acceptance, preparation-attempt reporting, hostile exception access, closed schemas and sticky staging failures. Unjoined writer handles are preserved as unresolved and are not flushed or closed by the parent. Future actual binding gaps remain explicitly blocked.
- Reporting review found missing snapshot-hash/count bindings and ambiguous historical README labels. Draft helpers were preserved, those checks were tightened, and the four controls passed a separate review. Ordinary display/search failures and one atomic patch-context miss caused no protected access or evidence overwrite.

- The independent implementation-review helper first refused twice while its ordinary hash-verification whitelist omitted .jsonl receipts (58e22b, exit 1), then COPYING/.c/.h/.rst source or licence text (7dcd5f, exit 1). The failed helper revisions and metadata were preserved; no approval receipt existed. After correcting only hash-verification eligibility, the final review passed (43422a, exit 0). The frozen implementation and test sources were unchanged.

Recorded development invocations, interpreter flags, source versions, timings, logs and negative results remain in the local adapter, entry and independent development summaries and exclusive receipts. The adapter stdin-runner payload remains in tool history rather than separate run-script files. Concurrent draft edits are identified in those receipts; they are not presented as held-source passes. No threshold was relaxed. The final sealed combined qualification below is the sole acceptance authority.

The new adapter owns one read-only unbuffered descriptor per phase, one capture pass, one rewind and one decode pass, each with a real final descriptor EOF probe. The pipeline receives a read(n)-only facade. Attempts, normal returns, exact known byte prefixes, unknown failed-read effects, rewind/close outcomes and verified passes are separate. Progress is journaled at bounded 16-MiB milestones. Named and descriptor stamps and whole-source hashes must reconcile within and across phases. Production requires the fresh Windows READONLY attribute and never changes it; matching observations do not establish an atomic filesystem snapshot. The new orchestration preserves the old checks while calling pinned capture/measure functions; it does not call the historical orchestration wrapper. Trusted callback boundaries are not a security sandbox.

Exclusive parent/child reservations preserve partial records and refuse collisions. An attempt record is durable before launch/preparation. Each source observation is staged, accepted by the core and written in one matching journal envelope. Parent acceptance requires agreement among process exit, sole stdout summary, terminal journal, exact result-byte digest, source transcripts, adapter snapshot, cleanup flags and before/after ordinary pins. Any own write, flush, fsync or close failure forces refusal without rewriting prior evidence. Known failures are sticky; partial journals provide only durable-prefix lower bounds. There is no retry, reopen, fallback, automatic reboot or rollback.

The prospective actual child deadline is fixed at **300 seconds**, with one kill attempt, one termination wait of at most **5 seconds**, and one reader join of at most **1 second each**. Live stdout/stderr retention is capped at **2 MiB each**, using 4096-byte raw-reader chunks; child result/journal caps are **8 MiB each**, 1024 journal rows, 16-KiB rows and 544 source rows. Timeout or uncertain direct-child/pipe ownership always needs review. This is not a process tree containment, cancellation, total-memory or actual-source performance proof. The final synthetic qualification uses its separately predeclared **1800-second** deadline; its logs are checked after capture, which is not a live memory bound.

The unchanged two-phase core still freezes nine metadata roles and reconciles all five historical inventory blocks in both phases. Phase A releases raw prefixes before B. Only two primary descriptor spans may be collected; stage 2 follows full B lineage and both complete lead outcomes. Root proposals and broad planner statuses remain suppressed. No bitmap, inode, filesystem-directory or content range is followed. Success permits one protected preparation, two pipeline invocations, two source opens and four complete source passes. Limits remain 4096 prefix bytes per lead, 1024 groups and 32768 descriptor bytes per lead, 65536 aggregate selected descriptor bytes. Selected-buffer allowances are 73728 / 139264 bytes, plus one descriptor conversion up to 32768 bytes; capture/header transients are separately 1040 / 512 bytes. These are neither whole-process nor aggregate managed-memory caps; releasing references is not secure erasure.

The public publication set is exactly eight reviewed files:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`
- `research/GDT_IO_ADAPTER_DESIGN.md`
- `research/sessions/20261019-RA-003-gdt-io-design.md`

Four local private notes are updated with their previous histories/bytes preserved:
`private/session-state.json`, `private/feature-progress.json`,
`private/feature-progress.md` and `private/owner-intake.md`. The public/private
feature records keep English and native FTP first. Source lock, prior results,
analysis acts and 115 unrelated tracked files remain unchanged. Private code,
fixtures, logs, hashes and receipts are neither staged nor uploaded.

No actual firmware, operational constants or saved raw prefix was opened. No planner was applied to actual fields. Actual host/child entry files were reviewed as source/AST only; neither was imported or executed, and no activation artifacts were created in the session. Selected pure definitions from pinned capture/stream text ran only with invented data and an invented identity cipher. No cryptographic runtime import, upstream launcher, camera/USB/driver/service operation, acquisition, agreement acceptance or upload occurred. There was no new actual analysis act.

Actual activation is additionally blocked by a fixed semantic-review barrier: the existing engineering scope and rights assessment explicitly grant no execution authority. Their hashes alone cannot supply the missing future scope/rights validation. The actual entry is not ready. A separate review must close those semantics and any resulting source changes before an activation seal can be accepted; no legal approval status is invented here.

Source review also leaves dormant preparation gaps: complete pre-import alias and transitive module-origin checks, mechanical binding of every authored role to the qualified source map, exact native cipher/loader origins, and wheel-record uniqueness plus verified-file/open identity. The fixed activation barrier prevents these prospective bindings from running. They require separate source changes, qualification and review before that barrier can be removed. Invented-file control qualification does not close them.

English menus and native camera-to-server Wi-Fi FTP remain the primary goals. FL2/FL3 are deferred, calibrated custom looks need a separate later gate, and a HOST-ASSISTED bridge remains optional. No language resource/policy mapping or native FTP backend was observed. Feature support, exact-body correspondence, filesystem/content validity, authentication, recovery/rollback and all device-write gates remain unproved. Download consent does not establish inspection or reuse rights. The prior narrow research rationale and contract/constants uncertainty remain unchanged; the future activation must refresh and bind its prerequisites.

The [design report](../GDT_IO_ADAPTER_DESIGN.md),
[handoff](../../docs/CODEX_HANDOFF.md), [backlog](../../docs/BACKLOG.md) and
[feature progress](../../docs/FEATURE_PROGRESS.md) carry this continuation.
Overall pre-camera goal remains active; this package made progress.

Next single package: **RA-003: prepare and independently review the one-shot activation seal for the frozen two-phase primary-GDT observation; no execution**.
