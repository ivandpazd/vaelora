"""Host-side invariants for Vaelora Terrain Suite v6.0-rc1."""
from __future__ import annotations
import sys
from pathlib import Path
BLENDER_DIR=Path(__file__).resolve().parents[1]/"blender"; sys.path.insert(0,str(BLENDER_DIR))
from vaelora_terrain_suite_v6_spec import BENCHMARK36_V6, SUITE_V6_BRIEFS, SUITE_V6_CANDIDATE, SUITE_V6_DENSITY_TARGET, SUITE_V6_FAMILIES, SUITE_V6_VARIANTS, benchmark36_v6_count
from vaelora_style import TERRAIN_SUITE_V6_CANDIDATE, TERRAIN_SUITE_V6_PACKAGE_REVISION

def main():
    assert SUITE_V6_CANDIDATE=="6.0-rc1"==TERRAIN_SUITE_V6_CANDIDATE
    assert TERRAIN_SUITE_V6_PACKAGE_REVISION==1
    assert abs(SUITE_V6_DENSITY_TARGET-.68)<1e-9
    assert benchmark36_v6_count()==36 and len(BENCHMARK36_V6)==6 and all(len(r)==6 for r in BENCHMARK36_V6)
    assert set(SUITE_V6_FAMILIES)==set(SUITE_V6_VARIANTS)==set(SUITE_V6_BRIEFS)
    assert SUITE_V6_VARIANTS["coast"]==6 and all(v==4 for k,v in SUITE_V6_VARIANTS.items() if k!="coast")
    src=(BLENDER_DIR/"vaelora_terrain_suite_v6.py").read_text(encoding="utf-8")
    for token in ("_create_palm", "snow_leaf", "_create_spire", "VAE_V6_MountainFoundation", "geo.hex_contains_disc", "terrain_suite_v6_benchmark36"):
        assert token in src, token
    assert 'variant in (1,3)' in src, "desert/snow authored accent variants missing"
    assert 'p=_safe_point(rng,"mid",.72,occ,.24)' in src, "palm canopy edge-clearance guard missing"
    assert 'conifer=True,snow=True' in src, "snow tree must use snow-covered foliage"
    desert=src.split("def _build_desert",1)[1].split("def _build_snow",1)[0]
    assert "_create_palm" in desert and "_create_v6_tree" not in desert, "desert may only spawn palm trees"
    snow=src.split("def _build_snow",1)[1].split("def _build_forest",1)[0]
    assert "conifer=True,snow=True" in snow, "snow trees must use snow-covered foliage"
    print("Vaelora Terrain Suite v6.0-rc1 invariants: PASS")
if __name__=="__main__": main()
