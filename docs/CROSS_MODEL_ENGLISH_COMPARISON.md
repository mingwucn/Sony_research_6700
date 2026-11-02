# Cross-Model Native English Unlock Analysis: Sony α6700 (`ILCE-6700`) vs. A7CR (`ILCE-7CR`) vs. A7M5 (`ILCE-7M5`) — Mainland China (`CN1`) Versions

**Date**: 2026-11-01  
**Evidence Classification**: `static-inference`, `offline-tested` (α6700 Ver. 2.00 + pinned A7C II / A7CR / PMCA reference repositories), `source-report` (A7M5 / BIONZ XR2 platform behavior)  
**Camera Commands Executed**: `none`

---

## 1. Executive Summary

- **Sony A7CR (`ILCE-7CR`, Mainland China `CN1`) — Shares the Exact Same Unmasking Process as α6700 (`ILCE-6700`)**:
  - The **A7CR** is a same-generation **BIONZ XR (`CXD90057`)** sibling of the **α6700 (`ILCE-6700`)** and **A7C II (`ILCE-7CM2`)** (2023 generation).
  - It shares the **identical firmware container encryption (`CXD90057_k8`)**, partition layout (`/dev/nflasha15` mounted at `/usr`), core application binary (`/usr/lib/appFw.so`), native English `.uxc` string bank architecture, Backup property IDs (`0x010d008f` & `0x02cf0000`), and USB `Senser`/`Jiritsu` service-mode execution chain.
  - Consequently, A7CR (`CN1`) can use the **exact same 4-byte `english_predicate` patch (`cset w20, eq` ➔ `mov w20, #1`)** in `/usr/lib/appFw.so` (plus Warm-Boot Image `wbi4` invalidation), provided that **A7CR's own `appFw.so` file offset** is resolved offline first.
- **Sony A7M5 (`ILCE-7M5` / Alpha 7 V, Mainland China `CN1`) — Does NOT Share the Same Execution Process Today**:
  - Released in late 2025 / early 2026, the **A7M5 (`ILCE-7M5`)** transitions to Sony's next-generation **BIONZ XR2** processor platform.
  - Although its user-space UI framework (`appFw.so`, `.uxc` string resources, and `0x010d008f`–`0x010d00b1` language flags in `Backup.bin`) retains the same logical localization design, **Sony updated the USB `Senser` authentication handshake and platform security on BIONZ XR2**.
  - Standard `CXD90057` / `Sony-PMCA-RE` service-mode transitions and authentication handshakes fail on the A7M5 (`Invalid response: 9`, USB pipe stalls, or immediate camera reboots), blocking both `appFw.so` binary patching and `Backup.bin` property tweaking over USB until a BIONZ XR2-compatible service transport is established.

---

## 2. Side-by-Side Technical Comparison (`CN1` Mainland China SKUs)

| Technical Dimension | Sony α6700 (`ILCE-6700` CN1) | Sony A7CR (`ILCE-7CR` CN1) | Sony A7M5 (`ILCE-7M5` / A7V CN1) |
| :--- | :--- | :--- | :--- |
| **Processor / SoC Generation** | **BIONZ XR (`CXD90057`)** + AI Unit (2023) | **BIONZ XR (`CXD90057`)** + AI Unit (2023) | **BIONZ XR2** + AI Unit (Late 2025 / 2026) |
| **Firmware Container (`BODYDATA.DAT`)** | `FDAT` encrypted with `CXD90057_k8` ([`FDAT_CRYPTO_PROVENANCE.md`](../research/FDAT_CRYPTO_PROVENANCE.md)) | `FDAT` encrypted with `CXD90057_k8` (same SoC family) | BIONZ XR2 `FDAT` container (requires XR2 key/signing verification) |
| **Application Partition & FS** | `/dev/nflasha15` (`ext2`, mounted `/usr` `ro`) | `/dev/nflasha15` (`ext2`, mounted `/usr` `ro`, verified in [`external/a7cr-reference/README.md`](../external/a7cr-reference/README.md)) | `/usr` application partition (BIONZ XR2 layout) |
| **Target Shared Library** | `/usr/lib/appFw.so` (`89,027,992` B on Ver. 2.00) | `/usr/lib/appFw.so` (`> 93.8 MB` on Ver. 2.01) | `/usr/lib/appFw.so` (BIONZ XR2 build) |
| **Native English `.uxc` Banks** | **100% present** (`string_english*.uxc`, 11,917 IDs matching `schinese`) | **100% present** (`string_english*.uxc` shipped in `CN1` image) | **Present** (`string_english*.uxc` shipped in `CN1` image) |
| **Language Menu Gate (`Choice 0`)** | Resource ID `0x0204e2be` (`"English"`) guarded by `english_predicate` in `appFw.so` | **Identical**: Resource ID `0x0204e2be` guarded by `english_predicate` in `appFw.so` | **Same logical design**: `appFw.so` menu predicate + `Backup.bin` flags |
| **Backup Availability Property ID** | `0x010d008f` (`0x02` = disabled on `CN1`; `0x01` = enabled) | `0x010d008f` (`0x02` = disabled on `CN1`; `0x01` = enabled) | `0x010d008f`–`0x010d00b1` (35 per-language 1-byte flags) |
| **Selected Language Property ID** | `0x02cf0000` (`0` = English, `25` = Simplified Chinese) | `0x02cf0000` (`0` = English, `25` = Simplified Chinese) | `0x02cf0000` |
| **USB Mass Storage ➔ Service PID** | MSC `054C:0E76` (or `047D`) ➔ Service `054C:0336` | MSC `054C:0E8A` ➔ Service `054C:0336` ([`transport.py`](../external/a7c2-reference/src/fl23/transport.py)) | **Blocked / Changed**: `Senser` authentication handshake fails (`Invalid response: 9` / reboot) |
| **Warm-Boot Snapshot (`WBI`)** | `/dev/nflasha5` (`*wbi4`) | `/sys/power/image_dev` = `*wbi4`; uses `image_drop=1` ➔ `image_mode=0` ([`wbi.c`](../external/a7c2-reference/src/fl23/native/wbi.c)) | Retained fast-boot snapshot |

