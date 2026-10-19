# RA-003: checked-buffer detached metadata loader

2026-10-20. Branch `codex/ra003-detached-metadata-loader`, baseline `ea90d64`. Evidence: static-inference, offline-tested. Previous goal turn made progress deriving static import rosters; this turn makes progress binding the public validators to captured bytes. Overall pre-camera goal remains active.

The new host-only loader captures the fixed fourteen-source roster and expected hashes, validates the complete static graph and all source bytes, then prepares all bytecode before the first supplied member executes. Frozen code-object identities, load order and external-import policy are checked before execution and at each integrity check. Every module is frozen immediately after loading, so later source execution cannot silently replace an earlier module's globals. Caller source/hash mappings are copied.

Absolute `from tools import declared_leaf` resolves solely to the already loaded owned object in a detached namespace. No process module alias is installed, replaced or deleted, and preexisting tools entries are preserved. Bare/dotted/relative/star/undeclared imports refuse. Standard-library imports delegate to trusted builtins for the source-derived explicit external names; their actual origins remain unauthenticated. No generic role/function dispatcher is exposed by the checked API: its sole call is validate_invented_context_composition.

The call checks the complete public graph before and after the existing fourteen-contract metadata composition and legacy/successor comparison. That path invokes the existing eleven retained exact-source validators on invented records. Live fingerprints include module globals and owned aliases, function code/defaults/keyword defaults/annotations/closure cells/attributes, wrapped functions, bound method functions, class dictionaries/inheritance/metaclass identity, properties and static/class methods. Shared owned modules are checked separately. This is trusted authored code under a one-owner model, not a hostile-thread sandbox. Borrowed stdlib objects, other instance internals, the loader/audit implementation and interpreter bootstrap remain trust assumptions; full validator_execution_owned stays false.

Returned data is copied into bounded exact builtin JSON types before release, rejecting owned functions/modules/objects and cycles. Exact compact-JSON UTF-8, escaping, key, scalar, punctuation and aggregate-byte accounting occurs before whole-result serialization. Bounds: 200,000 counted nodes, depth 100, 2MiB strings/keys, 4,096-bit integers, finite floats, 8MiB serialized output. These are output-model bounds, not an aggregate process-memory cap. Pre/post-call checks also surround result detachment. The receipt reports checked_public_buffer_execution=true narrowly; all startup, permission, feature, recovery and device-write flags remain false.

Failure is sticky, including an inner swallowed import failure. BaseException paths clear owned module/source/bytecode/fingerprint/namespace references, captured code-object construction references and borrowed foreign snapshots without altering sys.modules. Primary failures remain primary if cleanup also fails. Reentry/reclose and calls before load refuse. Direct CLI exits 2 before imports; run_runtime refuses real_activation_pending.

## Review findings and qualification

Independent source review found two material issues before nonstub integration: DL-GR-001, whole-result allocation preceded the serialized limit; DL-GR-002, mutable compiled/order/external state could diverge from the original hash claim. Both were repaired with incremental accounting and frozen construction identities/policy; regressions prove oversized records refuse before json.dumps and replaced compiled code/order/external policy refuses before exec. No guard was weakened. Later cleanup review proactively removed retained code-object references; a fresh exclusive V2 qualification covers those final bytes.

Final **48/48 passed**, zero failures/errors/skips, exit **0**; **41 public invented-source cases + seven nonstub integration cases**, **19.69031899998663s wrapper / 19.670s suite**. All **113** source/test/scope/fixture/qualification pins match current bytes; installed Crypto/Cryptodome/cffi aliases empty. Independent reviewer verified all pins and 48 successful log outcomes, accepted both repairs and final evidence with no remaining material finding, and performed no execution/protected-input reads.

Nonstub integration covers both prepared and operational-shaped records through the fourteen public and eleven retained validators, complete shared legacy fields without context authority, the original bridge_wheel conflict refusal, unchanged inputs and foreign process modules, ambient candidate/basis functions patched to raise yet unused, and actual captured class/function-default mutation refusal. Returned data has no owned function/global references. Public cases cover import policy, defaults/closures/annotations/descriptors/inheritance, result detachment/type/size/escape accounting, constructor/partial-load/call interrupts, swallowed failures, cleanup chaining, changed compiled policy and foreign replacement preservation.

