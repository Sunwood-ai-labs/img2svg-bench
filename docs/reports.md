# Reports

## What is generated

`scripts/build_vtracer_report.py` generates `output/vtracer/experiments/report.md` by reading:

- `output/vtracer/experiments/experiment_summary.csv`
- generated SVG artifacts under `output/vtracer/experiments/`

The report is meant for fast review and contains embedded SVG snippets for each candidate.

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
