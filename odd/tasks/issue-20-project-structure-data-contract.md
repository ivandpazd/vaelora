# Issue #20 — project structure and data contract
Branch: `feature/20-project-structure-data-contract` from `dev`; delivery: single PR (user-selected); runner: Godot 4.7.2 headless script tests.
Objective: lock the in-repository Godot foundation and content/domain boundaries for the complete approved prototype, without implementing gameplay systems.

## Specs

1. **S1 — Project foundation.** User request: “Quiero que actues como un experto en desarrollo de videojuegos con Godot y debes crear una base ultra profesional para que todo funcione a la perfección y nos sirva para el juego completo”. Create the approved `game/` project root with clear app, simulation, content, presentation, platform, assets, and tests ownership. Preserve the existing Godot 4.7.2 Compatibility decision. Check: Godot headless editor import/parse and repository structure readback.
2. **S2 — Content contract.** Keep stable IDs, shared-vs-civilization content, and all content facts within GDD §17. Define typed authored Resource data and tested validation without encoding gameplay formulas in resources. Check: public catalog/resource tests; representative Auren, Brasal, and Meadow data load and validate.
3. **S3 — Domain boundary.** Document model ownership for board, entities, commands, events, results, tuning, and persistence. Simulation has no dependency on scenes, rendering, input, or platform APIs; use canonical axial hex coordinates and preserve deterministic, rejected-command-no-mutation invariants. Check: architecture readback and dependency scan.
4. **S4 — Canonical docs.** Update architecture proposal and project structure/data dictionary to reflect this issue's approved decisions, clearly preserving open/deferred decisions and later stage gates. Check: links, diff check, and source-of-truth consistency.

## Tasks
- T1 — Establish project/data contract, samples, tests, docs, and validation. Route: inline (one cohesive unit; no writer trigger). Status: complete; focused checks passed. Commit: `2545a22`.

## Log
- L1 — User request verbatim: “Me parece bien. Utiliza el AGENTS.md y todas las skills que hemos creado para este proyecto en concreto. Veo que quieres crear la estructura de carpetas. Quiero que actues como un experto en desarrollo de videojuegos con Godot y debes crear una base ultra profesional para que todo funcione a la perfección y nos sirva para el juego completo”
- L2 — User authorized the approved `game/` architecture proposal and asked for a professional foundation; project AGENTS.md, not breadth for its own sake, governs scope. The user selected same-repository development; exact directory decision is approved here for issue #20.
- L3 — RED observed 2026-10-20: Godot 4.7.2 headless test failed to parse because referenced content classes and sample resources do not yet exist. Continue with minimal typed contracts; do not claim system-level tests beyond issue #20.
- L4 — User selected one PR: “hazlo todo en una unica PR mejor”. The 410-line change is one cohesive issue #20 deliverable; preserve it intact and document the over-budget exception rationale in the PR rather than splitting behavior or removing content.
- L5 — GREEN observed 2026-10-20: `Godot --headless --editor --path game --quit` and `Godot --headless --path game --script res://tests/test_content_contract.gd` passed; `git diff --check` passed; content-layer dependency scan found no scene/render/input/platform API imports.
- L6 — Native review assessment for `2545a22` against `origin/dev`: risk `medium`; `review_due: false`; reason `under_budget`. No native review was started.
