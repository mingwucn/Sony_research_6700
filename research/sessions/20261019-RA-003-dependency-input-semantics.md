# RA-003: dependency input semantics

Session started 2026-10-19 on `codex/ra003-dependency-input-semantics`, HEAD
`e375ac8`. Evidence: static-inference and offline-tested. Camera commands: **none**.
Session continued across midnight and was finalized on 2026-10-20 local time.
English/native Wi-Fi FTP remain primary, FL2/FL3 deferred. The previous goal turn
made progress by qualifying the invented authority envelope; this turn adds
semantic checks for two of its ordinary roles. The full pre-camera goal is active.

## What changed

The new `tools/dependency_input_semantics.py` validates `dependency_packet` and
`dependency_fixed` from the original bytes already bound by the four-document
invented envelope. It calls the retained pure `dependency_execution.bind_runtime_packet`
contract, rather than reimplementing its package/proof/root, config/cache, source
and review predicates. That binder imports authored helpers but performs no file,
native-loader or process operation. A synthetic runtime-shaped packet alone is
not evidence that runtime execution happened.

A separate caller-supplied prior anchor binds the original fixed-document digest,
prior dependency-review digest, operation ID and explicit dependency-alias to
envelope-source-role mapping. Its original-byte hash is supplied outside the
four-document chain. The map must match the dependency policy alias roster,
select distinct existing envelope roles, and pass the retained source-byte checks.
The full 44-role envelope remains separately bound. No production alias map is
inferred from the invented two-alias fixture; the final source/import closure and
checked-loader ownership still require review.

The packet is inside the candidate. Making its review field reference the current
outer review would create a hash cycle. All four current document hashes are
explicitly rejected as prior-review IDs. The prior anchor is separate from that
graph. Both external digests remain caller anchors: these functions cannot prove
reviewer identity, human consent, that expectations were independently selected,
or that the claimed prior review preceded execution. A fully rebound set with new
caller anchors can remain self-consistent without becoming authoritative.

Original packet/fixed file hashes, original config/cache UTF-8 text hashes and
canonical expectation/package object hashes are separately named. Reformatting
fixed JSON refuses under the old original-byte anchor; an explicitly changed
caller anchor can accept the new bytes while retaining the same object hash.
Source substitutions and changed fixed policy/package/root expectations refuse,
including after the surrounding envelope is rebound. Package proof mismatches,
config operation mismatches, wrong source maps and injected packet inputs refuse.

Operation correspondence here is prior-anchor ID to dependency expectation/config
only. The existing candidate has no operation/session field; current candidate
context binding remains unresolved. Interpreter strings/argv in that envelope
are still supplied metadata, not verified startup, exact runtime identity or
bootstrap/source correspondence.

The result lists two checked roles and **twelve pending ordinary roles**. It never
claims current basis/prerequisite/role/qualification/activity semantics. The
existing historical-index receipt checks remain unchanged. Declared cache/package
equality is not fresh descriptor collection or evidence of actual installed
bytes. All freshness, producer authentication, interpreter, actual-input,
execution, feature, recovery and device-write flags remain false. No protected
buffers are API inputs; no actual activation record, firmware/constants/cache
inspection, dependency activation, upstream execution, download/upload or camera
operation occurred. Direct CLI and runtime API refuse.

## Exact commands and results

Interpreter: CPython 3.13.12, Windows AMD64,
`C:/ProgramData/miniconda3/python.exe`.

- `git status --short --branch`: clean initial `codex/ra003-authority-grammar`, exit0.
- Two initial `rg` calls used Windows wildcard path arguments (and one nonexistent public GDT path), exiting1. Explicit existing authored paths and later `-g` selection corrected the read-only searches; no files changed or actual inputs opened.
- `git switch -c codex/ra003-dependency-input-semantics`: exit0.
- `New-Item -ItemType Directory -Path private/sessions/20261019-RA-003-dependency-input-semantics -ErrorAction Stop`: success, exclusive session folder.
- `C:/ProgramData/miniconda3/python.exe -B -m unittest discover -s tests -p test_dependency_input_semantics.py -v`: initial15/15passed, exit0, 2.336s.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-dependency-input-semantics/qualify.py`: intermediate63/63passed, zero errors/failures/skips, exit0, 3.143089s; 63public source/test/packet pins stable.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_input_semantics.py`; `Write-Output "dependency_semantics_cli_native_exit=$LASTEXITCODE"`: native exit2, no module output.
- `New-Item -ItemType Directory -Path private/sessions/20261019-RA-003-dependency-input-semantics/final -ErrorAction Stop`; `Copy-Item -LiteralPath private/sessions/20261019-RA-003-dependency-input-semantics/qualify.py -Destination private/sessions/20261019-RA-003-dependency-input-semantics/final/qualify.py -ErrorAction Stop`: success, fresh final outputs.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-dependency-input-semantics/final/qualify.py`: **66/66passed**, zero failures/errors/skips, exit**0**, **3.956437s**. **63** public source/test/packet hashes stable. Composition21new+45retained(22authority+14scope+9outer contract). No loaded Cryptodome aliases at completion. Only invented inputs/inert source strings; no installed backend or cipher execution. Historical full suites not rerun.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-dependency-input-semantics/record.py`: final pin/result verification, exclusive backups, synchronized public/private notes/state.
- `git diff --check`; `git diff --cached --check`: whitespace/content staging review, no device effects.

Final raw log SHA-256: `f09b72fbae84e02c2b206e8192e5148aca5ea41754f1aef7e24208779e276e40`.
The source reviewer accepted the initial narrowly scoped implementation and
recommended additional negative/boundary cases. Those were added before the final
qualification; all initial/final evidence is retained. Source review does not
authorize any act or prove the actual observation. No test threshold changed.
Reviewer `gate_review` also accepted the final test delta and saved evidence,
independently matching all 63 pins, the raw log digest and 66 passing outcomes.
The reviewer performed no execution or actual-input access.

## Files, remaining work and next package

Changed public files: new module, `tests/test_dependency_input_semantics.py`, this
report, `research/STATE.json`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md` and
`docs/FEATURE_PROGRESS.md`. Private scripts, raw logs/results and source-review
receipts remain ignored; private session and per-feature progress notes updated
with exclusive backups. Source lock, migration packet, frozen predecessors and
all historical full-suite evidence unchanged. No requested feature, recovery or
device-write gate passed.

The remaining twelve ordinary roles, full operational host/child authority and
source mapping, exact startup/context, activity-specific rights/trust decision,
fresh collection and protected continuation remain unqualified. Exact body/build,
English resources/restriction consumers, native FTP backend/direct Wi-Fi behavior,
independent backups and practical recovery remain unresolved. No owner fact needs
to be requested for this invented source-only package.

Next single package: **RA-003: implement and independently review basis, source-manifest and prerequisite cross-validation against the existing ordinary role-planning and pure GDT preflight contracts, using invented records and authored checked-buffer sources. Bind the nine-role basis, protected source/constants identity labels and current role/import plan; preserve the two-role dependency checks and explicitly track the other pending ordinary roles. Qualify stale/rebound/mismatched metadata refusal. Keep runtime disabled; no actual activation records, dependency activation, firmware/constants/native payload reads or camera.**
