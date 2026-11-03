"""Create deterministic side-by-side A/B review boards for Vaelora visual iterations."""
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    copy = image.convert("RGB")
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, (29, 39, 43))
    x = (size[0] - copy.width) // 2
    y = (size[1] - copy.height) // 2
    canvas.paste(copy, (x, y))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--before-label", default="BEFORE")
    parser.add_argument("--after-label", default="AFTER")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    before = Image.open(args.before)
    after = Image.open(args.after)
    panel_size = (960, 540)
    header = 54
    out = Image.new("RGB", (panel_size[0] * 2, panel_size[1] + header), (23, 31, 34))
    draw = ImageDraw.Draw(out)
    font = ImageFont.load_default()
    draw.text((18, 18), args.before_label, font=font, fill=(235, 239, 236))
    draw.text((panel_size[0] + 18, 18), args.after_label, font=font, fill=(235, 239, 236))
    out.paste(fit(before, panel_size), (0, header))
    out.paste(fit(after, panel_size), (panel_size[0], header))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.output, quality=94)
    print(args.output)


if __name__ == "__main__":
    main()
