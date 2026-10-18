"""Read a local UFU chunk directory as data, without extracting any contents.

The reviewed reference establishes only magic + size/type/payload framing.
This tool checks that interpretation against file bounds and an expected hash;
it does not authenticate a Sony container or validate undocumented semantics.
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
from typing import BinaryIO

try:
    from .artifact_probe import probe_bytes
except ImportError:
    if __package__:
        raise
    from artifact_probe import probe_bytes

MAGIC = b"\x89UFU\r\n\x1a\n"
MAX_BYTES = 2 * 1024**3
MAX_CHUNKS = 4096
READ_BYTES = 1024**2
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class UFUError(ValueError):
    """Refuse ambiguous, changed or unsupported input without revealing its path."""


def index_stream(stream: BinaryIO, file_size: int, expected_sha256: str,
                 *, max_chunks: int = MAX_CHUNKS, probe_fdat: bool = False) -> dict[str, object]:
    """Consume one bounded stream, optionally classifying an in-memory prefix.

    Offsets are zero-based PACKAGE FILE offsets, never process/flash addresses.
    Exact EOF coverage means only that the reviewed framing spans this stream.
    No checksum, signature, end-marker or chunk-order semantics are inferred.
    With probe_fdat, retain at most 4096 bytes from a single FDAT only until
    classification. No prefix bytes or component contents enter the result.
    """
    if type(file_size) is not int or not len(MAGIC) <= file_size <= MAX_BYTES:
        raise UFUError("file size outside the bounded inventory policy")
    if not isinstance(expected_sha256, str) or not SHA256.fullmatch(expected_sha256):
        raise UFUError("provide an exact lowercase SHA-256")
    if type(max_chunks) is not int or not 1 <= max_chunks <= MAX_CHUNKS:
        raise UFUError("invalid chunk-count policy")
    if type(probe_fdat) is not bool:
        raise UFUError("invalid FDAT probe policy")
    digest = hashlib.sha256()

    def read_exact(length: int) -> bytes:
        # Used only for eight-byte framing fields, never a declared payload.
        value = bytearray()
        while len(value) < length:
            part = stream.read(length - len(value))
            if not part:
                raise UFUError("truncated framing field")
            value.extend(part)
            digest.update(part)
        return bytes(value)

    if read_exact(8) != MAGIC:
        raise UFUError("unsupported UFU identifier")
    offset = 8
    chunks = []
    fdat_seen = False
    fdat_prefix = bytearray()
    while offset < file_size:
        if len(chunks) >= max_chunks:
            raise UFUError("chunk-count limit reached")
        if file_size - offset < 8:
            raise UFUError("unsupported trailing bytes or truncated chunk header")
        header = read_exact(8)
        size = int.from_bytes(header[:4], "big")
        tag = header[4:]
        payload_offset = offset + 8
        if size > file_size - payload_offset:
            raise UFUError("declared chunk extends beyond the file")
        capture_prefix = probe_fdat and tag == b"FDAT"
        if capture_prefix:
            if fdat_seen:
                raise UFUError("FDAT probe requires an unambiguous single span")
            fdat_seen = True
        chunks.append({"index": len(chunks), "type_hex": tag.hex(),
                       "type_ascii": tag.decode("ascii") if all(32 <= b < 127 for b in tag) else None,
                       "header_file_offset": offset, "payload_file_offset": payload_offset,
                       "payload_bytes": size, "end_file_offset_exclusive": payload_offset + size})
        remaining = size
        while remaining:
            part = stream.read(min(remaining, READ_BYTES))
            if not part:
                raise UFUError("truncated chunk payload")
            digest.update(part)
            if capture_prefix and len(fdat_prefix) < 4096:
                fdat_prefix.extend(part[:4096 - len(fdat_prefix)])
            remaining -= len(part)
        offset = payload_offset + size  # Eight-byte header guarantees progress even for size zero.
    if stream.read(1):
        raise UFUError("input exceeds the declared file size")
    actual_sha256 = digest.hexdigest()
    if actual_sha256 != expected_sha256:
        raise UFUError("source SHA-256 mismatch; no directory is valid")
    fdat = [chunk for chunk in chunks if chunk["type_hex"] == "46444154"]
    fdat_status = ("absent" if not fdat else "ambiguous_multiple" if len(fdat) > 1
                   else "empty" if fdat[0]["payload_bytes"] == 0 else "single_bounded_span")
    result = {"schema_version": 1, "tool": "ufu_inventory", "tool_version": "0.2.0",
            "evidence_class": "offline-tested", "bytes": file_size, "sha256": actual_sha256,
            "format": "sony_ufu_framing_candidate", "status": "framing_spans_entire_file",
            "address_type": "package_file_offset", "chunk_count": len(chunks), "chunks": chunks,
            "fdat_status": fdat_status, "compatibility": "UNVERIFIED",
            "container_validated": False, "checksums_verified": False, "signature_verified": False,
            "chunk_semantics_verified": False, "identity_inferred": False,
            "extraction_performed": False, "decompression_performed": False,
            "decryption_performed": False, "execution_performed": False,
            "camera_access_performed": False}
    if probe_fdat:
        # Classify only after the entire original file and its hash passed.
        result["fdat_probe"] = {"prefix_limit": 4096, "prefix_bytes_observed": len(fdat_prefix),
                                "raw_prefix_output": False,
                                "candidate": probe_bytes(bytes(fdat_prefix), fdat[0]["payload_bytes"])
                                if fdat_status == "single_bounded_span" else None,
                                "status": "signature_only" if fdat_status == "single_bounded_span" else fdat_status}
    return result


def _stamp(info: os.stat_result, *, ctime: bool = True) -> tuple[int, ...]:
    common = (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns)
    return common + (info.st_ctime_ns,) if ctime else common


def inspect_file(path: Path, expected_sha256: str, expected_bytes: int,
                 *, probe_fdat: bool = False) -> dict[str, object]:
    """Read a regular file in a trusted workspace, detecting observable changes.

    Intermediate directories must be trusted, as for offline_inventory. These
    stat checks are not an adversarial-filesystem sandbox or a snapshot guarantee.
    """
    if type(expected_bytes) is not int or not 8 <= expected_bytes <= MAX_BYTES:
        raise UFUError("invalid expected byte count")
    fd = None
    try:
        named_before = path.lstat()
        if not stat.S_ISREG(named_before.st_mode):
            raise UFUError("input must be an ordinary regular file")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
        fd = os.open(path, flags)
        before = os.fstat(fd)
        if (not stat.S_ISREG(before.st_mode) or before.st_size != expected_bytes
                or _stamp(before, ctime=False) != _stamp(named_before, ctime=False)):
            raise UFUError("source identity or size changed before reading")
        # Keep descriptor ownership in finally, including parser failures.
        with os.fdopen(fd, "rb", closefd=False) as stream:
            result = index_stream(stream, before.st_size, expected_sha256, probe_fdat=probe_fdat)
        after = os.fstat(fd)
        named_after = path.lstat()
        if (not stat.S_ISREG(named_after.st_mode)
                or _stamp(before) != _stamp(after)
                or _stamp(named_before) != _stamp(named_after)
                or _stamp(after, ctime=False) != _stamp(named_after, ctime=False)):
            raise UFUError("source changed during reading; no directory is valid")
        return result
    except OSError as exc:
        raise UFUError("input is missing, inaccessible or changed") from exc
    finally:
        if fd is not None:
            os.close(fd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--expect-sha256", required=True)
    parser.add_argument("--expect-bytes", type=int, required=True)
    parser.add_argument("--probe-fdat", action="store_true",
                        help="classify at most 4096 FDAT prefix bytes in memory; never output the bytes")
    args = parser.parse_args(argv)
    try:
        result = inspect_file(args.input, args.expect_sha256, args.expect_bytes,
                              probe_fdat=args.probe_fdat)
    except UFUError as exc:
        print(f"UFU inventory refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
