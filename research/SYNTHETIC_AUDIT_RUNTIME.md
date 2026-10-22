# Genuine Python audit probes in the synthetic runtime path

2026-10-22. Evidence: **static-inference**, **offline-tested**. Native English and
native camera-to-server Wi-Fi FTP stay first. Camera commands: **none**.

The current invented-files child now delegates startup, audit installation,
audit probing and the producer callback to unchanged original `RuntimeOps`
methods. The source class/methods and runtime dispatch, controller, collection,
producer and frozen parent verification remain unchanged. Instance shims record
production calls separately from original delegations and cleanup probes. A
labelled constructor double still supplies the operations object; bootstrap,
native loader, public-vector cipher and protected processing remain inert.

The positive performs one genuine startup call, one original audit installation,
one original production probe and one original callback. Startup results agree
with separately recorded child isolation flags. A passive observer installed
before the guard sees the genuine Python probe event before guard handling and
records only token-match booleans and guard state, never the token. The original
guard acknowledges exactly one correct production probe. The original callback
uses synthetic AES and the same public-vector lookup behavior, not real crypto.

The independent filesystem oracle remains in the joined path: 356 newly authored
invented files, 398 original reader calls and 10 original root calls in the
positive. Every successful read matches its full independently captured receipt
and byte hash; unchanged roots match separately captured directory identities.
No installed dependency or executable native payload is read. Five simulated
native events still call the exact guard hook directly. There is no emitted
`ctypes.*` event and no native-loader audit qualification. The positive retains
72 vector lookups and one producer callback.

| Separate negative mode | Original refusal | Final probe count / sticky failure |
|---|---|---|
| Existing hook suppresses original guard registration | `audit_not_acknowledged` | 0 / false |
| Production shim omits its probe | `audit_not_acknowledged` | 0 / false |
| Original probe sends wrong token | `audit_probe` | 0 / true |
| Original probe sends a second valid token | `audit_probe` | 1 / true |
| Wrong-token error swallowed, followed by valid original probe | `audit_not_acknowledged` | 1 / true |
| Install shim interrupts before original method | `synthetic_audit_install_error` | 0 / false |
| Probe shim interrupts before original method | `synthetic_audit_probe_error` | 0 / false |

Suppression uses a separate existing hook raising RuntimeError on
`sys.addaudithook`: the original install method returns, but the absent guard
acknowledgement is still refused. Wrong/duplicate probes exercise the unchanged
guard condition. Swallowing the first invalid-probe exception cannot clear its
sticky failure even though the following correct probe increments the count.
Delegated flags follow production delegation counts; cleanup calls do not turn
an interrupted/skipped production operation into a delegated one.

All seven negatives retain `needs_review`, close unclaimed prepared callbacks,
perform no protected source passes or constants reads and invoke neither the
fake loader nor producer callback. They observe 361 ordinary dependency reads
before refusal. No automatic retry occurs.

After base ownership cleanup, every case records an inactive, finished guard and
calls the original probe method directly once with a nonmatching invented cleanup
token. The guard count remains unchanged. The independent observer records that
event, then disables itself; the optional suppressor is also disabled. Registered
Python audit hooks remain until disposable-process exit. They are explicitly
reported retained/inert, never removed or restored. Suppressed-install and
install-error modes never register the guard. Their cleanup probe proves an
inactive guard object and observer delivery, not delivery to a registered guard.

Current qualification is **8 new cases plus 66 regressions: 74 distinct cases**,
zero failures/errors/skips, with 103 matching stable source pins. The previous
153-case filesystem qualification is inherited under its unchanged 101 pins;
its **full suite was not rerun**. Fourteen prior filesystem/runtime cases are
rerun within the current 66 regressions. Totals are not added. The preliminary
focused run and positive smoke are also excluded from distinct-case totals.
[Commands, logs and changed files](sessions/20261022-audit-probe.md).

The child safety-hook source is unchanged and still denies actual native/network/
subprocess activity. This remains trusted local composition, not a hostile-code
or hostile-filesystem sandbox. Foreign audit-hook interference, foreign-wrapper
replacement, ambiguous close completion and physical recovery are not covered.
The original Windows contract remains required. Legacy runtime-shaped fields
saying actual observation or no injection remain synthetic schema, while outer
actual-runtime, installed-dependency, authentication, operational acceptance,
execution, feature, recovery and device-write claims stay false.

All 16 frozen ordinary records, five historical pending dispositions and three
actual dependency nulls remain unchanged. No current actual executable/source
manifest migration, protected input/source processing, upstream execution,
network/download/upload, driver/firmware operation or camera contact occurs.
English/native FTP and practical rollback/recovery remain unvalidated.

Next single package: RA-003: qualify an original RuntimeOps instance with an explicit inert bootstrap/cipher adapter through the existing invented-files preparation and parent path. Retain original reader/root/startup/audit/callback methods and inactive retained-hook cleanup. No installed/native/protected inputs or camera contact. English/native FTP stay first.
