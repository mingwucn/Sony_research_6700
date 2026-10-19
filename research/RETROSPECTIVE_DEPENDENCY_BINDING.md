# Retrospective dependency comparison

Evidence: static-inference, offline-tested. This prepares the shared host-side
analysis path for native English and native Wi-Fi FTP research. It does not map
either camera feature. FL2/FL3 remains deferred.

`tools/dependency_retrospective.py` derives an explicitly retrospective
expectation from supplied ordinary metadata, then calls the unchanged lossless
legacy adapter. Package Python/native hashes and identities come from the saved
manifest, installed receipts and recomputed proof. Trusted origins come from the
saved raw receipts. Package/runtime paths come from the saved configuration and
entry-startup record. All are rechecked by the full legacy adapter against the
configuration, raw transcript, journal and completion record.

The earlier expectation schema requires a root digest. Here it is explicitly a
`retrospective_path_label_v1` digest of domain and path, **not a directory stat
identity**. A named blocker records that distinction. The configuration digest
is canonical JSON plus newline, distinct from the original file hash. The cache
digest is a caller declaration; cache contents are not opened or revalidated.
Producer hashes must match the reviewed runtime/continuation source profile;
the pure function authenticates no executing buffers or historical events.

Every legacy blocker remains. New blockers explicitly cover expectations derived
after observation, path labels, unauthenticated executing buffers and the
cache-digest declaration. Original raw/journal strings remain unchanged in the
returned envelope. No prior approval, fresh observation, runtime authority,
feature, recovery or device-write acceptance follows.

The private `saved_diagnostic.py` wrapper has ten fixed inputs: three authored
pure helper sources, two authored producer sources and five ordinary saved
metadata records. All ten bounded regular-file reads and SHA-256 checks must
finish before the three pure helper buffers execute. Producer sources are
hashed only. The `tools` namespace is restored on success or refusal. No cache
body, installed dependency, native payload, firmware or camera input is opened.

Every input uses an embedded descriptor reader: ancestor directory/reparse
checks, regular single-link file checks, read-only descriptor open, cross-API
identity checks, bounded reads/EOF and stable pre/post metadata. These are
cooperative filesystem checks, not a hostile-filesystem sandbox. A first design
loaded the reader before those checks and omitted that read from accounting;
review rejected it. The final wrapper removes that bootstrap entirely.

The historical descriptor supervisor contains an elapsed-time decimal. Only
that outer field is accepted as a nonnegative finite Decimal; selected package
metadata still passes the strict integer/Boolean JSON contract. This is a
projection of manifest, receipts and proof plus descriptor scope markers,
**not revalidation of the entire earlier descriptor audit or its read ledger**.

The wrapper exclusively creates its attempt directory and writes a start record
before reading inputs. It writes private result/completion or a needs_review
refusal. Existing output blocks replay; no automatic retry, reboot or rollback.
An interruption requires inspection of existing output. Files here are private
diagnostics; no crash-durable transaction guarantee is asserted.

Commands, tests, exact source reviews, application outcome and remaining work
are recorded in the [session report](sessions/20261019-RA-003-retrospective-binding.md).
