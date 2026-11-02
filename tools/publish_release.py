# -*- coding: utf-8 -*-
"""Publish standalone release to GitHub Releases for mingwucn/Sony_research_6700."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = PROJECT_ROOT / "dist" / "Sony_a6700_Customizer_v1.0.0_win64.zip"

REPO = "mingwucn/Sony_research_6700"
TAG = "v1.0.0"
NAME = "Sony α6700 极简定制工具 v1.0.0 (FTP Menus & Native English)"

BODY = """## 🚀 Sony α6700 (ILCE-6700) 极简定制工具 v1.0.0

仅适用于国行 Sony α6700、固件 **Ver. 2.00** 的精确目标：
1. **原生英文语言菜单 (`EN-101`)**：开放 `Setup -> Area/Date -> Language -> English`，使用相机原生英文资源，不改写中文字库、区域码或 Wi-Fi 频段配置。
2. **FTP 菜单与动作 (`FT-101`)**：开放网络 FTP 设置、相册回放「选择传输」81 处权限和回放自定义键 `Action 0x0817`。
   - 菜单与动作绑定已有固件静态分析和真机菜单回读证据。
   - 端到端上传、断线重连与长效网络传输仍需结合相机无线环境和 FTP 服务器持续验证，菜单出现不等于传输成功。

---

### 📊 写入范围与恢复架构
- **逻辑修改**：92 处目标，共 94 个变化字节。
- **物理足迹**：两项全选时计划处理 7 个独立段，共 236,018 字节（约 230.5 KiB），单段 <= 128 KiB；其余 235,924 个段内字节来自预读并原样保留。
- **持久快照**：写前将完整原始/目标 `.bin` 缓冲保存并 `fsync()`，同时追加 JSONL 事务事件。
- **全段校验**：每段写入后重新读取完整段并逐字节比对，而非只检查修改点。多段整体不是原子事务。
- **中断锁定**：超时、断连或 mismatch 立即进入 `NEEDS_REVIEW`，不自动重试或自动回退。
- **第 7 页恢复**：启动检测未闭环会话，先只读对账，再明确选择回退修改段或续写写前状态段；异常/部分段禁止续写。
- **有条件出厂还原**：依赖 USB 服务模式与固件文件保持可访问；硬件损坏或固件不可访问时不保证软件层恢复。

---

### 📦 资产下载与运行
1. 下载并解压 `Sony_a6700_Customizer_v1.0.0_win64.zip`（独立便携版，无需系统 Python）。
2. 双击 **`SonyA6700Customizer.exe`** 或 **`启动_Sony_a6700定制工具.bat`**。
3. 相机开机，USB 设为 **海量存储器 (Mass Storage)**，关闭其他相机访问软件。
4. 按界面完成须知、驱动、准备、只读检测和功能管理；发现中断会话时先进入第 7 页只读对账。

---

### 💡 曾用 Powerful6700 或早期版本的用户
- 工具会识别基础网络菜单已开启的 `PARTIAL` 状态，并跳过已符合目标值的字段。
- 可补齐相册菜单、Action `0x0817` 和英文断言。
- FTP 服务器和 Wi-Fi 配置位于 Backup NVRAM；本工具目标仅为 `/usr/lib/appFw.so`，不主动读写或重置这些配置。
"""


def get_token() -> str:
    proc = subprocess.Popen(["git", "credential", "fill"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    stdout, _ = proc.communicate("protocol=https\nhost=github.com\n")
    creds = dict(line.split("=", 1) for line in stdout.splitlines() if "=" in line)
    token = creds.get("password")
    if not token:
        raise RuntimeError("未能从 git credential manager 获取 GitHub 访问令牌")
    return token


def main():
    if not ZIP_PATH.is_file():
        raise FileNotFoundError(f"未找到发布 zip 文件: {ZIP_PATH}")

    zip_bytes = ZIP_PATH.read_bytes()
    zip_size = len(zip_bytes)
    print(f"发布资产文件: {ZIP_PATH.name} ({zip_size:,} 字节 / {zip_size/(1024*1024):.2f} MB)")

    token = get_token()
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "SonyResearchPusher",
    }

    # 1. Check if release already exists
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/releases/tags/{TAG}", headers=headers)
    release_data = None
    try:
        with urllib.request.urlopen(req) as resp:
            release_data = json.load(resp)
            print(f"检测到已有 Release: {release_data.get('html_url')}")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            pass
        else:
            raise

    # 2. Create or update release metadata
    payload = {
        "tag_name": TAG,
        "target_commitish": "main",
        "name": NAME,
        "body": BODY,
        "draft": False,
        "prerelease": False,
    }
    if not release_data:
        print(f"正在创建 Release {TAG}...")
        create_req = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/releases",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", **headers},
            method="POST",
        )
        with urllib.request.urlopen(create_req) as resp:
            release_data = json.load(resp)
            print(f"✓ Release 创建成功: {release_data.get('html_url')}")
    else:
        print(f"正在同步更新 Release {TAG} 说明文档...")
        patch_req = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/releases/{release_data['id']}",
            data=json.dumps({"name": NAME, "body": BODY}).encode("utf-8"),
            headers={"Content-Type": "application/json", **headers},
            method="PATCH",
        )
        with urllib.request.urlopen(patch_req) as resp:
            release_data = json.load(resp)

    # 3. Check existing assets in release
    upload_url_template = release_data["upload_url"]  # format: https://uploads.github.com/.../assets{?name,label}
    upload_url_base = upload_url_template.split("{")[0]

    assets = release_data.get("assets", [])
    for a in assets:
        if a["name"] == ZIP_PATH.name:
            print(f"删除同名旧资产: {a['name']} (ID: {a['id']})...")
            del_req = urllib.request.Request(
                f"https://api.github.com/repos/{REPO}/releases/assets/{a['id']}",
                headers=headers,
                method="DELETE",
            )
            with urllib.request.urlopen(del_req) as resp:
                pass

    # 4. Upload zip asset
    print(f"正在上传资产 {ZIP_PATH.name} ({zip_size/(1024*1024):.2f} MB)...")
    upload_url = f"{upload_url_base}?name={urllib.parse.quote(ZIP_PATH.name)}"
    upload_req = urllib.request.Request(
        upload_url,
        data=zip_bytes,
        headers={
            "Content-Type": "application/zip",
            "Content-Length": str(zip_size),
            **headers,
        },
        method="POST",
    )
    with urllib.request.urlopen(upload_req) as resp:
        asset_data = json.load(resp)
        print(f"✓ 资产上传成功: {asset_data.get('browser_download_url')}")

    print("\n========================================================")
    print(f"🎉 GitHub Release 发布完成！")
    print(f"Release 页面: {release_data.get('html_url')}")
    print(f"直接下载链接: {asset_data.get('browser_download_url')}")
    print(f"========================================================")


if __name__ == "__main__":
    main()
