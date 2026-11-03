#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import shutil
HERE=Path(__file__).resolve().parent
REPO=Path.cwd().resolve()
REPLACE=[Path("tools/blender/vaelora_style.py"),Path("tools/blender/vaelora_artkit.py"),Path("tools/art/test_contract.py")]
ADD=[Path("tools/blender/vaelora_terrain_suite_spec.py"),Path("tools/blender/vaelora_terrain_suite_v5.py"),Path("tools/art/test_terrain_suite_v5.py")]
style=REPO/"tools/blender/vaelora_style.py"
if not style.exists(): raise SystemExit("ERROR: ejecuta el updater desde la raíz del repositorio Vaelora.")
text=style.read_text(encoding="utf-8")
if 'TERRAIN_RELEASE_CANDIDATE: Final[str] = "5.0-rc2"' not in text:
    raise SystemExit("ERROR: Terrain v5.0-rc2 corregido debe estar instalado antes de la suite general.")
# Preflight exact capabilities that the suite uses. This prevents another hidden material/helper mismatch.
materials=REPO/"tools/blender/vaelora_materials.py"
geometry=REPO/"tools/blender/vaelora_geometry.py"
if not materials.exists() or not geometry.exists():
    raise SystemExit("ERROR: faltan vaelora_materials.py o vaelora_geometry.py.")
mat_text=materials.read_text(encoding="utf-8")
geo_text=geometry.read_text(encoding="utf-8")
for token in ('def create_terrain_v3_material', '"meadow_v4"', '"plains_v3"'):
    if token not in mat_text: raise SystemExit(f"ERROR: base rc2 incompleta; falta material/capacidad: {token}")
for token in ('def hex_contains_disc', 'def random_hex_ring_point', 'def create_mountain_formation', 'def create_water_highlights'):
    if token not in geo_text: raise SystemExit(f"ERROR: base rc2 incompleta; falta helper geométrico: {token}")
if 'TERRAIN_SUITE_PACKAGE_REVISION: Final[int] = 2' in text:
    raise SystemExit("Terrain Suite v5.0-rc1 General reviewed/r2 parece estar ya aplicada.")
# Accept either clean rc2 or the earlier pre-review suite package.
if 'TERRAIN_SUITE_GENERAL_CANDIDATE: Final[str] = "5.0-rc1-general"' in text:
    print("Upgrading earlier Terrain Suite v5.0-rc1 General to reviewed package revision 2.")
for rel in REPLACE:
    src=HERE/"reference_files"/rel; dst=REPO/rel
    if not src.exists() or not dst.exists(): raise SystemExit(f"ERROR: falta archivo requerido: {rel}")
    shutil.copy2(dst,dst.with_name(dst.name+".before-terrain-suite-v5-r2")); shutil.copy2(src,dst)
for rel in ADD:
    src=HERE/"reference_files"/rel; dst=REPO/rel
    if not src.exists(): raise SystemExit(f"ERROR: falta archivo del paquete: {rel}")
    if dst.exists(): shutil.copy2(dst,dst.with_name(dst.name+".before-terrain-suite-v5-r2"))
    dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
print("Applied Vaelora Terrain Suite v5.0-rc1 General — reviewed package r2.")
print("  - current Meadow v5.0-rc2 remains the baseline")
print("  - candidate Plains/Hills/Mountain/Peak/Forest/Water polish added")
print("  - real candidate Desert v1 and Snow v1 families added")
print("  - four authored macro archetypes per candidate land family")
print("  - Coast review guarantees all three semantic shoreline morphologies")
print("  - 36-hex benchmark is mathematically centred and safely framed")
print("  - production TERRAIN_VARIANTS are intentionally not promoted yet")
print("Backups: *.before-terrain-suite-v5-r2")
