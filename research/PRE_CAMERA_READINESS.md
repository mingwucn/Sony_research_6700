# Pre-camera work coverage

This ledger preserves the full objective: FL2/FL3 stills and preview, separately
gated calibrated custom still-photo looks, native English menus and native Wi-Fi
FTP; a host-assisted bridge remains optional. It records preparation, not feature
support. All target facts, USB observations and device approvals remain absent.

Owner priority update (2026-10-18): English and native Wi-Fi FTP are primary;
FL2/FL3 is deferred, with calibrated custom looks after it. The complete ledger
below preserves future work without making it a prerequisite for English/FTP.

The broad owner request authorizes continued host-only work beyond RA-002. It does
not approve a device operation. All target-independent implementation here uses
authored code and synthetic inputs. No target profile, offsets, assets or source
values were populated from the references.

The [feature progress note](../docs/FEATURE_PROGRESS.md) and ignored internal
feature note summarize the requested functions independently of package status.
No prepared or passed host package is promoted into a working camera function.

## Every work package and its evidence boundary

| Package | Current pre-camera work | Requirement still needing evidence |
|---|---|---|
| RA-001 | Private intake/host baseline prepared; historical errors preserved | Owner body/setup facts remain unknown |
| RA-002 | Locked source/provenance/rights audit committed | Component reuse and target applicability are separate unresolved gates |
| RA-003 | Inventory portability repair, bounded probe, lineage template and extractor text audit | Installed firmware, matching legitimate input and applicable extraction/child manifest |
| RA-004 | [Observation/access preparation](TARGET_EVIDENCE_GAPS.md) | Identity, separately approved observations and exact-target access proposal |
| RA-005 | Backup coverage inventory/template prepared | Approved route, independent reads/copies and actual protected-state coverage |
| RA-006 | Architecture/recovery evidence gaps explicit | Target segments/ABI/storage/settings/retained-state mappings and recovery envelope |
| RA-007 | Candidate/inverse guards, in-memory simulator and durable synthetic journal/OS ownership; Windows subprocess crash/reopen tests | Exact-target semantics/reviews, POSIX and final-revision portability, any future executor qualification |
| EN-101 | Existing language hypotheses/critical-resource protocol retained | Actual language list, resources and all policy-field consumers |
| EN-102 | Generic guards available; no candidate generated | EN-101 result, target sources and narrow inverse/preservation proof |
| EN-103 | Physical validation protocol retained | Accepted candidate, approved hardware test and ENT-01..06 observations |
| EN-104 | Resource/uninstall dependencies specified | Individually proven features and ENT-07 integration evidence |
| CL-101 | Repeatability/capture protocol retained | Actual stock looks, owner recipes and baseline photographs |
| CL-102 | AP-to-CP layer investigation queue prepared | Target artifacts, independent xrefs and all reachable routes |
| CL-103 | Donor/target distinction and preservation rules retained | Legitimate donor inputs, target layout, capacity and adapted data specification |
| CL-104 | Generic guard/inverse tests available | Target coherent FL23 candidate, instruction/control-flow review and G4 proposal |
| CL-105 | Still/metadata/preservation matrix retained | Approved target execution, measured still effects and complete protected readback |
| CL-106 | Preview/load-state protocol retained | Target evidence and physical no-shutter/transition/performance tests |
| CL-107 | Domain/holdout/selected-slot requirements retained | Stable FL23 baseline, calibration inputs/rights and target slot/resource ownership |
| FT-101 | Native backend hypothesis and dependency queue prepared | Target backend/task/UI/network/media evidence; no route selected |
| FT-102 | Durable mock queue plus 19-case constrained loopback FTPS run, full read-back/TLS/race/fault tests | Independent/deployment peers, physical faults, real media and native constraints |
| FT-103 | Native-origin acceptance remains explicit | One approved camera-resident upload and end-to-end server equality |
| FT-104 | Generic queue grouping/reconciliation can be simulated | Target media-completion/lifecycle events and native automatic capture |
| FT-105 | Security/resource acceptance protocol retained | Target certificate behavior, coexistence, shooting/thermal/battery measurements |
| FT-106 | Optional bridge architecture retained | Model-specific PC Remote/SDK evidence and separately approved camera leg |
| IN-101 | Composition/uninstall protocol retained | Independently accepted target features and complete combination matrix |
| IN-102 | Local synthetic checks, clean committed-tree/no-pip reproduction on the same Windows host, CI preparation and publication policy | Actual remote Windows/Linux CI, clean OS/independent hosts, real-symlink and broader release evidence |
| IN-103 | Soak/reversal/reproduction protocol retained | Accepted features, hardware qualification and independent eligible reproduction |

