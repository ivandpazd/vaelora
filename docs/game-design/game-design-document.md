# Vaelora — Game Design Document

**Status:** Preproduction baseline. Confirmed rules are separated from decisions still requiring design or balance work.

**Product:** A compact, turn-based fantasy 4X strategy game for Android, Windows, macOS, Linux, and Web.
**Design goal:** Keep the approachable readability of small-map strategy games while adding meaningful city development, production queues, and asymmetric civilizations without growing into a Civilization-scale simulation.

## 1. Product pillars

1. **Readable strategy:** hex maps, clear turns, one military unit per tile, and a focused set of city choices.
2. **Cities that develop:** cities claim land, grow over time, generate income, and build one unit or structure at a time.
3. **Trade-offs, not busywork:** each city has one active production project; research is a civilization-wide, single active project; workers have limited uses.
4. **Asymmetric civilizations:** a shared strategic foundation with distinct strengths, units, buildings, and economic approaches.
5. **Complete presentation from the prototype:** 2D, fixed isometric, bright fantasy art, landscape layout, and finished-quality assets; no placeholder-art release.

## 2. Player experience and match setup

The initial game is local single-player against one AI: exactly two civilizations participate. The player selects their civilization; the AI civilization is selected randomly. Difficulty is selected before the match and stays fixed. Easy, Intermediate, and Hard primarily change the AI's starting resources; Easy begins on the same resources as the player, with higher levels receiving larger advantages. Exact bonuses are TBD.

At setup, the player selects a match type, map type/size, and difficulty. The map is generated from a seed selected automatically. The game should retain the seed with the save so a map can be reproduced. Starting regions are not mirror images, but should have minimum separation and broadly comparable opportunities. Exact map families, dimensions, and fairness metrics are TBD. Future expansion may allow more participants according to map size; it is not part of the initial two-player scope.

## 3. Core loop and turn structure

**Explore → settle → develop → research → produce and position forces → contest territory → pursue the selected victory condition.**

A full round is strictly sequential: the human completes their turn, then each AI takes its turn one at a time. Turns never interleave. Production and research progress once when their civilization completes its turn. The player should be able to inspect a global standings screen during the match; it shows only total score, not score broken down by category.

## 4. Map, terrain, and visibility

The world is a procedurally generated hex grid. Terrain affects movement, defense, available improvements, and city resources.

- **Mountains** are traversable but reduce movement.
- **Peaks** are impassable.
- Forest terrain provides cover, especially against ranged attacks.
- Sea/coastal tiles support ports and naval play where terrain and city access permit.
- Other terrain yields, exact terrain set, and numerical movement/defense modifiers are TBD.

Fog of war hides unexplored tiles. Explored tiles outside the current vision range of a friendly city or unit remain visible as explored terrain but do not provide current sight of activity. Vision radii and reveal rules are TBD.

## 5. Cities and territory

Only a settler can found a city. The player cannot rename a city initially: its name is drawn randomly from a list belonging to its civilization. Cities begin at level 1 and can reach level 6. When a city levels up, it may claim additional tiles. A tile can be assigned to only one city, including where two cities' potential ranges overlap.

Cities grow gradually from resources and improvements in their assigned territory. Growth is not purchased with coins. Cities generate coins every turn, with higher-level cities producing more. Buildings and terrain improvements can contribute different economic, growth, production, or military benefits. Exact yields, growth thresholds, tile-claim selection rules, and level-up rewards remain TBD.

Captured cities transfer to the victor and cannot be razed. They keep their level and buildings; active production is canceled on capture. They remain on the map under new ownership. A civilization is eliminated when it loses its last city, even if it still has units.

## 6. City production and buildings

Each city may have exactly one active production project: **one unit or one building**, never both. Projects require a fixed number of turns. Illustrative early estimates—not locked balance values—are: worker 2 turns, basic soldier 4, settler 5, cavalry 6. City level, technologies, resources, and buildings may reduce production time. No city may be leveled up by paying coins.

Buildings should create distinct strategic choices by improving city growth, income, production, defense, or units produced there. Candidate roles include granary, barracks, walls, and academy; the final roster, prerequisites, stacking limits, and effects are TBD. A building unlocked through civilization-wide research becomes available to all eligible cities.

Naval combat units can be produced only in a coastal city with a port, using that city's same single production slot.

## 7. Improvements, workers, and roads

A worker can perform three improvement actions during its lifetime, then disappears. Each improvement assignment takes one turn and consumes one of the worker's three uses. A tile may have at most one non-road improvement. Improvements must match the terrain and benefit only the city to which the tile is assigned; examples include farms on meadows, mines on mountains, lumber facilities in forests, and ports on suitable coast/sea tiles.

