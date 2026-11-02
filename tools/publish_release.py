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
NAME = "Sony α6700 极简定制工具 v1.0.0 (Full FTP & True Native English)"

BODY = """## 🚀 Sony α6700 (ILCE-6700) 极简定制工具 v1.0.0

本工具为国行 Sony α6700（固件版本 **Ver. 2.00**）提供两大核心功能的极简安全定制：
1. **真·原生英文语言菜单解锁 (`EN-101`)**：直接放开 `Setup -> Area/Date -> Language -> English` 原生选项，零 `.uxc` 字库污染，不改机身区域码与 Wi-Fi 频段。
2. **完整 Wi-Fi FTP 传输支持 (`FT-101`)**：不仅开启网络 FTP 设置菜单（`0x05a5`–`0x05b0`），更精准补齐相册回放界面的 **`回放快捷键 0x0817`（看图一键上传照片）**。

---

### 📦 资产下载与快速运行
- **下载文件**：`Sony_a6700_Customizer_v1.0.0_win64.zip`（16.0 MB，绿色免安装）
- **运行说明**：
  1. 下载解压至任意目录（**无需安装 Python 或任何第三方环境**）。
  2. 双击运行 **`SonyA6700Customizer.exe`** 或 **`启动_Sony_a6700定制工具.bat`**。
  3. 将相机开机，USB 连接模式设为 **海量存储器 (Mass Storage)** 并连接电脑。
  4. 按照软件界面 6 步引导即可完成无损只读备份与写入。

---

### 💡 针对曾用 Powerful6700 开启过 FTP 的用户
- 本工具会自动检测到相机已开启网络菜单（`PARTIAL` 状态）。
- 写入时自动跳过已改动的 9 处网络菜单（`no-op`），仅精准补齐此前缺失的 **`0x03f17ce4`（回放相册自定义键）** 与 **`0x023080f8`（真原生英文）**。
- **相机内已设置的 FTP 服务器 IP、账号密码、上传目录和 Wi-Fi 密码 100% 完好保留**，绝不清除或重置。

---

### 🛡️ 离线安全事务与出厂还原
- **只读预读与零变化探针**：每次写入前均自动进行只读校验并保存写前备份，写入前执行零改动硬件探针测试。
- **极简修改足迹**：全功能仅改动 `/usr/lib/appFw.so` 中共 14 个字节，绝不改动内核、bootloader、传感器标定和无线射频。
- **一键出厂还原**：随时可在软件中一键 100% 恢复为官方原厂状态。
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

    # 2. Create release if not exists
    if not release_data:
        print(f"正在创建 Release {TAG}...")
        payload = {
            "tag_name": TAG,
            "target_commitish": "main",
            "name": NAME,
            "body": BODY,
            "draft": False,
            "prerelease": False,
        }
        create_req = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/releases",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", **headers},
            method="POST",
        )
        with urllib.request.urlopen(create_req) as resp:
            release_data = json.load(resp)
            print(f"✓ Release 创建成功: {release_data.get('html_url')}")

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
