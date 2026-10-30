# Production Plan

**Status:** working plan. It sequences design, implementation, and validation without cutting the complete agreed initial game scope.

## Delivery principles

- Resolve rules and data contracts before implementing behavior that depends on them.
- Track each unresolved product decision as an issue with acceptance criteria; accepted decisions update their canonical documentation.
- Deliver complete two-player gameplay systems for the first prototype rather than a reduced rules demo.
- Use final-quality art throughout the prototype; placeholder visuals are not acceptable.
- Keep Android, Windows, macOS, Linux, and Web exportable throughout development. Prioritize runtime checks for Web and Android during bootstrap; run Windows, macOS, and Linux launch checks when packaged builds are available. Deferred desktop runtime checks do not block the engine/renderer decision in issue #19; they remain part of the vertical-slice platform gate.
- Add the remaining four planned civilizations only after the prototype passes the final test battery.

## Phases and gates

### 0. Repository and documentation foundation

Establish the branch model, issue/PR templates, README, documentation index, and current design baseline. Apply GitHub branch rules and publish the initial docs only after review. **Exit:** docs and GitHub workflow available on the default branch; `dev` exists; unresolved design decisions have issues or a named owner.

### 1. Design lock for the initial game

Resolve implementation-blocking choices in the [open decisions register](../game-design/open-decisions.md): map constraints, exact terrain and city rules, initial content, economy/research/production formulas, combat/naval behavior, AI, scoring, saves, interaction requirements, accessibility/localization, tutorial/onboarding/pacing, naming/text ownership, and the Trama landmark boundary. Issue #27 records the cosmetic-only landmark rule, and issue #28 records the naming/text policy. Representative visual/audio slices and measured audio budgets remain pending evidence gates for issues #17/#18; no unreviewed sample is accepted. Issues #22 and #23 define measurable adaptive interaction/display and save/migration contracts; runtime behavior remains later-stage implementation and validation work. Use playtest prototypes for uncertain balance rather than freezing guesses.

Balance evidence follows the [Balance Methodology and Scenario Catalog](../game-design/balance-methodology.md): fixed seeds, named metrics, initial tolerances, explicit tuning ownership, and rerun rules. A value is not considered locked merely because it appears in code or passes one unseeded match.

**Exit:** every initial rule has observable acceptance criteria, all starting units/buildings/technologies have data, procedural fairness has measurable tests, and the named accessibility/localization checks are ready to execute. The issue #22 viewport, safe-area, and rejected-action checks and issue #23 migration, corruption-recovery, and slot-preservation checks are specified before dependent systems are implemented.

### 2. Godot foundation and vertical slice

Create the Godot project and content/simulation boundaries. Implement deterministic hex state, one complete turn, seeded map loading, city selection/production, and cross-platform input/presentation flow. Assets used in this slice must be final-quality even if not all gameplay systems are present yet. Accept representative visual and audio slices and measure asset/audio budgets on representative target devices before integration.

#### Stage 2 vertical-slice scenario (`VS-01`)

Use the established `BAL-07-AUREN-BRASAL-IDENTITY` fixture as the reproducible end-to-end scenario: seed `1407`, Continents, Medium, Auren League versus Brasal clans, Intermediate difficulty, and Combined victory. Run both player orders with the same seed and setup; do not add a scenario-only game rule, unit, resource, or advantage. Combined matches end only through the GDD's existing conquest or knowledge conditions.

