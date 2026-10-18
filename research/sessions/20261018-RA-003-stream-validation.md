# RA-003 session: bounded-memory FDAT stream validation

2026-10-18. Topic branch `codex/ra003-stream-validation`, parent
`84e750de41f208d7e0ad6c21c869ca0d9483aeb1`. Host-side R0 only. English and native
Wi-Fi FTP remain primary; FL2/FL3 deferred, calibrated custom looks later and
separately gated, optional bridge **HOST-ASSISTED**. Camera commands: **none**.

## Result

One predeclared hypothesis passed complete experimental stream checks, exit **0**,
**28.836450s**, one pipeline, no retry/fallback. Both predeclared parent passes
matched **1,024,017,848 bytes** and SHA-256
`d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c`.
Fresh framing, encountered IV, same-descriptor/source observations and original
read-only attribute checks passed.

All **1,000,017 physical blocks** passed envelope sums and exact terminal-position
checks with continuous CBC state. Logical decoded length: **1,020,017,152 bytes**;
SHA-256 `e48b05235ddba0d8098fa4d71dd88d85ffe4e5ab440581003c6c3b4d5a813373`.
Final payload 832 bytes; no empty blocks or short nonterminal blocks observed.
Header hash agrees with the previous bounded trial.

Only after all source/stream checks did the existing pure header validator
receive that measured length. Declared decoded-FDAT file spans fit without overlap:
header `[0,512)`, U slot `[512,1253888)`, firmware `[1253888,1020017152)`;
P slot is an empty sentinel at 512. Firmware ends at measured EOF. These are
declared file offsets, never target/storage/runtime addresses. Child formats and
slot-count semantics remain unvalidated.

The [scope and detailed result](../FDAT_STREAM_VALIDATION.md) distinguish format
consistency from authentication, installed-body correspondence and feature support.
No decoded stream or component file was retained. No upstream launcher, firmware,
camera command, decompressor or disassembler ran. No feature or device-write gate passed.

## Exact commands and observed results

Repository-root working directory. PowerShell **7.6.5**, Windows AMD64 build
26300.9711; CPython **3.13.12**, `C:\ProgramData\miniconda3\python.exe`.
Crypto qualification and the actual runner used the existing isolated private
venv with `-I -B -X utf8`, pycryptodomex **3.24.1**. No network request, download,
dependency installation, hosted CI or clean export occurred in this package.

```powershell
git status --short --branch
git log -1 --format='%H %s'
New-Item -ItemType Directory -Path 'private/sessions/20261018-RA-003-stream-validation' -ErrorAction Stop
python -B -X utf8 private/sessions/20261018-RA-003-stream-validation/bootstrap.py
python -B -X utf8 private/sessions/20261018-RA-003-stream-validation/bootstrap.py
python -B -X utf8 private/sessions/20261018-RA-003-stream-validation/run-tests.py
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 private/sessions/20261018-RA-003-stream-validation/run-real.py
python -B -X utf8 private/sessions/20261018-RA-003-stream-validation/update-notes.py
```

- Initial Git inspection: clean `codex/ra003-header-trial` at the parent above,
  exit 0. Read repository instructions, plans, backlog, intake, public/private
  state and relevant prior source/test records as ordinary host files.
- Created the new private session directory without replacing existing evidence.
  Recorded the exact before-read scope before any full-stream decoding.
- First bootstrap invocation: **exit 1**. Its clean-tree guard rejected the new
  scope note created immediately before it. It stopped before snapshots, branch
  creation or firmware I/O. Preserved the original helper/error and corrected
  the guard to allow exactly that new scope path at the known parent.
- Second bootstrap invocation: **exit 0**, six byte-identical before snapshots
  and 89 tracked-file hashes preserved. It ran
  `git switch -c codex/ra003-stream-validation`, exit 0. This helper correction
  is separate from the actual experiment; the real pipeline was never retried.
- New synthetic qualification: **45/45 passed, zero skipped**, exit **0**,
  unittest **0.415s**, wrapper **1.047502s**. No firmware/operational constants
  loaded. Full argv, source hashes and terminal stdout/stderr are private.
- Actual runner: **exit 0**, **28.836450s**, one hypothesis/pipeline, two
  predeclared reads on one fresh descriptor. Exclusive/fsynced journal preceded
  source I/O. Both complete parent hashes matched. Seven provisional progress
  entries and one final result are preserved; no progress entry implied acceptance.
- All **351 installed wheel artifact hashes** matched the pinned wheel before
  crypto import. The pinned constants source was checked as AST/data only;
  operational values were not executed as source, displayed or published.
- Notes update: **exit 0**, public/private state and feature progress synchronized.

The relevant new qualification is the 45 private stream cases. Public executable
code/tests, locks, target profiles and thresholds are unchanged. The previous
standard-library suite remains historical: **228 total, 225 passed, three skipped**,
exit 0. It was not rerun. Private synthetic tests use the pinned crypto dependency;
they are separate from the standard-library suite.

## Method, review and limitations

The complete ciphertext stream was decoded through bounded memory. One ECB
operation handles the first physical 512 bytes; one continuous CBC state handles
the rest. Payload hashing excludes block envelopes and padding. The reader checks
every block's sum, capacity and terminal position; zero/odd later lengths are
allowed. The encountered IV must equal the preliminary captured IV. The entire
parent, including other chunks and the uninterpreted 256-byte trailer, is hashed
again during actual decoding.

