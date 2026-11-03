# Vaelora — Art Production Pipeline v0.3

## 1. Purpose

Create consistent commercial-quality 2D runtime art from reproducible Blender sources without turning procedural generation into a substitute for art direction.

The current terrain appearance baseline is [Terrain Visual Language v1](TERRAIN_VISUAL_LANGUAGE_V1.md), using Terrain Suite `v6.2-rc1`. The `generated-v0.3.2-r2/` paths below document the earlier integrated pipeline and must not be mistaken for v6.2 production exports.

Pipeline:

`design contract → deterministic Blender source → 4× render → 2× Lanczos → image QA → contextual review → Godot import → platform review → human acceptance`

## 2. Production pin

Accepted v0.3 benchmark renders use **Blender 5.2.3 LTS**.

Other Blender 5.2.x builds may be used for iteration, but a candidate promoted to `accepted` is regenerated on the pin and compared for drift.

## 3. Source structure

```text
tools/blender/
  vaelora_style.py         immutable visual tokens
  vaelora_contract.py      terrain/faction/unit briefs + stable seed derivation
  vaelora_composition.py   authored composition templates
  vaelora_materials.py     procedural material factories
  vaelora_geometry.py      reusable modelling primitives/constructors
  vaelora_render.py        camera/light/render/manifest
  vaelora_artkit.py        terrain/coast/hero-prop generation
  vaelora_faction_kit.py   cities/benchmark units
  OPENCODE_PROMPT.md       AI/MCP operating contract

tools/art/
  audit_pipeline.py
  downsample.py
  validate_outputs.py
  validate_manifests.py
  make_review_sheet.py
  estimate_texture_budget.py
```

## 4. Generated directory contract

```text
generated-v0.3.2-r2/
  source/            editable .blend snapshots
  raw_4x/            Blender work renders
  manifests/         JSON manifest schema v3
  final_2x/          game-ready review PNGs
  shadows_2x/        modular contact shadows where applicable
  review/            contact sheets, grayscale, crops, thumbnail proxies
  qa/                JSON reports and budget estimates
```

Generated folders are evidence/output. The generator code and accepted source art remain the authority.

## 5. Determinism

All accepted procedural variations derive local seeds with BLAKE2 from:

`root seed + stable namespace + semantic parts`.

Do not use Python process `hash()` or global random calls.

A/B art review always regenerates the same semantic seed.

## 6. Manifest schema v3

Every render manifest records at minimum:

- schema version;
- asset ID;
- art-style ID;
- generator version;
- lifecycle state;
- seed;
- family;
- source script;
- SHA-256 of relevant source modules;
- Blender version and production pin;
- renderer/color-management profile;
- camera values;
- canvas sizes;
- world bounds;
- estimated geometry statistics;
- provenance;
- post-process record;
- QA state.

This is traceability, not gameplay identity.

## 7. Modelling workflow

1. Read canonical brief.
2. Choose/derive stable seed.
3. Reset scene.
4. Build from reusable geometry/material/composition modules.
5. Validate footprint/safe zones before render.
6. Apply master camera/light only.
7. Render transparent 4× PNG.
8. Save source `.blend` snapshot for benchmark/candidate assets.
9. Write manifest.

## 8. Post-process workflow

Host Python performs:

1. validate work-canvas dimensions;
2. convert to RGBA;
3. Lanczos downsample to final 2×;
4. generate compact contact shadow for modular object families;
5. compute alpha bounding box/occupancy;
6. compute edge-alpha checks;
7. write postprocess metadata;
8. run QA.

Do not resize manually in image editors between pipeline stages.

## 9. Review generation

For every candidate set produce:

- color contact sheet;
- grayscale sheet;
- Steam 320 proxy;
- 75/100/125 crop set;
- family repetition stress view;
- contextual mixed-board view.

## 10. Production sequence

### Gate 0 — Plains material/hex benchmark

Purpose: validate geometry, material, lighting, camera and geological side signature before multiplying assets.

### Gate 1 — 19-hex environment slice

Purpose: validate whole-board composition, repetition, land/water transition, forest/relief hierarchy.

### Gate 2 — Auren/Brasal representative slice

Purpose: validate faction planning language and Basic Soldier silhouettes.

### Gate 3 — coast connection system

Purpose: validate the finite 3×2×6 shoreline edge library (36 overlays), analytical edge joins and water quality.

### Gate 4 — shared infrastructure

Road/Farm/Lumber/Mine/Port.

### Gate 5 — city/building modularity

All three city stages plus building attachments.

### Gate 6 — unit roster

Idle language first, then approved animation scope.

### Gate 7 — overlays/UI

Fog, territory, selection, HUD and menu art.

### Gate 8 — integrated prototype visual pass

Actual Godot scene across target viewports/platforms.

### Gate 9 — commercial presentation

Screenshots/key art/capsules after runtime identity is stable.

## 11. AI/OpenCode operating rule

OpenCode + Blender MCP must modify the reproducible source system rather than manually “fixing” one generated mesh unless a deliberate hero asset requires hand-authoring.

When a generated family fails:

1. reproduce same seed;
2. identify failed contract;
3. fix generator/template/material;
4. regenerate same seed;
5. compare A/B;
6. only then inspect new variants.

## 12. Hand-authored exception

Procedural generation is not mandatory for every final asset. A hero city focal structure, key-art element or difficult unit may be hand-modelled in Blender if:

- source is editable;
- camera/scale/material contracts are preserved;
- provenance is recorded;
- it does not create a one-off style inconsistent with procedural families.

The goal is consistency, not procedural purity.

## 13. Failure policy

Stop production expansion if a benchmark has a Blocker or unresolved Major defect. Do not generate “the rest” hoping consistency will hide a weak foundation.

## 14. Blender production reference

Production pin verification: `https://www.blender.org/releases/5-2/`

## v0.3.2-r2 reconciliation rules

### Finite-library fidelity

The generator is allowed to be procedural, but accepted runtime content is finite. Source-context benchmarks therefore select from the exact finite exported vocabulary rather than generating benchmark-only morphology.

Canonical review roots:

- terrain/benchmark root seed: `22100`;
- faction slice root seed: `23000`;
- coast morphology root seed: `23100`.

A coast tile selects one of six authored variants (two per semantic morphology) deterministically and reuses that variant for every sea-facing edge. The export library therefore contains 36 shoreline overlays (3 morphologies × 2 variants × 6 directions), not six random edges and not 64 baked neighbor masks.

### Grounding rule

Trees, grass, rocks, hill formations and mountain formations sample the actual sculpted terrain surface at their anchor point. Fixed-Z placement is prohibited for terrain decoration where the underlying surface is non-planar. Coast-base relief is intentionally restrained because shoreline overlays are reusable runtime assets and must sit cleanly across all coast-base variants.

### Review evidence hierarchy

1. isolated final 2x sprite;
2. wrapped 75/100/125% sheet containing **every** candidate;
3. grayscale sheet;
4. Blender source-context benchmark built from finite runtime variants;
5. coast stress scene;
6. real Godot runtime-composition screenshot;
7. Web/Android/desktop measurement before Stage-2 closure.

A pretty Blender benchmark cannot substitute for step 6.
