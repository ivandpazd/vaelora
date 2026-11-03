"""Host-readable contract for Vaelora Terrain Suite v6.0-rc1.

v6 is deliberately parallel to the reviewed v5 suite so every family can be A/B
validated before promotion. The visual target is the approved sculpted/painterly
reference set: broad terrain masses, saturated but controlled colour, strong
strategy-scale readability and no prop clipping.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Final

SUITE_V6_CANDIDATE: Final[str] = "6.0-rc1"
SUITE_V6_DENSITY_TARGET: Final[float] = 0.68

SUITE_V6_FAMILIES: Final[tuple[str, ...]] = (
    "meadow", "plains", "forest", "hills", "mountain", "peak",
    "desert", "snow", "water", "coast",
)

SUITE_V6_VARIANTS: Final[dict[str, int]] = {
    "meadow": 4, "plains": 4, "forest": 4, "hills": 4,
    "mountain": 4, "peak": 4, "desert": 4, "snow": 4,
    "water": 4, "coast": 6,
}

@dataclass(frozen=True)
class V6FamilyBrief:
    family: str
    target_read: str
    signature: str
    forbidden: str

SUITE_V6_BRIEFS: Final[dict[str, V6FamilyBrief]] = {
    "meadow": V6FamilyBrief("meadow", "fertile sculpted painterly baseline", "green/yellow-green masses + curated surface life", "flat procedural lawn"),
    "plains": V6FamilyBrief("plains", "open luminous rolling grassland", "long gentle swells + sparse flowers/rock", "empty beige/olive plate"),
    "forest": V6FamilyBrief("forest", "integrated grove masses with readable ground", "mixed broadleaf/conifer clusters + lively understory", "tree objects scattered independently"),
    "hills": V6FamilyBrief("hills", "broad unmistakable rolling landforms", "multiple crest directions + saddles + warm lit ridges", "meadow plus one bump"),
    "mountain": V6FamilyBrief("mountain", "terrain itself becomes mountain", "60-75 percent broad rocky mass + ridges/talus/alpine grass", "large rock prop on flat tile"),
    "peak": V6FamilyBrief("peak", "mountain base with one hero summit", "broad mountain foundation + dominant integrated spire", "isolated needle stuck in ground"),
    "desert": V6FamilyBrief("desert", "real sculpted arid terrain", "dunes + warm rock + sparse dry grass + palms only", "beige plains or temperate tree"),
    "snow": V6FamilyBrief("snow", "cold sculpted snowfield", "drifts + rock + snow-covered foliage", "white recolour or green foliage"),
    "water": V6FamilyBrief("water", "serene painterly depth", "broad depth fields + restrained curved glints", "wave carpet"),
    "coast": V6FamilyBrief("coast", "organic sandy land/water transition", "coves/headlands + shallow wash + anchored rock", "straight ribbon"),
}

# Same stable 6x6 integration topology as reviewed v5, allowing direct A/B comparison.
BENCHMARK36_V6: Final[tuple[tuple[str, ...], ...]] = (
    ("open_sea", "open_sea", "shallow_sea", "meadow", "forest", "snow"),
    ("open_sea", "shallow_sea", "meadow", "forest", "hills", "snow"),
    ("open_sea", "shallow_sea", "meadow", "plains", "hills", "mountain"),
    ("open_sea", "shallow_sea", "meadow", "plains", "hills", "mountain"),
    ("open_sea", "shallow_sea", "meadow", "plains", "desert", "mountain"),
    ("open_sea", "shallow_sea", "meadow", "plains", "desert", "peak"),
)

def benchmark36_v6_count() -> int:
    return sum(len(row) for row in BENCHMARK36_V6)
