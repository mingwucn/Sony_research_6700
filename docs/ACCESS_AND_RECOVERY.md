# Access, backup, persistence and recovery engineering

Read AGENTS.md first. This document specifies gates and experiments to be implemented locally. It deliberately contains no guessed alpha6700 service command, partition writer or firmware address.

## 1. Risk tiers

| Tier | Activity | Initialization status |
|---|---|---|
| R0 | Offline local-file reading, analysis and synthetic tests | Available; no camera contact |
| R1 | Normal camera UI observation and ordinary USB descriptor/identity queries | Requires owner-approved local observation; does not include mode changes |
| R2 | Service authentication, USB re-enumeration, temporary uploads/native execution, elevated diagnostics | Not yet established for this target; separate approval and source review |
| R3 | Native persistent-setting writes/saves | Blocked until exact field semantics, backups and inverse are established |
| R4 | Program/resource-file modification and related retained-state operations | Blocked until the full write gate passes |
| R5 | Bootloader/NOR/raw-partition replacement, calibration transplantation, hardware recovery experiments | Outside the current scope |

A command advertised as read-only can still switch USB mode, execute privileged code or create temporary files. Classify by actual side effects. The reference FL23 Backup/Check preparation is an R2-style operation, not R0/R1 [R1 installation guide in REFERENCE_ANALYSIS.md]. Firmware updater mode and service mode are distinct paths; success in one is not evidence for the other.

## 2. Acquisition decision tree

First collect the version/language/menu facts from the body and the host's normal USB descriptors. Do not use another model's VID/PID to replace a driver. Prefer ordinary installed OS tools for descriptor observation; record both vendor/product IDs and interface-level information, without publishing serials. Close competing camera applications before an approved protocol session. Do not disable OS security broadly to make a tool run.

Next obtain the matching official package where possible and analyze it offline. Audit the extractor before use, retain original bytes and verify extracted lengths/container checksums. Never run extracted programs on the host. Distinguish ELF headers, raw images, filesystem images and update containers rather than selecting a parser based only on a suffix. If components are encrypted or opaque, document exactly what is missing. Do not manufacture a decrypted result.

Then inspect candidate service tooling at a pinned revision. Trace the startup path through enumeration, authentication, re-enumeration, native helper loading and result handling. Inventory all temporary paths, remounts, native write/save calls and cleanup behaviour. Identify hard-coded models, product indices, addresses, return structures and worker ABIs. A reviewed source path must exist for the target; removing a check is not a compatibility test.

An R2 proposal must include a bounded goal, expected inputs/outputs, code and asset hashes, every intended side effect, power requirements, timeout behaviour and the procedure for reconciling an uncertain result. Run host-side transport mocks first. Real authentication is not attempted until the owner approves this proposal.

## 3. Required original-state coverage

Create a catalogue of every object a planned feature could mutate, plus surrounding/protected state. At minimum investigate application programs, image-processing programs, resources, product-feature configuration, user settings, device-specific calibration, filesystem metadata and boot-loading state. Actual alpha6700 paths, unit IDs and storage layout remain unknown until observed.

For immutable programs, obtain two independent reads when feasible, compare complete sizes/hashes and retain an independent copy on another drive. A second copy of one read protects storage failure but is not a second acquisition. For settings, collect separate snapshots and classify changeable counters before comparison. Never repeatedly write snapshots back to make them match.

Record gaps: inaccessible calibration, regions only available through a package, volatile state not captured, or recovery requiring a still-booting OS. An application-file backup must not be called a complete firmware backup. Preserve the original acquisition forever; later feature changes use fresh current-state captures and a separate known-good catalogue.

Store a private manifest containing body alias, acquisition method, model/version evidence, logical object ID, actual local path, camera path when known, length, hash, read timestamps, tool revisions and classification. The committed starter intentionally emits no original filenames or paths and does not authenticate any model identity.

## 4. Storage and executable mapping

Before candidate generation, document the target's AP/CP architecture, endian mode, instruction state, program segments, relocation rules and file-to-memory translations. Use at least two independent anchors for every critical function: for example a resource/string xref plus control-flow/data-flow correspondence. Similar instruction bytes alone are not sufficient. Include all incoming branches, return behaviour, caller-saved/callee-saved state and literal/data references.

For each candidate placement, prove that bytes are loaded, mapped with appropriate permissions, within lifetime, and not used as initialized data, BSS, stacks, DMA buffers or a different overlay. Scan references and loader behaviour. Zero-filled space or an executable page flag alone is not proof of safe free space. No growth/repacking is allowed merely because a tool can write a larger file; validate the actual loader/container constraints first.

For each changed storage object, establish mount/filesystem behaviour, file length/inode requirements, atomicity limits, synchronization requirements and readback mechanisms. Reference ext2/vfat devices and partition numbers are not alpha6700 facts. Device-specific planning must decide whether fixed-window writes, native settings APIs or another supported mechanism is appropriate.

## 5. Persistence and retained-state investigation

Separate four questions: what is stored, what saved settings will restore, what program/runtime state is currently active, and what a normal or complete power cycle reloads. Identify any retained image/snapshot mechanism from target evidence. Do not invoke the reference WBI functions or delete snapshot files based on matching names.

