"""Synthetic framing tests; no firmware, upstream modules or network inputs."""
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from tools import ufu_inventory


# Hand-written byte oracle: three chunks at offsets 8, 19 and 32. The hash
# was calculated independently of the parser and is fixed with this fixture.
FIXTURE = (
    b"\x89UFU\r\n\x1a\n"
    b"\x00\x00\x00\x03INFOabc"
    b"\x00\x00\x00\x05FDAT12345"
    b"\x00\x00\x00\x00END!"
)
FIXTURE_SHA256 = "7d725f141a471c95d1f3f96849f86b1cb91bd1dfb830ee1839f70417881a74ae"


def framed(*chunks):
    """Build test data using struct, separately from the reader's integer logic."""
    return b"\x89UFU\r\n\x1a\n" + b"".join(
        struct.pack(">I4s", len(payload), tag) + payload for tag, payload in chunks
    )


def inspect_bytes(data, **kwargs):
    return ufu_inventory.index_stream(
        io.BytesIO(data), len(data), hashlib.sha256(data).hexdigest(), **kwargs
    )


class RecordingStream(io.BytesIO):
    def __init__(self, data, *, short_reads=False):
        super().__init__(data)
        self.requests = []
        self.short_reads = short_reads

    def read(self, size=-1):
        if not 0 < size <= 1024 * 1024:
            raise AssertionError("reader requested an unbounded/oversized read")
        self.requests.append(size)
        return super().read(min(size, 3) if self.short_reads else size)


