# RA-003: explicit historical-context preflight

2026-10-20; branch `codex/ra003-historical-context-repair-v6`, base `e7b07d0`.
Evidence: **static-inference**, **offline-tested**. Prior goal turn made reference
pin progress; it did not advance shared implementation. This turn qualifies a
versioned repair of two demonstrated host preflight defects. Goal remains active.
English/native Wi-Fi FTP first; FL2/FL3/custom looks deferred, bridge optional.

## Result and boundaries

The [versioned gate](../HISTORICAL_CONTEXT_PREFLIGHT.md) uses the reviewed exact
29-source ancestry map and an explicit hash-selected historical context. Whole
dependency-config bytes are pinned, including the historical operation ID; the
old dependency-profile pin omitted that field. Original seal/proof/root/session
are bound separately. The current candidate still must match the proposed act.
Neither the old config nor frozen evidence is rewritten.

The existing captured-source outer preflight now selects v6 only through an
explicit closed migration argument. Its current-candidate/current-request guard
is retained. Its v2 result is consistency-only. The v6 gate returns false
execution/feature/recovery/write flags and removes the child argv. The old v5
comparison entry and refusal behavior remain available. Inherited v5 record
schemas are compared, not promoted to new bootstrap qualification or authority.

AST conservation checks verify all **22 inherited functions** retain their
predicates and all **20 policy constants** are unchanged: the sole behavioral
delta supplies a validated historical context to `_source_cache`; one inherited
docstring's blank lines changed. The original v5 gate and separate ancestry
validator retain their exact hashes. No guessed namespace or basename fallback.

**137/137 focused standard-library tests passed**, zero failures/errors/skips,
exit **0**, **51.206s**; ten selected source/test pins stable. Composition:
**33 ported ancestry + 20 new context/full composition + 84 retained public**
cases. The new complete invented 27-input bundle reaches the real captured gate
and contract, without stubbing gate semantics. Tests cover wrong contexts,
changed raw sources, stale hashes, current decisions, original v1 refusal,
pending refusal and saved-result claim promotion. They are not protected runtime
or camera tests. No broad historical/full-repository suite rerun.

Actual ordinary metadata: the earlier **55-source/11-validator** pending review
still passes all **six** historical checks against **25** original historical
inputs. The new comparison reproduces the original namespace `contract` refusal
and `operation_binding` refusal, then validates **29** mapped sources and **47**
inert cached text receipts using separate context. Cached Python text is data
only. Original source buffers agree with the selected retained 29 copies.

No current accepted candidate/review/decision/seal or two activity inputs were
fabricated. A minimal in-memory comparison descriptor selects the already
recorded proposal operation; it is not an accepted act record. The incomplete
actual full bundle refuses `contract`. The actual all-five-pending proposal
refuses `observation_undecided` before migration, without supplied authority
records. The collector preserves the earlier saved-result semantics: recomputed
from original in-memory bytes, not crash-durable publication or independent
runtime attestation.

The **51-source operational / 46-role prepared rosters**, three historical
dependency null fields and all five activity decisions are unchanged. Production
preparation still calls the old retained-gate interface: its explicit migration,
bootstrap/source qualification and genuine activity decisions remain work. This
turn does not claim the protected operational path is ready or complete.

## Commands, attempts and review

All host commands ran in the project root with CPython **3.13.12**, Anaconda,
Windows AMD64. Exact isolated interpreter commands:

```powershell
git status --short --branch
git switch -c codex/ra003-historical-context-repair-v6
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-historical-context-v6/build.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-historical-context-v6/collect.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-historical-context-v6/collect-r2.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-historical-context-v6/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_historical_gate.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-historical-context-v6/record.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-historical-context-v6/check_publication.py
```

Builder **0**; original collector **1**; new collector revision 2 **0**;
qualification **0**; direct CLI deliberately **2**, empty stdout/stderr;
publication **0**, final publication consistency check **0**. That final check
confirms every selected historical/source pin remains stable, all requirement,
validation, risk and gate acceptance entries are unchanged, other work packages
are unchanged and old public/internal notes remain preserved. No input or
operational retry: collector revisions read
ordinary metadata into distinct exclusive output folders. Original failed source
and outputs are retained.

