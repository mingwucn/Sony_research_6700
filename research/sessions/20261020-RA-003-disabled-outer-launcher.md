# RA-003: disabled operational outer launcher

2026-10-20; branch `codex/ra003-disabled-outer-launcher`, based on `1b231c2`.
Evidence: static-inference and offline-tested. English/native Wi-Fi FTP first;
FL2/FL3 deferred. No actual input analysis or camera contact.

The authored launcher now captures the exact 49 child source roles, composes
pending records, owns one isolated child attempt and reconciles its saved
preflight/results against supervised process facts. The child uses the real
retained metadata gate and materialization on invented inputs. Its 46 semantic
roles are a separate checked projection. Fixture generation stays private.
Both public CLIs exit 2 and public runtime entry points refuse.
See [design and remaining gap](../DISABLED_OPERATIONAL_LAUNCHER.md).

The independently reviewed changes bind all 29 retained source bytes, hashes,
sizes and original origins before parent controller/factory execution; clean up
partially constructed parent source loaders; preserve the primary exception and
known process disposition if final publication fails; and reject extra terminal/
evidence fields or malformed digest types. Added regressions cover these four
findings. Reviewer accepted the final three public source hashes with no residual
material finding. Cleanup owners are independent; no automatic retry is added.

## Qualification and limits

CPython **3.13.12**, Anaconda Windows AMD64, executable
`C:/ProgramData/miniconda3/python.exe`; isolated/no-site/no-bytecode, UTF-8,
optimization 0. Source-only review did not access actual inputs.

**150/150 focused tests passed**, zero failures/errors/skips, exit **0**,
**64.676778s**; **106 source/test pins stable** and subsequently revalidated.
This suite comprises the previous 132 cases plus 18 launcher test methods;
subtests are not counted as additional methods. Eight selected modules ran.
The RuntimeOps constructor was blocked. The tests exercise public refusal,
capture/original-source binding, bounded bootstrap checks, parse-all-before-entry,
saved-record validation, cleanup ownership and publication failures.
Unmodified-bootstrap subprocess tests execute inert authored child fixtures.
The full historical suite was not rerun.

Public test log SHA-256:
`fbbb1608bb6d0358bf2d5e8d476891b83e0e0db3a457c31fe8a466ca036a2275`.

The final process wrapper exits **0**, **54.749705s**, with **109 stable pins**:

| Invented case | Wrapper / child | Result | Supervised seconds |
|---|---|---|---|
| Complete | 0 / 0 | consistent_pending_composition | 21.463017 |
| Saved preflight altered | 0 / 0 | needs_review: operational_saved_hash | 20.695107 |
| Captured adapter altered | 0 / no process receipt | needs_review: operational_launch_saved_source before launch | Not applicable |

Both launched cases had one launch attempt, observed exit, closed pipes/readers,
no timeout, no kill/wait attempts and all parent owners closed. All three cases
report closed helper/validation/bootstrap/adapter/outer owners and false
execution/feature/recovery/write flags. The source refusal occurs in the
prelaunch check; it provides no independently observed process counter.

The complete composition uses an explicitly **modified qualification bootstrap**,
which hash-binds an additional private test setup source outside the 49 production
roles. It substitutes runtime dispatch, completion collection and parent saved-
runtime verification. Invented crypto/native observations are injected; no
installed crypto/native backend activates. This proves neither the unmodified
operational runtime path nor authenticity of runtime-shaped fixture observations.
Host imports, interpreter/stdlib and the initial reader/bootstrap remain trusted
assumptions outside captured child sources. Hashes establish bytes, not rights.

## Preserved exploratory outcomes

Each attempt used a new private directory; failed evidence was retained.
No unknown operation was blindly retried.

- `driver.py complete v1`: exit 1 before launch; embedded fixture/setup exceeded
  the fixed 64 KiB request bound. Kept that limit and moved qualification-only
  setup into a separately bounded, hash-bound source file.
- `driver.py complete v2`: exit 1 before launch; helper construction returned the
  loaded package instead of its owner, and cleanup then raised AttributeError.
  Corrected ownership return; cleanup success is not claimed for this attempt.
