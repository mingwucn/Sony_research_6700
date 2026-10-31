"""Verify target sectors against stock and patched hashes.

Can check individual 512-byte raw sector files or a full partition image.
Outputs exact status: STOCK, PATCHED, or UNKNOWN/CORRUPT.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

# Add project root to sys.path if run directly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.patch_spec import (
    SECTOR_SIZE,
    get_combined_targets,
)


def verify_image(image_path: Path) -> int:
    targets = get_combined_targets()
    print(f"Inspecting image: {image_path}")
    size = image_path.stat().st_size
    print(f"File size: {size} bytes ({size // SECTOR_SIZE} sectors)")

    with image_path.open("rb") as f:
        all_ok = True
        for target in targets:
            byte_off = target.sector * SECTOR_SIZE
            if byte_off + SECTOR_SIZE > size:
                print(f"[{target.target_id}] ERROR: Sector {target.sector} is outside image bounds!")
                all_ok = False
                continue

            f.seek(byte_off)
            data = f.read(SECTOR_SIZE)
            actual_sha = hashlib.sha256(data).hexdigest()

            if actual_sha == target.stock_sector_sha256:
                status = "STOCK (Factory Unmodified)"
            elif actual_sha == target.patched_sector_sha256:
                status = "PATCHED (Feature Enabled)"
            else:
                status = f"UNKNOWN/MISMATCH (Actual SHA-256: {actual_sha})"
                all_ok = False

            print(f"[{target.target_id}] Sector {target.sector} (+{target.offset_in_sector}): {status}")

    return 0 if all_ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify target sectors in /dev/nflasha15 image")
    parser.add_argument("image", type=Path, help="Path to /dev/nflasha15 ext2 partition image")
    args = parser.parse_args()

    if not args.image.is_file():
        print(f"File not found: {args.image}", file=sys.stderr)
        return 2

    return verify_image(args.image)


if __name__ == "__main__":
    sys.exit(main())
