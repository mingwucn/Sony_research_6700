# RA-003: ancestry-bound v6 source chain

2026-10-19. Branch `codex/ra003-v6-chain-finalize`; starting HEAD `171bc4c`, tracked tree clean. Evidence: **offline-tested**, **static-inference**. Previous goal turn: progress; this continuation: progress. The broader pre-camera goal remains incomplete.

## Result and scope

The successor gate and entry now require two additional ordinary inputs: the explicit 29-row ancestry map and its preserved historical 35-case qualification. Both have fixed external entry hashes. The versioned v6 candidate/decision/review/seal and qualification schemas reject v5 records. All 29 source paths retain explicit historical keys: **26 unchanged sources and three previously reviewed replacements**. Historical seals, sources and failed diagnostic remain unchanged.

Final invented qualification: **305/305 passed**, zero skipped, child/wrapper exit **0**, **114.266s** suite / **114.78642710001441s** wrapper. Composition:

- **284 unit/gate cases**: 234 adapted retained cases, 35 ported ancestry cases and 15 new chain cases.
- **14 production-bootstrap cases**, including exact main launching an unchanged child that refuses invented references.
- **Seven real-process invented composition cases**, including narrow success with strict outer refusal of injected provenance, phase-two failure, deadline cleanup, malformed output, missing receipt and source mutation.

All **89** qualification source/fixture hashes match their snapshots and final files. **86** nonbootstrap hashes are fixed in the gate; gate/entry/ordinary-reader hashes are independently bound through candidate and qualification rows, avoiding a self-hash cycle. The ancestry fixture is local to this captured closure. All **84** recorded predecessor inputs remain unchanged.

The full 305-case wrapper evidence is distinct from the gate-consumable **284-unit-case projection**. Explicit source-name normalization preserves all 89 pins without collisions; the projection retains the full raw result hash and projector hash. Two owner-authorized local source-only reviewers independently accepted final source and saved evidence. They did not execute or independently reproduce tests. A projector ordering finding was repaired before use: verified helper bytes are now checked before compilation/execution. Superseded projector text is reconstructed and retained; it is not an exact-byte original archive.

## Evidence identities

| Artifact | SHA-256 |
|---|---|
| Final gate | `9643b1547eb4363ce87451913dbe40c83b0e51b7b5e58720bb93354478e1e35a` |
| Final entry | `b79fd860efebd660a0f199f843cee57700c5a0870ce5632ef57bc61eec8932d1` |
| Full 305-case qualification result | `f4e1575dfee32753abfef0df79e60a378cad1ac0402c0c9062526ca8360443e8` |
| Projected 284-case gate result | `110242c957dea9a99372496630ac26265d67a1cc21100db2d93cbcfdb44a94b6` |
| Aggregated current qualification review | `bf5821920d8d7142128688d4fb29990a541898d9b21f64812394edbb532a452a` |

Raw logs, snapshots, four independent source/evidence review artifacts, source/map pins, projection and predecessor-verification records stay private. No upstream code or payload was added to Git.

## Commands and results

Interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython **3.13.12**, Windows AMD64. Host only.

- `git status --short --branch`: initially clean; exit 0.
- `git switch -c codex/ra003-v6-chain-finalize`: exit 0.
- Read/authored-source metadata scripts ran with `-I -S -B -X utf8 -`; final source-policy discovery, 89 source/snapshot checks and 84 predecessor checks exit 0. No saved operational source-cache execution.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-ancestry-chain-v6/qualify_chain.py *> private/sessions/20261019-RA-003-ancestry-chain-v6/qualification-wrapper.log
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-ancestry-chain-v6/prepare_qualification_result.py *> private/sessions/20261019-RA-003-ancestry-chain-v6/projection.log
```

Both exit **0**. Qualifier launches the same interpreter with `-I -S -B -X utf8` and the absolute `successor_runner.py` path, cwd the v6 session, a 300-second direct-child deadline and exclusive output directory. Source snapshot and exact argv are retained. This deadline is not proof of process-tree termination or a whole-process memory quota. The projection runs once after qualification and independently checks raw logs, full result, source policy and all source identities before exclusive publication.

Earlier development logs remain preserved: 234 cases with one failure/one error (fixture paths); 284 cases with two setup errors (missing-document negatives); 305 cases with 21 errors (missing copied runtime source); then 305 passes in 108.934s before final policy freeze. All were host/invented work. Two stale bootstrap schema assertions were also corrected. Exact interactive unit-only command text was not retained; these failed development logs are not the accepted qualification. Final command, source snapshot and structured observed IDs are retained above. No thresholds were relaxed after failures.

JSON parsing and `git diff --check` pass. Changed tracked files: this report, `research/STATE.json`, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `docs/CODEX_HANDOFF.md`. Internal session/feature notes updated after exclusive byte-preserving backups. Authored implementation and invented fixture work remain ignored and private.

## Limits and next work

Four inherited host-boundary unit cases use an explicit inert validation stand-in. Successful composition uses invented streams and injected AES/native adapters; strict outer acceptance correctly remains `needs_review`. Historical noninjected dependency-only evidence is separate. Neither the complete fixed production policy nor an actual saved operational bundle is accepted by this qualification. No fresh saved diagnostic or GDT observation was performed.

English and native Wi-Fi FTP remain primary and unvalidated; FL2/FL3 deferred, calibrated custom looks later, optional host-assisted bridge separate. Exact mainland binary identity, act-specific proprietary inspection basis, complete binding/basis reconciliation and recovery remain unresolved. The prior rights answer stays No/unknown. Feature, recovery and device-write gates remain false.

Camera commands: **none**. No actual firmware, operational constants, saved actual prefix or installed third-party crypto dependency read/execution; no camera contact, driver/firmware change, private upload, upstream launcher/service execution or invented target offsets.

Next single work package: **RA-003: prepare and independently review one v6 saved-metadata reconciliation diagnostic against the frozen qualification and explicit ancestry, then run only that ordinary-metadata diagnostic; no protected-input inspection or runtime activation.**
