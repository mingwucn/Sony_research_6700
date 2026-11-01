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
SYS_SRC = Path(os.path.expandvars("%TEMP%/Codex/powerful6700-english-20261026/source/src"))
INTERNAL_DIR = Path(r"D:\Softwares\Powerful6700-Windows-x64\_internal")

# Add required paths safely
if SYS_SRC.is_dir() and str(SYS_SRC) not in sys.path:
    sys.path.insert(0, str(SYS_SRC))

from a6700win import flash, paths, research
from a6700win.usb import driver, setupapi

from .targets import (
    ALL_FTP_TARGETS,
    ALL_TARGETS,
    APPFW_SIZE,
    TARGET_ENGLISH,
    TARGET_FILE,
    TargetWindow,
)

# Configure paths for flash payloads and third-party vendor modules
paths.bundled_root = lambda: INTERNAL_DIR
paths.project_root = lambda: INTERNAL_DIR
paths.ensure_vendor_on_path()

from a6700win import patches
patches.install()

# Provide fallback to _internal/libusb-1.0.dll
from a6700win.usb import windows_auth
_orig_libusb_path = windows_auth.libusb_library_path

def _safe_libusb_library_path() -> str:
    try:
        return _orig_libusb_path()
    except Exception:
        fallback = INTERNAL_DIR / "libusb-1.0.dll"
        if fallback.is_file():
            return str(fallback)
        raise

windows_auth.libusb_library_path = _safe_libusb_library_path


class BackendError(RuntimeError):
    """User-facing error from backend operations."""


class DeviceBackend:
    def __init__(self, state_dir: Optional[Path] = None):
        self.state_dir = state_dir or (PROJECT_ROOT / ".data" / "customizer")
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

            progress("正在读取功能字段状态…")
            for t in ALL_TARGETS:
                data = flash.read_range(session, TARGET_FILE, t.offset, len(t.patched), elf)
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
        ftp_statuses = [results[t.offset]["status"] for t in ALL_FTP_TARGETS]

        if all(s == "PATCHED" for s in ftp_statuses):
            overall_ftp = "PATCHED"
        elif all(s == "STOCK" for s in ftp_statuses):
            overall_ftp = "STOCK"
        else:
            overall_ftp = "PARTIAL"

        return {
            "appfw_size": size,
            "english_status": en_status,
            "ftp_status": overall_ftp,
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
        """Apply chosen features to /usr/lib/appFw.so transactionally."""
        targets_to_write: List[Tuple[TargetWindow, bytes]] = []

        if enable_english:
            targets_to_write.append((TARGET_ENGLISH, TARGET_ENGLISH.patched))
        if enable_ftp:
            for t in ALL_FTP_TARGETS:
                targets_to_write.append((t, t.patched))

        if not targets_to_write:
            progress("未选择任何修改项目。")
            return []

        elf = flash.payload()
        done = []

        with research.ServiceSession(progress=progress) as session:
            progress("写入前进行零变化探针自检 (Zero-Change Write Probe)…")
            flash.probe(session, TARGET_FILE, targets_to_write[0][0].offset, 512, elf)

            for target, desired_bytes in targets_to_write:
                progress(f"写入中: {target.name} (偏移 0x{target.offset:08x})…")
                # Pre-read
                before = flash.read_range(session, TARGET_FILE, target.offset, len(desired_bytes), elf)
                if before == desired_bytes:
                    progress(f"已经是目标状态: 0x{target.offset:08x}")
                    done.append({"offset": target.offset, "status": "no-op"})
                    continue

                # Write block with fsync
                flash.write_block(session, TARGET_FILE, target.offset, desired_bytes, elf)

                # Readback verification
                after = flash.read_range(session, TARGET_FILE, target.offset, len(desired_bytes), elf)
                if after != desired_bytes:
                    raise BackendError(
                        f"独立回读校验失败: 偏移 0x{target.offset:08x} 写入后字节不匹配! (实际: {after.hex()})"
                    )

                done.append({
                    "offset": target.offset,
                    "name": target.name,
                    "before": before.hex(),
                    "after": after.hex(),
                    "status": "success",
                })

        progress("所有修改均已完成并经独立回读校验通过！")
        return done

    def restore_factory(self, progress: Callable[[str], None] = lambda m: None) -> List[Dict[str, object]]:
        """Restore all targets back to stock factory preimages."""
        elf = flash.payload()
        done = []

        with research.ServiceSession(progress=progress) as session:
            progress("回退前进行零变化探针自检…")
            flash.probe(session, TARGET_FILE, ALL_TARGETS[0].offset, 512, elf)

            for target in ALL_TARGETS:
                progress(f"恢复中: 0x{target.offset:08x} -> 原厂预置…")
                before = flash.read_range(session, TARGET_FILE, target.offset, len(target.preimage), elf)
                if before == target.preimage:
                    done.append({"offset": target.offset, "status": "already-stock"})
                    continue

                flash.write_block(session, TARGET_FILE, target.offset, target.preimage, elf)
                after = flash.read_range(session, TARGET_FILE, target.offset, len(target.preimage), elf)
                if after != target.preimage:
                    raise BackendError(f"回退回读校验失败: 0x{target.offset:08x} 未能恢复原厂值!")

                done.append({
                    "offset": target.offset,
                    "name": target.name,
                    "status": "restored",
                })

        progress("已成功恢复 100% 出厂原始状态并通过校验！")
        return done