---

## 3. Deep Dive: How the α6700 `EN-101` Process Applies to A7CR (`ILCE-7CR`)

### 3.1 Shared Binary Mechanism (`english_predicate` in `/usr/lib/appFw.so`)
On `CXD90057` cameras (α6700, A7C II, A7CR), Sony's `Setup -> Area/Date -> Language` menu table is an array of 32-byte (`0x20`) descriptors in `.data.rel.ro`:

```c
struct LanguageChoiceEntry {
    uint32_t choice_index;      // +0x00: 0 = English
    uint32_t resource_id;       // +0x04: 0x0204e2be ("English" in string_*.uxc)
    uint64_t reserved_08;       // +0x08: 0
    uint64_t reserved_10;       // +0x10: 0
    uint64_t predicate_fn_ptr;  // +0x18: relocated via .rela.dyn to english_predicate()
};
```

In `english_predicate`, the AArch64 function constructs a temporary `BackupClient` on the stack, reads Backup item **`0x010d008f`**, compares the returned status against `1` (`enabled`), and sets `w20` via `cset w20, eq`:

```armasm
mov  w0, #0x10df          ; e0 1f 02 52  \_ w0 = 0x010d008f (Language_English_Permit)
movk w0, #0x000d, lsl #16 ; a0 01 a0 72  /
bl   BackupClient::read   ; ...
cset w20, eq              ; f4 17 9f 1a  <-- PATCH TARGET: replace with 34 00 80 52 (mov w20, #1)
```

Because `english_predicate` is referenced **exclusively** by Entry 0 of the Language Menu table (zero other callers in the entire `appFw.so` binary), patching `f4 17 9f 1a` (`cset w20, eq`) to `34 00 80 52` (`mov w20, #1`):
1. Unconditionally exposes **English** in `Setup -> Area/Date -> Language`.
2. Preserves the C++ `BackupClient` constructor/destructor lifecycle and stack frame unwinding.
3. Leaves `Backup.bin` (`0x010d008f = 2`) and all NVRAM regional/Wi-Fi/video compliance settings untouched.
4. Allows Sony's native menu handler to persist `0x02cf0000 = 0` (English) across power cycles when selected by the user.

### 3.2 Three Model-Specific Adaptations Required for A7CR
> [!CAUTION]
> **Never write α6700's raw file offset (`0x023080f8`) directly to an A7CR!** Although both binaries are compiled from the same Sony application framework, A7CR's `/usr/lib/appFw.so` has a different file size and link-time section layout.

To run the exact same unmasking process on a Chinese Mainland **A7CR (`ILCE-7CR`)**, only three parameters change:

1. **Locate A7CR's `english_predicate` Offset Offline (< 1 Minute)**:
   - Unpack A7CR's official `BODYDATA.DAT` using the `CXD90057_k8` FDAT decryptor and extract `/usr/lib/appFw.so` from `/dev/nflasha15`.
   - Search `.data.rel.ro` for the 8-byte header of Choice 0: `00 00 00 00 be e2 04 02` (`choice_index = 0`, `resource_id = 0x0204e2be`), then look up the `R_AARCH64_RELATIVE` addend in `.rela.dyn` targeting `+0x18` of that entry.
   - Alternatively, scan `.text` in A7CR's `appFw.so` for the exact instruction sequence loading `0x010d008f` (`e0 1f 02 52 a0 01 a0 72`) followed within 16 bytes by `f4 17 9f 1a` (`cset w20, eq`).
