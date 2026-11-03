# Visual reconciliation v0.3.2-r1

**Historical record:** this r1 shoreline count and terrain assessment describe that earlier revision. The current terrain appearance baseline is [Terrain Visual Language v1](../game-design/TERRAIN_VISUAL_LANGUAGE_V1.md); its production coastline inventory is documented in the current [asset catalog](../game-design/asset-catalog.md).

**Purpose:** preserve the strongest work from v0.3/v0.3.1 while correcting regressions and contradictions introduced during rapid iteration toward v0.3.2.

## 1. What is deliberately preserved

The following decisions already produced convincing evidence and are **not reset** by this revision:

- Art style identity remains `vaelora-sculpted-diorama-v2`.
- Blender-as-source -> transparent 2D PNG runtime architecture.
- Fixed 45° yaw / 30° elevation orthographic camera.
- 4x working render -> premultiplied-alpha Lanczos -> 2x final.
- Terrain palette and luminous-fantasy direction.
- Exact hex perimeter and sculpted geological side layers.
- Authored forest negative space and current forest composition grammar.
- Directional mountain/peak language.
- Auren and Brasal Stage-2 city compositions already judged positively.
- Unit canvas `256x128`, orthographic framing `4.35`, and measured unit frame Z offset `+0.08`.
- Auren civic/order and Brasal work/repair narrative languages.
- Human-only asset acceptance lifecycle.

## 2. Regressions/problems found in the previous v0.3.2 update

### Partial-package regression

The earlier v0.3.2 was distributed as a small update and did not include the full canonical visual documentation created in v0.3. This made good prior work appear lost and allowed code to move ahead of its specification.

**Resolution:** v0.3.2-r1 is a full, self-contained reconciliation package containing the canonical documents, tools and asset contracts together.

### Coast specification drift

Canonical documents still described six corner-resolver sprites while code had moved to Coast System v3 without visible corner patches.

**Resolution:** the canonical runtime contract is now three shoreline morphology variants x six directions = **18 edge overlays**, with analytical shared endpoints and no visible corner-resolver sprites.

### Benchmark/runtime mismatch

The source-context benchmark could derive unique procedural seeds per tile, while Godot would import a finite sprite library. A visually excellent benchmark could therefore approve detail unavailable at runtime.

**Resolution:** terrain, coast, city and unit review scenes use the same finite seed namespace as exportable sprites. The final quality gate also requires an actual Godot board screenshot.

### Axial-spacing defect

The earlier benchmark helper effectively halved the pointy-top axial Y step, causing tile overlap and contributing to false land/water intersections.

**Resolution:** the immutable contract uses `x = sqrt(3) * R` and `y = 1.5 * R`; host-side invariants lock both values.

### Fixed-Z decoration

Terrain decoration could be placed at a constant Z while the underlying surface was sculpted, allowing subtle float/sink defects.

**Resolution:** terrain decoration and relief formations sample their local sculpted surface. Coast-base sculpt amplitude is restrained for reusable shoreline compatibility.

### QA blind spots

The previous QA could:

- accept stale source manifests;
- omit assets from a gameplay-scale sheet when a row exceeded 1920 px;
- reject an asset with exactly the documented 5 px margin;
- miss cross-facing unit scale/anchor drift;
- create a premium scorecard without validating it.

**Resolution:** v0.3.2-r1 validates current source hashes/version/style/Blender pin, wraps all review-sheet assets, uses correct exclusive bbox semantics, checks six-facing groups, and validates human scorecards.

## 3. Improvements retained from v0.3.2

The reconciliation does not revert useful premium work. It retains:

- denser sculpted terrain topology with exact perimeter;
- richer tree material families and grounding/root treatment;
- richer mountain hierarchy;
- Stage-1/2/3 city progression work while preserving Stage-2 baseline composition;
- Character Body v3 and accepted unit framing;
- Coast System v3 continuous edge concept;
- premium >=9 per-area / >=9.3 mean review target;
- quality-suite and fixed-seed A/B philosophy.

## 4. What is still intentionally unproven

This source audit cannot claim visual scores. The following require Blender/Godot evidence on the user's Mac:

- final Coast System v3 morphology after corrected axial spacing;
- all nine terrain families at gameplay scale;
- all three city stages in color and grayscale;
- Character Body v3 six-facing visual quality;
- actual 2D Godot layering/anchors/import behavior;
- mipmap ON/OFF comparison;
- representative platform memory/overdraw/frame cost;
- human >=9/9.3 scorecard.

Do not expand the production catalog merely because v0.3.2-r1 passes source/QA checks.
