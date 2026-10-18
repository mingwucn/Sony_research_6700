"""Host-only FT-102 queue foundation. No socket, FTP client or camera API exists here.

The only supplied transport is an in-memory mock. Its strong capabilities are
assumptions to test, never evidence about a real FTP/FTPS server.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Callable


class QueueError(ValueError):
    """Invalid input/state, unavailable source, or an unsafe state transition."""


class SourceError(QueueError):
    """Local source is unavailable, changed or outside synthetic source bounds."""


class TransportError(Exception):
    """Mock error category without credentials, server text or source paths."""

    def __init__(self, kind: str, *, uncertain: bool = False):
        if kind not in {"transient", "auth", "permission", "quota", "tls", "collision"}:
            raise ValueError("unknown transport error category")
        self.kind = kind
        self.uncertain = uncertain
        super().__init__(kind)


@dataclass(frozen=True)
class Observation:
    size: int
    sha256: str | None


@dataclass(frozen=True)
class Capture:
    body_alias: str
    session_id: str
    card_id: str
    object_id: str
    capture_sequence: int
    filename: str
    format: str
    expected_formats: tuple[str, ...] = ("JPEG",)
    completion_evidence: str = "synthetic-fixture"


_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")
_COMPONENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}\Z")
_HASH = re.compile(r"[0-9a-f]{64}\Z")
_STATES = {"ready", "transferring", "verification_pending", "finalizing",
           "ready_to_finalize", "committed", "retryable_error", "permanent_error",
           "needs_review", "cancelled"}
_INFLIGHT = {"transferring", "verification_pending", "finalizing"}
_MAX_BYTES = 32 * 1024 * 1024  # Synthetic foundation bound, not camera format support.


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _relative(value: str) -> str:
    if not isinstance(value, str) or not value or len(value) > 384:
        raise QueueError("invalid relative filename")
    parts = value.split("/")
    if any(not _COMPONENT.fullmatch(p) or p in {".", ".."} or p.endswith(".")
           for p in parts):
        raise QueueError("invalid relative filename")
    # ASCII-only intentionally excludes ambiguous encodings and FTP command input.
    return value


def _capture(value: Capture) -> Capture:
    for key in ("body_alias", "session_id", "card_id", "object_id"):
        if not isinstance(getattr(value, key), str) or not _TOKEN.fullmatch(getattr(value, key)):
            raise QueueError("invalid capture identity")
    if type(value.capture_sequence) is not int or not 0 <= value.capture_sequence <= 2**63 - 1:
        raise QueueError("invalid capture sequence")
    _relative(value.filename)
    if value.format not in {"RAW", "JPEG"}:
        raise QueueError("unsupported synthetic format label")
    if (type(value.expected_formats) is not tuple or not value.expected_formats
            or len(set(value.expected_formats)) != len(value.expected_formats)
            or any(f not in {"RAW", "JPEG"} for f in value.expected_formats)
            or value.format not in value.expected_formats):
        raise QueueError("invalid capture group formats")
    if value.completion_evidence != "synthetic-fixture":
        raise QueueError("only synthetic completion evidence is implemented")
    return value


def _identity(capture: Capture, *, group: bool = False) -> str:
    fields = {k: getattr(capture, k) for k in
              ("body_alias", "session_id", "card_id", "capture_sequence")}
    if not group:
        fields.update(object_id=capture.object_id, filename=capture.filename, format=capture.format)
    return _hash(json.dumps(fields, sort_keys=True, separators=(",", ":")).encode("ascii"))


def _root(value: str) -> str:
    if not isinstance(value, str) or not value.startswith("/") or value.endswith("/"):
        raise QueueError("invalid constrained remote root")
    _relative(value[1:])
    return value


def _json_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise QueueError("duplicate durable-state key")
        result[key] = value
    return result


class MockTransport:
    """In-memory exclusive upload/rename and complete hash observation.

    This mock assumes verified TLS and race-free no-clobber operations. FTP RNTO
    is not presumed to provide these guarantees on an actual server.
    """

    def __init__(self):
        self.objects: dict[str, bytes] = {}
        self.calls: list[tuple[str, str]] = []
        self.verified_tls = True
        self.hash_available = True

    def check_security(self) -> None:
        if not self.verified_tls:
            raise TransportError("tls")

    def inspect(self, path: str) -> Observation | None:
        self.calls.append(("inspect", path))
        data = self.objects.get(path)
        return None if data is None else Observation(len(data), _hash(data) if self.hash_available else None)

    def upload_exclusive(self, path: str, data: bytes) -> None:
        self.calls.append(("upload", path))
        if path in self.objects:
            raise TransportError("collision")
        self.objects[path] = data

    def rename_exclusive(self, temporary: str, final: str) -> None:
        self.calls.append(("rename", final))
        if final in self.objects:
            raise TransportError("collision")
        if temporary not in self.objects:
            raise TransportError("transient")
        self.objects[final] = self.objects.pop(temporary)


class TransferQueue:
    """Single-owner durable queue over an immutable, caller-owned local spool.

    Use create/load and close (or a context manager). A leftover lease is never
    removed automatically after a crash: inspect/reconcile it locally first.
    Queue operations never remove or modify source files.
    """

    def __init__(self, state_path: Path, spool: Path):
        self.path = Path(state_path)
        self.spool = Path(spool).resolve(strict=True)
        if not self.spool.is_dir() or not self.path.parent.is_dir() or self.path.is_symlink():
            raise QueueError("invalid queue/spool location")
        self.lease = self.path.with_name(self.path.name + ".lock")
        self._lease_fd = os.open(self.lease, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        self.entries: dict[str, dict] = {}
        self.remote_root = "/incoming"
        self.max_attempts = 3

    @classmethod
    def create(cls, state_path: Path, spool: Path, *, remote_root: str = "/incoming",
               max_attempts: int = 3) -> TransferQueue:
        if Path(state_path).exists():
            raise QueueError("refuse to replace existing durable state")
        if type(max_attempts) is not int or not 1 <= max_attempts <= 5:
            raise QueueError("attempt bound must be between one and five")
        remote_root = _root(remote_root)
        queue = cls(state_path, spool)
        try:
            # Another legitimate creator may have completed between the first
            # existence check and this process acquiring the exclusive lease.
            if queue.path.exists():
                raise QueueError("refuse to replace existing durable state")
            queue.remote_root, queue.max_attempts = remote_root, max_attempts
            queue._persist()
        except BaseException:
            queue.close()
            raise
        return queue

    @classmethod
    def load(cls, state_path: Path, spool: Path) -> TransferQueue:
        queue = cls(state_path, spool)
        try:
            if not queue.path.is_file() or queue.path.stat().st_size > 4 * 1024 * 1024:
                raise QueueError("invalid durable-state file")
            data = json.loads(queue.path.read_text(encoding="utf-8"), object_pairs_hook=_json_object)
            queue._validate(data)
            queue.remote_root, queue.max_attempts = data["remote_root"], data["max_attempts"]
            queue.entries = {e["id"]: e for e in data["entries"]}
            for entry in queue.entries.values():
                if entry["state"] in _INFLIGHT:
                    entry["state"], entry["reason"] = "needs_review", "interrupted_operation"
            queue._persist()
        except BaseException:
            queue.close()
            raise
        return queue

    def close(self) -> None:
        if self._lease_fd is not None:
            os.close(self._lease_fd)
            self._lease_fd = None
            self.lease.unlink()

    def __enter__(self) -> TransferQueue:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _persist(self) -> None:
        if self._lease_fd is None:
            raise QueueError("queue is closed")
        data = {"schema_version": 1, "remote_root": self.remote_root,
                "max_attempts": self.max_attempts,
                "entries": sorted(self.entries.values(), key=lambda e: e["id"])}
        self._validate(data)
        temporary: str | None = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                             prefix=self.path.name + ".", suffix=".tmp",
                                             dir=self.path.parent, delete=False) as stream:
                temporary = stream.name
                json.dump(data, stream, sort_keys=True, indent=2, allow_nan=False)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
            temporary = None
            # Directory fsync is unavailable on some hosts, notably Windows.
            if os.name == "posix":
                fd = os.open(self.path.parent, os.O_RDONLY)
                try:
                    os.fsync(fd)
                finally:
                    os.close(fd)
        finally:
            if temporary is not None:
                os.unlink(temporary)

    @staticmethod
    def _validate(data: dict) -> None:
        if type(data) is not dict or set(data) != {"schema_version", "remote_root", "max_attempts", "entries"}:
            raise QueueError("invalid durable-state schema")
        if type(data["schema_version"]) is not int or data["schema_version"] != 1:
            raise QueueError("unsupported durable-state schema")
        _root(data["remote_root"])
        if type(data["max_attempts"]) is not int or not 1 <= data["max_attempts"] <= 5:
            raise QueueError("invalid durable attempt bound")
        if type(data["entries"]) is not list or len(data["entries"]) > 10000:
            raise QueueError("invalid durable entry list")
        ids: set[str] = set()
        groups: dict[str, tuple[set[str], set[str]]] = {}
        for entry in data["entries"]:
            keys = {"id", "group_id", "capture", "source", "size", "sha256", "state", "attempts",
                    "next_attempt", "reason", "verified_final_sha256"}
            if (type(entry) is not dict or set(entry) != keys or type(entry["capture"]) is not dict
                    or set(entry["capture"]) != set(Capture.__dataclass_fields__)):
                raise QueueError("invalid durable entry schema")
            try:
                fields = dict(entry["capture"])
                if type(fields.get("expected_formats")) not in {list, tuple}:
                    raise QueueError("invalid durable capture formats")
                fields["expected_formats"] = tuple(fields["expected_formats"])
                capture = _capture(Capture(**fields))
            except (TypeError, AttributeError) as error:
                raise QueueError("invalid durable capture") from error
            if entry["id"] != _identity(capture) or entry["group_id"] != _identity(capture, group=True):
                raise QueueError("durable identity mismatch")
            if entry["id"] in ids:
                raise QueueError("duplicate durable identity")
            ids.add(entry["id"])
            expected, formats = groups.setdefault(entry["group_id"], (set(capture.expected_formats), set()))
            if expected != set(capture.expected_formats) or capture.format in formats:
                raise QueueError("inconsistent durable capture group")
            formats.add(capture.format)
            _relative(entry["source"])
            if type(entry["size"]) is not int or not 0 < entry["size"] <= _MAX_BYTES:
                raise QueueError("invalid durable source size")
            if not isinstance(entry["sha256"], str) or not _HASH.fullmatch(entry["sha256"]):
                raise QueueError("invalid durable source digest")
            if not isinstance(entry["state"], str) or entry["state"] not in _STATES:
                raise QueueError("invalid durable state")
            if type(entry["attempts"]) is not int or not 0 <= entry["attempts"] <= data["max_attempts"]:
                raise QueueError("invalid durable attempts")
            if (type(entry["next_attempt"]) not in {int, float} or not math.isfinite(entry["next_attempt"])
                    or entry["next_attempt"] < 0):
                raise QueueError("invalid durable retry time")
            if not isinstance(entry["reason"], str) or not re.fullmatch(r"[a-z_]{0,64}", entry["reason"]):
                raise QueueError("invalid durable reason")
            if entry["verified_final_sha256"] is not None and entry["verified_final_sha256"] != entry["sha256"]:
                raise QueueError("invalid durable verification")
            if (entry["state"] == "committed") != (entry["verified_final_sha256"] == entry["sha256"]):
                raise QueueError("committed state requires full digest evidence")

    def _source(self, source: str) -> bytes:
        path = self.spool
        for component in _relative(source).split("/"):
            path = path / component
            if path.is_symlink():
                raise SourceError("source links are refused")
        try:
            before = path.stat()
            if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= _MAX_BYTES:
                raise SourceError("source must be a bounded nonempty regular file")
            with path.open("rb") as stream:
                opened = os.fstat(stream.fileno())
                if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                        opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns):
                    raise SourceError("source changed before reading")
                result = stream.read(_MAX_BYTES + 1)
                after = os.fstat(stream.fileno())
            if (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns) != (
                    after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns) or len(result) != after.st_size:
                raise SourceError("source changed while reading")
            return result
        except OSError as error:
            raise SourceError("source unavailable") from error

    def enqueue(self, capture: Capture, source: str) -> str:
        capture = _capture(capture)
        content = self._source(source)
        identity = _identity(capture)
        previous = self.entries.get(identity)
        if previous is not None:
            if previous["sha256"] != _hash(content) or previous["size"] != len(content):
                raise QueueError("capture identity reused with different content")
            return identity
        # A group's expected membership must not change as its second object arrives.
        group_id = _identity(capture, group=True)
        if any(e["group_id"] == group_id and set(e["capture"]["expected_formats"]) != set(capture.expected_formats)
               for e in self.entries.values()):
            raise QueueError("capture group expectation changed")
        if any(e["group_id"] == group_id and e["capture"]["format"] == capture.format
               for e in self.entries.values()):
            raise QueueError("capture group already has that format")
        self.entries[identity] = {
            "id": identity, "group_id": group_id, "capture": asdict(capture), "source": _relative(source),
            "size": len(content), "sha256": _hash(content), "state": "ready", "attempts": 0,
            "next_attempt": 0, "reason": "", "verified_final_sha256": None}
        self._persist()
        return identity

    def paths(self, identity: str) -> tuple[str, str]:
        entry = self.entries[identity]
        suffix = ".arw" if entry["capture"]["format"] == "RAW" else ".jpg"
        final = self.remote_root + "/" + identity + suffix
        return final + ".part", final

    def group_status(self, group_id: str) -> dict:
        entries = [e for e in self.entries.values() if e["group_id"] == group_id]
        if not entries:
            raise QueueError("unknown capture group")
        expected = set(entries[0]["capture"]["expected_formats"])
        complete = {e["capture"]["format"] for e in entries if e["state"] == "committed"}
        return {"expected": sorted(expected), "committed": sorted(complete), "complete": complete == expected}

    @staticmethod
    def _matches(observation: Observation | None, entry: dict) -> bool:
        return observation is not None and observation.size == entry["size"] and observation.sha256 == entry["sha256"]

    def _state(self, entry: dict, state: str, reason: str = "") -> None:
        entry["state"], entry["reason"] = state, reason
        if state != "committed":
            entry["verified_final_sha256"] = None
        self._persist()

    def _failure(self, entry: dict, error: TransportError, now: float) -> None:
        if error.uncertain:
            self._state(entry, "needs_review", "uncertain_" + error.kind)
        elif error.kind == "transient" and entry["attempts"] < self.max_attempts:
            # Deterministic identity-derived jitter keeps tests/recovery reproducible.
            jitter = int(entry["id"][:2], 16) / 256
            entry["next_attempt"] = now + min(60, 2 ** entry["attempts"]) + jitter
            self._state(entry, "retryable_error", "transient")
        else:
            self._state(entry, "permanent_error", error.kind)

    def run_one(self, identity: str, transport: MockTransport, *, now: float = 0,
                cancelled: Callable[[], bool] = lambda: False) -> str:
        """One bounded attempt; no timer, retry loop, worker or network is started."""
        if type(now) not in {int, float} or not math.isfinite(now) or now < 0:
            raise QueueError("invalid caller-supplied time")
        entry = self.entries[identity]
        if entry["state"] not in {"ready", "retryable_error", "ready_to_finalize"}:
            raise QueueError("entry requires an explicit different transition")
        if now < entry["next_attempt"]:
            return entry["state"]
        if cancelled():
            self._state(entry, "cancelled", "cancelled_before_operation")
            return entry["state"]
        temporary, final = self.paths(identity)
        finalize_only = entry["state"] == "ready_to_finalize"
        if entry["attempts"] >= self.max_attempts:
            self._state(entry, "permanent_error", "attempt_bound")
            return entry["state"]
        entry["attempts"] += 1
        self._persist()
        mutated = False
        try:
            transport.check_security()
            content = self._source(entry["source"])
            if len(content) != entry["size"] or _hash(content) != entry["sha256"]:
                raise SourceError("source digest changed")
            existing_final = transport.inspect(final)
            if existing_final is not None:
                if self._matches(existing_final, entry):
                    entry["verified_final_sha256"] = entry["sha256"]
                    self._state(entry, "committed", "existing_final_hash_verified")
                else:
                    self._state(entry, "needs_review", "final_collision_or_unverified")
                return entry["state"]
            existing_temp = transport.inspect(temporary)
            if finalize_only:
                if not self._matches(existing_temp, entry):
                    self._state(entry, "needs_review", "temporary_changed_or_unverified")
                    return entry["state"]
            elif existing_temp is not None:
                self._state(entry, "needs_review", "existing_temporary_requires_reconciliation")
                return entry["state"]
            else:
                self._state(entry, "transferring")
                transport.upload_exclusive(temporary, content)
                mutated = True
                self._state(entry, "verification_pending")
                if not self._matches(transport.inspect(temporary), entry):
                    self._state(entry, "needs_review", "temporary_hash_not_verified")
                    return entry["state"]
            if cancelled():
                self._state(entry, "needs_review", "cancelled_with_remote_temporary")
                return entry["state"]
            self._state(entry, "finalizing")
            transport.rename_exclusive(temporary, final)
            mutated = True
            if not self._matches(transport.inspect(final), entry):
                self._state(entry, "needs_review", "final_hash_not_verified")
            else:
                entry["verified_final_sha256"] = entry["sha256"]
                self._state(entry, "committed", "final_hash_verified")
        except TransportError as error:
            # Once a remote object exists, even a known read error cannot justify reupload.
            if mutated or finalize_only:
                error = TransportError(error.kind, uncertain=True)
            self._failure(entry, error, now)
        except SourceError:
            self._state(entry, "needs_review" if finalize_only else "permanent_error", "source_unavailable_or_changed")
        except Exception:
            # Unexpected adapter responses are never interpreted as safe retry permission.
            self._state(entry, "needs_review", "unexpected_adapter_or_persistence_error")
        return entry["state"]

    def reconcile(self, identity: str, transport: MockTransport) -> str:
        """Read-only mock observations; never uploads, renames or deletes anything."""
        entry = self.entries[identity]
        if entry["state"] != "needs_review":
            raise QueueError("reconciliation requires needs_review")
        temporary, final = self.paths(identity)
        try:
            transport.check_security()
            observed_final, observed_temp = transport.inspect(final), transport.inspect(temporary)
            if observed_final is not None:
                if self._matches(observed_final, entry):
                    entry["verified_final_sha256"] = entry["sha256"]
                    self._state(entry, "committed", "reconciled_final_hash_verified")
                else:
                    self._state(entry, "needs_review", "final_collision_or_unverified")
            elif observed_temp is not None:
                if self._matches(observed_temp, entry):
                    self._state(entry, "ready_to_finalize", "reconciled_temporary_hash_verified")
                else:
                    self._state(entry, "needs_review", "temporary_collision_or_unverified")
            elif entry["attempts"] < self.max_attempts:
                self._state(entry, "ready", "reconciled_remote_absent")
            else:
                self._state(entry, "permanent_error", "attempt_bound")
        except TransportError:
            self._state(entry, "needs_review", "reconciliation_read_failed")
        except Exception:
            self._state(entry, "needs_review", "unexpected_reconciliation_error")
        return entry["state"]
