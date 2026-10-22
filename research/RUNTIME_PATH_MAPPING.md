# Runtime origin, path and complete-receipt mapping

2026-10-23. Evidence: **static-inference**, **offline-tested**. Native English
menus and native camera-to-server Wi-Fi FTP remain first. Camera commands: **none**.
No legal inquiry, network, installed/native activation or protected-input read.

The existing `tools/dependency_legacy_bridge.py` now supplies
`prepare_runtime_mapping` and `validate_runtime_mapping`. They validate supplied
ordinary records with the retained `_package`, `_policy` and `_receipt` helpers,
then preserve each origin's root domain, relative/absolute path, content metadata
and identity. Every supplied full receipt has both path forms and separate
canonical SHA-256 tokens. Changing only the path is reversible; no stamp,
read-only declaration or root association is silently dropped.

The original `project_native_policy` produces the relative comparison view when
all trusted receipts are supplied. That view needs the domain sidecar: a legacy
relative path alone does not identify an external runtime root. Distinct roots
must not collapse to one relative label. Casefold path collisions, declared
physical identity aliases, inconsistent proofs and incomplete supplied receipts
are refused. Identity-alias checks compare caller records, not actual hard links.

The existing retained comparison accepts an optional `runtime_mapping`. Its
original packet binder supplies policy/package inputs first; mapping validation
recomputes against those inputs and the supplied trusted receipts. A valid
mapping for another operation cannot replace that context. Default comparison
output and the public runtime refusal remain unchanged.

## Saved ordinary evidence

Only the saved ordinary package and successor expectation descriptors were read.
All **351** historical package receipt pairs and **21** origin descriptors map:
11 Python aliases, five native aliases and five trusted runtime aliases. Both
root domains and root identity hashes are preserved as historical declarations.
The private mapping is **817,248 bytes** and stays ignored.

The five trusted origins contain five-field identity summaries, without complete
open receipts. A complete token includes the path, read-only declaration and all
four eight-field stamps. It cannot be reconstructed from an identity subset,
content hash or size. The saved mapping therefore records **five missing full
runtime receipts**, with no invented stamps or receipt tokens and no relative
native policy. A partial metadata mapping establishes no current filesystem
observation, freshness or executable binding.

## Qualification and limits

**155 distinct current synthetic cases pass: 29 new + 126 affected regressions**,
zero failures/errors/skips, CPython 3.13.12 with `-I -S -B -X utf8`, exit 0.
Tests include full receipt round trips, same CROSS identity with changed ctime
or attributes, cross-root/casefold collisions, wrong domains, incomplete receipts,
alias/proof/path drift, output tampering, false authority and genuine retained
binder integration. No installed/native import or bootstrap is exercised.

The first integrated qualification exposed three errors: the older invented
fixture reused inode IDs across distinct files. The new integration fixture now
assigns distinct invented IDs and rebuilds all dependent proof/binding hashes.
The alias rejection, production predicates and existing fixtures were unchanged.
Earlier runs and the failed log are preserved and excluded from the final total.
Independent source and fixture reviews found no blocking defect.

All 16 other captured authored source pins and frozen **16 ordinary records / five
pending dispositions / three dependency nulls** remain unchanged. Existing bridge
functions retain their ASTs except the explicit optional comparison join. No
source-manifest migration, actual allow record or executable bundle was created.
[Exact commands, results and changed files](sessions/20261023-runtime-mapping.md).

Fresh runtime/origin/root observations, five full runtime receipts, complete
native-event behavior, bounded journal/stop entry and current execution bindings
remain unresolved. Protected processing, exact-body correspondence, English
resource/policy mapping, native FTP backend/lifecycle and practical rollback are
unvalidated. No feature, recovery or device-write gate passed. FL2/FL3 stays
deferred; custom looks remain separately gated later; any bridge is **host-assisted**.

## Next single work package

RA-003: implement and qualify a bootstrap-only disposable-child entry and bounded
private event journal using supplied invented imports and events. Exercise the
original bootstrap method through an inert import adapter and parent verification;
stop before package imports, controller and protected processing. Preserve the
review packet refusal, native-denying synthetic hook and frozen 16/5/3. No
installed/native/protected input reads, actual activation or camera contact.
English/native FTP remain first.
