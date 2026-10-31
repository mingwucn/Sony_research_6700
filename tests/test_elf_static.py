"""Invented ELF images only; no real firmware, device, files or external tools."""
import struct
import unittest

from tools.elf_static import ElfError, ElfImage


TEXT_OFFSET = 0x200
TEXT_VA = 0x400200
RO_OFFSET = 0x300
RO_VA = 0x500300
SHOFF = 0x600


def fixture():
    data = bytearray(0x800)
    data[:7] = b"\x7fELF\x02\x01\x01"
    struct.pack_into("<HHIQQQIHHHHHH", data, 16,
                     3, 183, 1, TEXT_VA, 64, SHOFF, 0, 64, 56, 2, 64, 6, 5)
    struct.pack_into("<IIQQQQQQ", data, 64, 1, 5, TEXT_OFFSET, TEXT_VA, 0,
                     0x100, 0x120, 0x100)
    struct.pack_into("<IIQQQQQQ", data, 120, 1, 4, RO_OFFSET, RO_VA, 0,
                     0x200, 0x200, 0x100)
    data[RO_OFFSET:RO_OFFSET + 17] = b"Language\0ALLLANG\0"
    strings = b"\0getLanguage\0setLanguage\0"
    data[0x380:0x380 + len(strings)] = strings
    names = b"\0.text\0.rodata\0.strtab\0.dynsym\0.shstrtab\0"
    data[0x500:0x500 + len(names)] = names
    rows = [
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (names.index(b".text"), 1, 6, TEXT_VA, TEXT_OFFSET, 0x40, 0, 0, 4, 0),
        (names.index(b".rodata"), 1, 2, RO_VA, RO_OFFSET, 0x40, 0, 0, 1, 0),
        (names.index(b".strtab"), 3, 0, 0, 0x380, len(strings), 0, 0, 1, 0),
        (names.index(b".dynsym"), 11, 0, 0, 0x400, 72, 3, 1, 8, 24),
        (names.index(b".shstrtab"), 3, 0, 0, 0x500, len(names), 0, 0, 1, 0),
    ]
    for i, row in enumerate(rows):
        struct.pack_into("<IIQQQQIIQQ", data, SHOFF + i * 64, *row)
    struct.pack_into("<IBBHQQ", data, 0x418, 1, 0x12, 2, 1, TEXT_VA + 16, 8)
    struct.pack_into("<IBBHQQ", data, 0x430, strings.index(b"setLanguage"), 0x12, 0, 0, 0, 0)
    return data


