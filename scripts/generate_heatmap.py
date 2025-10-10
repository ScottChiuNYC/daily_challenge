#!/usr/bin/env python
"""Small wrapper script to generate the yearly heatmap and stage the output.

This script is intended to be referenced by a pre-commit hook. It imports the
package (installed editable via pre-commit additional_dependencies) and runs
the generator. If the generated image changes, it will be `git add`ed so the
commit can include the updated image.
"""
from pathlib import Path
import subprocess

try:
    from daily_challenge import draw_2025_heatmap
except Exception:
    # If the package isn't importable, try importing relative from this repo
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from daily_challenge import draw_2025_heatmap


def main():
    out = Path("yearly_heatmaps") / "2025.png"
    # Ensure directory exists and run the generator
    draw_2025_heatmap()

    # If output exists, stage it so the commit includes the generated image
    if out.exists():
        subprocess.run(["git", "add", str(out)])


if __name__ == "__main__":
    main()
