# Requested functions: progress and next evidence

Updated: **2026-10-19**. This is the feature-level progress note; the
[backlog](BACKLOG.md) tracks work packages and [STATE](../research/STATE.json)
records machine-readable evidence. An internal copy is kept in ignored
`private/feature-progress.json` and `private/feature-progress.md`.

**None of the requested camera functions has been validated on this body.**
Owner reports α6700 firmware **2.00** and current menu language **简体中文**
(Simplified Chinese), **Chinese mainland version**, and **English unavailable**
(**source-report**, 2026-10-18). The full offered-language list is not supplied;
exact regional SKU and binary identity are unverified. Agent camera access/writes:
none. No device-write gate has passed. Progress below describes
completed preparation separately from actual feature operation.

| Requested function | Owner priority | Current progress | What is still missing | Next feature package |
|---|---|---|---|---|
| **Native English menus** | Primary | Owner reports English absent on mainland version; hypotheses, preservation rules and critical-message plan prepared. No unlock feasibility established. | Rights-cleared matching resources/binaries; distinguish restricted selection from missing resources, with narrow policy/all-consumer evidence. Exact SKU unverified; full list not supplied. | EN-101: restricted-language/resource feasibility after RA-003 |
| **Native camera-to-server Wi-Fi FTP** | Primary | Host queue/protocol foundation tested. Two owner-approved Sony source configs enable FTPGET/FTPPUT; client text is plain FTP. This is a static lead, with final binary/body mapping unproved. | Exact target backend/ABI/applet/invocation/media/network/lifecycle evidence; then one camera-resident manual upload with full server equality. Automatic post-capture transfer is a later, separate step. | FT-101; later FT-103 manual, FT-104 automatic |
| **FL2/FL3 still-photo looks and matching preview** | Deferred | Reference-code/rights audit, synthetic candidate/inverse guards and durable synthetic transaction safeguards prepared. No alpha6700 mapping or candidate exists. | Exact firmware/AP/CP/resource evidence, stock looks/recipes and photo baseline, capacity/dispatch/metadata/preview mapping, conditional recovery. | CL-101/CL-102 when resumed, after target prerequisites |
| **Calibrated custom still-photo looks** | Later, after FL2/FL3 | Separately gated second phase specified. No calibrated fit or target slot is proved. | Stable FL2/FL3 still/preview baseline; explicit DCP/cube/Sony-ST domain; legitimate calibration and holdout inputs; target slot, precision and resource ownership. | CL-107, after CL-105/106 and calibration inputs |
| **Optional HOST-ASSISTED bridge** | Optional, separate result | Architecture and reusable synthetic host-transfer leg prepared. No camera-to-host adapter exists. | Verified model/firmware/SDK capabilities, capture-completion signal, physical-shutter versus remote-trigger behavior, formats/card retention and a separately approved camera leg. | FT-106 only if pursued; does not satisfy native FTP |

Owner priority confirmed on **2026-10-18**: English and native FTP come first.
FL2/FL3 is deferred; custom looks follow FL2/FL3 and their own calibration gate.
The bridge stays optional and separately labelled. A host-generated upload cannot
be recorded as native camera Wi-Fi FTP.

