# Creative Looks: alpha6700 implementation design

Scope: FL2/FL3 first; calibrated custom still-photo looks second. No target addresses or camera patch are supplied by this plan. Refer to REFERENCE_ANALYSIS.md for R1/R2 and Sony source S1. Work packages CL-101 through CL-107 are defined in BACKLOG.md.

## 1. Establish the unmodified baseline

On the exact body/build, record the native look list, six custom recipes, eight adjustment controls, reset/default markers, still/movie separation and situations in which Creative Look is disabled. Sony's alpha6700 guide lists ST, PT, NT, VV, VV2, FL, IN, SH, BW and SE and six custom recipe slots; it also documents restrictions with Picture Profile/Log settings [S1]. Verify the actual body rather than assuming every menu observation matches a current web guide.

Preserve all owner recipes before research. Capture a small repeatability dataset with fixed exposure, white balance, focus, lens, scene and lighting. Include repeated ST frames and a native different look such as FL. These establish sensor/lighting/compression variation and a positive control. Do not interpret a tiny numerical JPEG difference as evidence of a new colour pipeline.

The first feature target is a new JPEG made by the camera plus preview and playback. RAW capture integrity must be preserved, but a look applied to an embedded JPEG or metadata is not a changed RAW sensor mosaic. HEIF/HLG, colour spaces and movie output need their own tests. Native video LUT facilities, where present, are not evidence of arbitrary still-photo LUT application.

## 2. Build the target architecture map

Collect the exact AP, CP and resource objects through the approved acquisition process. Identify formats and instruction sets independently. Make a private mapping table with these fields:

```text
logical_function | object_sha256 | file_offset | span_length | linked_VA
runtime_address_if_observed | instruction_state | callers | callees
resource_or_data_anchor | semantic_evidence | confidence | unresolved_questions
```

Use null for unknown addresses. A file offset is not a virtual address. Record how translation is derived from segments/loaders, including relocations. Match functions by control/data flow, constants and multiple xrefs, not a uniform offset delta from A7C II/A7CR.

Inspect the following layers separately:

| Layer | Questions to answer on the alpha6700 | Expected artifact |
|---|---|---|
| Names/resources | Are FL2/FL3 strings and required layouts present? Which IDs/loaders own them? | Resource coverage and xref report |
| Product visibility | What product/feature rule controls list inclusion? | Exact field semantics and consumers |
| Selection capability | What separately permits selection under current mode? | Capability/guard map |
| Slot model | How many ordinary/reserved/custom slots exist? Which are actually used? | Slot ownership and bounds table |
| Saved bindings | Which settings restore selected/base looks at boot? | Typed saved-state schema, not guessed adjacent IDs |
| AP conversion | How is a selected look translated into a processing request? | Input/output table including invalid/special cases |
| CP dispatch | Which paths serve stills, preview and movies? | Complete dispatch/control-flow map |
| Gamma/chroma/matrices | How are records indexed, sized, selected and interpolated? | Target record-layout specification |
| Metadata/playback | Which writers produce numeric modes, names and playback identifiers? | Tag/writer map with raw values |
| Defaults/reset | Where are factory defaults and current values stored? | Reset-path and persistence model |
| Boot loading | What makes changed storage become active? | Target-specific load/retained-state evidence |

A layer can be present while the next is absent. Record that explicitly rather than changing several flags until a menu appears.

## 3. Reference identifiers: comparison only

R2 reports the following distinct identities for its A7CR 2.01 implementation. These are search/comparison anchors, not alpha6700 assignments:

| Meaning | A7CR FL2 / FL3 reference | alpha6700 target |
|---|---|---|
| Ordinary parameter slots | 16 / 17 | UNKNOWN |
| AP stored look values | 10 / 11 | UNKNOWN |
| UI internal enum | 17 / 18 | UNKNOWN |
| CP mode / CreativeStyle field | 19 / 20 | UNKNOWN |
| Still colour parameter | 55 / 56 | UNKNOWN |
| Gamma row | 48 / 49 | UNKNOWN |
| MakerNote ColorMode | 22 / 23 | UNKNOWN |

Never assume that a numerical match means the same namespace. Adjacent Backup IDs may be unrelated settings. Discover the alpha6700 mapping from readers, writers and bounded tables. If no spare slot or record capacity exists, describe the required structural expansion and its loader implications before generating a patch.

## 4. FL2/FL3 data integration

Use the reference donor ILCE-1M2 4.00 as an initial source for look-stage comparison. Confirm every record's format, channel order, scaling, illuminant variants, ISO-dependent gamma columns, checksums and target-specific fields. Preserve alpha6700 sensor white-balance calibration, black levels, lens data, defect correction and unrelated colour tables.

Separate donor look data from donor functions. Adapt the target's existing processing and parameter-selection paths rather than transplanting whole donor binaries. Compare record structure against known target native looks before mapping new entries. For each added record, prove capacity, unused status and absence of other references; zero contents alone do not establish ownership.

The offline builder must preserve every existing look's mappings and referenced records, not only the bytes outside an obvious new-table window. It should emit a report listing every changed range, every inherited donor record, format transformations and target-only fields retained. Re-run generation from the same inputs and require identical output hashes.

Factory adjustment defaults are different from the underlying look transform. Establish the donor defaults from sources and verify the target's native per-look reset path. Do not bulk-reset the owner's eight adjustment values merely to match a reference screenshot. Provision only the intended new bindings/defaults, then use a scoped reset when appropriate and approved. The pre-existing recipes must remain recoverable.

