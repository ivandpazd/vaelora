# World and Civilizations

## Tone and purpose

Vaelora's lore gives the strategy game a recognizable setting and supports future store and landing-page copy. It stays direct and grounded: political disputes, trade, routes, settlement growth, and competition for territory. The setting is context for play, not an epic prophecy or a world-ending crisis.

## The continent of Vaelora

Vaelora is a continent of settlements separated by forests, plains, mountains, coastlines, and stretches of open sea. In earlier generations, roads and signal beacons linked distant communities. The network—known as **the Trama**—made trade and communication more reliable and helped settlements coordinate.

Maintaining the Trama required shared investment. The central administration and local rulers disagreed about which roads deserved repair and who should pay. Some routes were prioritized, others deteriorated, and political disputes weakened the agreements that had held the network together. As connections failed, the alliance responsible for maintaining them dissolved. This was a gradual infrastructure and political failure, not a magical apocalypse.

Generations later, the settlements of Vaelora are rebuilding. Cities compete for productive land, trade routes, resources, and influence. Some leaders invest in connections and research; others rely on military strength or distinctive economic practices. The match begins with two rival civilizations contesting a newly generated region of the continent.

## The Trama as world and game motif

The Trama is the old road-and-beacon network; it is not a playable faction or a separate magic system. Its legacy can appear through road-building, map landmarks, city histories, ruins, and visual motifs. Current gameplay roads are practical infrastructure that improves movement and rewards completed connections between a civilization's own cities.

**Open:** whether old beacons, ruins, or remnants provide any mechanical effect. Do not add an effect merely because the lore mentions them.

## Planned civilizations

| Civilization | People | Prototype timing | Identity status |
|---|---|---|---|
| Auren League | Humans | Initial prototype | Resolved in issue #11; infrastructure-led baseline with Civic Charter and Public Works |
| Brasal clans | Orcs | Initial prototype | Resolved in issue #12; adaptive frontier identity with Foraging Doctrine and Warband Tradition |
| Raíces de Nymara | Elves | After prototype gate | Working name and archetype; design not finalized |
| Círculos de Durn | Dwarves | After prototype gate | Working name and archetype; design not finalized |
| Compañías de la Chispa | Goblins | After prototype gate | Working name and archetype; design not finalized |
| Vigilia de los Nombres | Skeletons | After prototype gate | Working name and archetype; design not finalized |

The six concepts are original fantasy peoples informed by familiar fantasy archetypes. They are not Warhammer factions or derivative setting canon. The initial prototype should only implement humans and orcs until its final test battery is complete.

## Civilization design rules

- The technology tree is approximately 80% shared and 20% civilization-specific.
- Asymmetry is about trade-offs and specialization, not making a civilization unable to use core game systems.
- A civilization can retain access to common infrastructure such as ports or lumber facilities even if it specializes elsewhere.
- The initial shared unit roles are settlers, explorers, and basic soldiers. Their exact stats may differ between civilizations.
- Workers are discussed as civilian utility units with three improvement uses; whether workers are included in the initial production roster alongside the three named roles remains unresolved.
- Each civilization needs a name pool for randomly named cities; players cannot rename cities in the initial scope.

## Prototype faction design briefs

These are design prompts, not finalized mechanics.

### Auren League — humans

**Identity statement:** The Auren League rebuilds the Trama through coordinated civic investment. It is the approachable infrastructure-and-research baseline: connect cities, turn reliable administration into production, and use a broad technology route to choose between expansion, development, and conquest.

**Player-facing promise:** *Connect first, then make every city count.* Auren rewards visible, deliberate networks rather than hidden information, free units, or a separate rules system.

#### Strategic identity and trade-offs

- The League's core advantage is dependable infrastructure: its strongest faction-specific effects require research and active road connections between its own cities.
- The League has no innate unit or building-stat modifier. Settlers, workers, explorers, soldiers, buildings, production costs, and shared technologies use the common prototype rules unless an accepted technology below changes them.
- The trade-off is tempo: Auren must invest workers, road segments, and research before its strongest production benefit appears. An early military rush remains possible, but it does not receive a faction discount.
- The intended routes are readable and complementary: Civic Charter supports territorial growth, while Public Works supports connected-city production. Neither technology makes a peaceful victory automatic or blocks conquest.

