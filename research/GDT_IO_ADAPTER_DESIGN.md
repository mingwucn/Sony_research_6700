# Primary-GDT I/O adapter qualification

2026-10-19. RA-003; evidence: **static-inference / offline-tested**.
Camera commands: **none**.

**666/666 synthetic cases passed**, zero failures/errors/skips, exit **0**. CPython **3.13.12**; **800.360s** suite / **801.228s** wrapper. The ordered suite contains **547 retained + 119 new cases** and pins **80 source files**.

The file adapter and pure entry controls are qualified only on newly invented ordinary
files and inert child processes. Actual bindings have source/AST review only. The
predecessor core's limitations remain byte-for-byte, including its original synthetic
instrumentation limitation; the new adapter evidence is recorded separately.

The new adapter owns one read-only unbuffered descriptor per phase, one capture pass, one rewind and one decode pass, each with a real final descriptor EOF probe. The pipeline receives a read(n)-only facade. Attempts, normal returns, exact known byte prefixes, unknown failed-read effects, rewind/close outcomes and verified passes are separate. Progress is journaled at bounded 16-MiB milestones. Named and descriptor stamps and whole-source hashes must reconcile within and across phases. Production requires the fresh Windows READONLY attribute and never changes it; matching observations do not establish an atomic filesystem snapshot. The new orchestration preserves the old checks while calling pinned capture/measure functions; it does not call the historical orchestration wrapper. Trusted callback boundaries are not a security sandbox.

The unchanged two-phase core still freezes nine metadata roles and reconciles all five historical inventory blocks in both phases. Phase A releases raw prefixes before B. Only two primary descriptor spans may be collected; stage 2 follows full B lineage and both complete lead outcomes. Root proposals and broad planner statuses remain suppressed. No bitmap, inode, filesystem-directory or content range is followed. Success permits one protected preparation, two pipeline invocations, two source opens and four complete source passes. Limits remain 4096 prefix bytes per lead, 1024 groups and 32768 descriptor bytes per lead, 65536 aggregate selected descriptor bytes. Selected-buffer allowances are 73728 / 139264 bytes, plus one descriptor conversion up to 32768 bytes; capture/header transients are separately 1040 / 512 bytes. These are neither whole-process nor aggregate managed-memory caps; releasing references is not secure erasure.

Exclusive parent/child reservations preserve partial records and refuse collisions. An attempt record is durable before launch/preparation. Each source observation is staged, accepted by the core and written in one matching journal envelope. Parent acceptance requires agreement among process exit, sole stdout summary, terminal journal, exact result-byte digest, source transcripts, adapter snapshot, cleanup flags and before/after ordinary pins. Any own write, flush, fsync or close failure forces refusal without rewriting prior evidence. Known failures are sticky; partial journals provide only durable-prefix lower bounds. There is no retry, reopen, fallback, automatic reboot or rollback.

The prospective actual child deadline is fixed at **300 seconds**, with one kill attempt, one termination wait of at most **5 seconds**, and one reader join of at most **1 second each**. Live stdout/stderr retention is capped at **2 MiB each**, using 4096-byte raw-reader chunks; child result/journal caps are **8 MiB each**, 1024 journal rows, 16-KiB rows and 544 source rows. Timeout or uncertain direct-child/pipe ownership always needs review. This is not a process tree containment, cancellation, total-memory or actual-source performance proof. The final synthetic qualification uses its separately predeclared **1800-second** deadline; its logs are checked after capture, which is not a live memory bound.

No actual firmware, operational constants or saved raw prefix was opened. No planner was applied to actual fields. Actual host/child entry files were reviewed as source/AST only; neither was imported or executed, and no activation artifacts were created in the session. Selected pure definitions from pinned capture/stream text ran only with invented data and an invented identity cipher. No cryptographic runtime import, upstream launcher, camera/USB/driver/service operation, acquisition, agreement acceptance or upload occurred. There was no new actual analysis act.

Actual activation is additionally blocked by a fixed semantic-review barrier: the existing engineering scope and rights assessment explicitly grant no execution authority. Their hashes alone cannot supply the missing future scope/rights validation. The actual entry is not ready. A separate review must close those semantics and any resulting source changes before an activation seal can be accepted; no legal approval status is invented here.

Source review also leaves dormant preparation gaps: complete pre-import alias and transitive module-origin checks, mechanical binding of every authored role to the qualified source map, exact native cipher/loader origins, and wheel-record uniqueness plus verified-file/open identity. The fixed activation barrier prevents these prospective bindings from running. They require separate source changes, qualification and review before that barrier can be removed. Invented-file control qualification does not close them.

English menus and native camera-to-server Wi-Fi FTP remain the primary goals. FL2/FL3 are deferred, calibrated custom looks need a separate later gate, and a HOST-ASSISTED bridge remains optional. No language resource/policy mapping or native FTP backend was observed. Feature support, exact-body correspondence, filesystem/content validity, authentication, recovery/rollback and all device-write gates remain unproved. Download consent does not establish inspection or reuse rights. The prior narrow research rationale and contract/constants uncertainty remain unchanged; the future activation must refresh and bind its prerequisites.

All 329 ordinary predecessor originals, 67 inherited source copies and the one
ordinary source reference remain unchanged. Three historical cases were excluded
before execution: two require crypto and one reads saved actual metadata. They are
not reported as skipped. The sealed central qualification is the final pass authority.

See the [session report](sessions/20261019-RA-003-gdt-io-design.md),
[two-phase scope](GDT_METADATA_SCOPE.md) and
[preceding pure runner](GDT_RUNNER_DESIGN.md).

Next single package: **RA-003: prepare and independently review the one-shot activation seal for the frozen two-phase primary-GDT observation; no execution**.
