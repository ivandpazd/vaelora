# Persistent OpenCode / Blender MCP contract — Vaelora Art Pipeline v0.3

You are working on **Vaelora**, an original commercial turn-based fantasy strategy game.

Your task is not “generate low-poly art”. You are operating a controlled visual-development system whose target identity is **Vaelora Sculpted Diorama**.

## Mandatory reading before any visual change

Read, in this order:

1. `AGENTS.md`
2. `README.md`
3. `docs/game-design/game-design-document.md`
4. `docs/game-design/world-and-civilizations.md`
5. `docs/game-design/visual-development-framework.md`
6. `docs/game-design/visual-art-bible.md`
7. `docs/game-design/TERRAIN_VISUAL_LANGUAGE_V1.md` for terrain work
8. the narrow visual document for the current family
9. `docs/game-design/visual-quality-gate.md`
10. `docs/game-design/art-production-pipeline.md`
11. `docs/technical/godot-art-integration.md`

If those documents conflict, STOP and report the conflict. Do not decide silently.

## Product boundary

Godot runtime is 2D with a fixed 2:1 dimetric presentation. Blender is an authoring/render tool. Final board assets are transparent 2D sprites/overlays, not a conversion of the project into runtime 3D.

The current terrain appearance decision is [Terrain Visual Language v1](../../docs/game-design/TERRAIN_VISUAL_LANGUAGE_V1.md) at Terrain Suite `v6.2-rc1`: Mountain/Peak use the final v6.2 forms; Water, Coast, Meadow, Plains, Hills, Forest, Desert, and Snow remain frozen from v6.1. This does not waive the asset-acceptance or Godot runtime gates below.

Do not add gameplay rules, unique units, unique buildings, resources, biome types, interactive ruins or visual affordances not approved by the GDD.

## Style identity

Target:

> hand-crafted stylized fantasy landscape, sculpted forms, painterly procedural materials, orthographic board-game readability, controlled mid-frequency detail, luminous fantasy lighting.

Avoid using “low poly” as the primary target phrase. Polygon economy is a production property, not the aesthetic identity.

## Multi-role review sequence

Before changing a generator, evaluate the request from all five roles:

### 1. Gameplay-readability reviewer

- What category/state must be readable at 75% zoom?
- Which area must remain clear for unit/road/overlay information?
- Could any cosmetic detail imply a mechanic?

### 2. Art director

- What is the macro silhouette?
- What are the hero/support masses?
- Which material response defines the object?
- What would make the output look generic/procedural?

### 3. Narrative/world reviewer

- What does the object say about Vaelora?
- Is that statement supported by current canon?
- If faction-specific, does it express social organization/craft instead of stereotype?

### 4. Technical artist

- Does it preserve registration/canvas/camera?
- Is the seed deterministic?
- Is the output modular rather than combinatorial?
- Will transparent area/texture count remain practical?

### 5. QA reviewer

- Which automatic gate and human evidence will prove success?
- Which exact existing seed should be regenerated for A/B comparison?

Only then modify code.

## Modelling hard rules

### General

- Do not leave an untouched primitive as a primary visible form.
- Use reusable constructors and named composition templates.
- Preserve the exact external hex footprint.
- Interior relief must fall to canonical edge elevation.
- Use deliberate negative space.
- Avoid uniform random scatter.
- Avoid symmetry unless the faction/composition explicitly calls for it.

### Rocks

Use authored irregular convex forms/planes. Do not use IcoSphere or random rotated cubes as the final source.

### Mountains

Build directional geological structure:

`main ridge -> shoulder -> shelf -> secondary spur -> talus`

Never cone/pyramid/volcano/starburst.

### Trees

Build:

`tapered trunk -> visible branches -> 3–6 irregular foliage masses`

Species must differ by silhouette. No cylinder + cone. No identical ball clusters.

### Water

Static render must look finished. Use broad low-frequency color/depth response plus restrained highlight forms. Do not rely on a later Godot shader to rescue weak static water.

## Faction hard rules

### Auren

