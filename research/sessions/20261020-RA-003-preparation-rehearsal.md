# RA-003: invented preparation process rehearsal

2026-10-20, branch `codex/ra003-preparation-rehearsal`, starting commit `9fa24f2`.
Evidence: static-inference and offline-tested. English and native Wi-Fi FTP first;
FL2/FL3 deferred. Previous goal turn: progress, fresh reference findings committed
as `cf28a11` in the separate reference worktree. This turn completes the pending
preparation rehearsal and changes the next integration package.

## Outcome and boundaries

**132/132 focused standard-library tests pass**, zero failures/errors/skips,
exit **0**, **59.804s**. Seven modules include the prior six preparation/engine
modules and the host-entry regressions. All **103** captured source/test pins
were stable during qualification and revalidated afterward. RuntimeOps construction
was blocked while loading/running public suites. No historical full-suite claim.

Three private process cases completed under the retained 300-second deadline,
2 MiB per-log cap, 5-second kill wait and 1-second reader join policy. Each used
one child launch with no timeout, kill or retry. Child bootstrap binds exact
argv/profile, request, packet and **74 source roles**, checks stable file identity
and hashes, and parses/compiles all source buffers before child entry.

| Case | Observed result | Elapsed | Cleanup |
|---|---|---|---|
| Complete invented preparation, `complete-v7` | Child 0, supervisor 0, wrapper 0; saved-parent consistency accepted | 21.348s | Callback, preparation, helper and adapter closed; all parent owners/records closed |
| Altered captured source, `source_tamper-v1` | Child 2, supervisor 1, wrapper 0 for expected `source_binding` refusal | 0.276s | Parent owners/records closed; child entry never reached; no child cleanup claim |
| Altered saved preflight, `preflight_tamper-v1` | Child 0, supervisor 0, wrapper 0 for expected `operational_saved_preflight` refusal | 21.673s | Child owners closed; parent refusal closes acquired owners |

The full invented case executes the real retained metadata gate, source refresh,
materialization, ScopedCallbacks, disabled child engine, saved-preflight wrapper
and owned supervisor. Only newly generated invented stream/constants and a fake
dependency are used. Runtime dispatch, completion collection and parent runtime
verification are explicit substitutions. OS process facts are observed for this
qualification harness; the production outer path remains unassembled. The source
tamper changes only a newly captured disposable authored copy; its original is
preserved. All other captured source hashes revalidate. This is not actual
activation, installed dependency/native loading or firmware analysis.

The new runtime-shaped completion collector is unit-qualified with intercepted
saved reads, including its fixed `invented=False` grammar and refusal of parent
mode before I/O. It is not exercised end to end by the invented collector.

## Reviewed changes and failures preserved

`dependency_operational_entry` retains the bound runtime inputs and collects
completion evidence before helper/adapter teardown. Collection failure prevents
a success result and still performs once-owned cleanup. It rechecks request and
owner integrity before cleanup. `dependency_successor_wiring` supplies the fixed
saved-composition/bridge-hash/stdout collector without activating an observer.

`dependency_host_entry.cached_module` now copies standard builtins explicitly.
Without this, execution inside the detached outer loader inherited its tools-only
importer and the retained gdt_preflight/ext_preflight import refused. The retained
bootstrap still applies its own checked AuthoredSources importer. This boundary
does not authenticate the interpreter/stdlib. Three test files cover collection
order/failure, fixed saved grammar/mode, and the nested-bootstrap importer.

Local source-only independent review accepted the six public deltas and two
private rehearsal helpers, with no residual material finding. All eight reviewed
raw-byte hashes revalidate in the private audit receipt. No review read firmware,
constants or native payloads. Rehearsal/bootstrap helpers are qualification-only.

Six earlier exploratory complete attempts stopped and remain preserved:

1. Original `complete` (v1), wrapper 1: qualification imports occupied a clean alias.
2. `complete v2`, wrapper 1: unrelated old metadata-fixture pin assertion; obsolete
   fixture chain removed from this new rehearsal, no threshold relaxed.
3. `complete v3`, child 2/wrapper 1: relative helper origins; corrected to captured
   absolute source origins.
