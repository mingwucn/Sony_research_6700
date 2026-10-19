# Ordered local-Codex work packages

All packages start OPEN unless marked otherwise in a later reviewed commit. Their identifiers are stable; GitHub issue numbers are a separate tracking layer. Each package should produce a small reviewable commit or pull request, a test/evidence report and a next-action statement. A dependency is an evidence gate, not merely an earlier issue being closed.

Read MASTER_PLAN.md for requirements and milestones, ACCESS_AND_RECOVERY.md for risk tiers, and VALIDATION.md for test IDs. R0 means host-side artifact work without camera contact; ordinary source-repository retrieval is allowed but is not a camera/network experiment. Device approvals remain separate from repository permission.

## Shared foundation

### RA-001 — Reproduce the workspace and complete the owner intake

Dependencies: none. Risk: R0. Read AGENTS, this backlog and CODEX_HANDOFF; record host OS/CPU/Python and current Git state. Run the 15 synthetic inventory tests. Create private owner-intake and session-state files without overwriting existing evidence. Ask only for missing facts from OWNER_INTAKE; no firmware update or USB access is required.

Deliver: sanitized research/sessions/YYYYMMDD-RA-001.md, test command/results and an updated STATE with remaining unknowns. Accept when the tests pass on the actual local host or failures are precisely diagnosed, private files are ignored, and no camera contact occurred. Missing camera facts do not block useful environment work.

Status (2026-10-18): COMPLETED with a diagnosed host test error; see [session report](../research/sessions/20261018-RA-001.md). Windows AMD64 / CPython 3.13.12 ran 15 tests: 13 passed, one error and one symlink-creation skip, exit 1. A bounded synthetic diagnostic reproduced cross-API `st_ctime_ns` disagreement in 198/200 cycles, explaining the helper's unchanged-file rejection on this host; underlying OS/CPython cause remains unproven. Helper/tests were left unchanged, and Windows inventory reliability and symlink coverage remain unresolved. Private intake/state were created without overwriting evidence; owner answered unknown to remaining body/setup facts. No camera contact occurred. This closes RA-001's documented failure-diagnosis alternative, not all M0 work or any device-write gate. RA-002 followed in a separate session below.

### RA-002 — Pin and audit reference code and reuse rights

Depends on RA-001. Risk: R0. Check out R1/R2 at the locked commits, compare current paths against REFERENCE_ANALYSIS, and inspect entry points without running launchers. Audit R1 transport/native workers and dependency imports for hard-coded model/addresses, writes, temporary execution, remounts and cleanup. Pin a full PMCA revision only if it becomes a candidate dependency. Review each intended reused component's licence rather than assuming a root licence covers firmware-derived assets.

Deliver: reference-audit with code paths, side-effect categories, unresolved dependencies and reuse/licence decisions. Accept when a reviewer can distinguish reusable host logic from incompatible device helpers. Do not copy a complete third-party tool or modify its MODEL constant as a port.

Status (2026-10-18): COMPLETED within the documented static scope; see [reference audit](../research/REFERENCE_AUDIT.md) and [session report](../research/sessions/20261018-RA-002.md). R1/R2 clean locked checkouts and all 120 tracked source-tree file identities were verified. R1's actual vendored PMCA candidate was pinned to `a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0`; all 19 vendored files and copied MIT text match. Entry points, transport/native side effects, model/ABI constraints, dependencies and component rights are recorded. No upstream code was run or integrated; source-to-binary equivalence, target suitability and reuse-rights gaps remain unresolved. One local synthetic run had 12 passes, two metadata-check errors and one symlink skip (exit 1); existing helper/tests were unchanged. Camera commands: none. RA-003 is next, with installed firmware still required before target-specific acquisition.

### RA-003 — Build the official-package and local-artifact inventory

Depends on RA-001; firmware facts needed for target-specific retrieval. Risk: R0. Acquire the official package matching the installed version when available, retain original bytes, record provenance and hash, and audit an extractor before using it. Extend the starter with offline container/format identification only after adding synthetic tests. Record encryption, compression, signatures, partial updates and omitted per-body state honestly.

Deliver: private package/extraction manifests and sanitized component inventory. Accept when every extracted object has source lineage and deterministic sizes/hashes, or a precise unsupported-format diagnosis. Do not flash to make a convenient package match the body. Package availability is not a device-write route.

Continuation (2026-10-18): IN PROGRESS, target acquisition BLOCKED. [Artifact intake](ARTIFACT_INTAKE.md) records a same-read bounded header probe, lineage template and static review of the pinned PMCA DAT locator. The [official-source refresh](../research/OFFICIAL_SOURCE_REFRESH.md) resolved public catalogue access and observed the USA 2.00 listing. A later [owner report](../research/sessions/20261018-owner-ui-intake.md) supplies installed version 2.00, but does not verify regional applicability or exact binary identity. No exact-target package was supplied, selected or downloaded. Legitimate matching-input provenance/extraction remains unresolved. Synthetic recognition and matching version labels do not close RA-003.

Latest continuation: [official-package provenance/rights](../research/OFFICIAL_PACKAGE_INTAKE.md)
and [session commands/results](../research/sessions/20261018-RA-003-package.md)
record 2.00 metadata and a single zero-byte asset GET stopped on an unreviewed
redirect, without retry. Owner firmware inspection permission: **No / unknown**.
Firmware analysis is blocked; recovery remains unproved. Sony's separate
version-labelled OSS page has 34 package links. The owner approved two BusyBox
source downloads; both were acquired once and audited privately for component
licences, configs/specs and client source. Both supplied configs enable
FTPGET/FTPPUT, a static lead only. Next single package: **RA-003 rights-cleared
exact-2.00 binary intake and source/binary correspondence**, blocked on suitable
firmware inspection rights and legitimate applicable bytes. No target binary,
updater execution, native transfer or recovery proof exists.

Mainland continuation (2026-10-18): [official Sony China source/terms](../research/MAINLAND_FIRMWARE_SOURCE.md)
and [commands/results](../research/sessions/20261018-RA-003-mainland.md) identify
the legitimate mainland 2.00 offer and published asset reference. No firmware
URL request, agreement acceptance, inquiry, extraction or device contact.
Next single package: **RA-003 rights-basis resolution for mainland 2.00 offline
unpacking/static analysis**, using the prepared inquiry or another documented
applicable licence/statutory basis. Download agreement acceptance alone does not
establish that scope; no blanket prohibition on ordinary hashing is inferred.

