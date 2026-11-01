@echo off
chcp 65001 >nul
title Sony α6700 定制工具 (FTP 与原生英文解锁)

echo =======================================================
echo   Sony α6700 (ILCE-6700 固件 2.00) 定制工具
echo   完整 FTP 支持 (含回放按键上传) + 原生英文语言解锁
echo =======================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python 环境，请确认已安装 Python 3.10+ 并加入 PATH。
    pause
    exit /b 1
)

python -c "import usb.core" >nul 2>nul
if %errorlevel% neq 0 (
    echo [提示] 检测到缺少 pyusb 通信依赖，正在自动安装...
    python -m pip install pyusb libusb-package
)

echo [信息] 正在启动图形界面...
start "" python -X utf8 apps\a6700_customizer\app_gui.py
exit /b 0
