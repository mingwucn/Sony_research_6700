# RA-003: reviewed factory source gate and source-cache successor

2026-10-19. Topic branch: `codex/ra003-factory-source-gate`.
Evidence: **static-inference**, **offline-tested**. Public-project claims remain **source-report**.

## Result

The successor v4 gate and loader now bind the repaired factory to its separate
29-case contract and eight-case authored-child qualification. The closed proof
also binds the 26 authored roles, child controller, wiring and runtime lineage.
The loader checks all three integration buffers against the validated map before
executing any cached module. Historical 51/162-case evidence is preserved as
historical evidence, not rewritten to certify the successor factory.

**207/207 invented-input tests passed**, zero skips, exit **0**, **4.152s**;
wrapper **4.565525599988177s**. Composition is 188 retained cases, 18 direct
migration/refusal cases and one automatic fixed-reference case. Tests cover
qualification downgrade/substitution, changed source identity, unauthorized
promotion, old bundle schema and refusal before cached-module execution.
All **47** source/specification/evidence snapshot paths remained byte-identical
through this final run; the gate qualification has **15** source pins.
This is gate/loader testing with invented inputs, not full parent/child integration.

A separate one-shot preparation freshly snapshotted **47 ordinary Python sources**,
**814,219 bytes**, with **47 close attempts and 47 EOF probes**. Exactly one source
identity changed: the integration factory, from the earlier 8,500-byte revision
to the repaired 8,861-byte revision. The pure gate accepted the successor's
three integration hashes against saved qualification metadata. The new loader's
fixed cache/receipt hashes now identify this new preparation. Cached dependency
and target module bodies were never executed. The only preparation executables
were authored source-snapshot and pure-gate helpers. No firmware, operational
constants, saved raw prefixes or native payload was opened.

The factory SHA-256 is
`3cd438eb42db7d64c18752fab3580b47915de8ccd2d95efc431fd67fe3b0e08c`.
All **42** prior overlay source/specification pins remain unchanged. Earlier
snapshots, logs and review reports remain additive private evidence.

## Review findings and negative results

Two source reviewers found no new blocker in the v4 gate/loader delta. A separate
collector source review caught a Python-only snapshot helper being used for JSON
metadata, plus unbounded initial self/helper reads. Both were fixed before the
collector ran: exact pinned ordinary metadata/self/helper inputs use the existing
bounded ordinary reader; the Python-only helper snapshots only the 47 Python rows.
Seven invented reader tests passed in **0.037s**, exit **0**, zero skips.
They cover valid JSON, wrong hash, empty/oversized input, hardlinks, directories
and relative paths; no symlink/reparse runtime test is claimed by this seven-case
suite. The test command's raw output is in the host command transcript, without a
dedicated raw log file; its exact source pins and result are saved privately.

The initial collector review's hash was captured after concurrent repairs, while
its findings described the earlier source. Original artifacts remain preserved;
a separate identity clarification explicitly says that initial whole-file hash
is unavailable and that those findings do not apply to the corrected revision.
The final collector re-review pins the corrected bytes independently.

Initial gate development run: **207 cases, 206 passes, one failure**, exit **1**,
**4.240s**. The old bootstrap test expected 25 input reads; adding the explicit
factory-evidence input requires 26. Corrected the assertion to the declared
input roster length, without weakening a gate predicate or acceptance threshold.
Second run: **207/207 passed**, exit **0**, **4.265s**, wrapper **4.635200299962889s**.
After updating the actual cache/receipt references and wrapper source inventory,
the final 207-case run above passed. Each run has its own raw logs and snapshots.

## Requested external-project check

The separately pinned [public-source audit](20261019-RA-003-a6700-powerful-audit.md)
remains the implementation baseline, commit
`0c6294a83988f196adfc980de59f9a1d0b92e8e2`. Refreshed the public README,
development plan, manual and NOTICE through web text reads; no new main-branch
commit or full code tree was pinned by this refresh. The GitHub tree page failed
to fetch through the web tool; raw public Markdown text was accessible.