2. **USB Mass Storage Product ID (`PID`)**:
   - In USB Mass Storage mode, α6700 enumerates as `054C:0E76` (or `047D`), whereas the A7C II / A7CR family enumerates as **`054C:0E8A`** (see [`external/a7c2-reference/src/fl23/transport.py`](../external/a7c2-reference/src/fl23/transport.py)).
   - After `SonySenserAuthDevice` switches the camera into service mode, both α6700 and A7CR enumerate as the identical `Senser` service PID **`054C:0336`**.
3. **Warm-Boot Image (`WBI`) Snapshot Invalidation (`*wbi4`)**:
   - As documented in [`external/a7cr-reference/README.md`](../external/a7cr-reference/README.md) (Section 4) and [`external/a7c2-reference/src/fl23/native/wbi.c`](../external/a7c2-reference/src/fl23/native/wbi.c), A7CR caches the running `appFw.so` process state in a Warm-Boot Image (`*wbi4`).
   - After patching `/usr/lib/appFw.so` on `/dev/nflasha15` (via `remount rw` ➔ `pwrite64` ➔ `fsync` ➔ `remount ro`), execute the sysfs invalidation sequence before shutting down:
     1. Verify `/sys/power/image_mode` reads `2\n` and `/sys/power/image_dev` reads `*wbi4\n`.
     2. Write ASCII `1` (1 byte) to `/sys/power/image_drop`.
     3. Immediately write ASCII `0` (1 byte) to `/sys/power/image_mode` (so the kernel does not regenerate a stale WBI snapshot during shutdown).
     4. Power off, remove the battery for 60 seconds, and cold-boot so the camera loads the freshly patched `appFw.so` from `/dev/nflasha15`.

---

## 4. Why A7M5 (`ILCE-7M5` / Alpha 7 V) Differs at the Execution Layer

The **Sony A7M5 (`ILCE-7M5`)**, announced in December 2025, introduces Sony's next-generation **BIONZ XR2** processor. While its user-space menu architecture still restricts English on Mainland China (`CN1`) and Japanese (`J1`) bodies via `0x010d008f` and `appFw.so`, two critical platform changes prevent using the α6700 / A7CR unlock tools on the A7M5 today:

1. **Updated USB `Senser` Authentication & Service-Mode Security**:
   - Both the `appFw.so` binary patch route and the `pmca-console` Backup property route rely on transitioning the camera from USB Mass Storage mode into Sony's `Senser` (`054C:0336`) service mode and completing a challenge-response authentication handshake.
   - On the **A7M5 (`ILCE-7M5`, Firmware Ver. 1.01 / 2.00)**, Sony updated the `Senser` authentication protocol on the BIONZ XR2 platform. Standard `Sony-PMCA-RE` / `windows_auth` handshakes fail with `Invalid response: 9`, USB endpoint stalls, or immediate camera reboots.
2. **Firmware Container (`FDAT`) Encryption Key**:
   - Because the A7M5 uses the new BIONZ XR2 SoC rather than `CXD90057`, unpacking `BODYDATA.DAT` offline requires verifying the BIONZ XR2 FDAT key/format rather than assuming `CXD90057_k8`.

---

## 5. Why `appFw.so` Predicate Patching (`EN-101`) Is Safer Than `pmca` `Backup.bin` Tweaks on `CXD90057` Cameras (α6700 / A7CR / A7C II)

Historically, community users attempted to unlock languages on Sony cameras using `Sony-PMCA-RE` (`LanguageTweak` in [`pmca/platform/tweaks.py`](../private/english-program-handoff-20261026/github-method/retained-source/pmca/platform/tweaks.py) and [`pmca/platform/backup.py`](../private/english-program-handoff-20261026/github-method/retained-source/pmca/platform/backup.py)), which overwrites all 35 Backup properties (`0x010d008f` through `0x010d00b1`) with `0x01`.

Our static audit identified three major advantages of the **4-byte `appFw.so` `english_predicate` patch (`EN-101`)** over modifying `Backup.bin` on modern `CN1` cameras:

| Comparison Criterion | Traditional `pmca` `Backup.bin` Route (`0x010d008f`..`0x010d00b1`) | Surgical `appFw.so` `english_predicate` Route (`EN-101`) |
| :--- | :--- | :--- |
| **Protected Attribute Bit (`attr & 0x01`)** | `0x010d008f` has the protection bit set in `CN1` `Backup.bin`. `BackupPatchDataInterface` must clear `attr & ~1`, rewrite the entire catalog, and rewrite again to restore `attr`, which often stalls on `CXD90057` USB pipes. | **Zero `Backup.bin` writes required** during unlock. `0x010d008f` remains at its factory protected value (`0x02`). |
| **Broken `CN1` Factory Restore in `pmca`** | In `pmca/platform/backup.py` (line 200), `'CN1'` is hardcoded from older camera generations as `[1, 0, 1, ...]` (assuming English was enabled `1` on `CN1`). Disabling the tweak in `pmca` **fails to restore `0x010d008f` to `2`** on modern `CN1` bodies. | **100% deterministic 4-byte inverse**: restoring `34 00 80 52` ➔ `f4 17 9f 1a` in `/usr/lib/appFw.so` returns the binary to its exact factory SHA-256 hash. |
| **Scope & Side Effects** | Modifies 35 NVRAM language availability flags simultaneously in `/setting/Backup.bin`. | Modifies **only 1 instruction (4 bytes)** in `english_predicate`, which has **1 caller** (`Choice 0: English` in the Language Menu table). |


