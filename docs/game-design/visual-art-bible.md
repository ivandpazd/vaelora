# Vaelora — Visual Art Bible v0.3

**Status:** production-quality visual contract. [Terrain Visual Language v1](TERRAIN_VISUAL_LANGUAGE_V1.md) is closed at Terrain Suite `v6.2-rc1` as a scoped art-direction baseline; the full representative slice still requires production exports, Godot runtime review, and explicit human acceptance.

**Art style ID:** `vaelora-sculpted-diorama-v2`

## 1. The visual identity

**Vaelora Sculpted Diorama** is a premium stylized fantasy landscape built as if each hex were a small hand-sculpted fragment of a larger world. Forms are simplified for strategy readability but shaped with enough intentional asymmetry, material response and environmental storytelling to avoid generic low-poly output.

The art should feel:

- luminous rather than dark;
- tactile rather than flat;
- crafted rather than procedurally scattered;
- grounded fantasy rather than exaggerated high-magic spectacle;
- readable rather than hyper-detailed;
- warm and inviting without becoming toy-like or childish.

The player should be able to identify a Vaelora screenshot from the combination of **sculpted geological hexes, luminous natural materials, deliberate negative space, the Trama route/beacon motif, and civilization-specific settlement planning**.

## 2. Non-negotiable principles

1. **Strategy readability is the first art requirement.** Terrain, city stage, unit role and state must survive 75% overview zoom.
2. **Primary forms are sculpted, never stock primitives.** Construction primitives are allowed internally; recognizable untouched primitive silhouettes are not.
3. **Procedural generation uses authored grammar.** Randomness chooses among designed patterns and controlled ranges; it does not decide composition from scratch.
4. **Terrain remains civilization-neutral.** Faction accents belong to civilization assets, improvements and UI, not the shared world.
5. **Faction identity survives grayscale.** Spatial organization, shape and materials must differentiate Auren and Brasal before color does.
6. **Exact six-edge registration is immutable.** Interior terrain relief falls to zero before the external footprint.
7. **No terrain is baked under modular gameplay objects.** Cities, units, buildings, improvements and props remain reusable.
8. **Material response is painterly and procedural.** No photographic texture dependence in the prototype environment kit.
9. **Environmental storytelling never creates false gameplay affordance.** Cosmetic Trama remnants look historical, not lootable or interactable.
10. **Close-up beauty may not destroy overview clarity.** Detail that disappears harmlessly is fine; detail that becomes noise is not.
11. **The visual system must scale to an 80×50 map.** Individual hero assets cannot require every visible tile to be unique.
12. **A screenshot is part of the acceptance test.** Art that only looks good isolated in Blender has failed.

## 3. Detail hierarchy

Target distribution:

- **Macro ≈70%** — silhouette, terrain mass, city organization, unit pose.
- **Meso ≈20%** — branches, roofs, stone shelves, work-yard structures, repair bands.
- **Micro ≈10%** — flowers, cracks, small stones, tiny trim.

Microdetail must never be used to rescue weak macro design.

## 3.1 Distance/detail tiers

Vaelora is reviewed at three practical reads rather than one beauty render:

- **Macro / always-readable:** terrain category, relief class, city stage, unit role/equipment, coast-vs-sea boundary. These must survive 75% zoom and may never depend on microdetail.
- **Meso / normal-play richness:** tree species rhythm, roofs, stone shelves, civic/work-yard structure, repair bands. These should enrich 100% without becoming required state.
- **Micro / close-inspection reward:** flowers, tiny grass, small stones, subtle material variation and surface marks. These must disappear harmlessly when reduced.

Where runtime profiling/readability warrants it, purely cosmetic microdetail may be authored as an optional presentation layer that can be hidden/faded in a reduced-detail profile. Gameplay identity, coast registration, roads, improvements, city stage and unit silhouettes never move into that optional layer.

## 4. Visual hierarchy in gameplay

Highest to lowest priority:

1. currently selected/actionable unit or city;
2. friendly/enemy unit silhouette;
3. city ownership and stage;
4. terrain category and strategic relief;
5. improvement/road/port state;
6. territory and interaction overlays;
7. environmental variation;
8. purely cosmetic Trama remnants.

An art pass may intentionally remove foliage, props or detail where a higher layer needs the screen space.

## 5. Camera and projection

All game-ready renders use one locked orthographic master camera:

- yaw: **45°**;
- elevation: **30°**;
- fixed **2:1 dimetric** presentation;
- no perspective lens;
- no per-asset camera adjustment;
- six unit facings are world rotations, never camera rotations.

The camera is a production tool and a style rule. A model that only works after changing the camera does not work for Vaelora.

## 6. Canvas and supersampling contract

| Family | Logical | Final 2× PNG | Work render |
|---|---:|---:|---:|
| Terrain | 128×64 | 256×128 | 512×256 |
| Overlay | 128×64 | 256×128 | 512×256 |
| Unit | 128×64 | 256×128 | 512×256 |
| City | 256×128 | 512×256 | 1024×512 |
| Hero prop | 128×64 | 256×128 | 512×256 |

