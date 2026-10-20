# RA-003: closed v2 migration transport qualification

2026-10-20. Branch `codex/ra003-v2-handoff-qualified`, based on `26793af`. Evidence: **static-inference**, **offline-tested**. English and native Wi-Fi FTP remain first. Camera commands: **none**.

## Result and limits

The existing observation projection, packet decoder, parent/child gate dispatch and saved-preflight arguments now carry one closed, hash-bound historical migration record. V1 behavior remains unchanged. Current candidate/request operation equality remains enforced independently from historical context. V2 validates consistency and then refuses `operational_process_v6_execution_pending` before output writes, bootstrap materialization, helpers, protected preparation or process launch. The independent host context refusal remains. Constructor handoff is wired but unreachable through this v2 execution refusal.

**214/214 tests passed**, zero failures/errors/skips, exit **0**, **110.414s**. All **21** selected source/test SHA-256 pins stayed stable. Composition: prior 165 cases, 18 operational-launcher cases, 19 observation-launcher cases and 12 new migration-transport cases. Tests use invented records/buffers and inert synthetic children. Parent/child boundary tests substitute capture/owner/packet checks while exercising real gate and metadata code; they do not qualify actual source capture, installed dependencies or protected execution. Saved-preflight verification checks consistency rather than authenticating a supplied validated result.

Independent authorized authored-source review: **12/12 passed**, exit **0**, **12.760s**, no blocking findings. Its five reviewed file pins exactly match this qualification. No new reviewer was spawned for this continuation.

An earlier focused run had **29 passes and one failure**, exit **1**, **16.334s**: its test patched a live captured Preparation class, correctly triggering the owned-source mutation guard. The test fixture was corrected by removing that mutation; production guards were unchanged. The subsequent 31-case migration/observation-launcher run completed successfully, exit **0**, **34.822s**. Its existing process handle `75717` was polled to terminal completion rather than restarted. Formal qualification used handle `19610`, polled to terminal completion. The earlier focused outputs remain in the conversation tool record; the formal full log and receipts are preserved privately.

Ordinary-only source comparison confirms **51** original source roles, exactly **five** current source deltas and **zero** byte deltas in the **46** prepared roles. Observation launcher is an additional changed tool outside the original 51-source roster. Frozen original manifests, gate/proof/cache and historical records were not migrated. Gate replacement remains proposed. Four selected ordinary records match the preselected baseline; all five dispositions remain pending and all three dependency null fields remain. This package does not rerun an actual pending operational chain or claim a new actual runtime refusal; its actual-data check is an ordinary metadata/source comparison.

No actual current candidate/review/decision/seal, executable bundle, new permission, approved act, dependency binding or operational bootstrap was created. No firmware, operational constants, native payload or installed dependency was accessed or activated. No network acquisition, upstream launcher, private upload, driver/firmware change or camera action. Native English/FTP mapping, exact-body correspondence, recovery and device-write gates remain unresolved.

## Exact commands

PowerShell; **CPython 3.13.12**, `C:/ProgramData/miniconda3/python.exe`, isolated standard-library flags below. New private output directories/files were created exclusively; previous collectors and receipts were preserved.

```powershell
git status --short --branch
git switch -c codex/ra003-v2-handoff-qualified
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-v2-migration-handoff/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-v2-migration-handoff/check_metadata.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-v2-migration-handoff/record.py
git diff --check
git diff --stat
```

Qualification exit **0**, metadata comparison exit **0**, recorder exit **0**. Qualifier loads these exact unittest modules: `test_dependency_historical_gate`, `test_dependency_historical_outer`, `test_dependency_observation_outer`, `test_dependency_observation_contract`, `test_dependency_pending_review`, `test_dependency_legacy_comparison`, `test_dependency_operational_preparation`, `test_dependency_preparation_migration`, `test_dependency_host_entry`, `test_dependency_migration_transport`, `test_dependency_operational_launcher`, `test_dependency_observation_launcher`. This focused selection is not a complete repository test run.

Qualifier and recorder also invoked the following direct CLIs, each with **exit 2**, empty stdout/stderr, confirming public activation remains disabled:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_operational_metadata.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_operational_preparation.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_host_entry.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_operational_child.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_operational_launcher.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_observation_launcher.py
```

Private session contains qualification script, raw test log, test/pin receipts, metadata comparison, independent review receipt, CLI refusals, recorder validation and before-images. Internal session/function notes are synchronized. Previous goal turn **progress**: `26793af` records a fresh pinned external-reference comparison. This turn **progress**: concrete existing-path implementation plus qualified refusal coverage; the full goal remains incomplete.

Changed public files: three tools (`dependency_operational_child`, `dependency_operational_launcher`, `dependency_observation_launcher`), new migration-transport tests, adjusted operational-launcher fixture, [technical note](../V2_MIGRATION_HANDOFF.md), this report, STATE, gap ledger/audit, BACKLOG, CODEX_HANDOFF and FEATURE_PROGRESS. No source lock change, foreign implementation or target profile.

After reviewing those paths only:

```powershell
git add -- tools/dependency_operational_child.py tools/dependency_operational_launcher.py tools/dependency_observation_launcher.py tests/test_dependency_migration_transport.py tests/test_dependency_operational_launcher.py research/V2_MIGRATION_HANDOFF.md research/sessions/20261020-RA-003-v2-migration-handoff.md research/STATE.json research/PRE_CAMERA_GAP_LEDGER.json research/PRE_CAMERA_GAP_AUDIT.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "feat: carry closed historical migration through consistency transport"
git status --short --branch
```

## Next single work package

**RA-003: qualify a distinct current-operation execution-context constructor using the original retained baseline and current request on invented inputs.** Establish exact source, document, ordinary-input and command bindings independently of the v6 consistency receipt. Keep the v2 launcher refusal and all five pending activity decisions until that separate work is reviewed; no actual allow records, dependency activation, protected reads or camera contact.
