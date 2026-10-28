# Automated Testing Strategy

**Status:** approved runner and initial test boundary for Stage 2, selected under issue #21. This document does not define or implement gameplay rules.

## Runner

Use GUT 9.7.1, vendored at `game/addons/gut/`, for GDScript tests. The project uses Godot 4.7.2; GUT 9.7.1 documents support for Godot 4.7.x. A minimal probe on Godot 4.7.2 confirmed that a passing assertion exits with status `0`, while an intentional assertion failure prints the assertion message and exits with status `1`.

Run the full headless suite from the repository root:

```sh
godot --headless --path game --script res://addons/gut/gut_cmdln.gd -gdir=res://tests -gpost_run_script=res://tests/require_tests_hook.gd -gexit
```

Run one suite while iterating:

```sh
godot --headless --path game --script res://addons/gut/gut_cmdln.gd -gtest=res://tests/test_content_contract.gd -gpost_run_script=res://tests/require_tests_hook.gd -gexit
```

The same full-suite command is the future CI test step. CI must install the documented Godot version, run the command from the checkout root, preserve the process exit status, and retain the complete failure output. The post-run hook turns GUT's otherwise-successful zero-test run into an actionable failure. Do not report success based on an editor launch or a test run that reports `Nothing was run`.

## Test categories and ownership

| Category | Scope and boundary | Evidence / source contract |
|---|---|---|
| Content and model unit tests | Validate resource schemas, stable IDs, formulas, and small deterministic model operations without scenes. | Current `game/tests/test_content_contract.gd`; data rules in the GDD and `game/content/`. |
| Simulation tests | Exercise implemented map generation, command validation, combat, turn transitions, and other authoritative rules through their public simulation interfaces. Use fixed seeds and assert returned outcomes plus state preservation after rejected commands. | Gameplay systems are not implemented yet. Add these tests alongside or after those systems; regression suite tracked by issue #55. GDD §§3–12 and accepted decisions apply. |
| Integration tests | Exercise app/use-case orchestration through the same validated command path used by human and AI intents, without making the scene tree authoritative. | Add when the app and simulation boundaries have runnable implementations; GDD core loop and the accepted architecture boundary apply. |
| UI and interaction checks | Verify scene behavior, navigation, accessible feedback, localization, and input-device flows. Use GUT where an automated scene check is meaningful; retain manual scenarios for real device/input behavior. | GDD §13 `ACC-01`–`ACC-07` and `LOC-01`–`LOC-04`; record target platform, build, steps, and result. |
| Save and migration tests | Verify exact round-trip state, SHA-256 envelope checksums, current-plus-two-previous compatibility, every sequential migration through the public load path, rejected future/out-of-window/corrupt inputs, manual overwrite confirmation, atomic replacement, and preservation of both original bytes and active match on failure. Exercise autosave/backup rotation only from a valid autosave. | Issue #23 owns the accepted save contract; implement these deterministic checks at the model persistence boundary. Add packaged-target scenarios for actual `user://` storage and Web storage failures. |
| Platform smoke tests | Launch and exercise packaged builds on each target family; an editor or headless run is not platform coverage. | Production plan Stage 2 and Stage 4 gates; GDD §13 checks and platform limitations are recorded per target. |

## Determinism, fixtures, and snapshots

- Every randomized simulation test supplies an explicit, named seed and records its inputs. A failure report must include the seed, scenario, and relevant command sequence so the case can be rerun.
- Authored game content remains under `game/content/data/`; tests reference it rather than copying it into test fixtures.
- Isolated test setup belongs under `game/tests/fixtures/<domain>/`. Fixtures are test-owned, reviewed with the behavior they cover, and changed only when the accepted contract or intended scenario changes.
- Keep expected values small and explicit in tests. A serialized snapshot may be checked in only when its schema and ownership are documented; update it deliberately with the related contract/test change, never by automatic regeneration after a failure.
- Do not add guessed expected results for unimplemented or unresolved gameplay rules. Their tests wait for the system implementation and accepted design contract.

## Failure and CI policy

- Assertions identify the violated contract and include useful expected/actual values.
- A test failure, zero-test run, or engine/script error must leave a non-zero process status. The required post-run hook rejects zero tests; do not suppress runner errors with `-gerrors_do_not_cause_failure`.
- CI should use the same headless invocation as local development and should preserve console output. Platform, UI input, save-location, and export checks remain separate evidence rather than being inferred from this command.
- Keep generated output and caches outside versioned test fixtures. Do not commit editor caches, test logs, or generated result files.

## Current coverage and deferred work

The current suite covers the content-resource contract and stable-ID catalog behavior. There are no gameplay simulation scripts on the Stage 2 foundation base yet, so terrain generation, commands, combat, and turn-transition regression tests are intentionally deferred to issue #55. Issue #23 now specifies save/migration coverage, which is added alongside the persistence implementation rather than by introducing a production save system during design lock. The final prototype test battery remains the Stage 4 production gate.
