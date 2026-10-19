# RA-003: explicit historical source ancestry

2026-10-19. Branch `codex/ra003-source-ancestry`, starting HEAD `885d755`, tracked tree clean. Evidence: **static-inference**, **offline-tested**. Previous goal turn: **progress** (saved diagnostic refusal identified the source namespace defect). Current goal turn: **progress** (isolated successor and relevant invented qualification).

The isolated successor now maps each of 29 current role/bootstrap source paths to one explicit historical seal key. It preserves nested paths and rejects basename/prefix fallback. The map binds the exact historical seal bytes and canonical parsed seal, all current paths, original hashes and current hashes. All rows must be present and unique under case folding; relative traversal and alternate ancestors refuse. The existing three replacement checks still require exact reviewed old/new identities. The other 26 sources must retain their original hashes. The effective map remains keyed by current repository-relative paths for the later loader.

The original gate, seal, cache, metadata and refused diagnostic remain unchanged. No target address or firmware bytes are involved. The ancestry map is private source/provenance metadata, never a target support profile or activation allowlist.

## Qualification and independent review

**35/35 tests passed**, zero skipped, exit **0**, **0.638s suite / 0.982064s wrapper**. Five source/fixture/map pins match before and after and have retained snapshots. Invented cases cover the complete pure bundle/cache graph (47 source buffers), all 29 migrated paths, three bootstrap files, nested distinct files with the same basename, missing/extra roles, changed old/new hashes, raw/parsed seal substitutions, wrong ancestors, path traversal, duplicate/casefold aliases, overlay changes and authority promotion.

Positive bundle tests explicitly substitute invented authority/map fixtures; they do not establish production fixed-policy acceptance or execute cached sources. The two frozen-production checks only verify map/source identities and preservation of the predecessor. Historical 232/253/81-case qualifications were not rerun or relabelled as this successor's qualification. Full gate/entry/child/native composition remains pending.

The first development run had **34 passes and one error**, exit **1**, **0.628s**. It exposed a second mismatch: after historical lookup succeeded, cache validation still expected flat bootstrap paths. Independent gate review found the same issue. The initial gate and log were preserved. The corrected cache check uses the exact frozen ancestry row's current path for each bootstrap source. Second development run: **35 passes**, zero skips, exit **0**, **0.612s**. No acceptance threshold or historical evidence changed.

Two independent source reviews cover the corrected component. The gate review closed the bootstrap finding; the runtime review assessed mapping, source identity and invented-test boundaries. Review is source-only, not independent execution or a camera result. `preparation.json` deliberately records the initial revision; a separate `revision-history.json` distinguishes it from the corrected qualification.

Identity anchors:

- Predecessor gate: `faa196abe6dbea4ef141deab810558f8f0e03fdda9bc0b9d9c4b6acda2f25172`.
- Initial successor: `c088c8bec65b928c9926cc39d1b7e55e0edec64ebacf54266ac221a40f5ebd94`.
- Corrected successor: `c938fefe599860764e908feae8ad9718e6acca65b155999f807e96cfc6a3ae64`.
- Frozen ancestry: `8c424160ee6567f436e8259d986092b414be8569eff927f4d6d109ddf7c58f5c`.
- Qualification result: `349fb4766eaa14adc9dc1cf17d43c86fe76d1851d3c18646232ce729cdafb796`.

## Commands and results

Host: Windows AMD64, CPython **3.13.12**, interpreter `C:\ProgramData\miniconda3\python.exe`. Commands below are host-only; source preparation processes only already-saved structured source metadata.

```powershell
git status --short
git branch --show-current
git switch -c codex/ra003-source-ancestry
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-operational-reconciliation/prepare_ancestry.py
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-source-ancestry/test_ancestry.py
C:\ProgramData\miniconda3\python.exe -I -S -B -X utf8 private/sessions/20261019-RA-003-source-ancestry/qualify.py
git diff --check
```

Branch and preparation: exit **0**. The development test command ran twice with distinct retained logs and source revision identities, exits **1**, then **0**, as above. The qualification wrapper launched exactly one child with the same isolated flags, `qualify.py child`, and a 30-second deadline; exit **0**, no timeout. Exact argv/cwd and source snapshots are retained privately. Source/hash/log/JSON verification and final diff checks pass. An initial documentation read referenced nonexistent `parent_evidence_cases.py`; the authoritative test file is `outer/test_parent_evidence.py`; no implementation depended on the missing path.

Changed tracked files: this report, `docs/BACKLOG.md`, `docs/FEATURE_PROGRESS.md`, `docs/CODEX_HANDOFF.md`, and `research/STATE.json`. Private source, map, test/result/log/review material remains ignored. Internal session/feature notes were updated after byte-preserving backups.

Camera commands: **none**. No network, private upload, native/dependency execution, firmware/constants/saved-prefix read, upstream launcher, driver change or camera action. Only saved ordinary metadata and authored code were read; paths recorded inside metadata were not followed to target inputs. Native English and native Wi-Fi FTP remain priorities but unsupported here. No complete operational bundle, inspection act, recovery or device-write gate passed. Goal remains active.

## Next single work package

**RA-003: bind the reviewed ancestry successor and its qualification into a versioned gate/entry source chain, then qualify the complete invented parent/child composition before a fresh saved-metadata diagnostic.** Preserve historical qualification identities and avoid a self-containing source/result hash cycle. Complete binding-plan recomputation, saved-basis semantic validation and activity-specific scope/rights/review/seal remain subsequent prerequisites before any real metadata act.
