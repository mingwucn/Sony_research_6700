# RA-003: isolated invented-metadata startup

2026-10-20. Topic branch `codex/ra003-isolated-metadata-entry`, starting HEAD `a46fb12` (clean).
Evidence: **offline-tested**, **static-inference**. This is host preparation, not target feature validation.

Two helper source buffers (source_import_audit and detached_metadata_loader) are supplied as bytes, checked against external expected digests, and both compiled before either executes. They receive detached modules and a fixed helper import policy, without authored sys.modules aliases. The resulting loader checks the fourteen public sources and composes the eleven retained ordinary host validators. No upstream sources, camera payloads or installed crypto dependency execute. The packet accepts invented metadata, not file paths or native/runtime callbacks. Source origins are fixed synthetic labels, not authenticated disk origins. Expected helper/public pins come from the prior independently reviewed qualification; matching them is not proof of permission, review authority or freshness.

The child is invoked exactly as `[sys.executable, '-I', '-S', '-B', '-X', 'utf8', '-c', BOOTSTRAP, expected_packet_sha256]`. It checks sys.orig_argv, the fixed bootstrap digest and expected interpreter/version/flags/path, then observes no site/tools/crypto aliases before and after. A checked startup profile is a limited observation; it does not authenticate the interpreter distribution or all transitive stdlib origins. The parent remains trusted. This is reviewed authored code, not a hostile-code sandbox.

Wire data uses explicit type tags for bytes and JSON builtins; dictionary values cannot impersonate a byte tag. Duplicate keys, nonfinite numbers (including exponent overflow), bool/int substitutions in startup policy, unknown shapes, wrong sources and runtime requests refuse. Input packet: 16 MiB; source buffers: 8 MiB total / 2 MiB each; argument tree: 100,000 nodes / depth 80; output: 8 MiB per pipe. Complete success output passes cumulative UTF-8/escape/key accounting before serialization. These are data-model/pipe budgets, not aggregate process memory limits. Returned outer and retained-loader contracts are closed and checked against source pins; authority flags remain false.

Supervision launches once. Normal poll completion incurs no extra kill/wait. Timeout or interruption attempts at most one kill and one bounded wait; failed or uncertain actions are not repeated. Every pipe has a close-attempt/completion record shared by writer and parent. A failed close is never retried. Cleanup attempts other independent actions while retaining the primary exception, with a metadata_completion receipt attached; failed waits do not claim the process reaped. Live pipe-owning threads retain their pipes and produce needs_review. Writer exceptions, including KeyboardInterrupt after delivery, cannot be silently converted into success. No automatic restart.

## Qualification and independent review

Final **77/77 passed**, zero failures/errors/skips, exit **0**, 31.639054899977054 seconds wrapper / 31.595 seconds unittest. **41 retained loader + 30 new public + 6 nonstub integration** cases; **117** source pins remained stable. CPython **3.13.12**, Windows AMD64, `C:/ProgramData/miniconda3/python.exe`.

Six real disposable children exercised the actual fourteen-public/eleven-retained invented chain: prepared, operational-shaped, complete common legacy metadata and ambient function substitution all completed; original wheel conflict and operation mismatch refused (exit 2). Every process reaped and all pipe threads stopped. Inputs and parent aliases remained unchanged; no installed dependency aliases appeared. Other tests cover packet/hash/source/origin/type/startup/result tampering, argument bounds, timeout/output overflow, primary exception retention, kill/wait/join/close failures, unknown close completion and writer failure after valid output. Direct CLI exits 2 with empty output; runtime API refuses. No original wheel or operational input was inspected.

Owner-authorized local reviewer gate_review performed static-only review. Material findings repaired: IE-GR-001 duplicate/uncertain lifecycle actions and masked primary failures; IE-GR-002 open/untyped result/startup schemas and pre-allocation budget gaps; IE-GR-003 writer/parent duplicate stdin close; IE-GR-004 unrecorded non-OSError writer exceptions. Focused regressions cover each. Final source review found no remaining material issue within this scope; final evidence acceptance is recorded in the session outcome.

Preliminary runs: 19/19 in 9.906s and 27/27 in 10.209s, exit 0. First full qualification: 76/76, exit 0, 31.127631700015627s, 117 pins, log fcf049c243a6c00507e80e8b8766626671af3088e2b8878a85ea1a4afbd4a0af, preserved in private/sessions/20261020-RA-003-isolated-metadata-entry. It is historical pre-writer-repair evidence. The V2 run was needed because source changed; it was not restarted after a polling timeout. No historical full suite rerun.

Final log SHA-256: `b3ea62daeb95538e2f9a3c0da9b57f200b603f64cbf23f7474951055bdae835e`.
Child observations SHA-256: `369230d2475306016223d5c6a4f1987f974e834c4024c3e84cce2b434bf89778`.
Entry source: `41c90441b4268946a9e702b1484a3b879a15f698d9458e0cae2a1b4cd9448507`.
Public tests: `8a135d2b83a62615a0dea3ced4b57407e7f0292be4f01d85c0c1303171b3a704`.
Qualifier: `1d37acc2e4337c634416986f44e405f77561e4c93750b32eb472924a4e30c6f5`.
Result: `eec376ff0465212e27a9d54731ed15c113e097e7e43ee77c962d9a682728774b`.

## Exact commands and results

```powershell
git status --short --branch
git switch -c codex/ra003-isolated-metadata-entry
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path[:0]=['.','tests'];r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_isolated_metadata_entry'));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-metadata-entry/qualify.py
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-isolated-metadata-entry-v2 -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-RA-003-isolated-metadata-entry/qualify.py -Destination private/sessions/20261020-RA-003-isolated-metadata-entry-v2/qualify.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-metadata-entry-v2/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-metadata-entry-v2/record.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-isolated-metadata-entry-v2/finalize_notes.py
git diff --check
```

All qualification/recording commands exit 0. The first two public commands used evolving source (19 then 27 cases); the final 30-case source is covered by V2's 77 cases. An exploratory search/read of nonexistent dependency_supervisor.py failed; no code or test failure followed. Exact fixed child argv is above; source code is owned here, not an upstream launcher. Logs/results/notes backups are exclusively created. Final independent review accepted the 77 results, all 117 pins and six child receipts; stale top-level public/private report, suite and next-package pointers were reconciled after additional exclusive backups. Explicit eight-path staging, staged content/path/whitespace inspection and a topic commit complete this package; no source lock change or push.

Changed public files: tools/isolated_metadata_entry.py, tests/test_isolated_metadata_entry.py, this report, research/STATE.json, research/PRE_CAMERA_READINESS.md, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md. Private session/feature notes synchronized after exclusive backups.

Activity-specific inspection rights/consent, actual executing dependency/source origins, the operational binding and exact-body correspondence remain unresolved. The owner rights answer remains **No / unknown**; this package makes no new legal determination. Mainland English restriction/resources, native Wi-Fi FTP backend/direct-server evidence, full backup coverage and usable rollback remain unverified. English/native FTP remain primary; FL2/FL3 deferred, calibrated custom looks separately later; optional bridge HOST-ASSISTED.

Camera commands: **none**. No firmware/constants/saved raw stream/camera-native payload reads, installed dependency activation, download/upload, upstream launcher, driver/firmware change or feature/recovery/device-write gate.

Next single work package: **RA-003: reconcile the isolated invented-only entry and checked source closure with the frozen primary-GDT scope; produce one executable-path gap assessment that identifies the exact activity-specific rights/consent and source-origin prerequisites for any actual metadata observation. Do not add a generic gate layer or activate anything; no firmware/constants/native payload reads, installed dependency activation or camera contact.**
