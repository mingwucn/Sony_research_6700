# RA-003: retrospective metadata comparison and preserved refusal

2026-10-19. Branch `codex/ra003-retrospective-binding`.
Evidence: offline-tested, static-inference. Previous goal turn: progress
(owner-requested public-reference check completed). Current turn: progress
(new composition qualified and an actual saved comparison attempted once).

**The saved comparison was not accepted.** One reviewed application exited **1**
with `needs_review / legacy_binding`. All ten planned input hashes matched;
the refused predicate is not yet localized. No retry or threshold change.

## Changes and scope

Added `tools/dependency_retrospective.py` and eighteen invented-data tests.
The pure module derives an explicitly retrospective expectation and invokes the
unchanged legacy adapter. Package origins use saved installed receipts/proof;
trusted origins and roots use saved observations. Root digests are named path
labels, not directory observations. Configuration canonical digest and input
file hash remain distinct. Producer/cache digests are declarations, not source
authority or cache-content validation. Every legacy blocker remains.

The private diagnostic reads five ordinary authored sources and five ordinary
saved metadata records under exact path/hash/bounds checks. Three pure helpers
execute from checked buffers; two producer sources are hashed without execution.
All ten input pins are checked before helper execution. The `tools` namespace
is restored. The old descriptor audit is explicitly only a selected-field
projection; its entire ledger is not revalidated. Details:
[design](../RETROSPECTIVE_DEPENDENCY_BINDING.md).

Two independent local source reviews accepted the pure component. Review of
the first wrapper found an unchecked external-reader bootstrap and an omitted
read count. Both were corrected by removing that bootstrap and using an
embedded bounded ordinary-file reader for all ten inputs. Eleven wrapper tests
cover byte substitutions before execution, namespace restoration, exact output
accounting, real temporary-file success/refusal and sticky no-replay behavior,
plus pre-open directory/oversize/hardlink refusal. Both reviewers accepted the
corrected exact source. No reviewer executed code or opened old input bodies.

## Commands and results

Host: Windows AMD64; interpreter `C:/ProgramData/miniconda3/python.exe`,
CPython **3.13.12**, flags **`-I -S -B -X utf8`**.

- `git status --short --branch`: clean start on
  `codex/a6700-reference-check-20261019`, HEAD `c7c5474`.
- `git switch -c codex/ra003-retrospective-binding`: exit **0**.
- Focused authored standard-library unittest discovery via stdin, pattern
  `test_dependency_retrospective.py`, explicit repository import root:
  **18/18 passed**, zero skips, exit **0**, **8.916s** suite /
  **8.970952700008638s** wrapper. `focused.log` and `focused.json` retained.
- Initial private wrapper qualification:
  `& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-retrospective-binding/test_saved_diagnostic.py -v`:
  **8/8 passed**, zero skips, exit **0**, **1.769s**. Review then found the
  bootstrap/accounting issues above; passing tests did not establish readiness.
- Corrected wrapper qualified through standard-library `importlib` loading of
  that authored test module and `unittest.defaultTestLoader.loadTestsFromModule`:
  **11/11 passed**, zero skips, exit **0**, **2.571s** suite /
  **2.571494599978905s** wrapper. Exact hashes/log in `wrapper-tests-r2.json`.
- Full host regression used this exact PowerShell pipeline:

```powershell
@'
import hashlib,json,pathlib,sys,time,unittest
root=pathlib.Path.cwd();sys.path.insert(0,str(root));session=root/'private/sessions/20261019-RA-003-retrospective-binding'
start=time.monotonic()
with (session/'full-host.log').open('x',encoding='utf-8') as log:
 suite=unittest.defaultTestLoader.discover('tests',pattern='test_*.py')
 result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
receipt=dict(total=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),exit_code=0 if result.wasSuccessful() else 1,wrapper_seconds=time.monotonic()-start,log_sha256=hashlib.sha256((session/'full-host.log').read_bytes()).hexdigest())
with (session/'full-host.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2));print((session/'full-host.log').read_text()[-450:]);sys.exit(receipt['exit_code'])
'@ | & C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -
```

