# RA-003: invented authority document envelope

2026-10-19 host session; branch `codex/ra003-authority-grammar`, starting commit
`c496b2f`. Evidence: static-inference and offline-tested. Camera commands: **none**.
English and native Wi-Fi FTP remain first; FL2/FL3 deferred. No feature/recovery/write gate passed.

The previous goal turn refreshed an unchanged reference, with no progress on the
shared protected-analysis path. This turn reconciled the unfinished scope work
and implemented a concrete original-byte document validator. The overall goal
remains active; this is partial authority/input grammar work.

## Behavior and boundaries

`tools/dependency_authority_grammar.py` is a pure supplied-buffer validator.
It has no filesystem, network, subprocess, upstream or device operations.
It checks a closed four-document graph: candidate, review, decision and seal.
Review binds original candidate bytes; decision binds candidate/review bytes;
seal binds all three. An external caller-supplied seal digest closes the graph.
There are no reverse/self edges or extra fields. This proves consistency with
that supplied anchor, not independent reviewer identity, rights or human consent.
Reformatted original bytes require new binding even when JSON values are equal.
Duplicate JSON keys, nonfinite numbers (including overflowing exponents), unknown
schemas, fields and rosters refuse. Documents and individual buffers are bounded
to 2 MiB each; this is not an aggregate process-memory cap.

Prepared and operational-shaped invented documents have separate decision
outcomes (`pending` / `accepted_shape`). Both require `invented: true`, and every
returned execution/feature/recovery/write flag remains false. Actual operational
schemas are rejected. Direct isolated CLI exits 2 before project imports;
`run_runtime` always refuses. No executable actual activation packet was created.

The candidate binds 44 source-role buffers (43 child comparison labels plus host),
14 ordinary buffer receipts, and two protected identity labels. Protected bytes
are not an API argument and reads remain unauthorized. The historical index
binds original bytes of all 16 historical-only roles with comparison-only purpose.
All 17 historical blockers and five rights uncertainties remain explicit.
Scope bytes are independently checked by the unchanged migration policy.

**Remaining semantic boundary:** ordinary records other than the historical
index are opaque byte receipts. The validator does not yet parse the nine-role
basis, current source/prerequisite/dependency records, qualification index, or
activity-specific rights assessment. Separate namespaces do not establish
freshness: rebinding invented historical bytes into an ordinary role can pass
this envelope. An explicit passing test records that limitation. Candidate
source pins are not required to equal historical comparison pins: replacements
are planned. Interpreter identity/argv are supplied strings, not observed runtime
identity or bootstrap/source correspondence. These gaps require the next package;
this envelope cannot replace the operational gate.

The source reviewer identified an overbroad test name suggesting freshness proof.
It was renamed to describe historical receipt mismatch and blocker removal;
the limitation was documented and a boundary test added. No acceptance threshold
was weakened. Initial and final logs are preserved privately. Source review is
distinct from test execution and is not an execution decision.

Independent reviewer `gate_review` accepted the corrected final source/test
delta and checked all seven saved hashes, the raw log digest and 45 individual
passing outcomes. No reviewer executed code or accessed actual inputs.

## Exact commands and results

Interpreter: CPython 3.13.12, Windows AMD64,
`C:/ProgramData/miniconda3/python.exe`.

