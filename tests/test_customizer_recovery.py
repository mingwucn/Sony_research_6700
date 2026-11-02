# -*- coding: utf-8 -*-
"""Offline tests for interrupted customizer transaction recovery."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from apps.a6700_customizer import app_backend
from apps.a6700_customizer.app_backend import BackendError, DeviceBackend
from apps.a6700_customizer.recovery_journal import JournalStatus, RecoveryJournal, SpanClassification
from apps.a6700_customizer.targets import APPFW_SIZE, TargetSpan, TargetWindow


class _SessionContext:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc, tb):
        return False


class TestCustomizerRecovery(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.backend = DeviceBackend(state_dir=Path(self.temp_dir.name))
        self.target1 = TargetWindow(0x100, b"\x00", b"\x01", "Target 1", "ftp")
        self.target2 = TargetWindow(0x110, b"\xaa", b"\xbb", "Target 2", "ftp")
        self.target3 = TargetWindow(0x200, b"\x00", b"\x01", "Target 3", "ftp")
        self.span1 = TargetSpan(0x100, 32, [self.target1, self.target2])
        self.span2 = TargetSpan(0x200, 16, [self.target3])
        self.spans = [self.span1, self.span2]
        self.stock1 = bytearray(32)
        self.stock1[16] = 0xAA
        self.stock1 = bytes(self.stock1)
        self.target_data1 = b"\x01" + self.stock1[1:16] + b"\xbb" + self.stock1[17:]
        self.stock2 = bytes(16)
        self.target_data2 = b"\x01" + bytes(15)
        self.device = {
            self.span1.offset: self.stock1,
            self.span2.offset: self.stock2,
        }
        self.writes = []
        self.session = object()

        patches = [
            mock.patch.object(app_backend, "build_target_spans", side_effect=lambda _targets: self.spans),
            mock.patch.object(app_backend.flash, "payload", return_value=b"elf"),
            mock.patch.object(app_backend.flash, "stat", return_value=APPFW_SIZE),
            mock.patch.object(app_backend.flash, "probe", return_value={}),
            mock.patch.object(app_backend.flash, "read_range", side_effect=self._read_range),
            mock.patch.object(app_backend.flash, "write_block", side_effect=self._write_block),
            mock.patch.object(
                app_backend.research, "ServiceSession", side_effect=lambda **_kwargs: _SessionContext(self.session)
            ),
        ]
        for patcher in patches:
            patcher.start()
            self.addCleanup(patcher.stop)

    def _read_range(self, _session, _path, offset, length, _elf):
        return self.device[offset][:length]

    def _write_block(self, _session, _path, offset, data, _elf):
        self.writes.append((offset, data))
        self.device[offset] = data
        return {"ok": True}

    def _create_journal(self, mode="apply", spans=None, prepare=True):
        journal = RecoveryJournal.create(self.backend.journals_dir, mode, spans or self.spans)
        if prepare:
            for index, span in enumerate(spans or self.spans, start=1):
                if span == self.span1:
                    before, after = self.stock1, self.target_data1
                else:
                    before, after = self.stock2, self.target_data2
                if mode == "restore":
                    before, after = after, before
                journal.record_span_prepared(index, span, before, after)
        return journal

    def test_journal_reconstructs_only_recorded_spans(self):
        journal = self._create_journal(spans=[self.span2], prepare=False)
        selected = self.backend._spans_for_journal(journal, self.spans)
        self.assertEqual(selected, [self.span2])

    def test_resume_requires_reconciliation(self):
        journal = self._create_journal()
        with self.assertRaisesRegex(BackendError, "只读对账"):
            self.backend.resume_interrupted_session(journal=journal)
        self.assertEqual(self.writes, [])

    def test_rollback_requires_reconciliation(self):
        journal = self._create_journal()
        with self.assertRaisesRegex(BackendError, "只读对账"):
            self.backend.rollback_interrupted_session(journal=journal)
        self.assertEqual(self.writes, [])

    def test_resume_writes_only_untouched_spans(self):
        self.device[self.span1.offset] = self.target_data1
        journal = self._create_journal()
        summary = self.backend.reconcile_device(journal=journal)
        self.assertTrue(summary["can_resume"])

        result = self.backend.resume_interrupted_session(journal=journal, reconciliation=summary)
        self.assertEqual([offset for offset, _data in self.writes], [self.span2.offset])
        self.assertEqual([item["status"] for item in result], ["already-target", "resumed"])
        self.assertEqual(journal.read_meta()["status"], JournalStatus.COMMITTED.value)
        self.assertEqual(self.device[self.span2.offset], self.target_data2)

    def test_resume_closes_already_target_session_without_writes(self):
        self.device[self.span1.offset] = self.target_data1
        self.device[self.span2.offset] = self.target_data2
        journal = self._create_journal()
        summary = self.backend.reconcile_device(journal=journal)
        result = self.backend.resume_interrupted_session(journal=journal, reconciliation=summary)
        self.assertEqual(self.writes, [])
        self.assertTrue(all(item["status"] == "already-target" for item in result))
        self.assertEqual(journal.read_meta()["status"], JournalStatus.COMMITTED.value)

    def test_resume_refuses_partial_span(self):
        self.device[self.span1.offset] = b"\x55" * self.span1.length
        journal = self._create_journal()
        summary = self.backend.reconcile_device(journal=journal)
        self.assertFalse(summary["can_resume"])
        with self.assertRaisesRegex(BackendError, "禁止续写"):
            self.backend.resume_interrupted_session(journal=journal, reconciliation=summary)
        self.assertEqual(self.writes, [])

    def test_restore_mode_resume_targets_factory_bytes(self):
        self.spans = [self.span1]
        self.device[self.span1.offset] = self.target_data1
        journal = self._create_journal(mode="restore", spans=self.spans)
        summary = self.backend.reconcile_device(journal=journal)
        self.assertEqual(
            summary["findings"][0]["classification"], SpanClassification.UNTOUCHED_STOCK.value
        )
        self.backend.resume_interrupted_session(journal=journal, reconciliation=summary)
        self.assertEqual(self.device[self.span1.offset], self.stock1)

    def test_rollback_skips_untouched_span_with_saved_snapshot(self):
        self.device[self.span2.offset] = self.target_data2
        journal = self._create_journal()
        summary = self.backend.reconcile_device(journal=journal)
        result = self.backend.rollback_interrupted_session(journal=journal, reconciliation=summary)
        self.assertEqual([offset for offset, _data in self.writes], [self.span2.offset])
        self.assertEqual([item["status"] for item in result], ["already-stock", "rolled-back"])
        self.assertEqual(journal.read_meta()["status"], JournalStatus.REVERTED.value)

    def test_rollback_preflights_all_required_stock_snapshots(self):
        self.device[self.span2.offset] = self.target_data2
        journal = self._create_journal()
        summary = self.backend.reconcile_device(journal=journal)
        Path(journal.session_dir / "span_02_stock.bin").unlink()
        with self.assertRaisesRegex(BackendError, "缺少完整写前原始快照"):
            self.backend.rollback_interrupted_session(journal=journal, reconciliation=summary)
        self.assertEqual(self.writes, [])

    def test_stale_scan_stops_before_any_write(self):
        journal = self._create_journal()
        summary = self.backend.reconcile_device(journal=journal)
        self.device[self.span2.offset] = b"\x01" + bytes(14) + b"\x02"
        with self.assertRaisesRegex(BackendError, "对账后发生变化"):
            self.backend.resume_interrupted_session(journal=journal, reconciliation=summary)
        self.assertEqual(self.writes, [])
        self.assertEqual(journal.read_meta()["status"], JournalStatus.NEEDS_REVIEW.value)

    def test_write_failure_locks_session(self):
        journal = self._create_journal()
        summary = self.backend.reconcile_device(journal=journal)
        with mock.patch.object(app_backend.flash, "write_block", side_effect=TimeoutError("timeout")):
            with self.assertRaisesRegex(BackendError, "NEEDS_REVIEW"):
                self.backend.resume_interrupted_session(journal=journal, reconciliation=summary)
        self.assertEqual(journal.read_meta()["status"], JournalStatus.NEEDS_REVIEW.value)

    def test_apply_preflights_all_spans_before_probe(self):
        self.device[self.span2.offset] = b"\x55" * self.span2.length
        with self.assertRaisesRegex(BackendError, "预读校验不匹配"):
            self.backend.apply_features(False, True)
        self.assertEqual(self.writes, [])
        app_backend.flash.probe.assert_not_called()

    def test_restore_rejects_unknown_bytes_before_probe(self):
        self.device[self.span2.offset] = b"\x55" * self.span2.length
        with self.assertRaisesRegex(BackendError, "还原预读校验不匹配"):
            self.backend.restore_factory()
        self.assertEqual(self.writes, [])
        app_backend.flash.probe.assert_not_called()

    def test_probe_is_bounded_by_small_journaled_span(self):
        target = TargetWindow(0x100, bytes.fromhex("f4179f1a"), bytes.fromhex("34008052"), "English", "english")
        self.spans = [TargetSpan(0x100, 4, [target])]
        self.device = {0x100: target.preimage}
        result = self.backend.apply_features(True, False)
        app_backend.flash.probe.assert_called_once_with(self.session, app_backend.TARGET_FILE, 0x100, 4, b"elf")
        self.assertEqual(result[0]["status"], "success")
        self.assertEqual(self.device[0x100], target.patched)

    def test_resume_does_not_fabricate_snapshot_for_pre_patched_span(self):
        self.device[self.span1.offset] = self.target_data1
        journal = self._create_journal(prepare=False)
        summary = self.backend.reconcile_device(journal=journal)
        self.backend.resume_interrupted_session(journal=journal, reconciliation=summary)
        self.assertFalse(Path(journal.session_dir / "span_01_stock.bin").exists())
        self.assertTrue(Path(journal.session_dir / "span_02_stock.bin").is_file())
        app_backend.flash.probe.assert_called_once_with(
            self.session, app_backend.TARGET_FILE, self.span2.offset, self.span2.length, b"elf"
        )

    def test_failed_resume_rolls_back_only_session_touched_spans(self):
        self.device[self.span1.offset] = self.target_data1
        journal = self._create_journal(prepare=False)
        summary = self.backend.reconcile_device(journal=journal)

        def fail_after_write(_session, _path, offset, data, _elf):
            self.device[offset] = data
            raise TimeoutError("uncertain write result")

        with mock.patch.object(app_backend.flash, "write_block", side_effect=fail_after_write):
            with self.assertRaisesRegex(BackendError, "NEEDS_REVIEW"):
                self.backend.resume_interrupted_session(journal=journal, reconciliation=summary)
        reconciled = self.backend.reconcile_device(journal=journal)
        result = self.backend.rollback_interrupted_session(journal=journal, reconciliation=reconciled)
        self.assertEqual([item["status"] for item in result], ["baseline-target", "rolled-back"])
        self.assertEqual(self.device[self.span1.offset], self.target_data1)
        self.assertEqual(self.device[self.span2.offset], self.stock2)
        self.assertEqual(journal.read_meta()["status"], JournalStatus.REVERTED.value)

    def test_same_length_snapshot_corruption_is_rejected(self):
        journal = self._create_journal()
        snapshot = Path(journal.session_dir / "span_01_stock.bin")
        damaged = bytearray(snapshot.read_bytes())
        damaged[0] ^= 0xFF
        snapshot.write_bytes(damaged)
        with self.assertRaisesRegex(BackendError, "快照哈希校验失败"):
            self.backend.reconcile_device(journal=journal)
        self.assertEqual(self.writes, [])


if __name__ == "__main__":
    unittest.main()
