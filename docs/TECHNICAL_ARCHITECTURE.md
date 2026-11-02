# Sony α6700 (ILCE-6700) Firmware Ver. 2.00 — Technical Architecture & Reverse-Engineering Whitepaper

**Evidence Classification**: `static-inference` (verified on official CN1 Firmware Ver. 2.00 decrypted partition image `nflasha15.img`) and `offline-tested` (76 unit tests covering ELF64 parsing, ext2 block translation, UXC resource parity, sector SHA-256 roundtrip patching, and GUI target state machines).

---

## 1. Firmware Partition & Target Binary Layout

### 1.1 Partition `/dev/nflasha15` (Application & UI Resource Root)
In the Sony α6700 (ILCE-6700) Ver. 2.00 firmware update container (`Update_ILCE6700V200.dat`), the primary application logic and localization string databases reside on `/dev/nflasha15`:
- **Filesystem Type**: `ext2`
- **Total Size**: `130,023,424` bytes (`253,952` sectors of `512` bytes; `31,744` blocks of `4,096` bytes)
- **Block Size**: `4,096` bytes (`8` × `512`-byte sectors per ext2 block)
- **Inode Size**: `256` bytes (`s_inodes_per_group = 8192`)

### 1.2 Target Shared Library: `/usr/lib/appFw.so`
- **ext2 Inode**: `24583`
- **File Size**: `89,027,992` bytes (`0x054e7598`)
- **Stock SHA-256**: `e65fd595052be5d0e98ce8000dfcb94f90a2f8309de70ef140375052009b0ef3`
- **ELF Architecture**: 64-bit ARM (`AArch64`), little-endian (`ET_DYN` shared object)

#### ELF64 Program Headers (`PT_LOAD`)
Wait-free static translation between file offsets and link-time virtual addresses (`VA`) is governed by the four `PT_LOAD` segments in `/usr/lib/appFw.so`:

| Segment | Permissions | File Offset Range | Link-Time Virtual Address (`VA`) | Delta (`VA - FileOffset`) | Contents |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `LOAD #0` | `R E` | `0x00000000` – `0x0365180c` | `0x00000000` – `0x0365180c` | `0x00000000` | `.rela.dyn`, `.plt`, `.text` (application & menu predicates) |
| `LOAD #1` | `R  ` | `0x03652000` – `0x04a2b768` | `0x03652000` – `0x04a2b768` | `0x00000000` | `.rodata`, custom key binding tables (`0x03665ec0`), action capability table (`0x03f14c38`) |
| `LOAD #2` | `R W` | `0x04a2c000` – `0x05403280` | `0x04a3c000` – `0x05413280` | `+0x00010000` | `.data.rel.ro`, Language Menu choice table (`file 0x04b44180` / `VA 0x04b54180`) |
| `LOAD #3` | `R W` | `0x05404000` – `0x054e7598` | `0x05424000` – `0x05507598` | `+0x00020000` | `.data`, `.bss` |

> [!IMPORTANT]
> Because `LOAD #0` (`.text`) and `LOAD #1` (`.rodata`) have a link-time VA delta of **`0`**, file offsets inside `.text` and `.rodata` are numerically identical to their link-time virtual addresses. In `LOAD #2` (`.data.rel.ro`), `VA = FileOffset + 0x10000`.

---

## 2. Feature 1: True Native English Menu Unlock (`EN-101`)

### 2.1 UXC Resource Completeness Verification
In `/usr/local/share/language/` on `/dev/nflasha15`, the Mainland China (CN1) Ver. 2.00 firmware contains all four official English `.uxc` string banks alongside Simplified Chinese:

| English UXC Resource File | File Size | SHA-256 | Matching `schinese` Resource IDs |
| :--- | :--- | :--- | :--- |
| `string_english.uxc` | `308,588` B | `e0aa7185de74f0bc94a718040e3bc71bb8fa1971b6826be069f9045017c9134c` | `5,849 / 5,849` (100% parity) |
| `string_english_3.uxc` | `144,344` B | `27885a474de44181931f51841213efcc0117c7a0b31f7f0365f44df087b08e8f` | `2,022 / 2,022` (100% parity) |
| `string_english_6.uxc` | `144,344` B | `27885a474de44181931f51841213efcc0117c7a0b31f7f0365f44df087b08e8f` | `2,022 / 2,022` (100% parity) |
| `string_english_22.uxc` | `144,412` B | `bb1bb9057b3095b1cfcf55c92b07ef392ec3b56a0e68f55814fa4df82ef318f7` | `2,024 / 2,024` (100% parity) |

