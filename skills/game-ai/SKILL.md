---
name: game-ai
description: "Trigger: AI opponent, difficulty, planning, heuristic, bot turn, decision making, visible information. Build fair AI through the same legal command contract as the player."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load for opponent planning, difficulty, AI behavior, evaluation heuristics, or AI performance work.

## Hard Rules
- Give AI only the information and legal actions available to the human.
- Route AI actions through the same validation and transition path.
- Keep difficulty differences explicit: documented planning horizon and starting economy only unless design changes.
- Preserve deterministic behavior under a fixed seed and state.

## Decision Gates
- Legal action set: derive it from authoritative validation.
- Difficulty change: document player-visible effect and balance evidence.
- Timeout risk: use a bounded deterministic fallback, never an illegal action.

## Execution Steps
1. Define the decision point, information set, and objective.
2. Measure baseline quality and turn cost on fixed scenarios.
3. Implement and test legal, deterministic decisions.
4. Compare AI and human-visible outcomes without hidden advantages.

## Output Contract
Return information set, strategy, difficulty effect, determinism evidence, performance, and scenarios.

## References
- `docs/technical/architecture-proposal.md`
- `docs/game-design/game-design-document.md`
- `docs/game-design/balance-methodology.md`
