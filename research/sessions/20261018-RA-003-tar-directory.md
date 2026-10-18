# RA-003 session: metadata-only tar-directory trial refused

2026-10-18 UTC / 2026-10-19 Europe/Paris. Branch `codex/ra003-tar-directory`,
parent `1accd029cc900573199a320e924b64cb1a230af4`. Host R0 only. English and
native Wi-Fi FTP remain first; FL2/FL3 deferred, calibrated custom looks later
and separately gated, optional bridge **HOST-ASSISTED**. Camera commands: **none**.

## Actual result and its limits

One newly scoped experiment ended **needs_review**, script/result/journal exit
**2**, host-tool exit **1**, **28.603684s**, one pipeline, no retry/fallback.
The fixed **unsafe_path** guard refused a header during tentative observation.
The preliminary complete-parent SHA-256 passed; all **351** installed dependency
hashes and **133** qualified synthetic cases were recorded before decoding.

The actual decoding pass did not finish. No final actual-pass parent/logical-stream
hash, source after-stamp, fresh header/span/prefix lineage acceptance, tar end/tail
validation, accepted directory, child identity or whole-extent digest is claimed.
Earlier stream/prefix results remain unchanged with their original scope.

Tentative physical-header encounter counter **114** is not an accepted member
count. The recorded member count **0** follows parser discard and does not mean
an empty archive. Global cursor and extent bytes seen are different checkpoints
in the failing callback. No offending field role/value or exact predicate is
identified: the same guard checks member names and link targets. An absolute or
parent-relative link can be valid metadata, but that specific cause is unobserved.

Both observer cleanup checks reported no failure; no raw prefix/payload/decoded
stream/member file, decompression, disassembly, upstream/firmware execution or
camera contact. No accepted names or directory metadata survived the failure.
The original failed journal and implementation stay preserved; no threshold was
relaxed after the actual failure and no second read was attempted.

## Exact commands and results

Repository-root working directory. PowerShell **7.6.5**; Windows AMD64 build
26300.9711; standard CPython **3.13.12**,
`C:\ProgramData\miniconda3\python.exe`. Synthetic crypto/actual runner use the
existing pinned private isolated venv and pycryptodomex **3.24.1**. No download,
dependency installation, new agreement or private upload.

```powershell
git status --short --branch
git log -2 --oneline
python -B -X utf8 private/sessions/20261018-RA-003-tar-directory/bootstrap.py
python -B -X utf8 private/sessions/20261018-RA-003-tar-directory/run-tests.py
python -B -X utf8 private/sessions/20261018-RA-003-tar-directory/seal-scope.py
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 private/sessions/20261018-RA-003-tar-directory/run-real.py
python -B -X utf8 private/sessions/20261018-RA-003-tar-directory/update-notes.py
```

- Initial Git clean at the parent above; required instructions/plans/state/intake
  read. Bootstrap exit **0**: six exclusive original snapshots and **93** tracked
  file hashes; `git switch -c codex/ra003-tar-directory`, exit **0**.
- Seven authored foundation/test files copied unchanged from the pinned prefix
  session, with exclusive lineage receipt. New parser, acceptance/cleanup and tests
  remain private. Exact source hashes accompany qualification and actual journal.
- Combined suite **133/133 passed**, zero skipped, exit **0**, unittest **0.749s**,
  wrapper **1.606387s**: 93 unchanged foundation cases, 24 tar, 13 acceptance and
  three late-pipeline/cleanup cases. Exact argv, 13 source hashes, four dependency
  hashes and terminal logs persisted. No firmware or operational constants used.
- Scope seal exit **0**: exclusive before-read scope copied and hashed after
  qualification, before real source I/O. Independent source/runner reviews passed.
- Actual command: host execution session 90943, final chunk `419c26`, host-tool
  exit **1**; script terminal/result/journal exit **2**, **needs_review**,
  **28.603684s**. Preserve both exit observations. Exclusive/fsynced journal before
  source I/O; one preliminary hash completed, actual decoding pass stopped.
  Seven progress entries remain provisional; terminal journal equals result.
- Notes update exit **0**; public/private per-function progress and next package
  synchronized. No actual read repeated by publication checks.

Auxiliary agent commands, using the same pinned isolated venv:

```powershell
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 private/sessions/20261018-RA-003-tar-directory/test_tar_inventory.py
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 private/sessions/20261018-RA-003-tar-directory/test_acceptance.py
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 private/sessions/20261018-RA-003-tar-directory/test_pipeline.py
```

