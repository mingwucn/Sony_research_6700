"""Synthetic tests for optional, same-pass FDAT signature identification."""
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

from tools import artifact_probe, ufu_inventory


def frame(*chunks):
    return b"\x89UFU\r\n\x1a\n" + b"".join(
        struct.pack(">I4s", len(payload), tag) + payload for tag, payload in chunks
    )


def identify(data, **kwargs):
    return ufu_inventory.index_stream(
        io.BytesIO(data), len(data), hashlib.sha256(data).hexdigest(), **kwargs
    )


class SequentialStream(io.BytesIO):
    """Make a second pass, oversized read or unbounded read observable."""

    def __init__(self, data, *, short_reads=False):
        super().__init__(data)
        self.requests = []
        self.short_reads = short_reads

    def read(self, size=-1):
        if not 0 < size <= 1024 * 1024:
            raise AssertionError("read exceeds bounded stream policy")
        position = self.tell()
        result = super().read(min(size, 3) if self.short_reads else size)
        self.requests.append((position, size, len(result)))
        return result

    def seek(self, *args):
        raise AssertionError("a prefix probe must not seek or reread")


class FDATSignatureTests(unittest.TestCase):
    def test_exact_eight_byte_signature_and_minimum_declared_size(self):
        for size in (512, 513, 4096, 1000000):
            with self.subTest(size=size):
                self.assertEqual(artifact_probe.probe_bytes(b"UDTRFIRM", size), {
                    "format": "sony_fdat_header_signature_candidate",
                    "status": "container_not_validated",
                })

    def test_full_signature_in_short_object_is_malformed(self):
        for size in (8, 9, 511):
            with self.subTest(size=size):
                self.assertEqual(artifact_probe.probe_bytes(b"UDTRFIRM", size), {
                    "format": "sony_fdat_header_signature_candidate",
                    "status": "malformed_header",
                })

    def test_partial_and_nonmatching_signatures_are_opaque(self):
        for prefix in (b"", b"U", b"UDTRFIR", b"udtrfirm", b"xUDTRFIRM", b"UDTRFIRX"):
            with self.subTest(prefix=prefix):
                self.assertEqual(artifact_probe.probe_bytes(prefix, 512), {
                    "format": "unknown", "status": "unsupported_opaque",
                })


