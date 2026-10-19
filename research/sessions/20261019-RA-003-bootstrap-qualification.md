# RA-003: production bootstrap on invented authority

2026-10-19. Branch `codex/ra003-bootstrap-lab`. Evidence: **offline-tested**, **static-inference**. Previous goal turn: progress; current turn: progress. The complete pre-camera goal remains active, not complete.

## Result and boundary

**14/14 bootstrap tests pass**, zero skips, exit **0**, **24.535s** suite / **24.89459830004489s** wrapper. All **85** source/fixture pins match before/after, current files and snapshots. All **82** inherited authored/invented copies match their predecessor; no production source changed. Runtime and gate reviewers inspected authored sources/record metadata only, without execution or protected inputs. Their exact reviewed pins match current files.

The exact production `bootstrap` implementation, ordinary reader and pure gate are now exercised against fresh invented documents. The positive test deliberately substitutes the in-memory `REFERENCE_PINS` dictionary; it does not qualify the saved production policy or supply owner consent. Generated candidate/decision/review/seal and qualification documents are test fixtures only. Exact entry bytes replace the earlier custom child driver in the temporary fixture.

Tests cover wrong external seal, duplicate seal key, changed candidate/helper, wrong repository root, missing input role, protected-path substitution and hardlinked bootstrap file. Assertions establish refusal before helper execution or ordinary input reads as applicable. A changed cached source is refused on fresh source refresh. Wrong child operation ID is refused after bootstrap and before source preparation/child records. An actual isolated optimized interpreter is refused before its first bootstrap read.

The real `main` host path loads actual authored modules, prepares bindings and launches an unchanged child process. The parent's test policy is not inherited by that process. Its fixed production references correctly refuse the invented bundle: child exit **2**, narrow parent exit **1**, outer exit **2 / needs_review**. No child source receipt or dependency provenance is created. This is observed refusal, not successful production child/native composition. Earlier seven-case injected composition and 207 adapted unit cases remain distinct historical evidence, not new reruns.

## Remaining contract finding and frozen evidence

Gate review found **BOOT-GR-001**: the current v4/207-case gate has no closed parent-composition evidence input or reference. Dynamic entry/self hashes do not require the repaired parent's seven-case result, complete source roster and reviews. The successor chain is incomplete; no actual activation occurred.

A new private `parent-evidence.json` freezes the historical seven IDs, complete **81-source** qualification map, tested predecessor entry identity, raw result/log hashes, two review hashes, exact counts and explicitly false operational/execution/dependency flags. SHA-256: `8b9dc7a70894802799a66cc747cd171ddaf9f0e565c04cb2cc0a3e9ad7975b24`. It is not consumed by the current gate and cannot authorize an act.

The source review specifies noncircular ordering: preserve historical tested-entry identity; add a closed predecessor-evidence input/reference; finalize successor gate/entry and test policy; qualify final sources afterward; bind the later result and review through the external seal. A new reference literal changes the entry whole-file hash. Never relabel the old seven-case hash as coverage of that new entry. Rerun required composition against final source before claiming it.

## Exact commands and development results

Windows AMD64, CPython **3.13.12**, interpreter `C:\ProgramData\miniconda3\python.exe`.

```powershell
git status --short
git branch --show-current
git switch -c codex/ra003-bootstrap-lab
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-bootstrap-lab/qualify_bootstrap.py development-001
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-bootstrap-lab/qualify_bootstrap.py development-002
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-bootstrap-lab/qualify_bootstrap.py development-003
git diff --check
```

Starting tracked tree clean on `codex/ra003-parent-child-records`; branch creation exit 0. Each qualifier captures its exact child argv (`-I -S -B -X utf8 test_bootstrap.py`), Python version, raw stdout/stderr, source snapshots and synthetic per-test JSON/text/log records. The supervisor propagates child failure and source drift, with a 300-second timeout; it did not fire. Its in-memory output capture has no byte/memory cap and timeout handling proves no arbitrary-descendant cleanup.

- development-001: **13/13**, exit 0, **22.734s / 23.08566119999159s**. Initial bootstrap coverage.
- development-002: **14/14**, exit 0, **24.252s / 24.616409999958705s**. Added real optimized-startup refusal and exact fresh-source exception assertion.
- Review found a low-severity test assertion used `child-journal.jsonl` instead of actual `observation-journal.jsonl`. The earlier no-refresh assertion already enforced the stronger boundary. Corrected the name and added all-inputs-read/no-child-source-record assertions.
- development-003: **14/14**, exit 0, **24.535s / 24.89459830004489s**. Source rereview confirms that finding resolved. No threshold lowered; all earlier logs retained.
- Parent-evidence preparation initially exited **1** because a raw CRLF log did not match its line-end regex; no output record was created. A corrected parser view normalizes CRLF while hashing untouched raw bytes, checks exactly seven unique IDs and exits **0**. Both outcomes are noted privately; no test result was changed.
- Host-authored standard-library verification via `python.exe -I -S -B -X utf8 -`: exit **0**, rehashes all 85 current/snapshot files and 82 unchanged predecessor copies, checks exact 14 unique IDs and current review-source pins. Summary and source hashes retained privately. It executes no tested source and reads no real firmware or native input.

Only authored sources and invented fixtures are copied; standard-library venv creates temporary no-pip environments without downloads. The positive read spy covers bootstrap ordinary reads, not a whole-host filesystem sandbox. Generated source-cache JSON contains invented dependency source and authored source only. No protected real inputs or operational native images participate.

## Handoff

Changed tracked files: this report, README, BACKLOG, CODEX_HANDOFF, FEATURE_PROGRESS and STATE. Tests, qualification records, reviews, frozen historical evidence and backed-up private continuity remain ignored. Source lock and all predecessor source files are unchanged.

Native English and native Wi-Fi FTP remain first; FL2/FL3/custom looks remain deferred. Exact-body identity, usable feature mapping, noninjected full composition and proven rollback remain prerequisites. The optional bridge remains separate. English/FTP support, recovery and device-write gates stay false.

Camera commands: **none**. No real firmware/constants/saved-prefix/native payload read, installed audited dependency execution, upstream launcher, download, private upload, driver change or device write in this package.

Next single work package: **RA-003: implement and qualify the closed successor parent-evidence contract, bind it in gate/entry references, then qualify final source and parent/child composition with independent source review before selecting any actual metadata act.**
