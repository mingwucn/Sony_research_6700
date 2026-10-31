"""Read UXC-v7 resource records without changing or executing any input.

Field layout is a format-study reference from the pinned Powerful6700 source.
Only UTF-8, kind-8, bounded indexed string resources are accepted here.
"""
from dataclasses import dataclass
import struct

class UxcError(ValueError):
    pass

@dataclass(frozen=True)
class UxcResource:
    group: int
    slot_count: int
    texts: dict[int, str]

def parse_uxc(data: bytes, max_bytes: int = 8*1024*1024) -> UxcResource:
    if type(max_bytes) is not int or max_bytes < 20:
        raise UxcError("invalid resource byte budget")
    if type(data) is not bytes or not 20 <= len(data) <= max_bytes or len(data)%4:
        raise UxcError("invalid resource size")
    if data[:8] != b"uxc\x07\0\0\0\0":
        raise UxcError("unsupported resource magic")
    kind, group, descriptor = struct.unpack_from("<HHI",data,8)
    count = descriptor & 8191
    if kind != 8 or group > 0x7ff or not count or descriptor != (count | (((count+1)&~1)<<12)):
        raise UxcError("unsupported index descriptor")
    base = (16+2*count+3)&~3
    if base >= len(data):
        raise UxcError("index exceeds resource")
    records = {}
    ranges = []
    for index in range(count):
        pointer = struct.unpack_from("<H",data,16+2*index)[0]
        if pointer == 65535:
            continue
        at = base + 4*pointer
        rid = 0x02000000 | ((group<<13)+index)
        if at+5 > len(data):
            raise UxcError("record outside resource")
        tag = struct.unpack_from("<I",data,at)[0]
        if tag != (0x1e000000 | (rid & 0xffffff)):
            raise UxcError("index and record id disagree")
        end = data.find(b"\0",at+4)
        if end < 0 or ((end+4)&~3) > len(data):
            raise UxcError("unterminated or unpadded record")
        try:
            text = data[at+4:end].decode("utf-8",errors="strict")
        except UnicodeDecodeError as exc:
            raise UxcError("invalid UTF-8") from exc
        ranges.append((at,(end+4)&~3))
        records[rid] = text
    ranges.sort()
    if any(a[1] > b[0] for a,b in zip(ranges,ranges[1:])):
        raise UxcError("overlapping records")
    return UxcResource(group,count,records)
