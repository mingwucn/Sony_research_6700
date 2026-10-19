# RA-003: localize the refusal and separate cache hash domains

2026-10-19. Branch: `codex/ra003-digest-localization-result`.
Evidence: static-inference, offline-tested. English and native Wi-Fi FTP remain
first; FL2/FL3 deferred, calibrated custom looks later and bridge separate.
Previous goal turn: **progress** (fresh public-reference identity check and saved
findings). Current goal turn: **progress** (first refusal localized and separate
saved-record comparison completed). The overall pre-camera goal remains active.

## Findings and actual outcomes

The original refused comparison and its source are preserved. A separate
diagnostic found its first failed predicate:
`raw_cache_equals_declared_cache_file_digest`. The recorded cache file-byte hash
and the producer's canonical-JSON-plus-newline hash differ. The two configuration
digest predicates and reviewed public-vector-plan predicate match.

The producer source establishes the hash domains; no cache body was opened.
Unequal hashes alone establish neither cache-content change nor a serialization-
only explanation. Configuration file bytes also differ from their canonical
serialization, while the canonical configuration predicate matches.

Two exact source reviews accepted the diagnostic. Its once-only application
completed **exit 0**, **0.5347248s** tool wall time, with **five ordinary reads /
93,748 bytes**. All input pins matched. Two narrow outcome reviews reconciled
the new ledger and digest results. No legacy adapter executed in this diagnostic.

A separate corrected-domain retrospective comparison then completed **exit 0**,
**0.9998656s** tool wall time, **thirteen ordinary reads / 2,448,945 bytes**.
Seven inputs were authored source texts (five pure helpers executed; two producer
sources hashed only), six were saved metadata. It found consistency under the
unchanged legacy predicates for the selected package metadata, **eleven Python
origins, five trusted origins and five native loads**, raw/journal anchors,
callback/publication order and saved startup projections. This is supplied-record
consistency, not independent authentication of those historical events.

Two source reviews accepted that exact separate wrapper before application. Two
outcome reviews checked its frozen ledger and parent-projected summary only;
they did not open the full result body.

The canonical cache expectation is explicitly the **same raw record's self-report**.
The original file hash remains separately typed. All fourteen previous blockers
remain, with three new cache self-report/content blockers: **seventeen total**.
Original raw/journal hashes remain unchanged; parent rechecked the original
refusal SHA-256 before and after application. No historical evidence was rewritten.
The successor event contract is **not applied**; cache contents, whole descriptor
audit, current dependencies and pre-execution approval remain unverified.

See [hash-domain design and limits](../DEPENDENCY_DIGEST_DOMAINS.md). No actual
firmware, constants, cache body, installed dependency or native payload was read
or executed; no upload, launcher, camera operation or new network request.

## Exact commands and qualification

Windows AMD64 / CPython **3.13.12**, interpreter
`C:/ProgramData/miniconda3/python.exe`. All commands are host-only.

```powershell
git status --short --branch
git switch -c codex/ra003-digest-localization-result
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-binding-localization/digest_once.py
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-cache-domain-comparison/qualify.py
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-cache-domain-comparison/full_host.py
& C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-cache-domain-comparison/saved_comparison.py
```

All above exits **0**. Both applications were separately frozen after exact
source review; each actual application occurred once with no automatic retry.
The last command was run only after the full suite completed on its original
process handle. `qualify.py` invokes invented inputs and temporary files only;
its expected negative-test refusal is not an actual application failure.

| Qualification | Result | Duration and scope |
|---|---|---|
| Earlier digest diagnostic public cases | 8/8 passed | 0.471s; invented JSON only, retained in the full 403-case run |
| Earlier digest diagnostic wrapper cases | 9/9 passed | 0.496s suite / 0.4971877999487333s wrapper; invented temporary files |
| Retained full host run | 403 cases; 400 passed, three platform skips, exit 0 | 56.655s suite / 57.00333860004321s wrapper; original process reached terminal during the intervening reference review |
| New cache-domain qualification | 21/21 passed, zero skips, exit 0 | 8 pure + 13 wrapper; 4.662s suite / 4.663042399974074s wrapper |
| New full authored host regression | 411 cases; 408 passed, three platform skips, exit 0 | 403 retained + 8 new public cases; 65.888s suite / 66.2369148999569s wrapper |

No hardware, native camera FTP, deployment server, firmware/GDT or recovery test.
Earlier diagnostic qualification commands and private log/receipt pins are kept
in the ignored localization session. Both new command scripts are also retained
privately to preserve their exact test selection and invocation.

One new freeze-preparation stdin script exited **1** before writing a freeze or
starting an application: `ast.literal_eval` cannot resolve the authored `BASE`
string concatenation in PLAN. A restricted AST string/tuple/dict reader corrected
the preparer; subsequent preparation exited **0**. Source, tested predicates and
application thresholds were unchanged. The failed preparation receipt is retained;
neither actual diagnostic was retried.

Private sessions: `private/sessions/20261019-RA-003-binding-localization` and
`private/sessions/20261019-RA-003-cache-domain-comparison`. They retain freezes,
exact source reviews, exclusive start/result/completion records, tests and host
invocation receipts. The corrected full result embeds old input bodies and is
not uploaded. Its outcome reviewers are restricted to authored sources, new
ledgers and the explicitly parent-projected summary; full body correctness is
not independently reproduced by those reviews.

## Completion record and remaining work

Changed public files:

- `tools/dependency_digest_diagnostic.py`
- `tools/dependency_cache_basis.py`
- `tests/test_dependency_digest_diagnostic.py`
- `tests/test_dependency_cache_basis.py`
- `research/DEPENDENCY_DIGEST_DOMAINS.md`
- `research/sessions/20261019-RA-003-binding-localization.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`

Private `session-state.json`, `feature-progress.json` and `feature-progress.md`
are synchronized after exclusive backups. Reviewed
paths are staged explicitly; no private data or third-party material enters Git.
JSON parsing, `git diff --check`, staged paths and staged content are checked
before commit. Source lock and earlier source/evidence files remain unchanged.

Camera commands: **none**. No feature supported, recovery proved or device-write
gate passed. Historical dependency-manifest/native-policy blockers remain in their
frozen plan. Exact body correspondence, service access, rollback, native English
resources and native FTP backend remain unresolved.

Next single work package: **RA-003: design and qualify a prospective dependency-only
producer for the successor contract, with expectations fixed before execution and
explicit guard, durability, callback and cleanup events; independently review its
source before any installed-dependency or protected-input act.** Do not synthesize
missing historical events or treat this retrospective comparison as prior approval.
