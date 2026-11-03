# Vaelora — Sculpted Shape Language v0.3

This document owns modelling shape rules. It translates the Art Bible into geometry constraints for Blender and AI-assisted generation.

## 1. Frequency hierarchy

Every asset is reviewed in three bands:

- **Macro ≈70%**: silhouette, ridge direction, canopy mass, roof mass, unit pose.
- **Meso ≈20%**: branches, rock shelves, windows, repair bands, undergrowth.
- **Micro ≈10%**: cracks, flowers, tiny stones, trim.

If microdetail makes the macro read worse, remove it.

## 2. Primitive policy

Primitives are construction tools, not visible design solutions.

Allowed:

- cylinder as a temporary branch section that is tapered/merged/obscured into a tree;
- cube as a block-out that is tapered/skewed/beveled/combined into architecture;
- simple planes as cloth/grass where the final silhouette remains authored.

Rejected:

- cone tree;
- IcoSphere boulder;
- cube rock;
- untouched rectangular fantasy house repeated with random scale;
- radial cone mountain.

## 3. Terrain base

External six-edge boundary is exact. Do not bevel/displace the registration perimeter.

Interior surface:

- broad low-frequency height field;
- falloff begins before edge safety band;
- boundary vertices return to canonical elevation;
- slope changes are designed around category identity.

Side wall:

- consistent depth family;
- topsoil/clay/deep layer logic;
- subtle irregular internal stratum breaks allowed;
- no geometry crossing neighboring footprint.

## 4. Rocks

Primary rock constructor:

1. flat grounding ring;
2. asymmetrical middle ring;
3. displaced crown;
4. convex hull/faceted planes;
5. selective tiny bevel only where razor edges look artificial.

Target visible complexity: about 7–18 meaningful faces for small/medium rocks, more only for hero geological formations.

Rock families need different proportions, not just scale.

## 5. Hills

Hill composition uses one directional ridge or saddle. Rock exposure follows ridge orientation. Grass follows lower slopes.

Avoid circular symmetry and three equally spaced bumps.

## 6. Mountains

Build geological hierarchy:

`main ridge -> shoulder -> shelf -> secondary spur -> talus -> base vegetation`

The primary ridge has a deliberate azimuth. Secondary forms support it. Peak placement must not make a starburst.

### Mountain

- broad enough to read as traversable high relief;
- visible lower shelves;
- some base vegetation;
- 3–5 separated, embedded exposed-rock zones with terrain visible between them;
- no long continuous stone rib, floating rock plate or completely vertical needle.

### Peak

- narrower upper ridge;
- stronger vertical asymmetry;
- integrated mountain base with one of four distinguishable summit archetypes: `alpine_offset`, `broken_summit`, `twin_shoulder`, `escarpment`;
- smaller/wider talus base relative to height;
- sparse vegetation;
- optional pale upper face accents;
- no needle/obelisk or walkable-looking top platform.

## 7. Trees

A tree comprises:

`rooted trunk -> branch hierarchy -> 3–6 foliage masses -> species silhouette`

### Trunk

- taper from base;
- slight lean/curvature;
- base may broaden or split;
- branch attachment points not evenly spaced.

### Foliage

Use irregular convex masses with different aspect ratios. Avoid identical blobs.

### Broadleaf round

Wide crown with 1–2 larger side masses.

### Broadleaf columnar

Taller narrower crown with vertical rhythm.

### Conifer

Layered taper with visible gaps/trunk; never stacked perfect cones.

### Wind-bent

Directional trunk/crown; leeward foliage mass is visibly displaced.

## 8. Forest

Use named composition templates. At least one hero tree anchors the rear mass. Preserve front/central opening.

Undergrowth should visually connect tree groups but never fill the unit window.

## 9. Architecture general

Buildings use a small number of strong masses and readable roof profiles. Windows/trim are meso detail, not the silhouette.

Avoid tiny chimneys, railings or ornament that disappear at 75% but clutter alpha edges.

### Grounding

Every structure has a readable base/footing. Contact shadows supplement grounding but do not hide floating geometry.

## 10. Auren shape grammar

- upright proportion;
- clean wall planes;
- hip/gable roofs with controlled angles;
- arches and standards;
- civic building taller/clearer than residences;
- plazas/routes create alignment;
- repeated vertical beacon motif in moderation.

Use controlled symmetry only where it expresses civic planning.

## 11. Brasal shape grammar

- lower/wider roof masses;
- timber over stone footing;
- visibly added repair/extension forms;
- work-yard horizontal elements;
- workshop/longhouse anchors;
- asymmetrical placement with coherent work logic.

Repair should look capable, not broken-down.

## 12. Units

Use broad continuous masses after downsample.

- legs/arms taper and overlap torso/equipment;
- head/helmet is a single readable mass;
- shield/tool/weapon defines role;
- equipment may be oversized 10–15%;
- pose must remain inside tile envelope.

Disconnected-looking capsule limbs are rejected even if technically connected by overlap.

## 13. Ships

Patrol ship should use:

- compact hull;
- one strong sail/standard shape;
- readable bow/stern orientation;
- modest faction construction adaptation;
- no giant mast forest or detailed rigging that disappears.

## 14. Improvements

Improvement silhouette sits below units/cities in hierarchy.

Farm: field pattern is the mass; small structures are support.

Lumber: log stacks/platform define read, tree canopy remains present.

Mine: entrance/support and exposed rock define read.

Port: dock geometry aligns strongly to shoreline direction.

Road: line continuity is the shape.

## 15. Negative-space ownership

Keep clear space around:

- unit feet;
- city entrance/plaza;
- road centre/junction;
- port endpoint;
- coast endpoints;
- selection boundary;
- resource/UI anchor zones.

Negative space is not unfinished art.
