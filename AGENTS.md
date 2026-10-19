# Vaelora AI contribution contract

Vaelora is a 2D, turn-based fantasy strategy game in preproduction. Treat the repository documentation as the product contract and do not invent rules, scope, assets, or platform guarantees.

## Read before acting

1. `README.md` for product scope and current status.
2. `docs/production/production-plan.md` for phases and gates.
3. `docs/game-design/game-design-document.md` and `docs/game-design/open-decisions.md` for gameplay authority.
4. `docs/technical/architecture-proposal.md` for proposed boundaries; it is not fully approved until marked so.
5. `docs/project/development-workflow.md` for issues, branches, PRs, commits, and promotion.

If sources conflict, stop and report the conflict. Never silently turn an open decision into an implementation rule.

## Production stages

ODD may organize the work underneath this lifecycle, but it must not replace it. Every task, issue, PR, and skill invocation declares one primary stage and its gate:

| Stage | Purpose | Exit gate |
|---|---|---|
| 0. Foundation | Repository, documentation, workflow, and ownership | Canonical docs and delivery workflow are usable. |
| 1. Design lock | Rules, content contracts, balance scenarios, UX, and technical decisions | Blocking decisions have acceptance criteria and owners. |
| 2. Vertical slice | Godot foundation and one reproducible end-to-end scenario | Seeded scenario is playable on the intended target families. |
| 3. Complete prototype | Both initial civilizations and all agreed baseline systems | Full agreed match is playable with final-quality assets. |
| 4. Test battery | Regression, fairness, saves, AI, UX, visual, and platform validation | Blocking defects are resolved and evidence is recorded. |
| 5. Expansion and release | New civilizations, optimization, packaging, store/release preparation | Release evidence and promotion gate are complete. |

Do not skip a stage gate because an artifact exists. A later-stage request must identify which earlier-stage assumptions it depends on and whether they are locked.

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

## Efficient skill selection

- Select the smallest skill set that can safely decide or execute the request. One primary skill is the default.
- Add a supporting skill only when the change crosses a real discipline boundary, such as gameplay plus UI, or content plus balance.
- Do not activate every skill listed for a stage, repeat a check already covered by the responsible discipline, or create a second document for the same decision.
- Keep stage and gate reporting lightweight for small work; use the full production gate only when the requested outcome actually advances that gate.
- Prefer the existing project workflow, helpers, tests, and evidence formats before introducing new process or tooling.

## Handoff contract

Every substantial change must state: objective, canonical sources, affected role(s), dependencies, changed files, checks run and their observed result, manual/platform evidence where applicable, open decisions, and risk. Do not claim completion when a required check is unavailable or skipped.

It must also state: `Stage`, `Gate`, `Primary skill`, `Supporting skills`, and whether the work advances or merely prepares that gate.
