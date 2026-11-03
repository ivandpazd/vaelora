# Visual reconciliation — v0.3.2-r2

**Historical record:** this document preserves the r2 decisions and review vocabulary. The current terrain appearance baseline is [Terrain Visual Language v1](../game-design/TERRAIN_VISUAL_LANGUAGE_V1.md); the full premium and Godot runtime gates remain open.

**Purpose:** preserve the strongest accepted/liked work from v0.3/v0.3.1 while improving authored variation, professional readability discipline and premium review coverage before further rendering.

## 1. Preserved anchors

These are intentionally retained unless new visual evidence proves they regress:

- Art identity: `vaelora-sculpted-diorama-v2`.
- Palette family and luminous-fantasy lighting intent.
- Fixed 45° yaw / 30° elevation orthographic camera.
- 4× source render -> premultiplied-alpha Lanczos -> 2× final PNG.
- exact hex registration and geological side-wall concept.
- forest negative-space grammar.
- directional ridge/spur/shelf mountain language.
- Stage-2 Auren civic/order composition.
- Stage-2 Brasal workshop/yard/repair composition.
- Basic Soldier canvas/framing baseline: ortho 4.35, frame Z offset 0.08.
- finite 32-terrain / 36-coast / 6-city-stage / 12-soldier-facing review vocabulary.

## 2. Problems found after r1 review

### Variant authorship was still uneven

Forest already used authored templates, while Meadow/Plains depended mainly on random placement/count changes and Hills/Mountains chose their principal direction from seed. This can produce deterministic variation without strong art-direction intent.

**r2 resolution:** Meadow and Plains now use four authored composition templates each; Hills/Mountain/Peak variants have authored primary directions with only small deterministic jitter.

### Terrain undulation could still reveal radial construction

The r1 terrain surface had more sectors than v0.3, but its height field was still based on harmonics of angle around the centre. Large captures could still expose a starburst/concentric feel.

**r2 resolution:** the premium surface field now uses low-frequency directional XY plane waves that fade to exactly zero at the perimeter.

### Coast morphology variants were seed variants, not semantic variants

Three coast variants existed, but their identity was largely the product of seed variation.

**r2 resolution:** Coast System v4 defines three explicit cosmetic morphology families: gentle sand shelf, mixed sand/stone, narrow eroded shore. Each has different width/pocket/rock/foam logic while sharing exact endpoints and gameplay meaning.

### Coast stress did not necessarily show all three morphologies

The deterministic tile hash could select duplicate morphology variants in one review image.

**r2 resolution:** the stress scene deliberately forces one example of each finite morphology family while still using the exact exportable library code.

### Basic Soldier head/hands remained too procedural

The v3 body was substantially better, but head and hands still originated from generic/random hull logic.

**r2 resolution:** head planes are authored (chin/jaw/temple/crown), hands use dedicated tapered masses, and small faction silhouette cues are added without changing the accepted framing.

### Premium review could hide weak subfamilies

Forest+Mountain were one score, and Water had no independent premium area.

**r2 resolution:** premium scoring independently covers terrain base, cities, forests, mountains/peaks, water, coast, soldiers, unit framing and overall composition.

### Repetition evidence was specified but not automated

The Art Bible required 7-hex repetition review but the generator did not provide a dedicated command.

**r2 resolution:** `--asset repetition-stress` renders 7-hex flowers for Meadow, Plains, Forest, Hills and Mountain; the complete quality suite includes them.

## 3. Professional readability refinements

The visual contract now explicitly separates:

- Macro/always-readable information;
- Meso/normal-play richness;
- Micro/close-inspection reward.

Purely cosmetic microdetail may later move to an optional presentation layer if real Godot 75% tests show eye fatigue. Gameplay state never depends on that layer.

Value hierarchy is also explicit: units/city landmarks and interaction feedback must dominate environmental decoration at gameplay scale.

## 4. What r2 deliberately does not change blindly

r2 does not redesign the palette, master camera, city Stage-2 ground plans, forest template philosophy, base mountain grammar, sprite dimensions or unit role equipment. Those already have positive evidence and should only move after an A/B render demonstrates a real benefit.

## 5. Acceptance rule

The next source of truth is visual evidence. Do not expand production merely because r2 passes source QA. Use fixed seeds and compare against the preserved v0.3/v0.3.1 images. Final visual lock requires every premium area >=9.0, mean >=9.3, zero open Blocker/Major defects and real Godot composition evidence.
