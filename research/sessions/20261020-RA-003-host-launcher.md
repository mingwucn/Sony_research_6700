# RA-003: complete invented host launcher migration

2026-10-20. Topic branch `codex/ra003-host-launcher`.
Evidence: static-inference, offline-tested. Previous goal turn was progress,
committed as `15d7936`. The full pre-camera objective remains active.

The authored launcher now captures source text, builds the isolated bootstrap and
request, sets up owned parent helpers, invokes the frozen supervisor, and reconciles
saved child results through dependency_host_entry. Child orchestration and closed
process schemas are authored public modules. The private driver creates invented
fixtures and delegates these procedures to the public launcher. No fixture generator
or historical hardware observation is made into operational authority.

English and native FTP remain first; FL2/FL3 and calibrated looks remain deferred.
No source lock, frozen scope or historical observation was changed.

## Qualification

**207/207 passed**, zero failures/errors/skips, exit **0**;
191 public regressions and 16 invented process
cases; 284.066659s wrapper; 190 source pins stable.
Interpreter `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12 Windows AMD64, isolated/no-site/
no-user-site/no-bytecode, optimize 0. Raw log SHA-256 `d90bb19cf84404b90abb63a65dba6da29a9cd3f67ef20fe009561a7249834929`.
Private logs, executable source snapshots and per-process commands/results remain local.

| Public source/test | Qualified working-file SHA-256 |
|---|---|
| tools/dependency_host_launcher.py | `b97a527c22d069bc2924e8a5188a0432c4d7f228c527810bf9f97a89e7568ef3` |
| tools/dependency_host_child.py | `559ab4c0bfc164b8d34dfeaa3d0260e7ac0a343390c80aefa3004cfb57585d9d` |
| tools/dependency_host_process_contract.py | `6573028a4cbfbc698ae457eb8a855a20b7d3658974579b89ea0df999d7c464ba` |
| tests/test_dependency_host_launcher.py | `9aea4c913b9dbf76a0df34f087cf73d5b0947bfcd29ed808b24760d8746dfd98` |

The capture roster grows from 61 to 62 labels by explicitly including the public
launcher. The prepared adapter map remains 46 labels/41 unique paths. New files
are copied exclusively; retained buffers must match original gate bytes/hash/size.
The parent checks the complete buffer roster and request receipt map before any
bootstrap execution, including retained source paths and dependency/closure buffers.
Packet bytes, operation, folder/request path, context roots/session and exact child
argv are bound to original held/saved records before execution and again before spawn.
All captured child sources compile before execution in the isolated bootstrap.

Complete invented execution verifies eleven dependency artifacts and two bridge
envelopes, two source opens/two closes, four identity-cipher constructions, one
factory, one record close and one callback release. Early metadata failures perform
zero observer preparation/stream/cipher/record/factory work. Refused and unknown
outcomes remain distinct, including changed records/source origins, load/post-load
interruptions, live source changes, phase-two/factory faults and saved-result semantic
mutations whose outer digest is rebound. Output replay refuses overwriting evidence.

Every final process reports exit observed, pipe readers joined/closed, no timeout,
kill or wait escalation. Parent validation loader, parent helpers and bootstrap
aliases are released. The fixed 300/5/1-second supervisor limits and 2MiB-per-pipe
cap are preserved. Its timeout/log-overflow branches were not newly exercised here;
retained supervision unit regressions run, including mocked faults. Qualification
has a separate 100-second per-process harness bound.

Public tests block actual observer construction. Complete process fixtures permit
only fixed invented source/constants, identity cipher and fake dependency inputs.
Direct CLIs exit 2 before imports; run_runtime refuses real_activation_pending.
The child retains explicitly invented fault selectors for qualification; no actual
observer branch was enabled. Real interpreter/stdlib/bootstrap authenticity is not
established by caller receipts or this test suite.

## Review and negative evidence

Independent review found a parent-side execution gap: captured buffers could be
supplied independently from request/gate receipts, and substituted packets/commands
could be detected only after execution. Whole-roster, retained gate, dependency,
packet and launch-context checks now run before the first parent bootstrap load,
with no-execution/no-spawn regression tests. A second gap left an unmounted loader
unclosed after reserve_parent interrupted; cleanup is now independent of mount state
and preserves the primary failure even when cleanup fails. Re-review accepted both
repairs for this invented-only source delta; no operational acceptance follows.

Initial smoke-v1 completed before those repairs; smoke-v2 completed after them,
both exit 0. Initial focused test run used a fixture missing its invented scope:
three subtests within one test method stopped at invented_only instead of reaching
the buffer predicate (14 tests, three reported subtest failures, exit 1). Initial
source/result preserved privately. Adding the scope to the fixture fixed the test;
no production predicate changed. Corrected focused run: 14/14 pass, exit 0, 0.749s.
Final frozen qualification supersedes these diagnostics. No other failure was hidden.

## Exact commands and results

All commands ran on the host. Starting tree clean on codex/ra003-host-entry-qualified.

```powershell
git status --short --branch
git switch -c codex/ra003-host-launcher
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-host-launcher -ErrorAction Stop | Out-Null
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-host-launcher/driver.py private/sessions/20261020-RA-003-host-launcher/smoke-v1 complete
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path[:0]=['.','tests'];r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_host_launcher'));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-host-launcher/driver.py private/sessions/20261020-RA-003-host-launcher/smoke-v2 complete
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-host-launcher/qualify.py qualification-v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-host-launcher/record.py
git diff --check
git add -- tools/dependency_host_launcher.py tools/dependency_host_child.py tools/dependency_host_process_contract.py tests/test_dependency_host_launcher.py research/HOST_LAUNCHER_MIGRATION.md research/sessions/20261020-RA-003-host-launcher.md docs/BACKLOG.md docs/FEATURE_PROGRESS.md docs/CODEX_HANDOFF.md research/PRE_CAMERA_READINESS.md research/STATE.json
git diff --cached --check
git diff --cached --stat
git diff --cached
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-host-launcher/check_stage.py
git commit -m "migrate invented host bootstrap and supervisor orchestration"
git status --short --branch
```

Branch/acquisition-free authoring and both smokes: exit 0. Focused command ran
twice, first exit 1 then 0 as explained above. Final qualification exit 0.
No upstream module was imported/executed. Broader historical/full suites were not
rerun without a relevant change. Some exploratory rg reads used an incorrect
legacy filename and returned path-not-found; no operation or evidence was lost.

Changed public files: three tools, one test, this report and assessment,
docs/BACKLOG.md, docs/FEATURE_PROGRESS.md, docs/CODEX_HANDOFF.md,
research/PRE_CAMERA_READINESS.md, research/STATE.json. Private notes backed up and
updated. Qualified source pins and normalized staged source bytes are checked before
commit. Source lock and frozen scope remain unchanged.

Remaining prerequisites: operational readiness and concrete activity decisions;
actual startup/source trust/dependency observation; exact-body binary/SKU identity;
English restriction/resource and onboard FTP mapping; rollback/recovery and independently
verified backup copies on separate storage before writes. Existing rights No/unknown
and five activity-specific uncertainties are preserved, with no new blanket consent
condition inferred. Legacy role-source texts remain supplied ordinary inputs rather
than being implicitly relicensed or claimed as a self-contained distributable runtime.

Camera commands: **none**. No actual firmware/constants/native payload reads,
installed dependency activation, actual activation record, downloads/uploads,
upstream launcher/service execution, private upload or camera/driver/firmware changes.
No feature support, recovery or device-write gate passed.

Next single package: **RA-003: audit the complete migrated host launcher against the frozen operational scope and existing five activity-specific decisions, identifying concrete remaining runtime/source-trust/ordinary-record bindings and preparing one non-executable transition plan toward the next bounded offline metadata observation. Use authored source and ordinary metadata only; keep actual activation disabled and preserve prior evidence. No actual activation record, installed dependency activation, firmware/constants/native payload read, download/upload or camera contact.**
