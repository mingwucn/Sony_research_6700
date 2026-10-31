# α6700 2.00: English resources and language policy

2026-10-26. Evidence: **static-inference**, **offline-tested**. This is a
package-level result; installed-body correspondence and native behavior remain
unverified. Camera commands: **none**. Network commands: **none**.

The locally retained official mainland 2.00 package contains English resources
for all four string families. Its startup resource path can resolve English
from the selected-language value even when English's menu-availability flag is
disabled. A language-only selected-setting route is therefore supported by
static evidence, without requiring a blanket region conversion. A working
unlock and complete preservation of runtime regional state remain unverified.

The latest [boot-handoff review](sessions/20261026-english-boot-handoff.md)
adds exact updater-layout and root-filesystem startup evidence. The packaged
script path attempts the application mount, conditionally loads the settings
driver with a zero load argument, then launches the application bootstrap.
That argument joins the previously traced preexisting-memory initialization
path. Actual startup success, the live settings header, native memory source,
separate program clients and complete regional preservation remain unbound.
The warm-boot-image role is explicit; its contents are not yet identified as
the kernel or the separate program. No camera commands were run.

The [memory-source continuation](sessions/20261026-english-boot-memory.md)
hashes the entire exact warm-boot member while retaining only a prefix and
bounded contexts. It identifies shared packaged device-tree bytes, native-name
occurrences and shallow image-header candidates, then separates those from
provider definitions and complete files. A distinct pre-loop initializer
launch and fixed probe/reply callback are traced, with no program-memory
readiness claim. The exact checked program-header pair has no raw match in
this member; that result does not exclude compressed or constructed forms.
The native memory mapping and complete regional preservation remain open.

The latest [native-memory review](sessions/20261026-english-native-memory-map.md)
corroborates a 1,314-record section layout and a native AArch64 Image header.
It binds both missing converter definitions through 6,089 export records and
separate native diagnostic references. The packaged program-address value
falls in an omitted section interval; this does not identify its producer or
prove absence from memory. Complete cache semantics, actual settings/program
memory and regional preservation remain open. The owner explicitly authorized
research reverse engineering; offline-only and no-camera constraints continue.

The latest [program-handoff and reference review](sessions/20261026-english-program-handoff.md)
locates the exact program file named by a conditional native loader path.
Independent filesystem and allocation-chain checks reproduce the complete file,
which matches the native header predicate. A conditional direct-copy model,
entry references and the API destination layout are corroborated. Normal
preload and selected-language clients remain open. Pinned PMCA sources support
separate language flags as a method; their regional defaults and blanket
catalog workaround do not transfer to the target. No write payload was made.

The latest [program-client review](sessions/20261026-english-program-clients.md) maps all native API slots and exact descriptor wrappers. Its finite direct callback path uses an initially distinct non-language item, while the reviewed write/reset wrapper reference forms have no callers. Dynamic and indirect clients, table mutation, normal preload and live state remain unresolved. The writable-data escape copy is backup intent rather than a demonstrated remap. These results narrow the search without proving complete regional preservation or a working unlock.

## Input and reproducibility

The existing acquired package is 1,024,017,848 bytes, SHA-256
`d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c`.
The authored stream decoder reproduced the prior full logical-stream hash,
`e48b05235ddba0d8098fa4d71dd88d85ffe4e5ab440581003c6c3b4d5a813373`,
after checking all 1,000,017 physical block envelopes and terminal state.
Only the selected application filesystem image was retained, with SHA-256
`8dfa61a10f3c91f39e13fc640ad022afcd697168a9d3a3d15353a0ad1e70f872`.
Its classic ext2 metadata was read through a bounded callback; it was never mounted.

The extracted 89,027,992-byte application has SHA-256
`e65fd595052be5d0e98ce8000dfcb94f90a2f8309de70ef140375052009b0ef3`.
This is the official-package object, not a claim about a running process or the
owner's installed file. All target bytes, complete resource text, instruction
records, API identifiers and ELF address mappings remain in ignored private
evidence. No firmware, resource replacement or settings payload is published.

