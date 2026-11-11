# Playback FTP Extras Experimental 0.6.0

The offline FTP filter prototype uses the shared A7CR workbench shell from the owner's referenced build. **Advanced → Prepare offline filter candidate…** connects an authored native FTP query to Sony's playback sets and existing active selector/count publisher in a private App candidate. It saves an exact inverse. This is an offline file action; **camera installation of filtering is disabled**. Working filtering on the camera has not been established.

To inspect this work now, open the new EXE, choose the Advanced tab and select **Prepare offline filter candidate…**. Select a complete private α6700 CN1 Body 2.00 App reference, then an existing private output folder outside Git and system Temp. The source must match the complete pinned build after the existing 99-field English/FTP guard. Those fields are preserved exactly; unknown bytes stop preparation. A new folder contains `candidate.app`, `inverse.original.app`, `plan.json` and `result.json`. Keep these private. This action needs no camera, leaves the selected inspection and acknowledgement state intact, and starts no service operation.

The active prototype supports FTP status alone, including native pair/group rules. All ten other filter criteria must be off. The preview-count handler is unchanged. It uses a bounded 64-result immutable registry; once full it refuses a new result and retains the old one until the App restarts. The exact loader layout, native allocation behavior, recursive database read locks and a current-image installation/recovery route still need qualification. Do not install the offline candidate with an older sparse writer. The existing shortcut/title actions below remain separate.

This private experimental build offers three separate camera changes for the owner-confirmed **ILCE-6700, Body 2.00**: expose **FTP Trans. (This Img.)** in playback Custom Key Setting, expose general **FTP Transfer** for C1/C2, or correct the third FTP-status label to Sony's existing **Success. Trans. Img.** text. All three are experimental; the general-transfer reader and writer have offline qualification but have not been tested on this camera. These actions leave playback-filter execution unchanged.

**FTP Transfer** (general selection/progress, roster row `0x4a8`) is a separate experimental action. It reads exactly two 512-byte App windows, at `0x03788e00` (the existing `0x4c7` current-image row) and `0x03788c00` (the general-transfer row), then plans one logical byte change at `0x03788dc3` for C1/C2 category 21. It reads and writes no WBI. The observed current-image assignment is preserved, including an already-enabled `0101` pair; title/WBI state and the ten playback permission halfwords are outside this two-window observation. The writer changes one logical byte in one 512-byte transaction window; physical write extent and geometry remain **UNVERIFIED**. A separate native reader verifies the same two windows after the write. Failed-start recovery is unproven; the saved two-window preimage is a partial backup, not a full firmware backup. Use the separate review prompt and stop on uncertain execution.

The owner reports normal English and Network FTP working, and the FTP filter menu visible after the earlier ten-byte permission change. Version 0.4.1 requires those ten permission halfwords to remain enabled. It preserves the 0.4.0 and 0.3.1 packages and does not repeat that earlier action.

Service authentication and helper staging may change camera files. Persistent changes could affect the working camera. Full storage backup, recovery after failure to start, physical WBI geometry and WBI integrity handling remain unproven. The saved preimages are partial backups. An experimental label and passing tests do not establish safety or working camera behavior.

## Unified Quick Unlock & Connection Auto-Sensing

Version 0.6.0 adds the general FTP Transfer reader and action to the existing manual inspection and separate button routes:

1. **Live USB Connection Auto-Sensing**:
   - The top banner continuously monitors Windows PnP devnode status in the background.
   - 🟢 **Ready (`0E76 MSC`)**: WinUSB is bound and camera is ready for service.
   - 🟡 **Driver Needed (`0E76 MSC`)**: Camera is present in Mass Storage mode but needs WinUSB.
   - 🟠 **Wrong Mode (`096F`)**: Camera is in PC Remote / Updater mode. Guidance is displayed directly on screen: switch camera USB Connection Mode to Mass Storage (MSC) (`Menu ➔ Network ➔ USB ➔ USB Connection Mode ➔ Mass Storage`).
   - ⚪ **Disconnected**: Prompts to connect camera in Mass Storage mode.

