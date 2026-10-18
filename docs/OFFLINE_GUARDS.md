# Synthetic candidate and transaction foundations

These standard-library modules implement part of RA-007 without any target
firmware, offsets or access route. Their evidence class is **offline-tested** on
authored synthetic fixtures. Every candidate and transaction has
`device_eligible == False`. No target profile is accepted, and the repository's
`profiles/ilce6700.UNVERIFIED.json` is explicitly rejected.

Neither module has a CLI, device adapter, filesystem writer, firmware loader,
native-code loader or executor. Importing them does not retrieve or execute
upstream code. The bytes in their tests are invented text records; no donor
firmware, settings, calibration, profiles or generated firmware payloads are
included. No camera command was run.

## Candidate API and checks

`tools/candidate_guards.py` exposes:

| API | Contract |
|---|---|
| `identify(component, data)` | SHA-256 and exact size of nonempty immutable bytes |
| `SyntheticProfile` | Exact complete component identity tuple, protected ranges, synthetic model/region/version and explicit full tool-revision claim |
| `FixtureIdentity` | Separate caller-supplied fixture model/version/region/profile labels, checked for exact equality with the profile |
| `ReviewFacts` | Required nonempty fixture references for instruction boundaries, control flow, address mapping, protected regions, unselected records and storage size |
| `Edit` | Component, explicit `file_offset`, bounded offset, expected bytes and same-length replacement bytes |
| `build_candidate(..., fixture_identity=...)` | Validate the complete set before constructing any output; return immutable in-memory bytes and canonical JSON |
| `invert_candidate(candidate, sources)` | Require the entire exact candidate set, apply inverse edits in memory, then verify every original whole-object identity |

Only profiles marked `SYNTHETIC_ONLY`, with model/region `SYNTHETIC`, are
accepted. Profile IDs and fixture versions must explicitly begin `synthetic-`.
Missing and mismatched identity labels, unknown profiles, missing review facts,
truncated/changed/mixed objects, missing/extra components and duplicate component
identities are refused. The full expected identity set binds components to one
declared synthetic baseline; it does not infer a compatible pair from names.

Edits must use integer nonnegative offsets and nonempty equal-length byte
strings. Expected windows are checked against the original bytes before output
construction. Size changes, no-op edits, overlapping windows, unknown
components, out-of-bounds windows and protected-range intersections are refused.
Virtual and runtime addresses are refused, without conversion to file offsets.
Protected ranges also require valid bounds and explicit reasons. Adjacent edits
are permitted. A candidate supplied again as a source is refused by its changed
whole-object identity, including a partly applied component set.

The generator checks unchanged bytes outside all selected windows, protected
bytes and object sizes, then constructs the exact inverse and verifies equality
with the full original byte set. Unselected components are included in both
identity sets. The canonical JSON sorts components, edits and protected ranges;
it contains no timestamps, output paths or run IDs. Its baseline-set digest is
over the canonical complete original identity set. Forward/inverse descriptions
and before/after whole-object identities are included.

The tool revision is a required **caller claim** with full lowercase Git-hash
shape. It is not looked up or authenticated. Review references are required
fixture attestations, not a disassembler, rights decision or proof that real
instructions are safe. A caller can author different synthetic profiles; no
real-target allowlist or trusted-profile registry has been implemented. Do not
interpret this API as device eligibility or a machine-enforced write gate.

## Transaction API and state model

`tools/transaction_model.py` exposes immutable `Operation` and `JournalRecord`
records, an explicit shared `OwnershipRegistry`, and `TransactionSimulator`.
Objects and operations are supplied as invented in-memory byte strings. The
constructor checks complete initial bytes, unique operation IDs, equal sizes,
the source expected at each operation's position, and the
`synthetic_mutation` category. This is a simulator of mutation ordering; it does
not validate actual camera operations or call the candidate builder implicitly.

The usual sequence is:

```text
created -> open() -> ready
ready -> prepare_next() -> prepared
prepared -> simulate_result("confirmed") -> ready | complete
complete -> close() -> closed
```

`prepare_next()` checks current simulated objects and appends the prepared
record before enabling simulated mutation. The record contains operation ID,
category, component, complete before/after hashes, attempt number and object
boundary. `simulate_result()` refuses to mutate without that record, and
appends a request record before changing its in-memory object.

