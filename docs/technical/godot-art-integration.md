# Vaelora — Godot Art Integration Contract v0.3

**Target engine:** Godot 4.7.x, Compatibility renderer, 2D runtime.

This document owns how accepted visual assets enter Godot. It does not own gameplay rules or Blender modelling.

[Terrain Visual Language v1](../game-design/TERRAIN_VISUAL_LANGUAGE_V1.md) fixes the source appearance at Terrain Suite `v6.2-rc1`; its Blender review renders are not the accepted 2D PNGs or runtime-composition proof required here.

## 1. Runtime composition

A board cell is presented as layered content rather than one baked mega-sprite:

```text
HexPresentation
  TerrainBase
  TerrainEdges
  TerrainFeature
  Road
  Improvement
  PropShadow
  Prop
  CityShadow
  City
  UnitShadow
  Unit
  TerritoryOverlay
  SelectionOverlay
  FogOverlay
  FeedbackFX
```

The simulation exposes stable content/state IDs; presentation maps those IDs to visual assets. Resource paths and sprite filenames are never authoritative gameplay identity.

## 2. Z-band contract

Use centralized z bands from `vaelora_style.py`. Individual assets may use small local offsets inside a band but may not cross semantic layers ad hoc.

Example:

- terrain: 0–29;
- route/infrastructure: 30–49;
- props/cities/units: 50–79;
- territory/selection/fog: 80–109;
- transient feedback: 110+.

This prevents one-off z fixes from accumulating into rendering bugs.

## 3. Texture import profile

Default for final 2D art:

- source format: transparent PNG;
- compression: **Lossless** for acceptance/reference builds;
- repeat: disabled unless a dedicated shader explicitly requires it;
- filtering: Linear for painterly sprites;
- mipmaps: evaluate per family, not globally;
- Detect 3D: not relevant to the 2D sprite pipeline.

Godot documents Lossless as the default/common mode for 2D and warns that VRAM compression can produce visible artifacts in lower-resolution 2D textures. Do not change to VRAM compression only to reduce memory without side-by-side evidence.

## 4. Mipmap decision

Vaelora uses 75/100/125% zoom. Mipmaps can reduce grain/shimmer when sprites are scaled down, but increase texture memory by roughly one third.

Therefore:

- Terrain: test mipmaps ON/OFF at 75% and during camera movement.
- City/unit: test ON/OFF; prefer OFF if no visible shimmer.
- UI/overlays: normally OFF unless a specific scale case benefits.
- Final decision is evidence-based on representative Android/Web/desktop targets.

If mipmaps are enabled, use Linear Mipmap filtering for non-pixel-art sprites.

## 5. Atlas strategy

Authoring assets remain individual PNGs for review and traceability. Runtime packaging may atlas accepted sprites by family to reduce texture switches.

Suggested atlas families:

- shared terrain bases;
- coast/road overlays;
- neutral decorations;
- Auren cities/buildings;
- Brasal cities/buildings;
- Auren units per animation;
- Brasal units per animation;
- fog/interaction overlays.

Do not pack unrelated UI/store art with board sprites.

Atlas generation is a build step; it must not become the source asset.

## 6. Large map rendering

The maximum generation bounds are 80×50 hexes. Do not assume every tile needs an independent heavyweight scene node with bespoke materials.

Stage-2 spike should compare:

1. layered Sprite2D/region approach;
2. TileMapLayer/atlas approach for terrain-like layers;
3. MultiMeshInstance2D only if profiling shows thousands of repeated sprites create a bottleneck and its all-or-none culling trade-off is acceptable.

Optimization must follow measurements. A visually simpler architecture that stays readable across Web/Android is preferable to premature complexity.

## 7. Alpha and overdraw

Transparent canvases are convenient but can waste fill rate. QA records alpha bounding boxes and occupied coverage.

Rules:

- terrain intentionally fills much of its canvas;
- units/props should use tight but safe framing;
- city canvas may be wider, but empty transparent area must be justified by consistent registration;
- avoid huge soft glow textures spanning multiple tiles;
- contact shadows remain compact.

