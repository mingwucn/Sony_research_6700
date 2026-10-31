# EN-101: offline α6700 2.00 resource and language-setting trace

2026-10-26. Evidence: **static-inference**, **offline-tested**. The previous
goal turn and this continuation both made progress: actual package evidence
now replaces the missing-resource/selector hypothesis with an inspected path.
The active language-only goal remains incomplete while callback and earlier
initialization behavior remain unresolved.

## Scope and result

The owner explicitly requested actual firmware analysis, then language-only
enablement feasibility, offline without touching the camera. This separately
scoped work used the existing locally acquired official package. It did not
alter historical RA-003 decisions or authorize camera operations.

The [findings](../ENGLISH_FIRMWARE_FINDINGS.md) record provenance, resource counts,
policy, current-language persistence and the reviewed startup fallback. Four
English families contain the same 11,917 IDs as Chinese, with 23 shared blanks.
Exact code and resource metadata support a current-language-only English route;
the reviewed setter and startup path do not require enabling the protected
English permission or changing a region setting. This is a bounded static
conclusion, not a demonstrated unlock or complete state-preservation proof.

The same-family shipped CN1/ALLLANG comparison has 40 current item differences
in its primary AP catalog and 35 in its separate CP catalog, with zero record
metadata differences in either. The complete files differ at 97 byte positions.
Whole-table replacement is excluded. Both AP language item payloads are distinct and have no
overlap with other present item payloads; a second review also checked
capacities and metadata headers. Installed-body identity/current values remain
unverified. The MainDest fallback alone does not select the owner's table.

The native Backup provider checks item metadata and supports narrow logical
item writes. Synchronization persists broader storage. Selected language has a
callback attribute; the permission item has conditional protection. A focused
reset trace and finite callback/save review are recorded below. Callback
consumers, other initialization, durable preservation and inverse/recovery
remain unresolved.

## Actual-input work

All firmware was treated as inert data. Authored tools parsed the ext2 image,
ELF, UXC records and Backup metadata. No mount, target instruction execution,
upstream launcher, installer, service worker, network request or camera API was
used. Host AES code from the previously pinned dependency was executed after
rechecking its wheel hash and all 351 recorded installed files.

One complete verified decoding pass retained only the application filesystem
member; another retained five declared Backup members, under 5 MiB total.
Each reproduced the prior logical-stream SHA-256 and every selected payload
hash, checking all block envelopes and terminal state. Each finished once,
exit 0; no failed actual extraction was retried. All sources were opened for
reading; selected target bytes and detailed address/identifier records remain
in ignored private storage.

The durable local evidence root is `private/english-offline-20261026/`, including
scope records, extraction receipts, resource inventory, current-only catalog
comparison, source/ELF instruction records, independent audits and test logs.
No generated firmware or settings payload exists. Nothing was staged, committed
or pushed for this work.

## Qualification

Interpreter: **CPython 3.13.12**. Ordinary authored parsers/tests used
`C:/ProgramData/miniconda3/python.exe`. Full decoding and the existing stream
suite used the previously retained private crypto environment's Python 3.13.12.
The following are exact commands from the workspace root; every final command
listed exited **0**, with no skipped cases:

| Command | Cases | Evidence limit |
|---|---:|---|
| `python -B -m unittest tests.test_ext2_readonly tests.test_elf_static tests.test_uxc_readonly -v` | 66 | Invented filesystem/ELF/resource bytes; no authenticity or rendering proof |
| `python -I -B -m unittest discover -s private/english-offline-20261026 -p test_aarch64_trace.py -v` | 7 | Bounded instruction-reference recognizer; not a full disassembler |
| `python -I -B -m unittest discover -s private/english-offline-20261026/backup-provider-review -p test_backup_catalog_readonly.py -v` | 14 | Current-only BK4 metadata interpretation and bounds |
| `python -I -B private/english-offline-20261026/extract_application.py --self-test` | 8 | Selected-stream slice boundaries and reconciliation |
| `private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B private/sessions/20261018-RA-003-stream-validation/test_stream.py` | 45 | Existing synthetic stream qualification rerun before actual extraction |

Total: **140 distinct synthetic cases passed**. The 45 stream cases are existing
regressions, not new tests. Repeated runs of the same cases are counted once.
Historical unrelated suites were not rerun or included.

Actual-data commands, also exit 0:

```
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B private/english-offline-20261026/extract_application.py
python -I -B private/english-offline-20261026/inspect_resources.py
python -I -B private/english-offline-20261026/validate_resources.py
private/sessions/20261018-RA-003-crypto-provenance/crypto-env/Scripts/python.exe -I -B private/english-offline-20261026/extract_backup_catalog.py
python -I -B private/english-offline-20261026/backup-provider-review/compare_catalogs.py
python -I -B private/english-offline-20261026/check_language_aliases.py
python -I -B private/english-offline-20261026/resource_bank_registration.py
python -I -B private/english-offline-20261026/consolidate_language_refresh_new.py
python -I -B private/english-offline-20261026/language_only_data_trace.py
python -I -B private/english-offline-20261026/audit_language_aliases.py
python -I -B private/english-offline-20261026/audit_language_refresh.py
```

