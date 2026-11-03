# Vaelora — Visual Asset Catalog v0.3

This is the exhaustive initial-prototype visual production inventory. Counts are planning counts, not permission to skip quality gates.

The [Terrain Visual Language v1](TERRAIN_VISUAL_LANGUAGE_V1.md) review suite covers ten visual families, including Desert and Snow. The inventory below is the **initial-prototype runtime plan** derived from the nine gameplay terrain categories; it is not a claim that v6.2 sprites have been exported or that Desert/Snow are new playable categories.

## 1. Shared terrain bases

| Family | Variants | Delivery |
|---|---:|---|
| Meadow | 4 | individual 2× PNG + source/manifest |
| Plains | 4 | same |
| Forest | 4 | same |
| Hills | 4 | same |
| Mountain | 3 | same |
| Peak | 2 | same |
| Coast land base | 3 | same |
| Shallow sea | 4 | same |
| Open sea | 4 | same |

Initial base total: **32** terrain variants.

## 2. Coast modular system

- **3 semantic shoreline morphologies × 2 authored variants × 6 world directions = 36 reusable edge overlays**;
- no visible corner-resolver sprites; adjacent accepted edges share analytically identical endpoints;
- morphology families are `gentle sand shelf`, `mixed sand/stone`, and `narrow eroded shore`; one coast tile selects one authored variant and reuses it for all sea-facing edges;
- one fixed-seed coast stress review scene plus runtime-composition evidence.

Do not produce all neighbor masks as unique baked tiles.

## 3. Neutral environment decoration

Curated reusable library:

- rock slate families: 6–10 forms;
- warm rock families: 4–6;
- grass clump families: 6;
- dry-grass clump families: 4;
- flower clusters: 3 low-density palettes;
- shrubs/undergrowth: 4;
- tree species × form variants: 4 species × 3–4 primary shapes.

These are generator components, not necessarily separately exported runtime sprites.

## 4. Trama hero props

Initial presentation-only props:

1. broken signal beacon;
2. old route/waystone;
3. collapsed signal base.

Each gets 1 accepted hero design plus controlled seed variation if needed. Sparse placement only.

## 5. Road system

Runtime-composable road representation:

- 6 centre-to-edge half segments;
- 1 centre hub/merge treatment;
- optional end cap where presentation requires it;
- city tile connection visual;
- road-on-improvement coexistence test.

Road material remains civilization-neutral in the initial prototype unless an accepted visual-only variation does not alter gameplay clarity.

## 6. Improvements

Each shared improvement receives faction-compatible but mechanically identical visual adaptation where appropriate.

### Farm

- shared field geometry language;
- Auren small support prop set;
- Brasal small support prop set;
- 2–3 cosmetic field-layout variants if repetition requires.

### Lumber facility

- forest remains visible;
- log stack/work platform;
- Auren/Brasal support construction adaptation.

### Mine

- hill/mountain remains identifiable;
- mine mouth/support/ore-work cue;
- faction adaptation in timber/metal details.

### Port

- 6 directional shore orientations or runtime rotation where pixel registration remains exact;
- Auren dock adaptation;
- Brasal dock adaptation;
- ship spawn/readability clearance.

## 7. Cities

Base city sprites:

- Auren Stage 1, 2, 3;
- Brasal Stage 1, 2, 3.

Total base cities: **6**.

City sprites do not bake optional buildings.

## 8. Building attachments

Shared gameplay buildings receive faction-specific visual language but use modular attachments rather than every combination being prebaked.

| Building | Auren attachment | Brasal attachment | Special rule |
|---|---|---|---|
| Granary | yes | yes | compact growth/storage cue |
| Barracks | yes | yes | military training cue, not giant fortress |
| Walls | perimeter overlay | perimeter overlay | stage-compatible perimeter |
| Academy | yes | yes | research/learning cue, no magic tower |

Total primary building attachment designs: **8 + 2 wall overlays** (with stage compatibility tested).

## 9. Units

Shared roles:

- Settler
- Worker
- Explorer
- Basic Soldier
- Patrol Ship

For each civilization:

- 6 facings per idle pose;
- movement animation where approved;
- attack animation for combat roles;
- role/faction silhouette review.

Do not multiply animation scope before the idle role language is accepted.

## 10. Unit animation planning

Maximum bespoke initial animation frame budget per approved action:

- 6 frames × 6 facings;
- 12 fps;
- movement can loop;
- attack ≤0.5 seconds.

Spritesheets remain one animation/faction/role group, not one monolithic sheet for the whole game.

## 11. Fog and board state

Prefer runtime-generated/shader/polygon presentation where practical:

- unexplored;
- explored/not visible;
- visible baseline;
- territory border/fill;
- selection outline;
- legal move/target indication;
- attack target indication;
- city territory claim candidate.

These states require accessibility variants and are not baked into terrain.

## 12. Gameplay effects

Reusable concise effects:

- selection confirmation;
- invalid action feedback;
- move arrival/step feedback;
- melee impact;
- ranged impact;
- city level-up;
- research completion;
- production completion;
- capture/ownership transition;
- victory/defeat presentation.

Effects must respect reduced-motion.

## 13. UI iconography

### Core actions/status

- move;
- attack;
- found city;
- improve;
- road;
- end turn;
- production;
- research;
- coins;
- food/growth;
- production points;
- research points;
- defense;
- vision;
- movement.

### Terrain/improvement

9 terrain icons + Farm/Lumber/Mine/Port/Road.

### Units/buildings

5 unit-role icons + 4 building icons.

### Technology

16 initial technology nodes (12 shared + 2 Auren + 2 Brasal) receive consistent icon language.

### Setup

3 map-type icons, 3 map-size states, 3 difficulty states, victory-mode icons, seed/read-only presentation.

Icons are vector-like/readable presentation assets; they do not need Blender.

## 14. HUD and menus

Visual systems needed:

- main menu;
- new match/setup;
- civilization selection;
- in-game HUD;
- selected unit/city panel;
- city management/territory claim;
- production chooser;
- research tree;
- standings;
- save/load;
- settings/accessibility;
- codex/tutorial;
- victory/match summary;
- confirmation/error messaging.

Art direction should be derived from accepted board art, not designed as a separate fantasy theme.

## 15. Marketing/store assets

Separate deliverables derived from accepted game art:

- Steam header capsule;
- small capsule;
- main capsule;
- vertical capsule;
- library capsule;
- library hero;
- library logo;
- shortcut/app icons;
- minimum six strong gameplay screenshots;
- key art/source composition.

Store graphics are marketing compositions, not runtime textures.

## 16. Audio visual companions

Audio is a separate discipline, but art must provide redundant visual feedback for events that also have sound: turn boundary, warning, combat, production, research, victory.

## 17. Future civilizations

Nymara, Durn, goblins and skeletons are deliberately not production assets for the initial prototype. The shared pipeline must leave room for them without locking their final visual canon now.
