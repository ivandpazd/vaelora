"""Run the host-side Vaelora v0.3.2-r2 review gate for one or more generated roots."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(*args: str) -> None:
    cmd = [sys.executable, *args]
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("roots", nargs="+", type=Path)
    parser.add_argument("--review-output", type=Path, default=Path("game/assets/art-review-v0.3.2-r2.jpg"))
    parser.add_argument("--qa-dir", type=Path, default=Path("game/assets/qa-v0.3.2-r2"))
    args = parser.parse_args()
    roots = [p.resolve() for p in args.roots]
    qa = args.qa_dir.resolve()
    qa.mkdir(parents=True, exist_ok=True)

    for root in roots:
        run(str(HERE / "downsample.py"), str(root))

    root_args = [str(p) for p in roots]
    run(str(HERE / "validate_manifests.py"), *root_args, "--json", str(qa / "manifests.json"))
    run(str(HERE / "validate_outputs.py"), *root_args, "--json", str(qa / "images.json"))
    run(str(HERE / "estimate_texture_budget.py"), *root_args, "--json", str(qa / "texture-budget-no-mips.json"))
    run(str(HERE / "estimate_texture_budget.py"), *root_args, "--mipmaps", "--json", str(qa / "texture-budget-with-mips.json"))
    run(str(HERE / "make_review_sheet.py"), *root_args, "--output", str(args.review_output.resolve()))
    print("Vaelora v0.3.2-r2 host-side gate completed. Human art/game review is still required.")


if __name__ == "__main__":
    main()
