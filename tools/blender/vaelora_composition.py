"""Authored composition grammar for Vaelora Sculpted Diorama v0.3.2-r2.

The generator is procedural, but composition is not random scatter. This module keeps
visual grammar in named templates so review can compare like-for-like across revisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class Anchor:
    x: float
    y: float
    scale: float = 1.0
    role: str = "support"
    rotation_deg: float = 0.0


# Screen-space aware forest arrangements. The lower/front central region stays open.
FOREST_TEMPLATES: Final[tuple[tuple[Anchor, ...], ...]] = (
    (
        Anchor(-0.92, 0.48, 0.90, "support"), Anchor(-0.50, 0.90, 1.06, "hero"),
        Anchor(0.02, 1.00, 0.88, "support"), Anchor(0.70, 0.73, 1.00, "hero"),
        Anchor(1.00, 0.16, 0.78, "edge"), Anchor(-0.98, -0.08, 0.80, "edge"),
        Anchor(0.64, -0.56, 0.82, "edge"),
    ),
    (
        Anchor(-0.84, 0.72, 1.04, "hero"), Anchor(-0.24, 0.96, 0.82, "support"),
        Anchor(0.42, 0.93, 0.96, "hero"), Anchor(0.93, 0.48, 0.79, "edge"),
        Anchor(-1.02, 0.05, 0.77, "edge"), Anchor(0.87, -0.28, 0.86, "support"),
        Anchor(-0.52, -0.58, 0.80, "edge"),
    ),
    (
        Anchor(-0.95, 0.35, 0.86, "support"), Anchor(-0.60, 0.86, 1.03, "hero"),
        Anchor(0.00, 1.02, 0.82, "support"), Anchor(0.60, 0.87, 0.98, "hero"),
        Anchor(0.98, 0.30, 0.80, "edge"), Anchor(-0.82, -0.35, 0.76, "edge"),
        Anchor(0.72, -0.50, 0.83, "edge"),
    ),
    (
        Anchor(-0.90, 0.60, 0.94, "support"), Anchor(-0.32, 0.98, 1.08, "hero"),
        Anchor(0.31, 0.93, 0.84, "support"), Anchor(0.88, 0.57, 0.97, "hero"),
        Anchor(1.00, -0.02, 0.76, "edge"), Anchor(-0.95, -0.20, 0.78, "edge"),
        Anchor(0.48, -0.63, 0.81, "edge"),
    ),
)



# Authored open-terrain compositions. These are deliberately sparse: variation is
# compositional first, stochastic second. Roles are interpreted by the terrain kit.
MEADOW_TEMPLATES: Final[tuple[tuple[Anchor, ...], ...]] = (
    (Anchor(-0.92, 0.52, 0.92, "grass"), Anchor(0.72, 0.74, 0.88, "grass"), Anchor(0.96, -0.32, 0.78, "grass"), Anchor(-0.60, -0.64, 0.76, "grass"), Anchor(-0.18, 0.92, 0.85, "flower"), Anchor(0.62, 0.15, 0.78, "flower")),
    (Anchor(-0.78, 0.74, 0.88, "grass"), Anchor(0.18, 0.94, 0.90, "grass"), Anchor(0.92, 0.42, 0.76, "grass"), Anchor(0.74, -0.62, 0.74, "grass"), Anchor(-0.82, -0.32, 0.74, "grass"), Anchor(0.28, 0.45, 0.82, "flower"), Anchor(-0.28, -0.78, 0.72, "rock")),
    (Anchor(-0.94, 0.16, 0.78, "grass"), Anchor(-0.52, 0.82, 0.90, "grass"), Anchor(0.42, 0.88, 0.88, "grass"), Anchor(0.92, 0.10, 0.76, "grass"), Anchor(0.52, -0.72, 0.74, "grass"), Anchor(-0.20, 0.48, 0.82, "flower"), Anchor(0.76, 0.54, 0.74, "flower")),
    (Anchor(-0.86, 0.58, 0.88, "grass"), Anchor(0.02, 0.96, 0.92, "grass"), Anchor(0.86, 0.62, 0.80, "grass"), Anchor(0.94, -0.30, 0.72, "grass"), Anchor(-0.72, -0.56, 0.76, "grass"), Anchor(-0.34, 0.18, 0.78, "flower"), Anchor(0.58, -0.56, 0.70, "rock")),
)

PLAINS_TEMPLATES: Final[tuple[tuple[Anchor, ...], ...]] = (
    (Anchor(-0.96, 0.58, 0.90, "dry"), Anchor(-0.42, 0.78, 0.82, "dry"), Anchor(0.26, 0.84, 0.86, "dry"), Anchor(0.88, 0.42, 0.80, "dry"), Anchor(0.78, -0.52, 0.72, "dry"), Anchor(-0.74, -0.54, 0.74, "dry"), Anchor(0.30, 0.20, 0.70, "earth")),
    (Anchor(-0.82, 0.82, 0.90, "dry"), Anchor(-0.10, 0.92, 0.82, "dry"), Anchor(0.64, 0.70, 0.86, "dry"), Anchor(0.94, -0.10, 0.72, "dry"), Anchor(0.42, -0.76, 0.78, "dry"), Anchor(-0.72, -0.48, 0.76, "dry"), Anchor(-0.16, 0.12, 0.72, "rock")),
    (Anchor(-0.94, 0.28, 0.82, "dry"), Anchor(-0.48, 0.88, 0.88, "dry"), Anchor(0.20, 0.94, 0.80, "dry"), Anchor(0.88, 0.54, 0.86, "dry"), Anchor(0.78, -0.44, 0.72, "dry"), Anchor(-0.60, -0.64, 0.74, "dry"), Anchor(0.38, 0.12, 0.70, "earth"), Anchor(-0.28, 0.46, 0.68, "rock")),
    (Anchor(-0.84, 0.70, 0.86, "dry"), Anchor(-0.18, 0.90, 0.90, "dry"), Anchor(0.58, 0.82, 0.84, "dry"), Anchor(0.94, 0.08, 0.74, "dry"), Anchor(0.56, -0.70, 0.78, "dry"), Anchor(-0.78, -0.36, 0.72, "dry"), Anchor(0.10, 0.24, 0.72, "earth")),
)



# Terrain v2 broad painterly swatches. These are intentionally large, sparse and
# authored per finite variant so tonal variation follows composition rather than
# random scatter. rotation_deg gives the dominant brush direction.
MEADOW_SURFACE_SWATCHES: Final[tuple[tuple[Anchor, ...], ...]] = (
    (Anchor(-0.52, 0.34, 0.95, "warm", 18.0), Anchor(0.58, -0.34, 0.78, "cool", -22.0), Anchor(0.18, 0.72, 0.52, "warm", 42.0)),
    (Anchor(-0.66, -0.18, 0.82, "cool", 28.0), Anchor(0.42, 0.42, 0.94, "warm", 8.0), Anchor(0.64, -0.58, 0.46, "earth", -18.0)),
    (Anchor(-0.34, 0.56, 0.94, "warm", -12.0), Anchor(0.62, 0.12, 0.82, "cool", 34.0), Anchor(-0.62, -0.52, 0.48, "earth", 18.0)),
    (Anchor(-0.62, 0.18, 0.86, "cool", -28.0), Anchor(0.34, -0.34, 0.96, "warm", 24.0), Anchor(0.54, 0.66, 0.50, "warm", -8.0)),
)

PLAINS_SURFACE_SWATCHES: Final[tuple[tuple[Anchor, ...], ...]] = (
    (Anchor(-0.58, 0.28, 0.94, "warm", 8.0), Anchor(0.48, -0.38, 0.78, "pale", -18.0), Anchor(0.46, 0.60, 0.50, "earth", 34.0)),
    (Anchor(-0.62, -0.22, 0.84, "pale", 24.0), Anchor(0.40, 0.38, 0.96, "warm", -6.0), Anchor(0.68, -0.46, 0.46, "earth", 12.0)),
    (Anchor(-0.36, 0.56, 0.92, "warm", -20.0), Anchor(0.62, 0.08, 0.82, "pale", 26.0), Anchor(-0.62, -0.48, 0.52, "earth", 8.0)),
    (Anchor(-0.62, 0.16, 0.88, "pale", -30.0), Anchor(0.32, -0.34, 0.96, "warm", 18.0), Anchor(0.54, 0.62, 0.48, "earth", -12.0)),
)

# Authored relief orientation sets. Small deterministic jitter may be added, but the
# variant's primary direction is intentional and survives seed changes.
HILL_DIRECTIONS_DEG: Final[tuple[float, ...]] = (8.0, 62.0, 128.0, 198.0)
MOUNTAIN_DIRECTIONS_DEG: Final[tuple[float, ...]] = (18.0, 82.0, 148.0)
PEAK_DIRECTIONS_DEG: Final[tuple[float, ...]] = (32.0, 118.0)


# City anchors are intentionally distinct in planning logic, not merely palette.
AUREN_CITY_ANCHORS: Final[dict[int, tuple[Anchor, ...]]] = {
    # Stage 1 must read as a compact civic seed, not a nearly complete town.
    1: (
        Anchor(0.0, 0.42, 1.08, "civic"),
        Anchor(-0.56, -0.12, 0.72),
        Anchor(0.57, -0.10, 0.70),
    ),
    # Stage 2 preserves the composition already judged positively in the v0.3.1 baseline.
    2: (Anchor(0.0, 0.42, 1.08, "civic"), Anchor(-0.68, 0.05, 0.76), Anchor(0.67, 0.03, 0.74), Anchor(-0.52, -0.58, 0.68), Anchor(0.52, -0.56, 0.66), Anchor(-0.84, 0.52, 0.60), Anchor(0.84, 0.50, 0.58)),
    3: (Anchor(0.0, 0.42, 1.12, "civic"), Anchor(-0.68, 0.05, 0.78), Anchor(0.67, 0.03, 0.76), Anchor(-0.52, -0.58, 0.70), Anchor(0.52, -0.56, 0.68), Anchor(-0.84, 0.52, 0.62), Anchor(0.84, 0.50, 0.60), Anchor(0.0, -0.88, 0.64), Anchor(-1.03, -0.35, 0.55), Anchor(1.03, -0.34, 0.55)),
}

BRASAL_CITY_ANCHORS: Final[dict[int, tuple[Anchor, ...]]] = {
    # Stage 1 is workshop + two support masses around a small working yard.
    1: (
        Anchor(0.12, 0.48, 1.06, "workshop"),
        Anchor(-0.60, -0.12, 0.76),
        Anchor(0.62, -0.18, 0.72),
    ),
    # Stage 2 preserves the composition already judged positively in the v0.3.1 baseline.
    2: (Anchor(0.12, 0.48, 1.06, "workshop"), Anchor(-0.72, 0.08, 0.80), Anchor(0.78, -0.04, 0.73), Anchor(-0.52, -0.64, 0.70), Anchor(0.54, -0.72, 0.66), Anchor(-0.95, 0.55, 0.61), Anchor(0.93, 0.53, 0.60)),
    3: (Anchor(0.12, 0.48, 1.10, "workshop"), Anchor(-0.72, 0.08, 0.82), Anchor(0.78, -0.04, 0.75), Anchor(-0.52, -0.64, 0.72), Anchor(0.54, -0.72, 0.68), Anchor(-0.95, 0.55, 0.62), Anchor(0.93, 0.53, 0.61), Anchor(-0.16, -1.00, 0.61), Anchor(1.08, 0.20, 0.54)),
}

# Road overlays use six canonical edge directions. Geometry code owns the exact path.
ROAD_CONNECTION_KEYS: Final[tuple[str, ...]] = ("e0", "e1", "e2", "e3", "e4", "e5")

# Review camera compositions; not gameplay map-generation rules.
BENCHMARK_LAYOUT_19: Final[dict[tuple[int, int], str]] = {
    (-2, 0): "mountain", (-2, 1): "forest", (-2, 2): "peak",
    (-1, -1): "plains", (-1, 0): "hills", (-1, 1): "meadow", (-1, 2): "forest",
    (0, -2): "coast_base", (0, -1): "coast_base", (0, 0): "coast_base", (0, 1): "coast_base", (0, 2): "coast_base",
    (1, -2): "shallow_sea", (1, -1): "shallow_sea", (1, 0): "shallow_sea", (1, 1): "shallow_sea",
    (2, -2): "open_sea", (2, -1): "open_sea", (2, 0): "open_sea",
}
