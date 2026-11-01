# Issue #17 Visual Slice — Candidate

**Status:** Blender-authored review candidate; not accepted production art. The project owner must review and accept the slice before issue #17 closes or downstream production treats it as approved.

## Source and provenance

- `create_visual_slice.py` is the editable, deterministic Blender Python source.
- `issue_17_visual_slice.blend` is the native editable Blender review scene, including the low-poly terrain, city, unit, camera, and material models used for the renders.
- All geometry, materials, and renders are original Vaelora project work. No external models, textures, fonts, or audio are used.
- The supplied Vaelora key art and canon faction briefs inform the candidate; no source image is traced or embedded.
- The user-selected Polytopia reference is limited to general low-poly faceting, isometric readability, and small-screen hierarchy. No Polytopia geometry, textures, characters, faction identifiers, or compositions are copied. Context: [Sifted interview with Felix Ekenstam](https://sifted.eu/articles/elon-musk-polytopia-video-game) and [official Polytopia game graphics page](https://polytopia.io/game-graphics); these do not document the exact production pipeline.
- The installed Blender build used for this candidate is 5.4.0 Alpha. Re-render with that build for byte-consistent output; do not treat this as the project's approved Blender version.

## Candidate outputs

| Asset | Dimensions | Role |
|---|---:|---|
| `terrain_meadow_2x.png` | 256 × 128 | Flowering Meadow |
| `terrain_plains_2x.png` | 256 × 128 | Shared Plains tile |
| `terrain_forest_2x.png` | 256 × 128 | Dense, broad-crown Forest |
| `terrain_hills_2x.png` | 256 × 128 | Rolling Hills |
| `terrain_mountain_2x.png` | 256 × 128 | Traversable Mountain |
| `terrain_coast_2x.png` | 256 × 128 | Land-and-water Coast boundary |
| `terrain_shallow_sea_2x.png` | 256 × 128 | Shallow sea |
| `terrain_open_sea_2x.png` | 256 × 128 | Open sea |
| `terrain_peak_2x.png` | 256 × 128 | High, snow-capped inaccessible Peak |
| `city_auren_level_3_4_2x.png` | 512 × 256 | Auren civic city stage |
| `city_brasal_level_3_4_2x.png` | 512 × 256 | Brasal frontier city stage |
| `unit_auren_basic_soldier_2x.png` | 256 × 128 | Auren Basic soldier, one review facing |
| `unit_brasal_basic_soldier_2x.png` | 256 × 128 | Brasal Basic soldier, one review facing |
| `review_slice_75.png` | 720 × 540 | Compact 4 × 4 landscape at 75% zoom |
| `review_slice_100.png` | 720 × 540 | Compact 4 × 4 landscape at 100% zoom |
| `review_slice_125.png` | 720 × 540 | Compact 4 × 4 landscape at 125% zoom |

The terrain catalogue follows the nine categories in GDD §4; terrain is distinguished by silhouette, luminance, and material texture as well as hue. Coast includes a land/water transition, Forest occupies a full cell, and Peak has a distinct high summit without adding gameplay rules. Cities/units remain focal assets in the landscape composition. The latest pass is an original, shallow 2.5D Blender scene: fixed orthographic dimetric camera, compact faceted volumes, soft light, and restrained pigment texture. It tests the approved style direction without changing Vaelora's 2D gameplay presentation. **This is an exploratory style study, not accepted final art; it may inform clearly labeled internal functional visuals, but the owner must judge the balance of volume, faceting, painterly finish, and readability before final refinement or acceptance.** The unit PNGs are single visual-slice poses, not complete six-facing or animated production sheets. These candidates are not final production imports and must stay outside `game/assets/`; no Godot integration has been performed. Import presets, in-engine registration, runtime readability, accessibility, and platform behavior remain unverified.

## Re-render

From the repository root:

```sh
"/Applications/Blender.app/Contents/MacOS/Blender" --background --factory-startup --python-exit-code 1 --python docs/game-design/art-samples/issue_17/create_visual_slice.py
```

The script uses a fixed random seed for terrain details and writes only to this directory.
