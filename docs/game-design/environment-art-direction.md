# Vaelora — Environment Art Direction v0.3

## 1. Environment goal

The environment must carry most of Vaelora’s visual appeal while remaining a readable strategic substrate. It should feel richer than minimal low-poly strategy art, but calmer than a dense city builder.

## 2. Value architecture

The world uses a controlled mid-value range so units, overlays and faction accents can sit above it. Extremely dark terrain shadows and extremely bright terrain highlights are avoided except for small snow/foam/specular accents.

Value separation should make these groups readable in grayscale:

- open land;
- vegetation mass;
- rock relief;
- water;
- city/unit silhouette;
- overlay feedback.

## 3. Terrain-detail budget

### Open terrain

Low density. 1–3 small clusters, broad clean surface.

### Forest

High vertical density but controlled centre opening.

### Hills

Medium density; ridge shape dominates.

### Mountain/Peak

High macro complexity, low decorative clutter.

For the closed [terrain v1 baseline](TERRAIN_VISUAL_LANGUAGE_V1.md), surface scatter is reduced and edge-aware: keep outcrops grounded in actual relief, visible terrain between Mountain fragments, and quiet space at tile boundaries.

### Coast

Medium-high edge detail, low interior clutter.

### Sea

Very low detail; visual rest.

## 4. Geological logic

Rock features should show plausible directional structure even in stylized form:

- ridges have a dominant axis;
- shelves relate to ridge direction;
- talus accumulates below steep faces;
- exposed stone on hills follows erosion direction;
- peaks narrow toward upper structure;
- coast rocks align with shoreline forces rather than random radial placement.

## 5. Tree design

Tree species differ by macro silhouette:

| Species | Macro read | Branch read | Use |
|---|---|---|---|
| Broadleaf round | broad crown | visible lateral supports | general temperate forest |
| Broadleaf columnar | narrower vertical crown | stronger central rise | forest rhythm/settlement edges |
| Conifer | layered taper with gaps | visible central trunk | altitude/variety |
| Wind-bent | directional asymmetric crown | windward branch logic | coast/exposed areas |

No species is a rescaled version of the same blob.

## 6. Coast system

Coast is composed from:

- shared coast land base;
- one of three **semantic** shoreline morphology families;
- two authored variants × six world-direction edge overlays per morphology family;
- shallow-water wash, wet sand, dry sand and vegetation transition generated from one shared shoreline curve;
- restrained broken foam and controlled rock breakup.

The three morphology families are intentionally different rather than three random seeds:

1. **Gentle sand shelf** — broadest beach, softest curvature, very sparse rocks.
2. **Mixed sand/stone shore** — narrower beach pockets, stronger irregularity and occasional exposed stone.
3. **Narrow eroded shore** — tight sand/shingle band, strongest land-to-water shape, more geological punctuation.

All three are cosmetic. None implies different movement, yields, port legality or combat rules.

There are **no visible corner-resolver sprites**. Adjacent edges must meet at the same analytically defined endpoint so a multi-edge coast reads as one continuous shoreline. Stress test all 64 six-edge masks conceptually, but runtime builds them from the 36-edge finite library rather than 64 baked tiles.

## 7. Water

Static water must already look finished. Runtime animation is optional enhancement.

Shallow sea:

- more turquoise;
- subtle seabed hint;
- shorter, softer highlight forms;
- occasional submerged stone form.

Open sea:

- deeper/cooler;
- less seabed information;
- longer broad highlight forms;
- lower contrast noise.

## 8. Seasonal/weather scope

No seasonal terrain system is part of the initial prototype. The closed terrain-v1 visual suite contains Snow and Desert review families; they do not add playable terrain categories or authorize winter, autumn, desert-map, or seasonal variants in the initial prototype. Peak pale accents are terrain-specific, not a winter system.

## 9. Environment acceptance images

Every terrain batch must include:

- isolated asset sheet;
- 7-hex repetition flower;
- 19-hex mixed board;
- grayscale sheet;
- 75/100/125% crop comparison;
- 320 px thumbnail proxy;
- coast connection stress image where relevant.
