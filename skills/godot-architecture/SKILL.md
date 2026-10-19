---
name: godot-architecture
description: "Trigger: Godot architecture, scene tree, GDScript, project bootstrap, simulation boundary, resource, adapter, export. Keep Vaelora maintainable and deterministic."
license: Apache-2.0
metadata:
  author: "vaelora"
  version: "1.0"
---

## Activation Contract
Load for Godot project structure, engine decisions, scene organization, GDScript conventions, resources, and platform adapters.

## Hard Rules
- Keep simulation independent from scenes, rendering, input hardware, and platform APIs.
- Use one canonical coordinate model for hex rules; project to isometric coordinates only in presentation.
- Prefer explicit data resources and stable IDs over faction branches in scenes.
- Confirm engine and export behavior against current official documentation before locking it.

## Decision Gates
- Proposal status: preserve alternatives and open questions.
- Approved boundary: implement behind the documented layer.
- Platform-specific need: isolate it in an adapter and test the fallback.

## Execution Steps
1. Locate the owning layer and existing seam.
2. Define data flow, dependencies, lifecycle, and test seam.
3. Implement the smallest boundary-preserving change.
4. Run deterministic tests and relevant exports without mutating source after verification.

## Output Contract
Return layer, ownership, dependencies, invariants, tests, platform impact, and open decisions.

## References
- `docs/technical/architecture-proposal.md`
- `docs/project/development-workflow.md`