class FDATStreamTests(unittest.TestCase):
    def test_opt_in_identifies_fdat_not_other_chunk_or_package_prefix(self):
        data = frame((b"INFO", b"UDTRFIRM" + b"other-chunk-secret" * 100),
                     (b"FDAT", b"opaque-fdat-secret" * 32),
                     (b"TAIL", b"UDTRFIRM" + bytes(512)))
        result = identify(data, probe_fdat=True)
        self.assertEqual(result["fdat_probe"]["candidate"], {
            "format": "unknown", "status": "unsupported_opaque",
        })
        self.assertEqual(result["fdat_probe"]["prefix_bytes_observed"], 576)
        self.assertEqual(result["sha256"], hashlib.sha256(data).hexdigest())

    def test_prefix_capture_at_4096_boundary(self):
        for size in (4095, 4096, 4097, 10000):
            payload = b"UDTRFIRM" + bytes((index % 251 for index in range(size - 8)))
            data = frame((b"INFO", b"must-not-be-captured"), (b"FDAT", payload))
            with self.subTest(size=size), mock.patch.object(
                    ufu_inventory, "probe_bytes", wraps=artifact_probe.probe_bytes) as classifier:
                result = identify(data, probe_fdat=True)
                classifier.assert_called_once_with(payload[:4096], size)
                self.assertEqual(result["fdat_probe"]["prefix_limit"], 4096)
                self.assertEqual(result["fdat_probe"]["prefix_bytes_observed"], min(size, 4096))
                self.assertFalse(result["fdat_probe"]["raw_prefix_output"])

    def test_small_fdat_passes_its_actual_size_to_signature_classifier(self):
        for size, expected in ((8, "malformed_header"), (511, "malformed_header"),
                               (512, "container_not_validated")):
            with self.subTest(size=size):
                result = identify(frame((b"FDAT", b"UDTRFIRM" + bytes(size - 8))),
                                  probe_fdat=True)
                self.assertEqual(result["fdat_probe"]["candidate"]["status"], expected)
                self.assertEqual(result["fdat_probe"]["status"], "signature_only")

    def test_other_known_signature_is_a_candidate_not_sony_identity(self):
        result = identify(frame((b"FDAT", b"PK\x03\x04" + bytes(40))), probe_fdat=True)
        self.assertEqual(result["fdat_probe"]["candidate"], {
            "format": "zip_signature_candidate", "status": "container_not_validated",
        })
        self.assertEqual(result["compatibility"], "UNVERIFIED")
        self.assertFalse(result["identity_inferred"])
        self.assertFalse(result["container_validated"])
        self.assertFalse(result["extraction_performed"])
        self.assertFalse(result["decompression_performed"])
        self.assertFalse(result["decryption_performed"])
        self.assertFalse(result["execution_performed"])
        self.assertFalse(result["camera_access_performed"])

    def test_default_retains_directory_behavior_without_invoking_classifier(self):
        data = frame((b"FDAT", b"UDTRFIRM" + bytes(512)))
        with mock.patch.object(ufu_inventory, "probe_bytes") as classifier:
            implicit = identify(data)
            explicit = identify(data, probe_fdat=False)
        classifier.assert_not_called()
        self.assertEqual(implicit, explicit)
        self.assertNotIn("fdat_probe", implicit)
        self.assertEqual(implicit["fdat_status"], "single_bounded_span")

    def test_absent_empty_and_similarly_named_chunks_do_not_call_classifier(self):
        cases = [(frame(), "absent"), (frame((b"INFO", b"UDTRFIRM")), "absent"),
                 (frame((b"fdat", b"UDTRFIRM")), "absent"),
                 (frame((b"FDAT", b"")), "empty")]
        for data, status in cases:
            with self.subTest(status=status, size=len(data)), mock.patch.object(
                    ufu_inventory, "probe_bytes") as classifier:
                result = identify(data, probe_fdat=True)
                classifier.assert_not_called()
                self.assertEqual(result["fdat_status"], status)
                self.assertEqual(result["fdat_probe"]["status"], status)
                self.assertEqual(result["fdat_probe"]["prefix_bytes_observed"], 0)
                self.assertIsNone(result["fdat_probe"]["candidate"])

    def test_duplicate_fdat_refused_only_for_opt_in(self):
        for first, second in ((b"", b""), (b"", b"UDTRFIRM"),
                              (b"one", b"two"), (b"UDTRFIRM", b"")):
            data = frame((b"FDAT", first), (b"INFO", b"gap"), (b"FDAT", second))
            with self.subTest(lengths=(len(first), len(second))):
                self.assertEqual(identify(data)["fdat_status"], "ambiguous_multiple")
                with mock.patch.object(ufu_inventory, "probe_bytes") as classifier:
                    with self.assertRaisesRegex(ufu_inventory.UFUError, "unambiguous single span"):
                        identify(data, probe_fdat=True)
                    classifier.assert_not_called()

    def test_probe_policy_requires_actual_bool_before_reading(self):
        data = frame((b"FDAT", b"x"))
        for flag in (None, 0, 1, 0.0, "true", [], object()):
            stream = SequentialStream(data)
            with self.subTest(flag=flag), self.assertRaisesRegex(
                    ufu_inventory.UFUError, "probe policy"):
                ufu_inventory.index_stream(stream, len(data), hashlib.sha256(data).hexdigest(),
                                           probe_fdat=flag)
            self.assertEqual(stream.requests, [])

    def test_hash_failure_never_calls_classifier(self):
        data = frame((b"FDAT", b"UDTRFIRM" + bytes(512)))
        with mock.patch.object(ufu_inventory, "probe_bytes") as classifier:
            with self.assertRaisesRegex(ufu_inventory.UFUError, "SHA-256 mismatch"):
                ufu_inventory.index_stream(io.BytesIO(data), len(data), "0" * 64,
                                           probe_fdat=True)
            classifier.assert_not_called()

    def test_later_framing_failure_never_calls_classifier_or_returns_prefix(self):
        data = frame((b"FDAT", b"UDTRFIRM" + bytes(512))) + b"short"
        with mock.patch.object(ufu_inventory, "probe_bytes") as classifier:
            with self.assertRaises(ufu_inventory.UFUError):
                identify(data, probe_fdat=True)
            classifier.assert_not_called()

    def test_classification_waits_for_whole_file_eof_in_one_bounded_pass(self):
        payload = b"UDTRFIRM" + b"private-synthetic-prefix" * 100000
        data = frame((b"INFO", b"before"), (b"FDAT", payload), (b"TAIL", b"after"))
        stream = SequentialStream(data)

        def classify(prefix, size):
            self.assertEqual(stream.tell(), len(data))
            self.assertEqual(stream.requests[-1], (len(data), 1, 0))
            self.assertEqual(prefix, payload[:4096])
            self.assertEqual(size, len(payload))
            return artifact_probe.probe_bytes(prefix, size)

        with mock.patch.object(ufu_inventory, "probe_bytes", side_effect=classify) as classifier:
            result = ufu_inventory.index_stream(stream, len(data), hashlib.sha256(data).hexdigest(),
                                                probe_fdat=True)
            classifier.assert_called_once()
        self.assertEqual(sum(count for _, _, count in stream.requests), len(data))
        self.assertEqual(result["sha256"], hashlib.sha256(data).hexdigest())
        self.assertLessEqual(max(size for _, size, _ in stream.requests), 1024 * 1024)
        encoded = json.dumps(result)
        self.assertNotIn("private-synthetic-prefix", encoded)
        self.assertNotIn(payload[:32].hex(), encoded)
        self.assertLess(len(encoded), 3000)

    def test_short_reads_accumulate_the_exact_fdat_prefix(self):
        payload = b"UDTRFIRM" + b"short-read-secret" * 300
        data = frame((b"INFO", b"skip-me"), (b"FDAT", payload), (b"TAIL", b"tail"))
        stream = SequentialStream(data, short_reads=True)
        with mock.patch.object(ufu_inventory, "probe_bytes", wraps=artifact_probe.probe_bytes) as classifier:
            result = ufu_inventory.index_stream(stream, len(data), hashlib.sha256(data).hexdigest(),
                                                probe_fdat=True)
            classifier.assert_called_once_with(payload[:4096], len(payload))
        self.assertEqual(result, identify(data, probe_fdat=True))
        self.assertEqual(sum(count for _, _, count in stream.requests), len(data))


