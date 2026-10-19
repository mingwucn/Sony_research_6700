# RA-003: lossless legacy dependency adapter

2026-10-19. Branch `codex/ra003-legacy-dependency-adapter`, parent `9e606b9`.
Evidence: **static-inference**, **offline-tested**. English and native Wi-Fi FTP
remain primary; FL2/FL3 and custom looks remain deferred/separately gated.

Previous goal turn: **progress**, completing/reviewing the detached successor
contract. Current goal turn: **progress**, auditing the actual authored producer
schemas and qualifying a separate lossless legacy adapter. The overall
pre-camera objective remains incomplete.

## Result and producer audit

[Design, identities and predicate matrix](../LEGACY_DEPENDENCY_ADAPTER.md).
The existing producer cannot losslessly emit the prospective successor schema:
publication is one combined journal marker; guard installation/completion and
cleanup are not separate journal events. A schema rename or reconstructed
fsync event would invent historical evidence.

The adapter returns `legacy_records_consistent_with_blockers`, preserving the
original raw/journal text and detached expectation/package/configuration/
completion records. It validates corresponding source/descriptor/native records,
both event number domains, vector metadata, startup and the publication/callback
sequence. No new events are emitted. All authority and feature/recovery/write
flags remain false. Unknown fields refuse rather than being silently discarded.

Qualification covers the exact five-native-load Windows/ctypes profile, with
CPython 3.13.12 and version 3.24.1 package metadata. AESNI-absent and other
platform/backend variants refuse. This is not complete validation of dependency
internals or proof that its alleged activity happened.

Only ordinary authored producer source was inspected. Its public known-answer
vector metadata was extracted by AST literal parsing, not source execution.
No actual saved dependency receipts/configuration/cache, firmware, operational
constants or native payload was read. Existing producer and historical records
are unchanged. The public test keys are not private inputs.

## Development failures and independent review

Initial qualification: **50 cases, 49 passed / one failed, exit 1**, 8.729s suite /
8.9328868999728s wrapper. The implementation correctly refused a Boolean count
as `integer`; a test expected `legacy_vectors`. Only that expected error code
was corrected. No predicate was relaxed. Initial source/test snapshots and
complete raw logs remain private.

Two owner-authorized local source reviewers found real gaps before any actual
application:

- Initial vectors were merely shape-checked, although the producer requires
  exact public known-answer metadata. A fixed reviewed plan digest and correct
  public fixture now bind the values, including rehashed-substitution refusals.
- Startup module membership could contradict the `_ctypes` flag; they now bind.
- Source-byte metadata needed the producer's 1 MiB individual / 4 MiB aggregate
  bounds. Fully rebound oversized inputs now refuse.
- Vector events could occur during unfinished imports or before their AES/mode
  native completions. These prerequisites now bind; lazy CBC remains valid.
- Producer canonical raw publication and event bounds were missing. Canonical
  raw plus newline is at most 2 MiB; each raw/journal event plus newline at most
  32,768 bytes, separately from preserved original text.

Intermediate **56/56 passed**, zero skips, exit 0, 10.764s suite /
10.983817100001033s wrapper. Review then found the native-order and publication
bounds gaps; four further regressions cover them.
Final **60/60 passed**, zero skipped, exit 0, 13.984s suite /
14.19006300001638s wrapper. Both reviewers accepted final exact source/test
identities for the narrow blocked-envelope scope. They read source and saved
invented-test logs only: no test execution or independent reproduction claimed.

## Exact commands and results

Host: Windows AMD64, CPython **3.13.12**, interpreter
`C:/ProgramData/miniconda3/python.exe`.

- `git status --short --branch`: clean on `codex/ra003-successor-contract-qualified`.
- `git switch -c codex/ra003-legacy-dependency-adapter`: exit 0.
- `Get-Content` and `Get-FileHash` of the two existing authored producer files:
  source-only audit, no import or execution. Their hashes are in the design.
- Host-authored standard-library stdin script through the interpreter below:
  AST parse/literal extraction of only public vector constants from the pinned
  runtime source, reconstruct six metadata rows and hash canonical JSON.
  Plan SHA-256 `a914aca415d20a87a56440f36944f7ac6082ecbc36387b68694175a579bc43b5`.

Focused command, executed for the three justified development versions above:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests',pattern='test_dependency_legacy.py'));raise SystemExit(not r.wasSuccessful())"
```

Full current-tree standard-library regression:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));raise SystemExit(not r.wasSuccessful())"
```

**377 cases: 374 passed, three skipped, exit 0**, 53.688s suite /
54.54892450000625s wrapper. Composition: 317 inherited + 60 new cases. Skips
cover the Windows-inapplicable fork and two unavailable real symlink cases.
Full log SHA-256: `21ed70197f5bbf6f38531ff45cc63f048d975edec959513c6ed0f006ad7c1123`.

Raw stdout/stderr, exact argv, source/log hashes and elapsed times are retained
privately. Standard-library wrappers propagated each child exit code. Historical
private gate suites, active dependencies, real server/camera behavior and actual
record application were not tested.

| Qualified source | SHA-256 |
|---|---|
| tools/dependency_legacy.py | 13c6f6e7ca84d9cd24bdbd2060310e355fea697f5af743c3f3fe765efbef76af |
| tests/test_dependency_legacy.py | 7c466935ddf4e34e94d571edc7e007fcfbeb302869ccafeaa8a3a0e1b9c7812c |

Shared validator SHA remains
`63eb311df4c818458edd28dd9853c3c20234460f3cf145eb16886ef0abbb12f3`.

Changed public files: the adapter and test above, research/LEGACY_DEPENDENCY_ADAPTER.md,
this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md and
research/STATE.json. Private session and feature notes are synchronized with
exclusive backups. Exact-path staging, JSON and whitespace checks; source lock
and prior producer/source pins unchanged. No push.

Unresolved: producer/source authority, retrospective expectation/input binding,
cache contents, historical event truth, missing journal/open-mode evidence and
fresh runtime observation. Historical dependency/native-policy blockers remain
recorded. No actual saved-record application or runtime activation performed.
Exact-body compatibility, English/native FTP implementation and verified
rollback/recovery remain unproved. No new owner fact is needed for the next
offline package.

Camera commands: **none**. No new network/download/install, upstream launcher,
dependency/native execution, protected-input read, private upload, driver or
device change. No feature, operational, recovery or device-write gate passed.

## Next single work package

**RA-003: bind the adapter, shared validator and exact producer identities into
one saved-metadata diagnostic with explicitly retrospective expectations;
qualify source substitutions and complete input cross-bindings, then obtain
independent source review before a once-only ordinary saved-record
application.** No native dependency loading, protected-input inspection or
camera contact.
