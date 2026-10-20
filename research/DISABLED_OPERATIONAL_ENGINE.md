# Disabled operational engine composition

2026-10-20. Evidence: static-inference and offline-tested. English and native
Wi-Fi FTP remain primary; camera commands: none.

`tools/dependency_operational_entry.py` now provides separate private child and
parent engine compositions. It imports only the standard library. Public
`run_runtime` and the direct CLI refuse before inspecting caller arguments or
importing project modules. These private functions can perform work if called;
Python privacy is not a security boundary or permission check.

The child validates the existing prepared source/request mapping before metadata
preparation. It then calls the checked adapter's existing runtime continuation,
with its supplied trusted wiring and without an observer/cipher/mode selector.
The callback comes from the trusted metadata preparation, not a runtime packet.
The existing controller remains responsible for fresh dependency collection,
durable raw receipts, the AES owner, protected callback ordering and two phases.
Only invented records and intercepted dispatch were tested here.

The wrapper tracks callback claim, completion and sticky failure. Swallowed
callback/reentry failures cannot produce a successful engine return. Callback
release and record close must have completed. A failed or uncertain close is
sticky and is never retried. Independent cleanup attempts cover callbacks,
records, helper owner, adapter owner and metadata preparation, preserving the
primary exception if cleanup also fails. Callback cleanup precedes helper and
metadata teardown. Legacy callback close's normal `None` return is supported;
record close requires exactly `True`.

The parent composes existing `reconcile_runtime` and saved-runtime verification.
It rejects incomplete process facts through the existing prepared adapter before
the saved verifier and closes helper/adapter owners independently. It does not
spawn a child or authenticate caller-supplied process facts. Its engine-result
wrapper explicitly leaves production qualification, execution, feature support,
recovery and device-write gates false; it is not a process completion receipt.

The helper loader now retains its checked source buffers and freezes mode,
load order, origins, source hashes and compiled code identities at construction.
It checks those identities before first execution and during integrity checks.
Replacing compiled code cannot leave matching source-buffer claims accepted.
The existing neutral child aliases and detached parent verification remain.
This is trusted authored-source composition, not a hostile-code sandbox.

## Boundaries still requiring integration

This is **partial operational engine composition**, not a complete operational
launcher or ordinary-record grammar. The new entry/wiring/preparation and fifth
parent verifier source must be bound by the future checked outer source owner.
The prepared map still has 46 roles/41 paths and pending decisions; it is not
silently expanded to include this new entry. The original invented launcher and
metadata preparation retain their fixed invented-input restrictions. They are
not relabelled, and their 62-source process roster is not an operational roster.

The future outer path must provide independently checked metadata preparation,
current ordinary/preflight/result records, exact source/command ownership and
OS-derived supervision facts before reaching these engines. The existing
supervisor, bootstrap and saved-preflight ownership must be integrated explicitly.
Interpreter/stdlib/initial bootstrap remain trusted assumptions. Human consent,
legal basis and byte consistency remain separate; all five activity-specific
decisions stay pending. No actual activation record is assembled by this change.

Next single package: **RA-003: bind the disabled operational engine composition
into a separately source-owned outer parent/child preparation and saved-result
path. Derive its exact source map and operational ordinary/preflight/result
contracts, preserving the frozen supervision and observation limits. Qualify
only with invented records and intercepted runtime calls; independently review
before any actual record assembly or activation. No installed dependency
activation, firmware/constants/native payload reads, downloads/uploads or camera
contact; keep the five decisions pending.**


Current reservation integration (2026-10-20): the child no longer accepts pre-reserved records. It prepares once, validates the complete packet/context binding, allocates an empty strict close proxy, then reserves child journals using the prepared control. Failed preparation/binding or proxy construction performs no reservation; an acquisition error is not retried. An acquired handle closes once on later failure. See [qualification](sessions/20261020-RA-003-late-record-reservation.md). The outer and operational ordinary-record migration remains pending.


Preparation update (2026-10-20): [Separate checked preparation and pending records](OPERATIONAL_PREPARATION.md) now bind the child preparation and saved-parent engine to original metadata/source bytes. Complete outer source capture, real retained metadata/materialization integration, completion evidence and OS-derived supervision remain pending. Earlier boundary descriptions above are historical; no operational activation is qualified.
