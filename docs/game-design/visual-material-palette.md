# Vaelora — Material and Palette Contract v0.3

## 1. Palette philosophy

Terrain uses a restrained natural spectrum so gameplay overlays and civilization accents remain legible. Exact hex values are starting production tokens, not license to flatten materials into solid colors.

The shared terrain values below follow `tools/blender/vaelora_style.py` for the closed [Terrain Visual Language v1](TERRAIN_VISUAL_LANGUAGE_V1.md) baseline. Earlier v0.3 water tokens are historical, not a second current palette.

## 2. Shared terrain tokens

| Token | Hex | Role |
|---|---|---|
| Meadow shadow | `#466947` | cool vegetation shade |
| Meadow mid | `#6F9651` | fertile open-land base |
| Meadow light | `#91B75F` | warm lit grass |
| Plains shadow | `#776C43` | dry olive shade |
| Plains mid | `#A99C58` | dry grass base |
| Plains light | `#C4B96B` | sunlit dry grass |
| Forest shadow | `#294B38` | canopy depth |
| Forest mid | `#3F6E46` | broad forest mass |
| Forest light | `#5F8B50` | canopy light |
| Earth dark | `#493329` | deep soil |
| Earth mid | `#6B4935` | exposed earth |
| Clay | `#9B6249` | intermediate stratum |
| Sand | `#CEAE70` | coast transition |
| Sand light | `#E1C88E` | lit beach accents |
| Stone dark | `#46515A` | deep/cool face |
| Stone mid | `#66727A` | primary rock |
| Stone light | `#899397` | lit rock plane |
| Warm stone | `#8A8174` | lower/warm geology |
| Snow/pale stone | `#E2E9E5` | Snow-family surface and Peak upper accent |
| Shallow water | `#5BA39C` | near-shore body |
| Shallow light | `#83C4B3` | broad water light |
| Open water | `#2D687A` | open-sea base |
| Deep water | `#173F50` | depth/shadow |
| Foam | `#DEE9E1` | restrained shoreline accent |

## 3. Faction tokens

### Auren

- Deep blue `#183A63`
- Light blue `#42688C`
- Civic gold `#D6A63A`
- Warm ivory `#F2E8CF`
- Civic stone `#B9AA8A`
- Warning red `#A8443F`

Gold is punctuation, not surface coverage.

### Brasal

- Charcoal `#24262B`
- Ember red `#B84A3A`
- Copper `#C47A44`
- Weathered bone `#D8C7A2`
- Deep moss `#3F5A43`
- Weathered wood `#76503B`

Red is pressure/military emphasis, not the default color of every building.

## 4. Material response matrix

| Material | Roughness intent | Bump | Color frequency | Signature |
|---|---|---|---|---|
| Foliage | high | very low | broad | grouped tonal mass |
| Soil | high | low | broad-medium | warm mottling |
| Clay | high | low | broad | layered side-wall cue |
| Stone | medium-high | low-medium | broad-medium | planar orientation response |
| Wood | high | low | directional broad | bands, repair-friendly |
| Iron/steel | medium | very low | broad | controlled edge highlight |
| Copper | medium | very low | broad | warm craft accent |
| Cloth | high | very low | broad | clean faction block |
| Water | medium | low normal | broad + tiny normal | depth/light separation |

## 5. Orientation response

Stone/terrain may use surface normal to alter value subtly. This is an art-direction aid, not physically exact lighting. The change should reinforce planes without creating toon bands.

## 6. Noise rules

Procedural noise is allowed only when it survives downsample as material richness rather than pixel noise.

- no high-frequency speckle;
- no identical noise scale on every material;
- no high-contrast noise under transparent water;
- no texture detail that creates false edges at 75% zoom.

## 7. Material reuse

Use shared material factories and tokens. Do not create one-off almost-identical materials per asset unless a deliberate visual rule requires it.

## 8. Lighting interaction

Palette is evaluated only under the canonical master light rig. A material that requires bespoke per-asset lighting is rejected.

## 9. Grayscale/value rule

Faction/terrain distinctions must remain readable when hue is removed. If two categories collapse in grayscale, adjust value/shape/material frequency before increasing saturation.


## Premium value/contrast discipline

A near-10 screenshot is not achieved by increasing saturation everywhere. Local value hierarchy should normally read:

1. selected/actionable feedback (highest temporary contrast);
2. units and city landmarks;
3. strategic relief/terrain boundary;
4. improvements/roads;
5. environmental decoration (lowest contrast).

At 75% zoom, grass, flowers, roof patches and material mottling must collapse into their parent value mass instead of creating speckle. Units may be lightened locally or given clearer material separation when they merge into terrain; terrain should not be globally darkened merely to make units pop.

Grayscale review is mandatory for faction identity and terrain-class separation. A beautiful color render that becomes a same-value mush in grayscale cannot score >=9 in material/readability.