## 5. Candidate decomposition

Prepare independent logical change groups even if final compatibility requires an ordered multi-object transaction:

CL-A: menu/resources and selection capability. CL-B: slot identity and AP-to-CP conversion. CL-C: CP still processing and new look records. CL-D: saved bindings and defaults. CL-E: metadata/playback mapping. CL-F: preview and retained-state integration.

Each group has exact inputs, outputs, preservation rules and inverse. A menu-only intermediate may be unsuitable for hardware use because it exposes incomplete processing; decomposition is for analysis/review, not permission to install unsafe intermediate states. The approved device candidate must keep all reachable routes valid.

A future planner should accept a target profile plus original program/settings copies, and output candidate files, a machine-readable edit manifest, a preservation report and an inverse description. It must not open USB. Candidate eligibility is exact model/build/source-state plus region where relevant; version text alone is insufficient. A second application must either be explicitly recognized as already applied or refused. Do not infer idempotency from a button label.

## 6. Still, movie and preview boundaries

Trace new-look values through still preview, actual still capture, playback, mode switching, saved memory recalls and movie/log entry. Preserve native invalid-value handling. Do not allow an unimplemented movie enum to index a still-only table. A deliberately defined safe fallback may be acceptable during a still-only phase, but must be tested, documented and not falsely presented as FL2/FL3 movie processing.

Validate preview without a shutter press, without relying on a half-press to refresh state, and after sleep/wake or playback transitions. R1 reports cases where photos were correct while preview retained an earlier look [R1 failures]. Therefore output-file correctness does not close preview requirements.

If stale preview is observed, trace table construction, cache keys, validity state, submission and consumer acknowledgement independently. Do not refit working colour data to fix a transport/cache defect. Any hook must preserve instruction boundaries, all incoming branch targets, register/stack conventions and the lifetime of cached data. Reuse native mechanisms only after target-specific tracing. Repeated upload is not free: measure CPU/transfer work, frame rate, startup latency, battery and temperature before claiming negligible impact.

## 7. Metadata and output validation

Preserve original files and extract both raw numeric tags and decoded names. Record parser/version and tag group; an older metadata tool may not know a new enum. A tag name, an in-camera playback label and actual pixel processing are independent observations. Compare new files rather than old photos taken before modification.

Suggested local analysis after tool review is an ExifTool report with grouped/numeric values, plus image-dimension/decodability checks and controlled patch-region statistics. The existence of a CreativeStyle/ColorMode-like tag does not prove a donor match. Confirm no unrelated metadata corruption, no RAW decoding failure and no file-size/truncation fault.

For a donor-equivalence claim, use a physical donor or a justified colour-domain reference and independent validation scenes. Otherwise describe the result as a selective port of donor look data with measured alpha6700 output, not verified pixel-equivalence to an Alpha 1 II.

## 8. Custom DCP/LUT-derived looks: separate second phase

First establish one slot with a synthetic diagnostic table and a deterministic offline fit; do not immediately overwrite all six owner slots. After the routing is proved, support selected-slot import while retaining unselected native recipes, dynamic titles and reset behaviour. Six-slot capacity is a target investigation, not inherited from another body's memory layout.

A DCP is a RAW-development profile and may include camera calibration, tone, look and illuminant-dependent stages. A cube LUT has an input domain, encoding, gamut and sampling order. Neither should be applied directly to Sony ST output without an explicit bridge. Record which stages are retained or omitted and why. Preserve target sensor calibration; a filename containing a camera model is not evidence of calibrated compatibility.

Collect paired linear RAW-derived data and ST output under fixed conditions, using multiple scenes and illuminants. Separate calibration/training from holdout validation by scene or chart session, not merely adjacent pixels. Fit the target-native representation, report interpolation and quantization choices, and measure clipping, neutral-axis behaviour, hue discontinuities, saturated colours and skin patches. Establish numerical thresholds from measured baseline variability before evaluating candidates.

R1 describes a 5x9x9, three-channel signed 7-bit correction representation for its body [R1 integration]. Verify the alpha6700's own dimensions, storage, unpacking and uploader before reusing that assumption. A retained native coefficient precision does not imply full fidelity to a source DCP. Exact Fuji/Ricoh simulation claims require separate evidence.

Names require resource-loader and layout validation in all supported languages, especially the newly enabled English path. Validate byte lengths, encodings, glyph coverage, resource checksums and dynamic naming of unimported slots. Do not replace an entire regional resource package to change six titles. Preview, still output, metadata and recipe persistence must each be demonstrated.

## 9. Required outputs and go/no-go

Before hardware: target mapping dossier; source/donor inventories; record-layout specification; reproducible candidate/inverse; proof of preserved native records; invalid-enum and mode-boundary tests; resource validation; and a feature-specific device test script. Any critical UNKNOWN remains a blocker.

After hardware: full file/unit readback; scoped loaded-state observations; new stills/playback; preview switching record; per-look reset and persistence tests; existing-look/movie regression; and an approved reversal result where feasible. Report exact firmware/body count and the remaining untested format/mode combinations.

FL2/FL3 success does not authorize the custom-LUT extension automatically. Custom-look success on one slot does not authorize all-slot resource or memory changes. Each expansion returns through candidate review and the write gate.