Roads are a separate tile feature and do not use the non-road improvement slot. A worker can build them outside city vision. Each road segment consumes one worker use. Roads can be used by friendly and enemy units and increase movement speed. A complete road route between two cities of the same civilization provides an economic and growth bonus regardless of route length. The current balancing proposal is +10% per other connected own city, capped at +50%; road-routing rules, construction in enemy-controlled territory, and exact stacking are still to be settled.

## 8. Knowledge and research

Research belongs to the civilization, not to an individual city. Only one technology can be active at once. Technologies take a number of turns to complete and form a prerequisite tree. Approximately 80% of the tree is shared; approximately 20% is civilization-specific. Research can unlock units, buildings, improvements, and movement or combat capabilities. For example, road knowledge enables workers to create roads and can increase unit movement on them; granary knowledge makes granaries available to all eligible cities.

Research duration responds to the civilization's development—such as number and level of cities and their construction/infrastructure—so peaceful investment can accelerate technological progress. Military strength should not speed unrelated research. Exact formula and the role, if any, of military research bonuses are TBD. Coins may be spent as a **one-time payment when a research project begins** to accelerate that project; this is optional and is not a recurring upkeep. Exact amount/effect and whether the payment can be changed after starting are TBD.

Knowledge victory requires completing 100% of the civilization's entire technology tree.

## 9. Units, movement, and combat

The named initial core roster is settlers, explorers, and basic soldiers. Workers are described separately as civilian utility units for improvements and roads, with three uses; the indicative worker production time is 2 turns. Whether workers are included in the initial production roster alongside the three named roles is still to be confirmed before implementation. Civilizations may have different characteristics and later asymmetric variants. Additional military unit types are outside the initial roster unless separately approved.

There can be only one military unit on a hex. Friendly units may be traversed when movement permits. A unit may move and then attack in the same turn if the move and target are within its allowed ranges; after attacking it cannot take another action that turn. Rest is a separate player-activated action and cannot be combined with moving or attacking. Rest restores 25% of maximum health, or 40% total when used inside a friendly city.

Combat damage accumulates; surviving units retain their remaining health. A defender automatically retaliates in adjacent melee combat. Ranged attacks from outside melee adjacency do not trigger that retaliation. When an attacker wins, it occupies the defeated enemy's tile; a victorious defender stays on its own tile. Exact hit/damage formulas, unit stats, ranged distances, and healing constraints are TBD.

Defensive strength is affected by location: cities provide a defense bonus, walls add defense, forests give cover against ranged attacks, and mountains give stronger defense. Numerical values and interaction/stacking rules are TBD.

## 10. Naval transport

A land unit that embarks remains that same unit in a vulnerable transport state; it is not a separately produced unit. It may end a turn in open sea when needed to reach distant land and is vulnerable while transported. Naval combat vessels are a separate class that can attack; they follow the coastal-city-and-port production rule above. Embark/disembark restrictions, transport movement and combat rules, and open-sea survival are TBD.

## 11. Match types and victory

The setup menu offers:

- **Turn limit:** match ends after a preset number of turns determined by the number of opponents; the highest total score wins.
- **Total conquest:** no turn limit; win by controlling the remaining cities/eliminating the opponent.
- **Knowledge:** no turn limit; win by completing 100% of the technology tree.
- **Combined:** total conquest or 100% knowledge, whichever happens first.

The turn-limit score combines technological development, number and level of cities, and military performance through cities conquered and enemy units eliminated. The standings view exposes only the aggregate score. Scoring weights, tie resolution, exact turn limits, and conquest end-state details remain TBD.

## 12. Saving and accessibility constraints

The player may save manually at any time. Automatic saves occur every five **complete rounds**, after all participants have finished—not every player turn. More frequent saves are manual. Save-slot UX, save compatibility/versioning, and platform-specific storage behavior require technical design.

The game is 2D with a fixed isometric perspective and must be played in landscape orientation. Touch, mouse, keyboard, controller support, UI scaling, and accessibility options are TBD and must be designed per platform before implementation.

## 13. Setting and civilization identity

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

## 14. Art and audio direction

All gameplay is 2D with a consistent, fixed isometric camera. Initial art should feel bright, luminous, and fantastical; darker palettes or alternate setting themes are future scope. Blender is a possible supporting tool for asset creation, but final game resources should match the 2D art pipeline. All prototype assets must be final-quality; placeholder visuals are not acceptable. Audio direction, animation budget, palette, silhouettes, and asset specifications remain TBD.

## 15. Open decisions before implementation

The following are intentionally unresolved—not implied approvals: whether workers are part of the initial roster; map sizes and terrain catalog; start-resource tables; exact AI behavior; city growth and claim formulas; complete production, building, improvement, unit, and technology rosters; project costs/durations; combat equations and stack rules; vision radii; naval restrictions; road placement/routing and bonuses; score weights/ties/turn limits; save compatibility and UX; platform-specific controls/accessibility; and final asset/audio specifications. These should be decided in focused batches and playtested rather than guessed in code.
