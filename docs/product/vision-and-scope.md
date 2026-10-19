# Product Vision and Scope

## One-sentence vision

Vaelora is a focused, turn-based fantasy strategy game where players grow productive cities, shape a connected territory, develop shared and civilization-specific knowledge, and compete for a clear victory condition on a readable hex map.

## Player promise

A match should make the player feel that each turn presents a small number of meaningful choices: what a city should produce, where territory should grow, what the civilization should research, which routes to build, and where units should explore or fight. The game should reward both expansion and peaceful development while keeping military conquest viable.

## Product pillars

1. **Simple to read, strategic to master.** Fixed-isometric hex maps, a sequential turn order, one military unit per tile, and one active production project per city keep the board legible.
2. **Cities are active engines.** Cities grow over time, claim useful territory, generate coins, and build one unit or building at a time.
3. **Infrastructure has strategic value.** Terrain improvements benefit their assigned city; roads connect any distance between friendly cities, improve movement, and support growth and income.
4. **Progress is civilization-wide.** One technology can be researched at a time; approximately 80% of the tree is shared and approximately 20% supports faction identity.
5. **Asymmetry without hard exclusion.** Civilizations have different strengths and options, but should not be barred from ordinary strategic functions solely by identity.
6. **Finished presentation from the first playable build.** The prototype uses final-quality art, a consistent 2D isometric camera, landscape layouts, and the intended bright fantasy direction.

## Platform and session model

| Decision | Scope |
|---|---|
| Engine and language | Godot and GDScript |
| Initial player mode | Local single-player against AI; exactly two participants |
| Target platforms | Android, Windows, macOS, Linux, and Web from the start |
| Camera and layout | 2D, fixed isometric perspective, mandatory landscape orientation |
| Map | Procedural hex map with a stored seed; asymmetric starts with minimum separation and broadly comparable opportunity |
| Save behavior | Manual save at any time; automatic save every five complete rounds |
| Multiplayer/networking | Not part of initial scope |

The target platform set is a design commitment. The supported browser matrix, Android minimum version, input-device priorities, memory budget, performance targets, and storefront requirements remain open technical decisions.

## Initial prototype scope

The prototype should implement the complete agreed initial ruleset with two playable civilizations: the human **Liga de Auren** and the orc **Clanes de Brasal**. It includes procedural seeded maps, all four match modes, city growth and territory, one-action city production, research, workers and improvements, roads, fog of war, land and naval transport play, combat, AI, score/victory rules, and save/resume. Exact content values must be approved before implementation, not improvised in code.

The other four planned civilization concepts—elves, dwarves, goblins, and skeletons—follow only after the initial prototype passes its final test battery. The expansion gate is intended to protect balance and regression quality, not to reduce the first prototype's game systems.

## Explicit non-goals for the first prototype

- Online or competitive multiplayer.
- Campaign, narrative missions, or metagame progression.
- Mid-match difficulty changes.
- Player-selected or editable city names.
- City destruction/razing.
- Temporary placeholder art or a temporary non-isometric view.
- Expanding the participant count beyond two before the initial game has been validated.

## Audience and market assumptions

**Assumption to validate:** the primary audience is players who enjoy turn-based empire building but prefer shorter, more readable matches than a full-scale 4X simulation. This is a positioning hypothesis, not a demographic claim. The product's onboarding, expected match length, accessibility requirements, and commercial model have not yet been specified.

## Success criteria for the first complete prototype

- A new player can complete the first match without needing undocumented rules.
- City production, growth, territory ownership, research, and turn progression remain predictable and inspectable.
- Both initial civilizations can pursue multiple victory approaches and each has a distinct strategic identity.
- Procedural maps are reproducible from saves and meet the agreed separation/fairness checks.
- Manual saves and five-complete-round autosaves resume the exact match state.
- All supported platform families pass the same core gameplay acceptance scenarios.
- The final test battery is green before work begins on the other four civilizations.

## Open product questions

Match length, onboarding/tutorial, commercial model, localization, accessibility targets, visual asset budget, sound direction, browser support matrix, and measurable performance budgets require separate decisions. See the [open design decisions register](../game-design/open-decisions.md) for gameplay-specific questions.
