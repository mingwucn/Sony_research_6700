# RA-003: official package, bounded identification and statutory route

Date: 2026-10-18. Basis: `3ef8bb9ef75979e852bfe00201196385bdca2d9f`.
Topic branch: `codex/ra003-package-law`; initial working tree clean.

## Results and limits

The owner separately approved one request to the reviewed Sony redirect
destination. The frozen local helper made one GET: **HTTP 200, exit 0,
1,024,017,848 bytes**, matching Sony's declared size. Transfer and stored-file
SHA-256 values agree:

```text
d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c
```

No further redirect or retry occurred. The earlier HTTP 302/zero-byte stopped
request and both consent snapshots remain intact. Raw firmware stays ignored,
private and untracked. A reversible Windows read-only attribute was set;
size/mtime remained unchanged. This is not tamper-proof immutability, an
independent backup or a recovery test. No Sony reference SHA-256 was observed;
local equality is not independent authenticity or installed-build equivalence.

The existing authored probe read the file for size/hash and classified at most
4,096 prefix bytes from that same read: **exit 0**, **1.609954 seconds**,
`sony_ufu_signature_candidate` / `container_not_validated`. Its SHA-256 agrees
with acquisition. Output remains **UNVERIFIED**, identity not inferred. No
chunk traversal, component extraction, decompression, decryption, disassembly,
loader, upstream import or firmware execution occurred. Paths/raw prefixes are
omitted from the probe JSON; the exact input argv is retained privately.

The [updated dossier](../MAINLAND_FIRMWARE_SOURCE.md) records an important
addition to the China review: Copyright Law **Article 50(5) expressly addresses
software reverse-engineering research**, with conditions. Four official public
law/commentary pages were captured as inert text, one request each, HTTP 200.
This strengthens the statutory route; the accepted terms and exact later acts
still require assessment. Written Sony permission is not the only possible
basis. No bypass procedure or full proprietary-analysis permission is declared.

Evidence: public-law/offer/consent facts are **source-report**; implications for
later research scope are **static-inference**; the actual authored bounded probe
is **offline-tested**, solely for its recorded output. No device evidence exists.
The limited court search did not locate a directly applicable firmware-analysis
holding; two targeted SPC follow-up accesses timed out. That search does not
establish that no relevant authority exists. Failed NPC PDF/government web opens
are not treated as inspected sources; the successful NCAC/NSFC texts support the
statutory finding.

English and native camera-to-server Wi-Fi FTP remain first. No English resource,
restriction consumer or native FTP backend/lifecycle is validated. FL2/FL3 is
deferred; custom still looks remain later and separately gated. The optional
HOST-ASSISTED bridge remains separate. Recovery is unestablished and no device-
write gate has passed.

## Exact commands and checks

PowerShell 7.6.5; **CPython 3.13.12** at
`C:\ProgramData\miniconda3\python.exe`. Repository-root commands:

```powershell
git status --short --branch
git log -1 --format="%H %s"
git switch -c codex/ra003-package-law
python -B -X utf8 private/sessions/20261018-RA-003-cn-scope/acquire-redirect-only.py --consent-record private/sessions/20261018-RA-003-cn-scope/redirect-download-consent.json
python -B -X utf8 private/sessions/20261018-RA-003-package-law/capture-law.py
python -B -X utf8 private/sessions/20261018-RA-003-package-law/run-bounded-probe.py
python -B -X utf8 private/sessions/20261018-RA-003-package-law/record-findings.py
python -B -X utf8 private/sessions/20261018-RA-003-package-law/verify-final.py
git -c core.safecrlf=false diff --check
```

Branch, acquisition, four-page capture and actual probe exited 0. The probe
wrapper retains the exact interpreter/input argv, stdout/stderr and tool hash
privately. Four current-note snapshots precede edits; preservation metadata has
a before/after journal. One diagnostic `rg` call included nonexistent `src`,
exited 1 and still located `tools/artifact_probe.py`; subsequent exact-file reads
resolved that search error. No failed firmware request was retried.

Local evidence verification: **28 check groups passed**, seven tracked JSON
files parsed and 102 local Markdown links resolved, **exit 0**. The authored
tool and synthetic fixtures are unchanged; prior 8/8 artifact-probe tests are
retained without rerun. Their synthetic coverage is distinct from this actual
bounded identification, and neither validates the UFU container or camera.

## Reviewed changes and completion

Public files: README, ARTIFACT_INTAKE, BACKLOG, CODEX_HANDOFF, FEATURE_PROGRESS,
MAINLAND_FIRMWARE_SOURCE, OFFICIAL_PACKAGE_INTAKE, STATE and this session report.
Private current notes, firmware, consent/acquisition/probe/preservation evidence
and raw public-page captures are ignored and unstaged. Reference locks,
UNVERIFIED profile, master plan, validation thresholds and host code are unchanged.

```powershell
git -c core.safecrlf=false add -- README.md docs/ARTIFACT_INTAKE.md docs/BACKLOG.md docs/CODEX_HANDOFF.md docs/FEATURE_PROGRESS.md research/MAINLAND_FIRMWARE_SOURCE.md research/OFFICIAL_PACKAGE_INTAKE.md research/STATE.json research/sessions/20261018-RA-003-package-law.md
git -c core.safecrlf=false diff --cached --check
git diff --cached --name-only
git diff --cached
git commit -m "docs: record official package identity and China research provision"
git status --short --branch
```

Commit identity, staged-content review and final working-tree status are recorded
in the private completion receipt and accompanying response. No push, third-
party code integration/relicensing, external inquiry or private upload occurred.

## Next single work package

**RA-003: assess and document the exact container-inventory/extraction acts
against the China statutory research route and accepted terms, then audit the
applicable parser before use.** Input provenance/size/hash and bounded signature
are now recorded. Full proposed analysis scope, container validity, source/build
correspondence and exact-body applicability remain open. No offsets, resources,
component ABI or backend support can be inferred from the signature alone.

Camera commands: **none**. Device access/writes, driver changes, firmware or
upstream execution, extraction/disassembly, protection bypass and uploads: **none**.
