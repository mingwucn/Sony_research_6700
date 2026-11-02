# Session report: 2026-11-02 / transaction recovery GUI and release

Status: COMPLETED for offline implementation, synthetic/mocked qualification, portable packaging and GitHub asset publication. Physical interrupted-session recovery validation: NOT RUN.

## Context

- Repository before work: `eaedd44` on `codex/powerful6700-english-review-20261026`.
- After work: reviewed but uncommitted working-tree changes on the same branch; no Git mutation performed.
- Scope: implement the handoff in `docs/TRANSACTION_RECOVERY_AND_GUI_REDESIGN.md`, close recovery gaps exposed by GUI wiring, disclose real write footprints, package and publish the Windows portable ZIP.
- Host: Windows AMD64; CPython 3.10.20 (`C:\Users\mingwucn\.conda\envs\ai\python.exe`) for tests/publication; project-local `.venv` with PyInstaller 6.22.3, pyusb 1.3.1 and libusb-package 1.0.30.0 for build/self-test.
- Session device risk tier: R0 offline/host only plus explicitly requested GitHub Release upload. No R1/R2/R3/R4 camera operation was performed.
- Camera contacted: NO. Persistent camera writes: NO. Camera commands: `[]`.
- Target scope remains ILCE-6700 CN1 Ver. 2.00; no serials, credentials, firmware dumps or body artifacts were accessed.

## Commands and actions actually performed

Host test/build commands relevant to the final result:

1. `python -X utf8 -m unittest tests/test_recovery_journal.py tests/test_customizer_recovery.py tests/test_customizer_targets.py tests/test_patch_spec.py tests/test_elf_static.py tests/test_ext2_readonly.py tests/test_uxc_readonly.py`
   - Final exit code 0; 106/106 passed in 2.409 seconds. Earlier development runs exposed and corrected a synthetic buffer-length fixture and an immutability fixture; no threshold was relaxed.
2. `python -m venv .venv && .venv/Scripts/python.exe -m pip install pyinstaller pyusb libusb-package`
   - Exit code 0. All third-party build packages were installed only inside the ignored project-local environment.
3. `.venv/Scripts/python.exe -X utf8 run_customizer.py --self-test .data/gui-selftest.json`
   - Final exit code 0. The initial host environment lacked `pyusb`; after isolation, the source self-test also exposed a source-tree worker root error in `a6700win/paths.py`, which was corrected.
4. `.venv/Scripts/python.exe -X utf8 tools/build_dist.py`
   - First build: PyInstaller succeeded, clean-PATH self-test exited 1 because the test did not initialize the vendored `a6700_unlock` path.
   - Final build: exit code 0; extracted portable executable passed all seven clean-PATH checks: GUI import, Tk window, native payloads, WDI, libusb, USB auth modules, state directory and elevated-worker no-op.
5. `python -X utf8 tools/publish_release.py`
   - Exit code 0. Updated release notes and replaced the same-named v1.0.0 asset with the tested ZIP.
6. `git diff --check`
   - Exit code 0. `git status --short` and the working diff were inspected; no staging, commit or push was performed.

No command opened a USB device, authenticated a camera service session, read firmware, wrote firmware, rebooted a body or contacted an FTP server.

## Results

| Test / observation | Expected | Observed | Status | Evidence class |
|---|---|---|---|---|
| Focused customizer suite | All cases pass without hardware | 106/106 passed, exit 0 | PASS | offline-tested |
| Resume requires reconciliation and refuses partial/stale states | No mutation on rejected paths | Mocked coverage passed | PASS | offline-tested |
| Full apply/restore preflight | All spans validated and snapshotted before probe/write | Mocked coverage passed | PASS | offline-tested |
| Snapshot integrity/provenance | SHA-256 verified; prepared snapshots immutable; baseline-patched spans not fabricated | Mocked coverage passed | PASS | offline-tested |
| Mixed-baseline rollback | Only session-touched spans rolled back | Mocked coverage passed | PASS | offline-tested |
| Journal discovery | Unclosed, damaged and unknown metadata fail closed | Synthetic coverage passed | PASS | offline-tested |
| Tk startup | Page construction and startup reconciliation do not crash | Source and packaged Tk checks passed | PASS | offline-tested |
| Portable clean-PATH self-test | Extracted EXE runs without system Python | All seven checks passed | PASS | offline-tested |
| On-device interrupted write/reconciliation/rollback | Separate approved physical test | Not performed | NOT RUN | physical-tested |
| Native FTP long-duration end-to-end transfer | Separate camera/server test | Not performed in this session | NOT RUN | physical-tested |

Portable artifact:

- Path: `dist/Sony_a6700_Customizer_v1.0.0_win64.zip`
- Size: 20,622,587 bytes (19.67 MiB)
- SHA-256: `28ebd066bb8a15d27d16b711123339e7418e977060d649e2e4b50c6f0423a0f1`
- Release: https://github.com/mingwucn/Sony_research_6700/releases/tag/v1.0.0
- Asset: https://github.com/mingwucn/Sony_research_6700/releases/download/v1.0.0/Sony_a6700_Customizer_v1.0.0_win64.zip

Sanitized code/documents changed:

- Recovery/backend: `apps/a6700_customizer/recovery_journal.py`, `app_backend.py`.
- GUI/startup: `apps/a6700_customizer/app_gui.py`, `apps/a6700_customizer/a6700win/paths.py`, `run_customizer.py`.
- Tests: `tests/test_customizer_recovery.py`, `tests/test_recovery_journal.py`, `tests/test_customizer_targets.py`.
- Documentation/release/state: `README.md`, `docs/USER_GUIDE_CN.md`, `tools/publish_release.py`, `docs/BACKLOG.md`, `research/STATE.json`, this report.
- Local privacy: `.gitignore` now excludes `/.data/` runtime journals/backups.

Protected-state comparison: NOT RUN. Physical recovery/inverse result: NOT RUN. Mocked inverse and failure paths only; no recovery guarantee follows.

## Failures, uncertainty and current state

- Last confirmed state: 106 focused tests and the final portable clean-PATH self-test pass; GitHub Release upload succeeded. Working tree contains reviewed uncommitted changes.
- Unknown device operation: none in this session. No camera I/O remains active from this session.
- The implementation uses sequential independent spans, not an atomic multi-span write. Later-span failure can leave earlier verified spans modified until explicit reconciled recovery.
- Physical power loss, USB disconnect on the real body, service-mode survival, unbootable-body recovery and end-to-end FTP transfer reliability remain untested here.
- The release tag points at `main`; this session did not commit or push source changes because separate Git mutation confirmation is required by the operating instructions. The uploaded binary was built from the reviewed working tree described above.

## Decision and next step

Conclusion: the requested GUI, guarded recovery workflow, truthful disclosures, documentation and portable release are implemented and offline-verified. Hardware recovery and long-term FTP success are not claimed.

Next single work package: review, commit and push the current offline source/test/documentation changes, then separately plan an owner-approved exact-body interrupted-session reconciliation drill with explicit R4 commands and recovery limits.

Proposed next command/experiment: Git review/commit/push only; risk R0 and no camera contact. Owner approval needed for Git mutation under this session's operating rules: YES. Any future camera drill requires separate explicit approval.
STATE/backlog updated without promoting unverified claims: YES. Staging: NOT RUN; working diff reviewed for private material: YES.
