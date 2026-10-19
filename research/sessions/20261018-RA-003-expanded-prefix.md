# RA-003 session: expanded-prefix trial refused; metadata preflight gap

2026-10-18 UTC / 2026-10-19 Europe/Paris. Topic branch
`codex/ra003-expanded-prefix`, parent `30251eb86dec6a5c851f4b211070cf3f7a60809b`.
Host R0 only. Native English and native Wi-Fi FTP first; FL2/FL3 deferred,
calibrated custom looks later and separately gated; optional bridge **HOST-ASSISTED**.
Camera commands: **none**. No feature or device-write gate passed.

## Observations and diagnosis

One frozen same-five expanded-header trial stopped **needs_review**, script exit **2**, host exit **1**, **38.945781s**.
Qualification **278/278 passed**, zero skipped, exit **0**, **2.001s**; 27 new cases plus 251 retained, all 27 foundation files unchanged.
Failure code **expanded_prefix_acceptance_failed**; no accepted expanded candidates, fresh directory or persisted stream-validation result.
Static source/metadata review finds float timing fields in prior summaries rejected by the new freezer; this is a sufficient blocker, not a logged precise runtime stage.
Observer cleanup reported no failures. No retry, fallback, changed threshold, child files or raw-prefix output.
Earlier five unknown classifications and all prior evidence remain unchanged. No decompression/disassembly, upstream/firmware execution, camera or feature/write gate.


The frozen runner reached its post-stream acceptance phase. The preliminary
complete-parent hash is journalled. Seven progress rows remained provisional;
the tentative cleanup-time cursor reaches **1,020,017,152 logical bytes**,
parser state **tail**, **139 physical headers**. These counters are not an
accepted fresh directory or final lineage result. Post-discard member count **0**
means cleared metadata, not an empty archive. No complete member coverage,
expanded format result, original-classification reconciliation or new directory
equality result is accepted from this trial.

Two independent source/metadata-only reviews identify a deterministic mismatch:
the new coordinator freezes the whole public prior stream/component-prefix
summaries using a primitive-tree validator that rejects floats. Those preserved
summaries include floating-point `synthetic_unittest_seconds` and
`real_elapsed_seconds`. The first such saved prior-stream field is sufficient to
refuse before the original acceptance gate or expanded callbacks. This is
**static-inference**; the fixed generic runtime diagnostic does not identify its
precise internal refusal stage, and the fresh measured object was not persisted.

The synthetic fixtures and before-read review missed the production summaries'
timing fields. Passing **278** synthetic cases did not establish coverage of that
actual metadata shape. This is a host integration/qualification gap, not evidence
about firmware format, English resources or native FTP feasibility. Preserve
the failed result and all **32** sealed source/runner hashes. No gate, threshold,
key or parser was changed after the failure; no actual retry or fallback.

Earlier accepted stream, component-prefix, directory and five original unknown
member-prefix observations remain intact. The earlier failed tar trial and link
diagnostic/policy remain intact too. No child files, raw prefix/decoded stream
files, TOC or offset following, strings search, decompression, disassembly,
upstream launchers, firmware execution, camera/USB/driver/service action or
target profile. No accepted candidate counts are published.

## Exact commands and results

Repository root; PowerShell **7.6.5**, Windows AMD64 build **26300.9711**.
Standard **CPython 3.13.12**, `C:\ProgramData\miniconda3\python.exe`.
Existing isolated private pycryptodomex **3.24.1** environment reused; no new
download, installation, agreement, private upload or external analysis service.

```powershell
git status --short --branch
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/bootstrap.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/prepare.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/run-qualification.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/seal-scope.py
& 'D:/LocalWork/Sony_research_6700/private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe' -I -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/run-real.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/record-refusal-host.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/update-refusal-notes.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/create-refusal-report.py
```

- Initial Git clean at the parent above; required instructions/plans/intake/state
  read. Bootstrap **exit 0** (`8138ed`): six exclusive snapshots, **103 tracked-file
  hashes**, `git switch -c codex/ra003-expanded-prefix`, **exit 0**; **27** prior
  qualified source/test files copied byte-identically. Preparation **exit 0** (`45decc`).
- Focused gate **21/21 passed**, **exit 0**, **0.385s** (`0b1b03`); final
  gate+encrypted-pipeline **27/27**, zero skips, **exit 0**, **0.770s** (`f43970`);
  independent review **27/27**, zero skips, **exit 0**, **0.792s** (`3dd2a5`).
  Focused argv, from this private session directory:

  ```powershell
  & 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 -m unittest -v test_expanded_gate
  & 'D:/LocalWork/Sony_research_6700/private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe' -B -X utf8 -m unittest -v test_expanded_gate test_expanded_pipeline
  ```

- Authoritative isolated combined qualification **278/278 passed**, zero skipped,
  **exit 0**, unittest **2.001s**, wrapper **2.951561s** (`8b23f2`).
  Inner argv uses that private interpreter with `-I -B -X utf8` and this
  session's `test_expanded_all.py`. **31 source/test hashes** and four authored
  dependency hashes recorded. No actual firmware or constants in fixtures.
