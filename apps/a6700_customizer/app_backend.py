"""Backend service connecting to Sony α6700 via service mode.

Uses the verified Windows WinUSB / Senser service communication and
native flash_write.elf payload from Powerful6700-Windows.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = Path(__file__).resolve().parent

# Use only the vendored a6700win copy shipped next to this module.
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))


def default_state_dir() -> Path:
    """Writable state/backup directory: next to the exe when frozen."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "data"
    return PROJECT_ROOT / ".data" / "customizer"


def get_resource_root() -> Path:
    """Resolve base directory containing native/ and third_party/ payloads."""
    # 1. PyInstaller frozen environment
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass and (Path(meipass) / "native").is_dir():
            return Path(meipass)
        exe_dir = Path(sys.executable).resolve().parent
        for cand in [exe_dir / "_internal", exe_dir]:
            if (cand / "native").is_dir():
                return cand

    # 2. Local payloads directory in source tree
    local_payloads = PACKAGE_DIR / "payloads"
    if (local_payloads / "native").is_dir():
        return local_payloads

    # 3. Environment override or external Powerful6700 fallback
    env_root = os.environ.get("POWERFUL6700_ROOT")
    if env_root:
        p = Path(env_root) / "_internal"
        if (p / "native").is_dir():
            return p
    powerful_internal = Path(r"D:\Softwares\Powerful6700-Windows-x64\_internal")
    if (powerful_internal / "native").is_dir():
        return powerful_internal

    return local_payloads


INTERNAL_DIR = get_resource_root()

from a6700win import flash, paths, research
from a6700win.usb import driver, setupapi

from .recovery_journal import JournalStatus, RecoveryJournal, SpanClassification
from .targets import (
    ALL_FTP_TARGETS,
    ALL_TARGETS,
    APPFW_SIZE,
    INTERLEAVED_PRESERVED_BYTES,
    LOGICAL_CHANGED_BYTES,
    LOGICAL_TARGET_COUNT,
    PHYSICAL_SPANS_COUNT,
    PHYSICAL_WRITE_FOOTPRINT_BYTES,
    TARGET_ENGLISH,
    TARGET_FILE,
    TARGET_FTP_GALLERY_MENUS,
    TARGET_FTP_NETWORK_SETTINGS,
    TARGET_FTP_PLAYBACK_KEY,
    TargetSpan,
    TargetWindow,
    build_target_spans,
)


