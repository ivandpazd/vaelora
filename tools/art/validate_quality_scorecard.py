"""Validate the human premium visual scorecard; never computes art quality automatically."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scorecard", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()

    data = json.loads(args.scorecard.read_text(encoding="utf-8"))
    minimum = float(data.get("minimum_area_score", 9.0))
    average_target = float(data.get("minimum_average_score", 9.3))
    errors: list[str] = []
    area_scores: dict[str, float] = {}

    for area, payload in (data.get("areas") or {}).items():
        criteria = payload.get("criteria") or {}
        missing = [name for name, value in criteria.items() if value is None]
        if missing:
            errors.append(f"{area}: unscored criteria {missing}")
            continue
        values = []
        for name, value in criteria.items():
            try:
                number = float(value)
            except (TypeError, ValueError):
                errors.append(f"{area}.{name}: score must be numeric")
                continue
            if not (0.0 <= number <= 10.0):
                errors.append(f"{area}.{name}: score {number} outside 0..10")
            values.append(number)
        if len(values) != len(criteria):
            continue
        computed = sum(values) / len(values) if values else 0.0
        declared = payload.get("score")
        if declared is None:
            errors.append(f"{area}: area score missing; computed criterion mean is {computed:.2f}")
        else:
            declared_f = float(declared)
            if abs(declared_f - computed) > 0.15:
                errors.append(f"{area}: declared score {declared_f:.2f} differs from criterion mean {computed:.2f}")
            area_scores[area] = declared_f
            if declared_f < minimum:
                errors.append(f"{area}: score {declared_f:.2f} below premium minimum {minimum:.2f}")
        if payload.get("blockers"):
            errors.append(f"{area}: unresolved blockers {payload['blockers']}")
        if payload.get("majors"):
            errors.append(f"{area}: unresolved majors {payload['majors']}")

    average = sum(area_scores.values()) / len(area_scores) if area_scores else 0.0
    if len(area_scores) == len(data.get("areas") or {}) and average < average_target:
        errors.append(f"overall area average {average:.2f} below target {average_target:.2f}")

    report = {
        "scorecard": str(args.scorecard),
        "area_scores": area_scores,
        "average": average,
        "minimum_area_score": minimum,
        "minimum_average_score": average_target,
        "errors": errors,
        "passed": not errors,
        "note": "PASS means the human-entered review meets the declared gate; it is not automatic art approval.",
    }
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
