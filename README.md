# Sony alpha6700 research

Initial research and local-Codex hand-off, prepared on 2026-10-18.

**Status: planning and offline tooling only. No alpha6700 firmware patch, English unlock, service-access method, or native FTP implementation has been validated by this project. No camera was connected or modified during initialization.**

## Objectives

1. **Priority: native English menus**, preserving the body's original regional/radio configuration and calibration. Owner reports English is unavailable on this mainland China version; enablement feasibility is unverified.
2. **Priority: native camera-to-server FTP over Wi-Fi**, manual uploads first, then automatic transfer. Keep an optional host-assisted bridge separate.
3. **Deferred: FL2/FL3 Creative Looks**, then calibrated custom DCP/LUT-derived still-photo looks as a separately gated extension.

The owner confirmed this priority order on 2026-10-18. FL2/FL3 work must not delay
English or native FTP; all feature acceptance and device-approval gates still apply.

Owner intake (2026-10-18, **source-report**): α6700, firmware **2.00**,
current menu language **简体中文 (Simplified Chinese)**, **Chinese mainland
version**, and **English unavailable**. The complete language
list has not been supplied; exact regional SKU and binary identity remain
unverified. See the [latest intake](research/sessions/20261018-owner-mainland-english.md).
Version text does not verify binary identity. Do not update firmware, run another
model's installer, or change product identifiers merely to begin this project.

Current [RA-003 package/rights findings](research/OFFICIAL_PACKAGE_INTAKE.md):
the [official mainland 2.00 source and its agreement](research/MAINLAND_FIRMWARE_SOURCE.md)
are identified. The [package/statutory-route continuation](research/sessions/20261018-RA-003-package-law.md)
records consented acquisition, size/hash and bounded UFU identification. The later
[scoped directory audit](research/UFU_CONTAINER_AUDIT.md) records five bounded
chunks and one FDAT span, without extracting contents. The latest
[FDAT/extractor audit](research/FDAT_EXTRACTOR_AUDIT.md) records an opaque
4,096-byte prefix result and a pinned source-only candidate. The later
[decoding plan](research/FDAT_DECODING_PLAN.md) documents the narrow research
rationale and a synthetic decoded-header validator. The later
[crypto/provenance audit](research/FDAT_CRYPTO_PROVENANCE.md) pins private inputs and records eight
isolated AES primitive tests. The later
[bounded header trial](research/FDAT_HEADER_TRIAL.md) passed one predeclared real
hypothesis. The latest [stream validation](research/FDAT_STREAM_VALIDATION.md) checked
all 1,000,017 physical blocks, measured 1,020,017,152 logical bytes and checked declared
extent bounds/non-overlap after 45 new synthetic passes. Component formats and
English/FTP mapping remain unverified; no decoded component files were retained.
The latest [component-prefix experiment](research/COMPONENT_PREFIX_AUDIT.md) found
SquashFS v4 and ustar header candidates, 4,096 bytes each, after 93 synthetic
passes and full lineage revalidation. No component directory or feature mapping yet.
The later [tar-directory trial](research/TAR_DIRECTORY_AUDIT.md) stopped at its
fixed `unsafe_path` guard after 133 synthetic passes. No directory was accepted;
the later [bounded path/link diagnostic](research/TAR_PATH_DIAGNOSTIC.md)
identifies the first refused field/predicate after complete source lineage checks.
The later [opaque-link metadata inventory](research/TAR_LINK_INVENTORY.md)
checks the complete tar directory privately; links are never followed or written.
The latest [selected-member prefix study](research/MEMBER_PREFIX_AUDIT.md)
checked five private image-category candidates; all were unknown under the limited
classifier. The latest [image-header design](research/IMAGE_HEADER_DESIGN.md)
audits four pinned public parsers and qualifies separate synthetic predicates;
no new actual read in that design package. The later [expanded-prefix trial](research/EXPANDED_PREFIX_AUDIT.md)
stopped at acceptance; static review identifies a prior-summary schema mismatch.
No expanded result accepted. The later [metadata preflight](research/METADATA_PREFLIGHT.md)
qualified production-summary handling with 320 synthetic passes and no actual replay.
The later [preflight comparison](research/PREFLIGHT_COMPARISON.md) records one separately
frozen same-five outcome; full formats and English/FTP mapping remain pending. China
Copyright Law Article 50(5) expressly addresses reverse-engineering research;
its limits and the accepted terms remain part of the scoped analysis review.
The activity-specific basis for proprietary unpacking/static disassembly remains
unestablished; the earlier owner rights answer stays **No / unknown**.
Recovery is unproved; separate OSS offers are static leads only. No native
feature is validated.

