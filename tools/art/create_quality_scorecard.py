"""Create the human-review scorecard for Vaelora v0.3.2-r2 premium visual gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

AREAS = {
    "terrain_general": ["macro_shape", "surface_material", "strata", "variant_authorship", "gameplay_readability"],
    "cities": ["faction_identity", "stage_progression", "silhouette", "material_depth", "grayscale_read", "functional_cue_capacity"],
    "forests": ["cluster_composition", "species_silhouette", "negative_space", "grounding", "repetition_resistance"],
    "mountains_peaks": ["ridge_directionality", "geological_hierarchy", "mountain_peak_distinction", "base_grounding", "repetition_resistance"],
    "water": ["shallow_open_distinction", "visual_rest", "highlight_language", "material_depth", "gameplay_readability"],
    "coast": ["shoreline_continuity", "morphology_authorship", "wet_dry_transition", "foam", "land_sea_read", "multi_edge_stitch"],
    "soldiers": ["anatomy", "pose", "role_read", "faction_identity", "equipment_integration", "six_facing_consistency"],
    "unit_framing": ["safe_margin", "perceived_scale", "anchor_consistency"],
    "overall": ["identity", "hierarchy", "luminous_fantasy", "steam_read", "coherence", "runtime_fidelity"],
}



def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--target", type=float, default=9.0)
    parser.add_argument("--average-target", type=float, default=9.3)
    args = parser.parse_args()
    payload = {
        "version": "0.3.2-r2",
        "scale": "0-10 human review",
        "minimum_area_score": args.target,
        "minimum_average_score": args.average_target,
        "automatic_acceptance": False,
        "blocker_or_major_allowed": False,
        "areas": {
            area: {
                "score": None,
                "criteria": {criterion: None for criterion in criteria},
                "blockers": [],
                "majors": [],
                "notes": [],
            }
            for area, criteria in AREAS.items()
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
