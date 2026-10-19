# RA-003: authored import closure and bootstrap ownership audit

2026-10-20; branch `codex/ra003-source-closure`, baseline `a7f3b36`. Evidence: static-inference, offline-tested. Previous goal turn was progress: candidate/context checks committed. This turn derives and qualifies the next concrete source-ownership requirements; overall pre-camera goal remains active.

## Source-derived result

The candidate-context path has **14 public authored modules, 22 distinct authored import edges and 1,980 syntactic call sites**. Its separate retained validator path has **11 source modules, 13 authored edges and 1,449 call sites**. All branches, nested functions/classes, decorators and defaults are scanned conservatively. This is a complete static import roster for the accepted syntax and supplied graph, not an observed runtime call graph or complete executing-code closure. Calls are inventories only; aliases/data flow, embedded code strings and transitive external dependencies are not analyzed.

Public dependency-first order: dependency_outer_contract, dependency_operational_scope, dependency_authority_grammar, dependency_basis_links, dependency_basis_recompute, dependency_evidence, dependency_producer, dependency_package_preflight, dependency_execution, dependency_input_semantics, dependency_source_receipts, dependency_activity_metadata, dependency_legacy_bridge, dependency_candidate_context. All are under tools. The function-local package_preflight import is included even though its presence does not show that runtime branch ran.

Detached roots: binding, acceptance, link_acceptance, member_acceptance, metadata_preflight, expanded_gate, ext_superblock, ext_preflight, ext_read_planner, ext_gate, gdt_preflight. These exact source texts match the frozen scope pins. The other fifteen retained roles remain outside this executing-validator roster; no protected validator/capture/core code is compiled or executed. This audit itself compiles or executes none of the inspected 25 modules; only the authored audit helper, test harness and stdlib run.

The new pure audit accepts supplied bytes and explicit expected hashes. It resolves direct imports and from-namespace leaf imports, records external stdlib labels, topologically orders the graph and inventories every AST call expression. It refuses unknown/missing imports, relative/star imports, ambiguous from-authored-leaf symbol imports, bare namespace imports, namespace/leaf overlap or missing namespace parents, case-fold aliases, stdlib-name shadowing, cycles, unused supplied sources, malformed syntax, source/hash rosters and declared size/node limits. Bounds are input-model limits, not a total-process memory cap. Hashes and stdlib names remain caller claims, not independent authority.

## Ownership and bootstrap gaps

| Boundary | Evidence and remaining requirement |
|---|---|
| Ambient tools namespace | No tools/__init__.py exists. Do not invent or pin it. Namespace portions, search paths, import finders/hooks, preexisting modules and package attributes are not owned by current source hashes. |
| Public metadata helpers | Current ordinary imports can resolve preloaded modules. Exact captured source bytes must be tied to the live functions, defaults/closures/globals and owned import semantics before a stronger execution claim. |
| Retained preflight loader | basis_recompute has AST compile at line 80, builtin import dispatch at 99, module execution at 112 and getattr dispatch at 127. Its local eleven-module ownership does not cover ambient public helpers. |
| Latent dependency engine | producer has installed-source compile/exec at 217, dynamic TRUSTED imports at 289, and Cryptodome imports at 324/326. Presence is recorded; none was activated. These source sites cannot be promoted to an approved dependency or firmware operation. |
| Interpreter and stdlib | The observed Python path/version and -I -S -B -X utf8 flags do not authenticate executable bytes, startup state, environment, stdlib origins, builtins, native extensions or transitive imports. sys.stdlib_module_names supplies classification labels only. |
| Audit/expectation trust | Audit helper/harness and expected source policy need independent, noncircular review and capture. Even matching source hashes can differ from already imported live code. This audit is not a sandbox or an operational allowlist. |

Direct public external imports: ast, builtins, copy, hashlib, importlib, importlib.abc, importlib.util, json, math, ntpath, os, pathlib, stat, sys, types, unicodedata. Detached external imports: ast, base64, copy, csv, functools, hashlib, io, json, math, re, stat, unicodedata, zipfile. Their source/native transitive closure and actual origins are not verified. All ownership/startup/activation flags remain false. No new rights determination; owner firmware-inspection rights answer stays **No / unknown**.

## Qualification and exact commands/results

Windows AMD64, CPython 3.13.12 at `C:/ProgramData/miniconda3/python.exe`. Final **26/26 passed**, **19 invented-buffer public cases + seven current-source AST integration cases**, zero failures/errors/skips, exit **0**, **0.6050325999967754s wrapper**. All **30 pins** stable. No inspected public/detached source module or installed crypto/native package was imported. Prior 203-case qualification remains preserved, not rerun.

