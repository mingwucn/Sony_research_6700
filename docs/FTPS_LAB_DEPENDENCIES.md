# FT-102 isolated host laboratory dependencies

This is a host-only dependency/extraction record. It supplies no camera route,
native FTP result or host-assisted bridge. The seven runtime artifacts in
`references/host-lab.lock.json` are separate from camera-reference pins in
`references/sources.lock.json`. Artifact identification and static review are
`offline-tested`/`static-inference`; they do not establish native binary safety,
server interoperability or distribution rights for every bundled component.

## Selected artifacts and provenance

The lock targets the observed **CPython 3.13.12, Windows AMD64** host only.
Changing Python/platform or an artifact requires a new review/lock. Public PyPI
metadata and downloaded artifacts were retained in a new ignored directory,
`external/ft102-reviewed-artifacts-20261018`. Whole-file SHA-256 matches the
official metadata for all seven runtime artifacts. All six runtime wheels have
complete, unique RECORD member sets and correct SHA-256/length entries. None
contains `.pth` startup hooks or archive symlinks. The additional downloaded
cryptography 46.0.5 wheel is a comparison artifact and is excluded from the
runtime lock; it is not asserted identical to the installed Conda distribution.

| Component | Exact runtime artifact | Reviewed terms / dependency decision |
|---|---|---|
| pyftpdlib 2.2.0 | `pyftpdlib-2.2.0.tar.gz` | MIT. Only source archive available; export reviewed package source without building. |
| pyasynchat 1.0.5 | `pyasynchat-1.0.5-py3-none-any.whl` | PSF-2.0. Requires pyasyncore >=1.0.2; selected exact 1.0.5. |
| pyasyncore 1.0.5 | `pyasyncore-1.0.5-py3-none-any.whl` | PSF-2.0; no external runtime dependency. |
| pyOpenSSL 26.4.0 | `pyopenssl-26.4.0-py3-none-any.whl` | Apache-2.0. Requires cryptography >=49,<51. |
| cryptography 50.0.0 | `cryptography-50.0.0-cp311-abi3-win_amd64.whl` | Apache-2.0 OR BSD-3-Clause; requires cffi >=2.0.0 on CPython. Contains `_rust.pyd`. |
| cffi 2.0.0 | `cffi-2.0.0-cp313-cp313-win_amd64.whl` | Actual wheel LICENSE says MIT No Attribution (MIT-0), with per-file exceptions; metadata says MIT. Requires pycparser on CPython. Contains `_cffi_backend...pyd`. |
| pycparser 2.23 | `pycparser-2.23-py3-none-any.whl` | BSD-3-Clause, with separate retained PLY 3.9 BSD headers. No external runtime dependency. |