China-scope continuation (2026-10-18): [facts, acquisition results and commands](../research/sessions/20261018-RA-003-cn-scope.md)
record the owner's China/personal/noncommercial scope and explicit limited
download consent. The initial request stopped on the recorded HTTP 302; any
separately approved destination result is recorded in STATE. No extraction or
execution. China Article 17 is a candidate basis; activity-specific analysis
rights and exact-body/build correspondence remain unestablished. Next single
package: **RA-003 activity-specific rights-basis resolution for proprietary
unpacking/static analysis**; English and native FTP retain priority.

Package/statutory continuation (2026-10-18): [commands/results](../research/sessions/20261018-RA-003-package-law.md).
Separate owner destination consent led to HTTP 200 and the declared 1,024,017,848
bytes, with matching transfer/stored SHA-256. Authored identification probe:
UFU signature candidate, container not validated; no extraction/execution.
Copyright Law Article 50(5) expressly recognizes reverse-engineering research
as a technical-measure exception with conditions. Next single package:
**RA-003 exact act/terms assessment and applicable-parser audit**. This is not
an English/FTP result, exact-body match, recovery proof or write-gate pass.

UFU continuation (2026-10-18): [act/parser audit](../research/UFU_CONTAINER_AUDIT.md)
and [commands/results](../research/sessions/20261018-RA-003-ufu-inventory.md).
An authored metadata-only reader reports five bounded chunk spans covering the
file under the reviewed framing, including one nonempty FDAT. No contents were
extracted/interpreted or output. Full local suite: 179 total, 176 passed, three
skipped, exit 0. The next single package is **RA-003 bounded FDAT format
identification and applicable-extractor audit before copying/decompression**.
Container semantics, later analysis scope and exact-body correspondence remain
unverified; no feature or device gate passed.

FDAT continuation (2026-10-18): [audit](../research/FDAT_EXTRACTOR_AUDIT.md)
and [commands/results](../research/sessions/20261018-RA-003-fdat-identification.md).
The 4,096-byte in-memory prefix returned unknown/unsupported_opaque, exit 0;
whole-file identity agrees. Source-only candidate pinned and audited; direct use
not accepted, no upstream execution. Suite: 198 total, 195 passed, three skipped,
exit 0. RA-003 stays partial; exact-body/build, actual decoding scope and component
formats remain unresolved. Next single package: **RA-003: establish an act-specific FDAT decoding basis and bounded decoder design before real decryption or component copying**.
No native feature or recovery/write gate passed.

Decoding-design continuation (2026-10-18): [plan](../research/FDAT_DECODING_PLAN.md)
and [commands/results](../research/sessions/20261018-RA-003-decoding-design.md). Narrow statutory research rationale
is documented for bounded private in-memory format study; accepted-contract
interaction remains unresolved. A pure decoded-header validator passed 30 final
focused cases; full suite 225 passed, 3 skipped, 228 total, exit 0. No real decoding,
component copy or dependency/key adoption occurred. Next single package:
**RA-003: audit and pin the minimal crypto dependency and public-constant provenance for a bounded private header-decoding trial**. RA-003 stays partial.

Crypto-provenance continuation (2026-10-18): [audit](../research/FDAT_CRYPTO_PROVENANCE.md) and
[commands/results](../research/sessions/20261018-RA-003-crypto-provenance.md). Pinned public constants and a private
AES wheel were verified; eight isolated primitive cases passed, exit 0. No real
firmware read/decoding. Underlying derivation and contract interaction remain
unresolved; one predeclared experimental hypothesis is not a support profile.
Next single package: **RA-003: implement, synthetically qualify and run one bounded private FDAT header trial for the predeclared CXD90057_k8 hypothesis**. RA-003 stays partial.

Header-trial continuation (2026-10-18): [bounded result](../research/FDAT_HEADER_TRIAL.md)
and [exact commands/results](../research/sessions/20261018-RA-003-header-trial.md). One predeclared real hypothesis passed envelope/header CRC
predicates, exit 0; corrected synthetic run 45/45 passed. Initial 36/37 fixture-expectation
failure preserved. Full-stream length, declared extent bounds, component formats
and body correspondence remain unverified. No component files, upstream execution,
camera contact or feature/write gate. Next single package: **RA-003: assess and document the necessary private full-stream format-study scope, implement and synthetically qualify bounded FDAT stream validation, then measure decoded length and SHA-256 through bounded memory without retaining decoded-stream or component files**.
RA-003 stays partial; this supersedes the preceding continuation's next step.

Stream-validation continuation (2026-10-18): [bounded-memory result](../research/FDAT_STREAM_VALIDATION.md)
and [commands/results](../research/sessions/20261018-RA-003-stream-validation.md). All 1,000,017 physical envelopes/terminal
positions checked; 1,020,017,152 logical bytes measured. Declared extents fit that
length without overlap. New qualification 45/45 passed, exit 0; real single
pipeline exit 0 in 28.836450s. No component files/formats, body correspondence,
English/FTP finding or recovery/write gate. Earlier continuations above are history.
RA-003 stays partial. Next single package: **RA-003: document the necessary private selected-component scope, then synthetically qualify and run bounded in-memory identification of the declared U-slot and firmware extent prefixes, retaining lineage metadata only**.

Component-prefix continuation (2026-10-18): [bounded result](../research/COMPONENT_PREFIX_AUDIT.md)
and [commands/results](../research/sessions/20261018-RA-003-component-prefix.md). U-slot SquashFS v4 and firmware
ustar header candidates; 4,096 bytes each, complete source/stream lineage
revalidated. New suite 93/93 passed; one real pipeline exit 0, 23.899888s.
No raw output, child files/directory, decompression, disassembly, body match
or feature/write gate. Earlier continuations above are history.
Next single package: **RA-003: document and qualify a bounded-memory, metadata-only tar-directory inventory of the candidate ustar firmware extent, then run it with full source/stream lineage checks and no child files**.

Tar-directory continuation (2026-10-19 local / 2026-10-18 UTC):
[bounded refusal](../research/TAR_DIRECTORY_AUDIT.md) and [commands/results](../research/sessions/20261018-RA-003-tar-directory.md).
One newly scoped tar-directory experiment stopped at the fixed **unsafe_path**
guard, **needs_review**, script exit **2**, host-tool exit **1**, **28.603684s**.
Combined synthetic qualification **133/133 passed**, zero skipped, exit **0**,
**0.749s**. Preliminary complete-parent hash passed; actual-pass final hashes,
fresh lineage acceptance and tar end/tail checks did not complete. No directory
accepted. Tentative header counter 114 is not a member inventory; post-discard
member count 0 does not mean an empty archive. Both observers cleared.
The offending member-name/link-target category is unknown. No retry, parser
fallback, threshold relaxation, child files, decompression/disassembly, camera
contact or feature/write gate. Prior measured observations remain unchanged.
Earlier continuations are historical. Next single package: **RA-003: qualify and run one bounded tar path/link diagnostic that records the first refusal category privately, completes source/stream lineage validation, and accepts no directory or child files**.