Parser first focused run: **23/23**, exit 0, 0.028s; final reviewed run **24/24**,
exit 0, 0.033s, both receipts/logs preserved. Initial acceptance-only 11 cases
passed, 0.041s. Adding independent stdlib-generated USTAR integration exposed a
seven-byte POSIX signature literal: **12 passes/one error of 13**, exit 1. The
implementation literal was corrected to the proper eight bytes; no acceptance
threshold relaxed. Initial failure was preserved as a tool-output transcription,
with its missing initial start time/raw byte-stream log explicitly recorded.
Corrected acceptance **13/13**, exit 0, 0.068s, persisted logs/receipt. Later shared
cleanup and late encoded-pipeline **3/3**, exit 0, 0.053s, tool output only. The
captured combined suite is authoritative for all final source identities.

Before the actual read, source review also corrected empty PAX extension/value
handling, nonregular PAX size overrides and failure diagnostics/cleanup. These
are implementation/review corrections before sealing; the actual `unsafe_path`
refusal predicate remains unchanged afterward.

Public executable modules/tests, source/dependency locks, target profiles and
existing thresholds are unchanged. Historical standard-library suite **228 total,
225 passed, three skipped**, exit 0, was not rerun. No new CI/export or host/camera
qualification is claimed.

## Review, controls and remaining prerequisites

The [before-read scope and source review](../TAR_DIRECTORY_AUDIT.md) records the
fixed USTAR/GNU/PAX subset, caps and strict end/padding policy. Pinned CPython
v3.13.12 source was inspected as text; independent stdlib tar writers generate
synthetic test fixtures only. Official GNU indexed format text was reviewed.
Current POSIX browser page returned **HTTP 403**; full text was not inspected.

Synthetic coverage includes member/header/payload/extent hashes; boundary/odd/zero
callbacks; safe names/link metadata; GNU/PAX variants; malformed/unsupported forms;
caps; truncation/padding/end/tail; poisoned/sealed state; and late encrypted-envelope
or actual-pass parent-hash failures after tar end with no finish/classification.
Independent review of the actual negative evidence found no accepted inventory.

Managed pipeline design budget **8 MiB**, source reads at most **1 MiB**, crypto
batches at most **64 KiB**, encoded directory metadata at most **2 MiB**. These are
not measured/capped whole-process memory or secure-erasure guarantees. Private
Python/native crypto ran; no upstream launcher or firmware code. Trusted paths
and observable checks are not atomic filesystem snapshots.

Contract interaction, independent constants derivation and later component-copy/
decompression/disassembly/distribution scope remain unresolved. Exact body/build/
SKU correspondence, English resources/restriction mechanism, native FTP backend/
ABI/invocation/media/network/lifecycle and verified rollback/recovery remain
unproved. No new owner fact is needed for the next offline diagnostic. No feature
support, target profile, authenticity, recovery or device-write gate passed.

## Changed files and next single package

Reviewed public scope, **11 files**:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`
- `research/COMPONENT_PREFIX_AUDIT.md`
- `research/TAR_DIRECTORY_AUDIT.md`
- `research/PRE_CAMERA_AUDIT.md`
- `research/PRE_CAMERA_READINESS.md`
- `research/sessions/20261018-RA-003-tar-directory.md`

Ignored private changes: new authored reader/acceptance/tests/runner, snapshots,
scope, logs, failed result/host receipt, verification/index/commit receipts and
session/feature JSON plus intake/progress Markdown. Prior evidence preserved;
no private firmware/keys/payloads/paths staged, push or history rewrite.

Next single package: **RA-003: qualify and run one bounded tar path/link diagnostic that records the first refusal category privately, completes source/stream lineage validation, and accepts no directory or child files**.

Preserve the rejection predicates and original failure. Capture at most one
bounded private record of field role/origin, closed predicate category, header
ordinal/type, labelled positions, byte length and hashes, without path text/raw
bytes. Stop semantic directory parsing after that rejection and continue only
the qualified source/stream/prefix checks; discard the diagnostic on any later
failure. No directory acceptance, rule relaxation or automatic retry. Full
pre-camera goal stays active; previous turn and this turn both made progress,
consecutive no-progress count **0**.

Final publication commands:

```powershell
python -B -X utf8 private/sessions/20261018-RA-003-tar-directory/verify-notes.py
python -B -X utf8 private/sessions/20261018-RA-003-tar-directory/stage-review.py
git -c protocol.allow=never commit -m "docs: record refused private tar directory trial"
python -B -X utf8 private/sessions/20261018-RA-003-tar-directory/finalize.py
git status --short --branch
```

Metadata-only verification checks original snapshots/scope, actual test/source
pins, terminal failure/journal/cleanup, preserved prior evidence and unpassed
gates, public/private continuity, JSON/links, out-of-scope files and whitespace.
Explicit staging compares all named paths, working hashes and normalized Git
blobs; full staged diff remains private. Actual commit, post-commit verification
and clean status are recorded in the private completion receipt.
