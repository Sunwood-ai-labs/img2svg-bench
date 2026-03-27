# Reports

## What is generated

`scripts/build_vtracer_report.py` generates `output/vtracer/experiments/report.md` by reading:

- `output/vtracer/experiments/experiment_summary.csv`
- generated SVG artifacts under `output/vtracer/experiments/`

The report is meant for fast review and contains embedded SVG snippets for each candidate.

## Published sample gallery

The repository also checks in a small set of representative SVG outputs under `docs/public/results/` so the public README and docs can show real generated results without relying on ignored local artifacts.

| Sample A / clean | Sample A / poster |
| --- | --- |
| ![Sample A clean](/results/sample-a-clean.svg) | ![Sample A poster](/results/sample-a-poster.svg) |
| `129.7 KB` / `93 paths` / `1.30 s` | `61.1 KB` / `36 paths` / `0.44 s` |

| Sample B / clean | Sample B / poster |
| --- | --- |
| ![Sample B clean](/results/sample-b-clean.svg) | ![Sample B poster](/results/sample-b-poster.svg) |
| `210.0 KB` / `123 paths` / `0.84 s` | `108.2 KB` / `46 paths` / `0.51 s` |

These published samples are intentionally compact. Use the locally generated `report.md` to inspect the full preset matrix.

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