Path/link diagnostic continuation (2026-10-19 local / 2026-10-18 UTC):
[audit](../research/TAR_PATH_DIAGNOSTIC.md) and [commands/results](../research/sessions/20261018-RA-003-tar-path-diagnostic.md).
One bounded first-refusal diagnostic completed, script and host exit **0**, **28.299963s**.
Synthetic qualification **171/171 passed**, zero skipped, exit **0**, **0.916s**.
The first refused field is **link_target**, origin **header**,
predicate **empty_or_parent_component**. Combined categories retain their stated ambiguity.
Complete parent/logical-stream identities, header, declared spans and both prior
prefixes agree. Semantic tar parsing stopped permanently at the unchanged guard;
no directory accepted or tar-end/tail validation. One private bounded event,
no path text/raw bytes in it. No retry/fallback, child files, decompression,
disassembly, camera contact or feature/write gate. Earlier failed evidence is preserved.
Earlier continuations are historical. Next single package: **RA-003: review the observed path/link predicate, qualify an explicit metadata-only policy and run one bounded directory inventory with complete lineage and no child files**.

Opaque-link inventory continuation (2026-10-19 local / 2026-10-18 UTC):
[audit](../research/TAR_LINK_INVENTORY.md) and [commands/results](../research/sessions/20261018-RA-003-tar-link-inventory.md).
One bounded opaque-link directory inventory completed, script and host exit **0**, **29.409064s**.
Synthetic qualification **171/171 passed**, zero skipped, exit **0**, **1.060s**.
Private inventory: **137 members** (97 regular files, 39 directories,
0 hard links, 1 symbolic link); **80182** compact UTF-8 JSON bytes.
Complete source/stream/header/span/prefix lineage, tar framing, member padding,
two end blocks and zero remainder checked. Link targets are opaque private
metadata, never followed/resolved/materialized or claimed safe for extraction.
Member-path guards unchanged; the link-policy change was documented before
this trial. No child files, decompression/disassembly, camera or feature/write gate.
Member formats and English/FTP mapping remain unverified; earlier evidence preserved.
Earlier continuations are historical. Next single package: **RA-003: review the private directory to select minimal English/FTP-relevant members, then document, qualify and run bounded in-memory prefix identification with full lineage and no child files**.

Selected-member prefix continuation (2026-10-19 local / 2026-10-18 UTC):
[audit](../research/MEMBER_PREFIX_AUDIT.md) and [commands/results](../research/sessions/20261018-RA-003-member-prefix.md).
One selected-member prefix experiment completed, script and host exit **0**, **32.470943s**.
Synthetic qualification **202/202 passed**, zero skipped, exit **0**, **1.317s**.
**Five regular image-category candidates**, **4,096 bytes each / 20,480 bytes total**;
all five returned **unknown / unsupported_opaque** under the fixed classifier.
Complete fresh source/stream/header/span/original-prefix lineage and exact whole
directory equality passed before selected classification. No complete member
was covered by these prefixes; raw buffers discarded, no child files or links followed.
Classifier coverage is limited; this does not establish missing formats, English
resources or FTP code. No decompression/disassembly, camera or feature/write gate.
Earlier continuations are historical. Next single package: **RA-003: audit pinned image-format parser sources and reuse rights, then design and synthetically qualify bounded structural header predicates for the five opaque candidates before another actual read**.

Source-only image-header design (2026-10-19 local / 2026-10-18 UTC):
[audit](../research/IMAGE_HEADER_DESIGN.md) and [commands/results](../research/sessions/20261018-RA-003-image-header-design.md).
Four public parser blobs (**16,708 bytes**) verified at the existing immutable pin;
published MIT notice reviewed and preserved with private source copies.
Separate bounded AXFS/ext-family/legacy-FAT/LZPT header predicates qualified
with **251/251 synthetic passes** (49 new plus 202 retained),
zero skipped, exit **0**, **1.271s**. All 23 baseline files unchanged.
The new API remains standalone and unintegrated. **No actual firmware, member
prefix or operational-constants read**; prior five unknown observations unchanged.
No filesystem, English, native FTP, body-match, recovery or device-write gate.
Earlier continuations are historical. Next single package: **RA-003: implement and qualify an all-prefix reconciliation gate, then run one frozen expanded-header comparison on the same five members with full prior lineage**.

Refused expanded-prefix trial (2026-10-19 local / 2026-10-18 UTC):
[audit](../research/EXPANDED_PREFIX_AUDIT.md) and [commands/results](../research/sessions/20261018-RA-003-expanded-prefix.md).
One frozen same-five expanded-header trial stopped **needs_review**, script exit **2**, host exit **1**, **38.945781s**.
Qualification **278/278 passed**, zero skipped, exit **0**, **2.001s**; 27 new cases plus 251 retained, all 27 foundation files unchanged.
Failure code **expanded_prefix_acceptance_failed**; no accepted expanded candidates, fresh directory or persisted stream-validation result.
Static source/metadata review finds float timing fields in prior summaries rejected by the new freezer; this is a sufficient blocker, not a logged precise runtime stage.
Observer cleanup reported no failures. No retry, fallback, changed threshold, child files or raw-prefix output.
Earlier five unknown classifications and all prior evidence remain unchanged. No decompression/disassembly, upstream/firmware execution, camera or feature/write gate.
Earlier next-package recommendations are historical. Next single package: **RA-003: design and synthetically qualify exact prior-metadata preflight using preserved production summaries, resolving the timing-field schema mismatch before any new actual prefix read**.

Metadata-only production-summary preflight (2026-10-19):
[audit](../research/METADATA_PREFLIGHT.md) and [commands/results](../research/sessions/20261019-RA-003-metadata-preflight.md).
Metadata-only qualification **320/320 passed**, zero skipped, exit **0**, **7.649s**; **42 new + 278 retained** cases.
**30** retained source/test files and all **32** historical failed-trial source/runner pins remain unchanged.
Only the new session gate copy is revised; its preflight preserves every field and exact type, with a narrow allowance for finite nonnegative built-in timing floats at two root keys in two prior-summary roles.
Production metadata shapes, signed zero, bounded trees, fixed role/stage diagnostics, mutation isolation and cleanup flags are qualified offline.
No firmware/key/raw-prefix input, actual replay, new download, upstream execution, camera or feature/write gate.
The earlier expanded trial remains **needs_review**, script **2** / host **1**; its precise runtime refusal stage stays unrecorded.
Earlier five unknown classifications and all other actual results remain unchanged. A future pre-I/O runner is still to be frozen and reviewed.
Earlier next-package recommendations are historical. Next single package: **RA-003: freeze and review a runner with pre-I/O metadata preflight and bounded stage diagnostics, then run one separately scoped same-five expanded-header comparison with complete prior lineage**.

