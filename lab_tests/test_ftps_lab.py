"""Synthetic loopback interoperability tests, invoked only by run_ftps_lab.py.

Files and certificates are retained in the new private workspace. No camera,
external address, endpoint discovery or production credential is accepted.
"""
from dataclasses import replace
import ftplib
import hashlib
import io
from pathlib import Path
import socket
import ssl
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

from lab.ftps_client import LoopbackFTPSClient
from lab.ftps_server import LoopbackServer, make_certificate
from tools.transfer_queue import Capture, QueueError, TransferQueue, TransportError


WORKSPACE: Path | None = None
SERVERS: list[LoopbackServer] = []


class LoopbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if WORKSPACE is None:
            raise RuntimeError("use the reviewed opt-in lab runner")
        cls.certificate, cls.key = make_certificate(WORKSPACE / "tls-fixture")

    def setUp(self):
        self.root = WORKSPACE / self._testMethodName
        self.root.mkdir()
        self.spool = self.root / "spool"
        self.spool.mkdir()
        self.queue = TransferQueue.create(self.root / "queue.json", self.spool)
        self.addCleanup(lambda: self.queue.close())
        self.server = self.server_at("server")
        self.capture = Capture("synthetic-body", "lab-session", "card-A", "object-1",
                               1, "DSC00001.JPG", "JPEG")
        self.payload = b"synthetic fixture, not a photograph\x00\xff" * 128

    def server_at(self, name, **kwargs):
        server = LoopbackServer(self.root / name, self.certificate, self.key, **kwargs)
        server.start()
        SERVERS.append(server)
        self.addCleanup(server.stop)
        return server

    def client(self, server=None, **kwargs):
        server = server or self.server
        client = LoopbackFTPSClient(server.port, server.username, server.password,
                                    cafile=str(self.certificate), **kwargs)
        self.addCleanup(client.close)
        return client

    def raw(self, *, protected=True, server=None):
        server = server or self.server
        context = ssl.create_default_context(cafile=str(self.certificate))
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        ftp = ftplib.FTP_TLS(context=context, timeout=5)
        self.addCleanup(ftp.close)
        ftp.connect("127.0.0.1", server.port)
        ftp.auth()
        ftp.login(server.username, server.password)
        if protected:
            ftp.prot_p()
        ftp.voidcmd("TYPE I")
        return ftp

    def enqueue(self, *, payload=None):
        data = self.payload if payload is None else payload
        with (self.spool / "fixture.bin").open("xb") as stream:
            stream.write(data)
        identity = self.queue.enqueue(self.capture, "fixture.bin")
        return identity, self.queue.paths(identity)

    def reload(self):
        self.queue.close()
        self.queue = TransferQueue.load(self.root / "queue.json", self.spool)

    def remote(self, path):
        return self.server.incoming / path.rsplit("/", 1)[1]

    def assert_source(self, payload=None):
        self.assertEqual((self.spool / "fixture.bin").read_bytes(),
                         self.payload if payload is None else payload)

    def test_100_objects_50_groups_full_readback_and_reload(self):
        expected, groups = {}, set()
        for index in range(100):
            kind, sequence = ("RAW" if index % 2 == 0 else "JPEG"), index // 2
            data = hashlib.sha256(str(index).encode("ascii")).digest() * (index + 1)
            name = f"fixture-{index:03d}.bin"
            with (self.spool / name).open("xb") as stream:
                stream.write(data)
            capture = replace(self.capture, object_id=f"object-{index}", capture_sequence=sequence,
                              filename=f"DSC{sequence:05d}.{'ARW' if kind == 'RAW' else 'JPG'}",
                              format=kind, expected_formats=("RAW", "JPEG"))
            identity = self.queue.enqueue(capture, name)
            expected[identity] = (name, data)
            groups.add(self.queue.entries[identity]["group_id"])
        self.reload()
        client = self.client()
        for identity, (name, data) in expected.items():
            self.assertEqual(self.queue.run_one(identity, client), "committed",
                             self.queue.entries[identity]["reason"])
            temporary, final = self.queue.paths(identity)
            self.assertEqual(self.remote(final).read_bytes(), data)
            self.assertFalse(self.remote(temporary).exists())
            self.assertEqual((self.spool / name).read_bytes(), data)
        self.assertEqual(self.server.events.count("upload_requested"), 100)
        self.assertEqual(self.server.events.count("finalized"), 100)
        self.assertEqual(len(list(self.server.incoming.iterdir())), 100)
        self.assertTrue(all(self.queue.group_status(group)["complete"] for group in groups))
        self.reload()
        self.assertTrue(all(entry["state"] == "committed" for entry in self.queue.entries.values()))

    def test_certificate_trust_and_hostname_fail_closed(self):
        with self.assertRaises(TransportError) as caught:
            LoopbackFTPSClient(self.server.port, self.server.username, self.server.password)
        self.assertEqual(caught.exception.kind, "tls")
        context = ssl.create_default_context(cafile=str(self.certificate))
        ftp = ftplib.FTP_TLS(context=context, timeout=5)
        self.addCleanup(ftp.close)
        ftp.connect("127.0.0.1", self.server.port)
        # This changes only the expected certificate name after the numeric
        # connect. No DNS lookup or connection to this invented name occurs.
        ftp.host = "mismatch.invalid"
        with self.assertRaises(ssl.SSLCertVerificationError):
            ftp.auth()
        self.assertEqual(list(self.server.incoming.iterdir()), [])

    def test_plaintext_login_clear_data_and_active_mode_refused(self):
        plain = ftplib.FTP(timeout=5)
        self.addCleanup(plain.close)
        plain.connect("127.0.0.1", self.server.port)
        with self.assertRaises(ftplib.error_perm):
            plain.sendcmd("USER synthetic")
        ftp = self.raw(protected=False)
        with self.assertRaises(ftplib.error_perm):
            ftp.sendcmd("PASV")
        with self.assertRaises(ftplib.error_perm):
            ftp.sendcmd("PROT C")
        ftp.prot_p()
        with self.assertRaises(ftplib.error_perm):
            ftp.sendcmd("PORT 127,0,0,1,200,1")
        self.client().check_security()

    def test_authentication_failure_has_fixed_category(self):
        with self.assertRaises(TransportError) as caught:
            LoopbackFTPSClient(self.server.port, self.server.username, "deliberately-wrong",
                               cafile=str(self.certificate))
        self.assertEqual(caught.exception.kind, "auth")
        self.assertNotIn("deliberately-wrong", str(caught.exception))
        self.assertNotIn(self.server.password, str(caught.exception))
        self.assertEqual(self.server.events, [])

    def test_unconstrained_endpoint_refused_and_stock_stor_overwrite_observed(self):
        comparison = self.server_at("stock-stor-comparison", constrained=False)
        with self.assertRaises(TransportError) as caught:
            self.client(comparison)
        self.assertEqual(caught.exception.kind, "permission")
        ftp = self.raw(server=comparison)
        path = "/incoming/" + "a" * 64 + ".jpg.part"
        ftp.storbinary("STOR " + path, io.BytesIO(b"long synthetic original"))
        ftp.storbinary("STOR " + path, io.BytesIO(b"short"))
        self.assertEqual((comparison.incoming / path.rsplit("/", 1)[1]).read_bytes(), b"short")

    def test_existing_temporary_and_final_are_preserved(self):
        identity, (temporary, final) = self.enqueue()
        self.remote(temporary).write_bytes(b"retained partial")
        self.assertEqual(self.queue.run_one(identity, self.client()), "needs_review")
        self.assertEqual(self.queue.reconcile(identity, self.client()), "needs_review")
        self.assertEqual(self.remote(temporary).read_bytes(), b"retained partial")
        same_size_collision = b"X" * len(self.payload)
        self.remote(final).write_bytes(same_size_collision)
        self.assertEqual(self.queue.reconcile(identity, self.client()), "needs_review")
        self.assertEqual(self.remote(final).read_bytes(), same_size_collision)
        self.assertEqual(self.server.events, [])
        self.assert_source()

    def test_concurrent_exclusive_upload_has_one_winner(self):
        _, (temporary, _) = self.enqueue()
        clients = [self.client(), self.client()]
        barrier = threading.Barrier(2, timeout=5)
        payloads = [b"A" * 8192, b"B" * 8192]

        def upload(index):
            barrier.wait()
            try:
                clients[index].upload_exclusive(temporary, payloads[index])
                return "success"
            except TransportError as error:
                return error.kind

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(upload, (0, 1)))
        self.assertEqual(sorted(results), ["collision", "success"])
        self.assertEqual(self.remote(temporary).read_bytes(), payloads[results.index("success")])
        self.assertEqual(self.server.events.count("upload_requested"), 1)

    def test_concurrent_finalization_preserves_winner(self):
        _, (temporary, final) = self.enqueue()
        self.client().upload_exclusive(temporary, self.payload)
        clients = [self.raw(), self.raw()]
        for client in clients:
            self.assertTrue(client.sendcmd("RNFR " + temporary).startswith("350"))
        barrier = threading.Barrier(2, timeout=5)

        def finalize(index):
            barrier.wait()
            try:
                return clients[index].sendcmd("RNTO " + final)[:3]
            except ftplib.Error as error:
                return str(error)[:3]

        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(finalize, (0, 1)))
        self.assertEqual(results.count("250"), 1)
        self.assertIn(next(result for result in results if result != "250"), {"550"})
        self.assertEqual(self.remote(final).read_bytes(), self.payload)
        self.assertEqual(self.server.events.count("finalized"), 1)

    def test_destination_appearing_after_rnfr_is_never_overwritten(self):
        _, (temporary, final) = self.enqueue()
        client = self.client()
        client.upload_exclusive(temporary, self.payload)
        ftp = self.raw()
        self.assertTrue(ftp.sendcmd("RNFR " + temporary).startswith("350"))
        retained = b"external synthetic winner"
        with self.remote(final).open("xb") as stream:
            stream.write(retained)
        with self.assertRaises(ftplib.error_perm) as caught:
            ftp.sendcmd("RNTO " + final)
        self.assertEqual(str(caught.exception), "550 LAB-COLLISION")
        self.assertEqual(self.remote(final).read_bytes(), retained)
        self.assertEqual(self.remote(temporary).read_bytes(), self.payload)
        self.assertEqual(self.server.events.count("finalized"), 0)
        self.assert_source()

    def test_active_upload_cannot_be_finalized_by_second_session(self):
        _, (temporary, final) = self.enqueue()
        ftp = self.raw()
        data = ftp.transfercmd("STOR " + temporary)
        self.addCleanup(data.close)
        data.sendall(self.payload)
        other = self.raw()
        with self.assertRaises(ftplib.error_temp) as caught:
            other.sendcmd("RNFR " + temporary)
        self.assertEqual(str(caught.exception), "450 LAB-UPLOAD-IN-FLIGHT")
        self.assertFalse(self.remote(final).exists())
        data.unwrap().close()
        self.assertTrue(ftp.voidresp().startswith("226"))
        self.client().rename_exclusive(temporary, final)
        self.assertEqual(self.remote(final).read_bytes(), self.payload)

    def test_abandoned_pending_upload_releases_active_marker(self):
        _, (temporary, _) = self.enqueue()
        ftp = self.raw()
        # Request a passive listener but never establish the data connection.
        ftp.sendcmd("PASV")
        self.assertTrue(ftp.sendcmd("STOR " + temporary).startswith("150"))
        self.assertTrue(self.server.active_uploads)
        ftp.quit()  # Server processes close before replying to a new session.
        other = self.raw()
        self.assertTrue(other.sendcmd("RNFR " + temporary).startswith("350"))
        client = self.client()
        self.assertFalse(self.server.active_uploads)
        observation = client.inspect(temporary)
        self.assertEqual(observation.size, 0)
        self.assertTrue(self.remote(temporary).exists())

    def test_deferred_tls_close_keeps_open_upload_guarded(self):
        from pyftpdlib.handlers.ftps.ssl import SSLConnectionMixin

        _, (temporary, final) = self.enqueue()
        ftp = self.raw()
        data = ftp.transfercmd("STOR " + temporary)
        self.addCleanup(data.close)
        data.sendall(self.payload)
        original, held = SSLConnectionMixin._do_ssl_shutdown, []

        def defer_data_shutdown(channel):
            handle = getattr(channel, "file_obj", None)
            if handle is not None and not handle.closed:
                held.append(channel)
                return  # Simulate WantRead/WantWrite deferring data/file close.
            return original(channel)

        with patch.object(SSLConnectionMixin, "_do_ssl_shutdown", new=defer_data_shutdown):
            ftp.close()
            other = self.raw()
            with self.assertRaises(ftplib.error_temp) as caught:
                other.sendcmd("RNFR " + temporary)
            self.assertEqual(str(caught.exception), "450 LAB-UPLOAD-IN-FLIGHT")
            self.assertTrue(held)
            self.assertTrue(any(not channel.file_obj.closed for channel in held))
            self.assertTrue(self.server.active_uploads)
            self.assertFalse(self.remote(final).exists())
        data.close()  # Restore normal closure; server cleanup owns its channels.
        self.assert_source()

    def test_thread_start_failure_closes_bound_listener(self):
        server = LoopbackServer(self.root / "startup-failure", self.certificate, self.key)
        with patch("lab.ftps_server.threading.Thread.start", side_effect=RuntimeError("synthetic start failure")):
            with self.assertRaises(RuntimeError):
                server.start()
        self.assertIsNone(server._thread)
        self.assertTrue(server._server.socket is None or server._server.socket.fileno() == -1)
        server.stop()

    def test_upload_completion_loss_reload_and_read_only_reconciliation(self):
        identity, (temporary, final) = self.enqueue()
        self.server.upload_fault = "drop_after_upload"
        self.assertEqual(self.queue.run_one(identity, self.client()), "needs_review")
        self.assertEqual(self.remote(temporary).read_bytes(), self.payload)
        self.reload()
        before = list(self.server.events)
        client = self.client()
        self.assertEqual(self.queue.reconcile(identity, client), "ready_to_finalize")
        self.assertEqual(self.server.events, before)
        self.assertFalse(self.remote(final).exists())
        self.assertEqual(self.queue.run_one(identity, client), "committed")
        self.assertEqual(self.server.events.count("upload_requested"), 1)
        self.assert_source()

    def test_partial_upload_disconnect_preserves_evidence_without_retry(self):
        payload = b"synthetic partial disconnect\x00" * 16384
        identity, (temporary, final) = self.enqueue(payload=payload)
        self.server.upload_fault = "partial_disconnect"
        self.assertEqual(self.queue.run_one(identity, self.client()), "needs_review")
        partial = self.remote(temporary).read_bytes()
        self.assertGreater(len(partial), 0)
        self.assertLess(len(partial), len(payload))
        self.reload()
        before = list(self.server.events)
        self.assertEqual(self.queue.reconcile(identity, self.client()), "needs_review")
        self.assertEqual(self.server.events, before)
        with self.assertRaises(QueueError):
            self.queue.run_one(identity, self.client())
        self.assertEqual(self.remote(temporary).read_bytes(), partial)
        self.assertFalse(self.remote(final).exists())
        self.assert_source(payload)

    def test_rename_reply_loss_reconciles_without_second_mutation(self):
        identity, (_, final) = self.enqueue()
        self.server.rename_fault = "drop_after_rename"
        self.assertEqual(self.queue.run_one(identity, self.client()), "needs_review")
        self.assertEqual(self.remote(final).read_bytes(), self.payload)
        self.reload()
        before = list(self.server.events)
        self.assertEqual(self.queue.reconcile(identity, self.client()), "committed")
        self.assertEqual(self.server.events, before)
        self.assert_source()

    def test_interrupted_link_unlink_keeps_both_and_reconciles_read_only(self):
        identity, (temporary, final) = self.enqueue()
        self.server.rename_fault = "after_link"
        self.assertEqual(self.queue.run_one(identity, self.client()), "needs_review")
        self.assertEqual(self.remote(final).read_bytes(), self.payload)
        self.assertEqual(self.remote(temporary).read_bytes(), self.payload)
        self.reload()
        before = list(self.server.events)
        self.assertEqual(self.queue.reconcile(identity, self.client()), "committed")
        self.assertEqual(self.server.events, before)
        self.assertTrue(self.remote(temporary).exists())
        self.assert_source()

    def test_permission_and_quota_are_uncertain_then_explicitly_reconciled(self):
        for index, fault in enumerate(("permission", "quota")):
            with self.subTest(fault=fault):
                name = f"fixture-{index}.bin"
                (self.spool / name).write_bytes(self.payload)
                identity = self.queue.enqueue(replace(self.capture, capture_sequence=index), name)
                self.server.upload_fault = fault
                self.assertEqual(self.queue.run_one(identity, self.client()), "needs_review")
                self.assertEqual(self.queue.entries[identity]["reason"], "uncertain_" + fault)
                self.assertEqual(self.queue.reconcile(identity, self.client()), "ready")
                self.assertEqual((self.spool / name).read_bytes(), self.payload)
        self.assertEqual(self.server.events.count("upload_requested"), 0)

    def test_receiver_bound_and_listener_shutdown(self):
        limited = self.server_at("bounded-server", receive_limit=1024)
        path = "/incoming/" + "b" * 64 + ".jpg.part"
        with self.assertRaises(TransportError) as caught:
            self.client(limited).upload_exclusive(path, b"X" * 65536)
        self.assertTrue(caught.exception.uncertain)
        partial = (limited.incoming / path.rsplit("/", 1)[1]).read_bytes()
        self.assertLessEqual(len(partial), 1024)
        self.assertIn("receive_bound_disconnect", limited.events)
        port = limited.port
        limited.stop()
        self.assertFalse(limited._thread.is_alive())
        # Exact known lab listener only; never enumerate ports or other devices.
        with self.assertRaises(OSError):
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                pass
