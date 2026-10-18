# Owner intake: mainland version and English absence

Date: 2026-10-18. Scope: host-only documentation/JSON continuity update.
Evidence basis: `320a3efdfc5de1f18ffef04bf4ee1fad5a83bf74`.
Topic branch: `codex/en101-mainland-intake`. No remote publication in this session.

## New owner evidence and interpretation

The owner explicitly reports **English is unavailable** and **this is the
Chinese mainland version**. Record both as **source-report**, alongside the
previously reported a6700, version **2.00**, current **简体中文**. This supersedes
the earlier unknown English/market status; the earlier session remains history.

The full offered-language list is not supplied. The earlier full-list-not-checked
answer remains historical; this update does not claim a fresh complete list
inspection. Exact regional SKU/internal product identity, purchase location,
binary/resource identity and unlock feasibility remain unverified. Neither a
single-language-only menu nor absent English resources follows from this report.

EN-101 now follows the restricted-language/resource investigation: distinguish
present-but-restricted English resources from missing/incomplete resources,
then identify any narrow policy and all its consumers before a candidate.
A repeat full-list request is not the immediate prerequisite for recording
English absence. No restriction field, offset, donor payload or service route
has been selected.

English and native Wi-Fi FTP remain primary. Native FTP findings, deferred
FL2/FL3/custom looks and the separate optional HOST-ASSISTED bridge are unchanged.
No requested camera function is validated and no device-write gate has passed.

## Commands, checks and results

All commands ran in the repository root through PowerShell; checks use
CPython 3.13.12, `C:\ProgramData\miniconda3\python.exe`.

| Exact command | Result |
|---|---|
| `git status --short --branch` | Exit 0; clean `codex/ra003-firmware200-intake`, basis `320a3ef` |
| `git switch -c codex/en101-mainland-intake` | Exit 0; new topic branch from the clean basis |
| `python -B -X utf8 private/sessions/20261018-owner-mainland-english/update-intake.py` | Exit 0; 16 current public/private notes updated; no code changed |
| `python -B -X utf8 private/sessions/20261018-owner-mainland-english/verify-intake.py` | Exit 0; 15 check groups passed, 7 tracked JSON files parsed and 105 local Markdown links resolved |
| `git diff --check` | Exit 0; no whitespace errors (existing Git LF/CRLF notices only) |

Before updating current private notes, an exclusive new session directory and
four byte-preserving `before-*` snapshots were created with standard-library
Python; `before.json` records hashes, basis and branch. The local updater and
verifier remain ignored private audit helpers. They do not import or execute
upstream source. Existing private evidence and historical reports are preserved.

The verifier checks source-report semantics, retained unknowns/history,
public/private mirrors, unchanged other features/rights/recovery/qualification,
closed device gates, protected hashes, snapshot hashes, ignored private files,
JSON syntax, changed-path scope and local Markdown links. Independent review
found no material issues; explicit staged-content inspection precedes the commit. No code was changed,
so the previous 154-test qualification and focused 8-test probe results remain
historical; neither suite was rerun for this intake correction.

## Changed files

Reviewed public files:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/ENGLISH_LANGUAGE.md`
- `docs/FEATURE_PROGRESS.md`
- `research/OFFICIAL_PACKAGE_INTAKE.md`
- `research/OFFICIAL_SOURCE_REFRESH.md`
- `research/PRE_CAMERA_AUDIT.md`
- `research/PRE_CAMERA_READINESS.md`
- `research/STATE.json`
- `research/TARGET_EVIDENCE_GAPS.md`
- `research/sessions/20261018-owner-mainland-english.md`

Private current intake/state and both feature-progress files are updated with
their previous bytes preserved locally. None is staged. AGENTS, MASTER_PLAN,
VALIDATION, source/dependency locks and the UNVERIFIED profile remain unchanged.

The reviewed staging command is:

```powershell
git add -- README.md docs/ARTIFACT_INTAKE.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/ENGLISH_LANGUAGE.md docs/FEATURE_PROGRESS.md research/OFFICIAL_PACKAGE_INTAKE.md research/OFFICIAL_SOURCE_REFRESH.md research/PRE_CAMERA_AUDIT.md research/PRE_CAMERA_READINESS.md research/STATE.json research/TARGET_EVIDENCE_GAPS.md research/sessions/20261018-owner-mainland-english.md
git diff --cached --check
git diff --cached --name-only
git diff --cached
git commit -m "docs: record mainland version and English absence"
git status --short --branch
```

Completion results: explicit staging and staged whitespace checks exit 0; the
13 public paths above are the complete staged scope. Commit exit 0; final working
tree clean on the topic branch. No push. The commit identity is retained in
private continuity notes and in the accompanying session response.

## Remaining prerequisites and next single work package

Next single host package: **RA-003 rights-cleared exact-2.00 binary intake and
source/binary correspondence**, blocked on suitable proprietary firmware
inspection rights and legitimate bytes applicable to this exact body/build.
The owner still reports firmware inspection permission **No / unknown**.
The mainland version report does not establish that the previously inspected
UK/JP package metadata or separate OSS sources match the body.

Exact resources/policy, native FTP integration and an approved exact-target
access route remain unproved. History, health/setup, power/media, backup storage
and risk-tolerance facts remain unresolved. The full language list is useful
supporting detail, not the immediate blocker to the reported English absence.

The owner's prerequisite of verified rollback/recovery before firmware writes
remains **not established**. No backup coverage, independently verified copies,
exact-target inverse or failed-boot restore route has been verified.

Camera commands: **none**. Agent camera access/writes: **none**. No network
retrieval, driver/firmware change, upstream launcher/service execution or private
upload occurred in this intake session.
