"""Independent, synthetic decoded-FDAT header and extent-policy tests.

Literal offsets below are the test oracle, not imported parser constants. The
CRC oracle uses the bitwise IEEE algorithm rather than the parser's zlib call.
No firmware bytes, upstream modules, files, crypto or devices are used.
"""
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import struct
import unittest

from tools import fdat_header

_DEFAULT_HEADER = object()


def oracle_crc32(data):
    crc = 0xffffffff
    for value in data:
        crc ^= value
        for _ in range(8):
            crc = (crc >> 1) ^ (0xedb88320 if crc & 1 else 0)
    return crc ^ 0xffffffff


def seal(header):
    result = bytearray(header)
    struct.pack_into("<I", result, 8, oracle_crc32(result[12:512]))
    return bytes(result)


def put_u32(header, offset, value):
    struct.pack_into("<I", header, offset, value)


def put_slot(header, index, mode, offset, size):
    base = 64 + index * 16
    header[base:base + 16] = bytes(16)
    header[base] = mode
    put_u32(header, base + 4, offset)
    put_u32(header, base + 8, size)


def fixture():
    header = bytearray(512)
    header[0:8] = b"UDTRFIRM"
    header[12:16] = b"0100"
    header[16] = ord("U")
    header[20] = ord("N")
    header[32:34] = bytes((7, 3))
    for offset, value in ((36, 0x01020304), (40, 0x11223344),
                          (48, 576), (52, 96), (56, 2)):
        put_u32(header, offset, value)
    put_slot(header, 0, ord("U"), 512, 64)
    # The zero-size P sentinel intentionally shares the U start offset.
    put_slot(header, 1, ord("P"), 512, 0)
    return seal(header)


