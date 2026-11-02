# Session Report: Masked Functions & Commercial Tiering Analysis — Sony α6700 (`ILCE-6700`) (2026-11-01)

## 1. Scope & Objectives
- **Packages**: `FT-101` (Native Wi-Fi FTP), `EN-101` (Native English Localization), `RA-002` (Static capability table & cross-model audit)
- **Evidence Classification**: `static-inference` (verified on official CN1 Firmware Ver. 2.00 decrypted partition `/dev/nflasha15` and binary `/usr/lib/appFw.so`), `source-report` (cross-model BIONZ XR firmware audit, Sony SDK documentation, and upstream capability logs), `offline-tested` (76 unit tests).
- **Summary**:
  1. Documented the commercial and technical reasons why Sony masks native Wi-Fi FTP on the α6700 (`ILCE-6700`):
     - **Commercial**: The α6700 shares the identical 26MP BSI APS-C sensor and BIONZ XR (`CXD90057`) application processor with the cinema-line **FX30 (`ILME-FX30`)** and runs a single unified `/usr/lib/appFw.so` binary across all BIONZ XR cameras. Sony masks FTP on the α6700 to protect product tiering between enthusiast hybrid cameras and Cinema Line / professional press bodies (FX30, A7 IV).
     - **Technical**: Gated via the Master Action Capability Table in `.rodata` of `/usr/lib/appFw.so` at `0x03f14c38 + (ActionID * 8)`:
       - Network FTP setup screens: 9 actions (`0x05a5`–`0x05b0`) at `0x03f17524`–`0x03f17564` (ext2 Sector `129210`).
       - Playback Custom Key single-button FTP transfer: Action `0x0817` (`2071`) at `0x03f17ce4` (ext2 Sector `445966` `+0xE4`), bound at `0x03666b70` to Resource ID `0x021c668e`.
  2. Established a comprehensive three-tier taxonomy of other functions masked or present in α6700 firmware:
     - **Category A (Regional Localization Locks, 100% Complete Resources & Code)**: Native English & 34 International Languages on Mainland China (`CN1`) bodies via `english_predicate` (`0x023080d0`), NVRAM `0x010d008f`, and `cset w20, eq` at `0x023080f8`.
     - **Category B (Model-Tier Capability Masks with Working Firmware Backends)**: Shutter Closed when Power Off (`关机快门闭合 / 防尘快门`), Flexible Video Exposure Mode (`视频灵活曝光模式`), and Electronic Shutter Sound (`电子快门音开关与音量`).
     - **Category C (Present in UI / Strings but Missing Co-Processor Support / Unsafe)**: Pixel Shift Multi Shooting (`像素转换多重拍摄` - lacks IBIS sub-pixel CP routines), Dynamic Active Stabilization (`动态积极防抖` - lacks calibrated gyro/crop tables), and Creative Looks `FL2` / `FL3` (slots and 3D LUT matrices unpopulated on Ver. 2.00).
  3. Published comprehensive technical documentation in [`docs/MASKED_FUNCTIONS_AND_TIERING.md`](file:///d:/LocalWork/Sony_research_6700/docs/MASKED_FUNCTIONS_AND_TIERING.md).

---

## 2. Offline Verification & Unit Test Results
- **Command**:
  ```powershell
  python -X utf8 -m unittest tests/test_customizer_targets.py tests/test_patch_spec.py tests/test_elf_static.py tests/test_ext2_readonly.py tests/test_uxc_readonly.py -v
  ```
- **Interpreter**: `C:\ProgramData\miniconda3\python.exe` (CPython 3.13.12 on Windows AMD64)
- **Result**: **76 tests ran in 0.024s — 76 passed, 0 failed, 0 skipped, exit code 0**.
- **Camera Commands Executed**: `none`.

---

## 3. Next Single Actionable Work Package
- **Owner Hardware Verification on α6700 (`EN-01`/`EN-02` & `FT-01`)**:
  - Connect the Sony α6700 (CN1 Ver. 2.00) in Mass Storage mode.
  - Launch [`启动_A6700定制工具.bat`](file:///d:/LocalWork/Sony_research_6700/%E5%90%AF%E5%8A%A8_A6700%E5%AE%9A%E5%88%B6%E5%B7%A5%E5%85%B7.bat).
  - Run Step 4 (`开始只读检查与备份`) to record timestamped JSON pre-flight backups, followed by Step 5 (`一键写入选中功能`) to apply the 14-byte patch, cold-boot the camera, and verify native English and custom key FTP transfer.
