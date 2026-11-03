# Vaelora Terrain Suite v5.0-rc1 General — reviewed package r2

Unified candidate terrain pass built on top of Terrain v5.0-rc2.

## Included

- Meadow: preserves the accepted v5.0-rc2 baseline.
- Plains v5 candidate.
- Forest final-polish candidate.
- Hills v5 candidate.
- Mountain v5 candidate.
- Peak v5 candidate.
- Desert/Arid v1 **real candidate family** (not a recoloured proxy).
- Snow v1 **real candidate family** (not a white proxy).
- Water final-polish review family using Water v2 geometry/material language.
- Coast final-polish review using the existing Coast v5.1 shoreline system.

The suite runs parallel to the current production generators so a weak candidate family cannot silently replace a working asset. Once the mixed benchmark is accepted, families can be promoted into the canonical terrain contract.

## Main outputs

- one 7-hex review image per family;
- one mixed 36-hex integration benchmark;
- deterministic seeds;
- exact hex registration;
- clip-safe scatter;
- ~70% visual-detail philosophy inherited from Meadow v5.


## Final-sweep changes

- benchmark36 camera centering + safe 23.8 framing;
- guaranteed Coast morphology coverage;
- four authored macro archetypes per candidate land family;
- variant-aware forest cluster plans;
- updater material/geometry preflight.