2. **⚡ Quick Unlock (Recommended)**:
   - Current-image action: `[✓] Enable current-image FTP shortcut` (the UI reports if it is already active).
   - General action: `[ ] Enable FTP Transfer for C1/C2` (selected and inspected separately).
   - Cosmetic Follow-up: `[ ] Correct Transferred-Image Menu Label` (optional).
   - Status Badges: Displays `[✓ Already Active]` if the function is already present in firmware, avoiding redundant writes.
   - **`🚀 Unlock Selected Functions` Button**:
     - Selects the 7-window read for current-image/label actions or the 2-window App-only read for FTP Transfer.
     - Shows a plain-English confirmation with the exact target, partial backup scope and recovery limits.
     - Performs one selected write with native guards and a profile-specific independent readback.
     - Leaves assignment, restart persistence and real transfer behavior to explicit camera checks.

## Inspect and follow up in the same window

1. Close the original customizer and all other camera tools. Use only the same alpha6700, with normal operation and English working. Connect USB in Mass Storage mode with the existing drivers.
2. Open `SonyA6700PlaybackExtrasExperimental.exe`. **Check connection** reads Windows metadata only. An existing WinUSB binding needs no installation. The separate **Install USB driver** workflow retains its exact-target review; service actions never install a driver. A7CR, unknown models, multiple Sony devices and shared service PID `0336` are excluded from driver installation.
3. Check the camera-conditions box. Select **Read playback state** for the current-image shortcut/label, or **Read FTP Transfer row** for the general action. The general read stages a temporary reader for exactly two App windows and no WBI. Wait for the worker to finish; the app selects the inspection only if all five files validate and its final report matches the saved result. Nothing starts automatically afterward.
4. Keep the app open. Follow the report's disconnect instructions, check the normal screen and English, reconnect in Mass Storage mode, and check the camera-conditions box again. The matching inspection remains selected. Choose the corresponding action and confirm its exact review. General FTP Transfer requires the two-window inspection; the current-image shortcut and label require the seven-window inspection.
5. After a verified write, follow its physical-check instructions. The consumed inspection is cleared. Once the camera is checked/reconnected and the conditions box checked, select **Read playback state** again in the same window before choosing the other change. Each read/write is a separately selected operation; one worker owns the camera at a time.

Preserve every private `RECORD_DIR`. Keep the five inspection files together: `intent.json`, `result.json`, `capture.json`, `response.bin`, and `transport-UNVERIFIED.bin`. General FTP Transfer accepts only its complete two-window App record; current-image/label actions accept their seven-window record. A version 0.3.1 six-window capture cannot be used here. **Choose saved inspection folder** validates the selected profile before use.

A report that stops at preflight with **no service attempt** contains no capture. In particular, the owner's 182208 record has only intent/result and reports that exactly one healthy Sony storage-mode device was not found. This is a connection refusal, not a completed inspection. Version 0.4.1 explains it clearly, leaves the incomplete folder unselected, and allows a new explicitly selected connection check/read after correcting the connection. It never retries by itself.

A complete **PERSISTED** capture can coexist with an unconfirmed service STOP and an exit code of 2. The app validates and retains that capture, but still requires the normal-screen/English/reconnection acknowledgement before another camera operation. A missing or malformed final report, conflicting reports, incomplete service read, or uncertain write blocks further camera actions for review. Do not infer that a helper stopped from an observation timeout. Preserve power/USB/records whenever the report directs it; restarting the app is not a recovery method.

## Exact changes

| Action | Intended logical change | Software transaction targets |
| --- | --- | --- |
| Playback FTP shortcut | App file `0x03788e52` and `0x03788e53`, each `00` to `01`, for existing playback assignment categories 20 and 21 | One App window at `0x03788e00`; the writer never opens WBI |
| General FTP Transfer | App file `0x03788dc3`, `00` to `01`, for C1/C2 category 21 | One App transaction window at `0x03788c00`; the two-window App observation also checks the existing `0x4c7` row at `0x03788e00`; no WBI reads or writes |
| Transferred-image label | Title RID `0x020080ce` to `0x02006077` at App file `0x04c36b8c` and existing assumed WBI device-file coordinate `0x025c1d8c`; two changed bytes per field | WBI window `0x025c1c00`, then App window `0x04c36a00` |

Every transaction target is 512 bytes. These are software coordinates, not proven physical flash units; two or four logical byte changes do not bound physical writes. The label action preserves the smartphone leaf using the old title and all UXC resource files. These actions do not change existing button assignments, transfer-handler instructions, backend parameter `0x568`, firmware version, region, calibration or English settings.

The seven-window observation includes App `0x04bca200`, `0x04c0b400`, `0x04c36a00`, assumed WBI device-file `0x02514400`, `0x02586600`, `0x025c1c00`, and App `0x03788e00`. The three existing WBI locations remain assumed mappings; no WBI shortcut counterpart is inferred.

