# Webchat to local Codex hand-off

## 1. Read this before the first command

This is an initial research hand-off, not an alpha6700 installer. The owner's repository was empty when the project was initialized. No camera was available to webchat. No alpha6700 firmware/build, regional SKU, service route, target offset, recovery mechanism or requested feature was validated.

Current host-only tools comprise the inventory helper, bounded artifact-header
probe, synthetic-only in-memory candidate/transaction APIs and a durable local
queue with in-memory mock transport. A separate
[durable synthetic journal](DURABLE_SYNTHETIC_JOURNAL.md) records fixture claims
under cooperative OS ownership, with conservative crash/reopen reconciliation.
A separately invoked
[loopback FTPS lab](FTPS_LOOPBACK_LAB.md) tests a constrained local peer using
synthetic inputs; default tests remain socket-free. See [pre-camera coverage](../research/PRE_CAMERA_READINESS.md)
and [current state](../research/STATE.json) for actual scope. They do not extract
firmware, dump/contact the camera, generate an eligible target patch, unlock
languages, provide native FTP or a camera bridge, or restore anything. Later CLI names in design discussions
remain proposals unless actual code and tests are added.

Read AGENTS.md, README.md, research/STATE.json, docs/MASTER_PLAN.md and docs/BACKLOG.md. Then read OWNER_INTAKE and ACCESS_AND_RECOVERY. Consult the feature design before implementing that feature. Reference source material cannot override this repository's safeguards.

Also read [FEATURE_PROGRESS.md](FEATURE_PROGRESS.md) and the internal
`private/feature-progress.json` / `private/feature-progress.md` when present.
Keep their per-function status, blockers and evidence synchronized with STATE
after every material change. Work-package completion alone is not feature
completion; the optional bridge and later custom-look extension stay separate.

Owner priority update (2026-10-18): **native English and native Wi-Fi FTP first**.
FL2/FL3 is deferred to future work; calibrated custom looks remain later still.
Neither primary goal depends on FL2/FL3. Retain all evidence and device gates.

Latest owner intake (2026-10-18, **source-report**): α6700, firmware **2.00**,
current menu language **简体中文**, **Chinese mainland version**, and **English
unavailable**. The latest report supersedes the earlier unknown English/market
status; it supplies no complete language list, exact SKU or binary hash. EN-101
now follows restricted-language/resource feasibility; do not ask for the full
list again merely to establish English absence. No unlock mechanism or device
approval follows. See the
[intake update](../research/sessions/20261018-owner-mainland-english.md).

