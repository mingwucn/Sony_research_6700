# Session report: 2026-10-18 / pre-camera R0 foundations

Status: host implementation completed for the bounded foundations below; overall
pre-camera objective remains ACTIVE with real-server/remote-host work and target
prerequisites outstanding. This does not close full RA-003/004/005/006/007, FT-102
or IN-102 acceptance, any feature or a device-write gate.

Starting commit: `2cdb777460035d37ee3708a2fc0fc639973d6e06`, clean
`codex/ra-002-reference-audit`. New topic branch:
`codex/pre-camera-offline-foundations`. Earlier RA-001/RA-002 evidence was retained.
The owner's broader objective authorizes independent host work after RA-002;
unknown firmware remains unknown. Risk: R0, no server listener this session.

Camera commands: **none**. No USB enumeration, protocol/network camera query,
mode transition, driver change, upstream launcher/import, firmware execution,
device write, automatic rollback/reboot or private-input upload occurred.

Host: Windows AMD64 build 26300.9711; CPython 3.13.12 at the existing local
interpreter; PowerShell 7.6.5 and Git 2.53.0.windows.2. No Python package or host
driver was installed. Public action refs/text and standard-format documentation
were read; no action code ran locally, no project push or workflow dispatch occurred.

## Implemented behavior and evidence

| Work | Result | Evidence and practical limit |
|---|---|---|
| Inventory portability | Cross-API identity/size/mtime matching, separate path/fd ctime stability; 27 pass/one skip | offline-tested; detects observable mutation, not an atomic snapshot |
| Bounded artifact probe | Same-read SHA-256/size plus at most 4096 prefix bytes; eight tests pass | offline-tested; header/signature leads only, no extraction, identity or ABI proof |
| Candidate guards | Exact complete synthetic source sets, reviewed fixture labels, bounds/protected windows, deterministic manifests and exact inverses; 20 tests pass | offline-tested; real/UNVERIFIED target profiles always refused; review refs are caller claims |
| Transaction model | Prepare ordering, single shared in-memory ownership, every two-object interruption boundary and explicit uncertain reconciliation/resume; 16 tests pass | offline-tested; no persistent device journal, OS camera lock or executor |
| Durable mock queue | 100 objects/50 RAW+JPEG groups plus identity/path/hash/retry/cancel/persistence/ownership failure cases; 25 tests pass | offline-tested; mock is not FTP/FTPS, native Wi-Fi or a host-assisted camera bridge |
| CI preparation | Four Windows/Linux × Python 3.10/3.13 jobs; verified immutable action pins, minimal permissions, synthetic-only inputs | static-inference; workflow acceptance and all remote jobs NOT RUN |
| Target preparation | Artifact lineage/backup templates, extractor text audit and evidence-gap dossier; all 27 packages mapped | static-inference; no target mapping, acquisition, backup or access approval |

Independent queue review found two implementation defects before integration:
failed persistence of a committed hash could leave an inconsistent review state,
and concurrent creators could race the initial existence check. Both were fixed
with focused regression tests. Earlier focused logs remain private; the final
combined result below includes both fixes. No acceptance threshold was relaxed.

The PMCA DAT locator was inspected only as Git object text at the already locked
revision. Its header/chunk scan does not establish bounded complete extraction or
alpha6700 applicability, and its implementation was not adopted. No actual target
package exists in the checked private workspace; no whole-host search was made.
An empty blocked private package ledger is not a diagnosis of an unseen package.

## Exact commands and results

All commands below are host-side from the repository root. The private capture
utility writes a NEW JSONL per label with prepared argv before execution and then
the output/exit result. It executes authored local code/tests or read-only Git.

