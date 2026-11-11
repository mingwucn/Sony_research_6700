# Sony α6700 (ILCE-6700) Firmware Research & Minimalist Customizer (Full FTP + Native English)

**Latest Status (2026-11-02): The Ver. 2.00 customizer now discloses 94 logical changed bytes versus 7 spans / 236,018 physical bytes, journals full raw span snapshots, requires read-only reconciliation after interruption, and passes 106 focused offline tests plus the portable clean-PATH self-test. Physical interrupted-session recovery and long-duration FTP reliability remain separate validation work.**

---

## 🌟 Core Breakthroughs

### 1. True Native English Menu Unlock (`EN-101`) — Zero `.uxc` String Corruption
- **Problem with prior tools**: Existing tools (such as `Powerful6700-Windows`) did not unlock the native English menu; they merely overwrote 4 Creative Look strings inside the Simplified Chinese resource file (`string_schinese.uxc`).
- **Root Cause Discovered**: The official Mainland China (CN1) firmware (`Ver. 2.00`) already ships with **100% complete native English UI resource banks** (`string_english.uxc`, `string_english_3.uxc`, `string_english_6.uxc`, `string_english_22.uxc` — 11,917 Resource IDs matching Simplified Chinese 1:1) in `/dev/nflasha15`. However, Choice 0 (`English`, Resource ID `0x0204e2be`) in the Setup Language menu table (`0x04b44180`) is guarded by an availability predicate (`english_predicate` at link-time VA `0x023080d0`, relocated via `.rela.dyn` at `0x00aa3a58`). That predicate reads Backup property `0x010d008f` (which is `2` on CN1 bodies) and executes `cmp w0, #1` followed by `cset w20, eq` at file offset **`0x023080f8`**.
- **Surgical 4-Byte Solution**: Patching **`0x023080f8`** in `/usr/lib/appFw.so` from `f4 17 9f 1a` (`cset w20, eq`) to `34 00 80 52` (`mov w20, #1`) forces `english_predicate` to return `1` while keeping its stack frame constructor (`0x03137990`), destructor (`0x0313759c`), and all regional/Wi-Fi/compliance settings (`0x010d008f`) untouched. Selecting **English** in `Setup -> Area/Date -> Language` natively updates Backup property `0x02cf0000` (Group 719) to `0` (Bank 0) and persists across reboots.

### 2. Native Wi-Fi FTP Menu and Playback Action Unlock (`FT-101`)
- **Problem with prior tools**: Enabling only the 9 Network FTP capability flags (`0x05a5`–`0x05b0`) exposed the setup menu, but the Playback FTP action remained unavailable because its parent Playback/Gallery menu permissions were disabled.
- **Menu and Action Scope**: The current target set enables the 9 Network flags, Action `0x0817` at `0x03f17ce4`, and 81 Playback/Gallery permissions. This exposes `Playback -> Select to Transfer` and permits `FTP传输` to be assigned in Playback Custom Key settings.
- **Evidence Boundary**: Firmware static analysis and on-device menu readback support the menu/action claims. End-to-end transfer reliability, reconnect behavior, and long-duration network operation remain subject to the camera Wi-Fi/server environment and continuing validation.

### 3. Minimalist Windows Desktop GUI (`Sony α6700 极简定制工具`)
- Modeled after the clean step-by-step workflow of `Powerful6700-Windows`, with unrelated experimental modifications excluded.
- Provides **only**:
  1. **FTP 网络配置菜单、相册回放「选择传输」菜单树与回放自定义键 `0x0817`**
  2. **原生英文菜单解锁（`Setup -> Language -> English` 谓词 `0x023080f8`）**
