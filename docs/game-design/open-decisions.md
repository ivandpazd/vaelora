# Open Design Decisions

This register prevents missing detail from being mistaken for approval. A question may be resolved through a design issue, playtest, or technical proof; when accepted, move the decision into its canonical specification and retain only the rationale needed to understand it.

## Priority legend

- **Blocking:** must be decided before the affected system is implemented or acceptance tests are written.
- **High:** needed before content/balance lock, but safe to explore in a sandbox.
- **Later:** explicitly outside the initial prototype or dependent on playtest evidence.

## Blocking before gameplay implementation

| Area | Decision still needed | Why it blocks | Priority |
|---|---|---|---|
| Match setup | Map types, dimensions, exact turn-limit rules, start resources, seed visibility | Defines generation inputs, UI, and fair-start tests | Blocking |
| Starts/fairness | Minimum distance and measurable comparability rules for player/AI starts | Necessary to validate procedural generation | Blocking |
| Terrain | Complete terrain set, yields, movement costs, vision, defense, and legal improvement matrix | Core rules depend on terrain | Blocking |
| City territory | Tile-claim selection, overlap resolution, growth thresholds, level rewards, level-6 behavior | Defines city growth and ownership invariants | Blocking |
| City production | Complete initial unit/building roster, prerequisites, build durations, interruption/queue rules | City action is a central turn choice | Blocking |
| Worker roster | Whether workers are part of initial city production alongside settlers, explorers, and basic soldiers | Affects city content and the worker economy | Blocking |
| Improvements | Initial improvement list, yields, stacking/upgrade rules, port placement and maintenance | Required for city growth/income and worker tests | Blocking |
| Roads | Legal tiles/ownership for construction, pathfinding/routing rules, route completion, bonus stacking | Roads affect movement and economy | Blocking |
| Research | Initial full shared and faction-specific technology trees, prerequisites, duration formula, acceleration payment and cancellation behavior | Required for research UI, victory, and balance | Blocking |
| Economy | Starting coins, city income by level, structure/improvement yields, exact road bonus | Necessary to tune production and acceleration | Blocking |
| Combat | Health/attack/defense formulas, movement/attack reach, ranged rules, retaliation, simultaneous actions, unit death and capture transition | Must be testable and deterministic | Blocking |
| Naval | Embark/disembark eligibility, transport stats and sea survival, coastal city/port rules, naval combat details | Required to complete sea maps and combat cases | Blocking |
| Victory/scoring | Exact score weights, tie resolution, turn-limit schedule, elimination and combined-mode priority | Determines match completion and standings | Blocking |
| AI/difficulty | AI decision policy and exact initial-resource bonuses for easy/intermediate/hard | Required for a complete local-versus-AI prototype | Blocking |
| Save/load | Save slots, auto-save replacement policy, serialization/versioning, platform persistence behavior | Manual saves and exact five-round autosaves are confirmed requirements | Blocking |
| Interaction | Touch/mouse/keyboard/controller priorities, selected unit/city flows, confirm/undo rules | Affects all five target families | Blocking |

## High priority before content lock

| Area | Question | Priority |
|---|---|---|
| Vision | City/unit vision radii and whether structures alter visibility | High |
| Civilizations | Exact human/orc identities, bonuses, buildings, unit stat variations, city-name pools | High |
| Cities | Whether city garrisons are allowed and how they interact with one-unit-per-hex | High |
| Improvements | Worker movement/action timing, whether an improvement can be cancelled or captured | High |
| Balance | Values should begin as tuning data and be iterated through seeded scenarios | High |
| UI/accessibility | Font scaling, color contrast, colorblind support, screen-reader scope, localization plan | High |
| Art/audio | Asset dimensions, silhouette standards, palette, animation scope, audio direction and budget | High |

## Later / future scope

- Expanding beyond two participants according to map size.
- Adding elves, dwarves, goblins, and skeletons after the complete prototype test battery passes.
- Darker map themes or different visual settings.
- Campaign, multiplayer, progression/meta systems, and player city renaming.
- Mechanical use of old Trama beacons or ruins; lore alone does not imply gameplay effects.

## Decision record format

When resolving an item, capture: question, evidence or playtest context, selected rule, rejected alternatives and trade-offs, acceptance checks, and affected document sections. Then update this table and the canonical GDD in the same change. Do not duplicate a long design debate here after it has been recorded in the relevant issue or accepted decision document.