The original collector completed the six pending-review checks, then failed an
assertion comparing `str(GateError)` with a bare stage name. GateError prefixes
its message. Reviewer independently identified the same error. Revision 2
changes only its output directory and three structured refusal captures to
`.stage`; review confirmed the exact four changes. Acceptance predicates and
private inputs were unchanged.

Earlier exploratory synthetic command (standard input, `-I -S -B -X utf8 -`):
`unittest.defaultTestLoader.loadTestsFromNames(['test_dependency_historical_gate',
'test_dependency_observation_outer'])`, TextTestRunner verbosity 2, exited **0**,
**61/61**, **14.090s**. The first six-case composition run exited **1**, with
one pass, three failures and two errors: fixture resealing changed request hashes
but retained the prior synthetic expected runtime. Updating that fixture
expectation left the runtime guard intact; corrected run **6/6**, **0**, **6.360s**.
These exploratory outputs were tool-visible, not separately saved raw logs.
Final qualification retains the complete 137-case raw log, structured result,
ten pins, CLI receipt and AST-conservation receipt privately. Its loader inserts
only repository/tests paths, then runs these exact modules:

```text
test_dependency_historical_gate
test_dependency_historical_outer
test_dependency_observation_outer
test_dependency_observation_contract
test_dependency_pending_review
test_dependency_legacy_comparison
test_dependency_operational_preparation
```

Authorized local reviewer `/root/historical_context_review` inspected authored
source only, including permitted own predecessor sources. No blocking core
finding; corrected collector finding resolved. It separately ran **53/53**
migration cases, **6.577s**. It did not inspect selected private metadata or run
the collector. Core reviewed SHA-256 pins:

```text
tools/dependency_historical_gate.py
25663aadb151d0cf9fe4b287accda99a52153bd7b12895f5b233bdee4db44459
tools/dependency_observation_outer.py
6841937f053b86749b3d9c70a20333069acf5e3300afed879f47332ada230396
tests/dependency_historical_fixture.py
9c5e0f2e2202822f97050069dc02478270ca5d4923d8cb18a3773769a4a0de23
tests/test_dependency_historical_gate.py
d65c742b9d55e03c1daf700cfb21f4127ad23fc8ad8192f6dd53ec73ba2219ff
tests/test_dependency_historical_outer.py
a80958a1839f79a96eee122e4633d1964297d8a61a822079917358784332c5b9
collector revision 2
9ac4aeaff7d2995773db8376cac8b0a5ecc6c4416fa4a251954d48ecc348746d
```

## Publication and prerequisites

Changed implementation/test files: the two tools and three fixture/test files
listed above. Changed notes: this report, `research/HISTORICAL_CONTEXT_PREFLIGHT.md`,
`research/STATE.json`, `research/PRE_CAMERA_GAP_LEDGER.json`,
`research/PRE_CAMERA_GAP_AUDIT.md`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`,
`docs/FEATURE_PROGRESS.md`. Private session/function notes and before-images
updated; frozen originals and prior current summaries preserved. The ledger's
requirement/validation/gate acceptance entries are unchanged and incomplete.
Source lock remains unchanged this turn. Staging is restricted to reviewed paths.

```powershell
git diff --check
git add -- tools/dependency_historical_gate.py tools/dependency_observation_outer.py tests/dependency_historical_fixture.py tests/test_dependency_historical_gate.py tests/test_dependency_historical_outer.py research/HISTORICAL_CONTEXT_PREFLIGHT.md research/sessions/20261020-RA-003-historical-context-v6.md research/STATE.json research/PRE_CAMERA_GAP_LEDGER.json research/PRE_CAMERA_GAP_AUDIT.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m "fix: separate historical context in versioned observation preflight"
git status --short --branch
```

Camera commands: **none**. No new network/download/upload, upstream execution,
firmware/constants/native payload read, installed dependency activation,
driver/firmware change, feature support or recovery/device-write gate passed.
Owner rollback prerequisite remains unmet. English resources/policy and native
FTP backend remain unmapped. Actual activity-specific basis, exact body/build
identity and approved recovery/access observations remain prerequisites.

Next single package: **RA-003: integrate the explicit v6 historical-context
handoff into the existing production-preparation path, reviewing its source
roster and bootstrap qualification. Qualify the complete invented preparation
sequence and actual pending refusal without changing frozen originals, creating
actual allow records, clearing dependency nulls, activating installed dependencies,
reading protected inputs or contacting the camera.**
