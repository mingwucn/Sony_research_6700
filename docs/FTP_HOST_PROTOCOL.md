# FT-102: synthetic host queue and protocol contract

Status: **offline-tested foundation only**. `tools/transfer_queue.py` supplies a
local queue and an in-memory mock. It contains no socket, FTP/FTPS client,
credentials, camera API, automatic worker or command-line uploader. This is
neither native FTP support nor a HOST-ASSISTED bridge. FT-101 remains blocked by
missing target acquisition/ABI evidence. A separate opt-in
[loopback FTPS lab](FTPS_LOOPBACK_LAB.md) now tests this queue against a constrained
independent peer. Mock results remain distinct from that evidence; neither closes
native constraints or arbitrary-server compatibility.

## Executable boundary

The caller supplies a private, immutable local synthetic spool, a new local
queue-state path and a conservative destination root such as `/incoming`.
`TransferQueue.create` refuses an existing state file. `load` validates the
whole schema and reconciles interrupted local states into `needs_review`.
Both acquire an exclusive `.lock` lease. The owner must close the queue; a
crash leaves a lease that requires local review before removal. The code never
guesses that a stale lease or camera session is safe to take over.

`enqueue(Capture(...), source_relative_name)` reads and hashes a bounded,
nonempty regular file, refusing source symlinks. The synthetic file limit is
32 MiB and the queue limit is 10,000 objects. These are host implementation
bounds, not support limits for camera JPEG, RAW, video or large files.
`run_one(id, MockTransport(), now=...)` performs at most one caller-triggered
attempt. `reconcile` performs only observations through the supplied transport and
changes local state; it never uploads, renames or deletes a remote object. The
mock uses in-memory observations; the lab adapter uses authenticated read-back.

The spool and queue directory must be private and controlled by one owner.
This foundation does not defend against an attacker concurrently replacing
directory entries, reparse points or hard links; it is not a sandbox. Caller
labels/relative names are stored locally and can themselves contain private
identifiers. Keep queue files, spools and journals out of Git. No raw exception
text, credentials, absolute source paths or server messages are stored by the
queue. Transport errors carry a fixed category; unexpected exception text is
discarded and causes `needs_review`.

## Identity, completion and path rules

Each object records body alias, session identity, card identity, object identity,
capture sequence, producer filename, format, expected group formats, local
source name, length, SHA-256, attempt count and durable state. The group identity
uses body/session/card/capture sequence; RAW and JPEG are separate object
identities linked by that group. At most one object per format belongs to a
group. Partial-pair completion remains visible through `group_status`.

Object identity includes the producer filename and object ID, but not its
content hash. Duplicate enqueue with the same identity/hash is idempotent;
changed content under an existing identity is refused. Distinct session, card
or capture sequence values prevent basename reuse/file-wrap collisions. These
values are supplied synthetic facts; no camera completion or card identity
adapter has been implemented. Only `completion_evidence="synthetic-fixture"`
is accepted. A size-stability heuristic cannot masquerade as a capture-complete
event. A future adapter must independently establish its actual guarantees.

Destination paths are recomputed, never loaded as arbitrary commands: fixed
constrained root + SHA-256 object identity + `.jpg`/`.arw`, with `.part` for the
temporary object. These suffixes are format labels, not format verification.
Identity tokens and paths use bounded ASCII alphabets. Empty components,
absolute local names, `.`/`..`, backslashes, colon, percent encoding, CR/LF and
non-ASCII filenames are refused. Non-ASCII input support is intentionally
UNSUPPORTED rather than silently transliterated. Directory creation, filename
encoding negotiation, resumed/ranged upload and arbitrary destinations are
not implemented.

## Durable transitions and uncertain completion

The working sequence is `ready -> transferring -> verification_pending ->
finalizing -> committed`. The queue writes and fsyncs a complete JSON snapshot
to a unique temporary file before atomic local replacement; POSIX additionally
fsyncs the containing directory. Windows directory durability and power-loss
recovery have not been physically tested. The lease, state schema and atomic
replacement are not a cryptographically authenticated journal. A locally
tampered state file is outside the integrity guarantee, although malformed
fields, duplicate keys/identities, invalid groups and derived-ID mismatches are
refused. A committed record represents earlier observed hash equality, not a
fresh guarantee that the remote object still exists unchanged.

