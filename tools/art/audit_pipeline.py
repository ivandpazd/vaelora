"""Static source audit for Vaelora Art Pipeline v0.3.2-r2."""
from __future__ import annotations

import argparse
import ast
import builtins
import json
import re
import symtable
from pathlib import Path

PROHIBITED_TEXT = {
    "primitive_ico_sphere_add": "IcoSphere primitive is prohibited as a primary final rock/foliage source",
    "hash(": "Python hash() is process-randomized and must not derive accepted asset seeds",
    "TODO": "unresolved TODO in production source",
    "FIXME": "unresolved FIXME in production source",
    "generated-v0.2": "stale v0.2 output path",
    "Art Pipeline v0.2": "stale v0.2 production label",
}
BUILTINS = set(dir(builtins))


def undefined_global_references(text: str, filename: str) -> list[str]:
    """Conservative symtable pass that catches missing module imports used in functions."""
    table = symtable.symtable(text, filename, "exec")
    module_names = {s.get_name() for s in table.get_symbols()}
    issues: set[str] = set()

    def walk(node):
        for symbol in node.get_symbols():
            name = symbol.get_name()
            if symbol.is_referenced() and symbol.is_global() and name not in module_names and name not in BUILTINS:
                issues.add(name)
        for child in node.get_children():
            walk(child)

    for child in table.get_children():
        walk(child)
    return sorted(issues)


def audit_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    try:
        ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        return [f"{path}: syntax error: {exc}"]
    for token, reason in PROHIBITED_TEXT.items():
        if token in text:
            issues.append(f"{path}: {reason} ({token})")
    for match in re.finditer(r"(?<![\w.])random\.(random|uniform|choice|randint|shuffle)\(", text):
        line = text.count("\n", 0, match.start()) + 1
        issues.append(f"{path}:{line}: use local random.Random(seed), not module-global random")
    for name in undefined_global_references(text, str(path)):
        issues.append(f"{path}: possible undefined global reference {name!r}")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, nargs="?", default=Path("tools/blender"))
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()
    paths = sorted(path for path in args.root.rglob("*.py") if path.resolve() != Path(__file__).resolve())
    issues = [issue for path in paths for issue in audit_file(path)]
    report = {"files": len(paths), "issues": issues, "passed": not issues}
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if issues else 0)


if __name__ == "__main__":
    main()
