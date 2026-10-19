# Feature: Game studio agent foundation
Branch: feature/14-seeded-balance-methodology
Delivery: one reviewable documentation/configuration work unit
Test runner: structural shell checks and skill-registry refresh

## Specs

### S1 — Agent operating contract
Create a root `AGENTS.md` that makes the existing Vaelora documentation, architecture boundaries, branch workflow, production stages, quality gates, and final-quality-art constraint executable for AI contributors.

Acceptance: contributors can identify canonical sources, required checks, prohibited shortcuts, and the expected handoff for design, code, content, art, QA, and release work.

### S2 — Professional game-development skills
Create project skills covering the professional disciplines needed from preproduction through final delivery, with concise LLM-first activation, explicit stage applicability, rules, decision gates, execution, output, and local references.

Acceptance: every skill has valid frontmatter, the required sections, and points to current local project documentation.

### S3 — Skill discovery configuration
Register the project skills in `.atl/skill-registry.md` using the repository skill-registry workflow.

Acceptance: the registry is generated successfully and contains the project skills without duplicate or stale project entries.

## Tasks

- T1 (S1): Create root agent contract — inline — complete — working tree.
- T2 (S2): Create professional discipline skills — inline — complete — working tree.
- T3 (S3): Refresh registry and validate configuration — inline — complete — working tree.

## Log

### L1
User request: "Revisa si existe un AGENTS.md en el proyecto y si se han creado skills especificas para el desarrollo del videojuego, desde las etapas previas hasta el final. En caso de no tener nada, me gustaría que crearas y configuraras el AGENTS.md y las distintas skills según los distintos perfiles profesionales que habría en un estudio de desarrollo y diseño de videojuegos profesional"

### L2
Initial inspection found no project `AGENTS.md`, no project `SKILL.md`, and no repository skill-style guide. Existing canonical sources are the README, production plan, development workflow, technical architecture proposal, game design documentation, and open decisions register. Global skill style guide will be used for project skills.

### L3
Created `AGENTS.md` plus 12 role skills. Refreshed `.atl/skill-registry.md` successfully; structural validation passed for all project skills. The registry remains local runtime metadata because `.atl/` is ignored by the repository.

### L4
Review found that role routing was clear but lifecycle-stage routing was implicit. The accepted correction is to add an explicit six-stage production model to `AGENTS.md` and a stage scope/gate to every skill, while retaining ODD only as the execution workflow underneath those product stages.
