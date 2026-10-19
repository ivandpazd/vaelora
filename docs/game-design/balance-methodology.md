# Balance Methodology and Scenario Catalog

This document defines how Vaelora balance is evaluated before and during implementation. It makes tuning reproducible: every conclusion names a fixed seed, setup, observation window, metric, tolerance, evidence status, and affected data.

## Decision summary

Vaelora uses a **hybrid balance process**:

1. **Deterministic scenario catalog:** fixed seeds and setups cover the principal strategic systems.
2. **Manual scenario review:** designers inspect player-facing choices, counterplay, readability, and illegal or surprising outcomes.
3. **Deterministic simulation batches:** once the simulation runner exists, repeated runs produce comparable metrics from the same seed and configuration.
4. **AI-vs-AI sampling:** a supplemental signal for matchup and victory diversity; it never replaces manual review or player-versus-AI checks.

The catalog is a measurement tool, not a promise that every scenario has already passed. A scenario is **not run**, **passed**, **failed**, or **blocked**; undocumented results are never treated as balance evidence.

## Evidence and change thresholds

### Required evidence for a tuning change

A balance change must include:

- the exact content-data IDs or formula changed;
- the scenario IDs and seeds rerun;
- before/after metric values and the relevant tolerance;
- a short explanation of the player-facing problem;
- the observed counterplay and any new regression risk.

No balance value is changed only because it feels wrong in one unseeded match or because one faction wins one run.

### Initial tolerance policy

These are initial prototype tolerances, not hidden guarantees:

| Metric | Initial tolerance or target | Interpretation |
|---|---:|---|
| Starting opportunity score | ≤15% difference | Existing fairness rule for comparable starting regions |
| Time to first additional city | 8–20 turns in standard Small/Medium openings | A faction outside the range needs explanation or tuning; starting city founding is excluded |
| City level 2 timing | 8–20 completed city turns after founding | Measures early growth without rewarding a single unusually rich tile |
| First shared technology | 5–14 civilization turns | Measures research access without forcing one technology order |
| First unique technology | 20–50 civilization turns | Measures whether identity is reachable without making it automatic |
| Basic soldier production | 4–10 city turns from an idle level-1 city with baseline production | Uses the shared cost and exposes faction-specific production effects |
| Equivalent faction matchup win share | 40–60% over a paired sample | A wider result is a signal for investigation, not an automatic balance failure |
| Victory diversity | No victory route above 70% in a mixed catalog sample | Prevents one route from dominating the initial ruleset |
| Road-network connectivity | First two-city connection by turn 12–30 when the scenario supplies a legal corridor | Measures infrastructure viability without requiring every map to be road-optimal |

Ranges are evaluated per scenario setup and difficulty. They are not averaged across incompatible map sizes or victory modes. A result outside a range becomes a **balance signal**; it becomes a blocking failure only when the scenario's expected observation or a regression invariant is violated.

## Scenario record format

Every catalog entry must record:

| Field | Requirement |
|---|---|
| Scenario ID | Stable uppercase identifier; never reuse an ID for a different setup |
| Seed | Fixed integer seed; changing it creates a new revision and preserves the old result |
| Setup | Map type, size, factions, difficulty, match type, and starting configuration |
| Focus | The system or interaction being evaluated |
| Expected observations | Player-facing choices and counterplay that must remain available |
| Metrics | Named measurements and their collection window |
| Tolerance | The applicable initial range or invariant |
| Evidence status | Not run, passed, failed, or blocked, with build and date when run |
| Owner | The person responsible for interpreting the result and approving a tuning proposal |

## Initial scenario catalog

The following eight scenarios cover the initial balance surface. They are design fixtures until the deterministic runner exists.

