"""α6700 Firmware 2.00 Combined Patch Specification (FTP + English).

Defines the exact byte-level transaction for enabling:
1. Playback FTP Custom Key (Action 0x0817)
2. True Native English Language Menu (english_predicate unmask)

Both targets reside exclusively on /dev/nflasha15 within /lib/appFw.so.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib


SECTOR_SIZE = 512
DEVICE_NAME = "/dev/nflasha15"

# Target 1: English Predicate (unconditional return 1)
# appFw.so offset 0x023080f8: cset w20, eq -> mov w20, #1
TARGET_EN_SECTOR = 383128
TARGET_EN_OFFSET_IN_SECTOR = 248
TARGET_EN_PREIMAGE = bytes.fromhex("f4179f1a")
TARGET_EN_PATCHED = bytes.fromhex("34008052")
STOCK_EN_SECTOR_SHA256 = "9358ef826d5b75e363bd122aa5cfdd218d644d5f72fd061648f53314c326aa36"
PATCHED_EN_SECTOR_SHA256 = "4eed8b81e8e4543ddec9befb692c7b236b043cb9d96ae3a9873360cd778b27b3"

# Target 2: Playback FTP Custom Key (Action 0x0817 capability)
# appFw.so offset 0x03f17ce4: 00 -> 01
TARGET_FTP_SECTOR = 445966
TARGET_FTP_OFFSET_IN_SECTOR = 228
TARGET_FTP_PREIMAGE = bytes.fromhex("00")
TARGET_FTP_PATCHED = bytes.fromhex("01")
STOCK_FTP_SECTOR_SHA256 = "7c899be67183d264a73c0357ee4874247359d1a3dc10156279a0d853a618bdb1"
PATCHED_FTP_SECTOR_SHA256 = "5669b7f9919257f3f7890d5b4fc26ef818119c0c239b6f63288218e9ae9bbb50"


class PatchError(ValueError):
    """Raised when sector verification or patch operation fails."""


@dataclass(frozen=True)
class TargetSector:
    target_id: str
    device: str
    sector: int
    offset_in_sector: int
    preimage: bytes
    patched: bytes
    stock_sector_sha256: str
    patched_sector_sha256: str

    def verify_stock_sector(self, sector_bytes: bytes) -> bool:
        if len(sector_bytes) != SECTOR_SIZE:
            raise PatchError(f"Sector {self.sector} must be {SECTOR_SIZE} bytes")
        actual_hash = hashlib.sha256(sector_bytes).hexdigest()
        if actual_hash != self.stock_sector_sha256:
            return False
        off = self.offset_in_sector
        end = off + len(self.preimage)
        if sector_bytes[off:end] != self.preimage:
            return False
        return True

    def verify_patched_sector(self, sector_bytes: bytes) -> bool:
        if len(sector_bytes) != SECTOR_SIZE:
            raise PatchError(f"Sector {self.sector} must be {SECTOR_SIZE} bytes")
        actual_hash = hashlib.sha256(sector_bytes).hexdigest()
        if actual_hash != self.patched_sector_sha256:
            return False
        off = self.offset_in_sector
        end = off + len(self.patched)
        if sector_bytes[off:end] != self.patched:
            return False
        return True

    def apply_patch(self, stock_sector_bytes: bytes) -> bytes:
        if not self.verify_stock_sector(stock_sector_bytes):
            raise PatchError(f"Pre-image verification failed for target {self.target_id}")
        data = bytearray(stock_sector_bytes)
        off = self.offset_in_sector
        end = off + len(self.patched)
        data[off:end] = self.patched
        result = bytes(data)
        if not self.verify_patched_sector(result):
            raise PatchError(f"Post-patch verification failed for target {self.target_id}")
        return result

    def revert_patch(self, patched_sector_bytes: bytes) -> bytes:
        if not self.verify_patched_sector(patched_sector_bytes):
            raise PatchError(f"Patched-state verification failed for target {self.target_id}")
        data = bytearray(patched_sector_bytes)
        off = self.offset_in_sector
        end = off + len(self.preimage)
        data[off:end] = self.preimage
        result = bytes(data)
        if not self.verify_stock_sector(result):
            raise PatchError(f"Post-revert verification failed for target {self.target_id}")
        return result


def get_combined_targets() -> tuple[TargetSector, TargetSector]:
    """Return the ordered specification of all candidate targets."""
    en_target = TargetSector(
        target_id="APP-EN-01",
        device=DEVICE_NAME,
        sector=TARGET_EN_SECTOR,
        offset_in_sector=TARGET_EN_OFFSET_IN_SECTOR,
        preimage=TARGET_EN_PREIMAGE,
        patched=TARGET_EN_PATCHED,
        stock_sector_sha256=STOCK_EN_SECTOR_SHA256,
        patched_sector_sha256=PATCHED_EN_SECTOR_SHA256,
    )
    ftp_target = TargetSector(
        target_id="APP-FTP-01",
        device=DEVICE_NAME,
        sector=TARGET_FTP_SECTOR,
        offset_in_sector=TARGET_FTP_OFFSET_IN_SECTOR,
        preimage=TARGET_FTP_PREIMAGE,
        patched=TARGET_FTP_PATCHED,
        stock_sector_sha256=STOCK_FTP_SECTOR_SHA256,
        patched_sector_sha256=PATCHED_FTP_SECTOR_SHA256,
    )
    return (en_target, ftp_target)
