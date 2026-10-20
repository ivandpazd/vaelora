# Godot Project Structure and Data Contract

**Status:** approved for the Stage 2 project foundation by issue #20. This establishes ownership and data boundaries; it does not claim that gameplay systems, production content, or platform support are implemented.

## Project map

The complete Godot project lives at `game/` in this repository. Godot 4.7.2 stable and the Compatibility renderer are pinned by the approved issue #19 decision.

| Directory | Owns | Must not own |
|---|---|---|
| `game/app/` | Match setup, use cases, orchestration, conversion of player/AI intent into validated commands | Rules, rendering, raw device/platform APIs |
| `game/simulation/` | Authoritative board and entity state, deterministic rules/transitions, command validation, events and results | Scene nodes, UI state, input hardware, platform APIs |
| `game/content/` | Typed content schemas, stable-ID catalog, authored civilization/terrain/gameplay definitions | Rule formulas or presentation-specific faction branches |
| `game/presentation/` | Scenes, isometric projection, visible fog, animation, UI and accessible feedback | Authoritative game state or rule decisions |
| `game/platform/` | Input mapping, persistence backends, export and platform adapters | Gameplay semantics or a parallel validation path |
| `game/assets/` | Final-quality game assets and licensed editable sources | Placeholder production visuals |
| `game/tests/` | Deterministic content/model tests and integration checks | A second implementation of gameplay rules |

Runtime domain/model objects are not Nodes and do not depend on the scene tree. Use `RefCounted` for runtime objects requiring identity or managed lifetime; immutable/value-like types may use the smallest suitable GDScript value representation. The initial contract deliberately does not define a test framework or save envelope; those remain owned by issues #21 and #23 respectively.

## Dependency and state-flow rules

```text
platform input ──> app intent/use case ──> simulation validation/transition
AI planner ────────────────────────────> app intent/use case ──> simulation
simulation result/event ──> app/presentation feedback
content resources ──> app/simulation (resolved by stable ID)
platform persistence <── app/model serialization boundary
presentation projects canonical hex coordinates into isometric screen coordinates
```

- Simulation may depend on domain-safe content definitions/catalogs; it must not import `Node`, scenes, rendering, input adapters, or platform APIs.
- Human and AI intents pass through the same validation and transition path.
- A rejected command emits a result and leaves authoritative state unchanged.
- Hex rules use axial `(q, r)` coordinates. Isometric projection and screen coordinates are presentation concerns only.
- Content identity is a lowercase, dot-namespaced stable ID such as `terrain.meadow` or `technology.civic_charter`. IDs are not derived from localized/display text, resource paths, scene names, or ordering.
- Resources describe content and explicit references; simulation code owns formulas, legality, ordering, and state transitions. No faction-specific rule branches belong in scenes.
- Model persistence is a separate boundary. Saves persist IDs and model state, never serialized scene nodes. Versioning, checksum, migration, and slot semantics remain in issue #23 and the approved save contract.

## Data dictionary

| Concept | Authoritative representation | Identity/ownership and references |
|---|---|---|
| Content definition | Godot `Resource` subclass; designer-authored `.tres` | Required stable `id` and `display_name`; references use content IDs |
| Civilization | `CivilizationDefinition` resource | Stable civilization ID; shared unit/building/improvement/technology ID lists; unique technology IDs; canonical name pool; identity, heraldry, palette, silhouette, and naming-voice data |
| Terrain | `TerrainDefinition` resource | Stable terrain ID; movement domain/cost, base food/production/coin yields, defense, vision, line-of-sight, workable-territory flag, legal improvement IDs and road eligibility |
| Board | Simulation model collection keyed/indexed by canonical `HexCoord(q, r)` | Tiles have one coordinate and a terrain content ID; rendering never becomes board authority |
| Tile | Simulation model state | Terrain ID, optional city owner/city ID, optional non-road improvement ID, road feature, and other rule-owned tile state; at most one city owns a tile |
| Unit | Simulation entity state | Stable match-local entity ID, owning civilization ID, unit definition ID, axial position, and rule state; unit stats/action legality resolve from shared definitions and explicit effects |
| City | Simulation entity state | Stable match-local entity ID, owning civilization ID, tile coordinate, assigned tile coordinates, level/growth, production and research progress, and chosen name from its civilization pool |
| Command/intent | Immutable-by-convention input value plus actor/civilization ID | Identifies requested action and stable entity/content references; both human and AI use the same validator |
| Event/result | Simulation output value | Reports accepted/rejected outcome and deterministic state-change information; UI text is adapted outside simulation |
| Technology/modifier | Content definition referenced by stable ID | Prerequisites, cost, affected formula, timing, scope, stacking, and explicit effect follow GDD §17; formulas remain in tested simulation code |
| Tuning value | Authored content/config data with a single owner | Numeric data does not duplicate formulas; balance scenarios and tolerances remain in the balance catalog |
| Save model | Versioned model-level persistence contract (issue #23) | Stores civilization/content/completed-technology IDs and modifier-relevant authoritative state; excludes Nodes and display-order inference |

This dictionary assigns ownership, not unapproved field-level gameplay rules. Existing GDD/open-decision values remain authoritative; unresolved behavior must remain an explicit decision rather than be inferred from the schema.

## Initial content-resource examples

The initial project contains representative data resources for Auren League, Brasal clans, and Meadow. Civilization resources carry the approved common content ID lists, their own two unique technology IDs, the exact city-name pool, and the canonical identity/heraldry/palette/silhouette/naming-voice information. The Meadow resource reflects GDD §4: land movement cost 1, yields 2/0/0, no defense or vision bonus, workable territory, farm legality, and road eligibility. These references document the full prototype catalog contract; they do not imply those referenced unit/building/improvement/technology definitions are all implemented yet.

## Deferred decisions and boundaries

- Issue #21 selects the project test runner/framework.
- Issue #23 defines the save format, schema versioning, checksum, migration, and slot guarantees.
- Issue #24 owns minimum platform/browser versions and performance budgets.
- Issue #20 does not create gameplay systems, final art/audio, input mappings, export automation, or platform compatibility claims.
- Any change to persisted content IDs requires save-schema impact assessment. Unique units/buildings, faction base-stat changes, extra economy resources, additional civilizations, and technology-boundary changes remain deferred by GDD §17.