Result: **395 cases, 392 passed, three platform skips, exit 0**;
**57.942s** suite / **58.292091299954336s** wrapper. Three inherited skips
cover POSIX fork and two Windows real-symlink cases. These are host tests,
not target feature, access, firmware or recovery tests. Full log SHA-256:
`ee54ff2900f8536b2e70f366373d87ef270e0dd847d2420376c33f8baaf59b19`.

One pre-application freeze-preparation command exited **1** because it assumed
both reviewers used the same JSON field layout. No application directory or
freeze had been created. The distinct saved review schemas were inspected;
their exact source/test pins were then checked without relaxing acceptance.
The corrected freeze preparation exited **0**. This was not a failed/repeated
actual-record application.

The once-only saved application command was:

```powershell
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-retrospective-binding/saved_diagnostic.py
```

Result: **exit 1**, tool wall **0.9133515s**, stdout
`{"status": "needs_review", "code": "legacy_binding", "camera_commands": []}`.
Ten regular-file input reads returned **2,437,413 bytes**: **90,250 authored
source bytes** and **2,347,163 ordinary metadata bytes**. All exact SHA-256 pins
matched before the pure comparison ran. This count covers explicit diagnostic
inputs, excluding ordinary interpreter/stdlib/program startup. No accepted
`result.json` or `completion.json` exists; exclusive `started.json` and
`refusal.json` remain. The parent saved the observed tool exit separately; it
is not an independently observed process-completion receipt.

Two independent source/outcome reviews checked these new receipts against the
frozen roster without reopening older actual input bodies. Both accepted only
preservation and interpretation of the refusal. `legacy_binding` is reused by
configuration/cache/vector and event comparisons; no particular mismatch or
root cause is proved by that code alone. No saved source or receipt was changed.

## Pins and preservation

| Authored source | SHA-256 |
|---|---|
| tools/dependency_retrospective.py | 8041f0b640f8aad98ca261c319b45dfd18a6f73cae689310bd7c784988cb4162 |
| tests/test_dependency_retrospective.py | 5fd5ddbe54238cdb751a837b097b1abb82b043573ae2d3f88cce36e88c2042c6 |
| Private saved_diagnostic.py | 95001132c8b4cdc3d26c6d9ceb42e750078c79548d6d819137785b0561895369 |
| Private test_saved_diagnostic.py | 2e04aa883bf37eef310c1264d8784dacca209cbd114ab9040fee68533a553ec9 |
| Preserved refusal.json | 40d63a3447253eef9ef5e5a8639813892a6a7dd983d70d93966ee1a322cc1591 |

Original core/adapter and producer identities remain unchanged. Source lock
unchanged. Private evidence lives under
`private/sessions/20261019-RA-003-retrospective-binding`; state and feature notes
were synchronized after exclusive backups. Only authored public code, tests,
design, session report, backlog, handoff, feature note and sanitized state are
eligible for staging. No third-party inputs or private outputs are staged.

## Remaining prerequisites and next work

English and native camera-to-server Wi-Fi FTP remain primary and unvalidated.
FL2/FL3 is deferred; calibrated looks remain separately gated; the optional
host bridge is separate. The comparison refusal must be localized before any
successor application. Historical prior policy/authenticity, cache contents,
fresh runtime evidence, exact-body mapping and recovery remain unproved.
The frozen dependency/native-policy blockers remain recorded and uncleared.

**Camera commands: none.** No firmware, operational constants, cache body,
installed dependency or native payload was opened/executed. No network access,
upload, upstream launcher, driver change or device operation in this package.
No feature supported, recovery proved, execution authorized or device-write
gate passed. Goal remains active; full pre-camera preparation is incomplete.

Next single work package: **RA-003: localize the frozen `legacy_binding`
refusal with named source predicates and invented mismatch tests, then
independently review a narrowly scoped saved-digest diagnostic before any new
actual-record application.** Preserve the failed attempt; no protected-input,
dependency/native or camera access.
