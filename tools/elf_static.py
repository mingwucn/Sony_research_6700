"""Read ELF64 little-endian data and candidate AArch64 references as inert bytes.

No file, process, device, network, relocation or executable-loading API is used.
Virtual addresses are ELF link-time addresses, never runtime process addresses.
B/BL and adjacent ADRP+ADD matches are encoding candidates: executable segments
may contain data, and this module establishes neither reachability nor complete
control flow, function boundaries, ABI compatibility or patch safety.
"""
from __future__ import annotations

from dataclasses import dataclass
import struct


MAX_FILE_BYTES = 512 * 1024 * 1024
MAX_TABLE_ENTRIES = 1_000_000
MAX_STRING_BYTES = 1024 * 1024
U64_LIMIT = 1 << 64
PT_LOAD = 1
PF_X = 1
SHT_SYMTAB = 2
SHT_STRTAB = 3
SHT_NOBITS = 8
SHT_DYNSYM = 11


class ElfError(ValueError):
    """Malformed or unsupported ELF metadata, with no executable side effect."""


@dataclass(frozen=True)
class Segment:
    index: int
    type: int
    flags: int
    offset: int
    virtual_address: int
    physical_address: int
    file_size: int
    memory_size: int
    alignment: int


@dataclass(frozen=True)
class Section:
    index: int
    name: str
    type: int
    flags: int
    virtual_address: int
    offset: int
    size: int
    link: int
    info: int
    alignment: int
    entry_size: int


@dataclass(frozen=True)
class Symbol:
    table: str
    index: int
    name: str
    value: int
    size: int
    type: int
    binding: int
    visibility: int
    section_index: int


@dataclass(frozen=True)
class StringHit:
    file_offset: int
    virtual_addresses: tuple[int, ...]
    text: str


@dataclass(frozen=True)
class BranchReference:
    file_offset: int
    virtual_address: int
    target_va: int
    kind: str
    instruction: int


@dataclass(frozen=True)
class AddressReference:
    file_offset: int
    virtual_address: int
    target_va: int
    register: int
    kind: str = "adrp_add_adjacent"


def _integer(value: int, name: str, *, positive: bool = False) -> None:
    if type(value) is not int or value < (1 if positive else 0):
        raise ElfError("invalid " + name)