- **FTP:** the [development plan](https://github.com/xyzhangxin/sony-a6700-powerful/blob/main/开发计划与进展.md)
  reports RAW+JPEG FTP physically verified on the author's a6700 2.00. The
  inspected pinned implementation does not expose a reproducible FTP patch or
  backend invocation. Treat this as an important lead, without establishing
  Wi-Fi transport, relay independence or compatibility with this mainland body.
- **English:** no unlock was located in the inspected pinned text/tree; the
  refreshed feature plan supplies no English enablement result.
- **Rollback:** the [manual](https://github.com/xyzhangxin/sony-a6700-powerful/blob/main/操作手册.md)
  describes partial known-range readback and says physical eMMC capacity and
  complete restoration remain unverified. It does not meet the owner's proven
  rollback prerequisite. RAM injection belongs to R2 temporary native execution.
- **Rights:** [NOTICE](https://github.com/xyzhangxin/sony-a6700-powerful/blob/main/NOTICE)
  grants GPL-3.0-only for authored portions and explicitly does not relicense
  inherited unlicensed Pico source. No implementation or binary was adopted.

English and native Wi-Fi FTP remain first. FL2/FL3 and calibrated custom looks
remain deferred; any host-assisted bridge remains a separate optional result.

## Exact host commands and results

Interpreter: `C:\ProgramData\miniconda3\python.exe`, **CPython 3.13.12**.
Starting `git status --short --branch` showed a clean tracked tree on the topic
branch. Authored PowerShell here-string Python scripts used the same interpreter
with `-I -S -B -X utf8 -` to write additive private evidence, normalize test IDs,
verify all 47 cache bodies' sizes/hashes without executing them, preserve the
42 old pins and update sanitized notes. The final summary cross-check initially returned **1** because its parser duplicated method suffixes in unittest IDs. A corrected additive summary passed the exact 207-ID/source-pin policy check, exit **0**; raw test logs, cases and thresholds are unchanged. Other scripts returned **0**.

```powershell
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-factory-source-gate/test_collector_reads.py
# exit 0; 7/7; 0 skipped; 0.037s

C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-factory-source-gate/collect_sources.py b0250233f647d1072cb057c8bcbb80dc444651410b8ee9803897cfb9a0d19e87
# exit 0; 47 ordinary Python sources; 814219 bytes; collection 0.08319550001760945s

C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-factory-source-gate/run_qualification.py development-001
# exit 1; 206/207; 4.240s; wrapper 4.604876899975352s
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-factory-source-gate/run_qualification.py development-002
# exit 0; 207/207; 4.265s; wrapper 4.635200299962889s
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-factory-source-gate/run_qualification.py development-003
# exit 0; 207/207; 4.152s; wrapper 4.565525599988177s
```

These output-directory commands are historical records, not instructions to
rerun into existing directories. No broader historical suites were rerun.
The qualification wrapper has a 60-second child timeout, but buffers captured
stdout/stderr in memory. The collector's generated-output readback is unbounded;
input byte limits do not establish a whole-process memory limit. File identity
checks do not provide an atomic filesystem snapshot against arbitrary mutation.
Reviewers inspected authored sources/metadata only and executed no tests.

## Changed files, prerequisites and next package

Public changes: this report, README.md, docs/BACKLOG.md, docs/CODEX_HANDOFF.md,
docs/FEATURE_PROGRESS.md, research/STATE.json and a refresh addendum to the prior
external-project audit. Private ignored changes: the v4 authored source/test copy,
reviewed factory evidence, three development records and snapshots, reviewer
artifacts, fresh source/receipt cache and private/session-state.json continuity.
Private source/dependency bodies remain outside Git.

Remaining prerequisites: full parent-process/child composition using the successor
gate; a separately qualified noninjected dependency runtime; complete operational
review and separately frozen metadata-act selection; exact-body correspondence,
feature mapping, applicable rights and proven recovery before any device write.
No actual saved activation bundle was validated or activated, no metadata replay,
no upstream launcher or service tool, no dependency install, no private upload.
English/FTP support, recovery and the device-write gate remain **false**.
**Camera commands: none.** The overall pre-camera goal remains incomplete.

Next single work package: **RA-003: qualify the successor v4 gate, loader and
parent/child composition on invented inputs using the reviewed factory and
prepared source identities; resolve independent review findings before selecting
any actual metadata act.**

## Final review closure

After the cache/receipt reference update, the gate reviewer independently checked the two changed entry hashes, all 47 receipt identities, the final 207 passing case IDs and snapshot stability, with no new scoped blocker. Three distinct source reviewers contributed across gate, runtime and collector scopes; this is not operational acceptance. Final gate-review SHA-256: `5c9c03ae95216a96a9da98dda818eb407275436b42a8b22fc28cb599322822cc`. Corrected qualification-summary SHA-256: `b8120b67cdc1b61e1cb314a3a810f86259c98ebb1f828b44970deae08a96c962`. The earlier summary is preserved and explicitly unaccepted after its ID-parser defect. The final reviewer did not open cached source bodies.