Independent audits checked actual instruction encodings, import/relocation
links, selected English case, startup fallback, all 34 child enum records,
four bank-0 file associations and catalog non-aliasing. A complete global
control-flow or indirect-caller proof is not claimed.

## Corrections and negative results

- The model name registry was initially framed one row too early. Corrected
  registry boundaries and one-based ordinals are recorded. English identity
  was independently connected through its resource label and actual menu path;
  no guessed registry-to-storage conversion is used.
- Following-payload bytes were initially labelled as reset candidates in the
  catalog comparison. That interpretation is withdrawn. The accepted result
  is `catalog-comparison-current-only-private.json`; initial results remain
  retained and explicitly superseded. Final parser/tests make no reset claim.
- A full notification-ID search alone was initially used to narrow subscribers.
  Provider review established routing by the low 16 bits; that exclusion was
  withdrawn and a separate low-16-bit audit was saved. Neither finite survey
  establishes that no subscriber exists.
- A delegated registration's userspace request and candidate kernel handler
  share the expected argument layout, but the dispatcher's actual table-base
  link remains unproved. The initialized kernel allocation range is conditional
  on reaching that handler; its ordinal in a pointer table is insufficient to
  close the bridge. Earlier stronger private wording is retained as superseded.
- An optional directory-name walk stopped at its 10,000-entry guard, exit 1.
  It was not widened or treated as absence evidence; standalone Backup tables
  were found in already accepted tar metadata.
- A coverage-summary command first failed at stdout encoding after saving JSON;
  ASCII-safe output then completed, exit 0. Import/path and PLT-shape development
  errors were corrected before the final accepted runs. No acceptance threshold
  was relaxed and no failed camera operation exists.

## Remaining work

Next single package: identify the producer and invocation phase of the map entry
copied into the selected-language model, and determine whether it can replace a
saved English selection during initialization. The consumer and lookup helpers
are in the current local application; the producer remains to be located. Keep
the selected-language setting separate from its protected permission flag and
regional identity. Continue offline; prepare no write payload and do not contact
the camera.

A subsequent focused reset audit now qualifies only the selected-language
mode-1 path: native gates admit that field, fixed-size helper and source pointer
are traced, and the shipped CN1 reset source is 25. This is independent of the
withdrawn blanket following-byte interpretation; English-permission reset bytes
remain uninterpreted. The subsystem API forwards its caller's mode, so neither
startup invocation nor factory-reset behavior is assumed. Both commands exited 0:

```
python -I -B private/english-offline-20261026/language_reset_trace.py
python -I -B private/english-offline-20261026/audit_selected_language_reset.py
```

The AP/CP extent audit independently confirmed that the traced CP request's
local buffer is separate from both AP language bytes. The CP catalog has its
own English permission and no selected-language subsystem entries. DMA
direction, physical mappings and other synchronization stages remain outside
that conclusion. The ordinary AP subsystem-save trace copies current live AP
rows into scratch storage; it does not prove a one-byte physical transaction
or durable behavior. These final commands used CPython 3.13.12 and exited 0:

```
python -I -B private/english-offline-20261026/callback-review/trace_backup_sync.py
python -I -B private/english-offline-20261026/callback-review/inspect_cp_extent.py
python -I -B private/english-offline-20261026/audit_backup_sync_extent.py
python -I -B private/english-offline-20261026/finalize_low16_queue_audit_addendum.py
```

A finite normalization receipt checks all 34 native getter/setter cases and
the queued persistence worker's language case. They preserve the incoming
value, with no additional explicit region write in the reviewed worker body.
Other model-copy paths also preserve their inputs, but map/structure sources
and invocation phases remain unresolved. This narrows the next trace without
claiming no global normalization. These commands used CPython 3.13.12, exit 0:

```
python -I -B private/english-offline-20261026/finalize_language_normalization_receipt.py
python -I -B private/english-offline-20261026/audit_delegate_ap_and_normalization.py
python -I -B private/english-offline-20261026/callback-review/delegated-route/trace_delegated_route.py 0x7c0:0x890 0x13c0:0x15a0
```

All dependent inspection processes finished before final evidence verification.
The retained private evidence manifest checks file sizes, hashes and authored
Python syntax; it supplies no additional device-behavior proof. The final
manifest pins 203 retained files, parses 53 authored private Python sources and
rechecks both frozen provider pin sets. Bookkeeping and manifest commands use
CPython 3.13.12; both exited 0:

```
python -I -B private/english-offline-20261026/record_session.py
python -I -B private/english-offline-20261026/finalize_evidence.py
```

Cleanup was attempted only for this packet's empty task-owned directory under
`%TEMP%/Codex/a6700-english-offline-ef785f5b3157440e8f5691050075bcf2`.
Automatic approval review rejected that removal with `blocked by policy` before
execution. A subsequent read confirmed it still exists and is empty; no alternate
deletion or retry was attempted. Its exact resolved path and result are saved
privately. The earlier source-review scratch folder also remains after its prior
policy rejection and was not touched. Required research evidence is durably
stored in the workspace, outside Temp.

Camera commands executed: **none**. Network commands executed: **none**.
Firmware executed: **no**. Camera contact and write gates remain held.
