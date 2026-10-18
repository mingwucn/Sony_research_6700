# Reference assessment and source register

Inspection date: 2026-10-18. The live GitHub connector was used to resolve revisions and read current files. The initially retrieved A7C II web page contained an older layout than the live repository. The locked Git commit, not a cached page or mutable release attachment, is the reproducibility anchor.

Local RA-002 follow-up: [reference code and reuse-rights audit](../research/REFERENCE_AUDIT.md) verifies the locked R1/R2 source trees, traces entry/transport/native paths and records component-specific rights. PMCA candidate provenance is now pinned to `a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0`; all 19 files in R1's vendored subset match that revision. The initial observations below remain historical; the audit does not adopt newer R1 commits, third-party code or any alpha6700 access route.

## 1. Pinned references

| ID | Source | Exact identity used |
|---|---|---|
| R1 | QAQLeonard/a7c2-fl23-research | c0930d5b0ccd49c0a092dc883054cd6dce199649; commit dated 2026-10-18 |
| R2 | lzh2016zzz/a7cr-fl23-research | 43ba74441c8f10459ade41e84a379ad8005e6ef4; commit dated 2026-10-16 |
| R3 | ma1co/Sony-PMCA-RE candidate provenance | Full commit a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0 verified in RA-002; initial README blob 1c47cad4ceffcc0dfd574c83badbb1026419d6ee matches; tool/target support not validated |

R1 now has src/fl23, src/looks and docs/en. Historical look-toolkit paths and preview ZIP names from older descriptions should not be assumed current. Release downloads can change independently of a checkout; record their separate SHA-256 values before any use.

### R1: what was actually inspected

Read docs/en/fl23.md, docs/en/ai.md, docs/en/technical/integration.md, docs/en/technical/failures.md and src/fl23/core.py, plus directory metadata. This was a targeted source/design inspection, not a full audit or execution of all upstream code.

The core pins ILCE-7CM2 2.01 and exact AP/CP source and result hashes. Its planning logic checks edit bounds, original bytes, overlapping windows, full result hashes and preservation of existing colour records. These are useful patterns for an independently derived alpha6700 backend; changing the model/version constants would not port the implementation. The device-side native helpers and every transport dependency still need local review before reuse.

The FL23 guide distinguishes preparation, installation, reload and verification. Its preparation stage executes temporary native diagnostics, so it is not equivalent to host-only hashing or ordinary USB identity reads. Restoration is conditional on known current sources and retained access.

The custom-look integration notes describe a fitted native representation, ST-dependent routing and separate resource/settings/preview work. They report one-body photographic success, but distinguish it from unrecorded post-reload machine checks and unobserved running CP instruction memory. Do not transfer that evidence to this body. Earlier failures include restart loops and stale preview despite functioning photos. Those motivate separate physical tests, not a claim that identical failures will occur on an alpha6700.

### R2: its value and limits

R2 documents the AP/menu-to-CP-processing chain for ILCE-7CR 2.01 using ILCE-1M2 4.00 look data. It separates slot identity, UI identity, CP mode, gamma, colour parameters, saved settings and metadata. Some longer patch blocks and code are omitted, so the document cannot reconstruct a complete working patch by itself. Its latest metadata/default changes are not presented as fully validated across restart and new captures.

Use it to build a target investigation checklist and understand layer separation. Do not copy its offsets, Backup IDs, boot functions, partition devices or calibration into an alpha6700 candidate. The initial inspection found documentation rather than a reusable implementation; review rights before copying nontrivial material.

### R3: access research lead, not a supported alpha6700 recipe

The PMCA README distinguishes Android app installation, updater-mode execution and service mode. Compatibility and driver requirements differ; the updater route explicitly excludes some signed architectures. This does not establish support for the owner's alpha6700. OpenMemories/PMCA language-unlock advice for older bodies is not a substitute for exact-model evidence. Locally inspect the relevant implementation and compatibility records before proposing a command; do not run serviceshell or updatershell as a speculative probe.

## 2. Primary documentation and implications

