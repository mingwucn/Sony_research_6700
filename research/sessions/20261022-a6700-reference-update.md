# Updated a6700 reference review — 2026-10-22

Scope: R0 public-source acquisition and partial static review only. Evidence:
**source-report**, **static-inference**, and **offline-tested** integrity checks.
No upstream code was executed. Camera commands: **none**. No feature supported,
recovery proved, or device-write gate passed.

## Pin and acquisition

Reviewed [xyzhangxin/sony-a6700-powerful at
ac1cd0db5d0210292be1cee292d15034a222ae64](https://github.com/xyzhangxin/sony-a6700-powerful/tree/ac1cd0db5d0210292be1cee292d15034a222ae64),
observed at 2026-10-22T16:29:23.902695Z. Previous pin:
`c8e2aa100cfb02523d06cc6fc767d25a63cf943d`.
The recursive tree grew from 51 entries / 39 blobs to 195 entries / 160 blobs:
**122 added, 10 changed, 1 removed, 27 unchanged blobs**. Directory entries are
excluded from those delta counts. Updated upstream AGENTS text was not adopted.

Two authored collectors made 29 public metadata/text requests in total. Four
core documents plus 22 selected text files were saved privately, with byte
length, Git blob SHA-1 and SHA-256 verification against the pinned tree. Eight
Python sources were AST-parsed only. The public JSON catalog was parsed as data;
its patch addresses/bytes were not adopted or republished. No release ZIP,
native binary, firmware, protocol-constant module or private input was fetched.
Release metadata and pinned source are separate evidence: package contents,
signing, hashes and source-to-binary correspondence were not independently verified.
A moving raw-main browser response was stale; conclusions use the pinned tree
and verified pinned texts, not that response.

Selected review: application README/NOTICE/third-party notices; user, ordinary
USB root and write guides; FEATURES, BACKUP-RESTORE, VALIDATION, PROVENANCE,
FEATURE-SELECTION and ARCHITECTURE; catalog, planner, operations, backup,
device_profile, USB backend, two test sources and the feature catalog. This is
not a complete audit of the expanded codebase, native writer, service protocol,
desktop controller or release package. Upstream tests were read, not run.

## Findings that change our previous assessment

| Goal or prerequisite | New evidence | Remaining boundary |
|---|---|---|
| Native Wi-Fi FTP | Public application source and per-feature recipes now exist. The earlier implementation-unpublished finding is superseded. FTP can be selected independently. | Exact mainland build/ABI, native UI/config/media/task/network/credential/lifecycle chain and owner-body compatibility unverified. |
| FTP behavior | Author reports RAW+JPEG upload and transfer on reconnecting to a home network. Catalog changes 89 App bytes and 151 WBI bytes; FTP has no CP edit. | Source-report only. No accepted independent camera-origin Wi-Fi transfer, complete file equality/security evidence or automatic lifecycle qualification. Cross-power-cycle queue remains incompletely tested; playback untransferred filtering excluded. |
| Native English | No English/language feature among the six published catalog features or reviewed feature documents. | Mainland English absence remains owner-reported; restriction policy and complete English resources remain unmapped. This bounded review is not proof no solution exists. |
| Host application | Release metadata publishes prerelease `v0.1.0-dev33`, 2026-10-22T02:26:08Z. Packaged application targets Apple Silicon / macOS 13+, a6700 2.00. | No Windows package established for this host. Source device lock uses `fcntl`; Windows physical operation is explicitly unverified. Main source pin is not established as the release tag/package's exact source. |
| Feature isolation | Four available features: FTP, shutter curtain, flexible exposure, electronic shutter sound. Pixel Shift and Dynamic Active disabled. | Pixel Shift was withdrawn after a reported boot anomaly; incomplete features and other feature combinations must not be enabled opportunistically. FL2/FL3 and calibrated still looks remain deferred. |
| Rollback | Developer sparse state container covers 260 fixed sectors / 133,120 bytes: 149 target sectors plus 111 guards. Selected managed fields can be restored conditionally. | Desktop backup/restore hidden; full firmware/partition backup, downgrade, stock restoration and failed-boot recovery unimplemented/unverified. Closing features is not full recovery. Owner rollback prerequisite remains unmet. |

Primary sources: [release](https://github.com/xyzhangxin/sony-a6700-powerful/releases/tag/v0.1.0-dev33),
[pinned feature selection](https://github.com/xyzhangxin/sony-a6700-powerful/blob/ac1cd0db5d0210292be1cee292d15034a222ae64/应用/docs/FEATURE-SELECTION.md),
[pinned backup limits](https://github.com/xyzhangxin/sony-a6700-powerful/blob/ac1cd0db5d0210292be1cee292d15034a222ae64/应用/docs/BACKUP-RESTORE.md),
[pinned validation](https://github.com/xyzhangxin/sony-a6700-powerful/blob/ac1cd0db5d0210292be1cee292d15034a222ae64/应用/docs/VALIDATION.md).
Release metadata lists four assets; none was downloaded. Its author reports
137 no-device checks and one dev33 physical read-only preflight. These are not
our test results. Dev33 write/close cycles, repeated reconnects and multiple
bodies remain unvalidated in the release statement. The validation document's
older “not published” statement is superseded by the later release metadata.

All six catalog `evidence` paths are absent from the pinned public tree, both
as root-relative and application-relative paths. Public summaries exist, but
the referenced underlying research records were not available in that tree;
therefore historical physical claims cannot be independently reproduced from
the catalog alone. PROVENANCE describes these paths as audit indexes rather
than runtime dependencies. They are not treated as missing runtime files.

## Source-level controls and limits

The reviewed planner checks equal-length known values, bounds, non-overlap,
normalized image hashes and selected fields. Device inspection instead checks
its sparse guards/unmanaged bytes and known fields; it is not a whole-firmware
identity proof. Unselected fields are preserved by the reviewed planning loop.
The operation sequence includes a shared host lock, durable local intent and
preimages before the writer, followed by an independently requested readback.
Exceptions after an attempted write lead to uncertain/review states. These
observations establish source structure, not tested hardware fault recovery.
Native masks, physical mappings, authentication, payload equivalence and the
complete desktop retry/session path still need their own review.

“Ordinary USB” does not mean ordinary identification: the described inspect and
dry-run paths still authenticate service access and upload/execute temporary
native maintenance code. That would require separate R2 consent; persistent
changes need the applicable R3/R4 decision and write/recovery gates. No device
command or approval is issued by this review. R5 remains outside scope.

The new application declares GPL-3.0-only for authored code and preserves MIT
PMCA / compatible SHA-1 attribution. Bundled runtime notices and source/
replacement descriptions improve provenance. Root inherited Pico material
still has unresolved unlicensed portions. Notices do not independently prove
every provenance claim, distribution compliance or Sony firmware-analysis
rights. Nothing was reused, integrated or relicensed here.

## Commands and results

Baseline: clean local `4905502`; topic branch
`codex/a6700-reference-update-20261022`. Interpreter:
`C:/ProgramData/miniconda3/python.exe`, CPython **3.13.12**, Windows AMD64.
These are authored host commands; the private session directory is ignored.

```powershell
git status --short --branch
git switch -c codex/a6700-reference-update-20261022
New-Item -ItemType Directory -Path private/sessions/20261022-a6700-reference-update -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-a6700-reference-review-w/check_reference.py -Destination private/sessions/20261022-a6700-reference-update/check_reference.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-a6700-reference-update/check_reference.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-a6700-reference-update/fetch_selected.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-a6700-reference-update/verify_review.py
git diff --check
```

Collectors and offline verification: **exit 0**. Integrity checks verified all
26 text blobs, eight ASTs, tree delta, feature availability, FTP byte counts,
missing evidence indexes and release metadata. No upstream behavioral tests or
camera tests ran. Verification receipt is exclusive-create and is not blindly
rerunnable into the same output. One exploratory metadata query used the wrong
feature key (`native_ftp`); its `KeyError` was corrected to `native_wifi_ftp` and
had no mutation or camera effect.

Progress synchronization and preservation checks:

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-a6700-reference-update/update_notes.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-a6700-reference-update/check_notes.py
git check-ignore private/sessions/20261022-a6700-reference-update/verification-result.json private/session-state.json private/feature-progress.json
git diff --check
git add -- docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md references/sources.lock.json research/PRE_CAMERA_GAP_AUDIT.md research/PRE_CAMERA_GAP_LEDGER.json research/STATE.json research/sessions/20261022-a6700-reference-update.md
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git commit -m "docs: review updated a6700 USB and FTP reference source"
git status --short --branch
```

Synchronization, consistency, ignore and whitespace checks: **exit 0**.
The consistency check compares retained data against exclusive private
before-images: old activity decisions, device flags, recovery gates, other
package requirements and deferred features are unchanged; current public and
private pin/next-step summaries agree. Only the eight named authored public
files are staged and committed; private evidence and fetched reference texts
remain ignored. Git's LF-to-CRLF normalization notices are informational.
No remote submission/push occurred. No full behavioral suite was rerun for
these documentation-only changes; integrity/preservation checks cover this
review's claims without executing third-party code.

Changed public files: this report, `references/sources.lock.json`,
`research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`,
`research/PRE_CAMERA_GAP_AUDIT.md`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`,
and `docs/FEATURE_PROGRESS.md`. Private session/feature notes were updated
with their exact previous bytes preserved in this session's ignored folder.

## Next single work package

**FT-101: bounded static audit of the newly public FTP-only device chain** at
this pin: profile/catalog/native-reader/writer/protocol bindings, exact-build
and regional applicability, managed/protected coverage and inverse/recovery
limits. Acquire only necessary ordinary source under applicable component
terms, never run it or contact the camera. Produce an explicit gap matrix
against our manual-then-automatic FTP acceptance requirements. Do not adopt
patch offsets, bypass guards or imply that author success qualifies this body.

This new source route advances host review independently of the old GDT
analysis route. Its five pending activity decisions, frozen manifests and
refusals remain unchanged. English stays a primary goal; this update supplies
no English mechanism. The optional host-assisted bridge remains separate.