Historical preliminary runs: 33/33 in 2.066s; 38/38 in 2.665s; repaired 41/41 in 11.802s, all exit 0. First nonstub run: 48/48, 18.245286699966528s, exit 0, log e448d683e4c22abf4a20f6168f27aa587fe899875721156dba034e47084c24b8, preserved in its original private folder. Its source pins describe pre-cleanup bytes and are historical, not the final current qualification. The new V2 run was started because source changed, not because observation timed out. No historical full suite rerun.

Log SHA-256 `7dd312443dfcab88e824c1a4a013ec9930f3778892c2adc34fbc98b235ead71c`.
Loader `7177b075d2df689a17a313587f6e64c6c56625d4ad4cef62e1a3e3201498273c`.
Public tests `5787266ec23cd3b193e3728b3fe986030a2836d0f63f2d6508e342bec41cab68`.
Qualifier `4194972f4fe960ab56f3f085a22ffa9f7182a3e266a721c277fc789d6c06500c`.
Final result `40c26ca0ca266fd9a6da9591013cb2c1d89c81e9174a82372fc7839bac74bc64`.

## Exact commands and results

Windows AMD64, CPython 3.13.12 at `C:/ProgramData/miniconda3/python.exe`.

```powershell
git status --short --branch
git switch -c codex/ra003-detached-metadata-loader
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path[:0]=['.','tests'];r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromName('test_detached_metadata_loader'));raise SystemExit(not r.wasSuccessful())"
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-detached-metadata-loader -ErrorAction Stop | Out-Null
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-detached-metadata-loader/qualify.py
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-detached-metadata-loader-v2 -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath private/sessions/20261020-RA-003-detached-metadata-loader/qualify.py -Destination private/sessions/20261020-RA-003-detached-metadata-loader-v2/qualify.py -ErrorAction Stop
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-detached-metadata-loader-v2/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import subprocess,sys;r=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','tools/detached_metadata_loader.py'],capture_output=True,text=True);print('CLI child exit:',r.returncode);raise SystemExit(0 if r.returncode==2 and not r.stdout and not r.stderr else 1)"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-detached-metadata-loader-v2/record.py
git diff --check
```

All checks/wrappers exit 0; direct CLI child intentionally exits 2 with empty output. Standard-library stdin verifier recomputed 113 pins and log digest, exit 0. Qualification uses one captured prior authored fixture qualifier after fixed hash verification; no upstream code or private payload is executed. Logs/results and backups are created exclusively. Reviewed eight-path staging, staged content/path/whitespace inspection and topic commit follow; source lock unchanged.

Changed public files: tools/detached_metadata_loader.py, tests/test_detached_metadata_loader.py, this report, research/STATE.json, research/PRE_CAMERA_READINESS.md, docs/BACKLOG.md, docs/CODEX_HANDOFF.md and docs/FEATURE_PROGRESS.md. Private session and per-feature notes updated after exclusive backups.

Loader/audit bootstrap, independent review/owner authority, fresh source/dependency origin and activity-specific rights are still unresolved; owner inspection-rights answer remains **No / unknown**. No operational activation record or stronger legal conclusion follows. Exact-body correspondence, English restriction/resources, native Wi-Fi FTP implementation/direct-server evidence, complete backup coverage and usable rollback remain unverified. English/native FTP first; FL2/FL3 deferred, calibrated looks separately later; optional bridge HOST-ASSISTED.

Camera commands: **none**. No firmware/constants/saved raw stream/native payload reads, installed dependency activation, upstream launchers, download/upload, driver/firmware changes or feature/recovery/device-write gate.

Next single package: **RA-003: implement, independently review and qualify a no-site disposable host entry that captures the metadata loader and source-audit helper bytes against an external review anchor before executing them, then invokes the checked fourteen-public/eleven-retained validator composition on invented metadata only. Bind exact startup argv, source origins and import policy; observe startup/cleanup and refusal behavior without claiming complete interpreter/stdlib trust. No actual activation records, installed dependency activation, firmware/constants/native payload reads or camera; operational runtime remains disabled.**
