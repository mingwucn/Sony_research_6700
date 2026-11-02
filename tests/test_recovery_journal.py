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
        j1 = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        j1.record_commit()
        self.assertIsNone(RecoveryJournal.find_latest_unresolved(self.base_dir))

        j2 = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        j2.update_status(JournalStatus.NEEDS_REVIEW)
        found = RecoveryJournal.find_latest_unresolved(self.base_dir)
        self.assertIsNotNone(found)
        self.assertEqual(found.read_meta()["session_id"], j2.read_meta()["session_id"])

    def test_unresolved_lifecycle_includes_initialized_and_reconciled(self):
        for status in (
            JournalStatus.INITIALIZED,
            JournalStatus.IN_PROGRESS,
            JournalStatus.NEEDS_REVIEW,
            JournalStatus.RECONCILED,
        ):
            with self.subTest(status=status):
                base = self.base_dir / status.value
                journal = RecoveryJournal.create(base, "apply", [self.span1])
                journal.update_status(status)
                self.assertIsNotNone(RecoveryJournal.find_latest_unresolved(base))

    def test_terminal_lifecycle_states_are_resolved(self):
        for status in (JournalStatus.COMMITTED, JournalStatus.REVERTED):
            with self.subTest(status=status):
                base = self.base_dir / status.value
                journal = RecoveryJournal.create(base, "apply", [self.span1])
                journal.update_status(status)
                self.assertIsNone(RecoveryJournal.find_latest_unresolved(base))

    def test_target_span_binary_roundtrip(self):
        journal = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        journal.save_target_span_binary(1, b"TARGET")
        self.assertEqual(journal.load_target_span_binary(1), b"TARGET")

    def test_damaged_or_unknown_metadata_fails_closed(self):
        for index, content in enumerate(("{broken", "[]", json.dumps({"status": "UNRECOGNIZED"}))):
            with self.subTest(content=content):
                base = self.base_dir / str(index)
                journal = RecoveryJournal.create(base, "apply", [self.span1])
                journal.meta_file.write_text(content, encoding="utf-8")
                self.assertIsNotNone(RecoveryJournal.find_latest_unresolved(base))

    def test_session_ids_do_not_collide(self):
        first = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        second = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        self.assertNotEqual(first.session_dir, second.session_dir)

    def test_prepared_snapshots_are_idempotent_and_immutable(self):
        journal = RecoveryJournal.create(self.base_dir, "apply", [self.span1])
        stock = bytes(self.span1.length)
        target = b"\x01" + bytes(self.span1.length - 1)
        journal.record_span_prepared(1, self.span1, stock, target)
        journal.record_span_prepared(1, self.span1, stock, target)
        self.assertEqual(journal.load_stock_span_binary(1), stock)
        with self.assertRaisesRegex(RuntimeError, "拒绝覆盖"):
            journal.record_span_prepared(1, self.span1, b"\x02" + bytes(self.span1.length - 1), target)


if __name__ == "__main__":
    unittest.main()