The queue persists `transferring` before upload and `finalizing` before rename.
Any reloaded in-flight record becomes `needs_review`; no network mutation is
inferred safe from a restart. An error marked uncertain, or any later error
after a remote object exists, also requires review. A plain successful upload
response is insufficient: the temporary object must match complete SHA-256
and length, then the finalized object must independently match both.

Read-only reconciliation has these outcomes:

| Remote observation | Local next state/action |
|---|---|
| Final length and full hash match | `committed`, no second upload or rename |
| Final differs or has no full hash | `needs_review`, preserve it |
| No final; temporary full hash matches | `ready_to_finalize`; a separate bounded call may rename |
| Temporary is partial, differs or has only size | `needs_review`, preserve it |
| Both objects observed absent | `ready` only while the attempt budget remains |
| Read/security result unavailable | `needs_review`, no mutation |

If both a verified final and a temporary object remain, the final may be marked
committed while the temporary remains untouched for review. There is no
automatic remote cleanup, source deletion, format, reboot or card operation.
Cancellation before work becomes `cancelled`; cancellation after upload keeps
the remote temporary and enters `needs_review`. In-flight cancellation is
cooperative at operation boundaries, not an interrupt/abort guarantee.

## Retry and security contract

Each upload/finalization attempt consumes one of 1..5 configured attempts
(default 3), including a retry that only finalizes a reconciled temporary.
Only a transport error explicitly classified `transient` with a **known
absence of side effects** can schedule an automatic-eligible retry. The caller
must supply a new time and invoke `run_one` again: there is no retry loop.
Backoff is bounded exponential delay plus deterministic identity-derived
jitter; retry deadlines and attempts survive reload. Authentication,
permission, quota/server-full, certificate/TLS and collision failures stay
distinct and do not generate an uncontrolled retry. An uncertain upload or
rename cannot be retried until explicit read-only reconciliation.

The supplied mock requires `verified_tls=True` before any remote operation and
has no plaintext mode or fallback. This flag simulates a verified FTPS session;
it does not perform TLS, inspect certificates or prove secure transport.
There are no credential parameters or credential-storage implementation.

Future real-server work must separately verify passive binary transfer,
explicit FTPS certificate trust/hostname checks and data-channel protection,
timeouts, capability negotiation, complete server-side SHA-256 or read-back,
and no-clobber upload/finalization under races. The mock provides exclusive
upload/rename; FTP rename is **not assumed universally atomic or no-clobber**.
A real adapter lacking proved capabilities must refuse this contract rather
than overwrite, treat size as equality, bypass TLS or fall back to plaintext.
SFTP is a separate protocol and is not implemented. No real-server test or
dependency acquisition was performed for the original mock foundation. Later
isolated dependency/protocol evidence is recorded in the linked lab report.

## Synthetic results and outstanding tests

Run with the existing standard-library Python interpreter:

```powershell
python -m unittest discover -s tests -p test_transfer_queue.py -v
```

The focused suite uses only temporary local files and in-memory byte objects.
It includes 100 objects in 50 RAW/JPEG groups, source preservation, reload,
partial pairs, duplicates, file-number wrap, card/session changes, source
mutation/removal, path injection, bounded retries, ambiguous upload and rename,
hash-versus-size checks, corruption, TLS/auth/permission/quota classification,
cancel boundaries, malformed state, exclusive leases and failed local replace.
Exact interpreter, command, exit code and final count are recorded in the
sanitized session report, not inferred from this specification.

These are generic `offline-tested` subcases related to FTT-02..09/11; they do
not pass the complete FTT hardware/server acceptance rows. The separate lab adds
only its explicitly observed custom-peer/TLS/injected-fault results. Remaining
NOT RUN cases include actual camera file/capture completion events, native Wi-Fi,
camera-to-host API, sleep/power/card lifecycle, large camera files, real
non-ASCII path negotiation, hardware performance, Windows crash/power-loss
durability and independent-host reproduction.

Next FTP evidence: actual native constraints or a separately selected deployment
peer must be established before adapting the lab contract. Native FT-101 still
requires exact-target evidence before any native route can be selected.
