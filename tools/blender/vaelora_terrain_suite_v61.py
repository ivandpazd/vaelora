"""Vaelora Terrain Suite v6.1-rc1 — Mountain / Peak Integration Pass.

Frozen v6.0 families are delegated unchanged. Mountain and Peak are rebuilt so the
terrain surface carries the mass and visible rock is embedded into that mass. Coast
keeps the proven v5.1 topology but is visually softened by ~20%.
"""
from __future__ import annotations

import math
import random
from pathlib import Path

import bpy
from mathutils import Vector

import vaelora_geometry as geo
import vaelora_render as render
import vaelora_terrain_suite_v6 as v6
from vaelora_contract import coast_asset_seed, derive_seed
from vaelora_style import COAST_VARIANT_COUNT
from vaelora_terrain_suite_v61_spec import (
    BENCHMARK36_V61,
    COAST_VISUAL_SCALE,
    FROZEN_V61_FAMILIES,
    SUITE_V61_FAMILIES,
    SUITE_V61_VARIANTS,
)

SEA_KINDS = {"shallow_sea", "open_sea"}
AXIAL_EDGE = v6.AXIAL_EDGE
FLOWER7 = v6.FLOWER7
TAU = math.tau


def _boost_surface_relief(surface, factor: float, cap: float) -> None:
    """Make the terrain itself carry more of the mountain silhouette."""
    for vert in surface.data.vertices:
        z = vert.co.z
        if z > 0.0:
            vert.co.z = min(cap, z * factor + (0.035 if z > 0.10 else 0.0))
    surface.data.update()


def _embedded_ridge(rng, surface, *, name, center, direction, length, width, height, material, embed=0.16, asymmetry=0.22):
    """Terrain-conforming exposed stratum. Ends/sides are always buried locally."""
    x0, y0 = center
    tangent = Vector((math.cos(direction), math.sin(direction), 0.0))
    side = Vector((-math.sin(direction), math.cos(direction), 0.0))
    sections = 8
    verts = []
    across = (-1.0, -0.48, 0.0, 0.48, 1.0)
    levels = (0.0, 0.40, 1.0, 0.46, 0.0)
    for sec in range(sections):
        t = sec / (sections - 1)
        longitudinal = (t - 0.5) * length
        envelope = math.sin(math.pi * t) ** 0.78
        curve = math.sin(t * math.pi * 1.25 + 0.35) * length * 0.035
        centre = Vector((x0, y0, 0.0)) + tangent * longitudinal + side * curve
        local_h = height * envelope * rng.uniform(0.93, 1.06)
        local_w = width * (0.52 + 0.48 * envelope) * rng.uniform(0.96, 1.04)
        crest_bias = rng.uniform(-asymmetry, asymmetry) * local_w * envelope
        for a, level in zip(across, levels):
            q = centre + side * (a * local_w + crest_bias * (1.0 - abs(a)))
            terrain_z = geo.surface_z_at(surface, q.x, q.y, 0.0)
            # At ends and sides the stone is below the terrain; only the authored crest emerges.
            burial = embed * (0.52 + 0.48 * abs(a)) + (1.0 - envelope) * embed * 0.90
            z = terrain_z - burial + local_h * level
            verts.append((q.x, q.y, z))
    faces = []
    row = 5
    for sec in range(sections - 1):
        for a in range(4):
            v = sec * row + a
            faces.append((v, v + 1, v + row + 1, v + row))
    obj = geo.make_mesh(name, verts, faces)
    geo.set_material(obj, material)
    geo.shade_flat(obj)
    geo.bevel(obj, min(width, height) * 0.018, 1)
    return obj


