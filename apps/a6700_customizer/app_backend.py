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
from typing import Callable, Dict, List, Optional, Tuple

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

from .targets import (
    ALL_FTP_TARGETS,
    ALL_TARGETS,
    APPFW_SIZE,
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
paths.project_root = get_writable_root
paths.ensure_vendor_on_path()

from a6700win import patches
patches.install()

# Provide robust fallback to libusb-1.0.dll
from a6700win.usb import windows_auth
_orig_libusb_path = windows_auth.libusb_library_path

def _safe_libusb_library_path() -> str:
    try:
        return _orig_libusb_path()
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

windows_auth.libusb_library_path = _safe_libusb_library_path


class BackendError(RuntimeError):
    """User-facing error from backend operations."""


class DeviceBackend:
    def __init__(self, state_dir: Optional[Path] = None):
        self.state_dir = state_dir or default_state_dir()
        self.backup_dir = self.state_dir / "backups"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

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

            progress("正在高效批量预读功能字段状态…")
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
            ftp_note = "完整开放 (全网络菜单 + 完整相册回放选择传输菜单 + 回放快捷键已就绪)"
        elif network_patched and not (playback_key_patched and gallery_menus_patched):
            overall_ftp = "PARTIAL"
            ftp_note = "检测到已开启网络 FTP 菜单（如曾使用 Powerful6700 或早期版本），相册回放传输完整菜单尚未开启。本次写入将为您无损补齐【相册回放传输完整菜单 + 快捷键】，相机内原有的 FTP 服务器与 Wi-Fi 配置将被 100% 完整保留！"
        elif not network_patched and (playback_key_patched or gallery_menus_patched):
            overall_ftp = "PARTIAL"
            ftp_note = "检测到回放菜单或按键已部分修改，但网络设置未完全开启。"
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

    def apply_features(
        self,
        enable_english: bool,
        enable_ftp: bool,
        progress: Callable[[str], None] = lambda m: None,
    ) -> List[Dict[str, object]]:
        """Apply chosen features to /usr/lib/appFw.so transactionally using safe batched blocks."""
        targets_to_write: List[TargetWindow] = []

        if enable_english:
            targets_to_write.append(TARGET_ENGLISH)
        if enable_ftp:
            targets_to_write.extend(ALL_FTP_TARGETS)

        if not targets_to_write:
            progress("未选择任何修改项目。")
            return []

        spans = build_target_spans(targets_to_write)
        elf = flash.payload()
        done = []

        with research.ServiceSession(progress=progress) as session:
            progress("写入前进行零变化探针自检 (Zero-Change Write Probe)…")
            flash.probe(session, TARGET_FILE, spans[0].offset, 512, elf)

            for s_idx, span in enumerate(spans, start=1):
                progress(f"处理第 {s_idx}/{len(spans)} 固件段 (偏移 0x{span.offset:08x}, 跨度 {span.length} 字节)…")
                # Pre-read the span from camera
                current_data = bytearray(flash.read_range(session, TARGET_FILE, span.offset, span.length, elf))

                span_modified = False
                target_records = []
                for t in span.targets:
                    rel = t.offset - span.offset
                    cur = bytes(current_data[rel : rel + len(t.patched)])
                    target_records.append((t, rel, cur))
                    if cur != t.patched:
                        if cur != t.preimage and cur != t.patched:
                            raise BackendError(
                                f"固件预读校验不匹配: 目标 {t.name} (0x{t.offset:08x}) 实际内容为 {cur.hex()}，"
                                f"既非原厂预置 ({t.preimage.hex()}) 亦非补丁值 ({t.patched.hex()})，写入已终止以保护相机！"
                            )
                        current_data[rel : rel + len(t.patched)] = t.patched
                        span_modified = True

                if span_modified:
                    progress(f"正在写入固件段 0x{span.offset:08x}（{span.length} 字节）并执行硬件 fsync…")
                    flash.write_block(session, TARGET_FILE, span.offset, bytes(current_data), elf)

                    progress(f"正在对固件段 0x{span.offset:08x} 进行独立回读校验…")
                    verify_chunk = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                    for t, rel, before in target_records:
                        after = verify_chunk[rel : rel + len(t.patched)]
                        if after != t.patched:
                            raise BackendError(
                                f"独立回读校验失败: 目标 {t.name} (0x{t.offset:08x}) 写入后未生效 (实际: {after.hex()}, 预期: {t.patched.hex()})"
                            )
                        done.append({
                            "offset": t.offset,
                            "name": t.name,
                            "before": before.hex(),
                            "after": after.hex(),
                            "status": "success",
                        })
                else:
                    progress(f"固件段 0x{span.offset:08x} 内所有目标均已为目标状态，无需重复写入。")
                    for t, rel, before in target_records:
                        done.append({
                            "offset": t.offset,
                            "name": t.name,
                            "status": "no-op",
                        })

        progress("所有修改均已完成并经独立回读校验通过！")
        return done

    def restore_factory(self, progress: Callable[[str], None] = lambda m: None) -> List[Dict[str, object]]:
        """Restore all targets back to stock factory preimages using safe batched blocks."""
        spans = build_target_spans(ALL_TARGETS)
        elf = flash.payload()
        done = []

        with research.ServiceSession(progress=progress) as session:
            progress("回退前进行零变化探针自检…")
            flash.probe(session, TARGET_FILE, ALL_TARGETS[0].offset, 512, elf)

            for s_idx, span in enumerate(spans, start=1):
                progress(f"检查恢复固件段 ({s_idx}/{len(spans)}): 0x{span.offset:08x}…")
                current_data = bytearray(flash.read_range(session, TARGET_FILE, span.offset, span.length, elf))

                span_modified = False
                target_records = []
                for t in span.targets:
                    rel = t.offset - span.offset
                    cur = bytes(current_data[rel : rel + len(t.preimage)])
                    target_records.append((t, rel, cur))
                    if cur != t.preimage:
                        current_data[rel : rel + len(t.preimage)] = t.preimage
                        span_modified = True

                if span_modified:
                    progress(f"正在恢复段 0x{span.offset:08x}（{span.length} 字节）至原厂预置…")
                    flash.write_block(session, TARGET_FILE, span.offset, bytes(current_data), elf)

                    verify_chunk = flash.read_range(session, TARGET_FILE, span.offset, span.length, elf)
                    for t, rel, before in target_records:
                        after = verify_chunk[rel : rel + len(t.preimage)]
                        if after != t.preimage:
                            raise BackendError(
                                f"回退回读校验失败: 目标 {t.name} (0x{t.offset:08x}) 未能恢复原厂值!"
                            )
                        done.append({
                            "offset": t.offset,
                            "name": t.name,
                            "before": before.hex(),
                            "after": after.hex(),
                            "status": "restored",
                        })
                else:
                    for t, rel, before in target_records:
                        done.append({
                            "offset": t.offset,
                            "name": t.name,
                            "status": "already-stock",
                        })

        progress("已成功恢复 100% 出厂原始状态并通过校验！")
        return done
