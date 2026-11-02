# -*- coding: utf-8 -*-
"""Build standalone portable distribution of Sony α6700 Minimalist Customizer.

Generates:
  dist/SonyA6700Customizer/ (standalone folder with SonyA6700Customizer.exe & _internal/)
  dist/Sony_a6700_Customizer_v1.0.0_win64.zip (ready-to-distribute zip package)
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
APP_DIR = PROJECT_ROOT / "apps" / "a6700_customizer"
PAYLOADS_DIR = APP_DIR / "payloads"
ENTRY_SCRIPT = PROJECT_ROOT / "run_customizer.py"


def check_prerequisites():
    """Verify payloads and PyInstaller availability."""
    print("[1/5] 检查构建环境与资源载荷...")

    # 1. Check PyInstaller
    try:
        import PyInstaller
        print(f"  ✓ PyInstaller 版本: {PyInstaller.__version__}")
    except ImportError:
        print("  正在自动安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Check native payloads
    required_files = [
        PAYLOADS_DIR / "native" / "dump_range.elf",
        PAYLOADS_DIR / "native" / "flash_write.elf",
        PAYLOADS_DIR / "third_party" / "libwdi" / "wdi-simple.exe",
        PAYLOADS_DIR / "libusb-1.0.dll",
    ]
    for rf in required_files:
        if not rf.is_file():
            raise FileNotFoundError(f"缺少必要载荷文件: {rf}")
        print(f"  ✓ 载荷就绪: {rf.name} ({rf.stat().st_size:,} 字节)")


def run_pyinstaller():
    """Execute PyInstaller to bundle the application."""
    print("\n[2/5] 正在执行 PyInstaller 打包构建 (便携目录模式)...")

    native_src = str(PAYLOADS_DIR / "native")
    libwdi_src = str(PAYLOADS_DIR / "third_party" / "libwdi")
    libusb_src = str(PAYLOADS_DIR / "libusb-1.0.dll")

    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "SonyA6700Customizer",
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
    ]

    # If running inside a Conda environment, add Library/bin to paths
    conda_bin = Path(sys.prefix) / "Library" / "bin"
    if conda_bin.is_dir():
        cmd.extend(["--paths", str(conda_bin)])

    cmd.extend([
        # Add payloads
        "--add-data", f"{native_src};native",
        "--add-data", f"{libwdi_src};third_party/libwdi",
        "--add-data", f"{libusb_src};.",
        # Hidden imports
        "--hidden-import", "usb",
        "--hidden-import", "usb.core",
        "--hidden-import", "usb.util",
        "--hidden-import", "usb.backend.libusb1",
        "--hidden-import", "ctypes",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.messagebox",
        # Main entry
        str(ENTRY_SCRIPT),
    ])

    print("  执行命令:", " ".join(cmd))
    res = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    if res.returncode != 0:
        raise RuntimeError(f"PyInstaller 构建失败，退出码: {res.returncode}")
    print("  ✓ PyInstaller 构建成功！")


def copy_distribution_assets():
    """Add user manuals, runtime DLLs, and batch shortcuts to dist folder."""
    print("\n[3/5] 复制发布文档、运行时 DLL 与快捷启动引导...")
    out_dir = DIST_DIR / "SonyA6700Customizer"
    if not out_dir.is_dir():
        raise FileNotFoundError(f"未找到构建输出目录: {out_dir}")

    internal_dir = out_dir / "_internal"

    # Crucial: in Windows Conda environments, ensure ctypes/tk dependencies are bundled
    conda_bin = Path(sys.prefix) / "Library" / "bin"
    if conda_bin.is_dir():
        dll_patterns = ["ffi*.dll", "tcl86t.dll", "tk86t.dll", "liblzma.dll"]
        for pat in dll_patterns:
            for dll_file in conda_bin.glob(pat):
                dest = internal_dir / dll_file.name
                if not dest.is_file():
                    shutil.copy2(dll_file, dest)
                    print(f"  ✓ 补充 Conda 运行时 DLL: {dll_file.name}")

    # Copy user guide
    user_guide_src = PROJECT_ROOT / "docs" / "USER_GUIDE_CN.md"
    if user_guide_src.is_file():
        shutil.copy2(user_guide_src, out_dir / "使用手册_USER_GUIDE.md")
        print("  ✓ 已添加: 使用手册_USER_GUIDE.md")

    # Create convenient launcher bat in dist folder
    launcher_bat = out_dir / "启动_Sony_a6700定制工具.bat"
    with launcher_bat.open("w", encoding="gbk") as f:
        f.write("@echo off\r\n")
        f.write("cd /d \"%~dp0\"\r\n")
        f.write("start \"\" \"SonyA6700Customizer.exe\"\r\n")
    print("  ✓ 已添加: 启动_Sony_a6700定制工具.bat")


def create_zip_package() -> Path:
    """Compress dist directory into ready-to-share zip archive."""
    print("\n[4/5] 正在打包压缩为发布 zip 文件...")
    target_dir = DIST_DIR / "SonyA6700Customizer"
    zip_path = DIST_DIR / "Sony_a6700_Customizer_v1.0.0_win64.zip"

    if zip_path.is_file():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(target_dir):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(DIST_DIR)
                zf.write(full_path, rel_path)

    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"  ✓ 压缩包生成完成: {zip_path.name} ({size_mb:.2f} MB)")
    return zip_path


def verify_dist():
    """Check integrity of the output."""
    print("\n[5/5] 验证发布产物完整性与启动烟测...")
    exe_path = DIST_DIR / "SonyA6700Customizer" / "SonyA6700Customizer.exe"
    if not exe_path.is_file():
        raise FileNotFoundError(f"未找到主程序: {exe_path}")

    # Check payloads in _internal or app root
    internal_dir = DIST_DIR / "SonyA6700Customizer" / "_internal"
    native_elf = internal_dir / "native" / "flash_write.elf"
    libusb = internal_dir / "libusb-1.0.dll"

    if not native_elf.is_file():
        raise FileNotFoundError(f"构建目录缺少必要载荷: {native_elf}")
    if not libusb.is_file():
        raise FileNotFoundError(f"构建目录缺少 libusb: {libusb}")

    # Verify ctypes / tk dependencies
    ffi_dlls = list(internal_dir.glob("ffi*.dll"))
    if not ffi_dlls:
        raise FileNotFoundError(f"构建目录缺少 ctypes 依赖 ffi.dll: {internal_dir}")

    # Smoke test: launch process briefly to ensure no DLL load exception
    print("  执行可执行文件快速启动自测 (Smoke Test)...")
    proc = subprocess.Popen([str(exe_path)])
    try:
        proc.wait(timeout=2.0)
        # If it terminated in under 2 seconds, it crashed
        if proc.returncode != 0:
            raise RuntimeError(f"可执行文件启动立即异常退出，退出码: {proc.returncode}")
    except subprocess.TimeoutExpired:
        # Process is running normally! Terminate it
        proc.terminate()
        try:
            proc.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            proc.kill()
        print("  ✓ 可执行文件启动烟测成功（无 DLL 缺失弹窗或崩溃）！")

    print("  ✓ 主执行程序与底层载荷全部校验通过！")
    print(f"\n🎉 构建完成！发布目录: {DIST_DIR / 'SonyA6700Customizer'}")


def main():
    try:
        check_prerequisites()
        run_pyinstaller()
        copy_distribution_assets()
        zip_file = create_zip_package()
        verify_dist()
        print(f"\n========================================================")
        print(f"✅ 独立绿色免安装发布包已就绪:")
        print(f"   文件夹: {DIST_DIR / 'SonyA6700Customizer'}")
        print(f"   压缩包: {zip_file}")
        print(f"========================================================")
    except Exception as exc:
        print(f"\n❌ 构建失败: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
