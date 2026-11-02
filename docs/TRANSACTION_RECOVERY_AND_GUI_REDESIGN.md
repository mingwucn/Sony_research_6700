# Sony α6700 Customizer: Transaction Recovery Redesign & Handoff Plan

**Document Version**: 2.0.0  
**Date**: 2026-11-02  
**Target Hardware**: Sony ILCE-6700 (CN1 Mainland China SKU, Firmware Ver. 2.00)  
**Target Firmware Binary**: `/usr/lib/appFw.so` (Inode `24583` on `/dev/nflasha15`, Size `89,027,992` bytes, SHA-256 `e65fd595...`)  
**Repository Branch**: `codex/powerful6700-english-review-20261026` / `main` (clean, synchronized, and pushed to `origin`)

---

## 1. Executive Summary & Context

### 1.1 Verified Hardware Progress
1. **True Native English (`0x023080f8`: `mov w20, #1`)**:
   - Confirmed **100% working on physical hardware** by the user. `Setup -> Area/Date -> Language -> English` functions with zero `.uxc` text corruption.
2. **Network FTP Settings (`0x03F17524`–`0x03F17564`)**:
   - Confirmed accessible on physical hardware under `Network -> Transfer/Remote -> FTP Transfer`.

### 1.2 Discovered Deficiency & Root Cause
- **Observed**: The user tested Mode A (Playback Custom Key `0x0817` at `0x03F17CE4`), but `FTP Transfer` could not be assigned in `Playback Custom Key Setting`.
- **Root Cause**: In Sony BIONZ XR firmware, the custom key dispatcher checks if the parent Playback FTP feature subsystem is enabled before showing Action `0x0817` in the assignment list. Because all **81 Playback & Gallery menu permissions (`0x04BD7522`–`0x04C45F6A`)** were factory-disabled (`0x00`), the entire Playback FTP subsystem was suppressed by the UI filter.
- **Resolution (Mode B)**: We integrated all 81 Playback & Gallery menu permissions into `targets.py`. This natively unhides the complete `Playback -> Select to Transfer` menu (`此影像`, `多个影像`, `该组中所有影像`, `评级影像`, `RAW+J/H传输目标`, `传输JPEG大小`), which simultaneously unlocks Mode A (Custom Key assignment for Action `0x0817`).

---

## 2. Agreed Architectural Decisions (`/grill-me` Alignment)

| Area | Decision | Technical Rationale & Invariants |
| :--- | :--- | :--- |
| **Recovery Policy** | **Immediate `NEEDS_REVIEW` Lockout** | On any USB timeout, disconnect, or uncertain write response, immediately stop all further writes, lock the session, and prohibit blind retries or automatic rollbacks. Require an explicit read-only reconciliation scan before any resume or restore is permitted. |
| **Data Preservation** | **Raw Binary Span Dumps (`.bin`)** | Before sending any mutating command, save the full uncompressed raw pre-read stock buffer of each span (e.g. `span_04_stock.bin`, 122.6 KiB) to host storage and `fsync()`. Record its SHA-256 in an append-only `journal.jsonl`. |
| **Verification Scope** | **Full-Span Bit-for-Bit Readback** | After each span write, read back the **entire span length** (all `span.length` bytes, totaling 236 KiB across 7 spans) and verify that every single byte matches the sent buffer. Verifies both modified target bytes and unmodified interleaved bytes. |
| **Re-opening Workflow** | **Dedicated Reconciliation View** | If the app starts and detects an unresolved or `NEEDS_REVIEW` journal, intercept normal navigation, perform a read-only scan of the 7 spans, classify each (`UNTOUCHED_STOCK`, `FULLY_PATCHED`, `CORRUPTED_OR_PARTIAL`), and present safe rollback or resume actions. |
| **Truth in Labeling** | **Dual Metrics & Removed Claims** | Explicitly display both **Logical Changed Bytes (94 B across 92 targets)** and **Physical Write Footprint (7 spans / 236,018 B / 230.5 KiB)**. Remove all claims of "atomic installation", "guaranteed restoration", and "completed FTP support", replacing them with technical risk tiers (R4) and exact evidence boundaries. |

---

## 3. Current Project State & Completed Work

