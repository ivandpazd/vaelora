# Vaelora — Technical Architecture Proposal

**Status:** Proposal for review, not an implemented or fully approved architecture.
**Target engine/language:** Godot with GDScript, as selected by the user. Confirm the stable engine release and export support when the repository is initialized for implementation; do not rely on an unverified version string in this document.

## Targets and non-negotiable constraints

| Target | Constraint |
|---|---|
| Android | Landscape-only, touch-first interaction, mobile performance and save storage |
| Windows, macOS, Linux | Landscape presentation; mouse/keyboard support |
| Web | Browser export from the beginning; test memory, input, persistence, and load behavior in supported browsers |

The game is 2D, fixed-isometric, hex-based, single-player/local versus AI at first. Art assets must be production-quality from the prototype. Cross-platform behavior is a release requirement, not a later port.

## Recommended boundaries

Keep rules and state separate from rendering so the same game logic can run under desktop, mobile, and browser input. Treat this as a proposed organization to validate against the first vertical slice:

- **Domain/simulation:** board, hex coordinates, terrain, units, cities, ownership, technology, turns, combat, economy, victory, and deterministic resolution.
- **Application flow:** new-game setup, player commands, turn sequencing, AI turn requests, save/load orchestration, and event/result presentation.
- **Presentation:** isometric board rendering, fog/visibility overlays, selection, animation, HUD, menus, and platform-specific input adapters.
- **Content data:** civilization definitions, terrain, units, buildings, improvements, technologies, balance values, and localized text as data resources rather than rule branches scattered through scenes.
- **Platform services:** save paths, browser persistence, audio, input, and export-specific behavior behind narrow adapters.

Prefer command validation followed by a single authoritative state transition. Keep simulation decisions deterministic where possible and seed procedural generation explicitly. This supports reproducible bugs and saved games. AI should issue the same validated commands available to a human rather than mutate the board through a separate rules path.

## Scene and data organization (proposed)

Use scenes for screens and visual composition, not as the sole source of game truth. Keep model state in typed GDScript objects/resources or another measured Godot-native representation; avoid coupling saved state to ephemeral node paths. A candidate top-level separation is `app/`, `game/`, `ui/`, `content/`, `platform/`, and `tests/`. Final directory layout should follow the first vertical slice and editor constraints.

A save should contain a schema/version marker, match settings, random seed, round/active-turn state, and all authoritative state needed to resume deterministically. This is a recommendation; save format, migration policy, and compatibility guarantees require approval before they become implementation contracts.

## Test and validation approach

- Unit-test deterministic rules: hex distance/neighbors, legal movement, turn transitions, production/research advancement, combat results, city ownership/claims, and victory checks.
- Use seeded generation tests to check constraints such as separation and broadly comparable starts; exact thresholds must be specified first.
- Test save/load round trips and autosave only after complete rounds.
- Run the same gameplay acceptance scenarios on Android, Windows, macOS, Linux, and supported Web browsers before calling the prototype complete.
- Keep presentation tests focused on landscape layout, isometric readability, fog, touch/mouse parity, and UI scaling.

No implementation should begin until the open design values in the GDD that affect data contracts and testing have owners and acceptance criteria.
