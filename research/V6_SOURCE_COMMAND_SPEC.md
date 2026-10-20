# V6 source and command specification

2026-10-20. Evidence: **static-inference**, **offline-tested** for ordinary source
and metadata checks. This specification is non-executing, with no actual command,
allow decision, operation identifier, result-folder selection or target profile.
English and native Wi-Fi FTP remain first; camera commands: **none**.

## Exact source projection

The current observation comparison has 51 source roles: 49 child captures and
two host sources. Adding the existing contract/outer validators gives 53; adding
the observation launcher gives 54. The prepared adapter has 46 roles projected
through the existing explicit `PREPARED_PROCESS_ROLES` map, including its deliberate
aliases. These counts describe different rosters and must not be interchanged.

| Role | Current difference from original comparison | Prepared-map effect |
|---|---|---|
| host_entry | Reviewed explicit refusal of a v6 consistency execution context | None: outside the 46 prepared roles |
| operational_metadata | Reviewed context/proof receipt and original-input bindings | None: outside the 46 prepared roles |
| operational_preparation | Reviewed optional v6 gate/context handoff | None: outside the 46 prepared roles |
| retained_gate | Proposed substitution of `tools/dependency_historical_gate.py` for the frozen old gate | None: outside the 46 prepared roles |

The first three are actual authored changes. The fourth is **a proposed source
selection**, not an applied manifest migration or execution allowlist. All 46
prepared role identities still equal their original selected source bytes;
there are **zero prepared byte deltas**. The historical 51-source/46-role
manifests, frozen gate/proof/cache and original records remain unchanged.

The proposed gate uses an existing role, so a selected 51-source capture would
still contain 51 entries. The actual source/proof relationship must nevertheless
be checked under that gate; keeping a role name does not establish compatibility.
Fresh receipts, current derived outer maps and qualification would be needed.
Prepared source-map stability does not make outer code changes irrelevant.

## Demonstrated transport gaps

| Source seam | Observed current behavior | Required change before a v6 command can be reviewed |
|---|---|---|
| `dependency_observation_launcher.pending_projection` | Emits packet v1 without migration | Explicit versioned projection preserving closed context/proof bytes and pins |
| `dependency_operational_child.decode_packet` | Closed v1 field roster excludes migration | Closed v2 decoding and byte/pin bounds; preserve v1 semantics |
| `dependency_operational_launcher._prepare_pending` | Calls legacy `validate_bundle` | Explicit dispatch using current request operation and supplied historical context |
| `dependency_operational_child.child` | Calls legacy gate; constructor omits migration | Match parent dispatch and pass the exact captured handoff to Preparation |
| `dependency_operational_child.preflight_arguments` | Omits migration for saved checks | Preserve the same handoff in saved-preflight recomputation |
| `dependency_host_entry.make_context` | Explicitly refuses v6 consistency results | Keep refusal until a separate execution context/bootstrap is qualified |

Six exact source/hash/line witnesses and complete private proposed source rows
are retained in the local specification. The reviewed preparation change alone
cannot repair these calling seams. Rehashing an old packet or changing a boolean
will not make a current v6 execution route.

## Command frame and unresolved arguments

The current observation bootstrap text reconstructs deterministically to SHA-256
`63c051081d49cd871a4b1d8c55b8a569ff2c62e91436f13fdb1e510d438d489f`.
The nested pending bootstrap text hashes to
`9fc839f17e6c2ff316b88421af3d0d0719838d83a6113b65fdfcdc2743c99c86`.
These are existing authored command-text identities, **not a v6 bootstrap
qualification**. The text was composed twice with process/file-opening calls
blocked; neither bootstrap was executed.

The command frame remains the selected isolated interpreter, flags
`-I -S -B -X utf8 -c`, exact reviewed bootstrap text, then an absolute request-core
path and its whole-byte SHA-256. `A6700_OBSERVATION_PACKET_SHA256` binds the canonical
transport separately. Changing migration fields can change nested source and
transport bytes; later bootstrap edits require new hashes/qualification. No
synthetic values or placeholders are inserted into an actual command here.

Still unresolved: current source/gate selection review; closed migration
transport schema; parent/child dispatch and saved arguments; separately qualified
execution context/bootstrap; current original candidate/review/decision/seal;
dependency fields and fresh in-act observation; exact core/result paths and
transport binding; and five activity dispositions with independent decision
evidence. Existing partial pending proposal bytes are comparison evidence, not
an accepted complete current act. No legal disposition follows from this audit.

## Next single work package

**RA-003: implement and qualify the closed v2 migration handoff through the
existing packet/projection and parent/child preflight seams**, including saved
arguments. Retain v1 behavior and explicit v6 execution-context refusal. Qualify
invented complete, missing, altered, downgraded and cross-operation cases; ensure
v6 stops before bootstrap materialization, protected preparation, result writes
or process launch. Do not weaken the context refusal or infer runtime authority
from consistency. No actual allow records, source-manifest migration, dependency
activation, protected reads or camera contact.

[Exact commands and limitations](sessions/20261020-RA-003-v6-source-command-spec.md).
