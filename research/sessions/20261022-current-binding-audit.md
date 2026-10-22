# RA-003: finite current-binding audit and external-origin repair

2026-10-22. Branch `codex/ra003-current-binding-audit-20261022`, baseline
`032b3681d9fc46af22b84351783d2bb61d9aea64`. Evidence: **static-inference**,
**offline-tested**; saved metadata is historical evidence, not fresh runtime
observation. Previous goal turn: **progress**, joined synthetic preparation and
control handoff. This turn: **progress**, finite source audit and demonstrated
constructor repair. Overall goal remains active/incomplete.

Native English and native camera-to-server Wi-Fi FTP stay first. Camera
commands: **none**. No feature, recovery, installed runtime or device-write gate
passed. No new owner facts or legal questions are required.

## Concrete defect and repair

`make_current_context` previously added all 47 historical source-cache origins
to the repository-relative ordinary-file map. The gate permits exact cached
dependency/trusted Python origins outside that repository. The saved pinned
cache contains **43 repository-local rows and four external trusted rows**:
`ctypes`, `ctypes._endian`, `ctypes.util`, `platform`. Thus the constructor
would reject the recorded external layout before returning a current context.
The earlier all-local temporary fixtures concealed this mismatch.

The repair in `tools/dependency_host_entry.py` omits only external
`dependency:`/`trusted:` cache origins from that ordinary-file map. It still
checks absolute paths, parent traversal, valid digests and allowed external role
prefixes; complete role identity is the preceding gate's responsibility.
All current captured sources, retained analysis sources, current request,
packet and implementation bindings remain repository-contained. Historical
cache/config input documents remain hash-bound; no arbitrary root is added
to the ordinary reader and no external file is opened by the constructor.

Three regressions in `tests/test_dependency_current_context.py` cover external
metadata without reads/mutation, malformed external origins/digests and refusal
to omit an external retained analysis role. These are constructor-boundary
fixtures: moving invented row paths does not assert a newly validated gate or
observed external provenance. Independent source review approved the narrow fix.

The existing closed dependency binders (`dependency_execution.bind_runtime_packet`,
`dependency_producer.bind_inputs`) validate metadata. The package collector
(`dependency_package_preflight._collect`) and producer observation own fresh
external dependency/trusted reads. Those reads and the final actual runtime path
did **not** run here. The old
`make_context` and actual v6/public refusals are unchanged.

## Finite audit findings and readiness

| Binding | Evidence and disposition |
|---|---|
| Source closure | **49 child + 2 host = 51 comparison roles**; adding contract/outer validators gives **53**, and observation launcher gives **54**. These are distinct rosters. **55 authored files** were hashed and AST-parsed as data: original 51 plus proposed gate and three observation modules. |
| Current versus selected source bytes | Five roles differ from the frozen manifest: `host.launcher`, `host_entry`, `operational_metadata`, `operational_preparation`, `process_child`. Their current whole-file identities are retained privately. This is a fresh comparison, not acceptance of an old delta count. |
| Prepared projection | Existing explicit map projects **46 prepared roles**, including deliberate adapter entry aliases; **zero prepared byte deltas**. Logical adapter paths describe semantic roles; outer captures carry physical source origins. Stable prepared bytes do not qualify changed outer execution. |
| Selected gate | The frozen selected old gate declares no `validate_bundle_v6`; the proposed current historical gate does. Replacement is still a proposal. No actual source manifest or executable bundle was migrated or created. |
| Cache/config origins | All 47 cache metadata rows reconcile to the pinned layout; the 11 dependency and four trusted Python rows match config metadata. Only path/size/hash fields were examined; embedded base64 was not decoded. External file paths were not followed. |
| Historical/current separation | All **16** selected ordinary/proposal/request records match their original pins. Five historical pending dispositions and three dependency null fields remain unchanged; these are preserved comparison evidence, not repeated owner intake or a new operational act. No current candidate/review/decision/seal was assembled. |
| Command domains | Core request whole-byte hash, canonical transport hash/environment token, pending request/packet hashes and current source receipts remain separate. Both deterministic bootstrap identities match the prior recorded text identities below. Text identity alone is not a current startup qualification. |
| Context and control | Real checker and reservations are covered by the preceding joined tests. The repaired current constructor remains a separate pure seam that requires prior full gate, capture, retained-binding and exact-bootstrap checks. It does not authenticate supplied receipts or interpreter/stdlib. |
| Actual parent/child preparation | Both intentionally refuse v6 before the ordinary execution chain. After that refusal, both still call the old constructor, which independently refuses v6. Dropping only the first refusal cannot produce a working current-context path. |
| Pending comparison grammar | Adapter/pending metadata deliberately requires five pending/false decisions. Do not relabel those records as the current operational act or treat them as owner questions. Current source/gate/record integration remains engineering work. |
| Isolated composition | Existing transport reaches an inert child; joined control/helper tests use in-process alias removal, an in-memory ordinary registry, regenerated invented policy and inert dispatch/collection. A fresh isolated join with current context remains unqualified. |
| Final runtime and features | Existing real dispatch invokes the actual dependency controller. It was not used. No new native loading, GDT observation, resource/locale mapping, resident FTP trace, exact-body correspondence or recovery evidence follows. |

**Readiness decision: actual runtime use is not ready.** The finite audit is
complete and the demonstrated projection defect is repaired and qualified.
Continue offline current-context/isolated preparation integration. No additional
generic context or approval framework is indicated by this audit.