- `git status --short --branch`: identified staged scope work plus unstaged reference notes; preserved all content.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 -c "import ast,hashlib,json,pathlib; p=pathlib.Path('private/sessions/20261019-RA-003-operational-scope'); r=json.loads((p/'review-receipt.json').read_text()); old=(p/'policy.before-eof-format').read_bytes(); now=pathlib.Path('tools/dependency_operational_scope.py').read_bytes(); assert ast.dump(ast.parse(old))==ast.dump(ast.parse(now)); assert hashlib.sha256(old).hexdigest()==r['final_source_sha256']['tools/dependency_operational_scope.py']; pins={k:v for k,v in r['final_source_sha256'].items() if k!='tools/dependency_operational_scope.py'}; assert all(hashlib.sha256(pathlib.Path(k).read_bytes()).hexdigest()==v for k,v in pins.items()); print('EOF-only policy AST equivalence and remaining',len(pins),'reviewed pins verified')"`: exit 0, equivalent AST and 54 remaining pins verified.
- `git add -- docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/STATE.json`; `git diff --cached --check`; `git diff --cached --stat`; `git commit -m "feat: record reviewed operational scope and reference refresh"`: exit 0, commit `c496b2f`, preserving/reconciling the ten previously reviewed files.
- `git switch -c codex/ra003-authority-grammar`: exit 0.
- `C:/ProgramData/miniconda3/python.exe -B -m unittest tests.test_dependency_authority_grammar tests.test_dependency_operational_scope tests.test_dependency_outer_contract -v`: initial 43/43 passed, exit 0, 0.182s; before additional bounds/freshness-limit tests.
- `New-Item -ItemType Directory -Path private/sessions/20261019-RA-003-authority-grammar -ErrorAction Stop`: success, exclusive evidence directory.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-authority-grammar/qualify.py`: intermediate 44/44 passed, zero skips/errors/failures, exit 0, 0.256326s; seven pins stable.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 tools/dependency_authority_grammar.py`; `Write-Output "grammar_cli_native_exit=$LASTEXITCODE"`: native exit **2**, no tool output.
- `New-Item -ItemType Directory -Path private/sessions/20261019-RA-003-authority-grammar/final -ErrorAction Stop`; `Copy-Item -LiteralPath private/sessions/20261019-RA-003-authority-grammar/qualify.py -Destination private/sessions/20261019-RA-003-authority-grammar/final/qualify.py -ErrorAction Stop`: success, fresh exclusive outputs.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-authority-grammar/final/qualify.py`: **45/45 passed**, zero failures/errors/skips, exit **0**, **0.211134s**. Seven source/test/packet hashes stable. Composition: 22 new + 14 scope + 9 outer contract cases. No actual input or installed dependency activation; historical full suites not rerun.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-authority-grammar/record.py`: native exit 1 while parsing proposed JSON, after report/note creation and before JSON mutation. A text-splice expression lost a delimiter; prior JSON remained intact. No test code or thresholds changed.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-authority-grammar/repair_record.py`: exit 0. Reconciled existing outputs, verified public state still matched its saved backup, made new exclusive backups, and updated three JSON records through structured serialization; no duplicated note append. Both scripts and initial diagnostic retained privately.
- `git diff --check`; `git diff --cached --check`: whitespace/staging checks, no camera effect.

Final raw log SHA-256: `a7375abb3f7920c0617c15218c0a36de5039576d90b51d60805de5add9506a17`.

## Changed files and prerequisites

New module, `tests/test_dependency_authority_grammar.py`, this report,
`research/STATE.json`, `docs/BACKLOG.md`, `docs/CODEX_HANDOFF.md` and
`docs/FEATURE_PROGRESS.md`. Private source-review/test receipts and session/feature
notes are ignored, backed up without overwriting prior evidence. Source lock,
comparison packet and frozen predecessors unchanged. No firmware/constants/native
payload/private cache read, downloads/uploads, agreement, upstream launch, camera
contact or driver/firmware changes in this package.

Exact-body identity, English resources/restriction consumers, native FTP backend
and direct Wi-Fi behavior, rights/trust assessment, independent backups and
practical recovery remain unresolved. No device gate passed.

Next single work package: **RA-003: implement the role-specific ordinary metadata validators and cross-role bindings for the invented authority envelope, starting from the fourteen-role migration roster and existing pure preflight contracts. Distinguish historical comparisons from fresh current basis/source/prerequisite and dependency records; derive interpreter/bootstrap/source ownership requirements. Independently review and qualify changed-role/stale-evidence/refusal cases using invented documents only. No actual activation records, dependency activation, firmware/constants/native payload reads or camera; runtime remains disabled.**
