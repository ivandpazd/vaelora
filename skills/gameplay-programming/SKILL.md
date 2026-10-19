---
name: gameplay-programming
description: "Trigger: gameplay code, simulation, hex grid, turn system, command, combat, city, save state, deterministic test. Implement rules through authoritative transitions."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load for simulation, commands, entities, map generation, turns, combat, cities, persistence models, or deterministic tests.

## Stage Scope
Primary: stages 2–3; supports stage 4. Implement only rules whose stage-1 contract and persistence impact are understood.

## Hard Rules
- Receive intent, validate against authoritative state, apply one deterministic transition, and emit a result.
- Rejected commands must leave state unchanged.
- Use the same command path for human and AI.
- Do not serialize scene nodes; version, checksum, validate, and migrate model-level saves.

## Decision Gates
- Rule unclear: stop at the open decision.
- Existing helper/seam: reuse it; do not create a parallel state path.
- Persisted change: add migration and corruption-preservation tests.

## Execution Steps
1. Write a public-interface failing test for the requested rule.
2. Implement the smallest deterministic transition.
3. Test output, exit/error behavior, state, and prior behavior.
4. Refactor only while the full focused set remains green.

## Output Contract
Return changed rule, invariant, tests, determinism evidence, save impact, and known limitations.

## References
- `docs/technical/architecture-proposal.md`
- `docs/game-design/game-design-document.md`
- `docs/production/production-plan.md`
