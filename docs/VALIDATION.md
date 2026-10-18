# Validation, failure injection and release criteria

All numerical trial counts below are proposed acceptance targets, not results already obtained. The only initialization test result is 15 passing host-side synthetic tests for tools/offline_inventory.py. No camera, network-server, USB, firmware-patch or remote-CI test was run during initialization.

## 1. Evidence hierarchy

| Label | Meaning | Does not establish |
|---|---|---|
| source-report | An upstream author or Sony documents a result/capability | Reproduction on this body/build |
| static-inference | A claim supported by firmware data/control-flow analysis | Actual runtime behaviour |
| offline-tested | A host test, mock, parser, fit or emulator passed | Camera boot or peripheral correctness |
| device-readback | Actual bytes/settings were read and matched expectations | Loaded instruction state or image quality |
| runtime-observed | A specific live state/trace was observed | Every hidden path or future state |
| physical-tested | A body produced the recorded visual/transfer/operational result | General compatibility across bodies/versions |
| independently-reproduced | A separate eligible setup reproduced the stated procedure | Universal support |

Attach the narrowest applicable label to every claim. Store the observation, not only a conclusion. A test that was not run is NOT RUN, not PASS. An unsupported combination is explicitly UNSUPPORTED or BLOCKED. A flaky result remains a failure to qualify stability even if later attempts pass.

## 2. Offline safety and candidate tests

| ID | Test | Expected result |
|---|---|---|
| OFF-01 | Same inputs and pinned tool revision twice | Identical candidate bytes/manifests except separately recorded run metadata |
| OFF-02 | One source byte changed | Refuse before candidate eligibility/device activity |
| OFF-03 | Wrong model/version/region or unknown profile | Refuse with exact missing/mismatching precondition |
| OFF-04 | Partial/truncated source or mismatched component pair | Refuse; do not mix AP/CP from different baselines |
| OFF-05 | Negative/out-of-bounds/overlapping edit | Refuse before any write |
| OFF-06 | Reapply a candidate | Explicit already-applied classification or refusal, never a second implicit migration |
| OFF-07 | Forward then inverse on synthetic/eligible local copies | Exact original bytes and protected-state equality |
| OFF-08 | Invalid/special enum and all original look values | Preserved bounds/fallback behaviour; no table overrun |
| OFF-09 | Unselected recipe/resource records | Byte/semantic equality except independently justified dynamic fields |
| OFF-10 | Branch into replaced instruction region | All legal incoming targets remain valid; ABI and stack preserved |
| OFF-11 | Missing resources, bad checksum, invalid UTF encoding | Clean refusal/fallback specified before hardware |
| OFF-12 | Partial native result, timeout, disconnect, duplicate session | needs_review or bounded read-only handling; never blind write retry |
| OFF-13 | Interrupted multi-object transaction in mocks | Every boundary has a classified state and safe next analysis action |
| OFF-14 | Private-file/credential material in proposed commit | Block publication and sanitize; do not merely add an ignore rule afterward |

No actual power-cut during camera writes is required or authorized. Fault injection is initially host-only. Emulator stubs must be documented, especially for external routines, DMA, caches and timing. A stubbed consumer cannot prove real preview or upload semantics.

## 3. Shared hardware baseline and post-change checks

Before and after each feature, record exact body/build/source identities, power conditions, card/lens/settings, USB mode, and all planned side effects. Require full changed-object readback and a protected-settings comparison. Check startup, normal still capture, playback, AF, stabilization where used, normal USB transfer, normal Wi-Fi pairing/PC Remote, and the owner's important movie settings. Record pre-existing faults separately.

Run one approved normal shutdown/restart and one approved complete power-removal cycle after confirmed I/O completion. Expand to at least five normal restart cycles and three complete-power cycles for a release candidate, without inducing interruptions during writes. Define a timed startup baseline rather than accepting an impression of speed.

Any thermal warning, recurring crash, file corruption, unexplained settings difference or ambiguous write outcome stops the hardware campaign. Retain the current evidence and reconcile it before further mutation. Do not erase a failure by replacing its output files with a later successful run.

## 4. FL2/FL3 matrix

| ID | Trial | Initial qualification target |
|---|---|---|
| CLT-01 | Select ST, FL, FL2, FL3; capture and play back new files | Distinct expected routing, readable outputs, correct selected/playback identities |
| CLT-02 | Repeated static-scene ST captures | Establish baseline pixel/colour variability before setting difference thresholds |
| CLT-03 | Unpressed-shutter preview switching | 100 switches across native/new looks with a recorded sequence and no stale prior look |
| CLT-04 | Half-press, playback return, sleep/wake, mode-dial transition | No hidden refresh dependency or invalid selection state |
| CLT-05 | All ten native looks and six owner recipes | Basic capture/playback and preservation checks; no unowned-slot title changes |
| CLT-06 | Adjustment changes and per-look reset | Correct default markers and scoped reset, including persistence |
| CLT-07 | RAW+JPEG capture | RAW readability and JPEG/metadata behaviour separately checked |
| CLT-08 | HEIF, HLG, colour-space, high-ISO and exposure variants | Separate results; unsupported combinations remain declared |
| CLT-09 | Native movie, PP/log and still-to-movie transitions | Original behaviour preserved; new-look movie behaviour explicitly bounded |
| CLT-10 | Continuous shooting and selected long-exposure cases | No invalid buffer/file behaviour or unintended slowdown |
| CLT-11 | Return to prior known-good/stock using exact inverse | Complete storage/settings verification plus new capture/playback |

