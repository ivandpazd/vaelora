"""Vaelora 30-hex mixed-biome integration review.

Test-only scene. It does not add new production terrain kinds.
`desert_proxy` = current Plains geometry/decor with Sand top material.
`snow_proxy`   = current Peak geometry/decor with Snow top material.
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

import bpy

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_BLENDER_DIR = Path.cwd() / "tools" / "blender"
if str(REPO_BLENDER_DIR) not in sys.path:
    sys.path.insert(0, str(REPO_BLENDER_DIR))

import vaelora_artkit as artkit
import vaelora_geometry as geo
import vaelora_render as render
from vaelora_contract import coast_variant_for_tile, derive_seed
from vaelora_materials import world_materials
from vaelora_style import COAST_VARIANT_COUNT, HEX_AXIAL_X_STEP, HEX_AXIAL_Y_STEP, TERRAIN_VARIANTS

# Exactly 30 tiles: 6 columns x 5 rows in axial coordinates.
Q_VALUES = (-2, -1, 0, 1, 2, 3)
R_VALUES = (-2, -1, 0, 1, 2)

# Layout intentionally moves from sea -> coast -> fertile land -> relief/arid/snow.
# These are integration-review labels, not new runtime terrain IDs.
ROWS = {
    -2: ("open_sea",    "shallow_sea", "coast_base", "meadow", "mountain",     "snow_proxy"),
    -1: ("open_sea",    "shallow_sea", "coast_base", "forest", "hills",        "peak"),
     0: ("open_sea",    "shallow_sea", "coast_base", "meadow", "plains",       "mountain"),
     1: ("shallow_sea", "shallow_sea", "coast_base", "forest", "desert_proxy", "desert_proxy"),
     2: ("open_sea",    "shallow_sea", "coast_base", "plains", "desert_proxy", "snow_proxy"),
}

TERRAIN_MAP = {
    (q, r): ROWS[r][i]
    for r in R_VALUES
    for i, q in enumerate(Q_VALUES)
}
assert len(TERRAIN_MAP) == 30

SEA_KINDS = {"shallow_sea", "open_sea"}


def _base_kind(review_kind: str) -> str:
    if review_kind == "desert_proxy":
        return "plains"
    if review_kind == "snow_proxy":
        return "peak"
    return review_kind


def _variant_count(review_kind: str) -> int:
    return TERRAIN_VARIANTS[_base_kind(review_kind)]


def _world_pos(q: int, r: int) -> tuple[float, float]:
    return HEX_AXIAL_X_STEP * (q + r / 2.0), HEX_AXIAL_Y_STEP * r


# Center the whole 30-hex board around the canonical camera target.
ALL_POS = [_world_pos(q, r) for q, r in TERRAIN_MAP]
CENTER_X = sum(x for x, _ in ALL_POS) / len(ALL_POS)
CENTER_Y = sum(y for _, y in ALL_POS) / len(ALL_POS)


def _translate_new_objects(before: set[bpy.types.Object], q: int, r: int) -> None:
    x, y = _world_pos(q, r)
    dx, dy = x - CENTER_X, y - CENTER_Y
    for obj in [o for o in bpy.context.scene.objects if o not in before]:
        obj.location.x += dx
        obj.location.y += dy


def _surface_from_new(before: set[bpy.types.Object]) -> bpy.types.Object | None:
    candidates = [
        o for o in bpy.context.scene.objects
        if o not in before and o.name.startswith("VAE_Hex_PlayableSurface")
    ]
    return candidates[-1] if candidates else None


def _build_review_tile(review_kind: str, variant: int, seed: int) -> None:
    """Build production terrain, then apply test-only material proxies if requested."""
    base_kind = _base_kind(review_kind)
    artkit.build_terrain(base_kind, variant, seed)

    if review_kind not in {"desert_proxy", "snow_proxy"}:
        return

    # The playable surface is the last matching object created in this tile.
    surface = next(
        (o for o in reversed(list(bpy.context.scene.objects)) if o.name.startswith("VAE_Hex_PlayableSurface")),
        None,
    )
    if surface is None:
        return
    mats = world_materials()
    geo.set_material(surface, mats["sand"] if review_kind == "desert_proxy" else mats["snow"])


def _add_coast_edges(q: int, r: int, seed_root: int) -> None:
    """Use the real finite Coast v5.x overlay library on sea-facing coast edges."""
    variant = coast_variant_for_tile(seed_root, q, r, COAST_VARIANT_COUNT)
    for (dq, dr), edge in artkit.AXIAL_EDGE.items():
        neighbor = TERRAIN_MAP.get((q + dq, r + dr))
        if neighbor in SEA_KINDS:
            local_seed = artkit.coast_asset_seed(seed_root, variant, edge)
            geo.create_coast_edge(edge, random.Random(local_seed), morphology=variant)


def build_scene(seed: int) -> None:
    render.reset_scene()

    for idx, ((q, r), review_kind) in enumerate(TERRAIN_MAP.items()):
        base_kind = _base_kind(review_kind)
        variant = idx % _variant_count(review_kind)
        local_seed = derive_seed(seed, "terrain-30hex-integration", q, r, review_kind, variant)

        before = set(bpy.context.scene.objects)
        _build_review_tile(review_kind, variant, local_seed)

        if review_kind == "coast_base":
            _add_coast_edges(q, r, seed_root=derive_seed(seed, "terrain-30hex-coast"))

        _translate_new_objects(before, q, r)


def render_scene(seed: int, output: Path, strict: bool = True) -> Path:
    build_scene(seed)
    render.assert_blender_version(strict)
    camera = render.setup_master_camera("terrain")
    camera.data.ortho_scale = 22.8
    render.setup_lighting()

    review_dir = output / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    review_path = review_dir / "terrain_30hex_mixed_1920x1080.png"

    render.configure_render("terrain", review_path, transparent=False)
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    bpy.ops.render.render(write_still=True)
    render.save_blend(review_dir / "terrain_30hex_mixed.blend")
    return review_path


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    seed = int(argv[0]) if argv else 24000
    output = Path(argv[1]) if len(argv) > 1 else Path("game/assets/terrain/generated-v0.3.2-r2-terrain-v50rc2")
    path = render_scene(seed, output.resolve(), strict=True)
    print(f"30-hex mixed integration render: {path}")
