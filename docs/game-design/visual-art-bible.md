# Visual Art Bible — Initial Prototype

**Status:** Stage 1 visual direction and asset contract documented; representative art-slice acceptance is still pending.
**Scope:** The initial Auren League and Brasal clans prototype. This document defines visual production, not gameplay rules or evidence of platform performance.

## Visual direction

Use a **stylized painterly 2.5D language**: compact low-poly volumes, broad readable facets, soft directional light, and restrained material texture. Gameplay remains a 2D fixed-dimetric strategy map; the 2.5D treatment is a rendering method, not a change to simulation, camera interaction, or rules. Avoid both flat cutout/vector-only art and miniature-diorama realism. Keep silhouettes simplified and deliberate, geometry economical, facet edges broad rather than noisy, shadows soft and shallow, and surface variation painterly rather than procedural-looking. Shared terrain stays natural and subdued; faction and interaction accents are controlled. Terrain categories must remain distinguishable through shape, luminance, and texture, not hue alone. The existing faction palettes and heraldry in [World and Civilizations](world-and-civilizations.md) are authoritative. Do not imitate another game's characters, faction motifs, exact assets, or distinctive compositions; take only general lessons in low-poly simplification, isometric readability, and small-screen hierarchy. Do not use photorealistic rendering or texture that obscures state. Darker palettes and alternate setting themes are future scope.

### Reference and interpretation

The user-selected reference is the broad, readable, faceted low-poly/isometric language associated with *The Battle of Polytopia*, adapted to Vaelora's own painterly material direction and original faction/world identity. A public interview describes Polytopia's graphics as colorful and blocky, but does not document its production pipeline; this is a visual reference, not a claim about its tools or mesh construction ([Sifted interview with Felix Ekenstam](https://sifted.eu/articles/elon-musk-polytopia-video-game)). Do not use or trace Polytopia assets. The implementation study is created from original Blender geometry and materials.

Internal functional-development builds may use explicitly labeled provisional visuals while gameplay systems are being completed. Keep these visuals isolated from final assets and do not represent them as accepted art. Generated concepts, diagrams, editor previews, and unreviewed exports do not satisfy the representative-slice acceptance gate; final-quality assets are required before the accepted prototype and Stage 3 exit.

## Camera, scale, and hierarchy

- Use the GDD's fixed 2:1 dimetric projection and fixed orientation, with three discrete zoom levels: 75% overview, 100% standard, and 125% close. Use an orthographic camera; 3D forms must preserve the map's established 2D screen-space footprint and never imply a different playable surface.
- Model shallow terrain relief and simplified faceted assets in 3D, then render them as 2D game imagery. Avoid thick display plinths, dramatic perspective, hard studio shadows, glossy materials, and toy-like proportions. Use broad planes, soft painterly light, restrained roughness/texture, and controlled ambient fill to give volume without visual heaviness.
- Author and export at 2× the 100% reference dimensions. Preserve deliberate texture and edge readability at all three zooms; do not rely on detail visible only at close zoom.
- Validate the 75% view at the compact 720 × 540 logical 4:3 viewport. Also inspect 960 × 540, 1280 × 720, and 1920 × 1080, including 200% UI scale, under GDD §13's viewport and accessibility contract.
- Keep each unit and its animation within its own hex footprint. Distinguish Auren and Brasal with silhouette/material design as well as controlled accents.
- Represent city levels 1–2, 3–4, and 5–6 as three visual stages per civilization. Show growth primarily through building count and height, not palette changes alone.
- Keep terrain/environment presentation beneath clear gameplay overlays. Selection uses a thin hex outline plus a redundant UI indication without hiding terrain or units. Roads, improvements, ownership, fog, and actionable states must remain independently legible.
- The map may extend beneath cutouts; controls, text, focus indicators, and confirmations stay within platform safe areas. Do not communicate an essential state through color alone.

## Asset families and production contract

| Family | Initial specification |
|---|---|
| Terrain | One reusable tile per canonical GDD terrain category; civilization-neutral shared materials; shape, luminance, and restrained texture distinguish categories. At 100% the logical cell envelope is 128 × 64 px; source/export is 256 × 128 px at 2×. |
| Cities | Three growth stages per civilization (levels 1–2, 3–4, 5–6); count and height communicate stage. Use a 256 × 128 px logical canvas (512 × 256 px at 2×), bottom-centered on the city tile; art may rise above the tile but must not obscure adjacent actionable units. |
| Units | Idle pose for each initial unit, with faction-specific identity where applicable; six facing directions; remain inside one hex. Use a 128 × 64 px logical cell canvas (256 × 128 px at 2×). |
| Improvements and roads | Independent overlays on reusable terrain; road segments remain legible as connected routes. Use the terrain-cell canvas and registration. |
| Fog | Separate presentation layer distinguishing unexplored, explored, and currently visible states without changing simulation state; align to terrain-cell canvas. |
| Combat effects | Reusable effects separate from unit sprites; no more than six frames at 12 fps per effect. |
| HUD and menus | Clean forms with readable labels, focus, selection, action, confirmation, warning, and error states; no color-only status. |

Use transparent PNG for game-ready 2D assets. Preserve editable source files and project files where applicable; `.blend` is optional for assets authored with Blender, not a runtime requirement. Keep static assets individual. Export a separate PNG spritesheet for each unit/animation, one row per hex direction and frames across columns; frame dimensions match the family canvas above. Use lowercase `snake_case` names that identify civilization where applicable, asset/type, action or variant, and resolution; put `_2x` immediately before the extension for 2× exports. Record source ownership, provenance, license, and import requirements for external assets; exclude assets with unclear rights.

## Animation budget

- Idle units and environmental elements are static.
- Bespoke unit animation is limited to movement and melee/ranged attacks. Other actions use brief reusable feedback.
- Movement uses a reusable cycle of at most six frames at 12 fps; it may repeat along a path, but the unit remains within its current hex until the authoritative move completes and must not visually imply a rejected move succeeded.
- Melee and ranged attacks last at most 0.5 seconds and use at most six frames at 12 fps. Each pose/action supports all six hex directions.
- Ranged attacks show the firing action and target damage response; a projectile need not traverse intervening hexes. Attacker and target animations each observe the six-frame/12-fps limit.
- Non-essential motion respects the reduced-motion setting in GDD §13.

## Representative slice and acceptance

The representative slice is one shared Plains hex, one level 3–4 city and one Basic soldier for each prototype civilization. Review terrain, city and unit at 75%, 100%, and 125%, including the compact 720 × 540 viewport. Record source files, provenance/license, export settings, viewport captures, and defects; assess terrain readability, faction silhouettes, visual hierarchy, non-color cues, and consistency with this bible and the canon faction briefs.

[`art-samples/prototype-art-direction.svg`](art-samples/prototype-art-direction.svg) and its PNG export are an internally authored **conceptual study only**. They demonstrate composition and an alternative no-MCP workflow; they are not final-quality 2.5D assets, have not passed the quality review, and do not establish import, runtime, accessibility, or platform acceptance. The Blender study under `art-samples/issue_17/` remains an unaccepted candidate that may inform internal functional visuals but is not a production asset. Neither sample should be represented as accepted. Exact shared-terrain palette values and visual-slice acceptance remain evidence gates after gameplay functionality is complete and before Stage 3 exits; gameplay implementation may proceed before this art gate, but the accepted prototype may not.
