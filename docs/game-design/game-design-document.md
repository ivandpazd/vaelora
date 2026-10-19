# Vaelora — Game Design Document

**Status:** Preproduction baseline. Confirmed rules are separated from decisions still requiring design or balance work.

**Product:** A compact, turn-based fantasy 4X strategy game for Android, Windows, macOS, Linux, and Web.

This is the canonical gameplay baseline. The [product vision](../product/vision-and-scope.md), [world and civilizations](world-and-civilizations.md), and [open decisions register](open-decisions.md) provide complementary detail; do not treat a proposal or TBD as an accepted rule.
**Design goal:** Keep the approachable readability of small-map strategy games while adding meaningful city development, production queues, and asymmetric civilizations without growing into a Civilization-scale simulation.

## 1. Product pillars

1. **Readable strategy:** hex maps, clear turns, one military unit per tile, and a focused set of city choices.
2. **Cities that develop:** cities claim land, grow over time, generate income, and build one unit or structure at a time.
3. **Trade-offs, not busywork:** each city has one active production project; research is a civilization-wide, single active project; workers have limited uses.
4. **Asymmetric civilizations:** a shared strategic foundation with distinct strengths, units, buildings, and economic approaches.
5. **Complete presentation from the prototype:** 2D, fixed isometric, bright fantasy art, landscape layout, and finished-quality assets; no placeholder-art release.

## 2. Player experience and match setup

The initial game is local single-player against one AI: exactly two civilizations participate. The player selects their civilization; the AI civilization is selected randomly. Difficulty is selected before the match and stays fixed. Easy, Intermediate, and Hard primarily change the AI's starting resources; Easy begins on the same resources as the player, with higher levels receiving larger advantages. Exact bonuses are TBD. Future map sizes may support more participants, with an earlier long-term concept of up to six; this is not part of the initial two-player scope.

At setup, the player selects a match type, map type, map size, and difficulty. The initial release offers three map types: **Continents** (two major landmasses with coastal access), **Inland Sea** (a central sea surrounded by connected land), and **Archipelago** (several islands linked by navigable water). The initial sizes are **Small** (48 × 32 hexes), **Medium** (64 × 40), and **Large** (80 × 50). These dimensions describe the rectangular generation bounds; unusable water or edge tiles may reduce the playable area.

The map is generated from an automatically selected seed. The seed is displayed after match creation, included in the save, and shown in the match summary so a map can be reproduced. The player does not enter a seed during normal setup. The two starting city sites must be at least 12 hexes apart. Each starting region is evaluated within a radius of four hexes around its city site; the regions must contain at least 20 workable land tiles and their normalized opportunity scores must differ by no more than 15%. The score is calculated from the approved terrain/content weights for food, production, income, strategic terrain, and coastal access where the map type supports it. Starts are asymmetric by default; the generator must not mirror or rotate one starting region to create the other.

The initial turn-limit schedule is **100 turns for Small, 140 for Medium, and 180 for Large**. These limits apply only to Turn limit matches; the other modes have no turn limit. The base starting package is the same for both civilizations: one settler, one explorer, one worker, and 100 coins. Difficulty-specific AI advantages, if any, are applied on top of this base package and remain a separate decision. The initial city is founded by the settler and starts at level 1 with no building or production progress. Future expansion may allow more participants according to map size; it is not part of the initial two-player scope.

## 3. Core loop and turn structure

**Explore → settle → develop → research → produce and position forces → contest territory → pursue the selected victory condition.**

A full round is strictly sequential: the human completes their turn, then each AI takes its turn one at a time. Turns never interleave. Production and research progress once when their civilization completes its turn. The player should be able to inspect a global standings screen during the match; it shows only total score, not score broken down by category.

## 4. Map, terrain, and visibility

The world is a procedurally generated hex grid. Terrain affects movement, defense, line of sight, available improvements, and the base resources received by the city assigned to a tile. Yields in the table are base yields before improvements or civilization modifiers.