Every single menu label, dialog warning, playback prompt, and network error string (`11,917` total IDs) is already present in official English in the CN1 image.

### 2.2 The Language Menu Table (`0x04b44180`) & `.rela.dyn` Relocation
In `/usr/lib/appFw.so`, the Setup Language selection menu (`Setup -> Area/Date -> Language`) is driven by a 35-entry descriptor array at file offset **`0x04b44180`** (link-time VA **`0x04b54180`** in `LOAD #2`), where each entry is `0x20` (`32`) bytes:

```text
struct LanguageChoiceEntry {
    uint32_t choice_index;      // +0x00: 0 = English, 1 = French, ..., 10 = Simplified Chinese
    uint32_t resource_id;       // +0x04: UXC String Resource ID (0x0204e2be = "English")
    uint64_t reserved_08;       // +0x08: 0
    uint64_t reserved_10;       // +0x10: 0
    uint64_t predicate_fn_ptr;  // +0x18: Function pointer returning 1 (visible) or 0 (hidden)
};
```

For **Entry 0 (`English`, Resource ID `0x0204e2be`)**:
- The `predicate_fn_ptr` field is located at file offset **`0x04b44198`** (`VA 0x04b54198`).
- Inspecting `.rela.dyn` at file offset **`0x00aa3a58`** reveals an `R_AARCH64_RELATIVE` (`0x403`) relocation targeting `r_offset = 0x04b54198` with `r_addend = 0x023080d0`.
- Thus, at runtime, Entry 0's availability predicate resolves to **`english_predicate` at `0x023080d0`**.

### 2.3 Disassembly of `english_predicate` (`0x023080d0`)
Disassembling `/usr/lib/appFw.so` at file offset `0x023080d0` (`VA 0x023080d0`):

```armasm
0x023080d0: ff c3 00 d1    sub  sp, sp, #0x30
0x023080d4: f4 4f 01 a9    stp  x20, x19, [sp, #0x10]
0x023080d8: fd 7b 02 a9    stp  x29, x30, [sp, #0x20]
0x023080dc: fd 83 00 91    add  x29, sp, #0x20
0x023080e0: f3 23 00 91    add  x19, sp, #0x08
0x023080e4: e0 03 13 aa    mov  x0, x19
0x023080e8: 2a be 38 94    bl   0x03137990          ; BackupClient::BackupClient(&ctx)
0x023080ec: e0 1f 02 52    mov  w0, #0x10df         ; \_ w0 = 0x010d008f (Language_English_Permit)
0x023080f0: a0 01 a0 72    movk w0, #0x000d, lsl #16 ; /  (Exact: 0x010d008f)
0x023080f4: 41 c1 38 94    bl   0x031385f8          ; BackupClient::readByte(0x010d008f)
0x023080f8: f4 17 9f 1a    cset w20, eq             ; w20 = (w0 == 1) ? 1 : 0  <-- PATCH TARGET
0x023080fc: e0 03 13 aa    mov  x0, x19
0x02308100: e7 bc 38 94    bl   0x0313759c          ; BackupClient::~BackupClient(&ctx)
0x02308104: e0 03 14 2a    mov  w0, w20             ; return w20
0x02308108: fd 7b 42 a9    ldp  x29, x30, [sp, #0x20]
0x0230810c: f4 4f 41 a9    ldp  x20, x19, [sp, #0x10]
0x02308110: ff c3 00 91    add  sp, sp, #0x30
0x02308114: c0 03 5f d6    ret
```

- On Mainland China (CN1) cameras, Backup item `0x010d008f` holds `0x02` (disabled), whereas `0x031385f8` compares the value against `0x01` (enabled). Consequently, `cset w20, eq` sets `w20 = 0`, hiding `English` in the menu.
- **Why we patch `0x023080f8` (`cset w20, eq` ➔ `mov w20, #1`) instead of `0x023080d0`**:
  1. Patching `0x023080f8` (`f4 17 9f 1a` ➔ `34 00 80 52`) preserves the full C++ RAII lifecycle (`0x03137990` constructor and `0x0313759c` destructor) and stack frame unwinding.
  2. A full-binary cross-reference scan (`.text` `bl`/`b` targets, `adrp+add` pairs, and `.rela.dyn` addends) confirmed that **`0x023080d0` has exactly one reference in the entire 89 MB binary**: Entry 0 of the Language Menu table (`0x04b44198`).
  3. Backup property `0x010d008f` in NVRAM remains untouched (`0x02`), avoiding any regional consistency checksum issues. When the user selects `English` in the menu, Sony's native language setter updates Backup item `0x02cf0000` (Group 719) to `0` (Bank 0 = `string_english*.uxc`), which persists natively across power cycles.

