# Host validation and release-content review

Evidence class: **offline-tested** for observed synthetic runs; **static-inference**
for publication/workflow review. The final-code clean export and all four actual
Windows/Linux CI jobs passed on 2026-10-18. Results apply to the recorded
revision/interpreters/runner images, without camera feature or device eligibility.
The original preparation session performed no push; the later qualification
session pushed reviewed authored source and opened draft PR #5.

The later [loopback FTPS lab](FTPS_LOOPBACK_LAB.md) is a separate opt-in runtime
with locked private dependencies. Its `lab_tests/` directory is outside this
workflow's discovery path. New client/archive policy tests under `tests/` use
only the standard library and mocks/synthetic archives; they never start the
server, create the dependency environment or retrieve artifacts.

Local standard-library text assertions passed with exit 0: two full action
pins, four declared matrix combinations, read-only token scope, disabled
credential persistence, the two expected Python commands, and absence of secret
references, package installs, uploads and unsafe event triggers. A whitespace
check covered both new files. These are explicit content checks, not a YAML
parser or GitHub workflow acceptance test; no YAML package was installed.

## Prepared CI scope

[offline-tests.yml](../.github/workflows/offline-tests.yml) runs the repository's
standard-library synthetic `unittest` suite on GitHub-hosted `ubuntu-24.04` and
`windows-2025`, each with CPython 3.10 and 3.13, on pushes, pull requests and manual
dispatch. The job records `python -VV`, permits ten minutes per matrix job, and
keeps other jobs running when one fails so all observed failures remain visible.

The only token permission is `contents: read`. Checkout does not persist
credentials, fetch submodules or fetch LFS objects. The workflow installs no
Python packages, enables no dependency cache, supplies no private paths or
secrets, and uploads no artifacts. Tests create synthetic fixtures locally;
they must not import camera adapters, contact a camera or FTP server, retrieve
reference checkouts, or execute firmware or upstream launchers.

The hosted workflow itself uses GitHub's action/runner infrastructure. Checkout
retrieves this repository, and Python setup may provision a Python distribution
when it is absent from the hosted tool cache. This is not a fully network-isolated
or hermetic build. OS runner images and Python minor-version patch selections can
change; the interpreter output and run metadata must be recorded with results.
No private acquisition artifacts belong on hosted runners.

## Verified action pins

On 2026-10-18, read-only Git queries against the official `actions` repositories
returned these full commit pins. Both version refs were lightweight tags, with
no separate peeled-tag result. The floating major tags were inspected to choose
the maintained v7 line; the workflow uses only the full immutable commit IDs.