| Terrain | Movement cost | Base yield (food / production / coins) | Defense | Vision and movement rules |
|---|---:|---:|---:|---|
| Meadow | 1 | 2 / 0 / 0 | 0% | Open sight; normal movement |
| Plains | 1 | 1 / 1 / 0 | 0% | Open sight; normal movement |
| Forest | 2 | 1 / 1 / 0 | +15% | Blocks line of sight through the tile; ranged attacks into forest receive the forest defense modifier |
| Hills | 2 | 0 / 2 / 0 | +15% | A unit on hills gains +1 vision; hills block line of sight beyond the first hill tile |
| Mountain | 3 | 0 / 1 / 1 | +30% | A unit on a mountain gains +2 vision; mountains block line of sight beyond the tile |
| Coast | 1 | 1 / 0 / 1 | 0% | Traversable land adjacent to sea; open sight; eligible for a port when city access permits |
| Shallow sea | 1 for naval units | 0 / 0 / 0 | 0% | Naval and embarked movement; open sight; cannot hold cities or land improvements |
| Open sea | 2 for naval units | 0 / 0 / 0 | 0% | Naval and embarked movement; open sight; cannot hold cities or land improvements |
| Peak | Impassable | 0 / 0 / 0 | — | Blocks line of sight; no unit or improvement may occupy it |

The map generator must use these terrain categories in the initial prototype. A city may assign only workable land tiles—Meadow, Plains, Forest, Hills, Mountain, or Coast—to its territory. Sea tiles are not workable city territory.

Improvements are legal as follows: Farms on Meadow or Plains; lumber facilities on Forest; mines on Hills or Mountain; and ports on Coast. Roads may be built on any traversable land tile, including a tile that already has a non-road improvement. Peaks and all sea tiles reject land improvements and roads. A tile may have at most one non-road improvement.

Fog of war hides unexplored tiles. Explored tiles outside the current vision range of a friendly city or unit remain visible as explored terrain but do not provide current sight of activity. Units use a base vision radius of 2 hexes; cities use a base vision radius of 3. Hills and mountains add their terrain vision bonus, while forest, hills, mountains, and peaks apply the line-of-sight blocking rules above. Improvements do not change vision in the initial prototype.

## 5. Cities and territory

Only a settler can found a city. The player cannot rename a city initially: its name is drawn randomly from a list belonging to its civilization. Cities begin at level 1 and can reach level 6. Founding a city assigns its city tile and grants three territory-claim tokens. Each level-up grants two additional base claim tokens, for a base maximum of fourteen assigned tiles at level 6, including the city tile. Explicit civilization technologies may add claim tokens as described in the research tree. A tile can be assigned to only one city, including where two cities' potential ranges overlap.

A claim token may be spent on an unassigned, workable land tile within three hexes of the city and adjacent to the city's existing territory. The player chooses claims through the city view; the AI chooses the highest-opportunity legal tile, breaking ties by nearest distance and then canonical coordinate order. Claim tokens are retained if no legal tile is available and may be spent later. A city cannot claim another city's assigned tile, and claiming never removes territory from another city. Capturing a city transfers its assigned territory with it; the active production is still canceled on capture.

Cities grow gradually from resources and improvements in their assigned territory. Growth is not purchased with coins. Each completed city turn grants `floor(total assigned food yield / 3)` growth points, plus the Granary bonus when present. Cumulative growth thresholds are 20 points for level 2, 50 for level 3, 90 for level 4, 140 for level 5, and 200 for level 6. Cities generate coins every turn, with higher-level cities producing more. Buildings and terrain improvements can contribute different economic, growth, production, or military benefits. Territory claims and growth thresholds are fixed by this section; the economy section defines the remaining yield and building effects.

Captured cities transfer to the victor and cannot be razed. They keep their level and buildings; active production is canceled on capture. They remain on the map under new ownership. A civilization is eliminated when it loses its last city, even if it still has units.

## 6. City production and buildings

Each city may have exactly one active production project: **one unit or one building**, never both. There is no production queue. A project advances once when its civilization completes its turn, and the city becomes idle when the project finishes. Production does not consume coins. The durations below are baseline durations for a city producing three production points per turn; terrain, improvements, buildings, and explicit technologies can modify project progress through the rules in the economy section.

The initial production roster is:

| Project | Type | Base duration | Prerequisites and limits |
|---|---|---:|---|
| Worker | Civilian unit | 2 turns | Available from level 1; no per-city limit |
| Explorer | Civilian unit | 3 turns | Available from level 1; no per-city limit |
| Basic soldier | Military unit | 4 turns | Available from level 1; requires no building; one military unit per hex still applies |
| Settler | Civilian unit | 6 turns | Available from level 1; no per-city limit |
| Patrol ship | Naval unit | 5 turns | Coastal city, completed port improvement, and Seamanship technology |
| Granary | Building | 5 turns | Agriculture technology; one per city |
| Barracks | Building | 5 turns | Military Training technology; one per city |
| Walls | Building | 6 turns | Masonry technology; one per city |
| Academy | Building | 8 turns | Scholarship technology and city level 3; one per city |

The four initial buildings create distinct growth, military, defense, and research choices. A building unlocked through civilization-wide research becomes available to all eligible cities. Civilization-specific projects may extend this roster later, but they do not replace the initial shared projects.

Each project's production cost is its baseline duration multiplied by three. A city generates three base production points per completed turn plus the production yield of its assigned tiles and applicable building or technology bonuses. A project completes when its accumulated production reaches its cost; fractional progress is not used.

The player may cancel an active project before completion; cancellation loses its accumulated progress and leaves the city idle. Starting another project is therefore a deliberate reset, not a free queue reorder. If a completed unit has no legal deployment tile, the project remains complete but the unit is not spawned until a legal tile is available; no progress is lost. Capturing a city cancels its active project and loses its progress. No city may be leveled up by paying coins.

Naval combat units can be produced only in a coastal city with a port, using that city's same single production slot.

## 7. Improvements, workers, and roads

A worker can perform three improvement actions during its lifetime, then disappears. A worker has one action per turn: it may move, or it may construct or replace one improvement. It cannot move and improve in the same turn. Construction completes when the worker's civilization completes its turn and consumes one of the worker's three uses. A tile may have at most one non-road improvement, and improvements cannot be stacked or upgraded in the initial prototype.

| Improvement | Legal terrain | Effect | Prerequisite and limit |
|---|---|---|---|
| Farm | Meadow or Plains | +2 food to the assigned city | Available from the start; one per tile |
| Lumber facility | Forest | +1 production and +1 coin to the assigned city | Forestry technology; one per tile |
| Mine | Hills or Mountain | +2 production to the assigned city | Mining technology; one per tile |
| Port | Coast | +1 coin and enables Patrol ship production | Seamanship technology; one port per city |

Non-road improvements may be built only on a tile assigned to a city of the worker's civilization. They benefit only that assigned city. A port must be on a Coast tile in the city's territory and is available only to a city with coastal access. Ports have no maintenance cost in the initial prototype. Replacing an existing improvement is allowed, consumes one worker use, and removes the old improvement only when the replacement completes; a failed or invalid replacement leaves the original improvement unchanged.

Workers may construct improvements outside current city vision, provided the tile is legally assigned and visible through the player's known map state. An improvement cannot be canceled after the action begins. Improvements remain on a tile when its city is captured and transfer their benefits to the new owner; workers themselves are not captured and can be defeated normally by combat.

### Economy and production yields

Both civilizations begin with **100 coins**. A city produces base coins by level before assigned-tile and building effects:

| City level | Base coins per completed turn |
|---:|---:|
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |
| 4 | 7 |
| 5 | 8 |
| 6 | 10 |

The city's coin income is the sum of its level income, assigned-tile coin yields, and applicable improvement/building effects. The initial buildings add these effects: Granary grants +1 growth point per completed city turn; Barracks grants +1 production point per turn while producing a military unit; Walls grant +20% city defense; Academy grants +2 research points per completed civilization turn. Buildings have no coin maintenance in the initial prototype.

Production points are calculated as three base points plus assigned-tile production yields and applicable production bonuses. Growth points are calculated from assigned food as defined in §5, then building and route bonuses are added. The active road-network bonus is applied after all flat coin and growth sources: each other own city in the connected component grants +10%, capped at +50%, with fractional final values rounded down. Coins may be spent on the one-time research acceleration payment; they are not required for production, city growth, territory claims, roads, or improvements.

