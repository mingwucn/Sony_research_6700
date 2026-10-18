"""Hash explicitly supplied local artifacts. No USB, network or camera writes.

The output records user-supplied identity, not verified camera compatibility.
Redirect stdout only to a NEW private file, never over an input artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Iterable

TOOL_VERSION = "0.1.0"
LABEL = re.compile(r"[a-z][a-z0-9_-]{0,47}\Z")
MODEL = re.compile(r"[A-Z0-9-]{1,32}\Z")
FIRMWARE = re.compile(r"[A-Za-z0-9._-]{1,32}\Z")
KINDS = ("unknown", "body-dump", "official-package", "synthetic")


class InventoryError(ValueError):
    """An input could not be inventoried without ambiguity."""


def _fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_size,
            info.st_mtime_ns, info.st_ctime_ns)


def hash_artifact(path: Path) -> dict[str, object]:
    """Read one nonempty regular file, rejecting detectable concurrent changes.

    No directory recursion is performed. Intermediate directories must belong
    to a trusted local workspace; this is not an adversarial-filesystem sandbox.
    """
    fd = None
    try:
        initial = path.lstat()
        if not stat.S_ISREG(initial.st_mode):
            raise InventoryError("input must be a regular file, not a symlink or device")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        fd = os.open(path, flags)
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or _fingerprint(initial) != _fingerprint(before):
            raise InventoryError("input changed before reading")
        digest = hashlib.sha256()
        length = 0
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            length += len(chunk)
            digest.update(chunk)
        after = os.fstat(fd)
        named_after = path.lstat()
        if (_fingerprint(before) != _fingerprint(after)
                or _fingerprint(after) != _fingerprint(named_after)
                or not stat.S_ISREG(named_after.st_mode)
                or length != before.st_size):
            raise InventoryError("input changed during reading; no inventory is valid")
        if length == 0:
            raise InventoryError("empty artifacts are not accepted")
        return {"bytes": length, "sha256": digest.hexdigest()}
    except OSError as exc:
        # Do not include local paths or OS error strings in shareable output.
        raise InventoryError("artifact is missing, inaccessible, or changed") from exc
    finally:
        if fd is not None:
            os.close(fd)


def build_inventory(model: str, firmware: str, alias: str,
                    artifacts: Iterable[tuple[str, Path]],
                    kind: str = "unknown") -> dict[str, object]:
    if not MODEL.fullmatch(model):
        raise InventoryError("model must be a short uppercase model identifier")
    if not FIRMWARE.fullmatch(firmware):
        raise InventoryError("firmware must be a short identifier or UNKNOWN")
    if not LABEL.fullmatch(alias):
        raise InventoryError("alias must be a non-identifying lowercase label")
    if kind not in KINDS:
        raise InventoryError("unrecognized artifact kind")
    entries = list(artifacts)
    labels = [label for label, _ in entries]
    if not labels or any(not LABEL.fullmatch(label) for label in labels):
        raise InventoryError("provide at least one valid artifact label")
    if len(set(labels)) != len(labels):
        raise InventoryError("duplicate artifact labels are not accepted")
    records = []
    for label, path in sorted(entries):
        try:
            record = hash_artifact(Path(path))
        except InventoryError as exc:
            raise InventoryError(f"{label}: {exc}") from exc
        records.append({"label": label, **record})
    return {
        "schema_version": 1,
        "tool": "offline_inventory",
        "tool_version": TOOL_VERSION,
        "identity": {"model": model, "firmware": firmware, "body_alias": alias,
                     "source": "user-supplied; not read from camera"},
        "artifact_kind": kind,
        "camera_access_performed": False,
        "compatibility": "UNVERIFIED",
        "artifacts": records,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--firmware", required=True)
    parser.add_argument("--alias", required=True)
    parser.add_argument("--kind", choices=KINDS, default="unknown")
    parser.add_argument("--artifact", action="append", required=True,
                        metavar="LABEL=PATH")
    args = parser.parse_args(argv)
    try:
        artifacts = []
        for item in args.artifact:
            label, separator, path = item.partition("=")
            if not separator or not path:
                raise InventoryError("each artifact must be LABEL=PATH")
            artifacts.append((label, Path(path)))
        report = build_inventory(args.model, args.firmware, args.alias,
                                 artifacts, args.kind)
    except InventoryError as exc:
        print(f"inventory refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
