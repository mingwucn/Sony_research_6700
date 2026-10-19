# RA-003: fresh source cache and outer-binding migration

2026-10-19. Base `ec37accccf3042e37b30a8cd7f70dd57a0ec54da`. Topic branch `codex/ra003-gdt-source-cache`; starting tracked tree clean. CPython **3.13.12** at `C:/ProgramData/miniconda3/python.exe`, PowerShell 7.6.5, Windows 11 AMD64. Previous goal turn: **progress**. Current turn: **progress**, no-progress count zero; broad pre-camera goal remains active.

Fresh read-only snapshots collected **47 Python sources (813,391 bytes)**: 26 authored roles, three bootstrap sources, three integration sources, eleven dependency Python origins and four trusted Python origins. All 47 descriptor, close, EOF and whole-file hash receipts reconciled. The unchanged pure binding planner accepted the 23 eager/three protected source order. **20/20 synthetic snapshot tests passed**, zero skips, exit **0**. Six source-derived outer-gate migration requirements are now explicit. This is source preparation; the actual outer gate remains incomplete and independent operational review has not occurred. No firmware/constants/raw-prefix/native payload read, installed dependency execution, GDT replay or camera contact. English/native FTP and recovery remain unverified.

## Exact commands and results

Repository-root PowerShell:

```powershell
git status --short --branch
git switch -c codex/ra003-gdt-source-cache
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-source-cache/test_source_snapshot.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-source-cache/collect_sources.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-source-cache/audit_cache_and_migration.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-source-cache/publish.py
git -c core.safecrlf=false diff --check
git diff --stat
git -c core.safecrlf=false add -- README.md docs/ARTIFACT_INTAKE.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/STATE.json research/GDT_OUTER_BINDING_PREPARATION.md research/sessions/20261019-RA-003-gdt-source-cache.md
git -c core.safecrlf=false diff --cached --check
git diff --cached --name-only
git diff --cached
git commit -m "docs: record fresh GDT source cache and outer gate migration"
git status --short --branch
```

The synthetic command was launched once by a standard-library `subprocess.run` supervisor with a **30-second** timeout and captured stdout/stderr. **20/20 passed**, zero skips, exit **0**, **0.089s** suite / **0.364342600s** wrapper. Raw logs and source hashes are private. The source-reader tests exercise real invented files, bounded partial reads, non-execution sentinel bytes, wrong hash/size, source growth/EOF, hard links, directory/reparse rejection, descriptor changes, cross-API creation-time differences and no repeated close after uncertain completion. They do not qualify OS races or the future operational gate. No historical suite was rerun or added to 20.

Collection ran once: **exit 0**, **0.486994100s**, 47 source descriptors/47 close attempts/47 EOF probes, 813,391 bytes, all expected whole-file hashes matched. Six explicitly pinned ordinary JSON inputs supplied paths/metadata; those reads have bounded exact-byte/hash checks, not the Python-source descriptor receipt guarantee. No embedded firmware/constants/native path was followed. The pure source-binding planner accepted 23 eager and three protected roles; its two historical blockers remain. The separate same-agent audit exited **0**, reconciled all cache bytes/receipts and six migration requirements, checked 184 historical immutable-group entries and all 135 starting paths. Independent operational review is still required.

Preservation and exploratory diagnostics are retained privately. Initial baseline construction incorrectly resolved integration-relative qualification keys at repository root and stopped with FileNotFoundError/exit **1**, before baseline publication or analysis. The four already written private snapshots were verified identical and reused without overwrite; the corrected baseline exited **0**. Exploratory JSON lookup of a nonexistent collector-result filename was reported absent; the actual descriptor result is audit-result.json. Early source searches printed oversized embedded schema constants; later AST/range inspections omitted those long constants. None of these diagnostics caused source retries, firmware reads or any relaxed predicate.

Git/publication commands and exact exit codes are retained in the private completion receipt. Only explicitly reviewed public files are staged; no push or history rewrite. Prior source/qualification/activation/runtime records are preserved. The initial shell helpers used for baseline/tests and their outputs remain in this task's tool history and private receipts; the qualified test command above is their exact child argv.

## Changed files and remaining work

Public files (eight): README.md, docs/ARTIFACT_INTAKE.md, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md, research/STATE.json, research/GDT_OUTER_BINDING_PREPARATION.md, and this report. Private notes (four): private/session-state.json, private/feature-progress.json, private/feature-progress.md, private/owner-intake.md. Prior versions are preserved. New private helpers, tests, cached third-party source, receipts and migration specification remain ignored/untracked.

See [six source-derived migration requirements](../GDT_OUTER_BINDING_PREPARATION.md). The actual outer gate, distinct activity decision/seal and fresh in-act native proof remain absent. Exact-body/build correspondence, English restriction/resources, FTP backend/ABI/media/network/lifecycle, and verified backup/rollback/recovery remain unresolved. No feature, filesystem-content validity or device-write gate passes. Existing China research rationale and contract/component/constants uncertainties remain unchanged; no new permission-only barrier is invented.

**RA-003: implement and synthetically qualify the versioned outer host/child activation gate against the six source-derived migration requirements and 47-source cache; independent operational review and GDT replay remain separate**.

Camera commands: **none**. Firmware/constants/raw-prefix/native payload reads, GDT replay, installed dependency execution, device access/write, upstream launchers, driver/service changes, new downloads/installs/agreements, private uploads and network actions: **none**.
