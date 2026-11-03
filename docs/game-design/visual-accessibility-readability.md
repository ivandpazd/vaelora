# Vaelora — Visual Accessibility and Readability v0.3

## 1. Principle

Accessibility is built into base art rather than added as an overlay at the end. Essential states must remain understandable through shape, value, iconography or text in addition to hue.

## 2. Required non-color cues

- terrain categories: shape/texture/value;
- city stage: mass/count/landmark hierarchy;
- faction: settlement planning/silhouette/material blocks;
- unit role: equipment silhouette;
- selection: outline + UI indication;
- legal/illegal action: icon/shape/text feedback, not green/red only;
- fog states: opacity/value/treatment differences;
- ownership: border/marker system plus faction color.

## 3. Grayscale gate

All representative slices have a grayscale review. Grayscale is not a perfect simulation of color-vision differences; it is a hard test of value/silhouette dependence.

Failures include:

- Meadow and Plains become indistinguishable;
- Auren/Brasal city distinction disappears;
- roads vanish into terrain;
- selection outline merges with bright coast/foam;
- unit shield/weapon merges with background.

## 4. Small-scale gate

Review at:

- 75% overview;
- 100% standard;
- 125% close;
- compact 720×540 logical viewport;
- 320 px screenshot proxy.

Do not use the 125% close view to justify detail that damages 75% clarity.

## 5. Motion

Non-essential motion respects reduced-motion. Essential state changes use short feedback that remains understandable when motion is reduced.

## 6. Contrast ownership

UI/accessibility rules in the GDD own exact interface contrast requirements. Environment art supports them by reserving extreme luminance and saturation for focal/feedback layers rather than consuming the full range everywhere.

## 7. Occlusion

No decorative object may obscure:

- a unit’s main equipment silhouette;
- city ownership marker;
- road junction;
- port connection;
- resource/improvement identifier;
- selection boundary.

When overlap is unavoidable, presentation layering/outline wins over environmental fidelity.
