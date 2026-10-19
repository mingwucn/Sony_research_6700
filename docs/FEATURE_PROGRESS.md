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

Latest shared RA-003: [preflight comparison](../research/PREFLIGHT_COMPARISON.md).
Qualification **346/346 passed**, zero skipped, exit **0**, **12.080s**; **26 new + 320 retained** cases; all **35** predecessor files and **32** historical failed-trial pins preserved.
Actual terminal **complete_private_preflight_expanded_member_comparison**, script **0** / host **0**, **37.595937s**; pipeline attempts **1**, expanded callback attempts **5**.
Source observation **source_read_confirmed**; protected callback attempts are separate and missing preliminary verification does not establish no I/O.
One separately frozen same-five comparison passed its complete lineage and original-outcome checks; limited expanded header leads were recorded after pre-I/O metadata preflight.
No retry, fallback, child/decoded/raw-prefix files, decompression/disassembly, upstream/firmware execution, camera or feature/write gate.
Earlier five unknown outcomes and prior refusal remain unchanged; no retroactive runtime-stage claim.
Sanitized header-lead counts: ext_family_header_candidate/header_only: 2; fat_legacy_header_candidate/malformed_header: 2; unknown/unsupported_opaque: 1.
Selected raw retention remains bounded separately from metadata copies. Six retained prior trees and seven gate snapshots may coexist, each with a 2MiB serialized-role limit, plus caller objects/overhead/other buffers. Historical20MiB pipeline allowance is not an aggregate managed/process memory cap.
Next shared package: **RA-003: design and synthetically qualify a bounded ext-family superblock capability and geometry gate using pinned authoritative format sources; no actual replay or directory traversal**.

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
