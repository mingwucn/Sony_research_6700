# RA-003 session: first tar path refusal diagnosed

2026-10-18 UTC / 2026-10-19 Europe/Paris. Branch
`codex/ra003-tar-path-diagnostic`, parent
`e323db4a98140b84f014605b39d60a73ae93fb2e`. Host R0 only. English and
native Wi-Fi FTP remain first; FL2/FL3 deferred, calibrated custom looks later
and separately gated, optional bridge **HOST-ASSISTED**. Camera commands: **none**.

## Result and limits

One newly scoped experiment completed, script and host exit **0**,
**28.299963s**, one pipeline, no retry/fallback. A **header-supplied link target**
triggered the unchanged **empty_or_parent_component** predicate. This combined
category does not distinguish an empty component from `..`; it does not prove
the archive invalid or the link valid. Detailed field/header hashes, lengths,
positions and header type remain private; no field text/raw bytes in the event.

The semantic tar parser was immediately discarded and permanently disabled.
Independent source/stream/prefix validation continued: all **1,000,017** physical
blocks checked, **1,020,017,152** logical bytes, fresh complete parent/logical-stream
identities, header, declared spans and both 4,096-byte prefixes agree with prior
evidence. Observable source state remained stable. Only then was one bounded
private diagnostic released. No accepted directory, members, tar-end/tail checks,
whole-tar-extent digest, child files, decompression or disassembly is claimed.

The earlier failed trial and its incomplete lineage remain unchanged. This
separately scoped experiment supplies the missing first-refusal evidence; it
does not convert the failed trial into a passing inventory or relax its guard.
No firmware execution, upstream launcher or camera contact.

## Exact principal commands and results

Repository-root working directory. PowerShell **7.6.5**, Windows AMD64 build
26300.9711; standard CPython **3.13.12**,
`C:\ProgramData\miniconda3\python.exe`. The isolated synthetic/actual runner uses
the existing pinned private venv and pycryptodomex **3.24.1**. No new download,
installation, agreement or private upload.

```powershell
git status --short --branch
python -B -X utf8 private/sessions/20261018-RA-003-tar-path-diagnostic/bootstrap.py
python -B -X utf8 private/sessions/20261018-RA-003-tar-path-diagnostic/run-tests.py
python -B -X utf8 private/sessions/20261018-RA-003-tar-path-diagnostic/seal-scope.py
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 private/sessions/20261018-RA-003-tar-path-diagnostic/run-real.py
python -B -X utf8 private/sessions/20261018-RA-003-tar-path-diagnostic/update-notes.py
python -B -X utf8 private/sessions/20261018-RA-003-tar-path-diagnostic/clarify-history.py
```

- Initial Git clean at the parent above. Required instructions/plans/state/intake
  read. Bootstrap exit **0**: six exclusive original snapshots, **95** tracked
  file hashes, `git switch -c codex/ra003-tar-path-diagnostic`, exit **0**.
  Its enclosing copy driver then exited **1** on a wrong state-key lookup,
  before any copies or firmware read. Correct key used in a separate follow-up;
  **12** byte-identical foundation/test copies and exclusive lineage receipt,
  exit **0**. The setup error is preserved privately; no experiment was started.
- Final combined qualification **171/171 passed**, zero skipped, exit **0**,
  unittest **0.916s**, wrapper **1.497115s**. This includes the unchanged 133 cases
  and 38 diagnostic/coordinator cases. One diagnostic case also reruns all 24
  original parser cases against the instrumented class; these are not added
  again to the reported 171. No firmware/operational constants in fixtures.
  Exact argv, **18** authored source hashes, four dependency hashes and full
  stdout/stderr logs persisted.
- Scope seal exit **0**: exclusive before-read scope, all 18 qualified source
  hashes plus reviewed runner (**19**), and qualification-result SHA-256 frozen
  before actual source I/O. Independent scope/guard/coordinator/runner review
  passed. The tar header fork's unaffected AST matches the original.
- Actual command: host session **76058**, chunks `dc131a`, `6f4077`, terminal
  `b8b1ef`, exit **0**; script/result/journal also exit **0**, **28.299963s**.
  Exclusive/fsynced journal precedes input I/O. **351** installed dependency
  hashes checked; one preliminary and one actual-decoding complete-parent pass
  on the same descriptor. Seven progress entries are provisional; the terminal
  result and ten-row journal agree. No automatic retry or parser/key fallback.
- Metadata-only host receipt and notes update exit **0**. Private/public feature
  progress synchronized; prior observations, device gates and owner facts retained.
  Review prompted a historical-tense clarification in all current feature mirrors,
  exit **0**, so the prior missing-diagnostic sentence cannot contradict the new result.
  No actual source read repeated during documentation verification.

