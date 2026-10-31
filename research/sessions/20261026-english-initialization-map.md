# EN-101: English initialization, snapshot and notification paths

2026-10-26. Evidence: **static-inference**, **offline-tested**. This continues
the [resource and language-setting study](20261026-english-firmware-analysis.md).
The preceding goal turn made progress. This continuation resolves the compiled
initialization source, a separate saved-language snapshot and concrete callback
identities. The broader language-only goal remains active while the remaining
activation and runtime boundaries are reconciled.

## Result

The initializer does not supply a Chinese-only language default: its exact
compiled table supplies English, value 0. Independent assertions check all
2,930 unique key/value pairs, the selected entry, ELF constructor registration,
unchanged node copy and value lookup. Its model consumer is on the application's
system-initialization thread chain. A bounded reference survey found the
constructor and lookups; indirect mutation and total cross-thread ordering are
not proved absent.

The second model-copy source is a different persisted language snapshot.
Successful bulk reads populate its one-byte field from a distinct Backup item;
read-count mismatch uses the current model instead. Both shipped CN1 and
ALLLANG primary AP catalogs initialize that item to English. Its payload and
capacity overlap no other present primary payload. Metadata flags, provider
attributes, a four-byte model field and a one-byte saved item are kept distinct.
The owner's installed value is unknown.

On the reviewed explicit native-load boot arm, snapshot application precedes
the native current-language getter, and native loading precedes resource-bank
selection through a backward branch. Another arm skips that load. Its first
commands resolve through a concrete dispatch table to display setup, EVF frame
rate and EVF colour temperature; their reviewed local methods contain no direct
language reload. Asynchronous completion and transitive effects are not a global
language-preservation proof.

The compiled phase-scheduling initializer has 885 records, 879 unique keys and
no selected-language entry. Independent raw-word review confirms all key slots,
including four values reloaded from stack spills. A different 285-record
deferred observer table does contain the selected-language callback. That
callback builds the language persistence record unchanged; its daemon case
calls the native current-language setter. Normal notification queues an
update ID; its drain sets an engine pending flag, and batch completion uses
that flag to invoke the marker callback. All 34 compiled enum conversions
round-trip unchanged. Deferred activation still requires its enable flag.
The reviewed flush wrapper orders drain, deferred persistence and snapshot
flush. Requested and effective engine values are distinct runtime fields;
these checks do not prove they always agree.

The snapshot notification path can mark the language field dirty. Its flush
copies the selected model byte through the metadata descriptor and queues that
snapshot item for persistence. This is additional language state, not a global
region conversion. The enabled/dirty gates and queue phases must be preserved
when interpreting the static path.

## Scope and verification

All work used existing private inputs as inert bytes. Application SHA-256:
`e65fd595052be5d0e98ce8000dfcb94f90a2f8309de70ef140375052009b0ef3`.
No new acquisition, decryption, mount, firmware execution, upstream launcher,
device interface or network command was used. No patch, settings payload or
device command was prepared. Nothing was staged, committed or pushed.

The unchanged seven-case address recognizer was rerun: **7 passed**, exit 0;
the other 133 previously passing cases were not rerun. There are no new distinct
synthetic cases. Its output is retained in the tool transcript, with no separate
new regression log. Current qualification also uses exact-file assertions and
independent instruction/table checks. Interpreter:
`C:/ProgramData/miniconda3/python.exe`, CPython 3.13.12. Root and independent
checks below used `-I -B`; the three final source generators and regression used
`-B`.

Final verified commands, workspace-relative from
`D:/LocalWork/Sony_research_6700`; `python` below denotes that exact interpreter.
Each listed command exited **0**:

