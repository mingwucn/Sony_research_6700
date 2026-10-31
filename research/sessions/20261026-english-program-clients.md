# English restriction: conditional program API clients

2026-10-26. Evidence: **static-inference**, **offline-tested**.
Previous goal turn: progress. This turn: progress. Goal active/incomplete.
Camera commands: **none**. Network commands: **none**.

The exact conditional program identified in the
[previous review](20261026-english-program-handoff.md) now has a concrete native
API access map. Its reviewed client forms do not identify another language
restriction or language-related write. This narrows the remaining search; it
does not prove that selecting English preserves every regional state.

## API access and client inventory

Two independent parsers reconstruct all 211 native API slots: 194 have actual
relocations and 17 are initially zero. One relocation uses a section symbol
with a nonzero addend; an empty symbol name is not a null function. The program
contains 197 exact five-instruction wrappers covering all 194 populated slots
and two zero slots, with one duplicate wrapper. Each follows the program
header's descriptor pointer and tail-branches through a specific API entry.
No actual API publication or successful execution was observed.

All 35 Backup-family wrappers are mapped. Whole-file searches of aligned direct
branch encodings and raw 64-bit pointer literals find no references to the 12
write/reset-family wrappers. These are finite forms, not proof that computed
calls, aliases or other instruction sequences cannot use the same APIs.

The read-family survey has 142 direct branch-encoding candidates. Bounded local
recipes resolve 36 constant item arguments; 100 have dynamic definitions and
six remain behind unresolved definitions or barriers. None of the resolved
constants equals the selected-language, English-availability or reviewed
notification identifiers. Raw-byte matches and partial constant instructions
were not promoted to language clients. Counts describe the inspected forms and
are not a complete reachable call graph or distinct behavioral tests.

## The direct callback path

There is one direct caller of the registration wrapper. It walks an item table,
builds the provider's packed registration record, and supplies an output-handle
array. Under the packaged initial table, the first item is followed by a zero
sentinel, giving one registration. Independent reads of both exact packaged
catalogs identify that item as 128 bytes and distinct from language selection
and availability. The same function uses the native multi-read API with the
item/context arrays. Prior initialization, later mutation and current table
values remain conditions, not observed facts.

The provider invokes callbacks with item, size, copied data and context. The
program's complete five-instruction callback rearranges those arguments and
branches to a local copy-shaped routine, with context as destination. It does
not itself call a Backup write API. Complete copy semantics, destination
capacity and the validity/lifetime of current pointers are not established by
the packaged record. A separate direct unregister caller walks saved handles.

The native provider audit also confirms that the ordinary write returns an
effective record size after its memory update and optional notification. That
return does not prove that asynchronous notification was delivered or handled.
The ordinary read, bounded read and four-byte value-return APIs have different
contracts; a four-byte value return is not a read-into-buffer result.

## Initialization and address limits

The first entry encodes an intended zero-initialization range and a separate
escape/backup copy of writable data. The original writable interval lies
outside the reviewed clear range. This supports a backup-copy interpretation,
not relocation or invalidation of the original range. Direct diagnostic stores
and reached provider-initialization calls also mutate writable objects, so no
whole-range immutability claim is made. The hardware-command effects remain
static intent because the program was never executed.

The later entry has an empty first constructor array and 56 entries in the
second array. Their local instruction views do not close all transitive calls.
An adjacent function contains a reverse-copy path but has not been proved
entry-reachable. Program file offsets, conditional link addresses, copied
buffers and live runtime addresses remain distinct.

The older partial mnemonic formatter mislabels one prefetch-class encoding as
an ordinary load. All raw words are retained; no argument or copy-direction
claim relies on that label. The frozen formatter and historical evidence were
not edited.

## Verification and remaining work

Root analysis used the retained isolated CPython 3.13.12 with `-I -B -X utf8`:

```powershell
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-program-clients-20261026/survey_raw.py
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-program-clients-20261026/inspect_leads.py
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-program-clients-20261026/scan_first_page.py
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-program-clients-20261026/catalog_context.py
& '<private crypto-env>/Scripts/python.exe' -I -B -X utf8 private/english-program-clients-20261026/crosscheck_clients.py
```

All exited 0. Root crosschecks join all 211 independently parsed slots, recheck
985 exact wrapper words, independently repeat the finite write/reset reference
search, and verify the callback words and packaged catalog metadata. The
previous pure catalog helper was source-reviewed and hash-checked before use;
frozen generators and upstream entrypoints were not run or imported. Exact
worker commands, interpreters, failed host assumptions, corrections, identities
and limitations are retained privately. One worker invocation's exit status was
lost to truncated tool output; its saved callback result was independently
validated by the successful closure. These are static consistency checks;
no firmware behavior test, broad historical suite or physical test was run.

All new evidence is durable and ignored. No disposable scratch was created;
earlier preserved scratch was not deleted. No camera command, network request,
firmware execution, mount, emulation, payload, staging, commit, push or external
submission occurred.

English resources and the separate selected-language setting retain their
earlier static support for a language-only route. Normal preload, live
catalog/program identity, dynamic and indirect clients, the original 54
synchronous numeric-origin gaps and one forwarded asynchronous origin remain
open. Native rendering, persistence, complete regional/calibration preservation,
inverse and recovery remain unproved. No feature or device-write gate passed.

Next single work package: **EN-101: return to the application notification
origins and remaining dynamic Backup clients. Trace the unresolved item or
message arguments to selected-language subscriptions, then inspect those
callbacks' writes and startup/reset effects. Use the new conditional program
wrapper map to avoid treating its initial non-language callback as a language
consumer. Preserve normal-preload, live-state and lifetime gaps. Offline only;
no camera contact or write payload.**
