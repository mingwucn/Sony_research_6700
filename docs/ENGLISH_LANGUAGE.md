Current EN-101 evidence (2026-10-23): [finite feasibility dossier](../research/ENGLISH_FEASIBILITY.md). Ten critical native surfaces are tabulated; every resource/rendering result remains unverified. No unlock mechanism or EN acceptance gate passed.

# English-language enablement: target-specific design

Goal: native English menus, warnings and messages on the owner's ILCE-6700, without transplanting another region's complete identity or settings. Owner reports α6700 version 2.00, current 简体中文, Chinese mainland version and English unavailable (source-report, 2026-10-18). The exact SKU, complete offered-language list and binary/resource identity are unverified. See [latest intake](../research/sessions/20261018-owner-mainland-english.md). Sony's normal Language page is source S2 in REFERENCE_ANALYSIS.md. Work packages EN-101 through EN-104 apply.

## 1. Owner observation and the no-modification branch

For this body, the owner reports English absent: continue with the resource/policy hypotheses below, without requesting a repeat full-list check merely to establish that absence. This does not prove English resources are absent or a simple unlock exists. The generic decision branch remains: if later evidence shows English is already offered, use normal menu selection with the owner's approval, document the result, and close the unlock investigation as unnecessary for this body. A computer's English UI, a multilingual manual or a global firmware-download page is not evidence that English is selectable on a domestic camera.

Keep the reported mainland market label separate from an exact regional SKU or internal product identity. A full offered-language transcription remains useful supporting evidence when available; it is not required to record the explicit report of English absence. Preserve the original language and any visible region-related settings. No candidate may globally change region identity merely to expose English.

## 2. Hypotheses and distinguishing evidence

| Hypothesis | Evidence needed | Smallest implementation direction |
|---|---|---|
| English resources exist; language-specific allowlist blocks selection | Native resource IDs/text/glyphs are present; language-list construction reads a narrow configuration field | Scoped native-setting or language-mask change |
| English resources exist; a program policy restricts them | Configuration is insufficient, but the exact language-policy consumer is traced | Small exact-source AP/resource-policy change |
| English resources are missing or incomplete | Inventory and native resource decoding show absent critical strings/layouts/fonts | Same-model/same-build resource integration study |
| Product-region setting controls language and unrelated capabilities | One field has multiple proven consumers | Do not globally change the field; isolate language policy or keep blocked |
| Language support depends on an unreviewed service route | No safe exact-target read/write semantics | Continue offline; do not run a generic unlocker |

Use both resource presence and code/data-flow evidence. Finding the ASCII string English is insufficient: it may belong to help text, a remote protocol or another inactive resource set. Compressed resources require a validated parser before an absence claim.

## 3. Offline localization map

Identify the language enumeration, locale-to-resource mapping, available-language construction, current-language storage, defaults/reset sources, native setters and persistence operation. Record firmware object hashes and all field widths, endian rules, checksums/attributes and bounds.

Trace every consumer of a proposed configuration field. The desired change is language permission, not a blanket destination/region conversion. Keep radio bands/channels, regional compliance configuration, certification, video-system settings and other unrelated behaviour unchanged unless an independently scoped owner request is made. No regional-regulation interpretation is needed to justify this engineering boundary: those settings are simply outside this feature.

A same-model and same-build multilingual sample can be a useful comparison, but its complete settings must never be written onto the owner's body. Compare logical fields and resource formats, allowing for device-specific data and firmware packaging. Distinguish compiled defaults from the current persistent setting, and both from the list visible in the running process.

Document a native resource test plan covering ordinary menus, modal warnings, date/time setup, network authentication, playback, reset confirmations, firmware/version screens and accessibility messages when present. Avoid destructive actions to generate warnings; inspect dialogs without confirming format/reset, or use safe preconditions.

## 4. Preferred change: scoped persistent setting

Use this route only after the exact field and save semantics are established. Take a fresh snapshot of the owning settings unit and protected fields. Read the current value/attributes, compute a minimal modification of the confirmed language bits or selected-language enum, and preserve every unrelated bit. Use the native API only if its actual object scope and persistence operation are understood.

If the native API rewrites a larger unit, construct it from the fresh unit, not a donor or old backup. Read back the entire owning unit, compare all unaffected fields, and repeat the logical language read after normal reload. The inverse restores only the field changed by this operation, merged into fresh current state; it must not roll back newer owner settings.

A write timeout is ambiguous even for a one-byte change. Do not replay the write/save sequence until the current value and completion state are reconciled. Enter needs_review under ACCESS_AND_RECOVERY.md.

## 5. Alternative: narrow program/resource change

If a setting-only route is disproved, map the language-specific policy function and its callers. Validate its behaviour for all currently available languages, invalid locale values and reset/default states. Construct an exact-source bounded patch with expected bytes, complete program hashes and a tested inverse. Do not disable an entire product-identity check if a narrow language rule can be isolated.

Resource integration is a separate project increment. Require compatible IDs, string encodings, layout variants, fonts, resource indexes and integrity fields for the exact build. Missing warnings or modal strings can make a camera operationally unsafe even when its main menu looks correct. A whole A7C II/A7CR language package is not an alpha6700 resource patch.

If resource coverage cannot be established, return a precise coverage gap and needed same-build source. Do not install a partly translated package merely because most menu labels render.

## 6. Hardware experiment order

Record the original language and safe navigation route back. Apply only the approved English change, not FL23 at the same time. Verify complete readback and any required target-specific reload. Check the current-language selection, language list, primary menus, warnings and display text. Then test normal shutdown, sleep/wake and complete power removal after all I/O ends.

Confirm that stills, playback, Wi-Fi, USB and previously configured recipes still operate. Compare protected settings, including any region-linked fields discovered during analysis. Menu appearance alone cannot prove that a broad destination value had no side effects.

Exercise reversal on a working body when approved: use normal language selection or the exact inverse, then verify the original language and unchanged unrelated configuration. Reset-to-factory behaviour is a separate test requiring approval; it is not part of the default unlock procedure. A whole-camera reset is not used as a convenience to fix a language list.

## 7. Interaction with Creative Looks and FTP

English enablement may activate resource paths not exercised by the original region. Custom-look names must render there, and unimported slots must keep native dynamic titles. New FTP settings, dialogs and error strings must not reference resources absent from English. Design a shared resource-ID registry to detect collisions between feature candidates.

Combined uninstall must preserve the owner's currently chosen language when removing only FL23/FTP. Removing English support while leaving English selected may be an invalid state; define an explicit migration to an available original language before uninstalling resources or permission changes. This dependency must be encoded, not left to a manual guess.

## 8. Acceptance and failure conditions

EN-01 passes when English is native and all selected critical strings render correctly. EN-02 passes when normal/complete power cycles preserve the selected state and a controlled inverse works. EN-03 passes when target-specific protected-state comparison and regression tests show no unexplained side effects. Reset and future official updates remain separately qualified unless tested.

Stop for missing glyphs, invalid-string/resource reads, reboot loops, an unexplained regional-setting difference, uncertain save completion, or a non-reversible shared field. Preserve the evidence and choose a narrower hypothesis; do not compensate by changing the complete destination identity.

## 9. Deliverables

Produce a language/resource coverage table, typed configuration schema, field-consumer map, implementation decision record, candidate/inverse if required, preservation report and native-screen/persistence test results. Include a clear no-modification result if normal English selection already solves the owner's body.