class FDATHeaderTests(unittest.TestCase):
    def validate(self, header=_DEFAULT_HEADER, size=672):
        return fdat_header.validate_header(
            fixture() if header is _DEFAULT_HEADER else header, size)

    def assert_rejected(self, header, size=672, message=None):
        with self.assertRaises(fdat_header.FDATError) as raised:
            self.validate(header, size)
        if message is not None:
            self.assertIn(message, str(raised.exception))

    def test_independent_crc_oracle_and_fixed_fixture_checksum(self):
        self.assertEqual(oracle_crc32(b"123456789"), 0xcbf43926)
        header = fixture()
        self.assertEqual(len(header), 512)
        self.assertEqual(header[8:12], b"\x41\xd5\xbe\x07")
        self.assertEqual(oracle_crc32(header[12:512]), 0x07bed541)
        self.assertTrue(self.validate(header)["header_crc32_verified"])

    def test_literal_offsets_little_endian_values_and_extent_results(self):
        result = self.validate()
        self.assertEqual(result["model_field_code"], 0x01020304)
        self.assertEqual(result["region_field_code"], 0x11223344)
        self.assertEqual(result["version_minor_code"], 7)
        self.assertEqual(result["version_major_code"], 3)
        self.assertEqual(result["mode"], "U")
        self.assertEqual(result["luw_flag"], "N")
        self.assertEqual(result["firmware"], {
            "offset": 576, "bytes": 96, "end_offset_exclusive": 672})
        self.assertEqual(result["filesystem_slots"], [
            {"slot_index": 0, "mode": "U", "offset": 512,
             "bytes": 64, "end_offset_exclusive": 576},
            {"slot_index": 1, "mode": "P", "offset": 512,
             "bytes": 0, "end_offset_exclusive": 512},
        ])
        self.assertEqual(result["nonempty_spans"], [
            {"kind": "firmware", "offset": 576, "bytes": 96,
             "end_offset_exclusive": 672},
            {"kind": "filesystem", "slot_index": 0, "mode": "U",
             "offset": 512, "bytes": 64, "end_offset_exclusive": 576},
        ])

    def test_header_length_and_exact_bytes_type_are_enforced(self):
        class BytesSubclass(bytes):
            pass

        for header in (b"", bytes(7), bytes(8), fixture()[:511],
                       fixture() + b"x", bytearray(fixture()),
                       memoryview(fixture()), BytesSubclass(fixture()),
                       None, "synthetic", [0] * 512):
            with self.subTest(type=type(header).__name__,
                              length=len(header) if hasattr(header, "__len__") else None):
                self.assert_rejected(header)

    def test_caller_size_is_strict_integer_and_bounded_without_allocation(self):
        class IntSubclass(int):
            pass

        for size in (None, False, True, 672.0, "672", IntSubclass(672),
                     -1, 0, 511, 2 ** 31 + 1, 2 ** 64):
            with self.subTest(size=size):
                self.assert_rejected(fixture(), size)
        result = self.validate(size=2 ** 31)
        self.assertEqual(result["decoded_bytes"], 2 ** 31)
        self.assertTrue(result["decoded_bytes_is_caller_supplied"])

    def test_minimum_decoded_size_still_requires_positive_user_extent(self):
        header = bytearray(fixture())
        put_u32(header, 48, 0)
        put_u32(header, 52, 0)
        put_slot(header, 0, ord("U"), 512, 1)
        self.assert_rejected(seal(header), 512, "bounds")
        self.assertEqual(self.validate(seal(header), 513)["decoded_bytes"], 513)

    def test_identifiers_and_mode_flags_are_checked_with_valid_crc(self):
        for offset, value in ((0, b"XDTRFIRM"), (0, b"udtrfirm"),
                              (12, b"0200"), (12, b"0001"),
                              (16, b"P"), (16, b"\x00"),
                              (20, b"Y"), (20, b"\x00")):
            header = bytearray(fixture())
            header[offset:offset + len(value)] = value
            with self.subTest(offset=offset, value=value):
                self.assert_rejected(seal(header))

    def test_stored_checksum_endianness_and_coverage_are_not_interchangeable(self):
        for checksum in (struct.pack(">I", 0x07bed541),
                         struct.pack("<I", oracle_crc32(fixture()[12:508])),
                         struct.pack("<I", oracle_crc32(fixture())),
                         bytes(4)):
            header = bytearray(fixture())
            header[8:12] = checksum
            with self.subTest(checksum=checksum.hex()):
                self.assert_rejected(bytes(header), message="CRC32")

    def test_crc_covers_ordinary_header_and_slot_padding(self):
        for offset in (17, 31, 34, 37, 40, 44, 60, 65, 79):
            header = bytearray(fixture())
            header[offset] ^= 1
            with self.subTest(offset=offset):
                self.assert_rejected(bytes(header), message="CRC32")
                self.assertTrue(self.validate(seal(header))["header_crc32_verified"])

    def test_declared_count_is_bounded_but_not_equated_to_observed_slots(self):
        for count in (0, 1, 2, 27, 28):
            header = bytearray(fixture())
            put_u32(header, 56, count)
            with self.subTest(count=count):
                result = self.validate(seal(header))
                self.assertEqual(result["declared_filesystem_count"], count)
                self.assertEqual(result["observed_slot_count"], 2)
                self.assertIs(result["count_semantics_verified"], False)
        for count in (29, 0xffffffff):
            header = bytearray(fixture())
            put_u32(header, 56, count)
            with self.subTest(count=count):
                self.assert_rejected(seal(header), message="count")

    def test_last_slot_is_inspected_even_with_zero_declared_count(self):
        header = bytearray(fixture())
        header[496:512] = header[64:80]
        header[64:80] = bytes(16)
        put_u32(header, 56, 0)
        result = self.validate(seal(header))
        self.assertEqual([slot["slot_index"] for slot in result["filesystem_slots"]],
                         [1, 27])
        self.assertEqual(result["observed_slot_count"], 2)

    def test_late_duplicate_user_slot_is_rejected(self):
        header = bytearray(fixture())
        put_slot(header, 27, ord("U"), 672, 1)
        put_u32(header, 56, 1)
        self.assert_rejected(seal(header), 673, "one nonempty")

    def test_late_slot_bounds_are_not_hidden_by_declared_count(self):
        header = bytearray(fixture())
        put_slot(header, 27, ord("P"), 672, 1)
        put_u32(header, 56, 1)
        self.assert_rejected(seal(header), message="bounds")

    def test_one_positive_user_slot_is_a_host_subset_requirement(self):
        for mode, offset, size in ((0, 0, 0), (ord("P"), 512, 64),
                                   (ord("U"), 0, 0), (ord("U"), 512, 0)):
            header = bytearray(fixture())
            put_slot(header, 0, mode, offset, size)
            with self.subTest(mode=mode, offset=offset, size=size):
                self.assert_rejected(seal(header), message="one nonempty")

    def test_unknown_or_zero_mode_nonzero_records_are_unsupported(self):
        for mode, offset, size in ((ord("X"), 0, 0), (255, 512, 0),
                                   (0, 512, 0), (0, 0, 1)):
            header = bytearray(fixture())
            put_slot(header, 13, mode, offset, size)
            with self.subTest(mode=mode, offset=offset, size=size):
                self.assert_rejected(seal(header), message="slot form")
        header = bytearray(fixture())
        header[64 + 13 * 16 + 1] = 1
        self.assert_rejected(seal(header), message="slot form")

    def test_zero_records_are_ignored_and_extra_p_sentinels_are_reported(self):
        header = bytearray(fixture())
        put_slot(header, 13, ord("P"), 0, 0)
        result = self.validate(seal(header))
        self.assertEqual(result["observed_slot_count"], 3)
        self.assertEqual(result["filesystem_slots"][-1], {
            "slot_index": 13, "mode": "P", "offset": 0,
            "bytes": 0, "end_offset_exclusive": 0})
        self.assertEqual(len(result["nonempty_spans"]), 2)

    def test_empty_p_sentinels_may_share_extent_or_eof_positions(self):
        for offset in (0, 512, 550, 576, 672):
            header = bytearray(fixture())
            put_slot(header, 1, ord("P"), offset, 0)
            with self.subTest(offset=offset):
                result = self.validate(seal(header))
                self.assertEqual(result["filesystem_slots"][1]["offset"], offset)
                self.assertEqual(len(result["nonempty_spans"]), 2)

    def test_empty_p_sentinel_inside_header_or_beyond_eof_is_rejected(self):
        for offset in (1, 511, 673, 0xffffffff):
            header = bytearray(fixture())
            put_slot(header, 1, ord("P"), offset, 0)
            with self.subTest(offset=offset):
                self.assert_rejected(seal(header), message="empty extent")

    def test_empty_firmware_is_allowed_at_zero_payload_or_eof(self):
        for offset in (0, 512, 550, 672):
            header = bytearray(fixture())
            put_u32(header, 48, offset)
            put_u32(header, 52, 0)
            with self.subTest(offset=offset):
                result = self.validate(seal(header))
                self.assertEqual(result["firmware"]["offset"], offset)
                self.assertEqual(len(result["nonempty_spans"]), 1)

    def test_empty_firmware_inside_header_or_beyond_eof_is_rejected(self):
        for offset in (1, 511, 673, 0xffffffff):
            header = bytearray(fixture())
            put_u32(header, 48, offset)
            put_u32(header, 52, 0)
            with self.subTest(offset=offset):
                self.assert_rejected(seal(header), message="empty extent")

    def test_all_nonempty_extent_types_enforce_start_and_end_bounds(self):
        for kind in ("firmware", "U", "P"):
            for offset, size in ((0, 1), (511, 1), (672, 1), (673, 1),
                                 (576, 97), (0xffffffff, 1),
                                 (0xfffffff0, 32), (512, 0xffffffff)):
                header = bytearray(fixture())
                if kind == "firmware":
                    put_u32(header, 48, offset)
                    put_u32(header, 52, size)
                else:
                    put_slot(header, 0 if kind == "U" else 1,
                             ord(kind), offset, size)
                with self.subTest(kind=kind, offset=offset, size=size):
                    self.assert_rejected(seal(header), message="bounds")

    def test_touching_nonempty_extents_and_exact_eof_are_accepted(self):
        header = bytearray(fixture())
        put_u32(header, 48, 608)
        put_u32(header, 52, 64)
        put_slot(header, 1, ord("P"), 576, 32)
        result = self.validate(seal(header))
        self.assertEqual(len(result["nonempty_spans"]), 3)
        self.assertEqual(result["firmware"]["end_offset_exclusive"], 672)

    def test_valid_extents_need_not_be_in_slot_or_firmware_order(self):
        header = bytearray(fixture())
        put_u32(header, 48, 512)
        put_u32(header, 52, 32)
        put_slot(header, 0, ord("U"), 608, 64)
        put_slot(header, 1, ord("P"), 544, 64)
        result = self.validate(seal(header))
        self.assertEqual([span["offset"] for span in result["nonempty_spans"]],
                         [512, 608, 544])

    def test_each_pair_of_nonempty_extent_types_must_not_overlap(self):
        cases = (("U/firmware", 550, 32, 512, 64, 512, 0),
                 ("P/firmware", 576, 96, 512, 64, 600, 1),
                 ("U/P", 576, 96, 512, 64, 550, 1),
                 ("exact duplicate", 576, 96, 512, 64, 512, 64),
                 ("containing", 512, 160, 530, 1, 512, 0))
        for name, fw_offset, fw_size, u_offset, u_size, p_offset, p_size in cases:
            header = bytearray(fixture())
            put_u32(header, 48, fw_offset)
            put_u32(header, 52, fw_size)
            put_slot(header, 0, ord("U"), u_offset, u_size)
            put_slot(header, 1, ord("P"), p_offset, p_size)
            with self.subTest(name=name):
                self.assert_rejected(seal(header), message="overlap")

    def test_multiple_nonempty_p_slots_are_checked_against_each_other(self):
        header = bytearray(fixture())
        put_u32(header, 48, 0)
        put_u32(header, 52, 0)
        put_slot(header, 1, ord("P"), 576, 64)
        put_slot(header, 27, ord("P"), 630, 42)
        self.assert_rejected(seal(header), message="overlap")

    def test_uninterpreted_padding_is_reported_without_invented_semantics(self):
        self.assertIs(self.validate()["uninterpreted_padding_nonzero"], False)
        for offset in (17, 19, 21, 23, 24, 31, 34, 35, 44, 47,
                       60, 63, 65, 67, 76, 79, 81, 83, 92, 95):
            header = bytearray(fixture())
            header[offset] = 0xa5
            with self.subTest(offset=offset):
                result = self.validate(seal(header))
                self.assertIs(result["uninterpreted_padding_nonzero"], True)
                self.assertFalse(result["identity_inferred"])

    def test_final_reserved_predicate_is_distinct_from_valid_crc(self):
        for offset in (508, 509, 510, 511):
            header = bytearray(fixture())
            put_slot(header, 27, ord("P"), 0, 0)
            header[offset] = 1
            sealed = seal(header)
            self.assertEqual(struct.unpack_from("<I", sealed, 8)[0],
                             oracle_crc32(sealed[12:512]))
            with self.subTest(offset=offset):
                self.assert_rejected(sealed, message="reserved")

    def test_raw_model_region_and_version_codes_do_not_imply_identity(self):
        header = bytearray(fixture())
        put_u32(header, 36, 0xffffffff)
        put_u32(header, 40, 0xffffffff)
        header[32:34] = b"\xff\xff"
        result = self.validate(seal(header))
        self.assertEqual(result["model_field_code"], 0xffffffff)
        self.assertEqual(result["region_field_code"], 0xffffffff)
        self.assertEqual(result["version_major_code"], 255)
        self.assertEqual(result["version_minor_code"], 255)
        self.assertFalse(result["identity_inferred"])
        for semantic_key in ("model", "region", "firmware_version", "target_profile",
                             "package_offset", "virtual_address", "runtime_address"):
            self.assertNotIn(semantic_key, result)

    def test_metadata_flags_do_not_promote_header_crc_to_payload_or_support(self):
        result = self.validate()
        self.assertEqual(result["status"], "header_and_spans_only")
        self.assertEqual(result["address_type"], "decoded_fdat_file_offset")
        self.assertEqual(result["compatibility"], "UNVERIFIED")
        self.assertIs(result["header_crc32_verified"], True)
        self.assertIs(result["decoded_bytes_is_caller_supplied"], True)
        for key in ("payload_integrity_verified", "signature_verified",
                    "container_validated", "identity_inferred", "abi_verified",
                    "extraction_performed", "decryption_performed",
                    "decompression_performed", "execution_performed",
                    "camera_access_performed", "count_semantics_verified"):
            with self.subTest(key=key):
                self.assertIs(result[key], False)
        json.dumps(result, allow_nan=False)

    def test_payload_bytes_are_not_inputs_or_integrity_evidence(self):
        header = fixture()
        full_a = header + bytes(160)
        full_b = header + bytes([255]) * 160
        self.assertNotEqual(full_a, full_b)
        self.assertEqual(self.validate(full_a[:512], len(full_a)),
                         self.validate(full_b[:512], len(full_b)))
        self.assertFalse(self.validate(header)["payload_integrity_verified"])
        self.assert_rejected(full_a)

    def test_pure_api_emits_no_output_or_raw_input_on_success_and_rejection(self):
        marker = b"synthetic-private-marker"
        header = bytearray(fixture())
        header[100:100 + len(marker)] = marker
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            self.validate()
            with self.assertRaises(fdat_header.FDATError) as raised:
                self.validate(bytes(header))
        self.assertEqual(out.getvalue(), "")
        self.assertEqual(err.getvalue(), "")
        self.assertNotIn(marker.decode("ascii"), str(raised.exception))
        self.assertNotIn(repr(bytes(header)), str(raised.exception))


if __name__ == "__main__":
    unittest.main()
