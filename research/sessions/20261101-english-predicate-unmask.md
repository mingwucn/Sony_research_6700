# EN-101: English Menu Predicate Resolution & Combined Patch Specification

Date: 2026-11-01  
Evidence: **static-inference**, **offline-tested**  
Camera commands: **none**  
Network commands: **none**  

## 1. Summary of Work

In this session, we completed the static analysis and binary tracing for Work Package 2 (True Native English Unlock):

1. **Located English Menu Choice Record**:
   - Traced table in `appFw.so` at offset `0x04b44158` (ELF VA `0x04b54158`).
   - Choice 0 is English, associated with String Resource ID `0x0204e2be` ("English").
   - Function pointer slot at `0x04b44198` points directly to `english_predicate` (`0x023080d0`).

2. **Decompiled `english_predicate` (`0x023080d0`)**:
   - Function queries Backup availability item `0x010d008f`.
   - Evaluates: `cset w20, eq` at offset `0x023080f8` against value `1`.
   - On Mainland China firmware, Backup item returns `2` (disabled), suppressing English from the menu.
   - Patching instruction `0x023080f8` from `cset w20, eq` (`f4 17 9f 1a`) to `mov w20, #1` (`34 00 80 52`) forces the function to return `1` (True) while preserving all stack constructor/destructor invariants.

3. **Global Cross-Reference Audit**:
   - Scanned all 89MB of `appFw.so` for references to `english_predicate` (`0x023080d0`).
   - Zero direct branch/call instructions (`BL`/`B`) found.
   - Exactly two pointer references found:
     - Offset `0x04b44198`: Static pointer in Menu choice structure.
     - Offset `0x00aa3a68`: Addend in ELF `.rela.dyn` relocation table targeting VA `0x04b54198`.
   - Confirmed that `english_predicate` is strictly isolated and invoked exclusively by the Language Setup menu.

4. **Ext2 Physical Sector Mapping**:
   - Mapped both `english_predicate` and `FTP_TRANSFER` action capability offsets to raw ext2 block devices on `/dev/nflasha15`:
     - English Menu: Sector `383128`, rel `+248` (4 bytes: `f4179f1a` -> `34008052`).
     - Playback FTP: Sector `445966`, rel `+228` (1 byte: `00` -> `01`).
   - Computed and verified factory pre-image and patched sector SHA-256 hashes against `application-nflasha15.ext2`.

5. **Safety & Scope Boundary**:
   - The entire enhancement consists of **2 sectors** on `/dev/nflasha15` (5 bytes total).
   - Zero modifications to NOR flash, EEPROM/Backup partition, radio calibrations, or WBI.