def get_writable_root() -> Path:
    """Resolve writable root directory (next to exe when frozen, repo root in source)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return PROJECT_ROOT


# Configure paths for flash payloads and third-party vendor modules
paths._root = None
paths.bundled_root = get_resource_root


def _safe_payload_dir() -> Path:
    p = get_resource_root() / "native"
    if (p / "flash_write.elf").is_file():
        return p
    raise BackendError(f"未找到 native 写入载荷，搜寻路径: {p}")


flash.payload_dir = _safe_payload_dir


def _safe_libusb_library_path() -> str:
    """Resolve libusb-1.0.dll location across dev, portable, and external installs."""
    try:
        import libusb_package
        dll_path = libusb_package.get_library_path()
        if dll_path and Path(dll_path).is_file():
            return str(dll_path)
    except Exception:
        pass
    root = get_resource_root()
    for cand in [
        root / "libusb-1.0.dll",
        root / "_internal" / "libusb-1.0.dll",
        PACKAGE_DIR / "payloads" / "libusb-1.0.dll",
        Path(r"D:\Softwares\Powerful6700-Windows-x64\_internal\libusb-1.0.dll"),
    ]:
        if cand.is_file():
            return str(cand)
    raise BackendError("未找到 libusb-1.0.dll，请确认安装包完整。")


from a6700win.usb import windows_auth
windows_auth.libusb_library_path = _safe_libusb_library_path


class BackendError(RuntimeError):
    """User-facing error from backend operations."""


class DeviceBackend:
    def __init__(self, state_dir: Optional[Path] = None):
        self.state_dir = state_dir or default_state_dir()
        self.backup_dir = self.state_dir / "backups"
        self.journals_dir = self.state_dir / "journals"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.journals_dir.mkdir(parents=True, exist_ok=True)

    def get_unresolved_journal(self) -> Optional[RecoveryJournal]:
        """Return the latest journal that has not committed or reverted."""
        return RecoveryJournal.find_latest_unresolved(self.journals_dir)

    def check_driver(self) -> Dict[str, object]:
        """Check whether WinUSB driver is bound for Sony PIDs."""
        try:
            info = driver.scan()
            pids = info.get("enumeration", {}).get("pids", [])
            devs = info.get("devices", [])
            winusb_ok = any(d.get("service", "").lower() == "winusb" for d in devs)
            return {
                "ok": winusb_ok,
                "pids": pids,
                "devices": devs,
                "admin": info.get("admin", False),
                "driver_required": info.get("driver_required", False),
                "message": "WinUSB 驱动已就绪" if winusb_ok else ("检测到相机，但需要绑定 WinUSB 驱动" if devs else "未检测到 USB 相机（请确认开机并设为 MSC 模式）"),
            }
        except Exception as exc:
            return {"ok": False, "devices": [], "message": f"驱动检查异常: {exc}"}

    def install_driver(
        self,
        pids: Optional[List[int]] = None,
        progress: Callable[[str], None] = lambda m: None,
    ) -> Dict[str, object]:
        """Trigger WinUSB driver binding via UAC for supported camera PIDs."""
        try:
            target_pids = pids if pids is not None else list(driver.SUPPORTED_PIDS)
            if not isinstance(target_pids, (list, tuple)):
                target_pids = [target_pids]
            return driver.install(target_pids, progress=progress)
        except Exception as exc:
            raise BackendError(f"安装驱动失败: {exc}")

    def inspect_device(self, progress: Callable[[str], None] = lambda m: None) -> Dict[str, object]:
        """Read target offsets in /usr/lib/appFw.so and determine feature status."""
        progress("正在连接相机并认证 USB 服务模式…")
        elf = flash.payload()

        results = {}
        with research.ServiceSession(progress=progress) as session:
            progress("正在验证固件目标文件 /usr/lib/appFw.so…")
            size = flash.stat(session, TARGET_FILE, elf)
            if size != APPFW_SIZE:
                raise BackendError(f"目标文件大小不符: 实际 {size} 字节，预期 {APPFW_SIZE} 字节 (非 2.00 固件)")

            progress("正在读取功能字段状态（7 段分批预读）…")
            spans = build_target_spans(ALL_TARGETS)
            for s_idx, span in enumerate(spans, start=1):
                progress(f"正在读取固件段 ({s_idx}/{len(spans)}): 0x{span.offset:08x} ({span.length} 字节)…")
                chunk = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                for t in span.targets:
                    rel = t.offset - span.offset
                    data = chunk[rel : rel + len(t.patched)]
                    if data == t.patched:
                        status = "PATCHED"
                    elif data == t.preimage:
                        status = "STOCK"
                    else:
                        status = "MISMATCH"
                    results[t.offset] = {
                        "target": t,
                        "actual_bytes": data.hex(),
                        "status": status,
                    }

        # Analyze overall feature statuses
        en_status = results[TARGET_ENGLISH.offset]["status"]
        network_patched = all(results[t.offset]["status"] == "PATCHED" for t in TARGET_FTP_NETWORK_SETTINGS)
        playback_key_patched = (results[TARGET_FTP_PLAYBACK_KEY.offset]["status"] == "PATCHED")
        gallery_menus_patched = all(
            results[t.offset]["status"] == "PATCHED"
            for t in TARGET_FTP_GALLERY_MENUS
            if t.preimage != t.patched
        )
        full_ftp_patched = network_patched and playback_key_patched and gallery_menus_patched

        if full_ftp_patched:
            overall_ftp = "PATCHED"
            ftp_note = "功能已开放 (网络配置菜单、相册回放选择传输菜单与按键动作已生效)"
        elif network_patched and not (playback_key_patched and gallery_menus_patched):
            overall_ftp = "PARTIAL"
            ftp_note = "检测到已开启基础网络 FTP 菜单（如曾用 Powerful6700 或早期版本），相册回放传输完整菜单尚未开放。勾选后将补充写入相册回放权限段，相机内已存的服务器与 Wi-Fi 配置完整保留。"
        elif not network_patched and (playback_key_patched or gallery_menus_patched):
            overall_ftp = "PARTIAL"
            ftp_note = "检测到相册回放菜单或按键已部分开放，但网络设置未完全开启。"
        else:
            overall_ftp = "STOCK"
            ftp_note = "原厂未启用"

        return {
            "appfw_size": size,
            "english_status": en_status,
            "ftp_status": overall_ftp,
            "ftp_note": ftp_note,
            "is_powerful6700_upgrade": (network_patched and not (playback_key_patched and gallery_menus_patched)),
            "details": results,
            "unresolved_journal": (self.get_unresolved_journal() is not None),
            "timestamp": datetime.datetime.now().isoformat(),
        }

    def perform_backup(self, inspection: Dict[str, object], progress: Callable[[str], None] = lambda m: None) -> Path:
        """Create a local verified backup of all inspected targets."""
        progress("正在保存相机原始状态备份…")
        stamp = time.strftime("%Y%m%d_%H%M%S")
        out_file = self.backup_dir / f"backup_a6700_{stamp}.json"

        data = {
            "timestamp": stamp,
            "model": "ILCE-6700",
            "firmware": "2.00",
            "target_file": TARGET_FILE,
            "targets": {},
        }
        for off, info in inspection["details"].items():
            t = info["target"]
            data["targets"][f"0x{off:08x}"] = {
                "name": t.name,
                "feature": t.feature,
                "offset": off,
                "bytes_hex": info["actual_bytes"],
                "status": info["status"],
            }

        with out_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        progress(f"备份已安全存盘: {out_file.name}")
        return out_file

    @staticmethod
    def _spans_for_journal(
        journal: Optional[RecoveryJournal], canonical_spans: List[TargetSpan]
    ) -> List[TargetSpan]:
        if journal is None:
            return canonical_spans
        recorded = journal.read_meta().get("spans") or []
        by_shape = {(span.offset, span.length): span for span in canonical_spans}
        spans = []
        for item in recorded:
            key = (item.get("offset"), item.get("length"))
            if key not in by_shape:
                raise BackendError(f"会话日志包含未知固件段: offset={key[0]}, length={key[1]}")
            spans.append(by_shape[key])
        if not spans:
            raise BackendError("会话日志未记录任何固件段，拒绝执行恢复操作。")
        return spans

    @staticmethod
    def _reference_buffers(
        journal: Optional[RecoveryJournal], span_index: int, span: TargetSpan, current: bytes
    ) -> Tuple[bytes, bytes]:
        """Return pre-operation and target buffers without mixing apply/restore semantics."""
        stock_saved = journal.load_stock_span_binary(span_index) if journal else None
        target_saved = journal.load_target_span_binary(span_index) if journal else None
        if stock_saved is not None and len(stock_saved) != span.length:
            raise BackendError(f"固件段 {span_index} 的写前快照长度不符，拒绝恢复。")
        if target_saved is not None and len(target_saved) != span.length:
            raise BackendError(f"固件段 {span_index} 的目标快照长度不符，拒绝恢复。")
        recorded_hashes = journal.prepared_span_hashes(span_index) if journal else {}
        for data, hash_key, label in (
            (stock_saved, "stock_sha256", "写前"),
            (target_saved, "target_sha256", "目标"),
        ):
            if data is not None:
                expected_hash = recorded_hashes.get(hash_key)
                actual_hash = hashlib.sha256(data).hexdigest()
                if not expected_hash or actual_hash != expected_hash:
                    raise BackendError(f"固件段 {span_index} 的{label}快照哈希校验失败，拒绝恢复。")

        mode = journal.read_meta().get("mode") if journal else "apply"
        if mode not in ("apply", "restore"):
            raise BackendError(f"未知会话模式 {mode!r}，拒绝推断恢复目标。")
        before_values = (lambda t: t.patched) if mode == "restore" else (lambda t: t.preimage)
        after_values = (lambda t: t.preimage) if mode == "restore" else (lambda t: t.patched)

        if stock_saved is not None:
            stock_ref = stock_saved
        else:
            ref = bytearray(current)
            for target in span.targets:
                rel = target.offset - span.offset
                value = before_values(target)
                ref[rel : rel + len(value)] = value
            stock_ref = bytes(ref)

        if target_saved is not None:
            target_ref = target_saved
        else:
            ref = bytearray(stock_ref)
            for target in span.targets:
                rel = target.offset - span.offset
                value = after_values(target)
                ref[rel : rel + len(value)] = value
            target_ref = bytes(ref)
        return stock_ref, target_ref

    @staticmethod
    def _reconciliation_findings(
        journal: RecoveryJournal, reconciliation: Optional[Dict[str, Any]], spans: List[TargetSpan]
    ) -> Dict[int, Dict[str, Any]]:
        if not reconciliation:
            raise BackendError("安全锁定：必须先完成只读对账扫描，才能回退或续写。")
        if reconciliation.get("session_id") != journal.read_meta().get("session_id"):
            raise BackendError("对账结果与当前会话不匹配，请重新执行只读对账。")
        findings = reconciliation.get("findings") or []
        if reconciliation.get("total_spans") != len(spans) or len(findings) != len(spans):
            raise BackendError("对账结果的固件段数量不匹配，请重新执行只读对账。")
        by_index = {item.get("span_index"): item for item in findings}
        if set(by_index) != set(range(1, len(spans) + 1)):
            raise BackendError("对账结果的固件段索引不完整，请重新执行只读对账。")
        return by_index

    @staticmethod
    def _check_scan_freshness(span_index: int, current: bytes, finding: Dict[str, Any]) -> None:
        current_hash = hashlib.sha256(current).hexdigest()
        if current_hash != finding.get("read_sha256"):
            raise BackendError(f"固件段 {span_index} 在对账后发生变化，已停止；请重新只读对账。")

    def reconcile_device(
        self,
        journal: Optional[RecoveryJournal] = None,
        progress: Callable[[str], None] = lambda m: None,
    ) -> Dict[str, Any]:
        """Read each journaled span and classify it against both saved states."""
        target_journal = journal or self.get_unresolved_journal()
        spans = self._spans_for_journal(target_journal, build_target_spans(ALL_TARGETS))
        findings = []

        progress("开始连接相机执行只读对账扫描 (Read-Only Reconciliation)…")
        elf = flash.payload()
        with research.ServiceSession(progress=progress) as session:
            size = flash.stat(session, TARGET_FILE, elf)
            if size != APPFW_SIZE:
                raise BackendError(f"目标固件大小不符: 实际 {size} 字节，预期 {APPFW_SIZE} 字节")

            for s_idx, span in enumerate(spans, start=1):
                progress(f"对账固件段 ({s_idx}/{len(spans)}): 0x{span.offset:08x} ({span.length} 字节)…")
                chunk = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                stock_ref, target_ref = self._reference_buffers(target_journal, s_idx, span, chunk)

                if chunk == stock_ref:
                    classification = SpanClassification.UNTOUCHED_STOCK.value
                    status_text = "与写前快照完全一致"
                elif chunk == target_ref:
                    classification = SpanClassification.FULLY_PATCHED.value
                    status_text = "已达到会话目标状态"
                else:
                    classification = SpanClassification.CORRUPTED_OR_PARTIAL.value
                    status_text = "数据不匹配或处于部分写入状态"

                findings.append({
                    "span_index": s_idx,
                    "offset": span.offset,
                    "length": span.length,
                    "target_count": len(span.targets),
                    "read_sha256": hashlib.sha256(chunk).hexdigest(),
                    "stock_sha256": hashlib.sha256(stock_ref).hexdigest(),
                    "target_sha256": hashlib.sha256(target_ref).hexdigest(),
                    "classification": classification,
                    "status_text": status_text,
                })

        if target_journal:
            target_journal.record_reconciliation(findings)

        untouched = sum(1 for f in findings if f["classification"] == SpanClassification.UNTOUCHED_STOCK.value)
        patched = sum(1 for f in findings if f["classification"] == SpanClassification.FULLY_PATCHED.value)
        corrupt = sum(1 for f in findings if f["classification"] == SpanClassification.CORRUPTED_OR_PARTIAL.value)
        summary = {
            "session_id": target_journal.read_meta().get("session_id") if target_journal else None,
            "total_spans": len(spans),
            "untouched_stock": untouched,
            "fully_patched": patched,
            "corrupted_or_partial": corrupt,
            "can_resume": corrupt == 0,
            "can_rollback": corrupt > 0 or patched > 0,
            "findings": findings,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        progress(f"对账扫描完成: 写前状态 {untouched}/{len(spans)}, 目标状态 {patched}/{len(spans)}, 异常/部分状态 {corrupt}/{len(spans)}")
        return summary

    def resume_interrupted_session(
        self,
        journal: Optional[RecoveryJournal] = None,
        reconciliation: Optional[Dict[str, Any]] = None,
        progress: Callable[[str], None] = lambda m: None,
    ) -> List[Dict[str, Any]]:
        """Resume only spans still at their pre-operation state after a fresh scan."""
        target_journal = journal or self.get_unresolved_journal()
        if not target_journal:
            raise BackendError("未找到需要续写的中断会话日志。")
        spans = self._spans_for_journal(target_journal, build_target_spans(ALL_TARGETS))
        findings = self._reconciliation_findings(target_journal, reconciliation, spans)
        if any(
            finding.get("classification") == SpanClassification.CORRUPTED_OR_PARTIAL.value
            for finding in findings.values()
        ):
            raise BackendError("存在异常或部分写入段，禁止续写；请重新对账并选择回退。")

        done = []
        try:
            elf = flash.payload()
            progress("正在连接相机，复核对账结果并准备续写…")
            with research.ServiceSession(progress=progress) as session:
                if flash.stat(session, TARGET_FILE, elf) != APPFW_SIZE:
                    raise BackendError("目标固件文件大小不符，拒绝续写。")
                current_by_index = {}
                references = {}
                for s_idx, span in enumerate(spans, start=1):
                    current = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                    self._check_scan_freshness(s_idx, current, findings[s_idx])
                    stock_ref, target_ref = self._reference_buffers(target_journal, s_idx, span, current)
                    classification = findings[s_idx].get("classification")
                    if classification == SpanClassification.UNTOUCHED_STOCK.value and current != stock_ref:
                        raise BackendError(f"固件段 {s_idx} 与写前快照分类不一致，已停止。")
                    if classification == SpanClassification.FULLY_PATCHED.value and current != target_ref:
                        raise BackendError(f"固件段 {s_idx} 与目标状态分类不一致，已停止。")
                    current_by_index[s_idx] = current
                    references[s_idx] = (stock_ref, target_ref)

                pending_indices = [
                    s_idx for s_idx, current in current_by_index.items()
                    if current == references[s_idx][0] and current != references[s_idx][1]
                ]
                if pending_indices:
                    for s_idx in pending_indices:
                        stock_ref, target_ref = references[s_idx]
                        target_journal.record_span_prepared(s_idx, spans[s_idx - 1], stock_ref, target_ref)
                    probe_span = spans[pending_indices[0] - 1]
                    progress("续写前在待写段的已保存快照范围内执行零变化探针…")
                    flash.probe(session, TARGET_FILE, probe_span.offset, min(512, probe_span.length), elf)
                for s_idx, span in enumerate(spans, start=1):
                    current = current_by_index[s_idx]
                    stock_ref, target_ref = references[s_idx]
                    if current == target_ref:
                        progress(f"固件段 {s_idx}/{len(spans)} 已达到目标状态，跳过物理写入。")
                        done.append({"span_index": s_idx, "status": "already-target"})
                        continue
                    if current != stock_ref:
                        raise BackendError(f"固件段 {s_idx} 不再匹配已批准的续写状态，已停止。")

                    target_journal.record_span_writing(s_idx, span)
                    progress(f"正在续写固件段 {s_idx}/{len(spans)}: 0x{span.offset:08x} ({span.length} 字节)…")
                    write_result = flash.write_block(session, TARGET_FILE, span.offset, target_ref, elf)
                    target_journal.record_span_written(s_idx, span, write_result)
                    readback = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                    target_journal.record_span_verified(s_idx, span, readback, target_ref)
                    done.append({"span_index": s_idx, "status": "resumed"})

            target_journal.record_commit()
            progress("会话所有固件段均已达到目标状态并通过全跨度逐字节校验。")
            return done
        except Exception as exc:
            target_journal.update_status(JournalStatus.NEEDS_REVIEW)
            raise BackendError(f"恢复续写异常中断: {exc}（会话已锁定为 NEEDS_REVIEW）") from exc

    def rollback_interrupted_session(
        self,
        journal: Optional[RecoveryJournal] = None,
        reconciliation: Optional[Dict[str, Any]] = None,
        progress: Callable[[str], None] = lambda m: None,
    ) -> List[Dict[str, Any]]:
        """Roll back changed spans to saved pre-operation binaries after reconciliation."""
        target_journal = journal or self.get_unresolved_journal()
        if not target_journal:
            raise BackendError("未找到需要回退的中断会话日志。")
        spans = self._spans_for_journal(target_journal, build_target_spans(ALL_TARGETS))
        findings = self._reconciliation_findings(target_journal, reconciliation, spans)

        stock_by_index = {}
        rollback_indices = []
        baseline_target_indices = set()
        for s_idx, span in enumerate(spans, start=1):
            stock_bytes = target_journal.load_stock_span_binary(s_idx)
            classification = findings[s_idx].get("classification")
            session_touched = target_journal.span_has_any_event(
                s_idx, ("SPAN_PREPARED", "SPAN_WRITING", "SPAN_WRITTEN", "SPAN_VERIFIED")
            )
            baseline_target = (
                classification == SpanClassification.FULLY_PATCHED.value
                and stock_bytes is None and not session_touched
            )
            if baseline_target:
                baseline_target_indices.add(s_idx)
                stock_by_index[s_idx] = None
                continue
            if classification != SpanClassification.UNTOUCHED_STOCK.value:
                if stock_bytes is None or len(stock_bytes) != span.length:
                    raise BackendError(f"固件段 {s_idx} 缺少完整写前原始快照，禁止开始回退。")
                rollback_indices.append(s_idx)
            stock_ref, _target_ref = self._reference_buffers(
                target_journal, s_idx, span, stock_bytes or bytes(span.length)
            )
            stock_by_index[s_idx] = stock_ref if stock_bytes is not None else None

        done = []
        try:
            elf = flash.payload()
            progress("正在连接相机，复核对账结果并准备回退…")
            with research.ServiceSession(progress=progress) as session:
                if flash.stat(session, TARGET_FILE, elf) != APPFW_SIZE:
                    raise BackendError("目标固件文件大小不符，拒绝回退。")
                for s_idx, span in enumerate(spans, start=1):
                    current = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                    self._check_scan_freshness(s_idx, current, findings[s_idx])

                if rollback_indices:
                    probe_span = spans[rollback_indices[0] - 1]
                    progress("回退前在已保存原始快照的范围内执行零变化探针…")
                    flash.probe(session, TARGET_FILE, probe_span.offset, min(512, probe_span.length), elf)
                for s_idx, span in enumerate(spans, start=1):
                    stock_bytes = stock_by_index[s_idx]
                    if findings[s_idx].get("classification") == SpanClassification.UNTOUCHED_STOCK.value:
                        progress(f"固件段 {s_idx}/{len(spans)} 尚未偏离写前状态，跳过写入。")
                        done.append({"span_index": s_idx, "status": "already-stock"})
                        continue
                    if s_idx in baseline_target_indices:
                        progress(f"固件段 {s_idx}/{len(spans)} 在会话前已是目标状态且无会话写事件，跳过回退。")
                        done.append({"span_index": s_idx, "status": "baseline-target"})
                        continue

                    target_journal.record_span_writing(s_idx, span)
                    progress(f"正在回退固件段 {s_idx}/{len(spans)}: 0x{span.offset:08x} ({span.length} 字节)…")
                    write_result = flash.write_block(session, TARGET_FILE, span.offset, stock_bytes, elf)
                    target_journal.record_span_written(s_idx, span, write_result)
                    readback = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                    target_journal.record_span_verified(s_idx, span, readback, stock_bytes)
                    done.append({"span_index": s_idx, "status": "rolled-back"})

            target_journal.update_status(JournalStatus.REVERTED)
            progress("所有已修改段均已恢复至写前快照并通过全跨度逐字节校验。")
            return done
        except Exception as exc:
            target_journal.update_status(JournalStatus.NEEDS_REVIEW)
            raise BackendError(f"回退过程异常中断: {exc}（会话已锁定为 NEEDS_REVIEW）") from exc

    def apply_features(
        self,
        enable_english: bool,
        enable_ftp: bool,
        progress: Callable[[str], None] = lambda m: None,
    ) -> List[Dict[str, object]]:
        """Validate and snapshot every selected span before any write command."""
        unresolved = self.get_unresolved_journal()
        if unresolved:
            meta = unresolved.read_meta()
            raise BackendError(
                f"安全锁定: 会话 {meta.get('session_id')} 状态为 {meta.get('status', 'UNKNOWN')}。\n"
                "严禁盲目重复写入；请先完成「会话恢复与对账」。"
            )

        targets_to_write: List[TargetWindow] = []
        if enable_english:
            targets_to_write.append(TARGET_ENGLISH)
        if enable_ftp:
            targets_to_write.extend(ALL_FTP_TARGETS)
        if not targets_to_write:
            progress("未选择任何修改项目。")
            return []

        spans = build_target_spans(targets_to_write)
        journal = RecoveryJournal.create(self.journals_dir, "apply", spans)
        done = []
        try:
            elf = flash.payload()
            with research.ServiceSession(progress=progress) as session:
                if flash.stat(session, TARGET_FILE, elf) != APPFW_SIZE:
                    raise BackendError("目标固件文件大小不符，拒绝写入。")

                prepared = {}
                for s_idx, span in enumerate(spans, start=1):
                    progress(f"预读并校验第 {s_idx}/{len(spans)} 固件段 (0x{span.offset:08x}, {span.length} 字节)…")
                    current_data = bytearray(flash.read_range(session, TARGET_FILE, span.offset, span.length, elf))
                    stock_original = bytes(current_data)
                    span_modified = False
                    for target in span.targets:
                        rel = target.offset - span.offset
                        cur = bytes(current_data[rel : rel + len(target.patched)])
                        if cur not in (target.preimage, target.patched):
                            err = (
                                f"固件预读校验不匹配: 目标 {target.name} (0x{target.offset:08x}) "
                                f"实际 {cur.hex()}，原厂 {target.preimage.hex()}，补丁 {target.patched.hex()}。"
                            )
                            journal.record_span_failed(s_idx, span, err)
                            raise BackendError(err)
                        if cur != target.patched:
                            current_data[rel : rel + len(target.patched)] = target.patched
                            span_modified = True
                    patched_target = bytes(current_data)
                    journal.record_span_prepared(s_idx, span, stock_original, patched_target)
                    prepared[s_idx] = (patched_target, span_modified)

                if any(modified for _target, modified in prepared.values()):
                    progress("全部段快照已落盘；在首个快照范围内执行零变化探针…")
                    flash.probe(session, TARGET_FILE, spans[0].offset, min(512, spans[0].length), elf)

                for s_idx, span in enumerate(spans, start=1):
                    patched_target, span_modified = prepared[s_idx]
                    if not span_modified:
                        progress(f"固件段 0x{span.offset:08x} 已全部达到目标状态，跳过物理写入。")
                        done.append({
                            "span_index": s_idx, "offset": span.offset,
                            "length": span.length, "status": "no-op",
                        })
                        continue

                    journal.record_span_writing(s_idx, span)
                    progress(f"正在写入固件段 {s_idx}/{len(spans)}（0x{span.offset:08x}, {span.length} 字节）并执行硬件 fsync…")
                    write_result = flash.write_block(session, TARGET_FILE, span.offset, patched_target, elf)
                    journal.record_span_written(s_idx, span, write_result)
                    verify_chunk = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                    journal.record_span_verified(s_idx, span, verify_chunk, patched_target)
                    done.append({
                        "span_index": s_idx, "offset": span.offset,
                        "length": span.length, "status": "success",
                    })

            journal.record_commit()
            progress("所选目标均已达到目标状态；实际写入段已通过全跨度逐字节独立回读校验。")
            return done
        except Exception as exc:
            journal.update_status(JournalStatus.NEEDS_REVIEW)
            raise BackendError(f"分段写入异常中断: {exc}（会话已锁定为 NEEDS_REVIEW，原始快照已安全留存）") from exc

    def restore_factory(self, progress: Callable[[str], None] = lambda m: None) -> List[Dict[str, object]]:
        """Validate and snapshot every managed span before restoring factory values."""
        unresolved = self.get_unresolved_journal()
        if unresolved:
            meta = unresolved.read_meta()
            raise BackendError(
                f"安全锁定: 会话 {meta.get('session_id')} 状态为 {meta.get('status', 'UNKNOWN')}。"
                "请先在「会话恢复与对账」中完成只读对账。"
            )
        spans = build_target_spans(ALL_TARGETS)
        journal = RecoveryJournal.create(self.journals_dir, "restore", spans)
        done = []

        try:
            elf = flash.payload()
            with research.ServiceSession(progress=progress) as session:
                if flash.stat(session, TARGET_FILE, elf) != APPFW_SIZE:
                    raise BackendError("目标固件文件大小不符，拒绝还原。")
                prepared = {}
                for s_idx, span in enumerate(spans, start=1):
                    progress(f"预读并校验恢复段 ({s_idx}/{len(spans)}): 0x{span.offset:08x}…")
                    current_data = bytearray(flash.read_range(session, TARGET_FILE, span.offset, span.length, elf))
                    before_data = bytes(current_data)
                    span_modified = False
                    for target in span.targets:
                        rel = target.offset - span.offset
                        cur = bytes(current_data[rel : rel + len(target.preimage)])
                        if cur not in (target.preimage, target.patched):
                            err = (
                                f"还原预读校验不匹配: 目标 {target.name} (0x{target.offset:08x}) "
                                f"实际 {cur.hex()}，既非原厂值亦非已审查补丁值。"
                            )
                            journal.record_span_failed(s_idx, span, err)
                            raise BackendError(err)
                        if cur != target.preimage:
                            current_data[rel : rel + len(target.preimage)] = target.preimage
                            span_modified = True
                    stock_target = bytes(current_data)
                    journal.record_span_prepared(s_idx, span, before_data, stock_target)
                    prepared[s_idx] = (stock_target, span_modified)

                if any(modified for _target, modified in prepared.values()):
                    progress("全部段快照已落盘；在首个快照范围内执行零变化探针…")
                    flash.probe(session, TARGET_FILE, spans[0].offset, min(512, spans[0].length), elf)

                for s_idx, span in enumerate(spans, start=1):
                    stock_target, span_modified = prepared[s_idx]
                    if not span_modified:
                        done.append({
                            "span_index": s_idx, "offset": span.offset,
                            "length": span.length, "status": "already-stock",
                        })
                        continue
                    journal.record_span_writing(s_idx, span)
                    progress(f"正在恢复段 0x{span.offset:08x}（{span.length} 字节）至原厂预置…")
                    write_result = flash.write_block(session, TARGET_FILE, span.offset, stock_target, elf)
                    journal.record_span_written(s_idx, span, write_result)
                    verify_chunk = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                    journal.record_span_verified(s_idx, span, verify_chunk, stock_target)
                    done.append({
                        "span_index": s_idx, "offset": span.offset,
                        "length": span.length, "status": "restored",
                    })

            journal.record_commit()
            progress("管理字段均已达到原厂预置；实际恢复段已通过全跨度逐字节校验。")
            return done
        except Exception as exc:
            journal.update_status(JournalStatus.NEEDS_REVIEW)
            raise BackendError(f"回退过程异常中断: {exc}（会话已锁定为 NEEDS_REVIEW）") from exc