---

## 3. Feature 2: Candidate Wi-Fi FTP & Playback Custom Key (`FT-101`)

> **Hardware regression (2026-11-02):** Native English works and the Network FTP page is accessible, but the owner's Playback/Gallery FTP remains unavailable. The following candidate mechanism is **static inference**, not a validated FTP unlock. See [issue #1](https://github.com/mingwucn/Sony_research_6700/issues/1).

### 3.1 Why Upstream `Powerful6700` Missed the Playback Custom Key
Upstream `Powerful6700` patched 9 single-byte flags in the master action capability table (`0x03f14c38`) corresponding to Action IDs **`0x05a5` through `0x05b0`** (file offsets `0x03f17524`–`0x03f17564`). Those 9 flags unlock the **Network -> FTP Transfer** setup pages (Server configuration, Auto-transfer on capture, Target format, Directory hierarchy).

However, in Sony's UI architecture, **Custom Key assignment in Playback mode** (`Setup -> Operation Customize -> PB Custom Key Setting`) uses a completely separate action ID for triggering on-demand FTP transfer of the currently viewed image or group.

### 3.2 Tracing Resource ID `0x021c668e` (`"FTP Transfer"`) to Action `0x0817`
1. In `string_english.uxc` and `string_schinese.uxc`, the Playback Custom Key label **`"FTP Transfer"` / `"FTP传输"`** has Resource ID **`0x021c668e`**.
2. Scanning `/usr/lib/appFw.so` for little-endian `8e 66 1c 02` locates the Playback Custom Key binding table (`0x03665ec0`–`0x03666e10`, `24` bytes per entry).
3. At file offset **`0x03666b70`**, the entry reads:
   ```text
   0x03666b70: 8e 66 1c 02   ; Resource ID = 0x021c668e ("FTP Transfer" / "FTP传输")
   0x03666b74: 3f 00 00 00   ; Icon / Category ID = 0x003f
   0x03666b78: 88 00 00 00   ; Group ID = 0x0088
   0x03666b7c: 17 08 00 00   ; Action ID = 0x0817 (2071)
   0x03666b80: 04 01 00 00   ; Sub-code = 0x0104
   0x03666b84: 22 02 00 00   ; Help String ID = 0x0222
   ```
4. **Record location, independent of lookup formula.** The owner reports an 8-byte table of little-endian `{uint32_t action_id, uint32_t status}` records in the official CN1 2.00 `appFw.so`, with adjacent entries:
   ```text
   appFw.so file offset   ID bytes        status bytes      Action
   0x03F17CD8             16 08 00 00     00 00 00 00       0x0816 DISPLAY_FTP_ERROR_INFO
   0x03F17CE0             17 08 00 00     00 00 00 00       0x0817 FTP_TRANSFER
   0x03F17CE8             18 08 00 00     00 00 00 00       0x0818 FTP_FUNCTION
   ```
   If confirmed against an actual firmware read, this **directly establishes the 0x0817 record at file offset `0x03F17CE0` and its first status byte at `0x03F17CE4`**, regardless of the erroneous arithmetic. The user-supplied byte row has not yet been independently re-read as part of this change.

   The previous claim that the table is indexed from zero by Action ID is not supported:
   ```text
   0x0817 * 8 = 0x40B8
   0x03F14C38 + 0x40B8 = 0x03F18CF0 (NOT 0x03F17CE0)
   0x03F17CE0 - 0x03F14C38 = 0x30A8 = 0x615 * 8
   0x0817 - 0x0615 = 0x0202
   ```
   A **nonzero-base, densely indexed table starting at Action ID 0x0202** would fit these offsets just as a sparse or searched record table might. Only inspection of the first records and the actual resolver/disassembly can establish the mechanism. Do not call the table sparse solely on the basis of these three adjacent IDs.

