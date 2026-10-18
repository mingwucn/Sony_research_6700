# Offline inventory portability

Evidence class: **offline-tested**. This note concerns local synthetic files;
it establishes no camera access, backup completeness, feature support or device
write eligibility.

## Metadata comparison

RA-001 and RA-002 recorded false refusals on this Windows host when `Path.lstat`
and `os.fstat` returned different `st_ctime_ns` values for unchanged fixtures.
Those observations remain in their original reports. The underlying OS or
interpreter cause was not established.

The helper now compares device/inode identity, size and modification time when
matching a pathname to its opened descriptor. It compares the full fingerprint,
including `st_ctime_ns`, within each metadata API's sequence:

| Sequence | Compared metadata |
|---|---|
| Initial pathname to opened descriptor | Device, inode, size, modification time; regular-file checks |
| Descriptor before and after reading | Device, inode, size, modification time, change/creation time |
| Pathname before opening and after reading | Device, inode, size, modification time, change/creation time; regular-file checks |
| Final descriptor to final pathname | Device, inode, size, modification time |

This permits a stable difference between the APIs' ctime values without dropping
ctime-based mutation detection within either sequence. A changed inode or path,
changed same-size metadata, unexpected byte count, inaccessible input, or visible
symlink still refuses the entire result. Available `O_NOFOLLOW` and `O_NONBLOCK`
flags remain enabled. No retries or mutation operations were added.

These checks detect observable changes; they are not an atomic filesystem
snapshot or an adversarial-filesystem sandbox. Trusted intermediate directories
remain required. Filesystems with weak identity or timestamp semantics, changes
whose observable metadata is restored or unchanged, and changes after the final
check are not universally detectable. In particular, a ctime field that denotes
creation time does not promise content-change detection. Keep original artifacts
immutable and retain the acquisition/provenance evidence separately.

## Bounded inspection API

`inspect_artifact(path, prefix_limit=4096)` returns `(metadata, prefix_bytes)`.
The SHA-256, byte count and prefix come from the same descriptor read, with the
same refusal checks before a result is returned. The prefix limit must be an
integer from 0 through 4096; booleans and other types are refused. Prefix bytes
are private input and are not added to inventory JSON.

`hash_artifact(path)` still returns only `{"bytes": ..., "sha256": ...}` and
requests no prefix. Inventory JSON schema 1 and its unverified identity and
compatibility labels are unchanged. Tool version is now 0.2.0.

## Synthetic verification

On Windows AMD64 with CPython 3.13.12:

```text
python -m unittest discover -s tests -p test_offline_inventory.py -v
Exit: 0; 28 tests; 27 passed; 1 skipped; no failures or errors.
```

The suite includes deterministic cross-API ctime differences, ctime-only changes
within either API, before-open and after-open device/inode replacements,
same-size mutation, modified timestamps, short reads, read-error sanitization and
descriptor closure. Prefix tests cover exact source bytes from one read,
short/multi-chunk inputs, the default bound, zero length and invalid limits.

Deterministic symlink rejection runs without creating a symlink and verifies
that no descriptor is opened. The separate real-symlink test remains skipped
because this host cannot create that fixture. Mocked refusal coverage does not
establish real filesystem symlink behavior on this host. Other operating systems,
filesystems and Python versions were not tested in this session.

Camera commands: **none**. Network commands: **none**. No upstream code was run.
