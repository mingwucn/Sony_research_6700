# Owner model, version and current-language intake update

Date: **2026-10-18**. Scope: record supplied facts, synchronize progress notes and
adopt the owner's rollback recommendation as a pre-write prerequisite.
Topic branch: `codex/in-102-final-qualification`, starting at
`34d6bc08af7bf132c62d80320e15ba1c4bdfb1ab`, initially clean.

## Supplied facts and limits

Evidence class: **source-report**, from the owner's chat messages and explicit
clarification:

| Field | Recorded fact |
|---|---|
| Model label | a6700 / α6700; project target remains ILCE-6700 |
| Firmware version text | 2.00 |
| Current menu language | 简体中文 (Simplified Chinese) |
| Complete offered-language list | Not checked |
| English availability | Unknown |
| Regional SKU / purchase market | Unknown |
| Independent exact-build / binary identity | Not verified |

Current Simplified Chinese does not establish a Chinese-only language list or a
regional variant. No original version-screen image or binary artifact was
supplied. The observed public Sony 2.00 catalogue label and owner-reported 2.00
label agree; this does not prove byte identity or regional applicability.

English and native Wi-Fi FTP remain primary. Native FTP, FL2/FL3, calibrated
custom looks and the optional HOST-ASSISTED bridge gain no operating evidence
from this intake. All feature validation flags remain false. No device-write
gate or new device-action approval is recorded.

Owner also recommends a rollback system before writing new firmware. This is
adopted as an explicit prerequisite in the
[recovery/write contract](../../docs/ACCESS_AND_RECOVERY.md#8-write-gate-checklist).
Status: **not established; firmware writes blocked**. Required evidence includes
original/latest-known-good backup coverage, two independent verified storage
copies, an exact target inverse and viable restore routes for the relevant
failure states, including failed normal boot. Service loss is a separate case;
no rescue path or A/B boot system is assumed. Synthetic inverses/journals are
preparation only. There is no permission for a restore, same-byte write, reboot,
service transition, deliberate live interruption or automatic rollback.

## Preservation and checks

Before updating continuity, four existing private intake/progress files were
copied into NEW ignored snapshot files. The original Unknown response remains
in history; the private intake received an appended update. Prior session
reports and audit conclusions remain historical, with dated addenda linking
this newer evidence. No private photos, identifiers, credentials or inputs were
uploaded. No upstream code, updater or camera tool was executed.

Host: PowerShell on Windows AMD64; CPython **3.13.12** at
`C:/ProgramData/miniconda3/python.exe`. Exact commands and results:

```powershell
git status --short --branch
git log -1 --format=%H
python --version
python -I -S -B -X utf8 private/sessions/20261018-owner-ui-intake/update-notes.py
python -I -S -B -X utf8 private/sessions/20261018-owner-ui-intake/record-rollback-requirement.py
python -I -S -B -X utf8 private/sessions/20261018-owner-ui-intake/verify-notes.py
git diff --check
git check-ignore private/session-state.json private/owner-intake.md private/feature-progress.json private/feature-progress.md
```

All exited **0**. Initial status was clean on the topic branch; Python reported
3.13.12. The update synchronized public state and four private files. Verification
checked JSON parsing, identical public/private feature entries and priorities,
the three owner-reported labels and remaining unknowns, unchanged approvals,
preserved private snapshots/history, protected file hashes, unchanged code/tests/
workflow/locks/profile, relative documentation links and the reviewed path list.
An additional four NEW snapshots preserve the private state before recording the
rollback requirement. The final check also verifies the same unmet recovery
requirement in all structured notes. All four private paths were ignored.
Whitespace checks passed. Git's configured
LF-to-CRLF notices do not represent failures.

This documentation/intake-only change does not rerun the unchanged 154-test
synthetic suite. Its recorded results remain the prior qualification evidence;
these continuity checks add no firmware, device, network or feature coverage.
An independent read-only review checked the evidence distinctions.

## Reviewed public files

- `README.md`
- `docs/ACCESS_AND_RECOVERY.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/OFFICIAL_SOURCE_REFRESH.md`
- `research/PRE_CAMERA_AUDIT.md`
- `research/PRE_CAMERA_READINESS.md`
- `research/STATE.json`
- `research/TARGET_EVIDENCE_GAPS.md`
- `research/sessions/20261018-owner-ui-intake.md`

Only these reviewed public paths are staged. Four private continuity files and
their snapshots remain ignored. No push or PR update is part of this intake.

## Remaining prerequisites and next package

Remaining prerequisites include the full offered-language list and English
availability, regional SKU, legitimate matching package and its provenance/hash,
independent exact-body/build correspondence, and the previously unknown history,
health/setup, power/media, recovery tolerance and independent backup storage.
No access route, acquisition, target mapping or recovery envelope is established.

Next single host package: **RA-003 official-package provenance/intake for the
owner-reported α6700 version 2.00**. Preserve a legitimate official package in a
NEW private location, record origin/date/size/hash and inspect only through an
applicable reviewed offline parser. Do not execute its updater or claim a proved
exact-body/build match. EN-101 separately still needs the complete language list
using the existing no-change normal-menu observation instructions.

Agent camera commands: **none**. Agent device access/writes: **none**.
