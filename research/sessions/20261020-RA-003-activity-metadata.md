# RA-003: activity, history and qualification metadata

2026-10-20; branch `codex/ra003-activity-metadata`, base `0aacf04`.
Evidence: **offline-tested**, **static-inference**.

## Result

New pure `tools/dependency_activity_metadata.py` checks activity scope, activity rights, historical-evidence index and qualification index, then composes the previous ten-role validator on the same buffers. Full integration calls the actual retained validators without stubs. Fourteen invented role contracts now have checks; no unimplemented ordinary role contract remains. This is not a statement of complete semantic truth, freshness, execution readiness or feature support.

The activity record binds the frozen scope bytes and limits, protected identity labels, source manifest/receipt digests, source/dependency anchors and all historical blockers. Its purpose is offline metadata qualification. Numeric limits use canonical JSON comparisons so bools cannot replace integers. The rights record binds the activity's original bytes, preserves China/personal/noncommercial owner facts and **No / unknown** inspection rights, retains every uncertainty as unresolved, and requires decision pending/legal basis false/execution false. This records uncertainty; it does not determine law or grant inspection rights.

The existing historical index keeps its closed comparison-only schema, full historical roster and original-buffer receipts. Its new external activity anchor binds the original index bytes. The qualification index binds all thirteen other ordinary records (never itself), all 44 source buffers, five expressly supplied validator buffers and two invented result/log artifacts. The result binds source/validator receipts, opaque original log bytes, operation, claimed fourteen-role coverage, and exact externally selected positive test count with zero failures/errors/skips and exit 0. The external anchor binds four ordinary records, both artifacts, validator receipts and source/dependency anchors. All current sidecar operations must agree.

These are caller-pinned consistency claims. Arbitrary inert validator text and opaque logs can pass when the caller reanchors consistent records; a dedicated boundary test preserves this limitation. The five supplied validator buffers are neither complete helper closure nor proof of the functions executing in this process. No qualification log parser, independent reviewer identity, observed startup/source origin or freshness is provided. The index's claimed test count (seven in the invented fixture) is distinct from this session's actual 156-test result. Matching hashes are not permission. All output authority, rights, freshness, source-observation, recovery and feature/write flags remain false. Candidate-to-operation binding, complete semantics and legacy dependency bridging remain explicitly false.

The forward record graph is acyclic: activity scope refers to source/dependency anchors; rights refers to scope; result refers to sources/validators/log; index refers to the thirteen other ordinary roles and artifacts; the separate activity anchor binds those records. No current authority envelope document is accepted as an external expectation digest. Direct CLI exits 2; runtime API refuses.

## Verification

**156/156 passed**, zero failures/errors/skips, exit **0**, **21.50462169997627s wrapper / 21.481s suite**. Composition: **127 retained + 25 new public + 4 new private integration tests**. The prior three invented-file I/O tests were not rerun; their accepted evidence remains in the earlier report. **99 source/test/fixture/scope/lock pins** stable. Installed Crypto/Cryptodome/cffi alias list empty. No real inputs or installed dependency activation.

New tests cover scope widening, bool/integer confusion, wrong source/protected labels, blocker loss, rights promotion, missing history and index roles, self-index receipt, qualification count/type/coverage/authority errors, log/source/validator drift, operation mismatches, unknown fields, actual mode, bounded buffers and refusal before retained owned execution. The four full integration tests prove fourteen-role composition without stubs, frozen-source refusal despite rebinding all new claims, unchanged legacy plan blocker enforcement and dependency refusal before retained source execution. The test harness captures the previous authored qualifier once, verifies fixed SHA-256 `ede0f0781efe3344359b1da9aed8f67954f20822be5e20c3540568303b35fdeb` and compiles those exact bytes in a detached module. It reads ordinary authored Python texts and the previously pinned explicitly invented basis JSON only. Protected validator/capture/core source texts are hashed/AST-checked, not executed. No firmware/constants/native payload or saved stream is opened.

Qualification log SHA-256: `dee544cd227d033d9daa5378b2a07adc19ee41313cee0c506b8cce148ed88d65`.
Module SHA-256: `a0ac2a33275ee5cf70af82d18aef88b952e9d7f139e50ff68c85073db96022e2`.
Public test SHA-256: `fcd88c90d7e0b2e6591d96f36dc6a2ed66e0dea001120d6e15d22a91079fd39a`.
Qualifier SHA-256: `c7259c50fd267d1d1f13b2e7f73c39b2c87070f321d9ac494b255124732f52f6`.

## Exact commands and results

Host: Windows AMD64, CPython 3.13.12 at `C:/ProgramData/miniconda3/python.exe`.

```powershell
git status --short --branch
git switch -c codex/ra003-activity-metadata
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path.insert(0,'.');sys.path.insert(0,'tests');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('test_dependency_activity_metadata'));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-activity-metadata/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_activity_metadata.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import subprocess,sys;r=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','tools/dependency_activity_metadata.py']);print('Direct CLI child exit:',r.returncode);raise SystemExit(0 if r.returncode==2 else 1)"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-activity-metadata/record.py
git diff --check
```

Branch/status commands exit 0. Preliminary public invocation before final added cases: 19/19, exit 0, 2.980s. Accepted focused qualification: 156/156, exit 0 as above. PowerShell tool reported host exit 1 for direct CLI refusal; separate subprocess wrapper observed the intended child exit 2 and exits 0 itself. No test failure was hidden. A standard-library stdin verifier recomputed all 99 source pins and log hash, exit 0. Logs/results created exclusively; historical full suites not repeated. No acceptance threshold changed.

Changed public files: new module, new public tests, this report, docs/BACKLOG.md, docs/FEATURE_PROGRESS.md, docs/CODEX_HANDOFF.md and research/STATE.json. Private session and feature notes updated after exclusive original-byte backups. Stage only these seven reviewed files; private material remains untracked/ignored. Previous goal turn was progress (ten-role composition finalized); current turn is progress (remaining four contracts implemented and all fourteen composed). Full pre-camera objective remains active.

## Remaining prerequisites

Legacy dependency-plan/successor packet compatibility, current candidate-to-operation authority, complete execution/bootstrap helper closure and ownership, actual startup, independent expectation/review/owner authority, freshness and activity-specific rights remain unproved. Existing exact-body correspondence, native English, native Wi-Fi FTP and practical rollback/recovery are unverified. Completing invented role contracts does not close these prerequisites or authorize an actual activation packet.

Camera commands: **none**. No camera, firmware/constants/native payload/saved raw stream reads, upstream launcher, installed dependency activation, download, upload, driver or firmware change. English and native FTP remain primary; FL2/FL3 and later calibrated looks deferred; any optional bridge remains host-assisted.

Next single work package: **RA-003: derive, implement and independently qualify a source-only compatibility contract between the retained legacy dependency plan and successor dependency packet/fixed expectations. Explicitly reject unsupported version, source mapping, cache/native policy and operation correspondences; preserve independent authority, exact bootstrap closure, freshness and startup as separate unmet prerequisites. Invented records and authored source texts only; runtime disabled, no protected inputs or camera.**