## Reading order

- [Requested functions and progress](docs/FEATURE_PROGRESS.md): native English,
  FL2/FL3, later calibrated custom looks, native Wi-Fi FTP and optional bridge.
- [Master plan](docs/MASTER_PLAN.md): scope, dependencies, milestones and decision gates.
- [Owner intake and required inputs](docs/OWNER_INTAKE.md): exactly what local development needs, with privacy boundaries.
- [Reference assessment](docs/REFERENCE_ANALYSIS.md): pinned upstream sources, reusable methods and non-portable details.
- [Access, backup and recovery](docs/ACCESS_AND_RECOVERY.md): risk tiers, evidence capture and transaction rules.
- [Creative Looks implementation](docs/CREATIVE_LOOKS.md): AP/CP mapping, still output, preview, metadata, custom-look extension.
- [English language implementation](docs/ENGLISH_LANGUAGE.md): regional configuration versus resources and reversible migration.
- [FTP implementation](docs/FTP.md): native feasibility tree, protocol behaviour, security and separately labelled bridge.
- [Validation and release](docs/VALIDATION.md): concrete test cases, acceptance criteria and failure handling.
- [Task backlog](docs/BACKLOG.md): ordered, independently reviewable local-Codex work packages.
- [Codex hand-off](docs/CODEX_HANDOFF.md): first session, commands and the webchat/local collaboration protocol.

Read [AGENTS.md](AGENTS.md) before changing anything. Start with [project state](research/STATE.json), not a remembered chat conclusion. The executable starter is an offline artifact-inventory helper, not a patcher or camera-dump tool. [Source lock](references/sources.lock.json) records the upstream revisions used for this plan.

Host-only continuation now adds a bounded [artifact probe](docs/ARTIFACT_INTAKE.md),
[inventory portability repair](docs/INVENTORY_PORTABILITY.md), synthetic-only
[candidate/transaction models](docs/OFFLINE_GUARDS.md), a separate
[durable synthetic transaction journal](docs/DURABLE_SYNTHETIC_JOURNAL.md), and a durable
[mock transfer queue](docs/FTP_HOST_PROTOCOL.md). A separate opt-in
[synthetic loopback FTPS lab](docs/FTPS_LOOPBACK_LAB.md) tests a constrained peer
with pinned private dependencies. No camera adapter or device executor exists.
[Pre-camera coverage](research/PRE_CAMERA_READINESS.md)
keeps all 27 work packages and their remaining evidence requirements visible.
[Observed host validation](docs/HOST_VALIDATION.md) now records a clean final-code
export and passing four-job Windows/Linux CI. The [completion audit](research/PRE_CAMERA_AUDIT.md)
and [official-source refresh](research/OFFICIAL_SOURCE_REFRESH.md) preserve remaining
exact-target inputs and feature limits.

## Start locally

```sh
git clone git@github.com:mingwucn/a6700_research.git
cd a6700_research
python -m unittest discover -s tests -v
```

Use a supported Python 3.10+ interpreter available on the local machine; the starter uses only the standard library. On Windows, `py -3` may be substituted for `python`. Do not install USB drivers or run upstream launchers as part of this first step.

