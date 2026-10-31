# α6700 Firmware 2.00: Native English Language & Playback FTP Candidates

Date: 2026-11-01  
Evidence: **static-inference**, **offline-tested**  
Target model: Sony ILCE-6700 (Mainland China SKU, Firmware 2.00)  
Camera commands: **none**  
Network commands: **none**  

---

## 1. Executive Summary

This document specifies the exact, minimal, byte-level modifications required to enable:
1. **True Native English Language Menu (`EN-101`)**: Unhiding English in the camera's native Setup language selection menu without replacing or corrupting Chinese resource files, and allowing native persistence to Backup property `0x02cf0000`.
2. **Playback Gallery FTP Custom Key (`FT-101`)**: Enabling Action ID `0x0817` (`FTP_TRANSFER`) in the Playback Custom Key assignment list so that pressing a physical custom key during photo playback immediately queues images for FTP upload.

Both modifications target solely the application filesystem `/dev/nflasha15` inside `/lib/appFw.so`. No kernel, bootloader, warm-boot image (`/dev/nflasha5`), CP processor (`/dev/nflasha8`), or raw Backup database EEPROM structures are modified.

---

## 2. Firmware Identifiers & Baseline Hashes

All offsets and byte expectations are anchored to the official Sony Mainland China Ver. 2.00 release:

- **Update Package**: `BODYDATA.DAT` (1,024,017,848 bytes)
  - SHA-256: `d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c`
- **Application Filesystem Image**: `application-nflasha15.ext2` (673,741,824 bytes, 1024-byte blocks)
  - SHA-256: `8dfa61a10f3c91f39e13fc640ad022afcd697168a9d3a3d15353a0ad1e70f872`
- **Target Application Binary**: `/lib/appFw.so` (89,027,992 bytes, Inode 24583)
  - SHA-256: `e65fd595052be5d0e98ce8000dfcb94f90a2f8309de70ef140375052009b0ef3`

---

## 3. Candidate 1: Native English Menu Availability (`EN-101`)

### 3.1 Mechanism & Disassembly
In `appFw.so`, the Language Menu structure contains 34 language choice entries, each formatted as a 160-byte (`0xa0`) record. Choice Index 0 represents English:
- Choice Index: `0`
- Resource ID: `0x0204e2be` (String "English" in `string_english.uxc` / `string_simplifiedchinese.uxc`)
- Function Pointer Slot: Offset `0x04b44198` (ELF VA `0x04b54198`), populated via `.rela.dyn` relocation at `0x00aa3a58`.
- Availability Predicate: Function `english_predicate` at link-time VA `0x023080d0`.

The factory implementation of `english_predicate` executes:
```asm
0x023080d0: a9bd7bfd   stp  x29, x30, [sp, #-48]!
0x023080d4: 910003fd   mov  x29, sp
0x023080d8: a90153f3   stp  x19, x20, [sp, #16]
0x023080dc: 9100a3b3   add  x19, x29, #0x28
0x023080e0: aa1303e0   mov  x0, x19
0x023080e4: 9438be2b   bl   #0x3137990       ; stack object constructor
0x023080e8: 94320356   bl   #0x2f88e40       ; getEnglishAvailability(&obj)
0x023080ec: b9400000   ldr  w0, [x0]         ; load availability Backup value
0x023080f0: 7100041f   cmp  w0, #1           ; compare with 1 (enabled)
0x023080f4: aa1303e0   mov  x0, x19
0x023080f8: 1a9f17f4   cset w20, eq          ; w20 = (w0 == 1) ? 1 : 0
0x023080fc: 9438bd28   bl   #0x313759c       ; stack object destructor
0x02308100: 2a1403e0   mov  w0, w20          ; return value
0x02308104: a94153f3   ldp  x19, x20, [sp, #16]
0x02308108: a8c37bfd   ldp  x29, x30, [sp], #48
0x0230810c: d65f03c0   ret
```

On Mainland China cameras, Backup property `0x010d008f` returns `2` (disabled), causing `cset w20, eq` to evaluate to `0`. Consequently, English is suppressed from the setup menu.

