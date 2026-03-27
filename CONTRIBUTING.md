# Contributing to img2svg-bench

Thanks for helping improve `img2svg-bench`.

## What Contributions Fit Best

- new image-to-SVG runners
- better benchmark metrics
- dataset organization and documentation
- report-generation improvements
- docs, CI, and reproducibility fixes

## Ground Rules

- keep benchmark commands reproducible
- use `uv run ...` for Python commands in docs and examples
- do not commit private sample images by default
- do not commit local benchmark artifacts from `output/`
- keep English and Japanese docs structurally aligned when both are touched

## Development Workflow

Python setup:

```powershell
uv sync
```

Docs setup:

```powershell
npm install
```

Useful checks:

```powershell
uv run python -m py_compile scripts\remove_edge_background.py scripts\vtracer_experiments.py scripts\build_vtracer_report.py
npm run docs:build
```

## Adding a New Runner

When adding a new image-to-SVG tool:

1. document the tool and its constraints
2. keep inputs and outputs comparable with existing runners
3. capture metrics in a format that can be summarized later
4. update docs and benchmark methodology if the comparison surface changes

## Pull Requests

- keep changes focused
- explain what benchmark behavior changed
- include the verification commands you ran
- mention any limitations you could not verify locally
