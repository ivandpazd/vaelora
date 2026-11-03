"""Human premium visual scorecard for Vaelora v0.3.2.

The tool deliberately does not calculate a compensating average. Every critical visual
family must independently clear the target and no blocker/major may remain open.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TARGET = 9.0
AREAS = (
    "terrain_general",
    "cities",
    "forests_mountains",
    "soldiers",
    "coast",
    "overall",
)


def template() -> dict:
    return {
        "pipeline": "v0.3.2",
        "target_each_area": TARGET,
        "scores": {area: None for area in AREAS},
        "unit_framing": "PASS",
        "open_blockers": [],
        "open_majors": [],
        "notes": {},
        "accepted_by_human": False,
    }


def check(data: dict) -> list[str]:
    issues: list[str] = []
    scores = data.get("scores", {})
    for area in AREAS:
        value = scores.get(area)
        if not isinstance(value, (int, float)):
            issues.append(f"{area}: missing numeric score")
        elif value < TARGET:
            issues.append(f"{area}: {value:.1f}/10 < {TARGET:.1f}/10")
    if data.get("unit_framing") != "PASS":
        issues.append("unit_framing must be PASS")
    if data.get("open_blockers"):
        issues.append("open blockers remain")
    if data.get("open_majors"):
        issues.append("open majors remain")
    if data.get("accepted_by_human") is not True:
        issues.append("explicit human acceptance is still false")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    init = sub.add_parser("init")
    init.add_argument("path", type=Path)
    validate = sub.add_parser("check")
    validate.add_argument("path", type=Path)
    args = parser.parse_args()

    if args.cmd == "init":
        args.path.parent.mkdir(parents=True, exist_ok=True)
        args.path.write_text(json.dumps(template(), indent=2), encoding="utf-8")
        print(args.path)
        return

    data = json.loads(args.path.read_text(encoding="utf-8"))
    issues = check(data)
    report = {"passed": not issues, "target": TARGET, "issues": issues}
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if issues else 0)


if __name__ == "__main__":
    main()
