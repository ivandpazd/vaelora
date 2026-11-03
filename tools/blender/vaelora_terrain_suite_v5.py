"""Unified candidate terrain suite for Vaelora v5.0-rc1 General.

The suite is intentionally parallel to the current accepted/candidate generators.
It lets us validate a common v5 visual language before promoting every family into
TERRAIN_VARIANTS. Meadow v5.0-rc2 and Coast v5.1 remain the visual baselines.
"""
from __future__ import annotations

import math
import random
from pathlib import Path
from typing import Callable

import bpy
from mathutils import Vector

import vaelora_geometry as geo
import vaelora_render as render
from vaelora_contract import coast_asset_seed, derive_seed
from vaelora_materials import create_terrain_v3_material, world_materials
from vaelora_style import COAST_VARIANT_COUNT, HEX_AXIAL_X_STEP, HEX_AXIAL_Y_STEP, HEX_RADIUS
from vaelora_terrain_suite_spec import BENCHMARK36, SUITE_FAMILIES, SUITE_VARIANTS

TAU = math.tau
SEA_KINDS = {"shallow_sea", "open_sea"}
AXIAL_EDGE = {(0, 1): 0, (-1, 1): 1, (-1, 0): 2, (0, -1): 3, (1, -1): 4, (1, 0): 5}
FLOWER7 = ((0, 0), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1))


def _world_pos(q: int, r: int) -> tuple[float, float]:
    return HEX_AXIAL_X_STEP * (q + r / 2.0), HEX_AXIAL_Y_STEP * r


def _translate_new(before: set[bpy.types.Object], q: int, r: int, center: tuple[float, float] = (0.0, 0.0)) -> None:
    x, y = _world_pos(q, r)
    x -= center[0]
    y -= center[1]
    for obj in [o for o in bpy.context.scene.objects if o not in before]:
        obj.location.x += x
        obj.location.y += y


def _suite_materials() -> dict[str, bpy.types.Material]:
    """Candidate materials keep one painterly response but distinct biome palettes."""
    return {
        "plains_v5": create_terrain_v3_material("VAE_Suite_PlainsV5", "#5E6538", "#9A9853", "#D1C36A", broad_scale=1.22, micro_scale=6.2, roughness=0.91, bump_strength=0.060),
        "hill_ground": create_terrain_v3_material("VAE_Suite_HillGround", "#50613B", "#829052", "#B6AC64", broad_scale=1.18, micro_scale=5.8, roughness=0.91, bump_strength=0.065),
        "mountain_ground": create_terrain_v3_material("VAE_Suite_MountainGround", "#58604F", "#7F855C", "#A8A371", broad_scale=1.12, micro_scale=5.0, roughness=0.92, bump_strength=0.070),
        "desert": create_terrain_v3_material("VAE_Suite_DesertV1", "#90623E", "#C89A5E", "#E5C77D", broad_scale=1.08, micro_scale=7.0, roughness=0.94, bump_strength=0.055),
        "snow_ground": create_terrain_v3_material("VAE_Suite_SnowV1", "#A9BABD", "#D9E1DF", "#F3F1E7", broad_scale=1.10, micro_scale=7.2, roughness=0.78, bump_strength=0.038),
        "forest_ground": create_terrain_v3_material("VAE_Suite_ForestGround", "#405D43", "#718B54", "#9EAA65", broad_scale=1.18, micro_scale=6.0, roughness=0.92, bump_strength=0.058),
    }


def _hex_perimeter(samples_per_side: int = 6) -> list[Vector]:
    corners = [Vector((math.cos(math.radians(30 + 60 * i)) * HEX_RADIUS, math.sin(math.radians(30 + 60 * i)) * HEX_RADIUS, 0.0)) for i in range(6)]
    result: list[Vector] = []
    for i in range(6):
        a, b = corners[i], corners[(i + 1) % 6]
        for j in range(samples_per_side):
            t = j / samples_per_side
            result.append(a.lerp(b, t))
    return result


def _elliptic(x: float, y: float, cx: float, cy: float, rx: float, ry: float, angle: float, height: float, power: float = 1.5) -> float:
    ca, sa = math.cos(angle), math.sin(angle)
    dx, dy = x - cx, y - cy
    u, v = dx * ca + dy * sa, -dx * sa + dy * ca
    d2 = (u / max(rx, 0.001)) ** 2 + (v / max(ry, 0.001)) ** 2
    return height * math.exp(-(d2 ** power) * 1.35)


