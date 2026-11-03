# Vaelora — Premium Visual Convergence v0.3.2

## 1. Objective

v0.3.2 is the first iteration whose explicit goal is **not** to establish a viable art direction, but to move every currently benchmarked visual family toward a premium commercial bar.

Baseline from the v0.3/v0.3.1 review:

| Area | Baseline | v0.3.2 objective |
|---|---:|---:|
| Terrain general | 8/10 | >=9/10 |
| Cities | 7.5/10 | >=9/10 |
| Forests/mountains | 8/10 | >=9/10 |
| Soldiers | 6.5/10 | >=9/10 |
| Unit framing | PASS | remain PASS |
| Coast | 4.5/10 | >=9/10 |
| Overall board | ~7.8/10 | >=9/10 |

The aspiration is 9.5+. A score of 8 is considered **good but not accepted** for the premium gate.

## 2. Six simultaneous review lenses

Every v0.3.2 decision must survive all six lenses.

### Art direction

Does the asset have an intentional silhouette, material hierarchy, authored composition and recognizable Vaelora signature?

### Game design/readability

Can the player identify terrain, role, city/faction and strategic state at 75% without inspection?

### Narrative/worldbuilding

Does the form communicate the society/geology/history that actually exists in canon, without inventing mechanics?

### Technical art

Does it preserve exact registration, deterministic generation, fixed camera, canvas, alpha safety, runtime modularity and sensible texture cost?

### Production/editorial

Can the decision scale to the full catalog without hand-fixing every output or creating unmaintainable combinations?

### Commercial presentation

Does gameplay itself produce a screenshot that would look intentional beside professional strategy titles, without relying on a separate marketing art style?

## 3. Terrain general — 8 -> 9+

### Observed strengths

- extracted-world geological sides are distinctive;
- terrain remains immediately readable;
- sculpted top already avoids flat cookie tiles;
- color family is cohesive.

### Remaining 8/10 symptoms

- top relief can read slightly procedural/radial;
- microdetail distribution is still somewhat uniformly random;
- Meadow/Plains distinction can rely too much on color at distance;
- benchmark grid spacing bug contaminated earlier coast/terrain judgement;
- material response is pleasant but slightly muted.

### v0.3.2 changes

1. Four-ring coherent top-surface sculpt using shared phases instead of independent ring phases.
2. Exact canonical axial spacing constants with host-side invariant test.
3. Meadow ground detail grouped into quiet/active authored clusters.
4. Plains grass organized into lower directional lanes.
5. More luminous canonical light rig with restrained exposure lift.
6. Premium nine-terrain gallery for independent review.

### 9+ acceptance

- no tile overlap/gap;
- Meadow vs Plains readable in grayscale/value rhythm;
- surface feels naturally sculpted, not noise-displaced;
- detail disappears gracefully at 75%;
- close-up remains materially interesting at 125%;
- geology reads as one world-cut system across all land categories.

## 4. Cities — 7.5 -> 9+

### Observed strengths

- Auren and Brasal already separate strongly by color and mass;
- grayscale city distinction is promising;
- civic plaza vs workyard logic is visible;
- overall scale works on the board.

### Remaining 7.5 symptoms

- some buildings still read as simple block + roof;
- repeated house masses can dominate the cultural planning story;
- facade depth is under-resolved at 125%;
- Brasal dark roof family can collapse into one charcoal mass;
- Auren can still drift toward generic wealthy-human architecture.

### v0.3.2 changes

#### Auren

- stone plinths establish deliberate civic construction;
- eave shadows create facade depth;
- window grouping and gold strand become secondary hierarchy rather than flat decoration;
- civic beacon remains the dominant vertical landmark;
- plaza remains the primary organizational mass.

#### Brasal

- visible structural braces;
- copper/metal repair patches;
- workshop lean-to canopy;
- stronger functional construction cues around kiln/workyard;
- roof/wood/metal hierarchy prevents one dark blob.

### 9+ acceptance

- Auren reads as planned civic infrastructure without color;
- Brasal reads as adaptive repair/work culture without color;
- each city contains one dominant landmark plus supporting mass hierarchy;
- facade craft survives 125% without becoming noisy at 75%;
- neither reads as an asset-pack medieval town/orc village.

## 5. Forests and mountains — 8 -> 9+

### Forest changes

- species-specific foliage value families;
- root flares ground trunks;
- understory shrubs replace some generic grass filler;
- hero/support hierarchy remains authored by templates;
- central/front unit-clear space remains protected.