## English resource coverage

The independently authored [UXC reader](../tools/uxc_readonly.py) checks the
version/kind, descriptor, index, record IDs, bounds, UTF-8 and non-overlap. The
eight retained English and Simplified Chinese files were independently hashed
and reparsed with the final reader, reproducing the saved text dictionaries.

| Family | English records | Chinese records | IDs missing in English | Empty in both |
|---|---:|---:|---:|---:|
| main | 2,445 | 2,445 | 0 | 4 |
| `_f` | 3,731 | 3,731 | 0 | 19 |
| `_func_j` | 3,767 | 3,767 | 0 | 0 |
| `_g` | 1,974 | 1,974 | 0 | 0 |
| Total | 11,917 | 11,917 | 0 | 23 |

Each pair has identical resource-ID sets. All 23 empty English records are also
empty in Chinese; no nonempty Chinese record has an empty English counterpart.
The English files include setup, warning, authentication and FTP text. The
English language-choice label was resolved by its actual resource ID, connecting
the menu record to these resources rather than relying on an ASCII name alone.

The package's resource database also contains the four English filenames. Its
font list registers a Univers font path, and the corresponding font file is in
the application directory. Those are resource-dispatch/font leads, not proof
of glyph coverage, layout, fallback behavior or successful native rendering.
Per-screen reachability and all physical acceptance tests remain unrun.

## Restriction traced in the application

The exact application is an AArch64 ELF. The
[static ELF inspector](../tools/elf_static.py) maps file offsets separately from
ELF link-time virtual addresses. It does not load the object, apply relocations
or execute instructions. Bounded instruction recognizers produce candidates
that are checked in their surrounding instruction and relocation records.

The current trace connects these separate paths:

1. A per-language availability reader obtains one Backup byte. Stored value 1
   becomes enabled; stored value 2 becomes disabled. Other values enter a
   diagnostic path and are not a supported third state.
2. An English-specific wrapper supplies its own item to that reader. A model
   property exposes the result, and the English menu predicate tests it for
   enabled. The same menu record resolves to the English resource label and
   English choice value 0.
3. Current-language get/set functions use a different Backup item. They accept
   values 0 through 33 and preserve that value as a single byte. The selected
   language setter has one normal-path call to the imported Backup write API.

The generated name registry uses one-based ordinals while observed code uses
different numeric property values. Their general conversion is not assumed.
The English identity above is supported by its resource label and code path.
Likewise, a Backup-labelled name table is not assumed to use the same namespace
as the persistence API.

## Selected English can reach the resource banks

Two separate instruction reviews agree on the bounded startup path:

1. The language menu's current-value callback reads the selected-language model
   value, which is initialized from the native language getter.
2. The generic menu lookup first seeks an available choice with that value. If
   none matches, a second pass returns the matching choice without an
   availability call. This preserves the selected value in the reviewed path
   even if its menu predicate is disabled.
3. Startup passes that choice's item ID into the resource-bank selector. English
   choice 0 maps to bank 0 for all four string namespaces.
4. Independent exact-file assertions check the resource database's namespace
   headers, 34-bank indexes and bank-0 references. They resolve to the same four
   English files whose contents were parsed above.

This is stronger than resource presence alone. It supports investigating only
the selected-language setting, leaving the protected permission flag and
regional identity unchanged. It is not a runtime test: a complete search for
earlier normalization, indirect callbacks or additional restrictions is not
claimed, and rendering has not been observed.

## Language-only settings and regional defaults

Separate language permission and selection items make a narrow language-only
route plausible. An independent instruction review confirms that the valid
English selection path makes one Backup write call and does not call the
permission reader or a region setter. The traced video-system and Wi-Fi
destination selectors are different items. Sharing a Backup group does not
make these items the same field.

The imported Backup API is an interprocess client. Its receiver was traced into
the exact package's Backup kernel module. That implementation looks up an exact
item, checks the group and metadata, and copies the recorded item length. A
separate synchronization operation handles broader persistence and checksums.
A logical one-byte item therefore does not imply a one-byte physical transaction.

