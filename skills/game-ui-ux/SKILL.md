---
name: game-ui-ux
description: "Trigger: UI, UX, HUD, menu, input, accessibility, touch, controller, keyboard, focus, responsive layout. Design readable cross-platform strategy-game interaction."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load for screens, HUD, menus, feedback, input mapping, accessibility, focus, or interaction flows.

## Stage Scope
Primary: stages 1–4; supports stage 5. Interaction contracts are defined before vertical-slice implementation and rechecked per target family.

## Hard Rules
- Keep presentation and input adapters from owning authoritative game rules.
- Emit the same player intent vocabulary from touch, mouse, keyboard, and controller.
- Design landscape layouts, safe areas, readable selection, visible focus, and minimum target sizes.
- Make rejected commands explainable and preserve state.

## Decision Gates
- New interaction: define discoverability, confirmation, cancellation, and feedback.
- Device difference: adapt input, not gameplay semantics.
- Accessibility change: test keyboard/focus, scale, contrast, and non-visual feedback.

## Execution Steps
1. Map the user goal and state transitions.
2. Specify layout, input, feedback, focus, and error states.
3. Implement with representative final-quality visual context.
4. Validate device families and record screenshots or captures where useful.

## Output Contract
Return user goal, flow, states, device coverage, accessibility checks, and visual evidence.

## References
- `docs/technical/architecture-proposal.md`
- `docs/game-design/game-design-document.md`
- `README.md`
