"""α6700 Target Definitions for Full FTP and True Native English.

Targets solely reside in /usr/lib/appFw.so.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


TARGET_FILE = "/usr/lib/appFw.so"
APPFW_SIZE = 89027992
APPFW_SHA256 = "e65fd595052be5d0e98ce8000dfcb94f90a2f8309de70ef140375052009b0ef3"


@dataclass(frozen=True)
class TargetWindow:
    offset: int
    preimage: bytes
    patched: bytes
    name: str
    feature: str  # "ftp" or "english"


@dataclass(frozen=True)
class TargetSpan:
    offset: int
    length: int
    targets: List[TargetWindow]


# --- Feature 1: English Language Unmask ---
# Predicate at 0x023080f8: cset w20, eq -> mov w20, #1
TARGET_ENGLISH = TargetWindow(
    offset=0x023080F8,
    preimage=bytes.fromhex("f4179f1a"),
    patched=bytes.fromhex("34008052"),
    name="English availability predicate unmask (cset w20, eq -> mov w20, #1)",
    feature="english",
)

# --- Feature 2: Full FTP Support ---
# Part A: Playback Gallery Custom Key Action 0x0817 (FTP_TRANSFER)
TARGET_FTP_PLAYBACK_KEY = TargetWindow(
    offset=0x03F17CE4,
    preimage=bytes.fromhex("00"),
    patched=bytes.fromhex("01"),
    name="Playback Gallery Custom Key Action 0x0817 (FTP_TRANSFER)",
    feature="ftp",
)

# Part B: Network Menu FTP Settings (0x05a5..0x05b0)
TARGET_FTP_NETWORK_SETTINGS = [
    TargetWindow(0x03F17524, b"\x00", b"\x01", "Setting 0x05a5: FTP switch static model support", "ftp"),
    TargetWindow(0x03F1752C, b"\x00", b"\x01", "Setting 0x05a6: Connect method", "ftp"),
    TargetWindow(0x03F17534, b"\x00", b"\x01", "Setting 0x05a8: Server settings", "ftp"),
    TargetWindow(0x03F1753C, b"\x00", b"\x01", "Setting 0x05aa: Auto FTP transfer", "ftp"),
    TargetWindow(0x03F17544, b"\x00", b"\x01", "Setting 0x05ac: RAW+J transfer target", "ftp"),
    TargetWindow(0x03F1754C, b"\x00", b"\x01", "Setting 0x05ad: JPEG transfer image", "ftp"),
    TargetWindow(0x03F17554, b"\x00", b"\x01", "Setting 0x05ae: HEIF transfer image", "ftp"),
    TargetWindow(0x03F1755C, b"\x00", b"\x01", "Setting 0x05af: Transfer target", "ftp"),
    TargetWindow(0x03F17564, b"\x00", b"\x01", "Setting 0x05b0: FTP power save", "ftp"),
]

# Part C: Playback & Gallery Menu Tree Permissions (81 targets, 0x04BD7522..0x04C45F6A)
TARGET_FTP_GALLERY_MENUS = [
    TargetWindow(0x04BD7522, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-012)", "ftp"),
    TargetWindow(0x04BD7524, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-013)", "ftp"),
    TargetWindow(0x04BD7526, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-014)", "ftp"),
    TargetWindow(0x04BD7528, bytes.fromhex("00"), bytes.fromhex("01"), "FTP parent menu 0x226 current-model permission (edit-015)", "ftp"),
    TargetWindow(0x04BD752A, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-016)", "ftp"),
    TargetWindow(0x04BD752C, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-017)", "ftp"),
    TargetWindow(0x04BDE292, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x22d current-model permission (edit-018)", "ftp"),
    TargetWindow(0x04BEE732, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x227 current-model permission (edit-020)", "ftp"),
    TargetWindow(0x04BEE7E2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x22f current-model permission (edit-021)", "ftp"),
    TargetWindow(0x04BFF11A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x23c current-model permission (edit-022)", "ftp"),
    TargetWindow(0x04C01F9A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x903 current-model permission (edit-023)", "ftp"),
    TargetWindow(0x04C0203A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x904 current-model permission (edit-024)", "ftp"),
    TargetWindow(0x04C09CD2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x924 current-model permission (edit-025)", "ftp"),
    TargetWindow(0x04C09D72, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x925 current-model permission (edit-026)", "ftp"),
    TargetWindow(0x04C09E12, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x90a current-model permission (edit-027)", "ftp"),
    TargetWindow(0x04C09EB2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x90b current-model permission (edit-028)", "ftp"),
    TargetWindow(0x04C09F52, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x90c current-model permission (edit-029)", "ftp"),
    TargetWindow(0x04C09FF2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x90d current-model permission (edit-030)", "ftp"),
    TargetWindow(0x04C0A092, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x90e current-model permission (edit-031)", "ftp"),
    TargetWindow(0x04C0A132, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x90f current-model permission (edit-032)", "ftp"),
    TargetWindow(0x04C0A1D2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x910 current-model permission (edit-033)", "ftp"),
    TargetWindow(0x04C0A272, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x911 current-model permission (edit-034)", "ftp"),
    TargetWindow(0x04C0A312, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x912 current-model permission (edit-035)", "ftp"),
    TargetWindow(0x04C0B1A2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x236 current-model permission (edit-036)", "ftp"),
    TargetWindow(0x04C11232, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x918 current-model permission (edit-037)", "ftp"),
    TargetWindow(0x04C112D2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x919 current-model permission (edit-038)", "ftp"),
    TargetWindow(0x04C11EA2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x235 current-model permission (edit-039)", "ftp"),
    TargetWindow(0x04C11F52, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x228 current-model permission (edit-040)", "ftp"),
    TargetWindow(0x04C12002, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x238 current-model permission (edit-041)", "ftp"),
    TargetWindow(0x04C16BCE, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-042)", "ftp"),
    TargetWindow(0x04C16BD0, bytes.fromhex("00"), bytes.fromhex("00"), "FTP parent menu 0x262 current-model permission; parent:0x262: hide duplicate blank FTP parent (edit-043)", "ftp"),
    TargetWindow(0x04C16BD2, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-044)", "ftp"),
    TargetWindow(0x04C16BD4, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-045)", "ftp"),
    TargetWindow(0x04C16BD6, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-046)", "ftp"),
    TargetWindow(0x04C16BD8, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-047)", "ftp"),
    TargetWindow(0x04C16BDA, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-048)", "ftp"),
    TargetWindow(0x04C16BDC, bytes.fromhex("00"), bytes.fromhex("01"), "historically validated FTP parent permission column (app-only) (edit-049)", "ftp"),
    TargetWindow(0x04C17BD2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x916 current-model permission (edit-050)", "ftp"),
    TargetWindow(0x04C17C72, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x917 current-model permission (edit-051)", "ftp"),
    TargetWindow(0x04C1B402, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x906 current-model permission (edit-052)", "ftp"),
    TargetWindow(0x04C1B4A2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x907 current-model permission (edit-053)", "ftp"),
    TargetWindow(0x04C1B5E2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x909 current-model permission (edit-054)", "ftp"),
    TargetWindow(0x04C1B682, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x91f current-model permission (edit-055)", "ftp"),
    TargetWindow(0x04C1B722, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x920 current-model permission (edit-056)", "ftp"),
    TargetWindow(0x04C1B7C2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x91d current-model permission (edit-057)", "ftp"),
    TargetWindow(0x04C1B862, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x91e current-model permission (edit-058)", "ftp"),
    TargetWindow(0x04C1C082, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x93e current-model permission (edit-059)", "ftp"),
    TargetWindow(0x04C1C122, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x93f current-model permission (edit-060)", "ftp"),
    TargetWindow(0x04C1C1C2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x93c current-model permission (edit-061)", "ftp"),
    TargetWindow(0x04C1C262, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x93d current-model permission (edit-062)", "ftp"),
    TargetWindow(0x04C1C302, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x934 current-model permission (edit-063)", "ftp"),
    TargetWindow(0x04C1C3A2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x935 current-model permission (edit-064)", "ftp"),
    TargetWindow(0x04C1C442, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x936 current-model permission (edit-065)", "ftp"),
    TargetWindow(0x04C1C4E2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x937 current-model permission (edit-066)", "ftp"),
    TargetWindow(0x04C1DBB2, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x23b current-model permission (edit-068)", "ftp"),
    TargetWindow(0x04C2215A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x932 current-model permission (edit-071)", "ftp"),
    TargetWindow(0x04C221FA, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x933 current-model permission (edit-072)", "ftp"),
    TargetWindow(0x04C2502A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x234 current-model permission (edit-073)", "ftp"),
    TargetWindow(0x04C2518A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x23a current-model permission (edit-074)", "ftp"),
    TargetWindow(0x04C2523A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x239 current-model permission (edit-075)", "ftp"),
    TargetWindow(0x04C2814A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x938 current-model permission (edit-077)", "ftp"),
    TargetWindow(0x04C281EA, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x939 current-model permission (edit-078)", "ftp"),
    TargetWindow(0x04C2828A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x93a current-model permission (edit-079)", "ftp"),
    TargetWindow(0x04C2832A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x93b current-model permission (edit-080)", "ftp"),
    TargetWindow(0x04C283CA, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x92f current-model permission (edit-081)", "ftp"),
    TargetWindow(0x04C2846A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x930 current-model permission (edit-082)", "ftp"),
    TargetWindow(0x04C2850A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x931 current-model permission (edit-083)", "ftp"),
    TargetWindow(0x04C2EC3A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x237 current-model permission (edit-086)", "ftp"),
    TargetWindow(0x04C30A5A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x913 current-model permission (edit-087)", "ftp"),
    TargetWindow(0x04C30AFA, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x914 current-model permission (edit-088)", "ftp"),
    TargetWindow(0x04C30B9A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x915 current-model permission (edit-089)", "ftp"),
    TargetWindow(0x04C30C3A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x921 current-model permission (edit-090)", "ftp"),
    TargetWindow(0x04C30CDA, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x922 current-model permission (edit-091)", "ftp"),
    TargetWindow(0x04C30D7A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x923 current-model permission (edit-092)", "ftp"),
    TargetWindow(0x04C3177A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x928 current-model permission (edit-093)", "ftp"),
    TargetWindow(0x04C3195A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x92b current-model permission (edit-094)", "ftp"),
    TargetWindow(0x04C319FA, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x92c current-model permission (edit-095)", "ftp"),
    TargetWindow(0x04C3598A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x91a current-model permission (edit-096)", "ftp"),
    TargetWindow(0x04C35A2A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x91b current-model permission (edit-097)", "ftp"),
    TargetWindow(0x04C35ACA, bytes.fromhex("00"), bytes.fromhex("01"), "FTP leaf menu 0x91c current-model permission (edit-098)", "ftp"),
    TargetWindow(0x04C45F6A, bytes.fromhex("00"), bytes.fromhex("01"), "FTP child menu 0x22e current-model permission (edit-099)", "ftp"),
]

ALL_FTP_TARGETS: List[TargetWindow] = [TARGET_FTP_PLAYBACK_KEY] + TARGET_FTP_NETWORK_SETTINGS + TARGET_FTP_GALLERY_MENUS
ALL_TARGETS: List[TargetWindow] = [TARGET_ENGLISH] + ALL_FTP_TARGETS


def build_target_spans(
    targets: List[TargetWindow],
    max_span: int = 0x20000,
    max_gap: int = 0x10000,
) -> List[TargetSpan]:
    """Group target windows into minimal contiguous I/O spans.

    Ensures each span length <= max_span (default 128 KiB, safe USB write block),
    and splits at large gaps (> max_gap, default 64 KiB) to avoid unnecessary transfer.
    """
    if not targets:
        return []
    sorted_targets = sorted(targets, key=lambda t: t.offset)
    spans: List[TargetSpan] = []
    curr_targets: List[TargetWindow] = []
    for t in sorted_targets:
        t_len = max(len(t.preimage), len(t.patched))
        if not curr_targets:
            curr_targets = [t]
        else:
            new_span_len = (t.offset + t_len) - curr_targets[0].offset
            prev_len = max(len(curr_targets[-1].preimage), len(curr_targets[-1].patched))
            gap = t.offset - (curr_targets[-1].offset + prev_len)
            if new_span_len <= max_span and gap <= max_gap:
                curr_targets.append(t)
            else:
                start = curr_targets[0].offset
                last_len = max(len(curr_targets[-1].preimage), len(curr_targets[-1].patched))
                length = (curr_targets[-1].offset + last_len) - start
                spans.append(TargetSpan(offset=start, length=length, targets=curr_targets))
                curr_targets = [t]
    if curr_targets:
        start = curr_targets[0].offset
        last_len = max(len(curr_targets[-1].preimage), len(curr_targets[-1].patched))
        length = (curr_targets[-1].offset + last_len) - start
        spans.append(TargetSpan(offset=start, length=length, targets=curr_targets))
    return spans