#### Unique technologies

| Technology | Prerequisites | Cost | Exact effect | Formula or system affected |
|---|---|---:|---|---|
| Civic Charter | Agriculture and Scholarship | 35 RP | Grants one additional territory-claim token whenever an Auren city levels up from level 1 through level 5; level 6 grants no further token | City level-up claim-token award |
| Public Works | Engineering | 50 RP | Grants +1 production point per turn to each Auren city in an active own road network; a city must be connected to at least one other own city when its civilization turn resolves | City production points |

Public Works does not create a route, make a disconnected city eligible, alter the road-network coin or growth bonus, or stack for multiple connected cities. Civic Charter does not change claim legality, territory range, city growth thresholds, or the base level-6 maximum outside its documented extra tokens.

#### City names and naming rules

Cities draw uniformly without replacement from the following initial pool until the pool is exhausted: Auren, Ceralis, Doreva, Elandor, Faren, Halden, Ilyra, Liora, Maroven, Nareth, Orsena, Pellan, Queral, Ravelin, and Veyra. Names are assigned when a settler founds a city, cannot be chosen or edited by the player in the initial prototype, and are persisted in saves. If a later pool expansion is needed, new names must follow the same short, pronounceable, non-hyphenated naming rule and must not duplicate an existing name.

#### Heraldry and visual language

- **Heraldic mark:** a gold three-strand knot over a deep blue field, representing the Trama's connected routes and the League's civic institutions.
- **Palette:** deep blue `#183A63`, civic gold `#D6A63A`, warm ivory `#F2E8CF`, and restrained red `#A8443F` for warnings or military accents. Gold is an accent, not a full background, and must retain contrast at UI scale.
- **Silhouette:** clean human infantry and civic architecture with readable vertical standards, bridges, arches, road markers, ledgers, and beacon motifs. Avoid oversized armor, skull imagery, or uncontrolled ornament that would blur the contrast with Brasal clans.
- **Naming voice:** practical, civic, and place-based; prefer compact names that sound like established settlements rather than prophetic titles.

#### Seeded matchup scenario matrix

These deterministic scenario identifiers define the first balance checks; they are design fixtures to run once the Godot simulation exists, not claims that runtime playtests have already passed.

| Scenario | Match setup | Auren route to validate | Viability signal |
|---|---|---|---|
| `AUREN-01-TRAMA-RELAY` | Seed `1101`, Continents, Small, Auren vs Brasal clans | Research Forestry and Engineering, connect the first two cities, then use Public Works for production | Auren can reach a connected two-city network without abandoning a legal defensive response |
| `AUREN-02-CHARTER-EXPANSION` | Seed `1102`, Inland Sea, Medium, Auren vs Brasal clans | Research Agriculture → Scholarship → Civic Charter and use extra claims to secure a third-city corridor | Auren can expand territory and cities without requiring a mirrored or strictly superior start |
| `AUREN-03-CROSSROADS` | Seed `1103`, Archipelago, Medium, Auren vs Brasal clans | Research toward Engineering and Public Works while producing soldiers through the shared roster | Auren can contest or capture an exposed enemy city without a faction-specific combat bonus |

Each scenario must use the standard equal starting package, deterministic tie-breaking, and the approved fairness constraints. Balance testing may adjust the seeds or thresholds, but it must not silently change the identity or formulas above.

### Brasal clans — orcs

**Identity statement:** The Brasal clans are an adaptive frontier society that turns difficult land and organized pressure into momentum. They are the approachable aggression-and-resourcefulness counterpart to Auren: use ordinary infrastructure to sustain the frontier, then choose between stronger field provisioning and a faster basic-soldier response.

**Player-facing promise:** *Make the frontier feed the clan, then decide where the pressure lands.* Brasal rewards deliberate use of Forest and Plains territory plus timely military preparation without creating a second economy engine or making combat automatic.

#### Strategic identity and trade-offs

- The clans' core advantage is conditional tempo: their strongest effects require either productive Forest/Plains territory or a deliberate military research path.
- The clans have no innate unit or building-stat modifier. Settlers, workers, explorers, soldiers, buildings, ports, lumber facilities, production rules, and the shared technology tree remain common unless the accepted technologies below change them.
- The trade-off is dependence on context: Foraging Doctrine has no effect without assigned Forest or Plains tiles, while Warband Tradition arrives through a deeper military path and improves production tempo rather than combat statistics.
- Brasal can pursue peaceful development, infrastructure, or conquest. Its identity is visible through territory and production choices, and Auren can counter it by contesting productive land, disrupting roads, or forcing research trade-offs.

