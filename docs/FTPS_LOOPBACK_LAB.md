# FT-102: isolated synthetic FTPS laboratory

This opt-in lab tests the durable queue against an independent pyftpdlib-based
peer on literal **127.0.0.1**. It is host evidence only: no native camera FTP,
camera-to-host adapter, host-assisted bridge or device gate passes. The default
standard-library `tests/` suite never starts this server. The lab requires the
separately reviewed Windows runtime in the [dependency audit](FTPS_LAB_DEPENDENCIES.md)
and [host-lab lock](../references/host-lab.lock.json).

## Executable boundary

Importing `lab/ftps_server.py` loads no third-party code and opens no socket.
Its explicit `start()` loads the reviewed TLS/server runtime and binds an
ephemeral high port on IPv4 loopback. Passive data sockets inherit that address.
PORT/EPRT, REST/APPE, arbitrary filenames, listing, deletion and directory
creation are absent from its command allowlist. The file namespace is only
`/incoming/<64 lowercase hex>.jpg|arw[.part]`. Suffixes are synthetic format
labels, not validated photographs. Receive/read bounds are 32 MiB, not a camera
file-size capability.

The endpoint requires TLS on control and data channels, minimum TLS 1.2 and
PROT P. Random credentials and a new one-day certificate/private key stay
private; no host trust store changes. Windows chmod does not establish a
private NTFS ACL: an owner-controlled private directory is a precondition.
No production credentials, camera inputs or external host argument are accepted.

`lab/ftps_client.py` requires a high port, verifies certificate trust and IP
name, performs AUTH TLS before credentials, and requires protected passive
binary transfers. It refuses advertised non-loopback data addresses and missing
lab capabilities. There is no plaintext fallback, reconnect/retry loop, remote
cleanup or source deletion. Errors expose fixed categories. Mutation failures
remain uncertain and close the session.

## Custom server contract

Ordinary FTP does not guarantee the queue's exclusive operations. The observed
unconstrained STOR comparison overwrote/truncated a synthetic file. Upstream
RNTO delegates to platform-dependent os.rename; this is no universal atomic or
no-overwrite guarantee. The client requires this reviewed peer's explicit
**LAB-NOCLOBBER-V1** extension:

- STOR accepts temporary names only and creates with `xb`.
- Finalization exclusively links a closed temporary to a new final name, then
  unlinks the temporary. A destination appearing after RNFR is preserved.
  Link/unlink is not an atomic rename or a power-loss durability proof.
- Open uploads remain guarded across sessions, including deferred TLS closure.
  Pending uploads release markers only after the actual file closes.
- Only exact authenticated `550 LAB-NOT-FOUND` from SIZE establishes absence.
  Generic FTP 550 can mean permission denial; it is not proof of absence.
- Present objects are fully retrieved and SHA-256 hashed with exact length
  agreement. SIZE alone never establishes equality.

The filesystem is a trusted single-owner fixture, not a sandbox against hostile
directory, junction, hard-link or ACL replacement. The feature token is an
audited configuration contract, not attestation of an arbitrary server.

## Running and retaining evidence

After reviewing artifacts and preparing a NEW environment as documented in the
dependency audit, use that environment's Python and isolated mode. The workspace
in this example must be NEW:

```powershell
private/ftps-lab-20261018/Scripts/python.exe -I tools/run_ftps_lab.py --artifact-dir external/ft102-reviewed-artifacts-20261018 --workspace private/ftps-run-NEW
```

The runner re-verifies locked archives and all 220 extracted package files,
requires the matching preparation record, adds only this repository to the
isolated interpreter's path, and exclusively creates the private workspace.
A prepared journal precedes test imports, TLS fixtures and listeners. All
spools, queue states, logs and keys remain private and are retained after
failure. Existing environments/workspaces are refused. Run one lab at a time;
inspect a missing result or failed cleanup before another NEW run. Never blindly
retry the failed queue or delete its evidence.

`lab_tests/` is outside default discovery and CI. Direct execution without its
configured workspace refuses. Test cleanup closes clients, queue leases and
servers. The runner fails if any registered lab thread/control listener remains
open. The shutdown probe uses one exact known lab port, with no port enumeration.

## Observed coverage and limits

The [session report](../research/sessions/20261018-FT-102-loopback.md) records
exact commands, failures and counts. Coverage includes 100 files/50 synthetic
RAW/JPEG groups; full read-back and reload; same-size wrong-hash content;
temporary/final preservation; concurrent creation/finalization; a destination
created after RNFR; certificate/name/authentication rejection; clear control/data
and active-mode refusal; injected permission/quota/partial-upload/lost-reply
faults; interrupted link/unlink; forced deferred TLS closure; receive bounds;
startup failure; and shutdown. The final run passed **19 cases**, with **21 lab
servers stopped, zero live lab threads and zero open lab control listeners**.

Read-only reconciliation never uploads or renames: a matching temporary permits
a separate bounded finalization call; a matching final can be recorded committed
without repeating mutation. Partial/mismatching objects remain untouched.
Interrupted link/unlink deliberately preserves both names. Sources remain intact.

Injected host faults are not physical Wi-Fi loss, a genuinely full disk, OS
permission changes, process crashes or power failure. No real photo decoder,
non-ASCII negotiation, arbitrary server, camera lifecycle, shooting performance,
thermal/battery behavior, independent-host reproduction or native ABI constraint
is qualified. Native source-to-binary correspondence and complete bundled-component
publication rights remain unresolved. FT-102 remains partial for those native
and deployment constraints; FT-103 is not started.

Next single host package: **IN-102 clean authored-tree offline reproduction**,
without private artifacts, the lab runtime or reference checkouts. Actual remote
CI remains NOT RUN. Target-specific RA-003 still needs installed firmware and
legitimate matching-package provenance. Camera commands: **none**.