Five bounded Backup members were extracted in a separate full-lineage-checked
pass. Comparing the primary application-processor (AP) catalogs in the
same-family CN1 and ALLLANG shipped files gives:

| Logical item | Width | CN1 | ALLLANG | Relevant attribute |
|---|---:|---|---|---|
| English availability | 1 byte | disabled (2) | enabled (1) | Protection bit set; provider callback bit clear |
| Selected language | 1 byte | Simplified Chinese (25) | Japanese (1) | Provider callback bit set |
| Snapshot language | 1 byte | English (0) | English (0) | Separate item; provider callback bit clear |
| Video-system destination selector | 1 byte | 1 | 1 | Different exact item |
| Wi-Fi frequency-band destination selector | 1 byte | 1 | 1 | Different exact item |

The primary AP catalogs have 37,169 record slots, with 27,634 present items each.
Metadata, attributes and sizes agree; 40 current AP item values differ. The
separate coprocessor (CP) catalogs have 35 differing current item values; the
complete files differ at 97 byte positions. Thus replacing CN1 with ALLLANG
would alter more than English. Neither file is a backup of the owner's body.
The package's MainDest fallback names another product-prefix/market entry; it does not prove
which table the owner's installed firmware selected.

In each table, the English permission and selected-language payloads do not
overlap any other present item's current payload. This supports logical field
independence in those shipped files. It does not prove runtime callback effects
or preservation of an installed storage image.

Protection is conditional in the traced provider: it tests both the item
attribute and a runtime header state. Shipped header values do not establish the
body's current state or write eligibility. The remaining runtime callback,
initialization and reload questions are described below.

## Initialization and queued persistence

Exact-byte checks of every accepted native getter/setter case confirm that all
34 language values are preserved. The application persistence worker passes a
queued language value to the native setter unchanged; no additional explicit
region write occurs in that reviewed body.

The initialization map's source is now resolved: a compiled table of 2,930
unique key/value pairs contains English value 0 for selected language. Its ELF
constructor copies that pair unchanged, and the lookup returns its value field.
Independent exact-file assertions confirm the table, constructor registration
and copy. The consumer is reached through the application system-initialization
thread. A bounded reference audit found lookups and the constructor; lifetime
immutability and global ordering across threads remain unproved.

The other model-copy source is a separate saved snapshot language item.
Successful bulk reads load its one-byte value; a read-count mismatch instead
copies the current language model. Both consumers preserve the incoming value.
One secondary apply mode skips the language-copy body. The snapshot defaults
to English in both shipped catalogs and has no current-payload/capacity alias
with other present primary AP items. Its actual installed value is unobserved.

On the reviewed explicit native-load boot arm, snapshot application precedes
the native selected-language getter, and the latter precedes resource-bank
selection through a backward branch. A separate boot arm skips that native
load. Its three queued operations resolve to display setup, EVF frame rate and
EVF colour temperature. Their reviewed local methods have no direct language
reload; asynchronous completion and transitive effects are not fully proved.
These arms cannot be merged into one unconditional ordering claim.

The selected language also has an exact deferred observer entry. Its callback
copies the new model value into a language persistence record; the worker passes
that value to the native selected setter. The compiled phase-scheduling map
has no selected-language entry among its 885 initialized records. A separate
285-record observer table contains the resolved callback. These are different
maps; absence from one does not exclude the other or later mutations.

Ordinary notification first queues an update ID. The actual drain updates an
engine record and sets its pending flag; batch completion uses that flag to
invoke a separate callback. All 34 compiled language conversions round-trip
unchanged, including English, with no availability check in that bounded
converter. The callback can mark the deferred observer, conditional on an
enable flag. The reviewed wrapper orders the update drain before deferred
current-language persistence and then snapshot flushing.