Roads are a separate tile feature and do not use the non-road improvement slot. A worker can build one road segment as its action for the turn, including outside current city vision when the tile is known. Each segment consumes one worker use. Roads may be built on any traversable land tile—Meadow, Plains, Forest, Hills, Mountain, or Coast—provided the tile is unassigned or controlled by the worker's civilization. Roads cannot be built on enemy-controlled territory, Peaks, or sea tiles. Road construction does not require a technology in the initial prototype.

Roads remain usable by friendly and enemy units. Entering a road tile costs one movement point regardless of the underlying land terrain; roads do not change naval or embarked movement. City tiles count as connected road nodes without requiring a road segment. Road segments cannot be removed or upgraded in the initial prototype.

A route is complete when a continuous chain of adjacent road tiles and city tiles connects two or more cities of the same civilization. A route may pass through unassigned land and may contain branches. A route bonus is active only while every segment in the relevant connection is outside enemy-controlled territory. Each city receives **+10% to coin income and growth points for every other own city in its connected road network**, capped at **+50%**. The bonus is calculated from the current connected component; capturing a city or road tile can break or change the component immediately after the turn resolves.

## 8. Knowledge and research

Research belongs to the civilization, not to an individual city. Only one technology can be active at once and there is no research queue. Technologies form a prerequisite tree with approximately 75% shared technologies and two civilization-specific technologies for each prototype civilization. Research can unlock buildings and improvements or grant explicit movement, growth, vision, healing, production, or combat modifiers.

The initial shared technology tree is:

| Tier | Technology | Prerequisites | Cost | Initial effect |
|---|---|---|---:|---|
| 1 | Agriculture | None | 20 RP | Unlocks Granary |
| 1 | Forestry | None | 20 RP | Unlocks Lumber facility |
| 1 | Mining | None | 20 RP | Unlocks Mine |
| 1 | Military Training | None | 20 RP | Unlocks Barracks |
| 1 | Seamanship | None | 20 RP | Unlocks Port and Patrol ship |
| 1 | Scholarship | None | 20 RP | Unlocks Academy |
| 2 | Masonry | Mining | 35 RP | Unlocks Walls |
| 2 | Cartography | Scholarship | 35 RP | Explorers gain +1 vision |
| 2 | Logistics | Military Training and Mining | 35 RP | Civilian units gain +1 movement point when their move uses roads |
| 2 | Medicine | Agriculture and Scholarship | 35 RP | Rest heals 35% of maximum health, or 50% inside a friendly city |
| 3 | Engineering | Masonry and Mining | 50 RP | Building projects cost 3 fewer production points, to a minimum cost of 3 |
| 3 | Metallurgy | Military Training and Mining | 50 RP | Basic soldiers gain +10% attack and defense |

The Liga de Auren has two additional technologies: **Civic Charter** (Agriculture and Scholarship; 35 RP), which grants one additional territory-claim token at each city level-up before level 6, and **Public Works** (Engineering; 50 RP), which grants +1 production point per turn to cities connected by an active own road network. The Clanes de Brasal has two additional technologies: **Warband Tradition** (Military Training and Metallurgy; 35 RP), which reduces Basic soldier production cost from 12 to 9 points, and **Foraging Doctrine** (Agriculture and Medicine; 50 RP), which grants +1 food to assigned Forest and Plains tiles.

At the end of each civilization turn, research generates:

```text
research points = 4
                 + number of cities
                 + floor(sum of city levels / 2)
                 + floor(number of assigned tiles with non-road improvements / 4)
                 + 2 per completed Academy
```

Military strength does not contribute to research. The formula rewards peaceful city development, territory, and infrastructure without making combat a direct research multiplier. A technology completes when its accumulated research points reach its cost.

When a technology begins, the player may make one acceleration payment equal to **2 coins per research point in the technology's cost**. The payment immediately contributes **half of the technology's cost**, rounded up, and cannot be changed, refunded, or repeated. A technology may be canceled before completion, but all accumulated research and the acceleration payment are lost. Research and acceleration resolve only for the civilization whose turn has completed.

Knowledge victory requires completing 100% of the civilization's entire technology tree, including its civilization-specific technologies.

## 9. Units, movement, and combat

The named initial core roster is settlers, explorers, basic soldiers, and workers. Workers are civilian utility units for improvements and roads, with three uses. Civilizations may have different characteristics and later asymmetric variants. Additional military unit types are outside the initial land-combat roster unless separately approved.

