# Sony alpha6700 research

Initial research and local-Codex hand-off, prepared on 2026-10-18.

**Status: planning and offline tooling only. No alpha6700 firmware patch, English unlock, service-access method, or native FTP implementation has been validated by this project. No camera was connected or modified during initialization.**

## Objectives

1. **Priority: native English menus**, preserving the body's original regional/radio configuration and calibration. Actual language availability remains unknown.
2. **Priority: native camera-to-server FTP over Wi-Fi**, manual uploads first, then automatic transfer. Keep an optional host-assisted bridge separate.
3. **Deferred: FL2/FL3 Creative Looks**, then calibrated custom DCP/LUT-derived still-photo looks as a separately gated extension.

The owner confirmed this priority order on 2026-10-18. FL2/FL3 work must not delay
English or native FTP; all feature acceptance and device-approval gates still apply.

The currently installed firmware and regional variant are unknown. Do not update firmware, run another model's installer, or change product identifiers merely to begin this project.

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