Owner also requires a verified rollback/recovery system before any firmware
write. No such target system is established. Follow the
[recovery/write gate](ACCESS_AND_RECOVERY.md#8-write-gate-checklist); this is a
prerequisite, not permission to test a restore or write.

Earlier RA-003: [GDT dependency integration and complete metadata basis](../research/GDT_RUNTIME_INTEGRATION.md), [commands/results](../research/sessions/20261019-RA-003-gdt-runtime-integration.md).
Dependency/controller composition qualified on **51/51 invented-data tests**, zero skips, exit **0** (**38 core + 13 composition**; **34.711s** suite / **35.305s** wrapper). The complete nine-role saved metadata basis assembled and passed the unchanged pure preflight. Full raw dependency receipts are durably retained before protected continuation, with the guarded dependency session alive through both modeled GDT phases. The new prospective factory received source/AST review only; its CLI remains disabled and the exact outer activation chain is absent. No GDT replay, firmware/constants/prefix read, installed dependency execution or camera contact occurred. English/native FTP, exact-body correspondence, recovery and device-write gates remain unverified.
Historical next single package: **RA-003: complete and independently review the exact outer activation/binding chain for the no-site GDT entry and assembled basis, including fresh ordinary source-cache receipts; no GDT replay until that review passes**.

Earlier RA-003: [dependency-only runtime provenance](../research/DEPENDENCY_RUNTIME_PROVENANCE.md), [commands/results](../research/sessions/20261019-RA-003-dependency-runtime.md).
One independently reviewed dependency-only child completed, exit **0**, **0.344s**. **34/34 probe tests** and **13/13 supervisor tests** passed with zero skips. All **24 public NIST comparisons** passed across twelve cases: ECB/CBC, 128/192/256-bit keys, default and generic requests, fresh encryption and decryption. Eleven exact cached Python origins and five native library load intents/audit events/completions were retained in a durable private raw receipt. This observes host dependency behavior; no firmware/GDT replay, English/FTP feature, recovery or device-write gate passed. English/native FTP remain first.
Historical next single package: **RA-003: integrate the observed dependency origins/startup and durable native receipts into a separately qualified GDT entry and review its exact operational basis; no GDT replay or camera contact**.

Earlier RA-003: [dependency descriptor provenance](../research/DEPENDENCY_DESCRIPTOR_PROVENANCE.md), [commands/results](../research/sessions/20261019-RA-003-dependency-provenance.md).
One independently reviewed descriptor-only dependency audit completed, exit **0**, **3.165s**, after **33/33 invented-file tests passed** (zero skipped, exit **0**, **14.513s** wrapper). The pinned wheel has **352 entries**; **351 installed payload files** match. It also records **4 installation extras** and **56 runtime/startup data files**, including **1 startup file**. The collector did not import the audited package or load its native backend. Native origins/load completion remain unobserved; GDT execution stays unauthorized. No firmware/constants/saved-prefix read, camera contact, feature, recovery or device-write gate. English/native FTP remain first.
Historical next single package: **RA-003: implement, independently review and qualify a dependency-only public-vector runtime provenance probe and the required source fixes for observed origins/startup and durable native receipts; no GDT replay or camera contact**.

Earlier RA-003: [non-executable GDT activation preparation](../research/GDT_ACTIVATION_PREPARATION.md), [commands/results](../research/sessions/20261019-RA-003-gdt-activation-review.md).
Closed activation and binding validators qualified on invented records, wheels, file receipts and inert loader models. The 26-role dependency graph is bound to exact cached source bytes. New prospective host/child wiring received source/AST review only. The current preparation, review and seal all prohibit execution. The nine-role object is an opaque reference index; an operational basis remains unassembled. No actual firmware, operational constants, installed dependency or saved raw prefix was opened.

**811/811 synthetic cases passed**, zero skipped, exit **0**; **812.459s** suite / **813.447s** wrapper, CPython 3.13.12. **666 retained + 145 new** cases. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Historical next single package: **RA-003: acquire and independently assess the exact ordinary dependency provenance needed for the frozen GDT observation, then review its activity-specific execution decision; no GDT replay or camera contact**.

Earlier RA-003: [primary-GDT I/O adapter design](../research/GDT_IO_ADAPTER_DESIGN.md), [commands/results](../research/sessions/20261019-RA-003-gdt-io-design.md).
Primary-GDT file adapter and exclusive parent/child control qualified on invented ordinary files and inert child processes. Real os.read calls, EOF probes, source accounting, journal failures and bounded supervision are exercised. Actual host/child bindings received source/AST review only; the actual entry remains inactive and blocked pending exact scope/rights activation-semantic review. No actual firmware, operational constants or saved raw prefix was opened.

**666/666 synthetic cases passed**, zero skipped, exit **0**; **800.360s** suite / **801.228s** wrapper, CPython 3.13.12. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Historical next single package: **RA-003: prepare and independently review the one-shot activation seal for the frozen two-phase primary-GDT observation; no execution**.

Earlier RA-003: [primary-GDT runner design](../research/GDT_RUNNER_DESIGN.md), [commands/results](../research/sessions/20261019-RA-003-gdt-runner-design.md).
Two-phase primary-GDT runner, full-lineage gate and bounded collector qualified on invented data. Phase A reconciles all five historical blocks before planning; phase B repeats complete lineage before descriptor validation. Root proposals and broad planner success statuses are suppressed from outputs. Source telemetry is a synthetic protocol; the actual-I/O adapter and watchdog remain unimplemented. No actual firmware, constants or saved raw prefix was opened.

**547/547 synthetic cases passed**, zero skipped, exit **0**; **280.109s** suite / **280.948s** wrapper, CPython 3.13.12. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Historical next single package: **RA-003: implement and synthetically qualify a separately reviewed actual-I/O adapter and exclusive entry for the two-phase GDT scope, including source telemetry and watchdog; no actual execution**.

Earlier RA-003: [primary-GDT metadata scope](../research/GDT_METADATA_SCOPE.md), [commands/results](../research/sessions/20261019-RA-003-gdt-scope.md).
Primary-GDT observation engineering scope frozen: two planned inspection calls, four complete source passes (4,096,071,392 bytes on success), nine metadata roles, and at most 65,536 new descriptor bytes retained. Phase-A raw prefixes must be cleared before phase B; selected-raw allowances are 73,728 / 139,264 bytes, not process-memory caps. Root proposals are suppressed from every output and cannot reach a reader. Current official legal sources retain a narrow research rationale with unresolved contract/constants questions. No actual replay or planner application to saved actual data occurred.

Unchanged planner/observer baseline: **174/174 passed**, zero skipped, exit **0**, **0.163s**; all eight qualified source and 34 original pins unchanged. The new two-phase runner is not implemented or qualified.

Historical next single package: **RA-003: implement and synthetically qualify the frozen two-phase primary-GDT metadata runner and reconciliation gate; no actual replay or inode/content traversal**.

Earlier RA-003: [ext metadata planner design](../research/EXT_METADATA_PLANNER_DESIGN.md),
[commands/results](../research/sessions/20261019-RA-003-ext-planner-design.md).
Bounded ext metadata planner design: **174/174 synthetic passes**, zero skipped, exit **0**, **0.154s**; **52 retained + 122 new** cases; **8** qualified source/test pins. Invented buffers exercise primary-GDT and root-record proposals with counter, inode and group/reserved-metadata placement checks. All **13** retained ordinary source pins, prior actual results, analysis acts and source lock remain unchanged; no new source acquisition or historical full-suite rerun.

Limits: **1,024 groups**, **32,768 descriptor bytes**, **4,096 prefix bytes** (project budgets). No actual metadata/firmware application, traversal, raw output or camera; planning authorization and all filesystem/content, native English/FTP, recovery and device-write claims remain false.

Historical next single package: **RA-003: review and freeze the rights, lineage and byte limits for a bounded primary-GDT descriptor-metadata observation using the qualified planner; no inode/content traversal**.

Earlier RA-003: [ext-superblock metadata observation](../research/EXT_SUPERBLOCK_OBSERVATION.md),
[commands/results](../research/sessions/20261019-RA-003-ext-observation.md).
Qualification **359/359 passed**, zero skipped, exit **0**, **20.963s**; **320 retained + 39 new** cases. All **53** design-source pins and older seals remain unchanged.
Actual terminal **complete_private_ext_superblock_metadata_observation**, script **0** / host **0**, **38.274879s**. Preparation/pipeline/expanded/observer attempts: **1/1/5/2**.
Source observation **source_read_confirmed**; preparation attempts alone do not establish a read.
One separately frozen two-lead fixed-superblock metadata observation completed after full prior inventory and all-five outcome reconciliation.
Sanitized observation statuses: superblock_metadata_only: 2.
Geometry-issue counts: none under modeled predicates.
Capability blockers: none under modeled policy.
Classic feature-mask matches: **2**; this policy match establishes no planner or traversal eligibility.
All prior results and source lock remain unchanged. No filesystem/checksum/content/authentication, usable read plan, native English/FTP, exact-body, feature/write or recovery claim. No raw output, component files, traversal, decompression/disassembly, private upload, upstream/firmware execution or camera. Eight metadata roles and inherited 65,536 plus new 8,192 selected raw-byte allowances are not aggregate managed/process caps.

Historical next single package: **RA-003: design and synthetically qualify a bounded ext metadata read planner for the observed classic feature masks, adding counter, inode and table-placement eligibility checks; no actual replay or traversal**.

Earlier RA-003: [ext-superblock runner design](../research/EXT_SUPERBLOCK_RUNNER_DESIGN.md),
[commands/results](../research/sessions/20261019-RA-003-ext-runner-design.md).
Bounded ext-superblock runner design: **320/320 synthetic passes**, zero skipped, exit **0**, **17.064s**; **53** qualified source/test pins.
This qualification includes the unchanged **52** pure-observer cases and relevant standard-library lineage/gate regressions, plus new runner cases. Composition: **205** selected inherited regressions + **52** observer cases + **63** new cases. Two historical crypto-dependent cases are excluded, not skipped. This new 320-case suite differs from the historical 320-case preflight suite; historical suites were not rerun in full.
The frozen eight-role basis and complete prior four-key inventory must reconcile before either of two superblock callbacks. Their additional raw-retention allowance is **8,192 bytes**, alongside the inherited **65,536-byte** allowance; neither is an aggregate managed-memory or whole-process cap.
Raw buffers/logical streams were invented and callbacks synthetic; saved structured-metadata preflight was also qualified. No actual firmware, member prefix, operational constants or actual replay; all prior actual results, forty-source seal, four observer pins and analysis acts remain unchanged. The source lock is byte-identical; no new public-source acquisition.
The runner design prepares a later separately frozen metadata observation; it establishes no actual geometry, filesystem validity, usable read plan, English resources or native FTP backend. Planning authorization remains false. No traversal, checksum verification, component/raw files, private upload, upstream/firmware execution, camera, feature/write or recovery gate.

Historical next single package: **RA-003: separately freeze and review one actual two-lead ext-superblock metadata observation, then execute once with full fresh lineage and no traversal or raw output**.

Earlier RA-003: [ext-superblock design](../research/EXT_SUPERBLOCK_DESIGN.md),
[commands/results](../research/sessions/20261019-RA-003-ext-superblock-design.md).
Independent ext-superblock design: **52/52 synthetic passes**, zero skipped, exit **0**, **0.029s**; **4** qualified authored source/test pins.
Eight immutable Linux v6.6 reference texts (**398,478 bytes**) and GPL-2.0-only notices are pinned; signed-release authentication is not established. The separate observer copies no upstream implementation.
Only invented buffers were tested. No actual firmware, member prefix, operational constants or actual replay; all prior actual results, forty-source seal and analysis acts remain unchanged. Historical suites were not rerun.
The initial harness refused (host **1**, child **0**): its regex counted zero although the preserved log shows **52 passes**, zero skips, **0.027s**. A reviewed parser-view CRLF correction preserved raw logs and observer/tests/thresholds; one corrected qualification supplied the accepted result above.
Conditional geometry and conservative feature handling are a synthetic design result, not observed member capabilities, a usable read plan, filesystem validity or English/native FTP support. Planning authorization remains false. No traversal, checksum verification, child/raw files, private upload, upstream/firmware execution, camera, feature/write or recovery gate.

Historical next single package: **RA-003: freeze and synthetically qualify a bounded two-lead ext-superblock metadata-observation runner with complete prior lineage checks; no actual replay or directory traversal in that runner-design package**.

Earlier RA-003: [preflight comparison](../research/PREFLIGHT_COMPARISON.md),
[commands/results](../research/sessions/20261019-RA-003-preflight-comparison.md).
Qualification **346/346 passed**, zero skipped, exit **0**, **12.080s**; **26 new + 320 retained** cases; all **35** predecessor files and **32** historical failed-trial pins preserved.
Actual terminal **complete_private_preflight_expanded_member_comparison**, script **0** / host **0**, **37.595937s**; pipeline attempts **1**, expanded callback attempts **5**.
Source observation **source_read_confirmed**; protected callback attempts are separate and missing preliminary verification does not establish no I/O.
One separately frozen same-five comparison passed its complete lineage and original-outcome checks; limited expanded header leads were recorded after pre-I/O metadata preflight.
No retry, fallback, child/decoded/raw-prefix files, decompression/disassembly, upstream/firmware execution, camera or feature/write gate.
Earlier five unknown outcomes and prior refusal remain unchanged; no retroactive runtime-stage claim.
Sanitized header-lead counts: ext_family_header_candidate/header_only: 2; fat_legacy_header_candidate/malformed_header: 2; unknown/unsupported_opaque: 1.
Selected raw retention remains bounded separately from metadata copies. Six retained prior trees and seven gate snapshots may coexist, each with a 2MiB serialized-role limit, plus caller objects/overhead/other buffers. Historical20MiB pipeline allowance is not an aggregate managed/process memory cap.
Historical next single package: **RA-003: design and synthetically qualify a bounded ext-family superblock capability and geometry gate using pinned authoritative format sources; no actual replay or directory traversal**.

Earlier RA-003: [metadata preflight](../research/METADATA_PREFLIGHT.md),
[commands/results](../research/sessions/20261019-RA-003-metadata-preflight.md).
Metadata-only qualification **320/320 passed**, zero skipped, exit **0**, **7.649s**; **42 new + 278 retained** cases.
**30** retained source/test files and all **32** historical failed-trial source/runner pins remain unchanged.
Only the new session gate copy is revised; its preflight preserves every field and exact type, with a narrow allowance for finite nonnegative built-in timing floats at two root keys in two prior-summary roles.
Production metadata shapes, signed zero, bounded trees, fixed role/stage diagnostics, mutation isolation and cleanup flags are qualified offline.
No firmware/key/raw-prefix input, actual replay, new download, upstream execution, camera or feature/write gate.
The earlier expanded trial remains **needs_review**, script **2** / host **1**; its precise runtime refusal stage stays unrecorded.
Earlier five unknown classifications and all other actual results remain unchanged. A future pre-I/O runner is still to be frozen and reviewed.
Historical next single work package: **RA-003: freeze and review a runner with pre-I/O metadata preflight and bounded stage diagnostics, then run one separately scoped same-five expanded-header comparison with complete prior lineage**.

Earlier RA-003: [refused expanded-prefix trial](../research/EXPANDED_PREFIX_AUDIT.md),
[commands/results](../research/sessions/20261018-RA-003-expanded-prefix.md).
One frozen same-five expanded-header trial stopped **needs_review**, script exit **2**, host exit **1**, **38.945781s**.
Qualification **278/278 passed**, zero skipped, exit **0**, **2.001s**; 27 new cases plus 251 retained, all 27 foundation files unchanged.
Failure code **expanded_prefix_acceptance_failed**; no accepted expanded candidates, fresh directory or persisted stream-validation result.
Static source/metadata review finds float timing fields in prior summaries rejected by the new freezer; this is a sufficient blocker, not a logged precise runtime stage.
Observer cleanup reported no failures. No retry, fallback, changed threshold, child files or raw-prefix output.
Earlier five unknown classifications and all prior evidence remain unchanged. No decompression/disassembly, upstream/firmware execution, camera or feature/write gate.
Historical next single work package: **RA-003: design and synthetically qualify exact prior-metadata preflight using preserved production summaries, resolving the timing-field schema mismatch before any new actual prefix read**.

Earlier RA-003: [image-parser/header design](../research/IMAGE_HEADER_DESIGN.md),
[commands/results](../research/sessions/20261018-RA-003-image-header-design.md).
Four public parser blobs (**16,708 bytes**) verified at the existing immutable pin;
published MIT notice reviewed and preserved with private source copies.
Separate bounded AXFS/ext-family/legacy-FAT/LZPT header predicates qualified
with **251/251 synthetic passes** (49 new plus 202 retained),
zero skipped, exit **0**, **1.271s**. All 23 baseline files unchanged.
The new API remains standalone and unintegrated. **No actual firmware, member
prefix or operational-constants read**; prior five unknown observations unchanged.
No filesystem, English, native FTP, body-match, recovery or device-write gate.
Historical next single work package: **RA-003: implement and qualify an all-prefix reconciliation gate, then run one frozen expanded-header comparison on the same five members with full prior lineage**.

Earlier RA-003: [selected-member prefix study](../research/MEMBER_PREFIX_AUDIT.md),
[commands/results](../research/sessions/20261018-RA-003-member-prefix.md).
One selected-member prefix experiment completed, script and host exit **0**, **32.470943s**.
Synthetic qualification **202/202 passed**, zero skipped, exit **0**, **1.317s**.
**Five regular image-category candidates**, **4,096 bytes each / 20,480 bytes total**;
all five returned **unknown / unsupported_opaque** under the fixed classifier.
Complete fresh source/stream/header/span/original-prefix lineage and exact whole
directory equality passed before selected classification. No complete member
was covered by these prefixes; raw buffers discarded, no child files or links followed.
Classifier coverage is limited; this does not establish missing formats, English
resources or FTP code. No decompression/disassembly, camera or feature/write gate.
Historical next single work package: **RA-003: audit pinned image-format parser sources and reuse rights, then design and synthetically qualify bounded structural header predicates for the five opaque candidates before another actual read**.

Earlier RA-003: [opaque-link metadata inventory](../research/TAR_LINK_INVENTORY.md),
[commands/results](../research/sessions/20261018-RA-003-tar-link-inventory.md).
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
Historical next single work package: **RA-003: review the private directory to select minimal English/FTP-relevant members, then document, qualify and run bounded in-memory prefix identification with full lineage and no child files**.

Earlier RA-003: [bounded path/link diagnostic](../research/TAR_PATH_DIAGNOSTIC.md),
[commands/results](../research/sessions/20261018-RA-003-tar-path-diagnostic.md).
One bounded first-refusal diagnostic completed, script and host exit **0**, **28.299963s**.
Synthetic qualification **171/171 passed**, zero skipped, exit **0**, **0.916s**.
The first refused field is **link_target**, origin **header**,
predicate **empty_or_parent_component**. Combined categories retain their stated ambiguity.
Complete parent/logical-stream identities, header, declared spans and both prior
prefixes agree. Semantic tar parsing stopped permanently at the unchanged guard;
no directory accepted or tar-end/tail validation. One private bounded event,
no path text/raw bytes in it. No retry/fallback, child files, decompression,
disassembly, camera contact or feature/write gate. Earlier failed evidence is preserved.
Historical next single work package: **RA-003: review the observed path/link predicate, qualify an explicit metadata-only policy and run one bounded directory inventory with complete lineage and no child files**.

Earlier RA-003: [tar-directory refusal](../research/TAR_DIRECTORY_AUDIT.md) and
[commands/results](../research/sessions/20261018-RA-003-tar-directory.md).
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
Historical next single work package: **RA-003: qualify and run one bounded tar path/link diagnostic that records the first refusal category privately, completes source/stream lineage validation, and accepts no directory or child files**.

Earlier RA-003: [bounded component prefixes](../research/COMPONENT_PREFIX_AUDIT.md) and
[commands/results](../research/sessions/20261018-RA-003-component-prefix.md). U-slot SquashFS v4 and firmware ustar
header candidates, 4,096 bytes each. Complete parent/stream/header/spans agree
with prior lineage. Qualification 93/93 passed, exit 0; one real two-pass pipeline
exit 0, 23.899888s. No raw prefix/component files, decompression or disassembly.
No complete format, body, English/FTP, recovery or feature/write gate result.
Historical next single work package: **RA-003: document and qualify a bounded-memory, metadata-only tar-directory inventory of the candidate ustar firmware extent, then run it with full source/stream lineage checks and no child files**.

Earlier RA-003: [full-stream validation](../research/FDAT_STREAM_VALIDATION.md)
measured logical length/SHA and checked declared bounds without identifying children.

Earlier RA-003: [one bounded private header trial](../research/FDAT_HEADER_TRIAL.md).
That first-block observation remains preserved; the later stream result is separate.

Earlier RA-003: [crypto/public-constant provenance](../research/FDAT_CRYPTO_PROVENANCE.md) and
[commands/results](../research/sessions/20261018-RA-003-crypto-provenance.md). Pinned wheel/source identities and
eight isolated AES primitive tests are recorded. Native crypto code ran privately;
no fwtool/firmware or camera execution. One predeclared CXD90057_k8 trial needs
authored implementation and synthetic qualification; no exact-package key finding.
Next single work package: **RA-003: implement, synthetically qualify and run one bounded private FDAT header trial for the predeclared CXD90057_k8 hypothesis**.

Earlier RA-003: [bounded decoding basis/design](../research/FDAT_DECODING_PLAN.md)
and [commands/results](../research/sessions/20261018-RA-003-decoding-design.md). A pure decoded-header validator
checks CRC/extent metadata on synthetic inputs. Full suite: 228 total, 225 passed,
three skipped, exit 0. A narrow statutory rationale is documented; contract
interaction remains unresolved. No real payload read/decoding, crypto dependency
adoption or device action occurred.

Earlier RA-003: [bounded FDAT identification/extractor audit](../research/FDAT_EXTRACTOR_AUDIT.md)
and [commands/results](../research/sessions/20261018-RA-003-fdat-identification.md).
The prefix classifier returned unknown/unsupported_opaque; that is not proof of
encryption. Whole-file identity and previous spans agree. Local suite: 198 total,
195 passed, three skipped, exit 0. The open upstream PR candidate is source-only
and unvalidated for this exact package. This run interpreted a bounded prefix in
memory; it saved/output no prefix contents. No decoding or feature/write gate.

Earlier RA-003: [scoped UFU directory and parser audit](../research/UFU_CONTAINER_AUDIT.md)
and [commands/results](../research/sessions/20261018-RA-003-ufu-inventory.md).
An authored bounded reader and 179-test local suite passed (176 passed, three
skipped). Five chunk spans cover the acquired file under the audited framing;
one FDAT span is bounded. No payload contents were interpreted or output. Full
container semantics, component formats, extraction scope and installed-build
correspondence remain open. Next is bounded FDAT identification/extractor audit.
No camera command or feature/write gate passed.

Earlier RA-003: [official package, bounded identification and statutory route](../research/sessions/20261018-RA-003-package-law.md).
Separate destination consent led to HTTP 200, declared-size agreement and matching
transfer/stored SHA-256. Authored probe: UFU signature candidate; container not
validated. Article 50(5) expressly addresses software reverse-engineering research;
assess its conditions, exact acts and contract interaction before full analysis.
No unpacking/execution or camera contact occurred. Next single package is the
scoped RA-003 analysis/parser review in STATE.

Earlier RA-003: [China scope and limited acquisition results](../research/sessions/20261018-RA-003-cn-scope.md).
Owner confirms inspection in China for personal/noncommercial use. Download
consent is scoped; Article 17 is a candidate, not an established analysis basis.
See STATE for the recorded request/result, and the source dossier for scope.
No native feature, recovery route or write gate is validated.

Earlier RA-003 continuation: [official mainland 2.00 source/terms](../research/MAINLAND_FIRMWARE_SOURCE.md)
and [session results](../research/sessions/20261018-RA-003-mainland.md) are recorded.
No firmware URL GET/HEAD, agreement acceptance or external inquiry occurred.
Next single package: resolve the rights basis for proprietary offline unpacking/
static analysis using the prepared inquiry or another documented applicable
licence/statutory basis. Owner task authorization does not substitute for
third-party rights. Ordinary hashing is not equated with disassembly.

Earlier RA-003 [provenance/rights review](../research/OFFICIAL_PACKAGE_INTAKE.md):
the owner has **No / unknown** firmware inspection permission. One firmware GET
stopped at an unreviewed redirect with zero bytes and no retry; analysis remains
blocked. A separate Sony OSS page lists 34 source packages. The owner approved
only the two BusyBox source downloads under its notice. Both were audited
privately: supplied configs enable FTPGET/FTPPUT; final binary/body mapping is
unproved. No downloaded source was executed or integrated. Next single host
package: rights-cleared exact-2.00 binary intake/correspondence, blocked on rights
and legitimate applicable bytes. No native feature or recovery follows.

## 2. Responsibilities and continuity

| Participant | Responsibility | Must not claim |
|---|---|---|
| Webchat | Source research, design review, hypotheses, task decomposition and review of sanitized evidence | Access to local camera state that has not been supplied |
| Local Codex | Inspect actual local files/tools, implement host tooling, run tests, maintain private journals and propose exact hardware steps | Device success from host tests or another model's results |
| Owner | Provide missing body facts, approve device actions, maintain power/connection and observe physical results | That a repository push authorizes all possible camera mutations |

Git is the shared source of truth for authored code, sanitized findings and decisions. Private artifacts and detailed device state remain local. Read the newest committed state and local journal before resuming; do not rely on a remembered chat summary. A webchat request to investigate a hypothesis is not a blanket instruction to run every associated service command.

Initial offline-only means no camera communication or firmware execution. Normal authenticated Git operations and retrieval of public/official sources are separate host activities. Do not test a camera's network endpoints as part of this initial session.

## 3. Available starter commands

For a new checkout:

```sh
git clone git@github.com:mingwucn/a6700_research.git
cd a6700_research
git status --short --branch
python --version
python -m unittest discover -s tests -v
python tools/offline_inventory.py --help
python tools/artifact_probe.py --help
```

On Windows, use an existing supported Python 3.10+ interpreter, for example py -3 instead of python. Do not install a USB driver, firmware updater or third-party camera package to run these standard-library tests. Initialization tests passed under Python 3.13.5 on the webchat Linux host; Windows and the owner's computer remain untested.

That is the historical initialization result. Later local Windows tests and the
ctime portability repair are recorded in STATE and session reports. A final-code
clean export and the observed four-job Windows/Linux CI matrix have now passed;
see the [qualification report](../research/sessions/20261018-IN-102-final.md).
No camera function or device-write gate is established. See
[artifact intake](ARTIFACT_INTAKE.md) for the probe and
[host validation](HOST_VALIDATION.md) for current CI and publication limits.

If a checkout already exists, inspect status and branch first. Do not reclone over it, reset it, discard changes or force-pull. Use a fresh topic branch such as research/ra-001-intake when the local state permits. If the working tree is dirty, preserve it and isolate new work rather than guessing ownership.

The helper can inventory regular nonempty local files that have already been acquired through some separately authorized process. Example only, after substituting actual existing private paths and the observed firmware version:

```sh
python tools/offline_inventory.py --model ILCE-6700 --firmware UNKNOWN --alias body-01 --kind body-dump --artifact ap=private/body-01/original/ap-copy.bin --artifact cp=private/body-01/original/cp-copy.bin
```

These filenames do not identify real alpha6700 paths. UNKNOWN is an honest placeholder, not an eligible firmware version. The model/version/alias are user-supplied labels and are not verified by the tool. Kind body-dump is also a label, not proof of a complete backup. To inventory an official download, use kind official-package and a label such as package. Do not mix acquisition categories into one misleading report.

Output goes to stdout only. Save it to a NEW private file using an appropriate UTF-8 mechanism; never redirect over an input, because a shell can truncate a file before the Python program starts. Original paths/filenames are omitted from the JSON, but a person can still put a serial in an alias, and hashes can identify private material. Review any report before sharing it. The helper does not verify two backups, parse settings, establish restore coverage or authorize a writer.

## 4. Reference checkouts without execution

The two upstream commits are fixed in references/sources.lock.json. Optional host-side retrieval can use ignored external directories or an independent location. For a new external directory:

```sh
git clone --no-checkout https://github.com/QAQLeonard/a7c2-fl23-research.git external/a7c2-reference
git -C external/a7c2-reference checkout --detach c0930d5b0ccd49c0a092dc883054cd6dce199649
git clone --no-checkout https://github.com/lzh2016zzz/a7cr-fl23-research.git external/a7cr-reference
git -C external/a7cr-reference checkout --detach 43ba74441c8f10459ade41e84a379ad8005e6ef4
```

Do not overwrite an existing reference checkout. Inspect its status first. Do not run FL23.cmd, Custom-LUT.cmd, serviceshell, updatershell, a native worker or an installer merely because the files are present. Review dependencies and licences before importing code. New upstream commits or mutable release assets require a separate diff/hash review; they do not silently replace the lock.

## 5. First session: RA-001 only

Run the starter tests and record the interpreter and all skips/failures. Create a private intake from OWNER_INTAKE and a private session-state copy from templates/DEVICE_FACTS.json, adapting its purpose explicitly rather than pretending it is a populated observation. Do not overwrite an existing intake or journal. Gather owner-supplied firmware/regional/language/host facts; screen photos and serial-bearing details stay private.

Inspect the checked-in UNVERIFIED profile to confirm that it contains no executable support claim. Review git status and ignored-path handling. Create a sanitized session report using templates/SESSION_REPORT.md. Update research/STATE.json only with established facts; leave unknowns null. Commit only specifically reviewed authored files. No camera commands should have been run in this session.

RA-001 can finish with missing owner facts clearly recorded. Its purpose is to establish a reproducible local workspace and a precise intake, not to force a service connection. Proceed to RA-002 source audit after RA-001; do not jump directly to an installer.

## 6. Copy-paste initial Codex prompt

> Work in mingwucn/a6700_research. Read AGENTS.md, README.md, research/STATE.json, docs/CODEX_HANDOFF.md, docs/MASTER_PLAN.md, docs/BACKLOG.md and docs/OWNER_INTAKE.md. Execute RA-001 only: inspect the existing local Git state, record the host environment, run the standard-library synthetic tests, prepare a private owner intake without overwriting existing files, and write a sanitized session report. Prioritize native English menus and native camera-to-server Wi-Fi FTP. FL2/FL3 is deferred, with separately gated calibrated custom still-photo looks later; a host-assisted bridge is a separate optional result. Firmware and regional variant are unknown until observed. Do not contact the camera, change drivers or firmware, run upstream launchers or service tools, upload private inputs, or invent target offsets. Treat ordinary Git/source retrieval as host-side work only. Ask only for missing intake facts, continue useful offline work where possible, and finish with exact commands/results, files changed, unresolved prerequisites and the next single work package. Use a topic branch and stage only reviewed files. Do not mark a feature supported or a device-write gate passed.

## 7. Format for later work requests

A later request should name one work package, exact repository commit, local artifact inventory, relevant source hashes, current known device state and allowed risk tier. It should identify the hypothesis and expected output, not merely say make it work. Any R2/R3/R4 proposal includes the command/assets, expected side effects, stop conditions, current backups and conditional recovery limits before owner approval.

Before a real write, local Codex must recheck the target and candidate against actual fresh inputs. A webchat-approved design cannot certify a local byte sequence it has never inspected. Do not replace machine preconditions with a human confirmation string. No generic service helper is included in this starter because the exact alpha6700 route has not been established.

After an uncertain device outcome, report needs_review, the last confirmed journal step and whether I/O is still active. Do not reboot, retry or restore reflexively. Use the reconciliation procedure for the actual operation. Do not erase a workspace to rerun a clean installation.

## 8. Return packet to webchat

Return one sanitized session report and the corresponding Git commit or pull request. Include the task ID; owner-observed model/firmware/region where relevant; public source pins; non-secret command lines and exit codes; tests with PASS/FAIL/BLOCKED/NOT RUN; evidence class for each conclusion; exact unresolved question; and the next proposed action/risk tier. Include small relevant code excerpts or disassembly summaries with file-offset/VA distinctions when needed.

Do not attach complete firmware, camera backups/calibration, personal photographs, SDK distributions, credentials, serials/MACs or raw packet captures. Raw data stays available locally for reproducibility. Sanitized SHA-256 values may help compare inputs but should still be reviewed for disclosure implications.

Webchat can then review a concrete bounded question, for example whether a traced language field has unrelated consumers, whether a mode table's bounds are preserved, or whether FTP completion is reconciled after a lost reply. It should not be asked to infer camera runtime state from a screenshot of a successful host build.

## 9. Commit and review conventions

Use small branches/commits such as research/ra-002-access-audit, feat/offline-manifest-guards, research/en-101-language-map, research/cl-102-processing-map and research/ft-101-backend-survey. Names are examples, not existing branches. Prefix commit messages with docs, test, tooling or research as appropriate. Keep implementation and a device-result report distinguishable.

Review staged paths and content explicitly. A private repository and .gitignore are not permission to publish firmware or secrets. Never force-push or overwrite another contributor's work. CI, when added later, uses synthetic fixtures and does not require camera credentials or private binaries. A passing CI result must be an actual run, not an expectation.

## 10. Definition of a useful blocked result

A blocked package should contain the exact missing prerequisite, what was tested or inspected, what possibilities have been excluded, what remains uncertain and the smallest next acquisition/experiment. Examples are a missing exact-build resource package, an unverified service-helper ABI, or absent evidence for a capture-complete event. Such a report advances the project without pretending a feature is impossible or attempting unreviewed writes.

Earlier RA-003: [fresh source cache and outer-binding requirements](../research/GDT_OUTER_BINDING_PREPARATION.md), [commands/results](../research/sessions/20261019-RA-003-gdt-source-cache.md).
Fresh read-only snapshots collected **47 Python sources (813,391 bytes)**: 26 authored roles, three bootstrap sources, three integration sources, eleven dependency Python origins and four trusted Python origins. All 47 descriptor, close, EOF and whole-file hash receipts reconciled. The unchanged pure binding planner accepted the 23 eager/three protected source order. **20/20 synthetic snapshot tests passed**, zero skips, exit **0**. Six source-derived outer-gate migration requirements are now explicit. This is source preparation; the actual outer gate remains incomplete and independent operational review has not occurred. No firmware/constants/raw-prefix/native payload read, installed dependency execution, GDT replay or camera contact. English/native FTP and recovery remain unverified.
Next single package: **RA-003: independently review the frozen 38-source packet, corrected bootstrap and 124-case qualification against the metadata-act draft, then resolve findings; no actual activation or GDT replay before review passes**.


Earlier RA-003: [v2 gate progress](../research/GDT_OUTER_GATE_V2.md), [commands/results](../research/sessions/20261019-RA-003-gdt-outer-gate-v2.md).
V2 document validation, child ownership and parent completion checks passed **81/81 synthetic tests**, zero skips, exit **0**; **20** cases directly exercise invented completion receipts. The first 61-case qualification remains historical and is not added to 81. Historical authority pinning and full production bootstrap/factory review remain incomplete. No actual activation bundle or operational seal exists. English/native FTP, rollback and all device gates remain unverified.
Next single package: **RA-003: independently review the frozen 38-source packet, corrected bootstrap and 124-case qualification against the metadata-act draft, then resolve findings; no actual activation or GDT replay before review passes**.


Earlier RA-003: [outer authority and source review](../research/GDT_OUTER_AUTHORITY_REVIEW.md), [commands/results](../research/sessions/20261019-RA-003-gdt-authority-review.md).
The v2 entry now binds **18 reference hashes**, derived from preserved ordinary authorities. The missing historical qualification-review hash was verified through its already pinned review record. **105/105 invented-data tests passed**, zero skips, exit **0** (81 retained + 24 new). Same-agent source/AST and saved-metadata checks reconciled the nine-role basis, 26 authored roles and 47 cached sources. Independent operational review and actual bootstrap/GDT execution remain pending; English/native FTP and rollback remain unverified.
Next single package: **RA-003: independently review the frozen 38-source packet, corrected bootstrap and 124-case qualification against the metadata-act draft, then resolve findings; no actual activation or GDT replay before review passes**.


Earlier RA-003: [invented bootstrap qualification](../research/GDT_BOOTSTRAP_QUALIFICATION.md), [commands/results](../research/sessions/20261019-RA-003-gdt-bootstrap-qualification.md).
The ordinary bootstrap now preflights every input path and pinned archival hash **before opening any input document**. The first invented-file qualification exposed two refusal-order failures; both were fixed without changing tests. Final **124/124 passed**, zero skips, exit **0** (105 retained + 19 new). The complete bootstrap ran only with invented temporary documents and a test-only in-memory authority substitution. No actual saved-input activation or protected continuation ran. Independent review, English/native FTP and rollback remain pending.
Next single package: **RA-003: independently review the frozen 38-source packet, corrected bootstrap and 124-case qualification against the metadata-act draft, then resolve findings; no actual activation or GDT replay before review passes**.


Latest RA-003: [source review packet and proposed act](../research/GDT_REVIEW_PACKET.md), [commands/results](../research/sessions/20261019-RA-003-gdt-review-packet.md).
A private review packet now freezes **38 authored Python sources / 767,313 bytes**, eight review questions and a non-executable draft of the later metadata act. Packet checks verified **279 historical preservation entries** and **143 starting paths**, with all gate/source hashes unchanged. No new synthetic suite or actual observation ran. The prior 124-case result remains historical evidence, not a new pass or execution authority. Independent review remains pending; English/native FTP, exact-body correspondence and rollback remain unverified.
Next single package: **RA-003: independently review the frozen 38-source packet, corrected bootstrap and 124-case qualification against the metadata-act draft, then resolve findings; no actual activation or GDT replay before review passes**.


Historical authorization blocker (superseded by the authorized review round below): [independent-review audit](../research/sessions/20261019-RA-003-independent-review-blocker.md).
The source packet and proposed act are ready, but required independent review has not happened. The local-reviewer authorization request is unanswered. This same prerequisite is recorded in three consecutive completed goal turns; the current audit verified all 38 frozen source hashes and found no substantive next step that can bypass the review. The broad pre-camera goal is **blocked, not complete**. No code or tests changed and no camera/protected-input operation ran.
Next single package remains the independent review of the frozen source packet and act draft.


2026-10-19: [Independent source review findings](../research/sessions/20261019-RA-003-gdt-independent-review.md). Owner authorization received; three local reviewers returned **five distinct unresolved findings**, covering receipt/stdout encoding, interruption cleanup, root-proposal scope and qualification policy. They reported 17 distinct reviewed paths; all 38 frozen source pins remain unchanged. The unchanged **124/124 synthetic cases pass** (zero skips, exit 0), but miss production boundaries exposed by review. Review acceptance, activation, English/native FTP, recovery and device-write gates remain false. Next single package: **RA-003: preserve frozen sources, repair the five review findings in a new revision, add cross-module invented-data regressions and requalify; then obtain source re-review before any activation.**


2026-10-19: [Isolated review repairs](../research/sessions/20261019-RA-003-gdt-review-fixes.md). **Six source findings repaired and accepted by three source-only reviewers; 162/162 synthetic tests pass**, zero skips, exit 0. Original 38 source pins preserved; failed runs retained. Operational cache/reference/role migration and full composition acceptance remain pending. No actual activation, protected-input read or camera command; English/native FTP, recovery and write gates remain false. This supersedes the earlier unresolved-findings status for these scoped repairs only. Next single package: **RA-003: migrate and independently review the ordinary source-cache, role, reference and qualification chain to the repaired revision, with fresh bounded source receipts and invented host/child composition checks; no actual activation or GDT replay.**


2026-10-19: [Successor source preparation](../research/sessions/20261019-RA-003-repaired-source-migration.md): fresh **47-source / 813,858-byte** cache and complete rebased binding graph reconciled; **28/28** new synthetic tests pass. Exactly three changed cached sources retain separate scoped repair evidence. Both outer gate/loader enforcement points still need the same validated overlay; no operational activation, camera contact or feature/write gate. Next single package: RA-003: implement one closed repaired-source overlay in both the outer gate and loader, consuming the successor source/role graph; qualify the full invented host/child composition and independently review the migrated chain before selecting any actual act.


2026-10-19: [Shared source overlay](../research/sessions/20261019-RA-003-source-overlay.md): gate and loader now use one validated map; **188/188** synthetic tests pass. Source review found and resolved a nested-path incompatibility; scoped source acceptance received from three reviewers. Production callback-factory/native composition and operational acceptance remain pending. No camera contact or feature/write gate. Next single package: RA-003: qualify the authored callback factory and full host/child wiring using invented byte streams and source/dependency adapters, then independently review that composition before preparing a real metadata act.

2026-10-19 RA-003: [authored callback factory contracts and cleanup repair](../research/sessions/20261019-RA-003-factory-contracts.md). **29/29 invented-input tests passed**, zero skips, exit **0**; two independent source reviewers accepted a repair that releases remaining owned aliases before reporting an ownership mismatch. Actual factory/wiring functions were exercised with invented role/controller/dependency adapters. Full real adapter/controller/runtime composition and repaired-factory pin migration remain pending. All 42 prior source/specification pins are unchanged. No firmware/constants/prefix/native input, installed backend or camera access; English/native FTP, recovery and device-write gates remain false. Next single package: **RA-003: compose the repaired callback factory with the real authored adapter and controller on invented byte streams, qualify that composition, and migrate/review its new source pin in the outer gate before preparing any real metadata act.**

2026-10-19 RA-003: [authored child composition](../research/sessions/20261019-RA-003-factory-composition.md): **8/8 invented-input tests passed**, zero skips, exit **0**, **23.846s**. Real factory, 26 authored roles, adapter, child controller, wiring and runtime orchestration compose with invented AES/native/backend readers. Corrected a fixture/classifier mismatch and a supervisor fixture-roster defect; failed and superseded results remain preserved. Two source reviewers accepted the scoped result; 47 qualification inputs and all 42+4 prior pins match. Outer gate/parent integration and repaired-factory pin migration remain pending. No actual firmware/constants/prefix/native dependency or camera access; English/FTP, recovery and write gates remain false. Next single package: **RA-003: migrate the repaired factory source pin and its reviewed qualification into one successor outer gate/loader chain, then qualify parent-process and child composition on invented inputs before any real metadata act.**

2026-10-19 RA-003: [factory source gate](../research/sessions/20261019-RA-003-factory-source-gate.md): **207/207 invented-input tests passed**, zero skips, exit **0**, **4.152s**; seven separate ordinary-reader tests passed. The v4 gate/loader binds the repaired factory to its 29-case contract and eight-case child-composition evidence. Fresh **47-source / 814,219-byte** ordinary cache differs only in the factory, and fixed loader references identify it. Parent/child integration and operational acceptance remain pending. The refreshed external project remains a source-reported FTP lead with no established English unlock or proven rollback. No camera contact, protected input or cached dependency execution; English/FTP, recovery and write gates remain false. Next single package: **RA-003: qualify the successor v4 gate, loader and parent/child composition on invented inputs using the reviewed factory and prepared source identities; resolve independent review findings before selecting any actual metadata act.**


2026-10-19 RA-003: [parent/child composition](../research/sessions/20261019-RA-003-parent-child-composition.md): **7/7 real-process invented-input cases passed**, plus **207/207 adapted retained unit cases**, zero skips, exit 0. A reviewed parent module-lifetime repair keeps 23 ordinary roles available through reconciliation. All 81/82 recorded source and fixture pins match current files and snapshots. Strict outer acceptance still rejects injected native provenance; production bootstrap, fixed successor references and noninjected dependency composition remain pending. No actual firmware/constants/native input or camera contact; English/FTP, recovery and write gates remain false. Next single package: **RA-003: qualify production bootstrap on invented inputs and bind/review the repaired parent-loader revision in the complete successor source/qualification chain; no actual metadata act or camera contact.**


2026-10-19 RA-003: [production bootstrap on invented authority](../research/sessions/20261019-RA-003-bootstrap-qualification.md): **14/14 tests passed**, zero skips, exit 0; all **85** source/fixture pins and **82** predecessor copies verified. Exact bootstrap code accepts an explicit invented in-memory policy; real main launches an unchanged child that correctly refuses fixed production references. Review identified missing successor parent-evidence contract **BOOT-GR-001**; historical seven-case evidence is frozen, not consumed or activated. No production fixed-policy/native acceptance or camera contact; English/FTP, recovery and write gates remain false. Next single package: **RA-003: implement and qualify the closed successor parent-evidence contract, bind gate/entry references, then qualify final source and parent/child composition with independent source review; no actual metadata act or camera contact.**


2026-10-19 RA-003: [required parent evidence and v5 qualification](../research/sessions/20261019-RA-003-parent-evidence-v5.md): **253/253 passed**, zero skips, exit 0 (**232 gate/unit + 14 bootstrap + seven real-process invented composition cases**). Reviewed v5 gate/entry now require exact historical seven-case evidence; BOOT-GR-001 resolved in source. All 90 qualification pins and 86 predecessor inputs verified. Current source was qualified after references finalized; historical entry identity remains unchanged. Fixed production policy/native composition and actual saved bundle acceptance remain unqualified. No camera contact; English/FTP, recovery and write gates remain false. Next single package: **RA-003: qualify noninjected dependency-only composition for the frozen v5 revision using public AES vectors and live startup/native receipts, excluding firmware/constants; independently review scope before any actual metadata act or camera contact.**


2026-10-19 RA-003: [noninjected public-vector dependency continuation](../research/sessions/20261019-RA-003-dependency-continuation.md): **81/81 synthetic/inert tests passed**, zero skips, exit 0. One independently reviewed existing-venv child completed, exit **0**, **0.4664872s**, no retry. Exact frozen v5 runtime component passed **24 public AES comparisons before + 24 during the live callback**, with eleven source origins and five audited native loads. Full raw provenance was durably published before the single callback claim; two independent saved-output reviews accepted this dependency-only observation. Initial source-review blockers (interruption cleanup and executable binding) were repaired in new copies and regression-tested. Initial output-verifier raw/canonical path mismatch was corrected on saved outputs without repeating the act. This does not qualify the full v5 outer gate, actual saved operational bundle or GDT execution. No firmware/constants/saved-prefix or camera access; English/native FTP, recovery and device-write gates remain false. Next single package: **RA-003: reconcile and independently review the saved operational source/basis packet against the frozen v5 entry and dependency-continuation evidence, resolving remaining chain bindings before any actual metadata observation.**

2026-10-19 RA-003: [saved operational reconciliation](../research/sessions/20261019-RA-003-operational-reconciliation.md): **24/24 new invented regressions passed**, zero skips. Two reviewers accepted narrow diagnostic source after fixed read/hash/receipt repairs; the single actual saved-metadata diagnostic refused at historical source binding (exit 1). All29 current paths retain an activation prefix absent from the historical seal keys; a separate static ancestor mapping matches all29 hashes. Gate/cache/seal remain unchanged; no protected input/camera reads or operational acceptance. Next single package: **RA-003: implement and independently review an explicit historical source-namespace migration in a successor gate, qualify all 29 archived identities and negative collision/substitution cases, and bind the successor source/qualification chain before a fresh saved-metadata diagnostic.**

2026-10-19 RA-003: [explicit source ancestry](../research/sessions/20261019-RA-003-source-ancestry.md): **35/35 invented tests passed**, zero skipped, exit0,0.638s suite; five source/map/fixture pins stable. Two independent source reviews accepted the isolated29-row migration (26 unchanged,3 reviewed replacements). Initial34pass/1error and source preserved; explicit bootstrap-cache paths repaired. Historical gate/cache/seal and refused diagnostic unchanged. No new saved diagnostic, native/input/camera access or operational acceptance. Next single package: **RA-003: bind the reviewed ancestry successor and its qualification into a versioned gate/entry source chain, then qualify complete invented parent/child composition before a fresh saved-metadata diagnostic.**


2026-10-19 RA-003: [ancestry-bound v6 chain](../research/sessions/20261019-RA-003-ancestry-chain-v6.md): **305/305 invented tests passed**, zero skips, exit 0 (**284 unit + 14 bootstrap + seven real-process composition**, 114.266s suite). All **89** source/fixture and snapshot pins plus **84** predecessor inputs verified. Two source-only reviewers accepted final source and saved evidence; the 284-unit gate projection retains the raw 305-case result hash. Source-local ancestry fixture closes an evidence gap; projector helper identity is checked before execution. Fixed production policy/actual saved-bundle acceptance remain pending, and strict outer provenance refuses injected composition. No protected-input observation or camera contact; English/FTP, recovery and write gates remain false. Next single package: **RA-003: prepare and independently review one v6 saved-metadata reconciliation diagnostic against the frozen qualification and explicit ancestry, then run only that ordinary-metadata diagnostic; no protected-input inspection or runtime activation.**


2026-10-19 RA-003: [v6 saved-metadata reconciliation](../research/sessions/20261019-RA-003-v6-saved-reconciliation.md). **40/40 invented tests passed**, zero skips; one saved diagnostic returned **0** with **16 component stages passed**. Its **47 ordinary reads** (11 bootstrap + nine supplemental + 27 mapped documents) recorded stable identities and one close each. Two source-only reviewers accepted the narrow saved result; all nine source/snapshot pairs and reviewed artifact hashes reverified at publication without replay. Historical namespace mismatch is resolved; complete binding-plan recomputation and complete basis semantics remain pending. Source buffers were decoded/hashed as data; no cached-source, native dependency, firmware or camera execution. English/native FTP, recovery and device-write gates remain false. Next single package: **RA-003: prepare source-only complete binding-plan recomputation and complete saved-basis semantic validation against the frozen ordinary authority graph; qualify invented mismatch tests and obtain independent review before any new saved-metadata diagnostic.**


2026-10-19 RA-003: [complete-plan comparison and basis coverage design](../research/sessions/20261019-RA-003-binding-basis-design.md). **30/30 invented tests passed**, zero skips, exit **0**, **1.727s**; all **38** final snapshot pins and **33** authored-source origins verified. Two independent source-only reviewers accepted the corrected design. The complete plan is recomputed/compared on invented inputs while preserving blockers/false flags; the eleven-helper pure loader does not execute role buffers. Nine-role freeze_basis is bounded preflight/cross-binding, not complete evidence semantics. Initial unbounded serialization was repaired before any actual act; hostile graph regressions pass. Actual saved plan/preflight not run; full semantics, rights/operational/recovery gates remain pending. English/native FTP remain primary and unvalidated. Camera commands: none. Next single package: **RA-003: prepare and independently review a once-only ordinary-metadata diagnostic binding the eleven pure helper hashes to the frozen v6 source graph; recompute the entire binding plan with the real interpreter namespace and rerun the existing nine-role preflight, retaining full semantics and execution gates as unresolved.**


2026-10-19 RA-003: [complete saved binding-plan and nine-role preflight](../research/sessions/20261019-RA-003-binding-basis-diagnostic.md). **76/76 invented tests passed**, zero skips, five exits 0. Both original runtime findings were repaired and independently source-reviewed before one diagnostic: **child 0 / supervisor 0**, 0.68248560000211s, **17 stages**, **53 ordinary reads / 2,397,309 bytes**. Eleven exact reviewed pure cached helpers executed; all 26 role buffers checked, 97 actual namespace aliases unchanged. Two source-only outcome reviews accepted the narrow result. Full saved-basis semantics remain unresolved; both dependency/native-policy planner blockers remain. No firmware/constants/raw-prefix/native dependency or camera access, feature/recovery/write gate. English/native FTP remain primary. Camera commands: none. Next single package: **RA-003: implement and qualify comprehensive saved-only semantic predicates for the nine-role basis, explicitly retaining claims requiring fresh observation as blockers; obtain independent source review before any new actual metadata or protected-input act.**


2026-10-19 RA-003: [saved semantic predicate design](../research/sessions/20261019-RA-003-saved-semantics-design.md). **64/64 invented tests passed**, zero skips, exit **0**, **7.391s**; **57** current pins, **40** copied-source origins and **52** preserved R1 snapshot identities verified. Two source-only reviewers accepted the repaired per-interval extension feasibility after finding the aggregate bound too weak. Complete producer schemas, nine-role correlations and saved EXT derivation are qualified on invented records. Actual saved-record application, source authority, historical/raw truth and operational acceptance remain pending. English/native FTP remain primary and unvalidated; no camera/protected-input access, feature/recovery/write gate. Camera commands: none. Next single package: **RA-003: bind the reviewed saved-semantic validator and its scalar/helper hashes to the frozen ordinary source authority graph, qualify substituted-source and mismatch refusals, and independently review a once-only saved-record diagnostic before running it; no protected-input observation or runtime activation.**


2026-10-19 RA-003: [saved semantic binding diagnostic and contract correction](../research/sessions/20261019-RA-003-semantic-binding-diagnostic.md). **One saved-metadata diagnostic refused** (child 1 / supervisor 1, 0.8385605000075884s) at historical stream semantics after 17 stages. All 62 ordinary receipts / 2,473,268 bytes verified; no retry. Two saved-output reviews accepted the narrow refusal. Historical stream producer declares 4 MiB; the validator mistakenly required later 5 MiB. A one-literal successor preserves measured/prefix 5 MiB and passed **72/72 invented cases**, zero skips, exit 0, 8.125s (64 retained + eight new); two source reviews / 54 pins. No successor actual application or operational acceptance. Actual namespace assertion was not reached. English/native FTP remain primary; no protected-input/camera access, feature/recovery/write gate. Camera commands: none. Next single package: **RA-003: bind the reviewed historical-stream contract correction and producer identity into a successor saved-metadata diagnostic, qualify complete composition and source substitutions, and obtain exact-source review before a new once-only application; no protected-input or camera access.**
