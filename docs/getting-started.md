# Getting Started

## Prerequisites

- Python 3.11+
- [UV](https://docs.astral.sh/uv/) installed
- Node.js 20+ for docs build only

## Install dependencies

```powershell
uv sync
```

The command installs Python dependencies from `pyproject.toml`.

## Optional preprocessing

Use bright-edge background removal before experiments:

```powershell
uv run python scripts/remove_edge_background.py --inputs path/to/input.png
```

You can pass multiple files at once:

```powershell
uv run python scripts/remove_edge_background.py --inputs path/to/input1.png path/to/input2.jpg
```

## Run benchmark experiments

```powershell
uv run python scripts/vtracer_experiments.py --inputs output/preprocessed/input1.nobg.png output/preprocessed/input2.nobg.png
```

`experiment_summary.csv` is generated in `output/vtracer/experiments/`.

## Build a browsable report

```powershell
uv run python scripts/build_vtracer_report.py
```

Open `output/vtracer/experiments/report.md` to review:

- conversion results by preset
- preview of rendered SVGs
- timing and complexity metrics

## Local docs commands

To validate the docs site:

```bash
npm install
npm run docs:dev
npm run docs:build
```
