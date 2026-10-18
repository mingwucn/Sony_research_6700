# RA-003: bounded FDAT identification and source-only extractor audit

Date: 2026-10-18. Branch: `codex/ra003-fdat-identification`.
Basis: `e1bc6f995ad3014a8c5b821700288573c2182e86`; initial tree clean.

## Result and scope

The already acquired official mainland 2.00 package was read once locally using
the authored standard-library reader. Whole-file SHA-256 and the five framing
spans agree with acquisition and the preceding inventory. At most **4,096 FDAT
prefix bytes** were retained in memory and classified after full framing/hash
checks. Actual result: **unknown / unsupported_opaque**, exit **0**, empty stderr,
**1.486305 seconds**. No prefix contents were output or saved. The outer operation
label `signature_only` is not a successful signature match.

Package identity remains 1,024,017,848 bytes, SHA-256:

```text
d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c
```

The original size, modification time and read-only attribute were unchanged.
The FDAT span remains package FILE offset 156, length 1,024,017,680 bytes,
end-exclusive 1,024,017,836. These are observed package offsets, not target
addresses. This run interpreted a bounded prefix; the preceding directory-only
run's no-payload-interpretation statement remains historical. Unknown does not
establish encryption, compression, a cipher/key choice or absent functionality.

The [act/source audit](../FDAT_EXTRACTOR_AUDIT.md) extends the recorded narrow
ordinary-local-study assessment to in-memory signature identification. No new
terms acceptance, firmware request, private upload or external inquiry occurred.
It does not clear all later decryption, component copying or disassembly, or
decide accepted-contract enforceability. No owner question is pending for the
ordinary read completed here; the earlier rights answer remains No / unknown.

## Extractor lead and reuse rights

