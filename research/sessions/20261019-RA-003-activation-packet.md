# RA-003: activation packet audit and complete package collector

2026-10-19. Branch: `codex/ra003-activation-packet-completion`.
Evidence: **static-inference**, **offline-tested**. Previous goal turn: progress
(fresh reference identity and claims checked, public/private continuity updated).
Current turn: progress (activation gaps localized, complete collector qualified,
private non-runnable candidate assembled). The full pre-camera goal remains active.

English and native camera-to-server Wi-Fi FTP remain primary; FL2/FL3 is deferred.
The [activation design](../DEPENDENCY_ACTIVATION_PACKET.md) records six concrete
source/binding gaps. Existing child schemas and saved-result verification cover
invented composition only. Public production APIs refuse `RuntimeOps`; calling
private `_produce(invented=False)` would bypass the qualified entry. No such
activation command was prepared or executed. A non-runnable packet records these
gaps explicitly rather than inventing missing inputs or declaring readiness.

## Change and qualification scope

New `tools/dependency_package_preflight.py` validates all supplied input bindings
before observations, then collects **351 package files and five trusted origins**
through invented operations. It checks eleven Python source buffers against their
pinned cache, before/after root identities, manifest hashes/sizes, prior cross-API
identity and the eight-MiB concrete read bound. Absolute read receipts are retained;
separate projections change only their path to the manifest-relative key. Fresh
proofs are recomputed and distinguished from prior proofs. The collector never
calls bootstrap, native loading, cipher operations or a continuation callback.

This is sequential cooperative-filesystem collection, not an atomic snapshot or
proof of OS-mapped/transitive native bytes. The invented seam is not a security
sandbox. It rejects RuntimeOps/subclasses, and ordinary CLI exits 2. It is not
integrated into an actual child. All execution/feature/recovery/write authority
flags remain false. Partial actual failure records and execution-time freshness
rules still belong to the complete successor route.

Initial qualification ran 16 cases: 14 passed, one failure and one error, exit 1.
A fixture shallow copy allowed mutated nested stamps to change the prior proof;
exclusive source snapshots and diagnosis preserve this outcome. A deep-copy
fixture correction passed 16/16. Two source reviewers then identified separate
production gaps: mutable expected values passed to the observer and an initial
size check omitting trusted files. The collector now validates against its own
deep snapshot, gives the observer a separate copy, and bounds both file groups
before any observation. Three added regressions qualify those repairs. No
acceptance threshold was weakened.

Both independent source reviewers (`gate_review`, `runtime_review`) accepted the
final collector/tests/design with no remaining material finding for invented-only
scope. They ran no reviewed code or actual input reads. Saved parent-authored
review records report scope and identities, not cryptographic reviewer attestation
or consent for actual activation.

| Reviewed file | SHA-256 |
|---|---|
| Collector | `adc04e46823274d79d2c20ef5b0c02fe0421b079ad89de87458cb2cbfd3da1e0` |
| Collector tests | `bb43675c36d0b821b5647f99223e7db18e328409ed06859271f127b7302e840f` |
| Activation design | `7de5ab92f25e6f244f10f9b9f5358f6c3b24f84dca8c2a2315077cba224383ef` |

## Commands and retained evidence

Interpreter throughout: `C:/ProgramData/miniconda3/python.exe`, CPython 3.13.12,
Windows AMD64, isolated/site-disabled/no-bytecode startup.

Commands are run from the repository root:

```powershell
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-activation-packet/qualify.py focused
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-activation-packet/qualify.py full
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-activation-packet/prepare.py
```

Focused: **117/117 passed**, zero skips, exit **0**, **42.076s** suite /
**42.327735400001984s** wrapper; all eleven selected source/test pins stable.
Focused log SHA-256: `22d691b43843af0d5ac755e155f46f4eddb2b7f87d8afd0fe1da6e522accb134`.
Full-suite and packet results are recorded below.

The packet's refusing check was also run directly:

```powershell
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import pathlib,sys;sys.path.insert(0,str(pathlib.Path.cwd()));from tools import dependency_package_preflight as p;raise SystemExit(p.main())"
$activationCliExit = $LASTEXITCODE
Write-Output "Native CLI exit: $activationCliExit"
if ($activationCliExit -ne 2) { throw 'Unexpected CLI refusal exit' }
```

It emitted `needs_review` / `real_activation_pending`, native exit **2**, with
the explicit PowerShell assertion returning host **0**. The first direct check
emitted the same refusal but PowerShell normalized the host exit to **1** without
capturing the native code. The second check above repeated this documented
side-effect-free refusal only, with no input observation or activation.

The private candidate pins the authored candidate source closure, prior complete
invented qualification, new qualifications and review records, fixed public-vector
plan and intended bounded IO categories. It includes a refusing CLI check only;
the actual activation command and independently current runtime expectation are
absent by design. Historical launcher/runtime observations cannot fill those
expectations. No firmware/constants/native/cache-body inputs are read in this
preparation. The retained collector demonstration uses invented package bytes
only; output receipts are metadata, with no package contents embedded.

Changed public files: new collector, tests, activation design, this session report,
BACKLOG, HANDOFF, FEATURE_PROGRESS and STATE. Private session/feature notes are
updated after exclusive backups. Only explicitly reviewed public paths are staged;
source lock and third-party code are unchanged. Starting HEAD `f790a6c`; inherited
three untracked activation files are completed here. No push performed.

Camera commands: **none**. No device/driver/firmware operation, actual installed
dependency observation, protected-input read, upstream execution or private upload.
No English/FTP support, full rollback, recovery or device-write gate established.
The seventeen historical retrospective blockers remain.

Next single work package: **RA-003: implement and synthetically qualify the complete
noninjected dependency-only child/producer route with the complete package collector,
exact prospective input conversion and runtime/module rules, strict actual-record
parent verification, and once-only stop/reconciliation handling; independently
review before any installed-dependency observation. No protected inputs or camera.**

## Final retained results

Full suite: **528 cases, 525 passed / three existing platform skips**, exit **0**, **108.214s** suite / **108.64443119999487s** wrapper; all **42** source/test pins stable. Skips: POSIX fork inheritance on Windows, inventory symlink creation and UFU symlink creation.

Full log SHA-256: `ae4d8e50222c5d50d8beea2d148bd20b4821ce0274e406bd2ce2bc39c4fcd2f4`.

Preparation script exit **0**: one invented collection, 351 package + five trusted reads, four root observations, zero bootstrap/native/cipher/callback calls. Actual activation remains unavailable. Candidate SHA-256: `3be369f464a7a37fdd40895fda4882ec514f9470a57a3d12dd99d752ded59405`. Private receipt review is recorded separately.

Independent saved-metadata review (`gate_review`) found no material finding in
four current qualification links, source pins, all 351 absolute/relative
projections and proof rows, five trusted receipts, roots and false authority flags.
This accepts invented-record consistency only; prior evidence links and cache-byte
derivation were not replayed. Collection SHA-256:
`d3e679d59a738afcfee3d5767dfe473a835dc325a3d40971e0646cf4b8fcc712`.

Recording command: `& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-activation-packet/record.py`, exit **0**. JSON round-trip checks preserve all unmodified historical state keys. Staged paths/content and `git diff --cached --check` reviewed before commit.
