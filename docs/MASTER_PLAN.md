# Master implementation plan

Prepared 2026-10-18. This is a research and engineering programme, not an installation recipe. Source references are catalogued in REFERENCE_ANALYSIS.md and locked in ../references/sources.lock.json.

## 1. Product definition and interpretation

Owner priority update (2026-10-18): native English and native Wi-Fi FTP are the primary goals. FL2/FL3 is deferred to future work and must not delay either priority. Calibrated custom DCP/LUT-derived looks remain a separate later deliverable after a stable FL2/FL3 baseline. The visual target, when that track resumes, is still-photo output and matching live preview. Movie application of new looks is a separate compatibility question, while preservation of existing movie behaviour remains mandatory from the first patch.

English means the camera's own menus, warnings and messages, not an English PC utility or a translated manual. FTP means a camera-resident outbound client delivering files to an owner's server over Wi-Fi without an intermediate computer or phone. Manual selection is the first native FTP milestone; automatic post-capture transfer is the subsequent operational milestone. A host-assisted bridge can produce useful transfers earlier, but cannot close the native-FTP requirement.

After shared discovery, prioritize English feasibility and native FTP feasibility; pursue the smallest fully proved English change and camera-resident manual FTP before deferred looks work. English and FTP analyses can proceed independently; neither requires FL2/FL3. Implementation remains conditional on evidence: English is not automatically easy, and a hidden FTP flag is only one hypothesis. The user does not need to choose a firmware version before the installed baseline is identified.

## 2. Requirements and acceptance ownership

| ID | Deliverable | Minimum completion evidence |
|---|---|---|
| CL-01 | FL2/FL3 selectable as distinct looks | Exact-target menu and selection logic, persisted bindings, new photos and playback; no ST-only fallback disguised by names |
| CL-02 | Correct image-processing route | Gamma, colour parameters and relevant matrices traced and validated; physical differences exceed baseline repeatability |
| CL-03 | Preview follows the active look | Repeated switching without shutter presses, with no stale previous look; physical display evidence recorded separately |
| CL-04 | Preserve native behaviour | Existing looks, recipes, settings, image formats and supported movie/log paths pass regression cases |
| CL-05 | Custom look extension | One calibrated custom slot first, then selected-slot import and up to six only after capacity/resource evidence |
| EN-01 | Native English | English is selectable or deliberately selected and all tested critical menus/warnings render correctly |
| EN-02 | Persistence and reversal | Normal shutdown and complete power removal retain English; original selection/configuration can be restored |
| EN-03 | Narrow side effects | No unintended change to regional/radio configuration, unrelated settings or protected calibration |
| FT-01 | Native Wi-Fi manual upload | An onboard client sends a selected new file to the server; no relay process is involved |
| FT-02 | Reliable queue | RAW/JPEG pairing, reconnect, duplicates, partial transfer and power-state behaviour are defined and tested |
| FT-03 | Automatic delivery | Physical-shutter captures are queued when supported, with observable completion and bounded shooting impact |
| FT-04 | Security and privacy | Credentials remain private, remote paths are constrained and the chosen protocol's security is honestly identified |
| SAFE-01 | Reversible exact-target changes | Fresh backups, checked forward/inverse transitions, bounded writes and a documented recovery envelope |
| REPRO-01 | Reproducibility | Pinned sources, exact firmware hashes, test logs, tool versions and explicit supported combinations |

CL-05 and FT-03 are incremental milestones, not reasons to overstate CL-01 or FT-01. JPEG-first results do not imply HEIF/HLG support. A still-photo result does not imply a movie implementation. An actual successful rollback on a working body does not imply recovery from an unbootable body.

## 3. Present evidence and unknowns

