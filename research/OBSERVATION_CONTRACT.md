# Pure observation contract

2026-10-20; **static-inference**, **offline-tested**. Native English and native
camera-to-server Wi-Fi FTP remain first; FL2/FL3 deferred. Camera commands: **none**.

[Source](../tools/dependency_observation_contract.py) and
[tests](../tests/test_dependency_observation_contract.py) add the separate contract
identified in the [activity review packet](ACTIVITY_REVIEW_PACKET.md). Existing
pending contracts and the disabled launcher are byte-unchanged. The new module is
not loaded by that launcher and has no execution connection.

## Result and boundaries

The new schemas can express a proposed observation and all five separately
recorded `allow_scope` dispositions, unlike the existing pending-only/invented-only
grammars. Tests supply invented records and inert source strings using these new
schemas; they are not actual permission, activation records or target inputs.
`validate_proposal` can also describe pending/denied dispositions;
`validate_decided_scope` refuses either. Both return consistency only: authority,
rights, freshness, runtime qualification, execution and feature/recovery/write
flags remain false. A digest or actor claim does not establish human consent.

The API takes bounded byte buffers and externally selected expected digests. It
does not open file/path labels, import source strings, invoke loaders/observers,
start processes or accept protected payloads. Protected identities are size/hash
metadata only. Public direct CLI exits 2 before authored imports; `run_runtime`
raises `real_activation_pending`.

## Acyclic record binding

1. An immutable `gdt_observation_request_core_v1` binds operation, current source
   manifest, original dependency-fixed file, frozen scope-policy identity and
   output-folder label. It contains no proposal, decision, anchor or seal digest.
2. Source expectations, dependency inputs, activity scope/rights, historical index
   and qualification records bind that same operation/core. The qualification
   index binds the other thirteen ordinary records, never itself.
3. The proposal binds original request bytes, all fourteen ordinary receipt rows,
   protected identities and exact interpreter/profile digest/bootstrap/full
   ten-element argv. The argv contains the core request-file path and its hash.
   Path labels are inspected with pure path classes; no path is opened.
4. Review binds proposal bytes. Decision binds proposal, review and activity-rights
   bytes. Separately supplied external decision evidence binds proposal/request/
   review/decision to a caller-selected external digest. A locally rehashed chain
   cannot replace an unchanged outside anchor.

The core contains no circular authority reference. Future execution integration
must consume decision evidence separately from this immutable core; it must not
silently alter the core or reinterpret it as the current pending request schema.
No future operational launcher argv has been assembled here. Exact argv validation
uses an inert invented bootstrap in tests, not the actual disabled bootstrap.

Technical agreement with an external anchor is not authentication of its origin,
human authorization, legal sufficiency or freshness. Those facts remain outside
this pure validator. Interpreter/profile digest and source path declarations are
likewise expectations, not host or mapped-code attestation.

## Ordinary and source semantics

| Roles | Validation and limits |
|---|---|
| basis, source_manifest, prerequisites, binding_plan, role_authority, binding_schema | Byte-identical supplied original comparisons; original gate semantics and historical truth are not rerun or authenticated |
| authored_source_manifest | 49 child + 2 host expected source buffers; bounded unique relative Python paths and original hashes; exact prepared46-to-process51 projection |
| authored_source_receipts | Original-buffer receipts and manifest identity; review expectations only, freshness false |
| dependency_packet, dependency_fixed | Existing pure runtime packet binder checks original config/cache text, expectation/package/proof/root hashes and prior dependency review; exactly five child helper source aliases plus canonical prepared-map closure |
| activity_scope | Exact frozen limits/effects/stop rules, full I/O accounting and seventeen historical blockers |
| activity_rights | Preserved owner facts, same five decisions; pending, allow_scope or deny_scope with bounded evidence references; no rights inference |
| historical_evidence_index | Comparison-only receipts, nine basis-role names and unchanged seventeen blockers |
| qualification_index | Original other-thirteen receipts, source identity, bounded source/synthetic evidence references; freshness and actual-runtime verification false |

The six adapter function roles share their single source as before. Both the
process-role projection and dependency alias mapping must agree with the intended
adapter call. Internally consistent alternate source aliases are insufficient.
The original dependency review ID cannot be substituted with the new review ID.
Derived closure bytes are canonical JSON metadata, not Python source or a file.
The inventory establishes expected byte/role agreement, not complete execution
closure. Historical comparison semantic validity remains explicitly unverified by
this contract and still belongs to the retained gate during future integration.

Frozen scope remains two firmware opens, four full passes / 4,096,071,392 source
bytes, two metadata leads, 32,768 descriptor bytes each and 65,536 total, sequential
raw allowances 73,728/139,264, one preparation/two pipelines, and fixed supervision.
No inode/bitmap/directory/content interpretation, raw component output, network or
camera step is added. Complete stream decoding necessarily handles unselected
bytes. Retention allowances are not process-memory caps; raw reference release is
not secure erasure. Stop rules prohibit automatic retry/reboot/rollback after
unknown completion. All five **actual** activity decisions remain pending.

## Qualification and review

**98/98 passed**: 23 new and 75 retained (authority grammar, dependency semantics,
scope and pending launcher); zero failures/errors/skips, exit 0, **18.706s** suite /
**19.720849s** wrapper. **138 source pins stable**. Four direct public
CLIs (new contract and unchanged launcher/child/metadata) refuse with exit 2 and
empty stdout/stderr. No full historical process suite rerun; no runtime source
integration or actual input was qualified.

Adversarial cases rehash local edges while retaining semantic mutations: changed
scope/I/O/exclusions/stop rules, source/role substitution, dependency alias
omission/permutation, prior-review and config/cache hash-domain changes, retained
comparison replacement, freshness promotion, command/bootstrap/request mismatch,
undecided/refused evidence, outside-anchor mismatch, extra/protected ordinary roles,
duplicate/nonfinite/deep/oversized JSON and wrong buffer types. The no-I/O test
blocks file opens/process creation/RuntimeOps while pure validation succeeds.

Independent source review required the exact five-helper/closure alias fix; the
earlier passing two-alias fixture was too weak for the intended call. It also
confirmed the prepared-role projection, anchor bounds and dual-parser path guard.
Corrected source/test hashes were reviewed before final qualification. This is
static review plus main-agent host tests, not independent runtime reproduction.
[Exact commands, source hashes and evidence](sessions/20261020-RA-003-observation-contract.md).

Next single work package: **RA-003: integrate the reviewed pure observation contract into a separate disabled source-captured outer preflight and saved-parent validation path. Derive the explicit source-roster delta, immutable request-core and separately supplied authority-record bindings; preserve original comparison inputs, exact dependency projection, fixed I/O/supervision limits and the pending route. Qualify complete, changed-anchor/source/argv, undecided and cleanup/refusal cases with invented records and intercepted runtime only; independently review before actual record assembly. Keep public activation disabled and all actual activity decisions pending; no firmware/constants/native payload reads, installed dependency activation, downloads/uploads or camera contact.**
