# RA-003 session: five selected member prefixes remain opaque

2026-10-18 UTC / 2026-10-19 Europe/Paris. Topic branch
`codex/ra003-member-prefix`, parent `e1f421f10da8d85ea20775f8a3abb774b8a302c5`.
Host R0 only. Native English and native Wi-Fi FTP first; FL2/FL3 deferred,
calibrated custom looks later and separately gated, optional bridge
**HOST-ASSISTED**. Camera commands: **none**.

## Observations and limits

One bounded experiment completed, script and host exit **0**, **32.470943s**,
one pipeline with two planned descriptor passes, no retry/fallback. Five regular
image-category candidates were selected from the prior accepted private directory
using names as leads only. All exact records and 132 exclusion rationales are
private. The selection covers the image-named category without arbitrarily
guessing which image owns English/FTP; it does not establish global minimality,
actual partition identity, resources or backend contents.

Each prefix was **4,096 bytes**, **20,480 bytes total**. All five returned
**unknown / unsupported_opaque** under the unchanged bounded classifier.
Its format coverage is limited; this is not proof of missing English resources,
missing FTP code, invalid child images or an impossible native implementation.
No prefix covered a complete member; the explicit complete-member-prefix count
is **0**. Raw prefix buffers were discarded; no raw accepted output or child files.

Fresh complete parent/logical-stream identities, header, declared spans, both
original component prefixes and the entire tar directory matched prior evidence.
All **1,000,017 physical blocks** checked; logical size **1,020,017,152 bytes**.
The private directory remains **137 members**, **139 headers**, zero extensions,
**80,182 compact JSON bytes**. Full member/extent hashes and tar padding/end/tail
checks were repeated in the single decoding pass. Only after exact whole-directory
equality could selected classification run. Original read-only source state remained
observably stable. Link targets were never normalized, resolved or followed.

The existing [opaque-link policy](../TAR_LINK_INVENTORY.md), earlier failed tar
trial and first-refusal diagnostic remain unchanged. No changed guard/threshold,
new key/parser fallback, strings search, decompression, disassembly, upstream or
firmware execution, camera contact or feature/write gate. No target support profile.

## Exact commands and results

Working directory: repository root. PowerShell **7.6.5**, Windows AMD64 build
26300.9711; standard CPython **3.13.12** at
`C:\ProgramData\miniconda3\python.exe`. Existing isolated venv/pinned
pycryptodomex **3.24.1** reused. No download, installation, agreement or private upload.

```powershell
git status --short --branch
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-member-prefix/bootstrap.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-member-prefix/prepare.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-member-prefix/prepare-runner.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-member-prefix/run-tests.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-member-prefix/seal-scope.py
& 'D:/LocalWork/Sony_research_6700/private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe' -I -B -X utf8 private/sessions/20261018-RA-003-member-prefix/run-real.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-member-prefix/record-host.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-member-prefix/update-notes.py
```

- Initial Git clean at the parent above. Required instructions/plans/state/intake
  read. Bootstrap exit **0**: six exclusive snapshots, **99 tracked-file hashes**,
  `git switch -c codex/ra003-member-prefix`, exit **0**, and **17 unchanged**
  foundation/test files copied with lineage receipt. Selection review was a separate
  source/metadata-only operation, exit **0**; no actual input read.
- Preparation wrappers exit **0**. Five exact accepted regular-member records,
  original result/directory identity and private selection-review identity pinned.
  Synthetic driver invokes only authored local tests in the existing isolated venv.
- Combined qualification **202/202 passed**, zero skipped, exit **0**,
  unittest **1.317s**, wrapper **2.113401s**: 171 retained cases plus 17 collector
  and 14 coordinator/pipeline cases. Nested legacy checks are not counted again.
  Exact argv, **23 source hashes**, four authored dependency hashes and full logs
  persisted. No actual firmware or operational constants in synthetic fixtures.
- Independent before-read source/scope/runner review passed. All 24 source/runner
  files parsed; exact selection and unchanged foundations checked. Seal exit **0**:
  exclusive scope, plan SHA-256, 23 qualified sources plus runner (**24**) and
  qualification-result hash frozen before source I/O.
- Actual host session **52023**, chunks `007459`, `8c4e64`, terminal `c20e95`;
  host exit **0**, script/result/journal exit **0**, **32.470943s**. Exclusive/fsynced
  journal precedes input I/O. **351 installed dependency hashes** checked, then one
  preliminary and one decoding complete-parent pass on the same descriptor.
  Ten journal rows; seven provisional progress rows and final result agree.
