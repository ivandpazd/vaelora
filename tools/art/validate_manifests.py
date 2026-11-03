"""Validate Vaelora manifest schema v3, source freshness and production pin."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

BLENDER_DIR = Path(__file__).resolve().parents[1] / "blender"
if str(BLENDER_DIR) not in sys.path:
    sys.path.insert(0, str(BLENDER_DIR))

from vaelora_style import (  # noqa: E402
    ART_STYLE_ID,
    GENERATOR_VERSION,
    MANIFEST_SCHEMA_VERSION,
    PRODUCTION_BLENDER_VERSION,
)

REQUIRED = {
    "manifest_schema", "asset_id", "art_style_id", "generator_version", "lifecycle_state",
    "seed", "family", "source_script", "source_sha256", "blender_version",
    "production_blender_pin", "renderer", "camera", "canvas", "provenance",
    "statistics", "acceptance_state",
}
FAMILIES = {"terrain", "overlay", "unit", "city", "hero_prop"}
STATES = {"concept", "benchmark", "production_candidate", "accepted", "shipped", "rejected"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def inspect(path: Path, *, require_production_pin: bool, require_current_sources: bool) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path}: invalid JSON: {exc}"]

    missing = sorted(REQUIRED - set(data))
    if missing:
        errors.append(f"{path.name}: missing keys {missing}")
    if data.get("manifest_schema") != MANIFEST_SCHEMA_VERSION:
        errors.append(f"{path.name}: manifest_schema must be {MANIFEST_SCHEMA_VERSION}")
    if data.get("generator_version") != GENERATOR_VERSION:
        errors.append(
            f"{path.name}: stale generator_version {data.get('generator_version')!r}; expected {GENERATOR_VERSION!r}"
        )
    if data.get("art_style_id") != ART_STYLE_ID:
        errors.append(f"{path.name}: art_style_id {data.get('art_style_id')!r}; expected {ART_STYLE_ID!r}")
    if data.get("renderer") != "BLENDER_EEVEE":
        errors.append(f"{path.name}: renderer must be BLENDER_EEVEE")
    if data.get("family") not in FAMILIES:
        errors.append(f"{path.name}: unknown family {data.get('family')!r}")
    if data.get("lifecycle_state") not in STATES:
        errors.append(f"{path.name}: invalid lifecycle_state {data.get('lifecycle_state')!r}")

    expected_pin = list(PRODUCTION_BLENDER_VERSION)
    if data.get("production_blender_pin") != expected_pin:
        errors.append(f"{path.name}: production_blender_pin must be {expected_pin}")
    if require_production_pin and data.get("blender_version") != expected_pin:
        errors.append(
            f"{path.name}: rendered with Blender {data.get('blender_version')}; production acceptance requires {expected_pin}"
        )

    hashes = data.get("source_sha256") or {}
    if not isinstance(hashes, dict) or len(hashes) < 4:
        errors.append(f"{path.name}: insufficient source_sha256 traceability")
    elif require_current_sources:
        for name, digest in hashes.items():
            if not isinstance(digest, str) or len(digest) != 64:
                errors.append(f"{path.name}: invalid SHA-256 for {name}")
                continue
            source = BLENDER_DIR / name
            if not source.exists():
                errors.append(f"{path.name}: source file recorded in manifest is missing: {name}")
                continue
            current = sha256(source)
            if current != digest:
                errors.append(f"{path.name}: stale source hash for {name}; regenerate asset")
    else:
        for name, digest in hashes.items():
            if not isinstance(digest, str) or len(digest) != 64:
                errors.append(f"{path.name}: invalid SHA-256 for {name}")

    canvas = data.get("canvas") or {}
    for key in ("logical", "final", "work"):
        if key not in canvas or len(canvas.get(key, [])) != 2:
            errors.append(f"{path.name}: invalid canvas.{key}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    parser.add_argument("--allow-review-blender", action="store_true", help="Allow a non-pinned Blender render for review-only evidence")
    parser.add_argument("--allow-stale-sources", action="store_true", help="Skip comparison of manifest source hashes with current source files")
    args = parser.parse_args()
    errors: list[str] = []
    checked = 0
    for root in args.roots:
        for path in sorted((root / "manifests").glob("*.json")):
            checked += 1
            errors.extend(
                inspect(
                    path,
                    require_production_pin=not args.allow_review_blender,
                    require_current_sources=not args.allow_stale_sources,
                )
            )
    report = {"checked": checked, "errors": errors, "passed": not errors}
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
