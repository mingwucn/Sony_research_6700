# RA-003: bounded decoding assessment and synthetic header validation

Date: 2026-10-18. Branch: `codex/ra003-decoding-design`.
Basis: `40e0218766246f6a3292fa7c89912d8bdae01a69`; initial tree clean.

## Result

The [bounded decoding plan](../FDAT_DECODING_PLAN.md) documents a usable narrow
statutory research rationale for private in-memory format study. It records
accepted-contract interaction separately and does not impose separate Sony
permission as the only basis. The next task is concrete implementation/public-
constant provenance review and bounded trial preparation. No country/purpose or
ordinary-read question is repeated. Full component copying and modification are
not declared cleared.

A new authored pure standard-library
[decoded-header validator](../../tools/fdat_header.py) checks an exact 512-byte
header, CRC32 and every declared firmware/filesystem extent against a supplied
decoded length. It scans all 28 slots, distinguishes zero-sized P sentinels from
nonempty spans, refuses ambiguous U slots, and rejects out-of-bounds/overlapping
nonempty extents. Unknown count/padding semantics stay unverified. The accepted
subset is explicit host policy, not a Sony specification or alpha6700 profile.

Only synthetic decoded headers were supplied. No real payload was opened,
decrypted, copied or interpreted in this session. The previously recorded opaque
FDAT result remains unchanged; neither a cipher nor key profile was selected.
The function has no CLI, file, cryptography, network, execution or device API.
It reports decoded-FDAT file offsets and integer field codes, with no package-
to-runtime address translation, model/build identity or feature support inference.
Header CRC is not payload integrity or signature authentication.

The source audit also identified a critical future boundary: a four-byte block
envelope precedes the logical header, so that header crosses the candidate's
first cipher region. Size arithmetic fits one candidate shape but identifies
neither algorithm nor key. A real header trial cannot establish full decoded
length; measured full-stream validation is required before extent validation or
selected component copying. No upstream implementation/constants were fetched,
imported, installed or executed here. Existing immutable source pins are unchanged.

Evidence: refreshed primary law/terms and pinned source text **source-report**;
scoped research interpretation, format/design audit **static-inference**;
authored synthetic tests **offline-tested**. No new actual-input or device
evidence is claimed.

## Source refresh and limits

