# Technical Architecture Proposal

**Status:** proposal for review; engine, renderer, repository location, and the issue #20 project/data boundaries below are approved. Unlisted architecture choices remain open.
**Engine/language:** Godot 4.7.2 stable (`4.7.2.stable.official.ed1daf0bf`) with GDScript, using the Compatibility renderer. Pin this version for project bootstrap; evaluate later stable upgrades through an explicit issue and export/runtime checks rather than upgrading automatically.

## Constraints

- Ship the same core game to Android, Windows, macOS, Linux, and Web from the start.
- Keep the complete Godot project in this GitHub repository at `game/`; no separate project repository is planned.
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

The canonical content boundary is defined in the [GDD prototype content contract](../game-design/game-design-document.md#17-prototype-content-contract). Prefer data resources for the two civilization definitions and their content references, with shared rules and explicit faction modifiers. The initial contract contains five shared unit records, four shared building records, five shared improvement/road records, twelve shared technology records, two Auren technology records, and two Brasal technology records. The technology ratio is measured by node count: 12/16 shared equals 75%, accepted within the 75–85% tolerance around the 80% target.

Keep formulas in testable code rather than copying near-identical logic into each faction resource. Every content entry needs a stable ID, display/name data, prerequisites, cost or base stats where applicable, affected formula, timing, scope, and stacking behavior. Civilization-specific entries may reference shared entries and explicit modifiers, but scenes must not contain faction branches that duplicate rule behavior. The first vertical slice must load both civilization definitions and exercise at least one shared and one unique technology for each faction through the same production, research, AI, and save/load paths. Unique units, unique buildings, faction-specific base stats, extra economy resources, and new technology nodes are deferred by the contract and require a new design decision.

The [Balance Methodology and Scenario Catalog](../game-design/balance-methodology.md) owns scenario IDs, fixed seeds, metric definitions, initial tolerances, evidence status, and rerun scope. Content data owns tunable values; simulation code owns formulas and validation; scenario records own reproducible evidence. A tuning change must not introduce a second source of truth or alter a persisted content ID without the corresponding save-schema assessment.

Approved Godot project structure (issue #20):

```text
game/
  project.godot
  app/                 match setup, use cases, command orchestration
  simulation/          deterministic model, commands, rules, events, results
  content/             typed definitions, stable-ID catalog, authored resources
    resources/         civilization and terrain resource schemas
    data/              civilization and terrain .tres definitions
  presentation/        isometric projection, scenes, UI, effects, fog display
  platform/            input, persistence, export and platform adapters
  assets/              final-quality source and imported game assets
  tests/               deterministic model, content-contract, integration tests
```

Simulation and its model types are plain GDScript data objects (using `RefCounted` where runtime identity/lifetime is needed), never scene nodes. `HexCoord(q, r)` is the canonical axial coordinate model; isometric projection is presentation-only. Commands from human and AI adapters converge on one application validation path. Rejection must preserve authoritative state. Content references crossing runtime or save boundaries use stable IDs, never resource paths, display names, scene names, or list positions. See [Godot project structure and data contract](godot-project-structure.md) for the module dependency rules, type dictionary, and currently implemented content resources.

Content `.tres` resources own authored identity, names, references, and tunable values. Testable simulation code owns formulas, legality, transitions, and modifier application. This issue establishes schema boundaries and representative content only; it does not implement the game systems or claim the complete vertical-slice catalog has been authored.

## Persistence

A save should use a versioned, checksummed model-level JSON envelope containing match configuration, map seed and deterministic random-state, full authoritative board/entity state, active civilization/round, production/research progress, completed technologies, and fog/visibility state needed to resume. Do not serialize scene nodes. Use atomic temporary-file replacement, explicit sequential migrations, three manual slots, one autosave, and one previous-autosave backup. Validate checksums and invariants before load; preserve the original slot on any failure. Use Godot's `user://` abstraction for desktop, Android, and Web persistence. Test manual round trips, corrupted and unsupported saves, migration, manual-slot preservation, and autosave boundaries after all AI turns.

## Input and display

Separate player intents from input hardware so touch, mouse, keyboard, and controller adapters emit the same validated actions. Keep selection, preview, confirmation, cancellation, and focus navigation in the application/presentation boundary; only the simulation applies authoritative transitions. Design for landscape layouts, safe areas, readable hex selection, visible focus, 48 logical-pixel minimum targets, and the documented UI-scale presets. Follow the GDD's WCAG 2.2 AA-informed contrast, minimum text size, redundant feedback, reduced-motion, and scoped screen-reader requirements; preserve essential actions at 200% scaling. Keep player-facing text behind stable localization keys, with English source strings, English/Spanish prototype catalogs, English fallback, and layouts tested for 30% ordinary-text and 35% control-text expansion. Persist no input-device-specific gameplay state.

## AI boundary

The AI receives the same visible information and legal actions as a human. Difficulty is selected before the match and remains fixed; its explicit differences are starting coins and planning horizon as defined in the Game Design Document. Avoid difficulty modifiers that secretly change rules mid-match. AI decisions must pass through the same validated command path as human actions.

## Cross-platform validation

- Compatibility is selected because Web requires this renderer and the 2D game benefits from its broad hardware reach. Godot's Web export requires WebAssembly and WebGL 2.0 support.
- **Initial supported platform floor (issue #24):** use Godot 4.7's published minimum requirements for exported projects as the compatibility starting point, not as a performance guarantee.

  | Target | Initial operating-system/browser floor | Compatibility requirement |
  |---|---|---|
  | Windows | Windows 10 or newer | Compatibility renderer; OpenGL 3.3 or Direct3D 11 |
  | macOS | macOS 11 or newer on Intel; macOS 13 or newer on Apple silicon | Compatibility renderer; OpenGL 3.3 |
  | Linux | Distributions released after 2018 | Compatibility renderer; OpenGL 3.3 |
  | Android | Android 7.0 or newer | Compatibility renderer; OpenGL ES 3.0 |
  | Web | Two latest stable releases of Chrome, Edge, and Firefox | WebAssembly and WebGL 2.0 |

  Safari/WebKit and iOS are outside the initial guaranteed target matrix. Godot's CPU references are x86-32 with SSE2, x86_64 with SSE4.2, or ARMv8 for Windows; x86-32 with SSE2, x86_64 with SSE4.2, or ARMv7/ARMv8 for Linux; x86_64 or ARM for macOS; and 32/64-bit ARM or x86 for Android. Its published minimum RAM references for simple exports are 2 GB for native desktop, 1 GB for native mobile, 4 GB for desktop Web, and 2 GB for mobile Web. These are engine references only; representative Vaelora devices and actual minimum hardware remain subject to Stage 2 measurements. Reassess the OS/browser floors only through an explicit decision and validation evidence.
- Godot warns that CPU, GPU, memory, and storage needs vary with project scope. Vaelora's final-quality assets, 80 × 50 maps, and simulation workload must therefore be measured on representative devices at the selected floor before claiming supported performance. The engine's baseline does not itself establish Vaelora compatibility.
- The game uses landscape orientation. Human and AI input continue through the same validated action path; issue #20 will define the initial Godot input map as part of project bootstrap.
- This decision does not freeze texture filtering, compression, or per-asset import presets. Set those after the visual asset requirements and supported platform matrix are established; do not infer them from the smoke project's temporary export settings.
- Keep exports available for Android, Windows, macOS, Linux, and Web. Prioritize Web and Android runtime validation during bootstrap: verify Web launch in a supported browser and produce an Android APK; validate Android installation/runtime when the Android Studio/device test setup is ready.
- Produce Windows, macOS, and Linux exports during the engine feasibility decision. Their native runtime checks follow when packaged builds are available and are not blockers for resolving issue #19. These checks remain part of the later vertical-slice platform gate.
- Test landscape orientation, input parity, UI scaling, save persistence, memory, loading, and a complete match per target family.
- During the Stage 2 vertical slice, select and record representative minimum-spec devices for Android, Windows, macOS, and Linux, plus browser/OS combinations for Web. Measure startup and load time, generation time for the largest map, full-turn and AI response time, frame time, peak memory, and save size. Set numerical budgets from those measurements and approve them before the vertical-slice gate closes; until then, report them as pending rather than inventing thresholds.
- Run the GDD §13 `ACC-*` and `LOC-*` acceptance checks on Android, Windows, macOS, Linux, and supported Web browsers; record actual accessibility API support and platform-specific gaps.
- Run deterministic tests for hex geometry, legal movement, turns, city ownership, growth, production/research progress, combat, and victory.
- Use fixed seeds for regression tests; record failing seeds in test output.
- Do not mark a platform complete based only on successful editor execution or a successful export build.

## Technical questions still open

GDScript static typing policy, measured numerical performance budgets, save schema/migration guarantees, localization tooling, asset import settings, build automation, code signing, and release pipeline remain for project bootstrap and technical spikes. Issue #24 selects the initial platform floor and browser matrix; its numerical budgets must be established from representative vertical-slice measurements before that gate closes. GUT 9.7.1 is selected in issue #21; its test boundaries and commands are documented in the [automated testing strategy](testing-strategy.md).

The selected engine and renderer are recorded in [Open Decisions — Godot engine and renderer](../game-design/open-decisions.md#godot-engine-and-renderer--issue-19). The project directory and data boundaries are recorded in [Godot project structure and data contract](godot-project-structure.md) (issue #20).