class ElfImage:
    """Bounded static metadata reader over one immutable complete byte string."""

    def __init__(self, data: bytes):
        if type(data) is not bytes or not 64 <= len(data) <= MAX_FILE_BYTES:
            raise ElfError("complete immutable ELF bytes required within size limit")
        self.data = data
        if data[:7] != b"\x7fELF\x02\x01\x01":
            raise ElfError("only ELF64 little-endian version 1 is supported")
        fields = struct.unpack_from("<HHIQQQIHHHHHH", data, 16)
        (self.type, self.machine, version, self.entry, phoff, shoff, self.flags,
         ehsize, phentsize, phnum, shentsize, shnum, shstrndx) = fields
        if version != 1 or ehsize != 64:
            raise ElfError("invalid ELF version or header size")
        self._span(0, ehsize)
        section_zero = None
        if shoff:
            if shentsize < 64:
                raise ElfError("section header entry is too short")
            self._span(shoff, shentsize)
            section_zero = struct.unpack_from("<IIQQQQIIQQ", data, shoff)
            if section_zero[1] != 0:
                raise ElfError("section zero must be SHT_NULL")
            if shnum == 0:
                shnum = section_zero[5]
            if shstrndx == 0xffff:
                shstrndx = section_zero[6]
            if phnum == 0xffff:
                phnum = section_zero[7]
            if not shnum:
                raise ElfError("section table has no section zero")
        elif shnum or shstrndx or phnum == 0xffff:
            raise ElfError("missing section table or extended-numbering metadata")
        self._table(phoff, phentsize, phnum, 56, "program")
        self._table(shoff, shentsize, shnum, 64, "section")

        segments = []
        for index in range(phnum):
            row = struct.unpack_from("<IIQQQQQQ", data, phoff + index * phentsize)
            segment = Segment(index, *row)
            self._span(segment.offset, segment.file_size)
            if segment.type == PT_LOAD:
                if segment.file_size > segment.memory_size:
                    raise ElfError("load segment file extent exceeds memory extent")
                if segment.virtual_address + segment.memory_size > U64_LIMIT:
                    raise ElfError("load segment virtual extent overflows")
                if segment.alignment not in (0, 1):
                    if segment.alignment & (segment.alignment - 1):
                        raise ElfError("load segment alignment is not a power of two")
                    if (segment.offset - segment.virtual_address) % segment.alignment:
                        raise ElfError("load segment offset/address alignment mismatch")
            segments.append(segment)
        self.segments = tuple(segments)

        raw_sections = []
        for index in range(shnum):
            row = struct.unpack_from("<IIQQQQIIQQ", data, shoff + index * shentsize)
            if row[1] not in (0, SHT_NOBITS):
                self._span(row[4], row[5])
            if row[3] + row[5] > U64_LIMIT:
                raise ElfError("section virtual extent overflows")
            raw_sections.append(row)
        names = None
        if shstrndx:
            if shstrndx >= len(raw_sections) or raw_sections[shstrndx][1] != SHT_STRTAB:
                raise ElfError("section name table is not a string table")
            names = raw_sections[shstrndx]
            if names[2] & 0x800:
                raise ElfError("compressed section name tables are unsupported")
        sections = []
        for index, row in enumerate(raw_sections):
            if names is None and row[0]:
                raise ElfError("section name exists without a name table")
            name = "" if names is None else self._string(names[4], names[5], row[0])
            sections.append(Section(index, name, *row[1:]))
        self.sections = tuple(sections)

    def _span(self, offset: int, size: int) -> None:
        _integer(offset, "file offset")
        _integer(size, "file size")
        if offset > len(self.data) or size > len(self.data) - offset:
            raise ElfError("file extent is out of bounds")

    def _table(self, offset: int, entry: int, count: int, minimum: int, name: str) -> None:
        if not 0 <= count <= MAX_TABLE_ENTRIES:
            raise ElfError(name + " table entry limit exceeded")
        if count:
            if not offset or entry < minimum:
                raise ElfError("invalid " + name + " table shape")
            self._span(offset, count * entry)

    def _string(self, table_offset: int, table_size: int, index: int) -> str:
        self._span(table_offset, table_size)
        if not 0 <= index < table_size:
            raise ElfError("string index is out of bounds")
        at = table_offset + index
        end = self.data.find(b"\0", at, min(table_offset + table_size, at + MAX_STRING_BYTES + 1))
        if end < 0:
            raise ElfError("unterminated or oversized string")
        return self.data[at:end].decode("utf-8", "surrogateescape")

    def section_data(self, section: Section) -> bytes:
        if not isinstance(section, Section) or section not in self.sections:
            raise ElfError("unknown section")
        if section.type == SHT_NOBITS:
            raise ElfError("NOBITS section has no file bytes")
        if section.type == 0:
            return b""
        self._span(section.offset, section.size)
        return self.data[section.offset:section.offset + section.size]

    def symbols(self) -> tuple[Symbol, ...]:
        """Return both static and dynamic symbol tables; undefined values stay typed."""
        found = []
        for section in self.sections:
            if section.type not in (SHT_SYMTAB, SHT_DYNSYM):
                continue
            if section.flags & 0x800:
                raise ElfError("compressed symbol tables are unsupported")
            if (section.entry_size < 24 or section.size % section.entry_size
                    or section.size // section.entry_size > MAX_TABLE_ENTRIES):
                raise ElfError("invalid symbol table entry shape")
            if section.link >= len(self.sections):
                raise ElfError("symbol table string link is out of bounds")
            strings = self.sections[section.link]
            if strings.type != SHT_STRTAB or strings.flags & 0x800:
                raise ElfError("symbol table link is not a string table")
            for index in range(section.size // section.entry_size):
                if len(found) >= MAX_TABLE_ENTRIES:
                    raise ElfError("total symbol entry limit exceeded")
                name, info, other, shndx, value, size = struct.unpack_from(
                    "<IBBHQQ", self.data, section.offset + index * section.entry_size)
                if shndx == 0xffff:
                    raise ElfError("extended symbol section indices are unsupported")
                if shndx < 0xff00 and shndx >= len(self.sections):
                    raise ElfError("symbol section index is out of bounds")
                if value + size > U64_LIMIT:
                    raise ElfError("symbol extent overflows")
                found.append(Symbol(section.name, index,
                                    self._string(strings.offset, strings.size, name),
                                    value, size, info & 15, info >> 4, other & 3, shndx))
        return tuple(found)

    def va_to_offset(self, va: int, size: int = 1) -> int | None:
        """Map a link-time VA only through file-backed PT_LOAD spans; refuse ambiguity."""
        _integer(va, "virtual address")
        _integer(size, "mapping size", positive=True)
        if va + size > U64_LIMIT:
            raise ElfError("virtual mapping extent overflows")
        found = {s.offset + va - s.virtual_address for s in self.segments
                 if s.type == PT_LOAD and s.virtual_address <= va
                 and size <= s.file_size - (va - s.virtual_address)}
        if len(found) > 1:
            raise ElfError("virtual address maps to conflicting file bytes")
        return next(iter(found)) if found else None

    def offset_to_vas(self, offset: int, size: int = 1) -> tuple[int, ...]:
        _integer(size, "mapping size", positive=True)
        self._span(offset, size)
        return tuple(sorted({s.virtual_address + offset - s.offset for s in self.segments
                             if s.type == PT_LOAD and s.offset <= offset
                             and size <= s.file_size - (offset - s.offset)}))

    def find_ascii(self, needle: str | bytes, *, nul_terminated: bool = False,
                   max_hits: int = 100_000) -> tuple[StringHit, ...]:
        """Find raw printable-ASCII bytes, not proof that a program consumes a string."""
        if type(needle) is str:
            try:
                needle = needle.encode("ascii")
            except UnicodeEncodeError as exc:
                raise ElfError("ASCII needle required") from exc
        if type(needle) is not bytes or not needle or any(not 32 <= b < 127 for b in needle):
            raise ElfError("nonempty printable ASCII needle required")
        if type(nul_terminated) is not bool:
            raise ElfError("boolean termination option required")
        _integer(max_hits, "hit limit", positive=True)
        found = []
        start = 0
        pattern = needle + (b"\0" if nul_terminated else b"")
        while True:
            at = self.data.find(pattern, start)
            if at < 0:
                return tuple(found)
            if len(found) >= max_hits:
                raise ElfError("string hit limit exceeded")
            found.append(StringHit(at, self.offset_to_vas(at, len(pattern)), needle.decode("ascii")))
            start = at + 1

    def _instructions(self):
        if self.machine != 183:
            raise ElfError("AArch64 instruction decoding requires e_machine 183")
        # Merge executable file ranges sharing the same VA/file mapping. Avoid
        # a per-instruction set: real applications contain millions of words.
        mappings = {}
        for segment in self.segments:
            if segment.type != PT_LOAD or not segment.flags & PF_X:
                continue
            delta = segment.virtual_address - segment.offset
            mappings.setdefault(delta, []).append((segment.offset, segment.offset + segment.file_size))
        for delta, ranges in mappings.items():
            merged = []
            for start, end in sorted(ranges):
                if merged and start <= merged[-1][1]:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], end))
                else:
                    merged.append((start, end))
            for start, end in merged:
                start += (-(start + delta)) % 4
                for at in range(start, end - 3, 4):
                    va = at + delta
                    yield at, va, struct.unpack_from("<I", self.data, at)[0], end

    def branch_refs(self, target_va: int | None = None, *, include_b: bool = True
                    ) -> tuple[BranchReference, ...]:
        """Candidate B/BL imm26 references; embedded data and unreachable code may match."""
        if target_va is not None:
            _integer(target_va, "branch target")
            if target_va >= U64_LIMIT:
                raise ElfError("branch target overflows")
        if type(include_b) is not bool:
            raise ElfError("boolean branch option required")
        found = []
        for at, va, word, _end in self._instructions():
            if word & 0x7c000000 != 0x14000000:
                continue
            kind = "BL" if word & 0x80000000 else "B"
            if kind == "B" and not include_b:
                continue
            immediate = word & 0x03ffffff
            displacement = ((immediate ^ 0x02000000) - 0x02000000) * 4
            target = (va + displacement) % U64_LIMIT
            if target_va is None or target == target_va:
                found.append(BranchReference(at, va, target, kind, word))
        return tuple(found)

    def adrp_add_refs(self, target_va: int | None = None) -> tuple[AddressReference, ...]:
        """Candidate adjacent ADRP Xn + ADD Xd,Xn,#imm addresses, no data-flow claim."""
        if target_va is not None:
            _integer(target_va, "address target")
            if target_va >= U64_LIMIT:
                raise ElfError("address target overflows")
        found = []
        for at, va, word, end in self._instructions():
            if word & 0x9f000000 != 0x90000000 or at + 8 > end:
                continue
            register = word & 31
            if register == 31:
                continue
            add = struct.unpack_from("<I", self.data, at + 4)[0]
            if add & 0xff800000 != 0x91000000 or (add >> 5) & 31 != register or add & 31 == 31:
                continue
            immediate = ((word >> 5) & 0x7ffff) << 2 | ((word >> 29) & 3)
            page_delta = ((immediate ^ 0x100000) - 0x100000) << 12
            addend = ((add >> 10) & 0xfff) << (12 if add & 0x400000 else 0)
            target = ((va & ~0xfff) + page_delta + addend) % U64_LIMIT
            if target_va is None or target_va == target:
                found.append(AddressReference(at, va, target, add & 31))
        return tuple(found)
