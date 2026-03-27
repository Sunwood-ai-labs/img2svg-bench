---
layout: home

hero:
  name: img2svg-bench
  text: Benchmark image-to-SVG pipelines with reproducible local runs
  tagline: Compare tools, presets, and preprocessing steps with UV-managed scripts, Markdown reports, and GitHub Pages docs.
  image:
    src: /logo.svg
    alt: img2svg-bench logo
  actions:
    - theme: brand
      text: Getting Started
      link: /getting-started
    - theme: alt
      text: GitHub
      link: https://github.com/Sunwood-ai-labs/img2svg-bench

features:
  - title: Local-first benchmarking
    details: Keep private images local, run experiments on your machine, and commit only the benchmark harness.
  - title: Reproducible reports
    details: Generate CSV summaries and Markdown reports with embedded SVG previews for direct comparison.
  - title: Extensible runner design
    details: Start with VTracer today and grow toward broader image-to-SVG runner coverage over time.
---

## What This Project Measures

`img2svg-bench` currently captures a practical first layer of SVG benchmark metrics:

- runtime per preset
- output file size
- path count
- unique fill count
- output dimensions

The project is designed to grow from a strong baseline into a broader benchmark system for tools, datasets, and evaluation methods.