def _shape_params(kind: str, seed: int, variant: int):
    """Return a seed-rotated but variant-authored macro silhouette.

    The first suite draft used one template per biome and relied mostly on rotation /
    mirroring. That was technically varied but could still read as the same tile spun
    around. r2 keeps deterministic rotation while giving each of the four variants a
    genuinely different arrangement of masses, basins and shoulders.
    """
    rng = random.Random(derive_seed(seed, "suite-v5-shape", kind, variant))
    angle = rng.uniform(0.0, TAU)
    mirror = -1.0 if rng.random() < 0.5 else 1.0
    v = variant % 4

    archetypes = {
        "plains": (
            [(-0.42, 0.36, 1.18, 0.50, 0.18), (0.64, -0.40, 0.76, 0.34, 0.09), (0.06, -0.04, 0.72, 0.58, -0.055)],
            [(-0.70, -0.08, 0.86, 0.42, 0.13), (0.44, 0.48, 0.94, 0.44, 0.16), (0.48, -0.56, 0.66, 0.34, 0.08), (-0.08, 0.04, 0.68, 0.54, -0.045)],
            [(-0.10, 0.58, 1.30, 0.36, 0.16), (0.18, -0.54, 1.04, 0.34, 0.11), (-0.70, -0.24, 0.62, 0.44, -0.040)],
            [(0.58, 0.24, 1.10, 0.50, 0.18), (-0.58, -0.52, 0.72, 0.34, 0.10), (-0.48, 0.50, 0.62, 0.36, 0.07), (0.06, -0.02, 0.72, 0.58, -0.050)],
        ),
        "hills": (
            [(-0.62, 0.30, 0.84, 0.48, 0.31), (0.46, -0.18, 0.78, 0.46, 0.28), (0.54, 0.62, 0.56, 0.34, 0.15), (-0.02, 0.03, 0.58, 0.48, -0.08)],
            [(-0.58, -0.48, 0.70, 0.48, 0.29), (0.08, 0.44, 0.92, 0.48, 0.32), (0.70, -0.22, 0.60, 0.38, 0.18), (0.10, -0.06, 0.54, 0.48, -0.07)],
            [(-0.10, 0.58, 1.00, 0.40, 0.30), (-0.28, -0.54, 0.88, 0.40, 0.27), (0.70, 0.06, 0.54, 0.36, 0.17), (-0.02, 0.02, 0.56, 0.48, -0.085)],
            [(0.54, 0.42, 0.78, 0.46, 0.30), (-0.56, 0.06, 0.72, 0.44, 0.25), (0.34, -0.58, 0.74, 0.40, 0.24), (-0.04, -0.04, 0.58, 0.48, -0.075)],
        ),
        "mountain": (
            [(0.00, 0.12, 1.18, 0.72, 0.20), (-0.72, -0.38, 0.62, 0.42, 0.10)],
            [(-0.36, 0.28, 0.96, 0.64, 0.18), (0.58, -0.36, 0.82, 0.48, 0.13), (0.16, -0.08, 0.58, 0.44, -0.035)],
            [(0.26, 0.42, 1.18, 0.56, 0.19), (-0.42, -0.44, 0.72, 0.46, 0.11)],
            [(-0.32, -0.10, 1.08, 0.70, 0.19), (0.64, 0.40, 0.62, 0.40, 0.10), (-0.58, 0.48, 0.52, 0.36, 0.07)],
        ),
        "peak": (
            [(0.00, 0.10, 1.00, 0.66, 0.17), (0.52, -0.48, 0.56, 0.36, 0.08)],
            [(-0.22, 0.26, 0.86, 0.58, 0.16), (0.54, -0.18, 0.62, 0.40, 0.10)],
            [(0.18, -0.04, 1.02, 0.56, 0.17), (-0.54, 0.52, 0.50, 0.34, 0.075)],
            [(-0.18, -0.16, 0.92, 0.62, 0.16), (0.48, 0.46, 0.58, 0.36, 0.085), (-0.52, -0.46, 0.46, 0.32, 0.06)],
        ),
        "desert": (
            [(-0.54, 0.30, 1.30, 0.38, 0.22), (0.58, -0.34, 1.10, 0.33, 0.18), (0.00, 0.02, 0.74, 0.64, -0.06)],
            [(-0.12, 0.56, 1.36, 0.34, 0.20), (-0.20, -0.48, 1.22, 0.32, 0.17), (0.68, 0.02, 0.56, 0.40, -0.035)],
            [(-0.66, -0.18, 1.06, 0.36, 0.18), (0.18, 0.40, 1.30, 0.38, 0.22), (0.58, -0.54, 0.74, 0.34, 0.12), (0.04, -0.04, 0.66, 0.56, -0.055)],
            [(0.56, 0.34, 1.20, 0.38, 0.21), (-0.56, -0.40, 1.14, 0.34, 0.17), (-0.50, 0.52, 0.62, 0.32, 0.10), (0.02, 0.00, 0.70, 0.58, -0.05)],
        ),
        "snow": (
            [(-0.44, 0.34, 1.06, 0.52, 0.21), (0.58, -0.40, 0.82, 0.44, 0.13), (0.08, -0.02, 0.74, 0.58, -0.045)],
            [(-0.10, 0.56, 1.16, 0.44, 0.20), (-0.54, -0.42, 0.72, 0.40, 0.12), (0.60, -0.24, 0.66, 0.38, 0.10), (0.04, -0.02, 0.70, 0.56, -0.045)],
            [(0.46, 0.32, 1.08, 0.50, 0.20), (-0.52, 0.02, 0.74, 0.42, 0.12), (0.26, -0.58, 0.70, 0.38, 0.11), (0.02, -0.02, 0.70, 0.56, -0.05)],
            [(-0.34, -0.36, 1.04, 0.48, 0.18), (0.48, 0.46, 0.88, 0.44, 0.15), (-0.62, 0.52, 0.58, 0.34, 0.09), (0.08, 0.02, 0.72, 0.58, -0.045)],
        ),
        "forest": (
            [(-0.36, 0.32, 1.00, 0.56, 0.15), (0.56, -0.42, 0.78, 0.42, 0.08), (0.0, 0.0, 0.74, 0.62, -0.035)],
            [(0.42, 0.42, 0.94, 0.52, 0.14), (-0.58, -0.34, 0.78, 0.42, 0.09), (-0.10, 0.02, 0.70, 0.58, -0.035)],
            [(-0.52, 0.04, 0.90, 0.50, 0.14), (0.38, -0.52, 0.84, 0.44, 0.10), (0.48, 0.56, 0.56, 0.34, 0.07), (0.00, 0.00, 0.72, 0.60, -0.04)],
            [(0.18, 0.50, 1.00, 0.50, 0.15), (-0.44, -0.48, 0.74, 0.40, 0.09), (0.62, -0.18, 0.60, 0.36, 0.07), (0.02, -0.02, 0.72, 0.60, -0.035)],
        ),
    }
    source = archetypes.get(kind)
    if source is None:
        return angle, [(0.0, 0.0, 1.0, 0.7, 0.08)]

    # Preserve variant authorship while allowing a deterministic left/right mirror and
    # a very small seed offset. The offset is intentionally much smaller than a lobe.
    forms = []
    for cx, cy, rx, ry, h in source[v]:
        forms.append((
            cx * mirror + rng.uniform(-0.045, 0.045),
            cy + rng.uniform(-0.035, 0.035),
            rx * rng.uniform(0.96, 1.04),
            ry * rng.uniform(0.96, 1.04),
            h * rng.uniform(0.96, 1.04),
        ))
    return angle, forms


