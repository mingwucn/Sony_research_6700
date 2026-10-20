# RA-003: unchanged legacy gate, complete invented bundle

2026-10-20. Branch `codex/ra003-legacy-positive`; base `bdf5e95`. Evidence: **static-inference**, **offline-tested**.

Result: [captured preflight and saved comparison](../OBSERVATION_LEGACY_QUALIFICATION.md) now accept a complete invented legacy bundle through unchanged gate SHA-256 `faa196abe6dbea4ef141deab810558f8f0e03fdda9bc0b9d9c4b6acda2f25172`. No gate interception or policy weakening in the new cases. Production code unchanged.

## Commands and results

```powershell
git status --short --branch
# clean at bdf5e95 on codex/a6700-reference-check-20261020-q
git switch -c codex/ra003-legacy-positive
# exit 0
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_observation_legacy'));raise SystemExit(not r.wasSuccessful())"
# First exploratory 12-case run: exit 1, failures=11/errors=5, 11.276s.
# Fixture's outside runtime expectation was stale after rebuilt request hash.
# Corrected fixture expectation and deliberately deep source-mismatch case;
# unchanged gate/predicates. Second run: 12/12 pass, 15.360s, exit 0.
# Added protected identity, other valid operation and cleanup uncertainty cases;
# stronger no-I/O guards. Third run: 15/15 pass, 17.969s, exit 0.
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-legacy-positive/qualify.py
# exit 0; 127/127, failures/errors/skips 0/0/0;
# 47.694s suite / 48.358876s wrapper; 146 stable source pins.
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-legacy-positive/record.py
# exit 0; existing notes backed up before additive updates.
```

Qualification runs seven named modules: new legacy cases, retained observation outer/contract, authority grammar, input semantics, operational scope and operational launcher. CPython 3.13.12 Anaconda Windows AMD64, optimize 0, isolated/no-site/no-bytecode/UTF-8 startup. Standard library only; no actual dependency or camera. Full exact subprocess argv and per-CLI commands/results retained in private final/result.json; raw stdout/stderr and final test snapshot retained exclusively. Five public CLIs (observation outer/contract, operational launcher/child/metadata) refuse with exit 2 and empty output.

stdout SHA-256 `0515d594b3d5848f045c860e593fe4a7887a85aeeea50a1bcf670f2fd3547f8a`; stderr SHA-256 `d1fbbcbf4d977cdda847be8eae27d2a800a5e23c2479a3c84265930e09c1185d`. Every prior 141 pin rechecked; additional fixture/repair/test/driver sources checked before and after. Historical broad/process suites not rerun. Existing suite's stub-positive cases remain; new positive gate cases are unintercepted. No actual legacy record or current activation record qualification.

Independent source reviewer accepted SHA-256 `eb3c2b52e79f5eb88b98bb42ddfa13e80b3d57cbb54b951bc1b7be41b4b6ac8f` after clarifying authored-source reads. Later added refusal/cleanup cases also accepted. No remaining required fixes; source-only review, no execution/imports, no independent runtime reproduction. Reviewer construction guidance confirmed three exact frozen repairs and relational factory constraints; no new permission inferred.

Changed files: `tests/test_dependency_observation_legacy.py`, `research/OBSERVATION_LEGACY_QUALIFICATION.md`, this report, `research/OBSERVATION_OUTER.md`, `research/STATE.json`, `research/PRE_CAMERA_READINESS.md`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`. Private session/feature notes backed up; existing evidence preserved. Source lock byte-unchanged, no public-source acquisition in this package.

Limits/blockers: runtime and supervisor integration pending; initial loader/interpreter/stdlib trusted; dynamic closure/freshness/provenance unproved. Actual activity decisions accepted_contract_interaction, accompanying_component_terms, constants_provenance, narrow_research_hypothesis_scope and distinct_operational_act_decision all pending. Protected source/native dependency input unopened. Exact mainland binary/body mapping, English resources, native FTP backend, recovery and write prerequisites remain unproved. No actual records, runtime activation or feature gate. Camera commands: **none**.

Previous goal turn: **progress** (reference review committed bdf5e95). Current goal turn: **progress** (previously missing unchanged-gate positive path now qualified). Full pre-camera objective remains active and incomplete.

Next single work package: **RA-003: integrate the qualified observation preflight and saved comparison into a separate disabled launcher path with explicit observation review/decision/anchor inputs. Derive the executing source-roster delta and exact fourteen-role record projection, retain the existing pending path, and qualify the full invented bundle through owned supervision with explicit runtime substitutions. Independently review before actual record assembly. Keep actual activation disabled and all five activity decisions pending; no installed dependency activation, firmware/constants/native payload reads, downloads/uploads or camera contact.**

Retained authored fixtures/gate under ignored private paths are required locally; no fresh-checkout portability claim. Reviewed publication commands (all exit 0):

```powershell
git diff --check
git add -- tests/test_dependency_observation_legacy.py research/OBSERVATION_LEGACY_QUALIFICATION.md research/OBSERVATION_OUTER.md research/sessions/20261020-RA-003-legacy-positive.md research/STATE.json research/PRE_CAMERA_READINESS.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git commit -m "test: qualify complete invented legacy observation preflight"
git status --short --branch
```