Initial land-unit combat data is:

| Unit | Maximum health | Attack | Defense | Movement points | Combat role |
|---|---:|---:|---:|---:|---|
| Settler | 50 | 0 | 0 | 2 | Civilian; cannot attack |
| Worker | 50 | 0 | 0 | 2 | Civilian; cannot attack |
| Explorer | 60 | 0 | 5 | 4 | Civilian scout; cannot attack |
| Basic soldier | 100 | 30 | 20 | 3 | Melee military unit; range 1 |

There can be only one military unit on a hex. Friendly units may be traversed when movement permits, but a military unit cannot end its move on another military unit. A unit may move and then attack in the same turn if the move and target are within its allowed ranges; after attacking it cannot take another action that turn. Rest is a separate player-activated action and cannot be combined with moving or attacking. Rest restores 25% of maximum health, or 40% inside a friendly city; Medicine changes these values to 35% and 50%.

Combat is deterministic and sequential. Effective defense is the unit's defense stat multiplied by the sum of location modifiers: terrain, city tile (+25%), and Walls (+20%) are additive percentage modifiers. Damage is calculated as:

```text
damage = max(1, floor(attacker attack × 100 / (100 + effective defense)))
```

Damage accumulates and surviving units retain their remaining health. A defender automatically retaliates once after surviving an adjacent melee attack, using the same formula against the attacker's effective defense. Retaliation does not consume a separate turn action. Ranged attacks, when a later unit provides them, require line of sight and do not trigger retaliation when performed outside melee adjacency; the initial land roster has no ranged unit.

When an attacker wins, it occupies the defeated unit's tile. A victorious defender stays on its own tile. Units with health at or below zero are removed; civilians are destroyed rather than captured. The initial prototype has no city garrison: a city is captured when an enemy military unit enters its city tile while no defending military unit occupies it. If a defender occupies the tile, it must be defeated first, and the attacker captures the city only on a later legal entry. Capturing transfers the city, its level, buildings, assigned territory, and completed improvements; active production is canceled.

## 10. Naval transport

A land unit that embarks remains that same unit in a vulnerable transport state; it is not a separately produced unit and does not occupy a separate transport vessel. Settlers, workers, explorers, and basic soldiers may embark from the tile of a friendly coastal city with a completed Port. Embarkation consumes the unit's action for the turn. An embarked unit has 2 movement points, cannot attack, cannot use roads, and may end a turn in Shallow sea or Open sea.

Sea movement uses the terrain costs from §4: Shallow sea costs 1 movement point and Open sea costs 2. An embarked unit may disembark on an unoccupied Coast tile adjacent to its current sea tile, or into a friendly coastal city with a Port. The destination must not be enemy-controlled and must not contain an enemy military unit. Disembarkation consumes the unit's action for the turn; the unit cannot move or attack again that turn. Embarkation and disembarkation are therefore deliberate port or beachhead operations rather than free movement extensions.

The initial naval combat vessel is the Patrol ship: 100 maximum health, 25 attack, 15 defense, 4 movement points, and melee range 1. It can enter Shallow sea and Open sea, move and attack in the same turn, and uses the same deterministic damage and retaliation rules as land combat. Naval units occupy one military unit slot per sea hex. A Patrol ship may attack another Patrol ship or an embarked land unit; an embarked unit cannot retaliate. When an embarked unit reaches zero health, the land unit is lost. When a Patrol ship reaches zero health, it is removed.

Patrol ships can be produced only in a friendly coastal city with a completed Port and Seamanship technology, using the city's normal production slot. A captured city keeps its Port but cancels active ship production under the general city-capture rule. No naval ranged unit, naval blockade, refueling, or naval maintenance exists in the initial prototype.

## 11. Match types and victory

The setup menu offers:

- **Turn limit:** the match ends after the size-specific limit of 100, 140, or 180 complete rounds. The highest total score wins; losing the last city does not end this mode early, but the eliminated civilization's future turns are skipped.
- **Total conquest:** no turn limit; the first civilization to control the opponent's last city wins immediately.
- **Knowledge:** no turn limit; the first civilization to complete 100% of its complete technology tree wins immediately.
- **Combined:** the first civilization to satisfy total conquest or knowledge wins. At the end of a civilization turn, conquest is checked before knowledge if both conditions are satisfied by the same resolution.

