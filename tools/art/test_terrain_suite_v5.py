"""Host-side sanity tests for Terrain Suite v5.0-rc1 General."""
from __future__ import annotations
import sys
from pathlib import Path
BLENDER_DIR = Path(__file__).resolve().parents[1] / "blender"
sys.path.insert(0, str(BLENDER_DIR))
from vaelora_terrain_suite_spec import BENCHMARK36, SUITE_BRIEFS, SUITE_CANDIDATE, SUITE_FAMILIES, SUITE_SCATTER_DENSITY_TARGET, SUITE_VARIANTS, benchmark36_count
from vaelora_style import TERRAIN_SUITE_PACKAGE_REVISION

def main() -> None:
    assert SUITE_CANDIDATE == "5.0-rc1-general"
    assert TERRAIN_SUITE_PACKAGE_REVISION == 2
    assert benchmark36_count() == 36
    assert len(BENCHMARK36) == 6 and all(len(row) == 6 for row in BENCHMARK36)
    assert set(SUITE_FAMILIES) == set(SUITE_VARIANTS) == set(SUITE_BRIEFS)
    assert abs(SUITE_SCATTER_DENSITY_TARGET - 0.70) < 1e-9
    assert {"desert","snow","mountain","peak","hills","plains","forest","water","coast","meadow"} == set(SUITE_FAMILIES)
    assert all(count == 4 for family,count in SUITE_VARIANTS.items() if family != "coast")
    assert SUITE_VARIANTS["coast"] == 6
    # Integration map must contain all new candidate land families plus both water depths.
    kinds={kind for row in BENCHMARK36 for kind in row}
    assert {"meadow","plains","forest","hills","mountain","peak","desert","snow","shallow_sea","open_sea"} <= kinds
    # Benchmark must retain multiple sea depths and enough Meadow to make Coast transitions meaningful.
    flat=[kind for row in BENCHMARK36 for kind in row]
    assert flat.count("open_sea") >= 4 and flat.count("shallow_sea") >= 4
    assert flat.count("meadow") >= 4
    source=(BLENDER_DIR / "vaelora_terrain_suite_v5.py").read_text(encoding="utf-8")
    assert "centre=(sum(x for x,_ in positions)" in source, "benchmark/review centering guard missing"
    assert "forced_variants=(0,1,2,3,4)" in source, "coast morphology coverage guard missing"
    print("Vaelora Terrain Suite v5.0-rc1 General invariants: PASS")

if __name__ == "__main__": main()
