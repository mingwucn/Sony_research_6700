# Pre-contact decision: source lifecycle and ordinary observation

2026-10-22. Scope: R0 source review and preparation. Evidence:
**source-report**, **static-inference**, **offline-tested** integrity/syntax.
Camera commands: **none**. No native feature, recovery or device-write gate
passed. The full goal is incomplete; these findings do not authorize contact.

The pinned source audit is complete for the selected host takeover and desktop
session paths. **FT-101 remains partial** because native backend/ABI, exact-body,
security and physical acceptance evidence are still missing. A separately
prepared R1 inventory packet remains unexecuted: the owner explicitly chose
**Keep camera contact on hold**. Do not request approval again while that hold
stands. Offline work may continue within existing permissions; the full goal
was not paused. R1 does not require completion of the R4 firmware-write recovery gate.

## Lifecycle findings at the fixed reference pin

Reference `xyzhangxin/sony-a6700-powerful` at
[`ac1cd0db5d0210292be1cee292d15034a222ae64`](https://github.com/xyzhangxin/sony-a6700-powerful/tree/ac1cd0db5d0210292be1cee292d15034a222ae64).
Paths below are relative to `应用/`. Nine additional ordinary text blobs were
obtained: capture helper, real/demo bridges, bundle worker, three Swift sources
and two test sources. Across this and the two preceding reviews, 53 pinned text
blobs and 24 Python ASTs were verified. No Objective-C/Swift compilation,
upstream test execution, application launch, ELF download or camera command.

1. **The capture helper has device/host-storage side effects.**
   `src/a6700_unlock/native/mac_capture.m:11` enumerates whole disks below the
   selected USB service and invokes non-forced diskutil unmountDisk. Failure
   stops capture. `:104` selects one Sony MSC candidate, deduplicated by location;
   `:146` requires root; `:153` captures the device and `:156` surrenders it.
   No reset or driver replacement call was found in this helper, but media
   unmounting and interface capture make it unsuitable for an inventory-only
   proposal. A matching Sony MSC identity does not establish a6700/mainland
   build suitability. The helper's chosen identity is not passed as an exact
   identity binding to the later Python enumeration. The diskutil wait has no
   elapsed-time deadline in this source. This macOS path does not qualify the
   current Windows host for service work.

2. **Correction: the packaged real desktop handles the prior setup exception.**
   The earlier isolated controller busy-state concern is resolved by its
   caller: `src/a6700_unlock/desktop/physical_bridge.py:39`–`:58` catches
   Exception and KeyboardInterrupt, clears busy/readiness and emits a failure
   snapshot. Do not infer a permanent UI deadlock from the isolated controller.
   The previous audit expressly left caller coverage open; this closes that
   specific question. It does not close the separate worker-death case below.

3. **Cancellation/readback and uncertain service-exit findings remain.**
   The real bridge accepts cancellation at `physical_bridge.py:97`; the
   controller's cancellation checkpoint can interrupt the progress callback
   between writer return and independent readback. The operation becomes
   uncertain and the physical service exits the session, reaching STOP_SENSER
   without a reconciled-outcome condition. The upstream synthetic desktop test
   at `tests/test_desktop.py:220` expects uncertainty and one write after this
   cancellation; it does not assert completed independent readback or safe
   service exit. Its fake backend's exit merely records closed state. The
   source path conflicts with our reconciliation rule; hardware effects are
   untested. See [the original trace](FTP_SOURCE_CHAIN_AUDIT.md).

4. **Normal close protection does not cover every process-loss path.**
   `desktop/macos/OperationWindowGuard.swift:25` and `A6700Preview.swift:209`
   route normal window/app exit through allowWindowExit. PreviewModel's busy
   state includes pending requests, so ordinary intentional closure during a
   recognized operation is blocked. Explicit real-bridge shutdown calls
   end_session. Unexpected stdin EOF instead sets cancellation and joins a
   daemon thread for five seconds (`physical_bridge.py:106`), without an
   unconditional session close. `PreviewModel.swift:213` closes stdin, waits
   at most 1.5 seconds and may terminate the worker without a cleanup receipt.
   These are exceptional EOF/slow-cleanup gaps; they are not proof that normal
   window closure interrupts a writer.

5. **Worker death and session reuse need distinct treatment.**
   The Swift termination handler (`PreviewModel.swift:120`) displays a nonzero
   exit error without clearing pendingAction or the old busy snapshot. A worker
   loss during an operation can leave the close guard latched; no injected
   worker-death test was performed. Normal operations reuse one authenticated
   session and cooperative lock, with a fresh sparse read per operation.
   Restart-preparation closes that session and invalidates readiness. There
   is no new evidence of automatic writer retry. Demo disconnect/reconnect
   commands belong to the simulation bridge, not the physical worker API.

These findings qualify the earlier host review without changing its source pin.
The durable pre-operation journal and unresolved-prior-intent interlock gaps
remain. No source fixes were integrated into this repository's device path;
this project still has no adopted camera executor.

## Finite decision matrix

| Activity | Preparation status | Current decision / missing prerequisite |
|---|---|---|
| Normal Version/Language UI | Existing bounded packet; owner already reported a6700, 2.00, mainland and English absent. | No repeat generic intake needed. Further label/SKU observation is a separate future owner action; firmware recovery is not a prerequisite to reading normal screens. |
| R1 Windows inventory | [Exact one-query packet](../docs/WINDOWS_USB_OBSERVATION_PACKET.md), command metadata checked, syntax parsed, independently reviewed. | Prepared, not run or authorized; camera contact is on explicit owner hold. Only a later owner change to that hold and separate scoped approval/context can permit this observation. It cannot establish full descriptors, topology or firmware identity. |
| R2 service/native reader | USB source and effects reviewed; existing risk contract applies. | No-go: pre-execution exact-target/ABI evidence, qualified host route/binaries, temporary effects, durable intent, cleanup/reconciliation and scoped approval missing. Read-only intent does not make native execution R1. |
| R4 FTP App/WBI change | Catalog/profile correspondence and source transaction reviewed; explicit FTP selection possible. | No-go: qualified R2 route, exact current artifacts/candidate/inverse, full changed/protected coverage, independent copies, resolved uncertainty and owner-required recovery evidence absent. Menu/settings terminology does not make program changes R3. |
| English enablement | Owner absence report and resource/policy hypotheses recorded. | No mechanism or exact-build resource coverage established; no English action proposed. |
| GDT analysis preparation | Finite source/metadata audit complete; external trusted-origin projection repaired and synthetically qualified. | Isolated current-context handoff and actual source/gate/record migration remain; v6/public execution refused. No actual GDT/content observation or camera contact. |

No new code framework, guessed target profile, firmware change, extra dependency
or repeated generic intake can replace the missing external observations.
Failed-boot recovery remains a write prerequisite, not a blanket prerequisite
to every ordinary UI/OS inventory observation. R2 still needs its own explicit
failure/recovery envelope; permission for R1 would not supply it.

## Next single work package

RA-003: integrate and qualify the current-command context at the existing host/child preparation seams using invented inputs in a fresh isolated process. Reuse the exact bootstrap, source owners and genuine retained control/helpers; keep final dispatch inert and actual v6/public execution refused. Close the combined startup/handoff gap without new generic approval/context infrastructure, protected reads, dependency activation or camera contact. English/native FTP stay first.

[Finite source audit and repair](sessions/20261022-current-binding-audit.md).
