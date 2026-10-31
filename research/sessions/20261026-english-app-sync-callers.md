# EN-101: synchronous callers and notification type

2026-10-26. Evidence: **static-inference**, **offline-tested exact-byte checks**.
This continues the [infrastructure origin review](20261026-english-infra-origins.md).
The previous and current goal turns made progress. The language-only goal
remains active and incomplete.

All 44 direct callers of the application's synchronous registration wrapper
are traced to concrete arguments:

| Caller group | Sites | Fixed IDs | Conditional local allocations | Conditional kernel allocations |
|---|---:|---:|---:|---:|
| First | 15 | 2 | 11 | 2 |
| Middle | 15 | 0 | 15 | 0 |
| Last | 14 | 2 | 12 | 0 |
| Total | 44 | 4 | 38 | 2 |

The global origins depend on successful initialization, expected providers and
lifetime. Existing nonzero values can bypass allocation. The reviewed global
fields are BSS and have no file-backed current values. Failure diagnostics
call imported `__assert_fail`; its expected nonreturn behavior and actual
binding remain conditions. Teardown can release and clear fields, including
after an error diagnostic. No immutable-global or all-path range guarantee
is claimed. Callback bodies retain imported, virtual, table and queued effects.
These app caller sites are separate from the original 173 non-app unknowns.

A more useful notification boundary is now established. The traced shared
Backup notification calls the asynchronous send API. Native asynchronous
registration appends a callback to a list; synchronous registration stores its
record in a different slot. The userspace synchronous wrapper sends a type
flag through its common ioctl. The kernel's outer copy passes the inner-body
pointer to the selected handler, which reads that flag and selects synchronous
registration. Both reviewed asynchronous worker arms consume the asynchronous
list, including its shared fanout path. Equal numeric queue IDs alone cannot
turn that synchronous record into an asynchronous Backup subscriber on these
reviewed provider paths.

The root proof checks 47 exact words/operands and six relocations across three
pinned inputs. A separate review rechecks all 47 words and independently parses
five kernel relocations, the copied-body pointer edge and post-index list
operand. This closes an initially omitted evidence link between the outer and
inner registration bodies. No assumption about similarly named APIs substitutes
for the actual branch. Local and kernel queue namespaces remain distinct.

The 80 still-unreviewed original non-app origins divide into 54 synchronous
API sites and 26 asynchronous sites across 23 libraries. These are unchanged
numeric-origin gaps, now prioritized by callback type. The type distinction is
conditional on the pinned provider and ordinary structures; dynamic forwarding,
re-registration, indirect subscriptions and transitive setting effects remain
open. It does not prove complete subscriber absence or regional preservation.

The three caller packets retain the original 44 exact tuples, argument loads,
producer paths, callback bodies and finite tables. Their instruction windows
overlap and are not counted as distinct tests. No synthetic cases were added
or rerun. The static assertions do not execute or emulate firmware.

Inputs remained inert local files. All locations are ELF link-time virtual
addresses, or native-module ET_REL section offsets, with separate file offsets.
No runtime address, payload, firmware/upstream execution, new acquisition,
decryption, device/USB access or network command. Camera commands: **none**.
Network commands: **none**.

Interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython 3.13.12. Cwd:
`D:/LocalWork/Sony_research_6700`. `python` below denotes that exact executable.
Accepted final commands exited **0**:

```text
python -I -B -X utf8 private/english-app-sync-callers-20261026/first/retain_first.py
python -I -B -X utf8 private/english-app-sync-callers-20261026/first/audit_notification_types.py
python -I -B -X utf8 private/english-app-sync-callers-20261026/first/freeze_first.py
python -I -B -X utf8 private/english-app-sync-callers-20261026/middle/retain_middle.py
python -I -B -X utf8 private/english-app-sync-callers-20261026/middle/freeze_middle.py
python -I -B private/english-app-sync-callers-20261026/last/build_packet.py
python -I -B private/english-app-sync-callers-20261026/last/freeze_last.py
python -I -B -X utf8 private/english-app-sync-callers-20261026/retain_notification_callback_types.py
python -I -B -X utf8 private/english-app-sync-callers-20261026/record_app_sync_findings.py
python -I -B -X utf8 private/english-app-sync-callers-20261026/finalize_app_sync_packet.py
```

Exact worker commands, including their exploratory range arguments and any
flag differences, are retained privately. Isolated sibling imports were
corrected before accepted retention. Last's initial freeze expected seven
owned files but found eight; it stopped before writing a manifest and the
count was corrected. Input identities and acceptance scope did not change.

The combined integrity check rehashes all 203, 78, 61, 33 and 44 retained files
in the five preceding private packets, plus six public parser/test source pins.
Historical public-report hashes retain their dated scopes. All worker packets
have stopped writing before the final combined manifest is saved. Durable
evidence: `private/english-app-sync-callers-20261026/`. No disposable scratch
or Temp directory; no retry of earlier rejected cleanup, staging, commit or push.

English resources, separate language selection/availability and ordinary
English propagation continue to support a language-only route statically.
Installed-body correspondence, rendering, durability, complete unrelated/
regional/calibration-state preservation and inverse/recovery remain unverified.

Next single offline package: trace the 26 remaining asynchronous non-app
registration origins, starting with the Backup provider's own asynchronous
helper. Resolve queue IDs, callback entries and any selected-item filtering.
Preserve the 54 synchronous origin gaps, other app asynchronous/indirect
routes and all provider, lifetime and transitive-effect limits. No camera
contact or write payload.
