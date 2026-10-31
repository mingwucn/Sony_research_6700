"""Unit tests for α6700 Combined Patch Specification (FTP + English)."""
import os
import unittest

from tools.patch_spec import (
    SECTOR_SIZE,
    PatchError,
    get_combined_targets,
    STOCK_EN_SECTOR_SHA256,
    PATCHED_EN_SECTOR_SHA256,
    STOCK_FTP_SECTOR_SHA256,
    PATCHED_FTP_SECTOR_SHA256,
)


class TestPatchSpec(unittest.TestCase):
    def setUp(self):
        self.en_target, self.ftp_target = get_combined_targets()

    def test_target_metadata(self):
        self.assertEqual(self.en_target.target_id, "APP-EN-01")
        self.assertEqual(self.en_target.sector, 383128)
        self.assertEqual(self.en_target.offset_in_sector, 248)
        self.assertEqual(len(self.en_target.preimage), 4)
        self.assertEqual(len(self.en_target.patched), 4)

        self.assertEqual(self.ftp_target.target_id, "APP-FTP-01")
        self.assertEqual(self.ftp_target.sector, 445966)
        self.assertEqual(self.ftp_target.offset_in_sector, 228)
        self.assertEqual(len(self.ftp_target.preimage), 1)
        self.assertEqual(len(self.ftp_target.patched), 1)

    def test_synthetic_roundtrip_en(self):
        dummy_stock = bytearray(b"\x00" * SECTOR_SIZE)
        dummy_stock[248:252] = self.en_target.preimage

        from tools.patch_spec import TargetSector
        import hashlib
        stock_hash = hashlib.sha256(dummy_stock).hexdigest()
        patched_dummy = bytearray(dummy_stock)
        patched_dummy[248:252] = self.en_target.patched
        patched_hash = hashlib.sha256(patched_dummy).hexdigest()

        target = TargetSector(
            target_id="TEST-EN",
            device="/dev/test",
            sector=100,
            offset_in_sector=248,
            preimage=self.en_target.preimage,
            patched=self.en_target.patched,
            stock_sector_sha256=stock_hash,
            patched_sector_sha256=patched_hash,
        )

        patched = target.apply_patch(bytes(dummy_stock))
        self.assertEqual(patched[248:252], self.en_target.patched)
        self.assertTrue(target.verify_patched_sector(patched))

        reverted = target.revert_patch(patched)
        self.assertEqual(reverted[248:252], self.en_target.preimage)
        self.assertTrue(target.verify_stock_sector(reverted))

    def test_corrupt_preimage_rejected(self):
        corrupt_sector = bytearray(b"\x00" * SECTOR_SIZE)
        corrupt_sector[248:252] = b"\xde\xad\xbe\xef"
        with self.assertRaises(PatchError):
            self.en_target.apply_patch(bytes(corrupt_sector))

    def test_invalid_sector_size_rejected(self):
        with self.assertRaises(PatchError):
            self.en_target.verify_stock_sector(b"\x00" * 511)
        with self.assertRaises(PatchError):
            self.en_target.verify_stock_sector(b"\x00" * 513)

    def test_real_ext2_sectors_roundtrip(self):
        ext2_path = "private/english-offline-20261026/application-nflasha15.ext2"
        if not os.path.exists(ext2_path):
            self.skipTest("ext2 file not present in local test environment")

        with open(ext2_path, "rb") as f:
            # English sector
            f.seek(self.en_target.sector * SECTOR_SIZE)
            en_data = f.read(SECTOR_SIZE)
            self.assertTrue(self.en_target.verify_stock_sector(en_data))
            en_patched = self.en_target.apply_patch(en_data)
            self.assertTrue(self.en_target.verify_patched_sector(en_patched))
            self.assertEqual(self.en_target.revert_patch(en_patched), en_data)

            # FTP sector
            f.seek(self.ftp_target.sector * SECTOR_SIZE)
            ftp_data = f.read(SECTOR_SIZE)
            self.assertTrue(self.ftp_target.verify_stock_sector(ftp_data))
            ftp_patched = self.ftp_target.apply_patch(ftp_data)
            self.assertTrue(self.ftp_target.verify_patched_sector(ftp_patched))
            self.assertEqual(self.ftp_target.revert_patch(ftp_patched), ftp_data)


if __name__ == "__main__":
    unittest.main()
