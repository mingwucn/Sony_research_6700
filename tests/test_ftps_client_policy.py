"""Pure mocked FTPS policy tests. Default discovery creates no socket/listener."""

import ftplib
import hashlib
import ssl
import unittest
from unittest.mock import MagicMock, patch

from lab.ftps_client import LoopbackFTPSClient, _LoopbackFTP_TLS
from tools.transfer_queue import TransportError


class FTPSClientPolicyTests(unittest.TestCase):
    def setUp(self):
        self.factory_patch = patch("lab.ftps_client._LoopbackFTP_TLS", autospec=True)
        self.factory = self.factory_patch.start()
        self.addCleanup(self.factory_patch.stop)
        self.ftp = self.factory.return_value
        self.ftp.sock = MagicMock()
        self.ftp.sock.getpeername.return_value = ("127.0.0.1", 12345)
        self.ftp.sendcmd.return_value = "211-Features\n LAB-NOCLOBBER-V1\n211 End"
        self.ftp.size.return_value = 4
        self.socket_patch = patch("socket.create_connection", side_effect=AssertionError("policy tests must not open sockets"))
        self.socket_patch.start()
        self.addCleanup(self.socket_patch.stop)
        self.final = "/incoming/" + "a" * 64 + ".jpg"
        self.temporary = self.final + ".part"

    def client(self, **kwargs):
        result = LoopbackFTPSClient(12345, "lab-user", "synthetic-secret", **kwargs)
        self.addCleanup(result.close)
        return result

    def assert_error(self, operation, kind, uncertain=False):
        with self.assertRaises(TransportError) as caught:
            operation()
        self.assertEqual(caught.exception.kind, kind)
        self.assertEqual(caught.exception.uncertain, uncertain)
        self.assertEqual(str(caught.exception), kind)
        self.assertNotIn("synthetic-secret", repr(caught.exception))

    def test_verified_context_auth_before_credentials_and_protected_passive_data(self):
        context = ssl.create_default_context()
        with patch("lab.ftps_client.ssl.create_default_context", return_value=context) as create:
            client = self.client(cafile="synthetic-ca.pem", timeout=2)
        create.assert_called_once_with(cafile="synthetic-ca.pem")
        self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(context.check_hostname)
        self.assertGreaterEqual(context.minimum_version, ssl.TLSVersion.TLSv1_2)
        self.factory.assert_called_once_with(context=context, timeout=2)
        names = [call[0] for call in self.ftp.method_calls]
        self.assertLess(names.index("auth"), names.index("login"))
        self.assertLess(names.index("prot_p"), names.index("sendcmd"))
        self.ftp.connect.assert_called_once_with("127.0.0.1", 12345, timeout=2)
        self.ftp.set_pasv.assert_called_once_with(True)
        self.ftp.set_debuglevel.assert_called_once_with(0)
        self.assertNotIn("synthetic-secret", repr(client))
        client.check_security()

    def test_bad_ports_timeout_and_credential_controls_refused_before_connect(self):
        for port in (21, 1023, 65536, True, "12345"):
            with self.subTest(port=port), self.assertRaises(ValueError):
                LoopbackFTPSClient(port, "u", "p")
        for timeout in (0, 11, True, float("nan"), float("inf")):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                LoopbackFTPSClient(12345, "u", "p", timeout=timeout)
        for credential in ("", "x\r\nPASS y", "x\x00", "non-ascii-é", "x" * 257):
            with self.subTest(credential=credential), self.assertRaises(ValueError):
                LoopbackFTPSClient(12345, credential, "p")
        self.factory.assert_not_called()

    def test_auth_failure_never_sends_credentials_or_falls_back(self):
        self.ftp.auth.side_effect = ssl.SSLError("synthetic-secret server text")
        self.assert_error(self.client, "tls")
        self.ftp.login.assert_not_called()
        self.ftp.prot_p.assert_not_called()
        self.ftp.close.assert_called_once()

    def test_feature_missing_cannot_enable_mutations(self):
        for response in ("211 End", "211-Features\n X-LAB-NOCLOBBER-V1\n211 End",
                         "211-Features\n LAB-NOCLOBBER-V1 extra\n211 End"):
            self.ftp.sendcmd.return_value = response
            with self.subTest(response=response):
                self.assert_error(self.client, "permission")
        self.ftp.storbinary.assert_not_called()
        self.ftp.rename.assert_not_called()

    def test_control_peer_cannot_be_non_loopback(self):
        self.ftp.sock.getpeername.return_value = ("192.0.2.1", 12345)
        self.assert_error(self.client, "permission")
        self.ftp.auth.assert_not_called()

    def test_passive_host_and_port_are_strictly_loopback_high_port(self):
        # Exercise the real subclass policy without constructing or connecting it.
        ftp = object.__new__(_LoopbackFTP_TLS)
        ftp.sendcmd = MagicMock(return_value="227 Passive (127,0,0,1,48,57)")
        self.assertEqual(ftp.makepasv(), ("127.0.0.1", 12345))
        for response in ("227 Passive (192,0,2,1,48,57)", "227 Passive (127,0,0,1,0,21)"):
            ftp.sendcmd.return_value = response
            with self.subTest(response=response), self.assertRaises(ValueError):
                ftp.makepasv()

    def test_complete_retr_binary_hash_size_and_exact_notfound_token(self):
        client = self.client()
        blocks = (b"synthetic-", b"payload\x00\xff")

        def retrieve(command, consume, blocksize):
            self.assertEqual(command, "RETR " + self.final)
            self.assertEqual(blocksize, 64 * 1024)
            for block in blocks:
                consume(block)

        self.ftp.retrbinary.side_effect = retrieve
        self.ftp.size.return_value = len(b"".join(blocks))
        observation = client.inspect(self.final)
        self.assertEqual(observation.size, len(b"".join(blocks)))
        self.assertEqual(observation.sha256, hashlib.sha256(b"".join(blocks)).hexdigest())
        names = [call[0] for call in self.ftp.method_calls]
        self.assertLess(names.index("voidcmd"), names.index("size"))
        self.assertLess(names.index("size"), names.index("retrbinary"))
        self.ftp.size.side_effect = ftplib.error_perm("550 LAB-NOT-FOUND")
        self.assertIsNone(client.inspect(self.final))
        self.assertEqual(self.ftp.retrbinary.call_count, 1)
        self.ftp.voidcmd.assert_called_with("TYPE I")
        client.check_security()

    def test_size_only_is_not_hash_proof_and_changed_size_refused(self):
        client = self.client()
        self.ftp.size.return_value = 100
        self.ftp.retrbinary.side_effect = lambda command, consume, blocksize: consume(b"data")
        self.assert_error(lambda: client.inspect(self.final), "permission")
        self.ftp.retrbinary.assert_called_once()

    def test_only_size_exact_absence_token_means_absent(self):
        client = self.client()
        self.ftp.size.side_effect = ftplib.error_perm("550 LAB-NOT-FOUND extra")
        self.assert_error(lambda: client.inspect(self.final), "permission")
        self.ftp.retrbinary.assert_not_called()
        self.ftp.size.side_effect = None
        client = self.client()
        self.ftp.retrbinary.side_effect = ftplib.error_perm("550 LAB-NOT-FOUND")
        self.assert_error(lambda: client.inspect(self.final), "permission")
        self.assert_error(client.check_security, "tls")

    def test_550_permission_is_not_absence_and_server_text_is_discarded(self):
        client = self.client()
        self.ftp.retrbinary.side_effect = ftplib.error_perm("550 permission synthetic-secret")
        self.assert_error(lambda: client.inspect(self.final), "permission")
        self.ftp.close.assert_called_once()

    def test_read_limit_closes_desynchronized_session(self):
        client = self.client()

        def retrieve(command, consume, blocksize):
            consume(b"1234")
            consume(b"5")

        self.ftp.retrbinary.side_effect = retrieve
        with patch("lab.ftps_client.MAX_BYTES", 4):
            self.assert_error(lambda: client.inspect(self.final), "quota")
        self.assert_error(client.check_security, "tls")
        self.ftp.close.assert_called_once()

    def test_constrained_paths_and_same_identity_rename_before_mutation(self):
        client = self.client()
        for path in ("/incoming/../x", "ftp://127.0.0.1/x", "/outside/" + "a" * 64 + ".jpg",
                     self.final + "\r\nDELE x", "/incoming/" + "A" * 64 + ".jpg"):
            with self.subTest(path=path):
                self.assert_error(lambda: client.upload_exclusive(path, b"synthetic"), "permission")
        self.assert_error(lambda: client.upload_exclusive(self.final, b"synthetic"), "permission")
        self.assert_error(lambda: client.rename_exclusive(self.temporary, self.final.replace("a", "b")), "permission")
        self.ftp.storbinary.assert_not_called()
        self.ftp.rename.assert_not_called()

    def test_stor_binary_and_finalization_use_no_fallback_or_delete(self):
        client = self.client()
        self.ftp.storbinary.side_effect = lambda command, stream, blocksize: self.assertEqual(stream.read(), b"synthetic")
        client.upload_exclusive(self.temporary, b"synthetic")
        self.assertEqual(self.ftp.storbinary.call_args.args[0], "STOR " + self.temporary)
        client.rename_exclusive(self.temporary, self.final)
        self.ftp.rename.assert_called_once_with(self.temporary, self.final)
        self.ftp.delete.assert_not_called()
        self.ftp.prot_c.assert_not_called()
        self.ftp.quit.assert_not_called()

    def test_mutation_failures_are_uncertain_with_fixed_categories_and_no_retry(self):
        cases = ((ftplib.error_perm("530 synthetic-secret"), "auth"),
                 (ftplib.error_perm("550 LAB-COLLISION"), "collision"),
                 (ftplib.error_perm("550 synthetic-secret"), "permission"),
                 (ftplib.error_perm("552 synthetic-secret"), "quota"),
                 (ftplib.error_temp("451 synthetic-secret"), "transient"),
                 (ftplib.error_temp("421 synthetic-secret"), "transient"),
                 (ssl.SSLError("synthetic-secret"), "tls"),
                 (RuntimeError("synthetic-secret"), "transient"))
        for error, kind in cases:
            with self.subTest(error=type(error).__name__, kind=kind):
                self.ftp.reset_mock()
                client = self.client()
                self.ftp.storbinary.side_effect = error
                self.assert_error(lambda: client.upload_exclusive(self.temporary, b"synthetic"), kind, True)
                self.ftp.storbinary.assert_called_once()
                self.ftp.connect.assert_called_once()
                self.assert_error(client.check_security, "tls")
                self.ftp.storbinary.side_effect = None

    def test_rename_lost_reply_is_uncertain_and_not_repeated(self):
        client = self.client()
        self.ftp.rename.side_effect = TimeoutError("synthetic-secret")
        self.assert_error(lambda: client.rename_exclusive(self.temporary, self.final), "transient", True)
        self.ftp.rename.assert_called_once()
        self.assert_error(lambda: client.rename_exclusive(self.temporary, self.final), "tls")
        self.ftp.rename.assert_called_once()

    def test_read_only_known_temporary_errors_are_bounded_without_retry(self):
        for response in ("451 synthetic-secret", "421 synthetic-secret"):
            self.ftp.reset_mock()
            client = self.client()
            self.ftp.retrbinary.side_effect = ftplib.error_temp(response)
            with self.subTest(response=response):
                self.assert_error(lambda: client.inspect(self.final), "transient")
            self.ftp.retrbinary.assert_called_once()
            self.ftp.connect.assert_called_once()

    def test_context_close_is_local_and_closed_client_cannot_mutate(self):
        with self.client() as client:
            client.check_security()
        self.ftp.close.assert_called_once()
        self.ftp.quit.assert_not_called()
        self.assert_error(client.check_security, "tls")
        self.assert_error(lambda: client.upload_exclusive(self.temporary, b"synthetic"), "tls")
        self.ftp.storbinary.assert_not_called()


if __name__ == "__main__":
    unittest.main()