## Checks and retained records

The tool validates all five saved inspection files, selected fixed profile and native payload pins, nonces, transport, digests and recomputed analysis. The seven-window path accepts only consistent old/new App and WBI title values plus a wholly disabled/enabled current-image shortcut pair. The two-window path accepts only the pinned 0x4c7 current-image pair and 0x4a8 General FTP Transfer byte variants. Unknown bytes or partial states stop for review. An already applied action sends no service operation or writer; it reports only what the selected inspection contains.

Before staging a writer, a fresh capture for the selected profile must exactly equal the selected inspection. The tool saves and reads back preimages in a primary app-data location and a secondary location on a separately selected local fixed drive: 3,584 bytes for seven-window actions or 1,024 bytes for General FTP Transfer. Set `SONY_A6700_PLAYBACK_EXTRAS_SECONDARY_BACKUP` to an absolute directory on that separate drive before starting the tool. The writer refuses to stage if the secondary path is unset, is not a fixed local drive, or is on the same drive as the primary copy. Journals are persisted before upload. These are partial backups, not a full firmware image, and they do not prove failed-start recovery. Preserve both.

The native writer checks the complete App using its action-specific 99-field (current-image/label) or 100-field (General FTP Transfer) normalization policy before and after, stable App metadata and unchanged English bytes. It checks each full target immediately before writing and verifies its readback. A separate reader then requires all seven or both App windows to equal the plan. The two label targets are not atomic together. There is no automatic retry, rollback, WBI invalidation or deletion of staged camera files.

Native deadlines are 60 seconds to reach the first write and 120 seconds overall, checked between calls. They cannot cancel a blocked camera syscall. The host response wait is 180 seconds. A timeout does not prove the helper stopped.

**If writer completion is uncertain, keep camera power and USB connected, preserve every record, and stop for review. Do not retry, send another service command, disconnect, roll back or delete files.** The app withholds automatic service STOP after an operation error. A native verified result, full independent readback and service exit are separately reported. A service STOP error does not erase completed readback evidence or prove normal camera operation.

After completed readback, follow the report: when the access lamp is off, disconnect USB and check the normal screen, English and Network FTP. Preserve reports even if service exit was unconfirmed.

## Physical acceptance still required

For the shortcut, check **Setup → Operation Customize → Custom Key Setting (Playback)**. Check the existing C1/C2/MOVIE assignment category and the existing Fn/smartphone assignment category. Confirm **FTP Trans. (This Img.)** is listed, assign it to an available button, and verify it sends the displayed image through the camera's configured FTP connection. A visible label alone does not prove assignment or transfer.

For General FTP Transfer, check the same Playback Custom Key Setting picker and confirm **FTP Transfer** appears for C1/C2. Assign it to a different key from **FTP Trans. (This Img.)**, then restart normally and confirm both bindings remain. With Auto Transfer off, use the general action to select exactly two of the three test JPEGs and confirm it returns to the transfer-progress screen without adding files. Display the third JPEG and use the current-image action; only that third file should arrive. Compare each receiver receipt's size and SHA-256 with its card original. If the camera picker or behavior differs, preserve the report and stop rather than repeating the write.

For the label, check **Playback Filter Condition → FTP Transfer Status** and confirm the third choice reads **Success. Trans. Img.** instead of the internal token. Check English and Network FTP, then after normal shutdown and a restart check persistence. A battery-out restart may be needed to distinguish retained runtime state, as in the earlier permission test; perform it only after shutdown and with no uncertain writer pending.

Report each selected action, its `RESULT`, the observed UI text/behavior, restart persistence and receipt hashes, plus normal English/Network FTP operation. These actions do not claim to fix filtering after **Execute Filter**.

## Offline checks and provenance

The EXE supports `--self-check`, `--writer-self-check`, `--describe`, `--transport-self-check`, `--gui-self-check`, `--driver-self-check`, `--usb-observer-self-check`, `--workflow-self-check`, `--filter-payload-self-check` and `--general-transfer-reader-self-check`. These checks perform no camera commands or driver changes. The file-only CLI is `--prepare-filter-candidate ABSOLUTE_APP_PATH --output-parent ABSOLUTE_PRIVATE_FOLDER`. `BUILD.json` records source and dependency pins, per-action native payloads, source hashes and frozen check results. Authored filter source, payload and sanitized build metadata are included; complete App references/candidates are excluded. Keep the complete folder with its `_internal` directory; the EXE is not standalone.
