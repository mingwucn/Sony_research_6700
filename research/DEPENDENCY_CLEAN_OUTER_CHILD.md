# Invented clean outer child and parent reconciliation

Evidence: **static-inference**, **offline-tested**. This package connects the
[collected controller composition](DEPENDENCY_CONTROLLER_COMPOSITION.md) to a
real, isolated child process using invented streams and simulated dependency
loading. It provides no operational or protected-input activation entry.

## Source and namespace ownership

The parent plans the ordinary source graph before importing public helpers.
The child starts with `-I -S -B -X utf8` and refuses optimization. Its standard
library bootstrap verifies request/runtime/argv bindings and reads every declared
ordinary source into bounded, checked buffers before executing authored code.
The invented request declares 58 source roles, with a 2 MiB per-source and
16 MiB aggregate source-buffer limit, plus an 8 MiB packet limit. These are
reader bounds, not a whole-process memory cap.

The child plans the 26-role controller graph before loading dependency helpers.
`tools/dependency_namespace.py` compiles all six helpers before executing any
member and owns them under `_a6700_collected`. Copied module-local builtins route
the authored `from tools import dependency_*` imports to that fixed graph.
No source rewrite or removal/concealment of a preexisting `tools` alias occurs.
Unknown, forward-unavailable, changed or missing dependency imports refuse;
there is no disk fallback for those imports. Other imports use Python's normal
mechanism. This hook is an explicit semantic change, not a security sandbox.

The real role loader can then own `tools` and the controller's distinct role
aliases. The dependency guard and the same AES/provenance object stay alive
through both invented stream phases, role release and final modeled public-vector
checks. Native calls and crypto are simulated; non-public invented keys use an
identity cipher. The whole source closure is transitively included as a canonical
manifest in the dependency source binding, alongside the six direct helper buffers.
The literal fixture stream and constants identities prohibit substituting an
operational input into this private harness.

## Cleanup and parent evidence

Ownership cleanup begins with the first callback/namespace acquisition. It covers
partial helper installation and setup interruptions, and preserves foreign alias
replacements while releasing other owned aliases. Close/release attempts are
single attempts; primary failures remain failures. A process killed during timeout
cannot prove Python-level cleanup, and the parent records timeout/refusal instead.
Final cleanup checks and refusal publication preserve the primary exception.
The parent passes the same one-attempt record owner through supervision and
fallback cleanup. A loader-close error retains an already returned terminal child
receipt. Without such a receipt, the parent records no launch when none occurred,
or an explicit unknown disposition after a supervisor exception; it cannot
manufacture successful process cleanup.

The parent mounts only the 23 ordinary validation roles for inherited controller
reconciliation. It never loads the three protected roles. Bounded supervision
retains terminal child state, stdout/stderr and journals. After exit the parent
rechecks every source and packet receipt, eleven collected dependency artifacts,
both bridge raw hashes and the complete closed bridge completion envelope.
Release, dependency completion, false authority flags and the controller result
must agree. Summary JSON values are compared canonically; the exact stdout bytes
have their own digest. Reordering object keys alone is not a semantic mismatch.

Fault cases alter bridge authority/release/dependency fields and rebind the
outer artifact hash to ensure the parent checks meaning, not hashes alone.
Missing evidence, changed sources, interrupted setup/factory, second-phase read
failure, malformed stdout and an accelerated-clock timeout all remain refusals.
Existing operation folders cannot launch a second child or overwrite evidence.

Saved receipts demonstrate consistency of this invented execution. They do not
authenticate a hostile parent, mapped native bytes, an operating system, a camera
build or historical truth. Historical seventeen blockers remain. No actual
dependency activation, firmware/constants read, camera contact, feature support,
recovery proof or device-write gate is supplied.

## Next boundary

Before any protected-input activation preparation, reconcile this invented source
closure and neutral import semantics with the frozen operational source/binding
and dependency contract. Prepare one source-only operational delta and blocker
matrix, including rights/scope, exact buffers, parent validator ownership and
single-attempt cleanup. Independently review it; do not activate dependencies,
read firmware/constants or contact the camera in that work package.

Qualification commands, counts, negative history and source-review scope are
recorded in the [session report](sessions/20261019-RA-003-clean-outer-child.md).