Integration proves the 14/11 static inventories, dependency-first ordering, separate namespaces, omitted producer and required retained acceptance refusal, actual compile/import call-site visibility, byte-drift refusal and absence of inspected modules/dependency aliases from sys.modules. It does not execute candidate validation or inspect private payloads. Public cases cover supplied-source nonexecution, conditional/nested imports, all declared roster/ambiguity guards, alias-call inventory limits, decorators/bases, cycles, bounds/syntax and authority false flags.

```powershell
git status --short --branch
git switch -c codex/ra003-source-closure
New-Item -ItemType Directory -Path private/sessions/20261020-RA-003-source-closure -ErrorAction Stop | Out-Null
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import sys,unittest;sys.path[:0]=['.','tests'];r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromName('test_source_import_audit'));raise SystemExit(not r.wasSuccessful())"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-source-closure/qualify.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import subprocess,sys;r=subprocess.run([sys.executable,'-I','-S','-B','-X','utf8','tools/source_import_audit.py'],capture_output=True,text=True);print('CLI child exit:',r.returncode);raise SystemExit(0 if r.returncode==2 and not r.stdout and not r.stderr else 1)"
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261020-RA-003-source-closure/record.py
git diff --check
```

Preliminary public runs: 16/16 exit 0 (0.010s), then 19/19 exit 0 (0.012s) after explicit namespace-parent/leaf-symbol ambiguity cases were added. No initial test failure or weakened threshold. One exploratory rg glob was invalid on Windows (123); corrected with -g dependency*.py. Get-ChildItem tools/__init__.py returned missing/1; this negative observation establishes the explicit namespace-package gap, not a test error. Other commands and checking wrappers exit 0. Direct CLI deliberately exits 2 with empty output. Stdlib stdin verifier checks source/log/inventory hashes and counts, exit 0. All qualification outputs created exclusively; no rerun over them.

Log SHA-256 `ba7b6783ef03771dd4e0d11cca42b20e42be5818fd483580f24a02fc1e0b63d5`.
Private static inventory SHA-256 `03fdb2809a8f51435f65a762b3c0ebcd75ef33440abb37f0574f3a7aa9adf943`.
Audit helper SHA-256 `c113ba9ea40e8a898f20d8bcdd0831b896b8e9548e64711cb3ae969b0e27f5ba`.
Public tests SHA-256 `26114ddb49e7409bfe2e5c5cc901f79c480ed6af04b78381976322f3ac5539d9`.
Qualifier SHA-256 `7ebd8b6fec0cff60aed178730429146450ca1cb97fe366b6fa9dc7b16ad868ef`.
Result SHA-256 `4ff92b2e86f963c471a3ae68cbddb93d17f42051028351cd1d0b4687bb6ccee2`.

Independent source-only review derives the same 14/11 rosters and bootstrap gaps. Final implementation/evidence review is recorded before commit. Explicit eight-file staging and staged path/content/whitespace inspection required; no git add dot. Changed public files: tools/source_import_audit.py, tests/test_source_import_audit.py, this report, research/STATE.json, research/PRE_CAMERA_READINESS.md, docs/BACKLOG.md, docs/CODEX_HANDOFF.md and docs/FEATURE_PROGRESS.md. Internal session and per-feature notes updated after exclusive backups; source lock unchanged.

Final source-only implementation/evidence review accepted this conservative static scope with no material finding; independently verified all 30 current pins, 26 individual successful log outcomes (0.598s suite), both graph sizes and all declared authority limitations. Reviewer performed no execution or protected-input reads.

English/native FTP remain first. No English-resource or native-FTP backend discovery, exact-body correspondence, backup coverage, rollback/recovery or feature/device-write gate follows from this static inventory. FL2/FL3 deferred, calibrated looks separately later, optional bridge HOST-ASSISTED. Camera commands: **none**. No firmware/constants/raw stream/native payload reads, installed dependency activation, upstream execution, downloads/uploads or driver/firmware change.

Next single package: **RA-003: implement and independently qualify an exact-buffer detached loader for the derived fourteen public metadata-validator modules, composing their existing eleven-module retained preflight path on invented inputs only. Validate the entire expected source roster before execution; explicitly bind from-tools import semantics, preserve foreign sys.modules entries and detect live module/function mutation before and after calls. Separate interpreter/stdlib bootstrap trust from authored ownership. No actual activation, dependency activation, firmware/constants/native payload reads or camera; operational runtime stays disabled.**