def _create_integrated_summit(rng, surface, *, scale: float = 1.0):
    """Broad geological summit with every base ring following the mountain surface."""
    mats = v6._materials()
    cx = rng.uniform(-0.12, 0.10)
    cy = rng.uniform(-0.08, 0.12)
    direction = rng.uniform(0.0, TAU)
    ca, sa = math.cos(direction), math.sin(direction)

    levels = (
        (0.00, 0.78, 0.62, 0.15),
        (0.30, 0.61, 0.48, 0.05),
        (0.62, 0.40, 0.31, 0.00),
    )
    n = 9
    verts = []
    top_heights = []
    for zoff, rx, ry, burial in levels:
        ring_z = []
        for i in range(n):
            a = TAU * i / n
            wobble = rng.uniform(0.91, 1.09)
            ux = math.cos(a) * rx * wobble * scale
            uy = math.sin(a) * ry * rng.uniform(0.93, 1.07) * scale
            x = cx + ux * ca - uy * sa
            y = cy + ux * sa + uy * ca
            terrain_z = geo.surface_z_at(surface, x, y, 0.0)
            z = terrain_z - burial * scale + zoff * scale
            verts.append((x, y, z))
            ring_z.append(z)
        top_heights.append(max(ring_z))
    apex = len(verts)
    apex_shift = Vector((math.cos(direction + 0.32), math.sin(direction + 0.32), 0.0)) * 0.14 * scale
    apex_ground = geo.surface_z_at(surface, cx + apex_shift.x, cy + apex_shift.y, 0.0)
    apex_z = max(top_heights[-1] + 0.56 * scale, apex_ground + 1.02 * scale)
    verts.append((cx + apex_shift.x, cy + apex_shift.y, apex_z))

    faces = []
    for ring in range(len(levels) - 1):
        a0, b0 = ring * n, (ring + 1) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    top0 = (len(levels) - 1) * n
    for i in range(n):
        j = (i + 1) % n
        faces.append((top0 + i, top0 + j, apex))

    obj = geo.make_mesh("VAE_V61_IntegratedSummit", verts, faces)
    geo.set_material(obj, mats["rock"])
    geo.shade_flat(obj)
    geo.bevel(obj, 0.024 * scale, 1)
    return obj


def _talus(rng, surface, count: int, radius_min: float, radius_max: float):
    for _ in range(count):
        a = rng.uniform(0.0, TAU)
        r = rng.uniform(radius_min, radius_max)
        x, y = math.cos(a) * r, math.sin(a) * r
        if not geo.hex_contains_disc(x, y, 0.16):
            continue
        geo.create_sculpted_rock(
            rng,
            (x, y, geo.surface_z_at(surface, x, y, 0.0) + 0.012),
            scale=rng.uniform(0.08, 0.15),
            warm=rng.random() < 0.34,
        )


