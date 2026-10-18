# RA-003: official version 2.00 provenance and rights

Reviewed **2026-10-18**, host-side only. Evidence is **source-report** for
Sony's public pages and the owner's answers, and **static-inference** for
bounded source-text review. No firmware bytes were acquired and no firmware
extractor or downloaded source was executed. Two owner-approved source RPMs
were read as data. No camera was contacted. RA-003 remains incomplete.

## Version label and acquisition result

The owner reports **a6700, version 2.00**, with **简体中文** as the current
language. The complete language list, English availability and regional SKU
remain unknown. These labels are not independently verified binary identity.

The [Sony UK version 2.00 page](https://www.sony.co.uk/electronics/support/e-mount-body-ilce-6000-series/ilce-6700l/software/00298439)
lists **BODYDATA.DAT**, **1,024,017,848 bytes**, released **2025-06-10**.
The [Sony Japan model page](https://support.d-imaging.sony.co.jp/www/cscs/firm/?area=jp&lang=jp&mdl=ILCE-6700&ref=update)
also offered ILCE-6700 version 2.00 and an asset link. Japan-page provenance
does not establish the owner's region or the package's applicability to this body.

One host GET of that firmware asset stopped at an unreviewed redirect before
receiving firmware bytes. The attempt returned exit **1**, received **zero
bytes**, and created no firmware file. Its state is **needs_review**; there was
no automatic retry. There is no firmware size/hash observation or format
diagnosis. The empty-stream digest in the private failure journal is not a
firmware identity and must not be used as one.

Direct scripted UK/USA HTML requests returned HTTP 403; one USA web open and a
later UK web open timed out. A separate earlier UK web read succeeded. Browser
navigation/focus attempts also timed out before usable page state. These are
retrieval limitations, not evidence about the camera. Raw responses, failures
and acquisition records remain private.

## Firmware inspection permission

The Japan model page's linked download agreement was displayed as text; its
agreement control was not activated. Articles 2/3 describe use in the owned
product, a restoration-backup exception and restrictions on modification and
reverse engineering/source analysis. This review does not establish permission
for the proposed firmware inspection/extraction or redistribution. The displayed
terms are not an independently verified statement of every applicable right.

The owner answered **No / unknown** when asked whether they already have terms
or explicit permission covering offline inspection/extraction. Record that as
**permission not established**, not as a legal determination. No permission
document or firmware was supplied. Firmware acquisition/analysis remains
blocked on a suitable rights basis and reviewed provenance; an asset URL is not
a way around its download agreement. No firmware agreement control was activated.

## Separate open-source offers

Sony's [ILCE-6700 Ver.2.00 source page](https://oss.sony.net/Products/Linux/DI/ILCE-6700_Ver200.html)
contains **34 package links**. The locally saved HTML was parsed without
following those artifact links. Two entries are:

- `sony-target-dev-busybox-1.26.2-14000003.src.rpm`
- `sony-target-dev-busybox-1.34.1-14000103.src.rpm`

The [source-download notice](https://oss.sony.net/Products/Linux/notice.html)
states that downloading entails acceptance of its risk/liability and accompanying
component-licence terms. The owner explicitly answered **Approve the two source
downloads under that notice**. Each archive was downloaded once, HTTP 200,
without redirects, within a 30 MiB limit. Original bytes and acquisition records
remain private. This consent covers only the two source archives, with no
proprietary firmware or camera permission.

No independent Sony digest or RPM signature was verified. The hashes below
identify the retrieved source archives; they are not authenticated firmware or
source-to-running-binary correspondence evidence.

| Source RPM | Observed bytes | Whole-file SHA-256 |
|---|---:|---|
| BusyBox 1.26.2-14000003 | 2,145,431 | `d71511020e02c363f0f280ae176004ddcc54275515bbbb2e780aa4381365fba9` |
| BusyBox 1.34.1-14000103 | 2,498,983 | `25eb74466448f5bec6db9b3c7b8740ac9823a60d2a9510daab2e407536bd426c` |

The source `LICENSE` prefaces identify the combined BusyBox distribution as
GPL version 2 only; the reviewed `ftpgetput.c` headers say GPLv2 or later, and
both RPM specs declare
GPL2. These are component declarations; retain their notices and review the
specific material/obligations before future integration or redistribution. No
source, patch, build output or licence text was copied into the tracked project,
and no project-wide licence was selected by this audit.

Both RPMs and their nested source tarballs were listed before selected regular
members were read, with name, count, size and output limits. Archive-selected
filesystem paths were not extracted; selected data used fixed private aliases.
Existing Windows bsdtar/libarchive 3.8.9 and Python standard-library readers were
used; there was no build, import, installation or source execution.

## FTP source lead and its limits

Both supplied `dotconfig` files set **CONFIG_FTPGET=y** and
**CONFIG_FTPPUT=y**. Both disable FTPD and WGET. Their specs list `ftpget` and
`ftpput` under symbolic target-development bin paths. Private evidence retains
the exact config/spec/source text, member lineage and hashes.

| Evidence in shipped text | 1.26.2 | 1.34.1 |
|---|---|---|
| FTPGET / FTPPUT in dotconfig | Lines 772/773: enabled | Lines 863/864: enabled |
| FTPD / WGET in dotconfig | Lines 768/873: disabled | Lines 859/978: disabled |
| Spec lists ftpget / ftpput | Lines 248/249 | Lines 252/253 |
| Spec invokes external setup, then oldconfig | Lines 75/76 | Lines 69/70 |

The specs copy their supplied config and invoke external Sony setup macros and
`make oldconfig`. Final configuration, toolchain and source-to-binary identity
therefore remain unproved. Macro-based development paths are not observed
camera filesystem paths. The two package variants are not mapped to AP/CP,
processor, regional SKU or a running body component.

The reviewed FTP client contains a direct socket USER/PASS/STOR flow.
Version 1.34.1's separate TLS/SSL_CLIENT configuration flags do not establish
TLS in that FTP flow. No FTPS capability, certificate validation, camera UI,
capture-completion hook or automatic transfer follows. Nothing was connected to
a server or camera during this source audit.

The reviewed clients also lack the prepared host protocol's durable queue,
hash reconciliation and rename finalization; verbose command logging can expose
the password argument. These are observed source integration limits, not camera
behavior or a deployment proposal. All supplied patch headers were reviewed;
none directly names the dotconfig or FTP client source. External macro effects,
patch application and the final build remain untested.

This offer is separate from the proprietary firmware package. A component
licence would cover its specified material, not automatically the full firmware.
The model/version heading and source configuration do not prove which code runs
on this body, compiled applet availability, architecture/ABI, English resources
or a usable camera-resident FTP route. A host-side FTP client is host-assisted
preparation; a complete optional bridge also needs a proved camera-to-host leg.

## Recovery evidence

The model-specific update instructions displayed through the Japan page say an
already-2.00 body does not need the update, and warn that interrupted power can
leave the camera inoperable. Their limited card/file-copy troubleshooting is not
a general recovery system. The inspected pages did not establish downgrade,
same-version reinstall or recovery after failed normal boot/service access.
This bounded negative result does not establish that those routes are impossible.

The owner's **verified rollback/recovery before firmware writes** requirement
therefore remains unmet. A downloaded official package would not be a per-body
backup, exact inverse or proven restore route. No deliberate failure, write,
restore or automatic rollback is authorized by this review. The existing
[write gate](../docs/ACCESS_AND_RECOVERY.md#8-write-gate-checklist) remains in force.

## Extractor and host-test boundaries

The pinned PMCA DAT locator remains a small legacy UFU/FDAT span locator; its
missing bounds, authentication and target checks are described in
[artifact intake](../docs/ARTIFACT_INTAKE.md). Its MIT licence does not grant
rights in Sony firmware. No implementation was copied or run.

During delegated static review, Git object reads in the public PMCA partial clone
implicitly fetched missing public blobs. The intended no-network subtask boundary
was therefore not maintained. No private input was uploaded and no upstream code
was executed. Further offline object reads must disable lazy fetching or use
already present ordinary text. The source lock was not changed.

`python -B -X utf8 -m unittest tests.test_artifact_probe -v` passed **8/8**
synthetic tests, exit **0**, CPython **3.13.12**. This covers only the authored
bounded probe. It does not test an unseen firmware format, source RPM, camera,
native feature or recovery operation. The earlier full-suite qualification is
unchanged; it was not rerun for this documentation-only update.

Next single package: **RA-003, rights-cleared exact-2.00 binary intake and
source/binary correspondence**. This needs suitable firmware inspection rights
and legitimate applicable input bytes; it is blocked until those exist.
No further source download, speculative parser or build is required now.
See the [session commands/results](sessions/20261018-RA-003-package.md).