- Cases cover strict types/schemas/caps, whole measured/directory equality,
  all-five preflight including last-row failure, original classifications,
  caller/callback mutation, ambiguous results, late encrypted envelope/parent
  failures and original/expanded schema/classifier/cleanup errors. Production
  summary timing floats were omitted: the later diagnosed coverage gap remains.
- Before-read review passed (`66238b`); seal **exit 0** (`774a85`), **32
  source/test/runner pins**, exact qualification, plans, reviews and scope frozen.
  Review corrected cleanup flag accumulation and a nested metadata-key assertion
  before the run. Two review-helper metadata assertions failed before writing
  their receipt (`66b4bd`, `bc2a15`), corrected without actual input access;
  private review preserves those incidents.
- Actual host session **63400**, chunks `dbd4ff`, `4d59b0`, `edc47d`, terminal
  `b3886e`: **script/result/journal exit 2**, **host-tool exit 1**,
  **38.945781s**. One pipeline, two planned same-descriptor passes; exclusive/fsynced
  journal preceded input I/O. **351 installed dependency hashes** checked. Ten
  journal rows / seven provisional progress rows, terminal result agrees.
- Metadata-only host receipt **exit 0** (`ddc17b`). Independent diagnosis used
  preserved JSON/source only: source review (`d1d3f2`, **exit 0**) and gate review
  in private receipts. No experiment replay or firmware/key/prefix reread.
- Refusal notes/report commands **exit 0**. Success-path documentation drafts
  were never executed and remain private; they do not describe this outcome.

Historical standard-library suite **228 total / 225 passed / three skipped**,
exit **0**, was not rerun. No fresh CI/export, other-host or camera result claimed.

## Prerequisites and publication

Evidence: **static-inference**, **offline-tested**. No device-readback, camera
runtime, physical or independently reproduced target result. Full child formats/
content, AP/CP ownership, English restrictions/resources and native FTP backend,
ABI, invocation and media/network lifecycle remain unresolved. Exact SKU/build/
body/package correspondence, modification/health history, approved access route,
two independent backups and verified rollback/recovery remain device prerequisites.

The existing narrow private format-study rationale is recorded. Accepted-contract
interaction and constants derivation remain unresolved; no new general permission
inferred. Later copying/decompression/disassembly/distribution needs its own
activity-specific assessment. The official package is not an exact-body backup.
No new owner fact is needed for the next metadata-only work package.

At most **32,768 unique selected bytes**, **65,536 combined selected raw bytes**
during overlapping retention; actual plan **20,480 unique / 40,960 combined**.
**20 MiB managed design allowance**, not a measured/enforced whole-process cap;
compact directory **2 MiB** bound excludes Python/native/pretty-JSON overhead.
Managed observer/capture stores cleared. Callback/exception frames can retain
references; no secure erasure or callback sandbox claim.

Reviewed public scope, **12 files**: README.md; docs/ARTIFACT_INTAKE.md,
BACKLOG.md, CODEX_HANDOFF.md, FEATURE_PROGRESS.md; research/STATE.json,
IMAGE_HEADER_DESIGN.md, MEMBER_PREFIX_AUDIT.md, EXPANDED_PREFIX_AUDIT.md,
PRE_CAMERA_AUDIT.md, PRE_CAMERA_READINESS.md and this report.
Source lock, public executable code/tests and target profiles unchanged.

Private changes: authored gate/tests/runner, foundation copies, snapshots,
plans/reviews/qualification pins, journal/result/host receipt, failure diagnosis,
verification/staging/commit receipts and synchronized private session/feature/owner
notes. Member names/positions/prefix hashes, keys and raw inputs remain ignored.
No firmware/private files staged; no push or history rewrite.

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/prepare-publication.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/verify-refusal.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/stage-review.py
git -c protocol.allow=never commit -m "docs: record refused expanded prefix trial"
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-expanded-prefix/finalize.py
git status --short --branch
```

Publication preparation **exit 0** (`59956d`), no staging then. Final verification
uses metadata/source only: frozen pins, refusal, preserved history, no promotion
of tentative counters, private/public mirrors, JSON/links/privacy, **93 unchanged
out-of-scope tracked files** and whitespace. Explicit staging binds the exact
reviewed path list, working hashes and normalized Git blobs. Private completion
records commit/clean status. Full pre-camera goal remains active; previous/current
turn progress, consecutive no-progress count **0**.

Final metadata verification passed, **exit 0** (`925054`, independent; `f1ab8b`,
root): **28 groups**, **seven tracked JSON files**, **270 local Markdown links**,
**93 unchanged tracked files**. No actual input read or trial repetition.

Next single work package: **RA-003: design and synthetically qualify exact prior-metadata preflight using preserved production summaries, resolving the timing-field schema mismatch before any new actual prefix read**.
