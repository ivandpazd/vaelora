# Vaelora preproduction documentation
Objective: produce the source-of-truth preproduction documents for the Godot game, separating confirmed decisions from unresolved balance and implementation questions.
Branch: `docs/vaelora-preproduction` | Delivery: `ask-on-risk` | Test runner: structural Markdown readback (passive documentation; no runnable behavioral tests).

## Specs

### S1 — Complete game design document
- Authorized scope: document the agreed concept, core loop, setup, turns, map generation, exploration, cities, production, improvements, roads, research, economy, units, combat, victory, saves, prototype civilizations, narrative, and visual direction. Do not implement game code or invent exact values where the design leaves them open.
- User request (verbatim): “Me gustaría que empezáramos a preparar la documentación completa del proyecto como análisis previo antes de empezar a crear absolutamente nada.”
- Acceptance: a reader can understand the intended game and distinguish confirmed rules from open balance/design questions; approved decisions are not contradicted or silently expanded.
- Checks: inspect the rendered Markdown structure and verify every documented rule against the persisted design decisions.

### S2 — Technical direction and production plan
- Authorized scope: document Godot/GDScript targets, cross-platform constraints, proposed architecture boundaries and validation phases, clearly labeling recommendations/assumptions separately from user-approved decisions. Record that prototype starts with humans and orcs and only expands after the agreed test gate.
- User request (verbatim): “Si, tienes plenos poderes. La idea es que trabajemos en el repositorio de forma profesional para nuestro proyecto en Godot”
- Acceptance: technical recommendations do not masquerade as approved mechanics; scope reflects Android, Windows, macOS, Linux, and Web from the start and the stated 2D fixed-isometric landscape presentation.
- Checks: structural readback and cross-check platform/prototype constraints against the approved decisions.

### S3 — Repository entry point
- Authorized scope: replace the placeholder README with a concise project overview and links to the preproduction documents; add no implementation or asset files.
- Acceptance: README makes the project's status and documentation entry points clear.
- Checks: read back README links and verify their targets exist.

## Tasks
- [x] T1 — S1: Write the complete game design document — inline — complete — commit: `b20c211`.
- [x] T2 — S2: Write technical architecture proposal and production plan — inline — complete — commit: `b20c211`.
- [x] T3 — S3: Update README as documentation index — inline — complete — commit: `b20c211`.

## Log
- L1 (2026-10-16): “Me gustaría que empezáramos a preparar la documentación completa del proyecto como análisis previo antes de empezar a crear absolutamente nada.”
- L2 (2026-10-16): “Si, tienes plenos poderes. La idea es que trabajemos en el repositorio de forma profesional para nuestro proyecto en Godot”
- L3: Repository inspected: clean `main`, first commit `0e0564e`, remote `origin` already points to the user-provided Vaelora repository; only a placeholder `README.md` existed. Began work on branch `docs/vaelora-preproduction`.
- L4: Settled facts are taken from Engram observations 2137, 2138, and 2144. An older lore memory (2146) contains epic phrasing; follow the later preference 2144 for grounded, practical political/economic history. Exact gameplay numbers, full tech/building rosters, detailed AI, map sizing, and balance formulas remain open and must be labeled TBD rather than invented.
- L5: Completed the GDD, technical architecture proposal, production plan, and README index. Structural validation found all local Markdown links resolve. The worker is documented as a civilian utility role, but whether it belongs in the initial production roster remains explicitly open because the three named starting roles were separately constrained. No gameplay code or assets were created.
- L6: Work-unit commit `b20c211` (`docs: add Vaelora preproduction package`). Verification: Markdown heading/link/whitespace structural checks passed. Native assessment against `0e0564e` returned `risk: passive`, `review_due: false`, `review_due_reason: passive`; no review lifecycle was due.
- L7: The GitHub repository was read-only inspected after explicit user authorization. It has no `.github/ISSUE_TEMPLATE` directory and no open or closed issues. The issue-creation workflow requires a repository YAML Issue Form; therefore no issue was created. Publishing the docs or adding a form/pushing a PR was not attempted.