class FDATFileAndCLITests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.path = self.root / "private-serial-fdat-synthetic.dat"
        self.payload = b"UDTRFIRM" + b"never-publish-this-prefix" * 300
        self.data = frame((b"INFO", b"other-private-data"), (b"FDAT", self.payload))
        self.path.write_bytes(self.data)
        self.digest = hashlib.sha256(self.data).hexdigest()

    def call_cli(self, *flags, digest=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = ufu_inventory.main([
                "--input", str(self.path), "--expect-sha256", digest or self.digest,
                "--expect-bytes", str(len(self.data)), *flags,
            ])
        return result, stdout.getvalue(), stderr.getvalue()

    def test_inspect_file_forwards_opt_in_and_preserves_original(self):
        before = self.path.stat()
        result = ufu_inventory.inspect_file(self.path, self.digest, len(self.data), probe_fdat=True)
        self.assertEqual(result, identify(self.data, probe_fdat=True))
        after = self.path.stat()
        self.assertEqual((before.st_size, before.st_mtime_ns), (after.st_size, after.st_mtime_ns))
        self.assertEqual(self.path.read_bytes(), self.data)
        self.assertEqual(list(self.root.iterdir()), [self.path])

    def test_cli_default_and_opt_in_are_private_metadata_only(self):
        for flags in ((), ("--probe-fdat",)):
            with self.subTest(flags=flags):
                code, output, errors = self.call_cli(*flags)
                self.assertEqual(code, 0)
                self.assertEqual(errors, "")
                report = json.loads(output)
                self.assertEqual(report, identify(self.data, probe_fdat=bool(flags)))
                self.assertEqual("fdat_probe" in report, bool(flags))
                for private in (str(self.root), self.path.name, "never-publish-this-prefix",
                                self.payload[:32].hex(), "other-private-data"):
                    self.assertNotIn(private, output)
        self.assertEqual(list(self.root.iterdir()), [self.path])

    def test_cli_hash_refusal_emits_no_partial_json_or_prefix(self):
        with mock.patch.object(ufu_inventory, "probe_bytes") as classifier:
            code, output, errors = self.call_cli("--probe-fdat", digest="0" * 64)
            classifier.assert_not_called()
        self.assertEqual(code, 2)
        self.assertEqual(output, "")
        self.assertIn("SHA-256 mismatch", errors)
        self.assertNotIn(str(self.root), errors)
        self.assertNotIn(self.path.name, errors)
        self.assertNotIn("never-publish-this-prefix", errors)

    def test_cli_duplicate_refusal_is_private_and_default_stays_explicit(self):
        self.data = frame((b"FDAT", self.payload), (b"FDAT", b"second-secret"))
        self.path.write_bytes(self.data)
        self.digest = hashlib.sha256(self.data).hexdigest()
        code, output, errors = self.call_cli("--probe-fdat")
        self.assertEqual(code, 2)
        self.assertEqual(output, "")
        self.assertIn("unambiguous single span", errors)
        self.assertNotIn(self.path.name, errors)
        self.assertNotIn("second-secret", errors)
        code, output, errors = self.call_cli()
        self.assertEqual(code, 0)
        self.assertEqual(errors, "")
        self.assertEqual(json.loads(output)["fdat_status"], "ambiguous_multiple")
        self.assertNotIn("fdat_probe", json.loads(output))


if __name__ == "__main__":
    unittest.main()
