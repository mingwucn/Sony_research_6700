@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ====================================================
echo  Sony α6700 极简定制工具 - 独立发布包一键构建
echo ====================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未在系统 PATH 中找到 Python 解释器。
    pause
    exit /b 1
)

python -X utf8 tools/build_dist.py
if %errorlevel% neq 0 (
    echo.
    echo [错误] 打包失败，请检查上方日志。
    pause
    exit /b %errorlevel%
)

echo.
echo 构建完成！发布文件已放置在 dist/ 目录下。
pause
