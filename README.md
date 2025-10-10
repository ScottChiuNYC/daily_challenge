# daily_challenge

## Overview

`daily_challenge` generates a yearly activity heatmap based on Git commit dates. It's intended to help you visualize how often you work on a repository and can be used locally or in CI. The generated image can be embedded into `README.md` or other documentation.

## Install

```cmd
pip install daily-challenge
```

## Usage

- The main helper is `draw_2025_heatmap()` in `daily_challenge/__init__.py`.
- By default it saves to `yearly_heatmaps/2025.png` relative to the repository root. The package will try to detect the repo root using `git rev-parse --show-toplevel`; if that fails it falls back to the package parent directory.

Typical usage in a Python session:

```python
from daily_challenge import draw_2025_heatmap
draw_2025_heatmap()
```

After running, the image will be available at `yearly_heatmaps/2025.png`.

## Embedding the heatmap in README

Add a relative image link in Markdown to display the generated image (this repo already includes the example):

```markdown
![2025 Yearly Heatmap](yearly_heatmaps/2025.png)
```

Note: GitHub and other renderers will show the image only if the file is committed to the repository.

## Sharing hooks with collaborators

Local Git hooks (in `.git/hooks`) are not pushed to remotes. Recommended options to share hook behavior:

1. Use `pre-commit` (recommended). Add a `.pre-commit-config.yaml` to the repo and ask collaborators to run `pip install pre-commit && pre-commit install`.
2. Commit hook scripts into a directory (e.g. `.githooks/`) and instruct collaborators to run:

```cmd
git config core.hooksPath .githooks
```

### Enable the included pre-commit hook

This repository includes a simple pre-commit hook that regenerates the heatmap before each commit. The hook scripts live in `.githooks/` and there are installer helpers in `scripts/`.

On POSIX (macOS / Linux / Git Bash):

```sh
sh scripts/install-hooks.sh
```

On Windows (cmd.exe):

```cmd
scripts\install-hooks.cmd
```

After running the installer, verify the hooks path with:

```cmd
git config --get core.hooksPath
```

The hook runs this command:

```cmd
python -c "from daily_challenge import draw_2025_heatmap; draw_2025_heatmap()"
```


3. Use GitHub Actions under `.github/workflows/` to run checks on push/PR.

## Troubleshooting

- If the image doesn't appear after generation, make sure `yearly_heatmaps/2025.png` exists and is committed.
- If `git` isn't on PATH, the package will fall back to the project directory; ensure you run the script from the repo or provide an explicit repo_root to helper functions.

## Contributing

PRs welcome. If you add CI or packaging, consider including the generated heatmap in releases or creating a small script to update the README automatically.

---

![2025 Yearly Heatmap](yearly_heatmaps/2025.png)

