---
name: game-product-production
description: "Trigger: game scope, milestone, roadmap, production plan, feature brief, issue, definition of done. Govern product decisions and studio delivery from preproduction to release."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load for product scope, milestones, production sequencing, feature intake, issue readiness, or release planning.

## Stage Scope
Primary: stages 0–5. Own the transition between stages and never mark a gate complete without its evidence.

## Hard Rules
- Treat the README, production plan, GDD, and open-decisions register as authoritative in their domains.
- Do not approve an unresolved design decision by implication.
- Keep the first prototype boundary intact: two civilizations, final-quality assets, and all listed baseline systems.
- Make dependencies, acceptance criteria, ownership, and evidence explicit.

## Decision Gates
| State | Action |
|---|---|
| Rule unresolved | Record an issue and block dependent implementation. |
| Ready | Link canonical docs, outcome, criteria, dependencies, and checks. |
| Prototype gate | Require the production-plan test battery before expansion. |

## Execution Steps
1. Identify the player outcome and phase.
2. Check canonical scope and open decisions.
3. Define acceptance, dependencies, risks, and evidence.
4. Update the relevant project document with the accepted decision.

## Output Contract
Return outcome, phase, linked sources, acceptance criteria, dependencies, owner, risks, and next gate.

## References
- `README.md`
- `docs/production/production-plan.md`
- `docs/game-design/open-decisions.md`
- `docs/project/development-workflow.md`