4. `complete v4`, child 2/wrapper 1: real nested importer defect described above.
5. `complete v5`, child 2/wrapper 1: fake dependency helper aliases missing.
6. `complete v6`, child 2/wrapper 1: fake aliases installed before preparation;
   moved to the intercepted runtime dispatch, preserving the clean-start guard.

Each correction used an exclusive new attempt folder. None was an automatic retry
of an unknown device operation. Failed-child cleanup is not proved. Earlier private
harness versions were not all separately source-snapshotted; saved attempts and
traces are retained, while final source capture/review anchors the accepted runs.

## Exact commands, interpreter and evidence

CPython **3.13.12**, Windows AMD64, no-site isolated startup, optimize 0:

```powershell
git switch -c codex/ra003-preparation-rehearsal
# Failed exploratory attempts, each exit 1; preserved, corrected between runs
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/rehearse.py complete
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/rehearse.py complete v2
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/rehearse.py complete v3
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/rehearse.py complete v4
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/rehearse.py complete v5
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/rehearse.py complete v6
# Accepted complete case and expected negative cases: each wrapper exit 0
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/rehearse.py complete v7
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/rehearse.py source_tamper v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/rehearse.py preflight_tamper v1
# Focused suite, exit 0
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/qualify.py public-v1
# Saved-result, reviewed-source and captured-source reconciliation, exit 0
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/audit.py
```

Pending test and preflight processes were polled on their existing handles to
terminal exit 0 after the intervening reference review; neither was restarted.
Qualification log SHA-256:
`308eed0a03e6c51bf5f4f0e885c1716a71b6ffaa297330c8466b2abe8ad470d6`.
Private `audit.json` records eight reviewed source pins, all 103 qualification
pins revalidated, exact result/request/cleanup hashes and process observations.
The parent harness is trusted qualification code, not a production source-trust
or authority proof. Original frozen scopes, source lock and actual evidence stay
unchanged. Five activity-specific decisions remain pending.
Final independent notes review identified stale top-level latest-report/focused
suite pointers from an earlier package. Public/private pointers now refer to this
132-case result; previous values are backed up and historical evidence retained.

Changed public code/tests: `tools/dependency_host_entry.py`,
`tools/dependency_operational_entry.py`, `tools/dependency_successor_wiring.py`,
`tests/test_dependency_operational_entry.py`,
`tests/test_dependency_operational_preparation.py`,
`tests/test_dependency_successor_wiring.py`. Changed public notes: this report,
OPERATIONAL_PREPARATION, BACKLOG, FEATURE_PROGRESS, CODEX_HANDOFF,
PRE_CAMERA_READINESS and STATE. Private session/feature notes are backed up before
adding the same evidence. Only these reviewed public files are staged.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/record.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-preparation-rehearsal/repair_latest.py
git diff --check
git add -- tools/dependency_host_entry.py tools/dependency_operational_entry.py tools/dependency_successor_wiring.py tests/test_dependency_operational_entry.py tests/test_dependency_operational_preparation.py tests/test_dependency_successor_wiring.py research/OPERATIONAL_PREPARATION.md research/sessions/20261020-RA-003-preparation-rehearsal.md docs/BACKLOG.md docs/FEATURE_PROGRESS.md docs/CODEX_HANDOFF.md research/PRE_CAMERA_READINESS.md research/STATE.json
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "feat: qualify invented preparation through supervised child"
git status --short --branch
```

Camera commands: **none**. No actual firmware/constants/native payload or actual
activation-record reads/assembly, installed dependency activation, upstream
execution, network acquisition/upload, feature support, recovery or device-write
gate. English/native FTP and recovery remain unproved. The separate reference
check changed no implementation or scope here.

Next single work package: **RA-003: implement and independently review the separate
authored disabled operational outer launcher**, moving the qualified source
capture/bootstrap/supervisor/pending-preflight/result flow out of the private
fixture harness. Derive the exact executing source roster, retain fixed limits
and separate fixture generation; qualify invented complete/refusal/cleanup cases
with explicit runtime substitutions. Keep actual activation disabled and all five
activity-specific decisions pending; no actual input or camera contact.