def _create_surface(kind: str, seed: int, variant: int, material) -> bpy.types.Object:
    outer = _hex_perimeter(6)
    rings = 10 if kind not in {"mountain", "peak"} else 11
    inner_scale = 0.14
    angle, forms = _shape_params(kind, seed, variant)
    shape_rng = random.Random(derive_seed(seed, "suite-v5-surface-jitter", kind, variant))
    verts: list[tuple[float, float, float]] = []
    for ring in range(rings):
        t = ring / max(1, rings - 1)
        scale = 1.0 + (inner_scale - 1.0) * t
        edge_t = min(1.0, max(0.0, (1.0 - scale) / 0.30))
        weight = edge_t * edge_t * (3.0 - 2.0 * edge_t)
        for p in outer:
            x, y = p.x * scale, p.y * scale
            if ring == 0:
                z = 0.0
            else:
                z = 0.012
                for i, (cx, cy, rx, ry, h) in enumerate(forms):
                    z += _elliptic(x, y, cx, cy, rx, ry, angle + i * 0.37, h, 1.42 + i * 0.08)
                # Biome-specific restrained secondary structure. Dunes are broad and directional;
                # snow uses gentle drift breakup rather than a noisy white plate.
                if kind == "desert":
                    z += math.sin((x * math.cos(angle) + y * math.sin(angle)) * 1.72 + variant) * 0.022
                elif kind == "snow":
                    z += math.sin(x * 1.12 - y * 0.68 + variant * 0.7) * 0.014
                elif kind == "plains":
                    z += math.sin(x * 0.82 + y * 0.36 + variant) * 0.010
                z = (z + shape_rng.uniform(-0.003, 0.003)) * weight
                limit = 0.48 if kind == "hills" else 0.30
                z = max(-0.06, min(limit, z))
            verts.append((x, y, z))
    # centre
    center = 0.012
    for i, (cx, cy, rx, ry, h) in enumerate(forms):
        center += _elliptic(0.0, 0.0, cx, cy, rx, ry, angle + i * 0.37, h, 1.42 + i * 0.08)
    center = max(-0.06, min(0.48 if kind == "hills" else 0.30, center))
    center_idx = len(verts)
    verts.append((0.0, 0.0, center))
    sectors = len(outer)
    faces = []
    for ring in range(rings - 1):
        a0, a1 = ring * sectors, (ring + 1) * sectors
        for i in range(sectors):
            j = (i + 1) % sectors
            faces.append((a0 + i, a0 + j, a1 + j, a1 + i))
    inner0 = (rings - 1) * sectors
    for i in range(sectors):
        j = (i + 1) % sectors
        faces.append((inner0 + i, inner0 + j, center_idx))
    obj = geo.make_mesh(f"VAE_Suite_{kind}_Surface", verts, faces)
    geo.set_material(obj, material)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj


def _create_land_base(kind: str, seed: int, variant: int, material) -> bpy.types.Object:
    mats = world_materials()
    geo.create_hex_prism("VAE_Suite_GeologyDark", -0.22, -0.63, mats["earth"])
    geo.create_hex_prism("VAE_Suite_GeologyWarm", -0.11, -0.24, mats["clay"])
    geo.create_hex_prism("VAE_Suite_Topsoil", -0.035, -0.12, mats["earth"])
    geo.create_hex_side_band("VAE_Suite_SurfaceRim", 0.0, -0.040, material)
    return _create_surface(kind, seed, variant, material)


def _ground(surface, x: float, y: float, lift: float = 0.012) -> float:
    return geo.surface_z_at(surface, x, y, 0.0) + lift


def _safe_point(rng: random.Random, ring: str, clearance: float, occupied: list[tuple[float,float,float]], spacing: float = 0.18):
    for _ in range(220):
        p = geo.random_hex_ring_point(rng, ring, clearance=clearance)
        if p is None:
            return None
        x, y = p
        if all(math.hypot(x-ox, y-oy) >= spacing + orad for ox,oy,orad in occupied):
            return x, y
    return None


def _add_rock(rng, surface, occupied, ring="mid", scale=0.85, warm=True):
    clearance = 0.34 * scale + 0.04
    p = _safe_point(rng, ring, clearance, occupied, 0.13)
    if not p: return
    x,y=p; occupied.append((x,y,0.27*scale))
    geo.create_terrain_rock_cluster(rng, (x,y,_ground(surface,x,y,0.012)), scale, warm=warm)


def _add_grass(rng, surface, occupied, ring="mid", scale=0.76, dry=False):
    p = _safe_point(rng, ring, 0.18*scale+0.035, occupied, 0.07)
    if not p: return
    x,y=p; occupied.append((x,y,0.13*scale))
    if dry:
        geo.create_grass_clump(rng, (x,y,_ground(surface,x,y,0.006)), scale=scale, dry=True)
    else:
        geo.create_terrain_ground_clump_v41(rng, (x,y,_ground(surface,x,y,0.006)), scale)


