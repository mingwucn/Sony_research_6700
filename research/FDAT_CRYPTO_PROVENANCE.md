# RA-003: crypto dependency and public-constant provenance

Reviewed 2026-10-18 on `codex/ra003-crypto-provenance`, basis
`acede7703fd0fde539047c1c4e8cf7861bbbf94e`. English and native Wi-Fi FTP remain
primary. Camera commands: **none**. No actual firmware bytes were read here.

## Pinned host dependency

The private research environment uses **pycryptodomex 3.24.1**, only for the AES
ECB/CBC primitive API. Its [version metadata](https://pypi.org/pypi/pycryptodomex/3.24.1/json)
and locally verified artifact are pinned in [sources.lock.json](../references/sources.lock.json).

| Field | Recorded value |
|---|---|
| Wheel | `pycryptodomex-3.24.1-cp37-abi3-win_amd64.whl` |
| Bytes | 1,825,955 |
| SHA-256 | `82eb0dd8a95be97f03527b108ee49f9b86a7c534fa47fa7a510be3eab8ea9acd` |
| Wheel METADATA SHA-256 | `e23b7012d6be70d623a1ebd73d716b618cda40662afc506fe3c9e32b05c25dbe` |
| Observed source tag | `v3.24.1`, commit `59351474682db6648825f17b11112d6821d66cb9` |
| Namespace/API | `Cryptodome.Cipher.AES`, explicit ECB/CBC construction and decrypt |
| Declared Python dependencies | None; `Requires-Dist` absent |

The source tag is a provenance reference, not a reproduced build. One direct
wheel GET completed with no redirect or retry. All 351 hashed RECORD entries
matched; the archive has 352 entries, 4,264,914 uncompressed bytes and 42 AMD64
native modules. No absolute/traversal, duplicate, encrypted or symlink entries
were accepted. These checks establish the captured artifact's internal identity,
not a complete security audit or source-to-binary equivalence.

The exact wheel `Requires-Python` is
`>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*`.
The cp37/abi3/Windows AMD64 tag and actual tests below cover the recorded standard
CPython 3.13.12 Windows AMD64 host only. Do not infer support for every interpreter
allowed by the metadata string.

The [project licence](https://www.pycryptodome.org/src/license) and captured wheel
LICENSE/AUTHORS notices describe inherited public-domain code and BSD-2-Clause
contributions. Applicable notices must accompany any later redistribution; this
package does not redistribute the wheel. No firmware rights follow from that
licence. The [installation documentation](https://www.pycryptodome.org/src/installation)
says `pycryptodomex`/`Cryptodome` releases stop beginning with version 4.0. This
pin is deliberate for a bounded research experiment, with no continuing-fix or
generally-latest claim. A future namespace/version change requires review.

## Actual private runtime qualification

A new private venv, without system-site access, installed only the verified wheel
using `--isolated --no-index --no-deps --no-compile`. Tests ran under its Python
with `-I -B`, excluding user-site/PYTHONPATH/current-directory package shadowing.
Eight authored tests passed, exit **0**, unittest **0.093 seconds**:

- Pinned version and import location inside the isolated venv.
- [NIST SP 800-38A](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf)
  F.1.2 AES-128 ECB and F.2.6 AES-256 CBC decrypt known answers.
- CBC state continuity across uneven aligned chunks; fresh state between trials.
- Wrong IV and incorrect per-chunk resets differ from the expected plaintext.
- Portable AES with `use_aesni=False` returns the same known answers.
- Invalid key/IV lengths and unaligned data are rejected with fresh objects.

Only public test vectors were loaded. These checks execute third-party crypto
Python/native code; no fwtool module, firmware or operational key constant was
loaded. The venv is dependency isolation, not an OS sandbox. Default AES backend
selection was tested but its hardware choice was not instrumented. Portable AES
was requested explicitly in a separate case. This is not FIPS certification or
proof of a Sony decoder, signature verification, payload integrity or hardware.

The four reviewed AES/ECB/CBC/raw-interface texts load packaged native libraries
and may probe CPU features. The interface tries optional CFFI then ctypes; the
private environment supplied no CFFI. `platform.architecture()` prevents a broad
claim that library loading can never invoke a helper subprocess. Full transitive
source/native-code audit remains outside these four source excerpts.

## Public constants: identity, origin and scope

One direct GET acquired `fwtool/sony/constants.py` from the already pinned
fwtool fork commit `3955d7890fc38daf942bb52827599bfe35de4a14`, **privately**:

- 2,312 bytes; Git blob `a0908936fe3eb938ca25ca070eb49668e4143109` agrees with
  the earlier fixed recursive tree.
- SHA-256 `f9ff02a3889b587cd5bad5f4362fb73fee2f8f3591fc3ed6003eb8ac92d0622a`.
- AST-only inspection: 15 assignments, 13 byte literals and two earlier-name
  aliases; no imports or executable call expressions. It was never imported.
- The source's CBC path uses a 16-byte common AES constant and a 32-byte selected
  CBC-family constant. No operational constant value enters project reports or Git.

The fixed repository's MIT notice is a publication/reuse claim for its software,
not proof of Sony authorship/permission for every underlying value. The
[path history](https://api.github.com/repos/DavidBuchanan314/fwtool.py/commits?sha=3955d7890fc38daf942bb52827599bfe35de4a14&path=fwtool%2Fsony%2Fconstants.py&per_page=100)
has 17 commits. The 2026 additions name family support but do not provide an
independently verified derivation account. The only licence/notice-named path
in the fixed tree is LICENSE.txt; its history records the 2015 MIT addition.
Unknown origin is not proof that numeric constants are copyrighted, secret or
unlawful, and does not make separate Sony permission the only research route.

A captured [author comment](https://github.com/ma1co/fwtool.py/pull/52#issuecomment-5625960817)
does list ILCE-6700 among tested models, resolving the earlier missing local
comment citation. It supplies no exact 2.00/mainland package hash. A separate
[author explanation](https://github.com/ma1co/fwtool.py/pull/52#issuecomment-5634485055)
says the initial CXD90057 selection was k8 and some firmware uses k0, with a
derivation-code index. This is source-report, not independent derivation or a
unique selection for this package. Comments are mutable; their update times and
body hashes are retained privately. Operational values are excluded from reports.

The [narrow statutory assessment](FDAT_DECODING_PLAN.md) remains the documented
basis for necessary private format study; accepted Sony contract interaction is
still unresolved. This source audit is sufficient to prepare the scoped private
experiment without inventing another generic permission-only blocker. It does
not clear redistribution, unrelated component copies, modification or device
work. Keep source notices, operational constants and any decoding implementation
private; no working bypass implementation is published here.

## Decision and next experiment

Predeclare **CXD90057_k8 as one experimental hypothesis**, based on the source's
initial-selection report and ILCE-6700 testing claim. It is not an exact-package
key finding, processor/ABI proof, profile entry or target address. Stop after
that one trial; do not adopt the upstream automatic key loop or fallback on
failure. Shared first-stage ECB magic cannot distinguish CBC variants.

Preparation must independently test the authored envelope/header-trial code.
Retain only the first 1,024 FDAT bytes and 16 IV bytes at FDAT-relative
`length - 272`, in the same journaled whole-file identity/hash-checked read.
The first 512 physical bytes use ECB; CBC starts at physical 512 with fresh IV
state. The decoded header occupies physical plaintext `[4:516]` and crosses the
cipher boundary. Validate the full first-block checksum, length 512..1020,
nonterminal flag, header fields/final-zero predicate and CRC before reporting
metadata. An omitted 256-byte tail remains unauthenticated/uninterpreted.

A header-only trial cannot measure full decoded size. Declared component spans
must stay **unverified**; do not feed a ciphertext-derived estimate to the extent
validator and call bounds verified. Success authenticates neither the candidate,
container nor body. A negative result establishes no English/FTP absence.

Next single package: **RA-003: implement, synthetically qualify and run one
bounded private FDAT header trial for the predeclared CXD90057_k8 hypothesis**.
No trial was run here. Exact-body/build/resource correspondence and verified
rollback/recovery remain absent; no feature or device-write gate passed.


## Later bounded-header continuation (2026-10-18)

The [one-shot header result](FDAT_HEADER_TRIAL.md) and
[session commands/results](sessions/20261018-RA-003-header-trial.md) supersede
the preceding next-step statements. One predeclared hypothesis passed first-block
envelope/header predicates, exit 0; 45 corrected synthetic cases passed. No full-stream
decoded length, component bounds, resources/backend or body correspondence is proved.
Earlier opaque-prefix/no-decoding observations remain historical; no child files,
upstream execution, camera action or feature/write gate occurred here. Contract
interaction, constants derivation and verified rollback/recovery remain unresolved.
Next single package: **RA-003: assess and document the necessary private full-stream format-study scope, implement and synthetically qualify bounded FDAT stream validation, then measure decoded length and SHA-256 through bounded memory without retaining decoded-stream or component files**.
