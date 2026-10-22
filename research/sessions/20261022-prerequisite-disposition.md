# Five-entry correction and current-context implementation — 2026-10-22

Baseline: clean `f64cf34`; branch
`codex/ra003-prerequisite-disposition-20261022`.

The owner asked what the five prerequisites meant, what input was required and
what could be resolved offline. The later instruction explicitly stopped legal
research/questions. Camera contact remains on hold. No further owner input is
needed for the technical preparation undertaken here.

The prior assertion that no actionable offline implementation remained was too
broad. It treated our own scope decision and implementation work as missing
external approvals. [Current dispositions](../ANALYSIS_PREREQUISITES.md) correct
that framing; historical frozen operation records remain unchanged.

## Resolved work

The known notice inventory and public reference provenance were reconciled
without asking the owner to provide keys, derivation histories or camera records.
Unknown product-local notices and independently unreproduced derivation remain
recorded limitations, not new owner intake requirements. Legal investigation and
the additional-agreement question stopped at the owner's direction; no answer
about another agreement was inferred from that instruction.

The selected two-lead GDT study has a technically justified question, dependent
two-phase sequence and fixed resource/stop boundaries. Four source passes follow
the chosen validation method, without a claim that it is the only possible
method. This resolves the engineering scope item; it does not establish English
resources, a native FTP backend or target compatibility.

`tools/dependency_host_entry.py` adds `make_current_context` alongside the
unchanged legacy constructor. It reuses the same twelve-field context structure
and binds canonical current request bytes/hash, operation, request/packet paths,
source rows, preserved document identities and interpreter/argv. Conflicting
path/hash mappings refuse instead of silently overwriting. Nested basis and source
manifest data are copied, preventing caller mutation from retargeting the result.

The constructor is pure. The caller must still use the existing complete source
roster/capture, retained-source and reviewed-bootstrap request validators. The
constructor compares supplied identities; it does not authenticate them or
replace fresh saved-file checks. Path containment here is lexical. Existing I/O
policy remains responsible for actual file/link safety.

The old v6 refusal and runtime entry refusals remain. No automatic runtime path
calls the new constructor yet. `tests/test_dependency_current_context.py` uses
the real v6 validator code with invented policy/records, invented ordinary source
files and an inert parent-supervisor handoff. The latter substitutes control
methods; it does not qualify the retained runtime context checker or a complete
real operation. Tests also demonstrate that omitted source roles and a changed
self-consistent bootstrap still need the existing caller validators.

## Review and validation

`ftp_host_review` resolved the technical-scope and preparation-ownership issue
and implemented the constructor/tests. `native_source_review` reviewed operation,
path, digest and alias handling, and required explicit caller-validation and
inert-handoff limitations. `ftp_requirements` reconciled the existing notice
inventory. The primary agent reviewed the final authored diffs.

Host interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython **3.13.12**;
PowerShell **7.6.5**. **61 tests passed**, including **13 new tests**, zero
failures/errors/skips, exit **0**; unittest **25.907s**, wrapper **27.107s**.
Exact successful PowerShell command:

```powershell
@'
import pathlib, sys, time, unittest
root=pathlib.Path.cwd()
sys.path[:0]=[str(root),str(root/'tests')]
folder=root/'private/sessions/20261022-prerequisite-disposition'
folder.mkdir(parents=True,exist_ok=True)
path=folder/'current-context-tests-01.log'
with path.open('x',encoding='utf-8') as stream:
    started=time.monotonic()
    suite=unittest.defaultTestLoader.loadTestsFromNames(['test_dependency_current_context','test_dependency_host_entry','test_dependency_migration_transport','test_dependency_operational_launcher'])
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    elapsed=time.monotonic()-started
print(dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),seconds=elapsed,log=str(path)))
sys.exit(0 if result.wasSuccessful() else 1)
'@ | & C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -
```

An earlier log-opening attempt exited **1** because the new directory did not
exist; no tests ran in that attempt. The successful command creates the directory
and exclusively creates its log. A later rerun would need a new log name.
`git diff --check` and the interpreter version command exited **0**.

Qualified source SHA-256:

- `tools/dependency_host_entry.py`: `6ffbb73c72d9b6a7de887bd9607095f10ed348129f2be7c566f92077711bd2b1`
- `tests/test_dependency_current_context.py`: `2ab767d7ff50046a7533ef39589c3e7c91a38ddd66b382db3c8bf6d8041f1531`

The progress recorder ran with:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-prerequisite-disposition/update_progress.py
```

Exit **0**: current dispositions synchronized and prior bytes preserved. The public
ledger's old five-pending map is explicitly historical; original private decision
inputs remain unchanged. No gate is promoted by changing that documentation label.

`C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-prerequisite-disposition/verify_progress.py`
exited **0**: qualified source hashes still match, private historical fields remain
unchanged, no further owner input is required for preparation, and the contact hold
and unpassed device/feature/recovery gates are preserved. A separate standard-library
comparison also confirmed that public changes are limited to the reviewed current
progress fields and leave prior continuations/unrelated packages unchanged; exit **0**.

Changed public files: `tools/dependency_host_entry.py`,
`tests/test_dependency_current_context.py`, `research/ANALYSIS_PREREQUISITES.md`,
this report, `research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`,
`research/NEXT_ANALYSIS_EVIDENCE.md`, `research/PRE_CONTACT_DECISION.md`,
`research/PRE_CAMERA_GAP_AUDIT.md`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`,
and `docs/FEATURE_PROGRESS.md`. Private session/feature notes and new exclusive
logs, receipts and before-images remain ignored. No push or external submission.

## Scope accounting

Public web/reference reads occurred before the owner's instruction to stop legal
inquiry. That work stopped immediately after the instruction. No inquiry was sent,
new agreement accepted, private input uploaded or firmware downloaded.

One reviewer retrieved an already-cited public author comment whose response
included a value table. This exceeded the planned sanitized-provenance-only
subreview. The reviewer reported it; no values were used, copied into files or
published. No constants file, firmware or native binary was opened or executed.
The implementation/test review that followed read authored code only.

Camera commands: **none**. The prepared PnP query was not run. No upstream launcher,
service tool, firmware program, driver change or device write occurred. All
feature, recovery and device-write gates remain unpassed. English/native FTP
remain first and unvalidated; looks remain deferred and the bridge separate.

## Next single work package

**RA-003: qualify the constructed context against retained `verify_context`, then
integrate it into the existing disabled parent/child preparation path**, reconciling current source and bootstrap
bindings while preserving historical inputs. Qualify the complete handoff using
invented data before actual artifact processing. No camera contact or new owner
intake is needed for that engineering work.
