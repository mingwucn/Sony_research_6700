"""Bounded classic-ext2 inspection over an explicitly supplied read callback.

This module opens no paths, mounts nothing, and implements no write operation.
It is a conservative content reader, not a complete filesystem checker.
"""
from __future__ import annotations

from dataclasses import dataclass
import struct
from typing import Callable


class Ext2Error(ValueError):
    """The input is unsupported, malformed, or exceeds the inspection budget."""


@dataclass(frozen=True)
class Ext2Inode:
    number: int
    mode: int
    size: int
    flags: int
    blocks: tuple[int, ...]

    @property
    def kind(self) -> str:
        return {0x8000: "file", 0x4000: "directory", 0xA000: "symlink"}.get(
            self.mode & 0xF000, "special"
        )


@dataclass(frozen=True)
class Ext2DirEntry:
    name: str
    inode: int
    file_type: int


class Ext2Reader:
    """Read classic block-mapped ext2 with a finite file/directory size budget.

    ``read_at(offset, length)`` must return exactly the requested image bytes.
    All offsets passed to it are checked against ``image_size`` first. Symlinks
    are never followed. Classic direct and all three indirect levels are supported.
    Names use UTF-8 with surrogateescape, preserving non-UTF-8 filename bytes.
    """

    def __init__(
        self,
        read_at: Callable[[int, int], bytes],
        image_size: int,
        *,
        max_read_bytes: int = 128 * 1024 * 1024,
        max_directory_bytes: int = 16 * 1024 * 1024,
    ) -> None:
        if not callable(read_at):
            raise Ext2Error("read_at must be callable")
        for name, value in (("image_size", image_size),
                            ("max_read_bytes", max_read_bytes),
                            ("max_directory_bytes", max_directory_bytes)):
            if type(value) is not int or value <= 0:
                raise Ext2Error(name + " must be a positive integer")
        self._read_at = read_at
        self.image_size = image_size
        self.max_read_bytes = max_read_bytes
        self.max_directory_bytes = min(max_directory_bytes, max_read_bytes)
        sb = self._read(1024, 1024)
        if self._u16(sb, 56) != 0xEF53:
            raise Ext2Error("not an ext superblock")
        self.revision = self._u32(sb, 76)
        if self.revision not in (0, 1):
            raise Ext2Error("unsupported superblock revision")
        log_size = self._u32(sb, 24)
        if log_size > 2:
            raise Ext2Error("unsupported block size")
        self.block_size = 1024 << log_size
        if struct.unpack_from("<i", sb, 28)[0] != log_size:
            raise Ext2Error("fragments with a different size are unsupported")
        self.blocks_count = self._u32(sb, 4)
        self.inodes_count = self._u32(sb, 0)
        self.first_data_block = self._u32(sb, 20)
        self.blocks_per_group = self._u32(sb, 32)
        self.inodes_per_group = self._u32(sb, 40)
        if self.first_data_block != (1 if self.block_size == 1024 else 0):
            raise Ext2Error("invalid first data block")
        if not self.blocks_count or self.blocks_count <= self.first_data_block:
            raise Ext2Error("invalid block count")
        if self.blocks_count * self.block_size > self.image_size:
            raise Ext2Error("filesystem exceeds supplied image")
        if not 1 <= self.blocks_per_group <= self.block_size * 8:
            raise Ext2Error("invalid blocks per group")
        if self._u32(sb, 36) != self.blocks_per_group:
            raise Ext2Error("fragment groups are unsupported")
        if not 1 <= self.inodes_per_group <= self.block_size * 8:
            raise Ext2Error("invalid inodes per group")
        self.group_count = self._ceil(
            self.blocks_count - self.first_data_block, self.blocks_per_group
        )
        if not 1 <= self.inodes_count <= self.group_count * self.inodes_per_group:
            raise Ext2Error("invalid inode count")
        self.inode_size = 128 if self.revision == 0 else self._u16(sb, 88)
        if (self.inode_size < 128 or self.inode_size > self.block_size
                or self.inode_size & (self.inode_size - 1)):
            raise Ext2Error("unsupported inode size")
        self.feature_compat = self._u32(sb, 92) if self.revision else 0
        self.feature_incompat = self._u32(sb, 96) if self.revision else 0
        self.feature_ro_compat = self._u32(sb, 100) if self.revision else 0
        if self.feature_incompat & ~0x2:
            raise Ext2Error("unsupported incompat features (only FILETYPE supported)")
        if self.feature_ro_compat & ~0x3:
            raise Ext2Error("unsupported read-only-compatible features")
        if self.feature_compat & 0x4:
            raise Ext2Error("journaled filesystems are unsupported")
        descriptor_size = self._u16(sb, 254) if self.revision else 0
        if descriptor_size not in (0, 32):
            raise Ext2Error("unsupported group descriptor size")
        first_inode = self._u32(sb, 84) if self.revision else 11
        if not 11 <= first_inode <= self.inodes_count + 1:
            raise Ext2Error("invalid first nonreserved inode")
        self._gdt_offset = (self.first_data_block + 1) * self.block_size
        self._check_range(self._gdt_offset, self.group_count * 32)
        if self._gdt_offset + self.group_count * 32 > self.blocks_count * self.block_size:
            raise Ext2Error("group descriptor table exceeds filesystem")
        self._group_tables: dict[int, int] = {}

    @staticmethod
    def _u16(raw: bytes, offset: int) -> int:
        return struct.unpack_from("<H", raw, offset)[0]

    @staticmethod
    def _u32(raw: bytes, offset: int) -> int:
        return struct.unpack_from("<I", raw, offset)[0]

    @staticmethod
    def _ceil(value: int, divisor: int) -> int:
        return (value + divisor - 1) // divisor

    def _check_range(self, offset: int, length: int) -> None:
        if (type(offset) is not int or type(length) is not int
                or offset < 0 or length < 0 or offset > self.image_size
                or length > self.image_size - offset):
            raise Ext2Error("read range exceeds image")

    def _read(self, offset: int, length: int) -> bytes:
        self._check_range(offset, length)
        value = self._read_at(offset, length)
        if not isinstance(value, (bytes, bytearray, memoryview)) or len(value) != length:
            raise Ext2Error("short or nonbyte callback result")
        return bytes(value)

    def _block_number(self, number: int) -> None:
        if type(number) is not int or not self.first_data_block <= number < self.blocks_count:
            raise Ext2Error("block pointer exceeds filesystem")

    def _group_table(self, group: int) -> int:
        if group in self._group_tables:
            return self._group_tables[group]
        if not 0 <= group < self.group_count:
            raise Ext2Error("inode group exceeds filesystem")
        descriptor = self._read(self._gdt_offset + 32 * group, 32)
        block_bitmap, inode_bitmap, table = struct.unpack_from("<III", descriptor)
        start = self.first_data_block + group * self.blocks_per_group
        end = min(start + self.blocks_per_group, self.blocks_count)
        table_blocks = self._ceil(self.inodes_per_group * self.inode_size, self.block_size)
        if any(not start <= value < end for value in (block_bitmap, inode_bitmap, table)):
            raise Ext2Error("group metadata points outside its group")
        if table + table_blocks > end:
            raise Ext2Error("inode table exceeds its group")
        if (block_bitmap == inode_bitmap
                or table <= block_bitmap < table + table_blocks
                or table <= inode_bitmap < table + table_blocks):
            raise Ext2Error("overlapping group metadata")
        self._group_tables[group] = table
        return table

    def inode(self, number: int) -> Ext2Inode:
        if type(number) is not int or not 1 <= number <= self.inodes_count:
            raise Ext2Error("inode number exceeds filesystem")
        group, index = divmod(number - 1, self.inodes_per_group)
        table = self._group_table(group)
        raw = self._read(table * self.block_size + index * self.inode_size, self.inode_size)
        mode = self._u16(raw, 0)
        if not mode & 0xF000:
            raise Ext2Error("unallocated inode")
        flags = self._u32(raw, 32)
        if flags & (0x4 | 0x200 | 0x400 | 0x800 | 0x80000 | 0x10000000):
            raise Ext2Error("compressed, encrypted, extent or inline inode unsupported")
        size = self._u32(raw, 4)
        if mode & 0xF000 == 0x8000 and self.revision:
            high = self._u32(raw, 108)
            if high and not self.feature_ro_compat & 0x2:
                raise Ext2Error("large file without LARGE_FILE feature")
            size |= high << 32
        return Ext2Inode(number, mode, size, flags, struct.unpack_from("<15I", raw, 40))

    def _owned_inode(self, value: int | Ext2Inode) -> Ext2Inode:
        # Always reload by number: callers cannot bypass metadata validation by
        # constructing a forged dataclass or passing one from a different image.
        return self.inode(value.number if isinstance(value, Ext2Inode) else value)

    def _pointer(self, block: int, index: int) -> int:
        if block == 0:
            return 0
        self._block_number(block)
        if not 0 <= index < self.block_size // 4:
            raise Ext2Error("indirect index exceeds pointer block")
        value = self._u32(self._read(block * self.block_size + index * 4, 4), 0)
        if value:
            self._block_number(value)
        return value

    def _file_block(self, node: Ext2Inode, logical: int) -> int:
        per_block = self.block_size // 4
        if logical < 12:
            result = node.blocks[logical]
        elif logical < 12 + per_block:
            result = self._pointer(node.blocks[12], logical - 12)
        elif logical < 12 + per_block + per_block * per_block:
            outer, inner = divmod(logical - 12 - per_block, per_block)
            result = self._pointer(self._pointer(node.blocks[13], outer), inner)
        else:
            remaining = logical - 12 - per_block - per_block * per_block
            outer, remaining = divmod(remaining, per_block * per_block)
            middle, inner = divmod(remaining, per_block)
            result = self._pointer(
                self._pointer(self._pointer(node.blocks[14], outer), middle), inner
            )
        if result:
            self._block_number(result)
        return result

    def _contents(self, node: Ext2Inode, limit: int) -> bytes:
        if node.size > limit:
            raise Ext2Error("file size exceeds read budget")
        per_block = self.block_size // 4
        capacity = 12 + per_block + per_block ** 2 + per_block ** 3
        if self._ceil(node.size, self.block_size) > capacity:
            raise Ext2Error("file size exceeds classic block-map capacity")
        output = bytearray()
        for logical in range(self._ceil(node.size, self.block_size)):
            length = min(self.block_size, node.size - len(output))
            block = self._file_block(node, logical)
            output.extend(self._read(block * self.block_size, length) if block else bytes(length))
        return bytes(output)

    def read_file(self, value: int | Ext2Inode, max_bytes: int | None = None) -> bytes:
        node = self._owned_inode(value)
        if node.kind != "file":
            raise Ext2Error("read_file requires a regular file; symlinks are refused")
        if max_bytes is None:
            max_bytes = self.max_read_bytes
        if type(max_bytes) is not int or max_bytes < 0 or max_bytes > self.max_read_bytes:
            raise Ext2Error("invalid file read budget")
        return self._contents(node, max_bytes)

    def list_dir(self, value: int | Ext2Inode) -> list[Ext2DirEntry]:
        node = self._owned_inode(value)
        if node.kind != "directory":
            raise Ext2Error("list_dir requires a directory")
        if node.size % self.block_size:
            raise Ext2Error("directory size is not block aligned")
        raw = self._contents(node, self.max_directory_bytes)
        entries = []
        names: set[bytes] = set()
        for start in range(0, len(raw), self.block_size):
            offset = start
            end = start + self.block_size
            while offset < end:
                if end - offset < 8:
                    raise Ext2Error("truncated directory header")
                number, record_bytes = struct.unpack_from("<IH", raw, offset)
                if self.feature_incompat & 0x2:
                    name_bytes, kind = raw[offset + 6], raw[offset + 7]
                    if kind > 7:
                        raise Ext2Error("invalid directory file type")
                else:
                    name_bytes = self._u16(raw, offset + 6)
                    kind = 0
                if (record_bytes < 8 or record_bytes % 4
                        or record_bytes > end - offset or name_bytes > 255
                        or name_bytes > record_bytes - 8):
                    raise Ext2Error("invalid directory record length")
                if number:
                    if number > self.inodes_count or not name_bytes:
                        raise Ext2Error("invalid directory inode/name")
                    name = raw[offset + 8:offset + 8 + name_bytes]
                    if b"/" in name or b"\0" in name or name in names:
                        raise Ext2Error("invalid or duplicate directory name")
                    names.add(name)
                    entries.append(Ext2DirEntry(name.decode("utf-8", "surrogateescape"), number, kind))
                offset += record_bytes
        return entries

    def resolve(self, path: str) -> Ext2Inode:
        if (not isinstance(path, str) or not path.startswith("/")
                or "\0" in path or "\\" in path or len(path) > 4096):
            raise Ext2Error("require a bounded absolute POSIX image path")
        parts = path.split("/")
        stack = [self.inode(2)]
        for part in parts[1:]:
            if part == "":
                continue
            if stack[-1].kind != "directory":
                raise Ext2Error("path traverses a nondirectory")
            if part == ".":
                continue
            if part == "..":
                if len(stack) == 1:
                    raise Ext2Error("path escapes image root")
                stack.pop()
                continue
            if len(part.encode("utf-8", "surrogateescape")) > 255:
                raise Ext2Error("path component exceeds ext2 name limit")
            matches = [entry for entry in self.list_dir(stack[-1]) if entry.name == part]
            if len(matches) != 1:
                raise Ext2Error("image path component not found")
            node = self.inode(matches[0].inode)
            if node.kind == "symlink":
                raise Ext2Error("symlink traversal is refused")
            if matches[0].file_type:
                expected = {"file": 1, "directory": 2, "symlink": 7}.get(node.kind)
                if expected is not None and matches[0].file_type != expected:
                    raise Ext2Error("directory type disagrees with inode mode")
            stack.append(node)
        if path.endswith("/") and stack[-1].kind != "directory":
            raise Ext2Error("trailing slash requires a directory")
        return stack[-1]