```
python -I -B private/english-map-provenance-20261026/audit_initial_map.py
python -I -B private/english-map-provenance-20261026/audit_snapshot_metadata.py
python -I -B private/english-map-provenance-20261026/audit_deferred_observer.py
python -I -B private/english-map-provenance-20261026/trace_update_drain.py
python -I -B private/english-map-provenance-20261026/verify_retained.py
python -I -B private/english-map-provenance-20261026/phase/trace_consumer_phase.py
python -I -B private/english-map-provenance-20261026/independent/audit_compiled_callback_keys.py
python -I -B private/english-map-provenance-20261026/independent/audit_snapshot_binding.py
python -I -B private/english-map-provenance-20261026/scheduling/extract_callback_initializer.py
python -I -B private/english-map-provenance-20261026/scheduling/finalize_scheduling.py
python -I -B private/english-map-provenance-20261026/scheduling/normal-route-addendum/trace_normal_route.py
python -I -B private/english-map-provenance-20261026/scheduling/normal-route-addendum/retain_normal_route.py
python -I -B private/english-map-provenance-20261026/record_findings.py
python -I -B private/english-map-provenance-20261026/finalize_packet.py
python -B private/english-map-provenance-20261026/source/retain_bypass_command_provenance.py
python -B private/english-map-provenance-20261026/source/retain_bypass_sibling_display_identity.py
python -B private/english-map-provenance-20261026/source/retain_selected_snapshot_flush.py
python -B -m unittest discover -s private/english-offline-20261026 -p test_aarch64_trace.py -v
```

The earlier `source/retain_map_provenance.py` and
`source/retain_source_structure_provenance.py` generators also exited 0 with
the same interpreter, but their exact flags are unretained. They are excluded
from the exact-command block rather than reconstructed. Their outputs are
pinned and the central bindings have independent exact-file checks.

These checks prove only the declared static bindings. They do not establish
the owner's installed binary identity, actual enable flags, execution order,
native rendering, storage durability, region preservation on the body or a
usable device access/recovery route.

## Corrections and negative results

- An initial scheduling hypothesis used the wrong callback map. Complete
  initializer coverage excludes the selected key from that compiled map; the
  deferred observer is in a separate table. Neither result proves lifetime
  immutability.
- The normal notification queues an update ID. The immediate notification
  branch is an alternate, so it cannot be substituted for normal queued
  activation.
- A prospective queue-drain reference was another producer. A narrow anchored
  reference scan returned zero candidates, but its cross-call/liveness limits
  mean zero is not absence evidence. The actual drain was found independently
  through the command/update wrapper. That exploratory result is retained and
  excluded from positive closure claims.
- The optional all-MOVZ key-source assumption failed: four keys reload checked
  scalar spills. Initial zero/swap stores precede the final key writes. Raw
  failures and corrected exact-word checks remain private; no firmware input or
  acceptance scope was changed.
- The per-ID queue body updates engine state and sets its pending flag; an
  initially suggested direct interface callback was absent from the complete
  body and withdrawn. Batch completion is a separate activation edge.
- Independent snapshot review corrected one address-transcription assertion
  against the original raw body. The integrity recorder initially looked for
  private pins in public state and raised `KeyError`; it then checked their
  retained private-state location. Expected source hashes were unchanged.
- The finalizer initially used Windows' default text encoding for UTF-8 public
  state and stopped before saving its manifest. Explicit UTF-8 decoding fixed
  the host-side read; source bytes and expected hashes were unchanged.

The integrity audit rehashed all **203** prior manifest entries, the frozen
scheduling packet's **22** files and **4** dependencies, and **6** public
source/test pins. The normal-route addendum's **12** files and **2** dependencies
also match their frozen pins. A separate pinned next-package handoff retains
the selected rule/dependency starting headers; it does not claim rule
execution or normalize the earlier packet's scope. All prior pins remain
unchanged. Hash agreement is an identity check, not a device-safety result.

Durable evidence is under `private/english-map-provenance-20261026/`; previous
frozen evidence and its manifest were preserved. No disposable scratch or Temp
directory was created for this continuation. Earlier policy-rejected scratch
cleanup was not retried. Camera commands: **none**. Network commands: **none**.

Next single offline work package: trace the selected-language engine record's
requested-to-effective rules and dependencies. Determine whether availability
or regional inputs can replace requested English before the effective value
returns to the model. Keep current, requested and snapshot language separate.
No camera contact or write payload.