The original detailed deliverables/thresholds in BACKLOG.md, MASTER_PLAN.md and
VALIDATION.md remain authoritative. A preparation row does not close that package.
RA-003/004/005/006 and all feature results remain incomplete. The linked evidence
gaps dossier lists the minimum real artifacts and observations needed.

## Offline validation coverage and limits

- OFF-01..07 and OFF-09: generic synthetic source-set, bounds, identity, inverse
  and byte-preservation coverage only; no real model/build accepted.
- OFF-08: target enum and processing bounds remain NOT RUN.
- OFF-10: target instruction boundaries, incoming branches/ABI remain NOT RUN.
- OFF-11: resource decoding/checksum/UTF coverage remains NOT RUN. Header malformed
  input tests do not substitute for a native resource parser.
- OFF-12..13: in-memory simulation plus durable synthetic append/fsync, cooperative
  OS exclusion and subprocess crash/reopen/reconciliation on Windows. POSIX fork
  is skipped here. No camera transport, persistent device journal or OS camera
  lock was tested. See the [journal contract](../docs/DURABLE_SYNTHETIC_JOURNAL.md).
- OFF-14: explicit path/content review of the proposed local commit. This is not
  a comprehensive automatic secret/content-rights detector.
- FTT-03..09: mock scenarios and a separately audited custom loopback peer use
  synthetic spool bytes. The lab tests real TLS, full retrieval and exclusive
  operations for that peer only; host fault injections are not physical faults.
  These remain partial host evidence, not complete native FTT passes.
- All CLT-01..11, ENT-01..07, native FTT-01..12, target recovery/readback and
  independent reproduction remain NOT RUN. No device-write gate passes here.

Exact tests/results belong to the current session report and private raw logs.
Windows real-symlink behavior remains untested when fixture creation is skipped;
mocked symlink rejection has separate coverage. Remote CI is NOT RUN until an
actual run is inspected, irrespective of a workflow file being present.

## Remaining useful work and next target package

The [loopback lab](../docs/FTPS_LOOPBACK_LAB.md) now supplies observed host evidence
for its constrained peer, hash read-back, no-clobber finalization, certificate
failure and queue reload/reconciliation. Its link/unlink extension is not generic
FTP rename semantics or power-loss proof. Other peers, physical faults and target
constraints remain untested. [Clean authored-tree reproduction](sessions/20261018-IN-102-clean.md)
now passed 129 tests with one real-symlink skip in a fresh no-pip environment,
without private inputs/reference checkouts/lab runtime. All 58 exported files
remained unchanged. This is the same existing Windows host/base stdlib, not a
clean OS or independent-host result. Remote CI remains NOT RUN.

The separate [durable synthetic journal](../docs/DURABLE_SYNTHETIC_JOURNAL.md)
now has 23 focused passing tests with one POSIX-fork skip. The full suite passed
152 tests with two skips (POSIX fork and unavailable real symlink), exit 0, on
this Windows host. Actual hard-link refusal passed. A retained crash example
reconciled an applied operation without replay. [Session evidence](sessions/20261018-RA-007-durable-journal.md)
records failed attempts and limits. No device executor exists.

The next single host package is **IN-102 final-revision qualification**: a fresh
committed authored-tree/no-pip reproduction of this new code and observed results
from the existing Windows/Linux CI matrix, followed by publication and feature-note
consistency review. Earlier clean-run evidence remains tied to its older source
commit. POSIX and remote results remain NOT RUN until observed. These host checks
add no gate before ordinary separately approved UI observation.

The next target-specific package remains **RA-003**, beginning with the missing
installed-firmware fact and matching official-package provenance. No latest build
is substituted, and no camera update/contact is needed to continue independent
host work. Owner facts already answered Unknown are retained without repeated
questions. Camera commands in this preparation: **none**.
