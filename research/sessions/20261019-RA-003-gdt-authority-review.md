# RA-003: v2 authority pins and source review

2026-10-19. Branch `codex/ra003-gdt-authority-review`, base `c3e41e493debfec08c7562d8ec11a2d97868e21f`. Starting tracked tree clean. CPython **3.13.12**, `C:/ProgramData/miniconda3/python.exe`, Windows 11 AMD64, PowerShell 7.6.5. Previous goal turn **progress**; this turn **progress**, no-progress count zero. Broad pre-camera goal remains active.

The v2 entry now binds **18 reference hashes**, derived from preserved ordinary authorities. The missing historical qualification-review hash was verified through its already pinned review record. **105/105 invented-data tests passed**, zero skips, exit **0** (81 retained + 24 new). Same-agent source/AST and saved-metadata checks reconciled the nine-role basis, 26 authored roles and 47 cached sources. Independent operational review and actual bootstrap/GDT execution remain pending; English/native FTP and rollback remain unverified.

## Exact commands and results

Repository-root PowerShell:

```powershell
git status --short --branch
git switch -c codex/ra003-gdt-authority-review
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-authority-review/build_reference_policy.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-authority-review/qualify_001.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-authority-review/audit_source_bindings.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-gdt-authority-review/publish.py
git -c core.safecrlf=false diff --check
git diff --stat
git -c core.safecrlf=false add -- README.md docs/ARTIFACT_INTAKE.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/STATE.json research/GDT_OUTER_AUTHORITY_REVIEW.md research/sessions/20261019-RA-003-gdt-authority-review.md
git -c core.safecrlf=false diff --cached --check
git diff --cached --name-only
git diff --cached
git commit -m "docs: record v2 authority pins and source binding review"
git status --short --branch
```

Reference-policy builder: exit **0**, **18 pins**, **22 ordinary source/metadata files** verified against preserved direct/transitive authorities. It reads the authored old gate as AST only and follows no protected path. New implementation is copied into this new ignored session; the old 81-case implementation remains byte-identical.

Bounded qualifier: exit **0**, **105/105**, zero skips, **1.804s** suite / **2.154294900s** wrapper. Exact child argv is `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8` followed by this session's absolute `test_outer_v2.py` path. Deadline 60 seconds, monitored 4 MiB combined-log threshold, one terminate/wait five seconds then one kill/wait five seconds if necessary. No limit event or termination occurred. Monitoring is not a strict output-storage cap. Eight source/helper/scope hashes stayed stable. Raw logs, unique case identities, timings and pins remain private. Only invented-data tests ran; no actual bundle was constructed.

Source-binding audit: exit **0**, same-agent manual source trace plus AST/ordinary-data predicates, **220** historical preservation entries and **139** starting paths unchanged before publication; **47** cached source rows / **813,391 bytes**, nine basis roles and 18 entry-owned reference pins reconciled. The audit imports/executes only the pure authored validator. It does not import/execute production entry/factory or installed dependencies. A separate inline standard-library check normalized all 105 unique pass IDs and eight source pins into qualification-result.json and qualification-review.json; exit **0**, both preserve execution/ready false. Inline baseline/copy, AST extraction and source-edit commands and outputs are retained in task history and private before/provenance records. No failed qualification, replay or relaxed acceptance predicate this turn.

## Changed files, limitations and next package

Eight reviewed public files: README.md, docs/ARTIFACT_INTAKE.md, docs/BACKLOG.md, docs/CODEX_HANDOFF.md, docs/FEATURE_PROGRESS.md, research/STATE.json, research/GDT_OUTER_AUTHORITY_REVIEW.md and this report. Four private progress/intake files updated with snapshots preserved. New private implementation, fixtures, scripts, qualification and provenance records remain ignored. No push or history rewrite.

The earlier missing-review baseline lookup is resolved by a transitive check: the preserved preparation-chain review contains the old qualification-review hash. The pinned old gate source, inspected through AST without executing it, supplies historical scope/rights and role/schema hashes. Twelve other document hashes derive directly from preserved records. The eighteenth pin covers the dependency configuration, canonicalized with only operation_id removed; package paths, eleven Python origins, five native rows, five trusted origins and vectors remain fixed. Candidate consistency alone cannot replace this entry-owned policy. The pure validator now requires the reference policy argument with no default.

Twenty-four new tests cover seventeen independently resealed reference substitutions, native/vector profile substitution, missing/extra policy keys, omission of the mandatory argument, acceptance of the unchanged policy and permitted operation-ID rebinding. The 105 cases retain the prior 81, including twenty direct completion-receipt cases. None of the historical 811, integration 51 or snapshot 20 suites was rerun or added to 105.

Source review traces all six migration requirements: no-site argv/startup; new operation/session authority; exact dependency profile and preservation of old blockers; nine-role basis and separate qualifications; durable receipt-before-callback, live guard and owned cleanup; separate scope/rights/decision/review/seal. The source/AST audit reconciles 18 entry constants, full basis/source identity, 26 roles (23 eager/three protected), interpreter path and production wiring without injected runtime readers/backends. It executes only the pure source-cache validator on saved ordinary data: 47 cached rows / 813,391 bytes. It does not call validate_bundle on saved inputs, import the actual entry/factory, or create activation records.

The raw qualification was separately normalized into source-bound qualification result/review records. That review is same-agent, not independent operational review. No execution decision, actual candidate or activation review/seal was produced. Reviewer-name inequality cannot prove independence or legal correctness. Exact full startup is compared in the live child; the host performs its initial flag checks. Initial bootstrap reading/loading and actual complete host/child/protected integration still lack end-to-end runtime qualification. OS-mapped bytes, transitive native closure and filesystem races are not established.

All 220 inherited preservation entries, all 139 starting paths before publication and eight qualification pins matched. Prior implementations and results remain unchanged. Existing research rationale and contract/component/constants uncertainties remain unchanged. Exact-body/build correspondence, English restriction/resources, native FTP backend/ABI/network/media/lifecycle and verified two-copy backup/rollback/recovery remain unresolved. English/native FTP stay first; FL2/FL3 deferred and custom looks separately gated. No filesystem validity, feature support, recovery or device-write gate passes.

Next single package: **RA-003: independently review the frozen v2 gate, source bindings and 105-case qualification, resolve findings, and specify the exact later metadata act; no GDT replay before that review passes**.

Local review-subagent authorization was requested because the session's multi-agent rule requires explicit user authorization before spawning reviewers; no subagent was spawned in this package. This is a workflow prerequisite to that review method, not an additional camera or firmware licence requirement.

Camera commands: **none**. Firmware/constants/raw-prefix/native payload reads, installed dependency execution, actual GDT replay, device access/write, upstream launchers, driver/service changes, network/download/install/agreement and private uploads: **none**.
