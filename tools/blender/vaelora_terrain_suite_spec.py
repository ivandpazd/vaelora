"""Data-only contract for Vaelora Terrain Suite v5.0-rc1 General.

This module deliberately has no bpy import so host-side QA can validate the candidate
suite before Blender is launched. Desert and Snow are candidate production families,
not recoloured proxies.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Final

SUITE_CANDIDATE: Final[str] = "5.0-rc1-general"
SUITE_SCATTER_DENSITY_TARGET: Final[float] = 0.70

SUITE_FAMILIES: Final[tuple[str, ...]] = (
    "meadow", "plains", "forest", "hills", "mountain", "peak",
    "desert", "snow", "water", "coast",
)

SUITE_VARIANTS: Final[dict[str, int]] = {
    "meadow": 4,
    "plains": 4,
    "forest": 4,
    "hills": 4,
    "mountain": 4,
    "peak": 4,
    "desert": 4,
    "snow": 4,
    "water": 4,
    "coast": 6,
}

@dataclass(frozen=True)
class SuiteFamilyBrief:
    family: str
    macro_read: str
    palette_read: str
    scatter_read: str
    forbidden_read: str

SUITE_BRIEFS: Final[dict[str, SuiteFamilyBrief]] = {
    "meadow": SuiteFamilyBrief("meadow", "fertile sculpted shoulders + quiet basins", "fresh/cool greens + yellow-green crest light", "rocks + broad grass + sparse flowers", "flat green plate"),
    "plains": SuiteFamilyBrief("plains", "broad dry swells and long shoulders", "olive + straw + warm exposed soil", "dry grass + warm stones, very few flowers", "yellow meadow"),
    "forest": SuiteFamilyBrief("forest", "clustered vertical canopy masses over readable ground", "deep/mid greens + warm trunks", "2-3 authored tree clusters + sparse understory", "uniform tree carpet"),
    "hills": SuiteFamilyBrief("hills", "multiple unmistakable ridge masses + saddle", "grass + warm/cool exposed stone", "rocks/grass reinforce slopes", "meadow with bigger bumps"),
    "mountain": SuiteFamilyBrief("mountain", "main ridge + spur + buttress + talus integrated into ground", "cool stone + warm lit planes", "talus and sparse alpine grass", "single pyramid prop"),
    "peak": SuiteFamilyBrief("peak", "severe narrow vertical ridge, no walkable plateau", "dark/cool stone + pale upper planes", "very sparse base detail", "scaled mountain only"),
    "desert": SuiteFamilyBrief("desert", "asymmetric dunes + eroded basins", "sand/ochre/terracotta with warm rock", "rare dry grass + scattered stone", "beige plains"),
    "snow": SuiteFamilyBrief("snow", "snow drifts + compressed basins", "cool blue-grey shadow + ivory snow + exposed rock", "minimal rock + rare wind-bent vegetation", "white recolour"),
    "water": SuiteFamilyBrief("water", "broad low-frequency calm masses", "turquoise shallows + deeper blue-green open water", "clustered curved glints only", "repeating wave carpet"),
    "coast": SuiteFamilyBrief("coast", "irregular stitched shoreline with coves/headlands", "wet sand + dry sand + water wash", "small anchored rocks, no clutter", "road-like beige ribbon"),
}

# 6 x 6 axial rectangle = 36 integration tiles. Land/water adjacency automatically
# receives Coast v5.1 overlays in the Blender suite generator.
BENCHMARK36: Final[tuple[tuple[str, ...], ...]] = (
    ("open_sea", "open_sea", "shallow_sea", "meadow", "forest", "snow"),
    ("open_sea", "shallow_sea", "meadow", "forest", "hills", "snow"),
    ("open_sea", "shallow_sea", "meadow", "plains", "hills", "mountain"),
    ("open_sea", "shallow_sea", "meadow", "plains", "hills", "mountain"),
    ("open_sea", "shallow_sea", "meadow", "plains", "desert", "mountain"),
    ("open_sea", "shallow_sea", "meadow", "plains", "desert", "peak"),
)

def benchmark36_count() -> int:
    return sum(len(row) for row in BENCHMARK36)
