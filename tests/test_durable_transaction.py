"""Synthetic durable-journal and real subprocess ownership/restart tests.

Only invented local files are changed. No camera, socket, upstream code or
third-party package is used. Child interpreters import this authored tree.
"""

from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from tools import durable_transaction as durable
from tools.transaction_model import Operation


ROOT = Path(__file__).resolve().parents[1]
INITIAL = {"object-a": b"AAAA-0", "object-b": b"BBBB-0", "unselected": b"KEEP!!"}
OPERATIONS = (
    Operation("op-a", "object-a", b"AAAA-0", b"AAAA-1"),
    Operation("op-b", "object-b", b"BBBB-0", b"BBBB-1"),
)


def after(count):
    result = dict(INITIAL)
    for operation in OPERATIONS[:count]:
        result[operation.component] = operation.after
    return result


def encode_history(records):
    """Rehash an invented history to exercise semantic checks beyond hashes."""
    previous = "0" * 64
    lines = []
    for sequence, original in enumerate(records, 1):
        record = dict(original, sequence=sequence, previous_sha256=previous)
        record.pop("sha256", None)
        canonical = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        previous = hashlib.sha256(canonical).hexdigest()
        record["sha256"] = previous
        lines.append(json.dumps(record, sort_keys=True, separators=(",", ":")).encode() + b"\n")
    return b"".join(lines)


CHILD = r"""
import os
from pathlib import Path
import sys
sys.path.insert(0, sys.argv[1])
from tools.durable_transaction import DurableTransaction, OwnershipError
from tools.transaction_model import Operation
directory = Path(sys.argv[2])
mode = sys.argv[3]
initial = {'object-a': b'AAAA-0', 'object-b': b'BBBB-0', 'unselected': b'KEEP!!'}
operations = (Operation('op-a', 'object-a', b'AAAA-0', b'AAAA-1'),
              Operation('op-b', 'object-b', b'BBBB-0', b'BBBB-1'))
if mode == 'compete':
    try:
        candidate = DurableTransaction.create(directory / 'other.jsonl',
            directory / 'owner.lock', 'session-other', initial, operations)
    except OwnershipError:
        print('OWNERSHIP_REFUSED', flush=True)
        sys.exit(0)
    candidate.close()
    sys.exit(90)
transaction = DurableTransaction.create(directory / 'journal.jsonl',
    directory / 'owner.lock', 'session-1', initial, operations)
def observe():
    return {name: (directory / name).read_bytes() for name in initial}
def apply(operation):
    with (directory / operation.component).open('wb') as stream:
        stream.write(operation.after)
        stream.flush()
        os.fsync(stream.fileno())
operation = transaction.prepare_next(observe())
if mode == 'prepared':
    os._exit(23)
apply(operation)
if mode == 'applied':
    os._exit(23)
transaction.record_result('confirmed', observe())
if mode == 'confirmed':
    os._exit(23)
operation = transaction.prepare_next(observe())
apply(operation)
if mode == 'second-applied':
    os._exit(23)
transaction.record_result('confirmed', observe())
os._exit(23)
"""


class DurableTransactionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)
        self.counter = 0

    @contextmanager
    def transaction(self, *, directory=None, session="session-1", initial=None, operations=None):
        directory = directory or self.directory
        transaction = durable.DurableTransaction.create(
            directory / "journal.jsonl", directory / "owner.lock", session,
            INITIAL if initial is None else initial,
            OPERATIONS if operations is None else operations)
        try:
            yield transaction
        finally:
            transaction.close()

    def new_directory(self):
        self.counter += 1
        directory = self.directory / str(self.counter)
        directory.mkdir()
        return directory

    def reopen(self, directory=None, **changes):
        directory = directory or self.directory
        arguments = dict(journal_path=directory / "journal.jsonl",
                         lock_path=directory / "owner.lock", session_id="session-1",
                         initial_objects=INITIAL, operations=OPERATIONS)
        arguments.update(changes)
        return durable.DurableTransaction.reopen(**arguments)

    def assert_poisoned(self, transaction, directory=None):
        directory = directory or self.directory
        self.assertEqual(transaction.state, "needs_review")
        self.assertFalse(transaction.device_eligible)
        before = (directory / "journal.jsonl").read_bytes()
        actions = (
            lambda: transaction.prepare_next(INITIAL),
            lambda: transaction.record_result("confirmed", after(1)),
            transaction.interrupt_boundary,
            lambda: transaction.reconcile(INITIAL, "evidence-1"),
            transaction.resume,
        )
        for action in actions:
            with self.subTest(action=action):
                with self.assertRaises(durable.JournalError):
                    action()
                self.assertEqual((directory / "journal.jsonl").read_bytes(), before)

    def test_prepared_is_visible_and_synced_before_operation_returns(self):
        source = dict(INITIAL)
        with self.transaction(initial=source) as transaction:
            real_fsync = durable.os.fsync
            events_at_sync = []

            def observe_sync(descriptor):
                records = [json.loads(line) for line in
                           (self.directory / "journal.jsonl").read_bytes().splitlines()]
                events_at_sync.append(records[-1]["event"])
                real_fsync(descriptor)

            with patch.object(durable.os, "fsync", side_effect=observe_sync):
                returned = transaction.prepare_next(source)
            self.assertEqual(returned, OPERATIONS[0])
            self.assertIn("prepared", events_at_sync)
            self.assertEqual(source, INITIAL)
            self.assertFalse(transaction.device_eligible)
            transaction.record_result("confirmed", after(1))
            self.assertEqual(source, INITIAL, "journal must not execute fixture mutation")
            self.assertEqual(transaction.completed_operations, 1)

    def test_fsync_failure_returns_no_operation_and_poisons_every_progression(self):
        with self.transaction() as transaction:
            with patch.object(durable.os, "fsync", side_effect=OSError("synthetic sync failure")):
                with self.assertRaises(durable.PersistenceError):
                    transaction.prepare_next(INITIAL)
            self.assert_poisoned(transaction)

    def test_partial_append_preserves_evidence_and_poisons_handle(self):
        with self.transaction() as transaction:
            before = (self.directory / "journal.jsonl").read_bytes()

            def fail_after_prefix(stream, data):
                stream.write(data[:max(1, len(data) // 2)])
                stream.flush()
                raise OSError("synthetic partial append")

            with patch.object(durable, "_write_all", side_effect=fail_after_prefix):
                with self.assertRaises(durable.PersistenceError):
                    transaction.prepare_next(INITIAL)
            damaged = (self.directory / "journal.jsonl").read_bytes()
            self.assertTrue(damaged.startswith(before))
            self.assertGreater(len(damaged), len(before))
            self.assert_poisoned(transaction)
        with self.assertRaises(durable.JournalError):
            self.reopen()
        self.assertEqual((self.directory / "journal.jsonl").read_bytes(), damaged)

    def test_low_level_short_or_none_write_is_never_retried(self):
        from unittest.mock import Mock
        for result in (None, 0, 2):
            with self.subTest(result=result):
                stream = Mock()
                stream.write.return_value = result
                with self.assertRaises(OSError):
                    durable._write_all(stream, b"invented-record")
                stream.write.assert_called_once_with(b"invented-record")

    def test_failed_result_persistence_cannot_advance_or_resume(self):
        with self.transaction() as transaction:
            transaction.prepare_next(INITIAL)
            with patch.object(durable.os, "fsync", side_effect=OSError("synthetic result failure")):
                with self.assertRaises(durable.PersistenceError):
                    transaction.record_result("confirmed", after(1))
            self.assert_poisoned(transaction)

    def test_surviving_record_after_fsync_error_still_requires_reopen_review(self):
        # A mocked fsync error leaves a readable line here; this is not a
        # guarantee that those bytes survive an actual storage or power fault.
        for boundary, observation, classification, completed in (
                ("prepared", INITIAL, "not_applied", 0),
                ("confirmed", after(1), "confirmed_boundary", 1)):
            with self.subTest(boundary=boundary):
                directory = self.new_directory()
                with self.transaction(directory=directory) as transaction:
                    if boundary == "confirmed":
                        transaction.prepare_next(INITIAL)
                    with patch.object(durable.os, "fsync", side_effect=OSError("synthetic sync failure")):
                        with self.assertRaises(durable.PersistenceError):
                            if boundary == "prepared":
                                transaction.prepare_next(INITIAL)
                            else:
                                transaction.record_result("confirmed", observation)
                    self.assertEqual(transaction.state, "needs_review")
                    failed_bytes = (directory / "journal.jsonl").read_bytes()
                    with self.assertRaises(durable.JournalError):
                        transaction.resume()
                reopened = self.reopen(directory)
                try:
                    self.assertEqual(reopened.state, "needs_review")
                    self.assertTrue((directory / "journal.jsonl").read_bytes().startswith(failed_bytes))
                    with self.assertRaises(durable.JournalError):
                        reopened.prepare_next(observation)
                    with self.assertRaises(durable.JournalError):
                        reopened.resume()
                    self.assertEqual(reopened.reconcile(observation, "evidence-1"), classification)
                    self.assertEqual(reopened.state, "reconciled")
                    self.assertEqual(reopened.completed_operations, completed)
                    reopened.resume()
                    self.assertEqual(reopened.prepare_next(observation), OPERATIONS[completed])
                    self.assertFalse(reopened.device_eligible)
                finally:
                    reopened.close()

    def test_reconciliation_requires_complete_observation_and_explicit_resume(self):
        with self.transaction() as transaction:
            transaction.prepare_next(INITIAL)
            transaction.record_result("timeout_after", after(1))
            self.assertEqual(transaction.state, "needs_review")
            for observation in ({"object-a": OPERATIONS[0].after}, dict(after(1), extra=b"x")):
                with self.assertRaises(durable.JournalError):
                    transaction.reconcile(observation, "evidence-1")
            self.assertEqual(transaction.reconcile(after(1), "evidence-1"), "applied")
            self.assertEqual(transaction.state, "reconciled")
            self.assertEqual(transaction.completed_operations, 1)
            with self.assertRaises(durable.JournalError):
                transaction.prepare_next(after(1))
            transaction.resume()
            self.assertEqual(transaction.prepare_next(after(1)), OPERATIONS[1])

    def test_confirmed_nonapplication_allows_only_a_separate_prepared_attempt(self):
        with self.transaction() as transaction:
            transaction.prepare_next(INITIAL)
            transaction.record_result("timeout_before", INITIAL)
            with self.assertRaises(durable.JournalError):
                transaction.prepare_next(INITIAL)
            self.assertEqual(transaction.reconcile(INITIAL, "evidence-1"), "not_applied")
            self.assertEqual(transaction.completed_operations, 0)
            with self.assertRaises(durable.JournalError):
                transaction.prepare_next(INITIAL)
            transaction.resume()
            self.assertEqual(transaction.prepare_next(INITIAL), OPERATIONS[0])
            prepared_facts = [record["facts"] for record in transaction.journal
                              if record["event"] == "prepared"]
            self.assertEqual([facts["attempt"] for facts in prepared_facts], [1, 2])
            self.assertTrue(all(facts["category"] == "synthetic_mutation" for facts in prepared_facts))

    def test_partial_or_unselected_changes_remain_unresolved_without_rollback(self):
        for observation in (dict(INITIAL, **{"object-a": b"AAXX-0"}),
                            dict(after(1), unselected=b"CHANGED")):
            with self.subTest(observation=observation):
                directory = self.new_directory()
                with self.transaction(directory=directory) as transaction:
                    transaction.prepare_next(INITIAL)
                    transaction.record_result("partial", observation)
                    preserved = dict(observation)
                    self.assertEqual(transaction.reconcile(observation, "evidence-1"),
                                     "partial_or_mixed_state")
                    self.assertEqual(transaction.state, "needs_review")
                    with self.assertRaises(durable.JournalError):
                        transaction.resume()
                    self.assertEqual(observation, preserved)
                    self.assertEqual(transaction.completed_operations, 0)

    def test_fresh_full_source_map_required_before_preparation(self):
        invalid = ({"object-a": INITIAL["object-a"]}, dict(INITIAL, extra=b"extra"),
                   dict(INITIAL, unselected=b"DIFF!!"), after(1))
        for observation in invalid:
            with self.subTest(observation=observation):
                with self.transaction(directory=self.new_directory()) as transaction:
                    with self.assertRaises(durable.JournalError):
                        transaction.prepare_next(observation)
                    self.assertNotEqual(transaction.state, "prepared")

    def test_false_confirmed_claim_cannot_accept_incomplete_or_mixed_source(self):
        for observation in (INITIAL, {"object-a": OPERATIONS[0].after},
                            dict(after(1), unselected=b"DIFF!!")):
            with self.subTest(observation=observation):
                with self.transaction(directory=self.new_directory()) as transaction:
                    transaction.prepare_next(INITIAL)
                    try:
                        transaction.record_result("confirmed", observation)
                    except durable.JournalError:
                        pass
                    self.assertEqual(transaction.state, "needs_review")
                    self.assertEqual(transaction.completed_operations, 0)

    def test_detached_journal_records_cannot_rewrite_history(self):
        with self.transaction() as transaction:
            snapshot = transaction.journal
            self.assertIsInstance(snapshot, tuple)
            original = (self.directory / "journal.jsonl").read_bytes()
            snapshot[0]["event"] = "invented"
            snapshot[0]["facts"]["device_eligible"] = True
            self.assertEqual(transaction.journal[0]["event"], "created")
            self.assertFalse(transaction.journal[0]["facts"]["device_eligible"])
            self.assertEqual((self.directory / "journal.jsonl").read_bytes(), original)

    def test_existing_journal_is_never_overwritten(self):
        journal = self.directory / "journal.jsonl"
        journal.write_bytes(b"existing evidence\n")
        with self.assertRaises(durable.JournalError):
            with self.transaction():
                self.fail("existing journal accepted")
        self.assertEqual(journal.read_bytes(), b"existing evidence\n")

    def test_reopen_rejects_wrong_source_plan_session_and_lock_without_append(self):
        with self.transaction():
            pass
        original = (self.directory / "journal.jsonl").read_bytes()
        variants = (
            {"initial_objects": dict(INITIAL, unselected=b"DIFF!!")},
            {"operations": (Operation("op-a", "object-a", b"AAAA-0", b"AAAA-2"), OPERATIONS[1])},
            {"operations": tuple(reversed(OPERATIONS))},
            {"session_id": "session-other"},
            {"lock_path": self.directory / "unrelated.lock"},
        )
        for changes in variants:
            with self.subTest(changes=changes):
                with self.assertRaises(durable.JournalError):
                    self.reopen(**changes)
                self.assertEqual((self.directory / "journal.jsonl").read_bytes(), original)

    def test_wrong_or_unsupported_plan_is_refused_before_journal_creation(self):
        invalid = (
            ({}, OPERATIONS),
            (INITIAL, (Operation("op-a", "object-a", b"WRONG!", b"AAAA-1"),)),
            (INITIAL, (OPERATIONS[0], OPERATIONS[0])),
            (INITIAL, (Operation("op-a", "object-a", b"AAAA-0", b"A", "synthetic_mutation"),)),
            (INITIAL, (Operation("op-a", "object-a", b"AAAA-0", b"AAAA-1", "device_write"),)),
        )
        for source, operations in invalid:
            with self.subTest(source=source, operations=operations):
                directory = self.new_directory()
                with self.assertRaises(durable.JournalError):
                    with self.transaction(directory=directory, initial=source, operations=operations):
                        self.fail("unsupported plan accepted")
                self.assertFalse((directory / "journal.jsonl").exists())

    def test_initial_plan_limits_refuse_before_creating_a_journal(self):
        limits = (
            ("MAX_COMPONENTS", len(INITIAL) - 1),
            ("MAX_OPERATIONS", len(OPERATIONS) - 1),
            ("MAX_OBJECT_BYTES", max(map(len, INITIAL.values())) - 1),
            ("MAX_TOTAL_OBJECT_BYTES", sum(map(len, INITIAL.values())) - 1),
        )
        for name, limit in limits:
            with self.subTest(limit=name):
                directory = self.new_directory()
                with patch.object(durable, name, limit):
                    with self.assertRaises(durable.JournalError):
                        with self.transaction(directory=directory):
                            self.fail("oversized initial plan accepted")
                self.assertFalse((directory / "journal.jsonl").exists())

    def test_existing_history_limits_refuse_reopen_without_changing_evidence(self):
        with self.transaction() as transaction:
            transaction.prepare_next(INITIAL)
            transaction.record_result("confirmed", after(1))
        journal = self.directory / "journal.jsonl"
        evidence = journal.read_bytes()
        records = evidence.splitlines(keepends=True)
        limits = (("MAX_RECORDS", len(records) - 1),
                  ("MAX_RECORD_BYTES", max(map(len, records)) - 1),
                  ("MAX_JOURNAL_BYTES", len(evidence) - 1))
        for name, limit in limits:
            with self.subTest(limit=name):
                with patch.object(durable, name, limit):
                    with self.assertRaises(durable.JournalError):
                        self.reopen()
                self.assertEqual(journal.read_bytes(), evidence)

    def test_append_limits_preserve_bytes_and_stop_every_handle_transition(self):
        for name in ("MAX_RECORDS", "MAX_RECORD_BYTES", "MAX_JOURNAL_BYTES"):
            with self.subTest(limit=name):
                directory = self.new_directory()
                with self.transaction(directory=directory) as transaction:
                    journal = directory / "journal.jsonl"
                    evidence = journal.read_bytes()
                    limit = len(evidence) if name == "MAX_JOURNAL_BYTES" else 1
                    with patch.object(durable, name, limit):
                        with self.assertRaises(durable.PersistenceError):
                            transaction.prepare_next(INITIAL)
                    self.assertEqual(journal.read_bytes(), evidence)
                    self.assert_poisoned(transaction, directory)

    def test_actual_hardlinked_journal_is_refused_without_changing_either_name(self):
        with self.transaction():
            pass
        journal = self.directory / "journal.jsonl"
        linked = self.directory / "journal-alias.jsonl"
        evidence = journal.read_bytes()
        try:
            os.link(journal, linked)
        except (OSError, NotImplementedError) as error:
            self.skipTest("actual hard-link fixture unavailable on this local filesystem: "
                          + type(error).__name__)
        self.assertGreaterEqual(journal.stat().st_nlink, 2)
        for candidate in (journal, linked):
            with self.subTest(path=candidate.name):
                with self.assertRaises(durable.JournalError):
                    self.reopen(journal_path=candidate)
                self.assertEqual(journal.read_bytes(), evidence)
                self.assertEqual(linked.read_bytes(), evidence)

    @unittest.skipUnless(os.name == "nt", "Windows UNC/device/ADS syntax policy applies only on Windows")
    def test_unc_device_and_ads_paths_are_rejected_before_filesystem_observation(self):
        unsafe_paths = (r"\\server\share\journal.jsonl", "//server/share/journal.jsonl",
                        r"\\?\C:\journal.jsonl", r"\\.\PhysicalDrive0",
                        r"C:\journal.jsonl:stream")
        for name in unsafe_paths:
            with self.subTest(path=name):
                with patch.object(durable.Path, "lstat", side_effect=AssertionError("filesystem reached")):
                    with self.assertRaises(durable.JournalError):
                        durable._safe_path(name)

    def test_corrupt_or_torn_history_refuses_reopen_without_repair(self):
        with self.transaction() as transaction:
            transaction.prepare_next(INITIAL)
            transaction.record_result("confirmed", after(1))
        journal = self.directory / "journal.jsonl"
        good = journal.read_bytes()
        lines = good.splitlines(keepends=True)
        records = [json.loads(line) for line in lines]
        unknown = json.loads(json.dumps(records))
        unknown[1]["event"] = "unrecognized_event"
        eligible = json.loads(json.dumps(records))
        eligible[0]["facts"]["device_eligible"] = True
        variants = {
            "missing-final-newline": good[:-1],
            "torn-last-record": b"".join(lines[:-1]) + lines[-1][:len(lines[-1]) // 2],
            "wrong-record-hash": good.replace(b'"sha256":"', b'"sha256":"0', 1),
            "duplicate-record": lines[0] + lines[1] + lines[1] + b"".join(lines[2:]),
            "reordered-records": lines[0] + lines[2] + lines[1],
            "invalid-utf8": b"\xff" + good,
            "blank-record": lines[0] + b"\n" + b"".join(lines[1:]),
            "duplicate-json-key": b'{"sequence":999,' + lines[0][1:] + b"".join(lines[1:]),
            "unknown-event-valid-hashes": encode_history(unknown),
            "result-without-preparation-valid-hashes": encode_history([records[0], records[2]]),
            "duplicate-confirmation-valid-hashes": encode_history(records + [records[2]]),
            "device-eligible-valid-hashes": encode_history(eligible),
        }
        for field, value in (("schema_version", True), ("schema_version", 1.0),
                             ("synthetic_only", 1), ("device_eligible", 0),
                             ("operation_count", 2.0)):
            forged = json.loads(json.dumps(records))
            forged[0]["facts"][field] = value
            variants[f"header-{field}-{value!r}"] = encode_history(forged)
        for field, value in (("boundary", False), ("boundary", 0.0),
                             ("attempt", True), ("attempt", 1.0),
                             ("category", "device_write")):
            forged = json.loads(json.dumps(records))
            forged[1]["facts"][field] = value
            variants[f"prepared-{field}-{value!r}"] = encode_history(forged)
        for name, damaged in variants.items():
            with self.subTest(corruption=name):
                journal.write_bytes(damaged)
                with self.assertRaises(durable.JournalError):
                    self.reopen()
                self.assertEqual(journal.read_bytes(), damaged)

    def test_live_process_lock_excludes_another_process_and_is_not_unlinked(self):
        with self.transaction():
            lock = self.directory / "owner.lock"
            # Windows byte-range locks also deny another handle reading that byte.
            self.assertTrue(lock.exists())
            child = subprocess.run([sys.executable, "-I", "-S", "-B", "-X", "utf8", "-c", CHILD,
                                    str(ROOT), str(self.directory), "compete"],
                                   capture_output=True, text=True, timeout=15)
            self.assertEqual(child.returncode, 0, child.stderr)
            self.assertEqual(child.stdout.strip(), "OWNERSHIP_REFUSED")
            self.assertFalse((self.directory / "other.jsonl").exists())
            self.assertTrue(lock.exists())
        self.assertTrue(lock.exists())
        recognized_bytes = lock.read_bytes()
        self.assertTrue(recognized_bytes)
        other = durable.DurableTransaction.create(self.directory / "other.jsonl", lock,
                                                   "session-other", INITIAL, OPERATIONS)
        other.close()
        self.assertTrue(lock.exists())
        self.assertEqual(lock.read_bytes(), recognized_bytes)

    @unittest.skipUnless(hasattr(os, "fork"),
                         "POSIX fork inheritance requires Linux/Unix execution; unavailable on Windows")
    def test_forked_handle_cannot_mutate_or_unlock_parent_ownership(self):
        with self.transaction() as transaction:
            read_fd, write_fd = os.pipe()
            child_pid = os.fork()
            if child_pid == 0:
                os.close(read_fd)
                try:
                    refused = False
                    try:
                        transaction.prepare_next(INITIAL)
                    except durable.OwnershipError:
                        refused = True
                    transaction.close()
                    os.write(write_fd, b"REFUSED" if refused else b"UNSAFE")
                    os._exit(0)
                except BaseException:
                    os.write(write_fd, b"CHILD_ERROR")
                    os._exit(1)
            os.close(write_fd)
            try:
                deadline = time.monotonic() + 10
                while True:
                    finished, status = os.waitpid(child_pid, os.WNOHANG)
                    if finished:
                        break
                    if time.monotonic() >= deadline:
                        os.kill(child_pid, signal.SIGKILL)
                        os.waitpid(child_pid, 0)
                        self.fail("fork child did not finish within its bound")
                    time.sleep(0.01)
                self.assertTrue(os.WIFEXITED(status))
                self.assertEqual(os.WEXITSTATUS(status), 0)
                self.assertEqual(os.read(read_fd, 64), b"REFUSED")
                competitor = subprocess.run(
                    [sys.executable, "-I", "-S", "-B", "-X", "utf8", "-c", CHILD,
                     str(ROOT), str(self.directory), "compete"],
                    capture_output=True, text=True, timeout=15)
                self.assertEqual(competitor.returncode, 0, competitor.stderr)
                self.assertEqual(competitor.stdout.strip(), "OWNERSHIP_REFUSED")
                self.assertEqual(transaction.prepare_next(INITIAL), OPERATIONS[0])
            finally:
                os.close(read_fd)

    def test_real_process_crash_boundaries_require_observe_reconcile_and_resume(self):
        cases = (
            ("prepared", 0, "not_applied"),
            ("applied", 1, "applied"),
            ("confirmed", 1, "confirmed_boundary"),
            ("second-applied", 2, "applied"),
            ("complete", 2, "confirmed_boundary"),
        )
        for mode, completed, classification in cases:
            with self.subTest(boundary=mode):
                directory = self.new_directory()
                for name, content in INITIAL.items():
                    (directory / name).write_bytes(content)
                child = subprocess.run([sys.executable, "-I", "-S", "-B", "-X", "utf8", "-c", CHILD,
                                        str(ROOT), str(directory), mode],
                                       capture_output=True, text=True, timeout=15)
                self.assertEqual(child.returncode, 23, child.stderr)
                observation = {name: (directory / name).read_bytes() for name in INITIAL}
                self.assertEqual(observation, after(completed))
                transaction = self.reopen(directory)
                try:
                    self.assertEqual(transaction.state, "needs_review")
                    self.assertFalse(transaction.device_eligible)
                    for action in (lambda: transaction.prepare_next(observation),
                                   lambda: transaction.record_result("confirmed", observation),
                                   transaction.resume):
                        with self.assertRaises(durable.JournalError):
                            action()
                    self.assertEqual(transaction.reconcile(observation, "evidence-1"), classification)
                    self.assertEqual(transaction.state, "reconciled")
                    self.assertEqual(transaction.completed_operations, completed)
                    with self.assertRaises(durable.JournalError):
                        transaction.prepare_next(observation)
                    transaction.resume()
                    if completed < len(OPERATIONS):
                        self.assertEqual(transaction.prepare_next(observation), OPERATIONS[completed])
                        expected_attempt = 2 if mode == "prepared" else 1
                        self.assertEqual(transaction.journal[-1]["facts"]["attempt"], expected_attempt)
                    else:
                        self.assertEqual(transaction.state, "complete")
                        with self.assertRaises(durable.JournalError):
                            transaction.prepare_next(observation)
                    self.assertEqual({name: (directory / name).read_bytes() for name in INITIAL},
                                     observation, "restart/reconcile/resume must not execute fixture writes")
                    self.assertEqual(observation["unselected"], INITIAL["unselected"])
                finally:
                    transaction.close()
                self.assertTrue((directory / "owner.lock").exists())


if __name__ == "__main__":
    unittest.main()
