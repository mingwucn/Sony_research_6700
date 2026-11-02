# Sony ILCE-6700 CN1 Ver. 2.00 — Full Native FTP Enablement Plan

**Date:** 2026-11-02  
**Audience:** local Codex implementer, repository maintainer, and camera owner  
**Research mode for this plan:** R0 source review and documentation only. No camera, FTP server, driver, or firmware was touched.  
**Target baseline:** `mingwucn/Sony_research_6700` `main` @ `55054b91319393c598246c2e8302f84c0f74eab0`.  
**Reference upstream:** `xyzhangxin/sony-a6700-powerful` @ `d5bb9485dfe7cc4bf13a4ead3a7437c2f40240a9`.  
**Known defect:** issue #1, and draft PR #2 (must be reconciled with newer `main`; do not merge stale implementation unreviewed).

## 0. Executive decision and evidence discipline

Goal: a **camera-resident outbound FTP client** that can upload photographs from the α6700 over Wi-Fi to an owner-controlled server, **without a relay computer/phone**. First achieve manual upload, then automatic transfer, batch operation, reliability, and security. Do not implement an FTP *server* on the camera. Do not equate an English menu, visible network configuration, an installed byte, a successful readback, or an offline unit test with FTP functioning.

**Current owner hardware observations (issue #1, 2026-11-02):** native English selection works; `Network → FTP Transfer` can be opened; the desired Playback/Gallery FTP controls remain unavailable. A successful camera-to-server file receipt is **not established** on this camera. The exact missing entry/disabled state is not yet discriminated. Labels: `physical-tested` for the menu observation, `unverified` for playback and actual upload.

**Source-supported upstream baseline:** `xyzhangxin/sony-a6700-powerful` reports camera-tested native FTP, including RAW+JPEG, but does not claim validation of every Playback filter, persisted cross-power-cycle queue, or every camera body. Upstream's published profile describes **242 FTP fields**: **90 App + 152 WBI**, of which **89 App + 151 WBI bytes change**, distributed across **82 sectors** in its implementation. This is *source-report* evidence for a specific build/profile, not approval to write those fields on this body. The upstream's 81 application-side menu records match the 81 offsets in our newest `targets.py`; they are **FTP menu hierarchy permission records**, not independently proven Gallery-specific records. One parent `0x262` field has enabled value equal to stock `00` and must not be counted as a changed byte. FTP has no CP patch in the upstream feature catalog.

**Our current `main`:** 9 Network FTP flags + 81 FTP menu permissions (80 changed bytes) + 1 candidate playback `0x0817` action byte, plus one English-language 4-byte target. Thus **92 targets / 94 logical changed bytes** total; the current writer models **7 non-atomic spans / 236,018 physical bytes** for both features. These figures describe candidate storage changes, not functioning FTP. Our customizer does **not** currently implement WBI edits. `v1.0.0`'s original tag predates the 81-permission implementation; the release asset was also reportedly replaced after the tag, so do not assume a downloaded ZIP corresponds to current `main`.

**High-priority discrepancy:** issue #1 contains the owner's directly reported neighboring records in `appFw.so`:
- `0x03F17CD8: 16 08 00 00 | 00 00 00 00`, action `0x0816` (`DISPLAY_FTP_ERROR_INFO`).
- `0x03F17CE0: 17 08 00 00 | 00 00 00 00`, action `0x0817` (`FTP_TRANSFER`).
- `0x03F17CE8: 18 08 00 00 | 00 00 00 00`, action `0x0818` (`FTP_FUNCTION`).

These records support the **candidate identity** of `0x0817` at `0x03F17CE0` and place its status field at `+4`, but do not establish a working patch. An older report says its last four bytes are `00 01 01 01` rather than `00 00 00 00`. Resolve the discrepant bytes from stock/current actual build before any write. The old equation `0x03F14C38 + 0x0817 * 8 = 0x03F17CE0` is false: zero-based arithmetic gives `0x03F18CF0`. A dense table with nonzero base `0x0202` would be consistent with the observed record location; a sparse lookup is another hypothesis. Trace the resolver and the meaning of **all four** status bytes; do not assume `0x0818` should be patched.

**Cross-body limitation:** the `wanghm105/Powerful6700-Windows` repository documents another α6700 that uploads one photograph and then stalls, with a possible relation to `SONY/FTPNSEND.DAT` and native FTP transfer state. It is a separate device report. Its explanation about state persistence is **inference**, not runtime proof; no such defect has been demonstrated on this owner's body.

**Safety policy:** follow `AGENTS.md`, `docs/ACCESS_AND_RECOVERY.md`, and the owner hold recorded in the research history. R0 source work is permitted. Actual R1/R2 camera inspection and R4 App/WBI persistent writing require **separate explicit owner approval** for the exact action. Repo/PR permissions do **not** grant device-write permission. Do not intentionally disrupt power during a live write, bypass model/SKU checks, blindly delete a WBI, edit CP or radio-calibration data, cross-flash another model, or assert that service-mode recovery is guaranteed.

## 1. Precise product definition and P0/P1/P2 scope

| Capability | Acceptance criterion | Tier |
|---|---|---|
| Network settings | Menu visible; `FTP Function` can be turned on/off; selected server/Wi-Fi settings are retained and usable | P0 |
| Connection | Owner-controlled server is contacted by the **camera**, with no host uploader or USB relay | P0 |
| Single-image upload | A normally displayed, database-registered photograph is uploaded from Playback via a supported custom key/action; received bytes hash-match | P0 |
| Batch transfer | Select a set of images via the native Network FTP transfer UI; expected files arrive exactly according to documented selection semantics | P0 |
| Automatic upload | After capture finishes, configured JPEG/RAW (and RAW+JPEG where native options permit) transfer proceeds without a host relay | P0 |
| Status/error | Correct connected/transferring/completed/failed indication, and comprehensible diagnosis of failed authentication/connection | P1 |
| Multiple sequential files | Second and subsequent files upload without a stuck state; queue and cancel semantics are characterized | P1 |
| Reconnect | Wi-Fi/server loss followed by recovery does not lead to a permanent disabled FTP switch; pending transfers are reconciled | P1 |
| Shutdown/persistence | Normal restart preserves settings and defined queue behaviour; no crash or unexplained power-cycle dependency | P1 |
| Power/capture isolation | Network work does not prevent safe still capture, card use, orderly power-off, or normal standby | P1 |
| Advanced filters | Date/folder/rating/protected/untransferred/failed filters only where the α6700 backend/menu demonstrably supports them | P2 |
| Movie transfer and advanced modes | Add only after corresponding native menu/backend support and separate compatibility proof | P2 |
| Secure transfer | Confirm whether this **firmware** implements explicit FTPES/FTPS, and if so test certificate/hostname validation; SFTP is a different feature, not implied | P2 |

**Do not invent a separate top-level Gallery FTP configuration page.** Sony's A7CR references distinguish `Network → FTP Transfer → FTP Transfer Func.` for batch/configuration from a **playback custom key** for one image. Determine the actual α6700 menu layout by runtime observations; `Playback → Select to Transfer` in our current README is a **candidate claim**, not an acceptance criterion. The more recent A7V playback Fn menu must not be presumed to exist on the α6700.

## 2. Gates and stop conditions

| Gate | Prerequisite | Required evidence/output | Blocking failure |
|---|---|---|---|
| G0 — Source provenance | R0 only | Latest Git tree, pins, exact files, license review, code/test inventory | Unknown upstream build/provenance |
| G1 — Failure classification | UI observation; separately authorized transport read if needed | Exact menu path, hidden/greyed/error state, camera version, byte-state classification | Missing or contradictory state / `MISMATCH` |
| G2 — Identity and recovery | Separate approval before any nonordinary access | Target build identity, original+current states, protected-region guards, viable conditional recovery | No credible inverse, inaccessible WBI/firmware, unknown write scope |
| G3 — Root-cause linkage | Offline disassembly + fixtures | Action resolver, parent/leaf menu tree, WBI load state, FTP worker dispatch and falsifiable gating hypotheses | Claim rests only on string/offset proximity |
| G4 — Safe candidate | Offline-only first | Reproducible exact known-preimage plan, zero writes for any unknown value, full-span mock readback/recovery | Unsafe partial transaction or missing private snapshot |
| G5 — Owner-approved experiment | Independent explicit R4 approval and all earlier gates | Fresh preflight, limited candidate, durable journal, full readback, normal boot, observed menu | Any uncertainty/unknown results: stop; `NEEDS_REVIEW` |
| G6 — Operational acceptance | Camera + isolated owner-controlled FTP server | Repeated file receipts, hashes, error/retry/power tests | One-photo stall, missing menu, lost/unexpected files, unsafe state |

No G5 experiment may be initiated merely because this plan, a PR, or a successful test suite exists. Scope individual device requests by actual command and side effects. Step-4 service inspection is **read-only for target patch fields**, but service authentication/native helper execution is **R2**, not risk-free R1.

## 3. WP0 — Baseline and PR reconciliation (R0; start here)

**Input:** `main` at `55054b9`, issue #1 and its owner-correction comment, draft PR #2, ``README.md`, ``docs/FTP.md`, ``docs/TECHNICAL_ARCHITECTURE.md`, ``docs/USER_GUIDE_CN.md`, `docs/TRANSACTION_RECOVERY_AND_GUI_REDESIGN.md`, and ``apps/a6700_customizer/{targets,app_backend,app_gui,recovery_journal}.py`.

1. Freeze exact `main` and draft PR #2 heads; inspect the PR diff relative to current `main`. PR #2 was prepared for an **older ten-FTP-byte target set**. Rebase/cherry-pick only semantically valid changes onto the **current 92-target/seven-span code**. Never overwrite the current journal/reconciliation implementation with old per-byte writer logic.
2. Label `EN-101` English as owner-observed working, but `FT-101` as **network menu observed / playback unavailable / transfer unverified**.
3. Correct `README` and GUI wording (no “complete FTP”, “Gallery solved”, “100% restore”, “instant upload”). Rename `TARGET_FTP_GALLERY_MENUS` toward `TARGET_FTP_MENU_PERMISSIONS` unless source evidence demonstrates a Gallery-only dependency.
4. Record the misleading Network flag IDs in the README: upstream's actual sparse IDs at those offsets are `0x5a5, 0x5a6, 0x5a8, 0x5aa, 0x5ac, 0x5ad, 0x5ae, 0x5af, 0x5b0`, not a contiguous `0x5a5..0x5b0` series. No fabricated `0x5a7/0x5a9/0x5ab` entries.
5. Confirm `tools/patch_spec.py` and `research/plans/{forward_patch_plan,rollback_restore_plan}.json` are historically scoped and cannot be marketed as a complete full-FTP patch plan.
6. Add an evidence ledger with labels `source-report`, `static-inference`, `offline-tested`, `device-readback`, `runtime-observed`, `physical-tested`. No claim should advance without its corresponding receipt.

**Deliverable:** source/claim audit, reviewed status-only PR, updated issue #1 with sanitized findings; **no device action**.

## 4. WP1 — Canonical upstream FTP manifest comparison (R0)

**Pin:** `xyzhangxin/sony-a6700-powerful` @ `d5bb9485dfe7cc4bf13a4ead3a7437c2f40240a9`. Use its `应用/src/a6700_unlock/data/a6700-2.00.json` and rendered `应用/docs/FEATURES.md` only as pinned input. Review licensing before any code reuse; prefer independent parsers over vendoring the upstream runtime.

Create `tools/compare_ftp_manifests.py` and `tests/test_ftp_manifest_comparison.py`.

For every `feature=ftp` record, retain: stable field ID, image view (`app` or `wbi`), logical offset and address domain, expected stock/target, acceptable historical intermediates, source provenance and required structural guard. Verify:
- 242 total FTP fields = 90 application + 152 WBI.
- 240 changed bytes = 89 App + 151 WBI, with unchanged legacy `0x262` fields excluded from changed-byte metrics.
- All 81 new application permission offsets from our current implementation match upstream App offsets; nine Network parameter flag offsets match as well.
- `0x03F17CE4` is **our separate unverified playback action candidate**, **not** an upstream FTP catalog field.
- No two fields overlap incompatibly; no out-of-range offsets; no field uses an offset from the wrong image view; duplicate catalog IDs and unexpected stock values fail closed.
- An alternative build, unknown values, incomplete WBI, or a changed upstream hash produce a diagnostic/block, not an automatically widened patch.

Generate a **sanitized summary**, not a firmware image or private snapshot. Preserve distinct identity claims for the stock `appFw.so` size `89,027,992` / SHA-256 `e65fd595052be5d0e98ce8000dfcb94f90a2f8309de70ef140375052009b0ef3` and upstream's normalized WBI image identity. Normalized SHA values are **offline profile assumptions**, not proof of active runtime state or an exact current-body full-file hash.

**Deliverable:** machine-readable comparison + generated table + regression tests. **Gate:** deterministic totals and exact view separation.

## 5. WP2 — Determine whether WBI is the missing activation layer (R0 first)

**Question:** Does the live camera load menu/model capability state from an extracted WBI image that does not reflect edits applied only to `appFw.so`? This is a **hypothesis**, not yet established.

Workstream A, purely offline:
1. Distinguish four domains: (i) stock/current `appFw.so` bytes, (ii) decoded/extracted logical WBI2 bytes, (iii) any encrypted/raw WBI storage, and (iv) active runtime menu/feature state. An offset into (ii) is not a write address into (iii).
2. Compare upstream App parent/child/leaf permission records with its WBI counterparts and any model-gating counters/guards. Include `0x226`, `0x262` and candidate `0x0817`/`0x0818` context. Explain exactly which fields are persistent snapshots versus boot-produced derived state; do not assume all WBI edits are necessary after a genuinely cold boot.
3. Examine the firmware's WBI generation, load, validity/invalidation and boot selection sequence. Trace the actual a6700 logic; an A7CR `wbi4` workaround is **not transferable** on the strength of model-family similarity.
4. Evaluate a **non-writing** experiment that observes current App and WBI states after a normal shutdown/restart (individually approved R2 if service mode is involved). Record whether App and WBI disagree and whether observed menu state follows one view.
5. Define two competing hypotheses: **H-WBI-1**: stale WBI shadows already installed App menu permissions; **H-WBI-0**: App-only modifications are active and another gate is missing. Specify observations that falsify either.
6. If direct WBI editing or invalidation is indicated, write a separate **R4 operation design**, with exact current-body material, read/modify/write unit, guard bytes, independent backups, loader/boot implications, verify/restore procedures, and a recovery envelope. **Do not implement or run it until the write gate passes**.

**Suggested outputs:** `research/FTP_WBI_ACTIVATION_MAP.md`, `tools/inspect_ftp_wbi_offline.py`, synthetic fixtures and test cases. No private WBI images in Git.

## 6. WP3 — Resolve playback Action 0x0817 and registration path (R0)

The critical physical defect reported by the owner is missing/disabled playback FTP capability. Test that separately from network connectivity.

1. Read the exact **24-byte neighboring action records** `0x03F17CD8..0x03F17CEF` from the correct local stock/current App image. Document precise preimage, modified values and surrounding bytes; resolve the contradictory `00 01 01 01` vs `00 00 00 00` status. Only redacted result summaries enter Git.
2. Reverse-trace the actual action lookup implementation, e.g. code at proposed resolver `0x01440d0c`; prove whether the record array uses direct ID lookup, offset/stride, nonzero-based dense indexing, sorted/binary search, or a separate map. Correct the arithmetic and test that action IDs `0x0816`, `0x0817`, `0x0818` resolve to the observed records.
3. Trace `0x0817` from UI label Resource ID `0x021c668e`, binding table `0x03666b70` and per-mode custom-key configuration into the FTP transfer worker. Establish the actual **4-byte status field semantics**, which permission predicate(s) are evaluated, and whether the UI requires a parent category, active FTP switch, a connected server, particular playback mode, or a target image.
4. Inspect `0x0818` (`FTP_FUNCTION`) and `0x0816` (`DISPLAY_FTP_ERROR_INFO`) as contextual **diagnostics**. Do not set their bytes to 1 by guessing.
5. Separate three claims: (a) an option appears in `PB Custom Key Setting`, (b) the chosen key can be assigned/persisted, (c) pressing it initiates a real file transfer. All three require independent evidence.
6. Verify the available Sony cross-model menu patterns only as reference behaviour; do **not** copy A7CR/A7CII/A7IV offsets or assert that `Playback → Select to Transfer` must exist.

**Deliverables:** `research/FTP_ACTION_0817_RESOLVER.md`; testable call graph; disassembly excerpts; specific additional gates only if proved, with falsifiers.

## 7. WP4 — Trace the native FTP engine, completion and queue (R0 then approved observation)

Before adding a new client, inspect whether the target already provides usable paths for server configuration, Wi-Fi, capture completion, selected-file enumeration, upload, status reporting and cleanup. Upstream reports a working native engine; another A6700 repository reports a second-photo stall.

Candidate anchors to validate in the *correct* local image:
- `mpr::file::TransferStillFile`; `model::sequence_ftp_transfer` and its event transitions.
- `start_ftp_transfer`, `resume_ftp_transfer`, `FTP_TRANSFER_CMP`/stop/cancel/reconnect events.
- `PRM_setting_ftp_function`, `ftp_function_internal_state`, `is_ftp_func_temporary_off`, `ftp_transfer_list_add_state` and relevant network/error variables.
- The media-side queue path `SONY/FTPNSEND.DAT`, if present; determine read/write/restore semantics and ensure existing card data are never changed by diagnostics.
- Settings persistence (Wi-Fi, FTP credentials, transfer preferences) distinguished from menu model flags, WBI snapshots and file queue state.

Produce a **transfer-state diagram** showing `DISABLED → CONFIGURED → CONNECTING → IDLE → QUEUED → SENDING → COMPLETE/FAILED → IDLE`, plus `CANCELING`, `RECONNECTING` and `SHUTDOWN` paths. Every edge must be annotated as observed, statically inferred, or unknown. Especially prove second-transfer dispatch and whether cancellation removes/changes the action's availability.

If another camera stalls after one transfer, its GitHub report is a **test inspiration**, not proof that any particular on-card file, flashed Backup state, or runtime counter is the cause. Never automatically remove `FTPNSEND.DAT` as a "fix" or tamper with a user's card.

**Deliverables:** `research/FTP_ENGINE_AND_QUEUE_MAP.md`, redacted event taxonomy, minimal external-server test harness plan.

## 8. WP5 — Implement a fail-closed installation planner and conditional App/WBI writer

Only after WP1–WP4 provide exact candidate semantics, introduce code changes on a small reviewed topic PR. Do not add all 152 WBI fields as an unverified blanket modification.

**Proposed repository touchpoints:**
- `apps/a6700_customizer/targets.py`: separate verified upstream-aligned App flags, menu permissions, experimentally confirmed playback action(s), and **future WBI targets in their own address domain**; retain precise known-state invariants.
- `apps/a6700_customizer/app_backend.py`: preflight all selected storage objects and supported build identity before **any** mutating command; independent guarded transitions and per-object postread; no assumed "stock" for unknown bytes.
- `apps/a6700_customizer/recovery_journal.py`: append-only durable intent/expected/observed states with SHA-256 and raw private before/after units; extension to WBI only after its physical semantics are proved.
- `apps/a6700_customizer/app_gui.py`: show distinct `Network flags / FTP menu permissions / Playback action / WBI snapshot (if known)` state and **actual functional acceptance status**, plus explicit `BLOCKED/UNKNOWN/NEEDS_REVIEW`.
- `tools/patch_spec.py`, `tools/verify_target_sectors.py` and generated plans: regenerate from exact current profile, while retaining a clear historical scope for existing two-target plans.
- ``tests/test_customizer_targets.py`, ``tests/test_customizer_recovery.py`, ``tests/test_recovery_journal.py` and new FTP manifest/action/WBI/state-machine tests.

**Required executor invariants:**
1. Target body, firmware and profile must be established by more than file size; verify all critical known windows and a justified normalized file identity where possible.
2. **Preflight all spans/objects before first write.** A bad field in the last span yields **zero writes** across the entire operation.
3. Known `STOCK` ↔ `PATCHED` transitions only; unknown/mixed/corrupt states fail closed; read/modify/write preserves every unowned byte. An invariant `00→00` is an assertion, not an edit.
4. Before writing, save original **raw full-span** buffers, exact metadata, hashes and intent to durable host storage. Make two independent acquisitions where possible, and preserve both the original stock and current owner-modified good state; a JSON list of changed offsets is not a full image backup.
5. Multiple spans/partitions are **not atomic**. Journal each completion separately, read back entire span, and on timeout/disconnect enter `NEEDS_REVIEW`. Never resend, auto-reboot, auto-revert, or retry an ambiguous mutating command.
6. After disconnection, perform separately authorized **independent reconciliation**, classifying all observed spans as original/target/partial/unknown before any human-approved continuation.
7. Recovery requires the service path to remain accessible. A GUI `restore` button is **not** an unconditional rescue for a bootloop, corrupted WBI, USB failure, or missing firmware object.
8. Do not silently reset English settings, region/radio identifiers, server passwords, card database or user preference state.
9. A "zero-change write probe" can still physically write and therefore has its own risk; do not describe it as a read-only verification operation.
10. Remove/disable experimental write controls for candidates not yet approved or whose preimages are contradictory; never include such fields in "select all".

**Tests:** offline failure injection for all boundaries, wrong target, unknown latest field, preimage drift, short read, overlapping targets, stale profile, WBI view confusion, corrupt journal, missing snapshot, partial span, unplug/timeout/unknown completion, blocked double-session, full-span preserved-byte corruption, resume/rollback under an already reconciled state, and manifest/GUI count agreement. Preserve the current 106-case focused suite, expanding without regressing it.

## 9. WP6 — First physical acceptance (separate owner authorization)

Perform **no new firmware writes** at this stage if the already-visible Network FTP route can be tested as-is.

### 9.1 Owner camera UI observation (R1)

Record firmware/region only as needed, menu language, exact menu locations and whether items are **absent, grey, selectable, or erroring**. Capture photos of screens with all credentials/serials hidden:
1. `Network → Transfer/Remote → FTP Transfer Function` and `FTP Function` On/Off state.
2. Server settings, Wi-Fi connection status, FTP connection indicator/error details.
3. `Setup → Operation Customize → PB Custom Key Setting` category and all FTP labels visible/absent.
4. Current Playback function/Fn menu for a **normally displayed single still image** versus group view; do not misinterpret a menu that belongs under Network.
5. Full ordinary shutdown and restart without changing firmware or resetting settings. Record if results differ.

### 9.2 Optional service field inspection (R2; explicit separate approval)

Only use an already-audited service path and read-only target operation. Export **privately** the 9 Network flags, 81 menu permissions, `0x0816/17/18` record surroundings, relevant App identity and, if qualified, WBI normalized logical state. Compare the preexisting camera state to current target definitions and upstream catalog. **No same-byte probe or unrelated persistent writes**. Logs must omit personal identifiers and credentials.

Branch:
- App target stock + runtime menu absent: candidate not installed or old packaged executable. Diagnose version/provenance; do **not** blindly repeat installation.
- App target patched + runtime menu absent: WBI shadow, runtime predicate or mode registration remain candidates.
- Network menu on + FTP still disabled: inspect actual configuration/connection/mode, `0x0818` and state machine; do not assume missing Gallery fields.
- Action assignable + transfer fails: prioritize network settings and worker/queue rather than UI flags.
- Any `MISMATCH` or stale/mixed image: block writes and investigate first.

### 9.3 Controlled native FTP smoke test (R1 with owner-controlled network)

With the camera disconnected from USB/service mode, use a private Wi-Fi AP and an isolated FTP server on the same network, a disposable test user, restricted destination directory, and **non-sensitive test photos**. Do not expose plain FTP on the Internet. Confirm that server logs show the camera as the client and that no desktop uploader ran.

Start with a single still image from Network FTP selection if supported; compare original file SHA-256 with server receipt. Then immediately test a second and a third image, without a reboot or battery removal. This distinguishes "one file works" from a functional transfer queue. Document protocol negotiation and connection errors, but redact usernames, passwords, IP/MAC addresses and identifiable files before sharing summaries. FTPS is a later test **only if** the actual firmware supports it and validates certificates.

## 10. WP7 — Functional, reliability and state-machine acceptance matrix

The following are **engineering test thresholds**, not historical camera results. Reduce only with a documented reason and never imply unsupported native capabilities have passed.

| Test ID | Case | Pass evidence |
|---|---|---|
| T00 | Unmodified/read-only baseline | Complete UI/state matrix; no unexpected writes |
| T01 | Configure server and enable FTP | Camera connects; proper state icon; persists after ordinary restart |
| T02 | Single JPEG from Playback | Correct key/menu action; identical received SHA-256 |
| T03 | Second/third sequential upload | Both succeed without stalled `transferring` state |
| T04 | Manual batch of 20 stills | All selected files received and intact; no unrelated files |
| T05 | RAW+JPEG pairs | When the native selector exists, each specified pair arrives with correct identities |
| T06 | Automatic upload of 50 captures | Successful transfer after files finish writing; camera capture remains usable |
| T07 | Temporary AP/server loss, three cycles | Retried/reconciled files; no permanently greyed FTP switch; duplicates documented |
| T08 | Normal restart and subsequent uploads | Settings/queue semantics understood; no reboot-only stall |
| T09 | Cancel and resume under load | Worker returns to a usable state; no persistent unusable FTP UI |
| T10 | Format/media restrictions | Unsupported group-view/unknown database image is rejected appropriately; no crash |
| T11 | File name collision and target folders | Collision behaviour recorded; no unintended overwrite |
| T12 | Private FTPS endpoint, if native supported | Certificate and hostname checks work; invalid certificate is not silently accepted |
| T13 | Long-running 100-image/multi-session campaign | Byte integrity and failures tracked, battery/capture effects recorded |
| T14 | Approved rollback test, only when safe | Managed fields restored from justified original state, unrelated settings and English preserved |

**Reliability investigation when T03/T07/T09 fails:** preserve camera screen/status evidence, server timestamps and sanitized error codes. If a relevant `FTPNSEND.DAT` queue artifact exists, acquire a **copy** after a safe shutdown and mount, preserving original bytes; do not delete/edit the active card queue. Compare queue record count and file identity to worker state. Attribute failures to server setup, Wi-Fi, action UI, queue logic or runtime state only after discriminating observations.

**Do not perform destructive fault injection:** no deliberate unplug during a write, forced low-battery reset, unsafe card removal while transferring, or "battery pull" as a validation method.

## 11. WP8 — Conditional firmware experiment design (R4: not authorized by this plan)

If and only if the above experiments demonstrate that a new persistent App/WBI change is necessary, prepare an exact-body R4 review packet with:
- precise firmware/profile and target-body identity, user consent, scope, all files/partitions, preimages, new bytes, protected regions and control-flow support;
- complete read-only baseline + independent copies, full modified-units snapshots, immutable journal and staged rollbacks;
- a per-write interruption and recovery matrix, including the failure of service access and absence of guaranteed hardware restoration;
- bounded experiment altering only one **proved** missing gate/state group at a time, rather than copying all upstream settings indiscriminately;
- explicit expected firmware/readback/runtime observations, single-file server test and hard stop criteria;
- separate approval for any WBI edit/invalidation, reboot, new service payload, user setting write or firmware update.

Never transplant full donor binaries, model/calibration data, A7CR offsets, or CP control code. If no defensible recovery path exists, leave the R4 gate **closed**, record the limitation and continue offline analysis or use a **separately labelled host-assisted alternative** (which does not satisfy native FTP).

## 12. CI, provenance, release and documentation

1. Add a synthetic fixture corpus for stock/candidate/partial/unknown App action table, upstream App/WBI manifests, menu-parent records and transaction interruptions. Keep copyrighted full firmware and per-body backups private.
2. CI: run Python unit tests and static checks on supported desktop environments; explicit hardware evidence is collected locally by owner and is never asserted by CI.
3. Pin source revision, build dependencies, portable ZIP hash and generation logs. Publish a **new immutable prerelease** when safe; do not mutate an existing `v1.0.0` asset/tag to imply identical source provenance.
4. Show supported-state labels: **reference-known**, **candidate installed**, **menu observed**, **upload verified**, **reliability verified**. Allow “full native FTP working” only after P0 end-to-end plus sequential-upload acceptance, not after all bytes are 1.
5. Keep separate `EN-101` status and tests; do not make FTP experimental state affect native English, region or wireless radio configuration.
6. Update ``docs/FTP.md`, ``docs/USER_GUIDE_CN.md`, ``docs/BACKLOG.md`, ``docs/CODEX_HANDOFF.md`, `research/STATE.json` and a sanitized dated session report as work packages are completed. Mark legacy optimistic text as historical, not current truth.
7. Publish no firmware image, raw WBI/partition data, camera images, FTP credentials, body serial, MAC, real IP, complete capture, calibration data, or secret keys in GitHub issues/PRs.

## 13. Recommended small PR sequence

- **PR-A (R0, status/safety):** Reconcile draft PR #2 against current main; evidence labels, accurate menus/byte counts, fail-closed byte validation, incorrect math correction. No new offsets or firmware writes.
- **PR-B (R0, manifest):** Pinned upstream catalog reader, 242-field comparison, App/WBI address-domain validation, synthetic tests.
- **PR-C (R0, root cause):** Detailed `0x0817` resolver and playback UI graph, WBI activation/load analysis, falsifiable diagnosis. No write payload.
- **PR-D (R0, executor):** Safely staged App/WBI planner **only if proven**, no enabled live write for unsupported candidates; replay-safe journal, full-unit readback and simulation.
- **Owner-approved hardware trial:** Independent approval per R1/R2/R4 step; record readback and physical test receipts without private data.
- **PR-E (tests/reliability):** FTP local-server harness, queue/state failure classification, redacted acceptance evidence.
- **PR-F (release):** CI-qualified immutable prerelease with honest feature/status labels, recovery notes and release hashes.

## 14. First Codex work package — implement **now**, offline only

**Scope:** PR-A and preparation of PR-B, **not** an unverified firmware patch.

1. Read `AGENTS.md`, `README.md`, ``docs/CODEX_HANDOFF.md`, ``docs/MASTER_PLAN.md` and `research/STATE.json`.
2. Check out fresh `main`. Inspect draft PR #2 against newest 92-target/seven-span writer; do **not** merge old per-byte code.
3. Run the current focused offline tests (expected historical **106 cases**; record the *actual* result):
   `python -X utf8 -m unittest tests/test_recovery_journal.py tests/test_customizer_recovery.py tests/test_customizer_targets.py tests/test_patch_spec.py tests/test_elf_static.py tests/test_ext2_readonly.py tests/test_uxc_readonly.py -v`
4. Add a **zero-device-contact** audit that checks the 81 App offsets against upstream at its pinned hash, the nine sparse Network IDs, the separate action candidate and no-op `0x262` field. Include failing fixtures for view mismatch, unknown values, stale revision and an invalid action-index formula.
5. Correct only provably false README/GUI claims and mark `FT-101` physically incomplete. Preserve the established English path and all transaction-journal protections.
6. Generate `research/sessions/20261102-ftp-codex-r0-triage.md` with exact executed commands, test outcomes, changed files, unresolved hypotheses, and statement **camera/network commands: none**. Update project progress/State only with evidence, not presumed success.
7. Open a small reviewable PR. The **next single package after that** is the `0x0817` action resolver + WBI logical/runtime mapping in WP2/WP3, *still offline*.

**Exit:** no new patch bytes, no new device access, no release retag, no fabricated FTP success. A reader should be able to understand exactly why a current camera may show Network FTP but not the desired Playback action, what would distinguish the hypotheses, and what must be proven before any next write.

## 15. References

- Owner defect: https://github.com/mingwucn/Sony_research_6700/issues/1
- Owner action-record correction: https://github.com/mingwucn/Sony_research_6700/issues/1#issuecomment-6574307599
- Existing draft PR to reconcile: https://github.com/mingwucn/Sony_research_6700/pull/2
- Current targets: https://github.com/mingwucn/Sony_research_6700/blob/main/apps/a6700_customizer/targets.py
- Current writer and journal: https://github.com/mingwucn/Sony_research_6700/blob/main/apps/a6700_customizer/app_backend.py
- Upstream feature matrix: https://github.com/xyzhangxin/sony-a6700-powerful/blob/d5bb9485dfe7cc4bf13a4ead3a7437c2f40240a9/%E5%BA%94%E7%94%A8/docs/FEATURES.md
- Upstream profile: https://github.com/xyzhangxin/sony-a6700-powerful/blob/d5bb9485dfe7cc4bf13a4ead3a7437c2f40240a9/%E5%BA%94%E7%94%A8/src/a6700_unlock/data/a6700-2.00.json
- Our previous source audit: https://github.com/mingwucn/Sony_research_6700/blob/main/research/FTP_SOURCE_CHAIN_AUDIT.md
- Independent second-image issue: https://github.com/wanghm105/Powerful6700-Windows/blob/main/docs/FTP-KNOWN-ISSUE.md
- Sony A7CR single-image FTP reference: https://helpguide.sony.net/di/ftp_2370/v1/en/contents/single_transfer.html
- Sony A7CR batch FTP reference: https://helpguide.sony.net/di/ftp_2370/v1/en/contents/batch_transfer.html
- Sony FTP security/server reference (another model, for protocol behaviour only): https://helpguide.sony.net/di/ftp_2390/v1/en/contents/FTP_server_registration.html
