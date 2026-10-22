# RA-003: joined synthetic preparation and retained control handoff

2026-10-22. Branch `codex/ra003-joined-synthetic-handoff-20261022`, baseline
`1dac512817fda5aefe3c147bda42a9713c3f47aa`. Evidence: **offline-tested** and
**static-inference**. Native English and native camera-to-server Wi-Fi FTP
remain first. Camera commands: **none**. No feature, recovery or device-write
gate passed. The overall pre-camera goal remains active and incomplete.

Source-owned adapter projection and complete metadata preflight now feed the
current-context constructor and genuine retained record checker/reservations
in one synthetic sequence. The existing preparation, helper and engine owners
then transfer and clean up their resources. The final dependency dispatch,
completion collection and callback bodies are inert; no actual observer runs.

## Changes and review

- `tools/dependency_operational_launcher.py`: `_checked_metadata` shares the
  existing projection, gate, retained-source and full pending-preflight path
  with `_prepare_pending`. `prepare_synthetic_owned` snapshots the caller's
  packet, obtains real source owners, checks that path, writes the exclusive
  packet/request through the existing writer and finishes the current context.
  A successful caller owns cleanup; failure closes acquired owners and leaves
  partial files available for reconciliation. `_finish_current_context` is
  shared with the earlier data-only synthetic entry.
- `tests/test_dependency_preparation_migration.py`: optional temporary root,
  pinned authored control source and invented callback factory let the joined
  fixture reuse the existing preparation graph. Existing defaults are preserved.
- `tests/test_dependency_joined_handoff.py`: **11** cases join the path above
  to actual `Preparation`, `HelperSources` and `_continue_child` ownership.
  Tests cover rehashed metadata and disk drift, detached nested receipts,
  partial child-record reservation, dispatch/callback/collection interruption,
  incomplete returns and callback-close failure without retry. Real handles
  and transferred owners close along those paths; incomplete results cannot
  claim completion.

Independent local review found and resolved a caller-receipt alias: the packet
is now detached before full preflight, and mutation of the original maps cannot
alter the returned preflight arguments. It also found a fixture-only cleanup
gap: creating preexisting child evidence is now inside the parent-record
`finally` block. Final review found no remaining concrete blocker in this scope.

Actual parent and child v6 refusals remain before runtime/profile or command
output execution. Public runtime/CLI refusals remain. No new operational
allowlist, target profile, approval record or generic context schema was added.
The synthetic seam trusts its authored caller and invented profile; its name
does not enforce a sandbox or authenticate arbitrary supplied inputs.

## What was real and what remains simulated

| Stage | Observed scope |
|---|---|
| Projection, pending metadata preflight and v6 gate algorithm | Real authored source owners and validators; regenerated ancestry/evidence policy for invented records. Historical actual records are unchanged. |
| Current context and saved command | Real constructor, existing exclusive writer and saved-source checks over the invented temporary tree. |
| Retained control | Pinned unchanged authored checker, genuine `verify_context`, `reserve_parent`, `reserve_child` and ordinary file-handle close. The parent marker binds the synthetic child reservation. |
| Preparation and helper/adapter lifecycle | Real materialization/binding and ownership code. Ordinary refresh obtains invented bytes from the fixture's memory registry. |
| Child startup | Scoped removal/restoration of `tools` module aliases satisfies the unchanged helper guard in-process. This is not observed isolated-child startup. The earlier separate inert-bootstrap transport test remains in the combined suite. |
| Callback, dependency dispatch and completion | Explicitly inert invented wiring. No installed native/crypto activation, retained supervisor/observer or actual GDT processing. |

The retained control source is 58,942 bytes, SHA-256
`70a2ed3a0265894adace48e5285c0eb8962c666975f7df1a8e4f6141b918bb43`.
Only that exact named private authored source is used. It is not copied into
Git. A missing checker causes explicit skips; a different identity fails.
The checker verifies ordinary-file consistency, not argv/basis semantics or
execution authority. Complete source/request/bootstrap checks have their own
responsibilities. Synthetic success does not qualify the actual pending route.

## Commands and results

Host: Windows, PowerShell **7.6.5**, CPython **3.13.12** at
`C:/ProgramData/miniconda3/python.exe`. Initial Git state was clean on
`codex/ra003-synthetic-runtime-preparation-20261022` at the baseline above.

```powershell
git status --short --branch
git switch -c codex/ra003-joined-synthetic-handoff-20261022
New-Item -ItemType Directory -Path private/sessions/20261022-joined-handoff -ErrorAction Stop | Out-Null
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-joined-handoff/qualify.py qualification-01
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-joined-handoff/qualify.py qualification-02
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-joined-handoff/write_report.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-joined-handoff/record.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-joined-handoff/verify.py
git diff --check
```

The first combined attempt ran **150 cases: 149 passed, 1 skipped, no test
failures/errors**. It exited **1** because the final fixture cleanup/header
edit landed during its source capture (`source_stable=false`). It is preserved
as nonfinal evidence, not accepted qualification. No predicate or threshold was
relaxed. A prior focused 11-case pass overlaps this suite and is not added to
the total.