The turn-limit score is:

```text
score = technology score + city score + military score

technology score = sum of the research-point costs of completed technologies
city score       = (20 × owned cities) + (10 × sum of owned city levels)
military score   = (40 × enemy cities captured)
                   + (10 × enemy military units destroyed)
                   + (5 × enemy civilian units destroyed)
```

No points are awarded for damage, uncaptured territory, roads, coins, or incomplete projects. Scores update after each completed civilization turn, and the standings screen exposes only the aggregate total. At the turn limit, the final score is calculated after both participants complete the final round. Ties are resolved by completed research cost, then total city levels, then surviving military-unit count; if all three remain equal, the match is declared a draw.

## 12. AI and difficulty

The AI uses the same authoritative command interface, validation rules, visible information, production slots, research rules, movement points, and fog of war as the human player. It cannot inspect unexplored tiles, use illegal actions, receive free units, or change difficulty during a match. The AI civilization and difficulty are fixed at match setup.

The AI resolves each turn in this order:

1. Complete an immediately available victory or prevent an immediate opponent victory.
2. Defend a city that can be captured during the opponent's next turn.
3. Capture an undefended enemy city or defeat a reachable enemy unit when the action is legal and leaves the acting unit alive.
4. Choose city production: a threatened city prioritizes a Basic soldier; otherwise an idle city follows the current strategic priority of settlement, infrastructure, research, then military reinforcement.
5. Select research using the first available technology that unlocks the current strategic priority; if several are equal, use the shared-tree order in §8.
6. Spend claim tokens and construct legal improvements that improve the city's current priority; connect cities with roads when a route can be completed without entering enemy-controlled territory.
7. Move explorers toward the nearest highest-value unexplored region and move military units toward the nearest actionable threat or objective.

When an action has multiple legal choices, the AI evaluates the result within its difficulty horizon and breaks equal evaluations by highest immediate score, then lowest movement cost, then canonical coordinate order. Easy uses a one-turn horizon, Intermediate uses a two-turn horizon, and Hard uses a three-turn horizon. Horizons do not grant hidden information: every evaluated state uses only information the AI could currently see.

Difficulty changes only the AI's starting coins and planning horizon:

| Difficulty | AI starting coins | Planning horizon |
|---|---:|---:|
| Easy | 100 | 1 turn |
| Intermediate | 150 | 2 turns |
| Hard | 200 | 3 turns |

All difficulties receive the same starting units and technology state as the player. Easy therefore has no resource advantage; Intermediate receives 50 additional coins; Hard receives 100 additional coins. The AI uses deterministic tie-breaking so the same match seed, configuration, and visible state produce the same AI decisions.

## 13. Saving and accessibility constraints

The player may save manually at any command boundary, including during either participant's turn when no command is currently resolving. Each profile has three manual save slots, one dedicated autosave slot, and one previous-autosave backup. Manual saves are never overwritten by autosave. Automatic saves occur every five **complete rounds**, after all participants have finished—not every player turn. The autosave slot is replaced atomically and the previous autosave is retained as the backup.

Saves use a versioned, model-level JSON envelope rather than serialized scene nodes. Each save contains `schema_version`, `game_build`, timestamp, slot kind, match configuration, map seed, deterministic random-state, full authoritative board/entity state, ownership and territory, active civilization and round, production and research progress, completed technologies, fog/visibility state, and a checksum over the canonical payload. A successful save is written to a temporary file, validated, flushed, and atomically renamed into its slot.

Loading validates the checksum, schema version, required fields, value ranges, ownership invariants, and deterministic-state structure before replacing the active match. Schema migrations are explicit and sequential; a supported older schema is migrated into a new validated save while the original remains untouched. A newer unsupported schema, failed checksum, invalid state, or failed migration never partially loads and leaves the original slot unchanged. The loader offers the previous-autosave backup when the current autosave is invalid. There is no cloud synchronization in the initial prototype.

The Godot `user://` persistence abstraction is used for desktop, Android, and Web storage. Platform-specific paths are not exposed to gameplay code. Save and load errors are shown with the affected slot and a recovery action; they never silently discard a valid save.

