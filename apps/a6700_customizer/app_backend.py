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
        """Check if any transaction journal is in IN_PROGRESS or NEEDS_REVIEW."""
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

    def reconcile_device(
        self,
        journal: Optional[RecoveryJournal] = None,
        progress: Callable[[str], None] = lambda m: None,
    ) -> Dict[str, Any]:
        """Perform a read-only reconciliation scan on all target spans.

        Classifies each span against saved stock binaries or stock factory preimages:
        - UNTOUCHED_STOCK: 100% matches stock bytes.
        - FULLY_PATCHED: 100% matches expected target patched bytes.
        - CORRUPTED_OR_PARTIAL: Bytes mismatch both expected states.
        """
        target_journal = journal or self.get_unresolved_journal()
        elf = flash.payload()
        spans = build_target_spans(ALL_TARGETS)

        findings = []
        progress("开始连接相机执行只读对账扫描 (Read-Only Reconciliation)…")
        with research.ServiceSession(progress=progress) as session:
            size = flash.stat(session, TARGET_FILE, elf)
            if size != APPFW_SIZE:
                raise BackendError(f"目标固件大小不符: 实际 {size} 字节，预期 {APPFW_SIZE} 字节")

            for s_idx, span in enumerate(spans, start=1):
                progress(f"对账固件段 ({s_idx}/{len(spans)}): 0x{span.offset:08x} ({span.length} 字节)…")
                chunk = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                read_hash = hashlib.sha256(chunk).hexdigest()

                # Determine expected stock buffer
                stock_saved = target_journal.load_stock_span_binary(s_idx) if target_journal else None
                if stock_saved and len(stock_saved) == span.length:
                    stock_ref = stock_saved
                else:
                    ref = bytearray(chunk)
                    for t in span.targets:
                        rel = t.offset - span.offset
                        ref[rel : rel + len(t.preimage)] = t.preimage
                    stock_ref = bytes(ref)

                # Determine expected target buffer
                target_ref = bytearray(stock_ref)
                for t in span.targets:
                    rel = t.offset - span.offset
                    target_ref[rel : rel + len(t.patched)] = t.patched
                target_ref = bytes(target_ref)

                stock_hash = hashlib.sha256(stock_ref).hexdigest()
                target_hash = hashlib.sha256(target_ref).hexdigest()

                if chunk == stock_ref:
                    classification = SpanClassification.UNTOUCHED_STOCK.value
                    status_text = "完全处于出厂/未改动状态"
                elif chunk == target_ref:
                    classification = SpanClassification.FULLY_PATCHED.value
                    status_text = "已完整生效目标修改"
                else:
                    classification = SpanClassification.CORRUPTED_OR_PARTIAL.value
                    status_text = "数据不匹配或处于部分写入状态"

                findings.append({
                    "span_index": s_idx,
                    "offset": span.offset,
                    "length": span.length,
                    "target_count": len(span.targets),
                    "read_sha256": read_hash,
                    "stock_sha256": stock_hash,
                    "target_sha256": target_hash,
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
            "can_resume": (corrupt == 0 and patched < len(spans)),
            "can_rollback": (corrupt > 0 or patched > 0),
            "findings": findings,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        progress(f"对账扫描完成: 原厂状态 {untouched}/{len(spans)}, 目标状态 {patched}/{len(spans)}, 异常/部分状态 {corrupt}/{len(spans)}")
        return summary

    def rollback_interrupted_session(
        self,
        journal: Optional[RecoveryJournal] = None,
        progress: Callable[[str], None] = lambda m: None,
    ) -> List[Dict[str, Any]]:
        """Roll back all modified/interrupted spans to saved stock binaries."""
        target_journal = journal or self.get_unresolved_journal()
        if not target_journal:
            raise BackendError("未找到需要回退的中断会话日志。")

        elf = flash.payload()
        spans = build_target_spans(ALL_TARGETS)
        done = []

        progress("正在连接相机执行持久回退事务…")
        with research.ServiceSession(progress=progress) as session:
            flash.probe(session, TARGET_FILE, spans[0].offset, 512, elf)

            for s_idx, span in enumerate(spans, start=1):
                stock_bytes = target_journal.load_stock_span_binary(s_idx)
                if not stock_bytes or len(stock_bytes) != span.length:
                    current = bytearray(flash.read_range(session, TARGET_FILE, span.offset, span.length, elf))
                    for t in span.targets:
                        rel = t.offset - span.offset
                        current[rel : rel + len(t.preimage)] = t.preimage
                    stock_bytes = bytes(current)

                cur = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                if cur == stock_bytes:
                    progress(f"固件段 {s_idx}/{len(spans)} 0x{span.offset:08x} 已处于原厂状态，跳过写入。")
                    done.append({"span_index": s_idx, "status": "already_stock"})
                    continue

                progress(f"正在向相机回退固件段 {s_idx}/{len(spans)}: 0x{span.offset:08x} ({span.length} 字节)…")
                flash.write_block(session, TARGET_FILE, span.offset, stock_bytes, elf)

                progress(f"正在对段 {s_idx} 进行全跨度独立回读校验…")
                readback = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                if readback != stock_bytes:
                    raise BackendError(f"回退回读校验失败: 固件段 {s_idx} 未能恢复原厂数据！")

                done.append({"span_index": s_idx, "status": "rolled_back"})

        target_journal.update_status(JournalStatus.REVERTED)
        progress("中断会话已成功完全回退至原厂快照状态并通过全跨度校验！")
        return done

    def apply_features(
        self,
        enable_english: bool,
        enable_ftp: bool,
        progress: Callable[[str], None] = lambda m: None,
    ) -> List[Dict[str, object]]:
        """Apply chosen features using durable per-span journaling and full-span verification."""
        # 1. Enforce unresolved journal lockout
        unresolved = self.get_unresolved_journal()
        if unresolved:
            raise BackendError(
                f"安全锁定: 检测到上次写入会话 ({unresolved.read_meta().get('session_id')}) 处于未决或中断状态 (NEEDS_REVIEW)！\n"
                "严禁盲目尝试重复写入。请先执行「会话对账与恢复」，完成状态对账后再行操作。"
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
        elf = flash.payload()
        done = []

        try:
            with research.ServiceSession(progress=progress) as session:
                progress("写入前进行零变化探针自检 (Zero-Change Write Probe)…")
                flash.probe(session, TARGET_FILE, spans[0].offset, 512, elf)

                for s_idx, span in enumerate(spans, start=1):
                    progress(f"处理第 {s_idx}/{len(spans)} 固件段 (偏移 0x{span.offset:08x}, 跨度 {span.length} 字节)…")
                    # 1. Pre-read complete span from camera
                    current_data = bytearray(flash.read_range(session, TARGET_FILE, span.offset, span.length, elf))
                    stock_original = bytes(current_data)

                    # 2. Check each target within span and prepare patched span
                    span_modified = False
                    for t in span.targets:
                        rel = t.offset - span.offset
                        cur = bytes(current_data[rel : rel + len(t.patched)])
                        if cur != t.patched:
                            if cur != t.preimage and cur != t.patched:
                                err = (
                                    f"固件预读校验不匹配: 目标 {t.name} (0x{t.offset:08x}) 实际内容为 {cur.hex()}，"
                                    f"既非原厂预置 ({t.preimage.hex()}) 亦非补丁值 ({t.patched.hex()})，写入已终止以保护相机！"
                                )
                                journal.record_span_failed(s_idx, span, err)
                                raise BackendError(err)
                            current_data[rel : rel + len(t.patched)] = t.patched
                            span_modified = True

                    patched_target = bytes(current_data)

                    # 3. Durable journal: save complete stock binary and target binary to disk before writing
                    journal.record_span_prepared(s_idx, span, stock_original, patched_target)

                    if span_modified:
                        # 4. Write span
                        journal.record_span_writing(s_idx, span)
                        progress(f"正在写入固件段 {s_idx}/{len(spans)}（0x{span.offset:08x}, {span.length} 字节）并执行硬件 fsync…")
                        w_res = flash.write_block(session, TARGET_FILE, span.offset, patched_target, elf)
                        journal.record_span_written(s_idx, span, w_res)

                        # 5. Full-span readback verification (every single byte!)
                        progress(f"正在对固件段 {s_idx} 进行全跨度（{span.length} 字节全部比对）独立回读校验…")
                        verify_chunk = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                        journal.record_span_verified(s_idx, span, verify_chunk, patched_target)

                        done.append({
                            "span_index": s_idx,
                            "offset": span.offset,
                            "length": span.length,
                            "status": "success",
                        })
                    else:
                        progress(f"固件段 0x{span.offset:08x} 内所有目标均已为目标状态，跳过物理写入。")
                        done.append({
                            "span_index": s_idx,
                            "offset": span.offset,
                            "length": span.length,
                            "status": "no-op",
                        })

            journal.record_commit()
            progress("所有分段修改均已完成并经全跨度逐字节独立回读校验通过！")
            return done
        except Exception as exc:
            journal.update_status(JournalStatus.NEEDS_REVIEW)
            raise BackendError(f"分段写入异常中断: {exc}（会话已锁定为 NEEDS_REVIEW，原始快照已安全留存）")

    def restore_factory(self, progress: Callable[[str], None] = lambda m: None) -> List[Dict[str, object]]:
        """Restore all targets back to stock factory preimages with durable journaling."""
        spans = build_target_spans(ALL_TARGETS)
        journal = RecoveryJournal.create(self.journals_dir, "restore", spans)
        elf = flash.payload()
        done = []

        try:
            with research.ServiceSession(progress=progress) as session:
                progress("回退前进行零变化探针自检…")
                flash.probe(session, TARGET_FILE, ALL_TARGETS[0].offset, 512, elf)

                for s_idx, span in enumerate(spans, start=1):
                    progress(f"检查恢复固件段 ({s_idx}/{len(spans)}): 0x{span.offset:08x}…")
                    current_data = bytearray(flash.read_range(session, TARGET_FILE, span.offset, span.length, elf))
                    before_data = bytes(current_data)

                    span_modified = False
                    for t in span.targets:
                        rel = t.offset - span.offset
                        cur = bytes(current_data[rel : rel + len(t.preimage)])
                        if cur != t.preimage:
                            current_data[rel : rel + len(t.preimage)] = t.preimage
                            span_modified = True

                    stock_target = bytes(current_data)
                    journal.record_span_prepared(s_idx, span, before_data, stock_target)

                    if span_modified:
                        journal.record_span_writing(s_idx, span)
                        progress(f"正在恢复段 0x{span.offset:08x}（{span.length} 字节）至原厂预置…")
                        w_res = flash.write_block(session, TARGET_FILE, span.offset, stock_target, elf)
                        journal.record_span_written(s_idx, span, w_res)

                        progress(f"正在对固件段 {s_idx} 进行全跨度回退校验…")
                        verify_chunk = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                        journal.record_span_verified(s_idx, span, verify_chunk, stock_target)

                        done.append({
                            "span_index": s_idx,
                            "offset": span.offset,
                            "length": span.length,
                            "status": "restored",
                        })
                    else:
                        done.append({
                            "span_index": s_idx,
                            "offset": span.offset,
                            "length": span.length,
                            "status": "already-stock",
                        })

            journal.record_commit()
            progress("已成功恢复出厂原始预置并通过全跨度逐字节校验！")
            return done
        except Exception as exc:
            journal.update_status(JournalStatus.NEEDS_REVIEW)
            raise BackendError(f"回退过程异常中断: {exc}（会话已锁定为 NEEDS_REVIEW）")
