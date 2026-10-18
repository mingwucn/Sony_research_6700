# Pre-camera completion audit

Audit date: 2026-10-18. Code baseline:
`fb32370052a0ffe5d8a529edba971f962ce57654`. This note audits available
preparation against the 27 packages in [BACKLOG](../docs/BACKLOG.md), the
requirements and G0..G6 in [MASTER_PLAN](../docs/MASTER_PLAN.md), and the named
tests in [VALIDATION](../docs/VALIDATION.md). The original acceptance criteria
remain authoritative. An entry below describes evidence or a precise gap; it
does not close a package because a document exists.

**Native English and native camera-to-server Wi-Fi FTP are primary.** FL2/FL3
stills and matching preview are deferred; calibrated custom still-photo looks
remain separately gated after stable FL2/FL3. The optional HOST-ASSISTED bridge
is a fifth, separate function and cannot satisfy native FTP. All five camera
functions remain unvalidated. See [per-function progress](../docs/FEATURE_PROGRESS.md).

## Evidence now available

Later owner-intake addendum (2026-10-18): α6700 firmware **2.00** and current
language **简体中文** are now owner-reported; the full language list is unchecked.
The Unknown statements in this audit preserve its earlier evidence snapshot.
See [current intake](sessions/20261018-owner-ui-intake.md) and STATE for current
facts. English availability, region and exact binary identity remain unknown.
Next host package remains RA-003, now with the owner-reported version label.

- The [final-code qualification report](sessions/20261018-IN-102-final.md)
  records a NEW export of 63 committed regular files, 628,717 bytes, with Git blob
  identities and SHA-256 values verified before and unchanged after execution.
  A fresh no-pip stdlib environment on the existing Windows/CPython 3.13.12 host
  ran 154 tests: 152 passed, two skipped, exit 0, unittest time 16.918 s. The
  skips were unavailable local real-symlink creation and unavailable POSIX fork.
  This is fresh source/environment evidence, not a clean OS.
