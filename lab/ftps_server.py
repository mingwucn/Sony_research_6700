"""Constrained, opt-in loopback test endpoint, using separately reviewed dependencies.

This is a lab peer, not a production server or camera component. Importing this
module loads no third-party code and starts no socket. Only start() does so.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import logging
import os
from pathlib import Path
import re
import secrets
import threading


NAME = re.compile(r"[0-9a-f]{64}\.(?:jpg|arw)(?:\.part)?\Z")
MAX_BYTES = 32 * 1024 * 1024


def make_certificate(directory: Path) -> tuple[Path, Path]:
    """Create a new private, one-day self-signed fixture; alter no trust store."""
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID
    import ipaddress

    directory.mkdir()
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "FT102 synthetic loopback")])
    now = datetime.now(timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
            .public_key(key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(now - timedelta(minutes=1)).not_valid_after(now + timedelta(days=1))
            .add_extension(x509.SubjectAlternativeName([x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]), critical=False)
            .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
            .sign(key, hashes.SHA256()))
    certificate, private_key = directory / "certificate.pem", directory / "private-key.pem"
    for path, data in ((certificate, cert.public_bytes(serialization.Encoding.PEM)),
                       (private_key, key.private_bytes(serialization.Encoding.PEM,
                        serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))):
        with path.open("xb") as stream:
            stream.write(data)
        os.chmod(path, 0o600)
    return certificate, private_key


class LoopbackServer:
    """One private server thread, ephemeral credentials, explicit fault controls.

    Fault controls affect this invented endpoint only. Socket loss is not a
    physical Wi-Fi test. Finalization uses exclusive hard-link then unlink;
    it is no-clobber but not an atomic rename or a power-loss durability proof.
    """

    def __init__(self, root: Path, certificate: Path, key: Path, *, constrained: bool = True,
                 receive_limit: int = MAX_BYTES):
        if type(receive_limit) is not int or not 1 <= receive_limit <= MAX_BYTES:
            raise ValueError("invalid lab receive bound")
        self.root = Path(root).resolve()
        self.root.mkdir()
        self.incoming = self.root / "incoming"
        self.incoming.mkdir()
        self.certificate, self.key = certificate, key
        self.username, self.password = "synthetic", secrets.token_urlsafe(24)
        self.constrained = constrained
        self.receive_limit = receive_limit
        # Keep the actual open handle: a TLS close may defer file closure.
        self.active_uploads: dict[str, object] = {}
        self.upload_fault: str | None = None
        self.rename_fault: str | None = None
        self.events: list[str] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._server = None
        self.thread_error: str | None = None
        self.port = 0

    def start(self) -> LoopbackServer:
        from OpenSSL import SSL
        from pyftpdlib.authorizers import DummyAuthorizer
        from pyftpdlib.handlers import TLS_FTPHandler
        from pyftpdlib.handlers.ftps.data import TLS_DTPHandler
        from pyftpdlib.ioloop import IOLoop
        from pyftpdlib.servers import FTPServer

        if self._thread is not None:
            raise RuntimeError("server already started")
        owner = self
        # No raw command/path/password logging; retain only bounded event names.
        logger = logging.getLogger("pyftpdlib")
        logger.setLevel(logging.CRITICAL)
        logger.handlers = [logging.NullHandler()]
        logger.propagate = False

        class DataChannel(TLS_DTPHandler):
            ac_in_buffer_size = 1024

            def recv(self, size):
                if (self.receive and self.file_obj is not None and
                        self.tot_bytes_received >= 1024 and owner.upload_fault == "partial_disconnect"):
                    owner.upload_fault = None
                    owner.events.append("partial_data_disconnect")
                    self.cmd_channel.close()
                    return b""
                if self.receive and self.file_obj is not None:
                    chunk = super().recv(min(size, owner.receive_limit - self.tot_bytes_received + 1))
                    if self.tot_bytes_received + len(chunk) > owner.receive_limit:
                        owner.events.append("receive_bound_disconnect")
                        self.cmd_channel.close()
                        return b""
                    return chunk
                return super().recv(size)

        class Handler(TLS_FTPHandler):
            tls_control_required = True
            tls_data_required = True
            dtp_handler = DataChannel
            timeout = 5
            auth_failed_timeout = 0.01
            permit_foreign_addresses = False
            permit_privileged_ports = False
            use_sendfile = False
            encoding = "ascii"
            banner = "FT102 synthetic loopback lab"
            proto_cmds = {k: v for k, v in TLS_FTPHandler.proto_cmds.items() if k in {
                "AUTH", "USER", "PASS", "PBSZ", "PROT", "FEAT", "TYPE", "PASV",
                "EPSV", "STOR", "RETR", "SIZE", "RNFR", "RNTO", "QUIT", "NOOP"}}

            def __init__(self, *args, **kwargs):
                self._drop_upload_response = False
                super().__init__(*args, **kwargs)
                if self.connected and owner.constrained:
                    self._extra_feats.append("LAB-NOCLOBBER-V1")

            def log(self, *args, **kwargs):
                pass

            def log_cmd(self, *args, **kwargs):
                pass

            def log_transfer(self, *args, **kwargs):
                pass

            def close(self):
                pending = getattr(self, "_in_dtp_queue", None)
                pending_file = pending[0] if pending is not None else None
                try:
                    return super().close()
                finally:
                    # Upstream pending-STOR cleanup closes the file without
                    # calling on_incomplete_file_received. A TLS close can
                    # defer actual resource closure; never release an open file.
                    if pending_file is not None and pending_file.closed:
                        owner.active_uploads.pop(pending_file.name, None)

            def _active(self, file):
                if file not in owner.active_uploads:
                    return False
                handle = owner.active_uploads[file]
                if handle is not None and handle.closed:
                    # Reap a deferred pending-control close only after closure.
                    owner.active_uploads.pop(file, None)
                    return False
                return True

            def _valid(self, file):
                path = Path(file)
                return (path.parent == owner.incoming and NAME.fullmatch(path.name) is not None
                        and not path.is_symlink())

            def respond(self, response, *args, **kwargs):
                if response.startswith("226 ") and self._drop_upload_response:
                    self._drop_upload_response = False
                    owner.events.append("upload_response_lost")
                    self.close()
                    return
                return super().respond(response, *args, **kwargs)

            def ftp_PROT(self, line):
                if line.upper() != "P":
                    self.respond("550 LAB-TLS-REQUIRED")
                    return
                return super().ftp_PROT(line)

            def ftp_STOR(self, file, mode="w"):
                if not self._valid(file) or not file.endswith(".part"):
                    self.respond("550 LAB-PERMISSION")
                    return
                if owner.upload_fault in {"permission", "quota"}:
                    fault, owner.upload_fault = owner.upload_fault, None
                    owner.events.append(fault + "_refused")
                    self.respond("552 LAB-QUOTA" if fault == "quota" else "550 LAB-PERMISSION")
                    return
                if owner.constrained and Path(file).exists():
                    self.respond("550 LAB-COLLISION")
                    return
                self._drop_upload_response = owner.upload_fault == "drop_after_upload"
                if self._drop_upload_response:
                    owner.upload_fault = None
                owner.events.append("upload_requested")
                # Exclusive creation is the deciding operation, including races.
                owner.active_uploads[file] = None
                try:
                    result = super().ftp_STOR(file, mode="x" if owner.constrained else "w")
                except Exception:
                    owner.active_uploads.pop(file, None)
                    raise
                if result is None:
                    owner.active_uploads.pop(file, None)
                else:
                    owner.active_uploads[file] = (self.data_channel.file_obj if self.data_channel is not None
                                                  else self._in_dtp_queue[0])
                return result

            def on_file_received(self, file):
                owner.active_uploads.pop(file, None)

            def on_incomplete_file_received(self, file):
                owner.active_uploads.pop(file, None)

            def ftp_RETR(self, file):
                if not self._valid(file):
                    self.respond("550 LAB-PERMISSION")
                elif not Path(file).exists():
                    self.respond("550 LAB-NOT-FOUND")
                elif not Path(file).is_file() or Path(file).stat().st_size > MAX_BYTES:
                    self.respond("550 LAB-PERMISSION")
                else:
                    return super().ftp_RETR(file)

            def ftp_SIZE(self, file):
                if not self._valid(file):
                    self.respond("550 LAB-PERMISSION")
                elif not Path(file).exists():
                    self.respond("550 LAB-NOT-FOUND")
                else:
                    return super().ftp_SIZE(file)

            def ftp_RNFR(self, file):
                if not self._valid(file) or not file.endswith(".part"):
                    self.respond("550 LAB-PERMISSION")
                elif self._active(file):
                    self.respond("450 LAB-UPLOAD-IN-FLIGHT")
                elif not Path(file).exists():
                    self.respond("550 LAB-NOT-FOUND")
                else:
                    return super().ftp_RNFR(file)

            def ftp_RNTO(self, file):
                source, self._rnfr = self._rnfr, None
                if (source is None or not self._valid(file) or not self._valid(source)
                        or source != file + ".part"):
                    self.respond("550 LAB-PERMISSION")
                    return
                if self._active(source):
                    self.respond("450 LAB-UPLOAD-IN-FLIGHT")
                    return
                try:
                    if owner.constrained:
                        os.link(source, file)  # Fails if destination already exists.
                        if owner.rename_fault == "after_link":
                            owner.rename_fault = None
                            owner.events.append("final_link_response_lost")
                            self.close()
                            return
                        os.unlink(source)
                    else:
                        os.replace(source, file)  # Explicit unsafe lab comparison.
                except FileExistsError:
                    self.respond("550 LAB-COLLISION")
                except FileNotFoundError:
                    self.respond("550 LAB-NOT-FOUND")
                except OSError:
                    self.respond("451 LAB-STORAGE")
                else:
                    owner.events.append("finalized")
                    if owner.rename_fault == "drop_after_rename":
                        owner.rename_fault = None
                        owner.events.append("rename_response_lost")
                        self.close()
                    else:
                        self.respond("250 LAB-FINALIZED")
                        return source, file

        authorizer = DummyAuthorizer()
        # SIZE is guarded by the upstream metadata/listing permission 'l'.
        # LIST/MLSD remain absent from the command allowlist.
        authorizer.add_user(self.username, self.password, str(self.root), perm="elrwf")
        Handler.authorizer = authorizer
        context = SSL.Context(SSL.TLS_SERVER_METHOD)
        context.set_min_proto_version(SSL.TLS1_2_VERSION)
        context.use_certificate_chain_file(str(self.certificate))
        context.use_privatekey_file(str(self.key))
        context.check_privatekey()
        Handler.ssl_context = context
        self._server = FTPServer(("127.0.0.1", 0), Handler, ioloop=IOLoop())
        self._server.max_cons = 16
        self._server.max_cons_per_ip = 16
        assert self._server.socket.getsockname()[0] == "127.0.0.1"
        self.port = self._server.socket.getsockname()[1]

        def serve():
            try:
                while not self._stop.is_set():
                    self._server.serve_forever(timeout=0.02, blocking=False, handle_exit=False)
            except Exception as exc:
                self.thread_error = type(exc).__name__
            finally:
                try:
                    self._server.close_all()
                except Exception as exc:
                    self.thread_error = "shutdown_" + type(exc).__name__

        self._thread = threading.Thread(target=serve, name="FT102-loopback-lab", daemon=True)
        try:
            self._thread.start()
        except BaseException:
            self._server.close_all()
            self._thread = None
            raise
        return self

    def stop(self) -> None:
        if self._thread is not None:
            self._stop.set()
            self._thread.join(timeout=5)
            if self._thread.is_alive():
                raise RuntimeError("lab server did not stop; inspect live thread")
            if self.thread_error:
                raise RuntimeError("lab server failed: " + self.thread_error)
            if self._server.socket is not None and self._server.socket.fileno() != -1:
                raise RuntimeError("lab listener remains open after shutdown")

    def __enter__(self):
        return self.start()

    def __exit__(self, *_):
        self.stop()