Snapshot notification and flushing can copy the selected model byte into the
separate saved snapshot item. Requested and effective engine values occupy
different fields. The ordinary recompute path is now checked: when a queued
update supplies English and sets its recompute flag, the engine copies that
value into the effective field, or finds it already equal. The selected
compiled direct-rule list is empty, the special-case helper does not apply to
this parameter, and the reviewed policy predicate does not veto English.
Independent operand and branch checks support this finite result. Actual
queue execution and complete lifetime behavior remain unobserved.

Engine setup initially puts an invalid sentinel in the selected requested,
effective and saved-effective fields. It does not seed English or Chinese.
The selected parameter is absent from all 127 compiled initialization override
IDs. This setup follows the compiled model-map application on the reviewed
system-initialization slice; model defaults and engine initialization are
different objects and phases. The queued batch must replace the sentinel.

The selected parameter's one reverse rule points outward to the screen-reader
setting. Its English case has no effect block. This does not prove the target
setting always remains unchanged: it has two other rules, its own current
state and a distinct one-byte snapshot persistence descriptor. No unconditional
harmlessness or region-preservation claim follows from the rule's name or
English case alone. Current language, snapshot language, accessibility state
and resource-bank selection remain distinct.

## Callback and persistence boundaries

The provider's notification wrapper filters the changed item and calls a
subscriber function. The wrapper itself does not write a regional setting.
A finite survey of application, library and module registrations has not
identified a concrete selected-language subscriber. The traced kernel queue
route uses the identifier's low 16 bits; an earlier full-identifier-only
exclusion was therefore withdrawn. Userspace-local queue indexes belong to a
different route, selected by a flag bit before registration. A local lookup
mask does not establish an alias with the kernel notification queue.
Forwarded, indirect and external consumers remain open.

Initialized allocation ranges narrow some dynamic registrations. The previous
delegated ioctl dispatch gap is now resolved and independently checked: a
computed table anchor selects the handler that invokes the expected allocator.
The traced initialized range excludes the Backup notification queue, conditional
on its reached flag path and range state. Runtime device-handle binding, copy
and context gates, later range mutations and other registration routes remain
unobserved. This closes table selection, not all subscriber behavior.

A later review follows 77 registration arguments that the original narrow
recognizer left unknown across three libraries. Two are direct constants,
two have checked initial global values, and 67 have conditional allocator
origins. The other six now bind to a native timer service: identical creation
requests reach its registered handler, which allocates a timer queue and
returns that ID separately from its timer context. Under the reviewed native
provider, initialized pool and successful path, the returned queue range
excludes the Backup notification queue. This is conditional static evidence.

The earlier module survey omitted the synchronous registration API; the
expanded relocation survey found the timer handler. Its absence from the
earlier survey was a coverage gap. The new transport review also distinguishes
the actual kernel synchronous-send function from a similarly named export.
Independent exact-operand checks reproduce the handler, operation dispatch,
allocator call and returned fields from the module bytes.

The six callbacks dispatch timer messages to function pointers. Their finite
bodies and ten actual callback bodies are retained; queued receivers and a
virtual implementation remain unresolved. Identifying a timer origin does not
prove its eventual consumers cannot change settings. See the
[timer-service continuation](sessions/20261026-english-queue-service.md).

The subsequent [infrastructure review](sessions/20261026-english-infra-origins.md)
traces another 16 original unknown arguments across Remote, MFi and Bluetooth
Low Energy libraries: seven conditional local allocations, seven conditional
timer-service origins and two initialized object fields. That review reached
93 inspected original unknowns, with 80 in 46 libraries then unreviewed. The
two object fields are initial values with lifetime limits, not direct constant
arguments. Dynamic provider binding and initialized pool state remain conditions.

Remote allocation-failure logging can fall through to registration, and two
MFi callers ignore allocation status. An independent operand/path audit checks
those cases separately from a BLE success-gated path. Therefore an initialized
allocator range alone cannot exclude all registration paths. Ordinary remote
model and authentication/status Backup writes were also found. No reviewed
path binds them to a selected-language notification; transitive and queued
effects remain unclosed. No global subscriber absence or full regional
preservation is established.

