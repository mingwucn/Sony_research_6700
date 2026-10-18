"""Durable synthetic claims and cooperative host ownership, never a device executor.

Only caller-supplied immutable fixture bytes are described. No callback, device
adapter, automatic retry, rollback or filesystem repair exists. Flush/fsync and
advisory OS locks are host observations, not a power-loss or recovery guarantee.
All cooperating users of a resource must select the same stable lock pathname.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from typing import Mapping

from .transaction_model import Operation


MAX_COMPONENTS = 32
MAX_OPERATIONS = 128
MAX_OBJECT_BYTES = 1024 * 1024
MAX_TOTAL_OBJECT_BYTES = 8 * 1024 * 1024
MAX_RECORD_BYTES = 64 * 1024
MAX_JOURNAL_BYTES = 4 * 1024 * 1024
MAX_RECORDS = 4096
_LOCK_MAGIC = b"SYNTHETIC-TRANSACTION-LOCK-v1\n"
_ZERO_HASH = "0" * 64
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}\Z", re.ASCII)
_HASH = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)
_WINDOWS_DEVICE = re.compile(r"(?:CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])(?:\..*)?\Z", re.IGNORECASE)
_UNCERTAIN = frozenset({"timeout_before", "timeout_after", "disconnect_before",
                        "disconnect_after", "partial"})


class JournalError(ValueError):
    """Invalid synthetic plan, journal evidence or requested transition."""


class OwnershipError(JournalError):
    """Cooperative OS ownership cannot be established or retained."""


class PersistenceError(JournalError):
    """Append completion is uncertain; close and explicitly review existing bytes."""


def _identifier(value: object) -> str:
    if (not isinstance(value, str) or not _IDENTIFIER.fullmatch(value)
            or value.lower() in {"unknown", "unverified", "none", "todo"}):
        raise JournalError("explicit bounded synthetic identifier required")
    return value


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _metadata(objects: Mapping[str, bytes]) -> dict:
    return {name: {"size": len(data), "sha256": _sha(data)}
            for name, data in sorted(objects.items())}


def _write_all(stream, data: bytes) -> None:
    """One append attempt; a short write is retained, never completed or repaired."""
    written = stream.write(data)
    if type(written) is not int or written != len(data):
        raise OSError("incomplete journal append")


def _safe_path(value) -> Path:
    try:
        raw = os.fspath(value)
        if not isinstance(raw, str):
            raise JournalError("local journal path must be text")
        if os.name == "nt":
            windows = raw.replace("/", "\\")
            if (windows.startswith("\\\\") or windows.lower().startswith(("\\??\\", "\\device\\"))
                    or any(_WINDOWS_DEVICE.fullmatch(part.rstrip(" ."))
                           for part in windows.split("\\"))
                    or ":" in windows[2:] or any(ord(char) < 32 for char in windows)
                    or any(char in windows for char in '<>"|?*')):
                raise JournalError("only ordinary local paths; no UNC, device or stream paths")
        path = Path(os.path.abspath(raw))
        if len(str(path)) > 4096:
            raise JournalError("path exceeds local journal limit")
        for parent in reversed(path.parents):
            info = parent.lstat()
            if (not stat.S_ISDIR(info.st_mode) or parent.is_symlink()
                    or (hasattr(parent, "is_junction") and parent.is_junction())):
                raise JournalError("journal and lock parents must be ordinary directories")
        try:
            info = path.lstat()
        except FileNotFoundError:
            return path
        if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or path.is_symlink()
                or (hasattr(path, "is_junction") and path.is_junction())):
            raise JournalError("journal and lock must be plain single-link regular files")
        return path
    except (OSError, TypeError, ValueError) as exc:
        if isinstance(exc, JournalError):
            raise
        raise JournalError("invalid local journal or lock path") from exc


def _identity(info) -> tuple:
    return info.st_dev, info.st_ino


def _plain_descriptor(path: Path, stream) -> None:
    named = path.lstat()
    opened = os.fstat(stream.fileno())
    if (not stat.S_ISREG(named.st_mode) or not stat.S_ISREG(opened.st_mode)
            or named.st_nlink != 1 or opened.st_nlink != 1
            or _identity(named) != _identity(opened) or path.is_symlink()):
        raise JournalError("local evidence pathname or identity changed")


class _StableLock:
    def __init__(self, path: Path):
        self.path = path
        self.pid = os.getpid()
        self.stream = None
        self.locked = False
        flags = os.O_RDWR | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        try:
            try:
                descriptor = os.open(path, flags | os.O_CREAT | os.O_EXCL, 0o600)
                created = True
            except FileExistsError:
                descriptor = os.open(path, flags)
                created = False
            try:
                self.stream = os.fdopen(descriptor, "r+b", buffering=0)
            except BaseException:
                os.close(descriptor)
                raise
            _plain_descriptor(path, self.stream)
            if created:
                _write_all(self.stream, _LOCK_MAGIC)
                self.stream.flush()
                os.fsync(self.stream.fileno())
            self.stream.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.stream.fileno(), msvcrt.LK_NBLCK, 1)
            elif os.name == "posix":
                import fcntl
                fcntl.flock(self.stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            else:
                raise OwnershipError("no reviewed OS lock implementation for this host")
            self.locked = True
            self.stream.seek(0)
            if self.stream.read(len(_LOCK_MAGIC) + 1) != _LOCK_MAGIC:
                raise OwnershipError("unrecognized stable lock file; preserve and inspect it")
            self.check()
        except BaseException as exc:
            try:
                self.close()
            except BaseException:
                pass  # Descriptor close was attempted; preserve the original failure.
            if isinstance(exc, (OSError, JournalError)):
                raise OwnershipError("synthetic resource lock unavailable; no takeover attempted") from exc
            raise

    def check(self) -> None:
        if not self.locked or self.stream is None or os.getpid() != self.pid:
            raise OwnershipError("synthetic resource ownership is absent")
        try:
            _plain_descriptor(self.path, self.stream)
        except (OSError, JournalError) as exc:
            raise OwnershipError("stable lock pathname changed") from exc

    def close(self) -> None:
        # Closing the descriptor releases OS ownership even if explicit unlock fails.
        stream, self.stream = self.stream, None
        if stream is None:
            return
        try:
            # A fork child shares the flock open-file description. Its explicit
            # unlock would release the parent's ownership; only close its copy.
            if self.locked and os.getpid() == self.pid:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                elif os.name == "posix":
                    import fcntl
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
        finally:
            self.locked = False
            stream.close()


@dataclass
class _Cursor:
    index: int = 0
    pending: bool = False
    state: str = "ready"
    attempts: dict[str, int] = field(default_factory=dict)


class DurableTransaction:
    """Append-only synthetic journal, bound to a caller-chosen shared OS lock.

    ``create`` is exclusive. Every ``reopen`` requires the complete original plan,
    enters needs_review and demands fresh complete caller claims plus explicit
    reconciliation/resume. ``close`` releases handles at any state, never marks
    uncertain work complete. Crashes release OS ownership, never authorize replay.
    """

    @classmethod
    def create(cls, journal_path, lock_path, session_id: str,
               initial_objects: Mapping[str, bytes], operations: tuple[Operation, ...]):
        return cls(journal_path, lock_path, session_id, initial_objects, operations, new=True)

    @classmethod
    def reopen(cls, journal_path, lock_path, session_id: str,
               initial_objects: Mapping[str, bytes], operations: tuple[Operation, ...]):
        return cls(journal_path, lock_path, session_id, initial_objects, operations, new=False)

    def __init__(self, journal_path, lock_path, session_id, initial_objects, operations, *, new):
        self._closed = False
        self._poisoned = False
        self._stream = None
        self._lock = None
        self._records: list[dict] = []
        self._raw = b""
        self._cursor = _Cursor()
        self._session_id = _identifier(session_id)
        if not isinstance(initial_objects, Mapping) or not 1 <= len(initial_objects) <= MAX_COMPONENTS:
            raise JournalError("bounded complete synthetic object set required")
        self._initial = dict(initial_objects)
        for name, data in self._initial.items():
            _identifier(name)
            if not isinstance(data, bytes) or not 1 <= len(data) <= MAX_OBJECT_BYTES:
                raise JournalError("objects require bounded nonempty immutable synthetic bytes")
        if sum(map(len, self._initial.values())) > MAX_TOTAL_OBJECT_BYTES:
            raise JournalError("synthetic object set exceeds limit")
        if not isinstance(operations, tuple) or not 1 <= len(operations) <= MAX_OPERATIONS:
            raise JournalError("bounded immutable operation tuple required")
        self._operations = operations
        expected = dict(self._initial)
        # Hash fixture payloads once at construction. History replay compares
        # bounded metadata only, never repeatedly hashes the fixture byte sets.
        self._boundaries = [_metadata(self._initial)]
        seen = set()
        descriptions = []
        for operation in operations:
            if not isinstance(operation, Operation):
                raise JournalError("only immutable synthetic Operation values are accepted")
            _identifier(operation.operation_id)
            _identifier(operation.component)
            if (operation.operation_id in seen or operation.category != "synthetic_mutation"
                    or operation.component not in expected
                    or not isinstance(operation.before, bytes) or not isinstance(operation.after, bytes)
                    or operation.before != expected[operation.component]
                    or len(operation.before) != len(operation.after)
                    or operation.before == operation.after):
                raise JournalError("synthetic operation identity/source/order/size/category mismatch")
            seen.add(operation.operation_id)
            expected[operation.component] = operation.after
            before_hash = self._boundaries[-1][operation.component]["sha256"]
            after_hash = _sha(operation.after)
            next_boundary = {name: dict(value) for name, value in self._boundaries[-1].items()}
            next_boundary[operation.component] = {"size": len(operation.after), "sha256": after_hash}
            self._boundaries.append(next_boundary)
            descriptions.append({"operation_id": operation.operation_id, "component": operation.component,
                                 "category": operation.category, "size": len(operation.before),
                                 "before_sha256": before_hash, "after_sha256": after_hash})
        self._path = _safe_path(journal_path)
        lock_path = _safe_path(lock_path)
        if os.path.normcase(str(self._path)) == os.path.normcase(str(lock_path)):
            raise JournalError("journal and stable lock require different paths")
        self._header = {"schema_version": 1, "synthetic_only": True, "device_eligible": False,
                        "session_id": self._session_id,
                        "lock_path": os.path.normcase(str(lock_path.resolve())),
                        "plan_sha256": _sha(_canonical({"initial": self._boundaries[0],
                                                        "operations": descriptions})),
                        "initial_objects": self._boundaries[0], "operation_count": len(operations)}
        try:
            self._lock = _StableLock(lock_path)
            flags = os.O_RDWR | os.O_APPEND | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
            if new:
                flags |= os.O_CREAT | os.O_EXCL
            descriptor = os.open(self._path, flags, 0o600)
            try:
                self._stream = os.fdopen(descriptor, "r+b", buffering=0)
            except BaseException:
                os.close(descriptor)
                raise
            _plain_descriptor(self._path, self._stream)
            if new:
                self._append("created", self._header)
            else:
                self._stream.seek(0)
                self._raw = self._stream.read(MAX_JOURNAL_BYTES + 1)
                self._records = self._decode(self._raw)
                self._cursor = self._replay(self._records)
                self._append("reopened", self._boundary_facts())
        except BaseException as exc:
            try:
                self.close()
            except BaseException:
                pass  # Both handles were closed/attempted; retain the primary failure.
            if isinstance(exc, OSError):
                raise JournalError("journal could not be exclusively created or safely reopened") from exc
            raise

    @property
    def state(self) -> str:
        return "closed" if self._closed else self._cursor.state

    @property
    def completed_operations(self) -> int:
        return self._cursor.index

    @property
    def device_eligible(self) -> bool:
        return False

    @property
    def journal(self) -> tuple[dict, ...]:
        return tuple(json.loads(_canonical(record)) for record in self._records)

    def _available(self) -> None:
        if self._closed or self._poisoned:
            raise JournalError("closed or uncertain journal requires explicit reopen/review")
        if self._lock is None:
            raise OwnershipError("synthetic resource ownership is absent")
        try:
            self._lock.check()
        except (OSError, JournalError) as exc:
            self._poisoned = True
            self._cursor.state = "needs_review"
            raise OwnershipError("synthetic ownership changed; close and explicitly review") from exc

    def _boundary_facts(self) -> dict:
        return {"boundary": self._cursor.index,
                "operation_id": self._operations[self._cursor.index].operation_id
                if self._cursor.pending else None}

    def _observed(self, observed: Mapping[str, bytes]) -> dict:
        if not isinstance(observed, Mapping) or set(observed) != set(self._initial):
            raise JournalError("observation must cover the complete original synthetic object set")
        copy = dict(observed)
        if any(not isinstance(data, bytes) or len(data) > MAX_OBJECT_BYTES for data in copy.values()):
            raise JournalError("observations require bounded immutable synthetic bytes")
        if sum(map(len, copy.values())) > MAX_TOTAL_OBJECT_BYTES:
            raise JournalError("synthetic observation set exceeds limit")
        return _metadata(copy)

    def _valid_metadata(self, observed) -> None:
        if not isinstance(observed, dict) or set(observed) != set(self._initial):
            raise JournalError("invalid complete recorded observation")
        total = 0
        for value in observed.values():
            if (not isinstance(value, dict) or set(value) != {"size", "sha256"}
                    or type(value["size"]) is not int or not 0 <= value["size"] <= MAX_OBJECT_BYTES
                    or not isinstance(value["sha256"], str) or not _HASH.fullmatch(value["sha256"])):
                raise JournalError("invalid recorded observation metadata")
            total += value["size"]
        if total > MAX_TOTAL_OBJECT_BYTES:
            raise JournalError("recorded observation exceeds limit")

    def prepare_next(self, observed: Mapping[str, bytes]) -> Operation:
        self._available()
        if self._cursor.state != "ready":
            raise JournalError("prepare requires explicitly ready synthetic state")
        operation = self._operations[self._cursor.index]
        metadata = self._observed(observed)
        if metadata != self._boundaries[self._cursor.index]:
            self._append("boundary_interrupted", self._boundary_facts())
            raise JournalError("fresh complete synthetic source does not match confirmed boundary")
        self._append("prepared", {"boundary": self._cursor.index,
                     "operation_id": operation.operation_id, "component": operation.component,
                     "category": operation.category,
                     "attempt": self._cursor.attempts.get(operation.operation_id, 0) + 1,
                     "before_sha256": self._boundaries[self._cursor.index][operation.component]["sha256"],
                     "after_sha256": self._boundaries[self._cursor.index + 1][operation.component]["sha256"],
                     "observed": metadata})
        return operation

    def record_result(self, outcome: str, observed: Mapping[str, bytes]) -> None:
        self._available()
        if self._cursor.state != "prepared":
            raise JournalError("a durably prepared record is required before a synthetic result")
        if not isinstance(outcome, str) or outcome not in _UNCERTAIN | {"confirmed"}:
            raise JournalError("unknown synthetic result outcome")
        try:
            metadata = self._observed(observed)
        except JournalError:
            self._append("boundary_interrupted", self._boundary_facts())
            raise
        facts = {**self._boundary_facts(), "outcome": outcome, "observed": metadata}
        if outcome == "confirmed" and metadata == self._boundaries[self._cursor.index + 1]:
            self._append("result_confirmed", facts)
        else:
            if outcome == "confirmed":
                facts["outcome"] = "observation_mismatch"
            self._append("result_uncertain", facts)

    def interrupt_boundary(self) -> None:
        self._available()
        if self._cursor.state not in {"ready", "prepared", "complete"}:
            raise JournalError("not at an interruptible synthetic boundary")
        self._append("boundary_interrupted", self._boundary_facts())

    def _classification(self, cursor: _Cursor, observed: dict) -> str:
        if observed == self._boundaries[cursor.index]:
            return "not_applied" if cursor.pending else "confirmed_boundary"
        if cursor.pending and observed == self._boundaries[cursor.index + 1]:
            return "applied"
        return "partial_or_mixed_state"

    def reconcile(self, observed: Mapping[str, bytes], evidence_reference: str) -> str:
        self._available()
        if self._cursor.state != "needs_review":
            raise JournalError("reconciliation requires needs_review")
        _identifier(evidence_reference)
        metadata = self._observed(observed)
        classification = self._classification(self._cursor, metadata)
        self._append("reconciliation_unresolved" if classification == "partial_or_mixed_state" else "reconciled",
                     {**self._boundary_facts(), "classification": classification,
                      "evidence_reference": evidence_reference, "observed": metadata})
        return classification

    def resume(self) -> None:
        self._available()
        if self._cursor.state != "reconciled":
            raise JournalError("resume requires explicit successful observation/reconciliation")
        self._append("explicit_resume", {"boundary": self._cursor.index})

    def _decode(self, raw: bytes) -> list[dict]:
        if not raw or len(raw) > MAX_JOURNAL_BYTES or not raw.endswith(b"\n"):
            raise JournalError("empty, oversized or incomplete journal; preserve without repair")
        lines = raw[:-1].split(b"\n")
        if len(lines) > MAX_RECORDS:
            raise JournalError("journal record count exceeds limit")

        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise JournalError("duplicate journal JSON key")
                result[key] = value
            return result

        def constant(value):
            raise JournalError("non-finite journal JSON value")

        records = []
        previous = _ZERO_HASH
        for sequence, line in enumerate(lines, 1):
            if not line or len(line) + 1 > MAX_RECORD_BYTES:
                raise JournalError("empty or oversized journal record")
            try:
                record = json.loads(line.decode("ascii"), object_pairs_hook=unique, parse_constant=constant)
                if (not isinstance(record, dict)
                        or set(record) != {"sequence", "event", "facts", "previous_sha256", "sha256"}
                        or type(record["sequence"]) is not int or record["sequence"] != sequence
                        or not isinstance(record["event"], str) or not isinstance(record["facts"], dict)
                        or record["previous_sha256"] != previous
                        or not isinstance(record["sha256"], str) or not _HASH.fullmatch(record["sha256"])
                        or _canonical(record) != line):
                    raise JournalError("noncanonical or invalid journal envelope/sequence/chain")
                unsigned = {k: v for k, v in record.items() if k != "sha256"}
                if _sha(_canonical(unsigned)) != record["sha256"]:
                    raise JournalError("journal record hash mismatch")
            except (UnicodeError, json.JSONDecodeError, RecursionError, TypeError, ValueError) as exc:
                if isinstance(exc, JournalError):
                    raise
                raise JournalError("invalid strict journal encoding") from exc
            records.append(record)
            previous = record["sha256"]
        return records

    def _replay(self, records: list[dict]) -> _Cursor:
        if (not records or records[0]["event"] != "created"
                or _canonical(records[0]["facts"]) != _canonical(self._header)):
            raise JournalError("journal header, complete plan, session or stable lock does not match")
        cursor = _Cursor()
        for record in records[1:]:
            event, facts = record["event"], record["facts"]
            boundary = {"boundary": cursor.index,
                        "operation_id": self._operations[cursor.index].operation_id if cursor.pending else None}
            if event == "prepared":
                if cursor.state != "ready" or cursor.index >= len(self._operations):
                    raise JournalError("illegal prepared transition")
                operation = self._operations[cursor.index]
                expected = {"boundary": cursor.index, "operation_id": operation.operation_id,
                            "component": operation.component,
                            "before_sha256": self._boundaries[cursor.index][operation.component]["sha256"],
                            "category": operation.category,
                            "attempt": cursor.attempts.get(operation.operation_id, 0) + 1,
                            "after_sha256": self._boundaries[cursor.index + 1][operation.component]["sha256"],
                            "observed": self._boundaries[cursor.index]}
                if _canonical(facts) != _canonical(expected):
                    raise JournalError("prepared facts do not match full synthetic plan/boundary")
                cursor.attempts[operation.operation_id] = expected["attempt"]
                cursor.pending, cursor.state = True, "prepared"
            elif event in {"result_confirmed", "result_uncertain"}:
                if (cursor.state != "prepared" or not cursor.pending
                        or set(facts) != {"boundary", "operation_id", "outcome", "observed"}
                        or type(facts["boundary"]) is not int
                        or facts["boundary"] != boundary["boundary"]
                        or facts["operation_id"] != boundary["operation_id"]
                        or not isinstance(facts["outcome"], str)):
                    raise JournalError("illegal synthetic result transition")
                self._valid_metadata(facts["observed"])
                matches = facts["observed"] == self._boundaries[cursor.index + 1]
                if event == "result_confirmed":
                    if facts["outcome"] != "confirmed" or not matches:
                        raise JournalError("unproved complete synthetic result")
                    cursor.index += 1
                    cursor.pending = False
                    cursor.state = "complete" if cursor.index == len(self._operations) else "ready"
                else:
                    if (facts["outcome"] not in _UNCERTAIN | {"observation_mismatch"}
                            or (facts["outcome"] == "observation_mismatch" and matches)):
                        raise JournalError("invalid uncertain synthetic result")
                    cursor.state = "needs_review"
            elif event in {"reopened", "boundary_interrupted"}:
                if _canonical(facts) != _canonical(boundary) or (event == "boundary_interrupted"
                        and cursor.state not in {"ready", "prepared", "complete"}):
                    raise JournalError("invalid synthetic interruption/reopen boundary")
                cursor.state = "needs_review"
            elif event in {"reconciled", "reconciliation_unresolved"}:
                if (cursor.state != "needs_review" or set(facts) != {
                        "boundary", "operation_id", "classification", "evidence_reference", "observed"}
                        or type(facts["boundary"]) is not int
                        or facts["boundary"] != boundary["boundary"]
                        or facts["operation_id"] != boundary["operation_id"]):
                    raise JournalError("illegal synthetic reconciliation transition")
                _identifier(facts["evidence_reference"])
                self._valid_metadata(facts["observed"])
                classification = self._classification(cursor, facts["observed"])
                if (facts["classification"] != classification or (event == "reconciled")
                        != (classification != "partial_or_mixed_state")):
                    raise JournalError("reconciliation does not match complete boundary observations")
                if event == "reconciled":
                    if classification == "applied":
                        cursor.index += 1
                    cursor.pending, cursor.state = False, "reconciled"
            elif event == "explicit_resume":
                if (cursor.state != "reconciled"
                        or _canonical(facts) != _canonical({"boundary": cursor.index})):
                    raise JournalError("illegal explicit resume transition")
                cursor.state = "complete" if cursor.index == len(self._operations) else "ready"
            else:
                raise JournalError("unknown synthetic journal event")
        return cursor

    def _append(self, event: str, facts: dict) -> None:
        self._available()
        try:
            _plain_descriptor(self._path, self._stream)
            self._stream.seek(0)
            if self._stream.read(MAX_JOURNAL_BYTES + 1) != self._raw:
                raise JournalError("journal bytes changed outside this owner")
            record = {"sequence": len(self._records) + 1, "event": event, "facts": facts,
                      "previous_sha256": self._records[-1]["sha256"] if self._records else _ZERO_HASH}
            record["sha256"] = _sha(_canonical(record))
            line = _canonical(record) + b"\n"
            if (len(line) > MAX_RECORD_BYTES or len(self._raw) + len(line) > MAX_JOURNAL_BYTES
                    or len(self._records) + 1 > MAX_RECORDS):
                raise JournalError("journal append would exceed fixed limit")
            cursor = self._replay(self._records + [record])
            self._stream.seek(0, os.SEEK_END)
            _write_all(self._stream, line)
            self._stream.flush()
            os.fsync(self._stream.fileno())
            self._raw += line
            self._records.append(record)
            self._cursor = cursor
        except BaseException as exc:
            self._poisoned = True
            self._cursor.state = "needs_review"
            raise PersistenceError("journal append uncertain; preserve bytes and explicitly review") from exc

    def close(self) -> None:
        """Release OS handles at any state; never repair or declare work complete."""
        if self._closed:
            return
        self._closed = True
        stream, self._stream = self._stream, None
        try:
            if stream is not None:
                stream.close()
        finally:
            lock, self._lock = self._lock, None
            if lock is not None:
                lock.close()

    def __enter__(self):
        self._available()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
