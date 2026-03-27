# Contributing

## Intended contributions

- add new conversion runners
- improve preprocessing options
- expand metric definitions
- improve docs and onboarding

## Adding a new runner

1. Add a runner script or module under `scripts/` following existing style.
2. Accept image inputs from CLI and expose deterministic outputs.
3. Extend experiment orchestration with clear preset labels and metadata fields.
4. Ensure outputs are placed under `output/` so the benchmark report can ingest them.

## Documentation expectations

- add or update English docs
- keep mirrored Japanese docs under `docs/ja/`
- keep command examples compatible with UV-powered Python workflows

## Review workflow

Open PRs with:

- clear purpose and scope
- sample command output (or snippet)
- explicit note on backward-compatibility for existing outputs