5. **Conflicting reported status suffixes must be resolved before firmware changes.** The earlier research note encoded the `0x0817` record as `17 08 00 00 00 01 01 01`, whereas the owner now reports `17 08 00 00 00 00 00 00`. Both identify Action `0x0817` at `0x03F17CE0` and report a zero byte at `0x03F17CE4`, but differ in bytes `0x03F17CE5`–`0x03F17CE7`. Do not silently treat them as equal or assume the remaining bytes are irrelevant. Read the 24-byte window `0x03F17CD8`–`0x03F17CEF` on the correct firmware/build (or verify an authenticated offline image), compare stock and patched-state copies, and trace the status word interpretation. In particular, test whether neighboring Action `0x0818` (`FTP_FUNCTION`) is a separate global dependency; its location **alone** does not prove that it needs a write.
6. **Unverified one-byte candidate:** `0x03f17ce4` (`00 -> 01`) was hypothesized to enable Action `0x0817`. It has not been proven to expose playback controls or cause successful upload on this camera. Do not change additional firmware bytes until actual on-camera state and relevant predicates have been established.

---

## 4. Physical ext2 Block & Sector Translation on `/dev/nflasha15`

By traversing the block pointers (direct, indirect `786495`, and double-indirect `786496`) of **Inode `24583`** (`/usr/lib/appFw.so`) on `/dev/nflasha15`, each file offset maps deterministically to a physical 4096-byte ext2 block and 512-byte partition sector:

| Target Window | `/usr/lib/appFw.so` Offset | Logical 4K Block | Physical ext2 Block | Partition Byte Offset | 512B Sector Index | Offset in Sector |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`EN-101` (`english_predicate`)** | `0x023080f8` (4B) | `8968` (`0x2308`) | `47891` (`0x0bb13`) | `0x0bb130f8` | **Sector `383128`** (`0x05d898`) | `+248` (`0xF8`) |
| **`FT-101` (`Action 0x0817`)** | `0x03f17ce4` (1B) | `16151` (`0x3f17`) | `55745` (`0x0d9c1`) | `0x0d9c1ce4` | **Sector `445966`** (`0x06ce0e`) | `+228` (`0xE4`) |
| **`FT-101` (`0x05a5`–`0x05b0`)** | `0x03f17524`–`0x03f17564` (9×1B) | `16151` (`0x3f17`) | `55745` (`0x0d9c1`) | `0x0d9c1524`–`0x0d9c1564` | **Sector `445962`** (`0x06ce0a`) | `+292`–`+356` |

### Sector-Level Cryptographic Hashes (512-Byte Sectors)
- **Sector `383128` (`EN-101` English Predicate)**:
  - Stock SHA-256: `9358ef826d5b75e363bd122aa5cfdd218d644d5f72fd061648f53314c326aa36`
  - Patched SHA-256: `4eed8b81e8e4543ddec9befb692c7b236b043cb9d96ae3a9873360cd778b27b3`
- **Sector `445966` (`FT-101` Playback FTP Action `0x0817`)**:
  - Stock SHA-256: `7c899be67183d264a73c0357ee4874247359d1a3dc10156279a0d8f53a618bdb1`
  - Patched SHA-256: `5669b7f9919257f3f7890d5b4fc26ef818119c0c239b6f63288218e9ae9bbb50`

---

## 5. Desktop GUI Architecture & Transactional USB Execution (`apps/a6700_customizer/`)

