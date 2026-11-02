# FT-101: Missing on-camera Network FTP menu — differential diagnosis

**Recorded:** 2026-11-02. **Evidence class:** owner report + pinned GitHub source comparison + static catalog analysis. **Camera commands:** none. **Firmware writes:** none. **Runtime FTP test:** none.

## User correction, and contradiction to reconcile

The owner has now **explicitly confirmed** that **`FTP Transfer Function` is ABSENT—not greyed out or switched Off—under `MENU → Network → Transfer/Remote`** on the owner's firmware-modified Sony α6700, while the upstream `xyzhangxin/sony-a6700-powerful` demonstration/implementation shows that entry. Native English is correctly enabled on the owner's camera. **This resolves the earlier ambiguity about where the owner checked**; it does not establish which FTP permission or runtime source is responsible.

This conflicts with the earlier summary in issue #1, which stated that the Network FTP page could be opened but Playback/Gallery FTP was absent. The new report takes precedence for the present investigation, but **the conflicting observation must be recorded, not silently overwritten**. It is not yet known whether the earlier "Network page opens" report described a different executable or installed state. The **current** observation now unambiguously refers to the `Network → Transfer/Remote` submenu. Preserve the historical contradiction, but do not request another check merely to determine whether this FTP entry is absent.

**Upstream's claimed location is** `MENU → Network (网络) → Transfer/Remote (传输/远程) → FTP Transfer Function (FTP传输功能)`. This is **not** a separate top-level menu tab. If the user is expecting a Playback Gallery menu, there is a second distinct issue; Sony's related-camera documentation distinguishes Network FTP setup and Playback custom-key single-image transfer.

The working English patch is independent evidence of effective execution of the narrow `appFw.so` language predicate (`0x023080F8`). It **does not prove that FTP menu data are refreshed**, that FTP/WBI runtime flags are enabled, or that all changes in an installer reached this camera.

## Source pins (2026-11-02)

- Owner repository `mingwucn/Sony_research_6700` `main` @ `55054b91319393c598246c2e8302f84c0f74eab0`. The current target definitions are `apps/a6700_customizer/targets.py`.
- Upstream `xyzhangxin/sony-a6700-powerful` `main` @ `d5bb9485dfe7cc4bf13a4ead3a7437c2f40240a9`. Canonical profile: `应用/src/a6700_unlock/data/a6700-2.00.json`, rendered help `应用/docs/FEATURES.md`, user guide `Powerful6700使用说明.md`.
- Existing historical release: owner's original `v1.0.0` source tag contains nine Network targets and the one proposed Playback action but **not** the 81 App FTP permissions. Current `main` includes those 81. A GitHub release's attached ZIP may differ from its tag due to prior asset replacement, so do not infer installed bytes without readback.
- Related issues/PRs: issue #1, draft safety PR #2 (written against older target list), draft full plan PR #3.

## Crucial exact comparison: upstream menu permissions have App AND WBI representations

The upstream `feature=ftp` catalog contains exactly **242 records / 240 changed bytes**:

| View | Total records | Changed bytes | Description |
|---|---:|---:|---|
| `app` | 90 | 89 | 9 network parameter entries + 81 FTP permission records (one invariant) |
| `wbi` | 152 | 151 | 69 menu permission entries + 38 unsupported reference-counter fields + 36 derived support flags + 9 runtime availability entries |
| **Total** | **242** | **240** | These are logical changed bytes; physical writes may be much larger |

The **69 WBI menu permissions map one-to-one by menu ID** to 69 of the 81 App menu permission records: same 69 unique parent/child/leaf menu IDs, including parent `0x226` and duplicate-parent `0x262` (invariant `00 → 00`). The **other 12 App-only permission records** are described by upstream as historically validated additional parent-column modifications, not as proof of a separate Gallery FTP menu.

Nine WBI **runtime availability** entries appear at logical decoded WBI2 offsets:

| FTP parameter | WBI logical offset | Source's purpose |
|---|---|---|
| `0x05A5` | `0x0E4A6E2C` | FTP master switch runtime availability hash flag |
| `0x05A6` | `0x0E4A6E4C` | Connection-method model availability |
| `0x05A8` | `0x0E4A6E6C` | Server setting model availability |
| `0x05AA` | `0x0E4A6E8C` | Automatic-transfer model availability |
| `0x05AC` | `0x0E4A6EAC` | RAW/JPEG target model availability |
| `0x05AD` | `0x0E4A6ECC` | JPEG transfer setting model availability |
| `0x05AE` | `0x0E4A6EEC` | HEIF transfer setting model availability |
| `0x05AF` | `0x0E4A6F0C` | Transfer target model availability |
| `0x05B0` | `0x0E4A6F2C` | FTP power-saving setting model availability |

