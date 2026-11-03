# Vaelora — UI Visual Language v0.3

## 1. UI objective

The interface should feel like part of Vaelora’s world identity without pretending to be a physical medieval object. It is a modern strategy UI informed by the Trama’s language of **routes, nodes, links and civic markers**.

Avoid generic fantasy parchment, giant ornamental frames, metallic beveled buttons and texture-heavy panels.

## 2. Core visual grammar

- clean layered panels;
- route/node line motifs;
- restrained corner geometry inspired by hex/route connections;
- warm neutral surfaces over darker desaturated foundations;
- faction accent only where ownership/context matters;
- high information density handled through spacing and hierarchy, not decorative borders.

## 3. Relationship to board art

UI is visually calmer than the world. It should frame the board rather than compete with it.

Use:

- lower texture frequency;
- fewer material effects;
- controlled transparency only where readability remains strong;
- flat/clean iconography with modest depth cues.

## 4. Information hierarchy

Typical priority:

1. current action/confirmation;
2. selected object name/role/status;
3. resources/costs/progress;
4. available actions;
5. secondary explanation;
6. flavor text.

Do not give flavor text the same weight as action cost or rejection reason.

## 5. Color

Shared UI neutrals dominate. Faction colors identify ownership/context. Warning/error colors are reserved and redundant with icon/text.

Do not make every Auren panel blue and every Brasal panel red; this produces color fatigue and hurts contrast.

## 6. Icon language

Icons use:

- strong filled/outlined silhouette;
- consistent stroke weight where outlines are used;
- one focal metaphor;
- minimal internal detail;
- shape redundancy for resource/action meaning.

Test at compact logical sizes, not only as large SVG previews.

## 7. Buttons and action states

Each actionable control needs visually distinct:

- default;
- hover/focus;
- pressed/active;
- disabled;
- destructive/warning where applicable.

Keyboard/controller focus must not rely on hover or color alone.

## 8. Selected unit/city panel

Use a clear role/city header, key stats, action group and contextual state. Avoid embedding the whole character/city render if it consumes space better used for gameplay information; a compact portrait/icon can be derived later if useful.

## 9. Production/research

Production and research cards emphasize:

- name/icon;
- cost/progress;
- prerequisite/availability;
- effect summary;
- current selection.

Locked/illegal state needs an explicit reason, not only dimming.

## 10. Technology tree

The Trama route/node motif is particularly appropriate for the technology graph, but connections must reflect real prerequisites only. Decorative route lines must not create false dependencies.

Shared technologies use a neutral/common visual language. Unique faction technologies receive controlled faction accents and heraldic support.

## 11. Fog/territory/selection integration

World overlays and HUD feedback reinforce one another. Selection is not just a glowing hex: panel header/focus state must also confirm what is selected.

## 12. Localization

Layouts must tolerate the project’s documented text expansion targets. Avoid fixed-width labels designed only around short English strings.

Icons cannot replace localized text for essential ambiguous actions unless the meaning is universally clear and accessible labeling exists.

## 13. Typography

Typography selection remains a separate licensed-asset decision. Direction:

- highly readable UI sans/serif hybrid system or complementary family pair;
- avoid overly decorative fantasy display faces for body/UI text;
- distinctive display treatment may be reserved for logo/major headings;
- Spanish accents and future localization coverage are mandatory.

Do not commit a font merely because it visually matches; license and glyph coverage must be recorded.

## 14. Screen-specific tone

### Main menu

Large world image, strong logo, low navigation clutter.

### Match setup

Clear structured choices; map/civilization art supports comparison.

### In-game

Minimal obstruction; essential info anchored consistently.

### City/research

Higher information density but same visual grammar.

### Victory/summary

Can become more celebratory while remaining within the established palette/material language.
