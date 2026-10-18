"""Opt-in loopback FTPS lab adapter; neither native FTP nor a camera bridge.

Only an audited lab server advertising LAB-NOCLOBBER-V1 is eligible. Importing
this module opens no socket. Construction explicitly connects to 127.0.0.1.
"""

from __future__ import annotations

import ftplib
import hashlib
import io
import math
import re
import ssl

from tools.transfer_queue import Observation, TransportError


MAX_BYTES = 32 * 1024 * 1024
_PATH = re.compile(r"/incoming/[0-9a-f]{64}\.(?:jpg|arw)(?:\.part)?\Z")
_FEATURE = "LAB-NOCLOBBER-V1"
_NOT_FOUND = "550 LAB-NOT-FOUND"
_COLLISION = "550 LAB-COLLISION"


class _PolicyError(ValueError):
    """Fixed-message local policy refusal, never arbitrary server text."""


class _ReadLimitError(ValueError):
    pass


def _port(value: object) -> int:
    if type(value) is not int or not 1024 <= value <= 65535:
        raise _PolicyError("loopback lab requires a supplied high TCP port")
    return value


def _path(value: object) -> str:
    if not isinstance(value, str) or not _PATH.fullmatch(value):
        raise _PolicyError("path is outside the constrained lab namespace")
    return value


def _credential(value: object) -> str:
    if (not isinstance(value, str) or not 1 <= len(value) <= 256
            or any(not 32 <= ord(c) <= 126 for c in value)):
        raise _PolicyError("lab credentials must be bounded printable ASCII")
    return value


def _classify(error: Exception, *, mutation: bool) -> TransportError:
    """Use fixed categories only. Unknown failures always require review."""
    if isinstance(error, TransportError):
        return TransportError(error.kind, uncertain=error.uncertain or mutation)
    if isinstance(error, ssl.SSLError):
        return TransportError("tls", uncertain=mutation)
    if isinstance(error, _PolicyError):
        return TransportError("permission", uncertain=mutation)
    if isinstance(error, _ReadLimitError):
        return TransportError("quota", uncertain=mutation)
    if isinstance(error, ftplib.error_perm):
        response = str(error).strip()
        if response.startswith("530 "):
            return TransportError("auth", uncertain=mutation)
        if response == _COLLISION:
            return TransportError("collision", uncertain=mutation)
        if response.startswith("550 "):
            return TransportError("permission", uncertain=mutation)
        if response.startswith("552 "):
            return TransportError("quota", uncertain=mutation)
    if isinstance(error, ftplib.error_temp) and str(error)[:4] in {"451 ", "421 "}:
        return TransportError("transient", uncertain=mutation)
    if isinstance(error, (OSError, EOFError)):
        return TransportError("transient", uncertain=mutation)
    return TransportError("transient", uncertain=True)


class _LoopbackFTP_TLS(ftplib.FTP_TLS):
    def makepasv(self) -> tuple[str, int]:
        # Inspect the advertised address rather than silently ignoring a bad one.
        host, port = ftplib.parse227(self.sendcmd("PASV"))
        if host != "127.0.0.1":
            raise _PolicyError("passive data endpoint must be numeric IPv4 loopback")
        return host, _port(port)