Working renders are reduced using Lanczos. Acceptance is judged primarily on the final 2× output and actual in-game scale, not the supersampled source.

## 7. The extracted-world hex

The geological side wall is a signature, not decoration pasted onto a flat tile.

A land tile reads as:

1. living surface;
2. organic topsoil transition;
3. warm clay/earth stratum;
4. deeper darker mineral/rock body;
5. controlled lower edge.

The layers may vary slightly between biomes but keep the same physical logic. The result should suggest a cutaway piece of a continuous world, not a frosted cookie.

### 7.1 Interior relief

Interior vertices may rise/fall in broad forms. Relief must approach canonical boundary elevation before the six external edges. Never distort the neighbor registration perimeter.

### 7.2 Side-wall readability

The side wall must remain subordinate to gameplay surface. Strong stripes, saturated geology or repeating zebra patterns are rejected.

## 8. Composition zones

Every tile is composed with the fixed camera in mind:

- **rear/high zone:** tallest vegetation and hero relief;
- **central information zone:** primary terrain identity or improvement;
- **front quiet zone:** lower detail to protect units and selection feedback;
- **edge connection zone:** reserved for coast/road/port continuity;
- **UI-clear centre:** avoid visually dense microdetail under unit anchors.

Negative space is treated as authored content.

## 9. Terrain family identity

### Meadow

Soft fertile undulation, fresh medium-value greens, localized grass tufts, sparse flowers and a few warm stones. It should communicate productive/open terrain without looking manicured.

Reject: neon lawn, flat disk, flower carpet, excessive rocks.

### Plains

Warmer olive/gold, more exposed earth, lower vegetation and horizontal dry-grass rhythm. It must differ from Meadow through shape/value/texture even in grayscale.

Reject: Meadow recolored yellow.

### Forest

Designed clusters of 6–9 trees with 2–3 species, hero/support height hierarchy, visible trunks and a deliberate front/central opening. Undergrowth connects the composition but does not become noise.

Reject: uniform spacing, sphere piles, opaque green wall.

### Hills

One dominant low ridge or saddle plus exposed shelves. Readable direction, not radial bumps.

Reject: round mounds, identical repeated hills.

### Mountain

Main ridge → shoulder → shelf → secondary spur → talus/base vegetation. Its structural direction should be visible from the game camera.

Terrain mass leads; 3–5 discontinuous rock outcrops are embedded in the slope and separated by visible terrain. A long continuous stone rib or floating plate is not the v1 Mountain language.

Reject: cone, pyramid, volcano, starburst radial formation.

### Peak

A distinct impassable silhouette with greater vertical severity, narrower upper ridge and pale upper accents. Do not imply a walkable plateau.

The summit is asymmetric and integrated into the mountain foundation. The four v1 archetypes are `alpine_offset`, `broken_summit`, `twin_shoulder`, and `escarpment`; none is a standalone needle or obelisk.

Reject: Mountain simply scaled 130%.

### Coast

A hero system assembled from a shared coast land base plus a finite library of three shoreline morphologies across six world directions. Wet sand, dry sand, shallow-water wash and restrained foam derive from one continuous shoreline curve; adjacent edges share endpoints and require no visible corner patch.

Reject: baked permutation explosion, road-like sand ribbons, standalone corner patches, identical foam ribbon, water holes or seams at joins.

### Shallow sea

Turquoise, low-frequency variation, readable depth and subtle submerged forms. Calmer than a realistic ocean simulation.

### Open sea

Deeper blue-green, broader lighting shapes, minimal visual noise. It acts as visual rest around complex land masses.

## 10. Vegetation

Initial tree languages:

- broadleaf round;
- broadleaf columnar;
- elegant conifer;
- wind-bent/coastal.

A tree includes tapered trunk, visible branch structure and 3–6 irregular foliage masses. Species differ in silhouette before leaf color.

Ground vegetation uses clustered blades/tufts rather than covering the entire surface with equal density.

## 11. Materials

Materials are illustrative rather than physically exhaustive. They should respond consistently to the master lighting while retaining clear value grouping.

- foliage: broad tonal masses, matte, very restrained bump;
- soil/clay: warm, matte, low-frequency mottling;
- stone: cooler, faceted, moderate roughness, subtle mineral variation;
- wood: directional broad banding, no realistic tiny grain;
- metal: selective highlight, restrained metallic response;
- cloth: broad color mass, minimal bump;
- water: broad color/depth variation + small surface normal perturbation.

No material should create high-frequency shimmer after downsampling.

## 12. Lighting

One canonical luminous-fantasy rig:

- large warm key from upper/front-side;
- cool low-energy fill;
- very restrained cool rim to separate complex silhouettes;
- soft neutral world contribution;
- no cinematic black shadows;
- no per-asset relighting to hide modelling problems.

