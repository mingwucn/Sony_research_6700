# RA-004: proposed Windows USB inventory observation

Prepared 2026-10-22. **Not executed or authorized for device contact.** This is
a reviewable R1 packet for a later owner-approved observation. It does not
establish camera compatibility or authorize service mode, temporary native
execution, setting changes, reset, firmware writes or driver changes.

## Purpose and scope

Read the current local Windows PnP inventory once and retain the present USB
and USB storage rows privately. Microsoft documents Get-PnpDevice as returning
basic device information; PresentOnly limits the result to present devices.
It does not provide the exact installed firmware, camera SKU, full USB descriptor
tree, source hashes or a service-access qualification. Windows may perform its
normal enumeration/mounting when hardware is connected; connecting the cable
is itself part of the future approved observation, not an offline action.
[Microsoft command reference](https://learn.microsoft.com/en-us/powershell/module/pnpdevice/get-pnpdevice?view=windowsserver2025-ps).

The host has PnpDevice 1.0.0.0 and exposes Get-PnpDevice. Only command metadata
was checked during preparation; the query below was not invoked. No platform,
driver or module installation is proposed. The query has no remote CIM session,
upstream tools, raw USB requests, vendor authentication or device-control calls.

## Conditions for a later decision

- Owner approves this exact observation, including whether the existing cable
  will be connected. Record the consent in private/session-state.json before
  any query. Today's broad pre-camera goal does not supply that consent.
- Record the existing cable/port/hub, current camera USB setting and whether
  Sony applications are open from existing knowledge. Unknown remains unknown;
  this packet does not change the setting to MSC or direct unplug/replug cycles.
- Use the existing Windows host and ordinary user session. A driver, update,
  format or permission prompt means stop and record it; do not approve it as
  part of this packet. No administrator elevation is included.
- Confirm private/ is an ordinary local directory, not a symlink/junction or
  network-mounted camera path. Retain unrelated device identifiers privately
  too. The query gathers USB inventory broadly to avoid inventing a target ID.

## Exact proposed command block — only after scoped approval

Run from `D:\LocalWork\Sony_research_6700`. One query, no polling or retries.
The fixed private parent must already exist. A new GUID directory and
exclusive-create files preserve earlier observations. A prepared journal is
flushed before the query; it records scope, not an invented approval receipt.

```powershell
$ErrorActionPreference = 'Stop'
$usbParent = (Resolve-Path -LiteralPath '.\private').Path
$usbRunId = [Guid]::NewGuid().ToString('N')
$usbRun = Join-Path $usbParent ('usb-observation-' + $usbRunId)
New-Item -ItemType Directory -Path $usbRun -ErrorAction Stop | Out-Null
function Write-UsbObservationJson([string]$name, $value) {
    $usbBytes = [Text.Encoding]::UTF8.GetBytes(($value | ConvertTo-Json -Depth 6))
    $usbFile = [IO.File]::Open((Join-Path $usbRun $name), [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $usbFile.Write($usbBytes, 0, $usbBytes.Length); $usbFile.Flush($true) }
    finally { $usbFile.Dispose() }
}
Write-UsbObservationJson 'prepared.json' ([ordered]@{
    operation = $usbRunId; prepared_utc = [DateTime]::UtcNow.ToString('o')
    scope = 'one local present PnP query; USB and USBSTOR rows; no device control'
})
try {
    $usbRows = @(PnpDevice\Get-PnpDevice -PresentOnly -ErrorAction Stop |
        Where-Object { $_.InstanceId -like 'USB\*' -or $_.InstanceId -like 'USBSTOR\*' } |
        Select-Object Status, Class, FriendlyName, InstanceId)
    Write-UsbObservationJson 'inventory.json' ([ordered]@{
        observed_utc = [DateTime]::UtcNow.ToString('o'); count = $usbRows.Count; devices = $usbRows
    })
    Write-UsbObservationJson 'outcome.json' @{ status = 'query_completed'; camera_identity_verified = $false }
    Write-Output ('Private inventory saved; rows: ' + $usbRows.Count)
} catch {
    Write-UsbObservationJson 'failure.json' @{ status = 'needs_review'; error_type = $_.Exception.GetType().FullName }
    throw 'Observation stopped. Preserve the private journal; do not retry or change USB state automatically.'
}
```

File creation failures stop the block. A failure writing the failure record
itself can leave only prepared.json; preserve that as incomplete. If the shell
is interrupted or closes, missing outcome.json means incomplete, not successful
observation. The single query has no hard elapsed-time guarantee; if it hangs,
stop the host command and retain the journal without power cycling/resetting
the camera or automatically re-running the query.

## Interpretation and stop rules

Status/Class/FriendlyName/InstanceId are observations from Windows. A friendly
name or matching VID/PID is a lead, not proof of exact body or firmware. Several
rows may represent interfaces of one physical device. Do not count them as
multiple bodies or auto-select a row for service commands. This packet does not
resolve parent-child topology or identify a camera automatically.

Zero plausible camera rows, ambiguous rows, non-OK status, unexpected mode,
disconnection, missing outcome or an OS prompt ends this observation. No next
USB action is implicit. Review existing results first. A completed inventory
can narrow the next identity question; it cannot pass R2/R4 or recovery gates.
Accept query completion only after both JSON records parse, outcome.status is
query_completed, and inventory.count agrees with its devices array. File
existence alone is insufficient. Even coherent records do not identify a body.

Only a manually sanitized summary may enter Git: date, OS/tool version, query
outcome and relevant device class/status plus model-level VID/PID if reviewed.
Full InstanceId tails, serials, unrelated devices and raw JSON stay private.
Do not paste inventory.json into chat, an issue or an external analysis service.

## Preparation validation

The exact block is syntax-parsed with the installed PowerShell parser without
invoking it. Independent review checks query count, private output, no overwrite,
failure stops and distinction from service access. Parser success is not a
runtime test, camera identity or permission. [Session record](../research/sessions/20261022-FT-101-session-lifecycle.md).
