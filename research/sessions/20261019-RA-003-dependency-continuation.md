# RA-003: noninjected public-vector dependency continuation

2026-10-19. Branch `codex/ra003-dependency-continuation`.
Evidence: **offline-tested**, **static-inference**, **runtime-observed**.
Previous goal turn: **progress** (reference revision checked and evidence checklist recorded). This turn: **progress** (real host dependency continuation observed).

## Result and boundary

One reviewed existing-venv child ran with `-I -S -B -X utf8`, exit **0**, **0.4664872s**, no retry, deadline/log cap unused, child reaped. Exact runtime source from the frozen v5 packet is unchanged: SHA-256 `4a64bd6c63ff6e43b56ab7298e5fb84a6304e3576990eaa4aa020c551aeba8f1`.

Public NIST ECB/CBC AES-128/192/256 default/generic requests passed **24 comparisons before the callback and 24 during it**. Eleven package Python origins and five native loads (CPUID, AES, AESNI, ECB, CBC) reconciled; actual native audit was required, with no test injection. This does not prove a particular AESNI implementation was selected for each case.

The complete **56,665-byte** raw dependency receipt was flushed, fsynced, closed and freshly hash-checked before the journal marker and single callback claim. The callback checked the durable receipt/claim, original AES module and retained source finder/CDLL wrapper, then exercised loaded public-vector primitives. The runtime seals further native loads before continuation. Driver assertions verified source-finder/path/alias cleanup after return. Fifty-seven durable journal rows reconcile with the raw receipt and callback ordering.

This exercises the **v5 runtime component through a separate dependency-only driver**, not the complete v5 outer activation gate, actual saved operational bundle, GDT factory or firmware input. The Boolean continuation precondition is scoped to this public-vector act; it is not GDT authorization. No firmware, operational constants or saved prefix was read. Existing dependency/native/trusted runtime files were read and the dependency/native libraries executed; this is explicitly host native execution. No new download/install, upstream launcher or service tool was used.

## Qualification and review corrections

- Development-001: **68 passed**, zero skips, exit 0, **1.728s** / **2.0995815s** wrapper. Retained runtime/supervisor plus new invented receipt predicates.
- Development-002: **74 passed**, zero skips, exit 0, **1.826s** / **2.2347128s** wrapper. Added six inert launcher refusal/ownership tests.
- Both initial independent reviews withheld approval. A supervisor `Exception` boundary allowed `KeyboardInterrupt`/`SystemExit` to bypass cleanup; the mutable plan executable was not bound to the approved environment.
- New private supervisor copy catches `BaseException` at owned observation/termination/final-stat boundaries, records `needs_review` and attempts one bounded termination/reap. The launcher now requires each hashed review to bind the whole plan and derives/compares the executable with the pinned config before import/launch.
- Development-003: **81 passed**, zero skips, exit 0, **2.375s** / **2.7324798s** wrapper: 38 unchanged runtime + 16 supervisor + 17 receipt-predicate + ten inert launcher cases. Nine exact authored source/test snapshots match current bytes. The final operational plan contains eleven pins, including config/cache metadata identities; both successor source reviews approved that plan before the one child ran.

Initial reviews, plan, sources and all test runs are retained. All six original predecessor files and eleven final plan pins remained unchanged after the actual child. Only a new operation identifier changed in the copied config. No earlier sources/evidence were overwritten. Fixed-name review slots were preserved under both initial and r1 names before receiving exact successor copies.

The first post-run output verifier returned exit **1** because it compared the original loader spelling (`Util/..`) directly with the canonical configured path. Its source and failure are preserved. The corrected verifier uses the same normalized path comparison as the already reviewed runtime, while retaining raw audit spelling, exact descriptor paths and hashes. Verification of the **same saved outputs** then passed, exit **0**; no dependency execution was repeated or acceptance threshold weakened for a runtime failure.

## Commands and evidence

Host: Windows AMD64; CPython **3.13.12**, `C:\ProgramData\miniconda3\python.exe`. The child used the existing private venv launcher; under no-site startup its base prefix/path is the reviewed Miniconda installation. Exact child argv and startup observation are private metadata.

```powershell
git status --short
git branch --show-current
git switch -c codex/ra003-dependency-continuation
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-dependency-continuation/qualify.py development-003
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-dependency-continuation/run_once.py 09b72f3f4ec83fce00672e9fcdf0fb2b8f793c293563adf5612ab5f42f4832ba 4257dc6bd6d38f859169fc464306a50129780e743071650916021e469ff0c101
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-dependency-continuation/verify_completion.py
git diff --check
```

Starting tracked tree clean at `85b72ae` on `codex/a6700-powerful-recheck`. Branch creation and final commands exit **0**; initial verifier exit **1** as above. Earlier development-001/002 commands used the identical unittest child command recorded in their JSON and exclusive source snapshots. Their wrappers and ordinary copy/metadata/hash operations ran as authored standard-library stdin scripts under the same interpreter/flags. The one-shot launcher wrapper returned **0**, **0.8613599s**; its argv and raw stdout/stderr are retained. No hidden retry or live process remains.

- Plan SHA-256: `25b3fc51646ccfccfdfc848c6e4e5a91ad205b97314e1c19e2b340de6a6e2efd`.
- Native provenance SHA-256: `0add5346e7191290a871c508b598a186d6f23f0980f6d2e7e6547f29b5ea8968`.
- Result SHA-256: `52b09df2e36815c03c94a3dad85cda32f3cd39e54ed24c81bf1c296a1e20b75d`.
- Journal SHA-256: `9e2248a5da2fc3687dfc8fde2ae7071b2fd15a680d7e9c23bc9d7e7d77c9d86a`.

## Limits and next package

Trusted stdlib/_ctypes initialization is distinct from guarded package CDLL observations. Path hashes and descriptor receipts do not attest OS-mapped bytes, transitive native dependencies or arbitrary executable behavior. Cooperative durable calls do not guarantee persistence after hardware failure. Log caps are monitored; supervision owns a direct child only. Repeated interruption, failed termination, OS kill or storage failure can leave uncertain results; no automatic retry/rollback is authorized. The test wrapper's capture is in-memory and its timeout is not process-tree ownership proof.

English and native Wi-Fi FTP remain first; FL2/FL3/custom looks deferred; optional host-assisted bridge remains separate. Exact-body correspondence, target feature mappings, complete operational source/basis-chain acceptance and proven rollback remain unresolved. No feature, recovery or device-write gate passed.

Camera commands: **none**. No firmware/private payload upload, camera/USB contact, driver change or device write.

Next single work package: **RA-003: reconcile and independently review the saved operational source/basis packet against the frozen v5 entry and this dependency-continuation evidence, resolving remaining chain bindings before any actual metadata observation.**

## Independent saved-result review and publication

Two independent source/output reviewers accepted the saved dependency-only observation with no remaining scoped findings. Each recorded output/source hash was independently rechecked before publication.

- runtime-completion-review.json SHA-256: `e5a5b9b06569924412c50c6b8dece8f298e00d3fcdb2e9e64fd457f1220998a1`.
- io-completion-review.json SHA-256: `977a1fcfb82e9896ea4946290b2045c8e669afb5bd71d1d1db6e6d3a415e3441`.

Changed tracked files: this report, README.md, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md and research/STATE.json. Private authored code/tests, logs, receipt metadata and before-state backups remain ignored. Only reviewed sanitized documentation/state is staged. Source lock and existing feature/operational/write gates remain unchanged.
