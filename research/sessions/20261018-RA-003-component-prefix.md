# RA-003 session: bounded component-prefix identification

2026-10-18. Branch `codex/ra003-component-prefix`, parent
`e1f3c41827b58c1f13c5e136d2ea337d15ed8886`. Host-side R0 only. English and native
Wi-Fi FTP remain primary; FL2/FL3 deferred, custom looks later/separately gated,
optional bridge **HOST-ASSISTED**. Camera commands: **none**.

## Result

One experiment passed, exit **0**, **23.899888s**, one pipeline/two predeclared
full-parent hash passes, no retry/fallback. The U-slot prefix matches the reviewed
**SquashFS v4 little-endian header** predicates; the firmware prefix matches the
reviewed **ustar header** predicates. Both are **header_only candidates**:
`container_validated=false`, `abi_verified=false`. No directory/member contents,
English resources/restrictions, native FTP binary/invocation or body match is proved.

Exactly **4,096 logical bytes per selected extent**, **8,192 total**, were retained
transiently. Prefix hashes/declared spans and fixed classifier metadata are in the
[audit](../COMPONENT_PREFIX_AUDIT.md); they are not whole-component hashes.
No raw prefix, stream or child file was saved/output. No decompression,
disassembly, upstream/firmware execution or camera contact occurred.

Both complete parent hashes, all 1,000,017 envelope/terminal checks, fresh header
validation, source observations and prior lineage comparisons passed. Original
size **1,024,017,848**, SHA-256
`d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c`;
logical length **1,020,017,152**, SHA-256
`e48b05235ddba0d8098fa4d71dd88d85ffe4e5ab440581003c6c3b4d5a813373`.
Header SHA and declared decoded-file spans match the previous stream observation.
No target/runtime/storage mapping or accepted profile follows.

## Exact commands and results

Repository-root working directory, PowerShell **7.6.5**, Windows AMD64 build
26300.9711. Standard CPython **3.13.12**, `C:\ProgramData\miniconda3\python.exe`;
crypto tests/actual runner use the existing pinned isolated venv and
pycryptodomex **3.24.1**. No firmware download or dependency installation.

```powershell
git status --short --branch
git log -1 --format='%H %s'
python -B -X utf8 private/sessions/20261018-RA-003-component-prefix/bootstrap.py
python -B -X utf8 private/sessions/20261018-RA-003-component-prefix/prepare-core.py
python -B -X utf8 private/sessions/20261018-RA-003-component-prefix/run-tests.py
python -B -X utf8 private/sessions/20261018-RA-003-component-prefix/seal-scope.py
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 private/sessions/20261018-RA-003-component-prefix/run-real.py
python -B -X utf8 private/sessions/20261018-RA-003-component-prefix/update-notes.py
```

- Initial Git: clean `codex/ra003-stream-validation` at the parent above, exit 0.
  Instructions, plans, backlog, intake and current public/private evidence read.
- Bootstrap: exit 0; new private session, six exclusive byte-identical snapshots
  and **91 tracked-file hashes**. Exact branch command:
  `git switch -c codex/ra003-component-prefix`, exit 0.
- Core preparation: exit 0. Copied the pinned authored stream reader and unchanged
  45-case suite. Added an optional validated-payload observer and 5 MiB buffer
  design budget; prior implementation/evidence unchanged. Recorded exact edits.
- Combined qualification: **93/93 passed, zero skipped**, exit **0**, unittest
  **0.441s**, wrapper **0.863020s**. Includes 45 stream, seven observer, 24
  collector/acceptance and 17 classifier cases. Exact argv/source/dependency
  hashes and terminal stdout/stderr persisted privately. No firmware/constants used.
- Scope seal: exit 0, exact before-read scope copied/pinned before actual source I/O.
- Actual runner: exit **0**, **23.899888s**, one pipeline, two predeclared reads
  on one descriptor. Exclusive/fsynced journal precedes source I/O. All **351**
  installed wheel hashes verified; constants AST/data only, never source execution.
  Seven progress entries stay provisional; terminal journal equals result.
- Notes update: exit 0; public and private progress synchronized.

Auxiliary agent prechecks (tool outputs, no separate persistent logs):

```powershell
python -I -B -X utf8 private/sessions/20261018-RA-003-component-prefix/test_prefix.py
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B -X utf8 private/sessions/20261018-RA-003-component-prefix/test_prefix.py
python -B -X utf8 private/sessions/20261018-RA-003-component-prefix/test_classifier.py
```