The scenario exercises match setup, exploration, city founding and growth, territory improvement, city production, research, land combat, save/load, and a complete valid match outcome. Across the two player orders, both civilizations must complete at least one shared and one unique technology through the same content, research, save/load, and validated-command paths used by the human and AI. The full initial content inventory and explicit modifier/prerequisite validation remain required as specified in [GDD §17](../game-design/game-design-document.md#17-prototype-content-contract). Save/load checkpoints use the accepted [GDD §13](../game-design/game-design-document.md#13-saving-and-accessibility-constraints) contract. The scenario proves a vertical slice, not the complete prototype or every balance scenario.

| Evidence | Stage 2 acceptance |
|---|---|
| Reproducibility | Repeating each player order with seed `1407` and the same build/configuration produces the same authoritative initial map and the same outcomes for the same confirmed action sequence. A save/load checkpoint preserves the full authoritative state and deterministic continuation. |
| Functional path | Both runs complete the actions above and end through a valid Combined-mode victory. Human and AI actions use the same authoritative validation path; rejected actions preserve state. |
| Presentation and content | Every asset used is final-quality and rights-cleared. Required prototype content is present; no placeholder assets, scenario-only mechanics, or unapproved audio are used. |
| Automated evidence | Headless tests exercise the seed/configuration, public simulation and command interfaces, rejected-action state preservation, research/content paths, and save/load continuation. Record exact commands, build, seed, configuration, and results. |
| Platform smoke matrix | Record launch and the scenario's start-to-save/load checkpoint on Windows, macOS, and Linux desktop builds; one representative Android device at the selected floor; and each supported Web browser family in issue #24's current matrix. Record OS/device or browser/runtime versions, build, steps, result, and limitations separately; an export or editor run alone is not runtime evidence. |
| Gate ownership and failure | The issue owner/maintainer records the evidence; the integration reviewer checks it against this table. Any failed criterion, nondeterministic result, rejected-action state change, save/load mismatch, missing final-quality asset, or required-target smoke failure leaves Stage 2 open. Record the failing evidence and reopen the affected implementation work before reconsidering the gate. |

If seed `1407` cannot satisfy the required legal scenario without changing accepted rules, do not weaken this contract or tune the game around the fixture. Mark the run blocked, preserve its evidence, and propose a versioned replacement seed/setup with the prior result retained under the scenario-catalog rules.

**Exit:** one short end-to-end scenario is playable on target families and can be reproduced from a seed. The `ACC-*` and `LOC-*` checks in GDD §13 are run and their results or platform limitations recorded for Android, Windows, macOS, Linux, and supported Web browsers. Representative minimum-floor devices/browser combinations are used to measure startup/load, largest-map generation, turn and AI response, frame time, peak memory, and save size; numerical budgets are approved and recorded before this gate closes. The initial Godot system requirements are not treated as proof of Vaelora performance. This remains a later vertical-slice gate; issue #19 does not wait for deferred native desktop launch checks.

### 3. Complete two-civilization prototype

Implement all agreed match modes and initial systems for the human Auren League and orc Brasal clans: procedural maps; exploration/fog; settlement/cities/territory; city production/buildings; workers/improvements/roads; growth/economy; research; land movement/combat; transport/naval rules; AI; score and victory; manual and five-complete-round autosaves.

**Exit:** full matches can be completed on every target platform with final-quality visuals and no temporary gameplay rules.

### 4. Final prototype test battery

Test both player civilizations and AI selections/difficulties, every match type, multiple map seeds/types, fair starts, city capture/elimination, all victory routes, terrain/combat interactions, roads and worker exhaustion, interrupted and completed production/research, saves/resume/autosave, complete platform flows, and the GDD §13 accessibility/localization checks. Include regression coverage for failures discovered during the battery.

**Gate:** the test battery passes, blocking defects are resolved, game balance has been reviewed, and the two civilizations remain viable before expansion work begins.

### 5. Civilization expansion

Add Raíces de Nymara, Círculos de Durn, Compañías de la Chispa, and Vigilia de los Nombres after the prototype gate. Each needs a documented strategic identity, city names, content data, final assets, and regression/balance coverage against existing factions.

## Definition of ready for implementation

An issue is Ready when it has one clear player-facing outcome, links to accepted source documentation, lists acceptance criteria and dependencies, identifies data/visual effects, and names required automated/manual checks. If it changes an open design decision, acceptance is blocked until that decision is explicitly resolved.

## Definition of done

- Acceptance criteria pass and required automated checks are green.
- Relevant docs, balance data, and issue links are updated.
- Platform and manual scenarios are recorded where the behavior crosses UI, save, or export boundaries.
- No placeholder art or undocumented rules are introduced.
- Pull request is reviewed and merged through the agreed target branch.