def _build_plains(seed: int, variant: int):
    mats = _suite_materials(); rng=random.Random(derive_seed(seed,"suite-plains",variant))
    surface=_create_land_base("plains",seed,variant,mats["plains_v5"]); occupied=[]
    for ring in ("mid","outer"): _add_rock(rng,surface,occupied,ring,rng.uniform(0.62,0.82),True)
    for ring in ("outer","mid","mid","inner","outer"): _add_grass(rng,surface,occupied,ring,rng.uniform(0.55,0.78),True)
    if rng.random()<0.55:
        p=_safe_point(rng,"mid",0.10,occupied,0.08)
        if p: geo.create_flower_cluster(rng,(p[0],p[1],_ground(surface,*p,0.020)),scale=0.58)


def _build_hills(seed: int, variant: int):
    mats=_suite_materials(); rng=random.Random(derive_seed(seed,"suite-hills",variant))
    surface=_create_land_base("hills",seed,variant,mats["hill_ground"]); occupied=[]
    direction=rng.uniform(0,TAU)
    x,y=(rng.uniform(-0.14,0.14),rng.uniform(-0.10,0.18))
    geo.create_hill_formation(rng,(x,y,_ground(surface,x,y,0.004)),scale=rng.uniform(0.82,0.96),direction_rad=direction)
    # second lower ridge makes Hills unmistakable from Meadow without becoming Mountain.
    sx,sy=(-math.sin(direction)*0.54, math.cos(direction)*0.54)
    if geo.hex_contains_disc(sx,sy,0.55):
        geo.create_hill_formation(rng,(sx,sy,_ground(surface,sx,sy,0.004)),scale=0.56,direction_rad=direction+rng.uniform(-0.38,0.38))
    for ring in ("outer","mid","mid"): _add_rock(rng,surface,occupied,ring,rng.uniform(0.50,0.70),True)
    for ring in ("outer","mid","inner","outer"): _add_grass(rng,surface,occupied,ring,rng.uniform(0.52,0.72),True)


def _build_mountain(seed: int, variant: int, peak: bool=False):
    kind="peak" if peak else "mountain"; mats=_suite_materials(); rng=random.Random(derive_seed(seed,"suite-"+kind,variant))
    surface=_create_land_base(kind,seed,variant,mats["mountain_ground"]); occupied=[]
    direction=rng.uniform(0,TAU)
    scale=rng.uniform(0.82,0.94) if peak else rng.uniform(0.88,1.00)
    x,y=(rng.uniform(-0.10,0.10),rng.uniform(-0.08,0.12))
    geo.create_mountain_formation(rng,(x,y,_ground(surface,x,y,0.004)),scale=scale,peak=peak,direction_rad=direction)
    # Secondary talus/readability zone kept sparse for peaks.
    for ring in (("mid",) if peak else ("mid","outer")):
        _add_rock(rng,surface,occupied,ring,rng.uniform(0.46,0.66),warm=not peak)
    if not peak:
        for ring in ("outer","mid"): _add_grass(rng,surface,occupied,ring,rng.uniform(0.44,0.62),True)


def _build_desert(seed: int, variant: int):
    mats=_suite_materials(); rng=random.Random(derive_seed(seed,"suite-desert",variant))
    surface=_create_land_base("desert",seed,variant,mats["desert"]); occupied=[]
    for ring in ("mid","outer"): _add_rock(rng,surface,occupied,ring,rng.uniform(0.55,0.78),True)
    # Desert remains intentionally sparse: 2-3 dry tufts total, no flower carpet.
    for ring in rng.sample(["outer","mid","mid","inner"],3): _add_grass(rng,surface,occupied,ring,rng.uniform(0.48,0.68),True)
    if rng.random()<0.55:
        p=_safe_point(rng,"mid",0.20,occupied,0.10)
        if p:
            geo.create_sculpted_rock(rng,(p[0],p[1],_ground(surface,*p,0.010)),scale=0.16,warm=True)


def _build_snow(seed: int, variant: int):
    mats=_suite_materials(); rng=random.Random(derive_seed(seed,"suite-snow",variant))
    surface=_create_land_base("snow",seed,variant,mats["snow_ground"]); occupied=[]
    for ring in ("mid","outer"): _add_rock(rng,surface,occupied,ring,rng.uniform(0.52,0.72),False)
    # Rare wind-bent tree: a visual accent, not a snow forest.
    if variant % 2 == 1:
        p=_safe_point(rng,"mid",0.45,occupied,0.18)
        if p:
            x,y=p; occupied.append((x,y,0.28)); geo.create_tree(rng,(x,y,_ground(surface,x,y,0.005)),"wind_bent",scale=0.62)