Copy the intake/state templates into an ignored private workspace before adding body-specific details. Full firmware, camera backups, calibration, photos, credentials, SDK packages and generated firmware payloads stay outside Git, even while this repository is private. `.gitignore` is a convenience, not an access-control or secret-scanning system.

## Evidence policy

Source documentation, static inference, host tests, camera readback, runtime observation and physical photographic tests are different evidence classes. None may be silently promoted into another. Unknown target addresses, command support and recovery capabilities remain unknown until established on the exact target.

The reference repositories are independent experimental research, not Sony-signed firmware updates. The plan adapts their methodology; it does not transplant their device-specific offsets or promise their results on the alpha6700.

Earlier RA-003 source/synthetic continuation: [ext-superblock design](research/EXT_SUPERBLOCK_DESIGN.md).
Independent ext-superblock design: **52/52 synthetic passes**, zero skipped, exit **0**, **0.029s**; **4** qualified authored source/test pins.
Eight immutable Linux v6.6 reference texts (**398,478 bytes**) and GPL-2.0-only notices are pinned; signed-release authentication is not established. The separate observer copies no upstream implementation.
Only invented buffers were tested. No actual firmware, member prefix, operational constants or actual replay; all prior actual results, forty-source seal and analysis acts remain unchanged. Historical suites were not rerun.
The initial harness refused (host **1**, child **0**): its regex counted zero although the preserved log shows **52 passes**, zero skips, **0.027s**. A reviewed parser-view CRLF correction preserved raw logs and observer/tests/thresholds; one corrected qualification supplied the accepted result above.
Conditional geometry and conservative feature handling are a synthetic design result, not observed member capabilities, a usable read plan, filesystem validity or English/native FTP support. Planning authorization remains false. No traversal, checksum verification, child/raw files, private upload, upstream/firmware execution, camera, feature/write or recovery gate.

Earlier RA-003 synthetic continuation: [ext-superblock runner design](research/EXT_SUPERBLOCK_RUNNER_DESIGN.md).
Bounded ext-superblock runner design: **320/320 synthetic passes**, zero skipped, exit **0**, **17.064s**; **53** qualified source/test pins.
This qualification includes the unchanged **52** pure-observer cases and relevant standard-library lineage/gate regressions, plus new runner cases. Composition: **205** selected inherited regressions + **52** observer cases + **63** new cases. Two historical crypto-dependent cases are excluded, not skipped. This new 320-case suite differs from the historical 320-case preflight suite; historical suites were not rerun in full.
The frozen eight-role basis and complete prior four-key inventory must reconcile before either of two superblock callbacks. Their additional raw-retention allowance is **8,192 bytes**, alongside the inherited **65,536-byte** allowance; neither is an aggregate managed-memory or whole-process cap.
Raw buffers/logical streams were invented and callbacks synthetic; saved structured-metadata preflight was also qualified. No actual firmware, member prefix, operational constants or actual replay; all prior actual results, forty-source seal, four observer pins and analysis acts remain unchanged. The source lock is byte-identical; no new public-source acquisition.
The runner design prepares a later separately frozen metadata observation; it establishes no actual geometry, filesystem validity, usable read plan, English resources or native FTP backend. Planning authorization remains false. No traversal, checksum verification, component/raw files, private upload, upstream/firmware execution, camera, feature/write or recovery gate.