Observe unmodified startup behaviour first. After any approved future change, compare complete storage and selected runtime evidence where access is justified. AP runtime observations do not establish running CP instruction contents. CP disk hashes do not establish CP execution. A physical effect can support activation without proving every internal address hypothesis.

Any reload is scheduled only after all I/O is complete and the current state is reconciled. Full power removal means accounting for USB/other external power as well as the battery. Derive the actual procedure and wait conditions from target evidence; a one-minute instruction for the reference body is not automatically an alpha6700 requirement. Never repeatedly flash to fix a stale loaded state.

## 6. Future transaction contract

The device executor must use a private append-only journal with operation ID, body/source identity, command category, candidate hashes, before-state evidence, requested change, response and verification status. Flush a prepared record before sending a mutating request. Store no credentials in the journal. Define explicit legal transitions:

```text
unidentified -> identified -> access_reviewed -> acquired -> analyzed
-> candidate_prepared -> approved -> applying -> readback_verified
-> reload_pending -> runtime_checked -> physical_checked -> accepted
```

Any ambiguous operation enters needs_review, which is not a retry state. A restoration operation has its own prepared/approved/applying/verified sequence and exact expected current source. The journal is evidence, not authority: editing a status field cannot bypass fresh checks.

Do not pretend several files plus saved settings form a single atomic transaction. Establish a target-specific dependency order and analyze every interruption boundary. Journal which operation completed. Stage and validate locally first; use native checks without writes only after their effects have been audited. Read back complete changed files/units and verify protected data, not just patched windows.

A settings change requires read-modify-write semantics over a proved field, preserving unrelated bits/attributes, plus the exact persistence operation and readback. A whole-unit rewrite may still be necessary under a native API, but it must use the freshest current unit and prove preservation. Unknown changing fields are not automatically ignored.

## 7. Recovery matrix

| Observed condition | Permitted response pattern | Prohibited assumption |
|---|---|---|
| Offline mismatch | Stop candidate generation; retain inputs and diagnostics | Changing a declared hash makes bytes compatible |
| Standard read fails before any mode change | Investigate host/cable/session state with bounded, reviewed reads | Failure justifies switching into service mode |
| Service transition or temporary execution uncertain | Retain power/connection state and reconcile known results | Relaunching the whole tool is harmless |
| Write response lost, completion unknown | needs_review; inspect existing journal/results and independently read state only when safe | Timeout means nothing was written |
| Readback verifies but old behaviour persists | Analyze saved/runtime/retained state | Another flash will force activation |
| Body boots with a reproducible functional fault | Use a reviewed exact inverse only after current-state and access checks | Any older backup is appropriate |
| Boot loop or no service access | Stop repeated attempts; document the actual recovery envelope and repair options | A service restore button or SD updater is guaranteed to work |

Do not intentionally interrupt power during a real firmware write to test the journal. Simulate faults on the host. Deliberate destructive hardware fault injection requires another project scope and recovery capability. A successful same-byte or inverse write still carries hardware risk; it is not a free preliminary test.

## 8. Write gate checklist

Owner recommendation adopted on **2026-10-18**: establish a verified rollback and
recovery system **before any firmware/program write**. Current status:
**NOT ESTABLISHED; firmware writes remain blocked**. The offline inverse model
and synthetic journal are preparation only. This requirement does not authorize
a restore, same-byte write, reboot, service transition or destructive test.

Before a firmware/program-write proposal can pass, RA-005/006/007 must establish:

- Original stock and latest known-good states, complete coverage of every object
  the proposal can change, fresh source identities, and verified copies on two
  independent storage devices. Restore must preserve this body's calibration,
  regional/radio identity and unrelated current settings.
- An exact inverse for the specific current candidate, plus a reviewed restore
  sequence, full readback/protected-state checks and explicit stop conditions.
- An exact-target recovery matrix covering an ordinary functional regression,
  partial/unknown completion, failed normal boot and unavailable service access.
  Each route needs evidence of its prerequisites and reachability for that
  failure state. A restore that needs a working camera OS does not cover a boot
  failure; a service route does not cover loss of that service route. Unsupported
  states remain blockers for any write relying on recovery from them.
- Recorded verification evidence and a separate owner-approved restoration
  procedure. Do not brick the body or interrupt live writes to demonstrate a
  route. If adequate recovery cannot be established within scope, continue
  offline research and leave the firmware-write gate closed.

No automatic rollback follows a timeout or disconnect: enter needs_review and
reconcile the actual state before proposing a separately approved restore.
Bootloader/NOR/raw-partition or calibration replacement remains outside scope;
do not assume an A/B boot slot, Sony updater rescue or donor-body recovery exists.

The owner/reviewer must be shown the exact body/build/source identities; scoped feature and changed objects; complete backup coverage and independent copies; candidate/inverse hashes; source and control-flow review; protected-state comparison; target-specific write/reload sequence; simulated failure results; power/cable/single-owner conditions; and conditional recovery limits. The code must independently recheck eligibility immediately before mutation.

No public installer is permitted before these checks are machine-enforced and tested against wrong/partial/mixed sources. A graphical confirmation button is not a replacement for technical preconditions. The starter repository has no executor and intentionally cannot pass a device-write gate.
