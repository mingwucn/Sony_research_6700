# FT-101: published FTP source-chain audit

2026-10-22. Reference: `xyzhangxin/sony-a6700-powerful` at
[`ac1cd0db5d0210292be1cee292d15034a222ae64`](https://github.com/xyzhangxin/sony-a6700-powerful/tree/ac1cd0db5d0210292be1cee292d15034a222ae64).
Evidence: **source-report**, **static-inference**, **offline-tested** static
consistency checks. No upstream execution, compilation, camera access, feature
support, recovery proof or device-write gate pass.

The new source makes Route A (existing native client behind menu/settings
restrictions) the first FTP research lead. It does not publish the underlying
Sony client source or independently establish its complete execution chain.
English remains a primary goal with no mechanism supplied by this project;
FL2/FL3 and calibrated looks remain deferred, and the host-assisted bridge is
separate. This audit does not change the old GDT analysis permissions or inputs.

## Verified scope and chain

Eighteen additional ordinary pinned texts were acquired privately: application
LICENSE, native transaction C source, profile/manifest JSON, request protocol,
native/profile build scripts, USB legacy/packet builder, desktop physical and
controller code, preparation/CLI, native/USB test source, preparation/notice
documents and source-provenance index. No ELF, application ZIP, firmware,
protocol-constant module or body input was acquired. Packet-builder and USB
source contain protocol constants; these were read as source only, not
activated or republished. Upstream instructions were not adopted.

Together with the prior review, **44 text blobs** match pinned-tree size,
Git-blob identity and SHA-256 receipts; **19 Python files** parse as ASTs.
Three canonical bindings hold: catalog to profile, profile to native manifest,
and native C source to manifest. This is not a reproducible-build result:
packaged binaries were neither obtained nor compared with a local build.
The manifest still labels hardware validation pending, and the profile labels
unified selection pending. Later author-reported trials have narrower scopes.

| Stage | Source observation | What it does not prove |
|---|---|---|
| Preparation | Human confirmations, host environment and cooperating-process locks precede service work. | Confirmed identity, exclusive ownership across all software/accounts, or authorization under this project's gates. |
| USB access | Discover one Sony MSC candidate, authenticate, transition to service identity, authenticate again, receive ProductInfo response. | The ProductInfo response is not parsed into an exact mainland firmware/SKU allowlist. Authentication and native reading occur before sparse compatibility acceptance. |
| Reader | Upload temporary constructor and request; read fixed profile sectors and return a nonce-bound response. | An ordinary R1 identification read. Temporary native execution is R2 and requires its own decision. |
| Compatibility | Physical operations inspect 260 sectors: 149 targets and 111 guards; known fields and unmanaged hashes are checked. | Whole installed-image identity, contents outside the window, or exact regional applicability. Whole-image normalization belongs to a different offline planner path. |
| Selection | Explicit FTP selection changes its fields and preserves other observed bytes in the plan. | Omitted selection is FTP-only: omission and initial desktop selection include all available features. |
| Dispatch | Exclusive durable preimages, targets and intent precede writer dispatch. | A durable journal before service transition, or an interlock against unresolved intents from an earlier session. |
| Native writer | Fixed profile, all supplied preimages, allowed-difference masks, per-sector prewrite comparison, write/fsync/readback, best-effort reverse rollback. | Source/binary equivalence, physical atomicity, elapsed-time bounds, power-loss recovery or a boot rescue path. |
| Host verification | Fresh-nonce independent reader normally compares current sectors with target and rechecks compatibility. | Guaranteed readback under cancellation; see finding F1. |

Static data checks map all **355 catalog fields exactly once**, without logical
or physical field overlap, with equal-length known values and in-bounds image/
sector placement. The current profile has **zero volatile-byte exclusions**.
FTP has 242 fields (90 App / 152 WBI); 240 bytes change (89 / 151), across
**82 sectors**. One FTP-containing target sector is shared with another
feature. FTP has no CP edit, but the common reader includes CP sectors and the
writer opens all configured devices read-write even for FTP-only selection.
Unchanged sectors are skipped. No offset, hash or mapping is adopted as an
owner-target support profile.

The native masks cover four available features and exclude the two parked
features. They do not encode which available feature the owner selected or
enumerate allowed values for each field. Those restrictions rely on host
planning. The writer binds supplied before-images to current sectors, not to
an independently authenticated stock whole-image identity. Writes and rollback
operate on complete sectors; a byte mask limits permitted differences but does
not make the storage operation byte-granular or atomic.

## Findings that block adopting this device path

**F1 — Cancellation and uncertain completion are not reconciled before cleanup.**
`desktop/controller.py:401` raises KeyboardInterrupt at a progress checkpoint
when cancellation is set. `operations.py:309` dispatches the writer, then
`:317` calls progress before the independent reader at `:318`. Cancellation
during the writer can therefore suppress the subsequent readback and produce
`uncertain`. The restore path has the same ordering at `:222`, `:228` and `:229`.
CLI context unwinding enters `UsbBackend.__exit__` before the outer uncertainty
handler; desktop PhysicalService receives uncertainty and calls close_session
(`desktop/physical.py:108`). Both reach `usb/backend.py:207`, which sends
STOP_SENSER without a reconciled-completion condition. No writer resend loop
was found in these current paths. The finding is a static control-flow mismatch
with this project's retain-state/needs_review rule, not an observed claim that
STOP damages hardware. Cancellation, pending native execution and cleanup
semantics must be resolved together before a device proposal.

**F2 — Compatibility is checked after temporary execution and remains sparse.**
`usb/backend.py:142` and `usb/legacy.py:575` lead into service authentication;
`device_profile.py:143` supplies the sparse compatibility decision afterward.
Plan model/firmware strings come from the catalog (`device_profile.py:230`).
Neither matching display version 2.00 nor these strings establishes this
body's ABI, reader applicability or exact regional build. An independently
supported pre-execution target identity and route prerequisite remain missing.

**F3 — Local journals do not enforce cross-session reconciliation.**
`operations.py:42` provides exclusive writes and flushes, and `:295`–`:309`
durably records mutation intent before dispatch. The inspected operation and
physical-service paths start new run directories without requiring resolution
of previous uncertain intents. Initial durable operation records also follow
authentication and initial native reading. This differs from the required
pre-operation journal and unresolved-state interlock. The user-scoped flock
is useful for cooperating clients; it does not exclude unrelated USB tools.

**F4 — Rollback is conditional and narrower than the owner's requirement.**
`native/transaction.c:130` performs reverse restoration using RAM preimages and
touched flags while that process is still running. It cannot resume after loss
of execution, power or service access. Retry counts in `:46` and `:58` do not
bound blocking syscall duration. Rollback writes whole before-sectors without
a new concurrent-state reconciliation step. Sparse backups restore selected
managed fields, do not cover all firmware/settings/calibration, and do not
establish two independent copies or a failed-boot restore route. `close` writes
canonical disabled values, which is not necessarily the previous recognized
partial/legacy state. A source inverse and a successful normal-boot reversal
would still leave failed-boot recovery unproved.

Additional host findings for a later adoption decision: `backup.py:299` reads
and decompresses sectors.bin before enforcing expected uncompressed length,
so the compressed archive cap alone does not bound host allocation. Also,
`desktop/controller.py:406` can leave busy set when service setup raises;
outer bridge/application recovery needs review before calling this a permanent
UI failure. No malicious archive or upstream executable was run to test either.

## Acceptance evidence matrix

| Requirement | Current evidence | Missing acceptance evidence |
|---|---|---|
| FT-01 manual native Wi-Fi | Author RAW+JPEG/home-network reports; native menu/settings recipes; no new client introduced by these edits. | Native worker/config/media/network dependency chain, exact body applicability, camera-origin endpoints, no relay and server hash equality. |
| FT-02 queue reliability | Native settings and author positive uploads. | Pair recovery, duplicates, partial transfer, card/file-number reuse, reconnect and cross-power-cycle reconciliation. |
| FT-03 automatic delivery | Native automatic-transfer setting and home-network report. | Physical-shutter completion/event chain, durable queue, cancellation, sleep/shutdown and measured shooting impact. |
| FT-04 security/privacy | Packaging/journal privacy measures and ordinary network settings claims. | Actual FTP/FTPS capability, certificate/hostname validation, credential storage, destination/path controls and collision policy. Source packaging privacy is not client security. |
| SAFE-01 | Checked static mapping and source guards; conditional in-process inverse. | Complete changed/protected-object coverage, exact inverse for current state, independent copies, safe uncertainty handling and reachable recovery routes. |
| REPRO-01 | Fixed source pin, verified text receipts and internally consistent public metadata. | Complete build inputs/toolchain equivalence, packaged binary reproduction, raw test evidence and exact supported body combinations. |

The FTP catalog's underlying research-record path is absent in both root and
application namespaces of the pinned tree. All six feature evidence indexes
are absent similarly. Public summaries support source-report labels only.
Native emulator tests were reviewed as text: they inject invented sectors and
selected syscall failures. They do not prove physical flash, power-failure,
kernel-lifetime or camera behavior, and were not executed by this audit.

## Decision and remaining offline work

**FT-101 remains partial.** Route A is the preferred research lead; no native
transfer implementation or device executor is integrated here. The verified
catalog/profile correspondence establishes useful source consistency only.
The owner recovery prerequisite and all device gates remain closed.

Next single package: **FT-101 complete the host USB takeover and session-lifetime
audit at the same pin**, covering the macOS capture helper and desktop bridge/
worker exception paths. Resolve which F1/F3 actions can occur after uncertain
native completion and assemble a concrete pre-contact go/no-go matrix from
these existing requirements. Read ordinary source only; no installation,
compilation, upstream execution, camera contact or automatic hardware proposal.

Source references: paths and line numbers above are within `应用/src/a6700_unlock/`
at the locked commit; `scripts/build_native.py` is under `应用/`. Local copies
and receipts are private. [Session commands/results](sessions/20261022-FT-101-source-chain.md).
