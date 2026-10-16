# Vaelora — Preproduction and Delivery Plan

**Status:** Working plan. It sequences documentation and validation; it does not reduce the agreed game scope.

## Delivery principles

- Resolve the game rules before building systems that depend on them; mark unbalanced values as provisional rather than pretending they are final.
- Build the full agreed rule set for the initial two-player game, not a cut-down rules prototype.
- The first playable build uses the Liga de Auren and Clanes de Brasal; other four civilizations follow only after the prototype passes its final test battery.
- Keep all project visuals at final quality from the prototype onward. No placeholder assets.
- Support Android, Windows, macOS, Linux, and Web from the start; verify each export target as the project grows.

## Phases and exit criteria

### 0. Preproduction documentation

Deliver the GDD, technical architecture proposal, open-decision register, and repository entry point. Exit when confirmed rules and unresolved values are clearly distinguished and the initial scope is internally consistent.

### 1. Rule and content specification

Close the GDD's implementation-blocking questions: map constraints, exact turn/save semantics, city growth/territory, research and production formulas, unit/building/technology data for the two prototype civilizations, combat/naval rules, scoring, AI difficulty inputs, and interaction/accessibility requirements. Record balance values as tunable data and identify the tests that establish them.

### 2. Technical foundation and vertical slice

Create the Godot project, deterministic hex simulation, content data model, isometric board interaction, turn sequencing, save/load, and one complete match flow. Use only final-quality visual assets, even while the feature set is being assembled. Validate exports on all five target families.

### 3. Complete two-civilization prototype

Implement the complete agreed game rules and content for humans and orcs, procedural seeded maps, all match types, AI opponent, city development/production, research, roads/improvements, combat/naval play, scoring, manual saves, and five-round autosaves. No scope reduction or placeholder art. Exact content is governed by the approved specifications from Phase 1.

### 4. Final prototype test battery

Test full games across match modes, both player civilizations, AI civilizations/difficulties, map seeds and map types, capture/elimination, research and conquest victories, saves/resume, long turns, and every platform/export. Resolve blocking defects and balance issues before approving the prototype gate.

### 5. Civilization expansion

Only after the prototype passes the final test battery, add the remaining planned civilizations in a deliberate content sequence. Each needs distinct strategic identity, complete names/content/assets, and regression plus balance tests against the two prototype civilizations.

## Work not authorized by this document

This plan does not create online multiplayer, campaign progression, user-authored city names, mid-match difficulty changes, additional initial unit classes, or alternate dark-biome art direction. Those remain future decisions, not implied backlog commitments.

## Release-readiness checklist

- [ ] Every confirmed gameplay rule has an implementation acceptance test.
- [ ] All unresolved values that affect the initial game are decided and recorded.
- [ ] The two prototype civilizations are asymmetric but complete and viable.
- [ ] All five target platforms pass the agreed acceptance scenarios.
- [ ] Save/load and complete-round autosave behavior are verified.
- [ ] Final-quality art and landscape UI are consistent across devices.
- [ ] The full prototype test battery is green before civilization expansion begins.
