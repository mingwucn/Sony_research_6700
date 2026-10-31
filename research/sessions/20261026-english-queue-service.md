# EN-101: timer-service queue origins

2026-10-26. Evidence: **static-inference**, **offline-tested exact-byte checks**.
This continues the [engine and callback review](20261026-english-engine-rules.md).
The previous and current goal turns made concrete progress. The language-only
goal remains active and incomplete.

The six formerly unresolved shared service replies now bind to a native timer
service. Each caller sends an identical creation request. The reviewed library
route selects kernel transport; its dispatcher reaches the synchronous-send
implementation, whose queue lookup invokes the native registered callback.
The callback's operation table selects timer allocation for that request.
The successful handler returns the allocator's queue ID and a separate timer
context in the exact fields subsequently used by the callers.

The initialized allocator range excludes the Backup notification queue on
this reviewed successful native path. Provider binding, runtime range/pool
state, all success gates and lifetime remain conditions. The six origins are
classified separately from the 67 prior conditional allocator origins. No
global subscriber absence, working unlock or complete regional preservation
follows.

The old finite population of 77 unknown arguments across three libraries is
now classified as two constants, two initial globals with lifetime limits,
67 conditional allocator origins and six conditional timer-service origins.
Another 96 original unknown origins in 49 libraries remain unreviewed. These
are narrow recognizer results, not a complete inventory of all subscribers.

The six complete callback dispatchers and ten actual callback bodies are
retained. They handle timer messages and invoke function pointers. Queued
message receivers and a virtual callback implementation remain unresolved;
their eventual effects cannot be excluded from these bounded bodies.

The earlier module survey did not include the synchronous registration API.
Adding its relocation calls found the positive timer binding. A missing
recognizer result was not treated as absence. The transport trace also checks
the function actually reached, rather than substituting a similarly named
kernel export. The service receives the payload after the transport header;
all returned-field offsets are reconciled across that boundary.

An independent root audit checks 22 exact instruction words and five
relocations, including the reconstructed registration ID, callback literal,
operation table, allocator arguments, failure branch and returned fields.
The transport packet checks 77 exact words plus PLT/relocations; the handler
checks 76 timer-module words and 34 allocator words. These are finite source
assertions, not firmware emulation. No synthetic suite was rerun and no new
synthetic tests were added.

All inputs were inert retained local files. The timer module was extracted
from the existing application filesystem image without mounting it. No new
acquisition, decryption, firmware/upstream execution, payload, camera/device
interface or network command. Camera commands: **none**. Network commands:
**none**.

The interpreter was `C:/ProgramData/miniconda3/python.exe`, CPython 3.13.12,
with cwd `D:/LocalWork/Sony_research_6700`. Accepted retention/verification
commands below exited **0**; `python` denotes that exact executable:

```text
python -I -B private/english-queue-service-20261026/handler/inspect_handler.py initial
python -I -B private/english-queue-service-20261026/handler/inspect_handler.py kernel-sync-survey
python -I -B private/english-queue-service-20261026/handler/freeze_handler.py
python -I -B private/english-queue-service-20261026/transport/retain_transport.py
python -I -B private/english-queue-service-20261026/callers/retain_callers.py
python -I -B private/english-queue-service-20261026/callers/freeze_callers.py
python -I -B -X utf8 private/english-queue-service-20261026/audit_service_binding.py
python -I -B -X utf8 private/english-queue-service-20261026/verify_baselines.py
python -I -B -X utf8 private/english-queue-service-20261026/record_service_findings.py
python -I -B -X utf8 private/english-queue-service-20261026/finalize_service_packet.py
```

Caller exploratory API-name and isolated sibling-import errors were corrected
before accepted retention; their limits remain in private notes. No input
identity, target bytes or acceptance threshold was changed. The baseline
audit rehashed all 203, 78 and 61 files in the three preceding private packets
and six public parser/test source pins unchanged. Historical public-report
hashes refer to their earlier saved versions.

The module-retention command ran before a bounded static view in one
PowerShell invocation with combined exit 0. Its individual child exit was
not separately captured. The exact combined command is retained privately;
the later standalone handler freeze rehashes the module and asserts its
instructions and relocations with exit 0. Retention was not rerun over the
frozen packet.

Durable evidence is in `private/english-queue-service-20261026/`, including
full input hashes, instruction records, three frozen subpacket manifests and
the final combined manifest. No disposable scratch or Temp directory was
created. Earlier policy-rejected cleanup was not retried. No staging, commit
or push. Installed-body correspondence, rendering, durable persistence,
unrelated/regional-state preservation and inverse/recovery remain unverified.

Next single offline package: trace the 16 original unknown registration
arguments in libInfraRemote, libInfraMFi and libInfraBluetoothLowEnergy.
Resolve queue origins and callback entry points against the existing provider
namespaces. Preserve the other 80 original unknown origins and all indirect/
lifetime limits. No camera contact or write payload.
