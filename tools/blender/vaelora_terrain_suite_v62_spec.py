"""Host-readable contract for Vaelora Terrain Suite v6.2-rc1.

Final geological polish over v6.1. Everything except Mountain and Peak is frozen.
Mountain uses broken embedded outcrops instead of long continuous stone ribs.
Peak uses four distinct geological summit archetypes built on the v6.1 mountain base.
"""
from __future__ import annotations
from typing import Final
from vaelora_terrain_suite_v61_spec import BENCHMARK36_V61, SUITE_V61_FAMILIES, SUITE_V61_VARIANTS

SUITE_V62_CANDIDATE: Final[str] = "6.2-rc1"
SUITE_V62_FAMILIES: Final[tuple[str, ...]] = SUITE_V61_FAMILIES
SUITE_V62_VARIANTS: Final[dict[str, int]] = dict(SUITE_V61_VARIANTS)
FROZEN_V62_FAMILIES: Final[tuple[str, ...]] = (
    "meadow", "plains", "forest", "hills", "desert", "snow", "water", "coast",
)
CHANGED_V62_FAMILIES: Final[tuple[str, ...]] = ("mountain", "peak")
BENCHMARK36_V62: Final[tuple[tuple[str, ...], ...]] = BENCHMARK36_V61
MOUNTAIN_FRAGMENT_COUNT_TARGET: Final[tuple[int, int]] = (3, 5)
PEAK_ARCHETYPE_COUNT: Final[int] = 4

PEAK_ARCHETYPES: Final[tuple[str, ...]] = (
    "alpine_offset",
    "broken_summit",
    "twin_shoulder",
    "escarpment",
)

def benchmark36_v62_count() -> int:
    return sum(len(row) for row in BENCHMARK36_V62)