### 3.1 Completed Code & Commits
1. **`apps/a6700_customizer/targets.py`**:
   - Contains all 92 targets:
     - `TARGET_ENGLISH` (1 target, 4 B at `0x023080f8`)
     - `TARGET_FTP_PLAYBACK_KEY` (1 target, 1 B at `0x03f17ce4`, Action `0x0817`)
     - `TARGET_FTP_NETWORK_SETTINGS` (9 targets, 9 B at `0x03f17524`–`0x03f17564`)
     - `TARGET_FTP_GALLERY_MENUS` (81 targets, 80 B at `0x04bd7522`–`0x04c45f6a`; note that `0x04c16bd0` is invariant `00 -> 00` to hide duplicate blank parent `0x0262`)
   - `build_target_spans(targets, max_span=0x20000, max_gap=0x10000)`:
     - Groups the 92 targets into **7 contiguous spans**:
       - Span 0: `0x023080f8`, 4 B (English)
       - Span 1: `0x03f17524`, 1,985 B (Network FTP + Action 0x0817)
       - Span 2: `0x04bd7522`, 28,017 B (~27.4 KiB, Gallery group 0a)
       - Span 3: `0x04bee732`, 177 B (~0.2 KiB, Gallery group 0b)
       - Span 4: `0x04bff11a`, 125,593 B (~122.6 KiB, Gallery group 1)
       - Span 5: `0x04c2215a`, 80,241 B (~78.4 KiB, Gallery group 2)
       - Span 6: `0x04c45f6a`, 1 B (Gallery group 3)
     - Total write footprint: **236,018 bytes (~230.5 KiB)**.
     - Maximum span length: `125,593 B <= 131,072 B (0x20000)`, safely within the USB Senser 128 KiB limit.
   - Added canonical metric constants: `LOGICAL_TARGET_COUNT`, `LOGICAL_CHANGED_BYTES`, `PHYSICAL_SPANS_COUNT`, `PHYSICAL_WRITE_FOOTPRINT_BYTES`, `INTERLEAVED_PRESERVED_BYTES`.
2. **`apps/a6700_customizer/recovery_journal.py`** *(NEW)*:
   - Full append-only JSONL recovery journal with `meta.json` and explicit lifecycle states (`INITIALIZED`, `IN_PROGRESS`, `COMMITTED`, `NEEDS_REVIEW`, `RECONCILED`, `REVERTED`).
   - `save_stock_span_binary(span_idx, data)`: writes raw uncompressed bytes to `span_XX_stock.bin` with `fsync()`.
   - `record_span_verified`: validates full-span readback bytes; raises `RuntimeError` and sets `NEEDS_REVIEW` on any byte mismatch.
   - `find_latest_unresolved(base_dir)`: locates interrupted or unclosed sessions.
3. **`apps/a6700_customizer/app_backend.py`**:
   - Updated `DeviceBackend`:
     - Added `self.journals_dir = self.state_dir / "journals"`.
     - `get_unresolved_journal()`: checks for active / interrupted journals.
     - `reconcile_device(journal, progress)`: non-destructive read-only scan classifying all 7 spans as `UNTOUCHED_STOCK`, `FULLY_PATCHED`, or `CORRUPTED_OR_PARTIAL`.
     - `rollback_interrupted_session(journal, progress)`: rolls back non-stock spans using saved `span_XX_stock.bin` with full-span readback verification.
     - `apply_features()`: enforces unresolved journal lockout, records durable per-span transitions, writes complete stock binaries before mutating, and executes full-span bit-for-bit readback verification.
     - `restore_factory()`: durable per-span journaling with full-span verification.
4. **Unit Tests**:
   - `tests/test_recovery_journal.py`: 5 tests passing.
   - `tests/test_customizer_targets.py`: 6 tests passing.
   - Complete suite: **82/82 tests passing** in 0.35s (`python -X utf8 -m unittest tests/test_recovery_journal.py tests/test_customizer_targets.py tests/test_patch_spec.py tests/test_elf_static.py tests/test_ext2_readonly.py tests/test_uxc_readonly.py -v`).
5. **Git Status**:
   - Recent commits:
     - `4d5c40a`: `feat(ftp): enable Mode B (81 Gallery Playback menu permissions) with safe batched USB writes`
     - `b333023`: `feat(recovery): introduce durable per-span transaction journal and full-span readback verification`
   - Both `origin/main` and `origin/codex/powerful6700-english-review-20261026` are fully updated and synchronized.

---

## 4. Work Package for the Next LLM: Exact Action Items

The backend, target specifications, and journaling engine are **100% complete and tested**. The remaining task is to update the GUI frontend (`apps/a6700_customizer/app_gui.py`), documentation, and release packaging.

