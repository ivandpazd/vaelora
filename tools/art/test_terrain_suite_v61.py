"""Host-side invariants for Vaelora Terrain Suite v6.1-rc1."""
from __future__ import annotations
import sys
from pathlib import Path
BLENDER_DIR = Path(__file__).resolve().parents[1] / "blender"
sys.path.insert(0, str(BLENDER_DIR))
from vaelora_terrain_suite_v61_spec import (
    BENCHMARK36_V61, CHANGED_V61_FAMILIES, COAST_VISUAL_SCALE,
    FROZEN_V61_FAMILIES, MOUNTAIN_HEX_MASS_TARGET, SUITE_V61_CANDIDATE,
    SUITE_V61_FAMILIES, SUITE_V61_VARIANTS, benchmark36_v61_count,
)
from vaelora_style import TERRAIN_SUITE_V61_CANDIDATE, TERRAIN_SUITE_V61_PACKAGE_REVISION

def main():
    assert SUITE_V61_CANDIDATE == "6.1-rc1" == TERRAIN_SUITE_V61_CANDIDATE
    assert TERRAIN_SUITE_V61_PACKAGE_REVISION == 1
    assert benchmark36_v61_count() == 36 and len(BENCHMARK36_V61) == 6
    assert set(FROZEN_V61_FAMILIES) == {"meadow","plains","forest","hills","desert","snow","water"}
    assert CHANGED_V61_FAMILIES == ("mountain","peak","coast")
    assert MOUNTAIN_HEX_MASS_TARGET == (0.65, 0.80)
    assert abs(COAST_VISUAL_SCALE - 0.80) < 1e-9
    assert set(SUITE_V61_FAMILIES) == set(SUITE_V61_VARIANTS)
    src = (BLENDER_DIR / "vaelora_terrain_suite_v61.py").read_text(encoding="utf-8")
    for token in ("_boost_surface_relief", "_create_integrated_summit", "_soften_coast_edge", "Terrain-conforming exposed stratum", "VAE_V61_MountainStratumMain", "VAE_V61_IntegratedSummit"):
        assert token in src, token
    assert "_create_spire" not in src, "v6 needle spire must not be reused in v6.1"
    assert "return v6.build_candidate_tile" in src, "frozen v6 families must delegate unchanged"
    assert 'factor = COAST_VISUAL_SCALE' in src, "coast visual softening missing"
    art = (BLENDER_DIR / "vaelora_artkit.py").read_text(encoding="utf-8")
    assert "terrain-suite-v61-mountain" in art and "terrain-suite-v61-benchmark36" in art
    print("Vaelora Terrain Suite v6.1-rc1 invariants: PASS")
if __name__ == "__main__": main()
