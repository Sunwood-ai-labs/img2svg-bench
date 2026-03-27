# Benchmark Concepts

## Core idea

This repository compares image-to-SVG workflows by keeping each step explicit:

1. input normalization
2. optional preprocessing
3. conversion preset execution
4. metric collection
5. report assembly

This removes “manual tuning drift” and makes side-by-side results auditable.

## What counts as a benchmark run

One run is a combination of:

- source image
- preprocessing method (`none` or background-stripped)
- runner (`VTracer`)
- preset name

## Why CSV + Markdown

CSV gives stable machine-readable rows for automation and charts.
Markdown gives quick human review and visual references for SVG quality.

## Extending the benchmark design

Add new runners by following the same contract:

- accept image inputs from CLI
- emit generated outputs to a deterministic folder
- write timing and complexity metrics to structured records
- include enough metadata to rerun the exact experiment

Keep this contract stable and existing scripts remain easy to compare across tools.
