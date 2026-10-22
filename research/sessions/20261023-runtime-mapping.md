# RA-003: lossless runtime path/receipt mapping and retained comparison join

2026-10-23. Evidence: **static-inference**, **offline-tested**. Native English and
native Wi-Fi FTP remain primary; camera contact stays on explicit owner hold.
No owner intake or legal inquiry, installed/native activation, protected input,
network, upstream execution or device action.

Started clean at `35003ec40d72bab8bef03350ce1bc72037f096b5`; created topic branch
`codex/ra003-runtime-mapping-20261023`. Previous goal turn: **progress**, committed
nonexecuting bootstrap review preparation. Current turn: **progress**, implemented
domain/full-receipt mapping and joined it to the existing retained comparison.
The full pre-contact goal remains active and incomplete.

[Mapping behavior and remaining gaps](../RUNTIME_PATH_MAPPING.md). The existing
bridge reuses retained package/policy/receipt validators and its original native
projection. Both path domains, complete receipts and dual tokens survive the
comparison. Optional mapping validation follows the original packet binder and
cannot substitute its context. Default comparison output/refusal stays unchanged.

## Exact commands and results

Working directory `D:/LocalWork/Sony_research_6700`; Windows, PowerShell 7.6.5;
interpreter `C:/ProgramData/miniconda3/python.exe`, CPython 3.13.12.

```powershell
git status --short --branch
git log -1 --format=%H
git switch -c codex/ra003-runtime-mapping-20261023
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/snapshot.py
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/pin_bridge.py
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/qualify.py focused-01
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/qualify.py regression-01
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/prepare.py
```

All commands above exit **0**. Snapshot: eleven exclusive note before-images,
16 source pins and four additional bridge/context pins. Preliminary focused
26/26 and regressions 126/126 passed before the optional integration was added.
Preparation read only two saved ordinary JSON descriptors and retained all 351
package receipt pairs / 21 origin descriptors; five full runtime receipts absent.
No saved native policy was emitted. Partial private mapping: 817,248 bytes,
SHA-256 `417975057a8302668377492c120564bdaa536d9c78b27a4bfb1087b015386646`.

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/qualify.py focused-02
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/qualify.py regression-02
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/prepare.py preparation-02
```

`focused-02`: exit **1**, 29 run / 26 passed / **three errors**, zero failures or
skips. All three stop at `mapping_identity_alias`: the old invented bridge fixture
reuses inode IDs across file groups. Failure log SHA-256
`bbc4fe5512e68f79ee7e6717c83617bd8ad5006eb0d80d0ccb8b682cd9266e0d`.
`regression-02`: exit **0**, 126/126, zero failures/errors/skips. `preparation-02`:
exit **0**, same historical partial mapping/hash, original bridge ASTs preserved
except the optional mapping join; 16 other source pins and frozen 16/5/3 unchanged.

The correction changes only the new integration fixture: distinct invented IDs
and rebuilt origin identities, complete proof tokens, policy/binding/fixed hashes,
context and legacy projection. Production predicates and existing fixtures remain
unchanged. Genuine retained binder calls remain exercised. Independent review
accepted the source integration and correction; no acceptance threshold relaxed.

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/qualify.py focused-03
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/qualify.py regression-03
```

Final `focused-03`: exit **0**, **29/29**, zero failures/errors/skips,
**43.8272788 s**; log SHA-256
`a8252e5a018f8a5eebf4143e7393b21b99e55f3f93c81b8df16d9546952ee5f5`.
Final `regression-03`: exit **0**, **126/126**, zero failures/errors/skips,
**41.1222796 s**; log SHA-256
`e785387c2e1534adb4f10096a804bd7eae025d867ba83af0a063fb7535e15ee9`.
Modules: legacy bridge, dependency evidence, candidate context. Source pins stable
through both final runs. Final total **155 distinct cases**; preliminary runs,
failed attempt and prior 166-case bootstrap packet qualification are not added.
Audit guards deny native/installed imports, ctypes, subprocess and socket events.

Final exact-path verification and local commit commands:

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/record.py
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/prose_review.py
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/verify.py
git diff --check
git add -- tools/dependency_legacy_bridge.py tests/test_dependency_runtime_mapping.py research/RUNTIME_PATH_MAPPING.md research/sessions/20261023-runtime-mapping.md research/STATE.json research/PRE_CAMERA_GAP_LEDGER.json docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/PRE_CAMERA_GAP_AUDIT.md research/ANALYSIS_PREREQUISITES.md research/PRE_CONTACT_DECISION.md
git diff --cached --check
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/staged_review.py
git commit -m "feat: preserve runtime path domains and full receipt mappings"
& 'C:/ProgramData/miniconda3/python.exe' -I -S -B -X utf8 private/sessions/20261023-runtime-mapping/complete.py
git status --short --branch
```

Final checks: exit **0**, twelve explicit reviewed paths match working/index/commit
blobs; local commit, clean tree, no push. Commit ID and exact file hashes are in
the ignored completion receipt and Git log. Private helpers, before-images,
qualification logs, failed receipt and historical partial mapping remain ignored.

## Changed files and unresolved prerequisites

Changed code: `tools/dependency_legacy_bridge.py`; new tests:
`tests/test_dependency_runtime_mapping.py`. New reports:
`research/RUNTIME_PATH_MAPPING.md` and this report. Updated public notes:
`research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`, `docs/BACKLOG.md`,
`docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`, `research/PRE_CAMERA_GAP_AUDIT.md`,
`research/ANALYSIS_PREREQUISITES.md`, `research/PRE_CONTACT_DECISION.md`.
Ignored current notes: `private/session-state.json`, `private/feature-progress.json`
and `private/feature-progress.md`, updated from verified before-images.

Still missing: five complete runtime receipts and fresh runtime/origin/root
observations, full native-event behavior, bounded journal/bootstrap stop entry
and current execution binding. Exact-body English/FTP mapping and practical
rollback remain unqualified. No source-manifest migration, actual allow record,
executable bundle, activation or protected processing.

Next single package: **RA-003: implement and qualify a bootstrap-only disposable
child and bounded private event journal using invented imports/events**, exercising
the original bootstrap method through an inert import adapter and parent check.
Stop before package imports, controller and protected processing. Preserve review
packet refusal, native-denying hook and frozen 16/5/3. No installed/native/protected
reads, actual activation or camera contact. English/native FTP remain first.

Camera commands: **none**. Feature, recovery and device-write gates: **unpassed**.
FL2/FL3 deferred; custom looks separately gated later; any bridge **host-assisted**.
