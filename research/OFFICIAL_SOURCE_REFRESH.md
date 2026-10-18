# Official Sony source refresh

Observed on **2026-10-18**. Evidence class: **source-report** throughout.
This is a bounded review of public Sony HTML documentation, prioritizing native
English and native Wi-Fi FTP. It is separate from the original source lock and
from any exact-body observation.

The latest firmware entry observed in the inspected Sony USA catalogue and
linked release notes is **ILCE-6700 version 2.00, released 2025-06-10**. This
public release is not the owner's installed firmware. Owner-installed firmware
and regional variant remain **unknown (`null`)**. No package was downloaded,
selected as a matching target package, hashed or executed. No source-lock or
profile entry was changed.

## Public catalogue and release-note availability

- [Sony USA ILCE-6700 downloads](https://www.sony.com/electronics/support/e-mount-body-ilce-6000-series/ilce-6700/downloads)
  opened successfully and listed system software version 2.00 dated 06/10/2025.
- [Sony USA version 2.00 release notes](https://www.sony.com/electronics/support/software/00298441)
  opened successfully and confirmed version 2.00 and release date 06-10-2025.
  The date is recorded here as 2025-06-10; the UK catalogue search result used
  10/06/2025. The applicable-model list includes ILCE-6700 and its listed kits.
- [Sony UK ILCE-6700 downloads](https://www.sony.co.uk/electronics/support/e-mount-body-ilce-6000-series/ilce-6700/downloads)
  returned an **Internal Error** on one direct-open attempt. Its public search
  result listed version 2.00 dated 10/06/2025. The successful USA pages supplied
  direct catalogue and release-note evidence without escalating retrieval.

The release notes describe smartphone/tablet transfer changes and direct image
uploads to **Creators' Cloud**. A Sony cloud-upload feature is not evidence of
arbitrary camera-to-server FTP. No FTP reference appeared in the inspected
release-note text. This review does not establish that no other regional,
historical or unpublished build exists, and it does not recommend an update.
Instructions for installing firmware on the public page were not executed.

## English and native FTP documentation

| Source | Observed claim (`source-report`) | Boundary |
|---|---|---|
| [S2: ILCE-6700 Language](https://helpguide.sony.net/ilc/2320/v1/en/contents/0601_language.html) | Sony documents a Language setting for menu items, warnings and messages. | The page does not enumerate regional language sets or identify the owner's offered languages. English may already be available through normal menus; an unlock must not be presumed necessary. |
| [S3: ILCE-6700 menu catalogue](https://helpguide.sony.net/ilc/2320/v1/en/contents/221h_list_of_menu_items_ilc2320.html) | The inspected Network list includes PC Remote, Creators' Cloud and network configuration; no FTP item or FTP text match appeared. | This is a bounded documentation finding, not proof that an FTP backend is absent, that an undocumented route exists, or that any donor implementation is compatible. |
| [S4: ILCE-6700 PC Remote](https://helpguide.sony.net/ilc/2320/v1/en/contents/0903_pc_remote_function.html) | Sony documents Wi-Fi/USB computer control, including shooting and storing images on the computer. Access authentication and WPA2/WPA3 are recommended. | This is a possible host-assisted architecture lead. It does not prove unattended physical-shutter ingestion, capture-completion signalling, a functioning bridge, or native camera-to-server FTP. No authentication setting was changed. |
| [S5: Sony Camera Remote SDK landing page](https://support.d-imaging.sony.co.jp/app/sdk/en/index.html) | ILCE-6700 appears in the supported-device list; Sony directs readers to device-specific API references for supported interfaces. | A device listing is not a per-function or per-interface guarantee. No SDK/API package was downloaded, licensed for integration or executed in this refresh. |
| [S6: ILCE-7M4 / alpha7 IV FTP page](https://helpguide.sony.net/ilc/2110/v1/en/contents/TP1000653558.html) | This different-model guide explicitly documents an FTP Transfer menu. | It supplies no alpha6700 backend, ABI, offset, settings-identifier or compatibility evidence. |

The inspected ILCE-6700 Help Guide pages yielded useful body text despite their
JavaScript-disabled notices. Their content is documentation evidence, not a
version-matched observation of the owner's camera. The optional
**HOST-ASSISTED camera-to-host-to-server bridge remains a separate result** and
cannot satisfy native FTP acceptance.

## Deferred looks

[S1: ILCE-6700 Creative Look](https://helpguide.sony.net/ilc/2320/v1/en/contents/0411B_creative_look.html)
lists ST, PT, NT, VV, VV2, FL, IN, SH, BW and SE, plus six adjustable Custom Look
presets. No FL2/FL3 entry appeared in this page. Its Custom Look terminology
refers to adjusting existing presets; it does not establish arbitrary
calibrated still-photo table support. FL2/FL3 remains deferred behind English
and native FTP. Calibrated custom still-photo looks remain later, separately
gated work.

## Scope and unresolved evidence

Only ordinary public HTML and public search metadata were inspected. No
firmware, SDK, binary, camera input or private input was downloaded or uploaded.
No upstream launcher, installer or service tool was executed. No camera or
FTP/FTPS server endpoint was contacted. **Camera commands: none.** No tests were
run for this documentation-only refresh, and no feature or device-write gate
passed.

Missing prerequisites remain the owner's observed firmware, regional/SKU and
offered-language facts; exact-build resources/backend evidence; and separately
approved device identification/access and recovery evidence. This refresh adds
no target offsets, eligible profile or implementation. Historical initial
source-access failures and the unchanged source lock remain distinct from this
new observation.