A separate application review follows its five nonconstant synchronous
registration sites. Three load the output of a local queue constructor.
One forwards an input ID while creating a different queue; another forwards
all input arguments and has 44 direct callers. The subsequent
[caller and callback-type review](sessions/20261026-english-app-sync-callers.md)
traces all 44: four fixed IDs, 38 conditional local-allocation origins and two
conditional kernel-allocation origins. The source of reused global values,
teardown, failure diagnostics and transitive callback effects retain limits.
These application sites are outside the original 173 non-application unknown
population and are not added to its totals.

The actual shared Backup notification uses the asynchronous send API. The
reviewed provider appends asynchronous callbacks to a list and stores a
synchronous callback in a different slot. The userspace registration request's
type flag reaches the corresponding kernel registration branch through the
checked copied-body pointer. Both asynchronous dispatch arms consume the
asynchronous list. Therefore equal numeric queue IDs alone do not make a
synchronous registration a direct recipient of that Backup notification.
An independent review checks the pointer link, relocations and list operands.
This is conditional on the reviewed provider and normal structures; forwarding,
re-registration and indirect subscriptions remain separate questions.

Those 80 origins split into 54 synchronous API sites and 26 asynchronous sites
in 23 libraries. The [asynchronous-origin continuation](sessions/20261026-english-async-origins.md)
now inspects all 26 asynchronous sites: 19 conditional native timer-service
origins, three fixed-ID origins, three conditional kernel allocator origins
and one constructor-forwarded object field. None establishes a new actual
shared selected-language subscriber under the reviewed provider assumptions.
The original population now has 119 inspected sites and 54 synchronous numeric
origins still unreviewed. One inspected asynchronous field retains a numeric
forwarding gap; inspection does not mean all lifetime values are resolved.

The Backup provider's asynchronous helper allocates a temporary reply queue,
registers its reply callback and sends the original request to the caller's
destination. The reply callback unregisters, frees the reply and releases the
allocated ID before it can tail-call a user callback. That queue is distinct
from the shared settings notification under the pinned initialized allocator
and expected-provider conditions. Its user callback remains an indirect effect.
An independent operand review checks the allocation-output flow and cleanup.

For the forwarded network-handler field, a finite symbol survey rehashes 244
previously inventoried immediate regular files. Its visible direct constructor
users comprise two SSH initialization paths with a fixed local queue ID that
skip asynchronous registration when their async callback is null, and one
certificate path that constructs, sends and destroys an object without
registering it in that bounded path. This does not cover indirect/dynamic
users, other images, later field mutation or all lifetimes. The source field
therefore remains classified as caller-forwarded. No global subscriber absence
or complete regional preservation follows from these finite results.

The [kernel subscription continuation](sessions/20261026-english-kernel-subscriptions.md)
inspects all 19 direct asynchronous registration relocations in the retained
eight-module inventory. Fifteen use conditional native timer-service reply
origins; two use fixed nonshared IDs; one is a conditional temporary reply queue;
one is the generic shared Backup registration provider wrapper. This kernel
population is separate from the 173 non-app userspace unknowns above.

The shared provider wrapper compares the notification item with the exact item
copied from the client's registration. It invokes the registered client only
after equality. That identifies the provider contract, not the client that
registers selected language or every effect of that client's callback.
Native timer transport and instruction writeback were checked separately from
the earlier userspace ioctl route; allocator conclusions retain initialization,
success, binding and lifetime conditions.

LIRO's table reference is an API export vector. The reviewed path copies its
211 pointer slots into a separate program descriptor and then calls a program
entry. It does not itself pass a selected item or client callback to Backup
registration. An independent byte/relocation audit confirms the copy and entry
boundary. An earlier private note misnamed this vector as an unrelated BSS
array; that label is superseded, with the historical evidence preserved.

The loaded program pointer comes from module-supplied address information;
an optional file-loading path can populate the same location. Its header is
checked, but no exact retained program artifact or actual module parameters
are bound to that pointer. The program can therefore remain an indirect client
of the exported Backup API. The finite startup-file search is not an absence
proof for that program in other directories or components. Full selected-item
effects and regional preservation remain unproved.

