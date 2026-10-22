# FT-101 source-chain session — 2026-10-22

Baseline: clean `826afda`; topic branch `codex/ft101-source-chain-20261022`.
Previous goal turn: **progress** — published-source update changed the available
FTP research route. This turn: **progress** — traced the source chain, verified
bindings/mappings and identified concrete cancellation/cleanup and journal gaps.
The full pre-camera goal remains active and incomplete. No blocked or complete
goal transition is warranted by this new evidence.

[Full source-chain findings and acceptance matrix](../FTP_SOURCE_CHAIN_AUDIT.md).
Native English and native Wi-Fi FTP remain priorities. This is R0 host work.
Camera commands: **none**. Feature support, recovery and device-write gates:
**not passed**. Old GDT pending decisions and frozen source/input records are
unchanged; no protected firmware processing occurred.

## Exact substantive commands and results

Host interpreter: `C:/ProgramData/miniconda3/python.exe`, CPython 3.13.12,
Windows AMD64. Acquisition and checking scripts are authored locally; upstream
Python was parsed, never imported. Commands ran from the repository root.

```powershell
git status --short --branch
git log -1 --oneline
git switch -c codex/ft101-source-chain-20261022
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-ft101-source-chain/acquire.py
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-ft101-source-chain/check_source_chain.py
```

All exited **0**. Eighteen allowlisted immutable public text GETs, each HTTP200,
no redirects/retries, bounded bytes and exact Git blob checks. Saved by exclusive
creation. No binaries, installers, firmware or protocol-constant module fetched.
The combined offline checker verified **44 blobs / 19 ASTs**, three canonical
bindings, 355 exactly-once nonoverlapping field mappings, 260 sparse sectors,
FTP 89 App + 151 WBI changed bytes across 82 sectors, one shared target sector
and zero volatile exclusions. These are static data checks, not upstream test
passes, target semantics, supported-layout or hardware results. Native/USB test
source was inspected but not run. No new runtime dependencies were installed.

Three independent local reviewers inspected feature requirements, host failure
handling and native transaction source. Their findings were reconciled against
the pinned source: masks cover available features, not parked ones; rollback
is whole-sector/in-process; uncertain cleanup differs by CLI versus retained
desktop session. No review agent contacted a camera or executed upstream code.

## Remaining prerequisites

Exact mainland installed-build/ABI and pre-execution identity; native FTP worker,
media/event/network/security chain; source-to-binary reproducibility; owner
rollback requirement including interrupted/failed-boot states; safe cancellation
and durable unresolved-operation reconciliation. Full underlying author test
records are absent from the pinned tree. Host-only consistency does not close
any of these gaps. No missing generic intake question was repeated.

Next single package: **FT-101 host USB takeover/session-lifetime source audit**
for the macOS capture helper and desktop bridge/worker exception paths, followed
by a pre-contact go/no-go matrix tied to F1/F3 in the audit. No device execution.

## Notes, review and commit

```powershell
C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261022-ft101-source-chain/update_progress.py
git diff --check
git check-ignore private/sessions/20261022-ft101-source-chain/receipt.json private/session-state.json private/feature-progress.json
git add -- docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md docs/FTP.md references/sources.lock.json research/PRE_CAMERA_GAP_AUDIT.md research/PRE_CAMERA_GAP_LEDGER.json research/STATE.json research/FTP_SOURCE_CHAIN_AUDIT.md research/sessions/20261022-FT-101-source-chain.md
git diff --cached --check
git diff --cached --stat
git diff --cached --name-only
git commit -m "docs: audit pinned FTP source chain and failure handling"
git status --short --branch
```

Progress synchronization/preservation assertions, JSON serialization, ignore
checks and whitespace checks exited **0**. The authored updater retained exact
before-images privately and checked that device/recovery/activity flags did not
change and public/private next-step summaries agree. Source code under tools/
and tests/ was unchanged; no behavioral suite was rerun for these documentation
changes. The ten explicitly named public files were reviewed before staging.
Public/private feature notes now record the concrete source gaps. Fetched
reference texts, raw receipts and private state remain ignored. No push,
external issue or other submission was made.

Changed public files: `FTP_SOURCE_CHAIN_AUDIT.md`, this session report,
`STATE.json`, `PRE_CAMERA_GAP_LEDGER.json`, `PRE_CAMERA_GAP_AUDIT.md` under
research/; `sources.lock.json` under references/; and `BACKLOG.md`,
`CODEX_HANDOFF.md`, `FEATURE_PROGRESS.md`, `FTP.md` under docs/.
