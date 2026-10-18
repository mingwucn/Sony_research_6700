# RA-003 session: source-only image-header design

2026-10-18 UTC / 2026-10-19 Europe/Paris. Topic branch
`codex/ra003-image-header-design`, parent
`b030355a47e7fc42b4e2688a30e9bddd02de9bd9`. Host R0.
Native English and native Wi-Fi FTP first; FL2/FL3 deferred, calibrated custom
looks later and separately gated, optional bridge **HOST-ASSISTED**.
Camera commands: **none**. No firmware, raw member prefix or operational constant
was read by this package; no private input was uploaded.

## Result and limits

The [source/field/rights audit](../IMAGE_HEADER_DESIGN.md) covers four immutable
public AXFS/ext2/legacy-FAT/LZPT parser sources at the existing fwtool pin. Four
one-shot GETs returned HTTP **200**, **16,708 bytes total**, with exact sizes and
Git blob identities; per-file SHA-256 and journal remain private, public source
identities are in the [lock](../../references/sources.lock.json). No redirect,
retry, install, upstream import, parser/writer/launcher or firmware execution.
The web reader could not fetch the four GitHub pages; the separately scoped raw
source requests succeeded. This did not involve the firmware URL.

The published MIT notice accompanies private source copies; no per-file override
was found. LZPT's comments name kernel-header paths without pinned provenance or
licence; no kernel implementation was acquired or adopted. This source review
does not resolve accepted-contract interaction, constants derivation or proprietary
firmware copying/decompression/disassembly/distribution scope. No project-wide
licence or firmware permission is inferred from the source licence.

An independently authored standalone classifier inspects at most **4,096 bytes**
and known member extent, returning closed candidate metadata only. Its AXFS,
shared ext-family, conservative legacy-FAT and LZPT checks retain ambiguity and
leave filesystem validity, payload, ABI and authenticity false/unverified. Exact
field rules, intentionally unread fields and unsupported variants are documented
in the audit. Source-based field positions are member-relative file positions,
never target storage/runtime addresses.

**251/251 synthetic cases passed**, zero skipped, exit **0**, **1.271s**:
**202 retained + 25 authored candidate + 24 independent adversarial cases**.
All **23 baseline files** remain byte-identical. Independent source, rights,
field-layout and implementation reviews found no blocking issue. Qualification
pins **27 source/test files** plus four authored dependencies. The combined
suite reuses the existing isolated crypto environment for old synthetic tests;
new predicates use no crypto or third-party runtime.

The new classifier remains **unintegrated** and was not applied to actual data.
The five earlier unknown prefix outcomes and every prior actual experiment are
unchanged. No child image format, English resource/restriction, native FTP backend,
exact-body match, target profile, recovery path or device-write gate is established.

## Commands and observations

Repository-root working directory unless stated otherwise. Standard interpreter:
`C:\ProgramData\miniconda3\python.exe`, CPython **3.13.12**. Same recorded
Windows AMD64 host and PowerShell **7.6.5**; existing isolated pycryptodomex
**3.24.1** environment reused without installation.

```powershell
git status --short --branch
git log -1 --format="%H %s"
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-image-header-design/bootstrap.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-image-header-design/acquire-source.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-image-header-design/run-qualification.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-image-header-design/update-notes.py
```

- Initial Git clean at the parent above; required instructions, plans, state,
  backlog and intake reviewed. Previous goal turn: **progress**; consecutive
  no-progress count **0**. Bootstrap exit **0** (`fff2c2`): six exclusive original
  snapshots, **101 tracked-file hashes**, **23** verified unchanged foundation
  copies and `git switch -c codex/ra003-image-header-design`, exit **0**.
- Public-source acquisition exit **0** (`6a5c2e`), four exact pinned blobs and
  preserved MIT notice. Exclusive scope/journal precede requests. Sources were
  UTF-8 decoded and AST parsed as text; none executed. Three independent reviewers
  inspected source/metadata only. Source/helper Git identities checked again.
- Candidate focused suite from the new private session directory:
  `C:/ProgramData/miniconda3/python.exe -B -X utf8 -m unittest -v test_header_candidates`.
  Initial **25/25**, exit **0**, **0.007s** (`b44b11`); a wrong-signature fixture
  literal was refined to preserve its 16-byte field width, then final **25/25**,
  zero skipped, exit **0**, **0.009s** (`95242f`). No predicate changed after review.
