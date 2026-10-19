# Technical Architecture Proposal

**Status:** proposal for review; not an implemented or fully approved architecture.
**Engine/language:** Godot with GDScript, selected for the initial Android, desktop, and Web targets. Confirm the current stable engine version and export capabilities during project bootstrap; do not assume version-specific behavior without checking the official documentation.

## Constraints

- Ship the same core game to Android, Windows, macOS, Linux, and Web from the start.
- Use 2D graphics, a fixed isometric camera, hex-grid rules, and mandatory landscape orientation.
- Keep simulation rules independent from screen rendering and input device.
- Use seed-driven procedural maps so a saved or reported match can be reproduced.
- Use final-quality visual assets in the prototype, not placeholder art.
- Support manual saves at any time and autosaves after every five complete rounds.

## Proposed layers

| Layer | Responsibility | Must not own |
|---|---|---|
| Domain/simulation | Board, hex coordinates, terrain, units, cities, ownership, economy, turns, combat, research, victory | Scene-tree references, UI state, input-device details |
| Application/use cases | New match setup, validated player commands, AI actions, sequential turn orchestration, save/load coordination | Rendering or raw platform APIs |
| Presentation | Isometric board, selection, fog, animation, HUD, menus, accessible feedback | Authoritative game rules or persistent match truth |
| Content | Civilizations, tech, units, buildings, improvements, terrain, names, balance values | Behavior duplicated as faction-specific branches across scenes |
| Platform adapters | Input mapping, save locations, browser storage, audio and export-specific integration | Gameplay decisions |

### State changes

A recommended command flow is: receive an intent, validate it against the current authoritative state, apply one deterministic transition, emit a result/event for the UI, and save when the round boundary requires it. Rejected commands should leave the game state unchanged. AI should submit the same validated commands as a human so that both use one rules path.

Turn ownership must remain explicit: human turn completes first, then AI civilizations resolve sequentially. Production and research advance once for a civilization at the end of its turn. Autosave is triggered only after every participant has completed the fifth round, not after each individual turn.

## Hex board and map generation

Use one canonical coordinate model for neighbor lookup, distance, movement, range, city claims, and pathfinding. Keep render projection to isometric coordinates in a presentation adapter. The generator receives an explicit seed and configuration. Fairness constraints—minimum separation, start-region comparability, and terrain/resource thresholds—must be specified in testable terms before the generator is considered complete.

Fog-of-war state should distinguish at least unexplored, explored-but-not-currently-visible, and currently visible. Whether remembered enemy structures/units persist in explored fog is still open.

## Content and balance data

Prefer data resources for faction content and tuning values, with shared rules and explicit faction modifiers. Keep formulas in testable code rather than copying near-identical logic into each faction resource. The exact type system, resource schema, and directory layout should be chosen with the first vertical slice, then documented once actual editor constraints are known.

Candidate directory split:

```text
app/          screens, match flow, command orchestration
simulation/   board, entities, rules, transitions
content/      civilizations, terrain, units, structures, technologies
presentation/ isometric rendering, fog, effects, UI
platform/     input, persistence, export adapters
assets/       final visual/audio resources, licensed source files
 tests/       deterministic rule and integration tests
```

This is an initial organization proposal, not a requirement to adopt these exact names.

## Persistence

A save should use a versioned, checksummed model-level JSON envelope containing match configuration, map seed and deterministic random-state, full authoritative board/entity state, active civilization/round, production/research progress, completed technologies, and fog/visibility state needed to resume. Do not serialize scene nodes. Use atomic temporary-file replacement, explicit sequential migrations, three manual slots, one autosave, and one previous-autosave backup. Validate checksums and invariants before load; preserve the original slot on any failure. Use Godot's `user://` abstraction for desktop, Android, and Web persistence. Test manual round trips, corrupted and unsupported saves, migration, manual-slot preservation, and autosave boundaries after all AI turns.

## Input and display

Separate player intents from input hardware so touch, mouse, keyboard, and controller adapters emit the same validated actions. Keep selection, preview, confirmation, cancellation, and focus navigation in the application/presentation boundary; only the simulation applies authoritative transitions. Design for landscape layouts, safe areas, readable hex selection, visible focus, 48 logical-pixel minimum targets, and the documented UI-scale presets. Persist no input-device-specific gameplay state.

## AI boundary

The AI receives the same visible information and legal actions as a human. Difficulty is selected before the match and remains fixed; its explicit differences are starting coins and planning horizon as defined in the Game Design Document. Avoid difficulty modifiers that secretly change rules mid-match. AI decisions must pass through the same validated command path as human actions.

## Cross-platform validation

- Verify export and launch on Android, Windows, macOS, Linux, and supported Web browsers.
- Test landscape orientation, input parity, UI scaling, save persistence, memory, loading, and a complete match per target family.
- Run deterministic tests for hex geometry, legal movement, turns, city ownership, growth, production/research progress, combat, and victory.
- Use fixed seeds for regression tests; record failing seeds in test output.
- Do not mark a platform complete based only on successful editor execution or a successful export build.

## Technical questions still open

Godot version, renderer selection, GDScript static typing policy, folder names, test framework, minimum device/browser versions, performance budgets, save schema/migration guarantees, localization tooling, asset import settings, build automation, code signing, and release pipeline remain for project bootstrap and technical spikes.
