# RA-003: prospective dependency-only producer qualification

2026-10-19. Branch: `codex/ra003-producer-qualification`.
Evidence: **static-inference**, **offline-tested**. Camera commands: **none**.

Previous goal turn: **progress** — verified the public reference revision and saved
its current English/FTP/recovery assessment. Current turn: **progress** — completed
source/invented qualification of the pending prospective producer. The objective
of all pre-camera preparation remains active and incomplete.

The new [design](../PROSPECTIVE_DEPENDENCY_PRODUCER.md) replaces missing prospective
instrumentation with real import-hook, native-wrapper, publication and cleanup
operations exercised on invented modules/receipts. It does not rewrite historical
events or clear any of the seventeen retrospective blockers. Configuration/cache
hashes now explicitly mean original supplied UTF-8 bytes. The CLI refuses real
activation; its callable invented seam and caller review/source identities are
not execution authority.

Before qualification, source inspection corrected reentrant pending-load ownership,
byte-type vector comparisons, concrete Python module paths, aggregate identity-buffer
bounds and descriptor kind checks. Two independent owner-authorized source reviewers
then found optional-backend traversal could reach a later finder and cleanup could
escape before output handles closed. Both were repaired and re-reviewed at the
final hashes below, with no remaining source/synthetic blocker reported. Reviewer
receipts are parent-saved transcriptions of source-only findings, not runtime evidence.

All dependency sources, file receipts and expected package records in the tests
are invented. The fake cipher is a public-vector lookup table. No installed
cryptography or actual DLL is loaded. Two disposable children use real Python
audit hooks and manual audit events to test delivery, sticky caught refusals and
inert hooks after cleanup; they do not call the native loader or execute a shell.
The source-execution intent/completion trace is supplemental; the shared contract
validates completed-import events, not durable bracket semantics.

## Exact commands and results

Host: Windows AMD64. Interpreter `C:/ProgramData/miniconda3/python.exe`, CPython
3.13.12, isolated/no-site/no-bytecode UTF-8 invocation.

- `git status --short --branch`: started on `codex/a6700-reference-owner-check`,
  HEAD `7a871aa`, with the inherited untracked `tools/dependency_producer.py`.
- `git switch -c codex/ra003-producer-qualification`: exit **0**.
- Initial iterative commands:

```powershell
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests',pattern='test_dependency_producer.py'));raise SystemExit(not r.wasSuccessful())"
```

Initial **35/35** and expanded **42/42** passed, zero skips, exit **0**; suite
6.129s and 11.521s. After review repairs, the same expression with `verbosity=1`
passed **48/48**, zero skips, exit **0**, 11.443s. These preliminary console runs
were followed by the final source-pinned/logged qualification below. No failed
actual operation was retried; these runs used fresh synthetic temporary files.

```powershell
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-prospective-producer/qualify.py focused
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-prospective-producer/qualify.py full
```

The authored standard-library harness explicitly adds the repository root,
uses unittest discovery, reserves exclusive started/log/result files and checks
source hashes before/after. Focused: **48/48 passed**, zero skips, exit **0**,
**12.818s** suite / **13.056839800032321s** wrapper, five stable authored pins.
Full host: **459 cases, 456 passed / three platform skips**, no failures/errors,
exit **0**, **76.462s** suite / **76.8864651999902s** wrapper, 36 stable authored
source/test pins. Composition: 411 retained cases plus 48 new cases. Three skips
remain POSIX fork inheritance and two real-symlink cases unavailable on this host.
The harness is an ignored local reproducibility artifact, not an upstream launcher.

```powershell
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,runpy;sys.path.insert(0,'.');runpy.run_module('tools.dependency_producer',run_name='__main__')"
```

CLI exit **2**, expected `needs_review` / `real_activation_pending`, no camera
commands and no dependency/input access through main. The qualification harness
and CLI receipt, exact argv/interpreter, source pins and logs remain private.

| Reviewed authored file | SHA-256 |
|---|---|
| tools/dependency_producer.py | b68e0da3a28089ca97b64d6e2c37b62d77989930e684a973d2eb177732ede1fa |
| tests/test_dependency_producer.py | 1bc1058a495043b6f3c58a721e4c73a453bfc1a4817540c3410639c5d2075f87 |
| tools/dependency_evidence.py, unchanged | 63eb311df4c818458edd28dd9853c3c20234460f3cf145eb16886ef0abbb12f3 |

Focused log SHA-256: `a35a4e5a1af65d57106e07b0b80abbe03208a2ccd05775c98a905efd6308a914`.
Full log SHA-256: `ade05e31d5f2f11416d0e0e601bda9e914b5a5d67f8411dc553499605b1c6099`.

## Changes and unresolved prerequisites

Public changes: `tools/dependency_producer.py`, `tests/test_dependency_producer.py`,
`research/PROSPECTIVE_DEPENDENCY_PRODUCER.md`, this report, `research/STATE.json`,
`docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `docs/CODEX_HANDOFF.md`.
Internal session/feature notes are updated after exclusive backups. Only these
reviewed public paths are staged; no private input or third-party implementation.
JSON parsing, unchanged existing STATE fields, source/review hash correlation and
`git diff --check` are checked before commit.

Remaining host prerequisites are exact executing-source/runtime/bootstrap binding,
independently fixed fresh package/root expectations, acknowledged audit-hook
installation before loader use, a frozen disposable-child outer entry and bounded
once-only outcome reconciliation. File fsync and current-state readback do not
prove atomic publication, directory-entry crash durability, mapped native bytes
or transitive DLL identity. Historical saved-record consistency is unchanged.

English resources, native Wi-Fi FTP implementation, exact body/build correspondence,
service access, full rollback/recovery and all feature/device-write gates remain
unproved. No new network request, private upload, firmware/constants/cache-body
read, installed-dependency execution, upstream tool execution, driver change or
camera contact occurred. No gate is passed by this source/synthetic package.

Next single work package: **RA-003: design and synthetically qualify the frozen disposable-child outer entry, including exact executing-source/runtime bindings and positive audit-hook installation acknowledgement before any loader use; obtain independent source review before an actual dependency observation.**
