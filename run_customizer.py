# -*- coding: utf-8 -*-
"""Sony α6700 Minimalist Customizer - Desktop App Launcher.

Entry point for both direct python execution and PyInstaller freeze.

``--self-test <result.json>`` runs an offline, device-free startup check
(imports, Tk window, payload/driver/libusb resolution, USB auth modules)
and exits with code 0 on success. It never opens a USB device.
"""
from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

APP_DIR = PROJECT_ROOT / "apps" / "a6700_customizer"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


def _self_test(out_path: Path) -> int:
    checks: list[dict] = []

    def check(name, fn):
        try:
            detail = fn()
            checks.append({"name": name, "ok": True, "detail": str(detail)})
        except BaseException:  # noqa: BLE001 - report everything
            checks.append({"name": name, "ok": False, "detail": traceback.format_exc()})

    state = {}

    def import_gui():
        from apps.a6700_customizer import app_gui
        state["app_gui"] = app_gui
        return "ok"

    check("import_gui_and_backend", import_gui)

    if "app_gui" in state:
        from apps.a6700_customizer import app_backend
        from a6700win import dump, flash, paths
        from a6700win.usb import driver, windows_auth

        def tk_window():
            app = state["app_gui"].SonyCustomizerApp()
            app.update_idletasks()
            title = app.title()
            app.destroy()
            return title

        def payloads():
            return f"flash={len(flash.payload())}B dump={len(dump.payload())}B dir={flash.payload_dir()}"

        def wdi():
            exe = driver.wdi_executable()
            if not Path(exe).is_file():
                raise FileNotFoundError(exe)
            return exe

        def libusb():
            import ctypes
            path = windows_auth.libusb_library_path()
            ctypes.CDLL(path)
            from usb.backend import libusb1
            backend = libusb1.get_backend(find_library=lambda _name: path)
            if backend is None:
                raise RuntimeError("pyusb libusb1 backend unavailable")
            return path

        def auth_modules():
            paths.ensure_vendor_on_path()
            from a6700_unlock.usb import legacy  # loads PMCA reference modules
            return legacy.__file__

        def state_dir():
            return app_backend.default_state_dir()

        def elevated_worker_noop():
            import subprocess
            import tempfile
            with tempfile.TemporaryDirectory(prefix="a6700_worker_") as tmp:
                tmp_dir = Path(tmp)
                req = tmp_dir / "request.json"
                st = tmp_dir / "status.json"
                req.write_text(
                    json.dumps({"pids": [], "executable": "", "destination": tmp, "status_path": str(st)}),
                    encoding="utf-8",
                )
                cmd = driver._self_command(req)
                proc = subprocess.run(cmd, timeout=20, capture_output=True, text=True)
                if proc.returncode != 0 or not st.is_file():
                    raise RuntimeError(f"worker rc={proc.returncode} status_exists={st.is_file()}")
                status = json.loads(st.read_text(encoding="utf-8"))
                if not status.get("ok"):
                    raise RuntimeError(f"worker status={status}")
                return f"cmd={cmd[0]} ok=True"

        check("tk_window", tk_window)
        check("native_payloads", payloads)
        check("wdi_simple", wdi)
        check("libusb_load", libusb)
        check("usb_auth_modules", auth_modules)
        check("state_dir", state_dir)
        check("elevated_worker", elevated_worker_noop)

    ok = all(c["ok"] for c in checks)
    result = {
        "ok": ok,
        "frozen": bool(getattr(sys, "frozen", False)),
        "executable": sys.executable,
        "checks": checks,
    }
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if ok else 1


def main() -> None:
    if len(sys.argv) >= 3 and sys.argv[1] == "--elevated-worker":
        from apps.a6700_customizer import app_backend  # noqa: F401 - initializes paths/vendor
        from a6700win.usb import driver
        code = driver.run_elevated_worker(sys.argv[2])
        sys.stdout and sys.stdout.flush()
        os._exit(code)

    if len(sys.argv) >= 3 and sys.argv[1] == "--self-test":
        code = _self_test(Path(sys.argv[2]))
        sys.stdout and sys.stdout.flush()
        os._exit(code)

    from apps.a6700_customizer.app_gui import main as gui_main
    gui_main()


if __name__ == "__main__":
    main()
