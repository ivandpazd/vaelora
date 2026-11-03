# Terrain assets

Source/output area for the nine canonical gameplay terrain categories, the ten-family [Terrain Visual Language v1](../../../docs/game-design/TERRAIN_VISUAL_LANGUAGE_V1.md) review suite, the finite modular shoreline library, and neutral environment components. The ten visual families do not add Desert or Snow to the initial gameplay rules.

Coast runtime contract: three shoreline morphologies × two authored variants × six world directions = 36 reusable edge overlays. There are no visible corner-resolver sprites.

Do not bake gameplay overlays, territory, fog, cities, units, roads or improvements into terrain bases.

The `generated-terrain-suite-v62/review/` files are source-context review evidence, not accepted `final_2x` runtime sprites. Accepted terrain must preserve exact hex registration and pass repetition/context tests from the Quality Gate, including the fixed-seed coast stress scene and real Godot runtime-composition evidence.
