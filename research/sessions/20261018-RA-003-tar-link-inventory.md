# RA-003 session: private tar directory with opaque link metadata

2026-10-18 UTC / 2026-10-19 Europe/Paris. Topic branch
`codex/ra003-tar-link-inventory`, parent
`0f193f706d356b13dd5d3f9f894842f7efbe5c2f`. Host R0 only. Native English
and native Wi-Fi FTP remain first; FL2/FL3 deferred, calibrated custom looks
later and separately gated, optional bridge **HOST-ASSISTED**.
Camera commands: **none**.

## Result and limits

One newly scoped metadata inventory completed, script and host exit **0**,
**29.409064s**, one pipeline with two planned descriptor passes, no retry or
fallback. The accepted private directory contains **137 members**: **97 regular
files, 39 directories, zero hard links and one symbolic link**. It checked
**139 physical tar headers**, zero extension records, member padding, two zero
end blocks and the zero remainder. Compact UTF-8 directory JSON is **80,182
bytes**, below the fixed **2 MiB** limit including explicit policy fields.
Regular payloads and the complete extent were stream-hashed without saving
payloads. Detailed names, targets, member hashes and positions stay private.

The [before-read policy](../TAR_LINK_INVENTORY.md) deliberately changes only
link-target metadata handling. The former extraction-oriented predicate was
unnecessary for a directory observer that performs no filesystem materialization.
Link text is now exact, bounded UTF-8 opaque metadata; it is never normalized,
resolved, followed or claimed safe for extraction. Member-name guards, canonical
duplicate checks, checksums, sizes, framing and all caps remain unchanged.
This change was documented and qualified before the new experiment. The earlier
failed trial and successful first-refusal diagnostic remain unchanged; their
original rules and limitations are preserved.

Fresh complete source/logical-stream identities, header, declared spans and
both prior 4,096-byte prefixes agree. All **1,000,017 physical blocks** were
checked; logical size remains **1,020,017,152 bytes**. Observable source state
remained stable. Only after complete lineage acceptance could the tar observer
finish and the closed metadata schema be accepted.

No member prefix classification, member files, decoded-stream file,
decompression, disassembly, upstream/firmware execution or camera contact.
This is directory metadata evidence; member formats, English resources or
enablement, native FTP backend, authenticity, exact-body correspondence and
recovery remain unverified. No feature, target profile or device-write gate passed.

## Exact principal commands and results

Repository-root working directory. PowerShell **7.6.5**, Windows AMD64 build
26300.9711; standard CPython **3.13.12** at
`C:\ProgramData\miniconda3\python.exe`. Commands below use that interpreter
explicitly. The isolated synthetic and actual pipelines use the existing
private venv with pinned pycryptodomex **3.24.1**. No new download, installation,
agreement or private upload.

```powershell
git status --short --branch
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-tar-link-inventory/bootstrap.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-tar-link-inventory/run-tests.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-tar-link-inventory/seal-scope.py
& 'D:/LocalWork/Sony_research_6700/private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe' -I -B -X utf8 private/sessions/20261018-RA-003-tar-link-inventory/run-real.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-tar-link-inventory/record-host.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-tar-link-inventory/update-notes.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-tar-link-inventory/polish-notes.py
```

- Initial Git clean at the parent above. Required plans/state/intake/instructions
  read. Bootstrap exit **0**: six exclusive original snapshots, **97** tracked
  file hashes and `git switch -c codex/ra003-tar-link-inventory`, exit **0**.
  Twelve unchanged foundation/test files copied with hash-checked lineage.
- Combined qualification **171/171 passed**, zero skipped, exit **0**,
  unittest **1.060s**, wrapper **1.728426s**. It comprises the unchanged 133 cases plus 19 parser-policy
  and 19 acceptance/pipeline cases. A nested legacy parser check is not counted
  again. No actual firmware or operational constants in fixtures. Exact argv,
  18 authored source hashes, four dependency hashes and stdout/stderr retained.
- Scope seal exit **0**. Exclusive before-read scope, 18 qualified source hashes
  plus reviewed runner (**19**) and qualification-result SHA-256 sealed before
  source I/O. Independent source/scope/runner review passed. Unaffected header
  and finish logic matches the original after excluding explicit policy changes.
- Actual command: host session **46239**, chunks `9f883b`, `7a3a28`, terminal
  `707db8`; host exit **0**, script/journal/result exit **0**, **29.409064s**.
  Exclusive/fsynced journal precedes source I/O. **351** installed dependency
  hashes verified. One preliminary and one actual-decoding complete-parent pass
  on the same read-only descriptor. Progress is provisional; only terminal
  acceptance establishes the private directory. The ten-row journal agrees with
  the terminal result. No automatic retry or fallback.