**Critical address warning:** these are offsets within a **248,376,320-byte decoded, extracted WBI2 logical image**. They are **not** `/dev/nflasha5` raw sector offsets, direct physical addresses, or a patch recipe. Upstream's profile sets `scope=offline-known-snapshot-only` and `device_write_supported=false`; its released app's device writer is a separately reviewed implementation. Never use these offsets with the current App-only writer, force a WBI rewrite, or invalidate WBI as a speculative "cache flush."

**Hypotheses:**
- **H1 — older owner release installed.** The user's applied package could contain only the 9 Network flags + one `0x0817` action, not all App permissions. The newly added 81 App permission records may never have been installed.
- **H2 — App permissions installed but WBI state is stale/unmodified.** The menu hierarchy and/or runtime model availability may still be disabled in WBI. This is a strong lead because upstream changes both views and current tool changes only App; **not yet a proved boot dependency**.
- **H3 — another dynamic/mode predicate.** App and WBI may already be compatible while runtime settings, a missing parent menu, FTP global state, camera mode, or per-model dispatch still suppress the entry.
- **H4 — menu interpretation mismatch.** Upstream's FTP is under `Network → Transfer/Remote`, not an independent top-level tab or an automatically inserted `Playback → Select to Transfer` page.
- **H5 — incomplete/uncertain firmware-write session.** No reboot/current state is established, and current seven-span code can have a partial or unresolved transaction. Never repeat a write without journal reconciliation.

**What the English result rules out:** an explanation that *no modified appFw.so code can possibly run* on this camera. **What it does not rule out:** stale runtime-menu data, unmet FTP-specific flags, incomplete FTP target installation, or an unavailable native transfer action.

## Minimal differential diagnostic, in order of risk

### D0 — owner camera screen only, **no camera firmware modification** (R1 ordinary observation)