def _build_mountain_v61(seed: int, variant: int, peak: bool = False):
    kind = "peak" if peak else "mountain"
    mats = v6._materials()
    rng = random.Random(derive_seed(seed, "suite-v61-" + kind, variant))
    surface = v6._create_land_base(kind, seed, variant, mats["mountain_ground"])

    # The surface now owns the mountain silhouette; no giant slab sits above flat ground.
    _boost_surface_relief(surface, 1.48 if peak else 1.34, 1.12 if peak else 0.98)
    direction = rng.uniform(0.0, TAU)

    # Embedded stone strata reveal geology without creating a floating prop read.
    _embedded_ridge(
        rng, surface,
        name="VAE_V61_MountainStratumMain",
        center=(-0.06, 0.01),
        direction=direction,
        length=rng.uniform(2.15, 2.48) if not peak else rng.uniform(2.28, 2.56),
        width=rng.uniform(0.66, 0.80),
        height=rng.uniform(0.40, 0.50),
        material=mats["rock"],
        embed=0.20,
        asymmetry=0.26,
    )
    _embedded_ridge(
        rng, surface,
        name="VAE_V61_MountainStratumShoulder",
        center=(math.cos(direction + 1.05) * 0.20, math.sin(direction + 1.05) * 0.20),
        direction=direction + rng.choice((-1, 1)) * rng.uniform(0.70, 0.92),
        length=rng.uniform(1.20, 1.56),
        width=rng.uniform(0.42, 0.54),
        height=rng.uniform(0.26, 0.34),
        material=mats["rock_warm"],
        embed=0.17,
        asymmetry=0.30,
    )

    if peak:
        # The summit is a broad continuation of the mountain, not a separate needle.
        _create_integrated_summit(rng, surface, scale=rng.uniform(0.94, 1.04))
        _embedded_ridge(
            rng, surface,
            name="VAE_V61_PeakLowerButtress",
            center=(-math.cos(direction) * 0.22, -math.sin(direction) * 0.22),
            direction=direction - rng.choice((-1, 1)) * rng.uniform(0.40, 0.62),
            length=rng.uniform(1.05, 1.32),
            width=rng.uniform(0.34, 0.44),
            height=rng.uniform(0.20, 0.28),
            material=mats["rock_shadow"],
            embed=0.15,
            asymmetry=0.24,
        )
        _talus(rng, surface, 5, 0.72, 1.28)
    else:
        # A small lit shelf gives readable strata while remaining physically attached.
        _embedded_ridge(
            rng, surface,
            name="VAE_V61_MountainLitShelf",
            center=(math.cos(direction) * 0.12, math.sin(direction) * 0.12),
            direction=direction + 0.10,
            length=rng.uniform(0.74, 0.98),
            width=rng.uniform(0.22, 0.28),
            height=rng.uniform(0.14, 0.20),
            material=mats["rock_light"],
            embed=0.10,
            asymmetry=0.16,
        )
        _talus(rng, surface, 6, 0.76, 1.38)
        occupied = []
        for ring in ("outer", "outer"):
            v6._add_grass(rng, surface, occupied, ring, rng.uniform(0.34, 0.46), False, flowers=False)


def _soften_coast_edge(edge_index: int, rng: random.Random, morphology: int = 0):
    """Use Coast v5.1, then reduce shoreline/beach amplitude without changing edge registration."""
    objs = geo.create_coast_edge(edge_index, rng, morphology=morphology)
    a, b = geo.hex_edge_points(edge_index)
    ab = b - a
    denom = max(1e-9, ab.x * ab.x + ab.y * ab.y)
    for obj in objs:
        if obj.type != "MESH" or not obj.name.startswith("VAE_Coast_"):
            continue
        if "ShallowShelf" in obj.name:
            factor = 0.86
        elif "WetSand" in obj.name or "DrySand" in obj.name:
            factor = COAST_VISUAL_SCALE
        elif "Foam" in obj.name:
            factor = 0.82
        else:
            continue
        for vert in obj.data.vertices:
            p = Vector((vert.co.x, vert.co.y, 0.0))
            t = ((p.x - a.x) * ab.x + (p.y - a.y) * ab.y) / denom
            t = max(0.0, min(1.0, t))
            proj = a + ab * t
            delta = p - proj
            vert.co.x = proj.x + delta.x * factor
            vert.co.y = proj.y + delta.y * factor
        obj.data.update()
    return objs


def build_candidate_tile(kind: str, variant: int, seed: int, core_builder):
    if kind in FROZEN_V61_FAMILIES or kind in SEA_KINDS:
        return v6.build_candidate_tile(kind, variant, seed, core_builder)
    if kind == "mountain":
        return _build_mountain_v61(seed, variant, False)
    if kind == "peak":
        return _build_mountain_v61(seed, variant, True)
    raise ValueError(f"unknown Terrain Suite v6.1 kind: {kind}")


def _render(path: Path, blend: Path, ortho: float, strict: bool, resolution=(1920, 1080)):
    return v6._render(path, blend, ortho, strict, resolution)