| Command | Actual result |
|---|---|
| `git status --short --branch` / `git log -4 --oneline` | Clean starting branch at `2cdb777`; prior commits preserved |
| `git switch -c codex/pre-camera-offline-foundations` | Exit 0 |
| `python private/sessions/20261018-pre-camera-R0/capture.py prepare-private python private/sessions/20261018-pre-camera-R0/prepare_private.py` | Exit 0; prior state exclusive snapshot, hashes of 27 earlier private files, empty blocked package ledger |
| `python -m unittest discover -s tests -p test_offline_inventory.py -v` | CPython 3.13.12, exit 0; 28 total, 27 passed, one real-symlink skip |
| `python -m unittest discover -s tests -p test_artifact_probe.py -v` | Exit 0; eight passed |
| `python -m unittest discover -s tests -p test_candidate_guards.py -v` | Exit 0; 20 passed |
| `python -m unittest discover -s tests -p test_transaction_model.py -v` | Exit 0; 16 passed |
| `python -m unittest discover -s tests -p test_transfer_queue.py -v` | Final focused exit 0; 25 passed in 13.487 s |
| `python private/sessions/20261018-pre-camera-R0/capture.py combined-tests python -m unittest discover -s tests -v` | Exit 0; **97 total, 96 passed, zero errors/failures, one skip**, 12.259 s |
| `python tools/artifact_probe.py --help` | Exit 0; bounded local-file CLI only |
| `git -C external/pmca-reference show a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0:pmca/firmware/__init__.py` | Exit 0; text read, blob `a136d25c68e8cae340405e5237163038b7467745` |
| `git -C external/pmca-reference show a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0:pmca/util/__init__.py` | Exit 0; text read, blob `b2ee7d939661150ebb4c0c15f2b8a6eb0d96847e` |
| `git ls-remote --tags https://github.com/actions/checkout.git refs/tags/v7.0.1 'refs/tags/v7.0.1^{}'` | Exit 0; `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| `git ls-remote --tags https://github.com/actions/setup-python.git refs/tags/v7.0.0 'refs/tags/v7.0.0^{}'` | Exit 0; `5fda3b95a4ea91299a34e894583c3862153e4b97` |


Completion uses the same capture utility with unique labels and
`python private/sessions/20261018-pre-camera-R0/complete_session.py`:
`check`, then separate `stage <group>` / `commit <group>` calls for `inventory`,
`guards`, `queue`, `ci`, and `records`, followed by `private-state` and `final`.
Each stage call uses `git add --` with only its explicit reviewed paths, checks
`git diff --cached --name-only` and `git diff --cached --check`, and presents the
full staged diff before the separate commit. Final verification checks a clean
branch, all 25 authored paths, preserved private evidence and unchanged locked
sources/UNVERIFIED profile. Exact argv, results and commit identifiers are retained
in new private capture logs and ordinary Git history.

The initial completion check exited 1 before staging: its private evidence-map
lookup used forward slashes while Windows had recorded backslashes. The original
helper and failure log were preserved; key normalization repaired only the private
validator. No project code/test or evidence file was altered to conceal a failure.

Focused runs were wrapped by the same capture utility with unique labels; agent
review/runs are also documented in their authored notes. One early queue run
outlived the initial tool wait; a host process query established it had ended
before any fresh invocation. It was not treated as a live camera operation or
restarted solely because a tool wait expired.

The separate real-symlink fixture still cannot be created on this host. Mocked
symlink rejection passes but is not physical filesystem coverage. The initial
RA-001/002 failed inventory results remain in their original committed reports;
this repair neither erases them nor proves every Windows filesystem/Python build.

The former ELF reference endpoint timed out; the maintained gABI reference was
read. [Artifact intake](../../docs/ARTIFACT_INTAKE.md) and
[host validation](../../docs/HOST_VALIDATION.md) link the primary format/action
sources and distinguish declarations from observed results.

## Changed files and private evidence

Authored code/tests: inventory helper/test, artifact probe/test, candidate guards/test,
transaction model/test and transfer queue/test. New docs: ARTIFACT_INTAKE,
INVENTORY_PORTABILITY, OFFLINE_GUARDS, FTP_HOST_PROTOCOL and HOST_VALIDATION.
New preparation records: PRE_CAMERA_READINESS, TARGET_EVIDENCE_GAPS and this report.
New templates: ARTIFACT_LINEAGE and BACKUP_CATALOGUE. New synthetic CI workflow.
README, CODEX_HANDOFF, BACKLOG and STATE were reconciled with actual available APIs.

Raw logs, empty package ledger and previous/current private state remain under
ignored private storage. Owner intake, all earlier session files and the original
state snapshot are preserved. No reference checkout, source lock, target profile,
firmware/table bytes, third-party code, photo or private log is part of these commits.
Only explicitly reviewed paths are staged; staged paths/content and whitespace,
JSON/link checks, unchanged protected files and final commit/status are recorded
in the private completion evidence. No project-wide licence was selected.

## Completion boundary and next single package

The host foundation is testable; the full requested preparation remains active.
Real isolated-server FTP/FTPS tests and actual remote CI/clean-host evidence are
still available follow-up work. Firmware/region/body facts, legitimate exact-build
inputs, native ABI/storage/resources, access/recovery, backup coverage and physical
feature tests remain unresolved. No native backend route or target candidate was
selected. All CLT/ENT and native FTT tests are NOT RUN.

Next single available package: **FT-102 — isolated host-side server capability and
failure harness**, retaining synthetic-only inputs and separately scoped loopback
networking. It must prove actual TLS/hash/read-back/no-clobber assumptions or
document a precise unsupported capability. Target-specific RA-003 acquisition
remains blocked until installed firmware and matching provenance exist.
