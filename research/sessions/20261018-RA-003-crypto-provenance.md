# RA-003: pinned crypto and public-constant audit

Date 2026-10-18. Branch `codex/ra003-crypto-provenance`, clean basis
`acede7703fd0fde539047c1c4e8cf7861bbbf94e`. Previous goal turn: **progress**;
the committed decoding design and synthetic validator changed the next action.

## Results and evidence

The [crypto/provenance audit](../FDAT_CRYPTO_PROVENANCE.md) records a privately
acquired, size/hash-verified PyPI wheel, all hashed wheel RECORD entries, native
architecture, notices and isolated AES known-answer results. Eight authored
tests passed. A pinned public constants source was acquired privately and parsed
as data without import/execution or output of its values. Git blob/size/hash
agree with the fixed tree. No fwtool source, launcher or firmware was executed.

The earlier ILCE-6700 testing claim is supported by an author comment, now
captured with its exact permalink/body hash. Version/region/hash applicability
is still unverified. The source's initial k8 report supports one predeclared
experimental hypothesis, with no automatic fallback or target profile values.

Public metadata and source/licence/author statements are **source-report**;
format/provenance interpretation is **static-inference**; actual artifact checks
and authored AES cases are **offline-tested**. Neither a signature nor a
reproducible wheel build was verified. Native crypto code did run locally; camera
or fwtool execution did not. No real payload was opened or decoded this session.

## Exact commands and results

PowerShell 7.6.5; CPython 3.13.12, `C:\ProgramData\miniconda3\python.exe`.
Commands from the repository root:

```powershell
git status --short --branch
git log -1 --format="%H %s"
git switch -c codex/ra003-crypto-provenance
python -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/snapshot.py
python -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/capture-dependency.py
python -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/acquire-audit.py
python -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/capture-provenance.py
python -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/qualify-runtime.py
python -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/update-notes.py
```

All exited **0**. Private one-shot HTTP journals record metadata, wheel, public
source and history/comment requests; no redirect, retry or private upload.
No firmware was downloaded again. Raw source/comments/notices remain private.

The qualification wrapper ran these argv, with interpreter paths resolved to
the new private environment:

```powershell
python -B -X utf8 -m venv private/sessions/20261018-RA-003-crypto-provenance/crypto-env
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 -m pip --isolated install --no-index --no-deps --no-compile --disable-pip-version-check private/sessions/20261018-RA-003-crypto-provenance/pycryptodomex-3.24.1-cp37-abi3-win_amd64.whl
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/test-aes-runtime.py
```

Venv creation: exit 0, **11.987993 seconds**. Offline installation: exit 0,
**2.232966 seconds**. AES tests: **8 total/passed, zero skipped/failures/errors**,
exit **0**, unittest **0.093 seconds**, subprocess **0.570535 seconds**. Cases
cover pinned/import isolation, NIST AES-128 ECB/AES-256 CBC, chunk continuity,
fresh state, wrong-IV/reset negatives, portable AES and malformed input.
No operational constants were supplied to those tests.

Repository executable code/tests are unchanged. The prior standard-library
suite remains the recorded 228 total, 225 passed, three skipped, exit 0 on the
same code; it was not rerun merely for documentation/pin changes. No new hosted
CI, clean export/OS, full import/native-code audit or firmware applicability is
claimed. New JSON/link/pin/private-note consistency checks are recorded below.

## Publication and unresolved prerequisites

Changed public files (15): `README.md`, `docs/ARTIFACT_INTAKE.md`,
`docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`,
`references/sources.lock.json`, `research/STATE.json`,
`research/FDAT_CRYPTO_PROVENANCE.md`, `research/FDAT_DECODING_PLAN.md`,
`research/FDAT_EXTRACTOR_AUDIT.md`, `research/MAINLAND_FIRMWARE_SOURCE.md`,
`research/PRE_CAMERA_AUDIT.md`, `research/PRE_CAMERA_READINESS.md`,
`research/TARGET_EVIDENCE_GAPS.md` and this report. The final explicit staged
path list and exact index digest are retained privately. Four
earlier private note snapshots and protected-file hashes were preserved. No raw
wheel, constants, comments, firmware, credentials or decoding implementation is
published. Instructions, master plan, acceptance criteria and target profile
remain unchanged. Only reviewed paths are staged; no push.

Local record verification passed **29 consistency groups**, parsed all **seven
tracked JSON files** and resolved **181 local Markdown links**, exit **0**.
It checks preserved public-source/host-test evidence and notes without firmware
I/O. Independent reviews covered source provenance, crypto loading/operations
and current progress/gate consistency. Completion commands:

```powershell
python -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/prepare-receipts.py
python -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/verify-notes.py
python -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/stage-review.py
git -c core.safecrlf=false diff --cached --check
git diff --cached --name-only
git -c core.safecrlf=false diff --cached
git commit -m "docs: pin private FDAT crypto research prerequisites"
python -B -X utf8 private/sessions/20261018-RA-003-crypto-provenance/finalize.py
git status --short --branch
```

The staging helper refuses a nonempty initial index, stages the explicit 15
paths above and compares each index blob with its reviewed file. The private
commit receipt verifies parent, branch, exact changed paths, blobs and clean
tree; no private input is staged.

An earlier inline receipt-preparation command failed during Python parsing
(unterminated quoted string, exit **1**), before executing or changing files.
The saved `prepare-receipts.py` avoids nested shell quoting; the failure record
is retained privately. No acquisition or test was repeated as a result.

Crypto primitive qualification does not qualify a decoder. An authored bounded
trial implementation and independent malformed-envelope/header tests remain to
be completed before one actual read. Underlying constants derivation, accepted
contract interaction and exact-body/build correspondence remain unresolved;
their scope is distinguished from the documented narrow private-study basis.
English and native FTP remain primary and unvalidated, FL2/FL3 deferred, custom
looks later and the optional HOST-ASSISTED bridge separate. Verified rollback
and protected-state backup coverage remain prerequisites before future writes.

Next single package: **RA-003: implement, synthetically qualify and run one
bounded private FDAT header trial for the predeclared CXD90057_k8 hypothesis**.
Camera commands: **none**. No feature support or device-write gate passed.
