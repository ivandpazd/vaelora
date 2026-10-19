# Vaelora AI contribution contract

Vaelora is a 2D, turn-based fantasy strategy game in preproduction. Treat the repository documentation as the product contract and do not invent rules, scope, assets, or platform guarantees.

## Read before acting

1. `README.md` for product scope and current status.
2. `docs/production/production-plan.md` for phases and gates.
3. `docs/game-design/game-design-document.md` and `docs/game-design/open-decisions.md` for gameplay authority.
4. `docs/technical/architecture-proposal.md` for proposed boundaries; it is not fully approved until marked so.
5. `docs/project/development-workflow.md` for issues, branches, PRs, commits, and promotion.

If sources conflict, stop and report the conflict. Never silently turn an open decision into an implementation rule.

## Product and architecture guardrails

- Preserve deterministic, seed-driven simulation and reproducible saves, combat, turns, and tests.
- Keep domain/simulation independent from scene-tree, rendering, input hardware, and platform APIs.
- Route human and AI actions through the same validation path; rejected commands leave state unchanged.
- Keep content data separate from formulas and rules. Use stable content IDs and assess save-schema impact before changing them.
- Support Android, Windows, macOS, Linux, and Web deliberately; an editor run or export alone does not prove platform support.
- Use final-quality visual assets in the prototype. Do not introduce placeholder art or undocumented gameplay rules.
- Keep unresolved design, balance, technical, and release decisions explicit in the canonical docs or an issue.

## Delivery workflow

- Search open and closed issues before creating work. Every change entering `dev` needs one concrete issue.
- Work from `feature/<issue>-<slug>` branched from `dev`; target feature PRs at `dev` and promote only `dev` to `main`.
- Use Conventional Commits. Never add `Co-Authored-By`, AI attribution, credentials, or private data.
- Keep code, tests, content, documentation, and platform evidence in the same coherent work unit.
- For behavior changes, prefer deterministic RED → GREEN → REFACTOR tests through the public interface. Include manual scenarios for UI, save, export, and visual work.
- Update relevant documentation when behavior, content, balance, architecture, or workflow changes.

## Role routing

Load the narrowest project skill that matches the work. Skills are runtime contracts, not substitutes for the canonical docs.

| Discipline | Skill |
|---|---|
| Product, scope, production | `skills/game-product-production/SKILL.md` |
| Game rules and systems | `skills/game-design/SKILL.md` |
| Narrative and world | `skills/narrative-worldbuilding/SKILL.md` |
| Economy and balance | `skills/game-balance/SKILL.md` |
| Godot architecture | `skills/godot-architecture/SKILL.md` |
| Gameplay and simulation | `skills/gameplay-programming/SKILL.md` |
| AI opponent | `skills/game-ai/SKILL.md` |
| UI, UX, accessibility | `skills/game-ui-ux/SKILL.md` |
| 2D art and visual direction | `skills/game-art-direction/SKILL.md` |
| Audio | `skills/game-audio/SKILL.md` |
| QA and playtesting | `skills/game-qa/SKILL.md` |
| Build, platform, release | `skills/game-release/SKILL.md` |

## Handoff contract

Every substantial change must state: objective, canonical sources, affected role(s), dependencies, changed files, checks run and their observed result, manual/platform evidence where applicable, open decisions, and risk. Do not claim completion when a required check is unavailable or skipped.
