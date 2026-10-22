# Session-lifecycle review and R1 packet — 2026-10-22

Baseline clean `cb6ea1c`; branch `codex/ft101-session-lifecycle-20261022`.
Previous goal turn: **progress**, source chain and concrete failure paths
audited. This turn: **progress**, caller gap resolved, takeover/exceptional-exit
scope traced, and the missing exact Windows R1 packet prepared and independently
reviewed. The full goal remains active/incomplete; no completion or blocked
transition was claimed.

[Decision matrix and source findings](../PRE_CONTACT_DECISION.md).
[Prepared R1 packet](../../docs/WINDOWS_USB_OBSERVATION_PACKET.md).
Camera commands: **none**. The proposed PnP inventory query was not executed.
No upstream execution/compilation, binary acquisition, firmware processing,
driver/helper installation, device approval or feature/recovery/write pass.

## Commands and results

Executed from the repository root. Python: CPython 3.13.12 at
`C:/ProgramData/miniconda3/python.exe`; PowerShell **7.6.5**. Scripts below are
locally authored collectors/checkers and do not execute fetched code.

```powershell
git status --short --branch
git log -1 --oneline
git switch -c codex/ft101-session-lifecycle-20261022
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-ft101-session-lifecycle/acquire.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-ft101-session-lifecycle/verify_sources.py
Get-Command Get-PnpDevice | Select-Object Name,CommandType,Source,Version
& .\private\sessions\20261022-ft101-session-lifecycle\check_packet.ps1
```

All exit **0**. Nine allowlisted immutable text GETs succeeded HTTP200 without
redirects/retries; bytes/Git blob/SHA-256 were verified and saved exclusively.
Combined receipts: **53 text blobs, 24 AST-only Python parses**. No Objective-C
or Swift compile claim. Two independent read-only reviewers covered desktop
caller handling and the finite pre-contact requirements/Windows command packet.

Get-Command inspected metadata only: Get-PnpDevice is provided by PnpDevice
1.0.0.0. It did not invoke the PnP query. Microsoft's official
[Get-PnpDevice reference](https://learn.microsoft.com/en-us/powershell/module/pnpdevice/get-pnpdevice?view=windowsserver2025-ps)
and [ParseInput reference](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.language.parser.parseinput?view=powershellsdk-7.4.0)
were checked. The parser check finds one proposed module-qualified query and
zero syntax errors; it never invokes the parsed block. It was rerun after the
review suggestion to qualify the module and require coherent output records.
Final parsed block SHA-256:
`61905e3222141faf4eb267b5204a4d308174c322ff691c84a99b7495b5af46d7`.
The command allowlist is a review aid, not a sandbox or proof of runtime effects.

No behavioral upstream tests were run. The desktop tests were read to identify
their fake backend and cancellation expectations; they do not validate physical
STOP_SENSER, hardware faults or recovery. The R1 packet's consent and ordinary
private-directory prerequisites are procedural; the query has no hard deadline.

## Remaining prerequisites and next package

R1 requires the owner's exact-step decision and existing connection context.
R2 additionally requires target/ABI and host/binary qualification plus resolved
temporary execution, journal and cleanup behavior. R4 remains blocked by exact
current artifacts, candidate/inverse, protected coverage, copies and recovery.
English resource feasibility and five old GDT activity decisions remain open.
No previously supplied model/version/language fact was requested again.

Next single package: **RA-004 owner decision on the prepared R1 inventory;
execute once only if explicitly approved, then reconcile private results.**
The broad pre-contact objective does not itself authorize that execution.

## Saved notes and repository verification

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-ft101-session-lifecycle/update_progress.py
git diff --check
git check-ignore private/sessions/20261022-ft101-session-lifecycle/receipt.json private/session-state.json private/feature-progress.json
git add -- docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md docs/WINDOWS_USB_OBSERVATION_PACKET.md references/sources.lock.json research/FTP_SOURCE_CHAIN_AUDIT.md research/PRE_CAMERA_GAP_AUDIT.md research/PRE_CAMERA_GAP_LEDGER.json research/STATE.json research/PRE_CONTACT_DECISION.md research/sessions/20261022-FT-101-session-lifecycle.md
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git commit -m "docs: finish USB lifecycle review and prepare R1 inventory packet"
git status --short --branch
```

Progress/preservation assertions, JSON serialization, ignore checks and
whitespace checks exited **0**. The updater retained exact previous bytes of
modified public/private notes in this ignored session directory. Historical
activity decisions, recovery/device flags and unvalidated feature statuses
were preserved. Obsolete next-step suggestions were retained as history and
replaced with the specific pending R1 decision. Public/private summaries agree.
Eleven named authored public files were reviewed and staged; private reference
texts, receipts and identifiers are not staged. No push or external submission.

Changed public files: this report; `research/PRE_CONTACT_DECISION.md`,
`research/FTP_SOURCE_CHAIN_AUDIT.md`, `research/PRE_CAMERA_GAP_AUDIT.md`,
`research/PRE_CAMERA_GAP_LEDGER.json`, `research/STATE.json`,
`references/sources.lock.json`; and `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`,
`docs/FEATURE_PROGRESS.md`, `docs/WINDOWS_USB_OBSERVATION_PACKET.md`.
