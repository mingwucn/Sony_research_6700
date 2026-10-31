# Powerful6700 Windows: native-English feasibility review

2026-10-26. Evidence: **source-report**, **static-inference**. Camera commands:
**none**. Requested scope: inspect the supplied Windows package and public code
for a native-English unlock. No upstream program, installer, native payload,
USB query or camera operation was run; no firmware/body input or private package
`.data` contents were opened or uploaded.

## Conclusion

**This version does not implement a camera-language unlock. Further investigation
is plausible; a working English unlock is not established.** Its English-name
option changes four Creative Look labels inside the Simplified Chinese resource.
It does not select a native English locale or lift a language restriction.
The UXC parser and file-reading protocol are useful research leads, but neither
identifies the language-policy consumer or proves complete English resources.

FTP is a separate, concrete **native** feature lead. Its catalog reports
RAW+JPEG uploads and home-network transfers on an upstream body. This review
does not reproduce those tests or certify the owner's installed state. FTP
success supplies no evidence of a corresponding language-unlock switch.

## Sources and provenance

- Repository: [wanghm105/Powerful6700-Windows](https://github.com/wanghm105/Powerful6700-Windows).
- Inspected commit: `4a3e30cad2f608580854755654b12e1d4049c5de`;
  tree: `19935a6233dcedd7dbd5d4838b94d95be1a01047`. Current head was resolved once;
  subsequent source retrieval used this immutable commit.
- **58 selected text files** matched their Git blob SHA-1 and declared byte size;
  SHA-256 identities are retained in
  [the file manifest](../../references/powerful6700-windows-20261026.files.json).
  **46 Python files** were parsed as syntax, never imported or executed.
- The local package's vendored feature engine contains **31 ordinary source/data
  files**, including **27 Python sources**. All 31 match corresponding pinned-tree
  contents after CRLF-to-LF normalization. This is scoped source equivalence;
  it does not establish equivalence of the packaged EXE, embedded Python code,
  native executables or full release archive.
- README advertises 0.3.8, while pinned `src/a6700win/version.py:4` says 0.3.7.
  Commit/content identities govern this review; a displayed release label is
  insufficient to identify an executable.
- Upstream-authored code declares GPL-3.0-only; vendored notices identify
  separately licensed components. No implementation or payload was integrated,
  no project licence was selected, and no proprietary rights were inferred.
  Existing source pins and historical frozen evidence are preserved; the source
  lock gains a distinct reference entry, not a runtime adoption.

## Code findings

| Question | Observed source | Interpretation and limit |
|---|---|---|
| Does the English option change the camera language? | [looknames.py:29](https://github.com/wanghm105/Powerful6700-Windows/blob/4a3e30cad2f608580854755654b12e1d4049c5de/src/a6700win/looknames.py#L29) hardcodes `string_simplifiedchinese_f.uxc`; presets at lines 71–76 choose look names; `apply` at lines 440–451 rewrites selected records. | **Static-inference:** Creative Look labels only. No locale-selection operation is present in this path. Changing the path constant alone would not unlock English. |
| Is the resource format useful? | [uxc.py:65](https://github.com/wanghm105/Powerful6700-Windows/blob/4a3e30cad2f608580854755654b12e1d4049c5de/src/a6700win/uxc.py#L65) parses UXC-v7 records/UTF-8/resource IDs; lines 124–178 rebuild records and indexes. | **Static-inference:** a candidate offline resource comparator can use the documented format after validation. This review did not exercise the parser or decode any actual resource. |
| Are all English files present? | [BREAKTHROUGHS.md:16](https://github.com/wanghm105/Powerful6700-Windows/blob/4a3e30cad2f608580854755654b12e1d4049c5de/docs/BREAKTHROUGHS.md#L16) reports 162 app-directory files and main / `_f` / `_func_j` / `_g` variants with four sample sizes; the implemented label editor targets the Simplified Chinese `_f` file. | **Source-report:** useful inventory lead, without an English filename list, complete string coverage, fonts or rendering evidence. No presence or absence conclusion for complete English is justified. |
| Is language among the unlock features? | [a6700-2.00.json:19](https://github.com/wanghm105/Powerful6700-Windows/blob/4a3e30cad2f608580854755654b12e1d4049c5de/third_party/a6700_unlock/data/a6700-2.00.json#L19): `ftp`, `shutter`, `exposure`, `sound`, `pixel_shift`, `dynamic_active`; the first four are available. | No English feature appears. Source searches found no implemented language mask/current-language/locale-setting API in the bundled feature engine or reviewed Windows runtime. Search scope is the selected source and complete local vendored engine, not all possible firmware code. |
| What does FTP change? | The same catalog describes native FTP menus/switch/settings and upstream positive transfers, with 90 App and 152 WBI edit records. | **Source-report / static-inference:** native functionality rather than a host relay. Records are upstream catalog entries, not independent safe-write approval or exact-owner validation. Cross-power-cycle queue behavior is explicitly incompletely tested. |
| Does `Backup` expose Sony language properties? | `third_party/a6700_unlock/backup.py` and `operations.py` serialize sparse `.a6700backup` feature-state archives. | This is not a generic Sony Backup-property API. No language field, persistence setter or scoped inverse is supplied. |
| Is its inspection ordinary USB identification? | [backend.py:143](https://github.com/wanghm105/Powerful6700-Windows/blob/4a3e30cad2f608580854755654b12e1d4049c5de/third_party/a6700_unlock/usb/backend.py#L143) authenticates service mode; lines 185–203 transfer a request and reader ELF, execute the reader and collect results. `research.py:38–53` and `dump.py:173–177` expose a similar research path. | **Static-inference:** R2 service access, temporary camera-side file I/O and native execution. The absence of persistent feature writes does not make this R1 or authorize running it. Windows wrappers can also install drivers. |
| Do the guards establish language compatibility? | `device-profile.json:3–11` identifies a unified test-scope profile and `pending-unified-selection`; profile checks cover predefined sectors and feature states. | Sparse feature guards do not supply complete program/resource hashes, language-policy evidence or recovery for the owner's mainland body. No new target entry was adopted. |

## Feasibility decision

The preferred hypothesis remains **complete existing English resources with a
narrow language-specific restriction**. To establish it, find and compare the
actual English and Chinese resources for the matching build, then trace the
available-language list, selected-language storage, defaults and every consumer
of a proposed field. The exact internal regional identity remains unverified.
Do not substitute a whole region/destination change or another model's settings.

If resources are complete but a program policy blocks them, a narrow policy
change is a separate possibility after exact-source/control-flow evidence.
If critical English resources are missing, integration or translation becomes a
separate resource project. The existing eight-label rewrite establishes neither
complete translation nor a safe replacement strategy. Upstream reports an actual
partial language-resource write incident; an inverse requires more than saving
a file if service access later fails. No candidate, language field ID, offset,
device command, inverse, recovery claim or EN acceptance result is produced here.

## Verification and retained evidence

Interpreter: **CPython 3.13.12, Windows AMD64**. Exact source audit invocation:

```powershell
$taskScratchRoot=Join-Path ([IO.Path]::GetTempPath()) 'Codex\powerful6700-english-20261026'
python -I -B (Join-Path $taskScratchRoot 'audit_source.py')
```

Exit **0**: 58 Git-blob/size checks, 46 downloaded-source AST parses, 27 local
vendored-source AST parses, 31 normalized local comparisons and catalog/path
assertions passed. These are **source/provenance checks**, not feature behavior
tests; behavioral tests run: **0**. Historical suites were not rerun because no
runtime implementation changed. A transport-added trailing newline was removed
only where doing so recovered the exact predeclared Git blob. No upstream code
was executed to verify it.

Delivery validation used `python -I -B (Join-Path $taskScratchRoot
'validate_delivery.py')`, exit **0**, on the same interpreter. JSON/manifest
hashes, prior lock entries, held camera state, retained private evidence and local
report links passed. `git -c core.safecrlf=false diff --check` exited **0**.
The delivery validator is retained with the private audit evidence.

The authored audit script, full tree metadata, raw audit log, local file hashes
and private bundle details are retained under the ignored private session folder.
Disposable downloaded source and staging scratch remain in the task-owned OS
temporary folder `Codex/powerful6700-english-20261026`. Ownership of all 63 files,
the absolute target outside the workspace, absence of reparse points and durable
evidence were checked. Automatic approval review rejected deletion with
**blocked by policy**, without a more specific reason; cleanup did not occur.
The public manifest contains no firmware, body dump, credentials or payload bytes.
No camera commands, device reads/writes, firmware processing or external
submissions occurred. The existing camera-contact hold remains in force.

## Next single work package

**EN-101: establish matching alpha6700 2.00 English-resource coverage and the
locale-policy map.** Start from legitimately available exact-build resource
inputs and an app-directory inventory. Compare resource IDs across main, `_f`,
`_func_j` and `_g`, including critical dialogs/fonts, and trace language-list and
selected-language consumers. Deliver one coverage table, one selector/persistence
map and a go/no-go decision for a narrow unlock. The current package contains
code and manifests, not the required resource set or selector evidence. If these
inputs cannot be obtained within approved offline scope, record that precise
missing input; no extra synthetic preparation framework or device attempt can
substitute for it.
