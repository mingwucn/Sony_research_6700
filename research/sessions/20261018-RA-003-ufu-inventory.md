# RA-003: scoped container inventory and parser audit

Date: 2026-10-18. Branch: `codex/ra003-ufu-inventory`.
Basis: `0a04be8494d087b7f886c0284e95b7805795a0a1`; initial tree clean.

## Result

The [act/parser audit](../UFU_CONTAINER_AUDIT.md) documents a narrow statutory
assessment for local directory metadata, distinct from component extraction,
decompression, disassembly, distribution and device operations. Sony terms and
the earlier owner rights answer remain recorded; no blanket clearance is claimed.
The current primary law and Sony agreement were re-read. No new firmware request,
terms acceptance, external inquiry or private upload occurred.

The pinned PMCA locator was inspected as Git object text only. It is unsuitable
as a trusted extractor because it returns the first FDAT without bounds/full-file
checks. No upstream code was imported, copied, installed or executed. A new
authored standard-library reader checks framing, limits, source size/hash and
observable file changes, with no content extraction or firmware execution.

The private actual inventory exited **0**, **1.617467 seconds**, with empty stderr.
Five chunks **DATV / PROV / UDID / FDAT / DEND** span the 1,024,017,848-byte input
under the reviewed framing interpretation. The one nonempty FDAT payload spans
package file offsets **156 through 1,024,017,836 exclusive**, length
**1,024,017,680 bytes**. These are observed FILE offsets, not target addresses.
Whole-file SHA-256 matches acquisition:

```text
d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c
```

No component contents were written or output. The original size, modification
time and read-only attribute remained unchanged. CRC/signature/terminal/order
semantics, encryption/compression, model/build identity and exact-body applicability
remain unverified. A complete framing scan does not validate the container.

Evidence: statutory/source text **source-report**; scoped interpretation and
reference hazards **static-inference**; authored synthetic tests and actual
directory result **offline-tested**. No device evidence exists.

## Commands and tests

PowerShell 7.6.5, CPython **3.13.12** at
`C:\ProgramData\miniconda3\python.exe`. Repository-root commands:

```powershell
git status --short --branch
git log -1 --format="%H %s"
git switch -c codex/ra003-ufu-inventory
```

Source-only reads used `GIT_NO_LAZY_FETCH=1`, `GIT_TERMINAL_PROMPT=0`:

```powershell
git -c protocol.allow=never -C external/pmca-reference show a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0:pmca/firmware/__init__.py
git -c protocol.allow=never -C external/pmca-reference show a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0:pmca/util/__init__.py
git -c protocol.allow=never -C external/pmca-reference show a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0:LICENSE.txt
python -B -X utf8 -m unittest tests.test_ufu_inventory -v
python -B -X utf8 -m unittest discover -s tests -v
python -B -X utf8 private/sessions/20261018-RA-003-ufu-inventory/run-inventory.py
```

Branch and source reads exited **0**. The exact source commands, blob identities
and file hashes are preserved privately. The independent test author ran the
focused module: **25 total, 24 passed, one skipped**, exit **0**, 0.097 seconds.
The root ran the full suite once: **179 total, 176 passed, three skipped**,
**exit 0**, unittest **21.475 seconds**, wrapper elapsed **22.066025 seconds**.
Skips: POSIX fork inheritance on Windows and real symlink creation in the old
inventory and new UFU reader. Prior hosted CI does not cover the new reader.

Coverage includes an independent literal byte/offset/hash oracle, big-endian
lengths, truncated magic/header/payload, out-of-file spans, unsupported trailing
bytes, empty/absent/duplicate FDAT, zero-size progress, count/read limits, expected
hash/size refusal, short reads, observable metadata/name changes, descriptor cleanup
and CLI privacy. All test inputs are synthetic. Existing host behaviour passed
within this local matrix; neither tests nor metadata prove native feature support.

The real wrapper requires that full-suite result, journals before reading, and
runs this authored command with the actual input path retained privately:

```text
python -B -X utf8 tools/ufu_inventory.py --input ACTUAL_PRIVATE_PATH --expect-sha256 d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c --expect-bytes 1024017848
```

The placeholder is explanatory, not a runnable acquisition command. Input bytes
are read only for whole-file hashing and eight-byte framing; raw payloads never
enter the report. Exact argv, code hash and original metadata checks stay private.

## Reviewed files and remaining work

Changed public files: `tools/ufu_inventory.py`, `tests/test_ufu_inventory.py`,
`research/UFU_CONTAINER_AUDIT.md`, this report, `research/STATE.json`,
`research/MAINLAND_FIRMWARE_SOURCE.md`, `docs/ARTIFACT_INTAKE.md`,
`docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md` and `README.md`.
Current private notes are updated from preserved snapshots; firmware, raw logs,
source captures and manifests remain ignored and unstaged. Reference locks,
UNVERIFIED profile, master plan and validation thresholds are unchanged.

```powershell
python -B -X utf8 private/sessions/20261018-RA-003-ufu-inventory/verify-notes.py
git -c core.safecrlf=false diff --check
git -c core.safecrlf=false add -- README.md docs/ARTIFACT_INTAKE.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/MAINLAND_FIRMWARE_SOURCE.md research/STATE.json research/UFU_CONTAINER_AUDIT.md research/sessions/20261018-RA-003-ufu-inventory.md tools/ufu_inventory.py tests/test_ufu_inventory.py
git -c core.safecrlf=false diff --cached --check
git diff --cached --name-only
git -c core.safecrlf=false diff --cached
git commit -m "feat: inventory bounded UFU package framing offline"
git status --short --branch
```

Local evidence verification passed **30 check groups**, seven tracked JSON parses
and 110 local Markdown link checks, **exit 0**. It checks existing logs/manifests
and metadata without another firmware read. Exact staged-content review, commit
identity and final tree status are retained in the private completion receipt and
accompanying response. Private files are excluded from the reviewed index.
No push or hosted qualification of the new reader occurred.

English/native FTP remain primary; no resource or native backend was extracted
or validated. FL2/FL3 and calibrated custom still looks remain deferred; the
HOST-ASSISTED bridge remains optional and separate. Recovery is unestablished.

Next single work package: **RA-003 bounded FDAT format identification and
applicable-extractor audit before component copying/decompression**. Actual
component formats, source/build correspondence, full proposed analysis scope
and exact-body applicability remain open. No guessed support entry is added.

Camera commands: **none**. Device access/writes, driver changes, protection bypass,
component extraction/decompression/disassembly, firmware execution and uploads:
**none**. No feature or device-write gate passed.
