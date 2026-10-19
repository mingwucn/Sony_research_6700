# Internal collected-controller continuation

2026-10-19. Host-only design and invented qualification. English menus and native
camera-to-server Wi-Fi FTP remain primary; no feature, recovery or device-write
gate is passed by this work.

The [operational delta](DEPENDENCY_OPERATIONAL_DELTA.md) identified a concrete
composition gap: the invented controller replaced the observer callback, while
the collected runtime observer could only execute public vectors. A runtime
observer supplied by an entry caller would not be an acceptable repair.

The producer now owns an internal continuation slot, separate from the observer.
Collection and proof transition precede dependency bootstrap. The producer runs
its initial vectors, durably publishes and rechecks its raw transcript, records
one callback claim, executes the observer callback, and checks the guard, module
ownership, roots and raw bytes before entering the authored continuation.

The bridge passes an immutable mapping containing the exact AES module and the
current raw receipt anchor to one controller factory. It retains the bare
controller's existing two-phase behavior. Factory handoff must complete exactly
once; failure remains sticky even if a controller catches the exception.
Controller release and final vectors run before dependency guard cleanup; raw
bytes are checked again after the continuation. Foreign aliases, forbidden lazy
loads, changed roots and raw receipts remain refusals.
Context and operation identity are rechecked after controller release as well as
before entry/factory handoff, so late mutation cannot produce bridge success.

Records belong to the caller until exclusive operation-folder reservation. After
reservation the bridge owns at most one close attempt, including setup failures.
It releases callbacks once after controller entry, preserves primary exceptions,
and does not replay an unknown close or completion publication. Existing folders
refuse a new attempt. Failure envelopes distinguish selected mode from completed
observation; mode alone cannot establish an actual read.

The private authored runtime branch delegates to the execution module, which
constructs the concrete RuntimeOps internally after its existing platform/startup
checks. It accepts no observer argument. The public controller run_runtime entry
always refuses before reading arguments, and its CLI exits 2. The dependency-only
public runtime API retains its closed signature without observer, callback or
continuation parameters. Private Python functions are trusted source composition
seams, not security boundaries or authorization mechanisms.

Qualification uses invented package records, source texts, streams and simulated
native/cipher operations. Runtime-dispatch construction checks stop before the
observer/engine executes. Nominal saved-record grammar is not proof of an actual
observation. The extra observer vector callback is retained, so successful bridge
fixtures perform three sets of 24 cipher comparisons: initial, observer, and
post-controller. The raw transcript's original 12-case/24-comparison statement
still describes its initial pre-publication vectors only.

No operational packet, private firmware/constants read, installed dependency
activation, camera operation, upstream execution or new permission is included.
Historical seventeen blockers and loader/OS/transitive-library limitations are
unchanged. Exact-target mappings, English resources/consumers, native FTP backend,
media/network lifecycle and recovery before writes remain unresolved.

The successor package must migrate the frozen operational parent's old schema
and call path to the current composition's eleven dependency artifacts and the
controller/bridge completion envelopes, using invented inputs only. It must derive
the exact successor source roster, retain ordinary-only parent validation and
qualify refusal, ownership and unknown-completion behavior before preparing an
activation packet. This continuation alone does not close those integration gaps.
