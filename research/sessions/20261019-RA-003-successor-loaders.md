# RA-003: successor helper loaders and closed wiring

2026-10-19. Branch codex/ra003-successor-loaders; starting HEAD 672b060.
Evidence: static-inference and offline-tested. Camera commands: **none**.
English and native Wi-Fi FTP remain first; FL2/FL3 and custom looks are deferred.

Implemented [separate checked-buffer helper graphs and closed wiring](../SUCCESSOR_HELPER_LOADERS.md)
against the [reviewed binding specification](../OPERATIONAL_BINDING_SPEC.md).
Child and parent each load their exact five-role graph without invented helpers.
The child owns neutral aliases; the parent uses no sys.modules aliases and
checks shallow global identity before/after saved verification. Whole-graph
hash/AST/compile checks precede authored execution. Lazy imports retain the
same checked objects. Cleanup is one-attempt and preserves foreign replacements
and primary failures, including interrupted publication/close.

The private runtime-shaped wiring binds startup, packet, original expectations,
review/source buffers and operation before controller reservation. It passes
invented=False and no observer to the existing controller. It creates no extra
record owner, retry or process action after unknown completion. The private parent
seam selects saved runtime-record grammar. Public runtime entry and both CLIs
remain disabled; there is no operational request or dependency activation.

Full public host suite: **739 total, 736 passed,
3 existing platform skips**, zero failures/errors, exit0,
381.561208s. This is 708 retained public cases plus 31 new cases.
All 120 pinned authored source/test files matched before/after
the run and at recording. Interpreter C:\ProgramData\miniconda3\python.exe, CPython3.13.12 /
Windows AMD64. Full log SHA-256: `65856393c15ba84933b8240f40a4bf4de8193624447b0e5c78668019fa67d6ef`.

Two separate cleanup-interruption cases passed, zero skips, exit0,
0.291105s; 3 stable source pins.
Two checked-parent integration cases passed, zero skips, exit0,
8.849587s; 121 stable pins. The latter generates invented
controller artifacts, verifies them through the real five-helper parent graph,
and confirms they are refused by the runtime saved-record identity grammar.
These extra four cases are separate from the 739-case public suite.

Qualification uses invented source/packet/native/cipher observations. Runtime
dispatch shape is tested with a stubbed controller; two ownership cases use the
real controller, including one stopped before runtime observer construction.
No complete actual runtime producer/controller path or new operational outer
refusal grammar is qualified. The startup grammar tests use an explicit synthetic
profile; a separate fresh isolated process also passed actual Windows startup.
It reads only the authored wiring source. CLI checks returned2 with no output.
No test establishes hardware behavior, English, native FTP or recovery.

Two authorized independent source reviewers accepted the final four source/test
pins without material findings. The suggested interrupted publication/cleanup
tests were added separately and passed. Reviews are source-only and do not
authorize dependency activation or actual inputs. Frozen helper loaders, the
old adapter, source lock and historical evidence remain unchanged.

Final independent evidence review reconciled all 739 public results, both
separate two-case suites, CLI/startup receipts and current source pins, with no
material findings. This accepts the recorded host evidence within its stated
limits; it establishes no operational authority.

Exact principal commands and results, host-side only:

- `git status --short --branch`: exit0, initially clean on codex/ra003-binding-spec-reviewed.
- `git switch -c codex/ra003-successor-loaders`: exit0.
- `New-Item -ItemType Directory -Path private/sessions/20261019-RA-003-successor-loaders -ErrorAction Stop`: exclusive folder created.
- `C:/ProgramData/miniconda3/python.exe -B -X utf8 -m unittest discover -s tests -p test_dependency_successor_sources.py -v`: exit0, initial18/18 passed.
- `C:/ProgramData/miniconda3/python.exe -B -X utf8 -m unittest discover -s tests -p test_dependency_successor_wiring.py -v`: exit0, initial13/13 passed.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-successor-loaders/qualify.py`: exit0, full public results above. Live handle95189 polled without restart or replay.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-successor-loaders/test_interruptions.py`: exit0, two cases above; source pins and log retained.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-successor-loaders/test_parent_graph.py`: exit0, two checked-parent cases above.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-successor-loaders/cli_check.py`: harness exit0; two CLIs exit2, empty stdout/stderr; isolated Windows startup exit0. Exact subprocess argv retained privately.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-successor-loaders/record.py`: saved result/source checks and private backups before report/state/progress updates.
- `git diff --check`; `git diff --cached --check`: required before explicit reviewed path staging/commit. No push.

Public changed files: tools/dependency_successor_sources.py,
tools/dependency_successor_wiring.py, tests/test_dependency_successor_sources.py,
tests/test_dependency_successor_wiring.py, research/SUCCESSOR_HELPER_LOADERS.md,
this report, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md and
research/STATE.json. Private harnesses, logs, source pins/reviews and backed-up
session/feature notes remain ignored.

Remaining prerequisites: complete outer authority/input/startup/argv/request and
source binding, held helper ownership through final outer reconciliation,
separate closed success/refusal/unknown terminal grammar and complete invented
process-chain qualification. Activity-specific rights/trust reconciliation and
all seventeen historical blockers remain; owner inspection rights remain
No / unknown. Exact mainland-body/build identity, English restriction/resources,
native FTP backend/network lifecycle, backup completeness and conditional
recovery remain unproved. No actual firmware/constants/native dependency reads,
private uploads, upstream execution or camera contact. No feature, recovery or
device-write gate passed. The overall pre-camera goal remains incomplete/active.

Previous goal turn: progress (reviewed source binding specification). This turn:
progress (implemented and qualified successor loaders/wiring).

Next single work package: **RA-003: integrate successor helpers and wiring into a new source-only outer host/child/parent adapter with a closed authority/input roster, exact interpreter/argv/request/source binding and separate success/refusal/unknown terminal grammar. Qualify the complete chain on invented inputs, including single-owner release and supervised interruptions; independently review the source. Preserve frozen predecessors; public runtime remains disabled. No executable actual activation packet, actual dependency/firmware/constants reads or camera.**
