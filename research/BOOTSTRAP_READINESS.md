# Original bootstrap readiness review

2026-10-23. Evidence: **static-inference**, **offline-tested** (synthetic producer
tests only). Native English menus and native camera-to-server Wi-Fi FTP remain
first. Camera commands: **none**. No owner input is needed for the next preparation
package; legal research/questions remain stopped.

The original-instance integration remains qualified only on invented inputs.
This review resolves where that evidence ends and compares the saved ordinary
dependency descriptors with the retained preparation contract. No production or
test source changes, installed dependency activation, protected processing or
camera operation occur. Actual runtime, feature, recovery and write gates remain
unpassed.

## Bootstrap and selected safety hook

| Boundary | Source evidence | Consequence |
|---|---|---|
| Direct imports | `tools/dependency_producer.py:29,289`: `ctypes`, `_ctypes`, `ctypes.util`, `ctypes._endian`, `platform`, in that tuple's iteration order. | This specifies direct calls, not the transitive import closure, cache hits or actual native-event order. Imports can initialize `_ctypes` and OS-loader code. |
| Startup | `RuntimeOps.startup` at lines 281–286 requires Windows/CPython and reports flags; `_produce` at lines 299–303 rejects preloaded Cryptodome/CFFI-family aliases and requires isolation/no-site/no-user-site/no-bytecode. The dispatch has an additional pre-construction preload check. | An existing receipt or fake module does not establish a fresh child startup. The synthetic owner also forbids an inert preloaded `platform` alias; do not conflate the checks. |
| Audit installation | Lines 310–315 read the trusted origins, register the guard and require its genuine private probe acknowledgement before bootstrap. | Prior synthetic probe delivery is genuine Python audit evidence; it does not attest native bootstrap. |
| Bootstrap exceptions | `Guard.audit`, lines 147–149, permits at most one `ctypes.dlopen` with `(None,)` and one with `('kernel32',)` while bootstrap is true, in either order. | Neither is required or emitted into the producer journal. The allowlist is not a record that either load occurred or a complete native containment policy. Other `ctypes` event names are not handled by this guard. |
| Package wrapper | Bootstrap and trusted-origin comparisons occur at lines 316–319; the CDLL wrapper is installed at line 322. | The guarded package-loader observations begin after trusted bootstrap. They do not cover all interpreter, `_ctypes`, OS-loader or transitive DLL initialization. |
| Selected fixture | The current instance suffix inherits the hook in `tests/test_dependency_child_callbacks.py:52–61`. It rejects all `ctypes.*` events and imports rooted at `ctypes`/`_ctypes`. | A genuine cold bootstrap conflicts with the selected synthetic hook. Preserve that hook. The different isolated-handoff suffix is not the selected instance child suffix. |
| Inert adapter | `tests/dependency_instance_runtime_fixture.py` supplies ModuleType bootstrap objects and directly calls the original guard for invented native events; the original bootstrap method is not called. | The exact original observer instance and its six genuine delegated methods do not turn bootstrap, cipher lookups or protected-role doubles into actual activation. |
| Next step in the engine | `_produce` imports `Cryptodome.Util._raw_api` and AES immediately after wrapper setup, lines 324–326. | Calling `_produce` unchanged is not a bootstrap-only experiment. A future bootstrap-only entry must stop before package imports and any producer/controller continuation. |

The selected suffix chain is instance → audit → filesystem → runtime route → I/O
boundary → child-callback suffix. Only `DISK_IO` comes from the isolated-handoff
test. No hook was weakened and no fake import dispatcher was added as evidence
of real bootstrap.

## Saved descriptor comparison

The separately recorded historical dependency-only observations remain valid
within their stated scope. In particular, a prior collected observation covered
351 package rows plus five trusted origins. This review does not repeat it or
claim that no actual dependency observation ever occurred.

The saved ordinary package descriptor has 351 manifest rows, 351 installed
receipt rows and 351 installed-proof rows. Its roster and RECORD hashes agree;
the saved successor expectation binds that manifest and proof. No installed
file, wheel, RECORD bytes, embedded source cache, native payload or protected
input was opened to make this comparison.

