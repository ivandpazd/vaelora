"""Data-only visual content contract shared by Vaelora v0.3.2-r2 generators and QA."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Final


def derive_seed(root_seed: int, *parts: object) -> int:
    """Derive a stable 63-bit seed independent of Python process/hash randomization."""
    payload = "\0".join([str(root_seed), *(str(p) for p in parts)]).encode("utf-8")
    return int.from_bytes(hashlib.blake2b(payload, digest_size=8, person=b"vaelora3").digest(), "big") & ((1 << 63) - 1)


@dataclass(frozen=True)
class TerrainBrief:
    id: str
    movement_read: str
    macro_shape: str
    material_read: str
    negative_space: str
    forbidden_read: str


TERRAIN_BRIEFS: Final[dict[str, TerrainBrief]] = {
    "meadow": TerrainBrief("meadow", "open/easy", "soft fertile undulation", "fresh green + warm soil", "front-centre kept quiet", "flat green plate"),
    "plains": TerrainBrief("plains", "open/easy", "horizontal dry bands", "olive-gold + exposed earth", "broad clear centre", "recolored meadow"),
    "forest": TerrainBrief("forest", "slower/defensive", "clustered vertical canopy masses", "deep green + visible trunks", "deliberate unit window", "uniform tree carpet"),
    "hills": TerrainBrief("hills", "elevated/defensive", "directional low ridges", "grass + exposed warm/cool stone", "one readable saddle", "round lumps"),
    "mountain": TerrainBrief("mountain", "high relief/defensive", "main ridge + spur + shelves", "cool stone with warm lit planes", "base remains readable", "pyramid/volcano"),
    "peak": TerrainBrief("peak", "impassable", "severe vertical ridge", "pale upper stone/snow accents", "no implied walkable plateau", "scaled-up mountain only"),
    "coast_base": TerrainBrief("coast_base", "traversable shoreline", "land core with analytically stitched shoreline edges", "grass -> dry sand -> wet sand -> shallow-water wash", "continuous beach morphology and clear port edge", "road-like sand bands, visible corner patches or water holes"),
    "shallow_sea": TerrainBrief("shallow_sea", "naval/open", "broad calm water plane", "turquoise + faint submerged cues", "low visual noise", "wave carpet"),
    "open_sea": TerrainBrief("open_sea", "naval/deeper", "broad low-frequency water masses", "deeper blue-green", "maximum visual rest", "shallow sea recolor"),
}


@dataclass(frozen=True)
class FactionBrief:
    id: str
    planning_language: str
    silhouette_language: str
    material_language: str
    recurring_motifs: tuple[str, ...]
    forbidden_shortcuts: tuple[str, ...]


FACTION_BRIEFS: Final[dict[str, FactionBrief]] = {
    "auren": FactionBrief(
        "auren",
        "civic order expressed through plaza, axial routes and deliberate alignment",
        "upright, clean, vertical landmarks and controlled roof hierarchy",
        "warm ivory masonry, deep blue cloth/roof, restrained civic gold",
        ("three-strand route knot", "arch", "beacon", "ledger/marker", "bridge/route line"),
        ("generic medieval castle", "gold everywhere", "perfect sterile grid", "ornament that obscures function"),
    ),
    "brasal": FactionBrief(
        "brasal",
        "adaptive work settlement organized around longhouse/workshop, yard, storage and repair",
        "broad grounded roofs, practical tools, reinforced timber and low work structures",
        "weathered timber, stone footing, charcoal iron, copper repair accents, restrained moss",
        ("ascending iron bars", "kiln", "hooked work standard", "repair band", "field pack/tool rack"),
        ("skull overload", "spike forest", "chaotic junk pile", "evil-orc shorthand", "red everywhere"),
    ),
}


@dataclass(frozen=True)
class UnitBrief:
    role: str
    primary_read: str
    silhouette_anchor: str
    animation_priority: str


UNIT_BRIEFS: Final[dict[str, UnitBrief]] = {
    "settler": UnitBrief("settler", "founding/expansion", "travel bundle + staff/marker", "move, found feedback"),
    "worker": UnitBrief("worker", "improvement utility", "broad tool + pack", "move, work feedback"),
    "explorer": UnitBrief("explorer", "vision/scouting", "light pack + long staff/spyglass silhouette", "move"),
    "basic_soldier": UnitBrief("basic_soldier", "frontline combat", "shield + spear", "move, melee"),
    "patrol_ship": UnitBrief("patrol_ship", "naval combat", "compact hull + faction sail/standard", "move, ranged/melee feedback"),
}


REVIEW_SEEDS: Final[dict[str, int]] = {
    "terrain_plains": 22000,
    "terrain_benchmark": 22100,
    "faction_slice": 23000,
    "coast_stress": 23100,
    "grayscale_compare": 23200,
}


# Canonical finite-library seed helpers. Integrated review scenes must instantiate
# exactly the same seed/variant vocabulary that the 2D runtime imports.
def terrain_asset_seed(root_seed: int, kind: str, variant: int) -> int:
    return derive_seed(root_seed, "terrain", kind, variant)


def city_asset_seed(root_seed: int, faction: str, stage: int) -> int:
    return derive_seed(root_seed, "city", faction, stage)


def unit_asset_seed(root_seed: int, faction: str, role: str, facing: int) -> int:
    return derive_seed(root_seed, "unit", faction, role, facing)


def coast_asset_seed(root_seed: int, variant: int, edge: int) -> int:
    return derive_seed(root_seed, "coast", variant, edge)


def coast_variant_for_tile(root_seed: int, q: int, r: int, count: int) -> int:
    if count <= 0:
        raise ValueError("coast variant count must be positive")
    return derive_seed(root_seed, "coast-tile", q, r) % count


# Fixed acceptance-review wrappers. These keep the documented seeds discoverable
# while the generic helpers above allow controlled non-acceptance experiments.
def review_terrain_seed(kind: str, variant: int) -> int:
    return terrain_asset_seed(REVIEW_SEEDS["terrain_benchmark"], kind, variant)


def review_city_seed(faction: str, stage: int) -> int:
    return city_asset_seed(REVIEW_SEEDS["faction_slice"], faction, stage)


def review_unit_seed(faction: str, role: str, facing: int) -> int:
    return unit_asset_seed(REVIEW_SEEDS["faction_slice"], faction, role, facing)


def review_coast_seed(variant: int, edge: int) -> int:
    return coast_asset_seed(REVIEW_SEEDS["coast_stress"], variant, edge)


def review_coast_variant(q: int, r: int, count: int) -> int:
    return coast_variant_for_tile(REVIEW_SEEDS["coast_stress"], q, r, count)

