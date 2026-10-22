# EN-101: native English feasibility and critical-resource coverage

2026-10-23. Evidence: **source-report**, **static-inference**. Camera commands:
**none**. This is the missing finite preparation dossier required by
[EN-101](../docs/BACKLOG.md#en-101--resolve-languageresources-and-the-no-change-option),
[the language design](../docs/ENGLISH_LANGUAGE.md) and Master Plan M3. It does
not establish a usable unlock or pass EN-01, EN-02 or EN-03.

## Observations and their limits

| Question | Existing evidence | Conclusion |
|---|---|---|
| What body/version does the owner report? | [Owner intake](sessions/20261018-owner-mainland-english.md): a6700, 2.00, mainland China, current 简体中文, English unavailable. | Source-report only. Do not repeat generic language-list intake to establish absence. Exact SKU/internal identity and installed program/resource hashes are unverified. |
| Is a matching version-labelled package known? | [Official mainland source](MAINLAND_FIRMWARE_SOURCE.md), [acquisition report](sessions/20261018-RA-003-package-law.md) and [stream validation](FDAT_STREAM_VALIDATION.md). | Official version-labelled bytes and bounded package/stream lineage were recorded. A matching version string does not establish correspondence with the installed body's programs, resources or persistent configuration. No firmware was reopened for this dossier. |
| Have English strings/fonts/layouts been decoded? | [Component-prefix](COMPONENT_PREFIX_AUDIT.md), [tar inventory](TAR_LINK_INVENTORY.md) and [fixed-superblock observation](EXT_SUPERBLOCK_OBSERVATION.md) report container/filesystem metadata only. | No accepted per-resource language inventory or language-policy mapping exists. Neither English presence nor absence is proved. |
| Does the newly reviewed reference offer English enablement? | [Pinned reference update](sessions/20261022-a6700-reference-update.md): English was absent from the reviewed six-feature catalog. | No English mechanism was found in that reviewed scope. This does not prove that the camera lacks resources or that every possible method is impossible. |
| Is recovery established? | [Pre-contact matrix](PRE_CONTACT_DECISION.md) and [target evidence gaps](TARGET_EVIDENCE_GAPS.md). | No target-specific inverse or failed-boot recovery has been established. Required before any applicable write; not a prerequisite to ordinary approved observation. |

## Critical-resource coverage

Every row below is **UNVERIFIED / NOT RUN**. No resource IDs, file offsets,
runtime addresses, configuration fields, font identities or coverage percentages
are invented. The table distinguishes a resource inventory from eventual native
rendering: either can fail independently.

| Native surface | Offline evidence needed | Later physical acceptance |
|---|---|---|
| Language selector, current selection and original-language route | Locale enumeration, selector construction, selected/default storage and consumers; original Simplified Chinese remains available. | ENT-01 and ENT-06: deliberate English selection and controlled reversal. |
| Main shooting/setup menus | English resource IDs, indexes, encodings, glyph coverage and layouts for critical labels. | ENT-02/03: no blank/truncated critical instructions or invalid resources. |
| Shooting status and nondestructive warnings | Resource references for storage/battery/capture warnings and their reachable dialog paths. | ENT-02/03: safe warning conditions only; do not create damage or confirm destructive actions to obtain evidence. |
| Playback and file-operation dialogs | Playback labels, error strings, referenced fonts/layouts and complete resource resolution. | ENT-03; destructive deletion is not part of the first observation. |
| Wi-Fi and authentication | Native network setup, credential/error dialogs and resource dependencies. | ENT-03; credentials and captures remain private. No authentication bypass. |
| Date/time and initial-setup messages | Locale/date formatting paths, related strings and compiled versus saved defaults. | ENT-03; observe without changing the clock or initializing settings. |
| Version/system information | Version/help labels and resource mapping for this exact build. | ENT-03; reading a screen does not establish installed binary identity. |
| Format/reset confirmations | Complete warning and confirmation resources and safe navigation paths. | ENT-02 only if later approved and reachable without confirmation; no format/reset operation. |
| Accessibility or other critical modal messages, if present | Establish whether each surface exists, then inventory reachable resources/fonts/layouts. | ENT-02/03; absence of an unsearched string is insufficient. |
| FTP dialogs and error/status resources | Target-native FTP UI/backend correspondence, resource-ID ownership and English coverage. | ENT-07 only after independent FTP feasibility. A visible menu is insufficient. |

ENT-04 persistence, ENT-05 protected-state preservation and ENT-06 reversal are
also **NOT RUN**. They require a separately accepted exact-target mechanism and
applicable device approval. ENT-07 looks/custom-name interactions remain deferred
with the looks track; it must not delay the first English feasibility result.

## Narrow hypotheses and falsifiers

1. **Existing complete English resources, language-specific selector restriction.**
   Test by mapping the exact resource coverage above and tracing the complete
   selector/configuration consumers. Missing critical resources falsify the
   complete-resource premise. A field affecting unrelated product/radio behavior
   falsifies a proposed narrow field-only change unless its language effect can
   be isolated. A string named English alone confirms neither premise.
2. **Complete resources, program-level language policy.** Trace the actual
   selector call chain with source object hashes and typed address domains.
   No reachable policy consumer or incomplete English coverage leaves this
   route unestablished. No model-guard bypass or donor offset is proposed.
3. **Missing/incomplete resources.** An accepted exact-build inventory and
   decoder must show the specific missing critical resources; an opaque container
   or failed search cannot do so. This would require a separate same-model,
   same-build resource integration study, with compatibility evidence, before
   candidate construction. Whole donor settings or regional identity are excluded.

No route is selected. No patch candidate, typed target configuration schema,
field-consumer map or inverse exists. This dossier completes the evidence table
and falsifiable investigation plan; EN-101's target mechanism/resource acceptance
remains incomplete.

## Finite next evidence and stopping point

The next useful **offline feature evidence** is an accepted matching resource
inventory and locale-selector consumer map. The current synthetic runtime work
does not produce those inputs. Its endpoint is qualification of the existing
host preparation path, not successive receipt frameworks.

The separately prepared [Windows R1 inventory packet](../docs/WINDOWS_USB_OBSERVATION_PACKET.md)
remains held. It can later help with host/device identification, but cannot prove
English resources, native FTP or rollback. It requires the owner's later change
to the contact hold and separate scoped approval for the prepared query; no approval is requested
here. No extra bootstrap receipt join or R4 recovery demonstration is a blanket
prerequisite to that first R1 observation.

Native FTP remains a separate primary track: the [source-chain audit](FTP_SOURCE_CHAIN_AUDIT.md)
and [session-lifetime review](PRE_CONTACT_DECISION.md) establish concrete adoption
gaps, while camera-resident origin, transfer equality and lifecycle remain unproved.
An optional host-assisted bridge cannot close that requirement. FL2/FL3 and custom
looks remain deferred. No feature, recovery or device-write gate passed.