- Actual [push CI run 39149570514](https://github.com/mingwucn/a6700_research/actions/runs/39149570514)
  tested that exact code revision on Ubuntu 24.04 and Windows 2025, each with
  CPython 3.10 and 3.13. All four jobs ran 154 tests: 153 passed, one
  platform-specific skip, exit 0. Ubuntu exercised the POSIX inherited-lock
  regression and real symlinks; hosted Windows exercised real symlinks and the
  Windows path-syntax cases. The owner's local symlink limitation remains.
  [Supplemental PR run 39149603684](https://github.com/mingwucn/a6700_research/actions/runs/39149603684)
  also passed all four jobs on a merge tree identical to the code tree.
- [Reference auditing](REFERENCE_AUDIT.md), bounded artifact identification,
  candidate/inverse guards, synthetic transaction models and the durable
  synthetic journal have their stated host evidence. They supply no target
  offsets, supported profile, camera transport or device executor.
- The separate [FTPS loopback report](sessions/20261018-FT-102-loopback.md)
  records 19 passing cases using 100 synthetic files in 50 RAW/JPEG groups,
  real TLS and complete hash read-back against its constrained custom peer.
  All 21 lab servers stopped. Its no-clobber extension is a specific peer
  contract, not general FTP rename, arbitrary-server or physical-fault proof.
- [Official-source refresh](OFFICIAL_SOURCE_REFRESH.md) closes the initial
  catalogue-access failure: a public USA listing identifies version 2.00 dated
  2025-06-10. This is a public listing only, not the owner's installed firmware,
  a global-latest claim, a matching-package selection or an instruction to
  update. The documented Creators' Cloud upload is not arbitrary-server FTP;
  no FTP item appeared in the inspected menu/release-note text. This does not
  prove backend absence. Installed firmware and regional identity remain unknown.

The final-code report also records review of the proposed publication content.
No private camera input was needed for these runs. Passing hosted synthetic
tests does not establish independent camera reproduction, recovery or a feature.

## All 27 work packages

| Package | Available preparation/evidence | Remaining acceptance input or observation |
|---|---|---|
| RA-001 | Host/intake/session baseline; historical test failure and diagnosis retained | Owner body/setup facts remain Unknown; later host repairs do not rewrite the original result |
| RA-002 | Locked reference trees, entry-point/side-effect and component-rights audit | Exact-target applicability, native source/binary equivalence and rights for any future reuse remain separate |
| RA-003 | Inventory, bounded header probe, private lineage template, extractor text audit and official-source refresh | Observed installed firmware, legitimate matching input, applicable reviewed extraction and child manifests; a header match is not extraction |
| RA-004 | Existing R0 normal-UI observation/access dossier and device-facts template | Actual identity/language observations; separately approved USB scope if needed; reviewed exact-target acquisition proposal before service access |
| RA-005 | Backup coverage gaps and blank catalogue | Approved acquisition route, actual objects/metadata, independent reads where suitable, two verified copies on separate storage where possible, and protected-state coverage |
| RA-006 | Explicit architecture/storage/settings/recovery questions | Exact AP/CP ABI and segments, file/VA/runtime mapping, save/load semantics, protected objects and a reachable recovery envelope |
| RA-007 | Synthetic guards/inverse, in-memory and durable journals, ownership/crash/reopen tests; Windows/Linux CI | Target semantics and OFF-08/10/11, source/control-flow review, target profile/candidate and any later executor qualification; always device-ineligible now |
| EN-101 | No-change branch, language-policy hypotheses and critical-resource investigation protocol | Complete offered-language list; if English absent, target locale/resources and every consumer of a proposed restriction field |
| EN-102 | Generic exact-source/preservation/inverse guards | Accepted EN-101 route, exact source/settings units, critical resources and a narrow candidate with fresh-state inverse/preservation proof |
| EN-103 | ENT-01..06 and shared-regression procedure | Accepted candidate if needed, applicable owner approval, native screens/persistence/protected comparisons and controlled reversal |
| EN-104 | Resource-ID/uninstall dependency requirements | Independently accepted relevant features and ENT-07 composition evidence; deferred looks are not an English prerequisite |
| CL-101 | Stock/capture repeatability protocol, retained for later | Actual looks/recipes, private repeated control photographs and measured baseline; deferred |
| CL-102 | Complete AP-to-CP investigation queue | Target artifacts, independent cross-references, still/preview dispatch and all reachable selection/load routes; deferred |
| CL-103 | Donor/target distinction and calibration-preservation rules | Legitimate donor inputs/rights, decoded format, target capacity and unowned placement; deferred |
| CL-104 | Generic bounded candidate and inverse mechanisms | Coherent exact-target FL23 candidate, instruction/control-flow/ABI review and G4 proposal; deferred |
| CL-105 | Still/metadata/default/preservation matrix | Approved target execution, measured still effects and complete changed/protected-object readback; deferred |
| CL-106 | No-shutter preview and transition/performance procedure | Physical 100-switch and mode/power/load-state observations, applicable target changes and overhead evidence; deferred |
| CL-107 | Domain, holdout calibration and selected-slot requirements | Stable FL23 still/preview baseline, calibration inputs/rights, proved colour domain and target slot/resource ownership; separately gated later |
| FT-101 | Native backend A/B/C decision tree and dependency investigation queue | Target task/UI/config/media/network/credentials/lifecycle chain and ABI; no native route has been selected |
| FT-102 | Durable mock queue plus constrained 19-case loopback FTPS results | Native constraints; owner-selected deployment peer/protocol/path policy for deployment testing; physical faults, real media and target lifecycle |
| FT-103 | One-file native-origin and end-to-end equality criteria | Reviewed native route/candidate, approved camera-resident execution and actual server-side byte equality; a host upload does not qualify |
| FT-104 | Generic capture identity, grouping and ambiguous-result reconciliation | Proved target media-completion/capture events, native queue integration and physical-shutter/card/sleep/cancel observations |
| FT-105 | Security/coexistence/resource measurement protocol | Target certificate/authentication behaviour, stock comparison and owner-approved shooting/startup/thermal/battery limits |
| FT-106 | Optional HOST-ASSISTED architecture and synthetic host leg | Selected SDK/model/firmware capabilities, real completion/format/card-retention semantics and separately approved camera-to-host leg; optional |
| IN-101 | Composition, overlap and partial-uninstall requirements | Independently accepted features actually being combined, exact combined sources/inverses and their combination matrix |
| IN-102 | Final-code fresh authored-tree/no-pip run, actual four-job Windows/Linux CI and bounded content review | Scope stays the observed code/hosts; future imported components/public distribution need rights review; clean OS and independent eligible camera reproduction remain unproved |
| IN-103 | Soak/reversal/release criteria retained | Accepted hardware features, measured stability, safe approved reversal and independent eligible reproduction |

The ledger contains RA x 7, EN x 4, CL x 7, FT x 6 and IN x 3 = **27**.
Unselected SDKs, donors or deployment servers do not justify speculative adapters,
extra dependencies or further generic lab implementations.

## Gate boundaries

| Gate | Evidence boundary after this host preparation |
|---|---|
| G0 | Source/host reproducibility, provenance and publication-content evidence are available for the recorded scopes. Missing owner facts remain recorded. G0 is not USB approval or a camera-write decision |
| G1 | Exact identity and a bounded applicable acquisition/access proposal are absent. Ordinary UI observations and ordinary USB descriptors are separately scoped R1 actions; neither proves service access |
| G2 | No original-state acquisition, protected-object coverage, independent copies or credible target restoration route exists. A backup/hash alone would not establish recoverability |
| G3 | English/FTP have investigation plans, not exact-target feasibility dossiers. Required sources/consumers/dependencies are missing. Looks remain deferred; their dossier is not a prerequisite to advancing English/FTP |
| G4 | No eligible target profile/candidate/inverse, fresh target backups, reviewed write order or applicable device approval exists. Host CI cannot pass this gate |
| G5 | No single-feature device readback, loaded-state observation, physical result, shared regression or approved reversal has run |
| G6 | No accepted camera features are available for composition/soak/release qualification. Independent same-build reproduction and distribution rights remain separate future requirements |

SAFE-01 and REPRO-01 require exact target identities, current-state preservation,
logs, inverse/recovery and explicit combinations at the applicable later steps.
They are not satisfied by a synthetic journal. No gate change is made by this audit.

## Named validation families

| Family | Observed scope | Remaining evidence boundary |
|---|---|---|
| OFF-01..07, OFF-09 | Generic synthetic determinism/source refusal/bounds/replay/inverse/preservation subcases | Actual target inputs, native field/resource meaning and preservation remain unproved |
| OFF-08/10/11 | NOT RUN for a target | Target enums/bounds, instruction boundaries/incoming branches/ABI, and native resource/checksum/UTF decoding need real artifacts; malformed header tests cannot substitute |
| OFF-12/13 | Synthetic uncertain-result, multi-object boundary, durable append/ownership/crash/reopen/reconciliation tests, now exercised on Windows/Linux | No actual camera transport, device journal, camera ownership mechanism or physical interruption result; live power-cut tests are neither required nor authorized |
| OFF-14 | Explicit reviewed-path/content/origin checks for the recorded publication | Manual/bounded review is not a universal secret detector or reuse-rights guarantee; repeat for future proposed content |
| ENT-01..07 | Protocol prepared; all target trials NOT RUN | Actual selector/critical screens, persistence, protected settings, reversal and relevant combined-resource behaviour; EN-01..03 remain unvalidated |
| FTT-01..12 | Host subcases only, chiefly queue/fault/TLS/hash portions of FTT-03..09 | No native-origin FTT-01; real RAW/JPEG/large/non-ASCII handling, physical Wi-Fi faults, target lifecycle/shutter and performance are untested. FT-01..04 remain unvalidated |
| CLT-01..11 | Protocol prepared; all physical trials NOT RUN and deferred | Distinct still routing, measured repeatability, preview/transition/preservation/mode results and approved inverse. Custom looks repeat applicable trials only after their own domain/slot/calibration proof; CL-01..05 remain unvalidated |

Host error injection is not a real full disk, Wi-Fi disconnect, camera reboot or
card removal. A complete upload read-back from the custom peer is not native
camera-origin proof. Unsupported combinations remain explicit; no acceptance
threshold is reduced to turn preparation into a pass.

## Smallest existing owner-observation packet

[TARGET_EVIDENCE_GAPS](TARGET_EVIDENCE_GAPS.md) and
[DEVICE_FACTS](../templates/DEVICE_FACTS.json) already prepare the first contact.
Existing owner records can supply facts privately without any camera operation.
The owner already answered Unknown; this audit does not repeat that request.
The intake also preserves missing modification/repair history, ordinary health,
connection/apps, power/card readiness, repair-risk tolerance and independent
backup-storage availability. Those facts constrain their applicable later
operations; they do not turn the first UI observation into a service procedure.

When separately approved, begin only with ordinary model/label, Version and full
Language-menu observations, retaining original-language context and keeping any
serial-bearing original private. Do not confirm a reset/format or select a
firmware update. English already offered selects the normal-menu branch before
any unlock proposal. Any subsequent normal selection still needs its applicable
owner approval; viewing the list is not permission to mutate settings.

USB identification, service authentication/native execution and persistent
settings/program changes remain separate R1/R2/R3/R4 decisions. No launcher,
driver change, service command, firmware operation or camera command is proposed
by this audit. Unknown ports/apps/readiness do not justify probing them.
Backups, an executor, another lab or a CI result add no new gate before the
ordinary separately approved UI observation.

## Next single substantive package

**RA-003 exact-build intake**: reconcile observed installed firmware with a
legitimate matching package, record source provenance/unchanged hashes privately,
and use an applicable reviewed parser on new private copies. Installed-version
evidence and legitimate matching input are the present missing inputs. A public
2.00 listing cannot replace either. If that exact package is unavailable, record
the availability gap rather than updating the body to match a convenient file.
An alternative device-read route would require its own reviewed proposal and
approval.

Available target-independent preparation is exhausted for the current scope:
final-code clean reproduction and actual CI are observed, the bounded
official-source refresh is recorded, and every remaining substantive requirement
has a named owner/target/external input above. This is not completion of the
camera research goal. New legitimate inputs or a selected deployment peer can
make further useful host work possible. No additional generic tooling package is
required before the owner chooses to supply the existing UI observations.

Camera commands in this audit: **none**. Tests run by this audit: **none**;
results above reference the recorded qualification sessions. No feature support,
device-write gate, acquisition or recovery claim is established.
