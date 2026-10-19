---
name: game-art-direction
description: "Trigger: 2D art, visual direction, concept, environment, icon, asset, sprite, animation, art review, final-quality. Create coherent readable assets without placeholder shortcuts."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load for visual identity, concepts, sprites, environments, UI assets, animation, import settings, or art acceptance.

## Hard Rules
- Use the supplied key art and documented visual direction as references, not as implemented UI.
- Prototype assets must be final-quality; label drafts as drafts and never present placeholders as complete.
- Prioritize readability at landscape gameplay scale, faction distinction, and gameplay affordance.
- Track source rights, licenses, provenance, and import requirements.

## Decision Gates
- New asset: define gameplay role, scale, state variants, source, and acceptance.
- Visual change affecting rules: route it through game design.
- Imported asset: validate dimensions, color, compression, animation, and target platforms.

## Execution Steps
1. Read visual and world references.
2. Define style, silhouette, palette, usage, and constraints.
3. Produce or integrate the smallest complete asset set.
4. Review in gameplay context on target aspect ratios.

## Output Contract
Return asset list, visual intent, source/licensing, import settings, review evidence, and gaps.

## References
- `README.md`
- `docs/game-design/world-and-civilizations.md`
- `docs/production/production-plan.md`
