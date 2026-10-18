# Sony alpha6700 research

Initial research and local-Codex hand-off, prepared on 2026-10-18.

**Status: planning and offline tooling only. No alpha6700 firmware patch, English unlock, service-access method, or native FTP implementation has been validated by this project. No camera was connected or modified during initialization.**

## Objectives

1. **Priority: native English menus**, preserving the body's original regional/radio configuration and calibration. Owner reports English is unavailable on this mainland China version; enablement feasibility is unverified.
2. **Priority: native camera-to-server FTP over Wi-Fi**, manual uploads first, then automatic transfer. Keep an optional host-assisted bridge separate.
3. **Deferred: FL2/FL3 Creative Looks**, then calibrated custom DCP/LUT-derived still-photo looks as a separately gated extension.

The owner confirmed this priority order on 2026-10-18. FL2/FL3 work must not delay
English or native FTP; all feature acceptance and device-approval gates still apply.

Owner intake (2026-10-18, **source-report**): α6700, firmware **2.00**,
current menu language **简体中文 (Simplified Chinese)**, **Chinese mainland
version**, and **English unavailable**. The complete language
list has not been supplied; exact regional SKU and binary identity remain
unverified. See the [latest intake](research/sessions/20261018-owner-mainland-english.md).
Version text does not verify binary identity. Do not update firmware, run another
model's installer, or change product identifiers merely to begin this project.

Current [RA-003 package/rights findings](research/OFFICIAL_PACKAGE_INTAKE.md):
the [official mainland 2.00 source and its agreement](research/MAINLAND_FIRMWARE_SOURCE.md)
are identified. The [package/statutory-route continuation](research/sessions/20261018-RA-003-package-law.md)
records consented acquisition, size/hash and bounded UFU identification. The later
[scoped directory audit](research/UFU_CONTAINER_AUDIT.md) records five bounded
chunks and one FDAT span, without extracting contents. The latest
[FDAT/extractor audit](research/FDAT_EXTRACTOR_AUDIT.md) records an opaque
4,096-byte prefix result and a pinned source-only candidate. The later
[decoding plan](research/FDAT_DECODING_PLAN.md) documents the narrow research
rationale and a synthetic decoded-header validator. The later
[crypto/provenance audit](research/FDAT_CRYPTO_PROVENANCE.md) pins private inputs and records eight
isolated AES primitive tests. The later
[bounded header trial](research/FDAT_HEADER_TRIAL.md) passed one predeclared real
hypothesis. The latest [stream validation](research/FDAT_STREAM_VALIDATION.md) checked
all 1,000,017 physical blocks, measured 1,020,017,152 logical bytes and checked declared
extent bounds/non-overlap after 45 new synthetic passes. Component formats and
English/FTP mapping remain unverified; no decoded component files were retained. China
Copyright Law Article 50(5) expressly addresses reverse-engineering research;
its limits and the accepted terms remain part of the scoped analysis review.
The activity-specific basis for proprietary unpacking/static disassembly remains
unestablished; the earlier owner rights answer stays **No / unknown**.
Recovery is unproved; separate OSS offers are static leads only. No native
feature is validated.

## Reading order

- [Requested functions and progress](docs/FEATURE_PROGRESS.md): native English,
  FL2/FL3, later calibrated custom looks, native Wi-Fi FTP and optional bridge.
- [Master plan](docs/MASTER_PLAN.md): scope, dependencies, milestones and decision gates.
- [Owner intake and required inputs](docs/OWNER_INTAKE.md): exactly what local development needs, with privacy boundaries.
- [Reference assessment](docs/REFERENCE_ANALYSIS.md): pinned upstream sources, reusable methods and non-portable details.
- [Access, backup and recovery](docs/ACCESS_AND_RECOVERY.md): risk tiers, evidence capture and transaction rules.
- [Creative Looks implementation](docs/CREATIVE_LOOKS.md): AP/CP mapping, still output, preview, metadata, custom-look extension.
- [English language implementation](docs/ENGLISH_LANGUAGE.md): regional configuration versus resources and reversible migration.
- [FTP implementation](docs/FTP.md): native feasibility tree, protocol behaviour, security and separately labelled bridge.
- [Validation and release](docs/VALIDATION.md): concrete test cases, acceptance criteria and failure handling.
- [Task backlog](docs/BACKLOG.md): ordered, independently reviewable local-Codex work packages.
- [Codex hand-off](docs/CODEX_HANDOFF.md): first session, commands and the webchat/local collaboration protocol.

Read [AGENTS.md](AGENTS.md) before changing anything. Start with [project state](research/STATE.json), not a remembered chat conclusion. The executable starter is an offline artifact-inventory helper, not a patcher or camera-dump tool. [Source lock](references/sources.lock.json) records the upstream revisions used for this plan.

Host-only continuation now adds a bounded [artifact probe](docs/ARTIFACT_INTAKE.md),
[inventory portability repair](docs/INVENTORY_PORTABILITY.md), synthetic-only
[candidate/transaction models](docs/OFFLINE_GUARDS.md), a separate
[durable synthetic transaction journal](docs/DURABLE_SYNTHETIC_JOURNAL.md), and a durable
[mock transfer queue](docs/FTP_HOST_PROTOCOL.md). A separate opt-in
[synthetic loopback FTPS lab](docs/FTPS_LOOPBACK_LAB.md) tests a constrained peer
with pinned private dependencies. No camera adapter or device executor exists.
[Pre-camera coverage](research/PRE_CAMERA_READINESS.md)
keeps all 27 work packages and their remaining evidence requirements visible.
[Observed host validation](docs/HOST_VALIDATION.md) now records a clean final-code
export and passing four-job Windows/Linux CI. The [completion audit](research/PRE_CAMERA_AUDIT.md)
and [official-source refresh](research/OFFICIAL_SOURCE_REFRESH.md) preserve remaining
exact-target inputs and feature limits.

## Start locally

```sh
git clone git@github.com:mingwucn/a6700_research.git
cd a6700_research
python -m unittest discover -s tests -v
```

Use a supported Python 3.10+ interpreter available on the local machine; the starter uses only the standard library. On Windows, `py -3` may be substituted for `python`. Do not install USB drivers or run upstream launchers as part of this first step.

Copy the intake/state templates into an ignored private workspace before adding body-specific details. Full firmware, camera backups, calibration, photos, credentials, SDK packages and generated firmware payloads stay outside Git, even while this repository is private. `.gitignore` is a convenience, not an access-control or secret-scanning system.

## Evidence policy

Source documentation, static inference, host tests, camera readback, runtime observation and physical photographic tests are different evidence classes. None may be silently promoted into another. Unknown target addresses, command support and recovery capabilities remain unknown until established on the exact target.

The reference repositories are independent experimental research, not Sony-signed firmware updates. The plan adapts their methodology; it does not transplant their device-specific offsets or promise their results on the alpha6700.
