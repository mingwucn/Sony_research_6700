# RA-003: bound-buffer child preflight and audit acknowledgement

2026-10-19. Topic branch: `codex/ra003-child-entry-qualification`.
Evidence: **static-inference**, **offline-tested**. Camera commands: **none**.

Previous goal turn: **progress**, committed prospective-producer qualification
`797987b`. Current turn: **progress**, completed the authored-source bootstrap
portion of the disposable-child package. Full dependency-producer invocation
and installed-package readiness remain incomplete; the overall pre-camera
objective remains active. Native English and camera-to-server Wi-Fi FTP stay
primary and unvalidated; FL2/FL3 remains deferred.

The [new design](../DEPENDENCY_CHILD_PREFLIGHT.md) binds three complete authored
source buffers and the exact ordinary interpreter profile before entry execution.
An isolated child compiles those checked buffers, acknowledges a real audit hook,
disables it and stops before installed-dependency bootstrap. Its expected runtime
metadata is observed in a separate fresh child before the preflight request is
frozen. Parent execution, interpreter/stdlib binaries and prior review permission
are not authenticated by matching caller-supplied hashes. This preflight does not
invoke the full producer or establish fresh package/native evidence.

The producer now independently requires a fresh nonce acknowledgement before
`ops.bootstrap`. Missing, wrong, replayed and suppressed audit-hook installation
refuse before native loader use. A separate acknowledgement receipt preserves the
unchanged pure contract event grammar. The standalone CLI still refuses activation.

Two owner-authorized independent source reviewers found child interruptions could
leave a live child, output-read errors could escape without completion, and result
checks could accept promoted/extra flags. Repairs added one bounded termination/
reap attempt, retained refusal records and exact closed result/runtime/ack checks.
Deep JSON nesting was separately caught and qualified. Reviewers accepted the
final source/test hashes below for authored-source-only preflight; they did not
execute tests or inspect actual inputs. Their private receipts are parent-saved
transcriptions of their source-review messages.

## Exact commands and results

Host: Windows AMD64, CPython **3.13.12** at
`C:/ProgramData/miniconda3/python.exe`.

- `git status --short --branch`: clean at `797987b`, branch
  `codex/ra003-producer-qualification`.
- `git switch -c codex/ra003-child-entry-qualification`: exit **0**.
- Initial combined ordinary file inspection returned **1** because
  `docs/PRE_CAMERA_READINESS.md` does not exist. The correct
  `research/PRE_CAMERA_READINESS.md` was subsequently read successfully. No test,
  dependency observation or device operation occurred in that lookup.
- Preliminary source/synthetic runs used these exact commands:

```powershell
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.discover('tests',pattern='test_dependency_producer.py'));raise SystemExit(not r.wasSuccessful())"
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests',pattern='test_dependency_child_entry.py'));raise SystemExit(not r.wasSuccessful())"
```

Producer **52/52** passed, zero skips, exit **0**, 15.459s.
Initial child **15/15** passed, zero skips, exit **0**, 2.060s. After review
repairs, the child command with `verbosity=1` passed **20/20**, zero skips,
exit **0**, 2.738s, then final nested-output/reparse checks **20/20**, 2.725s.
These are fresh synthetic attempts, not automatic replays of a refused actual act.

Final source-pinned/logged qualification:

```powershell
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-child-entry/qualify.py focused
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-child-entry/qualify.py full
```

Focused: **72/72 passed**, no skips/failures/errors, exit **0**,
**16.675s** suite / **16.90279179997742s** wrapper; seven stable authored pins.
Full host: **483 cases, 480 passed / three platform skips**, no failures/errors,
exit **0**, **81.849s** suite / **82.29058430000441s** wrapper; **38** stable authored
source/test pins. Composition: 459 retained cases plus four nonce-ACK cases and
twenty child-entry cases. The three skips remain POSIX fork inheritance and two
real-symlink cases unavailable on this host. Both runs checked source hashes
before and after, reserved exclusive started/log/result files and used only the
standard-library authored harness.

Both ordinary CLIs were also invoked through this exact command form, separately
substituting `tools.dependency_child_entry` and `tools.dependency_producer`:

```powershell
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,runpy;sys.path.insert(0,'.');runpy.run_module('tools.dependency_child_entry',run_name='__main__')"
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,runpy;sys.path.insert(0,'.');runpy.run_module('tools.dependency_producer',run_name='__main__')"
```

Each returned **2**, `needs_review` / `real_activation_pending`, with no input
or dependency access through main. Exact argv/stdout/stderr receipts remain private.

| Final reviewed source | SHA-256 |
|---|---|
| tools/dependency_child_entry.py | 1534ecc2e1204b37cfd358d342184360809bab49edb7448fd0db951f7d2090b3 |
| tools/dependency_producer.py | 668ee642d24a1c7e915f116acc0ee081ce783cd0e7ad485b82b345dcf527acf2 |
| tests/test_dependency_child_entry.py | f0895acb28e4c5bd62370599b203b6e2a9f96c02be000b23262bd5f5e53b9d89 |
| tests/test_dependency_producer.py | fe16a69c6627abd8adf77db23f1739c189a0516ec0319945cffd609d1c51b015 |

Focused log: `9846be4f98c1fd8b0888c9d740cd1eac9a042c2b5917a009be64e62d20bc9881`.
Full log: `fa3fbf824b0a0782a0b6e55457921fdad8695439e577b32ef5cd4aaa1f41a2ac`.
The pure dependency contract/source lock are unchanged. Earlier source pins and
reports remain historical, not rewritten to the new producer revision.

## Changes, limits and next action

Eleven public files changed: the new child-entry source/test/design and this
report; existing producer source/test and its design; STATE, BACKLOG,
FEATURE_PROGRESS and CODEX_HANDOFF. Private session/feature notes are updated
after exclusive backups. Only reviewed public files are staged. JSON parsing,
review/test/source hash correlation and `git diff --check` are verified before
commit. The complete staged path list is retained in the private final receipt.

Qualification uses copied authored source buffers, invented expected substitutions
and mocked process failures; real audit tests use manual events, no native loader
or shell command. No installed module/cache, firmware, operational constants,
native payload or historical actual record was opened. No external request,
private upload, camera contact, driver/firmware change, feature/recovery gate or
device-write authorization occurred.

Parent/profile/review declarations are not authentication or approval. Full producer
composition, independently fixed fresh package/root/native expectations and reviewed
once-only activation remain prerequisites. The seventeen historical retrospective
blockers stay retained. Timeout/interruption and oversized output are refusals,
not automatic retries; unreaped children require process reconciliation. Output
read limits are not a hostile-code sandbox or whole-process/disk-output quota.

Next single work package: **RA-003: compose the bound child with the dependency-only producer using independently fixed package/root expectations; qualify the complete invented sequence and independently review the exact once-only activation packet before any installed-dependency observation.**