- `driver.py complete v3`: exit 0, child 0, complete, 21.045597s supervised.
- `driver.py preflight_tamper v1`: wrapper 1, child 0; the code correctly refused
  at the original hash check with operational_saved_hash, earlier than the
  harness's expected semantic error. Cleanup completed, 21.036383s supervised.
  Corrected the harness expectation; no production guard/threshold was relaxed.
- `driver.py capture_tamper v1`: exit 0 with expected prelaunch source refusal.

The private driver changed after review only to expect the stronger hash refusal.
Final driver SHA-256:
`bcafd5b7ff7802b90833d6ca89aed4154832372998b22dd9c9ae748ad63ff10b`.
Final process qualification pins that version. Earlier 13-case and 16-case
launcher-only runs passed before the final 18-method suite; only the final
source-stable qualification is the acceptance result above.

## Exact host commands

All commands below use the primary workspace. The qualification scripts create
exclusive output directories, capture source snapshots/raw logs and record
their exact child commands privately. They are historical commands, not retry
instructions for existing directories.

```powershell
git status --short --branch
git switch -c codex/ra003-disabled-outer-launcher
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-disabled-outer-launcher/driver.py complete v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-disabled-outer-launcher/driver.py complete v2
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-disabled-outer-launcher/driver.py complete v3
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-disabled-outer-launcher/driver.py preflight_tamper v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-disabled-outer-launcher/driver.py capture_tamper v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-disabled-outer-launcher/qualify.py public-v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-disabled-outer-launcher/qualify_process.py v1
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-disabled-outer-launcher/audit.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-disabled-outer-launcher/record.py
git diff --check
git add -- tools/dependency_operational_child.py tools/dependency_operational_launcher.py tests/test_dependency_operational_launcher.py research/DISABLED_OPERATIONAL_LAUNCHER.md research/OPERATIONAL_PREPARATION.md research/sessions/20261020-RA-003-disabled-outer-launcher.md docs/BACKLOG.md docs/FEATURE_PROGRESS.md docs/CODEX_HANDOFF.md research/PRE_CAMERA_READINESS.md research/STATE.json
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git commit -m "feat: add disabled source-captured operational launcher"
git status --short --branch
```

Exploratory exit codes are listed above. Final qualification, evidence audit,
recorder and Git commands exit 0. Audit rechecks all 106/109 qualified source
pins, the public log, final case flags/cleanup, all request/packet hashes and the
single intentional captured adapter drift. Before-images preserve private notes.

Reviewed public raw-byte SHA-256:

| File | SHA-256 |
|---|---|
| tools/dependency_operational_child.py | 157319007f1c435aef2bdee6cdbb21e5da5b9b60c7e165096de7a29c862c02e6 |
| tools/dependency_operational_launcher.py | e6091960b8457f59b63fe945c7aba9a1c9fa3a5a7dba823fe3406e70798e1fd6 |
| tests/test_dependency_operational_launcher.py | b3fea25e0d636bfc28c87d677b828f7bbe1b038e7420913a348056543788fd5d |

Changed public files: these two modules and test, assessment, preparation note,
this report, BACKLOG, FEATURE_PROGRESS, CODEX_HANDOFF, PRE_CAMERA_READINESS and
STATE (11). Private session/feature notes are separately backed up and updated.
The separately committed reference refresh `d781ef8` is not merged here; internal
reference notes and private evidence remain available. Source lock unchanged.

All five decisions remain pending: accepted contract interaction, accompanying
component terms, constants provenance, narrow research hypothesis/scope and a
distinct operational act decision. No actual activation record assembled,
installed dependency activated, firmware/constants/dependency-native payload
read, download/upload or camera contact in this launcher package. Camera commands:
**none**. Exact body identity, native English/FTP, recovery and device-write gates
remain unproved. Previous goal turn: progress (reference review committed
`d781ef8`); this turn: progress (reviewed launcher integrated and evidence recorded).

Next single package: **RA-003: qualify the fixed runtime-shaped completion
collector and saved-parent verification through this launcher using invented
records and the narrowest explicit observer substitution. Remove broader
dispatch/collector/parent-verifier replacements where possible; record every
remaining bootstrap/observer substitution and synthetic provenance. Do not
reinterpret runtime-shaped fixture fields as actual observations. Keep public
runtime disabled, all five decisions pending and actual inputs unopened.**