Known externally: the reference projects describe FL2/FL3 work on ILCE-7CM2/ILCE-7CR 2.01; the supplied A7CR work uses ILCE-1M2 4.00 as a look-data donor. Sony's alpha6700 guide documents ten standard looks and six custom recipe slots. Its inspected network menu does not list FTP, while PC Remote is documented. Sony's SDK lists ILCE-6700, but interface and function support remain version/model-specific. See REFERENCE_ANALYSIS.md for primary sources and caveats.

Unknown locally: body regional SKU, installed firmware, prior modifications, working service access, USB identities, AP/CP layout, boot persistence, language-resource availability, native FTP implementation presence, and practical recovery. None is filled with another model's value. Current official firmware-download pages were not reliably retrievable in the initial web session; no latest alpha6700 firmware number is asserted.

## 4. Shared architecture to build

Separate an offline analysis core from device access. The initial repository includes only an artifact-inventory helper and synthetic tests. Future components should be added incrementally:

| Component | Responsibility | Must not do |
|---|---|---|
| Artifact/provenance layer | Hashes, source lineage, extraction manifests, private inputs | Infer compatibility from filenames or upload private inputs |
| Target-profile registry | Exact model/build/region constraints, file identities, proved mappings | Accept wildcards, guessed offsets or an unknown profile |
| Read-only analysis layer | Firmware metadata, string/xref maps, candidate comparison | Import a USB writer or run firmware as a side effect |
| Patch planner | Build deterministic private candidates and inverse descriptions | Apply a device write or silently widen a patch |
| Preservation checker | Prove unrelated bytes/settings remain unchanged | Globally ignore differing settings or reuse stale snapshots |
| Device observation adapter | Explicitly scoped standard or service reads, logs | Hide mode switches/native execution behind a harmless name |
| Transaction executor | Eventually apply reviewed actions with a durable journal | Retry unknown writes, erase identity guards or reboot automatically |
| Feature modules | Looks, language, FTP with separate tests and manifests | Share unexplained offsets or entangle unrelated changes |
| Validation/report layer | Evidence classes, metrics, test matrix, sanitized summaries | Convert absent hardware evidence into a pass |

Proposed interfaces and filenames are design targets, not implemented commands. Only commands explicitly described as available in CODEX_HANDOFF.md exist at initialization.

## 5. Milestones, gates and outputs

### M0 — Reproducible offline workspace

Inputs: this repository and the two public reference repositories. Actions: read AGENTS, run synthetic tests, create an ignored local workspace, pin upstream checkout revisions, inspect dependencies and licences, and fill the owner intake. Outputs: local environment report, source-lock verification, sanitized session report and an unresolved-input list. Gate G0 passes when work can be reproduced without camera access and no sensitive inputs are staged. It does not authorize USB activity.

### M1 — Exact target and acquisition feasibility

Begin with the camera's own version/language/menu screens and host USB descriptor observation only after R1 approval. Compare the displayed identity with subsequent firmware files. Audit a candidate access path before any service authentication or code execution. Establish what every command writes, saves, uploads, remounts or reboots. Do not run the upstream A7C II Backup/Check GUI on an alpha6700.

Outputs: device-facts, transport-feasibility, risk review and a target-specific acquisition procedure. Gate G1 passes only for the documented scope. A standard PTP/USB read succeeding does not authorize service mode. No supported service route means offline extraction/comparison continues while device work remains blocked.

### M2 — Original-state capture and recovery envelope

After separate R2 approval, collect only artifacts supported by the reviewed route. Obtain target program/resource/configuration information, independent checksums, storage topology, boot-loading observations and protected-setting baselines. Use two copies and repeat acquisition where suitable. Immutable program hashes should agree; dynamic settings require typed comparison rather than pretending complete dumps are always identical.

Outputs: verified original-state inventory, target profile draft, private backup catalogue, persistence model and recovery matrix. Gate G2 requires complete coverage of every object any planned feature could change and a credible restoration route for that object. A missing route can be documented as a limitation, but it cannot be replaced by a promise that an SD update will recover everything. The owner's risk decision and the executor's technical preconditions remain separate.

