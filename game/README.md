# Vaelora Godot Project

This is the complete game project, kept in the repository under `game/`. It targets the approved Godot 4.7.2 stable build and Compatibility renderer.

Module ownership, the domain data dictionary, and dependency rules are documented in [`../docs/technical/godot-project-structure.md`](../docs/technical/godot-project-structure.md). The project is a foundation only: gameplay systems, scenes, input maps, export automation, and final assets are not claimed complete.

The GUT 9.7.1 test runner and test boundaries are documented in [`../docs/technical/testing-strategy.md`](../docs/technical/testing-strategy.md). Run the headless suite from the repository root with:

```sh
godot --headless --path game --script res://addons/gut/gut_cmdln.gd -gdir=res://tests -gpost_run_script=res://tests/require_tests_hook.gd -gexit
```
