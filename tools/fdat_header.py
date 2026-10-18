"""Check decoded FDAT header metadata against a caller-supplied stream size.

Format facts come from the source-only pin in references/sources.lock.json.
This conservative host subset is not a Sony specification or target profile.
No file, crypto, extraction, network or device API exists here.
"""
from __future__ import annotations

import zlib

HEADER_BYTES = 512
MAX_BYTES = 2 * 1024**3


class FDATError(ValueError):
    """Reject unsupported header metadata without reporting raw input bytes."""


def validate_header(header: bytes, decoded_bytes: int) -> dict[str, object]:
    """Validate one exact header and bounded, nonoverlapping declared extents.

    Positions are decoded-FDAT FILE offsets, never package or target addresses.
    The size is a caller claim: neither payload presence nor integrity is tested.
    The accepted subset requires normal user mode and one nonempty U slot. It
    tolerates zero-sized P sentinels and reports uninterpreted padding/counts.
    All 28 slots are inspected regardless of the declared filesystem count.
    """
    if type(header) is not bytes or len(header) != HEADER_BYTES:
        raise FDATError("provide exactly 512 decoded header bytes")
    if type(decoded_bytes) is not int or not HEADER_BYTES <= decoded_bytes <= MAX_BYTES:
        raise FDATError("decoded size outside the host policy")
    if header[:8] != b"UDTRFIRM" or header[12:16] != b"0100":
        raise FDATError("unsupported decoded identifier or version")
    if header[16:17] != b"U" or header[20:21] != b"N":
        raise FDATError("unsupported update mode or LUW flag")
    if header[508:512] != bytes(4):
        raise FDATError("unsupported final reserved field")

    def u32(offset: int) -> int:
        return int.from_bytes(header[offset:offset + 4], "little")

    if (zlib.crc32(header[12:HEADER_BYTES]) & 0xffffffff) != u32(8):
        raise FDATError("decoded header CRC32 mismatch")
    count = u32(56)
    if count > 28:
        raise FDATError("unsupported filesystem-count field")

    def extent(offset: int, size: int) -> dict[str, object]:
        # Empty extents have no bytes to overlap; offset zero represents only
        # an empty declaration. The source writer's P sentinel uses offset 512.
        if size == 0:
            if offset != 0 and not HEADER_BYTES <= offset <= decoded_bytes:
                raise FDATError("empty extent position outside the host policy")
        elif offset < HEADER_BYTES or offset > decoded_bytes or size > decoded_bytes - offset:
            raise FDATError("declared extent outside decoded payload bounds")
        return {"offset": offset, "bytes": size, "end_offset_exclusive": offset + size}

    firmware = extent(u32(48), u32(52))
    slots = []
    padding_nonzero = any(any(header[a:b]) for a, b in
                          [(17, 20), (21, 32), (34, 36), (44, 48), (60, 64)])
    for index in range(28):
        base = 64 + 16 * index
        record = header[base:base + 16]
        if record == bytes(16):
            continue
        if record[:1] not in (b"U", b"P"):
            raise FDATError("unsupported filesystem slot form")
        padding_nonzero |= bool(any(record[1:4]) or any(record[12:16]))
        slots.append({"slot_index": index, "mode": record[:1].decode("ascii"),
                      **extent(u32(base + 4), u32(base + 8))})
    user_slots = [slot for slot in slots if slot["mode"] == "U"]
    if len(user_slots) != 1 or user_slots[0]["bytes"] == 0:
        raise FDATError("host subset requires one nonempty user filesystem slot")

    spans = [{"kind": "firmware", **firmware}] if firmware["bytes"] else []
    spans += [{"kind": "filesystem", **slot} for slot in slots if slot["bytes"]]
    ordered = sorted(spans, key=lambda span: span["offset"])
    for previous, current in zip(ordered, ordered[1:]):
        if previous["end_offset_exclusive"] > current["offset"]:
            raise FDATError("declared nonempty extents overlap")

    return {"schema_version": 1, "tool": "fdat_header_validator", "tool_version": "0.1.0",
            "status": "header_and_spans_only", "address_type": "decoded_fdat_file_offset",
            "header_bytes": HEADER_BYTES, "decoded_bytes": decoded_bytes,
            "decoded_bytes_is_caller_supplied": True,
            "mode": "U", "luw_flag": "N", "model_field_code": u32(36),
            "region_field_code": u32(40), "version_major_code": header[33],
            "version_minor_code": header[32], "declared_filesystem_count": count,
            "observed_slot_count": len(slots), "count_semantics_verified": False,
            "uninterpreted_padding_nonzero": bool(padding_nonzero),
            "firmware": firmware, "filesystem_slots": slots, "nonempty_spans": spans,
            "header_crc32_verified": True, "payload_integrity_verified": False,
            "signature_verified": False, "container_validated": False,
            "identity_inferred": False, "abi_verified": False, "compatibility": "UNVERIFIED",
            "extraction_performed": False, "decryption_performed": False,
            "decompression_performed": False, "execution_performed": False,
            "camera_access_performed": False}