def _build_forest(seed: int, variant: int):
    mats=_suite_materials(); rng=random.Random(derive_seed(seed,"suite-forest",variant))
    surface=_create_land_base("forest",seed,variant,mats["forest_ground"]); occupied=[]
    # Variant-authored cluster plans avoid every forest reading as the same 4+3 tree pair.
    cluster_plans = (
        (("mid", 4), ("outer", 3)),
        (("outer", 3), ("mid", 3), ("mid", 2)),
        (("mid", 4), ("outer", 2)),
        (("outer", 3), ("mid", 2), ("outer", 2)),
    )
    cluster_centres=[]
    counts=[]
    for ring, count in cluster_plans[variant % 4]:
        p=_safe_point(rng,ring,0.48,occupied,0.25)
        if p:
            cluster_centres.append(p); counts.append(count); occupied.append((p[0],p[1],0.36))
    species=("broadleaf_round","broadleaf_columnar","conifer")
    for ci,(cx,cy) in enumerate(cluster_centres):
        count=counts[ci]
        for i in range(count):
            a=TAU*i/count+rng.uniform(-0.28,0.28); rr=rng.uniform(0.12,0.34)
            x,y=cx+math.cos(a)*rr,cy+math.sin(a)*rr
            if geo.hex_contains_disc(x,y,0.36):
                geo.create_tree(rng,(x,y,_ground(surface,x,y,0.006)),species[(i+variant+ci)%len(species)],scale=rng.uniform(0.76,0.96))
    for ring in ("outer","mid"): _add_rock(rng,surface,occupied,ring,rng.uniform(0.46,0.62),True)
    for ring in ("outer","mid","inner"): _add_grass(rng,surface,occupied,ring,rng.uniform(0.45,0.62),False)


def _build_water(seed: int, variant: int):
    rng=random.Random(derive_seed(seed,"suite-water",variant))
    open_sea = variant % 2 == 1
    kind="open_sea" if open_sea else "shallow_sea"
    geo.create_hex_base(kind,rng,variant=variant%4,terrain_seed=seed)
    # Final polish keeps broad quiet water and clustered curved glints only.
    geo.create_water_highlights(rng,open_sea=open_sea,count=3 if open_sea else 5)


def build_candidate_tile(kind: str, variant: int, seed: int, core_builder: Callable[[str,int,int],None]) -> None:
    """Build one local-space tile from the unified candidate vocabulary."""
    if kind == "meadow":
        core_builder("meadow", variant % 4, seed)
    elif kind == "plains": _build_plains(seed,variant)
    elif kind == "forest": _build_forest(seed,variant)
    elif kind == "hills": _build_hills(seed,variant)
    elif kind == "mountain": _build_mountain(seed,variant,False)
    elif kind == "peak": _build_mountain(seed,variant,True)
    elif kind == "desert": _build_desert(seed,variant)
    elif kind == "snow": _build_snow(seed,variant)
    elif kind == "water": _build_water(seed,variant)
    elif kind in SEA_KINDS:
        _build_water(seed, 1 if kind == "open_sea" else 0)
    else:
        raise ValueError(f"unknown Terrain Suite v5 kind: {kind}")


def _render_review(path: Path, blend_path: Path, *, ortho: float, strict: bool, resolution=(1920,1080)) -> None:
    render.assert_blender_version(strict)
    camera=render.setup_master_camera("terrain"); camera.data.ortho_scale=ortho
    render.setup_lighting(); path.parent.mkdir(parents=True,exist_ok=True)
    render.configure_render("terrain",path,transparent=False)
    scene=bpy.context.scene; scene.render.resolution_x=resolution[0]; scene.render.resolution_y=resolution[1]; scene.render.resolution_percentage=100
    bpy.ops.render.render(write_still=True); render.save_blend(blend_path)