def generate_family_review(family: str, seed: int, output: Path, strict: bool, core_builder):
    if family not in SUITE_V61_FAMILIES:
        raise ValueError(family)
    if family == "coast":
        return generate_coast_review(seed, output, strict, core_builder)
    render.reset_scene()
    for idx, (q, r) in enumerate(FLOWER7):
        variant = idx % SUITE_V61_VARIANTS[family]
        local = derive_seed(seed, "suite-v61-family", family, idx, variant)
        before = set(bpy.context.scene.objects)
        build_candidate_tile(family, variant, local, core_builder)
        v6._translate_new(before, q, r)
    ortho = 12.0 if family == "mountain" else 12.4 if family == "peak" else 11.4
    _render(
        output / "review" / f"terrain_suite_v61_{family}_1920x1080.png",
        output / "review" / f"terrain_suite_v61_{family}.blend",
        ortho,
        strict,
    )


def generate_coast_review(seed: int, output: Path, strict: bool, core_builder):
    render.reset_scene()
    layout = {(-1,0):"meadow", (-1,1):"meadow", (0,1):"plains", (0,0):"meadow", (1,0):"shallow_sea", (1,-1):"shallow_sea", (0,-1):"open_sea"}
    positions = [v6._world_pos(q, r) for q, r in layout]
    centre = (sum(x for x, _ in positions) / len(positions), sum(y for _, y in positions) / len(positions))
    forced = (0, 1, 2, 3, 4)
    cc = 0
    for idx, ((q, r), kind) in enumerate(layout.items()):
        before = set(bpy.context.scene.objects)
        build_candidate_tile(kind, idx % 4, derive_seed(seed, "suite-v61-coast-base", q, r), core_builder)
        if kind not in SEA_KINDS:
            for (dq, dr), edge in AXIAL_EDGE.items():
                if layout.get((q + dq, r + dr)) in SEA_KINDS:
                    cv = forced[cc % len(forced)] % COAST_VARIANT_COUNT
                    cc += 1
                    _soften_coast_edge(edge, random.Random(coast_asset_seed(seed, cv, edge)), morphology=cv)
        v6._translate_new(before, q, r, centre)
    _render(output / "review" / "terrain_suite_v61_coast_1920x1080.png", output / "review" / "terrain_suite_v61_coast.blend", 10.6, strict)


def generate_all_family_reviews(seed: int, output: Path, strict: bool, core_builder):
    for family in SUITE_V61_FAMILIES:
        generate_family_review(family, derive_seed(seed, "suite-v61-family-root", family), output, strict, core_builder)


def generate_benchmark36(seed: int, output: Path, strict: bool, core_builder):
    render.reset_scene()
    layout = {}
    for r, row in enumerate(BENCHMARK36_V61):
        for q, kind in enumerate(row):
            layout[(q, r)] = kind
    positions = [v6._world_pos(q, r) for q, r in layout]
    centre = (sum(x for x, _ in positions) / len(positions), sum(y for _, y in positions) / len(positions))
    for idx, ((q, r), kind) in enumerate(layout.items()):
        local = "water" if kind in SEA_KINDS else kind
        variant = idx % SUITE_V61_VARIANTS.get(local, 4)
        local_seed = derive_seed(seed, "suite-v61-benchmark36", q, r, kind, variant)
        before = set(bpy.context.scene.objects)
        build_candidate_tile(kind, variant, local_seed, core_builder)
        if kind not in SEA_KINDS:
            for (dq, dr), edge in AXIAL_EDGE.items():
                if layout.get((q + dq, r + dr)) in SEA_KINDS:
                    cv = derive_seed(seed, "suite-v61-coast", q, r) % COAST_VARIANT_COUNT
                    _soften_coast_edge(edge, random.Random(coast_asset_seed(seed, cv, edge)), morphology=cv)
        v6._translate_new(before, q, r, centre)
    _render(output / "review" / "terrain_suite_v61_benchmark36_1920x1080.png", output / "review" / "terrain_suite_v61_benchmark36.blend", 24.4, strict)