- **Built-in Transactional Safety**:
  - **Read-Only Pre-Inspection & JSON Backup**: Reads all 92 targets in 7 spans and saves timestamped target-state JSON in `backups/`.
  - **Durable Raw Span Journal**: Before each mutating span write, saves and `fsync()`s the complete pre-write and target `.bin` buffers in an append-only JSONL session journal.
  - **Sequential Independent Spans + Full Readback**: Each span is at most 128 KiB and is written and verified independently; every byte of the full span must match. This is not an atomic multi-span transaction.
  - **Immediate `NEEDS_REVIEW` Lockout**: Timeout, disconnect, stale reconciliation, or mismatch stops the session without blind retry or automatic rollback. Page 7 requires a read-only reconciliation before guarded resume or rollback from raw snapshots.
  - **Conditional Factory Restore**: Restores the managed fields to CN1 Ver. 2.00 constants only while USB service-mode communication and firmware access remain operational; hardware/inaccessible-firmware recovery is not guaranteed.

---

## 📊 Exact Binary & Partition Patch Specification

**Target Binary**: `/usr/lib/appFw.so` (Sony ILCE-6700 CN1 Firmware Ver. 2.00)
- **File Size**: `89,027,992` bytes (`0x054e7598`)
- **Stock SHA-256**: `e65fd595052be5d0e98ce8000dfcb94f90a2f8309de70ef140375052009b0ef3`
- **Filesystem Location**: `/dev/nflasha15` (ext2, 4096-byte blocks, 512-byte sectors, Inode `24583`)

| Feature Group | Target ID | `/usr/lib/appFw.so` Offset | `/dev/nflasha15` Sector | Stock Bytes | Patched Bytes | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Native English (`EN-101`)** | `english_menu_predicate` | `0x023080f8` (4B) | Sector `383128` (`+0xF8`) | `f4 17 9f 1a` | `34 00 80 52` | `cset w20, eq` ➔ `mov w20, #1` in `english_predicate` (`0x023080d0`) |
| **Playback FTP Key (`FT-101`)** | `ftp_playback_action_0817` | `0x03f17ce4` (1B) | Sector `445966` (`+0xE4`) | `00` | `01` | Unlocks Action `0x0817` (`FTP_TRANSFER`, RID `0x021c668e`) in Playback Custom Key menu |
| **Network FTP Menu (`FT-101`)** | `ftp_net_05a5` | `0x03f17524` (1B) | Sector `129210` (`+0x124`) | `00` | `01` | Action `0x05a5` — FTP Transfer Function master gate |
| **Network FTP Menu (`FT-101`)** | `ftp_net_05a6` | `0x03f1752c` (1B) | Sector `129210` (`+0x12C`) | `00` | `01` | Action `0x05a6` — FTP Server Selection |
| **Network FTP Menu (`FT-101`)** | `ftp_net_05a7` | `0x03f17534` (1B) | Sector `129210` (`+0x134`) | `00` | `01` | Action `0x05a7` — FTP Transfer Execute / Status |
| **Network FTP Menu (`FT-101`)** | `ftp_net_05a8` | `0x03f1753c` (1B) | Sector `129210` (`+0x13C`) | `00` | `01` | Action `0x05a8` — FTP Auto Transfer on Capture |
| **Network FTP Menu (`FT-101`)** | `ftp_net_05a9` | `0x03f17544` (1B) | Sector `129210` (`+0x144`) | `00` | `01` | Action `0x05a9` — FTP Transfer Target (RAW+JPEG / JPEG) |
| **Network FTP Menu (`FT-101`)** | `ftp_net_05aa` | `0x03f1754c` (1B) | Sector `129210` (`+0x14C`) | `00` | `01` | Action `0x05aa` — FTP Movie Transfer Target |
| **Network FTP Menu (`FT-101`)** | `ftp_net_05ab` | `0x03f17554` (1B) | Sector `129210` (`+0x154`) | `00` | `01` | Action `0x05ab` — FTP Power Save during Transfer |
| **Network FTP Menu (`FT-101`)** | `ftp_net_05ac` | `0x03f1755c` (1B) | Sector `129210` (`+0x15C`) | `00` | `01` | Action `0x05ac` — FTP Directory Hierarchy |
| **Network FTP Menu (`FT-101`)** | `ftp_net_05b0` | `0x03f17564` (1B) | Sector `129210` (`+0x164`) | `00` | `01` | Action `0x05b0` — FTP Display Transfer Result |

