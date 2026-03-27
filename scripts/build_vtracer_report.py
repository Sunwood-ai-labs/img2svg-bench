from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPERIMENT_DIR = ROOT / "output" / "vtracer" / "experiments"
DEFAULT_SUMMARY = DEFAULT_EXPERIMENT_DIR / "experiment_summary.csv"
DEFAULT_REPORT = DEFAULT_EXPERIMENT_DIR / "report.md"
HERO_PRESETS = ["poster", "clean", "detail", "binary_ink"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Markdown report from an experiment summary CSV.")
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY), help="Path to experiment_summary.csv.")
    parser.add_argument("--output", default=str(DEFAULT_REPORT), help="Output markdown report path.")
    parser.add_argument(
        "--title",
        default="VTracer Experiment Report",
        help="Title for the generated Markdown report.",
    )
    return parser.parse_args()


def load_rows(summary_path: Path) -> list[dict[str, str]]:
    with summary_path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def fmt_kb(num_bytes: str) -> str:
    return f"{int(num_bytes) / 1024:.1f} KB"


def source_value(row: dict[str, str]) -> str:
    return row.get("source_input") or row.get("source_png") or "unknown"


def row_map(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    return {(source_value(row), row["preset"]): row for row in rows}


def ordered_sources(rows: list[dict[str, str]]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for row in rows:
        source = source_value(row)
        if source not in seen:
            seen.add(source)
            ordered.append(source)
    return ordered


def ordered_presets(rows: list[dict[str, str]]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for row in rows:
        preset = row["preset"]
        if preset not in seen:
            seen.add(preset)
            ordered.append(preset)
    return ordered


def aggregate_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "## Aggregate Table",
        "",
        "| Source | Preset | Time | Size | Paths | Unique fills |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| `{source_value(row)}` | `{row['preset']}` | {row['seconds']} s | "
            f"{fmt_kb(row['bytes'])} | {row['path_count']} | {row['unique_fills']} |"
        )
    lines.append("")
    return "\n".join(lines)


def image_section(
    source_input: str,
    presets: list[str],
    lookup: dict[tuple[str, str], dict[str, str]],
) -> str:
    hero_presets = [preset for preset in HERO_PRESETS if (source_input, preset) in lookup]
    lines: list[str] = [f"## {source_input}", "", "### Rendered Comparison", "", "<table>", "  <tr>"]
    for preset in hero_presets:
        lines.append(f"    <th>{preset}</th>")
    lines.append("  </tr>")
    lines.append("  <tr>")
    for preset in hero_presets:
        row = lookup[(source_input, preset)]
        lines.append(
            "    <td>"
            f"<img src=\"./{row['svg_file']}\" width=\"240\" alt=\"{source_input} {preset}\" />"
            "</td>"
        )
    lines.append("  </tr>")
    lines.append("  <tr>")
    for preset in hero_presets:
        row = lookup[(source_input, preset)]
        lines.append(
            "    <td>"
            f"`{fmt_kb(row['bytes'])}` / `{row['path_count']} paths` / `{row['seconds']} s`"
            "</td>"
        )
    lines.append("  </tr>")
    lines.append("</table>")
    lines.append("")
    lines.append("### All Presets")
    lines.append("")
    lines.append("| Preset | SVG | Time | Size | Paths | Unique fills |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: |")
    for preset in presets:
        row = lookup.get((source_input, preset))
        if not row:
            continue
        lines.append(
            f"| `{preset}` | [link](./{row['svg_file']}) | {row['seconds']} s | "
            f"{fmt_kb(row['bytes'])} | {row['path_count']} | {row['unique_fills']} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_report(rows: list[dict[str, str]], title: str, summary_name: str) -> str:
    lookup = row_map(rows)
    sources = ordered_sources(rows)
    presets = ordered_presets(rows)
    parts = [
        f"# {title}",
        "",
        "Generated from local inputs and rendered SVG outputs.",
        "",
        f"- [summary CSV](./{summary_name})",
        "",
        "## Quick Take",
        "",
        "- `clean`: most practical balance in many cases.",
        "- `poster`: light and aggressively simplified.",
        "- `detail`: highest fidelity, but much heavier and slower.",
        "- `binary_ink`: useful for line-art style output.",
        "",
        aggregate_table(rows),
    ]
    for source in sources:
        parts.append(image_section(source, presets, lookup))
    return "\n".join(parts)


def main() -> None:
    args = parse_args()
    summary_path = Path(args.summary)
    output_path = Path(args.output)
    rows = load_rows(summary_path)
    report = build_report(rows, args.title, summary_path.name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