An open, unmerged [upstream PR #52](https://github.com/ma1co/fwtool.py/pull/52)
reports ILCE-6700 among tested models. It gives no matching 2.00/mainland/hash
evidence. The fork head is pinned to
`3955d7890fc38daf942bb52827599bfe35de4a14` in
[sources.lock.json](../../references/sources.lock.json). Upstream baseline
`cdba742b73eed5981480c326aeb30033aabf0223` is a distinct revision.

Seven source-text files and three public metadata records were obtained through
ten single GETs, each HTTP 200, with no redirects or retries. Exact URLs, byte
hashes and response identities are recorded privately. Source blobs match the
fixed commit/tree. Original three repository pins are unchanged. No separate cryptographic
key/constant files, firmware assets or runtime dependencies were fetched; source was not
imported, built, installed or executed. Some existing PMCA objects were unavailable
with lazy fetch disabled; no complete-tree absence claim follows.

The source defines decoded UDTRFIRM magic and a 512-byte header. The actual prefix
did not match any supported signature. The audit records missing extent/overlap/
model checks, short-header handling, a FilePart seek defect, incomplete block-size
and malformed-input handling and unauthenticated omitted-trailer semantics.
Direct use is not accepted as a trusted extractor. Reviewed code has MIT text;
this grants no proprietary Sony firmware rights. No implementation or keys were
integrated, and no project-wide licence was selected.

Evidence: upstream text/author claim **source-report**; parser hazards and scoped
assessment **static-inference**; authored tests and actual local classification
**offline-tested**. No device or independently reproduced decoder evidence exists.

## Exact commands and observed tests

PowerShell **7.6.5**, CPython **3.13.12**, executable
`C:\ProgramData\miniconda3\python.exe`; commands run from repository root:

```powershell
git status --short --branch
git log -1 --format="%H %s"
git switch -c codex/ra003-fdat-identification
python -B -X utf8 -m unittest tests.test_fdat_probe -v
python -B -X utf8 private/sessions/20261018-RA-003-fdat-identification/run-tests.py
python -B -X utf8 private/sessions/20261018-RA-003-fdat-identification/run-fdat-probe.py
python -B -X utf8 private/sessions/20261018-RA-003-fdat-identification/update-notes.py
```

Branch creation and all listed Python commands exited **0**. Independent focused
tests: **19 total, 19 passed**, no skips, unittest **0.071 seconds**. The root full
suite ran once through `run-tests.py`, invoking exactly:

```powershell
python -B -X utf8 -m unittest discover -s tests -v
```

**198 total, 195 passed, three skipped**, no failures/errors, exit **0**. Unittest
**19.030 seconds**; wrapper **19.515032 seconds**. Skips: POSIX fork inheritance
on Windows and actual symlink creation for the inventory and UFU reader. Tests
use synthetic data, including boundary capture, decoy chunks, duplicate/empty/
absent FDAT, strict opt-in, delayed classification after EOF/hash, short reads,
file preservation and output privacy. Prior hosted CI/fresh-export qualification
does not cover these new changes; no camera or real FTP-server coverage follows.

The journaled wrapper checked fresh full-suite results and exact tested code
hashes before the one real pass. Its actual private argv used the interpreter
above and this public command template:

```text
python -B -X utf8 tools/ufu_inventory.py --input ACTUAL_PRIVATE_PATH --expect-sha256 d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c --expect-bytes 1024017848 --probe-fdat
```

The placeholder protects private storage paths. Exact argv, journals, tool/input
lineage, stderr and result JSON remain local and ignored. The original payload
was not copied, decrypted, decompressed, disassembled or executed. Source-only
HTTP reads used immutable raw-source URLs under the pinned fork revision; their
complete request list and metadata are in the private source audit.

## Reviewed changes and verification

Changed public files: `README.md`, `docs/ARTIFACT_INTAKE.md`, `docs/BACKLOG.md`,
`docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`,
`references/sources.lock.json`, `research/MAINLAND_FIRMWARE_SOURCE.md`,
`research/STATE.json`, `research/FDAT_EXTRACTOR_AUDIT.md`, this report,
`tools/artifact_probe.py`, `tools/ufu_inventory.py`, `tests/test_fdat_probe.py`.
Private progress/intake notes were updated from four preserved snapshots.
Instructions, master plan, validation thresholds, host-lab lock and UNVERIFIED
profile are unchanged. The source lock intentionally adds only the reviewed
candidate entry, with original fields/pins preserved.

```powershell
python -B -X utf8 private/sessions/20261018-RA-003-fdat-identification/verify-notes.py
git -c core.safecrlf=false diff --check
git -c core.safecrlf=false add -- README.md docs/ARTIFACT_INTAKE.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md references/sources.lock.json research/MAINLAND_FIRMWARE_SOURCE.md research/STATE.json research/FDAT_EXTRACTOR_AUDIT.md research/sessions/20261018-RA-003-fdat-identification.md tools/artifact_probe.py tools/ufu_inventory.py tests/test_fdat_probe.py
git -c core.safecrlf=false diff --cached --check
git diff --cached --name-only
git -c core.safecrlf=false diff --cached
git commit -m "feat: identify bounded FDAT prefix and pin extractor audit"
git status --short --branch
```

Local evidence verification passed **38 check groups**, seven tracked JSON parses
and 121 local Markdown link checks, exit **0**, without another payload read.
The exact reviewed-index/commit receipt is recorded privately and reported with
the completed session. No push or new hosted CI occurred.

English and native Wi-Fi FTP stay primary and unvalidated. FL2/FL3 remains
deferred, calibrated custom still looks later, bridge optional **HOST-ASSISTED**.
RA-003 remains partial: bounded prefix identification is a negative result, not
a decoded component inventory. Exact-body/build/region correspondence, the
specific decoding/copying basis and bounded decoder design remain unresolved.
Verified rollback/recovery and independent current-state backups are not
established; no device-write gate passed.

Next single work package: **RA-003: establish an act-specific FDAT decoding basis
and bounded decoder design before real decryption or component copying**.

Camera commands: **none**. Device access/writes, driver changes, protection
bypass, component extraction/decompression/disassembly, firmware execution and
private uploads: **none**. No feature is marked supported.
