# img2svg-bench

[日本語版](./README.ja.md)

`img2svg-bench` is a local-first benchmark repository for comparing image-to-SVG tools, presets, and preprocessing pipelines.

Right now the repository focuses on a reproducible VTracer baseline:

- optional bright-edge background removal
- multiple VTracer presets
- CSV summaries
- Markdown reports with embedded SVG render previews

## Why This Repo Exists

Image-to-SVG comparisons are usually judged by eye, but benchmark work needs repeatable inputs and measurable outputs.

This repository is meant to make comparisons easier by keeping the workflow scriptable:

1. prepare input images
2. optionally preprocess them
3. run one or more SVG conversion presets
4. collect timing and SVG complexity metrics
5. generate a browsable Markdown report

## Current Scripts

- `scripts/remove_edge_background.py`
  Flood-fills bright border-connected background and saves transparent PNGs.
- `scripts/vtracer_experiments.py`
  Runs several VTracer presets against one or more input images and writes `experiment_summary.csv`.
- `scripts/build_vtracer_report.py`
  Builds a Markdown report from the CSV and embeds representative SVG outputs directly.

## Quick Start

Install dependencies with UV:

```powershell
uv sync
```

Optional preprocessing:

```powershell
uv run python scripts/remove_edge_background.py --inputs path/to/image1.png path/to/image2.jpg
```

Run VTracer experiments:

```powershell
uv run python scripts/vtracer_experiments.py --inputs output/preprocessed/image1.nobg.png output/preprocessed/image2.nobg.png
```

Build the Markdown report:

```powershell
uv run python scripts/build_vtracer_report.py
```

Outputs are written under `output/` by default and are intentionally ignored from Git.

## Metrics Collected Today

- runtime per preset
- output SVG size
- path count
- unique fill count
- output width and height

These are not enough for a full benchmark yet, but they provide a strong starting baseline.

## What Should Come Next

- add more runners beyond VTracer
- define dataset categories such as logos, characters, photos, line art, and diagrams
- add render-back image metrics
- separate fidelity metrics from editability metrics
- keep benchmark configs versioned and reproducible

## Repository Policy

- local benchmark artifacts live under `output/` and are not committed
- local/private input images are not published by default
- the repository is structured so you can bring your own images and generate reports locally
