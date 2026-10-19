# Collected dependency session and GDT controller composition

This successor design connects the current collector/producer contract to the
existing authored GDT controller and callback factory. Qualification uses
invented streams, keys and cipher behavior only. It does not activate a protected
firmware observation or extend the previous dependency-only runtime act.

## Contract reconciliation

| Boundary | Required behavior in this design |
|---|---|
| Current dependency input | Complete package/trusted-root collection and prospective proof conversion remain owned by `dependency_execution`; old config/cache receipts cannot replace a fresh collection. |
| Operation | The captured dependency policy, controller context and process identity must agree before collection and again before controller entry. The controller still verifies its own complete context. |
| Durable receipt | The factory receives an immutable AES/provenance mapping referencing the current producer's raw bytes, length and SHA-256. The journal must end in raw revalidation and the single callback claim for that operation/hash. |
| Session lifetime | The same dependency finder, native-load guard and AES owner remain active through factory setup, both controller phases, callback release and final public-vector checks. No alternate cipher backend is selected. |
| Controller result | Both tuple code and summary code require exact integers, agree and are restricted to the modeled codes. Refusal remains refusal. |
| Record ownership | The caller owns records before the exclusive attempt directory is reserved. The bridge then attempts closure at most once, including `BaseException` before controller/factory completion. The supplied controller must be bare, without an additional record-owner wrapper. |
| Failure | Preserve the primary exception, release callbacks once after controller entry, retain uncertain results for review and do not retry output publication or an unknown record close. |

`tools/dependency_controller.py` supplies only `run_invented`; `RuntimeOps` is
refused before collection and its CLI returns 2. Caller-supplied callbacks and
hashes are test interfaces, not an authorization boundary or security sandbox.

## What the integration fixture proves

The private authored fixture composes the unchanged real GDT controller,
`ScopedCallbacks`, source-role loader, runner and stream adapter with the current
collector/producer bridge. It checks successful two-pass stream handling, a
second-phase read failure, factory interruption and a caught forbidden native
load. Stream-adapter OS opens are restricted to a newly invented stream, read only;
native loading and crypto are simulated. Invented non-public test keys use an
identity cipher so that the synthetic stream remains interpretable. Public-vector
checks retain the dependency fixture's modeled cipher, not an installed backend.

The fixture temporarily removes/restores its already imported `tools` aliases
around old source planning and factory ownership. This isolates two authored
module graphs in one test interpreter. It is **not** a production bootstrap
solution and does not qualify coexistence of those graphs in an operational
child. No production binding guard was weakened. A new exact-buffer outer child
must establish a clean namespace and a single declared source closure before
dependency activation, without importing then concealing conflicting modules.

The fixture reserves an invented parent marker before child records; it does not
run or authenticate an actual parent/child process chain. Saved dependency
artifact validation remains a consistency check, not mapped-byte, process or
firmware authenticity evidence. Historical seventeen blockers remain recorded.

## Remaining prerequisite and next single package

RA-003: implement and qualify the successor **invented-only exact-buffer outer
child** with one source closure, namespace ownership planned before activation,
the current collected dependency contract held through the real controller, and
independent parent verification of dependency/controller/close/release results.
Exercise stop/unknown-completion reconciliation and obtain source review before
preparing any protected-input activation packet. No actual dependency activation,
firmware/constants reads, camera contact or feature/device-write authority belongs
to that package.

English and native camera-to-server Wi-Fi FTP remain primary and unvalidated;
FL2/FL3 remains deferred. No recovery or device-write gate passes here. See the
[session report](sessions/20261019-RA-003-collected-controller.md) for commands,
qualification results, review findings and evidence limits.
