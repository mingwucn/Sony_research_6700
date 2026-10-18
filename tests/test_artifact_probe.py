import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
import struct
import tempfile
import unittest

from tools.artifact_probe import build_report, main, probe_bytes


class ProbeTests(unittest.TestCase):
    def test_opaque_is_not_labelled_encrypted_or_compatible(self):
        result = probe_bytes(b"synthetic opaque bytes", 22)
        self.assertEqual(result["format"], "unknown")
        self.assertEqual(result["status"], "unsupported_opaque")

    def elf(self, bits=64, endian="little"):
        data = bytearray(64 if bits == 64 else 52)
        data[:7] = b"\x7fELF" + bytes([2 if bits == 64 else 1, 1 if endian == "little" else 2, 1])
        data[16:18] = (2).to_bytes(2, endian)
        data[18:20] = (183 if bits == 64 else 40).to_bytes(2, endian)
        data[20:24] = (1).to_bytes(4, endian)
        position = 52 if bits == 64 else 40
        data[position:position + 2] = len(data).to_bytes(2, endian)
        return bytes(data)

    def test_elf_both_classes_and_endians(self):
        for bits in (32, 64):
            for endian in ("little", "big"):
                result = probe_bytes(self.elf(bits, endian), 1000)
                self.assertEqual(result["format"], "elf_header_candidate")
                self.assertEqual(result["class_bits"], bits)
                self.assertEqual(result["byte_order"], endian)
                self.assertFalse(result["abi_verified"])

    def test_bad_elf_header_refused_as_candidate(self):
        valid = self.elf()
        for data in (valid[:10], valid[:30], valid[:4] + b"\x03" + valid[5:],
                     valid[:6] + b"\x00" + valid[7:], valid[:52] + b"\x00\x00" + valid[54:]):
            self.assertEqual(probe_bytes(data, len(data))["status"], "malformed_header")

    def test_pe_bounded_offsets(self):
        data = bytearray(100)
        data[:2] = b"MZ"
        struct.pack_into("<I", data, 60, 64)
        data[64:68] = b"PE\x00\x00"
        struct.pack_into("<H", data, 68, 0x8664)
        self.assertEqual(probe_bytes(bytes(data), 100)["format"], "pe_header_candidate")
        struct.pack_into("<I", data, 60, 0xffffffff)
        self.assertEqual(probe_bytes(bytes(data), 100)["status"], "malformed_header")
        struct.pack_into("<I", data, 60, 5000)
        self.assertEqual(probe_bytes(bytes(data), 10000)["status"], "header_outside_probe")

    def test_signatures_are_not_container_validation(self):
        for data, expected in ((b"PK\x03\x04" + bytes(40), "zip_signature_candidate"),
                               (b"\x1f\x8b\x08" + bytes(20), "gzip_signature_candidate"),
                               (b"\x89UFU\r\n\x1a\n" + bytes(20), "sony_ufu_signature_candidate")):
            result = probe_bytes(data, len(data))
            self.assertEqual(result["format"], expected)
            self.assertEqual(result["status"], "container_not_validated")

    def test_inconsistent_probe_lengths_refused(self):
        for prefix, size in ((b"abc", 2), (b"", 0), (bytes(4097), 5000), (b"x", True)):
            with self.assertRaises(ValueError):
                probe_bytes(prefix, size)

    def test_file_report_and_cli_privacy(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "private-serial.exe"
            path.write_bytes(b"arbitrary synthetic file")
            report = build_report([("sample", path)], "synthetic")
            self.assertEqual(report, build_report([("sample", path)], "synthetic"))
            encoded = json.dumps(report)
            self.assertNotIn(directory, encoded)
            self.assertNotIn(path.name, encoded)
            self.assertFalse(report["extraction_performed"])
            self.assertFalse(report["camera_access_performed"])
            self.assertEqual(report["compatibility"], "UNVERIFIED")
            output, errors = io.StringIO(), io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                code = main(["--kind", "synthetic", "--artifact", "sample=" + str(path)])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue()), report)
            output, errors = io.StringIO(), io.StringIO()
            with redirect_stdout(output), redirect_stderr(errors):
                code = main(["--artifact", "sample=" + str(path), "--artifact", "missing=" + str(path / "secret")])
            self.assertEqual(code, 2)
            self.assertEqual(output.getvalue(), "")
            self.assertNotIn(directory, errors.getvalue())

    def test_duplicate_and_bad_labels_refused(self):
        with self.assertRaises(ValueError):
            build_report([])
        with self.assertRaises(ValueError):
            build_report([("../../secret", Path("unused"))])
        with self.assertRaises(ValueError):
            build_report([("same", Path("unused")), ("same", Path("unused"))])


if __name__ == "__main__":
    unittest.main()
