"""Synthetic local-spool/in-memory transport tests. No network or camera access."""

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from tools.transfer_queue import Capture, MockTransport, QueueError, TransferQueue, TransportError


class FaultTransport(MockTransport):
    def __init__(self, operation, kind="transient", *, after=False, uncertain=False):
        super().__init__()
        self.operation, self.kind = operation, kind
        self.after, self.uncertain = after, uncertain
        self.remaining = 1

    def _fails(self, operation):
        if self.remaining and operation == self.operation:
            self.remaining -= 1
            return True
        return False

    def upload_exclusive(self, path, data):
        if self._fails("upload"):
            if self.after:
                super().upload_exclusive(path, data)
            raise TransportError(self.kind, uncertain=self.uncertain)
        super().upload_exclusive(path, data)

    def rename_exclusive(self, temporary, final):
        if self._fails("rename"):
            if self.after:
                super().rename_exclusive(temporary, final)
            raise TransportError(self.kind, uncertain=self.uncertain)
        super().rename_exclusive(temporary, final)


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.spool = self.root / "spool"
        self.spool.mkdir()
        self.path = self.root / "queue.json"
        self.queue = TransferQueue.create(self.path, self.spool)
        self.addCleanup(lambda: self.queue.close())
        self.capture = Capture("body-test", "session-1", "card-A", "object-1", 1, "DSC00001.JPG", "JPEG")
        self.payload = b"synthetic bytes only\x00\xff"
        self.write("one.bin", self.payload)

    def write(self, name, content):
        path = self.spool / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def enqueue(self):
        return self.queue.enqueue(self.capture, "one.bin")

    def reload(self):
        self.queue.close()
        self.queue = TransferQueue.load(self.path, self.spool)

    def test_100_objects_50_raw_jpeg_groups_are_verified_without_source_loss(self):
        transport = MockTransport()
        expected = {}
        groups = set()
        for index in range(100):
            fmt = "RAW" if index % 2 == 0 else "JPEG"
            sequence = index // 2
            source = f"fixtures/{index:03d}.bin"
            payload = hashlib.sha256(str(index).encode()).digest() * (index + 1)
            self.write(source, payload)
            capture = replace(self.capture, object_id=f"object-{index}", capture_sequence=sequence,
                              filename=f"DSC{sequence:05d}.{'ARW' if fmt == 'RAW' else 'JPG'}",
                              format=fmt, expected_formats=("RAW", "JPEG"))
            identity = self.queue.enqueue(capture, source)
            expected[identity] = (source, payload)
            groups.add(self.queue.entries[identity]["group_id"])
        self.reload()
        for identity, (source, payload) in expected.items():
            self.assertEqual(self.queue.run_one(identity, transport), "committed")
            self.assertEqual(transport.objects[self.queue.paths(identity)[1]], payload)
            self.assertEqual((self.spool / source).read_bytes(), payload)
        self.assertEqual(len(transport.objects), 100)
        self.assertEqual(len([c for c in transport.calls if c[0] == "upload"]), 100)
        self.assertTrue(all(self.queue.group_status(g)["complete"] for g in groups))
        self.reload()
        self.assertTrue(all(e["state"] == "committed" for e in self.queue.entries.values()))

    def test_partial_pair_is_explicit(self):
        capture = replace(self.capture, expected_formats=("RAW", "JPEG"))
        identity = self.queue.enqueue(capture, "one.bin")
        self.queue.run_one(identity, MockTransport())
        self.assertEqual(self.queue.group_status(self.queue.entries[identity]["group_id"]),
                         {"expected": ["JPEG", "RAW"], "committed": ["JPEG"], "complete": False})

    def test_identity_distinguishes_filename_wrap_card_and_session(self):
        ids = {self.enqueue()}
        for capture in (replace(self.capture, capture_sequence=10001), replace(self.capture, card_id="card-B"),
                        replace(self.capture, session_id="session-2")):
            ids.add(self.queue.enqueue(capture, "one.bin"))
        self.assertEqual(len(ids), 4)
        self.assertEqual(len({self.queue.paths(i)[1] for i in ids}), 4)

    def test_duplicate_is_idempotent_but_changed_content_is_refused(self):
        identity = self.enqueue()
        self.assertEqual(self.enqueue(), identity)
        self.assertEqual(len(self.queue.entries), 1)
        self.write("one.bin", b"different")
        with self.assertRaises(QueueError):
            self.enqueue()

    def test_duplicate_group_format_and_changed_pair_expectations_refused(self):
        self.enqueue()
        for capture in (replace(self.capture, object_id="other"),
                        replace(self.capture, object_id="raw", format="RAW", expected_formats=("RAW", "JPEG"))):
            with self.assertRaises(QueueError):
                self.queue.enqueue(capture, "one.bin")

    def test_paths_and_unproved_completion_are_rejected(self):
        for name in ("../x", "/x", "x\\y", "a//b", "a/../b", "x%2fy", "x\r\nSTOR z", "c:/x", "café.JPG", "a."):
            with self.subTest(name=name), self.assertRaises(QueueError):
                self.queue.enqueue(replace(self.capture, filename=name), "one.bin")
        for source in ("../one.bin", "/one.bin", "one.bin\nDELE x"):
            with self.subTest(source=source), self.assertRaises(QueueError):
                self.queue.enqueue(self.capture, source)
        with self.assertRaises(QueueError):
            self.queue.enqueue(replace(self.capture, completion_evidence="size-stable"), "one.bin")
        for root in ("/incoming/../x", "ftp://server/x", "/x\n", "/x/", "/x%2fy"):
            with self.subTest(root=root), self.assertRaises(QueueError):
                TransferQueue.create(self.root / "invalid.json", self.spool, remote_root=root)

    def test_source_changes_or_card_missing_prevent_upload(self):
        identity = self.enqueue()
        self.write("one.bin", b"S" * len(self.payload))
        transport = MockTransport()
        self.assertEqual(self.queue.run_one(identity, transport), "permanent_error")
        self.assertEqual(transport.calls, [])
        other = self.queue.enqueue(replace(self.capture, card_id="card-B"), "one.bin")
        (self.spool / "one.bin").unlink()  # Test fixture removes media, never queue code.
        self.assertEqual(self.queue.run_one(other, transport), "permanent_error")
        self.assertEqual(transport.calls, [])

    def test_retry_is_bounded_scheduled_and_requires_known_no_side_effect(self):
        identity = self.enqueue()
        transport = FaultTransport("upload")
        transport.remaining = 10
        now = 0
        for expected in ("retryable_error", "retryable_error", "permanent_error"):
            self.assertEqual(self.queue.run_one(identity, transport, now=now), expected)
            if expected == "retryable_error":
                attempts = self.queue.entries[identity]["attempts"]
                self.assertEqual(self.queue.run_one(identity, transport, now=now), expected)
                self.assertEqual(self.queue.entries[identity]["attempts"], attempts)
                now = self.queue.entries[identity]["next_attempt"]
        self.assertEqual(self.queue.entries[identity]["attempts"], 3)
        with self.assertRaises(QueueError):
            self.queue.run_one(identity, transport, now=100)

    def test_upload_disconnect_requires_read_only_reconciliation_before_finalizing(self):
        identity = self.enqueue()
        transport = FaultTransport("upload", after=True, uncertain=True)
        self.assertEqual(self.queue.run_one(identity, transport), "needs_review")
        with self.assertRaises(QueueError):
            self.queue.run_one(identity, transport)
        before = list(transport.calls)
        self.assertEqual(self.queue.reconcile(identity, transport), "ready_to_finalize")
        self.assertTrue(all(c[0] == "inspect" for c in transport.calls[len(before):]))
        self.reload()
        self.assertEqual(self.queue.run_one(identity, transport), "committed")
        self.assertEqual(len([c for c in transport.calls if c[0] == "upload"]), 1)

    def test_rename_disconnect_is_reconciled_without_second_upload_or_rename(self):
        identity = self.enqueue()
        transport = FaultTransport("rename", after=True, uncertain=True)
        self.assertEqual(self.queue.run_one(identity, transport), "needs_review")
        self.reload()
        self.assertEqual(self.queue.reconcile(identity, transport), "committed")
        self.assertEqual(len([c for c in transport.calls if c[0] == "upload"]), 1)
        self.assertEqual(len([c for c in transport.calls if c[0] == "rename"]), 1)

    def test_uncertain_absence_must_be_observed_before_retry(self):
        identity = self.enqueue()
        transport = FaultTransport("upload", uncertain=True)
        self.assertEqual(self.queue.run_one(identity, transport), "needs_review")
        self.assertEqual(self.queue.reconcile(identity, transport), "ready")
        self.assertEqual(self.queue.run_one(identity, transport), "committed")
        self.assertEqual(self.queue.entries[identity]["attempts"], 2)

    def test_finalization_attempts_are_bounded_too(self):
        identity = self.enqueue()
        transport = FaultTransport("rename", uncertain=True)
        transport.remaining = 20
        for attempt in range(3):
            self.assertEqual(self.queue.run_one(identity, transport), "needs_review")
            self.assertEqual(self.queue.reconcile(identity, transport), "ready_to_finalize")
        self.assertEqual(self.queue.run_one(identity, transport), "permanent_error")
        self.assertEqual(self.queue.entries[identity]["attempts"], 3)
        self.assertEqual(len([c for c in transport.calls if c[0] == "upload"]), 1)

    def test_size_only_and_same_size_wrong_hash_are_not_verification(self):
        identity = self.enqueue()
        transport = MockTransport()
        temporary, final = self.queue.paths(identity)
        transport.objects[final] = b"X" * len(self.payload)
        self.assertEqual(self.queue.run_one(identity, transport), "needs_review")
        self.assertEqual(transport.objects[final], b"X" * len(self.payload))
        self.assertEqual(self.queue.reconcile(identity, transport), "needs_review")
        transport.objects[final] = self.payload
        transport.hash_available = False
        self.assertEqual(self.queue.reconcile(identity, transport), "needs_review")
        self.assertNotIn(temporary, transport.objects)

    def test_partial_temporary_is_preserved_for_review_without_overwrite(self):
        identity = self.enqueue()
        transport = MockTransport()
        temporary, _ = self.queue.paths(identity)
        transport.objects[temporary] = b"partial"
        self.assertEqual(self.queue.run_one(identity, transport), "needs_review")
        self.assertEqual(self.queue.reconcile(identity, transport), "needs_review")
        self.assertEqual(transport.objects[temporary], b"partial")
        self.assertFalse(any(c[0] in {"upload", "rename"} for c in transport.calls))

    def test_existing_final_complete_hash_can_be_adopted_without_overwrite(self):
        identity = self.enqueue()
        transport = MockTransport()
        transport.objects[self.queue.paths(identity)[1]] = self.payload
        self.assertEqual(self.queue.run_one(identity, transport), "committed")
        self.assertFalse(any(c[0] in {"upload", "rename"} for c in transport.calls))

    def test_upload_success_without_complete_hash_never_finalizes(self):
        identity = self.enqueue()
        transport = MockTransport()
        transport.hash_available = False
        self.assertEqual(self.queue.run_one(identity, transport), "needs_review")
        temporary, final = self.queue.paths(identity)
        self.assertEqual(transport.objects[temporary], self.payload)
        self.assertNotIn(final, transport.objects)
        self.assertFalse(any(c[0] == "rename" for c in transport.calls))

    def test_final_hash_corruption_is_reviewed_and_unexpected_adapter_text_is_not_saved(self):
        class CorruptingTransport(MockTransport):
            def rename_exclusive(self, temporary, final):
                super().rename_exclusive(temporary, final)
                self.objects[final] = b"X" * len(self.objects[final])

        identity = self.enqueue()
        transport = CorruptingTransport()
        self.assertEqual(self.queue.run_one(identity, transport), "needs_review")
        self.assertEqual(self.queue.entries[identity]["reason"], "final_hash_not_verified")
        self.assertIsNone(self.queue.entries[identity]["verified_final_sha256"])

        class UnexpectedTransport(MockTransport):
            def upload_exclusive(self, path, data):
                super().upload_exclusive(path, data)
                raise QueueError("password=synthetic-secret /private/source")

        other = self.queue.enqueue(replace(self.capture, capture_sequence=2), "one.bin")
        self.assertEqual(self.queue.run_one(other, UnexpectedTransport()), "needs_review")
        self.assertNotIn("synthetic-secret", self.path.read_text())
        self.assertNotIn("/private/source", self.path.read_text())

    def test_auth_permission_quota_tls_failures_are_terminal_without_secret_text(self):
        for kind in ("auth", "permission", "quota", "tls"):
            with self.subTest(kind=kind):
                identity = self.queue.enqueue(replace(self.capture, capture_sequence=len(self.queue.entries)), "one.bin")
                transport = FaultTransport("upload", kind)
                self.assertEqual(self.queue.run_one(identity, transport), "permanent_error")
                self.assertEqual(self.queue.entries[identity]["reason"], kind)
        identity = self.queue.enqueue(replace(self.capture, capture_sequence=100), "one.bin")
        transport = MockTransport()
        transport.verified_tls = False
        self.assertEqual(self.queue.run_one(identity, transport), "permanent_error")
        self.assertEqual(transport.calls, [])
        self.assertNotIn("password", self.path.read_text())

    def test_cancellation_before_and_after_upload_preserves_sources_and_remote_temporary(self):
        identity = self.enqueue()
        transport = MockTransport()
        self.assertEqual(self.queue.run_one(identity, transport, cancelled=lambda: True), "cancelled")
        self.assertEqual(transport.calls, [])
        identity = self.queue.enqueue(replace(self.capture, capture_sequence=2), "one.bin")
        calls = iter((False, True))
        self.assertEqual(self.queue.run_one(identity, transport, cancelled=lambda: next(calls)), "needs_review")
        temporary, final = self.queue.paths(identity)
        self.assertEqual(transport.objects[temporary], self.payload)
        self.assertNotIn(final, transport.objects)
        self.assertEqual((self.spool / "one.bin").read_bytes(), self.payload)

    def test_each_inflight_reload_enters_review_and_does_not_retry_implicitly(self):
        identity = self.enqueue()
        for state in ("transferring", "verification_pending", "finalizing"):
            with self.subTest(state=state):
                self.queue.entries[identity]["state"] = state
                self.queue.entries[identity]["attempts"] = 1
                self.queue._persist()
                self.reload()
                self.assertEqual(self.queue.entries[identity]["state"], "needs_review")
                with self.assertRaises(QueueError):
                    self.queue.run_one(identity, MockTransport())

    def test_interrupted_persistence_keeps_last_complete_json_and_stops_upload(self):
        from unittest.mock import patch
        identity = self.enqueue()
        previous = self.path.read_bytes()
        transport = MockTransport()
        with patch("tools.transfer_queue.os.replace", side_effect=OSError("synthetic disk failure")):
            with self.assertRaises(OSError):
                self.queue.run_one(identity, transport)
        self.assertEqual(self.path.read_bytes(), previous)
        self.assertEqual(transport.calls, [])
        self.assertFalse(list(self.root.glob("*.tmp")))

    def test_commit_persistence_failure_after_remote_success_remains_reconcilable(self):
        from unittest.mock import patch
        identity = self.enqueue()
        transport = MockTransport()
        original = self.queue._persist
        failures = [1]

        def fail_commit_once():
            if self.queue.entries[identity]["state"] == "committed" and failures[0]:
                failures[0] -= 1
                raise OSError("synthetic commit persistence failure")
            original()

        with patch.object(self.queue, "_persist", side_effect=fail_commit_once):
            self.assertEqual(self.queue.run_one(identity, transport), "needs_review")
        self.assertIsNone(self.queue.entries[identity]["verified_final_sha256"])
        self.reload()
        self.assertEqual(self.queue.reconcile(identity, transport), "committed")
        self.assertEqual(len([c for c in transport.calls if c[0] == "upload"]), 1)
        self.queue.entries[identity]["verified_final_sha256"] = None
        self.queue._state(self.queue.entries[identity], "needs_review")
        failures[0] = 1
        original = self.queue._persist
        with patch.object(self.queue, "_persist", side_effect=fail_commit_once):
            self.assertEqual(self.queue.reconcile(identity, transport), "needs_review")
        self.assertIsNone(self.queue.entries[identity]["verified_final_sha256"])
        self.assertEqual(self.queue.reconcile(identity, transport), "committed")

    def test_duplicate_json_keys_and_malformed_durable_state_are_refused(self):
        self.enqueue()
        self.queue.close()
        baseline = json.loads(self.path.read_text())
        mutations = (
            lambda d: d.update(remote_root="/incoming/../../escape"),
            lambda d: d["entries"][0].update(source="../secret"),
            lambda d: d["entries"][0].update(state="committed"),
            lambda d: d["entries"][0].update(id="0" * 64),
            lambda d: d["entries"][0].update(attempts=True),
            lambda d: d["entries"].append(d["entries"][0]),
            lambda d: d.update(password="do-not-store"),
            lambda d: d["entries"][0].update(next_attempt=float("nan")),
            lambda d: d["entries"][0].update(state=[]),
            lambda d: d["entries"][0].update(verified_final_sha256=[]),
            lambda d: d["entries"][0]["capture"].pop("completion_evidence"),
        )
        for mutate in mutations:
            data = json.loads(json.dumps(baseline))
            mutate(data)
            self.path.write_text(json.dumps(data), encoding="utf-8")
            with self.subTest(mutation=mutate), self.assertRaises(QueueError):
                TransferQueue.load(self.path, self.spool)
            self.assertFalse(self.path.with_name("queue.json.lock").exists())
        self.path.write_text('{"schema_version":1,"schema_version":1}', encoding="utf-8")
        with self.assertRaises(QueueError):
            TransferQueue.load(self.path, self.spool)

    def test_existing_state_and_concurrent_owner_are_refused(self):
        with self.assertRaises(QueueError):
            TransferQueue.create(self.path, self.spool)
        with self.assertRaises(FileExistsError):
            TransferQueue.load(self.path, self.spool)

    def test_creator_rechecks_existing_state_after_acquiring_lease(self):
        from unittest.mock import patch
        alternate = self.root / "raced.json"
        retained = b"synthetic state from another completed creator"
        original = TransferQueue.__init__

        def racing_init(queue, state_path, spool):
            original(queue, state_path, spool)
            alternate.write_bytes(retained)

        with patch.object(TransferQueue, "__init__", new=racing_init):
            with self.assertRaises(QueueError):
                TransferQueue.create(alternate, self.spool)
        self.assertEqual(alternate.read_bytes(), retained)
        self.assertFalse(alternate.with_name("raced.json.lock").exists())


if __name__ == "__main__":
    unittest.main()