Use fixed WB/exposure/light for effect comparisons. Check neutral patches, skin, saturated colours, gradients and clipping. Establish tolerances against measured repeatability and held-out scenes; do not choose a colour-error threshold after seeing the candidate. Do not claim donor colour equivalence without a suitable physical or calibrated reference.

For custom looks, repeat the matrix for one slot, a partial subset and all intended slots. Verify unimported dynamic names and recipes, selected-slot ownership, ST-base constraints if actually required by the target design, bad-table handling, English resources and live-preview timing. Report fitting residuals separately from camera photographs.

## 5. English-language matrix

| ID | Trial | Acceptance |
|---|---|---|
| ENT-01 | Full native language selector and English selection | English available/selected as intended; original language still recoverable |
| ENT-02 | Main menus and non-destructive warning/modal dialogs | No blank labels, missing glyphs, truncated critical instructions or invalid resources |
| ENT-03 | Shooting/playback/network/date/version screens | Critical operation remains understandable and functional |
| ENT-04 | Normal/complete restart and sleep/wake | Selected language persists without unrelated initialization |
| ENT-05 | Protected region/configuration comparison | No unexplained change beyond the scoped language permission/selection |
| ENT-06 | Controlled reversal | Original language restored; newer unrelated settings preserved |
| ENT-07 | English plus FL23/custom names/FTP dialogs | Shared resource IDs and layouts remain valid |

Factory reset is not required in the initial hardware phase. If later approved, it has a distinct backup/restore plan and acceptance criteria; report the language defaults observed afterward. Do not claim persistence through official firmware updates unless that exact transition is separately tested.

## 6. FTP matrix

Use an isolated owner-controlled server and synthetic files before real images. Check both protocol completion and end-to-end bytes. Packet captures are private, especially in plaintext tests.

| ID | Trial | Acceptance |
|---|---|---|
| FTT-01 | Single JPEG manual native upload | Camera-resident origin proved; server-side length and SHA-256 match |
| FTT-02 | RAW/JPEG pair and supported large files | Both objects complete and their capture relationship is preserved |
| FTT-03 | 100-file synthetic queue and then a bounded real capture set | No silent loss, corruption or uncontrolled duplicates |
| FTT-04 | Wi-Fi loss during/between transfers | Bounded retry and state reconciliation; original remains intact |
| FTT-05 | Control-channel loss after data upload | Resolve remote completion before duplicate transmission/finalization |
| FTT-06 | Bad credentials, permissions, quota/server full | Correct classified error; no credential leak or infinite retry |
| FTT-07 | TLS certificate/hostname failure where FTPS is supported | Refusal; no automatic plaintext downgrade |
| FTT-08 | File collision, filename wrap, card change, non-ASCII names | Correct identity/path handling and no unintended overwrite |
| FTT-09 | Sleep/wake/restart with queued files | Durable queue state and defined resume behaviour |
| FTT-10 | Physical-shutter automatic capture and bursts | Transfer trigger proved; shooting impact measured against baseline |
| FTT-11 | Cancel/shutdown/card removal | Defined safe stop; no corruption or destructive cleanup |
| FTT-12 | Capture+network load | UI, startup, battery and thermal impact recorded; owner-approved limits met |

A bridge runs a separate copy of applicable tests labelled HOST-ASSISTED. Its FTT-01-equivalent does not prove native camera-origin networking. USB success does not imply wireless success. Remote-triggered capture does not imply physical-shutter event support. A size-only check is not recorded as a hash-equality test.

## 7. Composition and uninstall

Define a feature bitset/state matrix and test stock, English only, FL23 only, FTP only, pairwise combinations and the complete supported combination when all are independently ready. Test custom-LUT support as an additional variant, not a replacement for native-look regression. Composition must use reviewed source identities, not apply three stock-only patches sequentially against mismatching modified sources.

For disjoint binary windows, offline merging may be straightforward, but resource/settings/load-state dependencies still need analysis. For overlapping changes, produce a reviewed combined candidate and exact inverse rather than letting patch order decide semantics. Removing one feature must preserve newer user settings and the others. In particular, removing English resources while English remains selected requires a defined migration.

Official firmware updates create a new target. Document a supported return-to-stock procedure before any update only when it is actually established. Never tell the owner that an update will preserve custom patches or that downgraded firmware is necessarily installable.

## 8. Result record format

Every test record includes ID, date, operator/body alias, firmware and component hashes, candidate/manifest identity, settings, environment, exact command/actions, expected result, observed result, PASS/FAIL/BLOCKED/NOT RUN, evidence class, private artifact locations, sanitized artifact hashes and next action. Screenshots of a result dialog do not replace raw logs or actual output files.

Use templates/SESSION_REPORT.md for summaries and private/session-state.json for detailed device state. Keep the evidence ledger append-only. A changed conclusion cites the new evidence and leaves the earlier observation intact.

## 9. Release gate

A release requires an exact supported-build allowlist, code/source review, reproducible private candidate generation, machine-enforced source guards, clear feature/mode limits, inverse/restoration instructions within the validated recovery envelope, test reports and a rights/privacy review. Proprietary firmware/backups/calibration and user DCP-derived payloads are not included automatically.

One-body success is described as one-body success. A generally usable installer additionally needs independent same-build reproduction, clean-host setup tests, source-mismatch tests and a documented support/failure process. Until then label artifacts experimental research, not a stable or Sony-signed update.