Earlier RA-003: [ext-superblock metadata observation](research/EXT_SUPERBLOCK_OBSERVATION.md).
Qualification **359/359 passed**, zero skipped, exit **0**, **20.963s**; **320 retained + 39 new** cases. All **53** design-source pins and older seals remain unchanged.
Actual terminal **complete_private_ext_superblock_metadata_observation**, script **0** / host **0**, **38.274879s**. Preparation/pipeline/expanded/observer attempts: **1/1/5/2**.
Source observation **source_read_confirmed**; preparation attempts alone do not establish a read.
One separately frozen two-lead fixed-superblock metadata observation completed after full prior inventory and all-five outcome reconciliation.
Sanitized observation statuses: superblock_metadata_only: 2.
Geometry-issue counts: none under modeled predicates.
Capability blockers: none under modeled policy.
Classic feature-mask matches: **2**; this policy match establishes no planner or traversal eligibility.
All prior results and source lock remain unchanged. No filesystem/checksum/content/authentication, usable read plan, native English/FTP, exact-body, feature/write or recovery claim. No raw output, component files, traversal, decompression/disassembly, private upload, upstream/firmware execution or camera. Eight metadata roles and inherited 65,536 plus new 8,192 selected raw-byte allowances are not aggregate managed/process caps.

Earlier RA-003 synthetic continuation: [ext metadata planner design](research/EXT_METADATA_PLANNER_DESIGN.md).
Bounded ext metadata planner design: **174/174 synthetic passes**, zero skipped, exit **0**, **0.154s**; **52 retained + 122 new** cases; **8** qualified source/test pins. Invented buffers exercise primary-GDT and root-record proposals with counter, inode and group/reserved-metadata placement checks. All **13** retained ordinary source pins, prior actual results, analysis acts and source lock remain unchanged; no new source acquisition or historical full-suite rerun.

Limits: **1,024 groups**, **32,768 descriptor bytes**, **4,096 prefix bytes** (project budgets). No actual metadata/firmware application, traversal, raw output or camera; planning authorization and all filesystem/content, native English/FTP, recovery and device-write claims remain false.

Earlier RA-003 scope review: [primary-GDT metadata scope](research/GDT_METADATA_SCOPE.md), [commands/results](research/sessions/20261019-RA-003-gdt-scope.md).
Primary-GDT observation engineering scope frozen: two planned inspection calls, four complete source passes (4,096,071,392 bytes on success), nine metadata roles, and at most 65,536 new descriptor bytes retained. Phase-A raw prefixes must be cleared before phase B; selected-raw allowances are 73,728 / 139,264 bytes, not process-memory caps. Root proposals are suppressed from every output and cannot reach a reader. Current official legal sources retain a narrow research rationale with unresolved contract/constants questions. No actual replay or planner application to saved actual data occurred.

Unchanged planner/observer baseline: **174/174 passed**, zero skipped, exit **0**, **0.163s**; all eight qualified source and 34 original pins unchanged. The new two-phase runner is not implemented or qualified.

Historical next single package: **RA-003: implement and synthetically qualify the frozen two-phase primary-GDT metadata runner and reconciliation gate; no actual replay or inode/content traversal**.

Earlier RA-003 runner: [primary-GDT runner design](research/GDT_RUNNER_DESIGN.md), [commands/results](research/sessions/20261019-RA-003-gdt-runner-design.md).
Two-phase primary-GDT runner, full-lineage gate and bounded collector qualified on invented data. Phase A reconciles all five historical blocks before planning; phase B repeats complete lineage before descriptor validation. Root proposals and broad planner success statuses are suppressed from outputs. Source telemetry is a synthetic protocol; the actual-I/O adapter and watchdog remain unimplemented. No actual firmware, constants or saved raw prefix was opened.

**547/547 synthetic cases passed**, zero skipped, exit **0**; **280.109s** suite / **280.948s** wrapper, CPython 3.13.12. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Historical next single package: **RA-003: implement and synthetically qualify a separately reviewed actual-I/O adapter and exclusive entry for the two-phase GDT scope, including source telemetry and watchdog; no actual execution**.

Earlier RA-003 I/O adapter: [primary-GDT I/O adapter design](research/GDT_IO_ADAPTER_DESIGN.md), [commands/results](research/sessions/20261019-RA-003-gdt-io-design.md).
Primary-GDT file adapter and exclusive parent/child control qualified on invented ordinary files and inert child processes. Real os.read calls, EOF probes, source accounting, journal failures and bounded supervision are exercised. Actual host/child bindings received source/AST review only; the actual entry remains inactive and blocked pending exact scope/rights activation-semantic review. No actual firmware, operational constants or saved raw prefix was opened.

