# RA-003: current v6 source and command derivation

2026-10-20, branch `codex/ra003-v6-source-command-spec`, base `d37bd81`.
Previous goal turn: **progress**, recording the finite research/evidence packet.
This turn establishes the exact source projection and six calling-seam gaps;
the overall pre-camera objective remains incomplete.

Deliverable: [non-executing specification](../V6_SOURCE_COMMAND_SPEC.md).
Evidence: **static-inference**, **offline-tested** for source/metadata consistency.
Production/test code unchanged. The next implementation is now bounded to
existing packet/launcher/child preflight seams; no new framework is proposed.

## Exact commands and results

```powershell
git status --short --branch
git switch -c codex/ra003-v6-source-command-spec
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-v6-source-command-spec -ErrorAction Stop | Out-Null
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-v6-source-command-spec/derive.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-v6-source-command-spec/record.py
git diff --check
git diff --stat
```

Derivation exit **0**: 51 current source rows checked against the pinned original
manifest; exactly three outer authored-source deltas; one separately proposed
gate substitution; all 46 explicit prepared-role projections equal their
original source bytes. Counts: 49 child / 2 host / 51 comparison / 53 preflight /
54 transport / 46 prepared. Six AST/source witnesses confirm missing transport,
legacy gate dispatch and the retained context refusal. Fifteen earlier
qualification source/test pins still match. Bootstrap composition is deterministic
and matches the prior observation-bootstrap pin. Process and file-open calls
were blocked during composition; the produced text was never executed.

Only ordinary metadata and authored Python were read/imported; retained authored
bootstrap files were hashed as inert data. No installed package/native payload,
firmware, operational constants, dependency cache or camera input was opened.
An initial source search included a nonexistent `dependency_observation_child.py`
path and returned an error; file inventory confirmed the child implementation is
`dependency_operational_child.py`, which was then inspected. No execution attempt
or changed acceptance predicate resulted.

Recorder/metadata validation exit **0**: captured source pins stable, specification
remains non-executing, all five original activity decisions pending. Original
requirements, named cases, gates, risks, source lock and historical source
manifests unchanged. Three direct CLI refusal checks return **2**, empty output;
these execute only the authored early refusal, not bootstrap or child execution.
Private specification, pins, receipts and before-images remain outside Git.

Interpreter: **CPython 3.13.12**, `C:/ProgramData/miniconda3/python.exe`, isolated
flags above, Windows AMD64. No behavioral test suite rerun for this source/spec
audit; previous 165-case qualification remains historical. Static witnesses do
not qualify unimplemented transport changes or actual runtime behavior.

Changed public files: this report, `research/V6_SOURCE_COMMAND_SPEC.md`,
`research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`,
`research/PRE_CAMERA_GAP_AUDIT.md`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`,
`docs/FEATURE_PROGRESS.md`. Internal session/function notes updated with originals
preserved. No legal conclusion, act approval or complete actual command created.

Camera commands: **none**. No protected input processing, dependency activation,
upstream execution, download/upload or driver/firmware change. No English/FTP
support, recovery or device-write gate passed.

Next single package: **RA-003: implement and qualify the closed v2 migration
handoff through existing projection/packet and parent/child preflight seams**,
including saved arguments. Preserve v1 behavior and v6 context refusal; require
v6 to stop before bootstrap materialization, protected preparation, result writes
or process launch. Invented tests only; no actual approvals or protected inputs.

Publication after reviewing the eight named paths: explicit `git add --`,
`git diff --cached --check`, `git diff --cached --stat`, `git diff --cached`,
`git commit -m "Derive v6 source projection and missing command handoff seams"`,
`git status --short --branch`. Diff checks exit **0**.
