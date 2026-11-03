# Terrain Suite v5.0-rc1 General — acceptance gate

## Global blockers

- Any visible prop crosses the logical tile silhouette in an individual family sheet.
- Any terrain family reads as a recolour of another family rather than a distinct macro-shape/material vocabulary.
- Mountain/Peak read as a primitive cone/pyramid dropped on top of the tile.
- Hills can be confused with Meadow at gameplay scale.
- Desert reads as beige Plains or Snow reads as white recolour.
- Water becomes a repeated wave carpet or Coast regresses to road-like sand ribbons.
- The 36-hex benchmark becomes visually noisier than the accepted Meadow 70% density target.

## Target hierarchy

- Meadow: 9+ baseline; no regression.
- Coast: 9-ish baseline; no regression.
- Water: broad quiet read first, glints second.
- Plains: dry/open and clearly distinct from Meadow.
- Hills: multiple ridge masses and saddle visible immediately.
- Mountain: integrated main ridge + spur + buttress + talus.
- Peak: severe vertical silhouette without a walkable plateau.
- Forest: 2-3 canopy masses with readable ground/negative space.
- Desert: dune/erosion language and sparse vegetation.
- Snow: drift/rock language with cold shadow and sparse vegetation.

## Mixed benchmark

The benchmark must preserve a readable visual journey:

open sea -> shallow sea -> coast -> meadow/forest -> plains/hills -> mountain/desert/snow/peak.

No single family may look as if it belongs to an older art generation.

## Reviewed package r2 additional gates

- Benchmark36 must be centred around the canonical camera target; no corner tile or Peak silhouette may touch the review frame.
- Coast family sheet must visibly include all three semantic shoreline morphologies (sandy / mixed / rocky).
- Four candidate variants of each land family must differ in macro composition, not merely by seed rotation or mirroring.
- Forest variants must not all use the same tree-cluster count/layout.
- Installer must refuse an incomplete rc2 base before replacing files.
