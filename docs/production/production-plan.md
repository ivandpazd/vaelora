# Production Plan

**Status:** working plan. It sequences design, implementation, and validation without cutting the complete agreed initial game scope.

## Delivery principles

- Resolve rules and data contracts before implementing behavior that depends on them.
- Track each unresolved product decision as an issue with acceptance criteria; accepted decisions update their canonical documentation.
- Deliver complete two-player gameplay systems for the first prototype rather than a reduced rules demo.
- Use final-quality art throughout the prototype; placeholder visuals are not acceptable.
- Validate Android, Windows, macOS, Linux, and Web continuously instead of treating them as a later port.
- Add the remaining four planned civilizations only after the prototype passes the final test battery.

## Phases and gates

### 0. Repository and documentation foundation

Establish the branch model, issue/PR templates, README, documentation index, and current design baseline. Apply GitHub branch rules and publish the initial docs only after review. **Exit:** docs and GitHub workflow available on the default branch; `dev` exists; unresolved design decisions have issues or a named owner.

### 1. Design lock for the initial game

Resolve implementation-blocking choices in the [open decisions register](../game-design/open-decisions.md): map constraints, exact terrain and city rules, initial content, economy/research/production formulas, combat/naval behavior, AI, scoring, saves, and interaction requirements. Use playtest prototypes for uncertain balance rather than freezing guesses.

**Exit:** every initial rule has observable acceptance criteria, all starting units/buildings/technologies have data, and procedural fairness has measurable tests.

### 2. Godot foundation and vertical slice

Create the Godot project and content/simulation boundaries. Implement deterministic hex state, one complete turn, seeded map loading, city selection/production, and cross-platform input/presentation flow. Assets used in this slice must be final-quality even if not all gameplay systems are present yet.

**Exit:** one short end-to-end scenario is playable on target families and can be reproduced from a seed.

### 3. Complete two-civilization prototype

Implement all agreed match modes and initial systems for the human Liga de Auren and orc Clanes de Brasal: procedural maps; exploration/fog; settlement/cities/territory; city production/buildings; workers/improvements/roads; growth/economy; research; land movement/combat; transport/naval rules; AI; score and victory; manual and five-complete-round autosaves.

**Exit:** full matches can be completed on every target platform with final-quality visuals and no temporary gameplay rules.

### 4. Final prototype test battery

Test both player civilizations and AI selections/difficulties, every match type, multiple map seeds/types, fair starts, city capture/elimination, all victory routes, terrain/combat interactions, roads and worker exhaustion, interrupted and completed production/research, saves/resume/autosave, and complete platform flows. Include regression coverage for failures discovered during the battery.

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