Bootstrap SHA-256 values (composed as text, not run by the metadata audit):

- Pending: `9fc839f17e6c2ff316b88421af3d0d0719838d83a6113b65fdfcdc2743c99c86`.
- Observation: `63c051081d49cd871a4b1d8c55b8a569ff2c62e91436f13fdb1e510d438d489f`.

## Commands and results

Host: Windows, PowerShell 7.6.5, CPython **3.13.12** at
`C:/ProgramData/miniconda3/python.exe`. Git was clean at the baseline above.

```powershell
git status --short --branch
git switch -c codex/ra003-current-binding-audit-20261022
New-Item -ItemType Directory -Path private/sessions/20261022-current-binding-audit -ErrorAction Stop | Out-Null
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-current-binding-audit/audit.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-current-binding-audit/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-current-binding-audit/write_report.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-current-binding-audit/record.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-current-binding-audit/verify.py
git diff --check
```

Audit exit **0**: 51 source roles, 46 prepared roles, five current source deltas,
zero prepared byte deltas, 16 pinned selected records and four external trusted
cache rows. **75** audited metadata/source files remained byte-identical through
qualification. The 31 exact named private authored source files were read as
code data and AST-parsed, not executed; public pure definitions were imported
only to derive existing roster/projection/bootstrap contracts. Private locators
were read narrowly as text. Saved metadata was not passed to an actual gate,
controller, observer or dependency activation function.

Final qualification: **195 cases: 194 passed, 1 skipped,
zero failures/errors**, exit **0**, **121.384s** unittest /
**121.837s** runner. **36** public source/test
pins and all 75 audit pins stayed stable. The sole skip is Windows symlink
privilege error **1314**; hard-link refusal passed. No elevation or system
change. The earlier focused **28** cases (**27 passed, one same skip**;
**16.476s**, exit **0**) overlap this suite and are not added to its total.
No implementation/test failure or acceptance-threshold change occurred.

The runner explicitly loads these modules under `-I -S -B -X utf8`, adding
only repository/tests import paths; it performs no broad discovery:

```text
test_dependency_joined_handoff
test_dependency_current_context
test_dependency_retained_context
test_dependency_preparation_context
test_dependency_host_entry
test_dependency_migration_transport
test_dependency_operational_launcher
test_dependency_preparation_migration
test_dependency_operational_preparation
test_dependency_operational_entry
test_dependency_observation_contract
test_dependency_observation_launcher
```

This focused suite is not current whole-repository CI or a pristine-host result.
Final raw log: `private/sessions/20261022-current-binding-audit/qualification-01.log`,
SHA-256 `62763ecfb55e7ab60b87579dc108cd1ac2de16c690d79747e0c1ea184386b930`. The private session also
retains the exact source deltas/projection, metadata and source pins, gate AST
capabilities, focused log, scripts, note before-images, verification and Git
completion receipts. Progress recording, final invariant verification and
working/staged diff checks exit **0**.

Changed-source working-file SHA-256:

- `tools/dependency_host_entry.py`: `78be04ce3bc3532a44162feb801b5e95525431f3986256ddd26fe39525d774ae`.
- `tests/test_dependency_current_context.py`: `e8869e191895b13eaaddeca8fd0cde738059ea72c392b4a8bd9b631441f0c86f`.

Public/private progress notes are synchronized and keep the goal active. No
firmware, constants, raw prefixes, installed source files or native payloads
were opened; no external origins were opened, dependency activated, download,
upload, upstream launcher/service tool, driver/firmware change or camera contact
occurred. Source locks, historical cache/config and selected records remain
unchanged. Legal research/questions remain stopped. English/FTP remain
unvalidated; FL2/FL3 deferred; later calibrated looks and host-assisted bridge
stay separate.

## Reviewed files and next package

Public changes: the two source/test files above; this report;
`research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`,
`research/PRE_CAMERA_GAP_AUDIT.md`, `research/ANALYSIS_PREREQUISITES.md`,
`research/PRE_CONTACT_DECISION.md`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`,
`docs/FEATURE_PROGRESS.md`. Ignored changes: session scripts/logs/receipts and
`private/session-state.json`, `private/feature-progress.json`,
`private/feature-progress.md`, with prior note bytes preserved.

```powershell
git add -- tools/dependency_host_entry.py tests/test_dependency_current_context.py research/sessions/20261022-current-binding-audit.md research/STATE.json research/PRE_CAMERA_GAP_LEDGER.json research/PRE_CAMERA_GAP_AUDIT.md research/ANALYSIS_PREREQUISITES.md research/PRE_CONTACT_DECISION.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-current-binding-audit/verify.py final-state
git commit -m "fix: preserve external dependency origins in current context"
git status --short --branch
```

Stage only reviewed named files; local commit, no push or external submission.
The commit identity and clean-tree result are retained in the private completion
receipt and session response.

**Next single package:** RA-003: integrate and qualify the current-command context
at the existing host/child preparation seams using invented inputs in a fresh
isolated process. Reuse the exact bootstrap, source owners and genuine retained
control/helpers; keep final dispatch inert and actual v6/public execution refused.
Close the combined startup/handoff gap without new generic approval/context
infrastructure, protected reads, dependency activation or camera contact.
English/native FTP stay first.
