---
name: game-qa
description: "Trigger: QA, playtest, test plan, regression, bug reproduction, test battery, acceptance, deterministic test. Verify gameplay, content, saves, UI, and platforms with evidence."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load for test strategy, bug reproduction, playtests, regression, acceptance, balance evidence, or release gates.

## Hard Rules
- Reproduce reported failures before deciding they already work.
- Prefer fixed seeds and named scenarios; record exact inputs, build, platform, and outcome.
- Assert observable output, errors, persisted state, and unchanged state after rejection.
- Do not call an editor run, export, or one successful match complete platform coverage.

## Decision Gates
- Deterministic rule: automate through the public interface.
- UI/save/export boundary: add a documented manual scenario.
- Platform claim: test the packaged build on the target family.

## Execution Steps
1. Translate criteria into cases and evidence fields.
2. Run focused checks, then the applicable battery.
3. Triage failures by reproduction, severity, and ownership.
4. Add regression coverage before closing a fix.

## Output Contract
Return case IDs, environment, commands/scenarios, observed results, failures, evidence paths, and verdict per criterion.

## References
- `docs/production/production-plan.md`
- `docs/technical/architecture-proposal.md`
- `docs/project/development-workflow.md`
