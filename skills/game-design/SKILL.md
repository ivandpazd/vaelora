---
name: game-design
description: "Trigger: game design, mechanic, rules, unit, city, technology, victory, turn, combat, map, feature specification. Define observable and testable strategy-game behavior."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load when defining or changing gameplay rules, systems, content contracts, or player-facing interaction outcomes.

## Stage Scope
Primary: stage 1; supports stages 2–4. Stage 1 locks observable rules before dependent implementation.

## Hard Rules
- Read the GDD and open decisions before proposing a rule.
- Specify timing, inputs, validation, state transition, output, persistence, and edge cases.
- Preserve deterministic turns, seeded maps, fair starts, and explicit victory conditions.
- Separate shared rules from civilization content and keep deferred scope deferred.

## Decision Gates
| Question | Result |
|---|---|
| Canonical rule exists | Implement and test it; do not restate it differently. |
| Rule is open | Propose acceptance criteria and wait for an explicit decision. |
| Rule changes saved state | Require schema and migration assessment. |

## Execution Steps
1. Map the mechanic to the core loop and design pillar.
2. Write examples and acceptance criteria before implementation.
3. Identify affected systems, content IDs, UI feedback, and saves.
4. Add regression cases for every named behavior.

## Output Contract
Return rule intent, state model, examples, acceptance criteria, dependencies, and unresolved decisions.

## References
- `docs/game-design/game-design-document.md`
- `docs/game-design/open-decisions.md`
- `docs/technical/architecture-proposal.md`
