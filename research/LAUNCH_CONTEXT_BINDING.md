# RA-003: metadata and launch-request correlation

2026-10-20. Evidence: **static-inference**, **offline-tested**.

`tools/dependency_launch_context.py` now composes the existing checked fourteen-role
metadata validator with the prepared adapter request. It consumes original request
bytes and caller-supplied original context/legacy documents, not filesystem paths.
It neither starts a process nor constructs an observer. Public runtime/direct CLI
remain refusing. Checked-buffer owners and their lifecycle belong to the reviewed
caller; this module is a trusted composition function, not a sandbox or launcher.

The historical metadata grammar has 44 comparison source roles. The prepared
request has 46: 38 retained roles, six explicit replacements, and two added policy
imports. Retained bytes and origin labels must agree. The three loaded adapter
buffers must equal their prepared-map counterparts. The five validator source
claims, four shared dependency helpers, and shared scope/comparison policy buffers
must equal the corresponding checked metadata-owner buffers. All fourteen owner
buffers are rehashed against its frozen hashes before and after composition.
Path labels and supplied source receipts remain claims, not fresh opens.

Both paths must share operation, frozen limits, dependency review, original
package/config/cache, roots/native policy and other expectation fields. Source
digest rosters differ intentionally. The old dependency packet retains its two
explicit aliases; the current packet binds five helpers plus a derived canonical
closure manifest. Each existing pure binder validates its own packet/fixed/review
and original source buffers. Only the expectation/source digest fields that must
change are excluded from shared-field equality; package/root/fixed/review fields
remain bound. No historical document is rewritten to claim successor coverage.

Full invented composition executes the existing fourteen checked public metadata
modules and eleven retained ordinary preflight validators. Protected role sources
are only hash/AST checked; no GDT reader/pipeline or actual input executes in this
package. The invented fixture restores two former inert dependency source stand-ins
to authored comparison texts, then reconstructs its own dependency/source/activity
anchors and original-byte document chains. Historical saved evidence is untouched.

The new private qualification checks complete composition without input mutation,
noncanonical original request bytes, operation/source/origin/validator substitutions,
config/cache/package/native-policy/fixed/review changes, loaded-adapter replacement,
changed closure hashes, stale context/source receipts, scope widening, fully
rebound mutable metadata-owner buffers and second-owner acquisition failure.
Public tests separately establish refusal before owned code runs on changed raw
bytes, duplicate keys, nonfinite JSON, oversized input and public runtime calls.

Independent source review found that the retained metadata loader does not rehash
its exposed source buffers during intact(). This composition now verifies all
fourteen buffers against that loader's frozen hashes, with a fully rebound negative
case. Review also found an acquired metadata owner leaked when the fixture's
second owner failed; independent once-close cleanup now preserves the primary
exception and secondary cleanup cause. Both repairs were accepted source-only.

The result is a correlation of historical ordinary semantics with a current
request. It is NOT complete ordinary semantics for the 46-role request, fresh
startup/source/dependency provenance, reviewer/owner authentication, a rights
decision, an actual launch preflight, or permission to activate anything. The
existing isolated GDT process qualification remains historical and was not repeated
or silently extended. Its supervisor limits remain unchanged.

English/resource restriction mapping, native FTP backend, exact body/build,
complete backup and usable rollback remain unproved. English/native FTP retain
priority; FL2/FL3 and calibrated custom looks remain deferred; a bridge remains
HOST-ASSISTED. Five activity-specific questions remain pending with no new legal
determination or consent. No camera, feature, recovery or device-write gate passed.

91/91 focused cases pass, zero failures/errors/skips, exit 0; 71 public boundary/retained regressions plus 20 full invented composition/refusal cases, 25.282413s, 137 stable pins. Historical 44-role comparison and current 46-role request share 38 retained source buffers and origin labels; six replacements and two imports remain explicit. Independent source review repaired mutable owner-buffer binding and fixture acquisition cleanup. Current-role ordinary semantics and fresh outer integration remain pending. English/native FTP first; camera commands none; no feature/recovery/write gate.

Next single package: **RA-003: implement successor ordinary dependency/source semantics for the current 46-role prepared request, deriving the closure_manifest bytes directly from that same source map and binding the five checked helpers without labelling derived JSON as a Python source. Retain the old 44-role validator as comparison-only; migrate the affected ordinary contracts rather than pretending their old source-alias grammar already covers the successor. Qualify complete invented records and independent source review before connecting the current-role preflight to the isolated launcher. Keep actual observation/public runtime disabled, decisions pending, and no actual activation records, installed dependency activation, firmware/constants/native payload reads or camera contact.**