Preflight comparison (2026-10-19): [audit](../research/PREFLIGHT_COMPARISON.md) and [commands/results](../research/sessions/20261019-RA-003-preflight-comparison.md).
Qualification **346/346 passed**, zero skipped, exit **0**, **12.080s**; **26 new + 320 retained** cases; all **35** predecessor files and **32** historical failed-trial pins preserved.
Actual terminal **complete_private_preflight_expanded_member_comparison**, script **0** / host **0**, **37.595937s**; pipeline attempts **1**, expanded callback attempts **5**.
Source observation **source_read_confirmed**; protected callback attempts are separate and missing preliminary verification does not establish no I/O.
One separately frozen same-five comparison passed its complete lineage and original-outcome checks; limited expanded header leads were recorded after pre-I/O metadata preflight.
No retry, fallback, child/decoded/raw-prefix files, decompression/disassembly, upstream/firmware execution, camera or feature/write gate.
Earlier five unknown outcomes and prior refusal remain unchanged; no retroactive runtime-stage claim.
Sanitized header-lead counts: ext_family_header_candidate/header_only: 2; fat_legacy_header_candidate/malformed_header: 2; unknown/unsupported_opaque: 1.
Selected raw retention remains bounded separately from metadata copies. Six retained prior trees and seven gate snapshots may coexist, each with a 2MiB serialized-role limit, plus caller objects/overhead/other buffers. Historical20MiB pipeline allowance is not an aggregate managed/process memory cap.
Earlier recommendations are historical. Next single package: **RA-003: design and synthetically qualify a bounded ext-family superblock capability and geometry gate using pinned authoritative format sources; no actual replay or directory traversal**.

Ext-superblock source/synthetic design (2026-10-19): [audit](../research/EXT_SUPERBLOCK_DESIGN.md) and [commands/results](../research/sessions/20261019-RA-003-ext-superblock-design.md).
Independent ext-superblock design: **52/52 synthetic passes**, zero skipped, exit **0**, **0.029s**; **4** qualified authored source/test pins.
Eight immutable Linux v6.6 reference texts (**398,478 bytes**) and GPL-2.0-only notices are pinned; signed-release authentication is not established. The separate observer copies no upstream implementation.
Only invented buffers were tested. No actual firmware, member prefix, operational constants or actual replay; all prior actual results, forty-source seal and analysis acts remain unchanged. Historical suites were not rerun.
The initial harness refused (host **1**, child **0**): its regex counted zero although the preserved log shows **52 passes**, zero skips, **0.027s**. A reviewed parser-view CRLF correction preserved raw logs and observer/tests/thresholds; one corrected qualification supplied the accepted result above.
Conditional geometry and conservative feature handling are a synthetic design result, not observed member capabilities, a usable read plan, filesystem validity or English/native FTP support. Planning authorization remains false. No traversal, checksum verification, child/raw files, private upload, upstream/firmware execution, camera, feature/write or recovery gate.

Next single package: **RA-003: freeze and synthetically qualify a bounded two-lead ext-superblock metadata-observation runner with complete prior lineage checks; no actual replay or directory traversal in that runner-design package**.

Ext-superblock synthetic runner design (2026-10-19): [design](../research/EXT_SUPERBLOCK_RUNNER_DESIGN.md) and [commands/results](../research/sessions/20261019-RA-003-ext-runner-design.md).
Bounded ext-superblock runner design: **320/320 synthetic passes**, zero skipped, exit **0**, **17.064s**; **53** qualified source/test pins.
This qualification includes the unchanged **52** pure-observer cases and relevant standard-library lineage/gate regressions, plus new runner cases. Composition: **205** selected inherited regressions + **52** observer cases + **63** new cases. Two historical crypto-dependent cases are excluded, not skipped. This new 320-case suite differs from the historical 320-case preflight suite; historical suites were not rerun in full.
The frozen eight-role basis and complete prior four-key inventory must reconcile before either of two superblock callbacks. Their additional raw-retention allowance is **8,192 bytes**, alongside the inherited **65,536-byte** allowance; neither is an aggregate managed-memory or whole-process cap.
Raw buffers/logical streams were invented and callbacks synthetic; saved structured-metadata preflight was also qualified. No actual firmware, member prefix, operational constants or actual replay; all prior actual results, forty-source seal, four observer pins and analysis acts remain unchanged. The source lock is byte-identical; no new public-source acquisition.
The runner design prepares a later separately frozen metadata observation; it establishes no actual geometry, filesystem validity, usable read plan, English resources or native FTP backend. Planning authorization remains false. No traversal, checksum verification, component/raw files, private upload, upstream/firmware execution, camera, feature/write or recovery gate.

Next single package: **RA-003: separately freeze and review one actual two-lead ext-superblock metadata observation, then execute once with full fresh lineage and no traversal or raw output**.

Ext-superblock metadata observation (2026-10-19): [audit](../research/EXT_SUPERBLOCK_OBSERVATION.md) and [commands/results](../research/sessions/20261019-RA-003-ext-observation.md).
Qualification **359/359 passed**, zero skipped, exit **0**, **20.963s**; **320 retained + 39 new** cases. All **53** design-source pins and older seals remain unchanged.
Actual terminal **complete_private_ext_superblock_metadata_observation**, script **0** / host **0**, **38.274879s**. Preparation/pipeline/expanded/observer attempts: **1/1/5/2**.
Source observation **source_read_confirmed**; preparation attempts alone do not establish a read.
One separately frozen two-lead fixed-superblock metadata observation completed after full prior inventory and all-five outcome reconciliation.
Sanitized observation statuses: superblock_metadata_only: 2.
Geometry-issue counts: none under modeled predicates.
Capability blockers: none under modeled policy.
Classic feature-mask matches: **2**; this policy match establishes no planner or traversal eligibility.
All prior results and source lock remain unchanged. No filesystem/checksum/content/authentication, usable read plan, native English/FTP, exact-body, feature/write or recovery claim. No raw output, component files, traversal, decompression/disassembly, private upload, upstream/firmware execution or camera. Eight metadata roles and inherited 65,536 plus new 8,192 selected raw-byte allowances are not aggregate managed/process caps.

Next single package: **RA-003: design and synthetically qualify a bounded ext metadata read planner for the observed classic feature masks, adding counter, inode and table-placement eligibility checks; no actual replay or traversal**.