If profiling shows fill-rate pressure at high viewport resolution, evaluate trimmed mesh/region rendering for the most repeated families without changing source art.

## 8. Contact shadows

Unit/city/hero-prop shadow overlays are derived from final alpha and composited below the sprite. They are presentation assets, not gameplay state.

The shadow:

- stays subtle;
- cannot imply a different sun direction from the rendered sprite;
- does not cross into strong neighboring-tile darkness;
- is disabled/reduced only through a presentation profile, never individually per random asset.

## 9. Water overlay

Optional runtime water motion is a CanvasItem shader/overlay that moves highlights only. It must not modify terrain silhouette or authoritative state.

Required modes:

- Full: very slow highlight drift.
- Reduced motion: static.
- Low-performance profile: static.

Static Blender water art must already pass the visual gate.

## 10. Fog and territory

Fog is a separate state layer. It does not permanently darken source terrain PNGs.

Three states:

- unexplored;
- explored/not visible;
- currently visible.

Territory and selection feedback similarly remain separate, allowing accessibility and color-profile adjustment without regenerating terrain.

## 11. Pixel alignment and movement

Sprites are authored at 2× and shown at logical scale. Camera movement should avoid unstable subpixel shimmer. Validate:

- camera pan at 75/100/125%;
- unit movement interpolation;
- road/coast seams;
- texture filtering;
- mipmap choice.

Do not solve shimmer by switching the whole project to nearest-neighbor filtering; the art is not pixel art.

## 12. Content lookup

Recommended presentation data record:

```text
VisualAssetRef
  stable_visual_id
  family
  atlas/texture reference
  region
  anchor
  z_band
  shadow reference
  facings/frames
  accepted_art_revision
```

Gameplay persists content IDs, not these visual paths.

## 13. Import acceptance evidence

For every accepted family, record:

- import preset;
- mipmap state;
- filter state;
- memory shown by Godot importer;
- screenshot at 75/100/125%;
- Android/Web/desktop visual comparison;
- any artifact introduced by compression;
- batch/draw-call measurement for representative view.

## 14. External technical references

Recheck against the pinned Godot version during implementation:

- Image import/compression/mipmaps: `https://docs.godotengine.org/en/latest/tutorials/assets_pipeline/importing_images.html`
- Texture importer reference: `https://docs.godotengine.org/en/latest/classes/class_resourceimportertexture.html`
- MultiMesh optimization background: `https://docs.godotengine.org/en/latest/tutorials/performance/using_multimesh.html`

## v0.3.2-r2 runtime-fidelity acceptance

The final visual lock cannot be based only on Blender source-context renders. Before issue #17 is accepted, build a small Godot review scene that composes the actual accepted `final_2x` PNGs with the intended anchors and `Z_BANDS` and capture at least:

- the fixed 19-hex layout at 75%, 100% and 125%;
- one dense forest/city/unit overlap case;
- coast stress using the 36-edge finite shoreline library;
- color and grayscale screenshots;
- mipmaps OFF and ON for any family where the import choice is still open.

Use the pinned Godot version and record import settings/memory evidence. The Blender benchmark is source-context evidence; the Godot scene is runtime-fidelity evidence.

For 2D painterly art, start with Lossless import and measure before choosing VRAM compression. Mipmaps remain an evidence-based per-family choice because they can improve minification/camera zoom at a memory cost. Atlas packaging is a runtime optimization decision, not an authoring-format requirement; profile actual texture-switch/batching pressure before packing accepted assets.


## Premium visual-detail layer policy

The first accepted slice may keep low-risk microdetail baked into terrain sprites, but the presentation architecture must reserve an optional `terrain_detail` band between base/features and gameplay objects. If real Godot 75% testing shows eye fatigue or unit/resource competition, future purely cosmetic grass/flower/pebble sprites may move to this band and fade/hide by presentation profile.

Rules:

- never move terrain identity, coast, road, improvement, city or unit information into the optional band;
- Reduced Detail may hide cosmetic microdetail only;
- changes are driven by actual 75/100/125 evidence, not by arbitrary LOD thresholds;
- fading is preferred to distracting pop when feasible on target platforms.