### 5.1 Decoupled Python 3.13 Host UI + Freestanding AArch64 Camera Helpers
To avoid Python C-extension ABI conflicts (`python312.dll` vs. host Python 3.13) while reusing the battle-tested USB service-mode transport from `Powerful6700-Windows-x64`:
1. **[`apps/a6700_customizer/app_gui.py`](file:///d:/LocalWork/Sony_research_6700/apps/a6700_customizer/app_gui.py)** implements the 6-step wizard using standard-library `tkinter`/`ttk` (Tk 8.6) with a custom high-DPI dark theme.
2. **[`apps/a6700_customizer/app_backend.py`](file:///d:/LocalWork/Sony_research_6700/apps/a6700_customizer/app_backend.py)** dynamically binds `third_party/a6700_unlock` and `_internal` data payloads (`libusb-1.0.dll`, `windows_auth`, `dump_range.elf`, `flash_write.elf`) without polluting `sys.path` with incompatible `.pyd` binaries.
3. **[`apps/a6700_customizer/targets.py`](../apps/a6700_customizer/targets.py)** defines 11 proposed byte targets (14 bytes total) and a known-preimage transition guard. This guards individual operations against unknown bytes, **not** against all possible firmware identity mismatches or multi-window partial-write failure. The field values do not establish that FTP works in Playback.

### 5.2 Camera-Side Execution Flow (`Senser` / `Jiritsu` Service Mode)
During an inspection or write session (`_session_context()` in [`app_backend.py`](file:///d:/LocalWork/Sony_research_6700/apps/a6700_customizer/app_backend.py)):
1. **MSC to Service Transition**: Sends the vendor SCSI command over Mass Storage to switch the camera into Sony's `Senser` (`PID 0x0336`) USB service mode.
2. **Authentication**: Completes the challenge-response handshake via `windows_auth` and opens a `JiritsuSession` with `ShellSession` (`/bin/sh`).
3. **Read-Only Inspection (`dump_range.elf`)**:
   - Uploads freestanding AArch64 binary `dump_range.elf` (`18,528` bytes, SHA-256 `ff46f662f4b8635742c5750317c32693860515292d46e883cf90b082b713cc7a`) to `/tmp/dump_range`.
   - Reads the exact byte windows from `/usr/lib/appFw.so` (`0x023080f8` and `0x03f17524`–`0x03f17ce5`), streams them back over the bulk endpoint, and saves a verified JSON snapshot in `backups/`.
4. **Transactional Write (`flash_write.elf`)**:
   - Uploads freestanding AArch64 binary `flash_write.elf` (`74,040` bytes, SHA-256 `94b45897d2e75b516998a3b2bd88b6d54d2b47c5d5c1438bc3050a7c7fb88823`) to `/tmp/flash_write`.
   - **Step A (Zero-Change Probe)**: Executes `flash_write /usr/lib/appFw.so 36733176 <current_byte>` to verify that `/usr/lib/appFw.so` can be opened `O_RDWR`, written via `pwrite64`, flushed via `fsync`, and read back identically.
   - **Step B (Target Patch Application)**: Applies the requested byte patches (`0x023080f8` and/or the 10 FTP offsets), calling `fsync()` after each write.
   - **Step C (Independent Read-Back Verification)**: Re-runs `dump_range.elf` across all 11 target windows and verifies 100% byte equality against the desired target state.
   - **Step D (Session Exit)**: Cleans up `/tmp` binaries and exits service mode cleanly.


---

## 6. Cross-Model Applicability: Sony A7CR (`ILCE-7CR`) vs. A7M5 (`ILCE-7M5`) Mainland China (`CN1`)

See **[`docs/CROSS_MODEL_ENGLISH_COMPARISON.md`](file:///d:/LocalWork/Sony_research_6700/docs/CROSS_MODEL_ENGLISH_COMPARISON.md)** for the complete cross-model analysis:
- **Sony A7CR (`ILCE-7CR` CN1) — Shares the Exact Same Process (`CXD90057` Platform)**:
  - Uses the identical `CXD90057_k8` FDAT encryption, `/dev/nflasha15` (`ext2` at `/usr`), `/usr/lib/appFw.so` `english_predicate` (`0x010d008f` check via `cset w20, eq`), and `Senser`/`Jiritsu` (`054C:0336`) service mode.
  - Requires only: (1) resolving A7CR's own `english_predicate` file offset in A7CR's `appFw.so`, (2) using A7CR's Mass Storage PID (`054C:0E8A`), and (3) invalidating the `*wbi4` Warm-Boot Image (`image_drop=1` ➔ `image_mode=0`) before cold reboot.
- **Sony A7M5 (`ILCE-7M5` / Alpha 7 V CN1) — Blocked at the USB `Senser` Authentication Layer (`BIONZ XR2` Platform)**:
  - While its UI localization still uses `.uxc` string banks and `0x010d008f`–`0x010d00b1` flags, Sony updated the USB `Senser` authentication handshake on the late-2025 **BIONZ XR2** platform, causing standard `CXD90057` / `pmca` service-mode handshakes to fail (`Invalid response: 9` / disconnect).

---

## 7. Commercial Tiering & Masked Functions Analysis

See **[`docs/MASKED_FUNCTIONS_AND_TIERING.md`](file:///d:/LocalWork/Sony_research_6700/docs/MASKED_FUNCTIONS_AND_TIERING.md)** for the complete research paper examining:
1. Why Sony masks FTP on the α6700: shared BIONZ XR (`CXD90057`) architecture with the FX30 cinema body and market tiering segmentation.
2. The exact Master Capability Table (`0x03f14c38`) and Playback Custom Key Action `0x0817` mechanism.
3. Complete taxonomy of masked functions in α6700 firmware:
   - **Category A (Regional Locks)**: Native English and 34 international languages.
   - **Category B (Model-Tier Masks with Working Backends)**: Shutter Closed when Power Off, Flexible Exposure Mode, and Electronic Shutter Sound.
   - **Category C (Unsafe / Incomplete Backends)**: Pixel Shift, Dynamic Active Stabilization, and Creative Looks FL2/FL3.