- Metadata-only host receipt and notes update exit **0**. Public/private feature
  mirrors synchronized; prior facts, trials and device gates preserved.
  Documentation verification does not repeat the actual source read.
  A later prose-only singular-agreement correction exited **0**.

Focused commands, from the new private session directory:

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 -m unittest test_metadata_tar -v
& 'D:/LocalWork/Sony_research_6700/private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe' -B -X utf8 -m unittest -v test_link_acceptance test_link_pipeline
```

Focused parser **19/19 passed**, exit **0**, **0.083s**; acceptance/pipeline
**19/19 passed**, zero skipped, exit **0**, **0.303s**. These focused runs remain
distinct from the captured isolated combined suite. Synthetic encrypted UFU/CBC
integration covers successful opaque links and late envelope/parent-hash failures
after tentative tar end. Those failures reach neither finish nor classification.
Post-finish gate failure clears returned metadata, and cleanup failure prevents
acceptance. Exact parser/extent, schema/types, policy flags, limits, GNU/PAX link
selection, unsafe/duplicate member names, UTF-8/control errors and tail are covered.

Public executable code/tests, locks and profiles are unchanged. Historical
standard-library suite **228 total / 225 passed / three skipped**, exit **0**,
was not rerun. No fresh CI/export or other-host result is claimed.

## Remaining prerequisites

Evidence classes: **static-inference** and **offline-tested**. No device readback,
runtime observation, physical test or independently reproduced camera result.
The **8 MiB** managed pipeline design budget is not a measured/capped whole-process
memory or secure-erasure guarantee. Observable source checks are not an atomic
filesystem snapshot. The official package is not a body backup or rollback system.

Accepted-contract interaction, independent constants derivation and later
member-copy/decompression/disassembly/distribution scope remain unresolved.
Exact body/build/SKU correspondence, English resources/restriction mechanism,
native FTP backend/ABI/invocation/media/network lifecycle and verified rollback/
recovery remain unproved. No new owner fact is required for the next bounded
offline format-study package. Device steps retain their separate explicit gates.

## Changed files and next package

Reviewed public scope, **11 files**:

- `README.md`
- `docs/ARTIFACT_INTAKE.md`
- `docs/BACKLOG.md`
- `docs/CODEX_HANDOFF.md`
- `docs/FEATURE_PROGRESS.md`
- `research/STATE.json`
- `research/TAR_PATH_DIAGNOSTIC.md`
- `research/TAR_LINK_INVENTORY.md`
- `research/PRE_CAMERA_AUDIT.md`
- `research/PRE_CAMERA_READINESS.md`
- `research/sessions/20261018-RA-003-tar-link-inventory.md`

Ignored private changes: authored parser/acceptance/tests/runner, unchanged
foundations, original snapshots, frozen scope and hashes, qualification logs,
journal/result/host receipt, private directory, review/publication receipts,
current session/feature JSON and appended owner intake/progress Markdown.
Earlier evidence preserved. No private firmware, keys, payloads or detailed
directory staged; no push, history rewrite or camera operation.

Next single package: **RA-003: review the private directory to select minimal English/FTP-relevant members, then document, qualify and run bounded in-memory prefix identification with full lineage and no child files**.

This continues format identification without treating names or strings as
working feature evidence. Full pre-camera goal stays active; previous turn and
this turn made progress, consecutive no-progress count **0**.

Final publication commands:

```powershell
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-tar-link-inventory/verify-notes.py
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-tar-link-inventory/stage-review.py
git -c protocol.allow=never commit -m "docs: record opaque-link tar metadata inventory"
& 'C:/ProgramData/miniconda3/python.exe' -B -X utf8 private/sessions/20261018-RA-003-tar-link-inventory/finalize.py
git status --short --branch
```

Publication verification reads source/metadata only, checking frozen hashes,
terminal lineage, aggregate directory invariants, private/public mirrors,
historical evidence and unpassed gates, JSON/links, unchanged out-of-scope files
and whitespace. Staging checks the exact named paths, working hashes and normalized
Git blobs, retaining the full staged diff privately. Commit/verification/clean
status are recorded in the private completion receipt.

The first metadata-only verification exited **1** because a public Markdown
write converted LF to CRLF, so its byte-prefix comparison failed. The private
sealed scope hash remained exact and the public scope text matched after newline
normalization. The verifier now normalizes only that public prose comparison;
private scope/source hashes remain exact. The failure and adjustment are retained
privately. No inventory rerun or experimental acceptance-rule change followed.
