"""Validate tracked Python and notebook source without loading ML models."""

import ast
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tracked(pattern: str) -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", pattern], cwd=ROOT, text=True
    )
    return [ROOT / line for line in output.splitlines() if line]


def main() -> None:
    python_files = tracked("*.py")
    notebooks = tracked("*.ipynb")
    for path in python_files:
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for path in notebooks:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        assert notebook.get("nbformat") == 4, f"Unsupported format: {path.name}"
    print(f"Validated {len(python_files)} Python files and {len(notebooks)} notebooks")


if __name__ == "__main__":
    main()
