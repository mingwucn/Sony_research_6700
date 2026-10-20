# Explicit historical context in preparation

2026-10-20. Evidence: **offline-tested**, **static-inference**. Native English and
native Wi-Fi FTP remain first. No feature, recovery or device-write gate passed.

The existing source-owned `Preparation` accepts an optional closed four-field
historical migration handoff. It captures immutable context/proof bytes and their
external SHA-256 selections, checks the current request hash, and explicitly
selects the v6 gate. The legacy route remains unchanged. Saved metadata carries
the two migration receipts and historical operation separately from the current
operation; missing context cannot downgrade a v6 result into legacy metadata.
Context must match original dependency config, original seal, repository and
legacy session. A rehashed false context still refuses.

This integrates a **consistency-only** path. It produces
`pending_operational_preflight_v2` with `execution_bootstrap_qualified=false`.
The host refuses to turn `gdt_outer_consistency_v6` into an execution context.
Public runtime activation remains disabled. Saved verification recomputes
consistency using the supplied validated dictionary; it does not authenticate
that dictionary's provenance or rerun its separately owned gate.

**165/165** standard-library synthetic tests passed, zero failures/errors/skips,
exit **0**, **76.255s**; 15 selected source/test pins remained stable. Ten new
cases run the real gate, metadata validator, source refresh and materializer
against invented buffers, invented ordinary I/O and invented bootstrap sources.
They cover caller detachment, wrong request/context, downgrade, false saved
claims, execution-context refusal and cleanup exactly once. The qualification
also retains the previous 137 cases and 18 host-entry cases. An independent
authored-source reviewer found no blocking issue and ran 48 related cases.

The separately rechecked original pending proposal validates as comparison
metadata and then refuses `observation_undecided`. All five decisions are pending;
all three dependency null fields remain. Three current authored-source deltas
are identified against the frozen 51-source roster. The old bytes were recovered
from Git solely as inert comparison inputs, with exact saved sizes/hashes.
The 46-role prepared roster, frozen gate/proof/cache and records were not migrated.
No actual preparation/bootstrap or accepted current act was assembled or run.

Synthetic bootstrap success does not qualify historical bootstrap code or an
installed dependency. No firmware, operational constants or native payload read,
dependency activation, download/upload, camera contact or upstream execution.
Exact commands, failed fixture attempts and limitations are in the
[session report](sessions/20261020-RA-003-preparation-context.md).

Next single package: **RA-003: produce a finite evidence/disposition packet for
the next necessary English/FTP analysis act**, reconciling the five pending
decisions against already recorded terms, provenance and the actual research
hypothesis. Identify the exact missing prerequisite and whether the structural
GDT observation advances that hypothesis. Do not invent approvals, clear nulls,
assemble an executable bundle or perform protected processing.
