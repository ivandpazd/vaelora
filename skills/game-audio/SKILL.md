---
name: game-audio
description: "Trigger: game audio, music, sound effect, ambience, audio mix, accessibility, adaptive audio. Design audio that communicates state and respects platform constraints."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load for music, sound effects, ambience, feedback audio, mixing, audio assets, or audio accessibility.

## Hard Rules
- Tie important audio cues to observable game states, not hidden implementation details.
- Track provenance, licensing, format, looping, loudness, and platform constraints.
- Provide mute, volume, and reduced-distraction behavior where the UI contract requires it.
- Keep simulation independent from audio playback.

## Decision Gates
- Gameplay cue: define trigger, priority, repetition, and fallback.
- Music: define loop, transition, and interruption behavior.
- Platform issue: isolate adapter behavior and test the silent fallback.

## Execution Steps
1. Map audio purpose to player information.
2. Specify cue states, mix priority, and accessibility controls.
3. Integrate through presentation/platform boundaries.
4. Test interruption, save/load, focus changes, and target platforms.

## Output Contract
Return cue map, assets/provenance, mix behavior, accessibility checks, and platform evidence.

## References
- `docs/technical/architecture-proposal.md`
- `docs/game-design/game-design-document.md`
