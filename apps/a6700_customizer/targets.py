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

ALL_FTP_TARGETS: List[TargetWindow] = [TARGET_FTP_PLAYBACK_KEY] + TARGET_FTP_NETWORK_SETTINGS
ALL_TARGETS: List[TargetWindow] = [TARGET_ENGLISH] + ALL_FTP_TARGETS