1. Record which ZIP/build was used (`v1.0.0` original asset vs subsequently updated build vs source `main`). Record executable build identifier and SHA-256 if available. Release tag alone is not enough. **This is the highest-value next unanswered question.**
2. **Already completed by the owner:** `MENU → Network → Transfer/Remote → FTP Transfer Function` = **ABSENT**. Do not re-request or re-run this check without a documented change to installed software/state; screen photography is optional corroboration and should conceal any personal details.
3. Separately inspect `Setup → Operation Customize → PB Custom Key Setting` for `FTP Transfer` assignment. Do not confuse missing playback action with missing Network settings.
4. Check the existing USB customizer's **last completed transaction journal**, original target-state JSON and unresolved-session state on the host, without connecting the camera. Identify whether the executed build could have installed all 81 App menu fields. Use the `backup_a6700_YYYYMMDD_HHMMSS.json` snapshots in the portable build's `data/backups/` or source build's `.data/customizer/backups/`. These are **App target-state snapshots**, not WBI dumps or full firmware backups. The JSON format stores `targets["0x........"]` with `feature`, `bytes_hex`, and `status`.

   **Offline triage using already-existing JSON, without connecting the camera:** Look for one record per nine Network flag offsets (`0x03F17524`–`0x03F17564` in the source's exact sparse list), plus the 81 App permission records (`0x04BD7522`–`0x04C45F6A`, exact set in `targets.py`), and the independent `0x03F17CE4` action candidate. **If the backup predates an installation, its values do not prove what was later written.** An older tool may have produced only 11 targets total (9 Network, playback action, English). A current-source backup may contain 92 targets (81 permission records included). A snapshot containing all targets still is not proof of current storage if subsequent operations occurred.

   **Interpretation:** nine Network records and no 81-permission records suggests an old tool version, not necessarily an unsuccessful write. A recent 92-target snapshot with most permissions `STOCK` suggests incomplete App menu installation. A recent snapshot showing all App FTP targets `PATCHED` but FTP entry `ABSENT` makes a **runtime/WBI gate** a stronger hypothesis. Any `MISMATCH` means stop further writes. Never conclude `FTP operational` from a `PATCHED` group.
5. Confirm current firmware `Ver. 2.00` and that the language remains native English; do not reset settings or change radio region.

### D1 — only if necessary, separately approved service-mode inspection (R2)

A service read of target firmware windows **does not issue a target patch**, but may authenticate, change USB mode and execute a temporary helper; do not describe it as harmless read-only R1. The owner must approve exact tool, commands and known side effects first.

Privately retain:
- Nine App `0x05A5` etc. Network field preimages/current bytes;
- 81 App FTP menu permissions, including `0x04BD7528` parent `0x226` and invariant `0x04C16BD0` parent `0x262`;
- context of action `0x0816/0x0817/0x0818` at `0x03F17CD8..0x03F17CEF`, only as a separate playback diagnosis;
- if a **target-verified read path** exists, decoded current WBI2 field states corresponding to the upstream 69 menu permissions, counters/derived states and nine runtime availability fields;
- target build/profile identity, exact known/unknown state and any journal `NEEDS_REVIEW` lockout.

Do not publish firmware binaries, dumps, credential fields, MAC addresses, images or serials.

### D2 — decision matrix and next action

| Observation | Interpretation | Next step |
|---|---|---|
| App Network flags patched but many of 81 App menu fields STOCK | Old/incomplete installation is plausible | Prove installed artifact provenance and write journal; prepare separate **reviewed** plan only if the write safety gate passes |
| App Network/menu fields patched, WBI menu/runtime fields STOCK | WBI mismatch is a stronger candidate | Offline trace WBI load/boot and prove dependency; **no speculative WBI patch** |
| Both App and WBI target states patched but Network FTP absent | Other runtime predicate or incorrect menu path | Trace parent registration/visibility and FTP model initialization |
| App fields UNKNOWN/MISMATCH or journal unresolved | Build mismatch or interrupted transaction | Stop; reconcile identity and journal; no new writes |
| Network FTP present, only Playback action missing | Separate action `0x0817` issue | Trace resolver/binding and mode predicates; no automatic Gallery patch |
| Network FTP present and works, file transfer stalls | FTP backend/queue issue | Characterize with isolated server and safe tests before firmware edits |

**Stop conditions:** any unknown field, unsupported source hash, misidentified WBI view, contradictory current state, uncertain service access, unresolved transaction, inadequate original-state preservation, or missing recovery envelope. The working English configuration must be preserved.

## Required Codex handoff changes (R0 only)

1. Add a pure parser/test that validates upstream's **90 App / 152 WBI** fields, 89/151 *changed bytes*, the 69 paired menu IDs and 12 App-only additional records, and nine WBI runtime-availability entries. Input is a pinned local upstream checkout; do not bundle its firmware/images or execute its native writer.
2. Report old `v1.0.0` (9 Network + 1 Playback) versus current `main` (9 Network + 81 App menu + 1 Playback). Distinguish the release ZIP's actual identity from the tag; if unknown, say so.
3. Revise draft PR #3's plan to mark Network FTP on this body as **currently reported missing**, while retaining the earlier contradictory report and provenance.
4. Preserve current 7-span journaling and English unlock. Reconcile PR #2 only after reviewing its older writer assumptions.
5. Open a reviewable R0 code/doc PR; do not implement or test an R4 device patch automatically. A new WBI write strategy requires its own proven preimage, distinct storage mapping and independent approval.

## References

- Upstream App/WBI catalog (pin `d5bb948`): https://github.com/xyzhangxin/sony-a6700-powerful/blob/d5bb9485dfe7cc4bf13a4ead3a7437c2f40240a9/%E5%BA%94%E7%94%A8/src/a6700_unlock/data/a6700-2.00.json
- Upstream rendered manifest: https://github.com/xyzhangxin/sony-a6700-powerful/blob/d5bb9485dfe7cc4bf13a4ead3a7437c2f40240a9/%E5%BA%94%E7%94%A8/docs/FEATURES.md
- Upstream camera menu instructions: https://github.com/xyzhangxin/sony-a6700-powerful/blob/d5bb9485dfe7cc4bf13a4ead3a7437c2f40240a9/Powerful6700%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.md
- Owner current target definitions: https://github.com/mingwucn/Sony_research_6700/blob/55054b91319393c598246c2e8302f84c0f74eab0/apps/a6700_customizer/targets.py
- Owner regression and source-only review: https://github.com/mingwucn/Sony_research_6700/issues/1
- Previous full FTP plan: https://github.com/mingwucn/Sony_research_6700/pull/3