A targeted follow-up checks two startup artifacts omitted by the restricted
text search. The boot helper's code actually launches an initialization
executable, rather than merely naming it in usage text. An existing image
directory record supplies a specific next input, but equivalence of its image
path and the runtime launch path remains unverified. The initializer is not
therefore identified as the separate LIRO program.

The [initializer/database continuation](sessions/20261026-english-init-program.md)
then checks that existing executable and its initialization-database library as
inert bytes. A concrete table entry identifies LIRO and selects its special
parameter builder. The normal builder obtains a program address from Backup;
a distinct conditional mode adds a filename/load option. The actual separate
program contents and current parameters are still unbound. The optional file
path does not identify the normal program's source.

Explicit filesystem-table entries support the intended application mount
convention, but the reviewed calls do not prove which mapping was active before
the boot helper executed. Two direct initializer Backup-write calls target
other fixed items; that finite result does not bound all indirect or imported
effects. Three synchronous registrations already had fixed IDs in the original
inventory, so the 119/54/1 non-app population is unchanged. The next input is
the Backup program-address item's initialization/provenance contract in retained
application metadata/code. Full selected-language clients and regional
preservation remain unproved.

The [program-address continuation](sessions/20261026-english-program-address.md)
then establishes the initializer item's real catalog width: eight fixed inline
bytes in both retained same-family catalogs, with identical packaged content.
The native reader uses record metadata for its copy size, and LIRO converts
the supplied value using an external memory base. This neither observes the
current value/base nor maps a packaged number to a firmware file offset.
Generic catalog initialization obtains its live memory pointer from a file
header, with configurable paths/load behavior and explicit successful-provider,
validation and lifetime conditions. Finite kernel/userspace producer scans
identify the known initializer read but establish no item-specific writer or
global absence. The separate program/header bytes and selected-language clients
remain unbound. The next boundary is boot/catalog-header memory provenance.

The shipped files contain separate AP and CP catalog extents. An independent
instruction review confirms that the traced CP transfer request uses the CP
extent as its local buffer; both AP language bytes lie outside that extent.
The CP catalog has a separate English-permission field but no entries in the
selected-language subsystem. This separates those storage objects; it does
not prove the transfer direction, physical-memory mapping, every synchronization
stage or the behavior of CP permission consumers.

The reviewed ordinary AP subsystem-save path copies current live AP values
into a scratch file and then saves it. It persists the subsystem's rows and a
broader file transaction. It is not evidence that writing one logical byte
affects only one physical byte, nor a proof of durable camera behavior.

## Explicit reset differs from ordinary selection

A later focused reset trace, independently checked against instruction words
and relocations, establishes a narrower fact than the withdrawn following-byte
assumption: selected language passes the native mode-1 reset gates, and the
fixed-size helper copies one byte from its validated reset source. That byte is
25 in the shipped CN1 table and 1 in ALLLANG. The English permission item fails
those gates; no following byte is interpreted as its reset value.

This result is conditional on that explicit reset mode being called. The
subsystem reset API forwards the caller's mode; it does not force mode 1.
Nothing here establishes when a running camera invokes a reset, that an
ordinary language selection calls one, or that English would survive an
intentional reset. Other initialization and synchronization stages remain
separate questions.

No patch or executable device command has been prepared. No target support
profile, recovery claim or write gate follows from these findings. The owner's
actual permission values, full installed build identity, reload behavior and
protected-state preservation are unobserved.

Next single offline work package: inspect the existing image initialization
executable identified by the boot helper. Verify its runtime/image path mapping,
then trace LIRO startup parameters and program-image source. Use that evidence
to bind the separate loaded program before following selected-language
subscriptions; do not equate the initializer with that program or guess a
component/address.
Preserve the forwarded network-handler gap, 54 synchronous numeric-origin gaps
and all provider, lifetime and transitive-effect limits. Prepare no write
payload and do not contact the camera.
