"""Vaelora Terrain Suite v6.2-rc1 — final Mountain / Peak geological polish.

Everything already accepted in v6.1 stays frozen. Mountain keeps the terrain-led
mass from v6.1 but replaces long stone ribs with shorter, discontinuous embedded
outcrops. Peak keeps the same mountain foundation and replaces the remaining
regular/conical summit read with four distinct asymmetric geological archetypes.
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
import vaelora_terrain_suite_v61 as v61
from vaelora_contract import derive_seed
from vaelora_terrain_suite_v62_spec import (
    BENCHMARK36_V62,
    FROZEN_V62_FAMILIES,
    PEAK_ARCHETYPES,
    SUITE_V62_FAMILIES,
    SUITE_V62_VARIANTS,
)

SEA_KINDS = {"shallow_sea", "open_sea"}
FLOWER7 = v6.FLOWER7
AXIAL_EDGE = v6.AXIAL_EDGE
TAU = math.tau


def _rotated_offset(direction: float, along: float, side: float) -> tuple[float, float]:
    ca, sa = math.cos(direction), math.sin(direction)
    return along * ca - side * sa, along * sa + side * ca


def _broken_outcrops(rng: random.Random, surface, *, direction: float, peak: bool = False, variant: int = 0) -> None:
    """Create separated terrain-conforming outcrops instead of one continuous stone plate."""
    mats = v6._materials()
    # Each variant has a different geological rhythm. Gaps are intentional and
    # preserve visible terrain between exposed stone segments.
    plans = (
        ((-0.62, -0.02, 0.74, 0.38, 0.25), (0.02, 0.06, 0.62, 0.34, 0.22), (0.58, -0.07, 0.52, 0.31, 0.18)),
        ((-0.48, 0.13, 0.58, 0.34, 0.21), (0.24, -0.10, 0.76, 0.40, 0.25), (0.64, 0.16, 0.42, 0.28, 0.16)),
        ((-0.66, -0.10, 0.50, 0.31, 0.18), (-0.12, 0.11, 0.64, 0.36, 0.23), (0.46, -0.05, 0.62, 0.35, 0.22)),
        ((-0.42, 0.00, 0.68, 0.39, 0.24), (0.20, 0.15, 0.48, 0.30, 0.17), (0.56, -0.16, 0.54, 0.33, 0.19)),
    )
    plan = plans[variant % len(plans)]
    materials = (mats["rock"], mats["rock_warm"], mats["rock_shadow"])
    for idx, (along, side, length, width, height) in enumerate(plan):
        dx, dy = _rotated_offset(direction, along, side)
        v61._embedded_ridge(
            rng,
            surface,
            name=f"VAE_V62_BrokenOutcrop_{idx}",
            center=(dx, dy),
            direction=direction + rng.uniform(-0.16, 0.16),
            length=length * rng.uniform(0.94, 1.08) * (1.04 if peak else 1.0),
            width=width * rng.uniform(0.94, 1.06),
            height=height * rng.uniform(0.92, 1.08),
            material=materials[idx % len(materials)],
            embed=0.16 if peak else 0.17,
            asymmetry=0.34,
        )
    # One short cross-stratum breaks the railroad-track read and adds erosion logic.
    if variant % 2 == 1 or peak:
        dx, dy = _rotated_offset(direction, rng.uniform(-0.10, 0.18), rng.choice((-1, 1)) * rng.uniform(0.28, 0.42))
        v61._embedded_ridge(
            rng,
            surface,
            name="VAE_V62_CrossOutcrop",
            center=(dx, dy),
            direction=direction + rng.choice((-1, 1)) * rng.uniform(0.72, 1.00),
            length=rng.uniform(0.44, 0.64),
            width=rng.uniform(0.26, 0.34),
            height=rng.uniform(0.14, 0.20),
            material=mats["rock_light"] if not peak else mats["rock_warm"],
            embed=0.13,
            asymmetry=0.36,
        )


def _peak_profile(variant: int):
    """Four visibly different summit grammars. Values are local to the summit frame."""
    v = variant % 4
    if v == 0:  # Alpine offset: tall but broad, summit shifted off-axis.
        return {
            "name": "alpine_offset",
            "direction": 0.10,
            "rings": ((0.00, .78, .62, .12, 0.00, 0.00), (.30, .61, .45, .04, .05, .02), (.58, .39, .28, 0.00, .13, .04)),
            "apex": (.23, .06, .46), "mods": (0.08, 0.12, 0.15),
        }
    if v == 1:  # Broken summit: squat irregular crown with strong lateral displacement.
        return {
            "name": "broken_summit",
            "direction": -0.18,
            "rings": ((0.00, .82, .60, .13, 0.00, 0.00), (.26, .62, .43, .05, -.04, .03), (.51, .43, .27, 0.00, .12, .10)),
            "apex": (.28, .16, .36), "mods": (0.14, 0.18, 0.24),
        }
    if v == 2:  # Twin shoulder: broad main summit with a secondary high shoulder.
        return {
            "name": "twin_shoulder",
            "direction": 0.24,
            "rings": ((0.00, .86, .64, .13, 0.00, 0.00), (.28, .64, .48, .05, .02, -.04), (.55, .40, .31, 0.00, .12, -.07)),
            "apex": (.21, -.08, .42), "mods": (0.10, 0.14, 0.18),
        }
    # Escarpment: wide foot, compressed top, one steep face.
    return {
        "name": "escarpment",
        "direction": -0.34,
        "rings": ((0.00, .88, .56, .14, 0.00, 0.00), (.27, .66, .39, .05, .08, .00), (.50, .36, .22, 0.00, .18, -.02)),
        "apex": (.30, -.02, .38), "mods": (0.18, 0.20, 0.26),
    }


def _create_asymmetric_summit(rng: random.Random, surface, *, variant: int, scale: float = 1.0):
    mats = v6._materials()
    profile = _peak_profile(variant)
    direction = rng.uniform(0.0, TAU) + profile["direction"]
    ca, sa = math.cos(direction), math.sin(direction)
    cx = rng.uniform(-0.10, 0.08)
    cy = rng.uniform(-0.08, 0.10)
    n = 10
    verts: list[tuple[float, float, float]] = []
    top_z = []
    phases = (0.00, 0.17, -0.11)

    for ring_idx, (zoff, rx, ry, burial, sx, sy) in enumerate(profile["rings"]):
        ring_z = []
        mod_amp = profile["mods"][ring_idx]
        for i in range(n):
            a = TAU * i / n + phases[ring_idx]
            # Broad low-frequency angular deformation avoids a perfect cone.
            angular = 1.0 + mod_amp * math.sin(a * 2.0 + 0.7 * variant) + (mod_amp * 0.55) * math.sin(a * 3.0 - 0.4)
            angular *= rng.uniform(0.95, 1.05)
            ux = math.cos(a) * rx * angular * scale
            uy = math.sin(a) * ry * rng.uniform(0.94, 1.06) * scale
            local_cx = cx + (sx * ca - sy * sa) * scale
            local_cy = cy + (sx * sa + sy * ca) * scale
            x = local_cx + ux * ca - uy * sa
            y = local_cy + ux * sa + uy * ca
            ground = geo.surface_z_at(surface, x, y, 0.0)
            # Upper skyline is slightly broken; base always remains buried into terrain.
            skyline = 0.0 if ring_idx == 0 else math.sin(a * 2.0 + variant) * (0.020 + 0.012 * ring_idx) * scale
            z = ground - burial * scale + zoff * scale + skyline
            verts.append((x, y, z))
            ring_z.append(z)
        top_z.append(max(ring_z))

    apex_idx = len(verts)
    ax, ay, extra = profile["apex"]
    apex_x = cx + (ax * ca - ay * sa) * scale
    apex_y = cy + (ax * sa + ay * ca) * scale
    apex_ground = geo.surface_z_at(surface, apex_x, apex_y, 0.0)
    apex_z = max(top_z[-1] + extra * scale, apex_ground + (0.78 + extra * 0.42) * scale)
    verts.append((apex_x, apex_y, apex_z))

    faces = []
    rings = len(profile["rings"])
    for ring in range(rings - 1):
        a0, b0 = ring * n, (ring + 1) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    top0 = (rings - 1) * n
    for i in range(n):
        j = (i + 1) % n
        faces.append((top0 + i, top0 + j, apex_idx))

    obj = geo.make_mesh(f"VAE_V62_Peak_{profile['name']}", verts, faces)
    geo.set_material(obj, mats["rock"])
    geo.shade_flat(obj)
    geo.bevel(obj, 0.020 * scale, 1)

    # Extra high shoulder for the twin/broken families; it is embedded, not freestanding.
    if variant % 4 in (1, 2):
        shoulder_dir = direction + (-0.78 if variant % 4 == 1 else 0.70)
        dx, dy = _rotated_offset(direction, -0.08, 0.34 if variant % 4 == 2 else -0.30)
        v61._embedded_ridge(
            rng, surface,
            name="VAE_V62_PeakHighShoulder",
            center=(cx + dx, cy + dy),
            direction=shoulder_dir,
            length=rng.uniform(0.62, 0.82),
            width=rng.uniform(0.32, 0.40),
            height=rng.uniform(0.24, 0.32),
            material=mats["rock_warm"],
            embed=0.14,
            asymmetry=0.38,
        )
    return obj


def _build_mountain_v62(seed: int, variant: int, peak: bool = False):
    kind = "peak" if peak else "mountain"
    mats = v6._materials()
    rng = random.Random(derive_seed(seed, "suite-v62-" + kind, variant))
    surface = v6._create_land_base(kind, seed, variant, mats["mountain_ground"])

    # Keep the successful terrain-led v6.1 mass; the polish is geological, not a redesign.
    v61._boost_surface_relief(surface, 1.47 if peak else 1.35, 1.13 if peak else 0.99)
    base_direction = rng.uniform(0.0, TAU) + (variant % 4) * 0.18
    _broken_outcrops(rng, surface, direction=base_direction, peak=peak, variant=variant)

    if peak:
        _create_asymmetric_summit(rng, surface, variant=variant, scale=rng.uniform(0.96, 1.04))
        v61._talus(rng, surface, 5, 0.78, 1.32)
    else:
        v61._talus(rng, surface, 6, 0.78, 1.40)
        occupied = []
        for ring in ("outer", "outer"):
            v6._add_grass(rng, surface, occupied, ring, rng.uniform(0.32, 0.44), False, flowers=False)


def build_candidate_tile(kind: str, variant: int, seed: int, core_builder):
    if kind in FROZEN_V62_FAMILIES or kind in SEA_KINDS:
        return v61.build_candidate_tile(kind, variant, seed, core_builder)
    if kind == "mountain":
        return _build_mountain_v62(seed, variant, False)
    if kind == "peak":
        return _build_mountain_v62(seed, variant, True)
    raise ValueError(f"unknown Terrain Suite v6.2 kind: {kind}")


def _render(path: Path, blend: Path, ortho: float, strict: bool, resolution=(1920, 1080)):
    return v6._render(path, blend, ortho, strict, resolution)


def generate_family_review(family: str, seed: int, output: Path, strict: bool, core_builder):
    if family not in SUITE_V62_FAMILIES:
        raise ValueError(family)
    if family == "coast":
        # Coast is frozen exactly at the approved v6.1 behavior.
        return v61.generate_coast_review(seed, output, strict, core_builder)
    render.reset_scene()
    for idx, (q, r) in enumerate(FLOWER7):
        variant = idx % SUITE_V62_VARIANTS[family]
        local = derive_seed(seed, "suite-v62-family", family, idx, variant)
        before = set(bpy.context.scene.objects)
        build_candidate_tile(family, variant, local, core_builder)
        v6._translate_new(before, q, r)
    ortho = 12.2 if family == "mountain" else 12.6 if family == "peak" else 11.4
    _render(
        output / "review" / f"terrain_suite_v62_{family}_1920x1080.png",
        output / "review" / f"terrain_suite_v62_{family}.blend",
        ortho,
        strict,
    )


def generate_all_family_reviews(seed: int, output: Path, strict: bool, core_builder):
    for family in SUITE_V62_FAMILIES:
        generate_family_review(family, derive_seed(seed, "suite-v62-family-root", family), output, strict, core_builder)


def generate_benchmark36(seed: int, output: Path, strict: bool, core_builder):
    render.reset_scene()
    layout = {}
    for r, row in enumerate(BENCHMARK36_V62):
        for q, kind in enumerate(row):
            layout[(q, r)] = kind
    positions = [v6._world_pos(q, r) for q, r in layout]
    centre = (sum(x for x, _ in positions) / len(positions), sum(y for _, y in positions) / len(positions))
    for idx, ((q, r), kind) in enumerate(layout.items()):
        local = "water" if kind in SEA_KINDS else kind
        variant = idx % SUITE_V62_VARIANTS.get(local, 4)
        local_seed = derive_seed(seed, "suite-v62-benchmark36", q, r, kind, variant)
        before = set(bpy.context.scene.objects)
        build_candidate_tile(kind, variant, local_seed, core_builder)
        if kind not in SEA_KINDS:
            for (dq, dr), edge in AXIAL_EDGE.items():
                if layout.get((q + dq, r + dr)) in SEA_KINDS:
                    # Coast stays frozen at v6.1.
                    cv = derive_seed(seed, "suite-v62-coast", q, r) % 6
                    from vaelora_contract import coast_asset_seed
                    v61._soften_coast_edge(edge, random.Random(coast_asset_seed(seed, cv, edge)), morphology=cv)
        v6._translate_new(before, q, r, centre)
    _render(
        output / "review" / "terrain_suite_v62_benchmark36_1920x1080.png",
        output / "review" / "terrain_suite_v62_benchmark36.blend",
        24.4,
        strict,
    )
