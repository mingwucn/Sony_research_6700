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

Continuation (2026-10-18): IN PROGRESS, target acquisition BLOCKED. [Artifact intake](ARTIFACT_INTAKE.md) records a same-read bounded header probe, lineage template and static review of the pinned PMCA DAT locator. No exact-target package was supplied or selected; unknown installed firmware blocks matching-package acquisition/extraction. Synthetic format recognition does not close RA-003.

### RA-004 — Establish identity and review an access route

Depends on RA-001/002. Risk: R0 proposal, then separately approved R1; R2 remains a distinct decision. Obtain normal UI facts and, after approval, ordinary host USB descriptors. Identify a candidate service path from reviewed exact-target evidence. Describe every command's effects, re-enumeration, helper ABI, expected result, timeout and reconciliation procedure. Write transport mocks for known readiness/error cases.

Deliver: device-facts and access-proposal, including what is not supported. Accept when identity is consistent and the owner can approve or decline a bounded next action. Standard USB recognition does not authorize service authentication. A blocked service path leaves RA-003 and offline analysis available.

Continuation: R0 [observation/access preparation](../research/TARGET_EVIDENCE_GAPS.md) written. Identity and an applicable command-level route are absent; RA-004 acceptance remains BLOCKED. No observation, USB command or device approval occurred.

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

Continuation: [synthetic candidate guards and transaction simulator](OFFLINE_GUARDS.md) implemented with 36 focused passing tests. Generic OFF-01..07/09/12/13 subcases are covered; target OFF-08/10/11, durable device journal/process exclusion and real-target review remain absent. RA-007 is PARTIAL, synthetic-only and always device-ineligible.

## English track

### EN-101 — Resolve language/resources and the no-change option

Depends on RA-001 and RA-003/005 for binary analysis. Risk: R0; approved ordinary UI observation is R1. Verify whether English is already offered. If absent, map locale resources, selector construction, current/default values and all consumers of a candidate restriction field. Distinguish language-specific policy from global product/region identity.

Deliver: language feasibility record and critical-resource coverage table. Accept when a narrow hypothesis and falsifying evidence are identified, or normal menu selection resolves the request. Stop before mutation if English resources are incomplete or a shared region field is unexplained.

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

Continuation: [durable mock queue/protocol foundation](FTP_HOST_PROTOCOL.md) implemented and host-tested with synthetic spool files, 100 objects/50 pairs, hash reconciliation and persistence failures. This is PARTIAL FT-102: no server/socket/TLS handshake/client or native constraint qualification exists. Real isolated-server capability/failure testing is the next independent host package.

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

Continuation: Windows inventory false refusals repaired with same-API mutation checks retained; real symlink fixture still unavailable. [CI/host policy](HOST_VALIDATION.md) and pinned Windows/Linux matrix prepared. Local results do not prove remote CI; IN-102 remains PARTIAL with remote runs NOT RUN and rights limits retained.

### IN-103 — Soak, inverse and release qualification

Depends on IN-101/102 and relevant hardware results. Risk: approved physical use and reviewed inverses only. Execute the expanded restart/preview/queue/load targets in VALIDATION, record failures, test supported uninstall paths and document the conditional recovery envelope. Seek independent eligible-body reproduction before broad compatibility claims.

Deliver: exact support matrix, known limitations, user procedure, repair-risk disclosure and release decision. Accept only within tested firmware/body/mode scope. Official firmware updates and new regional variants are new targets, not automatically supported transitions.

## Work sequencing and closure

RA-001 and RA-002 completed their stated offline scopes. The owner's broader pre-camera request permits independent generic RA-003/007, FT-102 and IN-102 preparation; [coverage](../research/PRE_CAMERA_READINESS.md) records all package boundaries. The next single available host package is FT-102 isolated-server capability/failure testing; target-specific RA-003 retrieval still requires installed firmware. EN-101/CL-102/FT-101 share acquired evidence but remain separate dossiers. The preferred first hardware feature is the smallest fully proved reversible change, often a language setting when that hypothesis is established; priority is not a prediction that it will be easy.

Do not close a package because its document exists. Close it when its stated evidence is present, or explicitly resolve it as blocked/superseded with the reason and next action. Optional bridge/custom-look work must not hide missing primary requirements. Update STATE and the session report after every local work package.