Primary metadata: [pyftpdlib](https://pypi.org/pypi/pyftpdlib/2.2.0/json),
[pyasynchat](https://pypi.org/pypi/pyasynchat/1.0.5/json),
[pyasyncore](https://pypi.org/pypi/pyasyncore/1.0.5/json),
[pyOpenSSL](https://pypi.org/pypi/pyOpenSSL/26.4.0/json),
[cryptography](https://pypi.org/pypi/cryptography/50.0.0/json),
[cffi](https://pypi.org/pypi/cffi/2.0.0/json),
[pycparser](https://pypi.org/pypi/pycparser/2.23/json).

On Python 3.13, the selected metadata does not require typing-extensions.
cryptography's bcrypt dependency belongs to the unselected SSH extra. The
server's dev/test extras, pywin32/WindowsAuthorizer and optional OS-user
impersonation are not selected. The existing host cryptography 46.0.5 does not
satisfy selected PyOpenSSL 26.4.0; global packages are not upgraded or reused by
this preparation. Exact archive `Requires-Dist` headers are stored separately
from PyPI JSON because cryptography's metadata formatting differs in quotes
and spaces; the tool checks exact archived headers rather than implementing a
partial dependency-expression normalizer.

pyftpdlib's annotated tag object is
`08f25ef1f02962bcc1b9170641061a67cd3fa336`, peeled commit
`ace15a9ef5e60e14ecc25788025821f3f5d364f9`, tree
`ed70c4e2e6aa334bdeb6138e8503a00b841bbd9b`. Its source archive's **20 package
files**, LICENSE and pyproject.toml byte-match that Git commit. The ignored
Git clone has no worktree checkout; index deletion entries reflect this
objects-only state and are not described as a clean checked-out source tree.
The archive's unpinned setuptools build backend is never executed.
[Pinned source](https://github.com/giampaolo/pyftpdlib/tree/ace15a9ef5e60e14ecc25788025821f3f5d364f9),
[build metadata](https://github.com/giampaolo/pyftpdlib/blob/ace15a9ef5e60e14ecc25788025821f3f5d364f9/pyproject.toml).

The two compatibility modules' wheel source bytes match their pinned primary
sources: [asynchat at 1aa4388...](https://github.com/simonrob/pyasynchat/blob/1aa4388d7a168c8a39ec9b7685fe1bc29a152342/asynchat/__init__.py)
and [asyncore at 0efd128...](https://github.com/simonrob/pyasyncore/blob/0efd128e882c5f02bb587560ff6fb3066bf5982b/asyncore/__init__.py).
Their maintainers describe the code as legacy compatibility material without
continued core maintenance; this is a bounded test-server choice, not a new
production server design.

## Static execution and protocol review

AST parsing inspected 20 server, 7 PyOpenSSL, 78 cryptography, 18 cffi, 17
pycparser and the two compatibility-module Python files without importing
them. This is a call-site/import inventory, not exhaustive control-flow or
native-code proof. Server/PyOpenSSL code has no direct eval/exec/subprocess
sites in that inventory. cffi contains compiler/pkgconfig/build helpers that
can invoke subprocess/exec/eval; pycparser/PLY contains parser/table-generation
exec/eval sites. Those APIs and build paths are outside the proposed TLS
server runtime. Preserve their source/notices; do not describe the packages
as universally execution-free. The intended path uses published native
bindings rather than runtime compilation, and DummyAuthorizer rather than
OS-user impersonation. Importing the TLS runtime will load native Python
extensions and initialize OpenSSL; preparation itself performs no such import.

Both selected native payloads are PE AMD64. ABI compatibility is the wheel's
declaration pending actual isolated import/runtime testing. No native
disassembly, reproducible rebuild or complete bundled OpenSSL/libffi/Rust
component licence/provenance closure was established. Published package hashes
and RECORD hashes identify bytes; they do not prove source-to-binary identity.

The source review found contract gaps that the lab harness must handle:

- STOR defaults to `w`/`wb` at `handlers/ftp/control.py:1564,1579`; it can
  truncate an existing file. `filesystems.py:259` delegates rename to
  `os.rename`, called by RNTO at `handlers/ftp/control.py:2061,2072`.
  Platform-specific rename behaviour does not prove the mock's race-free
  no-clobber semantics. Review a constrained server extension and test an
  actual destination collision before queue integration.
- TLS control/data enforcement defaults to false at
  `handlers/ftps/control.py:68,69`. Explicitly require both. Supply a configured
  server context with minimum TLS 1.2 before accepting any connection.
- Passive data sockets bind the control socket's local address at
  `handlers/ftp/dispatchers.py:45,66`; bind control to literal `127.0.0.1`,
  assert every data bind/peer stays loopback, disable PORT/EPRT, retain foreign
  address refusal and do not configure a masquerade address.
- Host CPython ftplib.py:715 uses `_create_stdlib_context()` when FTP_TLS is
  given no context. Supply `ssl.create_default_context(cafile=private_lab_CA)`
  with hostname checks/CERT_REQUIRED explicitly; do not rely on the default.
  Protect the data channel with `prot_p()`. Generate private disposable
  certificate/key fixtures; never reuse upstream demo/test private keys or
  modify the host trust store.

Pinned [STOR/RNTO source](https://github.com/giampaolo/pyftpdlib/blob/ace15a9ef5e60e14ecc25788025821f3f5d364f9/pyftpdlib/handlers/ftp/control.py),
[filesystem source](https://github.com/giampaolo/pyftpdlib/blob/ace15a9ef5e60e14ecc25788025821f3f5d364f9/pyftpdlib/filesystems.py),
[TLS source](https://github.com/giampaolo/pyftpdlib/blob/ace15a9ef5e60e14ecc25788025821f3f5d364f9/pyftpdlib/handlers/ftps/control.py),
[passive source](https://github.com/giampaolo/pyftpdlib/blob/ace15a9ef5e60e14ecc25788025821f3f5d364f9/pyftpdlib/handlers/ftp/dispatchers.py),
[Python FTP_TLS documentation](https://docs.python.org/3.13/library/ftplib.html#ftp-tls-objects)
and [RFC 4217](https://datatracker.ietf.org/doc/html/rfc4217).

## Safe preparation interface

Run the repository's authored standard-library tool after placing exactly the
locked artifacts in an existing private/ignored directory. It does no download
and does not use pip, setup.py, package build backends or upstream launchers.

```powershell
python -I -S tools/prepare_ftps_lab.py --artifact-dir external/ft102-reviewed-artifacts-20261018 --verify-only
python -I -S tools/prepare_ftps_lab.py --artifact-dir external/ft102-reviewed-artifacts-20261018 --environment private/ftps-lab-20261018
```

The environment parent must exist; the environment itself must be NEW. The
tool verifies every artifact before creating the directory, creates a stdlib
venv without pip/system packages, and writes files exclusively. It checks
whole-file hashes/lengths, exact metadata, every wheel RECORD hash/path,
archive bounds, duplicate/case-colliding/unsafe Windows paths, symlinks/devices,
unexpected roots/native payloads and startup hooks. It never calls extractall.
Only the 20 reviewed server source files and its LICENSE/PKG-INFO are exported;
demo keys, test runners, external scripts and the build backend are not exported. All
wheel licence files, original metadata and per-file notices remain alongside
their code. A partial new environment is retained for local review and is not
automatically deleted or reused. The parent preparation interpreter uses
`-I -S` to suppress user/PYTHONPATH injection and site startup hooks. The
artifact/environment directories must remain under the owner's control;
this is not a sandbox against hostile concurrent filesystem replacement.

The complete server package includes its `__main__.py` source for provenance,
but the upstream `python -m pyftpdlib` CLI is outside the reviewed harness:
its defaults permit an anonymous service and an all-interface listener.
Use only the repository's reviewed, explicitly constrained lab entry point.

The intended subsequent runtime entry point is the environment's
`Scripts/python.exe -I <reviewed host lab harness>`. Isolated mode suppresses
user site/PYTHONPATH injection; any necessary repository-module path must be
an explicit reviewed harness choice. Merely preparing this environment starts
no server or socket and imports no third-party package. Runtime imports,
certificate generation and loopback endpoints belong to the next separately
recorded host-lab steps. The preparation record contains exact lock/artifact
identities and flags stating which actions were not performed.

## Reuse limits and remaining evidence

Retain MIT/PSF/Apache/BSD notices, applicable NOTICE files and per-file PLY
headers when copying or distributing components; mark modifications where
required. cffi's top licence explicitly permits per-file exceptions. The
PyOpenSSL and cryptography licence files were compared with pinned primary
sources, but this does not clear every native bundled dependency. No project
licence is selected or inherited implicitly. These artifacts are accepted
only for an isolated local lab; complete component rights/provenance remain a
publication/distribution blocker.
[Server MIT licence](https://github.com/giampaolo/pyftpdlib/blob/ace15a9ef5e60e14ecc25788025821f3f5d364f9/LICENSE),
[PyOpenSSL licence](https://github.com/pyca/pyopenssl/blob/07b1ef7cc2ed71c77ebc113d0c10fc045e40861a/LICENSE),
[cryptography licence](https://github.com/pyca/cryptography/blob/dcb7050b807b00392fa9fe2eac7cb362fcf355cc/LICENSE),
[cffi licence](https://github.com/python-cffi/cffi/blob/6366c01d84e9a78e7e85f12ebe9760ba5d19b6d3/LICENSE).

Actual FTP/FTPS endpoint behaviour, certificate/hostname rejection, encrypted
data channels, upload/finalization fault injection, complete server equality,
platform rename races and native import behaviour remain NOT RUN at dependency
preparation time. Their evidence must come from the independent server/client
harness. No camera command, native-transfer result or device-write gate follows
from this lock or from passing archive checks.

Subsequent observed runtime results are recorded separately in the
[loopback lab](FTPS_LOOPBACK_LAB.md) and its session report. The final isolated
Windows run passed 19 cases; this does not resolve bundled-component publication
rights, source-to-native-binary identity or target compatibility.
