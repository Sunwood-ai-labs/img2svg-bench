# Metrics and Outputs

## Current metric set

The default report currently contains:

- runtime (seconds)
- output SVG byte size
- SVG path count
- unique fill count
- output width and height
- generated artifact file names

These metrics are suitable for ranking throughput and structural complexity.

## How to read the CSV

`output/vtracer/experiments/experiment_summary.csv` has one row per image, preset, and run condition.

Recommended reading pattern:

1. sort by size + runtime to find efficient settings
2. scan fill/path counts for topology complexity
3. use report previews to confirm visual fidelity

## Current limits

- no structural image-level ground-truth fidelity score yet
- no editability quality score yet
- no cross-run hardware normalization by default

All limits are intentionally documented so future additions can target gaps explicitly.