- Metadata-only host receipt and public/private notes update exit **0**. No actual
  source read repeated during documentation verification. Earlier evidence retained.

Focused commands from the new private session directory:

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 -m unittest test_member_prefix -v
& 'D:/LocalWork/Sony_research_6700/private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe' -B -X utf8 -m unittest -v test_member_acceptance test_member_pipeline
```

Final focused collector **17/17**, exit **0**, **0.106s**; coordinator/pipeline
**14/14**, zero skipped, exit **0**, **0.320s**. The isolated combined receipt is
the authoritative qualification. Cases cover strict selection/metadata types,
labels, indices, regular records, bounds/non-overlap, mutation isolation, chunk
edges, short members and truthful complete-coverage count, cap/single-use/cleanup,
closed classifier schema, exact fresh directory and changed full-payload hashes.
Synthetic encrypted UFU/CBC integration injects late envelope and parent-hash
failures after selected capture and tar end: no finish or classification reaches
acceptance. Post-finish/classification/schema or cleanup failures clear metadata.

Public executable code/tests, source locks and target profiles unchanged.
Historical standard-library suite **228 total / 225 passed / three skipped**,
exit **0**, was not rerun. No fresh CI/export or other-host result claimed.

## Prerequisites and publication scope

Evidence: **static-inference** and **offline-tested**. No device-readback, runtime,
physical or independently reproduced camera result. The **16 MiB** managed design
allowance includes additional prior/working/encoded metadata; compact bounds exclude
Python/native/pretty-print overhead. No measured/enforced whole-process memory cap,
secure erasure or atomic filesystem snapshot is claimed. Maximum raw member-prefix
retention is **32,768 bytes**; actual **20,480**. No member names become host paths.

Accepted-contract interaction, independent constants derivation and later member
copy/decompression/disassembly/distribution scope remain unresolved. Child image
format, AP/CP/resource ownership, exact body/build/SKU match, English restriction/
resource coverage, native FTP backend/ABI/invocation/media/network lifecycle and
verified rollback/recovery remain unproved. The official package is not a body
backup. No new owner fact is required for the next bounded offline diagnostic.

Reviewed public scope, **11 files**:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`
- `research/TAR_LINK_INVENTORY.md`
- `research/MEMBER_PREFIX_AUDIT.md`
- `research/PRE_CAMERA_AUDIT.md`
- `research/PRE_CAMERA_READINESS.md`
- `research/sessions/20261018-RA-003-member-prefix.md`

Ignored private changes: authored collector/coordinator/tests/runner, unchanged
foundations, snapshots, metadata selection/review/plan, frozen scope/hashes,
qualification logs, journal/result/host receipt, verification/staging/commit
receipts and synchronized session/feature JSON plus appended owner/progress notes.
Names, targets, member/prefix hashes and positions remain private. No firmware,
keys, raw payloads or private analysis files staged. No push or history rewrite.

Final publication commands:

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-member-prefix/verify-notes.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-member-prefix/stage-review.py
git -c protocol.allow=never commit -m "docs: record bounded member prefix observations"
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-member-prefix/finalize.py
git status --short --branch
```

Verification uses source/metadata only, including sealed identities, terminal and
prior lineage, private/public mirrors, preserved history/gates, JSON/links,
unchanged out-of-scope tracked files, privacy and whitespace. Explicit staging
compares the exact path list, working hashes and normalized Git blobs; staged
content remains reviewable. Private completion receipt records commit and clean
status. Full pre-camera goal remains active; previous/current turn progress,
consecutive no-progress count **0**.

Final metadata verification passed, exit **0**: **27 groups**, **seven tracked
JSON files**, **242 local Markdown links**, and **90 unchanged tracked files**.
Independent publication review also passed. Its first metadata-only mirror check
used an incorrect common field name; it was corrected to the established two
private schemas and passed. This did not read the firmware or retry the experiment.

Independent metadata/reference continuation review passed, exit **0**. The pinned
reference tree lists four additional parser categories absent from the current
classifier; their blobs were not in the earlier local fetched subset. Tree
membership is not source-content or format evidence. Inspect pinned source/specs
and reuse rights before implementing more predicates; do not infer encryption,
corruption or a specific child format from these unknown results.

Next single package: **RA-003: audit pinned image-format parser sources and reuse rights, then design and synthetically qualify bounded structural header predicates for the five opaque candidates before another actual read**.
