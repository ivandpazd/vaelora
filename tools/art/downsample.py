"""Production post-process for Vaelora 4x working renders.

Uses premultiplied-alpha Lanczos resampling to avoid dark fringes on thin silhouettes,
then emits modular contact shadows for terrain-independent object families.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageFilter

FAMILY_FINAL = {
    "terrain": (256, 128),
    "overlay": (256, 128),
    "unit": (256, 128),
    "city": (512, 256),
    "hero_prop": (256, 128),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def resize_premultiplied(image: Image.Image, target: tuple[int, int]) -> Image.Image:
    """Resize straight-alpha RGBA without dark transparent-edge contamination."""
    rgba = image.convert("RGBA")
    premult = rgba.convert("RGBa")
    resized = premult.resize(target, Image.Resampling.LANCZOS)
    return resized.convert("RGBA")


def make_contact_shadow(image: Image.Image, family: str, out_path: Path) -> Path:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    if bbox is None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        shadow.save(out_path)
        return out_path
    l, t, r, b = bbox
    crop = alpha.crop(bbox)
    flatten = {"unit": 0.18, "city": 0.23, "hero_prop": 0.20}.get(family, 0.20)
    sh = max(2, round(crop.height * flatten))
    flattened = crop.resize((crop.width, sh), Image.Resampling.LANCZOS)
    blur_radius = 4 if family == "unit" else 7 if family == "city" else 5
    flattened = flattened.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    flattened = flattened.point(lambda a: round(a * 0.31))
    color = Image.new("RGBA", flattened.size, (23, 39, 43, 0))
    color.putalpha(flattened)
    x = min(max(0, l + 3), image.width - color.width)
    y = min(max(0, b - sh // 2 + 1), image.height - color.height)
    shadow.alpha_composite(color, (x, y))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    shadow.save(out_path, "PNG", optimize=True)
    return out_path


def downsample_manifest(manifest_path: Path, output_root: Path) -> Path:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    family = manifest["family"]
    asset_id = manifest["asset_id"]
    target = FAMILY_FINAL[family]
    raw_path = manifest_path.parent.parent / "raw_4x" / f"{asset_id}_4x.png"
    if not raw_path.exists():
        raise FileNotFoundError(raw_path)
    image = Image.open(raw_path).convert("RGBA")
    expected_work = tuple(manifest["canvas"]["work"])
    if image.size != expected_work:
        raise ValueError(f"{asset_id}: expected work size {expected_work}, got {image.size}")

    resized = resize_premultiplied(image, target)
    out_dir = output_root / "final_2x"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{asset_id}_2x.png"
    resized.save(out_path, "PNG", optimize=True)

    shadow_path = None
    if family in {"unit", "city", "hero_prop"}:
        shadow_path = make_contact_shadow(
            resized,
            family,
            output_root / "shadows_2x" / f"{asset_id}_shadow_2x.png",
        )

    manifest["postprocess"] = {
        "source": str(raw_path),
        "source_sha256": sha256(raw_path),
        "method": "Pillow RGBa premultiplied Image.Resampling.LANCZOS",
        "final_size": list(target),
        "output": str(out_path),
        "output_sha256": sha256(out_path),
        "shadow_output": str(shadow_path) if shadow_path else None,
        "shadow_sha256": sha256(shadow_path) if shadow_path else None,
    }
    manifest["acceptance_state"] = "automated_qa_pending"
    if manifest.get("lifecycle_state") == "concept":
        manifest["lifecycle_state"] = "benchmark"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, help="Generated asset root containing manifests/ and raw_4x/")
    args = parser.parse_args()
    root = args.root.resolve()
    manifests = sorted((root / "manifests").glob("*.json"))
    if not manifests:
        raise SystemExit(f"No manifests found under {root / 'manifests'}")
    for manifest in manifests:
        print(downsample_manifest(manifest, root))


if __name__ == "__main__":
    main()
