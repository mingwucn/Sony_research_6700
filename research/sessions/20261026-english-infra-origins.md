# EN-101: infrastructure registration origins and application forwarders

2026-10-26. Evidence: **static-inference**, **offline-tested exact-byte checks**.
This continues the [timer-service review](20261026-english-queue-service.md).
The previous and current goal turns made progress. The language-only goal
remains active and incomplete; no working unlock or device-write gate is claimed.

Sixteen more original unknown registration arguments now have concrete
provenance under their stated initialization, success and provider conditions:

| Library | Reviewed | Conditional local allocation | Conditional timer service | Initialized object fields |
|---|---:|---:|---:|---:|
| Remote | 6 | 3 | 1 | 2 |
| MFi | 5 | 3 | 2 | 0 |
| Bluetooth Low Energy | 5 | 1 | 4 | 0 |
| Total | 16 | 7 | 7 | 2 |

The overall original population is now 93 reviewed and 80 unreviewed in 46
libraries. The 93 comprise two direct constants, two initial globals, two
initialized object fields, 74 conditional allocator origins and 13 conditional
timer-service origins. Initial values are not lifetime immutability proofs.
These counts reconcile the original narrow recognizer's unknown population;
they are not a census of every possible subscriber or executable path.

The successful paths use queue namespaces/ranges distinct from the Backup
notification queue. Failure paths matter: Remote USB/IP wrappers log an
allocation failure and can fall through to registration. Two MFi callers
ignore allocation status. MFi's ordinary initialization checks an earlier
allocation result, but resume reuses its cached field. BLE has a checked
zero-result branch before the same-output registration load. An independent
root review checks 64 raw words, branch destinations, PLT identities and
output-field operands across these three cases. An initialized range does
not establish an all-path exclusion.

The finite callback bodies and concrete pointer bindings are retained.
They include queued messages, table function pointers, a dynamic callback
global and an iAP2 boundary. Ordinary constructor remote-model and
authentication/status Backup writes were found. They are positive write
leads, with no established reachability from a selected-language notification.
Neither their presence nor a callback's name proves regional side effects.
Transitive behavior, provider binding and field/pool lifetime remain open.

The root also reviewed the application's five nonconstant direct synchronous
registration sites. Three load newly created queue IDs with local allocator
provenance. The shared constructor initializes the destination and invokes
the allocator with combined flags; it does not test the allocator result
before loading the destination. One other site registers its original input
ID while storing a separately created queue elsewhere. The fifth forwards
input arguments unchanged through a wrapper with 44 direct callers. Numeric
caller arguments remain unreviewed. A second wrapper has no recognized
direct branch callers; indirect/relocated entries remain possible. These app
sites are separate from the 173 original non-app unknowns.

The application addendum checks 85 exact words/branches, including all 44
direct-call edges. The library packets check 83 Remote, 112 MFi and 154 BLE
instruction/operand facts, plus their separately recorded provider checks.
These are overlapping finite source assertions, not synthetic behavior tests
or firmware emulation. No synthetic suite was added or rerun this turn.

All input files remained inert local bytes. Three library files were extracted
from the retained filesystem image without mounting it and matched the old
whole-file hashes. Library/app locations are ELF link-time virtual addresses
with file offsets separately labelled; native-module locations retain ET_REL
section offsets. No runtime address is claimed.

Interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython 3.13.12. Cwd:
`D:/LocalWork/Sony_research_6700`. In the following accepted commands, `python`
means that exact executable. Each final command exited **0**:

```text
python -I -B private/english-infra-origins-20261026/remote/inspect_remote.py extract
python -I -B private/english-infra-origins-20261026/remote/retain_remote.py
python -I -B private/english-infra-origins-20261026/remote/freeze_remote.py
python -I -B private/english-infra-origins-20261026/mfi/extract_mfi.py
python -I -B private/english-infra-origins-20261026/mfi/retain_mfi.py
python -I -B private/english-infra-origins-20261026/mfi/freeze_mfi.py
python -I -B private/english-infra-origins-20261026/ble/extract_ble.py
python -I -B private/english-infra-origins-20261026/ble/retain_ble_arguments.py
python -I -B private/english-infra-origins-20261026/ble/freeze_ble.py
python -I -B -X utf8 private/english-infra-origins-20261026/retain_app_forwarder_callers.py
python -I -B -X utf8 private/english-infra-origins-20261026/retain_app_sync_addendum.py
python -I -B -X utf8 private/english-infra-origins-20261026/audit_registration_failure_paths.py
python -I -B -X utf8 private/english-infra-origins-20261026/verify_baselines.py
python -I -B -X utf8 private/english-infra-origins-20261026/record_infra_findings.py
python -I -B -X utf8 private/english-infra-origins-20261026/finalize_infra_packet.py
```

The initial root audit mislabeled one MFi PLT import as asynchronous; its
actual relocation names the synchronous API. The corrected audit passes
without changing input bytes or acceptance scope. An exploratory metadata
read assumed the wrong old JSON field type, and two attempted helper-source
reads named absent files; no retained firmware result was changed. BLE's
exploratory PowerShell wildcard had a path diagnostic before literal-path
reads. Corrections and finite limits are retained privately.

The baseline audit rehashes 203, 78, 61 and 33 files in the four preceding
private packets plus six public parser/test sources unchanged. Remote's
worker manifest pins three public documents as observed before integration.
Exact private snapshots preserve those versions; the root manifest separately
pins the deliberately updated public reports/state. No frozen worker input,
firmware, parser or receipt was rewritten to accommodate integration.

Durable evidence: `private/english-infra-origins-20261026/`. No disposable
scratch or Temp directory was created. Earlier rejected cleanup was not
retried. No acquisition, decryption, firmware/upstream execution, payload,
camera/device/USB command, network command, staging, commit or push.
Camera commands: **none**. Network commands: **none**.

English resources, the separate selection/availability fields and ordinary
English propagation retain static support. Full installed-body identity,
rendering, durability, indirect effects, unrelated/regional/calibration-state
preservation and inverse/recovery remain unverified.

Next single offline package: trace the 44 direct callers of the application's
generic synchronous registration wrapper. Resolve queue-ID arguments and
callback entry points against actual provider namespaces. Preserve the other
input-forwarding app site, indirect entries, 80 unreviewed non-app origins and
all lifetime/effect limits. No camera contact or write payload.
