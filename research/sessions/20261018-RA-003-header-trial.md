# RA-003 session: bounded private FDAT header trial

Date 2026-10-18. Branch `codex/ra003-header-trial`; parent
`1c952fd160cfeaa66bc239a5a23dd15c142cc9a0`. Risk R0 only. English and native Wi-Fi
FTP remain primary; FL2/FL3 deferred, calibrated custom looks later/separately gated,
optional bridge **HOST-ASSISTED**. Agent camera commands: **none**.

## Result

One predeclared `CXD90057_k8` hypothesis passed first-block envelope and logical
header checks, exit **0**, **6.517645s**. Actual original size/SHA-256,
fresh five-span framing, single-link/regular file identity and read-only metadata
stability passed. Retained 1,040 source bytes, decoded 1,024 physical bytes privately,
checked 512 logical header bytes. No raw bytes or working decoder enter Git.
No complete-stream length/hash, declared extent bounds, payload/signature integrity,
body correspondence, component formats, English mechanism, native FTP route or
recovery is established. No feature or device-write gate passed.

[Detailed audit](../FDAT_HEADER_TRIAL.md) records scope, tests, provenance and limits.

## Exact commands and observed results

Working directory: repository root. PowerShell 7.6.5 on Windows AMD64 build 26300.9711;
standard CPython 3.13.12 `C:\ProgramData\miniconda3\python.exe`. Crypto tests and
the real runner used its previously pinned private venv, `-I -B -X utf8`, with
pycryptodomex 3.24.1. No network/dependency install/download occurred this package.

```powershell
git status --short --branch
git log -1 --format='%H %s'
New-Item -ItemType Directory -Path 'private/sessions/20261018-RA-003-header-trial' -ErrorAction Stop
python -B -X utf8 private/sessions/20261018-RA-003-header-trial/bootstrap.py
python -B -X utf8 private/sessions/20261018-RA-003-header-trial/run-tests.py
python -B -X utf8 private/sessions/20261018-RA-003-header-trial/run-tests.py corrected
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 private/sessions/20261018-RA-003-header-trial/run-real.py
python -B -X utf8 private/sessions/20261018-RA-003-header-trial/update-notes.py
```

- Initial Git: clean `codex/ra003-crypto-provenance`, HEAD 1c952fd; exit 0. Initial
  inspections read AGENTS/README/HANDOFF/MASTER_PLAN/BACKLOG/OWNER_INTAKE/STATE and
  relevant source/plan/private records as ordinary local data.
- New private directory and bootstrap: exit 0; six byte-identical snapshots and
  87 tracked-file hashes preserved. Bootstrap ran exact `git switch -c codex/ra003-header-trial`.
- Initial tests: **37 total, 36 passed, one failure, zero skips**, exit 1,
  unittest 0.213s. Fixture expected a later framing error, but its shifted range
  already exceeded parent size. No firmware had been read. Original source/logs
  preserved; fixture corrected without weakening a policy. Independent review
  prompted a smaller-buffer read path, wrapper tests and stronger independent oracles.
- Corrected tests: **45/45 passed, zero skips**, exit 0, unittest 0.428s.
  Full argv, code hashes and terminal stdout/stderr are kept privately.
- One real runner: exit 0, elapsed 6.517645s; one hypothesis, no retry or
  fallback. All 351 installed wheel hashes checked before importing crypto. Pinned
  constants parsed as AST/data, never imported or executed. Real read starts only
  after exclusive/fsynced journal creation and successful qualification gates.
- Notes update: exit 0; public/private feature/state continuity synchronized.
- Read-only inspection helper error: `Get-Content -LiteralPath 'tools/fdat_probe.py'`
  returned exit 1 because that file does not exist. Located existing
  `tests/test_fdat_probe.py` and `tools/ufu_inventory.py`; no experiment or mutation
  resulted. This is separate from the initial synthetic fixture failure.

Repository executable code, standard-library tests, dependency/source locks and
target profile are unchanged. Prior standard-library suite 228 total / 225 passes / three
skips remains historical, not a rerun. The relevant newly executed qualification
is the 45 private synthetic cases and bounded actual trial. No hosted CI/export,
new host, firmware execution or hardware result is claimed.

## Method and limitations

