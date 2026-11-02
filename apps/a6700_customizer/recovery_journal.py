# -*- coding: utf-8 -*-
"""Durable Per-Span Transaction Journal and Recovery Manager for α6700 Customizer.

Implements AGENTS.md § Transaction and evidence rules & docs/ACCESS_AND_RECOVERY.md:
- Pre-writes full raw stock binary buffers to disk before any mutating command.
- Append-only JSONL journal recording explicit phase transitions per span.
- Strict fsync before and after modifying storage.
- Immediate 'NEEDS_REVIEW' lockout on timeout, disconnect, or byte mismatch.
- Re-opening and reconciliation state machine preventing unguided replay/rollback.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .targets import TargetSpan, TargetWindow


class JournalStatus(str, Enum):
    INITIALIZED = "INITIALIZED"
    IN_PROGRESS = "IN_PROGRESS"
    COMMITTED = "COMMITTED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    RECONCILED = "RECONCILED"
    REVERTED = "REVERTED"


class SpanClassification(str, Enum):
    UNTOUCHED_STOCK = "UNTOUCHED_STOCK"
    FULLY_PATCHED = "FULLY_PATCHED"
    CORRUPTED_OR_PARTIAL = "CORRUPTED_OR_PARTIAL"
    UNKNOWN = "UNKNOWN"


@dataclass
class JournalEvent:
    timestamp: str
    session_id: str
    event_type: str
    span_index: Optional[int] = None
    span_offset: Optional[int] = None
    span_length: Optional[int] = None
    stock_sha256: Optional[str] = None
    target_sha256: Optional[str] = None
    readback_sha256: Optional[str] = None
    detail: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

    def to_json_line(self) -> str:
        d = {k: v for k, v in asdict(self).items() if v is not None}
        return json.dumps(d, ensure_ascii=False)


class RecoveryJournal:
    """Manages an append-only per-span transaction journal on host storage."""

    def __init__(self, session_dir: Path):
        self.session_dir = session_dir
        self.journal_file = self.session_dir / "journal.jsonl"
        self.meta_file = self.session_dir / "meta.json"
        self.session_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def create(cls, base_dir: Path, mode: str, spans: List[TargetSpan]) -> "RecoveryJournal":
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        session_id = f"sess_{timestamp}_{mode}"
        session_dir = base_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=False)

        journal = cls(session_dir)
        meta = {
            "session_id": session_id,
            "mode": mode,
            "created_at": datetime.datetime.now().isoformat(),
            "status": JournalStatus.INITIALIZED.value,
            "span_count": len(spans),
            "spans": [
                {
                    "index": i,
                    "offset": s.offset,
                    "length": s.length,
                    "target_count": len(s.targets),
                }
                for i, s in enumerate(spans)
            ],
        }
        journal._write_meta(meta)
        journal.log_event(
            JournalEvent(
                timestamp=datetime.datetime.now().isoformat(),
                session_id=session_id,
                event_type="SESSION_START",
                detail=f"Initialized {mode} session with {len(spans)} spans",
                extra={"mode": mode, "span_count": len(spans)},
            )
        )
        return journal

    @classmethod
    def find_latest_unresolved(cls, base_dir: Path) -> Optional["RecoveryJournal"]:
        """Locate the latest session that has not committed or reverted."""
        if not base_dir.is_dir():
            return None
        unresolved_statuses = {
            JournalStatus.INITIALIZED.value,
            JournalStatus.IN_PROGRESS.value,
            JournalStatus.NEEDS_REVIEW.value,
            JournalStatus.RECONCILED.value,
        }
        terminal_statuses = {JournalStatus.COMMITTED.value, JournalStatus.REVERTED.value}
        candidate_dirs = sorted(base_dir.glob("sess_*"), reverse=True)
        for d in candidate_dirs:
            meta_path = d / "meta.json"
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except (OSError, ValueError, TypeError):
                # A damaged session record must fail closed, not unlock a new write.
                return cls(d)
            if not isinstance(meta, dict):
                return cls(d)
            status = meta.get("status")
            if status in unresolved_statuses or status not in terminal_statuses:
                return cls(d)
        return None

    def read_meta(self) -> Dict[str, Any]:
        if not self.meta_file.is_file():
            return {}
        return json.loads(self.meta_file.read_text(encoding="utf-8"))

    def _write_meta(self, meta: Dict[str, Any]) -> None:
        tmp = self.meta_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
        # Ensure fsync
        fd = os.open(str(tmp), os.O_RDWR)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
        tmp.replace(self.meta_file)

    def update_status(self, new_status: JournalStatus) -> None:
        meta = self.read_meta()
        meta["status"] = new_status.value
        meta["updated_at"] = datetime.datetime.now().isoformat()
        self._write_meta(meta)

    def log_event(self, event: JournalEvent) -> None:
        line = event.to_json_line() + "\n"
        with open(self.journal_file, "a", encoding="utf-8") as f:
            f.write(line)
            f.flush()
            os.fsync(f.fileno())

    def save_stock_span_binary(self, span_index: int, data: bytes) -> Path:
        """Preserve complete raw stock binary buffer to disk before any write."""
        bin_path = self.session_dir / f"span_{span_index:02d}_stock.bin"
        with open(bin_path, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        return bin_path

    def load_stock_span_binary(self, span_index: int) -> Optional[bytes]:
        bin_path = self.session_dir / f"span_{span_index:02d}_stock.bin"
        if bin_path.is_file():
            return bin_path.read_bytes()
        return None

    def save_target_span_binary(self, span_index: int, data: bytes) -> Path:
        """Preserve planned patched span buffer to disk."""
        bin_path = self.session_dir / f"span_{span_index:02d}_patched.bin"
        with open(bin_path, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        return bin_path

    def load_target_span_binary(self, span_index: int) -> Optional[bytes]:
        bin_path = self.session_dir / f"span_{span_index:02d}_patched.bin"
        if bin_path.is_file():
            return bin_path.read_bytes()
        return None

    def prepared_span_hashes(self, span_index: int) -> Dict[str, Optional[str]]:
        """Return the latest recorded hashes used to validate host-side snapshots."""
        if not self.journal_file.is_file():
            return {}
        with open(self.journal_file, "r", encoding="utf-8") as journal:
            for line in journal:
                event = json.loads(line)
                if event.get("event_type") == "SPAN_PREPARED" and event.get("span_index") == span_index:
                    return {
                        "stock_sha256": event.get("stock_sha256"),
                        "target_sha256": event.get("target_sha256"),
                    }
        return {}

    def span_has_any_event(self, span_index: int, event_types: Tuple[str, ...]) -> bool:
        if not self.journal_file.is_file():
            return False
        with open(self.journal_file, "r", encoding="utf-8") as journal:
            for line in journal:
                event = json.loads(line)
                if event.get("span_index") == span_index and event.get("event_type") in event_types:
                    return True
        return False

    def record_span_prepared(
        self, span_index: int, span: TargetSpan, stock_data: bytes, patched_data: bytes
    ) -> None:
        existing_stock = self.load_stock_span_binary(span_index)
        existing_target = self.load_target_span_binary(span_index)
        if existing_stock is not None or existing_target is not None:
            if existing_stock == stock_data and existing_target == patched_data:
                return
            raise RuntimeError(f"拒绝覆盖固件段 {span_index} 已存在的恢复快照。")
        self.save_stock_span_binary(span_index, stock_data)
        self.save_target_span_binary(span_index, patched_data)
        stock_hash = hashlib.sha256(stock_data).hexdigest()
        target_hash = hashlib.sha256(patched_data).hexdigest()

        self.update_status(JournalStatus.IN_PROGRESS)
        self.log_event(
            JournalEvent(
                timestamp=datetime.datetime.now().isoformat(),
                session_id=self.read_meta().get("session_id", ""),
                event_type="SPAN_PREPARED",
                span_index=span_index,
                span_offset=span.offset,
                span_length=span.length,
                stock_sha256=stock_hash,
                target_sha256=target_hash,
                detail=f"Span {span_index} prepared: stock {stock_hash[:8]}.. target {target_hash[:8]}..",
            )
        )

    def record_span_writing(self, span_index: int, span: TargetSpan) -> None:
        self.log_event(
            JournalEvent(
                timestamp=datetime.datetime.now().isoformat(),
                session_id=self.read_meta().get("session_id", ""),
                event_type="SPAN_WRITING",
                span_index=span_index,
                span_offset=span.offset,
                span_length=span.length,
                detail=f"Sending USB write command for span {span_index} (0x{span.offset:08x}, {span.length} B)",
            )
        )

    def record_span_written(self, span_index: int, span: TargetSpan, write_result: Dict[str, Any]) -> None:
        self.log_event(
            JournalEvent(
                timestamp=datetime.datetime.now().isoformat(),
                session_id=self.read_meta().get("session_id", ""),
                event_type="SPAN_WRITTEN",
                span_index=span_index,
                span_offset=span.offset,
                span_length=span.length,
                detail=f"Camera acknowledged write for span {span_index}",
                extra=write_result,
            )
        )

    def record_span_verified(
        self, span_index: int, span: TargetSpan, readback_data: bytes, expected_data: bytes
    ) -> None:
        readback_hash = hashlib.sha256(readback_data).hexdigest()
        expected_hash = hashlib.sha256(expected_data).hexdigest()

        if readback_data != expected_data:
            self.update_status(JournalStatus.NEEDS_REVIEW)
            self.log_event(
                JournalEvent(
                    timestamp=datetime.datetime.now().isoformat(),
                    session_id=self.read_meta().get("session_id", ""),
                    event_type="SPAN_VERIFICATION_FAILED",
                    span_index=span_index,
                    span_offset=span.offset,
                    span_length=span.length,
                    target_sha256=expected_hash,
                    readback_sha256=readback_hash,
                    detail=f"Full-span readback mismatch on span {span_index}! Expected {expected_hash}, got {readback_hash}",
                )
            )
            raise RuntimeError(
                f"全跨度回读校验失败: 固件段 {span_index} (0x{span.offset:08x}, {span.length} 字节) "
                f"回读哈希与预期哈希不符！已进入 NEEDS_REVIEW 锁定状态。"
            )

        self.log_event(
            JournalEvent(
                timestamp=datetime.datetime.now().isoformat(),
                session_id=self.read_meta().get("session_id", ""),
                event_type="SPAN_VERIFIED",
                span_index=span_index,
                span_offset=span.offset,
                span_length=span.length,
                readback_sha256=readback_hash,
                detail=f"Span {span_index} all {len(readback_data)} bytes verified bit-for-bit",
            )
        )

    def record_span_failed(self, span_index: int, span: TargetSpan, error_message: str) -> None:
        self.update_status(JournalStatus.NEEDS_REVIEW)
        self.log_event(
            JournalEvent(
                timestamp=datetime.datetime.now().isoformat(),
                session_id=self.read_meta().get("session_id", ""),
                event_type="SPAN_FAILED",
                span_index=span_index,
                span_offset=span.offset,
                span_length=span.length,
                detail=error_message,
            )
        )

    def record_commit(self) -> None:
        self.update_status(JournalStatus.COMMITTED)
        self.log_event(
            JournalEvent(
                timestamp=datetime.datetime.now().isoformat(),
                session_id=self.read_meta().get("session_id", ""),
                event_type="SESSION_COMMITTED",
                detail="All planned spans verified bit-for-bit and committed",
            )
        )

    def record_reconciliation(self, findings: List[Dict[str, Any]]) -> None:
        self.update_status(JournalStatus.RECONCILED)
        self.log_event(
            JournalEvent(
                timestamp=datetime.datetime.now().isoformat(),
                session_id=self.read_meta().get("session_id", ""),
                event_type="RECONCILIATION_COMPLETED",
                detail=f"Reconciliation completed for {len(findings)} spans",
                extra={"findings": findings},
            )
        )