Final stable combined qualification: **150 cases, 149 passed,
0 failures, 0 errors, 1 skipped**, exit **0**;
**95.445s** unittest / **95.838s** runner. All **7**
captured source/test files stayed byte-identical. The sole skip is Windows
symlink creation, privilege error **1314**; hard-link refusal passed. No elevation
or system change was attempted. Report creation, progress synchronization,
final invariant verification and diff checks exited **0**. The first private
invariant-verifier attempt exited **1** because it assumed `camera_contact_hold`
was a boolean; the existing schema stores an object. The verifier was corrected
to check its `active`, approval and execution fields, and passed. No project
state or acceptance condition was changed to satisfy that check.

The private runner explicitly loads these modules under `-I -S -B -X utf8`,
adding only the repository and tests directory to its import path. It uses no
broad discovery:

```text
test_dependency_joined_handoff
test_dependency_current_context
test_dependency_retained_context
test_dependency_preparation_context
test_dependency_host_entry
test_dependency_migration_transport
test_dependency_operational_launcher
test_dependency_preparation_migration
test_dependency_operational_preparation
test_dependency_operational_entry
```

This is focused integration qualification, not a new whole-repository, pristine
host or remote CI result. The dated 748-case suite remains historical and scoped.
Final raw log: `private/sessions/20261022-joined-handoff/qualification-02.log`,
SHA-256 `6dd9e620b1f1f8ad7def8276ab30f9b4a7761c6327983c398c402be1252c57a7`. The private directory
also retains the earlier attempt, source-pin receipts, scripts, note before-images,
verification and local Git completion receipt.

| Changed source/test | Working-file SHA-256 at qualification |
|---|---|
| `tests/test_dependency_joined_handoff.py` | `e112ccb66b86787eeab02d1bf776744fdb920819477c5d9f60d81759ccfaff8c` |
| `tests/test_dependency_preparation_migration.py` | `e3561568cd201c66fdd63f3e4b973bac301d3c9a995c04f80f5ae1861b65716c` |
| `tools/dependency_operational_launcher.py` | `8ff194d6a954904c0e0345edf4f0ae3f375213372d98421e90a7620e64bb09a1` |

## Progress notes, prerequisites and next package

Public state/backlog/feature/handoff notes and ignored internal notes agree on
the joined result and the next technical package. The authoritative goal tool
reports **active**; old blocked summaries and pending records remain historical.
Stale current pointers to the one-test deferred constructor and 61-case pending
review are corrected without changing those historical results. Published FTP
unlock-tool source is recorded as reviewed; its underlying resident backend and
body applicability are still unverified. Source-reviewed ordinary-USB/native
reader leads are distinguished from unqualified Windows/body access.

| Remaining prerequisite | Current disposition |
|---|---|
| Exact-current source/runtime closure | Finite audit and repair of the existing two-lead route remains: role/path/hash bindings, bootstrap, saved request/argv, historical/current projection, retained control/helper ownership and actual execution boundary. No new generic context layer is needed. |
| Actual metadata/content evidence | No actual GDT result follows from these tests. GDT is layout evidence only; resource/locale navigation and resident FTP code tracing are subsequent bounded content questions. |
| English | Matching resource coverage, locale/restriction consumers, fonts/layouts and narrow reversible selection are unmapped. Native English is unvalidated. |
| Native FTP | Published unlock source is a static lead. Resident UI/config/media/worker/network/credential/lifecycle chain, exact mainland binary correspondence and direct file-equality transfer evidence remain absent. |
| Exact body and recovery | Installed binary identity, Windows/body access, current-state preservation and a credible recovery envelope remain unverified. Camera contact stays on hold, including the Windows inventory query. |

No new owner facts or legal questions are needed for the next offline package.
No firmware, constants, native payloads or raw prefixes were opened this turn;
no downloads, uploads, upstream launchers/service tools, driver changes or camera
operations occurred. No feature, installed dependency, recovery or write gate
is qualified. FL2/FL3 remain deferred; calibrated looks and a host-assisted bridge
remain separate later results.

Public changed files: the three source/test files above; this report;
`research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`,
`research/PRE_CAMERA_GAP_AUDIT.md`, `research/ANALYSIS_PREREQUISITES.md`,
`research/PRE_CONTACT_DECISION.md`; `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`,
`docs/FEATURE_PROGRESS.md`. Ignored updates: `private/session-state.json`,
`private/feature-progress.json`, `private/feature-progress.md` and this session's
scripts/logs/receipts/before-images. Frozen originals and source locks stay unchanged.

After named-file content review, completion commands are:

```powershell
git add -- tools/dependency_operational_launcher.py tests/test_dependency_preparation_migration.py tests/test_dependency_joined_handoff.py research/sessions/20261022-joined-handoff.md research/STATE.json research/PRE_CAMERA_GAP_LEDGER.json research/PRE_CAMERA_GAP_AUDIT.md research/ANALYSIS_PREREQUISITES.md research/PRE_CONTACT_DECISION.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-joined-handoff/verify.py final-state
git commit -m "feat: qualify joined synthetic preflight handoff"
git status --short --branch
```

Only reviewed named files are staged and committed locally; no push or external
submission. The resulting commit is recorded in the ignored completion receipt
and the session response.

**Next single work package:** RA-003: audit the finite exact-current source/runtime
bindings for the existing two-lead GDT route. Compare current authored sources,
bootstrap and historical/current metadata against the frozen projections; identify
and repair concrete mismatches, then give an explicit readiness decision. No new
generic context layer, protected observation, dependency activation or camera
contact. English/native FTP stay first.