| Action | Observed version | Full commit | Official pinned source |
|---|---|---|---|
| `actions/checkout` | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` | [action metadata](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/action.yml), [README](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/README.md) |
| `actions/setup-python` | v7.0.0 | `5fda3b95a4ea91299a34e894583c3862153e4b97` | [action metadata](https://github.com/actions/setup-python/blob/5fda3b95a4ea91299a34e894583c3862153e4b97/action.yml), [README](https://github.com/actions/setup-python/blob/5fda3b95a4ea91299a34e894583c3862153e4b97/README.md) |

Exact pin-resolution commands, each exit 0:

```text
git ls-remote --tags https://github.com/actions/checkout.git refs/tags/v7.0.1 'refs/tags/v7.0.1^{}'
git ls-remote --tags https://github.com/actions/setup-python.git refs/tags/v7.0.0 'refs/tags/v7.0.0^{}'
```

The pinned `action.yml` files and READMEs were retrieved as text from
`raw.githubusercontent.com` and inspected without executing their JavaScript.
Both actions declare the Node 24 runtime; their documentation identifies runner
v2.327.1 or later for that runtime. This preparation selects GitHub-hosted runners
only and makes no self-hosted runner compatibility claim. No third-party action
code was copied into this repository or executed locally. Future action updates
require a new source/ref review and an explicit pin change.

## Local and future result interpretation

The exact local suite command is:

```text
python -m unittest discover -s tests -v
```

Record interpreter path/version, OS, branch/revision, command, exit code, counts
and every skip or failure in the session report. Local Windows results do not
prove the Ubuntu or alternate-Python jobs. A workflow file or valid-looking YAML
does not prove that GitHub accepted or executed it. For each future remote run,
record its URL, tested commit, matrix job, selected interpreter, exit status,
test counts, skips and relevant log evidence before changing `remote_ci_executed`.

Real symlink creation can be unavailable on Windows. The suite keeps that real
filesystem test separate from deterministic mocked symlink refusal. A skipped
real test remains **NOT TESTED** for that host; passing mocks do not replace real
filesystem coverage. Passing synthetic inventory, candidate or queue tests does
not qualify extraction completeness, a device access route, actual FTP/FTPS
semantics, backup recovery, or an alpha6700 feature.

## Earlier clean authored-tree reproduction (historical)

On 2026-10-18, a NEW export of commit
`9d5f4bafe5046f0de4e5dcdd0455bac362ba8a64` supplied 58 committed regular files
(526,953 bytes). Each Git blob identity and SHA-256 was checked before execution;
the whole exported source set was identical afterward. No `.git`, ignored
private inputs, reference checkouts, dependency artifacts or lab runtime were
copied. Lock metadata and authored lab/policy-test source are ordinary committed
files; the opt-in server suite was not run.

A NEW stdlib venv was created using CPython 3.13.12 with `-I -S -B -X utf8 -m
venv --without-pip --copies`. Its system-site option was false and its
site-packages directory was empty. Pip and the seven optional lab packages were
not discoverable. From an unrelated working directory, the venv interpreter ran
an authored wrapper with `-I -S -B -X utf8`; the wrapper explicitly added only the
export root and discovered its absolute `tests/` directory. All 16 recorded
authored/test module entries were within the export, except the expected
`tools` namespace entry without a file. Result: **130 total, 129 passed, 1 skipped,
exit 0**. The skip is unavailable real-symlink creation, still NOT TESTED.

The first wrapper mistakenly prohibited `socket.gethostname`, which stdlib
`platform.machine()` uses for local metadata on Windows. It produced 123 passes,
six setup errors and one skip, exit 1. That workspace, source and logs were
preserved. A reviewed NEW harness/workspace allowed and logged only that exact
local read, retaining all other `socket.*` prohibitions; tests and their
acceptance were unchanged. The successful run recorded one local hostname event,
zero prohibited socket events and no loaded pip/lab-package modules. The hook
covers its parent Python process, not subprocesses or an OS network boundary.

This is a clean source tree and fresh environment on the same existing Windows
host/base stdlib, **not** a clean OS, independent-host or remote CI result.
Native SSL/OS trust and inherited SSL configuration remain host dependencies;
checking selected module names is not a universal package scanner. At that earlier
revision, other platforms/interpreters and real symlinks were unobserved. The later qualification
below supplies recorded host results; physical faults and camera behavior remain
unproved. No dependency was installed/downloaded, and no network connection,
listener or camera operation was requested. [Exact commands and retained evidence](../research/sessions/20261018-IN-102-clean.md).

## Final-code qualification observed on 2026-10-18

Code revision: `fb32370052a0ffe5d8a529edba971f962ce57654`. A NEW verified export
contained **63 files / 628,717 bytes**, all unchanged after execution. A fresh
no-pip stdlib environment on the same Windows AMD64 host / CPython 3.13.12 ran
**154 total / 152 passed / two skipped / zero failures or errors, exit 0**.
The local skips are POSIX fork and unavailable real-symlink creation. Actual
hard-link refusal passed. No private/reference/lab runtime inputs were used.
The parent audit hook is a process-local check, without an OS/subprocess network
boundary; one local hostname metadata event was permitted and recorded.

[Push run 39149570514](https://github.com/mingwucn/a6700_research/actions/runs/39149570514)
tested that exact commit. Each job ran `python -VV` and
`python -m unittest discover -s tests -v`, with **154 total / 153 passed /
one platform-specific skip / zero failures or errors, exit 0**:

| Runner selector | Requested Python | Observed CPython | Suite seconds |
|---|---|---|---|
| Ubuntu 24.04 | 3.10 | 3.10.22 | 7.091 |
| Ubuntu 24.04 | 3.13 | 3.13.16 | 8.963 |
| Windows 2025 | 3.10 | 3.10.11 | 30.633 |
| Windows 2025 | 3.13 | 3.13.16 | 21.621 |

Observed images: Ubuntu `20261012.334.1`; Windows `windows-2025-vs2026` /
`20261007.264.1`. Ubuntu passed POSIX inherited-lock and actual symlink tests;
its skip is Windows path syntax. Hosted Windows passed actual symlink and
Windows path-policy tests; its skip is POSIX fork. This does not remove the
owner host's actual-symlink gap or qualify every filesystem/interpreter.

Supplemental [PR run 39149603684](https://github.com/mingwucn/a6700_research/actions/runs/39149603684)
also passed all four jobs with the same counts. Its merge checkout tree exactly
matches the tested code tree. All eight full job logs and API metadata were
inspected and retained privately. No failed job was hidden by rerunning.

The [session report](../research/sessions/20261018-IN-102-final.md) contains exact
commands, versions, job links, limits and the publication audit. The historical
58-file run above remains tied to its own older source revision. Current
qualification edits change documentation/state only; code, tests, workflow,
locks, target profile and acceptance thresholds remain byte-identical to the
qualified code revision. IN-102 remains partial for broader release/rights and
exact-target requirements; no pristine OS or camera qualification is claimed.

## Local release-content policy

Before staging, inspect `git status --short --branch`, review each authored
change and run `git diff --check`. Add only explicit reviewed paths. Then inspect
`git diff --cached --name-only`, `git diff --cached --check` and the complete
`git diff --cached` contents. Check `git ls-files --stage -- private/ external/`
and refuse publication if private/reference inputs are tracked. Ignore rules do
not protect tracked content or secrets pasted into otherwise ordinary files.

The review must exclude firmware and generated firmware/table payloads, dumps,
calibration, serial/MAC identifiers, photos, credentials, network captures, SDK
packages, private paths and raw logs. Review text as well as names; do not trust
file extensions, a private repository, or a green test run as a content check.
Inspect unexpected symlinks/hard links or binary additions before staging and
confirm each proposed file's origin. Keep private evidence local and publish only
sanitized authored summaries and synthetic fixtures.

Review component rights before importing third-party code or assets. The
[reference audit](../research/REFERENCE_AUDIT.md) records different source-code,
firmware-derived-data and profile terms; it is not a blanket redistribution
grant. This project still has no selected project-wide licence. CI configuration
does not select one or clear future dependencies.

Run relevant synthetic checks against the reviewed staged revision and record
limitations. Publication, release or a later device operation still requires its
own applicable evidence and authorization; no CI result passes a device-write
gate. These manual checks are a review policy, not an implemented secret scanner
or a guarantee that every prohibited datum can be detected automatically.

Camera commands in CI preparation and qualification: **none**. Host network
activity was limited to public official/reference material and authenticated
repository/CI operations. Only reviewed authored source and sanitized summaries
were pushed; private inputs and raw evidence were not uploaded.
