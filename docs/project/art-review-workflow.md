# Vaelora — Art Review Workflow v0.3

## 1. Purpose

Keep AI-assisted production fast without allowing unreviewed generated art to become canon or production debt.

## 2. Work unit

One art work unit should normally contain one of:

- a terrain family;
- coast connection system;
- one faction city stage family;
- one unit role across both prototype factions;
- one improvement family;
- one overlay family;
- one UI/iconography family.

Do not mix unrelated families merely because one Blender script can generate them.

## 3. Required evidence

Each review PR/work unit contains:

- source scripts and editable `.blend` where retained;
- manifests;
- final 2× PNGs;
- automated QA JSON;
- isolated contact sheet;
- grayscale sheet;
- 7-tile repetition stress where relevant;
- 19-hex contextual screenshot where relevant;
- 75/100/125% crops;
- Steam 320 px proxy;
- known defects and lifecycle state.

## 4. Review order

Reviewers should inspect in this order:

1. gameplay read at 75%;
2. silhouette/grayscale;
3. board composition;
4. faction/world identity;
5. materials/lighting;
6. microdetail at 125%;
7. technical QA/provenance.

Starting from zoomed-in beauty creates the wrong incentives.

## 5. Defect severity

### Blocker

Cannot be accepted: wrong registration, unreadable terrain/role, false gameplay affordance, clipping, broken provenance, clear derivative copying, incompatible camera.

### Major

Requires revision before acceptance: generic silhouette, faction distinction depends on hue, obvious repetition, poor coast seam, weak material hierarchy, noisy thumbnail.

### Minor

Can be accepted with tracked follow-up only if it does not affect readability: tiny tangent, low-value decorative imbalance, subtle material tuning.

## 6. AI role

AI may:

- generate controlled variants;
- refactor generator code;
- produce QA sheets;
- propose critique;
- compare metrics;
- repair Blocker/Major issues.

AI may not:

- promote lifecycle state to accepted;
- invent gameplay content to improve visuals;
- use unlicensed external meshes/textures;
- silently change camera/palette/scale contracts.

## 7. A/B review

When revising a generator, reproduce the same review seed and show old vs new at the same camera/canvas. Do not compare unrelated random variants and call the result an improvement.