Source reads are at most **1 MiB**, crypto batches **64 KiB**, accumulated logical
header **512 bytes**, managed source/crypto buffer design budget **4 MiB**. This
is not a total-process memory measurement/cap or an OS sandbox. Python/native
crypto code ran; upstream fwtool and firmware code did not. Trusted intermediate
directories and observable before/after file checks are not an atomic snapshot.

Synthetic cases exercise independently computed CRC/payload digest, cipher-call
continuity, 131 blocks across multiple batches, late corruption, zero/odd payloads,
short reads, parent framing/trailer changes, same-size between-pass mutation, IV
mutation, append, hardlink refusal, measured EOF+1, overlaps and nested flags.
Progress-callback delivery was observed during the real run; the synthetic cases
do not reach its 131072-block threshold. No claim of independent real hash
recomputation or another host/body follows.

Three independent read-only reviews covered pinned source semantics, scope and
qualified implementation/runner. A later metadata review confirmed journal/result
agreement, length arithmetic and spans without reading firmware or constants.
The pipeline records decoding true; the nested pure validator correctly records
its own decoding false. Caller-supplied size at that API is now a measured value.

The existing narrow statutory format-study rationale remains the documented basis.
Accepted-contract interaction and independent constants derivation are unresolved.
This does not clear later component copying, decompression, disassembly,
distribution, modification or device activity. Checksums/CRC/hashes establish
consistency and identity, not authentication/signatures, complete container
semantics, build/ABI/body equivalence, English/FTP support or recoverability.

## Changed files and unresolved prerequisites

Reviewed public scope, 16 files:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`
- `research/FDAT_STREAM_VALIDATION.md`
- `research/FDAT_HEADER_TRIAL.md`
- `research/FDAT_DECODING_PLAN.md`
- `research/FDAT_CRYPTO_PROVENANCE.md`
- `research/FDAT_EXTRACTOR_AUDIT.md`
- `research/MAINLAND_FIRMWARE_SOURCE.md`
- `research/PRE_CAMERA_AUDIT.md`
- `research/PRE_CAMERA_READINESS.md`
- `research/TARGET_EVIDENCE_GAPS.md`
- `research/sessions/20261018-RA-003-stream-validation.md`

Ignored private changes: session/feature JSON, private intake/progress Markdown,
new authored reader/tests/runner, before snapshots, test logs and actual
journal/result, review/verification/index/commit receipts. No private file or
third-party content is staged. No source input or earlier evidence overwritten,
no push or history rewrite.

Still needed: selected-component necessity/terms/retention/lineage and format
identification; matching resources and narrow English restriction mechanism;
native FTP binary/applet/ABI/invocation/media/network/lifecycle evidence. Exact
installed-body/build/SKU, current health/setup and verified rollback/recovery
remain absent. No extra owner fact is needed for the next offline package.
The full pre-camera goal remains active; this turn adds actual format evidence,
consecutive no-progress count 0.

Next single work package: **RA-003: document the necessary private selected-component scope, then synthetically qualify and run bounded in-memory identification of the declared U-slot and firmware extent prefixes, retaining lineage metadata only**.
Predeclare at most 4,096 logical bytes per nonempty extent, clipped to its bounds;
no raw-prefix files, decompression, disassembly or automatic parser/key fallback.
Preserve parent/stream hashes, labelled decoded-file spans, inspected lengths,
probe identity and classifier evidence. A match is a candidate, not component
validation or an English/FTP finding. Unknown stays unknown.


## Publication verification

The first metadata verifier returned exit 1 because it incorrectly required
README to repeat the entire next-package sentence. The corrected check requires
README's current-result link and retains exact next-package agreement in detailed
notes. Its original source/error are preserved. An inline PowerShell command to
prepare those receipts also returned exit 1 at shell parsing, before Python or
file I/O; the saved `prepare-receipts.py` replaces it. Neither involved a firmware
read or experiment retry. Independent review also corrected two stale backlog
statements about full-stream measurement and the global next package.
The first stage-helper invocation returned exit 1 before changing the index:
its broad receipt glob selected the helper-error JSON instead of a timestamped
passed receipt. The glob now selects timestamped receipts only; the error and
original line are preserved. This did not repeat any firmware operation.

Final commands:

```powershell
python -B -X utf8 private/sessions/20261018-RA-003-stream-validation/prepare-receipts.py
python -B -X utf8 private/sessions/20261018-RA-003-stream-validation/verify-notes.py
python -B -X utf8 private/sessions/20261018-RA-003-stream-validation/stage-review.py
git -c protocol.allow=never commit -m "docs: record measured private FDAT stream validation"
python -B -X utf8 private/sessions/20261018-RA-003-stream-validation/finalize.py
git status --short --branch
```

Each verification receipt is written exclusively with a timestamp. It checks
tested/actual code hashes and logs, pinned before-read scope, one-shot journal,
both source hashes/framing, measured-length arithmetic, declared extents, nested
flags, public/private mirrors, preserved prior results/owner facts, unpassed gates,
out-of-scope file hashes, JSON, local links, whitespace and the explicit 16-path
publication scope. It does not repeat actual firmware decoding.

The stage helper records working-file hashes and normalized Git blobs before
adding only the 16 named paths, then compares the actual index and saves its
full diff privately. Commit/post-commit verification and clean-tree results are
recorded in the private completion receipt and returned session result. No push.