The root MOJ page read timed out; no retry was made, and the official CAC mirror
was read instead. [Regulations Articles 6/16/17](https://www.cac.gov.cn/2013-02/08/c_12648744.htm),
[Copyright Law Articles 24/49–51/61](https://www.nsfc.gov.cn/p1/2871/2872/69475.html)
and [Sony agreement §§1/3/4/7](https://service.sony.com.cn/download/firm/00003046.html)
support the detailed assessment in the plan. No contract-enforceability ruling,
blanket research grant, new agreement acceptance or firmware request occurred.
Public documents and already captured pinned source text were read only.

## Exact commands and results

PowerShell **7.6.5**; CPython **3.13.12**, executable
`C:\ProgramData\miniconda3\python.exe`. Repository-root commands:

```powershell
git status --short --branch
git log -1 --format="%H %s"
git switch -c codex/ra003-decoding-design
python -B -X utf8 -m unittest tests.test_fdat_header -v
python -B -X utf8 private/sessions/20261018-RA-003-decoding-design/run-tests.py
python -B -X utf8 private/sessions/20261018-RA-003-decoding-design/update-notes.py
```

The focused command ran twice during test development. First: **30 total,
29 passed, one failure**, no errors/skips, exit **1**, unittest **0.243 seconds**.
The test helper treated explicit None as its default fixture, so the intended
rejection case never reached the API. A unique default sentinel fixed the test
helper; no validator change was needed. Corrected focused result: **30/30 passed**,
exit **0**, unittest **0.235 seconds**. Both original outputs are retained privately.

The root then ran the full suite once through `run-tests.py`, invoking exactly:

```powershell
python -B -X utf8 -m unittest discover -s tests -v
```

**228 total, 225 passed, three skipped**, no failures/errors, exit **0**. Unittest
**17.867 seconds**; wrapper **18.351320 seconds**. The private wrapper initially
recorded zero passes because its line-end regex saw Windows CRLF. The terminal
suite passed; the pass count was corrected from that same intact log using
`splitlines()`, with the initial record and reconciliation retained. The suite
was not rerun. The reporting defect did not affect the test process.

Skips remain POSIX fork inheritance on Windows and actual symlink creation in
the inventory and UFU reader. New cases use literal offsets, a separate bitwise
IEEE CRC oracle, a standard known vector and a frozen synthetic header checksum.
They cover exact types/lengths, endian values, CRC span, all-slot traversal,
sentinels, EOF/header bounds, pairwise overlap, ambiguity, padding, count limits,
raw-field identity limits and silent/private metadata output. Synthetic payload
changes demonstrate that a successful header CRC says nothing about payload
integrity. Old real framing/prefix results remain historical evidence.

No new export or hosted CI qualification covers this code. Tests do not validate
decryption, a complete container, native English/FTP, real servers or hardware.
Initial setup/branch commands, final test wrapper and note synchronization exited
**0**. No actual firmware command ran in this session.

## Reviewed changes and remaining work

Changed public files: `tools/fdat_header.py`, `tests/test_fdat_header.py`,
`research/FDAT_DECODING_PLAN.md`, this report, `research/STATE.json`,
`research/MAINLAND_FIRMWARE_SOURCE.md`, `README.md`, `docs/ARTIFACT_INTAKE.md`,
`docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`,
`research/PRE_CAMERA_READINESS.md`, `research/TARGET_EVIDENCE_GAPS.md` and
`research/PRE_CAMERA_AUDIT.md`. The last three receive current acquisition/next-
step corrections while preserving their older audit snapshots.
Current private progress/intake notes were updated from four preserved snapshots.
Both source locks, AGENTS, master plan, validation thresholds and UNVERIFIED
profile remain unchanged. No private input, raw source, cryptographic constants
or firmware enters the index.

```powershell
python -B -X utf8 private/sessions/20261018-RA-003-decoding-design/verify-notes.py
git -c core.safecrlf=false diff --check
git -c core.safecrlf=false add -- README.md docs/ARTIFACT_INTAKE.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/MAINLAND_FIRMWARE_SOURCE.md research/STATE.json research/FDAT_DECODING_PLAN.md research/sessions/20261018-RA-003-decoding-design.md tools/fdat_header.py tests/test_fdat_header.py research/PRE_CAMERA_READINESS.md research/TARGET_EVIDENCE_GAPS.md research/PRE_CAMERA_AUDIT.md
git -c core.safecrlf=false diff --cached --check
git diff --cached --name-only
git -c core.safecrlf=false diff --cached
git commit -m "feat: validate decoded FDAT headers with scoped research plan"
git status --short --branch
```

Local record verification passed **32 consistency groups**, parsed all **seven
tracked JSON files** and resolved **156 local Markdown links**, exit **0**. It
reconciles preserved logs and notes without opening real payloads. Independent
reviews covered the format design, statutory assessment, synthetic cases and
progress consistency. The exact reviewed-index/commit receipt is retained
privately. No push, private upload, external inquiry, driver change, firmware
execution or camera command occurred.

RA-003 remains partial. The real input is opaque; minimal crypto dependency and
public-constant provenance, exact variant, bounded trial and later selected-copy
scope remain unresolved. Exact-body/build/resource correspondence and verified
rollback/recovery are absent. English and native Wi-Fi FTP remain primary and
unvalidated; FL2/FL3 deferred, calibrated custom looks later, bridge optional
**HOST-ASSISTED**. No feature or device-write gate passed.

Next single work package: **RA-003: audit and pin the minimal crypto dependency
and public-constant provenance for a bounded private header-decoding trial**.
Camera commands: **none**.