def generate_family_review(family: str, seed: int, output: Path, strict: bool, core_builder: Callable[[str,int,int],None]) -> None:
    if family not in SUITE_FAMILIES:
        raise ValueError(family)
    if family == "coast":
        generate_coast_review(seed,output,strict,core_builder); return
    render.reset_scene()
    for idx,(q,r) in enumerate(FLOWER7):
        variant=idx % SUITE_VARIANTS[family]
        local_seed=derive_seed(seed,"suite-v5-family",family,idx,variant)
        before=set(bpy.context.scene.objects); build_candidate_tile(family,variant,local_seed,core_builder); _translate_new(before,q,r)
    _render_review(output/"review"/f"terrain_suite_v5_{family}_1920x1080.png", output/"review"/f"terrain_suite_v5_{family}.blend", ortho=11.4, strict=strict)


def generate_coast_review(seed: int, output: Path, strict: bool, core_builder: Callable[[str,int,int],None]) -> None:
    render.reset_scene()
    # Four land tiles against three water tiles: all three coast morphologies are visible.
    layout={(-1,0):"meadow",(-1,1):"meadow",(0,1):"plains",(0,0):"meadow",(1,0):"shallow_sea",(1,-1):"shallow_sea",(0,-1):"open_sea"}
    positions=[_world_pos(q,r) for q,r in layout]
    centre=(sum(x for x,_ in positions)/len(positions), sum(y for _,y in positions)/len(positions))
    coast_edge_counter=0
    forced_variants=(0,1,2,3,4)  # guarantees sandy / mixed / rocky in one review.
    for idx,((q,r),kind) in enumerate(layout.items()):
        before=set(bpy.context.scene.objects)
        build_candidate_tile(kind,idx%4,derive_seed(seed,"suite-coast-base",q,r),core_builder)
        if kind not in SEA_KINDS:
            for (dq,dr),edge in AXIAL_EDGE.items():
                if layout.get((q+dq,r+dr)) in SEA_KINDS:
                    cv=forced_variants[coast_edge_counter % len(forced_variants)] % COAST_VARIANT_COUNT
                    coast_edge_counter += 1
                    geo.create_coast_edge(edge,random.Random(coast_asset_seed(seed,cv,edge)),morphology=cv)
        _translate_new(before,q,r,centre)
    _render_review(output/"review"/"terrain_suite_v5_coast_1920x1080.png",output/"review"/"terrain_suite_v5_coast.blend",ortho=10.6,strict=strict)


def generate_all_family_reviews(seed: int, output: Path, strict: bool, core_builder: Callable[[str,int,int],None]) -> None:
    for family in SUITE_FAMILIES:
        generate_family_review(family,derive_seed(seed,"suite-family-root",family),output,strict,core_builder)


def generate_benchmark36(seed: int, output: Path, strict: bool, core_builder: Callable[[str,int,int],None]) -> None:
    render.reset_scene()
    layout: dict[tuple[int,int],str]={}
    for r,row in enumerate(BENCHMARK36):
        for q,kind in enumerate(row): layout[(q,r)]=kind
    positions=[_world_pos(q,r) for q,r in layout]
    centre=(sum(x for x,_ in positions)/len(positions), sum(y for _,y in positions)/len(positions))
    for idx,((q,r),kind) in enumerate(layout.items()):
        local_kind="water" if kind in SEA_KINDS else kind
        variant=idx % SUITE_VARIANTS.get(local_kind,4)
        local_seed=derive_seed(seed,"suite-v5-benchmark36",q,r,kind,variant)
        before=set(bpy.context.scene.objects)
        build_candidate_tile(kind,variant,local_seed,core_builder)
        if kind not in SEA_KINDS:
            for (dq,dr),edge in AXIAL_EDGE.items():
                if layout.get((q+dq,r+dr)) in SEA_KINDS:
                    cv=derive_seed(seed,"suite-v5-coast",q,r)%COAST_VARIANT_COUNT
                    geo.create_coast_edge(edge,random.Random(coast_asset_seed(seed,cv,edge)),morphology=cv)
        _translate_new(before,q,r,centre)
    # 36 tiles span more world-space than the accepted 30-hex baseline. 23.8 keeps
    # tall Peak silhouettes and corner tiles safely inside the 16:9 review frame.
    _render_review(output/"review"/"terrain_suite_v5_benchmark36_1920x1080.png",output/"review"/"terrain_suite_v5_benchmark36.blend",ortho=23.8,strict=strict)
