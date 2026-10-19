# Open Design Decisions

This register prevents missing detail from being mistaken for approval. A question may be resolved through a design issue, playtest, or technical proof; when accepted, move the decision into its canonical specification and retain only the rationale needed to understand it.

## Priority legend

- **Blocking:** must be decided before the affected system is implemented or acceptance tests are written.
- **High:** needed before content/balance lock, but safe to explore in a sandbox.
- **Later:** explicitly outside the initial prototype or dependent on playtest evidence.

## Blocking before gameplay implementation

| Area | Decision still needed | Why it blocks | Priority |
|---|---|---|---|
| Match setup | Resolved in GDD §2: three map types, three sizes, size-based turn limits, equal starting resources, and post-generation seed visibility | Keep acceptance tests aligned with the canonical rules | Resolved |
| Starts/fairness | Resolved in GDD §2: 12-hex minimum separation, radius-four regions, 20 workable land tiles, and a maximum 15% opportunity-score difference | Keep generation and fairness tests aligned with the canonical rules | Resolved |
| Terrain | Resolved in GDD §4: nine terrain categories, base yields, movement, vision, defense, line of sight, and legal improvements | Keep terrain data and generator tests aligned with the canonical rules | Resolved |
| City territory | Resolved in GDD §5: claim tokens, radius-three contiguous claims, overlap ownership, growth thresholds, and level-6 cap | Keep city ownership and growth tests aligned with the canonical rules | Resolved |
| City production | Resolved in GDD §§6 and 9: initial roster, prerequisites, durations, single-slot behavior, cancellation, deployment blocking, and capture interruption | Keep production and turn-resolution tests aligned with the canonical rules | Resolved |
| Worker roster | Resolved in GDD §§6 and 9: workers are initial civilian production units with three lifetime uses | Keep worker production and improvement tests aligned with the canonical rules | Resolved |
| Improvements | Resolved in GDD §7: four initial improvements, effects, legal terrain, worker timing, replacement, port placement, and no maintenance | Keep improvement and worker tests aligned with the canonical rules | Resolved |
| Roads | Resolved in GDD §7: legal tiles, ownership, worker cost, movement, connected routes, and capped economic/growth bonus | Keep road graph and turn-resolution tests aligned with the canonical rules | Resolved |
| Research | Resolved in GDD §8: initial shared/faction trees, prerequisites, costs, generation formula, acceleration payment, and cancellation | Keep research, unlock, and victory tests aligned with the canonical rules | Resolved |
| Economy | Resolved in GDD §7: starting coins, city income, production/growth formulas, building effects, and route bonus application | Keep economy, production, growth, and research tests aligned with the canonical rules | Resolved |
| Combat | Resolved in GDD §9: land-unit stats, deterministic damage, movement/attack, retaliation, ranged contract, death, and city capture | Keep combat and turn-resolution tests aligned with the canonical rules | Resolved |
| Naval | Resolved in GDD §10: embark/disembark, transport state, sea movement, Patrol ship stats, naval combat, and port production | Keep naval and transport tests aligned with the canonical rules | Resolved |
| Victory/scoring | Resolved in GDD §11: mode end states, score formula, tie resolution, elimination behavior, and combined-mode priority | Keep victory and standings tests aligned with the canonical rules | Resolved |
| AI/difficulty | Resolved in GDD §12: shared command path, deterministic policy, visibility limits, planning horizons, and starting-coin bonuses | Keep AI decision and fairness tests aligned with the canonical rules | Resolved |
| Save/load | Resolved in GDD §13 and the architecture proposal: slots, atomic autosave/backup, versioned checksummed envelope, migration, corruption handling, and platform abstraction | Keep persistence and recovery tests aligned with the canonical rules | Resolved |
| Interaction | Resolved in GDD §13: input priorities, shared action vocabulary, selection/preview/confirmation flow, bindings, focus, and UI scale | Keep input-adapter and command-validation tests aligned with the canonical rules | Resolved |

## High priority before content lock

| Area | Question | Priority |
|---|---|---|
| Vision | Resolved in GDD §4: unit radius 2, city radius 3, terrain line-of-sight rules, and no improvement-based vision changes | Keep visibility tests aligned with the canonical rules | Resolved |
| Civilizations | Brasal clans identity, later balance refinements, and future civilization content; Auren League identity resolved in issue #11 | High |
| Cities | Resolved in GDD §9: no city garrison in the initial prototype; military units defend city tiles | Keep city-capture tests aligned with the canonical rules | Resolved |
| Improvements | Resolved in GDD §7: one worker action per turn, no cancellation after start, replacement semantics, and transfer on city capture | Keep worker-action and ownership tests aligned with the canonical rules | Resolved |
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

