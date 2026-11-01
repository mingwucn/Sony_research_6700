# Sony α6700 (ILCE-6700) Firmware Research & Minimalist Customizer (Full FTP + Native English)

**Latest Status (2026-11-01): Reverse engineering, exact binary/sector patch specifications, offline roundtrip verification, and the standalone Windows GUI customizer (`apps/a6700_customizer`) for Mainland China Sony α6700 Firmware Ver. 2.00 are complete.**

---

## 🌟 Core Breakthroughs

### 1. True Native English Menu Unlock (`EN-101`) — Zero `.uxc` String Corruption
- **Problem with prior tools**: Existing tools (such as `Powerful6700-Windows`) did not unlock the native English menu; they merely overwrote 4 Creative Look strings inside the Simplified Chinese resource file (`string_schinese.uxc`).
- **Root Cause Discovered**: The official Mainland China (CN1) firmware (`Ver. 2.00`) already ships with **100% complete native English UI resource banks** (`string_english.uxc`, `string_english_3.uxc`, `string_english_6.uxc`, `string_english_22.uxc` — 11,917 Resource IDs matching Simplified Chinese 1:1) in `/dev/nflasha15`. However, Choice 0 (`English`, Resource ID `0x0204e2be`) in the Setup Language menu table (`0x04b44180`) is guarded by an availability predicate (`english_predicate` at link-time VA `0x023080d0`, relocated via `.rela.dyn` at `0x00aa3a58`). That predicate reads Backup property `0x010d008f` (which is `2` on CN1 bodies) and executes `cmp w0, #1` followed by `cset w20, eq` at file offset **`0x023080f8`**.
- **Surgical 4-Byte Solution**: Patching **`0x023080f8`** in `/usr/lib/appFw.so` from `f4 17 9f 1a` (`cset w20, eq`) to `34 00 80 52` (`mov w20, #1`) forces `english_predicate` to return `1` while keeping its stack frame constructor (`0x03137990`), destructor (`0x0313759c`), and all regional/Wi-Fi/compliance settings (`0x010d008f`) untouched. Selecting **English** in `Setup -> Area/Date -> Language` natively updates Backup property `0x02cf0000` (Group 719) to `0` (Bank 0) and persists across reboots.

### 2. Complete Native Wi-Fi FTP Support (`FT-101`) — Including Playback Custom Key (`0x0817`)
- **Problem with prior tools**: Enabling the 9 Network FTP capability flags (`0x05a5`–`0x05b0`) exposed the `Network -> FTP Transfer` setup menu, but users **could not assign a Custom Key in Playback mode** to trigger single-photo FTP uploads (`FTP传输` was hidden in `回放自定义键设置`).
- **Root Cause Discovered**: Tracing the Playback Custom Key binding table (`0x03665ec0`) revealed that Resource ID `0x021c668e` (`"FTP Transfer"` / `"FTP传输"`) is bound at `0x03666b70` to **Action ID `0x0817` (`2071`)**. The custom key dispatcher (`0x01440d0c`) filters assignable actions through the master 8-byte capability table (`0x03f14c38 + action_id * 8`). At entry **`0x03f17ce0`** (`Action 0x0817`), the availability byte at **`0x03f17ce4`** was `0x00` (disabled).
- **Complete 10-Byte Solution**: Enabling **`0x03f17ce4`** (`00` ➔ `01`) alongside the 9 Network FTP flags (`0x03f17524`–`0x03f17564`) unlocks both the full Network FTP configuration menu (Server, PASV, Destination Folder, Auto Transfer) **and** the Playback Custom Key assignment (`设置 -> 操作自定义 -> 回放自定义键设置 -> FTP传输`).

### 3. Minimalist Windows Desktop GUI (`Sony α6700 极简定制工具`)
- Modeled after the clean step-by-step workflow of `Powerful6700-Windows`, with **all unrelated experimental modifications removed** (no Creative Look LUTs, no shutter curtain tweaks, no exposure/sound/pixel-shift/stabilization hacks).
- Provides **only**:
  1. **原生完整 FTP 传输（含回放快捷键 `0x0817` + 网络菜单 `0x05a5`–`0x05b0`）**
  2. **原生英文菜单解锁（`Setup -> Language -> English` 谓词 `0x023080f8`）**