Communicate civic coordination through plaza, axes, routes, arches, beacons and hierarchy. Gold is accent only. Do not make a generic castle city.

### Brasal

Communicate adaptive frontier craft through longhouse/workshop, yard, storage, kiln, repair bands and grounded broad silhouettes. Do not use skull/spike/horn shorthand.

Auren and Brasal must remain distinguishable in grayscale.

## Units

Shared roles remain shared roles. Different faction equipment/material language must not imply different mechanics.

Use approximately 5–5.5-head stylization, slightly enlarged equipment, six canonical facings and compact tile containment.

## Procedural randomness

Use local `random.Random(seed)` only.

Derive sub-seeds through `vaelora_contract.derive_seed(root_seed, semantic_parts...)`.

Never use Python `hash()`.

Never create variation merely by increasing random jitter. Variation should come from designed templates/ranges.

## Camera/light

Never change the camera per asset.

Use the canonical render module. Never relight one asset to hide shape/material problems.

## Output lifecycle

A successful render is only `benchmark` or `production_candidate`.

You may NOT mark an asset `accepted` or `shipped`. Human approval is required.

## First review sequence

Do not generate the full catalog first.

1. Plains seed `22000`.
2. Mixed 19-hex benchmark seed `22100`.
3. Faction slice seed `23000`.
4. Coast stress seed `23100`.
5. Run host-side v0.3 gate.
6. Review final 2×, grayscale, gameplay-scale and 320 px outputs.
7. Fix Blocker/Major issues in source.
8. Regenerate the SAME seed and show A/B.

Only expand after explicit approval.

## Automatic rejection triggers

Reject your own output if any is true:

- primary primitive read;
- generic marketplace low-poly look;
- unreadable 75% silhouette;
- city factions distinguished mainly by hue;
- forest hides unit window;
- coastline has visible seam/corner double-up;
- mountain reads radial/conical;
- texture/material becomes noisy after downsample;
- prop looks interactable but is cosmetic;
- object floats/intersects visibly;
- camera/framing drift;
- canvas clipping;
- external model/texture with unclear rights;
- change invents gameplay/lore.

## A/B improvement rule

When asked to “make it better”:

1. identify one or more failing named gates;
2. change the generator/material/composition contract;
3. render same seed;
4. compare side by side at final 2× and gameplay scale;
5. explain what improved and what remains unresolved.

Do not replace a weak seed with a prettier random seed.

## Commercial quality bar

Do not ask “is this good for an indie?” Ask:

- would this asset look intentional beside professional strategy-game screenshots?
- is Vaelora recognizable without copying another title?
- does the board remain easy to read while still looking desirable in a Steam screenshot?

If not, keep iterating at the benchmark stage.

## v0.3.2-r2 premium acceptance override

The v0.3.2-r2 visual pass raises the human-review threshold. Do not describe an asset as accepted, final, production-ready, or complete unless all of the following are true:

- its reviewed area scores at least 9.0/10;
- the overall visual slice averages at least 9.3/10;
- there are no Blocker or Major defects;
- the relevant fixed-seed A/B comparison has been reviewed;
- 75/100/125%, grayscale and normal screenshot views all pass;
- technical QA passes;
- a human explicitly accepts it.

For v0.3.2-r2, pay particular attention to:

1. exact pointy-top axial spacing and zero tile overlap;
2. Coast System v4 continuity: no corner patch, road-like beach, water hole or floating foam;
3. sculpted terrain surfaces without obvious radial topology;
4. city growth stages and grayscale faction identity;
5. tree species/material hierarchy and grounded trunks;
6. mountain primary/secondary geological hierarchy;
7. Character Body v3 anatomy, pose, six-facing consistency and faction silhouette;
8. commercial-read quality at 320 px without sacrificing long-session readability.

9. benchmark/runtime fidelity: review scenes may only instantiate finite seed/variant assets that the 2D runtime can reproduce;
10. surface grounding: terrain decoration must sit on the actual sculpted surface;
11. final visual lock requires a real Godot runtime-composition screenshot, not only a Blender benchmark.

Never improve the review result by changing the fixed benchmark seed.