## Resolved decisions

### Auren League identity — initial prototype

- **Selected rule:** The Auren League is the approachable infrastructure-and-research baseline. It has no innate unit or building-stat modifier. **Civic Charter** requires Agriculture and Scholarship, costs 35 RP, and grants one additional claim token on each city level-up from level 1 through level 5. **Public Works** requires Engineering, costs 50 RP, and grants +1 production point per turn to each Auren city connected by an active own road network to at least one other own city. The initial city-name pool, heraldry, palette, silhouettes, and naming rules are defined in [World and Civilizations](world-and-civilizations.md#auren-league--humans). The first balance fixtures are `AUREN-01-TRAMA-RELAY` (seed 1101), `AUREN-02-CHARTER-EXPANSION` (seed 1102), and `AUREN-03-CROSSROADS` (seed 1103).
- **Trade-off:** Auren's advantage is visible and earned through roads, city development, and research, but it has a delayed payoff and no free military strength. Infrastructure can be disrupted and Civic Charter competes with other research priorities. This contrasts with the still-open Brasal clans identity without creating a separate rules system or preventing ordinary ports, lumber facilities, units, or buildings.
- **Rejected alternatives:** A pure research bonus was rejected because it would make the knowledge route strictly dominant and reduce the value of roads. A flat economic bonus was rejected because it would be invisible, always active, and difficult to contest. A free starting unit or unique military roster was rejected because it would distort the equal starting package and increase implementation scope. A defensive-only civic identity was rejected because it would not support the required expansion and conquest routes.
- **Balance risks:** Public Works may snowball after a safe two-city connection; Civic Charter may overvalue early expansion on high-opportunity maps; the fixed city-name pool may be exhausted in long matches; and the three scenario seeds may not expose enough map variance. Balance tests must track time to first connection, production gained from Public Works, claim-token value, city count, research completion, and conquest outcomes without changing the identity contract silently.
- **Acceptance checks:** The three named scenario fixtures use the standard equal starting package and fairness constraints; Auren has viable research, infrastructure, and conquest routes without a faction-specific combat bonus; unique technology prerequisites, costs, and formulas match GDD §8; city names and visual rules match the world document; and rejected alternatives and balance risks remain recorded here.
- **Affected canonical sections:** [Game Design Document §8](game-design-document.md#8-knowledge-and-research), [Game Design Document §14](game-design-document.md#14-setting-and-civilization-identity), and [World and Civilizations — Auren League](world-and-civilizations.md#auren-league--humans).

### Match setup — initial prototype

- **Selected rule:** The initial prototype uses Continents, Inland Sea, and Archipelago maps; Small (48 × 32), Medium (64 × 40), and Large (80 × 50) generation bounds; 100/140/180 turn limits by size for Turn limit matches; an equal base start of one settler, one explorer, one worker, and 100 coins; and automatic seeds displayed after match creation and stored in saves. Difficulty-specific AI advantages remain a separate decision.
- **Trade-off:** Fixed initial choices make generation, setup UI, and fairness tests implementable without pretending to support a wider map catalog. The seed is reproducible without adding a technical setup field that would burden new players.
- **Acceptance checks:** Both civilizations receive the same base starting package; the selected map type, size, turn limit, seed, and base package survive save/load; the normal setup flow does not require manual seed entry.
- **Affected canonical section:** [Game Design Document §2](game-design-document.md#2-player-experience-and-match-setup).

### Starting regions and fairness — initial prototype

- **Selected rule:** Starting city sites must be at least 12 hexes apart. Each radius-four starting region must contain at least 20 workable land tiles, and its normalized opportunity score must be within 15% of the other region. The score uses the approved terrain/content weights for food, production, income, strategic terrain, and supported coastal access. Starts remain asymmetric; the generator must not create one by mirroring or rotating the other.
- **Trade-off:** A bounded score protects the first expansion choices without requiring identical starts or a fully symmetric map. The score is data-driven so terrain and balance values can evolve without rewriting the fairness rule.
- **Acceptance checks:** The generator rejects illegal or unfair candidates; rejection derives the next candidate seed deterministically; accepted maps pass the distance, workable-land, and score-difference checks; regression tests record the seed for every failed fairness case.
- **Affected canonical section:** [Game Design Document §2](game-design-document.md#2-player-experience-and-match-setup).

### Terrain and visibility — initial prototype

- **Selected rule:** The initial prototype uses Meadow, Plains, Forest, Hills, Mountain, Coast, Shallow sea, Open sea, and Peak. Their base yields, movement costs, defense modifiers, vision bonuses, line-of-sight behavior, and legal improvements are defined in GDD §4. Units have base vision 2 and cities base vision 3. Only land categories are workable city territory; sea categories cannot contain cities or land improvements.
- **Trade-off:** Nine categories provide meaningful movement and settlement choices while keeping the first ruleset readable. Terrain values are explicit data rather than hidden behavior, allowing balance changes without changing terrain identity.
- **Acceptance checks:** Terrain generation produces only the defined categories; movement, defense, visibility, line of sight, city assignment, and improvement legality follow the table; rejected placements leave state unchanged; fixed seeds reproduce the same terrain and visibility state.
- **Affected canonical section:** [Game Design Document §4](game-design-document.md#4-map-terrain-and-visibility).

### City territory and growth — initial prototype

- **Selected rule:** A founded city owns its city tile and receives three claim tokens. Each level-up grants two more base tokens, reaching a base maximum of fourteen assigned tiles at level 6; explicit civilization technologies may add documented tokens. Claims must be workable, unassigned, within three hexes, and contiguous with existing territory. Claims are player-selected or deterministically AI-selected; tokens persist when no legal tile exists. Growth uses `floor(total assigned food yield / 3)` per completed city turn with cumulative thresholds of 20/50/90/140/200 for levels 2–6. Captured cities transfer their assigned territory.
- **Trade-off:** Claim tokens preserve meaningful city choices while preventing disconnected territory and automatic overwrites. Retaining unused tokens avoids punishing cities surrounded by rivals or impassable terrain.
- **Acceptance checks:** A tile has one owner at most; invalid or conflicting claims are rejected without state changes; captures transfer the complete assigned territory; level progression and base token counts are deterministic; level 6 grants no further base growth or claim tokens, while explicit civilization technologies may add their documented modifiers.
- **Affected canonical section:** [Game Design Document §5](game-design-document.md#5-cities-and-territory).

### City production and worker roster — initial prototype

- **Selected rule:** Every city has one production slot and no queue. The initial roster is Worker (2), Explorer (3), Basic soldier (4), Settler (6), Patrol ship (5), Granary (5), Barracks (5), Walls (6), and Academy (8), with prerequisites and one-per-city limits defined in GDD §6. Workers are included from the initial prototype and retain three lifetime improvement uses. A project advances once at the end of its civilization's turn.
- **Trade-off:** A short shared roster keeps city decisions legible while covering settlement, exploration, infrastructure, combat, naval access, growth, defense, and research. Cancellation deliberately loses progress so the single-slot rule remains strategically meaningful.
- **Acceptance checks:** Invalid projects are rejected without changing state; no city can queue two projects; cancellation loses progress; captured cities lose active production progress; blocked unit deployment preserves completed production without duplication; base project costs, production-point progress, and prerequisites are deterministic.
- **Affected canonical sections:** [Game Design Document §6](game-design-document.md#6-city-production-and-buildings) and [§9](game-design-document.md#9-units-movement-and-combat).

### Improvements and worker actions — initial prototype

- **Selected rule:** The initial improvements are Farm (+2 food), Lumber facility (+1 production/+1 coin), Mine (+2 production), and Port (+1 coin and Patrol ship access). Farms use Meadow/Plains, lumber uses Forest, mines use Hills/Mountain, and ports use Coast. Workers take one action per turn, spend one of three lifetime uses per construction or replacement, cannot cancel an action after it starts, and may work outside current city vision on legally assigned tiles. Improvements do not stack, have no maintenance, and transfer with captured city territory.
- **Trade-off:** Four improvements cover food, production, income, and naval access without creating a dense optimization layer before the core loop is playable. Replacement preserves long-term adaptation while consuming scarce worker actions.
- **Acceptance checks:** Invalid terrain, ownership, technology, duplicate-port, and replacement commands are rejected without state changes; construction completes only after the worker's civilization turn; worker uses decrease exactly once; captured improvements transfer benefits; ports remain maintenance-free in the initial prototype.
- **Affected canonical section:** [Game Design Document §7](game-design-document.md#7-improvements-workers-and-roads).

### Roads and connected routes — initial prototype

- **Selected rule:** Roads are separate tile features built by workers on traversable land that is unassigned or controlled by the worker's civilization. Each segment consumes one worker use and one worker action; roads require no technology, cannot be removed or upgraded, and are usable by both sides. Road movement costs one point per road tile. A connected component of roads and city tiles links own cities; each city receives +10% coin income and growth points per other own city in that component, capped at +50%. Enemy-controlled segments deactivate the affected route bonus.
- **Trade-off:** Allowing roads on unassigned land supports strategic infrastructure while forbidding construction in enemy territory prevents free access to contested land. A component-based bonus rewards network investment without depending on route length or a fragile single path.
- **Acceptance checks:** Invalid road placements are rejected without state changes; roads consume exactly one worker use; road and city adjacency determines connectivity; enemy units can traverse roads; terrain movement is reduced to one point on roads; route bonuses update when cities or road tiles change ownership and never exceed +50%.
- **Affected canonical section:** [Game Design Document §7](game-design-document.md#7-improvements-workers-and-roads).

### Research and technology — initial prototype

- **Selected rule:** Civilization research has one active technology and no queue. The initial tree contains twelve shared technologies plus two unique technologies for each prototype civilization. Shared costs are 20/35/50 research points by tier; research generation is `4 + cities + floor(sum city levels / 2) + floor(improved assigned tiles / 4) + 2 per Academy`. A one-time acceleration payment costs two coins per research point and contributes half the technology cost immediately. Cancellation loses progress and payment.
- **Trade-off:** The tree keeps most capabilities shared while making faction identity meaningful without hard-locking ordinary play. Development-based research rewards peaceful investment; excluding military strength avoids snowballing combat into an automatic knowledge victory.
- **Acceptance checks:** Prerequisites and unlocks are enforced; only one technology can be active; progress advances once per completed civilization turn; acceleration is applied once and cannot be refunded; cancellation loses all progress; knowledge victory requires the complete shared and faction-specific tree.
- **Affected canonical section:** [Game Design Document §8](game-design-document.md#8-knowledge-and-research).

### Economy and production yields — initial prototype

- **Selected rule:** Both civilizations start with 100 coins. City base income is 4/5/6/7/8/10 coins at levels 1–6. Cities generate 3 base production points plus assigned production yields and explicit bonuses. Granary adds +1 growth point, Barracks adds +1 production while producing military units, Walls add +20% city defense, and Academy adds +2 research points. Active road networks add +10% coin income and growth per other connected own city, capped at +50%, after flat sources.
- **Trade-off:** The economy uses a small number of explicit additive sources before percentage bonuses, making it inspectable and deterministic. Coins remain a strategic acceleration resource rather than a universal payment that obscures production choices.
- **Acceptance checks:** Starting coins, city-level income, tile/improvement/building effects, production progress, growth progress, research generation, and road multipliers match the formulas; final fractional coin/growth values round down; no unapproved maintenance or hidden costs occur.
- **Affected canonical section:** [Game Design Document §7](game-design-document.md#7-improvements-workers-and-roads).

### Land combat and city capture — initial prototype

- **Selected rule:** Settlers, workers, explorers, and Basic soldiers use explicit health, attack, defense, and movement values in GDD §9. Combat is sequential and deterministic; damage is `max(1, floor(attack × 100 / (100 + effective defense)))`. Terrain, city tiles, and Walls add defense modifiers. Melee defenders retaliate once; ranged attacks require line of sight and do not trigger distant retaliation. Units die at zero health, civilians are destroyed, and cities have no garrison: an enemy military unit captures an empty city tile by entering it.
- **Trade-off:** A single initial military role keeps the prototype readable while preserving a complete combat contract for later ranged units. No city garrison avoids a hidden second unit system and makes city defense depend on positioning.
- **Acceptance checks:** Movement and attack legality, damage, terrain modifiers, retaliation, rest healing, unit removal, and city capture are deterministic; rejected commands leave state unchanged; no combat action is simultaneous; city capture transfers the documented state and cancels active production.
- **Affected canonical section:** [Game Design Document §9](game-design-document.md#9-units-movement-and-combat).

### Naval transport and combat — initial prototype

- **Selected rule:** Land units embark from a friendly coastal city with a Port and retain their identity in a vulnerable transport state. Embarked units have 2 movement points, cannot attack, and may end in Shallow or Open sea. They disembark onto an unoccupied, non-enemy Coast tile or friendly port city, spending the full action. Patrol ships have 100 health, 25 attack, 15 defense, and 4 movement; they attack ships or embarked units with the land combat formula. Embarked units cannot retaliate, and no naval ranged or maintenance system exists initially.
- **Trade-off:** Treating transport as a state avoids a second cargo-capacity system while preserving vulnerability and meaningful ports. Requiring a friendly port to embark makes coastal infrastructure strategically valuable without preventing beachhead landings.
- **Acceptance checks:** Illegal embark/disembark commands are rejected without state changes; sea movement respects terrain costs and unit movement; embarked units cannot attack or retaliate; Patrol ship damage and death are deterministic; port production and city capture follow the shared production rules.
- **Affected canonical section:** [Game Design Document §10](game-design-document.md#10-naval-transport).

### Victory and scoring — initial prototype

- **Selected rule:** Turn limit matches last 100/140/180 complete rounds by map size and use technology, city, and military score components. Total conquest ends when the opponent loses its last city; Knowledge ends at 100% technology completion; Combined checks conquest before knowledge at each completed civilization turn. Turn-limit elimination does not end the clock early, and ties resolve through research cost, city levels, surviving military units, then a declared draw.
- **Trade-off:** The score rewards development, territory, and military outcomes without awarding opaque points for partial damage or unclaimed land. Explicit draws are preferable to arbitrary coin or seed tie-breakers.
- **Acceptance checks:** Each score event is counted once; mode-specific endings occur at the documented resolution point; turn-limit scoring occurs after the final complete round; combined priority is deterministic; ties produce the documented result.
- **Affected canonical section:** [Game Design Document §11](game-design-document.md#11-match-types-and-victory).

### AI and difficulty — initial prototype

- **Selected rule:** The AI uses the same visible state, fog of war, legal commands, production, research, and turn rules as the human. It follows a fixed priority order for victory, defense, capture, production, research, territory, infrastructure, and movement. Easy starts with 100 coins and a one-turn horizon; Intermediate with 150 coins and two turns; Hard with 200 coins and three turns. No difficulty grants extra units or hidden information.
- **Trade-off:** Planning horizon creates recognizable difficulty without changing the rules or requiring scripted cheating. Deterministic tie-breaking makes seeded matches reproducible and testable.
- **Acceptance checks:** AI actions are rejected by the same validators as human actions; hidden tiles never influence choices; starting bonuses are exact; each horizon produces deterministic choices; difficulty remains fixed and no free units or mid-match modifiers appear.
- **Affected canonical section:** [Game Design Document §12](game-design-document.md#12-ai-and-difficulty).

### Save/load and persistence — initial prototype

- **Selected rule:** Each profile has three manual slots, one autosave, and one previous-autosave backup. Saves use a checksummed versioned JSON model envelope with full authoritative state, map seed, deterministic random-state, fog, progress, and configuration. Manual saves occur at command boundaries; autosaves occur after every fifth complete round and replace atomically. Older supported schemas migrate sequentially; invalid, newer, or corrupted saves never partially load.
- **Trade-off:** A small fixed slot set is easy to explain and test, while the backup protects the only automatically replaced save. Model-level JSON keeps persistence independent from scene layout and platform paths.
- **Acceptance checks:** Manual slots are never overwritten by autosave; round-trip state is exact; checksum/schema/invariant failures preserve the original slot; migrations preserve state; autosave occurs only after all participants finish the fifth round; desktop, Android, and Web use the same `user://` persistence contract.
- **Affected canonical sections:** [Game Design Document §13](game-design-document.md#13-saving-and-accessibility-constraints) and [Technical Architecture Proposal — Persistence](../technical/architecture-proposal.md#persistence).

### Interaction and input — initial prototype

- **Selected rule:** Touch is primary on Android/touch Web, mouse/keyboard on desktop, and controller is supported where exposed. Every device emits the same action vocabulary. Actions use selection → preview → confirmation → validated transition; canceling a preview changes no state and there is no general undo after confirmation. End turn always requires confirmation. Controls, focus order, 48-pixel targets, and UI scale presets are defined in GDD §13.
- **Trade-off:** A shared intent layer prevents platform-specific rule drift while preview/confirmation protects high-consequence actions on touch and controller. No gesture-only action keeps the game discoverable and accessible.
- **Acceptance checks:** Equivalent inputs produce equivalent commands; illegal actions are unavailable or rejected without mutation; preview cancellation preserves hashes and prior output; confirmed commands apply once; end-turn confirmation cannot be bypassed; focus and labels remain usable at every UI scale.
- **Affected canonical sections:** [Game Design Document §13](game-design-document.md#13-saving-and-accessibility-constraints) and [Technical Architecture Proposal — Input and display](../technical/architecture-proposal.md#input-and-display).
