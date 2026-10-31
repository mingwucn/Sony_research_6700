# English restriction: native converter and memory-map evidence

2026-10-26. Evidence: **static-inference**, **offline-tested**, and retained
**source-report** provenance. Goal active/incomplete. Camera commands: **none**.
Network commands: **none**.

The mainland Chinese 2.00 package contains the English resources already
documented in the [firmware findings](../ENGLISH_FIRMWARE_FINDINGS.md). The
separate language availability and selection paths continue to support a
language-only route in static analysis. This continuation identifies the
previously missing native converter definitions and a corroborated section
layout. It does not establish a working unlock or complete regional preservation.

The owner explicitly authorized reverse engineering the mainland Chinese
firmware for research during this session. The working objective now records
that authorization and retains offline-only analysis, preservation of regional
settings and no camera contact. The goal tool cannot edit an active objective's
text; the clarified objective is saved in project state and handoff. The active
app-level goal remains unfinished.

## Findings

Three fresh authored bounded observers retained six selected file spans,
860,160 bytes in total. Each operation checked the complete original package,
decoded stream, all 1,000,017 physical envelopes and the entire exact
248,637,568-byte warm-boot member against the earlier identities. No complete
warm-boot file was retained and no firmware code was executed.

The tail contains a structurally consistent table of 1,314 records. All records
pass the reviewed alignment, size, flag and interval checks. Their stored-size
and memory-size totals independently reproduce two header fields, and the
stored-size sum places the table exactly after the serialized payload. There
are 1,267 records with equal stored and memory sizes and 47 with no stored
payload. The latter do not by themselves prove zero-fill behavior. Remaining
tail bytes are uninterpreted.

The inferred section layout predicts a native image start. A separate bounded
capture at that file position has a conventional AArch64 Image header. Its text
offset agrees with the section record and the already retained device tree's
memory base. Thousands of export-like name references independently agree on
the local static relationship between stored code values and file positions.
These checks corroborate this packaged layout; they do not establish a running
camera's mappings or a complete native loader implementation.

Both missing converter definitions now have separate export-name, native-code
and diagnostic-reference anchors. The narrow integer conversion branch is
identified. The cache converter contains additional guarded branches and system
instructions whose complete behavior remains unreviewed. A local function
identification is not a complete address-conversion contract or a safe device
operation.

The packaged program-address value lies in a 20 MiB gap between inferred
section intervals. It is not covered by any of the 1,314 records, including
records with no stored payload. The device tree declares the enclosing memory
but does not classify this gap through a reservation entry. This explains why
using a simple whole-file address subtraction was unjustified. It does not
prove that the separate program is absent from memory or identify its producer.

The initial four-label producer association was numerically ambiguous: the
same pointer values also resolve to a different real string group. That lead
was corrected before any mapping claim. Producer diagnostics refer to
sections, pages, compression and warm-boot operations, but their control flow
and exact header-field use remain unbound.

## Verification and limits

The isolated decoder interpreter was CPython 3.13.12. Exact root commands,
exit codes, dependency receipts, hashes and worker commands are retained in
ignored private evidence. The main root commands were:

```powershell
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-wbi-provider-20261026/capture/read_spans.py --self-test
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-wbi-provider-20261026/capture/read_spans.py
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-wbi-provider-20261026/capture-native-tail/read_spans.py --self-test
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-wbi-provider-20261026/capture-native-tail/read_spans.py
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-wbi-provider-20261026/capture-kernel-header/read_spans.py --self-test
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-wbi-provider-20261026/capture-kernel-header/read_spans.py
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-wbi-provider-20261026/audit_mapping.py
```

All exited 0. The same 110 invented observer cases passed for each new entry;
these are 110 distinct cases, not 330 distinct cases. The independent direct
table/header/export-anchor audit passed. Synthetic byte-selection checks do
not test native behavior. The final retained-evidence verification separately
checks current worker packets, earlier private packets and unchanged public
parser/test sources.

The live settings header and selected catalog, actual startup parameters and
memory lifetime, separate program bytes and selected-language clients remain
unbound. The original 119 inspected registration sites, 54 synchronous numeric
origin gaps and one forwarded asynchronous origin gap are unchanged. Complete
regional/calibration preservation, physical rendering, persistence, inverse and
recovery remain unproved. No feature or device-write gate passed.

All new outputs are durable ignored private evidence or sanitized project
reports. No disposable scratch was created; earlier preserved scratch was not
deleted. No camera command, mount, emulation, firmware execution, patch payload,
source mutation, stage, commit, push or external submission occurred.

Next single work package: **EN-101: trace the source and boot handoff of the
separate program in the interval omitted from the corroborated warm-boot section
layout. Start with exact retained boot/updater configuration and native loader
references, then select another component only when that provenance identifies
it. Complete the converter's remaining guarded/system-instruction semantics
where needed for that handoff. Preserve the live catalog/header, selected-language
client, lifetime and registration-origin gaps. Offline only; no camera contact
or write payload.**