Ext metadata planner design (2026-10-19): [audit](../research/EXT_METADATA_PLANNER_DESIGN.md) and [commands/results](../research/sessions/20261019-RA-003-ext-planner-design.md).
Bounded ext metadata planner design: **174/174 synthetic passes**, zero skipped, exit **0**, **0.154s**; **52 retained + 122 new** cases; **8** qualified source/test pins. Invented buffers exercise primary-GDT and root-record proposals with counter, inode and group/reserved-metadata placement checks. All **13** retained ordinary source pins, prior actual results, analysis acts and source lock remain unchanged; no new source acquisition or historical full-suite rerun.

Limits: **1,024 groups**, **32,768 descriptor bytes**, **4,096 prefix bytes** (project budgets). No actual metadata/firmware application, traversal, raw output or camera; planning authorization and all filesystem/content, native English/FTP, recovery and device-write claims remain false.

Next single package: **RA-003: review and freeze the rights, lineage and byte limits for a bounded primary-GDT descriptor-metadata observation using the qualified planner; no inode/content traversal**.

Primary-GDT scope review (2026-10-19): [primary-GDT metadata scope](../research/GDT_METADATA_SCOPE.md), [commands/results](../research/sessions/20261019-RA-003-gdt-scope.md).
Primary-GDT observation engineering scope frozen: two planned inspection calls, four complete source passes (4,096,071,392 bytes on success), nine metadata roles, and at most 65,536 new descriptor bytes retained. Phase-A raw prefixes must be cleared before phase B; selected-raw allowances are 73,728 / 139,264 bytes, not process-memory caps. Root proposals are suppressed from every output and cannot reach a reader. Current official legal sources retain a narrow research rationale with unresolved contract/constants questions. No actual replay or planner application to saved actual data occurred.

Unchanged planner/observer baseline: **174/174 passed**, zero skipped, exit **0**, **0.163s**; all eight qualified source and 34 original pins unchanged. The new two-phase runner is not implemented or qualified.

Next single package: **RA-003: implement and synthetically qualify the frozen two-phase primary-GDT metadata runner and reconciliation gate; no actual replay or inode/content traversal**.

Primary-GDT runner qualification (2026-10-19): [primary-GDT runner design](../research/GDT_RUNNER_DESIGN.md), [commands/results](../research/sessions/20261019-RA-003-gdt-runner-design.md).
Two-phase primary-GDT runner, full-lineage gate and bounded collector qualified on invented data. Phase A reconciles all five historical blocks before planning; phase B repeats complete lineage before descriptor validation. Root proposals and broad planner success statuses are suppressed from outputs. Source telemetry is a synthetic protocol; the actual-I/O adapter and watchdog remain unimplemented. No actual firmware, constants or saved raw prefix was opened.

**547/547 synthetic cases passed**, zero skipped, exit **0**; **280.109s** suite / **280.948s** wrapper, CPython 3.13.12. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Next single package: **RA-003: implement and synthetically qualify a separately reviewed actual-I/O adapter and exclusive entry for the two-phase GDT scope, including source telemetry and watchdog; no actual execution**.

Primary-GDT I/O adapter qualification (2026-10-19): [primary-GDT I/O adapter design](../research/GDT_IO_ADAPTER_DESIGN.md), [commands/results](../research/sessions/20261019-RA-003-gdt-io-design.md).
Primary-GDT file adapter and exclusive parent/child control qualified on invented ordinary files and inert child processes. Real os.read calls, EOF probes, source accounting, journal failures and bounded supervision are exercised. Actual host/child bindings received source/AST review only; the actual entry remains inactive and blocked pending exact scope/rights activation-semantic review. No actual firmware, operational constants or saved raw prefix was opened.

**666/666 synthetic cases passed**, zero skipped, exit **0**; **800.360s** suite / **801.228s** wrapper, CPython 3.13.12. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Next single package: **RA-003: prepare and independently review the one-shot activation seal for the frozen two-phase primary-GDT observation; no execution**.

Activation preparation qualification (2026-10-19): [non-executable GDT activation preparation](../research/GDT_ACTIVATION_PREPARATION.md), [commands/results](../research/sessions/20261019-RA-003-gdt-activation-review.md).
Closed activation and binding validators qualified on invented records, wheels, file receipts and inert loader models. The 26-role dependency graph is bound to exact cached source bytes. New prospective host/child wiring received source/AST review only. The current preparation, review and seal all prohibit execution. The nine-role object is an opaque reference index; an operational basis remains unassembled. No actual firmware, operational constants, installed dependency or saved raw prefix was opened.

**811/811 synthetic cases passed**, zero skipped, exit **0**; **812.459s** suite / **813.447s** wrapper, CPython 3.13.12. **666 retained + 145 new** cases. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Historical next single package: **RA-003: acquire and independently assess the exact ordinary dependency provenance needed for the frozen GDT observation, then review its activity-specific execution decision; no GDT replay or camera contact**.

Latest RA-003: [GDT dependency integration and complete metadata basis](../research/GDT_RUNTIME_INTEGRATION.md), [commands/results](../research/sessions/20261019-RA-003-gdt-runtime-integration.md).
Dependency/controller composition qualified on **51/51 invented-data tests**, zero skips, exit **0** (**38 core + 13 composition**; **34.711s** suite / **35.305s** wrapper). The complete nine-role saved metadata basis assembled and passed the unchanged pure preflight. Full raw dependency receipts are durably retained before protected continuation, with the guarded dependency session alive through both modeled GDT phases. The new prospective factory received source/AST review only; its CLI remains disabled and the exact outer activation chain is absent. No GDT replay, firmware/constants/prefix read, installed dependency execution or camera contact occurred. English/native FTP, exact-body correspondence, recovery and device-write gates remain unverified.
Next single package: **RA-003: complete and independently review the exact outer activation/binding chain for the no-site GDT entry and assembled basis, including fresh ordinary source-cache receipts; no GDT replay until that review passes**.

Earlier RA-003: [dependency-only runtime provenance](../research/DEPENDENCY_RUNTIME_PROVENANCE.md), [commands/results](../research/sessions/20261019-RA-003-dependency-runtime.md).
One independently reviewed dependency-only child completed, exit **0**, **0.344s**. **34/34 probe tests** and **13/13 supervisor tests** passed with zero skips. All **24 public NIST comparisons** passed across twelve cases: ECB/CBC, 128/192/256-bit keys, default and generic requests, fresh encryption and decryption. Eleven exact cached Python origins and five native library load intents/audit events/completions were retained in a durable private raw receipt. This observes host dependency behavior; no firmware/GDT replay, English/FTP feature, recovery or device-write gate passed. English/native FTP remain first.
Historical next single package: **RA-003: integrate the observed dependency origins/startup and durable native receipts into a separately qualified GDT entry and review its exact operational basis; no GDT replay or camera contact**.

