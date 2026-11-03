# Terrain Suite v5.0-rc1 General — execution plan

## Host gates

```bash
python -m py_compile tools/blender/*.py tools/art/*.py
python tools/art/test_contract.py
python tools/art/test_terrain_suite_v5.py
python tools/art/audit_pipeline.py tools/blender --json game/assets/qa-terrain-suite-v5/source-audit.json
```

## Generate all individual family reviews

```bash
"$BLENDER" --background --python tools/blender/vaelora_artkit.py -- \
  --asset terrain-suite-v5-all \
  --seed 25000 \
  --output game/assets/terrain/generated-terrain-suite-v5 \
  --strict-blender-version
```

## Generate the mixed 36-hex benchmark

```bash
"$BLENDER" --background --python tools/blender/vaelora_artkit.py -- \
  --asset terrain-suite-v5-benchmark36 \
  --seed 25100 \
  --output game/assets/terrain/generated-terrain-suite-v5 \
  --strict-blender-version
```
