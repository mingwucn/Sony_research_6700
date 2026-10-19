# RA-003: successor dependency evidence contract

2026-10-19. Branch `codex/ra003-successor-contract-qualified`, parent `d477e12`.
Evidence: **offline-tested**, **static-inference**. English and native Wi-Fi FTP
remain primary; no feature or device gate passed.

Previous goal turn: **progress**. It verified the unchanged public reference and
recorded evidence limits. Current goal turn: **progress**. It completes the
previously unfinished pure dependency contract, verifies regression coverage and
publishes its source-review findings and limitations. The overall pre-camera
objective remains incomplete.

## Result

[Design and exact boundaries](../SUCCESSOR_DEPENDENCY_CONTRACT.md).
`tools/dependency_evidence.py` checks a closed expectation, package manifest,
installed proof, observed origins, native intent/audit/completion and ordered
events. Separate package/runtime roots preserve the external trusted-origin
domain. Exact supplied UTF-8 receipt/journal hashes are bound to checked event
projections. The raw transcript ends at guard completion, before later events
refer to its digest, avoiding self-reference.

These are detached records and invented transcripts. The module does not open
actual paths, execute vectors, load dependencies or authenticate historical
events. New schemas do not describe an already implemented production emitter.
There is no existing raw-format adapter or saved-actual-record application in
this package. All execution/feature/operational/recovery/write authority remains
false, including the unsupported before-any-cipher-use assertion.

## Review and negative results

Two independent owner-authorized local reviewers inspected authored source.
The first review found that raw/journal digests were merely caller assertions
and that the aggregate serialized-size check happened after allocation. The
final source requires exact supplied transcript bytes and matching projections,
and counts escaped scalar/key/container representation before aggregate
serialization. These checks establish supplied-data consistency, not durable
storage or truthful loader observations. The byte bounds are not a whole-process
memory limit. Both reviewers found no remaining blocker for this narrow scope.
They did not execute tests or dependencies or inspect actual firmware/receipts.
One reviewer also checked the saved invented test log and source/log identities.
Independent reproduction is **not** claimed.

Initial development: **78 cases, two failed, exit 1**, 13.549s. Both malformed
inputs were correctly refused, but two tests expected a later error category
instead of the earlier `integer` refusal. A second pre-correction run preserved
the full failure log: 78 cases, two failures, exit 1, 13.420s. Its logging wrapper
returned 0 while recording child exit 1; this is not a passing qualification.
Only the two expected error categories were corrected; production predicates
were not relaxed. Eleven further negative cases brought the focused total to
89. Raw logs, development snapshots, commands and review notes remain private.

## Exact commands and results

Host: Windows AMD64, CPython **3.13.12**, interpreter
`C:/ProgramData/miniconda3/python.exe`.

- `git status --short --branch`: initially branch
  `codex/a6700-reference-review-20261019-latest`, with the two unfinished authored
  source/test files untracked; tracked tree clean.
- `git switch -c codex/ra003-successor-contract-qualified`: exit **0**.
- Standard-library SHA-256 comparison with the saved focused qualification:
  both final source identities unchanged. Source lock also unchanged.

Focused development command (qualification already saved before this
continuation; not rerun merely to repeat an unchanged result):

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests',pattern='test_dependency_evidence.py'));raise SystemExit(not r.wasSuccessful())"
```

**89 passed, zero skipped, exit 0**, 16.728s suite / 17.05953560001217s wrapper.

Full current-tree regression executed in this continuation:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));raise SystemExit(not r.wasSuccessful())"
```

**317 cases: 314 passed, three skipped, exit 0**, 35.615s suite /
36.31449729995802s wrapper. Composition: 228 inherited cases plus 89 new cases.
Skips are the Windows-inapplicable fork and two unavailable real-symlink cases.
Tests exercise invented records, strict schema/type/path/identity refusals,
source/config/roster substitutions, transcript substitution even with recomputed
digests, duplicate JSON keys, bounds, and callback/durability ordering.
Historical private gate suites, actual-input workflows, camera behavior and
real FTP delivery were not tested.

| Qualified source | SHA-256 |
|---|---|
| tools/dependency_evidence.py | 63eb311df4c818458edd28dd9853c3c20234460f3cf145eb16886ef0abbb12f3 |
| tests/test_dependency_evidence.py | 021750089ea2777f4952f6aadc189db8faf6ad2b0a749ea4cd1c2dd7386df36a |

Full regression log SHA-256:
`4d580d29720bf456e8bcf532ff228daf5cbac8db0a0d7fccca8421b0ebd0166d`.
Raw test commands/results and source-review records are retained privately.

Changed public files: source and test above, the design linked above, this
report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md and
research/STATE.json. Private session/feature notes are synchronized with
exclusive backups. Reviewed exact-path staging and whitespace/JSON checks;
no push, source-lock change or inherited implementation modification.

Camera commands: **none**. No new network/downloads, upstream launchers,
installed dependency execution, firmware/constants/native payload reads,
private uploads, device changes, feature support or recovery/write gate.
Historical `dependency_manifest_unobserved` and `native_policy_unobserved`
blockers remain recorded. Pre-execution policy approval/source authority,
producer/adaptor compatibility, fresh operational context and eventual
exact-body recovery remain unresolved.

## Next single work package

**RA-003: audit the existing authored dependency producer and saved-record
schemas, then implement and qualify a lossless adapter on invented old-format
receipts, preserving original transcript bytes, unknown fields and unsupported
claims as explicit refusals/blockers; obtain independent source review before
applying it to saved actual records.** No dependency execution, protected-input
inspection or camera contact.
