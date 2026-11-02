# Session Report: Cross-Model Native English Unlock Analysis — α6700 (`ILCE-6700`) vs. A7CR (`ILCE-7CR`) vs. A7M5 (`ILCE-7M5`) (2026-11-01)

## 1. Scope & Objectives
- **Packages**: `EN-101`, `RA-002` (Cross-model reference and platform applicability audit)
- **Evidence Classification**: `static-inference`, `offline-tested` (`ILCE-6700` Ver. 2.00 + pinned `a7cr-fl23-research`, `a7c2-fl23-research`, `fwtool.py`, and `Sony-PMCA-RE` sources), `source-report` (`ILCE-7M5` / BIONZ XR2 platform behavior)
- **Summary**:
  1. Evaluated whether Mainland China (`CN1`) **Sony A7CR (`ILCE-7CR`)** and **Sony A7M5 (`ILCE-7M5` / Alpha 7 V)** share the same Native English (`EN-101`) unmasking process as **Sony α6700 (`ILCE-6700` Ver. 2.00)**.
  2. Verified from pinned reference repositories ([`external/a7cr-reference/README.md`](file:///d:/LocalWork/Sony_research_6700/external/a7cr-reference/README.md) at commit `43ba74441c8f10459ade41e84a379ad8005e6ef4`, [`external/a7c2-reference/src/fl23/transport.py`](file:///d:/LocalWork/Sony_research_6700/external/a7c2-reference/src/fl23/transport.py) and [`wbi.c`](file:///d:/LocalWork/Sony_research_6700/external/a7c2-reference/src/fl23/native/wbi.c) at commit `c0930d5b0ccd49c0a092dc883054cd6dce199649`, and [`Sony-PMCA-RE`](file:///d:/LocalWork/Sony_research_6700/private/english-program-handoff-20261026/github-method/retained-source/pmca/platform/backup.py) at commit `a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0`):
     - **A7CR (`ILCE-7CR` CN1) shares the exact same mechanism and execution process as α6700 (`ILCE-6700` CN1)**: same 2023 **BIONZ XR (`CXD90057`)** SoC, `CXD90057_k8` FDAT firmware encryption, `/dev/nflasha15` (`ext2` mounted at `/usr`), `/usr/lib/appFw.so`, complete `string_english*.uxc` resources, Backup availability ID `0x010d008f` (`2` on `CN1`), selected language ID `0x02cf0000` (`0` = English), and `054C:0336` `Senser`/`Jiritsu` service mode. It requires only three model-specific adaptations: (a) resolving A7CR's own `english_predicate` file offset in A7CR's `/usr/lib/appFw.so` (never copying α6700's `0x023080f8` offset), (b) using A7CR's MSC USB PID `054C:0E8A`, and (c) invalidating the `*wbi4` Warm-Boot Image (`image_drop=1` -> `image_mode=0`) before cold reboot.
     - **A7M5 (`ILCE-7M5` / Alpha 7 V CN1) does NOT share the same execution process today**: while user-space localization still uses `.uxc` string banks and `0x010d008f`–`0x010d00b1` flags, the A7M5 runs on Sony's newer **BIONZ XR2** processor platform (late 2025 / 2026, Firmware Ver. 1.01 / 2.00) with an updated USB `Senser` challenge-response authentication protocol that rejects standard `CXD90057` / `pmca` service-mode handshakes (`Invalid response: 9`, USB pipe stall, or immediate reboot).
  3. Documented these findings in [`docs/CROSS_MODEL_ENGLISH_COMPARISON.md`](file:///d:/LocalWork/Sony_research_6700/docs/CROSS_MODEL_ENGLISH_COMPARISON.md) (English + Chinese), [`README.md`](file:///d:/LocalWork/Sony_research_6700/README.md), [`docs/TECHNICAL_ARCHITECTURE.md`](file:///d:/LocalWork/Sony_research_6700/docs/TECHNICAL_ARCHITECTURE.md), [`docs/USER_GUIDE_CN.md`](file:///d:/LocalWork/Sony_research_6700/docs/USER_GUIDE_CN.md), [`docs/ENGLISH_LANGUAGE.md`](file:///d:/LocalWork/Sony_research_6700/docs/ENGLISH_LANGUAGE.md), and [`docs/CODEX_HANDOFF.md`](file:///d:/LocalWork/Sony_research_6700/docs/CODEX_HANDOFF.md).

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
- **Owner Hardware Verification on α6700 (`EN-01`/`EN-02` & `FT-01`) or Optional Offline A7CR Offset Extraction**:
  1. For the **Sony α6700 (`ILCE-6700` Ver. 2.00)** body: run [`启动_A6700定制工具.bat`](file:///d:/LocalWork/Sony_research_6700/%E5%90%AF%E5%8A%A8_A6700%E5%AE%9A%E5%88%B6%E5%B7%A5%E5%85%B7.bat) through Step 4 (`开始只读检查与备份`) and Step 5 (`一键写入选中功能`), cold-boot the camera, and verify native English menu selection (`Setup -> Area/Date -> Language -> English`) and Playback Custom Key FTP transfer (`0x0817`).
  2. If adapting to **Sony A7CR (`ILCE-7CR` CN1)**: supply an extracted A7CR `/usr/lib/appFw.so` (or official `BODYDATA.DAT` for offline `CXD90057_k8` extraction) to resolve A7CR's exact `english_predicate` file offset and SHA-256 fingerprint before any A7CR device contact.