- **Built-in Transactional Safety**:
  - **Read-Only Pre-Inspection & Automatic Dual Backups**: Reads all 11 target windows from `/usr/lib/appFw.so`, verifies exact byte signatures, and saves timestamped JSON backups + `initial_backup.json` in `backups/` before any write is allowed.
  - **Zero-Change Write Probe**: Writes the camera's existing stock byte back to `0x023080f8` with `fsync` + read-back verification before applying any real modification.
  - **Atomic Write + `fsync` + Read-Back Verification**: Uses freestanding AArch64 native helpers (`dump_range.elf` & `flash_write.elf`) over the USB service session to modify `/usr/lib/appFw.so` in place, flush to NAND, and verify every modified byte.
  - **1-Click Factory Restore**: Restores all 14 bytes back to stock CN1 Ver. 2.00 constants (or from a saved backup snapshot) at any time.

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

### Prerequisites
1. **Windows 10 / 11 (x64)** with Python 3.10+ installed.
2. **Local Reference Runtime**: Place `Powerful6700-Windows-x64` at `D:\Softwares\Powerful6700-Windows-x64` (or set environment variable `POWERFUL6700_ROOT` to its path). The GUI reuses its signed/tested USB transport libraries (`libusb-1.0.dll`, `windows_auth`) and freestanding AArch64 camera helpers (`dump_range.elf`, `flash_write.elf`).
3. **Camera Preparation**:
   - Sony α6700 (ILCE-6700) running official Firmware **Ver. 2.00**.
   - Battery charged to **≥ 50%**.
   - Set camera USB mode to **Mass Storage (海量存储器 / MSC)**: `设置 (Setup) -> USB -> USB连接模式 -> 海量存储器 (Mass Storage)`.
   - Close Sony Creators' App, Imaging Edge, Lightroom, or any other software that accesses the camera over USB.

