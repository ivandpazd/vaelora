# Pre-delivery review — Terrain Suite v5.0-rc1 General

## Base reviewed

- Required base: Terrain v5.0-rc2 fixed.
- Meadow v5.0-rc2 preserved as the visual baseline.
- Coast v5.1 preserved instead of rewritten.
- Water v2 retained as the structural base and reviewed through the suite polish path.

## Findings corrected before packaging

1. Forest tree clearance was increased so canopy footprint is less likely to cross the logical tile edge.
2. Snow wind-bent tree clearance was increased for the same reason.
3. An unused Desert rock material definition was removed; Desert now honestly uses the existing warm-rock vocabulary until a dedicated rock material is promoted.
4. Desert and Snow remain separate real candidate builders with their own geometry/material/scatter rules; neither is a Plains/Peak proxy.
5. The suite stays parallel to production TERRAIN_VARIANTS. This prevents a visually weak candidate from silently replacing an already working production family before human review.

## Technical review

- Python compilation: PASS.
- Existing contract invariants: PASS on reconstructed current pipeline.
- Terrain Suite host invariants: PASS.
- Static pipeline audit: PASS, 0 issues.
- New artkit routes: PASS.
- Mixed benchmark tile count: 36 exactly.
- Deterministic BLAKE2 seed derivation retained.
- Exact pointy-top hex perimeter retained in candidate surfaces.
- Candidate scatter uses existing clip-safe hex containment helpers.

## Deliberate non-changes

- Camera 45° / 30° unchanged.
- Unit v4.1 unchanged.
- Coast v5.1 implementation unchanged.
- Current Meadow v5.0-rc2 implementation unchanged.
- Runtime production TERRAIN_VARIANTS not expanded yet.

## Remaining human/Blender gate

Actual Blender 5.2.3 LTS renders are still required. No static test can certify that Mountain, Peak, Desert, Snow or the mixed 36-hex composition are visually 9/10. Promotion to final v5 should happen only after the individual family sheets and benchmark36 pass human review.

## Final sweep / package revision 2

6. Fixed a real integration-review bug: benchmark36 is now centred around the canonical camera target instead of living in positive axial space.
7. Increased benchmark36 review framing from 20.2 to 23.8 so tall Peak silhouettes and 6x6 corner tiles have safe margin.
8. Coast review now deterministically covers all three semantic morphologies instead of merely hoping the seed selects them.
9. Candidate land families now have four authored macro archetypes; seed rotation/mirroring is secondary rather than the only source of variation.
10. Forest review variants now use different cluster plans instead of always the same 4+3 tree composition.
11. Updater now preflights required material keys and geometry helpers before replacing any files, preventing hidden rc2-base mismatches.