Three independent read-only reviews covered source semantics, qualification and
scope. Final core/wrapper and one-shot runner were reviewed before the real read.
No upstream module or launcher ran. The common/candidate source values were
selected only from the pinned file and never published. AES Python/native code
ran in the dependency-isolated venv; that is not an OS sandbox.

The per-read limit is 1 MiB; managed-source-buffer budget 3 MiB, retained bytes 1,040.
It is not a total-process memory measurement/cap. Whole-source hash/capture uses
one fresh ordinary read-only descriptor, same-API before/after stamps and cross-API
identity checks. Trusted intermediate directories and observable changes remain
limits. No complete decoded stream or component file is saved.

Checks cover the whole first physical block; logical header `[4:516]` crosses cipher
regions. Header CRC/sum are consistency checks, not authentication. No encoded
block ordinal exists; only physical first/nonterminal consistency was checked.
Slot forms, declared spans and full decoded size remain unverified; the extent
validator was not called with a guessed size. The omitted 256 trailer bytes remain
uninterpreted/unauthenticated. Raw observations stay under ignored
`private/sessions/20261018-RA-003-header-trial/`.

Existing statutory research rationale is the narrow basis; accepted-contract
interaction and independent constants derivation remain unresolved. No distribution,
component extraction, decompression, disassembly or device scope follows.

## Changed files and prerequisites

Reviewed public scope (15 files):

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`
- `research/FDAT_HEADER_TRIAL.md`
- `research/FDAT_DECODING_PLAN.md`
- `research/FDAT_CRYPTO_PROVENANCE.md`
- `research/FDAT_EXTRACTOR_AUDIT.md`
- `research/MAINLAND_FIRMWARE_SOURCE.md`
- `research/PRE_CAMERA_AUDIT.md`
- `research/PRE_CAMERA_READINESS.md`
- `research/TARGET_EVIDENCE_GAPS.md`
- `research/sessions/20261018-RA-003-header-trial.md`

Ignored private records: session/feature JSON and both private progress/intake MDs;
exclusive session sources, before snapshots, failed/successful tests and actual
trial journals/results. No private file is staged. No input overwritten, evidence
deleted, push or history rewrite performed.

Outstanding: full-stream measurement/every-envelope validation, then declared
extent bounds; later selected-component necessity/terms/lineage and format study;
exact installed-body/build/SKU, English restriction/resources and native FTP
backend/invocation/media/network lifecycle. Verified rollback/recovery and all
device approvals remain absent. No additional owner fact is needed for the next
offline package.

Previous goal turn: **progress**. This turn adds actual header evidence; the full
pre-camera objective remains active, consecutive no-progress count 0.

Next single package: **RA-003: assess and document the necessary private full-stream format-study scope, implement and synthetically qualify bounded FDAT stream validation, then measure decoded length and SHA-256 through bounded memory without retaining decoded-stream or component files**.
Stream/hash through bounded memory, retain no decoded-stream/component files,
and keep the same single hypothesis. All-block/terminal success would support
only measured format metadata and declared extent checks, not feature support.


## Final evidence and publication verification

Command:

```powershell
python -B -X utf8 private/sessions/20261018-RA-003-header-trial/copyedit.py
python -B -X utf8 private/sessions/20261018-RA-003-header-trial/prepare-receipts.py
python -B -X utf8 private/sessions/20261018-RA-003-header-trial/verify-notes.py
python -B -X utf8 private/sessions/20261018-RA-003-header-trial/stage-review.py
git -c protocol.allow=never commit -m "docs: record bounded private FDAT header trial"
python -B -X utf8 private/sessions/20261018-RA-003-header-trial/finalize.py
python -B -X utf8 private/sessions/20261018-RA-003-header-trial/verify-notes.py
git status --short --branch
```

Observed pre-stage verification: **29 groups passed**, exit **0**, seven tracked
JSON files parsed and **207 local Markdown links** in the 15-file public scope
resolved. Receipts preserve each verification run without repeating the actual
firmware trial. Checks cover exact tested/actual implementation hashes, terminal
test logs, one-shot journal/result agreement, original evidence preservation,
public/private mirrors, next package, unchanged source locks/profile/thresholds,
unpromoted device/feature/recovery gates and private ignored/untracked paths.

Final index review explicitly selects the 15 paths above, checks staged content
against reviewed working-file hashes and saves the complete staged diff privately.
Commit and post-commit verification results are recorded in the private completion
receipt and returned session result. No push is part of these commands.
