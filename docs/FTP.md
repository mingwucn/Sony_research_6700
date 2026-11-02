Latest FT-101 completion & GUI integration (2026-11-01): [Playback FTP action discovery](../research/sessions/20261031-playback-ftp-action-discovery.md), [GUI & documentation session](../research/sessions/20261101-customizer-gui-and-documentation.md), [technical architecture](TECHNICAL_ARCHITECTURE.md). In `/usr/lib/appFw.so` (CN1 Ver. 2.00), Playback Custom Key label `"FTP Transfer"` / `"FTP传输"` (Resource ID `0x021c668e`) is bound in the Playback Custom Key table at `0x03666b70` to **Action ID `0x0817` (`2071`)**. The custom key dispatcher (`0x01440d0c`) indexes the 8-byte master capability table (`0x03f14c38 + 0x0817 * 8 = 0x03f17ce0`), where availability gate **`0x03f17ce4`** was `0x00` (disabled). Patching **`0x03f17ce4`** (`00` -> `01`, ext2 Sector `445966` + `0xE4` on `/dev/nflasha15`) alongside the 9 Network FTP menu gates (`0x05a5`–`0x05b0` at `0x03f17524`–`0x03f17564`) unlocks both full Network FTP settings and Playback Custom Key single-button upload (`设置 -> 操作自定义 -> 回放自定义键设置 -> FTP传输`). Integrated into `apps/a6700_customizer/` with 76/76 passing offline unit tests. Earlier entries below retain historical scopes.