class LoopbackFTPSClient:
    """One verified, bounded lab connection with no retry/reconnect/delete path.

    There is no host parameter. Credentials stay in constructor locals and are
    never included in repr, debug output, persisted state or exception messages.
    The server feature is an audited lab extension, not standard FTP semantics.
    """

    def __init__(self, port: int, username: str, password: str, *,
                 cafile: str | None = None, timeout: float = 5.0):
        port = _port(port)
        username, password = _credential(username), _credential(password)
        if (type(timeout) not in {int, float} or not math.isfinite(timeout)
                or not 0.1 <= timeout <= 10):
            raise _PolicyError("lab timeout must be between 0.1 and 10 seconds")
        self._ftp: _LoopbackFTP_TLS | None = None
        self._secured = False
        try:
            context = ssl.create_default_context(cafile=cafile)
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            self._ftp = _LoopbackFTP_TLS(context=context, timeout=timeout)
            self._ftp.set_debuglevel(0)
            self._ftp.connect("127.0.0.1", port, timeout=timeout)
            if self._ftp.sock is None or self._ftp.sock.getpeername()[0] != "127.0.0.1":
                raise _PolicyError("control endpoint must be numeric IPv4 loopback")
            self._ftp.auth()  # AUTH TLS must complete before USER/PASS.
            self._ftp.login(username, password)
            self._ftp.prot_p()  # PBSZ 0 / PROT P; no clear data-channel fallback.
            self._ftp.set_pasv(True)
            features = self._ftp.sendcmd("FEAT")
            if _FEATURE not in {line.strip().upper() for line in features.splitlines()}:
                raise _PolicyError("audited exclusive-operation lab feature is required")
            self._secured = True
        except Exception as error:
            self.close()
            raise _classify(error, mutation=False) from None

    def check_security(self) -> None:
        if not self._secured or self._ftp is None or self._ftp.sock is None:
            raise TransportError("tls")

    def close(self) -> None:
        self._secured = False
        if self._ftp is not None:
            try:
                self._ftp.close()  # Local close, no QUIT/reconnect/cleanup command.
            except Exception:
                pass
            self._ftp = None

    def __enter__(self) -> LoopbackFTPSClient:
        self.check_security()
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def inspect(self, path: str) -> Observation | None:
        """Read and hash complete bounded bytes; only the fixed token means absent."""
        try:
            path = _path(path)
            self.check_security()
            digest = hashlib.sha256()
            size = 0
            # A missing RETR may already have opened the passive data socket.
            # Query SIZE first so absence cannot leave an unread TLS/data reply.
            self._ftp.voidcmd("TYPE I")
            try:
                expected_size = self._ftp.size(path)
            except ftplib.error_perm as error:
                if str(error).strip() == _NOT_FOUND:
                    return None
                raise
            if type(expected_size) is not int or expected_size < 0:
                raise _PolicyError("invalid lab size observation")
            if expected_size > MAX_BYTES:
                raise _ReadLimitError("lab size exceeds bounded object size")

            def consume(block: bytes) -> None:
                nonlocal size
                if not isinstance(block, bytes):
                    raise _PolicyError("invalid binary lab data")
                size += len(block)
                if size > MAX_BYTES:
                    raise _ReadLimitError("lab read exceeds bounded object size")
                digest.update(block)

            self._ftp.retrbinary("RETR " + path, consume, blocksize=64 * 1024)
            if size != expected_size:
                raise _PolicyError("full binary read disagrees with lab size observation")
            return Observation(size, digest.hexdigest())
        except ftplib.error_perm as error:
            self.close()
            raise _classify(error, mutation=False) from None
        except Exception as error:
            self.close()  # A failed RETR can leave an unread control reply.
            raise _classify(error, mutation=False) from None

    def upload_exclusive(self, path: str, data: bytes) -> None:
        try:
            path = _path(path)
            if not path.endswith(".part"):
                raise _PolicyError("uploads require a temporary lab object")
            if not isinstance(data, bytes) or not 0 < len(data) <= MAX_BYTES:
                raise _PolicyError("upload requires bounded nonempty immutable bytes")
            self.check_security()
        except Exception as error:
            raise _classify(error, mutation=False) from None
        try:
            self._ftp.storbinary("STOR " + path, io.BytesIO(data), blocksize=64 * 1024)
        except Exception as error:
            self.close()
            # A reply can be lost after STOR completed. Never infer non-application.
            raise _classify(error, mutation=True) from None

    def rename_exclusive(self, temporary: str, final: str) -> None:
        try:
            temporary, final = _path(temporary), _path(final)
            if not temporary.endswith(".part") or final != temporary[:-5]:
                raise _PolicyError("rename must finalize the same constrained lab identity")
            self.check_security()
        except Exception as error:
            raise _classify(error, mutation=False) from None
        try:
            self._ftp.rename(temporary, final)
        except Exception as error:
            self.close()
            # RNTO is never repeated after an ambiguous response.
            raise _classify(error, mutation=True) from None