| ID | Seed and setup | Focus | Expected observations and metrics | Tolerance |
|---|---|---|---|---|
| `BAL-01-OPENING` | Seed `1401`; Continents, Small; Auren League vs Brasal clans; Intermediate; Turn limit | Opening and first expansion | Found the starting city, explore, choose an early technology, and found the first additional city; record first-city, level-2, first-tech, and first-soldier timings | Opening ranges above; no faction-specific route is mandatory |
| `BAL-02-EXPANSION` | Seed `1402`; Inland Sea, Medium; both factions in both player orders; Intermediate; Turn limit | Territory and city growth | Compare claim legality, city count, level progression, assigned food, and peaceful expansion; record city and level timing by faction/order | Equal starting package; no player order exceeds the paired timing tolerance by more than 3 turns |
| `BAL-03-TRAMA-NETWORK` | Seed `1403`; Continents, Medium; both factions; Intermediate; Turn limit | Roads and connected-city economy | Build a legal two-city road network, measure connection timing, route bonuses, Public Works, worker uses, and disruption recovery | Connection by turns 12–30 when corridor is legal; route bonus never exceeds +50% |
| `BAL-04-SEAWAY` | Seed `1404`; Archipelago, Medium; both factions; Intermediate; Combined | Naval transport and ports | Research Seamanship, build a Port and Patrol ship, embark and disembark each core unit legally, and test naval pressure without a naval-only victory | No illegal sea transition; naval access must not make a faction's ordinary land route irrelevant |
| `BAL-05-FRONTIER-COMBAT` | Seed `1405`; Continents, Small; both factions; Hard AI; Total conquest | Combat, city capture, and counterplay | Compare Basic soldier production, terrain defense, Walls, retaliation, city capture, and last-city pressure | Equivalent matchup win share 40–60% in paired samples; no hidden faction combat bonus |
| `BAL-06-KNOWLEDGE` | Seed `1406`; Inland Sea, Medium; both factions; Intermediate; Knowledge | Research pacing and unique technology access | Reach shared and unique technologies, record research generation, acceleration use, prerequisites, and knowledge-victory timing | First shared tech 5–14 turns; first unique tech 20–50 turns; no faction is locked out of the tree |
| `BAL-07-AUREN-BRASAL-IDENTITY` | Seed `1407`; Continents, Medium; Auren League vs Brasal clans; both player orders; Intermediate; Combined | Civilization identity and matchup health | Exercise Civic Charter, Public Works, Warband Tradition, and Foraging Doctrine; compare peaceful, infrastructure, and conquest routes | Each faction has at least one viable route; no single route exceeds 70% in the mixed sample |
| `BAL-08-ENDGAME` | Seed `1408`; Continents, Large; both factions; Hard AI; Turn limit | Late-game pacing and victory diversity | Reach high city levels, complete networks, use remaining technologies, contest cities, and finish by score or another valid route | No stalled production/research loop; victory routes remain available and score tie-breakers are deterministic |

The Auren and Brasal identity fixtures in `world-and-civilizations.md` remain narrative/content fixtures. The `BAL-*` catalog is the authoritative balance suite; a tuning change affecting a faction must rerun `BAL-07` plus every other scenario whose focus uses the changed content.

## Tuning data ownership

- Numeric values belong in versioned content or tuning data, not duplicated scene constants or unexplained rule branches.
- The GDD owns the rule meaning and formula. Content data owns the value. The simulation owns calculation and validation. The scenario catalog owns evidence requirements.
- A balance proposal must identify the data owner, affected formula, dependent scenarios, and rollback value.
- A design/documentation PR may define or clarify a value; implementation PRs must not silently change a documented value without updating the canonical design record.
- Save compatibility is part of the review whenever a content ID, persisted value, or schema interpretation changes.

## Regression policy

| Change scope | Required rerun |
|---|---|
| One faction value, unique technology, or faction presentation value | `BAL-07` plus every scenario naming the affected content; rerun both player orders |
| Shared unit, building, improvement, technology, or formula | Full `BAL-01`–`BAL-08` catalog, both factions, and all applicable difficulties |
| Map generation, fairness threshold, terrain yield, or movement rule | Full catalog with the changed seed fixtures plus the fairness suite; preserve old seeds for comparison |
| AI policy, difficulty, victory, score, save, or turn-resolution rule | Full catalog, paired AI-vs-AI sample, and persistence/regression checks |
| Scenario setup or seed replacement | Preserve the old scenario record and result; introduce a new revision with a new ID or explicit revision suffix |

A failed or blocked rerun prevents the affected tuning change from being considered complete. A passed rerun records the build, seed, configuration, metric output, and reviewer in the implementation PR.
