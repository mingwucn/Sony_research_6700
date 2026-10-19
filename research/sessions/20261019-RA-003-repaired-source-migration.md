# RA-003: repaired source migration preparation

2026-10-19. Branch `codex/ra003-repaired-source-migration`; starting commit `625ae6cb7750a9459f7abe9241fcd6217420ba4a`. Evidence: **static-inference**, **offline-tested**. Previous goal turn: progress; this turn: progress. The broad pre-camera objective remains incomplete.

## Result and remaining integration

One fresh collection reconciled **47 Python sources / 813,858 bytes**, 47 descriptor close attempts and 47 EOF probes. Thirty-two authored sources now refer to the preserved repaired copies: **29 byte-identical** and exactly three changed (`gdt_gate`, `ext_read_planner`, inherited bootstrap `io_entry`). The eleven dependency and four trusted Python sources retain their earlier identities. Their source bytes were read and cached privately; they were never imported/executed. The three outer sources are excluded from this cache to avoid a future cache/entry reference cycle.

The new pure migration validator distinguishes unchanged source ancestry from the changed modules' scoped 162-case repair evidence. Historical 811-, 51-, 20- and 162-case records remain unchanged; none is relabelled as operational qualification of the successor chain. Twenty-eight new adversarial tests pass, covering missing/extra sources, changed/stale repair hashes, unexpected changes, path aliases/traversal, tampered bytes and incomplete/changed/nonregular read receipts.

Updated role and prerequisite maps reconcile all 26 roles. One effective source map contains 29 role/bootstrap pins. The unchanged **authored pure binding planner** checked the repaired authored source ASTs. Its complete result equals the earlier pinned graph except for the intended role-map replacement, preserving both dependency blockers, the 23 eager/three protected order and false readiness/runtime/authority flags. No other cached target module or actual factory ran. The other executed authored helpers were the new migration validator and previously qualified snapshot helper.

Two enforcement points remain unchanged in the frozen outer implementation: the gate's source-cache qualification check and the loader's effective qualified-source construction still require historical identities. Both must consume one validated closed repair overlay. Fresh collection and a source graph alone do not complete that integration. The future freeze order must keep role/cache/graph references before new outer sources, and outer qualification/review before an externally anchored candidate/decision/seal. A qualification-result hash must not be embedded in the same entry whose hash it contains.

## Commands and results

Interpreter: `C:\ProgramData\miniconda3\python.exe`, CPython 3.13.12. Exact commands:

```powershell
git status --short
git branch --show-current
git switch -c codex/ra003-repaired-source-migration
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 D:\LocalWork\Sony_research_6700\private\sessions\20261019-RA-003-repaired-source-migration\test_migration.py
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 D:\LocalWork\Sony_research_6700\private\sessions\20261019-RA-003-repaired-source-migration\collect.py 8d0c692440bbe33e56dbb3835196eeb301c315147fd1fcb8c584613deb048536
```

Starting tracked tree clean; topic-branch creation exit **0**. Tests: **28/28 passed**, zero skipped, exit **0**, suite **0.060s**, wrapper **0.2536882999702357s**. Qualification source bytes stayed unchanged. Collector: **one launch**, exit **0**, collection **0.5410857000388205s**, wrapper **0.7308824999490753s**, collector source stable. Host-authored supervision used closed stdin, captured logs and a 60-second timeout. Raw argv, output and receipts remain private. No failed collection or retry occurred; historical full suites were not rerun.

The collector freezes eight ordinary JSON input hashes before collection. It enforces isolated, no-site, no-bytecode, non-optimized startup explicitly. Input/helper/self/output readback uses bounded descriptor reads, parent link/reparse refusal, stable identity, EOF and a single close attempt. The 47 target source receipts exclude eight metadata reads, two helper-source reads, one collector self-read and seven generated-output readbacks, plus supervisor/validation reads. They are not a claim of only 47 total host file reads.

Same-agent independent readback matched seven output artifact hashes, all 47 decoded cache hashes and receipt summaries, the 29 effective pins, all 26 role maps and complete graph comparison. Thirty-eight original source pins and 41 repaired packet pins were checked before collection and are preserved.

## Review, correction and limits

Before collection, source review found missing fixed metadata authority and unbounded pre-hash metadata/helper reads. Both were repaired before the single launch: fixed literal pins, bounded descriptor reads and explicit startup refusal. A second source reviewer found no material blocker. Final source/metadata review found no new blocker, verifying the 32-entry ancestry, exactly three changed entries and all 29 effective pins. The reviewer did not execute code, reopen cached third-party bytes/receipts or independently reread the historical graph; its full-graph assessment relies on the collector's pinned comparison. This is limited source-preparation review.

Readback found the generated role draft retained the predecessor's authority wording. A separate `successor-role-draft.json` corrects that description and explicitly marks operational qualification pending; the original draft and its receipt are preserved. Future integration must use the successor draft and explicit scoped evidence rather than inherit the predecessor description.

No firmware, operational constants, saved raw prefix or native payload read; no native backend/dependency execution, actual entry activation, GDT replay, download, upload, driver change or camera operation. Camera commands: **none**. English and native FTP remain first priorities; FL2/FL3 and custom looks remain deferred. Exact-body/SKU/build correspondence, English mechanism, native FTP backend and proven recovery remain unresolved. No feature or device-write gate passed.

## Changed files and next package

New ignored private files: `migration.py`, `test_migration.py`, `collect.py`, exact command/log/result records, fresh source cache and receipts, migration/role/prerequisite/effective-source/binding drafts, successor-description addendum and review notes. Original frozen sources and previous session evidence remain intact. Public changes: this sanitized report, README, handoff, backlog, feature progress and STATE. Private session/feature continuity receives additive entries. Only reviewed public files are staged.

RA-003: implement one closed repaired-source overlay in both the outer gate and loader, consuming the successor source/role graph; qualify the full invented host/child composition and independently review the migrated chain before selecting any actual act.
