"""Host-readable contract for Vaelora Terrain Suite v6.1-rc1.

v6.1 is deliberately surgical. The visual families already judged near-final stay
frozen from v6.0-rc1. Only Mountain, Peak and Coast change:
- Mountain: terrain-led mass with embedded rock strata, no floating slab read.
- Peak: mountain foundation + broad geological summit, never an obelisk/needle.
- Coast: same proven v5.1 topology with roughly 20% lower visual amplitude.
"""
from __future__ import annotations
from typing import Final
from vaelora_terrain_suite_v6_spec import BENCHMARK36_V6, SUITE_V6_FAMILIES, SUITE_V6_VARIANTS

SUITE_V61_CANDIDATE: Final[str] = "6.1-rc1"
SUITE_V61_FAMILIES: Final[tuple[str, ...]] = SUITE_V6_FAMILIES
SUITE_V61_VARIANTS: Final[dict[str, int]] = dict(SUITE_V6_VARIANTS)
FROZEN_V61_FAMILIES: Final[tuple[str, ...]] = (
    "meadow", "plains", "forest", "hills", "desert", "snow", "water",
)
CHANGED_V61_FAMILIES: Final[tuple[str, ...]] = ("mountain", "peak", "coast")
BENCHMARK36_V61: Final[tuple[tuple[str, ...], ...]] = BENCHMARK36_V6
MOUNTAIN_HEX_MASS_TARGET: Final[tuple[float, float]] = (0.65, 0.80)
COAST_VISUAL_SCALE: Final[float] = 0.80

def benchmark36_v61_count() -> int:
    return sum(len(row) for row in BENCHMARK36_V61)