class UFUStreamTests(unittest.TestCase):
    def test_independent_fixture_offsets_sizes_big_endian_and_hash(self):
        result = ufu_inventory.index_stream(io.BytesIO(FIXTURE), 40, FIXTURE_SHA256)
        self.assertEqual(result["bytes"], 40)
        self.assertEqual(result["sha256"], FIXTURE_SHA256)
        self.assertEqual(result["chunk_count"], 3)
        self.assertEqual(result["address_type"], "package_file_offset")
        self.assertEqual(result["chunks"], [
            {"index": 0, "type_hex": "494e464f", "type_ascii": "INFO",
             "header_file_offset": 8, "payload_file_offset": 16,
             "payload_bytes": 3, "end_file_offset_exclusive": 19},
            {"index": 1, "type_hex": "46444154", "type_ascii": "FDAT",
             "header_file_offset": 19, "payload_file_offset": 27,
             "payload_bytes": 5, "end_file_offset_exclusive": 32},
            {"index": 2, "type_hex": "454e4421", "type_ascii": "END!",
             "header_file_offset": 32, "payload_file_offset": 40,
             "payload_bytes": 0, "end_file_offset_exclusive": 40},
        ])
        self.assertEqual(result["fdat_status"], "single_bounded_span")

    def test_framing_never_promotes_container_or_target_validation(self):
        result = inspect_bytes(FIXTURE)
        self.assertEqual(result["format"], "sony_ufu_framing_candidate")
        self.assertEqual(result["status"], "framing_spans_entire_file")
        self.assertEqual(result["compatibility"], "UNVERIFIED")
        for field in ("container_validated", "checksums_verified", "signature_verified",
                      "chunk_semantics_verified", "identity_inferred", "extraction_performed",
                      "decompression_performed", "decryption_performed", "execution_performed",
                      "camera_access_performed"):
            with self.subTest(field=field):
                self.assertIs(result[field], False)

    def test_binary_chunk_tags_are_hex_without_decoding_or_semantic_guess(self):
        result = inspect_bytes(framed((b"\x00\xff\x7f\x01", b"synthetic-data")))
        self.assertEqual(result["chunks"][0]["type_hex"], "00ff7f01")
        self.assertIsNone(result["chunks"][0]["type_ascii"])
        self.assertEqual(result["fdat_status"], "absent")

    def test_absent_empty_and_duplicate_fdat_remain_explicit(self):
        cases = [
            (framed(), "absent"),
            (framed((b"INFO", b"abc")), "absent"),
            (framed((b"FDAT", b"")), "empty"),
            (framed((b"FDAT", b"one"), (b"FDAT", b"two")), "ambiguous_multiple"),
            (framed((b"FDAT", b""), (b"FDAT", b"")), "ambiguous_multiple"),
        ]
        for data, expected in cases:
            with self.subTest(status=expected, bytes=len(data)):
                result = inspect_bytes(data)
                self.assertEqual(result["fdat_status"], expected)
                self.assertFalse(result["container_validated"])

    def test_zero_length_chunks_progress_and_exact_count_limit(self):
        data = framed((b"ZERO", b""), (b"FDAT", b""))
        result = inspect_bytes(data, max_chunks=2)
        self.assertEqual(result["chunk_count"], 2)
        self.assertEqual([chunk["header_file_offset"] for chunk in result["chunks"]], [8, 16])
        self.assertEqual(result["chunks"][-1]["end_file_offset_exclusive"], 24)
        with self.assertRaisesRegex(ufu_inventory.UFUError, "chunk-count"):
            inspect_bytes(data, max_chunks=1)

    def test_default_chunk_cap_stops_zero_size_chunk_flood(self):
        data = framed(*[(b"ZERO", b"")] * 4097)
        with self.assertRaisesRegex(ufu_inventory.UFUError, "chunk-count"):
            inspect_bytes(data)

    def test_invalid_size_and_count_policy_types_refused(self):
        for size in (True, 40.0, -1, 0, 7, 2 * 1024**3 + 1):
            with self.subTest(size=size), self.assertRaises(ufu_inventory.UFUError):
                ufu_inventory.index_stream(io.BytesIO(FIXTURE), size, FIXTURE_SHA256)
        for count in (True, 2.0, 0, -1, 4097):
            with self.subTest(count=count), self.assertRaises(ufu_inventory.UFUError):
                inspect_bytes(FIXTURE, max_chunks=count)

    def test_exact_lowercase_hash_required_and_wrong_digest_refused(self):
        for digest in (None, b"0" * 64, "0" * 63, "g" * 64,
                       FIXTURE_SHA256.upper(), FIXTURE_SHA256 + "\n", "0" * 64):
            with self.subTest(digest=digest), self.assertRaises(ufu_inventory.UFUError):
                ufu_inventory.index_stream(io.BytesIO(FIXTURE), 40, digest)

    def test_unsupported_magic_refused(self):
        with self.assertRaisesRegex(ufu_inventory.UFUError, "identifier"):
            inspect_bytes(b"unsupported" + FIXTURE[8:])

    def test_every_short_trailing_field_refused(self):
        for count in range(1, 8):
            with self.subTest(count=count), self.assertRaisesRegex(
                    ufu_inventory.UFUError, "trailing bytes|truncated chunk header"):
                inspect_bytes(FIXTURE + b"\x00" * count)

    def test_stream_truncation_in_magic_or_header_refused(self):
        for stream, declared_size in ((FIXTURE[:4], 8), (FIXTURE[:12], 40)):
            with self.subTest(size=len(stream)), self.assertRaisesRegex(
                    ufu_inventory.UFUError, "truncated framing"):
                ufu_inventory.index_stream(io.BytesIO(stream), declared_size, FIXTURE_SHA256)

    def test_declared_payload_overflow_refused_before_payload_read(self):
        data = b"\x89UFU\r\n\x1a\n\xff\xff\xff\xffFDAT"
        stream = RecordingStream(data)
        with self.assertRaisesRegex(ufu_inventory.UFUError, "beyond the file"):
            ufu_inventory.index_stream(stream, 16, hashlib.sha256(data).hexdigest())
        self.assertEqual(stream.requests, [8, 8])

    def test_payload_truncation_against_declared_stream_size_refused(self):
        data = framed((b"FDAT", b"four"))
        with self.assertRaisesRegex(ufu_inventory.UFUError, "truncated chunk payload"):
            ufu_inventory.index_stream(io.BytesIO(data[:-1]), len(data),
                                       hashlib.sha256(data).hexdigest())

    def test_bytes_beyond_expected_file_size_refused(self):
        with self.assertRaisesRegex(ufu_inventory.UFUError, "exceeds the declared"):
            ufu_inventory.index_stream(io.BytesIO(FIXTURE + b"extra"), 40, FIXTURE_SHA256)

    def test_large_payload_consumed_in_bounded_reads_not_retained(self):
        payload = b"synthetic-private-payload-" * 100000
        data = framed((b"FDAT", payload))
        stream = RecordingStream(data)
        result = ufu_inventory.index_stream(stream, len(data), hashlib.sha256(data).hexdigest())
        self.assertEqual(result["chunks"][0]["payload_bytes"], len(payload))
        self.assertGreater(len(stream.requests), 5)
        self.assertLessEqual(max(stream.requests), 1024 * 1024)
        encoded = json.dumps(result)
        self.assertNotIn("synthetic-private-payload", encoded)
        self.assertLess(len(encoded), 2000)

    def test_ordinary_short_reads_are_accumulated(self):
        stream = RecordingStream(FIXTURE, short_reads=True)
        result = ufu_inventory.index_stream(stream, 40, FIXTURE_SHA256)
        self.assertEqual(result, inspect_bytes(FIXTURE))


class UFUFileTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.path = self.root / "private-serial-synthetic.dat"
        self.path.write_bytes(FIXTURE)

    def test_regular_file_matches_stream_oracle_without_modification(self):
        before = self.path.stat()
        result = ufu_inventory.inspect_file(self.path, FIXTURE_SHA256, 40)
        after = self.path.stat()
        self.assertEqual(result, inspect_bytes(FIXTURE))
        self.assertEqual(self.path.read_bytes(), FIXTURE)
        self.assertEqual((before.st_size, before.st_mtime_ns),
                         (after.st_size, after.st_mtime_ns))
        self.assertEqual(list(self.root.iterdir()), [self.path])

    def test_wrong_expected_file_size_and_hash_refused(self):
        for size in (39, 41, True, 40.0):
            with self.subTest(size=size), self.assertRaises(ufu_inventory.UFUError):
                ufu_inventory.inspect_file(self.path, FIXTURE_SHA256, size)
        with self.assertRaisesRegex(ufu_inventory.UFUError, "SHA-256 mismatch"):
            ufu_inventory.inspect_file(self.path, "0" * 64, 40)

    def test_missing_files_and_directories_refused(self):
        for path in (self.root, self.root / "missing-private-serial.dat"):
            with self.subTest(path=path.name), self.assertRaises(ufu_inventory.UFUError):
                ufu_inventory.inspect_file(path, FIXTURE_SHA256, 40)

    def test_symlink_refused_when_host_allows_creation(self):
        link = self.root / "synthetic-link.dat"
        try:
            link.symlink_to(self.path)
        except (OSError, NotImplementedError) as exc:
            self.skipTest("host cannot create a real symlink: " + type(exc).__name__)
        with self.assertRaisesRegex(ufu_inventory.UFUError, "ordinary regular file"):
            ufu_inventory.inspect_file(link, FIXTURE_SHA256, 40)

    def test_observable_descriptor_metadata_change_rejects_result(self):
        original = self.path.stat()
        changed = SimpleNamespace(
            st_dev=original.st_dev, st_ino=original.st_ino, st_mode=original.st_mode,
            st_size=original.st_size, st_mtime_ns=original.st_mtime_ns,
            st_ctime_ns=original.st_ctime_ns + 1,
        )
        with mock.patch.object(ufu_inventory.os, "fstat", side_effect=[original, changed]):
            with self.assertRaisesRegex(ufu_inventory.UFUError, "changed during reading"):
                ufu_inventory.inspect_file(self.path, FIXTURE_SHA256, 40)

    def test_observable_named_file_replacement_rejects_result(self):
        original = self.path.lstat()
        changed = SimpleNamespace(
            st_dev=original.st_dev, st_ino=original.st_ino + 1, st_mode=original.st_mode,
            st_size=original.st_size, st_mtime_ns=original.st_mtime_ns,
            st_ctime_ns=original.st_ctime_ns,
        )
        with mock.patch.object(Path, "lstat", side_effect=[original, changed]):
            with self.assertRaisesRegex(ufu_inventory.UFUError, "changed during reading"):
                ufu_inventory.inspect_file(self.path, FIXTURE_SHA256, 40)

    def test_parser_refusal_closes_owned_descriptor(self):
        descriptors = []
        real_open = os.open

        def record_open(*args, **kwargs):
            descriptor = real_open(*args, **kwargs)
            descriptors.append(descriptor)
            return descriptor

        with mock.patch.object(ufu_inventory.os, "open", side_effect=record_open):
            with self.assertRaises(ufu_inventory.UFUError):
                ufu_inventory.inspect_file(self.path, "0" * 64, 40)
        self.assertEqual(len(descriptors), 1)
        with self.assertRaises(OSError):
            os.fstat(descriptors[0])

    def run_cli(self, path, digest=FIXTURE_SHA256, size=40):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = ufu_inventory.main(["--input", str(path), "--expect-sha256", digest,
                                       "--expect-bytes", str(size)])
        return code, output.getvalue(), errors.getvalue()

    def test_cli_success_reports_metadata_without_private_path_or_payload(self):
        code, output, errors = self.run_cli(self.path)
        self.assertEqual(code, 0)
        self.assertEqual(errors, "")
        self.assertEqual(json.loads(output), inspect_bytes(FIXTURE))
        self.assertNotIn(str(self.root), output)
        self.assertNotIn(self.path.name, output)
        self.assertNotIn("12345", output)
        self.assertEqual(list(self.root.iterdir()), [self.path])

    def test_cli_refusals_emit_no_partial_json_or_private_names(self):
        cases = [(self.path, "0" * 64, 40), (self.path, FIXTURE_SHA256, 41),
                 (self.root, FIXTURE_SHA256, 40),
                 (self.root / "missing-secret-serial.dat", FIXTURE_SHA256, 40)]
        malformed = self.root / "malformed-private-serial.dat"
        malformed.write_bytes(FIXTURE + b"\x00")
        cases.append((malformed, hashlib.sha256(malformed.read_bytes()).hexdigest(), 41))
        for path, digest, size in cases:
            with self.subTest(case=path.name, size=size):
                code, output, errors = self.run_cli(path, digest, size)
                self.assertEqual(code, 2)
                self.assertEqual(output, "")
                self.assertIn("UFU inventory refused:", errors)
                self.assertNotIn(str(self.root), errors)
                self.assertNotIn(path.name, errors)
                self.assertNotIn("Traceback", errors)


if __name__ == "__main__":
    unittest.main()