**666/666 synthetic cases passed**, zero skipped, exit **0**; **800.360s** suite / **801.228s** wrapper, CPython 3.13.12. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Historical next single package: **RA-003: prepare and independently review the one-shot activation seal for the frozen two-phase primary-GDT observation; no execution**.

Earlier RA-003: [dependency-only runtime provenance](research/DEPENDENCY_RUNTIME_PROVENANCE.md), [commands/results](research/sessions/20261019-RA-003-dependency-runtime.md).
One independently reviewed dependency-only child completed, exit **0**, **0.344s**. **34/34 probe tests** and **13/13 supervisor tests** passed with zero skips. All **24 public NIST comparisons** passed across twelve cases: ECB/CBC, 128/192/256-bit keys, default and generic requests, fresh encryption and decryption. Eleven exact cached Python origins and five native library load intents/audit events/completions were retained in a durable private raw receipt. This observes host dependency behavior; no firmware/GDT replay, English/FTP feature, recovery or device-write gate passed. English/native FTP remain first.
Historical next single package: **RA-003: integrate the observed dependency origins/startup and durable native receipts into a separately qualified GDT entry and review its exact operational basis; no GDT replay or camera contact**.

Earlier RA-003: [dependency descriptor provenance](research/DEPENDENCY_DESCRIPTOR_PROVENANCE.md), [commands/results](research/sessions/20261019-RA-003-dependency-provenance.md).
One independently reviewed descriptor-only dependency audit completed, exit **0**, **3.165s**, after **33/33 invented-file tests passed** (zero skipped, exit **0**, **14.513s** wrapper). The pinned wheel has **352 entries**; **351 installed payload files** match. It also records **4 installation extras** and **56 runtime/startup data files**, including **1 startup file**. The collector did not import the audited package or load its native backend. Native origins/load completion remain unobserved; GDT execution stays unauthorized. No firmware/constants/saved-prefix read, camera contact, feature, recovery or device-write gate. English/native FTP remain first.
Historical next single package: **RA-003: implement, independently review and qualify a dependency-only public-vector runtime provenance probe and the required source fixes for observed origins/startup and durable native receipts; no GDT replay or camera contact**.

Earlier RA-003 preparation: [non-executable GDT activation preparation](research/GDT_ACTIVATION_PREPARATION.md), [commands/results](research/sessions/20261019-RA-003-gdt-activation-review.md).
Closed activation and binding validators qualified on invented records, wheels, file receipts and inert loader models. The 26-role dependency graph is bound to exact cached source bytes. New prospective host/child wiring received source/AST review only. The current preparation, review and seal all prohibit execution. The nine-role object is an opaque reference index; an operational basis remains unassembled. No actual firmware, operational constants, installed dependency or saved raw prefix was opened.

**811/811 synthetic cases passed**, zero skipped, exit **0**; **812.459s** suite / **813.447s** wrapper, CPython 3.13.12. **666 retained + 145 new** cases. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Historical next single package: **RA-003: acquire and independently assess the exact ordinary dependency provenance needed for the frozen GDT observation, then review its activity-specific execution decision; no GDT replay or camera contact**.

Earlier RA-003: [GDT dependency integration and complete metadata basis](research/GDT_RUNTIME_INTEGRATION.md), [commands/results](research/sessions/20261019-RA-003-gdt-runtime-integration.md).
Dependency/controller composition qualified on **51/51 invented-data tests**, zero skips, exit **0** (**38 core + 13 composition**; **34.711s** suite / **35.305s** wrapper). The complete nine-role saved metadata basis assembled and passed the unchanged pure preflight. Full raw dependency receipts are durably retained before protected continuation, with the guarded dependency session alive through both modeled GDT phases. The new prospective factory received source/AST review only; its CLI remains disabled and the exact outer activation chain is absent. No GDT replay, firmware/constants/prefix read, installed dependency execution or camera contact occurred. English/native FTP, exact-body correspondence, recovery and device-write gates remain unverified.
Historical next single package: **RA-003: complete and independently review the exact outer activation/binding chain for the no-site GDT entry and assembled basis, including fresh ordinary source-cache receipts; no GDT replay until that review passes**.

