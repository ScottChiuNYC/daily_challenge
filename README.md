# daily_challenge — GitHub-hosted pre-commit hook

A lightweight pre-commit hook that regenerates a yearly activity heatmap from a repository's Git commit history and stages the generated PNG. This repository is intended to be referenced directly by other projects via `pre-commit` (no PyPI publication required).

Why use it?
- Quickly visualize contributor activity for the year.
- Keep a generated image in your repo (for example, embedded in the README) without having to run the generator manually.

Example output (committed to your repo):

![2025 Yearly Heatmap](yearly_heatmaps/2025.png)

## Install and Configure in Your Repository

1. Install and enable `pre-commit` in the target repository:

```bash
pip install pre-commit
pre-commit install
```

2. Add the following to your target repo's `.pre-commit-config.yaml` (in the root of the target repo):

```yaml
repos:
  - repo: https://github.com/ScottChiuNYC/daily_challenge
    rev: v0.1.1  # pin to a release or SHA for stability
    hooks:
      - id: daily-challenge
        name: daily challenge
        entry: python -c "from daily_challenge import main; main()"
        language: python
        additional_dependencies: ['matplotlib', 'numpy']
```

3. Recommended: Add the following image link to your repository's `README.md` so the generated heatmap will be displayed.

```md
![2025 Yearly Heatmap](yearly_heatmaps/2025.png)
```

## Behavior

- The hook regenerates `yearly_heatmaps/2025.png` and stages it with `git add` so it will be included in the running commit.
- The displayed image may not update immediately due to browser/CDN caching. A common solution is for the generator to update `README.md` with a cache-busting `?ts=` query parameter so viewers fetch the new image; that behavior is not implemented yet.

## Contributing

PRs welcome — especially for improving the hook manifest, docs, tests, or making the behavior configurable.

