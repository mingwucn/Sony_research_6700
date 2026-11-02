# -*- coding: utf-8 -*-
"""Build standalone portable distribution of Sony α6700 Minimalist Customizer.

Generates:
  dist/SonyA6700Customizer/ (standalone folder with SonyA6700Customizer.exe & _internal/)
  dist/Sony_a6700_Customizer_v1.0.0_win64.zip (ready-to-distribute zip package)

The build is only accepted after the *shipped zip* is extracted into a fresh
temporary directory and its exe passes ``--self-test`` with a minimal PATH
(no Python/Conda directories), which mimics a machine without Python.
"""
from __future__ import annotations

import ast
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
APP_NAME = "SonyA6700Customizer"
APP_DIR = PROJECT_ROOT / "apps" / "a6700_customizer"
PAYLOADS_DIR = APP_DIR / "payloads"
VENDOR_DIR = PAYLOADS_DIR / "third_party" / "a6700_unlock"
ENTRY_SCRIPT = PROJECT_ROOT / "run_customizer.py"
ZIP_NAME = "Sony_a6700_Customizer_v1.0.0_win64.zip"

# DLLs that Conda's _ctypes/_tkinter/_lzma link against but PyInstaller
# cannot resolve because Conda keeps them in <prefix>\Library\bin.
CONDA_DLL_PATTERNS = ["ffi*.dll", "tcl86t.dll", "tk86t.dll", "liblzma.dll",
                      "libbz2.dll", "zlib.dll", "libexpat.dll", "sqlite3.dll"]


def check_prerequisites():
    print("[1/6] 检查构建环境与资源载荷...")
    try:
        import PyInstaller
        print(f"  ✓ PyInstaller 版本: {PyInstaller.__version__}")
    except ImportError:
        print("  正在自动安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    for mod in ("usb", "libusb_package"):
        if importlib.util.find_spec(mod) is None:
            print(f"  正在安装缺失依赖 {mod}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install",
                                   "pyusb" if mod == "usb" else "libusb-package"])

    required = [
        PAYLOADS_DIR / "native" / "dump_range.elf",
        PAYLOADS_DIR / "native" / "flash_write.elf",
        PAYLOADS_DIR / "third_party" / "libwdi" / "wdi-simple.exe",
        PAYLOADS_DIR / "libusb-1.0.dll",
        VENDOR_DIR / "usb" / "legacy.py",
        VENDOR_DIR / "LICENSE",
    ]
    for rf in required:
        if not rf.is_file():
            raise FileNotFoundError(f"缺少必要载荷文件: {rf}")
        print(f"  ✓ 载荷就绪: {rf.relative_to(PAYLOADS_DIR)} ({rf.stat().st_size:,} 字节)")


def vendor_hidden_imports() -> list[str]:
    """Stdlib/third-party modules imported by the source-shipped a6700_unlock tree.

    a6700_unlock is shipped as plain source (it loads reference modules from
    file paths), so PyInstaller cannot see its imports; list them explicitly.
    """
    stdlib = set(sys.stdlib_module_names)
    wanted: set[str] = set()

    def keep(name: str) -> bool:
        top = name.split(".")[0]
        return top in stdlib or top in ("usb", "libusb_package")

    for py in VENDOR_DIR.rglob("*.py"):
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    if keep(a.name):
                        wanted.add(a.name)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                if not keep(node.module):
                    continue
                wanted.add(node.module)
                for a in node.names:
                    sub = f"{node.module}.{a.name}"
                    try:
                        if importlib.util.find_spec(sub) is not None:
                            wanted.add(sub)
                    except (ImportError, ValueError, AttributeError):
                        pass
    # Platform-specific modules that do not exist on Windows.
    wanted -= {"fcntl", "termios", "pwd", "grp", "resource", "posix"}
    return sorted(m for m in wanted if importlib.util.find_spec(m.split(".")[0]) is not None)


def run_pyinstaller():
    print("\n[2/6] 正在执行 PyInstaller 打包构建 (便携目录模式)...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean", "--onedir", "--windowed",
        "--name", APP_NAME,
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
        "--specpath", str(BUILD_DIR),
        "--paths", str(APP_DIR),  # vendored a6700win
        "--add-data", f"{PAYLOADS_DIR / 'native'};native",
        "--add-data", f"{PAYLOADS_DIR / 'third_party' / 'libwdi'};third_party/libwdi",
        "--add-data", f"{VENDOR_DIR};third_party/a6700_unlock",
        "--add-binary", f"{PAYLOADS_DIR / 'libusb-1.0.dll'};.",
        "--collect-all", "libusb_package",
        "--exclude-module", "PySide6",
        "--exclude-module", "PyQt5",
        "--exclude-module", "PyQt6",
    ]

    conda_bin = Path(sys.prefix) / "Library" / "bin"
    if conda_bin.is_dir():
        cmd += ["--paths", str(conda_bin)]
        for pat in CONDA_DLL_PATTERNS:
            for dll in conda_bin.glob(pat):
                cmd += ["--add-binary", f"{dll};."]

    hidden = vendor_hidden_imports() + [
        "ctypes", "ctypes.wintypes", "usb.core", "usb.util", "usb.backend.libusb1",
        "tkinter", "tkinter.ttk", "tkinter.messagebox",
    ]
    for mod in sorted(set(hidden)):
        cmd += ["--hidden-import", mod]
    print(f"  隐式依赖模块: {len(set(hidden))} 个")

    cmd.append(str(ENTRY_SCRIPT))
    res = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    if res.returncode != 0:
        raise RuntimeError(f"PyInstaller 构建失败，退出码: {res.returncode}")
    print("  ✓ PyInstaller 构建成功！")