| Retained field/contract | What ordinary descriptors already contain | What remains unresolved |
|---|---|---|
| `expected_files` | Historical 351 relative-path `{sha256,size}` manifest rows, matching the retained cardinality/row shape. | Selection as a current binding and freshness. The frozen null does not mean those historical values were never observed. |
| `record_sha256` | Historical manifest and installed-proof values agree. | A current reference and freshness; do not silently fill the frozen null. |
| Version/wheel identity | Historical version 3.24.1 and wheel identity are recorded. | Matching saved metadata does not reopen or attest the currently installed bytes. |
| Python/native origins | The successor has 11 Python aliases and five native aliases, with `{root,relative_path,sha256,size,identity}` rows. | A relative package-path projection can represent some old fields, but drops successor root/identity semantics. No policy conversion was performed. |
| Backend origins | Five successor trusted aliases: `_ctypes`, `ctypes`, `ctypes._endian`, `ctypes.util`, `platform`. | Retained `activation_native_policy_v1` requires `{path,sha256,open_identity_sha256}`. An identity subset is not a hash of a complete same-open receipt. Missing binding is not proof that no historical receipt exists. |
| Path domains | Successor `dependency_expectation_v1` separates absolute package/runtime roots with root identities. | The retained `_path` rejects absolute paths and drive colons. A relative rewrite would conceal external runtime origins; renaming `trusted_origins` to `backend_origins` is insufficient. |
| Current execution binding | Existing code binds operation, roots, sources/config/cache/manifest/proof/vector hashes, loader kwargs, bootstrap, request/packet and argv. | The saved six-source expectation is historical. Current source selection, current references and an authenticated future command are not emitted by this review. |

Sources: retained authored `activation_binding._path/_files/_policy/_dependency`
(lines 83–93, 135–196), `tools/dependency_evidence.py:218`,
`tools/dependency_execution.py:217`, and
`tools/dependency_operational_launcher.py:113,196`. Exact private descriptor paths
and hashes are recorded in the ignored session receipts.

The existing nonexecuting migration draft still describes 51 comparison roles,
46 prepared roles, five changed outer roles plus an explicit historical-gate
replacement. Selection remains unapplied. No current executable bundle or source
manifest migration was created. All 16 frozen ordinary records, five historical
pending dispositions, three actual-plan dependency nulls and production/public/v6
refusals are preserved. These historical dispositions are not new owner questions.

## Verification and remaining limits

The unchanged synthetic producer suite passes **52/52**, zero failures, errors or
skips, CPython 3.13.12 with `-I -S -B -X utf8`, exit 0. Its loaders/cipher are
invented; it does not execute the original bootstrap or installed native code.
Finite source review parses 17 authored ASTs and one inert source literal and
checks unchanged source bytes, selected safety hook and refusal functions.
Ordinary metadata checks preserve 16/5/3 and compare the historical 351-row
descriptors with the successor contract. Both checks exit 0.

The prior **82-case integration qualification is inherited, not rerun**; its two
saved log hashes and results were rechecked. The 52 producer cases are a subset
of that prior suite and must not be added to 82 as a new distinct-case total.
[Exact commands/results and changed files](sessions/20261023-bootstrap-readiness.md).

This is a finite static/cooperative-filesystem review, not runtime attestation
or a native sandbox. Actual bootstrap import/event order, fresh current source
and origin bindings, loaded native bytes/transitive dependencies, protected
decoder/GDT processing, exact-body correspondence, English resources/policy,
native FTP backend/lifecycle and practical rollback/recovery remain unverified.
FL2/FL3 stays deferred; custom looks are separately gated later. Any optional
bridge remains **host-assisted**.

## Next single work package

RA-003: prepare a bounded, nonexecuting bootstrap-only observation packet using
the existing observer/supervisor preparation path. Specify an original-bootstrap
entry that stops before Cryptodome imports, ordinary source/origin/receipt and
path-domain bindings, a separate future audit profile with bounded private event
journaling, and synthetic parent preparation/refusal cases. Carry unresolved
current bindings explicitly; preserve the current native-denying synthetic hook,
frozen records/nulls and production refusals. Emit no activation command or
actual allow record. No installed/native/protected input reads, activation or
camera contact; English/native FTP stay first.
