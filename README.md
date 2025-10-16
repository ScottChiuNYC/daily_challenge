# daily_challenge — GitHub-Hosted Pre-Commit Hook

A lightweight pre-commit hook that regenerates a yearly activity heatmap from a repository's Git commit history. 
This repository is intended to be referenced directly by other projects via `pre-commit` (no PyPI publication required).
A pre-commit hook runs automatically before Git creates a commit; this hook regenerates `yearly_heatmaps/2025.png` and stages it with `git add`.

Example output (committed to your repo):

![2025 Yearly Heatmap](yearly_heatmaps/2025.png?ts=10142025)

## Install and Configure in Your Repository

1. Install and enable `pre-commit` in the target repository:

```bash
pip install pre-commit
pre-commit install
```

2. Create a `.pre-commit-config.yaml` file at the root of the target repository and add the following contents:

```yaml
repos:
  - repo: https://github.com/ScottChiuNYC/daily_challenge
    rev: v0.1.2
    hooks:
      - id: daily-challenge
        name: daily challenge
        entry: python -c "from daily_challenge import main; main()"
        language: python
        additional_dependencies: ['matplotlib', 'numpy']
```

3. Optional, but recommended: Add the following image link to your repository's `README.md` to display the generated heatmap. The timestamp in the URL is a cache-buster that helps viewers fetch the updated image.

```md
![2025 Yearly Heatmap](yearly_heatmaps/2025.png?ts=10022025)
```

## Contributing

PRs welcome — especially for improving the hook manifest, docs, tests, or making the behavior configurable.

