# daily_challenge — GitHub-hosted pre-commit hook

This repository provides a pre-commit hook that regenerates a yearly activity heatmap (PNG) from Git commit history and stages the generated image. This project is distributed as a GitHub-hosted pre-commit hook (not published to PyPI).

Key points:
- The hook repository must include a top-level `.pre-commit-hooks.yaml` manifest describing available hooks. The manifest is a top-level YAML array of hook objects (see pre-commit docs).
- Other repositories can reference this hook directly from GitHub using `repo: https://github.com/<owner>/<repo>` and a `rev:` (tag, branch, or commit SHA).

## How other repos reference this hook

Add the following to the target repository's `.pre-commit-config.yaml` to use the hook from GitHub:

```yaml
repos:
  - repo: https://github.com/ScottChiuNYC/daily_challenge
    rev: main  # pin to a tag or commit for stability
    hooks:
      - id: draw-2025-heatmap
        # If you want pre-commit to create an isolated venv and install deps:
        language: python
        additional_dependencies: ['matplotlib', 'numpy']
        entry: python -m daily_challenge
```

Notes:
- Use `rev` pinned to a tag or commit SHA for reproducible behavior in CI. Using `rev: main` is convenient for development but less stable.
- During development you may prefer `language: system` and an editable install (developers run `pip install -e .` locally). For published hooks `language: python` + `additional_dependencies` is recommended.

## Why GitHub (not PyPI)?

Publishing the hook on GitHub makes it easy for other projects to reference it via `pre-commit` without requiring a PyPI release. The pre-commit ecosystem expects repository manifests (`.pre-commit-hooks.yaml`) at the repo root.

If you later want to publish a release on PyPI for convenience, you can — but it's not required for the hook to be usable.

## Hook behavior (important)

- The hook regenerates `yearly_heatmaps/2025.png`.
- To avoid recursive commits, the hook stages generated files and exits non-zero to abort the commit. This gives developers a chance to review the staged files and re-run `git commit` to include them.
- The generator optionally edits `README.md` to append or update a `?ts=` cache-busting query parameter on the image link so viewers will see the latest image instead of a cached copy.

## Manual usage

Generate the heatmap manually (Windows cmd):

```cmd
python -c "from daily_challenge import draw_2025_heatmap; draw_2025_heatmap()"
```

Or run the package (if installed):

```cmd
python -m daily_challenge
```

## Contributing

If you're publishing the hook from this repository, ensure:

- `.pre-commit-hooks.yaml` exists at the repo root and contains a top-level list of hooks.
- The hook `id` matches the one documented above (`draw-2025-heatmap`).
- Add a release tag and update README `rev:` examples to point to a stable tag or SHA.

PRs welcome — especially for improving the hook manifest, docs, and packaging.

---

![2025 Yearly Heatmap](yearly_heatmaps/2025.png)
    hooks:
