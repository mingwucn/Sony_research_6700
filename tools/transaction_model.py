"""An in-memory, synthetic transaction/journal state machine, never an executor.

No persistence, process lock, USB/network call, reboot, retry or rollback exists.
The simulated object's contents are known to the model, even for lost responses.
"""

from dataclasses import dataclass
import hashlib
from typing import Mapping


class TransactionError(ValueError):
    """A requested simulated transition is not currently legal."""


def _text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or value.strip().lower() in {
            "unknown", "unverified", "todo", "none"}:
        raise TransactionError(f"missing explicit {name}")
    return value


def _hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class Operation:
    operation_id: str
    component: str
    before: bytes
    after: bytes
    category: str = "synthetic_mutation"


@dataclass(frozen=True)
class JournalRecord:
    sequence: int
    event: str
    state: str
    operation_id: str | None
    facts: tuple[tuple[str, str], ...]


class OwnershipRegistry:
    """Process-memory ownership model; no OS/process concurrency guarantee."""

    def __init__(self):
        self._owners: dict[str, str] = {}
        self._sessions: set[str] = set()

    def acquire(self, session_id: str, resources: tuple[str, ...]) -> None:
        _text(session_id, "session id")
        if not isinstance(resources, tuple) or not resources or len(set(resources)) != len(resources):
            raise TransactionError("resources must be a nonempty unique immutable set")
        for resource in resources:
            _text(resource, "resource id")
        if session_id in self._sessions or any(r in self._owners for r in resources):
            raise TransactionError("duplicate session or resource owner")
        self._owners.update({r: session_id for r in resources})
        self._sessions.add(session_id)

    def owns(self, session_id: str, resources: tuple[str, ...]) -> bool:
        return session_id in self._sessions and all(self._owners.get(r) == session_id for r in resources)

    def release(self, session_id: str, resources: tuple[str, ...]) -> None:
        if not self.owns(session_id, resources):
            raise TransactionError("session does not own its resources")
        # Check the complete reservation, so a partial release cannot orphan a resource.
        if {r for r, owner in self._owners.items() if owner == session_id} != set(resources):
            raise TransactionError("incomplete resource release")
        for resource in resources:
            del self._owners[resource]
        self._sessions.remove(session_id)