The injected outcomes `timeout_before`, `timeout_after`, `disconnect_before`,
`disconnect_after` and `partial` all enter `needs_review`. A partial outcome
requires explicit distinct equal-size fixture bytes. Prepared-before-send,
between-object and final-confirmed boundaries can also be interrupted. The
model retains completed objects and records the exact boundary. It never
pretends several objects are one atomic update.

In `needs_review`, prepare, simulated mutation, resume and close are refused.
No operation retries, inverse, rollback, reboot or ownership release happens
automatically. The only next transition is
`reconcile(complete_observation, evidence_reference)`. The observation must
match the simulator's complete current object set; missing observations or
invented successful observations cannot clear uncertainty. The simulator can
classify:

| Observation | Classification and next action |
|---|---|
| Pending operation remains at its expected original bytes | `not_applied`; explicit `resume()` and a new prepared attempt are required |
| Pending operation matches complete expected resulting bytes | `applied`; advance once, require explicit `resume()`, do not repeat it |
| No pending operation and complete confirmed boundary matches | `confirmed_boundary`; require explicit `resume()` |
| Neither complete known state matches | `partial_or_mixed_state`; remain `needs_review`, retain ownership and evidence |

Successful reconciliation enters `reconciled`, which still cannot mutate.
Explicit `resume()` returns to `ready` or `complete`. A new attempt after
confirmed non-application has its own prepared record and attempt number; this
is deliberately distinct from blindly resending an uncertain operation.

Ownership acquisition checks the full requested resource set atomically within
this one Python object. Duplicate session IDs and overlapping resources are
refused. Failed acquisition does not reserve a partial set. Uncertain sessions
keep ownership; `close()` releases only a complete session. Callers must share
the same registry and reserve the same logical resource to model one owner.

The journal accessor returns immutable snapshots of immutable records. Existing
records remain present when more records are appended. This establishes only
in-memory ordering and caller-facing immutability: **no disk durability,
fsync/flush semantics, crash recovery, hostile-process protection, OS lock,
multi-process exclusion or physical atomicity is proved**. Losing the Python
process loses the model and its ownership registry. A durable device executor
must be separately designed, implemented and reviewed; changing this model's
status fields cannot authorize one.

## Test evidence and remaining coverage

Command run on CPython 3.13.12, Windows AMD64:

```powershell
python -m unittest tests.test_candidate_guards tests.test_transaction_model -v
```

Result: exit **0**, **36 passed**, no errors/failures/skips. This is targeted
coverage of these two new modules, not a claim about the older inventory suite,
remote CI, real input files or hardware.

| Validation ID | Synthetic evidence |
|---|---|
| OFF-01 | Repeated full candidate bytes/manifests, reversed mapping/profile/edit ordering |
| OFF-02 | A changed byte outside the edit windows causes whole-object refusal |
| OFF-03 | Real/unverified profiles, wrong fixture model/version/region/profile and missing review facts refused |
| OFF-04 | Truncated, missing, extra and mismatched component sets refused |
| OFF-05 | Negative/boolean/out-of-bounds/overlapping edits, growth and protected intersections refused; adjacency permitted |
| OFF-06 | Complete and partly applied candidate sets refused as sources |
| OFF-07 | Full forward/inverse byte equality; stale/partial inverse source refused |
| OFF-09 | Unselected invented recipe bytes and complete unselected component equal; no real resource semantics claimed |
| OFF-12 | Timeout/disconnect before/after mutation, explicit partial results, duplicate ownership, observations and reconciled resume |
| OFF-13 | Every boundary of a two-object sequence, prepared-before-send, uncertain second/last object and preserved earlier completion |

OFF-08 (real enum/dispatch bounds), OFF-10 (incoming branches/ABI/stack) and
OFF-11 (actual resource/checksum/encoding semantics) are **NOT RUN / not
implemented**. The required review-reference fields do not pass those tests.
The simulator also does not establish backup completeness, recovery access,
source-to-binary correspondence, runtime activation, colour calibration,
language behaviour, native FTP or feature composition. Private commit review
under OFF-14 remains a separate publication step.

The next implementation prerequisite for real candidate use is an exact-target
evidence set and reviewed profile/schema, instruction/resource-specific
validation, target-specific preservation and write/reload/recovery contracts.
Those facts are presently unavailable. Keep these modules synthetic-only.