The game is 2D with a fixed isometric perspective and must be played in landscape orientation. All platforms use the same action vocabulary through input adapters: select, inspect, move, attack, rest, embark, disembark, claim, improve, build road, choose production, choose research, save, cancel, and end turn.

Touch is the primary input on Android and supported Web touch devices. Mouse and keyboard are primary on Windows, macOS, Linux, and desktop Web. Controller input is supported on desktop and Android where the platform exposes a controller. No gameplay action is available only through a gesture: every action is also available from a visible command or focusable menu.

The interaction flow is selection → preview → confirmation → one validated state transition. Tapping or clicking a tile selects its city, unit, or available city/unit choice; a tile containing both shows both explicitly and never chooses implicitly. Selecting a friendly unit exposes only legal actions. Selecting a city opens territory, production, research, and save-related actions. Moving, attacking, improving, building roads, embarking, disembarking, claiming, choosing production or research, and ending the turn all show a preview and require confirmation. Canceling a preview changes no authoritative state. After confirmation, there is no general undo; a later command must be used to correct a reversible strategic choice.

On desktop, primary click selects and secondary click cancels or closes a preview; Enter confirms, Escape cancels, Space opens end-turn confirmation, the mouse wheel zooms, and middle-button drag pans. On touch, a tap selects, a second tap on a legal destination previews the action, a two-finger drag pans, and pinch zooms. On controllers, the left stick or D-pad moves focus, A confirms, B cancels/back, X opens the action menu, Y opens end-turn confirmation, and shoulder buttons cycle selectable units or cities. Keyboard and controller focus order follows the same visible action order as touch and mouse menus.

All actionable controls use a minimum 48 logical-pixel target, preserve landscape safe areas, provide visible focus, and expose text labels for screen readers where the platform supports them. UI scaling offers 100%, 125%, 150%, 175%, and 200% presets. Detailed localization, colorblind palette validation, and screen-reader coverage beyond actionable labels remain content-lock decisions.

## 14. Setting and civilization identity

Vaelora is both the game title and the continent. Its people once relied on **the Trama**, a network of roads and signal beacons that connected settlements and supported trade and communication. The network weakened through neglected upkeep and political disputes over which routes deserved investment. As connections failed, the alliance coordinating them dissolved. Generations later, rival civilizations rebuild, expand, and compete for control of valuable land and routes. This is grounded context for a strategy game, not a prophecy or world-ending epic.

The six planned civilization concepts are:

| Civilization | People | Initial status |
|---|---|---|
| Liga de Auren | Humans | Prototype |
| Clanes de Brasal | Orcs | Prototype |
| Raíces de Nymara | Elves | Later expansion |
| Círculos de Durn | Dwarves | Later expansion |
| Compañías de la Chispa | Goblins | Later expansion |
| Vigilia de los Nombres | Skeletons | Later expansion |

These are original fantasy civilizations inspired by familiar archetypes, not licensed Warhammer factions. Civilizations are asymmetric: specializations affect available options and strengths but do not wholly forbid common functions (for example, orcs may still build ports or lumber facilities). Their exact unique technologies, units, buildings, city-name lists, and economic identities remain TBD.

## 15. Art and audio direction

All gameplay is 2D with a consistent, fixed isometric camera. Initial art should feel bright, luminous, and fantastical; darker palettes or alternate setting themes are future scope. Blender is a possible supporting tool for asset creation, but final game resources should match the 2D art pipeline. All prototype assets must be final-quality; placeholder visuals are not acceptable. Audio direction, animation budget, palette, silhouettes, and asset specifications remain TBD.

## 16. Open decisions before implementation

The following remain intentionally unresolved—not implied approvals: save slots, save compatibility/versioning, and platform persistence; touch/mouse/keyboard/controller interaction priorities and accessibility; exact human/orc visual identities, city-name pools, and later balance refinements; final platform performance targets; and final art/audio specifications. These should be decided in focused batches and playtested rather than guessed in code. Terrain, map setup and fairness, city territory, production, workers, improvements, roads, research, economy, land combat, naval transport, victory/scoring, AI/difficulty, and city-garrison behavior are resolved in the preceding sections, subject to implementation verification and balance testing.
