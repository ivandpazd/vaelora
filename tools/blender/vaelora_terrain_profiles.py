"""Authored open-terrain profiles for Vaelora Terrain v3/v4.1.

This module is bpy-free by design. It stores deterministic art-direction data used by
Blender generators and can also be inspected by host-side QA/tests.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Final

from vaelora_contract import derive_seed


@dataclass(frozen=True)
class LandformSpec:
    """One authored elliptical terrain mass in tile-local XY space.

    Positive height raises terrain; negative height carves a basin. rotation_deg rotates
    the ellipse in tile space. falloff controls how tightly the form decays.
    """

    x: float
    y: float
    radius_x: float
    radius_y: float
    height: float
    rotation_deg: float = 0.0
    falloff: float = 1.45


@dataclass(frozen=True)
class RidgeSplineSpec:
    """Authored directional ridge defined by a short polyline in tile-local XY."""

    points: tuple[tuple[float, float], ...]
    width_left: float
    width_right: float
    height: float
    shoulder: float = 0.28
    falloff: float = 1.55


@dataclass(frozen=True)
class ColorMaskSpec:
    """Elliptical authoring mask baked into the terrain surface vertex color."""

    x: float
    y: float
    radius_x: float
    radius_y: float
    channel: str  # sun | earth | cool
    strength: float
    rotation_deg: float = 0.0
    falloff: float = 1.45


@dataclass(frozen=True)
class SurfaceSwatchSpec:
    x: float
    y: float
    radius_x: float
    radius_y: float
    material_key: str
    rotation_deg: float = 0.0
    lift: float = 0.0055


@dataclass(frozen=True)
class ScatterAnchorSpec:
    """Authored composition anchor for readable micro/meso terrain detail."""

    x: float
    y: float
    role: str
    scale: float = 1.0
    dry: bool = False


@dataclass(frozen=True)
class TerrainVariantProfile:
    landforms: tuple[LandformSpec, ...]
    swatches: tuple[SurfaceSwatchSpec, ...]
    scatter: tuple[ScatterAnchorSpec, ...]
    ridges: tuple[RidgeSplineSpec, ...] = ()
    color_masks: tuple[ColorMaskSpec, ...] = ()


@dataclass(frozen=True)
class TerrainProfile:
    kind: str
    base_material_key: str
    micro_height: float
    crown_height: float
    ring_count: int
    perimeter_subdivisions: int
    variants: tuple[TerrainVariantProfile, ...]
    system_version: int = 3


@dataclass(frozen=True)
class TerrainVariationContext:
    """Stable seed-derived composition transform for Terrain v4.3.

    The context changes the *composition* without changing the logical hex footprint:
    ridges/masks are rotated, mirrored, shifted and gently scaled inside the tile.
    It is deterministic for (kind, variant, seed), so generated runtime sprites remain
    reproducible and reviewable.
    """

    rotation_deg: float
    mirror_x: bool
    offset_x: float
    offset_y: float
    macro_scale: float
    height_scale: float
    scatter_phase_rad: float


def terrain_variation_context(kind: str, variant: int, seed: int) -> TerrainVariationContext:
    """Return a deterministic, bounded composition transform.

    Meadow v4.3 deliberately permits sizeable composition movement because the old
    system kept its main ridge and detail cluster in recognisably similar places.
    Other terrain families receive an identity context for backwards compatibility.
    """
    if kind != "meadow":
        return TerrainVariationContext(0.0, False, 0.0, 0.0, 1.0, 1.0, 0.0)

    rng = random.Random(derive_seed(seed, "terrain-v43", kind, variant))
    # Hex-friendly coarse rotations plus a small authored-looking drift avoid a
    # recognisable fixed ridge orientation while preserving large readable forms.
    coarse = rng.choice((0.0, 60.0, 120.0, 180.0, 240.0, 300.0))
    rotation = coarse + rng.uniform(-13.0, 13.0)
    angle = math.radians(rng.uniform(0.0, 360.0))
    offset_mag = rng.uniform(0.04, 0.28)
    return TerrainVariationContext(
        rotation_deg=rotation,
        mirror_x=rng.random() < 0.50,
        offset_x=math.cos(angle) * offset_mag,
        offset_y=math.sin(angle) * offset_mag,
        macro_scale=rng.uniform(0.90, 1.10),
        height_scale=rng.uniform(0.88, 1.12),
        scatter_phase_rad=rng.uniform(0.0, math.tau),
    )


# Terrain v3 art-direction goals:
# - one dominant macro landform with enough vertical range to read at 30° elevation;
# - one support form + one quiet basin, never equal-frequency noise everywhere;
# - vivid but coherent green/yellow-green palette;
# - hero rocks/grass large enough to survive 256x128 runtime sprites;
# - exact z=0 perimeter retained by the geometry builder.

MEADOW_V3: Final[TerrainProfile] = TerrainProfile(
    kind="meadow",
    base_material_key="meadow_v3",
    micro_height=0.014,
    crown_height=0.030,
    ring_count=10,
    perimeter_subdivisions=5,
    variants=(
        TerrainVariantProfile(
            landforms=(
                LandformSpec(0.35, 0.50, 1.00, 0.58, 0.44, 18.0, 1.30),
                LandformSpec(0.68, -0.52, 0.66, 0.40, 0.20, -18.0, 1.55),
                LandformSpec(-0.38, -0.28, 0.80, 0.68, -0.11, 12.0, 1.55),
                LandformSpec(-0.72, 0.46, 0.58, 0.46, 0.12, 42.0, 1.70),
            ),
            swatches=(
                SurfaceSwatchSpec(0.22, 0.58, 0.76, 0.30, "meadow_sun", 16.0),
                SurfaceSwatchSpec(-0.36, -0.24, 0.62, 0.34, "meadow_cool", -22.0),
                SurfaceSwatchSpec(0.62, -0.46, 0.42, 0.19, "meadow_warm", -12.0),
                SurfaceSwatchSpec(0.24, 0.34, 0.28, 0.11, "earth_light", 22.0, 0.006),
                SurfaceSwatchSpec(-0.58, -0.72, 0.25, 0.10, "earth_light", -8.0, 0.006),
            ),
            scatter=(
                ScatterAnchorSpec(-0.88, -0.66, "hero_grass", 1.35),
                ScatterAnchorSpec(0.78, 0.02, "hero_grass", 1.22),
                ScatterAnchorSpec(-0.74, 0.38, "grass", 0.95),
                ScatterAnchorSpec(0.16, 0.88, "grass", 0.88),
                ScatterAnchorSpec(0.76, -0.68, "rock_cluster", 1.10),
                ScatterAnchorSpec(-0.74, 0.02, "rock_cluster", 1.18),
                ScatterAnchorSpec(0.26, -0.60, "flower", 1.08),
                ScatterAnchorSpec(-0.32, 0.58, "flower", 0.82),
                ScatterAnchorSpec(0.00, -0.08, "leaf_patch", 1.00),
                ScatterAnchorSpec(0.48, 0.34, "leaf_patch", 0.90),
            ),
        ),
        TerrainVariantProfile(
            landforms=(
                LandformSpec(-0.48, 0.42, 0.96, 0.60, 0.42, 66.0, 1.34),
                LandformSpec(0.60, 0.58, 0.68, 0.44, 0.18, 18.0, 1.60),
                LandformSpec(0.26, -0.42, 0.78, 0.65, -0.10, -20.0, 1.55),
                LandformSpec(-0.54, -0.66, 0.54, 0.42, 0.14, 10.0, 1.65),
            ),
            swatches=(
                SurfaceSwatchSpec(-0.44, 0.48, 0.70, 0.28, "meadow_sun", 62.0),
                SurfaceSwatchSpec(0.28, -0.34, 0.62, 0.32, "meadow_cool", 12.0),
                SurfaceSwatchSpec(-0.50, -0.60, 0.42, 0.20, "meadow_warm", -14.0),
                SurfaceSwatchSpec(-0.22, 0.26, 0.26, 0.11, "earth_light", 55.0, 0.006),
            ),
            scatter=(
                ScatterAnchorSpec(0.82, -0.62, "hero_grass", 1.30),
                ScatterAnchorSpec(-0.82, 0.10, "hero_grass", 1.18),
                ScatterAnchorSpec(0.70, 0.38, "grass", 0.96),
                ScatterAnchorSpec(-0.22, 0.88, "grass", 0.88),
                ScatterAnchorSpec(-0.64, -0.62, "rock_cluster", 1.15),
                ScatterAnchorSpec(0.68, 0.58, "rock_cluster", 1.02),
                ScatterAnchorSpec(0.24, -0.58, "flower", 1.04),
                ScatterAnchorSpec(-0.32, 0.36, "flower", 0.86),
                ScatterAnchorSpec(0.10, 0.08, "leaf_patch", 1.05),
            ),
        ),
        TerrainVariantProfile(
            landforms=(
                LandformSpec(0.10, -0.52, 1.06, 0.58, 0.43, 126.0, 1.30),
                LandformSpec(-0.66, 0.56, 0.62, 0.44, 0.19, 36.0, 1.56),
                LandformSpec(0.50, 0.22, 0.82, 0.64, -0.11, 18.0, 1.52),
                LandformSpec(0.72, 0.72, 0.48, 0.38, 0.12, 84.0, 1.70),
            ),
            swatches=(
                SurfaceSwatchSpec(0.02, -0.46, 0.76, 0.30, "meadow_sun", 124.0),
                SurfaceSwatchSpec(0.48, 0.18, 0.60, 0.34, "meadow_cool", 10.0),
                SurfaceSwatchSpec(-0.60, 0.56, 0.40, 0.20, "meadow_warm", 28.0),
                SurfaceSwatchSpec(0.24, -0.18, 0.30, 0.10, "earth_light", 120.0, 0.006),
            ),
            scatter=(
                ScatterAnchorSpec(-0.72, -0.72, "hero_grass", 1.28),
                ScatterAnchorSpec(0.74, 0.48, "hero_grass", 1.16),
                ScatterAnchorSpec(-0.68, 0.42, "grass", 0.92),
                ScatterAnchorSpec(0.30, -0.88, "grass", 0.88),
                ScatterAnchorSpec(-0.56, 0.58, "rock_cluster", 1.18),
                ScatterAnchorSpec(0.68, -0.18, "rock_cluster", 1.04),
                ScatterAnchorSpec(0.16, 0.54, "flower", 1.05),
                ScatterAnchorSpec(-0.32, -0.44, "flower", 0.84),
                ScatterAnchorSpec(0.02, 0.08, "leaf_patch", 1.00),
            ),
        ),
        TerrainVariantProfile(
            landforms=(
                LandformSpec(-0.26, 0.54, 1.00, 0.56, 0.45, 206.0, 1.28),
                LandformSpec(0.64, -0.48, 0.66, 0.42, 0.18, 152.0, 1.58),
                LandformSpec(-0.32, -0.30, 0.80, 0.64, -0.10, 24.0, 1.56),
                LandformSpec(0.72, 0.56, 0.46, 0.36, 0.13, 8.0, 1.70),
            ),
            swatches=(
                SurfaceSwatchSpec(-0.20, 0.50, 0.74, 0.29, "meadow_sun", 204.0),
                SurfaceSwatchSpec(-0.28, -0.26, 0.60, 0.32, "meadow_cool", 22.0),
                SurfaceSwatchSpec(0.58, -0.44, 0.42, 0.20, "meadow_warm", 154.0),
                SurfaceSwatchSpec(-0.06, 0.26, 0.28, 0.10, "earth_light", 200.0, 0.006),
            ),
            scatter=(
                ScatterAnchorSpec(0.76, -0.66, "hero_grass", 1.34),
                ScatterAnchorSpec(-0.80, 0.02, "hero_grass", 1.16),
                ScatterAnchorSpec(0.56, 0.58, "grass", 0.94),
                ScatterAnchorSpec(-0.28, -0.82, "grass", 0.88),
                ScatterAnchorSpec(-0.68, 0.50, "rock_cluster", 1.16),
                ScatterAnchorSpec(0.62, -0.34, "rock_cluster", 1.04),
                ScatterAnchorSpec(0.18, 0.48, "flower", 1.00),
                ScatterAnchorSpec(-0.42, -0.40, "flower", 0.84),
                ScatterAnchorSpec(0.00, 0.04, "leaf_patch", 1.00),
            ),
        ),
    ),
)


MEADOW_V4: Final[TerrainProfile] = TerrainProfile(
    kind="meadow",
    base_material_key="meadow_v4",
    micro_height=0.008,
    crown_height=0.018,
    ring_count=12,
    perimeter_subdivisions=6,
    system_version=4,
    variants=(
        TerrainVariantProfile(
            landforms=(
                LandformSpec(-0.48, -0.08, 0.82, 0.72, -0.12, 8.0, 1.65),
                LandformSpec(0.78, -0.58, 0.62, 0.42, 0.16, -12.0, 1.70),
            ),
            ridges=(
                RidgeSplineSpec(((-1.12, 0.42), (-0.42, 0.63), (0.30, 0.76), (1.06, 0.52)), 0.42, 0.66, 0.58, 0.30, 1.48),
                RidgeSplineSpec(((-0.18, -0.70), (0.42, -0.54), (1.04, -0.28)), 0.34, 0.46, 0.26, 0.24, 1.62),
            ),
            # v4.1 Painterly Surface: broad sun/cool masses plus narrow erosion marks.
            # The masks live on the terrain mesh itself; no flat overlay polygons.
            color_masks=(
                ColorMaskSpec(0.08, 0.60, 1.42, 0.54, "sun", 1.02, 10.0, 1.30),
                ColorMaskSpec(0.58, -0.46, 0.96, 0.34, "sun", 0.86, -12.0, 1.38),
                ColorMaskSpec(-0.70, 0.12, 0.74, 0.22, "sun", 0.38, 20.0, 1.54),
                ColorMaskSpec(0.18, 0.44, 0.72, 0.15, "earth", 0.90, 18.0, 1.62),
                ColorMaskSpec(0.52, -0.42, 0.58, 0.12, "earth", 0.78, -10.0, 1.66),
                ColorMaskSpec(-0.64, -0.54, 0.34, 0.09, "earth", 0.56, -8.0, 1.74),
                ColorMaskSpec(-0.04, -0.08, 0.40, 0.10, "earth", 0.34, 48.0, 1.82),
                ColorMaskSpec(-0.42, -0.10, 1.06, 0.80, "cool", 0.96, 4.0, 1.34),
                ColorMaskSpec(0.74, 0.18, 0.56, 0.28, "cool", 0.28, -20.0, 1.52),
            ),
            swatches=(),
            # Composition hierarchy: 3 hero accents, low clumps and groundcover fill
            # the surface without uniformly scattering noise everywhere.
            scatter=(
                # v4.2: detail is intentionally spread around the tile instead of
                # forming a central ring. Outer anchors frame the macro landforms.
                ScatterAnchorSpec(-1.02, -0.60, "hero_grass", 1.08),
                ScatterAnchorSpec(0.94, 0.30, "hero_grass", 1.02),
                ScatterAnchorSpec(-0.18, 0.98, "hero_grass", 0.86),
                ScatterAnchorSpec(-0.84, 0.58, "medium_clump", 0.96),
                ScatterAnchorSpec(0.46, 0.76, "medium_clump", 0.88),
                ScatterAnchorSpec(-0.40, -0.72, "medium_clump", 0.96),
                ScatterAnchorSpec(0.88, -0.24, "medium_clump", 0.84),
                ScatterAnchorSpec(-0.96, -0.08, "medium_clump", 0.82),
                ScatterAnchorSpec(-0.76, 0.04, "rock_garden", 1.18),
                ScatterAnchorSpec(0.70, -0.70, "rock_garden", 1.10),
                ScatterAnchorSpec(-1.00, 0.30, "groundcover", 0.82),
                ScatterAnchorSpec(-0.52, 0.24, "groundcover", 0.88),
                ScatterAnchorSpec(0.12, -0.34, "groundcover", 0.92),
                ScatterAnchorSpec(0.62, 0.58, "groundcover", 0.86),
                ScatterAnchorSpec(0.96, -0.52, "groundcover", 0.76),
                ScatterAnchorSpec(0.18, 0.66, "groundcover", 0.80),
                ScatterAnchorSpec(-0.46, 0.66, "flower", 0.88),
                ScatterAnchorSpec(0.18, -0.76, "flower", 0.98),
                ScatterAnchorSpec(0.72, 0.12, "flower", 0.76),
                ScatterAnchorSpec(-0.98, 0.40, "flower", 0.70),
            ),
        ),
        TerrainVariantProfile(
            landforms=(LandformSpec(0.38, -0.28, 0.82, 0.66, -0.10, 0.0, 1.65),),
            ridges=(RidgeSplineSpec(((-1.00, -0.20), (-0.32, 0.18), (0.36, 0.54), (0.98, 0.72)), 0.50, 0.40, 0.54, 0.28, 1.50), RidgeSplineSpec(((-0.90, 0.68), (-0.28, 0.56), (0.28, 0.34)), 0.30, 0.42, 0.22, 0.20, 1.65)),
            color_masks=(
                ColorMaskSpec(-0.12, 0.38, 1.18, 0.42, "sun", 0.92, 32.0, 1.34),
                ColorMaskSpec(0.58, 0.60, 0.82, 0.24, "sun", 0.42, 18.0, 1.56),
                ColorMaskSpec(0.02, 0.28, 0.70, 0.18, "earth", 0.66, 34.0, 1.68),
                ColorMaskSpec(-0.46, -0.14, 0.38, 0.10, "earth", 0.30, -18.0, 1.82),
                ColorMaskSpec(0.38, -0.26, 0.94, 0.68, "cool", 0.62, 0.0, 1.36),
                ColorMaskSpec(-0.72, 0.14, 0.60, 0.26, "cool", 0.26, 28.0, 1.56),
            ),
            swatches=(),
            scatter=MEADOW_V3.variants[1].scatter,
        ),
        TerrainVariantProfile(
            landforms=(LandformSpec(0.42, 0.18, 0.80, 0.64, -0.10, 0.0, 1.65),),
            ridges=(RidgeSplineSpec(((-0.92, 0.74), (-0.44, 0.30), (0.08, -0.08), (0.74, -0.54)), 0.44, 0.58, 0.56, 0.30, 1.48), RidgeSplineSpec(((-0.78, -0.50), (-0.18, -0.62), (0.42, -0.50)), 0.32, 0.44, 0.23, 0.20, 1.66)),
            color_masks=(
                ColorMaskSpec(-0.18, 0.10, 1.12, 0.42, "sun", 0.90, -38.0, 1.34),
                ColorMaskSpec(-0.70, 0.56, 0.70, 0.22, "sun", 0.36, 16.0, 1.54),
                ColorMaskSpec(0.02, 0.02, 0.66, 0.16, "earth", 0.62, -38.0, 1.68),
                ColorMaskSpec(0.42, -0.26, 0.36, 0.10, "earth", 0.28, -8.0, 1.82),
                ColorMaskSpec(0.46, 0.22, 0.92, 0.68, "cool", 0.62, 0.0, 1.36),
                ColorMaskSpec(-0.42, -0.48, 0.52, 0.28, "cool", 0.24, -26.0, 1.52),
            ),
            swatches=(),
            scatter=MEADOW_V3.variants[2].scatter,
        ),
        TerrainVariantProfile(
            landforms=(LandformSpec(-0.34, -0.24, 0.82, 0.66, -0.10, 0.0, 1.65),),
            ridges=(RidgeSplineSpec(((-1.06, 0.54), (-0.36, 0.70), (0.42, 0.62), (1.02, 0.20)), 0.40, 0.62, 0.57, 0.30, 1.48), RidgeSplineSpec(((-0.52, -0.76), (0.02, -0.52), (0.66, -0.38)), 0.34, 0.46, 0.24, 0.20, 1.64)),
            color_masks=(
                ColorMaskSpec(-0.02, 0.56, 1.14, 0.42, "sun", 0.94, 6.0, 1.34),
                ColorMaskSpec(0.62, 0.42, 0.74, 0.24, "sun", 0.38, -18.0, 1.54),
                ColorMaskSpec(0.12, 0.48, 0.66, 0.16, "earth", 0.64, 8.0, 1.68),
                ColorMaskSpec(-0.46, -0.44, 0.38, 0.10, "earth", 0.30, -26.0, 1.82),
                ColorMaskSpec(-0.34, -0.20, 0.94, 0.68, "cool", 0.64, 0.0, 1.36),
                ColorMaskSpec(0.44, -0.10, 0.58, 0.24, "cool", 0.22, 30.0, 1.54),
            ),
            swatches=(),
            scatter=MEADOW_V3.variants[3].scatter,
        ),
    ),
)


PLAINS_V3: Final[TerrainProfile] = TerrainProfile(
    kind="plains",
    base_material_key="plains_v3",
    micro_height=0.012,
    crown_height=0.026,
    ring_count=10,
    perimeter_subdivisions=5,
    variants=(
        TerrainVariantProfile(
            landforms=(
                LandformSpec(0.26, 0.54, 1.10, 0.52, 0.38, 8.0, 1.36),
                LandformSpec(0.66, -0.48, 0.76, 0.38, 0.17, -18.0, 1.58),
                LandformSpec(-0.40, -0.28, 0.88, 0.62, -0.08, 12.0, 1.58),
                LandformSpec(-0.72, 0.50, 0.58, 0.38, 0.10, 42.0, 1.72),
            ),
            swatches=(
                SurfaceSwatchSpec(0.20, 0.52, 0.82, 0.28, "plains_sun", 8.0),
                SurfaceSwatchSpec(-0.34, -0.24, 0.66, 0.32, "plains_green", -18.0),
                SurfaceSwatchSpec(0.60, -0.44, 0.48, 0.18, "plains_warm", -12.0),
                SurfaceSwatchSpec(0.24, 0.28, 0.34, 0.11, "earth_light", 18.0, 0.006),
                SurfaceSwatchSpec(-0.56, -0.66, 0.28, 0.10, "earth", -4.0, 0.006),
            ),
            scatter=(
                ScatterAnchorSpec(-0.84, -0.66, "hero_grass", 1.28, True),
                ScatterAnchorSpec(0.76, 0.00, "hero_grass", 1.16, True),
                ScatterAnchorSpec(-0.70, 0.40, "grass", 0.90, True),
                ScatterAnchorSpec(0.18, 0.86, "grass", 0.84, True),
                ScatterAnchorSpec(0.72, -0.62, "rock_cluster", 1.10, True),
                ScatterAnchorSpec(-0.72, 0.00, "rock_cluster", 1.14, True),
                ScatterAnchorSpec(0.20, -0.56, "flower", 0.82, True),
                ScatterAnchorSpec(0.04, 0.02, "leaf_patch", 0.82, True),
            ),
        ),
        TerrainVariantProfile(
            landforms=(
                LandformSpec(-0.48, 0.46, 1.06, 0.52, 0.37, 56.0, 1.38),
                LandformSpec(0.58, 0.58, 0.72, 0.40, 0.15, 18.0, 1.60),
                LandformSpec(0.24, -0.40, 0.88, 0.62, -0.08, -16.0, 1.58),
                LandformSpec(-0.58, -0.68, 0.54, 0.36, 0.11, 8.0, 1.70),
            ),
            swatches=(
                SurfaceSwatchSpec(-0.40, 0.44, 0.78, 0.27, "plains_sun", 56.0),
                SurfaceSwatchSpec(0.26, -0.34, 0.64, 0.32, "plains_green", 10.0),
                SurfaceSwatchSpec(-0.52, -0.60, 0.44, 0.18, "plains_warm", -12.0),
                SurfaceSwatchSpec(-0.20, 0.26, 0.32, 0.11, "earth_light", 50.0, 0.006),
            ),
            scatter=(
                ScatterAnchorSpec(0.82, -0.60, "hero_grass", 1.26, True),
                ScatterAnchorSpec(-0.82, 0.08, "hero_grass", 1.14, True),
                ScatterAnchorSpec(0.68, 0.38, "grass", 0.88, True),
                ScatterAnchorSpec(-0.20, 0.84, "grass", 0.84, True),
                ScatterAnchorSpec(-0.64, -0.60, "rock_cluster", 1.12, True),
                ScatterAnchorSpec(0.66, 0.54, "rock_cluster", 1.00, True),
                ScatterAnchorSpec(0.18, -0.58, "flower", 0.80, True),
                ScatterAnchorSpec(0.08, 0.06, "leaf_patch", 0.80, True),
            ),
        ),
        TerrainVariantProfile(
            landforms=(
                LandformSpec(0.08, -0.54, 1.10, 0.52, 0.39, 116.0, 1.34),
                LandformSpec(-0.64, 0.54, 0.70, 0.40, 0.16, 34.0, 1.60),
                LandformSpec(0.48, 0.20, 0.88, 0.62, -0.08, 16.0, 1.58),
                LandformSpec(0.70, 0.72, 0.50, 0.34, 0.10, 80.0, 1.72),
            ),
            swatches=(
                SurfaceSwatchSpec(0.02, -0.48, 0.80, 0.28, "plains_sun", 116.0),
                SurfaceSwatchSpec(0.46, 0.18, 0.62, 0.30, "plains_green", 12.0),
                SurfaceSwatchSpec(-0.58, 0.54, 0.42, 0.18, "plains_warm", 26.0),
                SurfaceSwatchSpec(0.20, -0.18, 0.32, 0.11, "earth_light", 112.0, 0.006),
            ),
            scatter=(
                ScatterAnchorSpec(-0.72, -0.72, "hero_grass", 1.24, True),
                ScatterAnchorSpec(0.72, 0.46, "hero_grass", 1.12, True),
                ScatterAnchorSpec(-0.66, 0.40, "grass", 0.86, True),
                ScatterAnchorSpec(0.28, -0.86, "grass", 0.82, True),
                ScatterAnchorSpec(-0.56, 0.56, "rock_cluster", 1.12, True),
                ScatterAnchorSpec(0.66, -0.18, "rock_cluster", 1.00, True),
                ScatterAnchorSpec(0.14, 0.54, "flower", 0.82, True),
                ScatterAnchorSpec(0.00, 0.06, "leaf_patch", 0.80, True),
            ),
        ),
        TerrainVariantProfile(
            landforms=(
                LandformSpec(-0.24, 0.54, 1.08, 0.50, 0.39, 172.0, 1.34),
                LandformSpec(0.62, -0.46, 0.72, 0.38, 0.16, 148.0, 1.60),
                LandformSpec(-0.30, -0.28, 0.86, 0.62, -0.08, 22.0, 1.58),
                LandformSpec(0.70, 0.54, 0.48, 0.34, 0.11, 8.0, 1.70),
            ),
            swatches=(
                SurfaceSwatchSpec(-0.18, 0.50, 0.80, 0.28, "plains_sun", 172.0),
                SurfaceSwatchSpec(-0.28, -0.24, 0.62, 0.30, "plains_green", 18.0),
                SurfaceSwatchSpec(0.56, -0.42, 0.44, 0.18, "plains_warm", 148.0),
                SurfaceSwatchSpec(-0.06, 0.24, 0.32, 0.11, "earth_light", 168.0, 0.006),
            ),
            scatter=(
                ScatterAnchorSpec(0.76, -0.66, "hero_grass", 1.28, True),
                ScatterAnchorSpec(-0.80, 0.02, "hero_grass", 1.12, True),
                ScatterAnchorSpec(0.54, 0.56, "grass", 0.88, True),
                ScatterAnchorSpec(-0.26, -0.82, "grass", 0.84, True),
                ScatterAnchorSpec(-0.66, 0.48, "rock_cluster", 1.14, True),
                ScatterAnchorSpec(0.60, -0.32, "rock_cluster", 1.02, True),
                ScatterAnchorSpec(0.16, 0.46, "flower", 0.80, True),
                ScatterAnchorSpec(0.00, 0.04, "leaf_patch", 0.80, True),
            ),
        ),
    ),
)


TERRAIN_PROFILES: Final[dict[str, TerrainProfile]] = {
    "meadow": MEADOW_V4,
    "plains": PLAINS_V3,
}


def terrain_profile(kind: str) -> TerrainProfile:
    return TERRAIN_PROFILES[kind]
