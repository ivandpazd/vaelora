"""Validate that premium review evidence covers the complete finite visual library."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLENDER_DIR = HERE.parent / "blender"
if str(BLENDER_DIR) not in sys.path:
    sys.path.insert(0, str(BLENDER_DIR))

from vaelora_style import COAST_VARIANT_COUNT, TERRAIN_VARIANTS


def manifest_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    manifests = root / "manifests"
    if not manifests.exists():
        return ids
    for path in manifests.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            aid = data.get("asset_id")
            if aid:
                ids.add(str(aid))
        except Exception:
            continue
    return ids


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terrain-root", type=Path, required=True)
    parser.add_argument("--faction-root", type=Path, required=True)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()

    terrain_root = args.terrain_root.resolve()
    faction_root = args.faction_root.resolve()
    terrain_ids = manifest_ids(terrain_root)
    faction_ids = manifest_ids(faction_root)

    expected_terrain = {
        f"terrain_{kind}_{variant:02d}"
        for kind, count in TERRAIN_VARIANTS.items()
        for variant in range(count)
    }
    expected_coast = {
        f"coast_v{variant}_edge_{edge}"
        for variant in range(COAST_VARIANT_COUNT)
        for edge in range(6)
    }
    expected_cities = {
        f"city_{faction}_stage_{stage}"
        for faction in ("auren", "brasal")
        for stage in (1, 2, 3)
    }
    expected_units = {
        f"unit_{faction}_basic_soldier_idle_f{facing}"
        for faction in ("auren", "brasal")
        for facing in range(6)
    }
    expected_review_files = {
        "terrain_benchmark_1920x1080.png",
        "coast_stress_1920x1080.png",
        "repetition_meadow_1920x1080.png",
        "repetition_plains_1920x1080.png",
        "repetition_forest_1920x1080.png",
        "repetition_hills_1920x1080.png",
        "repetition_mountain_1920x1080.png",
    }
    review_dir = terrain_root / "review"
    actual_review = {p.name for p in review_dir.glob("*.png")} if review_dir.exists() else set()

    missing_terrain = sorted((expected_terrain | expected_coast) - terrain_ids)
    missing_faction = sorted((expected_cities | expected_units) - faction_ids)
    missing_review = sorted(expected_review_files - actual_review)
    errors = []
    if missing_terrain:
        errors.append(f"missing terrain/coast assets: {missing_terrain}")
    if missing_faction:
        errors.append(f"missing city/unit assets: {missing_faction}")
    if missing_review:
        errors.append(f"missing review evidence: {missing_review}")

    report = {
        "expected": {
            "terrain_variants": len(expected_terrain),
            "coast_edges": len(expected_coast),
            "city_stages": len(expected_cities),
            "soldier_facings": len(expected_units),
            "review_images": len(expected_review_files),
        },
        "present": {
            "terrain_manifest_ids": len(terrain_ids),
            "faction_manifest_ids": len(faction_ids),
            "review_pngs": len(actual_review),
        },
        "missing": {
            "terrain_coast": missing_terrain,
            "faction": missing_faction,
            "review": missing_review,
        },
        "errors": errors,
        "passed": not errors,
    }
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