Earlier RA-003: [dependency descriptor provenance](../research/DEPENDENCY_DESCRIPTOR_PROVENANCE.md), [commands/results](../research/sessions/20261019-RA-003-dependency-provenance.md).
One independently reviewed descriptor-only dependency audit completed, exit **0**, **3.165s**, after **33/33 invented-file tests passed** (zero skipped, exit **0**, **14.513s** wrapper). The pinned wheel has **352 entries**; **351 installed payload files** match. It also records **4 installation extras** and **56 runtime/startup data files**, including **1 startup file**. The collector did not import the audited package or load its native backend. Native origins/load completion remain unobserved; GDT execution stays unauthorized. No firmware/constants/saved-prefix read, camera contact, feature, recovery or device-write gate. English/native FTP remain first.
Historical next single package: **RA-003: implement, independently review and qualify a dependency-only public-vector runtime provenance probe and the required source fixes for observed origins/startup and durable native receipts; no GDT replay or camera contact**.

### RA-004 — Establish identity and review an access route

Depends on RA-001/002. Risk: R0 proposal, then separately approved R1; R2 remains a distinct decision. Obtain normal UI facts and, after approval, ordinary host USB descriptors. Identify a candidate service path from reviewed exact-target evidence. Describe every command's effects, re-enumeration, helper ABI, expected result, timeout and reconciliation procedure. Write transport mocks for known readiness/error cases.

Deliver: device-facts and access-proposal, including what is not supported. Accept when identity is consistent and the owner can approve or decline a bounded next action. Standard USB recognition does not authorize service authentication. A blocked service path leaves RA-003 and offline analysis available.

Continuation: R0 [observation/access preparation](../research/TARGET_EVIDENCE_GAPS.md) written. Owner subsequently reported α6700, firmware 2.00, current menu language 简体中文, Chinese mainland version and English unavailable. This is source-report; the full offered-language list is not supplied. Exact regional SKU, independently verified binary identity and an applicable command-level route remain absent; RA-004 acceptance remains BLOCKED. Agent camera/USB commands and device approvals: none.

### RA-005 — Acquire and verify original-state coverage

Depends on an approved and technically reviewed RA-004 route. Risk: R2 if temporary execution is necessary; no R3/R4 feature write. Catalogue AP/CP/resource/settings/calibration/storage/load-state objects actually accessible. Collect independent reads where suitable and two verified copies; distinguish duplicate storage copies from independent acquisition. Classify changing settings before comparing snapshots.

Deliver: private backup catalogue, coverage gaps and original-state manifest; share only a sanitized summary. Accept when all objects needed for the proposed feature are covered and immutable hashes agree, or the hardware track is explicitly blocked. Do not describe a few program files as a full camera backup.

Continuation: coverage gaps and a blank backup-catalogue template prepared; no acquisition, copies or recovery coverage established. RA-005 remains BLOCKED on its approved route and actual evidence.

### RA-006 — Map architecture, storage, persistence and recovery

Depends on RA-003/005 as applicable. Risk: R0 analysis; additional observation requires its own approved tier. Establish AP/CP format, instruction state, address translation, load extents, storage objects, native settings save semantics and retained-state behaviour. Map each contemplated failure to recovery mechanisms that actually remain reachable.

Deliver: target architecture dossier and conditional recovery matrix. Accept when file offsets/VA/runtime addresses are unambiguous and each changed object has an understood inverse/recovery envelope. No guessed target values enter an executable profile. Do not test recovery by deliberately interrupting a live write.

Continuation: target architecture/recovery gaps recorded without populating any mapping. RA-006 remains BLOCKED on exact-target artifacts and access evidence.

### RA-007 — Implement offline candidate guards and transaction models

Depends on RA-002 and enough RA-006 evidence for any target-specific fields. Risk: R0. Build reusable exact-source validation, bounded/non-overlapping edits, preservation comparisons, inverse generation and journal-state simulation with synthetic fixtures first. Keep USB code out of the offline module. The UNVERIFIED profile must always fail eligibility.

Deliver: tested host modules, manifest/schema proposal and OFF-01..14 results as applicable. Accept when wrong/partial/mixed source states, replay and ambiguous results are rejected. A generic passing engine is not an alpha6700 patch and does not authorize a device executor.

Continuation: [synthetic candidate guards and transaction simulator](OFFLINE_GUARDS.md) have 36 focused passing tests. The separate [durable synthetic journal](DURABLE_SYNTHETIC_JOURNAL.md) adds append/fsync ordering, cooperative OS ownership and conservative crash/reopen reconciliation: the original owner-Windows focused run passed 23 with one POSIX skip. [Final-code qualification](../research/sessions/20261018-IN-102-final.md) now passed a NEW 63-file clean export (152 passes/two skips) and four actual Windows/Linux CI jobs (153 passes/one platform skip each), including POSIX inherited-lock and hosted real-symlink cases. Generic OFF-01..07/09/12/13 subcases are covered; target OFF-08/10/11, real-target review and any device executor remain absent. RA-007 is PARTIAL, synthetic-only and always device-ineligible.

## English track

### EN-101 — Resolve language/resources and the no-change option

Depends on RA-001 and RA-003/005 for binary analysis. Risk: R0; approved ordinary UI observation is R1. Verify whether English is already offered. If absent, map locale resources, selector construction, current/default values and all consumers of a candidate restriction field. Distinguish language-specific policy from global product/region identity.

Deliver: language feasibility record and critical-resource coverage table. Accept when a narrow hypothesis and falsifying evidence are identified, or normal menu selection resolves the request. Stop before mutation if English resources are incomplete or a shared region field is unexplained.

Latest [intake](../research/sessions/20261018-owner-mainland-english.md) (2026-10-18, source-report): owner reports Chinese mainland version, English unavailable, current 简体中文 and version 2.00. The full list and exact SKU/build remain unverified. EN-101 now investigates restricted-language/resource feasibility with lawful matching artifacts; do not repeat the full-list request merely to establish English absence. No resource absence, restriction mechanism, simple unlock or feature success is inferred. Official version-labelled bytes are acquired. RA-003 has documented the narrow decoding rationale, crypto provenance and bounded header trial. The later full-stream trial measures logical length/SHA and validates declared extent bounds/non-overlap against measured EOF. Component formats, exact-body/build correspondence and English resource/restriction evidence remain unresolved.

### EN-102 — Build a narrow candidate and inverse

Depends on EN-101, RA-005/006/007. Risk: R0 construction. Prefer a proved native-setting migration; otherwise prepare a minimal exact-source program/resource change. Define fresh read-modify-write semantics and preserve unrelated fields/attributes. Validate all critical English resources and invalid locale handling. Define uninstall migration when English would otherwise remain selected but unavailable.

Deliver: private candidate/inverse, preservation report and EN-specific write proposal. Accept only after the G4 checklist is complete. A candidate is not approval to run it.

### EN-103 — Validate English on the body and reverse deliberately

