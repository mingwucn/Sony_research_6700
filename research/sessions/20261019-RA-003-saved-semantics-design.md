# RA-003: saved-basis semantic predicate design

2026-10-19. Topic branch `codex/ra003-saved-semantics-qualification`, starting HEAD `ffca91f` with a clean tracked tree. The unfinished ignored design was preserved and completed here. Evidence: **static-inference**, **offline-tested**; no independent execution/reproduction.

The [coverage design](../SAVED_BASIS_SEMANTICS_DESIGN.md) adds complete producer-envelope schemas, counter/span/chunk arithmetic, full directory/selection checks, original prefix-inventory binding and saved EXT scalar derivation to the existing nine-role detached preflight. Forty authored helper/fixture/producer sources are pinned. No upstream implementation was executed or adopted. Operational source authority and actual saved-record application are still pending.

## Qualification and independent review

Final suite: **64/64 invented tests passed**, zero skips, exit **0**, **7.391s**. It includes the earlier 52 methods, six producer/branch/policy methods and six extension-feasibility methods. Subtest branches are not counted as extra methods. Tests use complete invented records and synthetic byte buffers; no actual basis or source-cache bodies are read.

Two owner-authorized local reviewers independently inspected authored source and saved invented evidence. Both found the same blocking flaw in R1: aggregate extension-gap arithmetic could accept impossible parser histories. Each accepted extension has a header and nonempty padded payload; a 512-byte gap cannot contain one, even if another gap contributes unused capacity. R2 checks each interval's feasible count at 1024 through 66048 bytes per extension and constrains the saved total count to the sums of those ranges. Both final source reviews accept this repair within the narrow design scope. Reviewers did not execute tests or reproduce any camera observation.

All **57 R2 pins**, **40 copied-source origins** and **52 preserved R1 snapshot identities** verified. The separate saved-log check matches 64 AST test methods to 64 logged passes. The full R1 source/log snapshot, initial policy, old tests and failed runs remain private. Historical source seals and diagnostic outputs are unchanged.

Development outcomes retained:

| Run | Result | Interpretation |
|---|---|---|
| Initial | SyntaxError; no tests ran | Multiline `with` syntax corrected; original log retained. |
| R2 | 52 passes, 1.565s | Earlier unfinished design qualification, observed here without rerunning it. |
| R3 | 58 methods, one failure, 5.051s | A new negative test set an already-empty unknown-revision reason list to empty. Test expectation corrected; predicates unchanged. Shell's following log display returned 0; the unittest result was a failure. |
| R4 | 58 passes, 5.048s, exit 0 | Corrected status-mutation test; both reviews subsequently found the directory feasibility flaw. |
| R5 | 64 passes, 7.391s, exit 0 | Repaired per-interval feasibility plus six regressions. |

One multi-file patch initially failed its context check and applied no changes; the corrected patch succeeded before R5. The first publication helper refused before writes because the reviewers use different freeze-field names; the preserved helper was corrected to check each exact field and all 57 reviewed pins. It then succeeded without rerunning tests or changing evidence. No acceptance threshold was weakened after a failed test. Ordinary repository tests from the reference refresh were not rerun or claimed as qualification of this private validator.

## Commands, interpreter and limits

Interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython **3.13.12**, Windows AMD64. Tests use only authored sources, invented inputs and the standard library. Private producer runners were read as source, never run. New source copies and evidence outputs used exclusive creation; private notes were backed up before updates.

```powershell
git status --short --branch
git switch -c codex/ra003-saved-semantics-qualification
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-saved-semantics-design/test_saved_semantics.py *> private/sessions/20261019-RA-003-saved-semantics-design/tests-r3.log
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-saved-semantics-design/test_saved_semantics.py *> private/sessions/20261019-RA-003-saved-semantics-design/tests-r4.log
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-saved-semantics-design/test_saved_semantics.py *> private/sessions/20261019-RA-003-saved-semantics-design/tests-r5.log
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-saved-semantics-design/verify_qualification.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-saved-semantics-design/publish_design.py
git diff --check
```

R4/R5 shell commands explicitly ended with `exit $LASTEXITCODE`; both returned 0. The qualification verifier and publication check return 0. Host-authored stdlib stdin scripts added the fortieth producer pin, preserved all R1 files and wrote both immutable review manifests; they read ordinary authored sources/logs only. `prepare_sources.py` and the initial 52-case qualification belong to the earlier unfinished portion of this package and were not rerun here.

Saved-only consistency does not establish historical event truth, source/input authority, raw hash/classification/padding validity or fresh observation permission. The injected preflight module must be authenticated by the next integration. An 8 MiB encoded fingerprint limit is not a process-memory cap or sandbox. Scalar equivalence shares the observer arithmetic; the independent simple geometry calculation is narrower.

`complete_saved_basis_semantic_revalidation`, source-authority binding, operational acceptance and execution authority remain **false**. Retained dependency/native-policy blockers remain unresolved. English/native FTP, exact-body correspondence and recovery remain unverified. The owner rights answer remains **No / unknown**; no new permission or firmware-analysis scope is inferred.

Changed tracked files: this report, `research/SAVED_BASIS_SEMANTICS_DESIGN.md`, `research/STATE.json`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md`, `docs/FEATURE_PROGRESS.md`. Internal session and feature notes updated after byte-preserving exclusive backups. Only reviewed sanitized files are staged. Camera commands: **none**. No camera contact, raw/protected input access, native dependency execution, network acquisition/upload, driver or firmware change, feature/recovery/device-write gate passed.

Next single work package: **RA-003: bind the reviewed saved-semantic validator and its scalar/helper hashes to the frozen ordinary source authority graph, qualify substituted-source and mismatch refusals, and independently review a once-only saved-record diagnostic before running it; no protected-input observation or runtime activation.**

Private evidence identity summary (SHA-256):

- `saved_semantics.py`: `fb6a049b6d4647f347d479dfee4244fd96c27c4bf025da9819cd0c7e701ec3c0`
- `ext_saved_scalars.py`: `516fc94fd04701edd4ded1c3cc60586f32e525acc99dfc8b91fcd2d9f9d4c70f`
- `test_saved_semantics.py`: `c2a7e591811d3c60d1826d9f2a947dc77964eb318163de1ad702c5ce4af176c6`
- `verify_qualification.py`: `eafff5669e974ce690e621983eebad7b8e85ea01be597677278c6e537e666379`
- `gate-semantic-design-review-r2.json`: `9470840d58f46bed79b338b54cbf1610949434d68ee925819d84e6f1694dd498`
- `runtime-semantic-design-review-r2.json`: `eadf832f097c2eb0723e84b0feb0ceaa2e86ff995178750416b48b486c85ba57`
- `review-freeze-r2.json`: `196a04c8c269ebb66b8b294b4779813011104a0bc3325d44471600008b83007d`
- `tests-r5.log`: `697e374bcca7ff38d81750d1b7ab72848ed52a7b5bf2fb1dac64ffc9345241c7`