Owner prerequisite (2026-10-18): **verified rollback/recovery before any firmware
write**. It is not established on this body. Backup coverage, two independent
storage copies, an exact inverse and recovery access for the relevant failure
states remain required; synthetic guards are preparation only. See
[recovery/write gate](ACCESS_AND_RECOVERY.md#8-write-gate-checklist).

Earlier RA-003: [GDT dependency integration and complete metadata basis](../research/GDT_RUNTIME_INTEGRATION.md), [commands/results](../research/sessions/20261019-RA-003-gdt-runtime-integration.md).
Dependency/controller composition qualified on **51/51 invented-data tests**, zero skips, exit **0** (**38 core + 13 composition**; **34.711s** suite / **35.305s** wrapper). The complete nine-role saved metadata basis assembled and passed the unchanged pure preflight. Full raw dependency receipts are durably retained before protected continuation, with the guarded dependency session alive through both modeled GDT phases. The new prospective factory received source/AST review only; its CLI remains disabled and the exact outer activation chain is absent. No GDT replay, firmware/constants/prefix read, installed dependency execution or camera contact occurred. English/native FTP, exact-body correspondence, recovery and device-write gates remain unverified.
Historical next single package: **RA-003: complete and independently review the exact outer activation/binding chain for the no-site GDT entry and assembled basis, including fresh ordinary source-cache receipts; no GDT replay until that review passes**.

Earlier RA-003: [dependency-only runtime provenance](../research/DEPENDENCY_RUNTIME_PROVENANCE.md), [commands/results](../research/sessions/20261019-RA-003-dependency-runtime.md).
One independently reviewed dependency-only child completed, exit **0**, **0.344s**. **34/34 probe tests** and **13/13 supervisor tests** passed with zero skips. All **24 public NIST comparisons** passed across twelve cases: ECB/CBC, 128/192/256-bit keys, default and generic requests, fresh encryption and decryption. Eleven exact cached Python origins and five native library load intents/audit events/completions were retained in a durable private raw receipt. This observes host dependency behavior; no firmware/GDT replay, English/FTP feature, recovery or device-write gate passed. English/native FTP remain first.
Historical next single package: **RA-003: integrate the observed dependency origins/startup and durable native receipts into a separately qualified GDT entry and review its exact operational basis; no GDT replay or camera contact**.

Earlier RA-003: [dependency descriptor provenance](../research/DEPENDENCY_DESCRIPTOR_PROVENANCE.md), [commands/results](../research/sessions/20261019-RA-003-dependency-provenance.md).
One independently reviewed descriptor-only dependency audit completed, exit **0**, **3.165s**, after **33/33 invented-file tests passed** (zero skipped, exit **0**, **14.513s** wrapper). The pinned wheel has **352 entries**; **351 installed payload files** match. It also records **4 installation extras** and **56 runtime/startup data files**, including **1 startup file**. The collector did not import the audited package or load its native backend. Native origins/load completion remain unobserved; GDT execution stays unauthorized. No firmware/constants/saved-prefix read, camera contact, feature, recovery or device-write gate. English/native FTP remain first.
Historical next single package: **RA-003: implement, independently review and qualify a dependency-only public-vector runtime provenance probe and the required source fixes for observed origins/startup and durable native receipts; no GDT replay or camera contact**.

Earlier shared RA-003: [non-executable GDT activation preparation](../research/GDT_ACTIVATION_PREPARATION.md), [commands/results](../research/sessions/20261019-RA-003-gdt-activation-review.md).
Closed activation and binding validators qualified on invented records, wheels, file receipts and inert loader models. The 26-role dependency graph is bound to exact cached source bytes. New prospective host/child wiring received source/AST review only. The current preparation, review and seal all prohibit execution. The nine-role object is an opaque reference index; an operational basis remains unassembled. No actual firmware, operational constants, installed dependency or saved raw prefix was opened.

**811/811 synthetic cases passed**, zero skipped, exit **0**; **812.459s** suite / **813.447s** wrapper, CPython 3.13.12. **666 retained + 145 new** cases. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Historical next single package: **RA-003: acquire and independently assess the exact ordinary dependency provenance needed for the frozen GDT observation, then review its activity-specific execution decision; no GDT replay or camera contact**.

Earlier shared RA-003: [primary-GDT I/O adapter design](../research/GDT_IO_ADAPTER_DESIGN.md), [commands/results](../research/sessions/20261019-RA-003-gdt-io-design.md).
Primary-GDT file adapter and exclusive parent/child control qualified on invented ordinary files and inert child processes. Real os.read calls, EOF probes, source accounting, journal failures and bounded supervision are exercised. Actual host/child bindings received source/AST review only; the actual entry remains inactive and blocked pending exact scope/rights activation-semantic review. No actual firmware, operational constants or saved raw prefix was opened.

**666/666 synthetic cases passed**, zero skipped, exit **0**; **800.360s** suite / **801.228s** wrapper, CPython 3.13.12. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Historical next single package: **RA-003: prepare and independently review the one-shot activation seal for the frozen two-phase primary-GDT observation; no execution**.

Earlier shared RA-003: [primary-GDT runner design](../research/GDT_RUNNER_DESIGN.md), [commands/results](../research/sessions/20261019-RA-003-gdt-runner-design.md).
Two-phase primary-GDT runner, full-lineage gate and bounded collector qualified on invented data. Phase A reconciles all five historical blocks before planning; phase B repeats complete lineage before descriptor validation. Root proposals and broad planner success statuses are suppressed from outputs. Source telemetry is a synthetic protocol; the actual-I/O adapter and watchdog remain unimplemented. No actual firmware, constants or saved raw prefix was opened.

**547/547 synthetic cases passed**, zero skipped, exit **0**; **280.109s** suite / **280.948s** wrapper, CPython 3.13.12. Three historical cases were excluded before execution: two require crypto and one loads saved actual metadata. No target feature, recovery or device-write gate passed.

Historical next single package: **RA-003: implement and synthetically qualify a separately reviewed actual-I/O adapter and exclusive entry for the two-phase GDT scope, including source telemetry and watchdog; no actual execution**.

Earlier shared RA-003: [primary-GDT metadata scope](../research/GDT_METADATA_SCOPE.md), [commands/results](../research/sessions/20261019-RA-003-gdt-scope.md).
Primary-GDT observation engineering scope frozen: two planned inspection calls, four complete source passes (4,096,071,392 bytes on success), nine metadata roles, and at most 65,536 new descriptor bytes retained. Phase-A raw prefixes must be cleared before phase B; selected-raw allowances are 73,728 / 139,264 bytes, not process-memory caps. Root proposals are suppressed from every output and cannot reach a reader. Current official legal sources retain a narrow research rationale with unresolved contract/constants questions. No actual replay or planner application to saved actual data occurred.

Unchanged planner/observer baseline: **174/174 passed**, zero skipped, exit **0**, **0.163s**; all eight qualified source and 34 original pins unchanged. The new two-phase runner is not implemented or qualified.

Historical next single package: **RA-003: implement and synthetically qualify the frozen two-phase primary-GDT metadata runner and reconciliation gate; no actual replay or inode/content traversal**.

Earlier shared RA-003: [ext metadata planner design](../research/EXT_METADATA_PLANNER_DESIGN.md).
Bounded ext metadata planner design: **174/174 synthetic passes**, zero skipped, exit **0**, **0.154s**; **52 retained + 122 new** cases; **8** qualified source/test pins. Invented buffers exercise primary-GDT and root-record proposals with counter, inode and group/reserved-metadata placement checks. All **13** retained ordinary source pins, prior actual results, analysis acts and source lock remain unchanged; no new source acquisition or historical full-suite rerun.

Limits: **1,024 groups**, **32,768 descriptor bytes**, **4,096 prefix bytes** (project budgets). No actual metadata/firmware application, traversal, raw output or camera; planning authorization and all filesystem/content, native English/FTP, recovery and device-write claims remain false.

Historical next shared package: **RA-003: review and freeze the rights, lineage and byte limits for a bounded primary-GDT descriptor-metadata observation using the qualified planner; no inode/content traversal**.

## Verified preparation supporting these functions

- RA-001: host baseline/private intake prepared. Model/version/current-language
  facts were subsequently supplied; remaining setup facts stay Unknown.
  [Initial report](../research/sessions/20261018-RA-001.md),
  [owner intake update](../research/sessions/20261018-owner-ui-intake.md).
- RA-002: references pinned and static provenance/rights audit recorded;
  reuse/target limitations remain. [Audit](../research/REFERENCE_AUDIT.md).
- Inventory/probe and synthetic patch/transaction models exist, with no eligible
  device profile or executor. [Coverage](../research/PRE_CAMERA_READINESS.md).
- Final-code clean reproduction at `fb32370052a0ffe5d8a529edba971f962ce57654`:
  **154 total / 152 passed / two skipped**, exit 0, CPython 3.13.12 on the owner
  Windows host, NEW 63-file export and no-pip environment. Actual hard-link
  refusal passed; local POSIX fork and actual symlink creation were unavailable.
- Observed four-job Windows/Linux CI on Python 3.10/3.13: **154 total / 153
  passed / one platform skip per job**, all exit 0. Ubuntu ran POSIX inherited-lock
  and actual symlink refusal; hosted Windows ran actual symlink refusal.
  [Exact clean-run/CI/publication evidence](../research/sessions/20261018-IN-102-final.md).
  The older 58-file / 129-pass reproduction remains historical.
- Constrained loopback lab: **19 cases passed**, including 100 synthetic files
  in 50 groups; all 21 lab servers stopped. This proves only the documented host
  cases. [Exact commands/results](../research/sessions/20261018-FT-102-loopback.md).
- [Official Sony refresh](../research/OFFICIAL_SOURCE_REFRESH.md), **source-report**:
  public firmware catalogue/release notes and model-specific Language/menu/PC
  Remote pages inspected. This does not identify installed firmware, establish
  regional English availability or prove a native FTP backend. Creators' Cloud
  and a host-assisted PC Remote path do not establish arbitrary native FTP.
- [RA-003 provenance/rights review](../research/OFFICIAL_PACKAGE_INTAKE.md):
  official 2.00 package metadata recorded; one GET stopped with zero firmware
  bytes. Owner firmware inspection permission is **No / unknown**. Sony's
  separate source-offer list includes two BusyBox archives, explicitly approved
  by the owner and audited privately for licences/config/spec/client text.
  Supplied FTPGET/FTPPUT flags and spec file lists are leads; final binaries,
  body applicability, native invocation and FTPS remain unverified.

- Earlier mainland source/terms snapshot: [official mainland source and actual download terms](../research/MAINLAND_FIRMWARE_SOURCE.md)
  identified; published asset reference is provenance only. No firmware request,
  agreement acceptance or permission inquiry. Component rights, owner consent
  and the basis for proprietary unpacking/disassembly remain distinct.

- Earlier China-scope snapshot: [China scope and limited acquisition consent/results](../research/sessions/20261018-RA-003-cn-scope.md).
  Both public and private notes retain the owner's China/personal/noncommercial
  facts, bounded acquisition result and pending activity-specific analysis basis.
  These do not establish English resources or a native FTP implementation.

- Earlier RA-003: [package acquisition and express statutory research route](../research/sessions/20261018-RA-003-package-law.md).
  Separately consented HTTP 200 acquired the declared size with matching hashes;
  bounded identification found a UFU signature candidate only. No English
  resources or native FTP backend have been extracted or validated. Full proposed
  analysis scope and exact-body correspondence remain unresolved.

- Earlier RA-003: [scoped UFU directory/parser audit](../research/UFU_CONTAINER_AUDIT.md).
  The authored reader reports DATV, PROV, UDID, FDAT and DEND, with one bounded
  FDAT span. Full-suite local result: 176 passed, three skipped, exit 0.
  This is container-directory progress only; no English resources, FTP program,
  component semantics or exact-body correspondence are established.

- Earlier RA-003: [FDAT identification/extractor audit](../research/FDAT_EXTRACTOR_AUDIT.md).
  The 4,096-byte in-memory prefix is unknown/unsupported_opaque; no encryption or
  feature inference follows. Candidate source is pinned, not run. Full suite:
  195 passed, three skipped, exit 0. English resources and native FTP remain
  unextracted/unvalidated; both remain primary.

- Earlier RA-003: [bounded decoding plan](../research/FDAT_DECODING_PLAN.md).
  Narrow statutory rationale and synthetic decoded-header/extent validation are
  documented; no real decoding or resource/backend mapping. Full suite: 225 passed,
  three skipped, exit 0. Exact variant/dependency/constants provenance is next.

- Earlier RA-003: [crypto/provenance audit](../research/FDAT_CRYPTO_PROVENANCE.md).
  Pinned private AES runtime and public constants source; eight primitive tests
  passed. That session did not perform a real header trial or feature mapping.

- Earlier RA-003: [bounded private header trial](../research/FDAT_HEADER_TRIAL.md).
  One predeclared hypothesis passed envelope/header checks after 45 synthetic
  cases. That session did not measure full-stream length or validate component bounds.

- Earlier RA-003: [stream validation](../research/FDAT_STREAM_VALIDATION.md).
  All physical envelopes/terminal positions checked; logical length/SHA measured
  and declared bounds/non-overlap checked against measured EOF. No component
  formats, English/FTP mechanism or body correspondence established.

- Earlier RA-003: [component prefixes](../research/COMPONENT_PREFIX_AUDIT.md).
  Bounded SquashFS v4/ustar header candidates, with lineage and metadata only.
  No complete component format or English/FTP finding follows.

- Earlier RA-003: [tar-directory trial](../research/TAR_DIRECTORY_AUDIT.md).
  No directory accepted; the later bounded diagnostic identifies the refusing field/predicate.

The [completion audit](../research/PRE_CAMERA_AUDIT.md) accounts for all 27
packages and validation families. Next single host package: **RA-003: design and synthetically qualify a bounded ext-family superblock capability and geometry gate using pinned authoritative format sources; no actual replay or directory traversal**.
Ordinary acquisition and bounded signature evidence are recorded separately;
source/binary correspondence and exact-body identity remain unresolved. EN-101 uses
the owner-reported English absence to pursue restricted-language/resource
feasibility; a full-list transcription is no longer the immediate blocker.
See [latest intake](../research/sessions/20261018-owner-mainland-english.md).
Earlier Unknown responses are preserved as history. Host qualification and this intake
update do not validate any of the five camera functions above.

## Keeping the notes current

At session start, read this page, STATE and the internal feature note when it
exists. Whenever feature evidence, a blocker or a next step changes, update the
matching STATE feature entry, this page and the private note together, with a
dated session/evidence link. Record regressions and negative results too.
Use descriptive statuses rather than invented completion percentages. Promote
a function to validated only when its complete target acceptance evidence exists.
Keep serials, private paths, credentials, photos and raw observations in the
private note/journal; publish only sanitized summaries.

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


2026-10-19 public-source lead: [a6700 Powerful audit](../research/sessions/20261019-RA-003-a6700-powerful-audit.md). Pinned `0c6294a83988f196adfc980de59f9a1d0b92e8e2`: author reports FTP RAW+JPEG physical success on a6700 2.00; implementation is not published in the inspected tree. No English unlock found; full restoration remains unverified. Reference only, no payload adoption or device action. Next single package: RA-003: independently review the frozen 38-source GDT gate packet and 124-case qualification under the owner-authorized local source-only review boundary; resolve findings before any activation.


2026-10-19: [Independent source review findings](../research/sessions/20261019-RA-003-gdt-independent-review.md). Owner authorization received; three local reviewers returned **five distinct unresolved findings**, covering receipt/stdout encoding, interruption cleanup, root-proposal scope and qualification policy. They reported 17 distinct reviewed paths; all 38 frozen source pins remain unchanged. The unchanged **124/124 synthetic cases pass** (zero skips, exit 0), but miss production boundaries exposed by review. Review acceptance, activation, English/native FTP, recovery and device-write gates remain false. Next single package: **RA-003: preserve frozen sources, repair the five review findings in a new revision, add cross-module invented-data regressions and requalify; then obtain source re-review before any activation.**


2026-10-19: [Isolated review repairs](../research/sessions/20261019-RA-003-gdt-review-fixes.md). **Six source findings repaired and accepted by three source-only reviewers; 162/162 synthetic tests pass**, zero skips, exit 0. Original 38 source pins preserved; failed runs retained. Operational cache/reference/role migration and full composition acceptance remain pending. No actual activation, protected-input read or camera command; English/native FTP, recovery and write gates remain false. This supersedes the earlier unresolved-findings status for these scoped repairs only. Next single package: **RA-003: migrate and independently review the ordinary source-cache, role, reference and qualification chain to the repaired revision, with fresh bounded source receipts and invented host/child composition checks; no actual activation or GDT replay.**


2026-10-19: [Successor source preparation](../research/sessions/20261019-RA-003-repaired-source-migration.md): fresh **47-source / 813,858-byte** cache and complete rebased binding graph reconciled; **28/28** new synthetic tests pass. Exactly three changed cached sources retain separate scoped repair evidence. Both outer gate/loader enforcement points still need the same validated overlay; no operational activation, camera contact or feature/write gate. Next single package: RA-003: implement one closed repaired-source overlay in both the outer gate and loader, consuming the successor source/role graph; qualify the full invented host/child composition and independently review the migrated chain before selecting any actual act.
