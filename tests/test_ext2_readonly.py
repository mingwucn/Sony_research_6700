"""Invented ext2 images only: no local firmware, mounts, devices or network."""
import struct
import unittest

from tools.ext2_readonly import Ext2Error, Ext2Inode, Ext2Reader


class Image:
    BLOCK = 1024

    def __init__(self, *, revision=1, inode_size=128, filetype=True):
        self.raw = bytearray(96 * self.BLOCK)
        self.inode_size = 128 if revision == 0 else inode_size
        self.filetype = bool(filetype and revision)
        self.reads = []
        for offset, value in ((0, 32), (4, 96), (20, 1), (24, 0), (28, 0),
                              (32, 96), (36, 96), (40, 32), (76, revision),
                              (84, 11), (92, 0x38), (96, 2 if self.filetype else 0),
                              (100, 3)):
            self.sb32(offset, value)
        self.sb16(56, 0xEF53)
        self.sb16(88, inode_size)
        struct.pack_into("<III", self.raw, 2 * self.BLOCK, 3, 4, 5)
        self.node(2, 0x41ED, 1024, [12])
        self.node(11, 0x41ED, 1024, [13])
        self.node(12, 0x41ED, 1024, [14])
        self.node(13, 0x81A4, 8, [15])
        self.node(14, 0xA1FF, 7, [])
        self.node(15, 0x21A4, 0, [])
        self.directory(12, [(2, ".", 2), (2, "..", 2), (11, "share", 2),
                            (14, "link", 7), (15, "device", 3)])
        self.directory(13, [(11, ".", 2), (2, "..", 2), (12, "app", 2)])
        self.directory(14, [(12, ".", 2), (11, "..", 2), (13, "english.uxc", 1)])
        self.raw[15 * self.BLOCK:15 * self.BLOCK + 8] = b"English\0"

    def sb32(self, offset, value):
        struct.pack_into("<I", self.raw, 1024 + offset, value)

    def sb16(self, offset, value):
        struct.pack_into("<H", self.raw, 1024 + offset, value)

    def node(self, number, mode, size, blocks, *, flags=0, high=0):
        at = 5 * self.BLOCK + (number - 1) * self.inode_size
        self.raw[at:at + self.inode_size] = bytes(self.inode_size)
        struct.pack_into("<H", self.raw, at, mode)
        struct.pack_into("<I", self.raw, at + 4, size)
        struct.pack_into("<I", self.raw, at + 32, flags)
        struct.pack_into("<15I", self.raw, at + 40, *(blocks + [0] * (15 - len(blocks))))
        struct.pack_into("<I", self.raw, at + 108, high)

    def directory(self, block, entries):
        at = block * self.BLOCK
        self.raw[at:at + self.BLOCK] = bytes(self.BLOCK)
        for index, (number, name, kind) in enumerate(entries):
            encoded = name if isinstance(name, bytes) else name.encode()
            length = ((8 + len(encoded) + 3) // 4) * 4
            if index == len(entries) - 1:
                length = (block + 1) * self.BLOCK - at
            struct.pack_into("<IH", self.raw, at, number, length)
            if self.filetype:
                struct.pack_into("<BB", self.raw, at + 6, len(encoded), kind)
            else:
                struct.pack_into("<H", self.raw, at + 6, len(encoded))
            self.raw[at + 8:at + 8 + len(encoded)] = encoded
            at += length

    def pointer(self, block, index, value):
        struct.pack_into("<I", self.raw, block * self.BLOCK + index * 4, value)

    def read(self, offset, length):
        assert 0 <= offset <= len(self.raw) and 0 <= length <= len(self.raw) - offset
        self.reads.append((offset, length))
        return bytes(self.raw[offset:offset + length])

    def reader(self, **kwargs):
        return Ext2Reader(self.read, len(self.raw), **kwargs)


class Ext2ReadonlyTests(unittest.TestCase):
    def test_resolve_read_and_inode_metadata(self):
        fixture = Image()
        reader = fixture.reader()
        node = reader.resolve("/share/app/english.uxc")
        self.assertEqual((node.number, node.kind, node.size), (13, "file", 8))
        self.assertEqual(reader.read_file(node), b"English\0")
        self.assertEqual(reader.inode(2).kind, "directory")
        self.assertTrue(all(0 <= at and at + length <= len(fixture.raw)
                            for at, length in fixture.reads))

    def test_directory_listing_and_virtual_dot_parent(self):
        reader = Image().reader()
        entries = reader.list_dir(2)
        self.assertEqual([(e.name, e.inode, e.file_type) for e in entries[:3]],
                         [(".", 2, 2), ("..", 2, 2), ("share", 11, 2)])
        self.assertEqual(reader.resolve("/share/./app/../app//").number, 12)
        self.assertEqual(reader.resolve("/").number, 2)

    def test_revision_zero_and_legacy_directory_records(self):
        reader = Image(revision=0).reader()
        self.assertEqual(reader.inode_size, 128)
        self.assertEqual(reader.read_file(reader.resolve("/share/app/english.uxc")), b"English\0")
        self.assertEqual(reader.list_dir(2)[0].file_type, 0)

    def test_256_byte_inodes(self):
        reader = Image(inode_size=256).reader()
        self.assertEqual(reader.read_file(13), b"English\0")

    def test_second_inode_group_uses_its_own_descriptor_and_bounds(self):
        fixture = Image()
        fixture.raw.extend(bytes((257 - 96) * 1024))
        for offset, value in ((0, 64), (4, 257), (32, 128), (36, 128)):
            fixture.sb32(offset, value)
        struct.pack_into("<III", fixture.raw, 2048 + 32, 131, 132, 133)
        at = 133 * 1024
        struct.pack_into("<H", fixture.raw, at, 0x81A4)
        struct.pack_into("<I", fixture.raw, at + 4, 3)
        struct.pack_into("<I", fixture.raw, at + 40, 140)
        fixture.raw[140 * 1024:140 * 1024 + 3] = b"XYZ"
        reader = fixture.reader()
        self.assertEqual(reader.group_count, 2)
        self.assertEqual(reader.read_file(33), b"XYZ")
        struct.pack_into("<III", fixture.raw, 2048 + 32, 131, 132, 128)
        with self.assertRaisesRegex(Ext2Error, "outside its group"):
            fixture.reader().inode(33)

    def test_invalid_constructor_arguments_and_short_image(self):
        fixture = Image()
        for value in (0, -1, True, 3.5):
            with self.subTest(value=value), self.assertRaises(Ext2Error):
                Ext2Reader(fixture.read, value)
        for options in ({"max_read_bytes": 0}, {"max_directory_bytes": False}):
            with self.subTest(options=options), self.assertRaises(Ext2Error):
                fixture.reader(**options)
        with self.assertRaises(Ext2Error):
            Ext2Reader(None, len(fixture.raw))
        with self.assertRaisesRegex(Ext2Error, "range"):
            Ext2Reader(fixture.read, 1024)

    def test_sparse_direct_and_single_indirection(self):
        fixture = Image()
        pointers = [15] + [0] * 11 + [20]
        fixture.node(13, 0x81A4, 14 * 1024, pointers)
        fixture.pointer(20, 0, 21)
        fixture.raw[21 * 1024:22 * 1024] = b"S" * 1024
        result = fixture.reader().read_file(13)
        self.assertEqual(result[:8], b"English\0")
        self.assertEqual(result[1024:12 * 1024], bytes(11 * 1024))
        self.assertEqual(result[12 * 1024:13 * 1024], b"S" * 1024)
        self.assertEqual(result[13 * 1024:], bytes(1024))

    def test_double_indirection_and_missing_indirect_holes(self):
        fixture = Image()
        fixture.node(13, 0x81A4, 269 * 1024, [0] * 13 + [22])
        fixture.pointer(22, 0, 23)
        fixture.pointer(23, 0, 24)
        fixture.raw[24 * 1024:25 * 1024] = b"D" * 1024
        reader = fixture.reader()
        result = reader.read_file(13)
        self.assertEqual(result[:268 * 1024], bytes(268 * 1024))
        self.assertEqual(result[268 * 1024:], b"D" * 1024)
        self.assertEqual(reader._file_block(reader.inode(13), 268 + 256), 0)

    def test_triple_indirection_all_levels_and_holes(self):
        fixture = Image()
        fixture.node(13, 0x81A4, 1, [0] * 14 + [25])
        fixture.pointer(25, 1, 26)
        fixture.pointer(26, 2, 27)
        fixture.pointer(27, 3, 28)
        reader = fixture.reader()
        first_triple = 12 + 256 + 256 ** 2
        logical = first_triple + 256 ** 2 + 2 * 256 + 3
        self.assertEqual(reader._file_block(reader.inode(13), logical), 28)
        self.assertEqual(reader._file_block(reader.inode(13), first_triple), 0)
        self.assertEqual(reader._file_block(reader.inode(13), logical + 1), 0)

    def test_corrupt_triple_pointer_refused_before_out_of_bounds_callback(self):
        fixture = Image()
        fixture.node(13, 0x81A4, 1, [0] * 14 + [25])
        fixture.pointer(25, 0, 26)
        fixture.pointer(26, 0, 96)
        reader = fixture.reader()
        with self.assertRaisesRegex(Ext2Error, "block pointer"):
            reader._file_block(reader.inode(13), 12 + 256 + 256 ** 2)
        self.assertTrue(all(at + length <= len(fixture.raw) for at, length in fixture.reads))

    def test_file_budget_and_zero_length(self):
        fixture = Image()
        reader = fixture.reader(max_read_bytes=8)
        self.assertEqual(reader.read_file(13, max_bytes=8), b"English\0")
        with self.assertRaisesRegex(Ext2Error, "budget"):
            reader.read_file(13, max_bytes=7)
        with self.assertRaisesRegex(Ext2Error, "budget"):
            reader.read_file(13, max_bytes=9)
        fixture.node(13, 0x81A4, 0, [])
        self.assertEqual(reader.read_file(13, max_bytes=0), b"")

    def test_no_callback_on_invalid_range(self):
        fixture = Image()
        reader = fixture.reader()
        before = list(fixture.reads)
        for at, length in ((-1, 1), (0, -1), (len(fixture.raw), 1), (0, len(fixture.raw) + 1)):
            with self.subTest(at=at, length=length), self.assertRaises(Ext2Error):
                reader._read(at, length)
        self.assertEqual(fixture.reads, before)

    def test_callback_short_and_wrong_type(self):
        for callback in (lambda at, count: bytes(count - 1), lambda at, count: "x" * count):
            with self.subTest(callback=callback), self.assertRaisesRegex(Ext2Error, "callback"):
                Ext2Reader(callback, 4096)

    def test_superblock_corruption_and_unsupported_features(self):
        mutations = (("bad magic", 56, 0, 16), ("revision", 76, 2, 32),
                     ("block size", 24, 3, 32), ("first block", 20, 0, 32),
                     ("zero blocks", 4, 0, 32), ("image extent", 4, 1000, 32),
                     ("group count", 32, 0, 32), ("fragment size", 28, 1, 32),
                     ("fragment group", 36, 32, 32), ("inode group", 40, 0, 32),
                     ("inode count", 0, 33, 32), ("inode size", 88, 192, 16),
                     ("extents", 96, 0x42, 32), ("64-bit", 96, 0x82, 32),
                     ("checksum", 100, 0x403, 32), ("journal", 92, 0x3C, 32),
                     ("descriptor", 254, 64, 16), ("first inode", 84, 1, 32))
        for name, offset, value, width in mutations:
            with self.subTest(name=name):
                fixture = Image()
                (fixture.sb16 if width == 16 else fixture.sb32)(offset, value)
                with self.assertRaises(Ext2Error):
                    fixture.reader()

    def test_bad_inode_number_unallocated_and_flags(self):
        fixture = Image()
        reader = fixture.reader()
        for number in (0, -1, 33, True, "2"):
            with self.subTest(number=number), self.assertRaises(Ext2Error):
                reader.inode(number)
        with self.assertRaisesRegex(Ext2Error, "unallocated"):
            reader.inode(16)
        fixture.node(13, 0x81A4, 8, [15], flags=0x80000)
        with self.assertRaisesRegex(Ext2Error, "extent"):
            reader.inode(13)

    def test_bad_group_metadata(self):
        for fields in ((96, 4, 5), (3, 4, 95), (3, 3, 5), (5, 4, 5)):
            with self.subTest(fields=fields):
                fixture = Image()
                struct.pack_into("<III", fixture.raw, 2048, *fields)
                with self.assertRaises(Ext2Error):
                    fixture.reader().inode(2)

    def test_bad_direct_and_indirect_pointers(self):
        for level in ("direct", "single root", "single leaf", "double root", "double leaf"):
            with self.subTest(level=level):
                fixture = Image()
                if level == "direct":
                    fixture.node(13, 0x81A4, 1, [96])
                elif level.startswith("single"):
                    fixture.node(13, 0x81A4, 13 * 1024, [0] * 12 + [96 if level.endswith("root") else 20])
                    fixture.pointer(20, 0, 96)
                else:
                    fixture.node(13, 0x81A4, 269 * 1024, [0] * 13 + [96 if level.endswith("root") else 22])
                    fixture.pointer(22, 0, 96)
                with self.assertRaisesRegex(Ext2Error, "block pointer"):
                    fixture.reader().read_file(13)

    def test_path_refusals(self):
        reader = Image().reader()
        for path in ("share/app", "/../share", "/share/../../", "/share\\app",
                     "/share\0/app", "/" + "a" * 256, "/" + "a" * 4097,
                     "/share/app/english.uxc/", "/share/app/english.uxc/..", "/missing"):
            with self.subTest(path=path), self.assertRaises(Ext2Error):
                reader.resolve(path)

    def test_symlink_and_special_file_refused(self):
        reader = Image().reader()
        for path in ("/link", "/link/child"):
            with self.subTest(path=path), self.assertRaisesRegex(Ext2Error, "symlink"):
                reader.resolve(path)
        for number in (2, 14, 15):
            with self.subTest(number=number), self.assertRaises(Ext2Error):
                reader.read_file(number)
        with self.assertRaises(Ext2Error):
            reader.list_dir(13)

    def test_forged_inode_is_reloaded(self):
        reader = Image().reader()
        forged = Ext2Inode(13, 0x81A4, 1, 0, (95,) + (0,) * 14)
        self.assertEqual(reader.read_file(forged), b"English\0")

    def test_directory_corruption(self):
        mutations = ((4, "<H", 0), (4, "<H", 10), (4, "<H", 2048),
                     (6, "<B", 255), (0, "<I", 33), (7, "<B", 8))
        for offset, fmt, value in mutations:
            with self.subTest(offset=offset, fmt=fmt, value=value):
                fixture = Image()
                struct.pack_into(fmt, fixture.raw, 12 * 1024 + offset, value)
                with self.assertRaises(Ext2Error):
                    fixture.reader().list_dir(2)

    def test_duplicate_bad_names_and_type_mismatch(self):
        for entries in ([(2, ".", 2), (2, ".", 2)], [(2, b"bad/name", 2)],
                        [(2, b"bad\0name", 2)]):
            with self.subTest(entries=entries):
                fixture = Image()
                fixture.directory(12, entries)
                with self.assertRaises(Ext2Error):
                    fixture.reader().list_dir(2)
        fixture = Image()
        fixture.directory(12, [(11, "share", 1)])
        with self.assertRaisesRegex(Ext2Error, "disagrees"):
            fixture.reader().resolve("/share")

    def test_non_utf8_name_preserved(self):
        fixture = Image()
        fixture.directory(14, [(13, b"english\xff.uxc", 1)])
        reader = fixture.reader()
        name = reader.list_dir(12)[0].name
        self.assertEqual(name.encode("utf-8", "surrogateescape"), b"english\xff.uxc")
        self.assertEqual(reader.read_file(reader.resolve("/share/app/" + name)), b"English\0")

    def test_directory_size_and_budget(self):
        fixture = Image()
        fixture.node(2, 0x41ED, 9, [12])
        with self.assertRaisesRegex(Ext2Error, "aligned"):
            fixture.reader().list_dir(2)
        fixture.node(2, 0x41ED, 1024, [12])
        with self.assertRaisesRegex(Ext2Error, "budget"):
            fixture.reader(max_directory_bytes=8).list_dir(2)

    def test_large_file_feature_and_capacity_bounds(self):
        fixture = Image()
        fixture.sb32(100, 1)
        fixture.node(13, 0x81A4, 0, [], high=1)
        with self.assertRaisesRegex(Ext2Error, "LARGE_FILE"):
            fixture.reader().inode(13)
        fixture = Image()
        fixture.node(13, 0x81A4, 1, [], high=5)
        reader = fixture.reader(max_read_bytes=30 * 1024 ** 3)
        with self.assertRaisesRegex(Ext2Error, "capacity"):
            reader.read_file(13)


if __name__ == "__main__":
    unittest.main()
