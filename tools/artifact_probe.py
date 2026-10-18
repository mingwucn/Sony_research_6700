"""Bounded local header identification, with no extraction or executable loading.

Only explicitly supplied trusted-workspace files are read. Signatures are leads,
not proof of a complete/valid container, target identity, ABI or write eligibility.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Iterable

try:
    from .offline_inventory import InventoryError, KINDS, LABEL, inspect_artifact
except ImportError:
    if __package__:
        raise
    from offline_inventory import InventoryError, KINDS, LABEL, inspect_artifact


def probe_bytes(prefix: bytes, file_size: int) -> dict[str, object]:
    """Classify <=4096 prefix bytes; do not follow offsets or unpack containers."""
    if (not isinstance(prefix, bytes) or type(file_size) is not int or file_size <= 0
            or len(prefix) > 4096 or len(prefix) > file_size):
        raise ValueError("invalid bounded probe input")
    if prefix.startswith(b"\x7fELF"):
        result: dict[str, object] = {"format": "elf_header_candidate", "status": "malformed_header", "abi_verified": False}
        if len(prefix) < 16 or prefix[4] not in (1, 2) or prefix[5] not in (1, 2) or prefix[6] != 1:
            return result
        bits = 32 if prefix[4] == 1 else 64
        order = "little" if prefix[5] == 1 else "big"
        required, size_offset = (52, 40) if bits == 32 else (64, 52)
        if len(prefix) < required or file_size < required:
            return result
        if int.from_bytes(prefix[20:24], order) != 1 or int.from_bytes(prefix[size_offset:size_offset + 2], order) != required:
            return result
        result.update(status="header_only", class_bits=bits, byte_order=order,
                      machine_code=int.from_bytes(prefix[18:20], order))
        return result
    if prefix.startswith(b"MZ"):
        result = {"format": "dos_mz_candidate", "status": "malformed_header"}
        if len(prefix) < 64:
            return result
        offset = int.from_bytes(prefix[60:64], "little")
        if offset < 64 or offset + 24 > file_size:
            return result
        if offset + 24 > len(prefix):
            result["status"] = "header_outside_probe"
        elif prefix[offset:offset + 4] == b"PE\x00\x00":
            result.update(format="pe_header_candidate", status="header_only",
                          machine_code=int.from_bytes(prefix[offset + 4:offset + 6], "little"), abi_verified=False)
        return result
    for magic, minimum, name in ((b"PK\x03\x04", 30, "zip"), (b"PK\x05\x06", 22, "zip"),
                                  (b"\x1f\x8b\x08", 10, "gzip"), (b"\x89UFU\r\n\x1a\n", 8, "sony_ufu"),
                                  (b"UDTRFIRM", 512, "sony_fdat_header")):
        if prefix.startswith(magic):
            return {"format": name + "_signature_candidate",
                    "status": "container_not_validated" if file_size >= minimum else "malformed_header"}
    return {"format": "unknown", "status": "unsupported_opaque"}


def build_report(artifacts: Iterable[tuple[str, Path]], kind: str = "unknown") -> dict[str, object]:
    entries = list(artifacts)
    labels = [label for label, _ in entries]
    if not labels or any(not isinstance(label, str) or not LABEL.fullmatch(label) for label in labels):
        raise InventoryError("provide at least one valid artifact label")
    if len(labels) != len(set(labels)) or kind not in KINDS:
        raise InventoryError("duplicate labels or unrecognized kind")
    records = []
    for label, path in sorted(entries):
        try:
            metadata, prefix = inspect_artifact(Path(path), prefix_limit=4096)
        except InventoryError as exc:
            raise InventoryError(f"{label}: {exc}") from exc
        records.append({"label": label, **metadata, "header": probe_bytes(prefix, metadata["bytes"])})
    return {"schema_version": 1, "tool": "artifact_probe", "tool_version": "0.2.0", "artifact_kind": kind,
            "evidence_class": "offline-tested", "compatibility": "UNVERIFIED", "identity_inferred": False,
            "camera_access_performed": False, "extraction_performed": False, "artifacts": records}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=KINDS, default="unknown")
    parser.add_argument("--artifact", required=True, action="append", metavar="LABEL=PATH")
    args = parser.parse_args(argv)
    try:
        entries = []
        for item in args.artifact:
            label, separator, name = item.partition("=")
            if not separator or not name:
                raise InventoryError("each artifact must be LABEL=PATH")
            entries.append((label, Path(name)))
        report = build_report(entries, args.kind)
    except (InventoryError, ValueError) as exc:
        print(f"probe refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