### Action 1: Add Dual-Metric Breakdown Card & Correct Disclosures in `app_gui.py`
In `apps/a6700_customizer/app_gui.py`:
1. **On Page 5 (`_build_features_page`)**:
   - Below the checkboxes, insert a new styled card (`style="Card.TFrame"`):
     - **Title**: `📊 写入范围与足迹披露 (Truth in Labeling)`
     - **Metric 1**: `逻辑修改目标：94 字节 (92 处固件权限与语言断言)`
     - **Metric 2**: `物理写入跨度：7 个固件段，共 236,018 字节 (~230.5 KiB)`
     - **Preservation Note**: `安全说明：为适配 Senser 块传输上限（<=128 KiB）并防止往返掉线，采用 7 段微小块写入；段内其余 235,924 字节经只读预读原样保留，写入前后均执行逐字节哈希比对。`
2. **Remove Unsubstantiated Claims**:
   - Replace any remaining occurrences of `原子写入` / `原子事务` with `顺序分段事务写入（7 个独立段，单段 <= 128 KiB，各段独立执行写入与校验）`.
   - Replace any occurrences of `100% 保证恢复` / `绝无风险` with `有条件出厂还原（依赖 USB 服务模式保持正常通信；若硬件断电损坏或固件不可访问，无法保证软件层恢复）`.
   - Replace `彻底攻克` / `完美解决` / `一键秒传` with `已解锁网络配置菜单、相册回放选择传输菜单与快捷键动作绑定（经固件静态与真机菜单回读验证；端到端实际网络长效传输稳定性仍受相机无线与服务器环境影响，属于持续验证中状态）`.
3. **Update Sidebar Safety Badge (`_build_sidebar`)**:
   - Change `严守只读预读与原子事务` to:
     ```
     🛡️ R4 固件段级分段事务
     前置全量快照 · 逐字节回读校验
     ```

### Action 2: Add Startup Reconciliation Intercept in `app_gui.py`
1. **Startup Check**:
   - In `App.__init__` or `show_page`:
     ```python
     unresolved = self.backend.get_unresolved_journal()
     if unresolved:
         self.show_page("reconcile")
     ```
2. **Build `reconcile` Page (`_build_reconcile_page`)**:
   - Add nav item: `("reconcile", "⚠️ 7. 会话恢复与对账")` (only shown or highlighted when an unresolved session exists).
   - Display card:
     - Warning banner: `⚠️ 检测到上次写入会话未正常闭环或被中断 (状态: NEEDS_REVIEW)`
     - Details of the unresolved session (`session_id`, `created_at`).
     - Button 1: `🔍 开始只读对账扫描` -> calls `self.backend.reconcile_device()`.
       - Renders a list of the 7 spans showing their classification (`UNTOUCHED_STOCK` in green, `FULLY_PATCHED` in blue, `CORRUPTED_OR_PARTIAL` in red).
     - Button 2: `🔄 一键安全回退全部修改段` -> calls `self.backend.rollback_interrupted_session()`, which restores each non-stock span from `span_XX_stock.bin` with full-span readback verification.
     - Button 3: `▶️ 恢复并继续未完成段` -> resumes writing only unpatched spans.

### Action 3: Build & Publish Standalone Portable Package
1. Run the test suite:
   ```powershell
   python -X utf8 -m unittest tests/test_recovery_journal.py tests/test_customizer_targets.py tests/test_patch_spec.py tests/test_elf_static.py tests/test_ext2_readonly.py tests/test_uxc_readonly.py -v
   ```
2. Run the build script:
   ```powershell
   python -X utf8 tools/build_dist.py
   ```
   - Automatically builds `dist/SonyA6700Customizer/` and `dist/Sony_a6700_Customizer_v1.0.0_win64.zip`.
   - Runs the clean-PATH self-test in a fresh temporary directory.
3. Publish the release to GitHub:
   ```powershell
   python -X utf8 tools/publish_release.py
   ```

### Action 4: Documentation Synchronization
1. Update `docs/USER_GUIDE_CN.md` and `README.md` to reflect:
   - The dual metrics: 94 logical bytes vs 230.5 KiB physical footprint across 7 spans.
   - The recovery journal and reconciliation flow.
   - Removal of non-technical claims.
2. Update `research/STATE.json`:
   - Set `phase`: `"transaction_recovery_redesign_and_truth_in_labeling_complete"`.
   - Update timestamp and test suite counts.
3. Commit and push:
   ```powershell
   git add apps/a6700_customizer/app_gui.py README.md docs/USER_GUIDE_CN.md research/STATE.json
   git commit -m "feat(gui): show true write footprint, add reconciliation view, and correct absolute claims"
   git push origin <branch>
   ```
