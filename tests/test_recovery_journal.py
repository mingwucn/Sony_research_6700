# -*- coding: utf-8 -*-
"""Unit tests for Durable Per-Span Transaction Journal and Recovery Manager."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from apps.a6700_customizer.recovery_journal import (
    JournalEvent,
    JournalStatus,
    RecoveryJournal,
    SpanClassification,
)
from apps.a6700_customizer.targets import TargetSpan, TargetWindow


class TestRecoveryJournal(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        self.target1 = TargetWindow(0x100, b"\x00", b"\x01", "Target 1", "ftp")
        self.target2 = TargetWindow(0x110, b"\xaa", b"\xbb", "Target 2", "ftp")
        self.span1 = TargetSpan(offset=0x100, length=32, targets=[self.target1, self.target2])
        self.span2 = TargetSpan(offset=0x200, length=16, targets=[])

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_journal_creation_and_meta(self):
        journal = RecoveryJournal.create(self.base_dir, "apply", [self.span1, self.span2])
        meta = journal.read_meta()
        self.assertEqual(meta["mode"], "apply")
        self.assertEqual(meta["status"], JournalStatus.INITIALIZED.value)
        self.assertEqual(meta["span_count"], 2)
        self.assertTrue(journal.journal_file.is_file())

    def test_save_and_load_stock_span_binary(self):
        journal = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        dummy_data = b"STK" * 10
        bin_path = journal.save_stock_span_binary(1, dummy_data)
        self.assertTrue(bin_path.is_file())
        loaded = journal.load_stock_span_binary(1)
        self.assertEqual(loaded, dummy_data)

    def test_span_lifecycle_success(self):
        journal = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        stock = b"\x00" * 32
        patched = bytearray(stock)
        patched[0] = 0x01
        patched[16] = 0xBB
        patched = bytes(patched)

        journal.record_span_prepared(1, self.span1, stock, patched)
        meta = journal.read_meta()
        self.assertEqual(meta["status"], JournalStatus.IN_PROGRESS.value)

        journal.record_span_writing(1, self.span1)
        journal.record_span_written(1, self.span1, {"return": "ok"})
        # Successful readback matching every byte
        journal.record_span_verified(1, self.span1, patched, patched)
        journal.record_commit()

        final_meta = journal.read_meta()
        self.assertEqual(final_meta["status"], JournalStatus.COMMITTED.value)

    def test_readback_mismatch_raises_and_sets_needs_review(self):
        journal = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        stock = b"\x00" * 32
        patched = b"\x01" * 32
        corrupted_readback = b"\x01" * 31 + b"\x00"

        journal.record_span_prepared(1, self.span1, stock, patched)
        with self.assertRaises(RuntimeError):
            journal.record_span_verified(1, self.span1, corrupted_readback, patched)

        meta = journal.read_meta()
        self.assertEqual(meta["status"], JournalStatus.NEEDS_REVIEW.value)

    def test_find_latest_unresolved(self):
        # Initial committed session
        j1 = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        j1.record_commit()
        self.assertIsNone(RecoveryJournal.find_latest_unresolved(self.base_dir))

        # Interrupted session
        j2 = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        j2.update_status(JournalStatus.NEEDS_REVIEW)
        found = RecoveryJournal.find_latest_unresolved(self.base_dir)
        self.assertIsNotNone(found)
        self.assertEqual(found.read_meta()["session_id"], j2.read_meta()["session_id"])


if __name__ == "__main__":
    unittest.main()