#### Unique technologies

| Technology | Prerequisites | Cost | Exact effect | Formula or system affected |
|---|---|---:|---|---|
| Warband Tradition | Military Training and Metallurgy | 35 RP | Reduces Basic soldier production cost from 12 to 9 production points for Brasal cities | Basic soldier production cost |
| Foraging Doctrine | Agriculture and Medicine | 50 RP | Grants +1 food to every assigned Forest and Plains tile owned by Brasal; the bonus is included before city growth is calculated | Assigned-tile food and city growth |

Warband Tradition does not change Basic soldier attack, defense, health, movement, military-unit limits, or the shared production slot. Foraging Doctrine does not affect unassigned tiles, other terrain, coin income, production, city level thresholds, or enemy-owned territory. Both effects apply only after the technology is completed and remain part of the civilization's authoritative state.

#### City names and naming rules

Cities draw uniformly without replacement from the following initial pool until the pool is exhausted: Brasal, Dargan, Ghorra, Kraz, Morga, Naska, Odrik, Raska, Sarga, Thorga, Uldan, Varka, Vorg, Yagra, and Zorak. Names are assigned when a settler founds a city, cannot be chosen or edited by the player in the initial prototype, and are persisted in saves. If a later pool expansion is needed, new names must follow the same compact, hard-consonant, non-hyphenated naming rule and must not duplicate an existing name.

#### Heraldry and visual language

- **Heraldic mark:** three ascending iron bars beneath an ember-red sun, representing clan continuity, practical craft, and pressure moving forward together.
- **Palette:** charcoal `#24262B`, ember red `#B84A3A`, copper `#C47A44`, weathered bone `#D8C7A2`, and deep moss `#3F5A43` for terrain-linked accents. Red is reserved for active pressure and military emphasis; bone remains an accent, not a skin-tone shorthand.
- **Silhouette:** sturdy, mobile silhouettes with layered hide, practical iron, broad tools, hooked standards, field packs, and modular clan markers. Buildings favor reinforced timber, stone footings, kilns, storehouses, and visible repair work. Avoid generic spikes, skull overload, or visual shorthand that reduces the clans to brute force.
- **Naming voice:** concise, tactile, and clan-rooted; prefer names that sound like places shaped by labor, weather, and remembered agreements rather than random aggressive syllables.

#### Seeded matchup scenario matrix

These deterministic scenario identifiers define the first balance checks; they are design fixtures to run once the Godot simulation exists, not claims that runtime playtests have already passed.

| Scenario | Match setup | Brasal route to validate | Viability signal |
|---|---|---|---|
| `BRASAL-01-FORGE-AND-FIELD` | Seed `1201`, Continents, Small, Brasal vs Auren League | Research Agriculture → Medicine → Foraging Doctrine and develop assigned Forest/Plains tiles | Brasal can pursue a peaceful growth route without requiring conquest or a hidden income source |
| `BRASAL-02-BROKEN-GATE` | Seed `1202`, Inland Sea, Medium, Brasal vs Auren League | Use common roads, ports, and lumber facilities while delaying the unique military path | Brasal can build and maintain infrastructure without losing its identity or needing exclusive buildings |
| `BRASAL-03-WARBAND-PRESSURE` | Seed `1203`, Archipelago, Medium, Brasal vs Auren League | Research Military Training → Metallurgy → Warband Tradition and use the cost reduction to contest a city | Brasal can create conquest pressure while Auren retains readable counterplay through defense, roads, and research choices |

Each scenario must use the standard equal starting package, deterministic tie-breaking, and the approved fairness constraints. Balance testing may adjust the seeds or thresholds, but it must not silently change the identity or formulas above.

## Naming and content policy

Civilization names above are working canon for the prototype and future concepts. City names are drawn randomly from a civilization-specific list when a settler founds a city. No city rename action is planned initially. New lore should reinforce the game's direct, practical tone and should not introduce new gameplay rules without an explicit design decision.