def copy_distribution_assets():
    print("\n[3/6] 复制发布文档、许可证与快捷启动引导...")
    out_dir = DIST_DIR / APP_NAME
    if not out_dir.is_dir():
        raise FileNotFoundError(f"未找到构建输出目录: {out_dir}")

    user_guide_src = PROJECT_ROOT / "docs" / "USER_GUIDE_CN.md"
    if user_guide_src.is_file():
        shutil.copy2(user_guide_src, out_dir / "使用手册_USER_GUIDE.md")
        print("  ✓ 已添加: 使用手册_USER_GUIDE.md")

    licenses = out_dir / "licenses"
    licenses.mkdir(exist_ok=True)
    shutil.copy2(VENDOR_DIR / "LICENSE", licenses / "a6700_unlock-GPL-3.0.txt")
    print("  ✓ 已添加: licenses/a6700_unlock-GPL-3.0.txt")

    launcher_bat = out_dir / "启动_Sony_a6700定制工具.bat"
    with launcher_bat.open("w", encoding="gbk") as f:
        f.write("@echo off\r\n")
        f.write("cd /d \"%~dp0\"\r\n")
        f.write(f"start \"\" \"{APP_NAME}.exe\"\r\n")
    print("  ✓ 已添加: 启动_Sony_a6700定制工具.bat")


def create_zip_package() -> Path:
    print("\n[4/6] 正在打包压缩为发布 zip 文件...")
    target_dir = DIST_DIR / APP_NAME
    zip_path = DIST_DIR / ZIP_NAME
    if zip_path.is_file():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(target_dir):
            for file in files:
                full_path = Path(root) / file
                zf.write(full_path, full_path.relative_to(DIST_DIR))
    print(f"  ✓ 压缩包生成完成: {zip_path.name} ({zip_path.stat().st_size / 1048576:.2f} MB)")
    return zip_path


def _clean_env() -> dict:
    """Environment without Python/Conda on PATH, like a fresh user machine."""
    system_root = os.environ.get("SystemRoot", r"C:\Windows")
    env = {k: v for k, v in os.environ.items()
           if k.upper() not in {"PATH", "PYTHONPATH", "PYTHONHOME", "TCL_LIBRARY",
                                "TK_LIBRARY", "CONDA_PREFIX", "CONDA_DEFAULT_ENV"}}
    env["PATH"] = os.pathsep.join([str(Path(system_root) / "System32"), system_root])
    return env


def self_test_zip(zip_path: Path):
    print("\n[5/6] 解压发布 zip 至全新临时目录，以纯净 PATH 运行 --self-test ...")
    with tempfile.TemporaryDirectory(prefix="a6700_selftest_") as tmp:
        tmp_path = Path(tmp)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(tmp_path)
        exe = tmp_path / APP_NAME / f"{APP_NAME}.exe"
        result_file = tmp_path / "selftest.json"
        proc = subprocess.Popen([str(exe), "--self-test", str(result_file)],
                                env=_clean_env(), cwd=str(tmp_path))
        try:
            code = proc.wait(timeout=60)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            raise RuntimeError("自测超时（很可能弹出了启动异常对话框）")

        if not result_file.is_file():
            raise RuntimeError(f"自测未生成结果文件，退出码 {code}（启动阶段即崩溃）")
        result = json.loads(result_file.read_text(encoding="utf-8"))
        for c in result["checks"]:
            mark = "✓" if c["ok"] else "✗"
            detail = c["detail"].strip().splitlines()[-1] if c["detail"].strip() else ""
            print(f"  {mark} {c['name']}: {detail[:160]}")
        if code != 0 or not result["ok"]:
            failed = [c for c in result["checks"] if not c["ok"]]
            for c in failed:
                print(f"\n--- {c['name']} ---\n{c['detail']}")
            raise RuntimeError(f"自测失败（退出码 {code}）")
        print("  ✓ 发布包在纯净环境下自测全部通过！")


def main():
    try:
        check_prerequisites()
        run_pyinstaller()
        copy_distribution_assets()
        zip_file = create_zip_package()
        self_test_zip(zip_file)
        print("\n[6/6] 完成")
        print("========================================================")
        print("✅ 独立绿色免安装发布包已就绪并通过自测:")
        print(f"   文件夹: {DIST_DIR / APP_NAME}")
        print(f"   压缩包: {zip_file}")
        print("========================================================")
    except Exception as exc:
        print(f"\n❌ 构建失败: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