---

## 6. 中文核心结论与跨机型对比速查 (Chinese Summary)

针对国行（`CN1`）**Sony A7CR (`ILCE-7CR`)** 与 **Sony A7M5 (`ILCE-7M5` / Alpha 7 V)** 是否与 **Sony α6700 (`ILCE-6700`)** 共享同一套原生英文解锁（`EN-101`）流程，技术审计结论如下：

### 6.1 核心结论速览
1. **国行 A7CR (`ILCE-7CR`) —— ✅ 完全共享同一套底层机制与执行流程**：
   - **同代同芯架构**：A7CR 与 α6700、A7C II 同属 2023 年发布的 **BIONZ XR (`CXD90057`)** 平台，共享完全一致的 `CXD90057_k8` 固件加密容器、`ext2` 应用分区 (`/dev/nflasha15` 挂载于 `/usr`)、核心 UI 动态库 `/usr/lib/appFw.so`、内置完整 `string_english*.uxc` 原生英文字库、Backup 语言权限项 (`0x010d008f`) 与当前语言项 (`0x02cf0000`)，以及完全相同的 USB `Senser`/`Jiritsu` (`054C:0336`) 服务模式通信链路。
   - **相同的 4 字节精准补丁方案**：同样可以通过定位 `/usr/lib/appFw.so` 中语言菜单第 0 项（`English`，词条 ID `0x0204e2be`）的可用性谓词函数 `english_predicate`，将其内部比较 `0x010d008f == 1` 后的 `f4 17 9f 1a` (`cset w20, eq`) 替换为 `34 00 80 52` (`mov w20, #1`)，实现零字库污染、不破坏中文菜单、不触碰机身区域码与 Wi-Fi 合规参数的真·原生英文解锁。
   - **适配 A7CR 仅需注意 3 个机型参数差异**（严禁直接刷入 α6700 的原始文件偏移）：
     1. **重新定位 A7CR 专属文件偏移**：A7CR 的 `/usr/lib/appFw.so` 体积（Ver. 2.01 超过 `93.8 MB`）大于 α6700（Ver. 2.00 为 `89.0 MB`），不能直接写入 α6700 的 `0x023080f8`。只需在 A7CR 解包出的 `appFw.so` 中搜索 `.data.rel.ro` 表项 `00 00 00 00 be e2 04 02`（或搜索加载 `0x010d008f` 的机器码 `e0 1f 02 52 a0 01 a0 72` 加 `f4 17 9f 1a`），1 分钟内即可定位 A7CR 的准确 4 字节偏移。
     2. **海量存储模式 USB PID**：A7CR 在海量存储器 (MSC) 模式下枚举为 `054C:0E8A`（α6700 为 `054C:0E76`），切入服务模式后两者均为 `054C:0336`。
     3. **失效 `*wbi4` 快速启动休眠镜像 (WBI)**：修改完 A7CR 的 `/usr/lib/appFw.so` 后，需向 `/sys/power/image_drop` 写入 `"1"` 并立即向 `/sys/power/image_mode` 写入 `"0"`，随后关机拔电池静置冷启动，强制系统从 `/dev/nflasha15` 重新加载修改后的 `appFw.so`。

2. **国行 A7M5 (`ILCE-7M5` / Alpha 7 V) —— ❌ 逻辑架构相通，但当前无法共用执行链路**：
   - **跨代处理器平台**：A7M5（2025 年底发布，固件 Ver. 1.01 / 2.00）升级为全新一代 **BIONZ XR2** 处理器平台。
   - **USB 服务模式鉴权封堵**：虽然上层 UI 依然采用 `.uxc` 字库与 `0x010d008f` 语言权限位设计，但索尼在 BIONZ XR2 平台上更新了 USB `Senser` 服务模式的挑战-响应鉴权协议。现有的 `CXD90057` / `Sony-PMCA-RE` 握手工具在 A7M5 上会直接报错（`Invalid response: 9`、USB 管道挂起或相机立即重启），因此在适配 BIONZ XR2 新版鉴权协议与固件解包密钥前，无法直接使用 α6700 / A7CR 的改机工具。
