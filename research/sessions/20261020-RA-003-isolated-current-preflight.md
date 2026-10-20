# RA-003: isolated current preflight qualification

2026-10-20. Branch `codex/ra003-current-preflight-integrate`.
Evidence: static-inference, offline-tested. Previous goal turn was progress:
requested public-reference check committed as `368b39e`. This turn qualifies the
unfinished host integration; the overall pre-camera objective remains active.

The [assessment](../ISOLATED_CURRENT_PREFLIGHT.md) describes original record binding,
separate comparison/current/adapter graphs, explicit source-root conversion and
the pre-observer boundary. Source lock, frozen scope and historical observations
are unchanged. English/native FTP remain first; FL2/FL3 deferred.

## Final qualification

**175/175 passed**, zero failures/errors/skips, exit **0**.
Composition: **159 public regressions + 16 invented process cases**.
Wrapper 266.935385s; 187 source/reference pins stable before/after.
Interpreter `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12, Windows AMD64,
isolated/no-site/no-bytecode, optimize 0.
Raw qualification log SHA-256: `2d78f481e934e85ef1ac50c6b459eda007ede76dc7e1d24e8c11c0728357393d`.

| Public source/test | Qualified working-file SHA-256 |
|---|---|
| tools/dependency_outer_metadata.py | `de0110f5d054992df9058229c1fa3d14554f4296d828e011eaa2053fb9901d81` |
| tools/detached_metadata_loader.py | `229938e19c51990f1967db952a1f2984552886aabd2ceb81afc3fd524515cb25` |
| tools/dependency_launch_context.py | `8c6f41d03bec5e4c213c01cdb8afdeaf0f110bfcb177e079471db3ee2baa4927` |
| tests/test_dependency_outer_metadata.py | `3ebbc5306c47676405a798ab184a9ec16605f2e1d24b01ca67ec7b6b0903ab1a` |
| tests/test_detached_metadata_loader.py | `9be31f4490fb55ce6a2fe95c9f1e783e157ddab67a4c9cbb75bd2ccc619c55ac` |

The process source map has 61 labels; prepared map remains 46 labels/41 unique paths.
Fourteen comparison helpers and three current helpers execute from captured bytes;
the three-helper adapter owner remains distinct. Current fourteen-record validation
runs before `prepare_modules`. The original four gate documents, six basis records,
historical inputs and prepared request bytes are bound without rewriting originals.
The child result hash and closed saved-result schemas bind parent reconciliation
to original request/record hashes, comparison seal and explicit source roots.

Complete invented execution verifies eleven dependency artifacts, two bridge
envelopes and both GDT phases: two stream opens/two closes, four identity-cipher
constructions, one factory, one record close and one callback release. Early
metadata refusals show zero preparation/record/stream/cipher/factory attempts and
once-only closure of both metadata owners. Cases include changed request, basis,
history, retained source origin, live current code, comparison source buffer,
interruptions during/after load, phase-two read fault, factory interruption,
saved-result byte mutation and captured helper mutation. Semantic tampering tests
also rebind the outer hash while changing comparison seal or adding result fields.
These must remain unknown/needs_review rather than accepted preflight evidence.
The existing operation folder cannot overwrite its successful receipt on replay.

The real supervisor retains 300/5/1-second deadline/termination/join limits and
2MiB per pipe. Qualification has a separate 100-second per-process harness limit.
Every final case observed its child exit and joined/closed pipe readers; no kill,
wait escalation or timeout was needed. Timeout/log overflow policies were retained
from the earlier qualification and were not re-exercised in this focused run.

Public tests block the actual observer constructor. Process tests permit only the
fixed invented manifest/constants, fake dependency package and identity cipher.
This does not establish actual startup, current real-input semantics, dependency
activation, firmware contents, native English/FTP or exact-body applicability.
Invented receipt claims remain separate from fresh bootstrap source reads.

## Review and negative evidence

Independent source review found two gaps: all original gate-document hashes were
not yet bound to validated gate output, and saved comparison-seal semantics/closed
result rosters were not enforced by the parent. Both were repaired, with reanchored
document substitutions and rebound-hash saved-result tests. Re-review accepted the
repaired authored sources; it confers no operational or feature acceptance.

Initial qualification-v1: **169/170 passed**, one failure, zero errors/skips,
exit 1, 206.509601s, 187 stable pins. Its load-interruption injection changed global
builtins.exec, whereas the checked loader held its own copied builtins dictionary;
the case therefore completed normally instead of interrupting. The test now
patches the actual loader binding and restores it in finally. Original V1 source
snapshots, logs and result are preserved. Both complete final integration and the
corrected interruption case pass; no acceptance threshold was relaxed.

Prototype smoke-v1/v2 stopped at alias_occupied during fixture preparation.
Moving imports after binding preparation and before owner capture fixed that order.
Smoke-v3/v4 refused at outer_metadata_input_roster before any observer; the gate
intentionally retains q_snapshot_log as raw bytes, outside its parsed-input map.
The wrapper now checks every input against original gate hash/size and parses only
the gate's JSON roles. Smoke-v5 completed invented integration, exit 0. These were
prototype diagnostics, not final qualification. A separate 63-case focused public
run passed, exit 0, 13.761s; final qualification supersedes it.

## Exact commands and results

```powershell
git status --short --branch
git switch -c codex/ra003-current-preflight-integrate
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-current-preflight/driver.py private/sessions/20261020-RA-003-isolated-current-preflight/smoke-v1 complete
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-current-preflight/driver.py private/sessions/20261020-RA-003-isolated-current-preflight/smoke-v2 complete
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-current-preflight/driver.py private/sessions/20261020-RA-003-isolated-current-preflight/smoke-v3 complete
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-current-preflight/driver.py private/sessions/20261020-RA-003-isolated-current-preflight/smoke-v4 complete
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-current-preflight/driver.py private/sessions/20261020-RA-003-isolated-current-preflight/smoke-v5 complete
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path[:0]=['.','tests'];r=unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(n) for n in ['test_dependency_outer_metadata','test_detached_metadata_loader','test_dependency_current_metadata','test_dependency_launch_context']));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-current-preflight/qualify.py qualification-v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-current-preflight/qualify.py qualification-v2
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-current-preflight/record.py
git diff --check
git add -- tools/dependency_launch_context.py tools/detached_metadata_loader.py tools/dependency_outer_metadata.py tests/test_detached_metadata_loader.py tests/test_dependency_outer_metadata.py research/ISOLATED_CURRENT_PREFLIGHT.md research/sessions/20261020-RA-003-isolated-current-preflight.md docs/BACKLOG.md docs/FEATURE_PROGRESS.md docs/CODEX_HANDOFF.md research/PRE_CAMERA_READINESS.md research/STATE.json
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "qualify current metadata before isolated observer preparation"
git status --short --branch
```

Driver exit results in order: 1, 1, 1, 1, 0. Focused tests: 0.
Qualification V1: 1; final V2: 0. Raw per-process commands/results are retained
in the private final qualification result. Final pins include the executable test
closure; the later bookkeeping script only records documentation/state.

Changed public files: the three tools and two tests listed above; this report and
assessment; docs/BACKLOG.md, docs/FEATURE_PROGRESS.md, docs/CODEX_HANDOFF.md,
research/PRE_CAMERA_READINESS.md and research/STATE.json. Existing unfinished
source edits were completed on this topic branch. Private fixture/harness sources,
logs, source snapshots and session/feature notes stay ignored. Private notes are
backed up before updating; no private input or payload is staged. Staged normalized
source bytes are checked against the qualified working files before commit.

Unresolved prerequisites: concrete operational-entry migration and review; existing
five activity-specific decisions; exact-body binary/SKU correspondence; English
restriction/resource and onboard FTP mapping; verified rollback/recovery and two
independent backup locations before any write. No new blanket permission condition
is created and missing owner facts do not stop useful offline work.

Camera commands: **none**. No downloads/uploads, upstream launcher/service execution,
actual firmware/constants/native payload read, installed dependency activation,
actual activation record, driver/firmware changes or camera contact. Public runtime
and direct CLIs remain disabled. No feature/recovery/device-write gate passed.

Next single package: **RA-003: migrate the existing disabled host entry to the qualified current-preflight path, carrying the same original ordinary records through isolated startup, dependency lifetime, two-phase reader and saved-parent reconciliation. Independently review and qualify that executable path with invented inputs. Keep actual observation/public runtime disabled until the existing five activity-specific decisions are reconciled; no actual activation records, installed dependency activation, firmware/constants/native payload reads or camera contact.**