Auxiliary focused commands, from the new private session directory:

```powershell
C:\ProgramData\miniconda3\python.exe -B -X utf8 -m unittest test_diagnostic_tar -v
& 'D:/LocalWork/Sony_research_6700/private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe' -B -X utf8 -m unittest -v test_path_diagnostic test_diagnostic_pipeline
```

Final focused runs: guard **16/16**, exit **0**, **0.079s**; coordinator/pipeline
**22/22**, exit **0**, **0.227s**. Earlier focused additions also passed. Their
tool observations remain distinct from the authoritative captured isolated
combined suite above. Independent reviewer reran guard cases successfully.

Public executable code/tests, locks, profiles and existing acceptance thresholds
are unchanged. Historical full standard-library suite **228 total / 225 passed /
three skipped**, exit **0**, was not rerun. No fresh CI/export or other-host result.

## Controls, evidence and remaining prerequisites

[Frozen scope and observed result](../TAR_PATH_DIAGNOSTIC.md) define a **2,048-byte**
fixed-schema event, exact typed refusal, unchanged guard order and immediate
semantic parser disablement. No member/link path is followed or materialized.
Only closed role/origin/predicate codes are published; no detailed event digests
or positions. The combined predicate's remaining ambiguity is preserved.

Synthetic cases cover all predicate classes/priorities and selected field
origins, exact schema/types/caps, malformed and duplicate events, non-path
errors, extent binding, callbacks after refusal, missing refusal, poisoned state,
cleanup failure and source/prefix/lineage mismatch. Actual synthetic CBC/UFU
integration injects late envelope and parent-hash failures after event capture;
both discard the event and invoke neither classifier nor tar finish. A complete
valid synthetic pipeline releases only the lineage-checked event.

Managed pipeline design budget remains **8 MiB**, not measured/capped total
Python/native memory or secure erasure. Observable file checks are not an atomic
filesystem snapshot. Evidence is **static-inference** and **offline-tested**;
no device-readback, runtime-observed, physical-tested or independently reproduced
camera result is implied.

Contract interaction, independent constants derivation and later component-copy/
decompression/disassembly/distribution scope remain unresolved. Exact body/build/
SKU correspondence, English resources/restriction mechanism, native FTP backend/
ABI/invocation/media/network/lifecycle and verified rollback/recovery remain
unproved. No new owner fact is needed for the next offline policy/inventory work.
No support entry, feature, authenticity, recovery or device-write gate passed.

## Changed files and next single package

Reviewed public scope, **11 files**:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`
- `research/TAR_DIRECTORY_AUDIT.md`
- `research/TAR_PATH_DIAGNOSTIC.md`
- `research/PRE_CAMERA_AUDIT.md`
- `research/PRE_CAMERA_READINESS.md`
- `research/sessions/20261018-RA-003-tar-path-diagnostic.md`

Ignored private changes: new session's authored diagnostic/coordinator/tests/
runner, byte-identical foundations, snapshots, frozen scope, qualification logs,
journal/result/host receipt, verification/staging/commit receipts, and current
session/feature JSON plus appended intake/progress Markdown. Earlier evidence
preserved. No private firmware, keys, payloads or detailed event staged; no push,
history rewrite or camera operation.

Next single package: **RA-003: review the observed path/link predicate, qualify an explicit metadata-only policy and run one bounded directory inventory with complete lineage and no child files**.

That package should distinguish lexical link-target metadata from extraction-path
safety, preserve member-path guards/caps, and never resolve/follow/materialize
links. Document any changed acceptance rule and why before its new experiment;
this diagnostic has changed none. Full pre-camera goal stays active; previous
turn and this turn both made progress, consecutive no-progress count **0**.

Final publication commands:

```powershell
python -B -X utf8 private/sessions/20261018-RA-003-tar-path-diagnostic/verify-notes.py
python -B -X utf8 private/sessions/20261018-RA-003-tar-path-diagnostic/stage-review.py
git -c protocol.allow=never commit -m "docs: record bounded tar link diagnostic"
python -B -X utf8 private/sessions/20261018-RA-003-tar-path-diagnostic/finalize.py
git status --short --branch
```

Publication verification reads metadata/source only. It checks frozen hashes,
terminal/source lineage, private/public mirrors, preserved prior evidence and
unpassed gates, JSON/links, unchanged out-of-scope files and whitespace. Explicit
staging compares only the named paths, working hashes and normalized Git blobs;
full staged diff remains private. Final commit, verification and clean status
are recorded in the private completion receipt.