- Independent focused command from the same directory:
  `C:/ProgramData/miniconda3/python.exe -B -X utf8 -m unittest -v test_header_review`.
  **24/24**, zero skipped, exit **0**, **0.003s** (`fa0201`). It covers maximal
  unsigned sizes, exact extent endpoints, no large exponent evaluation/allocation,
  endian assumptions, root-area rounding, unsupported variants, polyglot ordering,
  strict built-in types, sanitized errors, fresh outputs and no raw metadata.
- Combined qualification exit **0** (`e458e7`), **251/251**, zero skipped,
  unittest **1.271s**, wrapper **2.004216s**. Actual captured isolated argv:

  ```powershell
  & 'D:/LocalWork/Sony_research_6700/private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe' -I -B -X utf8 private/sessions/20261018-RA-003-image-header-design/test_design_all.py
  ```

  One exclusive `qualification-20261018T230417645913Z` attempt, complete stdout/
  stderr, before/after source identities, dependency hashes and terminal receipt.
  Root pinned it in `qualification-final.json`, exit **0** (`59224b`). Tests contain
  invented synthetic geometry, no firmware or operational constants.
- Notes update exit **0** (`3686dc`); public and private per-function mirrors,
  current session, append-preserved history and next package synchronized.

Metadata/source locating helpers had missing-filename, invalid-wildcard and an
overbroad baseline-glob assertion. These were corrected using exact known paths
and the explicit 23-file list; private review receipts retain observations.
One rights receipt contained an unsupported tool identifier; a second exclusive
receipt explicitly invalidates it. No actual experiment, input read or acquisition
was retried. The final source and qualification identities agree.

Public executable code/tests, existing upstream pins and target profiles are
unchanged. Historical public standard-library suite **228 total / 225 passed /
three skipped**, exit **0**, was not rerun; no fresh CI/export/other-host claim.
This package's newly authored 49 tests use the standard library. No measured
whole-process memory cap, secure buffer erasure or actual-input integration claim.

## Publication and remaining prerequisites

Evidence: **source-report**, **static-inference**, **offline-tested**. No device,
runtime, physical or independently reproduced camera result. Reviewed public
scope, **12 files**:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `references/sources.lock.json`
- `research/STATE.json`
- `research/MEMBER_PREFIX_AUDIT.md`
- `research/IMAGE_HEADER_DESIGN.md`
- `research/PRE_CAMERA_AUDIT.md`
- `research/PRE_CAMERA_READINESS.md`
- `research/sessions/20261018-RA-003-image-header-design.md`

Private changes: copied unchanged foundations, independently authored module/
tests, driver/qualification wrappers, public source copies and full MIT notice,
snapshots, source/rights/field/implementation reviews, logs/results/hash pins,
verification/staging/commit receipts and synchronized session/feature JSON plus
appended owner/progress notes. Firmware, keys, raw prefixes, member identities,
names/targets/positions/hashes and private analysis remain outside Git.

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-image-header-design/verify-notes.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-image-header-design/stage-review.py
git -c protocol.allow=never commit -m "docs: audit image header references and synthetic predicates"
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-image-header-design/finalize.py
git status --short --branch
```

Final publication checks use only source and metadata: exact source/qualification
pins, unchanged previous evidence/gates, private/public mirrors and histories,
JSON/local links, privacy, exact reviewed paths/blobs and whitespace. All **91**
out-of-scope tracked files remained unchanged. Explicit staging and a private
completion receipt preserve commit and clean status. No push or history rewrite.

Final metadata verification passed, exit **0** (`eaf1fb`): **28 groups**, **seven
tracked JSON files**, **253 local Markdown links**, **91 unchanged tracked files**.
Independent publication review also passed, exit **0** (`687638`), checking all
12 public files, exact qualification/source pins, seven prior evidence blocks,
private mirrors and the absence of 372 private member/link/hash values. Its one
wording correction distinguishes passing `header_only` results from refused or
unsupported leads; no predicate, test or historical outcome changed.

Before an expanded actual predicate runs, a new reviewed coordinator must reconcile
all five earlier prefix hashes/classifications, exact member selection and fresh
complete source/stream/header/span/original-prefix/whole-directory lineage.
Then qualify and freeze the complete runner and journal a single experiment.
No new owner fact is needed for that bounded offline package. Actual image
contents, English restriction/resources, native FTP/backend lifecycle, exact-body
correspondence, backup coverage, independent storage copies and verified rollback/
recovery remain unresolved. The official update package is not a body backup.

Next single package: **RA-003: implement and qualify an all-prefix reconciliation gate, then run one frozen expanded-header comparison on the same five members with full prior lineage**.
The full pre-camera goal remains active; this turn made progress, no-progress
count **0**. No feature support or device-write gate passed.