Earlier RA-003: [fresh source cache and outer-binding requirements](research/GDT_OUTER_BINDING_PREPARATION.md), [commands/results](research/sessions/20261019-RA-003-gdt-source-cache.md).
Fresh read-only snapshots collected **47 Python sources (813,391 bytes)**: 26 authored roles, three bootstrap sources, three integration sources, eleven dependency Python origins and four trusted Python origins. All 47 descriptor, close, EOF and whole-file hash receipts reconciled. The unchanged pure binding planner accepted the 23 eager/three protected source order. **20/20 synthetic snapshot tests passed**, zero skips, exit **0**. Six source-derived outer-gate migration requirements are now explicit. This is source preparation; the actual outer gate remains incomplete and independent operational review has not occurred. No firmware/constants/raw-prefix/native payload read, installed dependency execution, GDT replay or camera contact. English/native FTP and recovery remain unverified.
Next single package: **RA-003: independently review the frozen 38-source packet, corrected bootstrap and 124-case qualification against the metadata-act draft, then resolve findings; no actual activation or GDT replay before review passes**.


Earlier RA-003: [v2 gate progress](research/GDT_OUTER_GATE_V2.md), [commands/results](research/sessions/20261019-RA-003-gdt-outer-gate-v2.md).
V2 document validation, child ownership and parent completion checks passed **81/81 synthetic tests**, zero skips, exit **0**; **20** cases directly exercise invented completion receipts. The first 61-case qualification remains historical and is not added to 81. Historical authority pinning and full production bootstrap/factory review remain incomplete. No actual activation bundle or operational seal exists. English/native FTP, rollback and all device gates remain unverified.
Next single package: **RA-003: independently review the frozen 38-source packet, corrected bootstrap and 124-case qualification against the metadata-act draft, then resolve findings; no actual activation or GDT replay before review passes**.


Earlier RA-003: [outer authority and source review](research/GDT_OUTER_AUTHORITY_REVIEW.md), [commands/results](research/sessions/20261019-RA-003-gdt-authority-review.md).
The v2 entry now binds **18 reference hashes**, derived from preserved ordinary authorities. The missing historical qualification-review hash was verified through its already pinned review record. **105/105 invented-data tests passed**, zero skips, exit **0** (81 retained + 24 new). Same-agent source/AST and saved-metadata checks reconciled the nine-role basis, 26 authored roles and 47 cached sources. Independent operational review and actual bootstrap/GDT execution remain pending; English/native FTP and rollback remain unverified.
Next single package: **RA-003: independently review the frozen 38-source packet, corrected bootstrap and 124-case qualification against the metadata-act draft, then resolve findings; no actual activation or GDT replay before review passes**.


Earlier RA-003: [invented bootstrap qualification](research/GDT_BOOTSTRAP_QUALIFICATION.md), [commands/results](research/sessions/20261019-RA-003-gdt-bootstrap-qualification.md).
The ordinary bootstrap now preflights every input path and pinned archival hash **before opening any input document**. The first invented-file qualification exposed two refusal-order failures; both were fixed without changing tests. Final **124/124 passed**, zero skips, exit **0** (105 retained + 19 new). The complete bootstrap ran only with invented temporary documents and a test-only in-memory authority substitution. No actual saved-input activation or protected continuation ran. Independent review, English/native FTP and rollback remain pending.
Next single package: **RA-003: independently review the frozen 38-source packet, corrected bootstrap and 124-case qualification against the metadata-act draft, then resolve findings; no actual activation or GDT replay before review passes**.


