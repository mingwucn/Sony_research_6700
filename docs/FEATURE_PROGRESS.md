# Requested functions: progress and next evidence

Updated: **2026-10-18**. This is the feature-level progress note; the
[backlog](BACKLOG.md) tracks work packages and [STATE](../research/STATE.json)
records machine-readable evidence. An internal copy is kept in ignored
`private/feature-progress.json` and `private/feature-progress.md`.

**None of the requested camera functions has been validated on this body.**
Owner reports α6700 firmware **2.00** and current menu language **简体中文**
(Simplified Chinese), **source-report**, 2026-10-18. The full language list has
not been checked; English availability and regional variant remain unknown.
Exact binary identity is unverified. Agent camera access/writes: none. No
device-write gate has passed. Progress below describes
completed preparation separately from actual feature operation.

| Requested function | Owner priority | Current progress | What is still missing | Next feature package |
|---|---|---|---|---|
| **Native English menus** | Primary | Language hypotheses, preservation rules and critical-message validation plan prepared. Actual English availability is unknown. | Actual language list; if restricted, exact-build resources and narrow policy-field/all-consumer evidence. English already offered would allow the normal-menu branch. | EN-101: offered-language observation first; exact-build acquisition if binary analysis is needed |
| **Native camera-to-server Wi-Fi FTP** | Primary | Host queue/protocol foundation tested, including a constrained loopback FTPS peer. Native backend/route remains uninvestigated on the target. | Target backend/ABI/media/network/lifecycle evidence; then one camera-resident manual upload with full server equality. Automatic post-capture transfer is a later, separate step. | FT-101; later FT-103 manual, FT-104 automatic |
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

The [completion audit](../research/PRE_CAMERA_AUDIT.md) accounts for all 27
packages and validation families. Next single host package: **RA-003, official
package provenance/intake for owner-reported version 2.00**, without executing an
updater. Legitimate matching-package provenance and exact binary identity remain
unresolved. EN-101 still needs the full offered-language list, using the existing
no-change normal-menu instructions; English may already be offered. Earlier
Unknown responses are preserved as history. Host qualification and this intake
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
