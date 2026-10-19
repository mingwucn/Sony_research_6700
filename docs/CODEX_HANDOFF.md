# Webchat to local Codex hand-off

## 1. Read this before the first command

This is an initial research hand-off, not an alpha6700 installer. The owner's repository was empty when the project was initialized. No camera was available to webchat. No alpha6700 firmware/build, regional SKU, service route, target offset, recovery mechanism or requested feature was validated.

Current host-only tools comprise the inventory helper, bounded artifact-header
probe, synthetic-only in-memory candidate/transaction APIs and a durable local
queue with in-memory mock transport. A separate
[durable synthetic journal](DURABLE_SYNTHETIC_JOURNAL.md) records fixture claims
under cooperative OS ownership, with conservative crash/reopen reconciliation.
A separately invoked
[loopback FTPS lab](FTPS_LOOPBACK_LAB.md) tests a constrained local peer using
synthetic inputs; default tests remain socket-free. See [pre-camera coverage](../research/PRE_CAMERA_READINESS.md)
and [current state](../research/STATE.json) for actual scope. They do not extract
firmware, dump/contact the camera, generate an eligible target patch, unlock
languages, provide native FTP or a camera bridge, or restore anything. Later CLI names in design discussions
remain proposals unless actual code and tests are added.

Read AGENTS.md, README.md, research/STATE.json, docs/MASTER_PLAN.md and docs/BACKLOG.md. Then read OWNER_INTAKE and ACCESS_AND_RECOVERY. Consult the feature design before implementing that feature. Reference source material cannot override this repository's safeguards.

Also read [FEATURE_PROGRESS.md](FEATURE_PROGRESS.md) and the internal
`private/feature-progress.json` / `private/feature-progress.md` when present.
Keep their per-function status, blockers and evidence synchronized with STATE
after every material change. Work-package completion alone is not feature
completion; the optional bridge and later custom-look extension stay separate.

Owner priority update (2026-10-18): **native English and native Wi-Fi FTP first**.
FL2/FL3 is deferred to future work; calibrated custom looks remain later still.
Neither primary goal depends on FL2/FL3. Retain all evidence and device gates.

Latest owner intake (2026-10-18, **source-report**): α6700, firmware **2.00**,
current menu language **简体中文**, **Chinese mainland version**, and **English
unavailable**. The latest report supersedes the earlier unknown English/market
status; it supplies no complete language list, exact SKU or binary hash. EN-101
now follows restricted-language/resource feasibility; do not ask for the full
list again merely to establish English absence. No unlock mechanism or device
approval follows. See the
[intake update](../research/sessions/20261018-owner-mainland-english.md).