Latest RA-003: [source review packet and proposed act](research/GDT_REVIEW_PACKET.md), [commands/results](research/sessions/20261019-RA-003-gdt-review-packet.md).
A private review packet now freezes **38 authored Python sources / 767,313 bytes**, eight review questions and a non-executable draft of the later metadata act. Packet checks verified **279 historical preservation entries** and **143 starting paths**, with all gate/source hashes unchanged. No new synthetic suite or actual observation ran. The prior 124-case result remains historical evidence, not a new pass or execution authority. Independent review remains pending; English/native FTP, exact-body correspondence and rollback remain unverified.
Next single package: **RA-003: independently review the frozen 38-source packet, corrected bootstrap and 124-case qualification against the metadata-act draft, then resolve findings; no actual activation or GDT replay before review passes**.


Historical authorization blocker (superseded by the authorized review round below): [independent-review audit](research/sessions/20261019-RA-003-independent-review-blocker.md).
The source packet and proposed act are ready, but required independent review has not happened. The local-reviewer authorization request is unanswered. This same prerequisite is recorded in three consecutive completed goal turns; the current audit verified all 38 frozen source hashes and found no substantive next step that can bypass the review. The broad pre-camera goal is **blocked, not complete**. No code or tests changed and no camera/protected-input operation ran.
Next single package remains the independent review of the frozen source packet and act draft.


2026-10-19: [Independent source review findings](research/sessions/20261019-RA-003-gdt-independent-review.md). Owner authorization received; three local reviewers returned **five distinct unresolved findings**, covering receipt/stdout encoding, interruption cleanup, root-proposal scope and qualification policy. They reported 17 distinct reviewed paths; all 38 frozen source pins remain unchanged. The unchanged **124/124 synthetic cases pass** (zero skips, exit 0), but miss production boundaries exposed by review. Review acceptance, activation, English/native FTP, recovery and device-write gates remain false. Next single package: **RA-003: preserve frozen sources, repair the five review findings in a new revision, add cross-module invented-data regressions and requalify; then obtain source re-review before any activation.**


2026-10-19: [Isolated review repairs](research/sessions/20261019-RA-003-gdt-review-fixes.md). **Six source findings repaired and accepted by three source-only reviewers; 162/162 synthetic tests pass**, zero skips, exit 0. Original 38 source pins preserved; failed runs retained. Operational cache/reference/role migration and full composition acceptance remain pending. No actual activation, protected-input read or camera command; English/native FTP, recovery and write gates remain false. This supersedes the earlier unresolved-findings status for these scoped repairs only. Next single package: **RA-003: migrate and independently review the ordinary source-cache, role, reference and qualification chain to the repaired revision, with fresh bounded source receipts and invented host/child composition checks; no actual activation or GDT replay.**


2026-10-19: [Successor source preparation](research/sessions/20261019-RA-003-repaired-source-migration.md): fresh **47-source / 813,858-byte** cache and complete rebased binding graph reconciled; **28/28** new synthetic tests pass. Exactly three changed cached sources retain separate scoped repair evidence. Both outer gate/loader enforcement points still need the same validated overlay; no operational activation, camera contact or feature/write gate. Next single package: RA-003: implement one closed repaired-source overlay in both the outer gate and loader, consuming the successor source/role graph; qualify the full invented host/child composition and independently review the migrated chain before selecting any actual act.


2026-10-19: [Shared source overlay](research/sessions/20261019-RA-003-source-overlay.md): gate and loader now use one validated map; **188/188** synthetic tests pass. Source review found and resolved a nested-path incompatibility; scoped source acceptance received from three reviewers. Production callback-factory/native composition and operational acceptance remain pending. No camera contact or feature/write gate. Next single package: RA-003: qualify the authored callback factory and full host/child wiring using invented byte streams and source/dependency adapters, then independently review that composition before preparing a real metadata act.