### Mountain changes

- existing directional ridge system is retained;
- additional base rock punctuation improves grounding;
- peak/mountain distinction remains structural, not just scale;
- material/light lift improves plane separation.

### 9+ acceptance

Forest:

- reads as one designed ecosystem, not seven independent trees;
- species differ before color;
- undergrowth joins the mass but never blocks units;
- no repeated foliage-ball silhouette.

Mountain/Peak:

- primary ridge direction obvious;
- secondary geology supports rather than mirrors the hero mass;
- no cone/volcano read;
- Peak reads impassable immediately;
- base feels anchored to tile rather than placed on top.

## 6. Soldiers — 6.5 -> 9+

### v0.3.1 achievement

- framing contract solved;
- upper/lower limbs introduced;
- faction stance differentiated;
- 75% role read improved.

### Remaining symptoms

- neck remains too long/isolated;
- torso/pelvis still show stacked-box ancestry;
- feet/hands are mechanically shaped;
- shoulder transitions still segmented;
- faction body language is present but not yet strong enough without color/equipment.

### Body v3 changes

- torso and pelvis become continuous layered convex anatomy hulls;
- neck shortened and thickened;
- head slightly enlarged to stylized miniature ratio;
- feet become sculpted hulls instead of blocks;
- arm bend increased to show weight and grip;
- Auren shoulder language reduced/ordered;
- Brasal body width/lean/asymmetry strengthened;
- framing remains `4.35` plus reviewed `0.08` framing offset.

### 9+ acceptance

- no geometric mannequin read at 125%;
- compact stylized miniature at 75%;
- same gameplay role is obvious across factions;
- Auren/Brassal differ in grayscale silhouette/body language;
- all six facings have comparable perceived size/quality;
- safety margin PASS remains stable.

## 7. Coast — 4.5 -> 9+

### Root-cause findings

Two problems were conflated in earlier reviews:

1. shoreline strips exposed modular construction;
2. the review map used **half the correct vertical axial spacing**, causing physical land/sea tile overlap and creating impossible blue triangles inside land.

The grid bug must be corrected before Coast System quality is judged again.

### Coast System v3 architecture

The 6 independent edge + corner-resolver approach is retired for accepted coast art.

Instead:

- each coast tile derives a 6-bit sea-neighbour mask;
- there are 63 non-empty mask outputs;
- each contiguous run of sea-facing edges is generated as one shoreline;
- adjacent edge endpoints share exact radial-bisector dry/wet/boundary points;
- dry/wet bands derive from the same curve;
- foam follows short portions of that curve;
- no water wedge is painted across land;
- no standalone corner geometry is visible.

This is a deliberate production trade: 63 small overlays are cheaper than a visibly modular premium coastline and do not multiply simulation states or hand-authored source files.

### 9+ acceptance

- no triangles/holes/overlap;
- no L-shaped/path-like sand;
- no visible corner component;
- beach width varies organically but remains restrained;
- foam is sparse and secondary;
- shore reads as erosion/transition, never road/pier;
- coast tile still reads as land;
- future port attachment space remains available.

## 8. Overall board — ~7.8 -> 9+

Overall score is reviewed only after every family passes independently.

v0.3.2 should improve the board through:

- corrected true hex tessellation;
- brighter but controlled plane separation;
- fewer uniform microdetail fields;
- stronger city facade hierarchy;
- more organic unit anatomy;
- coast no longer dominating attention through defects;
- water remaining visual rest.

A premium board should be pleasant to inspect at 125%, effortless to parse at 75%, and recognizable as Vaelora in a 320 px proxy.

## 9. Fixed review evidence

- `22000` Plains;
- `22100` mixed benchmark;
- `23000` representative factions;
- `23100` coast stress;
- `23200` premium nine-terrain gallery;
- `23300` premium faction showcase.

Every A/B uses the same semantic seed. A prettier replacement seed is not accepted as a fix.

## 10. Acceptance rule

The premium scorecard does not average away weakness.

Required:

- terrain general >=9;
- cities >=9;
- forests/mountains >=9;
- soldiers >=9;
- coast >=9;
- overall >=9;
- unit framing PASS;
- automated QA PASS;
- no Blocker;
- no Major;
- explicit human acceptance.

If one family scores 8.9, v0.3.2 is still a review candidate, not an accepted visual lock.
