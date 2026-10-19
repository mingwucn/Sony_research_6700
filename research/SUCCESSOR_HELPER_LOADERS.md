# Successor helper loaders and closed wiring

2026-10-19. Evidence: static-inference and offline-tested. English menus and
native camera-to-server Wi-Fi FTP remain primary; FL2/FL3 is deferred. Camera
commands: none. This implements the helper-loader/wiring part of the
[reviewed specification](OPERATIONAL_BINDING_SPEC.md). It creates no executable
operational packet, dependency activation or device permission.

`tools/dependency_successor_sources.py` provides two fixed, separate helper
graphs. Both share dependency_evidence, dependency_producer,
dependency_package_preflight and dependency_execution, in dependency order.
The child adds dependency_controller; the parent adds dependency_parent.
Neither includes dependency_invented. Unknown, extra or mismatched role maps
are refused. All five buffers must pass size, origin, digest, AST import and
compilation checks before any member executes. Source hashes are comparison
inputs, not independent authorization or provenance authentication.
Each raw helper is bounded to two MiB and the complete graph to eight MiB.
These are source-buffer limits, not aggregate managed-memory or process caps.

The child owns only `_a6700_successor` aliases and refuses preloaded neutral or
tools aliases rather than hiding them. The parent mounts no sys.modules aliases
and redirects authored tools imports to the checked objects even when live tools
aliases already exist. Parent helper globals have a shallow identity snapshot,
checked before and after saved verification. These checks are not a sandbox or
deep immutability proof. Dynamic Python behavior, interpreter/stdlib/OS trust
and complete operational import policy remain part of the outer binding.

Lazy imports check active ownership and cannot fall back to unchecked tools
members. Partial publication/execution and interruptions retain the primary
failure and attempt cleanup of every owned alias. Foreign replacements remain
untouched. Close and load are single-attempt operations; closed helpers cannot
be reused. The eventual outer engine must retain/check/release helper ownership
across the entire operation, including refused and unknown outcomes.

`tools/dependency_successor_wiring.py` has a closed private runtime composition
seam. It requires CPython/Windows isolated/no-site/no-user-site/no-bytecode,
unoptimized startup and no preloaded Crypto/Cryptodome aliases. It binds the
runtime packet with the existing binder against original expectation/package/
root hashes, source buffers and the new review hash. Operation/context/identity
must match before controller entry. Observer, backend, continuation and mode
overrides are absent from its signature. The controller receives invented=False
and no ops, so its existing engine constructs the observer internally.

That path has **not** performed actual dependency activation. The tests use
invented inputs with a stubbed engine, and a real controller stopped before
observer construction. Caller records remain untouched before reservation;
after reservation the existing controller owns the sole close attempt. Wiring
adds no second owner or automatic retry after failure/unknown completion.

The separate private parent seam selects saved runtime-record mode. Tests check
its exact call shape, real checked-buffer parent verification of invented
artifacts and rejection of those artifacts under the runtime-record grammar.
They do not establish a successful actual runtime-shaped producer/controller
transcript through the entire new outer process chain. An outer refusal must
never be promoted by the pure controller success verifier.

Both public runtime entries and module CLIs remain disabled (CLI exit2). The
old helper loader, seven-helper private parent loader and frozen invented
adapter are unchanged. Existing qualification is preserved; this does not
silently replace its source pins.

The [session report](sessions/20261019-RA-003-successor-loaders.md) records final
qualification commands/results, source pins and independent reviews. No actual
firmware/constants/native dependency reads, private uploads, upstream execution,
camera, feature/write gate or recovery proof belongs to this package. Historical
seventeen blockers and the activity-specific rights/trust assessment remain.

Next single package: integrate these successor helpers and wiring into a new
source-only outer host/child/parent adapter with a closed authority/input roster,
exact interpreter/argv/request/source binding and separate success/refusal/unknown
terminal grammar. Qualify the complete chain on invented inputs, including
single-owner release and supervised interruptions; independently review the
source. Preserve frozen predecessors; public runtime remains disabled. No
executable actual activation packet, actual dependency/firmware/constants reads
or camera.