### M3 — Three feature feasibility dossiers

English: establish whether an existing English resource set is blocked by a language-specific allowlist or whether resources/code are missing. Looks: map the complete AP-to-CP chain and donor data format. FTP: distinguish a hidden existing client from stripped backend code, then examine a small onboard implementation or a separately labelled bridge.

Outputs: EN feasibility, CL mapping, FTP decision record, target-specific evidence tables and candidate tests. Each dossier must include falsifying observations and the smallest next experiment. Gate G3 authorizes offline candidate construction only, not hardware installation.

### M4 — Deterministic candidate and reversible migration

Construct candidates from immutable local copies, one feature at a time. Produce complete before/after hashes, bounded edit descriptions, preservation reports, settings-field changes, load-state implications and inverse transitions. Test wrong source, duplicate application, partial source, overlapping edits, invalid enum values, absent resources and unknown transaction outcomes. Exclude sensor-specific donor calibration.

Gate G4 requires source review, passing host tests, explicit device approval, current backups, a target-specific write order and documented stop/recovery conditions. A typed approval may refer only to the reviewed candidate hashes. Editing state files to mark this gate passed is not permitted.

### M5 — Single-feature hardware validation

Apply one accepted candidate, verify complete readback, reconcile saved state, perform only the approved load/restart step after all I/O has ended, and capture physical results. Run the feature's minimum matrix plus shared regression. If uncertain, preserve evidence and return to analysis. Never merge an English change, new colour route and FTP startup hook into the first device experiment.

Gate G5 is a per-feature result on one exact body/build. Reversal must be exercised when safe and approved, with stock or prior known-good functionality checked afterward. Report which recovery conditions have not been tested.

### M6 — Composition, soak and release decision

Compose independently understood features offline using fresh source identities, then test pairwise combinations and the full combination. Allow different user selections, not one mandatory all-feature package. Verify uninstallation order, settings preservation, English resource interactions, FTP during capture, and stock movie/USB behaviour. Define upgrade incompatibility explicitly; modified firmware must not silently flow into a normal upgrade path.

Gate G6 requires the validation suite in VALIDATION.md, documented failure cases and exact support scope. Public distribution needs a separate rights review. A second same-version body can broaden evidence only after a guarded installer already rejects unknown states. There is no universal alpha6700 support claim at this stage.

## 6. Dependency graph and prioritization

```text
M0 -> exact identity / access review -> original-state + recovery evidence
                                   -> offline extraction and architecture map
original-state + architecture -> English feasibility -> English candidate/test
                             -> FL23 mapping -> FL23 candidate/test -> custom looks
                             -> native FTP survey -> resident-client candidate/test
                                                   -> bridge branch (separate result)
independent feature results -> composition -> soak / rollback -> release review
```

Evidence and risk determine which approved step is feasible within the owner's English/FTP priorities. Early English implementation is preferred only when a narrow, verified existing setting can be used. FTP analysis should start early because missing backend support could change the architecture. FL2/FL3 remains deferred; custom LUT work follows its stable basic look path and a measured colour-domain model. A release GUI comes last.

## 7. Decision records and stopping rules

Record a decision whenever the firmware baseline changes, a donor is selected, an address mapping becomes eligible, a recovery claim changes, a requirement is narrowed, or a bridge is chosen. Include alternatives, evidence, rejected assumptions and reversal implications.

Stop the relevant hardware track for an identity/hash mismatch, unknown write result, unexplained settings difference, uncertain code placement, missing critical resource, overheating, repeated crash, or inability to reach the planned recovery interface. Continue independent offline work where useful. A negative feasibility dossier is a valid research output; it is not permission to claim that every possible implementation is impossible.

The detailed implementation procedures are in CREATIVE_LOOKS.md, ENGLISH_LANGUAGE.md and FTP.md. The work packages and first-session hand-off are in BACKLOG.md and CODEX_HANDOFF.md.