def branch(source, target, *, link=False):
    return (0x94000000 if link else 0x14000000) | (((target - source) // 4) & 0x3ffffff)


def adrp(register, page_delta):
    bits = page_delta & 0x1fffff
    return 0x90000000 | (bits & 3) << 29 | (bits >> 2) << 5 | register


def add(register, base, value, *, shift=False):
    return 0x91000000 | (0x400000 if shift else 0) | value << 10 | base << 5 | register


class ElfStaticTests(unittest.TestCase):
    def test_header_sections_and_symbols(self):
        image = ElfImage(bytes(fixture()))
        self.assertEqual((image.machine, image.type, image.entry), (183, 3, TEXT_VA))
        self.assertEqual([s.name for s in image.sections], ["", ".text", ".rodata", ".strtab", ".dynsym", ".shstrtab"])
        defined, undefined = image.symbols()[1:]
        self.assertEqual((defined.name, defined.value, defined.size, defined.type, defined.binding,
                          defined.visibility, defined.section_index), ("getLanguage", TEXT_VA + 16, 8, 2, 1, 2, 1))
        self.assertEqual((undefined.name, undefined.value, undefined.section_index), ("setLanguage", 0, 0))

    def test_immutable_and_class_endian_version_checks(self):
        base = fixture()
        for value in (b"", bytearray(base), memoryview(base), bytes(base[:63])):
            with self.subTest(value_type=type(value)), self.assertRaises(ElfError):
                ElfImage(value)
        for at, value in ((0, 0), (4, 1), (5, 2), (6, 2), (20, 2), (52, 63)):
            bad = base.copy()
            bad[at] = value
            with self.subTest(at=at), self.assertRaises(ElfError):
                ElfImage(bytes(bad))

    def test_table_and_entry_bounds(self):
        for at, fmt, value in ((32, "Q", 0x7f0), (40, "Q", 0x7f0),
                               (54, "H", 55), (58, "H", 63), (60, "H", 65535)):
            data = fixture()
            struct.pack_into("<" + fmt, data, at, value)
            with self.subTest(at=at), self.assertRaises(ElfError):
                ElfImage(bytes(data))

    def test_section_zero_and_name_table_validation(self):
        for at, fmt, value in ((SHOFF + 4, "I", 1), (62, "H", 7),
                               (SHOFF + 5 * 64 + 4, "I", 1), (SHOFF + 64, "I", 999),
                               (SHOFF + 5 * 64 + 8, "Q", 0x800)):
            data = fixture()
            struct.pack_into("<" + fmt, data, at, value)
            with self.subTest(at=at), self.assertRaises(ElfError):
                ElfImage(bytes(data))

    def test_sectionless_elf_and_missing_tables(self):
        data = fixture()
        struct.pack_into("<Q", data, 40, 0)
        struct.pack_into("<HHH", data, 58, 0, 0, 0)
        image = ElfImage(bytes(data))
        self.assertEqual(image.sections, ())
        self.assertEqual(image.symbols(), ())
        struct.pack_into("<H", data, 60, 1)
        with self.assertRaises(ElfError):
            ElfImage(bytes(data))

    def test_extended_header_counts(self):
        data = fixture()
        struct.pack_into("<HH", data, 60, 0, 0xffff)
        struct.pack_into("<H", data, 56, 0xffff)
        struct.pack_into("<Q", data, SHOFF + 32, 6)
        struct.pack_into("<II", data, SHOFF + 40, 5, 2)
        image = ElfImage(bytes(data))
        self.assertEqual((len(image.sections), len(image.segments)), (6, 2))

    def test_load_segment_file_memory_alignment_and_overflow(self):
        for at, value in ((64 + 8, 0x900), (64 + 40, 0x20),
                          (64 + 48, 3), (64 + 16, TEXT_VA + 1),
                          (64 + 16, (1 << 64) - 0x100)):
            data = fixture()
            struct.pack_into("<Q", data, at, value)
            with self.subTest(at=at, value=value), self.assertRaises(ElfError):
                ElfImage(bytes(data))

    def test_file_backed_mapping_and_bss_exclusion(self):
        image = ElfImage(bytes(fixture()))
        self.assertEqual(image.va_to_offset(TEXT_VA + 12, 4), TEXT_OFFSET + 12)
        self.assertEqual(image.offset_to_vas(TEXT_OFFSET + 12, 4), (TEXT_VA + 12,))
        self.assertIsNone(image.va_to_offset(TEXT_VA + 0x100))
        self.assertIsNone(image.va_to_offset(TEXT_VA + 0xfe, 4))
        self.assertEqual(image.offset_to_vas(0), ())
        for value, size in ((True, 1), (-1, 1), (0, 0), ((1 << 64) - 1, 2)):
            with self.subTest(value=value, size=size), self.assertRaises(ElfError):
                image.va_to_offset(value, size)
        with self.assertRaises(ElfError):
            image.offset_to_vas(len(image.data), 1)

    def test_conflicting_virtual_mapping_refused(self):
        data = fixture()
        struct.pack_into("<Q", data, 120 + 16, TEXT_VA)
        image = ElfImage(bytes(data))
        with self.assertRaises(ElfError):
            image.va_to_offset(TEXT_VA)

    def test_alias_file_mapping_returns_all_virtual_addresses(self):
        data = fixture()
        struct.pack_into("<QQ", data, 120 + 8, TEXT_OFFSET, RO_VA - 0x100)
        image = ElfImage(bytes(data))
        self.assertEqual(image.offset_to_vas(TEXT_OFFSET), (TEXT_VA, RO_VA - 0x100))

    def test_section_bytes_and_nobits(self):
        data = fixture()
        image = ElfImage(bytes(data))
        self.assertTrue(image.section_data(image.sections[2]).startswith(b"Language\0"))
        self.assertEqual(image.section_data(image.sections[0]), b"")
        struct.pack_into("<I", data, SHOFF + 2 * 64 + 4, 8)
        struct.pack_into("<Q", data, SHOFF + 2 * 64 + 24, 0x100000)
        image = ElfImage(bytes(data))
        with self.assertRaises(ElfError):
            image.section_data(image.sections[2])
        with self.assertRaises(ElfError):
            image.section_data(None)

    def test_non_nobits_section_outside_image_refused(self):
        data = fixture()
        struct.pack_into("<Q", data, SHOFF + 2 * 64 + 24, 0x100000)
        with self.assertRaises(ElfError):
            ElfImage(bytes(data))

    def test_symbol_table_shape_and_string_link(self):
        for at, fmt, value in ((SHOFF + 4 * 64 + 56, "Q", 0),
                               (SHOFF + 4 * 64 + 32, "Q", 73),
                               (SHOFF + 4 * 64 + 40, "I", 999),
                               (SHOFF + 4 * 64 + 40, "I", 1),
                               (SHOFF + 4 * 64 + 8, "Q", 0x800)):
            data = fixture()
            struct.pack_into("<" + fmt, data, at, value)
            image = ElfImage(bytes(data))
            with self.subTest(at=at, value=value), self.assertRaises(ElfError):
                image.symbols()

    def test_symbol_string_bounds_and_termination(self):
        for name in (999,):
            data = fixture()
            struct.pack_into("<I", data, 0x418, name)
            with self.assertRaises(ElfError):
                ElfImage(bytes(data)).symbols()
        data = fixture()
        struct.pack_into("<Q", data, SHOFF + 3 * 64 + 32, 5)
        with self.assertRaises(ElfError):
            ElfImage(bytes(data)).symbols()

    def test_symbol_section_indices_and_extent_overflow(self):
        for index in (99, 0xffff):
            data = fixture()
            struct.pack_into("<H", data, 0x418 + 6, index)
            with self.subTest(index=index), self.assertRaises(ElfError):
                ElfImage(bytes(data)).symbols()
        data = fixture()
        struct.pack_into("<Q", data, 0x418 + 8, (1 << 64) - 1)
        with self.assertRaises(ElfError):
            ElfImage(bytes(data)).symbols()

    def test_static_symbol_table_is_also_reported(self):
        data = fixture()
        struct.pack_into("<I", data, SHOFF + 4 * 64 + 4, 2)
        self.assertEqual(ElfImage(bytes(data)).symbols()[1].name, "getLanguage")

    def test_ascii_target_search_mapping_and_suffix(self):
        image = ElfImage(bytes(fixture()))
        hits = image.find_ascii("Language")
        self.assertEqual(hits[0].file_offset, RO_OFFSET)
        self.assertEqual(hits[0].virtual_addresses, (RO_VA,))
        self.assertEqual(len(hits), 3)
        self.assertEqual(image.find_ascii(b"ALLLANG", nul_terminated=True)[0].file_offset, RO_OFFSET + 9)
        self.assertEqual(image.find_ascii("missing"), ())
        self.assertEqual(image.find_ascii("Lang", nul_terminated=True), ())

    def test_ascii_overlapping_hits_and_limit(self):
        data = fixture()
        data[RO_OFFSET:RO_OFFSET + 4] = b"aaaa"
        image = ElfImage(bytes(data))
        self.assertEqual([h.file_offset for h in image.find_ascii("aaa")], [RO_OFFSET, RO_OFFSET + 1])
        with self.assertRaises(ElfError):
            image.find_ascii("aaa", max_hits=1)

    def test_ascii_invalid_options(self):
        image = ElfImage(bytes(fixture()))
        for value in ("", "汉", b"a\0", b"\xff", bytearray(b"a"), None):
            with self.subTest(value=value), self.assertRaises(ElfError):
                image.find_ascii(value)
        with self.assertRaises(ElfError):
            image.find_ascii("a", max_hits=True)
        with self.assertRaises(ElfError):
            image.find_ascii("a", nul_terminated=1)

    def test_direct_forward_backward_b_and_bl(self):
        data = fixture()
        struct.pack_into("<III", data, TEXT_OFFSET,
                         branch(TEXT_VA, TEXT_VA + 32, link=True),
                         branch(TEXT_VA + 4, TEXT_VA - 16), 0xd503201f)
        image = ElfImage(bytes(data))
        refs = image.branch_refs()
        self.assertEqual([(r.kind, r.virtual_address, r.target_va) for r in refs],
                         [("BL", TEXT_VA, TEXT_VA + 32), ("B", TEXT_VA + 4, TEXT_VA - 16)])
        self.assertEqual(image.branch_refs(TEXT_VA + 32), (refs[0],))
        self.assertEqual(image.branch_refs(include_b=False), (refs[0],))

    def test_branch_negative_imm26_extreme(self):
        data = fixture()
        struct.pack_into("<I", data, TEXT_OFFSET, 0x96000000)
        ref = ElfImage(bytes(data)).branch_refs()[0]
        self.assertEqual(ref.target_va, (TEXT_VA - (1 << 27)) % (1 << 64))

    def test_nonexecuting_bytes_are_not_scanned_as_instructions(self):
        data = fixture()
        struct.pack_into("<I", data, RO_OFFSET, 0x94000001)
        self.assertEqual(ElfImage(bytes(data)).branch_refs(), ())

    def test_incomplete_final_instruction_is_ignored(self):
        data = fixture()
        struct.pack_into("<Q", data, 64 + 32, 3)
        struct.pack_into("<I", data, TEXT_OFFSET, 0x94000001)
        self.assertEqual(ElfImage(bytes(data)).branch_refs(), ())

    def test_machine_and_target_validation(self):
        data = fixture()
        struct.pack_into("<H", data, 18, 62)
        image = ElfImage(bytes(data))
        with self.assertRaises(ElfError):
            image.branch_refs()
        with self.assertRaises(ElfError):
            image.adrp_add_refs()
        image = ElfImage(bytes(fixture()))
        for target in (True, -1, 1 << 64):
            with self.subTest(target=target), self.assertRaises(ElfError):
                image.branch_refs(target)
        with self.assertRaises(ElfError):
            image.branch_refs(include_b=1)

    def test_duplicate_executable_segment_does_not_duplicate_references(self):
        data = fixture()
        data[120:176] = data[64:120]
        struct.pack_into("<I", data, TEXT_OFFSET, 0x94000001)
        self.assertEqual(len(ElfImage(bytes(data)).branch_refs()), 1)

    def test_adjacent_adrp_add_positive_and_negative_pages(self):
        for pages in (3, -2, -(1 << 20), (1 << 20) - 1):
            data = fixture()
            struct.pack_into("<II", data, TEXT_OFFSET, adrp(3, pages), add(4, 3, 0x345))
            image = ElfImage(bytes(data))
            target = ((TEXT_VA & ~0xfff) + pages * 4096 + 0x345) % (1 << 64)
            with self.subTest(pages=pages):
                ref, = image.adrp_add_refs(target)
                self.assertEqual((ref.target_va, ref.register), (target, 4))
                self.assertEqual(image.adrp_add_refs(target + 1), ())

    def test_adjacent_adrp_shifted_add(self):
        data = fixture()
        struct.pack_into("<II", data, TEXT_OFFSET, adrp(1, 0), add(2, 1, 3, shift=True))
        self.assertEqual(ElfImage(bytes(data)).adrp_add_refs()[0].target_va,
                         (TEXT_VA & ~0xfff) + 3 * 4096)

    def test_adrp_add_register_and_opcode_mismatches(self):
        for first, second in ((adrp(31, 0), add(1, 31, 1)),
                              (adrp(1, 0), add(2, 3, 1)),
                              (adrp(1, 0), add(31, 1, 1)),
                              (adrp(1, 0), 0xd503201f),
                              (adrp(1, 0), add(2, 1, 1) & ~0x80000000)):
            data = fixture()
            struct.pack_into("<II", data, TEXT_OFFSET, first, second)
            with self.subTest(first=first, second=second):
                self.assertEqual(ElfImage(bytes(data)).adrp_add_refs(), ())

    def test_adrp_requires_adjacent_instruction_and_complete_pair(self):
        data = fixture()
        struct.pack_into("<III", data, TEXT_OFFSET, adrp(1, 0), 0xd503201f, add(2, 1, 1))
        self.assertEqual(ElfImage(bytes(data)).adrp_add_refs(), ())
        struct.pack_into("<Q", data, 64 + 32, 4)
        self.assertEqual(ElfImage(bytes(data)).adrp_add_refs(), ())


if __name__ == "__main__":
    unittest.main()
