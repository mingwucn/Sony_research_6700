# RA-003: prepared dependency runtime packet

2026-10-19. Branch `codex/ra003-runtime-packet-capture`, starting clean HEAD
`e6581637af9c694048e4a001f84a8cbb95894dce`. Evidence: **offline-tested**,
**static-inference**. English and native Wi-Fi FTP remain first; FL2/FL3 deferred.

One host-only preparation completed, exit 0. The private packet/request binds
five authored source buffers, eleven freshly read ordinary Python sources
(58,080 bytes), prospective config/cache text digests, fixed policy/package/root
expectations and the actual isolated CPython runtime profile. Observed metadata
for 351 package files and five trusted origins matched the historical identities.
The 22 ordinary read receipts total 2,424,920 bytes. The only launched child was
the standard-library-only runtime profiler; it exited 0 and was reaped. The
dependency request was **not launched**. No native bodies, firmware/constants,
historical source-cache bodies, USB or camera were read.

Both existing authorized reviewers accepted preparation source and saved metadata
consistency. Before the first run, review repaired bounded bootstrap/evidence
reads, qualification bindings, pinned-buffer extraction instead of
`inspect.getsource`, ancestor-checked metadata observations, and partial-failure
evidence with primary-exception preservation. A later docs-only HEAD migration
changed exactly two literals; both reviewers rechecked it. Final preparation
script SHA-256: `13a647411f4930487c7af58de7f91942b8d4edd43eb3630e9963407da13e4602`.

Packet SHA-256: `6a052c5421ac1dc00b6d78a0168511ab039a113d6eb5db91050ecd30eb02def1`.
Request SHA-256: `6050ce4e33e6d73d119501b9cde0c6430deef38e3b4552d58cda3ad75ab4f944`.
Review-basis SHA-256: `3f2c1733875d67b985562f5cfe7e26d118d47f785c2bc741c8ab62deec41727d`.
Packet and third-party source contents stay private. Root-agent saved consistency
verification checked packet bytes, canonical policy/package, raw text hashes,
five authored copies and runtime bindings. Reviewers inspected saved metadata
only: they did not reopen the packet or installed paths. Digests are consistency
evidence, not authorization, executing-parent authentication or process attestation.

## Exact host commands and results

- `git status --short --branch`: clean tracked tree.
- `git switch -c codex/ra003-runtime-packet-capture`: exit 0.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-runtime-packet/prepare.py`:
  exit 0, one exclusive attempt, no retry. Its only Python child uses the same
  interpreter/flags with `-c` and the pinned-buffer `runtime_profile` function;
  15-second timeout, process returned and reaped. Actual source/profile/receipt
  metadata are retained privately.
- `New-Item -ItemType Directory -Path private/sessions/20261019-RA-003-runtime-packet/current-qualification -ErrorAction Stop`
  and `Copy-Item -LiteralPath private/sessions/20261019-RA-003-runtime-packet/qualify.py -Destination private/sessions/20261019-RA-003-runtime-packet/current-qualification/qualify.py -ErrorAction Stop`:
  exit 0, separate exclusive output folder.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-runtime-packet/current-qualification/qualify.py`:
  **23/23 passed**, zero skips, exit 0, **8.087048000015784s** wrapper;
  CPython **3.13.12**, Windows AMD64; all **45** source/test pins unchanged.
  Tests cover prospective text conversion and runtime/invented grammar refusals;
  they do not exercise installed native dependencies or camera behavior.
  Log SHA-256: `d4082862a6befeb9cd2a143993c3e4576cee9993f92527e396ffc13462bbf0ad`.
- An inline saved-record diagnostic exited 1 at its own 2 MiB bound on the
  2,642,183-byte preparation-evidence JSON, before saving a result. File sizes
  were inspected; a separate saved-metadata reader explicitly permits 4 MiB.
  No production threshold or packet/preparation attempt was changed or replayed.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-runtime-packet/verify_saved.py`:
  exit 0; fixed saved-artifact digest/runtime/text consistency only, no execution.
- `C:/ProgramData/miniconda3/python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-runtime-packet/record.py`:
  saves report/progress and backs up private notes; asserts existing STATE keys
  unchanged except phase and next package. `git diff --cached --check` and
  explicit staged-path/content review required before commit.

The prior full suite remains **619 cases / 616 passes / three existing platform
skips**, exit 0. No authored production/test source changed in this package, so
the full suite was not repeated. The previous external-project refresh did not
advance the shared pre-camera dependency path; this packet preparation does.

## Remaining prerequisites and next work

Complete installed package/trusted **bytes** remain historical until a fresh
runtime collection. Metadata matches and eleven source reads do not replace that
collection. The filesystem observations are sequential and non-atomic. The
ordinary preparation/parent is unauthenticated; a review digest cannot grant
authority. Native loading, transitive loaders and mapped bytes remain separate
limits. All seventeen historical blockers are retained. English/native FTP
mapping, exact-body identity, recovery and device-write gates remain unproved.

The next runtime attempt must use a new exclusive folder, the unchanged request,
exact reviewed source buffers and current runtime; freshly validate all 351
package and five trusted contents before bootstrap. Run public vectors only,
without protected callbacks. Preserve child disposition and partial evidence;
no automatic retry after timeout, interruption or uncertain completion. Reconcile
saved results before considering any later protected continuation.

Next single package: **RA-003: review one exact once-only dependency-runtime driver against this frozen request, then perform and reconcile a single dependency-only observation if its fresh bindings pass; public vectors only, no protected continuation or camera.**

Changed public files: this report, DEPENDENCY_RUNTIME_PACKET, dated successor
note in DEPENDENCY_ACTIVATION_PACKET, BACKLOG, HANDOFF, FEATURE_PROGRESS and STATE.
Private session/feature notes backed up before update. Camera commands: **none**.
No feature support, recovery or device-write gate passed. The overall goal remains active.