Depends on accepted EN-102 and explicit owner approval. Risk: R3 or R4 according to actual change. Apply one reviewed feature, verify complete readback, perform the proved reload only after I/O ends, and run ENT-01..06 plus shared regressions. Exercise a reviewed reversal when safe and approved.

Deliver: physical screen/persistence observations, protected-state comparison and inverse result. Accept only with no unexplained side effects. No whole-camera reset is used by default; reset/update behaviour remains untested until separately approved.

### EN-104 — Integrate English resource and uninstall dependencies

Depends on EN-103 and relevant look/FTP candidates. Risk: R0 integration followed by separately gated device validation. Check custom titles, native unimported-slot names, network dialogs and all resource-ID overlaps. Encode selected-language migration and preservation when removing another feature.

Deliver: composition constraints and ENT-07 results when hardware-tested. Accept when resource/uninstall dependencies are explicit rather than dependent on patch order.

## Creative Looks track

### CL-101 — Establish stock photographic and slot baselines

Depends on RA-001; ordinary physical captures require owner participation but no firmware change. Record native looks/recipes, disabled-mode rules, adjustment defaults and repeated ST/control-look photographs. Keep originals private. Define fixed exposure/WB/light and separate RAW data from rendered outputs.

Deliver: baseline protocol, repeatability measurements and recipe-preservation inventory. Accept when later pixel differences can be compared with real baseline variability. Do not derive a donor-equivalence claim from a menu label.

### CL-102 — Map the full target AP-to-CP chain

Depends on RA-003/005/006. Risk: R0. Investigate every layer in CREATIVE_LOOKS section 2, including selection permission, saved bindings, special/invalid enums, still/movie dispatch, metadata/reset and load state. Use R2 numbers only as reference-only anchors. Establish function matches with multiple independent xrefs/control-flow evidence.

Deliver: alpha6700 mapping dossier with explicit unknowns and confidence. Accept when each reachable new-look route is accounted for; menu-string discovery alone is insufficient.

### CL-103 — Specify and adapt donor look data

Depends on CL-102 and legitimate donor inputs. Risk: R0. Decode gamma, chroma and matrix records; identify illuminant/ISO variants and target-only fields. Prove available record capacity and absence of existing references. Retain target sensor/device calibration and every native look's referenced data.

Deliver: donor-to-target format specification, deterministic conversion tests and preservation checks. Accept when added records have provenance and correct bounds without wholesale donor functions or calibration.

### CL-104 — Generate the coherent FL23 candidate and inverse

Depends on CL-102/103 and RA-007. Risk: R0. Build independently reviewable menu, conversion, CP data, saved binding/default, metadata and preview change groups, then a coherent candidate that leaves no unsafe reachable intermediate route. Audit instructions, branches, ABI and loader placement. Run applicable OFF tests.

Deliver: exact-source candidate/inverse, control-flow review and G4 proposal. Accept when complete source/result identities and all protected-state expectations are machine-checkable. A menu-only partial state is not automatically suitable for a hardware trial.

### CL-105 — Validate stills, metadata, defaults and preservation

Depends on accepted CL-104 plus device approval and backups. Risk: R3/R4. Run new ST/FL/FL2/FL3 captures/playback, raw numeric metadata checks, scoped per-look resets and original-look/recipe/movie regressions. Verify complete storage/settings and qualified loaded-state evidence.

Deliver: CLT-01/02/05..11 results with unsupported combinations explicit. Accept when actual processing differs beyond repeatability and files remain valid; metadata alone cannot close the requirement. Record donor colour matching as unverified unless separately demonstrated.

### CL-106 — Qualify preview and load-state behaviour

Depends on CL-104/105, but preview-path analysis can begin earlier. Risk: R0 diagnosis then approved R4 changes only if required. Run the 100-switch no-shutter target and playback/sleep/mode transitions. If stale preview occurs, trace build/cache/submission/acknowledgement independently rather than changing working colour tables. Measure any repeated-upload overhead.

Deliver: CLT-03/04 evidence, exact preview fix/inverse when needed and startup/performance observations. Accept when physical preview follows the active look without an undocumented shutter refresh. Do not copy R1's preview hook or WBI action by address.

### CL-107 — Add calibrated selected-slot custom looks

Depends on a stable CL-105/106 baseline and domain/calibration inputs. Risk: R0 fitting first; later R3/R4 gated separately. Prove one diagnostic slot, establish Sony-ST/DCP/cube domain conversion and holdout validation, then implement selected-slot import with unselected recipes/names preserved. Expand to more slots only after target capacity and resource evidence.

Deliver: source-domain report, calibration/fit metrics, deterministic table candidate, selected-slot inverse and separate preview/photo/resource tests. Accept one slot before six. Do not claim full DCP fidelity, arbitrary LUT compatibility or branded-film equivalence without the required measurements.

## FTP track

### FT-101 — Survey native backend and dependency evidence

Depends on RA-003/005/006. Risk: R0. Trace candidate FTP strings/symbols into actual tasks, UI/configuration, media access, network lifecycle, credentials and status handling. Compare a donor only after ABI/import/storage/API analysis. Distinguish complete gated backend, partial backend and no currently found implementation.

Deliver: FTP feasibility dossier with positive and negative evidence. Accept when the selected next route A/B/C is justified; string absence alone cannot establish impossibility. Keep native status separate from bridge work.

### FT-102 — Implement host-side protocol and queue tests

Depends on FT-101 for native constraints; generic synthetic design can start after RA-001. Risk: R0 plus explicitly scoped local server/network testing, not camera access. Define FTP/FTPS protocol/security, path/duplicate/finalization semantics, capture identity, durable state and ambiguous-completion reconciliation. Test synthetic files against an isolated owner-controlled server; pin dependencies first.

Deliver: protocol specification, queue module, private server setup and FTT-03..08 host results. Accept when no source deletion, credential leak, silent plaintext fallback or uncontrolled retry exists. Distinguish a size check from end-to-end hash verification.

Continuation: the [durable mock queue](FTP_HOST_PROTOCOL.md) now also has a separately invoked [synthetic loopback FTPS lab](FTPS_LOOPBACK_LAB.md), with [pinned dependency/rights review](FTPS_LAB_DEPENDENCIES.md). Final host run: 19 cases passed, including 100 files/50 groups, complete read-back hashes, TLS/security refusals, no-clobber races and ambiguous-result reconciliation; all 21 lab servers stopped. Default standard-library suite: 129 passed, one real-symlink skip. See the [session report](../research/sessions/20261018-FT-102-loopback.md) for the initial failure and exact commands. FT-102 remains PARTIAL for native constraints, independent/deployment peers, physical faults, real files and target lifecycle. No native FTP or bridge result is established.