### Launching the Application
Double-click **[`启动_A6700定制工具.bat`](file:///d:/LocalWork/Sony_research_6700/%E5%90%AF%E5%8A%A8_A6700%E5%AE%9A%E5%88%B6%E5%B7%A5%E5%85%B7.bat)** in the repository root, or run from PowerShell/CMD:

```powershell
python -X utf8 -m apps.a6700_customizer.app_gui
```

### 6-Step Guided Workflow
1. **1. 操作前须知 (Pre-Flight Checklist)**: Review safety rules and check the confirmation box.
2. **2. 驱动检查 (WinUSB Driver Check)**: Click **重新扫描驱动**. If it shows `状态: WinUSB 驱动已就绪` (green), click **下一步：相机准备 ➔** directly. Otherwise, click **一键绑定 WinUSB 驱动** once.
3. **3. 相机准备 (Camera Preparation)**: Connect the camera via a data-capable USB-C cable in **Mass Storage (海量存储器)** mode.
4. **4. 检测与备份 (Read-Only Inspection & Auto-Backup)**: Click **开始只读检查与备份**. The tool reads `/usr/lib/appFw.so`, verifies exact byte signatures for FTP and English, and automatically writes a timestamped backup JSON to [`backups/`](file:///d:/LocalWork/Sony_research_6700/backups/).
5. **5. 功能管理 (Feature Management)**:
   - Check **启用完整 FTP 传输（网络菜单 + 回放快捷键 0x0817）** and/or **解锁原生英文菜单（Setup -> Language -> English）**.
   - Click **一键写入选中功能**. The tool performs a zero-change probe, patches the selected bytes, flushes to NAND (`fsync`), and verifies read-back equality.
   - **Power-cycle the camera**: Turn the camera switch OFF, wait 5 seconds, remove the battery for 5 seconds, reinsert, and power ON.
6. **6. 出厂还原 (1-Click Factory Restore)**: At any time, click **一键还原全部为原厂状态** (or **从备份文件还原...**) to restore all 14 bytes back to stock CN1 Ver. 2.00 values.

### Post-Unlock Camera Setup
- **To switch to Native English**:
  - Navigate to `设置 (Setup) -> 区域/日期 (Area/Date) -> 语言 (Language)` and select **English**.
- **To bind a Playback Custom Key for 1-button FTP upload**:
  - Navigate to `设置 (Setup) -> 操作自定义 (Operation Customize) -> 回放自定义键设置 (PB Custom Key Setting)` (or `Custom Key/Dial Set.` in English).
  - Select your preferred button (e.g., `C1`, `C2`, `AEL`, or `AF-ON`) and assign it to **`FTP传输` (`FTP Transfer`)**.
  - When reviewing photos in Playback mode, press that button to immediately queue/upload the current photo to your configured FTP server!

---

## 🛠️ Offline CLI Tools & Unit Tests

All static analysis, sector verification, and patch planning tools run 100% offline using only the Python standard library:

```powershell
# 1. Run the 76-case unit test suite (ELF, ext2, UXC, patch spec, and customizer targets)
python -X utf8 -m unittest tests/test_customizer_targets.py tests/test_patch_spec.py tests/test_elf_static.py tests/test_ext2_readonly.py tests/test_uxc_readonly.py -v

# 2. Verify stock vs. patched sectors on a raw /dev/nflasha15 image
python -X utf8 tools/verify_target_sectors.py <path-to-nflasha15.img>

# 3. Regenerate forward & rollback JSON patch plans from stock nflasha15.img
python -X utf8 tools/generate_patch_plan.py <path-to-nflasha15.img>
```

---

## 📂 Repository Structure & Documentation Index

### Applications & Tools
- **[`启动_A6700定制工具.bat`](file:///d:/LocalWork/Sony_research_6700/%E5%90%AF%E5%8A%A8_A6700%E5%AE%9A%E5%88%B6%E5%B7%A5%E5%85%B7.bat)**: One-click Windows launcher with automatic dependency verification (`pyusb`, `libusb-package`).
- **[`apps/a6700_customizer/app_gui.py`](file:///d:/LocalWork/Sony_research_6700/apps/a6700_customizer/app_gui.py)**: 6-step dark-mode Tkinter/ttk desktop GUI application.
- **[`apps/a6700_customizer/app_backend.py`](file:///d:/LocalWork/Sony_research_6700/apps/a6700_customizer/app_backend.py)**: Transactional camera backend (WinUSB driver check, USB service-mode session, read-only inspection, automatic backups, zero-change write probe, `flash_write.elf` execution, and factory restore).
- **[`apps/a6700_customizer/targets.py`](file:///d:/LocalWork/Sony_research_6700/apps/a6700_customizer/targets.py)**: Exact byte definitions and state evaluators for all 11 target windows (`14` bytes total) in `/usr/lib/appFw.so`.
- **[`tools/patch_spec.py`](file:///d:/LocalWork/Sony_research_6700/tools/patch_spec.py)**: Sector-level (`Sector 383128` & `Sector 445966`) cryptographic specification, SHA-256 verification, and offline roundtrip engine.
- **[`tools/verify_target_sectors.py`](file:///d:/LocalWork/Sony_research_6700/tools/verify_target_sectors.py)**: Standalone CLI inspector for raw `/dev/nflasha15` partition dumps.
- **[`tools/generate_patch_plan.py`](file:///d:/LocalWork/Sony_research_6700/tools/generate_patch_plan.py)**: Generates [`research/plans/forward_patch_plan.json`](file:///d:/LocalWork/Sony_research_6700/research/plans/forward_patch_plan.json) and [`research/plans/rollback_restore_plan.json`](file:///d:/LocalWork/Sony_research_6700/research/plans/rollback_restore_plan.json).

### Documentation (`docs/`)
- **[`docs/USER_GUIDE_CN.md`](file:///d:/LocalWork/Sony_research_6700/docs/USER_GUIDE_CN.md)**: Complete Chinese user manual (图文级步骤说明、常见报错排查、相机端回放快捷键设置、一键无损还原指南).
- **[`docs/TECHNICAL_ARCHITECTURE.md`](file:///d:/LocalWork/Sony_research_6700/docs/TECHNICAL_ARCHITECTURE.md)**: Deep-dive technical whitepaper covering ARM64 disassembly of `english_predicate`, `.rela.dyn` relocation analysis, Backup ID `0x010d008f` vs `0x02cf0000`, Action `0x0817` Playback Custom Key dispatch, ext2 block-to-sector mapping, and USB Senser/Jiritsu transactional write architecture.
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
