---
name: game-balance
description: "Trigger: balance, economy, tuning, fairness, scenario, metrics, seed, difficulty, progression. Produce reproducible balance evidence without hiding rules."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load for economy formulas, map fairness, progression, difficulty, combat tuning, or balance investigations.

## Hard Rules
- Use fixed seeds, named scenarios, metrics, tolerances, and rerun rules.
- Keep tunable values in content data and formulas in testable simulation code.
- Never use hidden information, free units, or undocumented modifiers to make AI or factions appear fair.
- Assess save-schema impact before changing persisted content IDs or formulas.

## Decision Gates
| Evidence | Action |
|---|---|
| One unseeded match | Treat as a hypothesis, not a balance lock. |
| Scenario within tolerance | Record evidence and owner. |
| Outside tolerance | Identify cause, tune one variable family, rerun. |

## Execution Steps
1. Select a catalog scenario and baseline.
2. Record seed, configuration, metrics, result, and tolerance.
3. Change the smallest responsible data or formula surface.
4. Rerun baseline and regression scenarios; document the decision.

## Output Contract
Return scenario IDs, seeds, metrics, baseline, change, results, tolerance, and recommendation.

## References
- `docs/game-design/balance-methodology.md`
- `docs/technical/architecture-proposal.md`
- `docs/production/production-plan.md`
