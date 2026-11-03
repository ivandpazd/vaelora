# Vaelora — Visual Asset Provenance and Rights Policy v0.3

## 1. Goal

Vaelora is intended for commercial distribution. Every shipped visual asset must have a clear source and usage right.

## 2. Internally generated procedural assets

For v0.3 environment/faction benchmarks, provenance is:

- Vaelora-owned generator source;
- deterministic seed;
- Blender production version;
- source-module SHA-256 hashes;
- no downloaded mesh/image texture unless explicitly documented.

The manifest records these facts.

## 3. External references

Existing games may be used to study broad principles such as readability, composition and quality. Do not trace or reproduce recognizable assets, buildings, unit silhouettes, icons, logos, textures or exact palettes from another game.

Reference images are not copied into runtime assets merely because they are available online.

## 4. External production assets

If a future asset uses a third-party font, texture, brush, model, icon, audio-visual element or marketplace pack, record:

- provider;
- exact asset/product;
- license;
- acquisition date;
- proof/license file location;
- modification status;
- redistribution restrictions;
- whether source may be committed publicly.

Exclude anything with unclear commercial rights.

## 5. Fonts

Font selection requires explicit license and required glyph coverage before integration. Do not bundle a font file in review packages unless redistribution is permitted.

## 6. AI-assisted workflow

AI tools may assist generation/code iteration, but the project maintains authored constraints, source code, deterministic generation and human review. Do not rely on an opaque external asset whose source/right cannot be explained.

Repository commit messages and public artifacts follow the project’s existing contribution policy; provenance records focus on asset rights/source rather than promotional AI attribution.

## 7. Public repository caution

Do not commit licensed source material whose license permits use in the game but forbids redistribution of source files. Keep such material outside the public repository or in an approved protected storage workflow.
