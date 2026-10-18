# Owner intake and required inputs

This form is for the local Codex session. No answer is assumed from the owner's language, location or previous camera discussions. The GitHub remote is already known: git@github.com:mingwucn/a6700_research.git. Do not ask the owner to repeat it.

## 1. Required before target-specific device work

Copy this section into private/owner-intake.md and fill unknown fields. A sanitized summary can later be shared in GitHub; the private file must not be staged.

| Field | Required information | Why it changes the plan |
|---|---|---|
| Body alias | A pseudonym such as body-01, not a serial | Links evidence without publishing identity |
| Exact model | ILCE-6700 from the body's own menu/label | Prevents A7C/A7CR/A7C II or other-model assumptions |
| Installed firmware | Exact version-screen text and a locally stored photograph | Selects the binary baseline; no automatic upgrade |
| Regional SKU | Country/market of purchase, label suffix if known, imported/domestic status | Language restriction cannot be inferred from the displayed language |
| Available languages | Photograph or transcription of the entire language menu; whether English is absent or merely not selected | May resolve the task without any firmware change |
| Modification history | Prior language tools, service operations, repairs, updates, custom firmware or unknown provenance | Stock version text alone is not an integrity check |
| Normal operation | Current boot, capture, playback, Wi-Fi and USB health | Separates pre-existing faults from research regressions |
| Host platform | OS/version, CPU architecture, Python availability, admin rights and physical ports | Selects analysis and possible USB tooling |
| Connection | Existing data-capable cable, direct port, hubs/docks, current Sony driver/app use | Avoids changing several transport variables together |
| Power and media | Battery health/charge, reliable power arrangement, expendable card with data already backed up | Sets conditions for controlled observation and later writes |
| Recovery tolerance | Whether the body is the only/essential camera, access to repair/spare body, acceptance of nonzero repair risk | Determines whether hardware experiments are appropriate |
| Private storage | Two backup locations, preferably separate physical drives; available space | Prevents a single host-disk failure from destroying originals |

Keep the complete serial, MAC, Wi-Fi SSID/password, FTP password, certificate private keys, local account names and authentication screenshots local. Do not place them in issues or chat transcripts merely to establish compatibility. Screen photographs may contain serials; redact shareable copies rather than modifying the originals.

## 2. Requirement choices to record without blocking offline work

Until changed by the owner, use these working defaults: FL2/FL3 still photos and matching preview are the first look milestone; custom DCP/LUT import is subsequent. Native English selection should preserve the option to return to the original language. Native Wi-Fi FTP manual upload is required first, with automatic transfer later. A bridge is optional and separately labelled. JPEG is the first image-format proof; RAW pairing and HEIF are expanded tests, not silently assumed capabilities.

Record the preferred primary shooting mode, JPEG/RAW/HEIF use, important existing custom recipes, video/log reliance, and any desired DCP/cube inputs with their source/input-domain descriptions and usage rights. For FTP, record Wi-Fi access-point versus direct operation, owner-controlled server OS/software, FTP versus explicit FTPS expectations, remote destination layout, RAW/JPEG policy, automatic versus selected transfer, and whether a temporary USB/PC bridge is acceptable. Real credentials are supplied only through a private local configuration mechanism after the client exists.

The lack of a colour chart, donor camera or FTP server does not prevent initial mapping. It does limit the claims that can be made later. Do not purchase equipment solely on an unverified compatibility assumption.

## 3. Files needed, in acquisition order

### A. Public reference material

Clone the two references into ignored external/ directories or outside this repository, then check out the locked commits. Keep dependency installation separate from executing their applications. Record the actual upstream commit and licence state. Do not redistribute bundled firmware-derived assets as though they were newly authored code.

### B. Official alpha6700 firmware package matching the installed version, when obtainable

Obtain it from an official Sony support channel and keep the downloaded bytes unmodified. Record model, declared version, source URL, download date, byte count and SHA-256. The latest downloadable package may not match the installed version. A package is not a complete per-body backup and may be encrypted, compressed, signed, incremental, or omit device-specific settings. Do not rename another model's package to make an extractor accept it. Do not install an update merely to obtain a convenient research baseline.

If the exact package is unavailable, record that limitation. A reviewed device-read route may still provide the relevant program files. Conversely, offline package extraction does not establish a safe way to write the body.

### C. Exact-body artifacts after access approval

The needed logical artifacts are AP application components, CP image-processing components, resource/language containers, product-feature tables, relevant saved-setting domains, storage/mount metadata and boot-loading information. Their alpha6700 filenames and devices are to be discovered. Reference names appFw.so and cpapp-b.bin are leads, not confirmed alpha6700 paths.

For every artifact, record how it was acquired, whether the camera changed mode or executed code, expected versus observed length, complete hash, and the relationship to the firmware package. Backup/calibration domains need a completeness map. Do not label an application-file copy as a full-flash backup. Dynamic fields require separate snapshots and a field-aware comparison.

### D. Donor data only when needed

For FL2/FL3, the reference donor ILCE-1M2 4.00 is an initial comparison source, not an instruction to cross-flash it. Use official package provenance and preserve the target's sensor calibration. For English, a same-model/same-build multilingual regional resource set is preferable to a different model, when legitimately available. For native FTP, choose a donor only after compatibility analysis; an alpha7 IV is a documented FTP example, not a drop-in binary source.

### E. Validation inputs

Keep original baseline photos, later comparison photos and screen recordings local. Use a static scene, fixed white balance/exposure/focus and a reproducible light source. A colour chart, neutral ramp and multiple illuminants improve later colour claims. Prepare an isolated owner-controlled FTP server and synthetic files before connecting a camera transfer client. Keep server logs and packet captures private unless thoroughly redacted.

## 4. Storage layout

```text
private/
  owner-intake.md
  session-state.json
  body-01/
    intake/                 # original screen photos and device facts
    original/YYYYMMDD/       # immutable acquisition snapshots
    current/YYYYMMDD/        # later pre-operation captures; never overwrite original
    packages/               # unmodified official downloads
    extracted/              # derived files plus extraction manifests
    analysis/               # disassembly projects and working hypotheses
    candidates/             # private forward/inverse outputs
    sessions/               # complete device journal and results
    tests/                  # photographs, measurements, private server records
```

The second independent backup must not merely be another directory on the same volume. Record its inventory locally. Do not put network-mounted experimental camera media inside the offline tool's input workspace. Use ordinary local regular-file copies.

## 5. What should be returned to webchat

Return the repository commit, a sanitized model/firmware/region summary, source and output hashes where appropriate, exact non-secret commands and exit codes, evidence labels, a small relevant excerpt of analysis and the next decision. State whether any device access occurred. For a failed device action, report the last confirmed state and whether completion is unknown, not only the exception text.

Do not send full backups, proprietary SDK archives, private keys, original personal photos or raw credential-bearing traces. A useful initial report can simply identify the remaining unknowns and show that the offline environment is reproducible.
