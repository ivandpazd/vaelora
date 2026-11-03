# Vaelora — Visual Development Framework v0.3

**Status:** master production framework for Stage 1 design lock and Stage 2 visual vertical slice.

This document is the entry point for every visual task. It does not replace the GDD, world canon or technical architecture. It defines how art, gameplay readability, narrative, production engineering, accessibility and commercial presentation are reconciled without creating conflicting sources of truth.

## 1. Product-level visual objective

Vaelora must look like a deliberately authored commercial strategy game, not a procedural demo and not an imitation of another hex strategy title. The visual promise is:

> **A luminous sculpted fantasy world presented as a premium strategic diorama: instantly readable from gameplay distance, rich enough to reward close inspection, and recognizably Vaelora without the logo.**

The visual system is successful only when all of these are true at once:

- the player reads terrain, units, cities and actions quickly;
- the world feels handcrafted even when generated procedurally;
- Auren and Brasal communicate different societies through planning, craft and silhouette;
- the Trama gives the setting a recurring visual language without inventing mechanics;
- runtime assets remain practical for Android, Web and desktop targets;
- screenshots are attractive enough to sell the fantasy of the game on Steam;
- asset generation is reproducible, reviewable and legally traceable.

## 2. Six review perspectives

Every production candidate is reviewed through six lenses. A pass in one lens cannot cancel a failure in another.

### 2.1 Art direction

Questions:

- Is the silhouette authored rather than primitive?
- Are macro, meso and micro detail correctly balanced?
- Are materials distinct without becoming photorealistic?
- Is the lighting coherent with the master scene?
- Does the asset contribute to the Sculpted Diorama identity?

### 2.2 Game design and readability

Questions:

- Can the gameplay category be recognized at 75% zoom?
- Does decoration obscure a unit, road, improvement or selection state?
- Could a cosmetic object be mistaken for an actionable object?
- Does the visual hierarchy match gameplay priority?
- Does the asset remain readable without relying on hue alone?

### 2.3 Narrative and worldbuilding

Questions:

- Does the object imply a believable place in Vaelora?
- Does it respect the grounded political/infrastructure tone of the Trama?
- Does faction architecture communicate how the society organizes work and space?
- Does environmental storytelling support existing canon rather than inventing lore or mechanics?

### 2.4 Technical development

Questions:

- Is the asset reproducible from source + seed?
- Does it respect exact registration, canvas, alpha and import contracts?
- Does it fit texture, overdraw and batching budgets?
- Does it avoid assumptions incompatible with Compatibility renderer, Web or Android?
- Can the same content ID survive visual revision without becoming a save dependency?

### 2.5 Production/editorial quality

Questions:

- Is there exactly one canonical source for the decision?
- Is the asset named, versioned and manifested consistently?
- Is its lifecycle state explicit?
- Are source rights and provenance recorded?
- Could another contributor reproduce the result without oral context?

### 2.6 Commercial presentation

Questions:

- Does it improve a 1920×1080 gameplay screenshot?
- Does it survive a 320 px thumbnail proxy?
- Does it contribute a recognizable visual hook for store capsules?
- Is the screenshot honest to gameplay rather than a separate impossible art style?

## 3. Source-of-truth map

| Decision | Canonical document |
|---|---|
| Gameplay meaning, legal terrain, unit/building roles | GDD |
| Lore, Trama, faction canon | `world-and-civilizations.md` |
| Overall art identity and hierarchy | `visual-art-bible.md` |
| Closed terrain-family art-direction baseline and evidence boundary | `TERRAIN_VISUAL_LANGUAGE_V1.md` |
| Shape construction | `visual-shape-language.md` |
| Palette/material response | `visual-material-palette.md` |
| Composition/negative space | `visual-composition-language.md` |
| Environmental visual design | `environment-art-direction.md` |
| Faction visual differentiation | `faction-visual-language.md` |
| Unit silhouettes and animation | `unit-visual-language.md` |
| Narrative use of visual props | `visual-narrative-language.md` |
| Accessibility/readability | `visual-accessibility-readability.md` |
| UI visual language | `ui-visual-language.md` |
| VFX/feedback language | `vfx-feedback-language.md` |
| Exhaustive production inventory | `asset-catalog.md` |
| Blender → PNG → Godot workflow | `art-production-pipeline.md` |
| Godot import/runtime composition | `../technical/godot-art-integration.md` |
| Performance/memory validation | `../technical/art-performance-budget.md` |
| Acceptance rubric | `visual-quality-gate.md` |
| Production order | `prototype-visual-roadmap.md` |
| Store/capsule/screenshot strategy | `steam-visual-strategy.md` |

When two documents overlap, the table above decides ownership. Supporting documents may reference a rule but should not redefine it.

## 4. Asset lifecycle

Every visual asset has one explicit lifecycle state:

1. **Concept** — explores form; never enters gameplay builds advertised as final.
2. **Benchmark** — generated specifically to test a rule or quality target.
3. **Production candidate** — source-complete and passes automated QA; awaiting human art/game review.
4. **Accepted** — approved against the current Art Bible and production pin.
5. **Shipped** — included in a promoted/release build with final provenance.
6. **Rejected** — retained only as evidence/reference; never silently reused.

A generated mesh or successful render is not an accepted asset.

## 5. Definition of “professional” for Vaelora

Professional does not mean maximum geometry or realism. For this game it means:

- intentional silhouette;
- consistent visual grammar;
- stable camera and scale;
- materials with controlled response;
- no visible procedural accidents;
- no accidental tangencies/floating/intersections;
- readable state at actual gameplay scale;
- reproducible source and QA evidence;
- deliberate variants rather than noise for its own sake;
- coherent marketing screenshots produced from real game assets.

## 6. Hard boundary: art may not invent game rules

Visual production may add cosmetic variation and presentation-only Trama remnants only within the accepted canon. It may not add:

- collectible-looking objects;
- magical resource nodes;
- faction-exclusive buildings not present in the GDD;
- terrain categories with mechanical-looking affordances;
- roads, bridges or ports that imply unsupported movement rules;
- weapon classes not in the roster;
- interactive-looking ruins with no interaction.

If an art idea would be better with a new mechanic, open a design decision rather than smuggling the mechanic into the art.

## 7. Quality philosophy

Use the following order whenever there is tension:

**readability → identity → composition → material richness → microdetail**.

The team may intentionally simplify a beautiful model if it reads better in strategy view. It may not add microdetail to compensate for a weak silhouette.

## 8. Human approval points

Human approval is mandatory after:

- Plains benchmark;
- 19-hex mixed-terrain benchmark;
- representative Auren/Brasal city + soldier slice;
- coast stress test;
- first complete improvement set;
- first complete unit-role set;
- final prototype visual integration scene;
- Steam screenshot/capsule art direction.

AI tooling may iterate between approvals, but it cannot promote the asset state to `accepted` by itself.
