# Vaelora — Visual Quality Gate v0.3

## 1. Gate philosophy

A candidate passes only when automated correctness, game readability, art direction, narrative coherence, runtime practicality and commercial presentation all pass.

[Terrain Visual Language v1](TERRAIN_VISUAL_LANGUAGE_V1.md) closes the terrain art-direction baseline only. Its v6.2 source-context approval does not mark individual PNGs accepted or satisfy the issue-17 integrated premium lock in Section 17.

## 2. Automated Gate A — source

Must pass:

- Python syntax;
- no process-random `hash()` seed derivation;
- no module-global random calls;
- no unresolved TODO/FIXME in production modules;
- no prohibited IcoSphere primary-source shortcut;
- manifest schema valid;
- source hashes present;
- production version recorded.

## 3. Automated Gate B — image

Must pass:

- correct final dimensions;
- alpha exists;
- no unit/city/prop clipping safe margin;
- contact shadow exists for applicable family;
- terrain occupies expected frame;
- alpha occupancy within family range;
- no accidental opaque background;
- no nontransparent pixels outside exact overlay expectations.

Warnings become human-review items rather than automatic passes.

## 3.1 Two-stage scoring contract

Sections 4–14 use a **0–5 candidate preflight scale**. Their job is to reject weak work early; `>=4/5` means “professional enough to continue review”, not “visual direction locked”.

Final visual-lock decisions use the **0–10 premium scorecard** in Section 17. No 0–5 score is converted automatically into a 0–10 score, and a 4/5 preflight pass cannot satisfy the >=9.0 premium gate by itself.

## 4. Art Gate C — silhouette

Score 0–5:

- 5: immediately identifiable, distinctive, clean at 75%;
- 4: professional and clear, small refinements possible;
- 3: functional but generic/weak;
- 2: role/category requires inspection;
- 1: confusing;
- 0: wrong category.

Production candidate needs **≥4**.

## 5. Art Gate D — shape craft

Review:

- primary forms do not read as primitives;
- asymmetry is intentional;
- bevel/faceting choices support scale;
- geological/tree/building structure feels constructed, not scattered;
- no visible intersections/tangencies/floating.

Needs **≥4/5**.

## 6. Art Gate E — materials/lighting

Review:

- material families distinguish correctly;
- no plastic uniformity;
- no high-frequency noise after downsample;
- light direction is coherent;
- shadows preserve information;
- palette leaves room for overlays/faction accents.

Needs **≥4/5**.

## 7. Game Gate F — readability

At 75%:

- terrain category recognized quickly;
- unit role recognized;
- city stage readable;
- roads/improvements visible;
- important overlays remain legible;
- decoration does not obscure action.

Any gameplay ambiguity is a **Blocker** regardless of average score.

## 8. Faction Gate G

Auren vs Brasal:

- grayscale distinction;
- planning-language distinction;
- silhouette/material distinction;
- no cultural caricature shortcut;
- same gameplay role still reads as shared role.

Requires **≥4/5** and no Blocker.

## 9. Narrative Gate H

- prop meaning agrees with canon;
- Trama feels infrastructural/historical;
- cosmetic prop does not look actionable;
- faction craft tells believable social story;
- no unapproved magical/resource content.

Any false mechanical affordance is **Major/Blocker** depending on severity.

## 10. Repetition Gate I

7-tile and 19-tile stress:

- no obvious cloned hero object;
- no stripe/seam pattern;
- variation remains same biome;
- negative-space pattern is not mechanically repeated;
- material noise does not tile conspicuously.

Requires **≥4/5**.

## 11. Coast Gate J

- edges meet exact footprint;
- adjacent shoreline edges meet without a visible corner patch, doubled foam or sand overlap;
- shallow→open sea transition is coherent;
- coast remains land, not half-water ambiguous tile;
- port attachment remains possible.

Any visible seam at normal gameplay scale is **Major**.

## 12. Runtime Gate K

Evidence from Godot:

- import profile recorded;
- no unacceptable compression artifact;
- mipmap decision evidenced;
- no obvious shimmer at camera motion;
- alpha/overdraw within measured profile;
- representative frame/memory impact recorded.

Until Stage-2 performance budgets are measured, this gate records evidence and flags regression rather than inventing hard frame numbers.

## 13. Commercial Gate L

At 1920×1080 and 320 px:

- scene has one or two clear focal areas;
- world identity is visible;
- terrain reads cleanly;
- screenshot is attractive without debug/UI clutter;
- asset does not look like generic low-poly marketplace art.

Requires **≥4/5** before marketing use.

## 14. Scorecard

Suggested candidate review table:

| Dimension | Score 0–5 | Weight |
|---|---:|---:|
| Gameplay readability | | 25% |
| Silhouette/shape craft | | 20% |
| Composition/negative space | | 15% |
| Materials/lighting | | 15% |
| Vaelora/faction identity | | 15% |
| Technical/runtime quality | | 5% |
| Commercial screenshot value | | 5% |

Acceptance target: **weighted ≥4.2/5**, every critical category ≥4, no Blocker, no unresolved Major.

This score is a review aid, not a loophole: a serious gameplay or registration failure cannot be averaged away.

## 15. Defect severity

### Blocker

Wrong footprint/camera, gameplay ambiguity, clipping, false mechanic, missing provenance, clearly derivative copied design, broken runtime composition.

### Major

Generic primary silhouette, hue-only faction distinction, obvious tile repetition, coast seam, plastic/noisy material, weak 75% read.

### Minor

Small decorative tangent, subtle palette imbalance, low-value microdetail issue that does not affect gameplay.

## 16. Required acceptance evidence for issue #17

- exact seed list;
- Blender 5.2.3 render version;
- source hashes/manifests;
- Plains benchmark;
- 19-hex mixed board;
- coast stress;
- Auren/Brasal Stage-2 cities;
- Basic Soldiers six facings;
- final 2× contact sheet;
- grayscale;
- 320 proxy;
- Godot 75/100/125 screenshot;
- automated reports;
- human decision recorded.

## 17. v0.3.2 premium lock

The representative slice is not visually locked merely because every automated check passes. For the v0.3.2 premium reconciliation pass, human review uses a 0–10 scorecard with these release-direction thresholds:

The premium scorecard evaluates these areas independently so weak families cannot hide behind an average: **terrain base, cities, forests, mountains/peaks, water, coast, soldiers, unit framing and overall composition**. Forest and mountain are intentionally separated; water is scored separately from coast.


- every reviewed area **>= 9.0**;
- mean of area scores **>= 9.3**;
- **zero open Blocker or Major** defects;
- exact 75/100/125% gameplay-scale evidence;
- color and grayscale evidence;
- 320 px commercial-read proxy;
- Blender source-context benchmark **and** actual Godot runtime-composition screenshot;
- all six unit facings and all three city stages represented;
- coast stress evidence built from the same finite shoreline library used by runtime.

A score of 10 is aspirational and means no obvious defect remains in normal gameplay use, representative close-up, grayscale, commercial-small-read or narrative coherence. It is not granted automatically and is not required for an individual asset to remain a candidate.

The scorecard is created by `tools/art/create_quality_scorecard.py` and checked by `tools/art/validate_quality_scorecard.py`. The validator only verifies the integrity of **human-entered** scores and open-severity lists; it never judges art automatically.

### Runtime-fidelity rule

A Blender benchmark cannot approve geometry that the 2D game cannot reproduce. Review scenes must instantiate the same finite seed/variant vocabulary used for exported terrain, coast, city and unit sprites. Final issue-17 acceptance additionally requires a screenshot from the real Godot board scene using accepted 2D assets and layer/import settings.
