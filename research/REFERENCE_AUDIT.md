# RA-002 reference code and reuse-rights audit

Audit date: 2026-10-18. Scope: R0 host-side Git retrieval, static source review,
source identity/provenance checks and this repository's synthetic tests. No
upstream Python module, launcher, test, installer, service tool, native worker,
build or release script was executed or imported. Camera commands: **none**.

This audit distinguishes useful methods from device-specific implementations.
It establishes no alpha6700 access route, feature support, ABI, offset, recovery
mechanism or device-write eligibility. No third-party code/data was copied into
tracked project files, and no project-wide licence was selected.

## 1. Revision and acquisition evidence

| ID | Pinned source | Local verification and scope |
|---|---|---|
| R1 | [QAQLeonard/a7c2-fl23-research](https://github.com/QAQLeonard/a7c2-fl23-research/tree/c0930d5b0ccd49c0a092dc883054cd6dce199649), `c0930d5b0ccd49c0a092dc883054cd6dce199649` | Clean detached checkout; all 119 tracked file blobs match the commit; 57 Python files parsed as text/AST only |
| R2 | [lzh2016zzz/a7cr-fl23-research](https://github.com/lzh2016zzz/a7cr-fl23-research/tree/43ba74441c8f10459ade41e84a379ad8005e6ef4), `43ba74441c8f10459ade41e84a379ad8005e6ef4` | Clean detached checkout; its complete one-file tree is README.md; blob matches |
| R3 | [ma1co/Sony-PMCA-RE](https://github.com/ma1co/Sony-PMCA-RE/tree/a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0), `a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0` | Exact commit fetched as Git objects for candidate-dependency provenance; no working-tree checkout or tool execution |

R1/R2 pins are unchanged from initialization. R1's clone initially resolved the
remote default HEAD to `c423bf277636bec660bf4c7f2908c1b8b84fcbe7`. A separate
`git diff --stat` review recorded 31 changed paths, 1126 insertions and 550
deletions, including custom-look entry/worker and documentation changes. That
newer revision was not checked out, fully audited or adopted. R2's clone default
HEAD already matched its pin. No mutable release attachment was acquired.

R3 became a candidate source reference because R1 imports vendored PMCA and
[its notices identify this full revision](https://github.com/QAQLeonard/a7c2-fl23-research/blob/c0930d5b0ccd49c0a092dc883054cd6dce199649/docs/en/notices.md#L9).
Git-tree comparison established **19/19 vendored files identical**, zero modified
or vendor-only files; 32 other upstream PMCA files are not in that subset and
were not audited. Its README blob is the previously locked
`1c47cad4ceffcc0dfd574c83badbb1026419d6ee`. Original LICENSE.txt blob
`77b0378407be242b5537f8dca3ed6402c91ba676` has identical text to R1's copied MIT
licence. This pins audit provenance; it does not adopt PMCA as an alpha6700
runtime dependency or validate its wider codebase.

Verification above is **offline-tested**. Upstream statements below are
**source-report**; conclusions drawn from source are **static-inference**.

## 2. Entry points, imports and host preparation

All paths/line numbers in sections 2–5 refer to locked R1.

| Path and evidence | Observed source behaviour | Reuse decision |
|---|---|---|
| `FL23.cmd:2`, `Custom-LUT.cmd:2`, `dev/windows/bootstrap.cmd:15–24`, `src/launcher.py:25–48,67–76` | Launcher chain may create a virtual environment, probe imports and run network-capable `pip install --requirement` before opening tools. Workflow help normally passes through preparation too. | Inspect text only; not an inspection command or approved setup workflow here. |
| `src/fl23/Start.ps1:2`, `Start.cmd:2`; `gui.py:39–64,76–79` | FL23 GUI dispatches app.py operations in subprocesses. GUI busy/close guards cover that process, not a cross-process camera lock. | Requires a separately designed single-owner adapter. |
| `src/fl23/core.py:1–22,42–50`; `transport.py:5–12` | Core has no direct USB import, but adds its vendor directory to Python's path and lazily imports the Backup parser. Transport imports PyUSB/libusb and vendored PMCA. | Re-derive a clean offline core; do not assume all imports are inert. |
| `src/fl23/requirements.txt:1–4` | Direct pins: PyUSB 1.3.1, libusb-package 1.0.30.0, pycryptodomex 3.24.1, PyYAML 6.0.3. | Crypto and YAML are declared. Wheel/sdist hashes and a full transitive/platform lock are absent. |
| `src/looks/requirements.txt:1–2`; `requirements-research.txt:1–4`; `looktool/references.py:11–12`, `hooks.py:6–22` | NumPy/SciPy use version ranges; research adds pinned Keystone and ranged Unicorn/Capstone. Keystone assembles ARM64 AP and Thumb CP instructions in the host when invoked. | No installation/build occurred; exact package/artifact/native-library rights remain unreviewed. |
| `src/fl23/vendor/pmca/usb/driver/windows/{setupapi,wpd,msc}.py` | Optional Windows branches use comtypes/win32file outside the reviewed generic transport route. `wpd.py:12–25` changes comtypes import machinery and generates wrappers on import. | Optional branches are not covered by generic-route dependency assumptions. |

Package versions are source declarations, not evidence that those packages work
on this host. No package distributions were downloaded or installed. The three syntax
warnings from text/AST parsing (`dev/usb/tests/test_launcher.py:23,30,32`, invalid
escape sequences) were recorded; parsing is not upstream test execution.

## 3. Transport, workers and actual side effects

| Source path and line evidence | Static finding | Project consequence |
|---|---|---|
| `src/fl23/transport.py:25–31,124–144`; `vendor/pmca/usb/__init__.py:23–29,48–50`; `vendor/pmca/usb/driver/generic/libusb.py:67–72` | Initial identity sends SCSI/Sony requests; device construction invokes backend reset, whose initial generic route attempts kernel-driver detachment. Exact Sony identities/model are fixed. | More than passive descriptor enumeration; not an approved alpha6700 R1 command. No USB constants copied. |
| `transport.py:77–122` | Bounded readiness polling retries explicit sense/busy responses; transfer timeout/disconnect propagates. | Useful method only; establish target semantics before any retry policy. |
| `transport.py:148–178`; `vendor/pmca/usb/sony.py:900–936` | Starts/authenticates Senser access, waits for a different service identity and authenticates again. Dependency start/stop suppress some USB exceptions. | R2 service transition; no target route established by this source. |
| `src/fl23/app.py:29–65,105–107`; `native/probe.c:1–4` | Preparation uploads staged modules/requests, then writes the special native-loader filename to execute diagnostics. It runs probe, installer mode 0 and WBI mode 0. | “Backup/Check” is R2 native execution and temporary camera writes, even without program installation. |
| `transport.py:188–207`; `app.py:41,85,117` | Temp filenames/packet types/upload lengths are constrained, but the path selector accepts traversal under its initial prefix; app intentionally traverses to preload/program files. | Narrow interface is not a filesystem sandbox. |
| `transport.py:179–194`; `app.py:38–65,226–234` | Called-method exceptions mark the session unhealthy; CLI errors record needs_review. Some response-format/status errors occur after that exception guard, leaving healthy true, and finally-cleanup may still issue commands. Native-result validation can also fail before cleanup. | Preserve evidence/refuse stale temp state as methods; independently design ambiguous-response reconciliation and cleanup. |
| `app.py:123–158`; `transport.py:208–216` | Fresh reads constrain particular CP units/AP bindings; native writes and separate subsystem saves are followed by RAM/stored comparisons. | R3 persistent settings; identifiers/layouts are reference-model-specific. No settings API adopted. |
| `app.py:159–178,196–208` | Install orders program writes/readback, setting saves and WBI mutation; restore orders settings before program inverse. Battery percentage is an owner-entered integer. | Not observed power telemetry, atomicity, universal restore or alpha6700 write sequencing. |
| `native/installer.c:7–23,33,62–85,112–152` | AArch64 Linux syscall/stat ABI, fixed AP/CP paths, mount/device assumptions, whole-file/window checks, remount, fixed-window writes, fsync/readback and read-only restoration. | R4 implementation tied to exact source/ABI/storage; no transplant or model-guard change. |
| `native/installer.c:43–50,96–110,134–139` | Handles partial writes/EINTR and automatically attempts reverse patching after a patch/hash failure. | Must not become this project's default handling of uncertain completion; review operation-specific reconciliation first. |
| `native/probe.c:76–120`; `runtime.c:13–37` | Finds a process mapping, reads fixed relative runtime locations and AP file-offset-derived spans; writes/fsyncs temporary reports and removes loader files. Runtime inspection does not read running CP instruction memory. | Target-specific R2 execution, not a pure read-only observation or AP/CP equivalence proof. |
| `native/wbi.c:31–75` | Mode 1 changes retained boot state through ordered sysfs writes and checks metadata/log markers. Other modes still execute native code and write a report. | Treat retained-state mutation separately; not harmless cleanup or a generic reload command. |

No automatic camera reboot call was found in the inspected execution path;
upstream instead instructs manual cold starts. That bounded negative finding
does not cover all vendored methods or future versions. No raw-flash or
process-memory write was found in the inspected installer C source; AP/CP file,
settings and retained-state mutations above remain substantial device actions.

The six asset-manifest hashes matched the fetched bytes (**offline-tested**).
Native source-to-binary correspondence, build reproducibility, disassembly,
control-flow/loader placement and actual worker behaviour remain **NOT RUN**.
Hashes and readable C source do not establish that a bundled worker is suitable
or safe on an alpha6700.

## 4. Offline planning and custom looks

`src/fl23/core.py:52–70` demonstrates whole-file source/result checks, bounded
equal-length expected-byte windows and overlap rejection. `:72–92` checks selected
mapping occupancy and preservation of existing colour records. `:94–114` permits
two specifically described changing counters during settings comparison. These
are useful guard patterns; their hashes, offsets, slot capacity, Backup IDs and
counter semantics remain A7C II 2.01 assumptions. Zero-filled space does not
prove alpha6700 ownership or capacity.

The custom-look GUI routes six offline actions to `looktool` (`src/looks/gui.py:12–18,103`).
The inspected toolkit emits private program/table candidates and manifests,
not a camera transaction; CLI output explicitly leaves display names unchanged
(`looktool/__main__.py:96–110,140–149`). `project.py:12–13,25–59` fixes ILCE-7CM2
2.01 and checks local binding inputs, not observed camera state.

`looktool/firmware.py:18–77` illustrates exact-source transitions and inverse
checking, but does not provide this project's explicit address-type/protected-region
policy or independent instruction review. `sixbuild.py:58–110`, `six.py:55–79`
and `hooks.py:12–64` use exact historical modified images and fixed AP/CP file
offsets, virtual-address translations, code placement and preview hooks. File
offsets and runtime/virtual addresses must remain separately labelled; none was
entered into an alpha6700 profile.

The six-look builder explicitly leaves resource files, fresh per-body settings,
native transaction/inverse and retained-image/physical cold-load integration
outstanding. Running CP memory is not directly read. DCP processing is a limited
look/tone approximation, with a provisional colour-coordinate model and an
explicit input-domain contract for cube fitting (`references.py:114–187`,
`native.py:111–134`, `calibration.py:75–80`, `project.py:63–82`). It does not establish
full DCP fidelity, calibrated alpha6700 colour or arbitrary LUT compatibility.

The [upstream failure record](https://github.com/QAQLeonard/a7c2-fl23-research/blob/c0930d5b0ccd49c0a092dc883054cd6dce199649/docs/en/technical/failures.md#L9)
reports restart loops despite offline checks/readback, title/slot problems and
stale preview/load state. These are **source-report**, not our reproduction or
an alpha6700 recovery route. R2 similarly remains an incomplete documentary
description with omitted patch blocks and outstanding later-stage photographic
validation (R2 README.md:11–13,69–71,178,221).

## 5. Component reuse-rights decisions

These are bounded findings from the pinned files, not a blanket grant for
everything in a repository/archive. No third-party implementation was integrated.

| Component | Evidence | Decision before reuse |
|---|---|---|
| R1 newly authored host/native source | [Root MIT licence](https://github.com/QAQLeonard/a7c2-fl23-research/blob/c0930d5b0ccd49c0a092dc883054cd6dce199649/LICENSE), identical src/fl23/LICENSE and src/looks/LICENSE; lines 12–13 require notices and 23–24 exclude inherited/Sony material | Method/reference now. Any later copied substantial portion must preserve its notices and receive component/provenance review; this project's licence remains undecided. |
| R1 licence notice routing | All three licences refer to absent NOTICE.md; actual English/Chinese notices are under docs/ | Record packaging inconsistency; carry the actual applicable notices if integration is later approved. |
| R3 PMCA subset | [Original LICENSE.txt](https://github.com/ma1co/Sony-PMCA-RE/blob/a82f5baaa8e9c3d9f28f94699e860fb2e48cc8e0/LICENSE.txt), MIT with ma1co copyright; exact matching vendored text and 19 source blobs | Candidate provenance pinned only. Preserve upstream notices if adopted; no target service adapter approved. |
| Secondary vendor origins | pmca/usb/crypto.py:1 cites ajalt/python-sha1; driver/osx.py:144 cites pyserial similarity; driver/windows/msc.py:81 cites calibre similarity | Pin and review relevant original contributions/terms before copying those components. Matching PMCA blobs does not settle every embedded origin. |
| Sony-derived patch/colour/curve bytes and native payload assets | assets/patches.json and colors.json contain firmware-derived values; [notices.md:22](https://github.com/QAQLeonard/a7c2-fl23-research/blob/c0930d5b0ccd49c0a092dc883054cd6dce199649/docs/en/notices.md#L22) retains Sony ownership; licence exclusions apply | No grant established by source MIT. Keep external; no payload/table copying into this project. Source/binary provenance must also be reviewed separately. |
| Fuji/MTriton profile releases | notices.md:16–18; docs/profiles/CC-BY-NC-SA-4.0.txt records attribution, noncommercial and share-alike conditions and expressly is not legal code | Not downloaded/adopted; code MIT does not cover profiles. Review exact original terms and provenance before any use/distribution. |
| Ricoh-adapted DCP releases | notices.md:19 and docs/profiles/manifest.json:120–188 say no separate redistribution licence supplied | No redistribution permission established. Manifest includes a 2023 copyright entry where the prose generalizes 2022; preserve per-file facts. |
| R2 notes/tables | Complete pinned tree is README only, no explicit licence/grant; README.md:225–236 acknowledges independently licensed sources | Authored methodological summaries with attribution only; no nontrivial prose/table/code/data copying. Disclaimer/acknowledgement is not a reuse grant. |
| YuuLuo service-preload reference | R1 notices.md:11 cites commit 1619f938663a36d41e72302a8cfee89a0f6acd1a and CC BY-SA 4.0 documentation | R1 source-report only; original terms/code not independently audited or adopted here. |
| Python/native package distributions | Declared requirements and import graph only; exact distributions were not acquired | Package and bundled-native-library licences/transitive locks remain prerequisites before installation/integration. |

`dev/release/build_release.py:11–19` can bundle source, documentation and binary
assets; `build_profiles.py:21–29` packages profiles separately. Publication filters,
owner supply and SHA-256 manifests do not clear rights for each included component.
No release bundle/profile archive was built, downloaded or redistributed here.

## 6. Findings, blockers and next work package

RA-002's audit acceptance is met within the stated static scope: sources are
pinned, main entry/transport/native paths and dependencies are identified, and
reviewers can distinguish reusable host methods from incompatible device helpers.
This is not a complete security audit of every upstream file or a reuse approval.

Remaining prerequisites:

- Exact alpha6700 identity/installed firmware/region, access route, ABI/storage,
  preservation/recovery evidence and independent backups remain absent.
- Source/binary correspondence and exact-target worker safety remain unestablished.
- Package artifact/transitive/platform locking, secondary provenance and
  component-specific rights need review before any third-party integration.
- R2 notes, Sony-derived payloads and Ricoh profiles have no reuse/distribution
  grant established by this audit. Other profile terms remain separate.
- R1 newer commits/releases are not reviewed or adopted; pinned findings do not
  describe the mutable default branch.
- Local Windows inventory tests remain unreliable: this session's single run
  had 12 passes, two errors at the existing unchanged-file check and one symlink
  skip (15 total, exit 1). RA-001's ctime diagnosis remains a known limitation;
  no code/test threshold was changed or repeat-until-pass run made.

No native English, FL2/FL3/custom look, native FTP or host-assisted bridge was
implemented/tested. No target support values or device-write gates changed.

Next single work package: **RA-003 — Build the official-package and local-artifact
inventory (R0)**. Start by reconciling the missing installed-firmware fact and
legitimate matching-package provenance; do not substitute the latest version or
update the body. Until that input exists, target-specific package acquisition is
blocked. RA-003 was not executed during this audit.
