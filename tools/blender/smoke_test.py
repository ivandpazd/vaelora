"""Blender-side construction smoke test for Vaelora v0.3.2.

Runs builders without writing PNGs so missing imports/API/construction errors are caught
before expensive benchmark renders.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import vaelora_artkit as art
import vaelora_faction_kit as faction
import vaelora_geometry as geo
import vaelora_render as render
from vaelora_contract import derive_seed
from vaelora_style import TERRAIN_VARIANTS


def main() -> None:
    render.assert_blender_version(strict=False)
    root = 23990

    for idx, kind in enumerate(TERRAIN_VARIANTS):
        render.reset_scene()
        art.build_terrain(kind, 0, derive_seed(root, "smoke-terrain", kind, idx))

    for mask in (1, 3, 5, 7, 9, 21, 31, 42, 63):
        render.reset_scene()
        import random
        geo.create_coast_mask(mask, random.Random(derive_seed(root, "smoke-coast", mask)))

    for faction_name in ("auren", "brasal"):
        render.reset_scene()
        faction.create_city(faction_name, 2, derive_seed(root, "smoke-city", faction_name))
        for facing in range(6):
            render.reset_scene()
            faction.create_basic_soldier(faction_name, facing, derive_seed(root, "smoke-unit", faction_name, facing))

    render.reset_scene()
    art.build_benchmark(derive_seed(root, "smoke-benchmark"))
    render.reset_scene()
    art.build_coast_stress(derive_seed(root, "smoke-coast-stress"))
    render.reset_scene()
    art.build_premium_terrain_gallery(derive_seed(root, "smoke-premium-terrain"))

    print("Vaelora v0.3.2 Blender construction smoke test: PASS")


if __name__ == "__main__":
    main()