Initial collector: 22 passed, exit 0, 0.052s; after two integration cases, 24
passed, exit 0, 0.233s. Classifier: 17 passed, exit 0, 0.005s. The persisted
combined 93-case receipt is authoritative for the final source identities.
No synthetic test or real experiment failed this package.

Public executable code/tests, source/dependency locks, target profiles and
thresholds are unchanged. Standard-library suite **228 total / 225 passed /
three skipped**, exit 0, remains historical, not rerun. No new CI/export/host
or camera qualification is claimed.

## Source review, controls and limits

Primary format sources and exact conservative predicates are linked in the
[audit](../COMPONENT_PREFIX_AUDIT.md). Fixed CPython v3.13.12 tar source GET:
HTTP 200, 114,407 bytes, SHA-256
`e741d0f405b82bdb99f3c9f3604add700d47a1a5ec819b237c1f488259e1f005`, matching
installed stdlib source. Read as source, never run as an upstream tool.
Some public-source lookups failed: Linux `super.c` browser HTTP 429, OpenGroup
pax HTTP 403, GNU tar manual HTTP 400/timeout; raw cramfs browser timeout had no
status. Three direct raw Linux host captures returned HTTPError without recorded
codes; no retries/files saved or raw-source hashes claimed. Fixed-version Linux
definitions/official documentation were successfully read through the browser.
No private input was uploaded and no external message/inquiry was sent.

Independent reviews covered observer changes, collector/classifier semantics,
source predicates, runner/qualification gates and final metadata. Classification
waited for complete source/stream/header/span equality. Tests cover logical
offset mapping across variable/zero/odd payloads, poisoned/sealed collectors,
bounded retention, malformed/unsupported headers, unsafe metadata and late
envelope failure after filled prefixes with the classifier uncalled.

The managed buffer design budget is **5 MiB** including 8,192 prefix bytes and
512 header bytes; source reads ≤1 MiB, crypto batches ≤64 KiB. This is not a
whole-process memory measurement/cap, secure erasure guarantee or OS sandbox.
Private Python/native crypto ran. Trusted directories and observable before/after
file checks are not atomic snapshots. Hashes/CRC/sums establish identity and
format consistency, not signatures, authenticity or body applicability.

The existing necessary private format-study rationale remains documented.
Accepted-contract interaction and independent constants derivation are unresolved.
No later component copying/decompression/disassembly/distribution/modification or
device work is cleared. No requested feature, rollback system or device-write
gate passed.

## Changed files and next package

Reviewed public scope, **11 files**:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`
- `research/COMPONENT_PREFIX_AUDIT.md`
- `research/FDAT_STREAM_VALIDATION.md`
- `research/PRE_CAMERA_AUDIT.md`
- `research/PRE_CAMERA_READINESS.md`
- `research/sessions/20261018-RA-003-component-prefix.md`

Ignored private changes: session/feature JSON, intake/progress Markdown, new
authored implementation/tests/runner, before snapshots, scope, logs, result and
verification/index/commit receipts. No private artifacts staged, prior evidence
overwritten, push or history rewrite.

Remaining prerequisites: supported tar directory framing/variants and child
lineage; later selected component format/copy/extractor scope; English resources
and restriction mechanism; FTP binary/applet/ABI/media/network/lifecycle route.
Exact-body/build/SKU, remaining health/setup and verified rollback/recovery remain
unproved. No new owner fact is needed for the next offline package.
Previous goal turn: progress. This turn supplies actual format leads; full
pre-camera goal stays active, consecutive no-progress count 0.

Next single package: **RA-003: document and qualify a bounded-memory, metadata-only tar-directory inventory of the candidate ustar firmware extent, then run it with full source/stream lineage checks and no child files**.
No member payload files, automatic decompression, parser/key fallback or camera
action. Directory structure must be observed before selecting a child copier.

Final publication commands:

```powershell
python -B -X utf8 private/sessions/20261018-RA-003-component-prefix/verify-notes.py
python -B -X utf8 private/sessions/20261018-RA-003-component-prefix/stage-review.py
git -c protocol.allow=never commit -m "docs: record bounded component format candidates"
python -B -X utf8 private/sessions/20261018-RA-003-component-prefix/finalize.py
git status --short --branch
```

Timestamped verification receipts cover implementation/log pins, preserved scope,
actual lineage/prefix metadata, unpromoted gates, public/private continuity,
unchanged out-of-scope files, JSON/links and whitespace. Explicit index review
compares the 11 named paths against working-file hashes and normalized Git blobs;
the full staged diff remains private. Commit/post-commit verification and clean
status are recorded in the private completion receipt and returned session result.
No actual decoding is repeated by these publication checks.