The key/fill relationship should support readable planes rather than dramatic mood shots.

## 13. Civilization architecture

### Auren League

Auren communicates **coordination, civic investment and route thinking**.

Spatial grammar:

- civic centre/plaza;
- deliberate axes;
- route alignments;
- vertical beacons/standards;
- arches/bridges/markers;
- hierarchy between civic building and supporting structures.

Material grammar:

- warm ivory/pale stone;
- deep blue controlled accents;
- gold as small civic/route punctuation;
- restrained warm wood.

Reject: generic fantasy castle, gold-covered city, sterile perfect grid.

### Brasal clans

Brasal communicates **adaptation, practical craft and frontier maintenance**.

Spatial grammar:

- longhouse/workshop anchor;
- work yard;
- kiln/forge/storage;
- structures following available space;
- visible repair and modular additions;
- broad grounded silhouettes.

Material grammar:

- weathered timber;
- stone footings;
- charcoal iron;
- copper repair accents;
- restrained moss/bone neutrals.

Reject: skull village, spike forest, random junk pile, “evil orc” color coding.

## 14. City stages

- Stage 1 = levels 1–2: clear anchor + small support cluster.
- Stage 2 = levels 3–4: recognizable town organization and secondary functions.
- Stage 3 = levels 5–6: stronger landmark hierarchy and denser but still readable settlement.

Growth is communicated by hierarchy/count/organization, not palette change or giant scale jump.

## 15. Unit language

Target body proportion ≈5–5.5 heads. Slightly enlarged hands/head and 10–15% oversized primary equipment improve strategy readability.

Body construction must merge into organic masses after downsampling; visible disconnected cylinders are rejected.

Role reads:

- Settler: travel/founding equipment and marker.
- Worker: practical tool + work pack.
- Explorer: light silhouette + scouting staff/spyglass language.
- Basic soldier: shield + spear; strong stance.
- Patrol ship: compact military hull and clear faction sail/standard.

Faction identity changes posture/equipment/material language without changing the gameplay role into a different class.

## 16. Improvements and infrastructure

Improvements must read from terrain scale without looking like miniature city buildings.

- Farm: field geometry + small practical anchor, not a full village.
- Lumber facility: stacked timber/work platform; forest remains visible.
- Mine: exposed entry/support/ore-working read; hill/mountain remains readable.
- Port: shoreline infrastructure that clearly connects land and sea.
- Road: route continuity is more important than surface decoration.

Road and port endpoints are treated as connection grammar, not freeform art.

## 17. Trama visual language

The Trama is old infrastructure. Its remnants may show:

- route markers;
- broken signal/beacon bases;
- eroded civic masonry;
- repeated three-strand/route geometry;
- repair scars and vegetation reclaiming old structures.

They should suggest **maintenance history and political fragmentation**, not magical catastrophe.

They are presentation-only in the initial prototype and therefore must look obviously non-actionable at gameplay scale.

## 18. Overlays and state

Terrain art remains visible beneath gameplay state. Selection/action/ownership/fog feedback uses redundant shape/value treatment and never relies solely on color.

A selection outline may brighten the hex edge, but must not visually convert terrain into a different biome.

## 19. Motion

Static environment is the default. Non-essential movement is sparse.

- water highlight drift: optional presentation overlay;
- flags: only if subtle and cheap;
- environmental idle motion: deferred unless it demonstrably improves the scene;
- reduced-motion mode disables non-essential motion.

Units reserve bespoke animation budget for movement and attacks; feedback for other actions may use reusable effects.

## 20. Store-facing quality

A strong Vaelora scene should remain recognizable at:

- full 1920×1080 screenshot;
- compact gameplay viewport;
- 320 px wide proxy;
- grayscale/value test.

Marketing compositions may use larger canvases and dedicated framing, but must use the same accepted visual language and must not imply gameplay fidelity that the game cannot deliver.

## 21. Automatic rejection

Reject without subjective debate when:

- an untouched primitive dominates a final silhouette;
- mountain reads as cone/pyramid/volcano;
- tree reads as cylinder + cone/sphere stack;
- external hex footprint changes;
- object clips canvas or floats visibly;
- city/unit contains baked terrain;
- Auren/Brasal require hue to distinguish them;
- coast connections visibly seam;
- repeated variants differ only by random clutter;
- material becomes noisy after 4×→2× reduction;
- lore decoration looks interactable;
- provenance is unclear;
- visual output violates the canonical gameplay meaning.

## 22. Representative slice acceptance

Issue #17 is not complete until real renders include:

- Plains benchmark;
- mixed 19-hex board;
- Stage-2 Auren city;
- Stage-2 Brasal city;
- Basic Soldier for both factions in all six facings;
- coast/water connection stress view;
- grayscale comparison;
- final 2× outputs and in-game-scale capture;
- automated QA report;
- explicit human acceptance.