### FT-103 — Prove one native camera-to-server upload

Depends on FT-101/102, RA safety gates and exact-target candidate review. Risk: R2 for an approved transient proof, or R3/R4 for a reviewed native enablement. Prefer an existing complete client; otherwise use the smallest bounded one-shot implementation before any resident startup hook. Use one non-sensitive test file and a constrained destination.

Deliver: camera-resident origin evidence, complete server-side equality, cleanup/readback and limitation report. Accept only for native FTT-01. A PC-generated upload or a visible FTP menu does not pass this package.

### FT-104 — Integrate reliable native queue and automatic capture

Depends on FT-103. Risk: R0 design then gated R3/R4. Connect proved media-completion/capture events, RAW/JPEG grouping, durable retry and manual/automatic status. Define card removal, sleep/shutdown, cancellation and file-wrap behaviour. Verify physical-shutter events rather than assuming remote-trigger support transfers automatically.

Deliver: queue/lifecycle integration candidate and FTT-02..11 hardware results. Accept when failed/ambiguous transfers reconcile without data loss or destructive cleanup. Exactly-once claims require the actual server/client guarantees, not a bare FTP success response.

### FT-105 — Qualify native security and resource impact

Depends on FT-103/104. Risk: controlled approved operational testing. Compare shooting responsiveness, burst behaviour, startup, temperature and battery use to stock. Test authentication/certificate/path failures and normal Wi-Fi/PC Remote coexistence. Establish owner-approved overhead limits before release.

Deliver: security review, FTT-12 measurements and supported-mode matrix. Accept when native transfer remains bounded and original functions are preserved. Do not alter Wi-Fi regional restrictions or introduce a general remote shell/file server.

### FT-106 — Optional host-assisted bridge, independently labelled

Depends on RA-001 and verified model-specific PC Remote/SDK capabilities, not on successful native FTP. Risk: host/server testing and approved normal camera use; no firmware modification. Start with synthetic spool/queue/uploader tests, then verify the real camera-to-host API, formats, physical-shutter versus remote-trigger behaviour, card retention and completion signal.

Deliver: HOST-ASSISTED bridge and a separate test report. Accept only for its stated transport/API configuration. This package cannot close FT-01/native FTP and must not be marketed as an onboard unlock.

## Integration and release

### IN-101 — Compose independently accepted features

Depends on the relevant EN/CL/FT individual results, not necessarily every optional extension. Risk: R0 composition then new G4 hardware approval. Detect edit/resource/settings overlaps, generate reviewed combined source identities and inverses, and test stock/individual/pairwise/all intended combinations. Preserve fresh user settings during partial uninstall.

Deliver: composition registry, dependency-aware uninstall and validation matrix. Accept when patch order does not decide undocumented behaviour and modified sources cannot bypass exact eligibility.

### IN-102 — Reproducibility, host portability and publication checks

Depends on stable host modules; can evolve before hardware readiness. Risk: R0. Add CI only after choosing/pinning dependencies and limiting permissions. Test Linux/Windows host behaviour, symlink/error cases, deterministic builds and clean-host setup. Audit staged content for firmware, calibration, credentials, photos and inherited rights. CI uses synthetic fixtures, never private camera dumps.

Deliver: CI configuration and actual run evidence when executed, release-content policy and licence inventory. Accept when remote CI results are recorded rather than inferred from local tests. No licence for third-party firmware/assets is implied by project code licensing.

Continuation: Windows inventory false refusals repaired with same-API mutation checks retained. [Final-code qualification](../research/sessions/20261018-IN-102-final.md) passed a NEW 63-file export/no-pip environment at fb32370: 154 total, 152 passes, two owner-Windows skips, exit 0. Actual Windows/Linux CI on Python 3.10/3.13 passed all four jobs: 154 total, 153 passes, one platform skip each, exit 0. Ubuntu ran POSIX fork and actual symlink; hosted Windows ran actual symlink. The earlier 58-file reproduction and first harness failure remain historical. Full logs, publication review and [host policy](HOST_VALIDATION.md) are retained. IN-102 remains PARTIAL for broader release/rights requirements; local owner-host symlink, arbitrary filesystems, pristine OS and camera behavior are not qualified.

### IN-103 — Soak, inverse and release qualification

Depends on IN-101/102 and relevant hardware results. Risk: approved physical use and reviewed inverses only. Execute the expanded restart/preview/queue/load targets in VALIDATION, record failures, test supported uninstall paths and document the conditional recovery envelope. Seek independent eligible-body reproduction before broad compatibility claims.

Deliver: exact support matrix, known limitations, user procedure, repair-risk disclosure and release decision. Accept only within tested firmware/body/mode scope. Official firmware updates and new regional variants are new targets, not automatically supported transitions.

## Work sequencing and closure

Owner priority update (2026-10-18): **English and native Wi-Fi FTP first**.
FL2/FL3 is deferred; calibrated custom looks remain separately gated after it.
Keep existing work for later use. EN/FT feasibility does not depend on CL work.
The optional host-assisted bridge remains a separate result.

RA-001 and RA-002 completed their stated offline scopes. Generic RA-003/007, FT-102 and IN-102 host preparation, final-code clean reproduction and observed four-job CI are recorded in the [completion audit](../research/PRE_CAMERA_AUDIT.md). The official-source refresh is complete within its bounded scope. Next single substantive host package: **RA-003: complete and independently review the exact outer activation/binding chain for the no-site GDT entry and assembled basis, including fresh ordinary source-cache receipts; no GDT replay until that review passes**. Official package size/hash, five UFU spans, complete experimental FDAT length/SHA and measured-size declared extent checks are recorded. Component formats, full later analysis scope and exact-body/build correspondence remain unresolved. Earlier Unknown answers are historical; remaining setup facts stay unknown. The existing RA-004 ordinary Version/Language UI packet is ready when the owner separately approves camera contact; more generic tests, deferred CL work or a backup/write gate are not prerequisites to that bounded UI observation. EN-101 and FT-101 require their own target evidence; the latest owner report places this body on the English-absent branch without establishing a restriction mechanism. No camera feature or device gate passes from host results.

Owner requirement (2026-10-18): **verified rollback/recovery before any firmware
write**. RA-005/006/007 cover backups, exact inverse, target recovery reachability
and transaction controls; their host preparation does not satisfy the target
gate. The [recovery contract](ACCESS_AND_RECOVERY.md#8-write-gate-checklist)
records the evidence required. No rollback system has been established and no
restore/write test is authorized by this requirement.

Do not close a package because its document exists. Close it when its stated evidence is present, or explicitly resolve it as blocked/superseded with the reason and next action. Optional bridge/custom-look work must not hide missing primary requirements. Update STATE and the session report after every local work package.
