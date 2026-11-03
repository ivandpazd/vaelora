# Vaelora — Visual Composition Language v0.3

This document owns composition: where visual mass is placed, where negative space is protected, how repeated procedural assets avoid looking algorithmic, and how a whole board remains legible.

## 1. Composition is authored grammar

Procedural generation may select and perturb a composition, but may not replace composition with uniform random placement. Every family uses a small number of named templates whose intent can be reviewed.

A good variant changes rhythm while preserving category identity. A bad variant merely changes random coordinates.

## 2. Screen-space assumptions

Because the camera is fixed, composition can be designed intentionally around the view.

For a canonical tile:

- rear third: supports taller mass;
- centre: primary category read;
- lower/front centre: protected visual window;
- six perimeter sectors: connection and adjacency safety;
- centre anchor: potential unit/improvement/city interaction zone.

## 3. Negative-space rules

Negative space is mandatory around:

- unit foot anchor;
- city plaza/entrance;
- road junctions;
- port/shore connection;
- coast endpoints;
- selection outline;
- improvement read.

A forest is not “more forest” because every empty region contains a tree.

## 4. Distribution rhythm

Use groups of unequal size. Prefer rhythms such as:

- 1 hero + 2 support + 3 edge masses;
- 2 hero masses with asymmetric support;
- broad primary mass + counterweight + empty window.

Avoid:

- even radial distribution;
- perfect left/right symmetry outside deliberate civic Auren motifs;
- equal spacing;
- identical rotations;
- random scatter with no focal hierarchy.

## 5. Terrain composition

### Meadow

Primary read is openness. Use micro-clusters at the periphery and preserve broad central calm.

### Plains

Use directional horizontal/dry-grass rhythms and larger exposed-ground shapes. The composition should feel wind-shaped rather than dotted.

### Forest

Use hero trees mostly in the rear/upper silhouette. Support trees frame an opening. Undergrowth bridges trees into groups rather than individual dots.

### Hills

Ridge direction becomes the composition spine. Secondary rocks and vegetation follow it rather than ignoring it.

### Mountain/Peak

Use one primary ridge direction and one meaningful counter-spur. Talus should reinforce gravity and geology, not encircle the centre evenly.

Mountain's separated outcrops and Peak's offset summit are selected from authored forms rather than assembled through uniform scatter. Keep the six-edge safety band and unit anchor legible; see the [terrain v1 closure](TERRAIN_VISUAL_LANGUAGE_V1.md).

### Coast

Shoreline edge is the primary composition. Decorative rocks/sand/foam must lead the eye along it and preserve connection endpoints.

### Sea

Use very low information density. Water is visual rest and should increase the apparent richness of adjacent land by contrast.

## 6. City composition

### Auren

Use deliberate hierarchy:

`civic anchor → plaza/route spine → secondary buildings → route markers`.

Stage growth expands the network rather than only filling every empty gap.

### Brasal

Use work logic:

`workshop/longhouse → yard → storage/kiln → adapted support structures`.

Stage growth should feel accretive and repaired, but still designed.

## 7. Units within a tile

At gameplay scale, a unit is a silhouette placed against terrain, not a small character portrait. Terrain families therefore protect enough central/front quiet space that unit equipment remains readable.

Unit pose should not extend aggressively into neighboring tile space. Long weapons can approach upper canvas regions but must stay inside the family safety envelope.

## 8. Board-level composition

A map screenshot must avoid visual monotony. The renderer should allow naturally occurring patterns such as:

- land mass + calm water breathing room;
- forest cluster adjacent to open meadow/plains;
- relief progression from hills to mountain/peak;
- city as local focal point, not equal in intensity to every tile;
- roads creating readable directional flow.

The procedural map generator owns terrain distribution mechanics. Art does not alter gameplay placement to improve a screenshot. Instead, asset variation and visual density respond to the existing board.

## 9. Variant design

For each terrain family, variants should differ along controlled axes:

- macro relief direction;
- hero/support placement;
- species mix;
- material mottling seed;
- microdetail cluster placement.

They must not differ in a way that implies different gameplay values.

## 10. Repetition stress test

For every family, generate a 7-tile flower and a 19-tile cluster using only that family. Reject if:

- a distinctive rock/tree repeats in an obvious grid;
- all tiles share the same empty/filled regions;
- visual seams create stripes;
- macro shape rotates in a mechanically repetitive pattern;
- the family becomes noisy when seen in bulk.

## 11. Thumbnail test

At 320 px width, only macro and strong meso forms survive. The scene should still show:

- clear land/water separation;
- readable mountains/forest/open terrain;
- city focal points;
- faction contrast;
- route/board structure.

If the thumbnail becomes texture soup, reduce detail rather than sharpening everything.