Replacing instruction `cset w20, eq` at `0x023080f8` with `mov w20, #1` guarantees that `english_predicate` unconditionally returns `1` (True) while preserving all stack constructor/destructor invariants and ABI conventions.

### 3.2 Exact Byte Specifications
- Target File: `/lib/appFw.so`
- Link-time VA / File Offset: `0x023080f8`
- Ext2 Logical Block: `35872` | Physical Block: `191564`
- Ext2 Image Byte Offset: `0x0bb130f8` (`196,161,784`)
- Target Device / Partition: `/dev/nflasha15`
- 512-byte Sector: `383128` (`0x0005d898`)
- Relative Offset in Sector: `+248` (`0x00f8`)
- Pre-Image (Factory): `f4 17 9f 1a` (`cset w20, eq`)
- Patched (Modified): `34 00 80 52` (`mov w20, #1`)
- Inverse (Rollback): `f4 17 9f 1a`
- Sector Hashes:
  - Factory Stock Sector SHA-256: `9358ef826d5b75e363bd122aa5cfdd218d644d5f72fd061648f53314c326aa36`
  - Patched Sector SHA-256: `4eed8b81e8e4543ddec9befb692c7b236b043cb9d96ae3a9873360cd778b27b3`

---

## 4. Candidate 2: Playback Gallery FTP Custom Key (`FT-101`)

### 4.1 Mechanism
The Playback Custom Key selection UI (`Menu 0x02aa`) gates available action assignments by checking model capability table entries in `appFw.so`.
- Action ID: `0x0817` (`FTP_TRANSFER`)
- UI Resource String: `0x021c668e` ("FTP Transfer" / "FTP传输")
- Capability Entry Offset: `0x03f17ce0` (8 bytes)
  - `0x03f17ce0..0x03f17ce3`: `17 08 00 00` (Action ID `0x0817`)
  - `0x03f17ce4`: `0x00` (Disabled on ILCE-6700 in factory firmware)
- Powerful6700-Windows patched Network Menu settings `0x05a5`–`0x05b0` at `0x03f17524`–`0x03f17564` (Sector 129210), but omitted Sector 129214 (`0x03f17ce4`).
- Toggling `0x03f17ce4` from `0x00` to `0x01` enables Action `0x0817`, permitting assignment of "FTP Transfer" to any Playback Custom Button (e.g. C1, C2, Trash/Delete).

### 4.2 Exact Byte Specifications
- Target File: `/lib/appFw.so`
- Link-time VA / File Offset: `0x03f17ce4`
- Ext2 Logical Block: `64607` | Physical Block: `222983`
- Ext2 Image Byte Offset: `0x0d9c1ce4` (`228,334,820`)
- Target Device / Partition: `/dev/nflasha15`
- 512-byte Sector: `445966` (`0x0006ce0e`)
- Relative Offset in Sector: `+228` (`0x00e4`)
- Pre-Image (Factory): `00`
- Patched (Modified): `01`
- Inverse (Rollback): `00`
- Sector Hashes:
  - Factory Stock Sector SHA-256: `7c899be67183d264a73c0357ee4874247359d1a3dc10156279a0d853a618bdb1`
  - Patched Sector SHA-256: `5669b7f9919257f3f7890d5b4fc26ef818119c0c239b6f63288218e9ae9bbb50`

---

## 5. Combined Transaction Matrix

| Target ID | Partition | Sector | Rel Offset | Width | Pre-Image | Target Bytes | Purpose |
|---|---|---:|---:|---:|---|---|---|
| `APP-EN-01` | `/dev/nflasha15` | `383128` | `+248` | 4 bytes | `f4 17 9f 1a` | `34 00 80 52` | Native English menu predicate unmask |
| `APP-FTP-01` | `/dev/nflasha15` | `445966` | `+228` | 1 byte | `00` | `01` | Playback FTP custom key assignment |

Total sectors modified: **2 sectors** (1,024 bytes).  
Total bytes modified across entire body: **5 bytes**.  
All other sectors and partitions remain strictly 100% factory identical.
