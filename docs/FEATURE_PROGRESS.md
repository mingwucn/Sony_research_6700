# Requested functions: progress and next evidence

Updated: **2026-10-18**. This is the feature-level progress note; the
[backlog](BACKLOG.md) tracks work packages and [STATE](../research/STATE.json)
records machine-readable evidence. An internal copy is kept in ignored
`private/feature-progress.json` and `private/feature-progress.md`.

**None of the requested camera functions has been validated on this body.**
Firmware, regional variant and available languages remain unknown. Camera
access/writes: none. No device-write gate has passed. Progress below describes
completed preparation separately from actual feature operation.

| Requested function | Current progress | What is still missing | Next feature package |
|---|---|---|---|
| **Native English menus** | Language hypotheses, preservation rules and critical-message validation plan prepared. Actual English availability is unknown. | Actual language list; if restricted, exact-build resources and narrow policy-field/all-consumer evidence. English already offered would allow the normal-menu branch. | EN-101, after exact-target intake/acquisition |
| **FL2/FL3 still-photo looks and matching preview** | Reference-code/rights audit and synthetic candidate/inverse guards prepared. No alpha6700 mapping or candidate exists. | Exact firmware/AP/CP/resource evidence, stock looks/recipes and photo baseline, capacity/dispatch/metadata/preview mapping, conditional recovery. | CL-101/CL-102, after their target prerequisites |
| **Calibrated custom still-photo looks** | Separately gated second phase specified. No calibrated fit or target slot is proved. | Stable FL2/FL3 still/preview baseline; explicit DCP/cube/Sony-ST domain; legitimate calibration and holdout inputs; target slot, precision and resource ownership. | CL-107, after CL-105/106 and calibration inputs |
| **Native camera-to-server Wi-Fi FTP** | Host queue/protocol foundation tested, including a constrained loopback FTPS peer. Native backend/route remains uninvestigated on the target. | Target backend/ABI/media/network/lifecycle evidence; then one camera-resident manual upload with full server equality. Automatic post-capture transfer is a later, separate step. | FT-101; later FT-103 manual, FT-104 automatic |
| **Optional HOST-ASSISTED bridge** | Architecture and reusable synthetic host-transfer leg prepared. No camera-to-host adapter exists. | Verified model/firmware/SDK capabilities, capture-completion signal, physical-shutter versus remote-trigger behavior, formats/card retention and a separately approved camera leg. | FT-106 only if pursued; does not satisfy native FTP |

FL2/FL3 remain the first look milestone; custom looks follow their own calibration
gate. The bridge stays optional and separately labelled. A host-generated upload
cannot be recorded as native camera Wi-Fi FTP.

## Verified preparation supporting these functions

- RA-001: host baseline/private intake prepared; owner body/setup facts remain
  Unknown. [Initial report](../research/sessions/20261018-RA-001.md).
- RA-002: references pinned and static provenance/rights audit recorded;
  reuse/target limitations remain. [Audit](../research/REFERENCE_AUDIT.md).
- Inventory/probe and synthetic patch/transaction models exist, with no eligible
  device profile or executor. [Coverage](../research/PRE_CAMERA_READINESS.md).
- Latest standard-library suite: **129 passed, 1 skipped**, exit 0.
  Constrained loopback lab: **19 cases passed**, including 100 synthetic files
  in 50 groups; all 21 lab servers stopped. This proves only the documented host
  cases. [Exact commands/results](../research/sessions/20261018-FT-102-loopback.md).

Current shared host package: **IN-102 clean authored-tree offline reproduction**.
The next target-specific package remains RA-003 once installed firmware and
legitimate matching-package provenance are available. Existing Unknown intake
answers are retained; no camera operation is implied by this note.

## Keeping the notes current

At session start, read this page, STATE and the internal feature note when it
exists. Whenever feature evidence, a blocker or a next step changes, update the
matching STATE feature entry, this page and the private note together, with a
dated session/evidence link. Record regressions and negative results too.
Use descriptive statuses rather than invented completion percentages. Promote
a function to validated only when its complete target acceptance evidence exists.
Keep serials, private paths, credentials, photos and raw observations in the
private note/journal; publish only sanitized summaries.
