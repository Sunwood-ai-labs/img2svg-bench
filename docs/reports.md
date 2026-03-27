# Reports

## What is generated

`scripts/build_vtracer_report.py` generates `output/vtracer/experiments/report.md` by reading:

- `output/vtracer/experiments/experiment_summary.csv`
- generated SVG artifacts under `output/vtracer/experiments/`

The report is meant for fast review and contains embedded SVG snippets for each candidate.

## Published Sample Results

These repo-managed SVGs are representative outputs from the current VTracer baseline. Because `output/` is ignored, the examples below are copied into `docs/public/results/` for GitHub Pages publishing.

| kiyoka_1 / clean | kiyoka_1 / poster |
| --- | --- |
| ![kiyoka_1 clean](/results/kiyoka-1-clean.svg) | ![kiyoka_1 poster](/results/kiyoka-1-poster.svg) |
| `129.7 KB` / `93 paths` / `1.30 s` | `61.1 KB` / `36 paths` / `0.44 s` |

| kiyoka_2 / clean | kiyoka_2 / poster |
| --- | --- |
| ![kiyoka_2 clean](/results/kiyoka-2-clean.svg) | ![kiyoka_2 poster](/results/kiyoka-2-poster.svg) |
| `210.0 KB` / `123 paths` / `0.84 s` | `108.2 KB` / `46 paths` / `0.51 s` |

These published samples are intentionally compact. Use the locally generated `report.md` to inspect the full preset matrix.

## Full Published Preset Matrix

Every currently published preset variant is listed below.

| Source | Preset | SVG | Size | Paths | Time |
| --- | --- | --- | ---: | ---: | ---: |
| `kiyoka_1` | `default` | [link](/results/kiyoka-1-default.svg) | 734.2 KB | 807 | 1.26 s |
| `kiyoka_1` | `clean` | [link](/results/kiyoka-1-clean.svg) | 129.7 KB | 93 | 1.30 s |
| `kiyoka_1` | `cutout` | [link](/results/kiyoka-1-cutout.svg) | 231.8 KB | 177 | 1.91 s |
| `kiyoka_1` | `polygon` | [link](/results/kiyoka-1-polygon.svg) | 62.7 KB | 296 | 1.12 s |
| `kiyoka_1` | `poster` | [link](/results/kiyoka-1-poster.svg) | 61.1 KB | 36 | 0.44 s |
| `kiyoka_1` | `detail` | [link](/results/kiyoka-1-detail.svg) | 1672.0 KB | 3268 | 11.29 s |
| `kiyoka_1` | `binary_ink` | [link](/results/kiyoka-1-binary-ink.svg) | 219.8 KB | 8 | 0.20 s |
| `kiyoka_2` | `default` | [link](/results/kiyoka-2-default.svg) | 938.8 KB | 832 | 0.87 s |
| `kiyoka_2` | `clean` | [link](/results/kiyoka-2-clean.svg) | 210.0 KB | 123 | 0.84 s |
| `kiyoka_2` | `cutout` | [link](/results/kiyoka-2-cutout.svg) | 386.8 KB | 212 | 1.49 s |
| `kiyoka_2` | `polygon` | [link](/results/kiyoka-2-polygon.svg) | 88.1 KB | 339 | 0.91 s |
| `kiyoka_2` | `poster` | [link](/results/kiyoka-2-poster.svg) | 108.2 KB | 46 | 0.51 s |
| `kiyoka_2` | `detail` | [link](/results/kiyoka-2-detail.svg) | 2121.9 KB | 3884 | 13.65 s |
| `kiyoka_2` | `binary_ink` | [link](/results/kiyoka-2-binary-ink.svg) | 40.2 KB | 9 | 0.18 s |

## Folder layout

Typical output layout:

```text
output/
  preprocessed/
    image1.nobg.png
  vtracer/
    experiments/
      image1.nobg__default.svg
      image1.nobg__clean.svg
      experiment_summary.csv
      report.md
```

## Recommended workflow

1. Run experiments after any preset change.
2. Build report.
3. Compare a baseline and candidate rows side by side.
4. Store the report in local artifacts for that run.

## Keeping reports auditable

Keep `experiment_summary.csv` and scripts versioned in git while avoiding large source images/artifacts.
Keep only a curated set of public sample SVGs under `docs/public/results/` so the docs stay lightweight.
