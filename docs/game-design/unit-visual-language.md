# Vaelora — Unit Visual Language v0.3

## 1. Strategy-scale character design

Units are strategic icons embodied as characters. Their first job is role recognition, second is faction recognition, third is personality.

Target proportion: about 5–5.5 heads tall, with slightly enlarged head/hands and primary equipment.

## 2. Shared role grammar

| Role | Primary silhouette | Secondary cue | Avoid |
|---|---|---|---|
| Settler | travel bundle + founding marker/staff | practical luggage | looking like a worker or soldier |
| Worker | dominant tool + work pack | sturdy stance | combat weapon read |
| Explorer | light tall silhouette + scouting staff/spyglass | small pack | looking militarized |
| Basic soldier | shield + spear | stable combat stance | tiny realistic weapon |
| Patrol ship | compact military hull + clear sail/standard | patrol equipment | giant warship scale |

## 3. Faction adaptation

A shared role remains the same class. Faction design changes:

- posture;
- shield/tool shape;
- materials;
- pack construction;
- helmet/cloth language;
- standard/heraldry.

It does not add a visual weapon that implies different mechanics.

## 4. Six-direction contract

Facings use canonical 60° world rotations. Camera remains fixed. Each facing is reviewed because weapon/shield overlap can create different silhouettes even from one model.

Required checks:

- no facing clips canvas;
- shield does not fully hide torso in three-quarter views;
- spear/tool does not merge into body silhouette;
- left/right facings remain identifiable;
- feet remain grounded with contact shadow.

## 5. Animation budget

Initial bespoke animations:

- movement: ≤6 frames at 12 fps loop;
- melee/ranged attack: ≤6 frames at 12 fps, ≤0.5 s;
- damage/death: reusable concise feedback unless later approved otherwise.

Settler/worker actions may use short reusable presentation feedback rather than full unique animation sets during the initial prototype.

## 6. Animation truthfulness

Visual movement may interpolate, but authoritative simulation state remains discrete. Rejected commands never animate as if successful.

## 7. Character-detail hierarchy

At runtime scale:

1. role equipment;
2. stance/body mass;
3. faction material blocks;
4. helmet/head shape;
5. only then small trim.

Facial detail is not a priority for board sprites.

## 8. Accessibility

Role cannot depend on faction hue. Shield/tool/pack silhouette supplies redundant recognition. Damage/selection feedback is external to the base sprite so unit art remains stable.