| ID | Primary source | Observation and bounded implication |
|---|---|---|
| S1 | Sony alpha6700 Creative Look guide | Ten listed native looks and six custom recipe slots; recipe customization is not arbitrary still-photo LUT import |
| S2 | Sony alpha6700 Language guide | Documents normal language selection; does not prove that English is selectable on every regional SKU |
| S3 | Sony alpha6700 menu list | Inspected network menu has no FTP item; absent documentation does not prove an absent binary backend |
| S4 | Sony alpha6700 PC Remote guide | Wi-Fi/USB remote operation and computer image storage are described; useful for a separately labelled bridge |
| S5 | Sony Camera Remote SDK page | Lists ILCE-6700; per-device interfaces and functions must be checked in the selected SDK's API reference |
| S6 | Sony alpha7 IV FTP Transfer guide | Provides a native FTP behaviour reference and possible donor-selection starting point, not binary compatibility proof |

The official alpha6700 firmware-download listings timed out during the initial session. No current/latest alpha6700 firmware version is asserted. Local development should record the exact installed version and retrieve official release notes independently. Sony's general SDK advice to use current firmware must not trigger an automatic update of a research body; assess baseline and access consequences first.

## 3. Reuse boundary

| Reuse as a method | Re-derive for the alpha6700 |
|---|---|
| Exact-file hashes and expected-byte edits | Whole-file source/result hashes |
| Forward/inverse transaction descriptions | Storage objects, safe write granularity and restore sequence |
| Separating menu, processing, settings and metadata | All enums, feature columns, resource IDs and conversion tables |
| Preserving unrelated records | Target calibration boundaries and dynamic-setting rules |
| Distinguishing storage and loaded state | Boot cache/snapshot mechanisms and proof of reload |
| Separate preview and captured-photo testing | Target display/processing/cache paths |
| Bounded initial-read retry design | Exact protocol semantics and target-specific USB identities |
| Calibrated domain fitting | Alpha6700 sensor/ST response and each input profile's domain |

Keep source-reported values in a clearly labelled reference-only table if needed for comparison. Do not put them in an executable target profile. A second implementation on A7C II demonstrates that model adaptation is possible in that case; it does not establish a uniform offset delta or universal platform compatibility.

## 4. Links for local investigation

R1 root: https://github.com/QAQLeonard/a7c2-fl23-research/tree/c0930d5b0ccd49c0a092dc883054cd6dce199649

R1 core: https://github.com/QAQLeonard/a7c2-fl23-research/blob/c0930d5b0ccd49c0a092dc883054cd6dce199649/src/fl23/core.py

R1 installation: https://github.com/QAQLeonard/a7c2-fl23-research/blob/c0930d5b0ccd49c0a092dc883054cd6dce199649/docs/en/fl23.md

R1 integration: https://github.com/QAQLeonard/a7c2-fl23-research/blob/c0930d5b0ccd49c0a092dc883054cd6dce199649/docs/en/technical/integration.md

R1 failures: https://github.com/QAQLeonard/a7c2-fl23-research/blob/c0930d5b0ccd49c0a092dc883054cd6dce199649/docs/en/technical/failures.md

R1 AI guide: https://github.com/QAQLeonard/a7c2-fl23-research/blob/c0930d5b0ccd49c0a092dc883054cd6dce199649/docs/en/ai.md

R2: https://github.com/lzh2016zzz/a7cr-fl23-research/blob/43ba74441c8f10459ade41e84a379ad8005e6ef4/README.md

R3 (RA-002 pinned candidate revision; target support remains unvalidated): https://github.com/ma1co/Sony-PMCA-RE/blob/a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0/README.md

S1: https://helpguide.sony.net/ilc/2320/v1/en/contents/0411B_creative_look.html

S2: https://helpguide.sony.net/ilc/2320/v1/en/contents/0601_language.html

S3: https://helpguide.sony.net/ilc/2320/v1/en/contents/221h_list_of_menu_items_ilc2320.html

S4: https://helpguide.sony.net/ilc/2320/v1/en/contents/0903_pc_remote_function.html

S5: https://support.d-imaging.sony.co.jp/app/sdk/en/index.html

S6: https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000653558.html

This register establishes what was read, not ownership of Sony firmware or permission to redistribute profile data. New authored tooling remains separate from any later third-party integration.
