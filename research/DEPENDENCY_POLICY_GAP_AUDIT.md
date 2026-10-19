# Dependency manifest and native policy: saved-evidence gap audit

2026-10-19. Evidence: **static-inference**, **offline-tested** on saved records and invented inputs. Native English and native Wi-Fi FTP remain primary. This is shared host preparation for inspecting the applicable package; it supplies no feature mapping.

The historical binding plan has two null-input blockers: `dependency_manifest_unobserved` and `native_policy_unobserved`. They are accurate for that frozen plan, but do not mean no later dependency evidence exists. The descriptor audit saved a manifest, 351 installed receipts and an installed proof. The later dependency-only continuation saved eleven package Python origins, five trusted origins and five guarded package native loads. Their historical scopes remain distinct.

## Predicate and evidence matrix

| Old production predicate | Saved evidence | Disposition |
|---|---|---|
| Dependency schema/version, exact wheel hash, RECORD hash, expected files | Descriptor `manifest` contains the closed wheel-manifest schema and 351-file roster | Available for explicit successor binding; do not edit the historical null plan |
| Exactly 351 relative unique paths, bounded sizes, SHA-256 per file, canonical roster digest; 351 RECORD rows/352 archive entries | Descriptor manifest | Check with unchanged `_manifest`; this is saved-record validation, not reopening the wheel or verifying current installation |
| Exact receipt keys/path/hash/size/read-only flag; regular single-link non-reparse files | 351 descriptor `installed_receipts` | Check with unchanged `verify_open_receipts` |
| Same-API before/after equality; cross-API device/inode/mode/size/mtime equality | Four saved stamps per installed receipt | Retain exact predicates. Separate runtime-data policy amendments do not weaken package-file checks |
| Installed proof record/roster cross-binding and per-file identity tokens | Descriptor `installed_proof` | Validate the saved proof with `_installed`, then require canonical equality with the recomputation from the same saved receipts |
| Closed native policy: version/backend/suffix/record, package Python origins, external backend origins, native libraries, `no_fallback` | Descriptor policy/receipt are null; continuation describes observed origins/load receipts, not an approved expectation policy | Requires a separately reviewed policy derived before execution. Observed successful loads cannot define an allowlist after the fact |
| Every policy origin uses constrained relative paths with no drive colon/backslash/absolute root | Continuation trusted origins use absolute external runtime paths | Directly incompatible. Do not strip prefixes or move/copy files to make old checks pass; bind explicit roots and provenance domains in a successor contract |
| Python and native package origins belong to the exact wheel roster; external backend origins carry their own identities | Whole payload roster has 351 rows; eleven Python origins and five native loads describe an executed subset; five trusted origins belong to the interpreter boundary | Keep the three domains separate. Counts alone cannot establish exact membership or source identity |
| Native intent binds name/path/hash/installed identity and selected loader API | New intents retain API, raw arguments/keywords, normalized path, before-open receipt and audit fields | New schema needs an explicit, lossless contract. Do not collapse raw versus normalized loader spelling or invent old identity tokens |
| Old native receipt contains matched `guarded_intents`/`native_loads`, exact origins and flags declaring guard-before-import/complete-before-cipher-use | New `dependency_probe_native_receipt_v1` has `intents`, `completions`, `failures`, audit status, AESNI observation and transitive-OS limitation; sequence is retained in surrounding events/journal | Direct shape differs. Preserve event ordering and completion evidence; Boolean renaming is insufficient |
| Old receipt asserts `complete_before_cipher_use` | Reviewed continuation source performs the public-vector loop before `guard.finish()` (lines 287–300); full receipt publication precedes the later callback | Completion before the callback and completion before any cipher use are different claims. Do not assert the old flag from the new result; distinguish bootstrap/public-vector use from protected continuation in the successor contract |
| Raw guard evidence retained durably before continuation and no additional native load afterward | Existing continuation reports fsync/close/hash verification before one public-vector callback | Useful saved ordering evidence. Bind receipt, journal, source/config and operation identity explicitly; not GDT execution authorization |
| Startup/import and loader trust boundary | Separate descriptor startup data and later `-I -S` runtime observations; trusted stdlib/_ctypes initialization precedes package guarded loads | Model bootstrap separately from package loads. A package guard does not prove every interpreter or OS native load was guarded |
| Fresh operational context and accepted source/basis chain | All evidence here describes earlier acts | Not established. No saved receipt proves current mapped bytes, transitive DLLs, current installation, exact-body applicability or future behavior |

The exact old pure source snapshot has SHA-256 `22558080636f15300590c22b9987216216f650b4edc58d7df89092643722de74`. Its original file and every historical plan/receipt remain unchanged. The comparison checks historical audit bytes against two saved references and the continuation records against their previously recorded SHA-256 values; this is cross-reference consistency, not authentication of historical events.

## Closed successor proposal

Use a new versioned contract rather than broaden the old path predicate. Require separate named roots for wheel payload and trusted interpreter/runtime, exact hashes and identity domains, exact expected alias/native sets, selected backend/suffix and an explicit bootstrap boundary. Reject duplicate/case-folded paths, traversal, paths outside their named root, missing/extra aliases, unexpected native loads and unsupported schema versions. Keep original loader arguments, normalized targets and audit arguments separately bound.

Bind each new contract to the complete saved manifest/installed proof, source/config identities, operation identifier, raw receipt, journal and callback order. Validation must distinguish a saved expectation from a runtime observation and a fresh observation. Qualification must include wrong-root/hash/alias/record, missing/extra completion, duplicate/reordered events, ambiguous load outcomes, changed runtime and misplaced callback/durability markers. A callback exercised on public vectors does not authorize firmware processing.

This is a proposal for later implementation and independent review. It creates no new executable adapter, policy, launch command, target profile or accepted operational seal. All authority/readiness flags remain false. The historical blockers remain recorded until a separately reviewed successor chain explicitly replaces their missing inputs.

## Result and next package

Exact comparison and qualification results are in the [session report](sessions/20261019-RA-003-dependency-policy-gap-audit.md). Tests cover invented receipt refusals and unchanged pure predicates, not an implemented successor contract. Current English/FTP support, recovery and device-write gates remain unpassed. Camera commands: **none**.

Next single work package: **RA-003: implement the closed successor dependency/native-evidence contract on invented inputs, preserving root domains, bootstrap boundaries and event/durability ordering; independently review it before applying it to saved actual receipts or authorizing any runtime/protected-input act.**
