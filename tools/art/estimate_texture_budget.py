"""Estimate decoded texture footprint for Vaelora final PNG families.

This is a planning estimate. Godot importer/runtime measurements remain authoritative.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image


def human_bytes(value: float) -> str:
    for unit in ("B", "KiB", "MiB", "GiB"):
        if value < 1024 or unit == "GiB":
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{value:.2f} GiB"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--mipmaps", action="store_true", help="Include estimated mipmap overhead (about one third)")
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()

    groups: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "decoded_bytes": 0, "disk_bytes": 0})
    assets = []
    for root in args.roots:
        manifests = root / "manifests"
        for mp in sorted(manifests.glob("*.json")):
            data = json.loads(mp.read_text(encoding="utf-8"))
            png = root / "final_2x" / f"{data['asset_id']}_2x.png"
            if not png.exists():
                continue
            with Image.open(png) as image:
                channels = 4 if "A" in image.getbands() else 3
                decoded = image.width * image.height * channels
            if args.mipmaps:
                decoded *= 4 / 3
            disk = png.stat().st_size
            g = groups[data["family"]]
            g["count"] += 1
            g["decoded_bytes"] += decoded
            g["disk_bytes"] += disk
            assets.append({"asset_id": data["asset_id"], "family": data["family"], "decoded_bytes": round(decoded), "disk_bytes": disk})

    total_decoded = sum(g["decoded_bytes"] for g in groups.values())
    total_disk = sum(g["disk_bytes"] for g in groups.values())
    report = {
        "mipmap_estimate_enabled": args.mipmaps,
        "groups": {k: {**v, "decoded_human": human_bytes(v["decoded_bytes"]), "disk_human": human_bytes(v["disk_bytes"])} for k, v in sorted(groups.items())},
        "totals": {"decoded_bytes": round(total_decoded), "decoded_human": human_bytes(total_decoded), "disk_bytes": total_disk, "disk_human": human_bytes(total_disk)},
        "assets": assets,
        "note": "Planning estimate only; verify Godot imported/runtime memory on representative targets.",
    }
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