class TransactionSimulator:
    """Simulate explicitly prepared operations on immutable fixture bytes.

    Timeout/disconnect/partial results require observation and reconciliation.
    The caller must explicitly resume even when the observed result is complete.
    Several objects are never represented as one atomic write.
    """

    UNCERTAIN_OUTCOMES = frozenset({"timeout_before", "timeout_after", "disconnect_before",
                                    "disconnect_after", "partial"})

    def __init__(self, session_id: str, resource_ids: tuple[str, ...],
                 initial_objects: Mapping[str, bytes], operations: tuple[Operation, ...],
                 registry: OwnershipRegistry):
        _text(session_id, "session id")
        if not isinstance(registry, OwnershipRegistry):
            raise TransactionError("explicit shared ownership registry required")
        if not isinstance(initial_objects, Mapping) or not initial_objects:
            raise TransactionError("missing initial object set")
        for name, data in initial_objects.items():
            _text(name, "component")
            if not isinstance(data, bytes) or not data:
                raise TransactionError("objects must be nonempty immutable synthetic bytes")
        if not isinstance(operations, tuple) or not operations:
            raise TransactionError("missing immutable operation sequence")
        expected = dict(initial_objects)
        seen = set()
        for operation in operations:
            if not isinstance(operation, Operation):
                raise TransactionError("invalid operation")
            _text(operation.operation_id, "operation id")
            if operation.operation_id in seen:
                raise TransactionError("duplicate operation id")
            seen.add(operation.operation_id)
            if operation.category != "synthetic_mutation":
                raise TransactionError("only synthetic mutation categories are accepted")
            if (operation.component not in expected or
                    not isinstance(operation.before, bytes) or not isinstance(operation.after, bytes)
                    or operation.before != expected[operation.component]
                    or len(operation.before) != len(operation.after)
                    or operation.before == operation.after):
                raise TransactionError("operation source/order/size mismatch")
            expected[operation.component] = operation.after
        self.session_id = session_id
        self.resource_ids = resource_ids
        self.registry = registry
        self.operations = operations
        self._objects = dict(initial_objects)
        self._confirmed = dict(initial_objects)
        self._journal: list[JournalRecord] = []
        self._index = 0
        self._pending: Operation | None = None
        self._attempts: dict[str, int] = {}
        self._state = "created"

    @property
    def state(self) -> str:
        return self._state

    @property
    def journal(self) -> tuple[JournalRecord, ...]:
        return tuple(self._journal)

    @property
    def completed_operations(self) -> int:
        return self._index

    @property
    def device_eligible(self) -> bool:
        return False

    def snapshot(self) -> dict[str, bytes]:
        """Return a copy of model observations; this performs no real read."""
        return dict(self._objects)

    def _record(self, event: str, operation: Operation | None = None, **facts: str) -> None:
        self._journal.append(JournalRecord(len(self._journal) + 1, event, self._state,
                                           operation.operation_id if operation else None,
                                           tuple(sorted(facts.items()))))

    def _owned(self) -> None:
        if not self.registry.owns(self.session_id, self.resource_ids):
            raise TransactionError("session ownership is absent")

    def open(self) -> None:
        if self._state != "created":
            raise TransactionError("session has already been opened")
        self.registry.acquire(self.session_id, self.resource_ids)
        self._state = "ready"
        self._record("session_opened", object_count=str(len(self._objects)))

    def prepare_next(self) -> None:
        self._owned()
        if self._state != "ready":
            raise TransactionError("prepare requires ready; needs_review is not a retry state")
        operation = self.operations[self._index]
        if self._objects != self._confirmed or self._objects[operation.component] != operation.before:
            self._state = "needs_review"
            self._record("source_mismatch", operation)
            raise TransactionError("fresh simulated source mismatch")
        attempt = self._attempts.get(operation.operation_id, 0) + 1
        # The prepared record is appended before the model permits mutation.
        self._record("prepared", operation, component=operation.component,
                     before_sha256=_hash(operation.before), after_sha256=_hash(operation.after),
                     category=operation.category, attempt=str(attempt),
                     boundary=str(self._index))
        self._attempts[operation.operation_id] = attempt
        self._pending = operation
        self._state = "prepared"

    def simulate_result(self, outcome: str, *, partial_bytes: bytes | None = None) -> None:
        self._owned()
        if self._state != "prepared" or self._pending is None:
            raise TransactionError("a prepared record is required before simulated mutation")
        if outcome != "confirmed" and outcome not in self.UNCERTAIN_OUTCOMES:
            raise TransactionError("unknown simulated outcome")
        operation = self._pending
        if outcome == "partial":
            if (not isinstance(partial_bytes, bytes) or len(partial_bytes) != len(operation.before)
                    or partial_bytes in (operation.before, operation.after)):
                raise TransactionError("partial outcome requires explicit distinct equal-size fixture bytes")
        elif partial_bytes is not None:
            raise TransactionError("partial bytes are only meaningful for a partial outcome")
        self._state = "applying"
        self._record("mutation_requested", operation, simulated_outcome=outcome)
        if outcome in {"confirmed", "timeout_after", "disconnect_after"}:
            self._objects[operation.component] = operation.after
        elif outcome == "partial":
            self._objects[operation.component] = partial_bytes
        if outcome == "confirmed":
            self._confirmed[operation.component] = operation.after
            self._index += 1
            self._pending = None
            self._state = "complete" if self._index == len(self.operations) else "ready"
            self._record("result_confirmed", operation,
                         after_sha256=_hash(self._objects[operation.component]))
        else:
            self._state = "needs_review"
            self._record("result_uncertain", operation, reason=outcome,
                         next_action="observe_existing_state_without_mutation")

    def interrupt_boundary(self) -> None:
        """Fault injection at any inter-object or prepared-before-send boundary."""
        self._owned()
        if self._state not in {"ready", "prepared", "complete"}:
            raise TransactionError("not at an interruptible boundary")
        self._state = "needs_review"
        self._record("boundary_interrupted", self._pending, boundary=str(self._index),
                     next_action="observe_existing_state_without_mutation")

    def reconcile(self, observed: Mapping[str, bytes], evidence_reference: str) -> str:
        self._owned()
        if self._state != "needs_review":
            raise TransactionError("reconciliation requires needs_review")
        _text(evidence_reference, "reconciliation evidence reference")
        if not isinstance(observed, Mapping) or dict(observed) != self._objects:
            raise TransactionError("observations must cover and match the complete simulated object set")
        observed_copy = dict(observed)
        expected_before = dict(self._confirmed)
        expected_after = dict(expected_before)
        if self._pending:
            expected_after[self._pending.component] = self._pending.after
        if observed_copy == expected_before:
            classification = "not_applied" if self._pending else "confirmed_boundary"
        elif self._pending and observed_copy == expected_after:
            classification = "applied"
            self._confirmed = expected_after
            self._index += 1
        else:
            self._record("reconciliation_unresolved", self._pending,
                         reason="partial_or_mixed_state", evidence=evidence_reference)
            return "partial_or_mixed_state"
        self._record("reconciled", self._pending, classification=classification,
                     evidence=evidence_reference, next_action="explicit_resume_required")
        self._pending = None
        self._state = "reconciled"
        return classification

    def resume(self) -> None:
        self._owned()
        if self._state != "reconciled" or self._objects != self._confirmed:
            raise TransactionError("resume requires explicit successful current-state reconciliation")
        self._state = "complete" if self._index == len(self.operations) else "ready"
        self._record("explicit_resume", boundary=str(self._index))

    def close(self) -> None:
        self._owned()
        if self._state != "complete":
            raise TransactionError("incomplete or uncertain sessions retain ownership")
        self.registry.release(self.session_id, self.resource_ids)
        self._state = "closed"
        self._record("session_closed")
