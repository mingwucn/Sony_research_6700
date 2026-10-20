# RA-003 disabled operational engine composition

2026-10-20. Branch `codex/ra003-operational-entry`.
Evidence: static-inference and offline-tested. Camera commands: **none**.

Previous goal turn: progress, commit `f04ed9e` readiness audit. Starting tree clean.
This implements part of the next source package: separate child and parent engine
composition and explicit result/cleanup boundaries. It does not complete the
operational launcher, ordinary-record migration or actual activation readiness.
See [implementation and remaining boundaries](../DISABLED_OPERATIONAL_ENGINE.md).

The child invokes trusted metadata preparation before the existing internal runtime
seam, without an injected observer/cipher/mode. It requires successful callback
completion, release and record close. Parent verification invokes the saved-runtime
seam after the existing prepared-source/process checks. Owners close independently
once; failures stay sticky and preserve primary exceptions. Engine returns leave
all feature/recovery/write/production qualification flags false. Caller-owned
wiring/preparation/source anchors and process facts still require the future outer
binding; matching buffers is not authenticated permission or OS evidence.

HelperSources now retains checked source buffers and freezes compiled code,
mode/order/origin/hash policy before execution. Independent source review found
that matching buffers alone did not bind replaced compiled code, and that claimed
callback state alone missed swallowed callback failure. Both findings were repaired;
new regressions cover compiled/policy replacement, source drift, callback error,
duplicate claim/release, uncertain close and independent failure cleanup. Final
source review accepted the repaired four-file delta. Private review.txt retains
final reviewed hashes; no operational approval was granted.

## Exact verification commands/results

```powershell
git status --short --branch
git switch -c codex/ra003-operational-entry
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-operational-entry -ErrorAction Stop | Out-Null
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-operational-entry/qualify.py initial-v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-operational-entry/qualify.py repaired-v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-operational-entry/qualify_full.py qualification-v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-operational-entry/driver.py private/sessions/20261020-RA-003-operational-entry/smoke-v1 complete
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-operational-entry/qualify_full.py qualification-v2
```

Initial/focused/smoke/final commands exit 0; the first full qualification-v1 exits 1. Initial 78/78 passes preceded independent review and do not
supersede its findings; initial code/tests and result/log are preserved privately.
Repaired focused qualification: 84/84 passes, zero failures/errors/skips, 46.070369
seconds wrapper. Full final qualification: **243/243 pass**, 227 public and
16 invented process cases; zero failures/errors/skips; 297.499384 seconds, 198 stable
source pins, exit **0**, CPython 3.13.12 Windows AMD64 with isolated/no-site/no-bytecode
flags and optimize 0. Log SHA-256: `52da785f4e852295eb57bfde1e428a36e73f8dd0ff602f2e549e62ea28439ec7`.

The first full run passed 227 public cases, but all 16 process cases stopped before
child launch on the historical frozen-source assertion. That comparison packet
pins the former helper text. The local fixture now supplies the preserved original
helper bytes, checked against the frozen size/SHA, only during historical seed
construction. Current execution captures still read the new helper normally.
Production predicates and historical records are unchanged. The failed 243-case
run, its log/result/source snapshots and initial fixture are preserved; the corrected
complete smoke and final full regression are separate new outputs. Independent
review accepted this fixture-only historical/current-source separation.

Public suites block RuntimeOps construction. New engine tests use invented records,
the real prepared adapter, and intercepted runtime/saved-verifier dispatch. Loader
regressions execute authored Python in isolated children; they load no installed
native dependency. The complete prior invented process suite was rerun because its
shared helper loader changed: fixed invented stream/constants, fake dependency and
identity cipher only. All process children exited, reader threads joined and pipes
closed; frozen 300/5/1-second and 2-MiB-per-pipe limits remain. No actual operational
metadata was read or qualified. Full current firmware/installed-library operation,
English, native FTP, recovery and device writes remain untested.

Exploratory rg reads used one wrong retained source location and a Windows wildcard
path, returning exit 1; the known integration/prospective_child.py location was then
read. No operation/output was retried or lost. Other ordinary reads used Get-Content
and rg only. No network requests, upstream execution, firmware/constants/native
payload reads, installed dependency activation or camera contact occurred.

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-operational-entry/record.py
git diff --check
git add -- tools/dependency_operational_entry.py tools/dependency_successor_sources.py tests/test_dependency_operational_entry.py tests/test_dependency_successor_sources.py research/DISABLED_OPERATIONAL_ENGINE.md research/sessions/20261020-RA-003-operational-entry.md research/STATE.json research/PRE_CAMERA_READINESS.md docs/BACKLOG.md docs/FEATURE_PROGRESS.md docs/CODEX_HANDOFF.md
git diff --cached --check
git diff --cached --stat
git commit -m "feat: compose disabled operational engines with owned cleanup"
git status --short --branch
```

Reviewed public files: two engine/loader sources, two test files, the implementation
assessment, this report, STATE, pre-camera ledger, backlog, feature progress and
handoff. Private session/feature notes backed up before update. Source lock, frozen
scope and historical evidence remain unchanged. No feature or device gate passed.

Remaining prerequisites: separately owned operational outer source closure, metadata
preparation and ordinary/preflight/result contracts, actual supervisor-derived
process bindings, five activity-specific decisions and current in-act dependency
provenance. Exact target/region correspondence and usable pre-write rollback remain
unproved for applicable later device work. Full pre-camera goal remains active.

Next single package: **RA-003: bind the disabled operational engine composition into a separately source-owned outer parent/child preparation and saved-result path. Derive its exact source map and operational ordinary/preflight/result contracts, preserving frozen supervision and observation limits. Qualify with invented records and intercepted runtime calls only; independently review before actual record assembly or activation. Keep five decisions pending; no installed dependency activation, firmware/constants/native payload reads, downloads/uploads or camera contact.**