Owner also requires a verified rollback/recovery system before any firmware
write. No such target system is established. Follow the
[recovery/write gate](ACCESS_AND_RECOVERY.md#8-write-gate-checklist); this is a
prerequisite, not permission to test a restore or write.

Latest RA-003: [refused expanded-prefix trial](../research/EXPANDED_PREFIX_AUDIT.md),
[commands/results](../research/sessions/20261018-RA-003-expanded-prefix.md).
One frozen same-five expanded-header trial stopped **needs_review**, script exit **2**, host exit **1**, **38.945781s**.
Qualification **278/278 passed**, zero skipped, exit **0**, **2.001s**; 27 new cases plus 251 retained, all 27 foundation files unchanged.
Failure code **expanded_prefix_acceptance_failed**; no accepted expanded candidates, fresh directory or persisted stream-validation result.
Static source/metadata review finds float timing fields in prior summaries rejected by the new freezer; this is a sufficient blocker, not a logged precise runtime stage.
Observer cleanup reported no failures. No retry, fallback, changed threshold, child files or raw-prefix output.
Earlier five unknown classifications and all prior evidence remain unchanged. No decompression/disassembly, upstream/firmware execution, camera or feature/write gate.
Next single work package: **RA-003: design and synthetically qualify exact prior-metadata preflight using preserved production summaries, resolving the timing-field schema mismatch before any new actual prefix read**.

Earlier RA-003: [image-parser/header design](../research/IMAGE_HEADER_DESIGN.md),
[commands/results](../research/sessions/20261018-RA-003-image-header-design.md).
Four public parser blobs (**16,708 bytes**) verified at the existing immutable pin;
published MIT notice reviewed and preserved with private source copies.
Separate bounded AXFS/ext-family/legacy-FAT/LZPT header predicates qualified
with **251/251 synthetic passes** (49 new plus 202 retained),
zero skipped, exit **0**, **1.271s**. All 23 baseline files unchanged.
The new API remains standalone and unintegrated. **No actual firmware, member
prefix or operational-constants read**; prior five unknown observations unchanged.
No filesystem, English, native FTP, body-match, recovery or device-write gate.
Historical next single work package: **RA-003: implement and qualify an all-prefix reconciliation gate, then run one frozen expanded-header comparison on the same five members with full prior lineage**.

Earlier RA-003: [selected-member prefix study](../research/MEMBER_PREFIX_AUDIT.md),
[commands/results](../research/sessions/20261018-RA-003-member-prefix.md).
One selected-member prefix experiment completed, script and host exit **0**, **32.470943s**.
Synthetic qualification **202/202 passed**, zero skipped, exit **0**, **1.317s**.
**Five regular image-category candidates**, **4,096 bytes each / 20,480 bytes total**;
all five returned **unknown / unsupported_opaque** under the fixed classifier.
Complete fresh source/stream/header/span/original-prefix lineage and exact whole
directory equality passed before selected classification. No complete member
was covered by these prefixes; raw buffers discarded, no child files or links followed.
Classifier coverage is limited; this does not establish missing formats, English
resources or FTP code. No decompression/disassembly, camera or feature/write gate.
Historical next single work package: **RA-003: audit pinned image-format parser sources and reuse rights, then design and synthetically qualify bounded structural header predicates for the five opaque candidates before another actual read**.

Earlier RA-003: [opaque-link metadata inventory](../research/TAR_LINK_INVENTORY.md),
[commands/results](../research/sessions/20261018-RA-003-tar-link-inventory.md).
One bounded opaque-link directory inventory completed, script and host exit **0**, **29.409064s**.
Synthetic qualification **171/171 passed**, zero skipped, exit **0**, **1.060s**.
Private inventory: **137 members** (97 regular files, 39 directories,
0 hard links, 1 symbolic link); **80182** compact UTF-8 JSON bytes.
Complete source/stream/header/span/prefix lineage, tar framing, member padding,
two end blocks and zero remainder checked. Link targets are opaque private
metadata, never followed/resolved/materialized or claimed safe for extraction.
Member-path guards unchanged; the link-policy change was documented before
this trial. No child files, decompression/disassembly, camera or feature/write gate.
Member formats and English/FTP mapping remain unverified; earlier evidence preserved.
Historical next single work package: **RA-003: review the private directory to select minimal English/FTP-relevant members, then document, qualify and run bounded in-memory prefix identification with full lineage and no child files**.

Earlier RA-003: [bounded path/link diagnostic](../research/TAR_PATH_DIAGNOSTIC.md),
[commands/results](../research/sessions/20261018-RA-003-tar-path-diagnostic.md).
One bounded first-refusal diagnostic completed, script and host exit **0**, **28.299963s**.
Synthetic qualification **171/171 passed**, zero skipped, exit **0**, **0.916s**.
The first refused field is **link_target**, origin **header**,
predicate **empty_or_parent_component**. Combined categories retain their stated ambiguity.
Complete parent/logical-stream identities, header, declared spans and both prior
prefixes agree. Semantic tar parsing stopped permanently at the unchanged guard;
no directory accepted or tar-end/tail validation. One private bounded event,
no path text/raw bytes in it. No retry/fallback, child files, decompression,
disassembly, camera contact or feature/write gate. Earlier failed evidence is preserved.
Historical next single work package: **RA-003: review the observed path/link predicate, qualify an explicit metadata-only policy and run one bounded directory inventory with complete lineage and no child files**.

Earlier RA-003: [tar-directory refusal](../research/TAR_DIRECTORY_AUDIT.md) and
[commands/results](../research/sessions/20261018-RA-003-tar-directory.md).
One newly scoped tar-directory experiment stopped at the fixed **unsafe_path**
guard, **needs_review**, script exit **2**, host-tool exit **1**, **28.603684s**.
Combined synthetic qualification **133/133 passed**, zero skipped, exit **0**,
**0.749s**. Preliminary complete-parent hash passed; actual-pass final hashes,
fresh lineage acceptance and tar end/tail checks did not complete. No directory
accepted. Tentative header counter 114 is not a member inventory; post-discard
member count 0 does not mean an empty archive. Both observers cleared.
The offending member-name/link-target category is unknown. No retry, parser
fallback, threshold relaxation, child files, decompression/disassembly, camera
contact or feature/write gate. Prior measured observations remain unchanged.
Historical next single work package: **RA-003: qualify and run one bounded tar path/link diagnostic that records the first refusal category privately, completes source/stream lineage validation, and accepts no directory or child files**.

Earlier RA-003: [bounded component prefixes](../research/COMPONENT_PREFIX_AUDIT.md) and
[commands/results](../research/sessions/20261018-RA-003-component-prefix.md). U-slot SquashFS v4 and firmware ustar
header candidates, 4,096 bytes each. Complete parent/stream/header/spans agree
with prior lineage. Qualification 93/93 passed, exit 0; one real two-pass pipeline
exit 0, 23.899888s. No raw prefix/component files, decompression or disassembly.
No complete format, body, English/FTP, recovery or feature/write gate result.
Historical next single work package: **RA-003: document and qualify a bounded-memory, metadata-only tar-directory inventory of the candidate ustar firmware extent, then run it with full source/stream lineage checks and no child files**.

Earlier RA-003: [full-stream validation](../research/FDAT_STREAM_VALIDATION.md)
measured logical length/SHA and checked declared bounds without identifying children.

Earlier RA-003: [one bounded private header trial](../research/FDAT_HEADER_TRIAL.md).
That first-block observation remains preserved; the later stream result is separate.

Earlier RA-003: [crypto/public-constant provenance](../research/FDAT_CRYPTO_PROVENANCE.md) and
[commands/results](../research/sessions/20261018-RA-003-crypto-provenance.md). Pinned wheel/source identities and
eight isolated AES primitive tests are recorded. Native crypto code ran privately;
no fwtool/firmware or camera execution. One predeclared CXD90057_k8 trial needs
authored implementation and synthetic qualification; no exact-package key finding.
Next single work package: **RA-003: implement, synthetically qualify and run one bounded private FDAT header trial for the predeclared CXD90057_k8 hypothesis**.

Earlier RA-003: [bounded decoding basis/design](../research/FDAT_DECODING_PLAN.md)
and [commands/results](../research/sessions/20261018-RA-003-decoding-design.md). A pure decoded-header validator
checks CRC/extent metadata on synthetic inputs. Full suite: 228 total, 225 passed,
three skipped, exit 0. A narrow statutory rationale is documented; contract
interaction remains unresolved. No real payload read/decoding, crypto dependency
adoption or device action occurred.

Earlier RA-003: [bounded FDAT identification/extractor audit](../research/FDAT_EXTRACTOR_AUDIT.md)
and [commands/results](../research/sessions/20261018-RA-003-fdat-identification.md).
The prefix classifier returned unknown/unsupported_opaque; that is not proof of
encryption. Whole-file identity and previous spans agree. Local suite: 198 total,
195 passed, three skipped, exit 0. The open upstream PR candidate is source-only
and unvalidated for this exact package. This run interpreted a bounded prefix in
memory; it saved/output no prefix contents. No decoding or feature/write gate.

Earlier RA-003: [scoped UFU directory and parser audit](../research/UFU_CONTAINER_AUDIT.md)
and [commands/results](../research/sessions/20261018-RA-003-ufu-inventory.md).
An authored bounded reader and 179-test local suite passed (176 passed, three
skipped). Five chunk spans cover the acquired file under the audited framing;
one FDAT span is bounded. No payload contents were interpreted or output. Full
container semantics, component formats, extraction scope and installed-build
correspondence remain open. Next is bounded FDAT identification/extractor audit.
No camera command or feature/write gate passed.

Earlier RA-003: [official package, bounded identification and statutory route](../research/sessions/20261018-RA-003-package-law.md).
Separate destination consent led to HTTP 200, declared-size agreement and matching
transfer/stored SHA-256. Authored probe: UFU signature candidate; container not
validated. Article 50(5) expressly addresses software reverse-engineering research;
assess its conditions, exact acts and contract interaction before full analysis.
No unpacking/execution or camera contact occurred. Next single package is the
scoped RA-003 analysis/parser review in STATE.

Earlier RA-003: [China scope and limited acquisition results](../research/sessions/20261018-RA-003-cn-scope.md).
Owner confirms inspection in China for personal/noncommercial use. Download
consent is scoped; Article 17 is a candidate, not an established analysis basis.
See STATE for the recorded request/result, and the source dossier for scope.
No native feature, recovery route or write gate is validated.

Earlier RA-003 continuation: [official mainland 2.00 source/terms](../research/MAINLAND_FIRMWARE_SOURCE.md)
and [session results](../research/sessions/20261018-RA-003-mainland.md) are recorded.
No firmware URL GET/HEAD, agreement acceptance or external inquiry occurred.
Next single package: resolve the rights basis for proprietary offline unpacking/
static analysis using the prepared inquiry or another documented applicable
licence/statutory basis. Owner task authorization does not substitute for
third-party rights. Ordinary hashing is not equated with disassembly.

Earlier RA-003 [provenance/rights review](../research/OFFICIAL_PACKAGE_INTAKE.md):
the owner has **No / unknown** firmware inspection permission. One firmware GET
stopped at an unreviewed redirect with zero bytes and no retry; analysis remains
blocked. A separate Sony OSS page lists 34 source packages. The owner approved
only the two BusyBox source downloads under its notice. Both were audited
privately: supplied configs enable FTPGET/FTPPUT; final binary/body mapping is
unproved. No downloaded source was executed or integrated. Next single host
package: rights-cleared exact-2.00 binary intake/correspondence, blocked on rights
and legitimate applicable bytes. No native feature or recovery follows.

## 2. Responsibilities and continuity

| Participant | Responsibility | Must not claim |
|---|---|---|
| Webchat | Source research, design review, hypotheses, task decomposition and review of sanitized evidence | Access to local camera state that has not been supplied |
| Local Codex | Inspect actual local files/tools, implement host tooling, run tests, maintain private journals and propose exact hardware steps | Device success from host tests or another model's results |
| Owner | Provide missing body facts, approve device actions, maintain power/connection and observe physical results | That a repository push authorizes all possible camera mutations |

Git is the shared source of truth for authored code, sanitized findings and decisions. Private artifacts and detailed device state remain local. Read the newest committed state and local journal before resuming; do not rely on a remembered chat summary. A webchat request to investigate a hypothesis is not a blanket instruction to run every associated service command.

Initial offline-only means no camera communication or firmware execution. Normal authenticated Git operations and retrieval of public/official sources are separate host activities. Do not test a camera's network endpoints as part of this initial session.

## 3. Available starter commands

For a new checkout:

```sh
git clone git@github.com:mingwucn/a6700_research.git
cd a6700_research
git status --short --branch
python --version
python -m unittest discover -s tests -v
python tools/offline_inventory.py --help
python tools/artifact_probe.py --help
```

On Windows, use an existing supported Python 3.10+ interpreter, for example py -3 instead of python. Do not install a USB driver, firmware updater or third-party camera package to run these standard-library tests. Initialization tests passed under Python 3.13.5 on the webchat Linux host; Windows and the owner's computer remain untested.

That is the historical initialization result. Later local Windows tests and the
ctime portability repair are recorded in STATE and session reports. A final-code
clean export and the observed four-job Windows/Linux CI matrix have now passed;
see the [qualification report](../research/sessions/20261018-IN-102-final.md).
No camera function or device-write gate is established. See
[artifact intake](ARTIFACT_INTAKE.md) for the probe and
[host validation](HOST_VALIDATION.md) for current CI and publication limits.

If a checkout already exists, inspect status and branch first. Do not reclone over it, reset it, discard changes or force-pull. Use a fresh topic branch such as research/ra-001-intake when the local state permits. If the working tree is dirty, preserve it and isolate new work rather than guessing ownership.

The helper can inventory regular nonempty local files that have already been acquired through some separately authorized process. Example only, after substituting actual existing private paths and the observed firmware version:

```sh
python tools/offline_inventory.py --model ILCE-6700 --firmware UNKNOWN --alias body-01 --kind body-dump --artifact ap=private/body-01/original/ap-copy.bin --artifact cp=private/body-01/original/cp-copy.bin
```

These filenames do not identify real alpha6700 paths. UNKNOWN is an honest placeholder, not an eligible firmware version. The model/version/alias are user-supplied labels and are not verified by the tool. Kind body-dump is also a label, not proof of a complete backup. To inventory an official download, use kind official-package and a label such as package. Do not mix acquisition categories into one misleading report.

Output goes to stdout only. Save it to a NEW private file using an appropriate UTF-8 mechanism; never redirect over an input, because a shell can truncate a file before the Python program starts. Original paths/filenames are omitted from the JSON, but a person can still put a serial in an alias, and hashes can identify private material. Review any report before sharing it. The helper does not verify two backups, parse settings, establish restore coverage or authorize a writer.

## 4. Reference checkouts without execution

The two upstream commits are fixed in references/sources.lock.json. Optional host-side retrieval can use ignored external directories or an independent location. For a new external directory:

```sh
git clone --no-checkout https://github.com/QAQLeonard/a7c2-fl23-research.git external/a7c2-reference
git -C external/a7c2-reference checkout --detach c0930d5b0ccd49c0a092dc883054cd6dce199649
git clone --no-checkout https://github.com/lzh2016zzz/a7cr-fl23-research.git external/a7cr-reference
git -C external/a7cr-reference checkout --detach 43ba74441c8f10459ade41e84a379ad8005e6ef4
```

Do not overwrite an existing reference checkout. Inspect its status first. Do not run FL23.cmd, Custom-LUT.cmd, serviceshell, updatershell, a native worker or an installer merely because the files are present. Review dependencies and licences before importing code. New upstream commits or mutable release assets require a separate diff/hash review; they do not silently replace the lock.

## 5. First session: RA-001 only

Run the starter tests and record the interpreter and all skips/failures. Create a private intake from OWNER_INTAKE and a private session-state copy from templates/DEVICE_FACTS.json, adapting its purpose explicitly rather than pretending it is a populated observation. Do not overwrite an existing intake or journal. Gather owner-supplied firmware/regional/language/host facts; screen photos and serial-bearing details stay private.

Inspect the checked-in UNVERIFIED profile to confirm that it contains no executable support claim. Review git status and ignored-path handling. Create a sanitized session report using templates/SESSION_REPORT.md. Update research/STATE.json only with established facts; leave unknowns null. Commit only specifically reviewed authored files. No camera commands should have been run in this session.

RA-001 can finish with missing owner facts clearly recorded. Its purpose is to establish a reproducible local workspace and a precise intake, not to force a service connection. Proceed to RA-002 source audit after RA-001; do not jump directly to an installer.

## 6. Copy-paste initial Codex prompt

> Work in mingwucn/a6700_research. Read AGENTS.md, README.md, research/STATE.json, docs/CODEX_HANDOFF.md, docs/MASTER_PLAN.md, docs/BACKLOG.md and docs/OWNER_INTAKE.md. Execute RA-001 only: inspect the existing local Git state, record the host environment, run the standard-library synthetic tests, prepare a private owner intake without overwriting existing files, and write a sanitized session report. Prioritize native English menus and native camera-to-server Wi-Fi FTP. FL2/FL3 is deferred, with separately gated calibrated custom still-photo looks later; a host-assisted bridge is a separate optional result. Firmware and regional variant are unknown until observed. Do not contact the camera, change drivers or firmware, run upstream launchers or service tools, upload private inputs, or invent target offsets. Treat ordinary Git/source retrieval as host-side work only. Ask only for missing intake facts, continue useful offline work where possible, and finish with exact commands/results, files changed, unresolved prerequisites and the next single work package. Use a topic branch and stage only reviewed files. Do not mark a feature supported or a device-write gate passed.

## 7. Format for later work requests

A later request should name one work package, exact repository commit, local artifact inventory, relevant source hashes, current known device state and allowed risk tier. It should identify the hypothesis and expected output, not merely say make it work. Any R2/R3/R4 proposal includes the command/assets, expected side effects, stop conditions, current backups and conditional recovery limits before owner approval.

Before a real write, local Codex must recheck the target and candidate against actual fresh inputs. A webchat-approved design cannot certify a local byte sequence it has never inspected. Do not replace machine preconditions with a human confirmation string. No generic service helper is included in this starter because the exact alpha6700 route has not been established.

After an uncertain device outcome, report needs_review, the last confirmed journal step and whether I/O is still active. Do not reboot, retry or restore reflexively. Use the reconciliation procedure for the actual operation. Do not erase a workspace to rerun a clean installation.

## 8. Return packet to webchat

Return one sanitized session report and the corresponding Git commit or pull request. Include the task ID; owner-observed model/firmware/region where relevant; public source pins; non-secret command lines and exit codes; tests with PASS/FAIL/BLOCKED/NOT RUN; evidence class for each conclusion; exact unresolved question; and the next proposed action/risk tier. Include small relevant code excerpts or disassembly summaries with file-offset/VA distinctions when needed.

Do not attach complete firmware, camera backups/calibration, personal photographs, SDK distributions, credentials, serials/MACs or raw packet captures. Raw data stays available locally for reproducibility. Sanitized SHA-256 values may help compare inputs but should still be reviewed for disclosure implications.

Webchat can then review a concrete bounded question, for example whether a traced language field has unrelated consumers, whether a mode table's bounds are preserved, or whether FTP completion is reconciled after a lost reply. It should not be asked to infer camera runtime state from a screenshot of a successful host build.

## 9. Commit and review conventions

Use small branches/commits such as research/ra-002-access-audit, feat/offline-manifest-guards, research/en-101-language-map, research/cl-102-processing-map and research/ft-101-backend-survey. Names are examples, not existing branches. Prefix commit messages with docs, test, tooling or research as appropriate. Keep implementation and a device-result report distinguishable.

Review staged paths and content explicitly. A private repository and .gitignore are not permission to publish firmware or secrets. Never force-push or overwrite another contributor's work. CI, when added later, uses synthetic fixtures and does not require camera credentials or private binaries. A passing CI result must be an actual run, not an expectation.

## 10. Definition of a useful blocked result

A blocked package should contain the exact missing prerequisite, what was tested or inspected, what possibilities have been excluded, what remains uncertain and the smallest next acquisition/experiment. Examples are a missing exact-build resource package, an unverified service-helper ABI, or absent evidence for a capture-complete event. Such a report advances the project without pretending a feature is impossible or attempting unreviewed writes.