---

## 🚀 Quick Start: Windows Desktop GUI (`Sony α6700 极简定制工具`)

### 📦 运行方式选择（二选一）

#### 方式 A（推荐 · 纯小白用户 · 免安装 Python 环境）：
1. **直接下载独立便携版**：前往 [GitHub Releases 页面](https://github.com/mingwucn/Sony_research_6700/releases/tag/v1.0.0) 或点击 **[直接下载 Sony_a6700_Customizer_v1.0.0_win64.zip (~22.7 MB)](https://github.com/mingwucn/Sony_research_6700/releases/download/v1.0.0/Sony_a6700_Customizer_v1.0.0_win64.zip)**。
2. 解压至电脑任意目录（**无需安装 Python 或任何第三方环境**）。
3. 双击运行 **`SonyA6700Customizer.exe`** 或 **`启动_Sony_a6700定制工具.bat`** 即可进入深色模式界面（含条件启动的第 7 页会话恢复）。
4. 开发者也可以在本地运行根目录下的 **[`打包独立发布版.bat`](file:///d:/LocalWork/Sony_research_6700/%E6%89%93%E5%8C%85%E7%8B%AC%E7%AB%8B%E5%8F%91%E5%87%86%E7%89%88.bat)**（或 `python tools/build_dist.py`）一键重新构建打包。

#### 方式 B（开发者 / 源码运行）：
1. **Windows 10 / 11 (x64)**，已安装 Python 3.10+。
2. 双击运行 **[`启动_A6700定制工具.bat`](file:///d:/LocalWork/Sony_research_6700/%E5%90%AF%E5%8A%A8_A6700%E5%AE%9A%E5%88%B6%E5%B7%A5%E5%85%B7.bat)**，脚本会自动校验环境依赖并启动界面：
   ```powershell
   python -X utf8 run_customizer.py
   ```

---

### 💡 针对曾用 Powerful6700 开启过 FTP 的用户

1. 第 4 步会识别 `部分启用 (Partial)` 状态；已符合目标值的网络菜单字段在写入时按段判断并跳过实际修改（`no-op`）。
2. 本次可补齐相册回放传输菜单（81 处权限）、Action `0x0817` 和英文语言断言。
3. FTP 服务器、账号和 Wi-Fi 配置位于 Backup NVRAM；本工具的目标仅为 `/usr/lib/appFw.so`，不主动读写或重置这些配置。
4. “出厂还原”会把本工具管理的全部 FTP 与英文字段写回 Ver. 2.00 预置值，包括此前由其他工具改写的网络位。该操作依赖 USB 服务模式与固件文件保持可访问。

---

### Camera Preparation
   - Sony α6700 (ILCE-6700) running official Firmware **Ver. 2.00**.
   - Battery charged to **≥ 50%** (80% or reliable USB power recommended).
   - Set camera USB mode to **Mass Storage (海量存储器 / MSC)**: `设置 (Setup) -> USB -> USB连接模式 -> 海量存储器 (Mass Storage)`.
   - Close Sony Creators' App, Imaging Edge, Lightroom, or any other software that accesses the camera over USB.

### Launching the Application
Double-click **[`启动_A6700定制工具.bat`](file:///d:/LocalWork/Sony_research_6700/%E5%90%AF%E5%8A%A8_A6700%E5%AE%9A%E5%88%B6%E5%B7%A5%E5%85%B7.bat)** in the repository root, or run from PowerShell/CMD:

```powershell
python -X utf8 -m apps.a6700_customizer.app_gui
```

### Guided Workflow and Interrupted-Session Recovery
1. **操作前须知 / 驱动检查 / 相机准备**：确认精确机型与固件、电量、WinUSB 和 MSC 连接，关闭所有其他相机访问程序。
2. **检测与备份**：只读检查 92 个目标并保存时间戳 JSON。便携版数据位于程序目录 `data/`，源码运行位于 `.data/customizer/`。
3. **功能管理**：页面同时披露 **94 个逻辑修改字节（92 处目标）**与两项全选时的 **7 段 / 236,018 字节（约 230.5 KiB）**计划物理足迹。其余 235,924 个段内字节来自预读并原样保留。
4. **顺序分段写入**：每段独立且不超过 128 KiB；写入前保存完整原始/目标 `.bin` 并记录 JSONL 日志，写入后全段逐字节回读。多段整体不是原子事务。
5. **异常恢复**：若启动时发现 `INITIALIZED`、`IN_PROGRESS`、`NEEDS_REVIEW` 或 `RECONCILED` 未闭环会话，应用进入第 7 页。先执行只读对账，再明确选择“回退全部修改段”或“续写未完成段”。异常/部分段禁止续写；任何异常都不会触发自动重试或自动回退。
6. **有条件出厂还原**：第 6 页将管理字段恢复为原厂预置值，依赖 USB 服务模式正常通信与固件可访问，不保证硬件损坏或固件不可访问场景下的软件恢复。

### Post-Unlock Camera Setup
- **To switch to Native English**: Navigate to `设置 (Setup) -> 区域/日期 (Area/Date) -> 语言 (Language)` and select **English**.
- **Mode B: Playback Gallery Transfer Menu**: Enter `播放 (Playback) -> 选择传输 (Select to Transfer)` to access the enabled image-selection and transfer-target menu entries.
- **Mode A: Playback Custom Key Binding**: Navigate to `设置 (Setup) -> 操作自定义 (Operation Customize) -> 回放自定义键设置 (PB Custom Key Setting)` and assign **`FTP传输` (`FTP Transfer`)** to a preferred key. Actual upload completion and long-term transfer reliability must be verified separately with the configured Wi-Fi/FTP server.

---

## 🛠️ Offline CLI Tools & Unit Tests

The focused customizer suite uses synthetic/mocked inputs and does not access a camera:

```powershell
# 106 cases: journal/recovery, targets/spans, patch spec, ELF, ext2 and UXC
python -X utf8 -m unittest tests/test_recovery_journal.py tests/test_customizer_recovery.py tests/test_customizer_targets.py tests/test_patch_spec.py tests/test_elf_static.py tests/test_ext2_readonly.py tests/test_uxc_readonly.py -v

# 2. Verify stock vs. patched sectors on a raw /dev/nflasha15 image
python -X utf8 tools/verify_target_sectors.py <path-to-nflasha15.img>

# 3. Regenerate forward & rollback JSON patch plans from stock nflasha15.img
python -X utf8 tools/generate_patch_plan.py <path-to-nflasha15.img>
```

---

## 🔍 Cross-Model Applicability: A7CR (`ILCE-7CR`) vs. A7M5 (`ILCE-7M5`) — Mainland China (`CN1`)

See **[`docs/CROSS_MODEL_ENGLISH_COMPARISON.md`](file:///d:/LocalWork/Sony_research_6700/docs/CROSS_MODEL_ENGLISH_COMPARISON.md)** for the full technical analysis:

| Camera Model (Mainland China `CN1`) | SoC / Generation | Shares Same `EN-101` Unmasking Process? | Key Technical Notes & Required Adaptations |
| :--- | :--- | :--- | :--- |
| **Sony α6700 (`ILCE-6700` Ver. 2.00)** | **BIONZ XR (`CXD90057`)** (2023) | ✅ **Baseline Target** | Patches `/usr/lib/appFw.so` at **`0x023080f8`** (`f4 17 9f 1a` ➔ `34 00 80 52`, `Sector 383128`) on `/dev/nflasha15`; MSC USB PID `054C:0E76` ➔ Service PID `054C:0336`. |
| **Sony A7CR (`ILCE-7CR` Ver. 2.01)** | **BIONZ XR (`CXD90057`)** (2023) | ✅ **Yes — Identical Mechanism & Workflow** | Same `CXD90057_k8` FDAT encryption, `/dev/nflasha15`, `/usr/lib/appFw.so`, `string_english*.uxc`, Backup ID `0x010d008f`, and `054C:0336` `Senser` service mode. **Do not copy α6700's `0x023080f8` offset**: resolve A7CR's own `english_predicate` offset (`Choice 0` `0x0204e2be` / `0x010d008f`), use MSC PID `054C:0E8A`, and invalidate Warm-Boot Image `*wbi4` (`image_drop=1` ➔ `image_mode=0`) before cold reboot. |
| **Sony A7M5 (`ILCE-7M5` / A7V)** | **BIONZ XR2** (Late 2025 / 2026) | ❌ **No — Blocked at USB `Senser` Auth Layer** | Retains the same user-space `.uxc` and `0x010d008f` localization design, but Sony updated the USB `Senser` challenge-response authentication protocol on **BIONZ XR2** (standard `CXD90057` / `pmca` handshakes fail with `Invalid response: 9` or immediate reboot). |

---

## 📂 Repository Structure & Documentation Index

### Applications & Tools
- **[`启动_A6700定制工具.bat`](file:///d:/LocalWork/Sony_research_6700/%E5%90%AF%E5%8A%A8_A6700%E5%AE%9A%E5%88%B6%E5%B7%A5%E5%85%B7.bat)**: One-click Windows launcher with automatic dependency verification (`pyusb`, `libusb-package`).
- **[`apps/a6700_customizer/app_gui.py`](file:///d:/LocalWork/Sony_research_6700/apps/a6700_customizer/app_gui.py)**: Dark-mode Tkinter/ttk GUI with feature management, conditional factory restore, and startup reconciliation.
- **[`apps/a6700_customizer/app_backend.py`](file:///d:/LocalWork/Sony_research_6700/apps/a6700_customizer/app_backend.py)**: Guarded camera backend with read-only inspection, durable span writes, full readback, reconciled resume/rollback, and factory restore.
- **[`apps/a6700_customizer/recovery_journal.py`](file:///d:/LocalWork/Sony_research_6700/apps/a6700_customizer/recovery_journal.py)**: Append-only JSONL journal and `fsync()`ed raw pre-write/target span binaries.
- **[`apps/a6700_customizer/targets.py`](file:///d:/LocalWork/Sony_research_6700/apps/a6700_customizer/targets.py)**: Exact definitions for 92 targets / 94 logical changed bytes and 7 spans / 236,018 physical bytes in `/usr/lib/appFw.so`.
- **[`tools/patch_spec.py`](file:///d:/LocalWork/Sony_research_6700/tools/patch_spec.py)**: Sector-level (`Sector 383128` & `Sector 445966`) cryptographic specification, SHA-256 verification, and offline roundtrip engine.
- **[`tools/verify_target_sectors.py`](file:///d:/LocalWork/Sony_research_6700/tools/verify_target_sectors.py)**: Standalone CLI inspector for raw `/dev/nflasha15` partition dumps.
- **[`tools/generate_patch_plan.py`](file:///d:/LocalWork/Sony_research_6700/tools/generate_patch_plan.py)**: Generates [`research/plans/forward_patch_plan.json`](file:///d:/LocalWork/Sony_research_6700/research/plans/forward_patch_plan.json) and [`research/plans/rollback_restore_plan.json`](file:///d:/LocalWork/Sony_research_6700/research/plans/rollback_restore_plan.json).

### Documentation (`docs/`)
- **[`docs/USER_GUIDE_CN.md`](file:///d:/LocalWork/Sony_research_6700/docs/USER_GUIDE_CN.md)**: Complete Chinese user manual (图文级步骤说明、常见报错排查、相机端回放快捷键设置、一键无损还原指南).
- **[`docs/TECHNICAL_ARCHITECTURE.md`](file:///d:/LocalWork/Sony_research_6700/docs/TECHNICAL_ARCHITECTURE.md)**: Deep-dive technical whitepaper covering ARM64 disassembly of `english_predicate`, `.rela.dyn` relocation analysis, Backup ID `0x010d008f` vs `0x02cf0000`, Action `0x0817` Playback Custom Key dispatch, ext2 block-to-sector mapping, and USB Senser/Jiritsu transactional write architecture.
- **[`docs/MASKED_FUNCTIONS_AND_TIERING.md`](file:///d:/LocalWork/Sony_research_6700/docs/MASKED_FUNCTIONS_AND_TIERING.md)**: In-depth analysis of why Sony masks FTP on α6700, commercial market tiering vs. FX30, technical gating in `appFw.so` (Network flags + Playback Custom Key Action `0x0817`), and a complete taxonomy of masked functions (regional locks, working firmware backends, and unsafe uncalibrated CP features).
- **[`docs/CROSS_MODEL_ENGLISH_COMPARISON.md`](file:///d:/LocalWork/Sony_research_6700/docs/CROSS_MODEL_ENGLISH_COMPARISON.md)**: Cross-model comparison of the Native English menu unlock process across Mainland China (`CN1`) **α6700 (`ILCE-6700`)**, **A7CR (`ILCE-7CR`)**, and **A7M5 (`ILCE-7M5` / Alpha 7 V)** (BIONZ XR `CXD90057` vs. BIONZ XR2 platform differences, `appFw.so` offset resolution, WBI `wbi4` invalidation, and `Senser` authentication).
- **[`docs/ENGLISH_LANGUAGE.md`](file:///d:/LocalWork/Sony_research_6700/docs/ENGLISH_LANGUAGE.md)**: Target-specific design and verification record for `EN-101` native English menu unlock.
- **[`docs/FTP.md`](file:///d:/LocalWork/Sony_research_6700/docs/FTP.md)**: Target-specific design and verification record for `FT-101` native Wi-Fi FTP and Playback Custom Key unlock.
- **[`docs/FEATURE_PROGRESS.md`](file:///d:/LocalWork/Sony_research_6700/docs/FEATURE_PROGRESS.md)**: Feature status matrix and historical progress log.
- **[`docs/ACCESS_AND_RECOVERY.md`](file:///d:/LocalWork/Sony_research_6700/docs/ACCESS_AND_RECOVERY.md)**: Risk tiers (`R0`–`R5`), backup rules, and transactional write gates.
- **[`docs/BACKLOG.md`](file:///d:/LocalWork/Sony_research_6700/docs/BACKLOG.md)**: Work package definitions and completion records.

### Reverse-Engineering Reports (`research/`)
- **[`research/ENGLISH_LANGUAGE_CANDIDATE.md`](file:///d:/LocalWork/Sony_research_6700/research/ENGLISH_LANGUAGE_CANDIDATE.md)**: Complete disassembly and proof of the 4-byte `english_predicate` patch at `0x023080f8`.
- **[`research/sessions/20261031-playback-ftp-action-discovery.md`](file:///d:/LocalWork/Sony_research_6700/research/sessions/20261031-playback-ftp-action-discovery.md)**: Discovery of Action `0x0817` (`FTP_TRANSFER`) at `0x03666b70` and capability gate `0x03f17ce4`.
- **[`research/sessions/20261101-english-predicate-unmask.md`](file:///d:/LocalWork/Sony_research_6700/research/sessions/20261101-english-predicate-unmask.md)**: Session report on `english_predicate` relocation, cross-reference audit, and sector mapping.
- **[`research/sessions/20261101-customizer-gui-and-documentation.md`](file:///d:/LocalWork/Sony_research_6700/research/sessions/20261101-customizer-gui-and-documentation.md)**: Session report on building and debugging the `Sony α6700 极简定制工具` GUI and completing project documentation.
- **[`research/sessions/20261101-cross-model-english-comparison.md`](file:///d:/LocalWork/Sony_research_6700/research/sessions/20261101-cross-model-english-comparison.md)**: Session report on cross-model Native English unlock applicability across Mainland China (`CN1`) α6700 (`ILCE-6700`), A7CR (`ILCE-7CR`), and A7M5 (`ILCE-7M5` / Alpha 7 V).
- **[`research/sessions/20261101-masked-functions-and-commercial-tiering.md`](file:///d:/LocalWork/Sony_research_6700/research/sessions/20261101-masked-functions-and-commercial-tiering.md)**: Session report on why Sony masks FTP and taxonomy of masked functions across BIONZ XR firmware.

---

<details>
<summary><b>📜 Historical Research & Audit Log (2026-10-18 to 2026-10-26)</b></summary>

### Earlier English Firmware & Reference Reviews (2026-10-26)
- [English firmware findings](research/ENGLISH_FIRMWARE_FINDINGS.md), 2026-10-26: English resources and separate availability/selection retain static support for a language-only route. The conditional program's native APIs and finite client forms are mapped; its initial direct callback is a separate non-language item. [Program-client review](research/sessions/20261026-english-program-clients.md).
- [Powerful6700 Windows review](research/sessions/20261026-powerful6700-english-review.md), 2026-10-26: Pinned commit `4a3e30cad2f608580854755654b12e1d4049c5de` audited; confirmed that upstream `Powerful6700-Windows` only renamed 4 Creative Look strings inside `string_schinese.uxc` and did not unlock the native English menu or the Playback FTP custom key (`0x0817`).

### Earlier RA-003 Package & Container Audits (2026-10-18 to 2026-10-23)
- [Official package intake](research/OFFICIAL_PACKAGE_INTAKE.md) and [Mainland firmware source](research/MAINLAND_FIRMWARE_SOURCE.md)
- [UFU container audit](research/UFU_CONTAINER_AUDIT.md) and [FDAT extractor audit](research/FDAT_EXTRACTOR_AUDIT.md)
- [FDAT decoding plan](research/FDAT_DECODING_PLAN.md), [Crypto provenance](research/FDAT_CRYPTO_PROVENANCE.md), [Header trial](research/FDAT_HEADER_TRIAL.md), and [Stream validation](research/FDAT_STREAM_VALIDATION.md)
- [Component prefix audit](research/COMPONENT_PREFIX_AUDIT.md), [Tar directory audit](research/TAR_DIRECTORY_AUDIT.md), [Tar path diagnostic](research/TAR_PATH_DIAGNOSTIC.md), and [Tar link inventory](research/TAR_LINK_INVENTORY.md)
- [Ext superblock design](research/EXT_SUPERBLOCK_DESIGN.md), [Ext superblock observation](research/EXT_SUPERBLOCK_OBSERVATION.md), and [Ext metadata planner design](research/EXT_METADATA_PLANNER_DESIGN.md)
- [GDT metadata scope](research/GDT_METADATA_SCOPE.md), [GDT runner design](research/GDT_RUNNER_DESIGN.md), and [GDT I/O adapter design](research/GDT_IO_ADAPTER_DESIGN.md)

</details>

## Playback FTP Shortcuts Experimental 0.6.0

An experimental α6700 bundle with separate **FTP Transfer** and **FTP Trans. (This Img.)** playback actions is under release review. The camera was not tested with this build; assignment, restart persistence and end-to-end transfer remain unverified. The public binary will be attached to a versioned prerelease after the release review. See the [candidate notes and provenance](release-candidates/playback-extras-v0.6.0-experimental/RELEASE_NOTES.md).
