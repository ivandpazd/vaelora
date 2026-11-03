"""Host-side invariants for Vaelora Terrain Suite v6.2-rc1."""
from __future__ import annotations
import sys
from pathlib import Path
BLENDER_DIR = Path(__file__).resolve().parents[1] / "blender"
sys.path.insert(0, str(BLENDER_DIR))
from vaelora_terrain_suite_v62_spec import (
    BENCHMARK36_V62, CHANGED_V62_FAMILIES, FROZEN_V62_FAMILIES,
    MOUNTAIN_FRAGMENT_COUNT_TARGET, PEAK_ARCHETYPE_COUNT, PEAK_ARCHETYPES,
    SUITE_V62_CANDIDATE, SUITE_V62_FAMILIES, SUITE_V62_VARIANTS,
    benchmark36_v62_count,
)
from vaelora_style import TERRAIN_SUITE_V62_CANDIDATE, TERRAIN_SUITE_V62_PACKAGE_REVISION

def main():
    assert SUITE_V62_CANDIDATE == "6.2-rc1" == TERRAIN_SUITE_V62_CANDIDATE
    assert TERRAIN_SUITE_V62_PACKAGE_REVISION == 1
    assert benchmark36_v62_count() == 36 and len(BENCHMARK36_V62) == 6
    assert CHANGED_V62_FAMILIES == ("mountain", "peak")
    assert set(FROZEN_V62_FAMILIES) == {"meadow","plains","forest","hills","desert","snow","water","coast"}
    assert MOUNTAIN_FRAGMENT_COUNT_TARGET == (3, 5)
    assert PEAK_ARCHETYPE_COUNT == 4 == len(PEAK_ARCHETYPES)
    assert set(SUITE_V62_FAMILIES) == set(SUITE_V62_VARIANTS)
    src = (BLENDER_DIR / "vaelora_terrain_suite_v62.py").read_text(encoding="utf-8")
    for token in (
        "_broken_outcrops", "_create_asymmetric_summit", "alpine_offset",
        "broken_summit", "twin_shoulder", "escarpment",
        "VAE_V62_BrokenOutcrop", "VAE_V62_Peak_",
    ):
        assert token in src, token
    assert "_create_spire" not in src, "old v6 needle spire must not return"
    assert "return v61.build_candidate_tile" in src, "frozen v6.1 families must delegate unchanged"
    assert "return v61.generate_coast_review" in src, "coast must stay frozen at v6.1"
    art = (BLENDER_DIR / "vaelora_artkit.py").read_text(encoding="utf-8")
    assert "terrain-suite-v62-mountain" in art and "terrain-suite-v62-benchmark36" in art
    print("Vaelora Terrain Suite v6.2-rc1 invariants: PASS")

if __name__ == "__main__":
    main()