> **Hardware status correction (2026-11-02):** Owner reports English menu working and Network FTP accessible, but Playback/Gallery FTP still unavailable. The `0x0817` byte patch is a **static candidate, not a demonstrated runtime fix**. See [FT-101 regression issue #1](https://github.com/mingwucn/Sony_research_6700/issues/1); do not interpret 76 offline tests or target-byte readback as successful FTP transfer.


Current FT-101 source audit (2026-10-22): [source chain and acceptance gaps](../research/FTP_SOURCE_CHAIN_AUDIT.md). 44 pinned text blobs / 19 ASTs and 355 field mappings verified; no upstream execution. Cancellation can suppress independent readback, and uncertain outcomes can trigger service exit; sparse compatibility and in-process rollback do not qualify this body or recovery. Native English and FTP remain primary and unvalidated. Camera commands: none. Next single package: FT-101: complete the pinned host USB takeover/session-lifetime source audit, including macOS capture helper and desktop bridge/worker exception paths; resolve uncertain-completion cleanup and persistent reconciliation findings into an explicit pre-contact go/no-go matrix. Ordinary source only; no installation, compilation, upstream execution or camera contact.

# FTP support: native-first research and a separate bridge

Scope: the alpha6700 acts as an outbound file-transfer client to an owner-controlled server. It is not an FTP server exposing the camera filesystem. Initial native success is manual upload over Wi-Fi with no intermediate host; automatic post-capture upload follows. Work packages FT-101 through FT-106 apply. Sources S3-S6 are in REFERENCE_ANALYSIS.md.

## 1. What is established and what is not

The inspected alpha6700 menu guide does not list FTP. This is a documentation observation, not proof that every relevant backend was stripped from the owner's firmware. The alpha7 IV has documented native FTP functionality and can inform behaviour/donor comparison. Its binary layout and libraries are not presumed compatible.

Sony documents alpha6700 PC Remote over Wi-Fi/USB and image storage on a computer. The SDK lists ILCE-6700, but supported interfaces and operations must be verified for a selected SDK/firmware combination. In particular, generic SDK Wi-Fi support is not evidence that every model supports every Wi-Fi API. SDK availability also does not establish background download of arbitrary existing card files or physical-shutter event support.

## 2. Native feasibility tree

```text
A. Complete FTP backend present but gated?
   yes -> trace configuration/UI/event path; minimal exact-target enablement
   no/uncertain -> B. Partial backend or compatible resident networking APIs?
       yes -> evaluate a small target-native client and its missing integrations
       no -> C. Compare a documented donor's module/ABI/dependency requirements
             and decide whether a bounded port is justified
A/B/C not currently actionable -> retain native status as blocked/unproven
                                  and optionally build D. host-assisted bridge
```

Investigate A before writing a new client. Do not conclude A from strings alone. Do not assume C is simpler than B: transplanting a dynamically linked donor service can require unavailable APIs, resource IDs, settings schemas and lifecycle infrastructure. A negative result in A does not prove native FTP impossible; it changes the implementation class and risk.

## 3. Static and runtime evidence to collect

Inventory AP executables/libraries, configuration tables, network managers, task/service registrations, UI resources and authentication/certificate mechanisms. Search decoded strings and symbol/xref material for FTP-related commands, schemes, transfer/error messages, remote-path handling, queue concepts and security options. Examples include USER/PASS, STOR, PASV/EPSV, REST, RNFR/RNTO and AUTH TLS. Such strings are leads only; they may be unused, shared or server-side code.

Trace a prospective upload from menu or capture event through file selection, credentials, connection establishment, data transfer, result/status update and cleanup. Identify which process owns Wi-Fi, DNS, sockets and power management. Determine whether a transfer module is actually linked/loaded and whether its task entry and settings schema exist. Assess mode restrictions rather than setting a guessed FTP enable bit.

For any donor candidate, compare instruction set, endian mode, executable ABI, loader, libc/libstdc++ versions, exported functions, IPC/service IDs, filesystem/media APIs, certificate APIs, resource IDs and persistent configuration format. Prefer adapting the target's native primitives over introducing a large foreign runtime. Record unresolved imports as blockers. Do not copy donor CP/sensor components for a transfer feature without independently established necessity.

Dynamic observation is allowed only through an approved route and an owner-controlled network. Avoid broad network scans. Packet traces and diagnostic dumps may expose credentials and device identifiers; keep them private. Native code execution to test a socket is R2, and installing a persistent daemon/startup hook is R4, not an ordinary read.

## 4. Route A: reuse a native hidden client

Prove that menu visibility, capability permission, settings storage, file-selection integration, transfer worker and status reporting are all connected. A visible FTP menu with an unavailable task is not support. Identify exact regional/model constraints and ensure that enabling transfer does not alter unrelated networking identity or bypass authentication.

First construct an offline candidate and a control-flow test for invalid/missing configuration. The first approved hardware proof is one non-sensitive file to an isolated server. Confirm camera-resident execution and endpoint addresses, record server-side byte count/hash and verify that no PC relay process supplied the file. Only then add queue, automatic transfer and user-facing error handling.

## 5. Route B/C: implement or port a bounded onboard client

The client should depend on confirmed target facilities for media enumeration, safe completed-file access, Wi-Fi/network lifecycle, persistent settings and status/UI. It must not read partially written captures, monopolize the media device, disable capture safety checks or continuously run while nominally off.

Develop and test protocol/queue logic on the host first using synthetic files and an isolated server. Compile target code only after the ABI/toolchain is pinned. A transient one-shot transfer on an approved target precedes any persistence/startup integration. The lifecycle contract must define startup trigger, stop/cancel, sleep, shutdown, card removal, recording, low battery and loss of network.

Prefer a small event-driven integration with bounded buffers, bounded retries and cooperative resource use. Determine supported event APIs rather than inventing a hook into an unknown function. If an application-level hook is required, it needs the same instruction/control-flow and load-placement review as a colour-processing patch. Do not hide an unreviewed resident process in a supposedly data-only configuration change.

## 6. Protocol and integrity specification

FTP, explicit FTPS and SFTP are different protocols. Plain FTP is permitted only as a clearly identified isolated-laboratory or otherwise deliberately accepted mode; it must not be described as encrypted. Prefer explicit FTPS where a validated TLS stack and certificate validation are available. SFTP is a separately implemented SSH-based option, not an FTPS checkbox. Verify protocol details against the selected client/server documentation and relevant specifications before implementation.

The first protocol subset is passive-mode binary upload to a constrained destination. Keep credentials in a private local/on-device configuration mechanism with narrowly defined access; do not put passwords in source, CLI process arguments, logs, packets shared to GitHub, or readable release profiles. Validate server certificate trust/hostname when using TLS. Never turn off validation merely to make a test pass, and never silently fall back to plaintext after TLS failure.

Define exact remote path handling, filename encoding, directory creation policy, allowed characters and collision policy. Prevent path traversal and unintended overwrite. Use a unique temporary destination and a verified finalization step when the server supports it. Do not claim that FTP rename is universally atomic or that every server supports the same resume semantics. Probe and document capabilities.

Transfer in binary mode. Validate a completed upload using server-side SHA-256 where available, or download/read-back on the lab server and compare hashes. Size alone is weaker evidence. A successful protocol response does not prove end-to-end equality after an ambiguous disconnect. Keep the original on the card and host spool by default; automatic source deletion is outside the initial scope.

## 7. Queue and capture semantics

Specify a durable queue record with body alias, media/session identity, object identifier where available, capture sequence, relative filename, file size, completion evidence, content hash when practical, destination, attempt count and state. Do not identify an image only by basename: filenames wrap and cards can be swapped. RAW/JPEG pairs are separate objects linked by a capture group; record partial-pair completion explicitly.

```text
observed -> waiting_for_capture_completion -> ready -> transferring
-> remote_verification_pending -> committed
                         -> retryable_error / permanent_error / needs_review
```

A file's unchanged size for a short interval is a heuristic, not proof that the camera finished writing it. Prefer a confirmed capture-complete/media API; otherwise qualify the adapter's weaker guarantee and do not delete the source. A mass-storage connection may constrain capture, so that behaviour must be measured on the selected mode rather than assumed.

Use bounded exponential retry with jitter for established retryable network errors. Keep authentication failures, unavailable media, unsupported format and permission failures distinct. A connection loss after upload may leave a complete remote file; reconcile by identity/hash before resending. Exactly-once delivery cannot be promised from a bare FTP connection alone. Design idempotent destination naming and reconciliation, and state remaining server-dependent cases.

Persist queue updates so restart cannot silently forget an in-progress file. Test card removal/reinsertion, filename reuse, long filenames, non-ASCII names, server full, quota exceeded, permission denied and two files with identical names. Do not format or delete camera media during queue recovery.

## 8. Shooting, power and operational limits

Measure unmodified capture-to-ready time, burst behaviour, UI responsiveness, startup, battery use and temperature under a reproducible workload. Then repeat with transfers enabled and disabled. Set an acceptable overhead target with the owner before release; do not invent a universal throughput or battery claim.

Start with manual upload outside active recording. Automatic physical-shutter capture, continuous bursts, RAW/JPEG pairs, movies and sleep-state persistence are separate tests. Prefer postponing/reducing network work over disrupting a capture. Define cancellation and progress reporting so a user can distinguish queued, transferring, failed and verified states.

Do not modify Wi-Fi country/channel restrictions to obtain connectivity. Preserve normal pairing/authentication and existing Creators/PC Remote behaviour. A network daemon should not become remotely reachable unless its service is explicitly part of the feature; the project requires an outbound client, not a general shell or camera file server.

## 9. Route D: practical host-assisted bridge

This can be developed without firmware mutation after normal PC Remote/SDK use is approved. The architecture is:

```text
camera -- supported PC Remote/SDK transfer --> private host spool
       --> completion/identity checks --> durable queue
       --> FTP or FTPS uploader --> owner-controlled server
```

The camera-to-host leg and host-to-server leg have independent capabilities/security. Start with documented Imaging Edge Remote saving to a host folder, or the selected SDK's supported capture/download API. Verify whether the physical shutter produces transferable events, whether existing card images can be fetched, whether the camera also saves to card, and which formats/modes are supported. Do not advertise wireless automatic transfer merely because remote-triggered USB capture works.

Prototype the spool/queue/uploader entirely with synthetic files. Apply the same integrity, credential, path, retry and no-source-deletion rules as the native client. For folder watching, do not treat file creation alone as completion; prefer a documented producer-completion signal or copy/stability validation and disclose limitations. Use a tiny existing-file test before a shooting session.

A bridge is labelled HOST-ASSISTED in UI, README, test results and release names. It requires a running intermediary and does not satisfy FT-01. Maintain a separate branch/module so bridge success cannot obscure unfinished native research. This fallback can coexist with continuing native investigation.

## 10. Deliverables and go/no-go

Produce a native-backend presence/absence-evidence report, dependency/ABI matrix, selected-route decision, protocol capability specification, synthetic server harness, queue model, security review and exact hardware trial proposal. Record an explicit native status: uninvestigated, evidence gathered, feasible candidate, one-file proven, queue proven, or operationally validated.

Native FTP is accepted only when a physical camera-resident transfer is demonstrated and data equality is verified. A menu, linked socket library, host upload or emulator result does not close it. Failure to find backend code by string search alone is not an exhaustive impossibility result.
