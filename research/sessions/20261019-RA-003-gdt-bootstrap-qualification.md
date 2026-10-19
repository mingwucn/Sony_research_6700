# RA-003: bootstrap refusal-order fix and invented-file qualification

2026-10-19. Topic branch `codex/ra003-gdt-bootstrap-qualification`, base `0d180540e8db6df7908ed8e89d6e556fb0b5b995`. Starting tracked tree clean. CPython **3.13.12**, `C:/ProgramData/miniconda3/python.exe`, Windows 11 AMD64, PowerShell 7.6.5. Previous goal turn **progress**; this turn **progress**, no-progress count zero. Broad pre-camera goal remains active.

The ordinary bootstrap now preflights every input path and pinned archival hash **before opening any input document**. The first invented-file qualification exposed two refusal-order failures; both were fixed without changing tests. Final **124/124 passed**, zero skips, exit **0** (105 retained + 19 new). The complete bootstrap ran only with invented temporary documents and a test-only in-memory authority substitution. No actual saved-input activation or protected continuation ran. Independent review, English/native FTP and rollback remain pending.

## Exact commands and results

Repository-root PowerShell:

```powershell
git status --short --branch
git switch -c codex/ra003-gdt-bootstrap-qualification
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-bootstrap-qualification/qualify_001.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-bootstrap-qualification/qualify_002.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-bootstrap-qualification/publish.py
git -c core.safecrlf=false diff --check
git diff --stat
git -c core.safecrlf=false add -- README.md docs/ARTIFACT_INTAKE.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/STATE.json research/GDT_BOOTSTRAP_QUALIFICATION.md research/sessions/20261019-RA-003-gdt-bootstrap-qualification.md
git -c core.safecrlf=false diff --cached --check
git diff --cached --name-only
git diff --cached
git commit -m "docs: record invented bootstrap qualification and preflight fix"
git status --short --branch
```

First qualifier: **124 tests, 122 passes, two failures, zero skips**, exit **1**, **3.010s** suite / **3.335744500s** wrapper. The two refusal-order failures were retained with all seven frozen source/helper/scope files. Final qualifier: **124/124**, zero skips, exit **0**, **2.825s** suite / **3.157964000s** wrapper. Same tests, corrected entry only; no acceptance change. Exact child argv is `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8` and the absolute path of this session's test_outer_v2.py.

Both wrappers use a 60-second deadline, monitored 4 MiB combined-log threshold, one terminate and five-second wait then one kill/five-second wait if necessary. No threshold or termination event occurred. Monitoring is not a strict output-storage cap. Source hashes stayed stable within each run. The 124 include 105 retained cases plus nineteen new bootstrap/reader/loader cases.

Inline standard-library preservation/review check: exit **0**, all **245** historical entries and **141** starting paths matched before publication; seven final pins and seven preserved failed-run pins matched. It verified the test file unchanged across the fix, the 105-case test prefix unchanged, 124 unique final pass identities and the fixed 18-reference production policy unchanged. Raw logs are separately hashed in the private review. Baseline/copy, new test construction, fix and review commands are retained in task history and private records. The publication helper also writes source-bound normalized qualification result/review records with execution/ready false; it creates no actual activation bundle.

## Changed files, limitations and next package

Eight public files: README.md, docs/ARTIFACT_INTAKE.md, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md, research/STATE.json, research/GDT_BOOTSTRAP_QUALIFICATION.md and this report. Four private progress/intake files updated with snapshots preserved. New private sources, tests, logs and records remain ignored. Only reviewed public paths are staged; no push or history rewrite.

The first 124-case run passed 122 and failed two. A resealed noncanonical final input path triggered rejection only after 22 ordinary input read attempts; a resealed incorrect archival hash triggered rejection after eight. Both were invented-data cases, with no real private inputs. The refusal-order predicate was set before the run. The correction splits preflight and reading into separate loops: all 22 roles must use their exact session-local inputs/role.json path (the snapshot log uses .log), and all seventeen archival document roles must match entry-owned reference hashes before the first ordinary input read. The eighteenth dependency-profile pin remains enforced by the pure validator. The test file is byte-identical across the fix; all seven failed-run source/helper/scope files are preserved.

Nineteen new cases cover initial reader acceptance/refusal for ordinary, empty, oversized, hardlinked, directory, relative and parent-traversal paths; duplicate/nonfinite bootstrap JSON; cached-module execution of supplied invented bytes, occupied-alias preservation and cleanup after compile/execute failure; complete invented-file bootstrap, bad external anchor, changed helper, absent input, and both all-input-preflight refusal cases. The 105 retained cases are an unchanged source prefix. Production initial_read, cached_module, bootstrap, ordinary reader and pure gate are exercised with authored helper source and invented temporary documents. A test-only in-memory substitution of reference hashes allows the invented authority chain; the fixed production 18-reference policy is unchanged. No main, prepare_modules, actual factory or actual saved-input bootstrap is called. Toy files are isolated in test temporary directories and removed by test cleanup.

This closes the specific untested invented-file bootstrap gap, not the actual protected host/child continuation. The old 811, integration 51, snapshot 20, 81 and 105 results retain their historical scopes and are not added to 124. All 245 inherited preservation entries and 141 starting paths matched before publication. Seven final qualification pins stayed stable; raw logs, negative source snapshots, unique pass IDs and source-bound normalized qualification records are private. Review remains same-agent. No actual candidate, decision, activation review or execution seal was assembled.

Independent operational review remains pending; a local subagent review request is unanswered, and the session requires explicit authorization before spawning reviewers. No additional request or permission-only firmware barrier was introduced. Actual bootstrap/native/protected integration, exact-body/build correspondence, English resources/restriction, native FTP backend/ABI/media/network/lifecycle and verified backup/rollback/recovery remain unresolved. OS races, mapped native bytes and transitive closure are unproved. English/native FTP stay first; FL2/FL3 deferred and custom looks separately gated. Existing research/contract/component/constants uncertainties remain unchanged. No feature, filesystem-validity, recovery or device-write gate passes.

Next single package: **RA-003: independently review the frozen corrected v2 bootstrap, source bindings and 124-case qualification, resolve findings, and specify the exact later metadata act; no actual GDT replay before review passes**.

Camera commands: **none**. Actual saved-input activation, firmware/constants/raw-prefix/native payload reads, installed dependency execution, actual GDT replay, device access/write, upstream launchers, driver/service changes, network/download/install/agreement and private uploads: **none**.
