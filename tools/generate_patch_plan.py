"""Generate structured forward and rollback transaction plans for α6700 (FTP + English).

Outputs deterministic JSON transaction files with verified hashes, bounds, and preimages.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.patch_spec import (
    SECTOR_SIZE,
    get_combined_targets,
)


def make_plans() -> tuple[dict, dict]:
    targets = get_combined_targets()
    forward_entries = []
    rollback_entries = []

    for t in targets:
        forward_entries.append({
            "target_id": t.target_id,
            "device": t.device,
            "sector": t.sector,
            "offset_in_sector": t.offset_in_sector,
            "length": len(t.patched),
            "expected_preimage_hex": t.preimage.hex(),
            "replacement_hex": t.patched.hex(),
            "stock_sector_sha256": t.stock_sector_sha256,
            "patched_sector_sha256": t.patched_sector_sha256,
        })

        rollback_entries.append({
            "target_id": t.target_id,
            "device": t.device,
            "sector": t.sector,
            "offset_in_sector": t.offset_in_sector,
            "length": len(t.preimage),
            "expected_preimage_hex": t.patched.hex(),
            "replacement_hex": t.preimage.hex(),
            "stock_sector_sha256": t.patched_sector_sha256,
            "patched_sector_sha256": t.stock_sector_sha256,
        })

    forward_plan = {
        "plan_type": "forward_patch",
        "description": "Sony ILCE-6700 2.00 Combined English Unmask + Playback FTP Custom Key",
        "model": "ILCE-6700",
        "firmware": "2.00",
        "sector_size": SECTOR_SIZE,
        "total_targets": len(forward_entries),
        "total_bytes_modified": sum(e["length"] for e in forward_entries),
        "entries": forward_entries,
    }

    rollback_plan = {
        "plan_type": "rollback_restore",
        "description": "Sony ILCE-6700 2.00 Factory 100% Restore Plan",
        "model": "ILCE-6700",
        "firmware": "2.00",
        "sector_size": SECTOR_SIZE,
        "total_targets": len(rollback_entries),
        "total_bytes_modified": sum(e["length"] for e in rollback_entries),
        "entries": rollback_entries,
    }

    return forward_plan, rollback_plan


def main() -> int:
    output_dir = PROJECT_ROOT / "research" / "plans"
    output_dir.mkdir(parents=True, exist_ok=True)

    forward_plan, rollback_plan = make_plans()

    forward_file = output_dir / "forward_patch_plan.json"
    rollback_file = output_dir / "rollback_restore_plan.json"

    with forward_file.open("w", encoding="utf-8") as f:
        json.dump(forward_plan, f, indent=2)
        f.write("\n")

    with rollback_file.open("w", encoding="utf-8") as f:
        json.dump(rollback_plan, f, indent=2)
        f.write("\n")

    print(f"Generated forward plan:  {forward_file}")
    print(f"Generated rollback plan: {rollback_file}")
    print(f"Targets: {forward_plan['total_targets']}, Total bytes modified: {forward_plan['total_bytes_modified']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
