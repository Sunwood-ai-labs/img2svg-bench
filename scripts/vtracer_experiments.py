from __future__ import annotations

import argparse
import csv
import io
import re
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
import vtracer


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "output" / "vtracer" / "experiments"


@dataclass(frozen=True)
class Preset:
    name: str
    description: str
    kwargs: dict[str, object]


PRESETS = [
    Preset("default", "VTracer default settings", {}),
    Preset(
        "clean",
        "More speckle cleanup and simpler curves",
        {
            "filter_speckle": 10,
            "color_precision": 6,
            "layer_difference": 20,
            "corner_threshold": 75,
            "length_threshold": 6.0,
            "splice_threshold": 60,
            "path_precision": 2,
        },
    ),
    Preset(
        "detail",
        "Keep more detail and tighter curves",
        {
            "filter_speckle": 2,
            "color_precision": 8,
            "layer_difference": 12,
            "corner_threshold": 50,
            "length_threshold": 3.5,
            "max_iterations": 16,
            "splice_threshold": 35,
            "path_precision": 4,
        },
    ),
    Preset(
        "cutout",
        "Cutout hierarchy to emphasize layered regions",
        {
            "hierarchical": "cutout",
            "filter_speckle": 6,
            "color_precision": 6,
            "layer_difference": 16,
            "path_precision": 3,
        },
    ),
    Preset(
        "polygon",
        "Polygon mode for a more faceted look",
        {
            "mode": "polygon",
            "filter_speckle": 6,
            "color_precision": 6,
            "layer_difference": 18,
            "corner_threshold": 85,
            "length_threshold": 5.5,
            "splice_threshold": 55,
            "path_precision": 2,
        },
    ),
    Preset(
        "poster",
        "Aggressive simplification for fewer shapes and colors",
        {
            "filter_speckle": 12,
            "color_precision": 5,
            "layer_difference": 24,
            "corner_threshold": 80,
            "length_threshold": 7.0,
            "max_iterations": 8,
            "splice_threshold": 70,
            "path_precision": 1,
        },
    ),
    Preset(
        "binary_ink",
        "Line-art style binary trace",
        {
            "colormode": "binary",
            "mode": "spline",
            "filter_speckle": 10,
            "corner_threshold": 70,
            "length_threshold": 6.0,
            "max_iterations": 12,
            "splice_threshold": 45,
            "path_precision": 2,
        },
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run VTracer presets on one or more input images.")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input image files.")
    parser.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Directory for SVG outputs and the summary CSV.",
    )
    parser.add_argument(
        "--summary-name",
        default="experiment_summary.csv",
        help="Filename for the generated CSV summary inside out-dir.",
    )
    parser.add_argument(
        "--presets",
        nargs="*",
        default=None,
        help="Optional subset of preset names to run.",
    )
    return parser.parse_args()


def selected_presets(names: list[str] | None) -> list[Preset]:
    if not names:
        return PRESETS
    wanted = set(names)
    presets = [preset for preset in PRESETS if preset.name in wanted]
    missing = wanted - {preset.name for preset in presets}
    if missing:
        raise SystemExit(f"Unknown preset(s): {', '.join(sorted(missing))}")
    return presets


def detect_format(img_bytes: bytes) -> str:
    with Image.open(io.BytesIO(img_bytes)) as img:
        img_format = (img.format or "").lower()
    if not img_format:
        raise SystemExit("Could not detect image format.")
    if img_format == "jpeg":
        return "jpg"
    return img_format


def slugify(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", path.stem)


def path_count(svg_text: str) -> int:
    return len(re.findall(r"<path\b", svg_text))


def unique_fill_count(svg_text: str) -> int:
    fills = set(re.findall(r'fill="([^"]+)"', svg_text))
    return len(fills)


def root_size(svg_path: Path) -> tuple[str, str]:
    root = ET.parse(svg_path).getroot()
    return root.attrib.get("width", ""), root.attrib.get("height", "")


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_csv = out_dir / args.summary_name
    presets = selected_presets(args.presets)

    rows: list[dict[str, object]] = []
    for input_arg in args.inputs:
        src = Path(input_arg)
        if not src.exists():
            raise FileNotFoundError(f"Missing input: {src}")

        img_bytes = src.read_bytes()
        img_format = detect_format(img_bytes)
        source_slug = slugify(src)

        for preset in presets:
            dst = out_dir / f"{source_slug}__{preset.name}.svg"
            started = time.perf_counter()
            svg = vtracer.convert_raw_image_to_svg(
                img_bytes,
                img_format=img_format,
                **preset.kwargs,
            )
            elapsed = time.perf_counter() - started
            dst.write_text(svg, encoding="utf-8")
            width, height = root_size(dst)
            row = {
                "source_input": src.name,
                "source_path": str(src),
                "preset": preset.name,
                "description": preset.description,
                "svg_file": dst.name,
                "seconds": f"{elapsed:.2f}",
                "bytes": dst.stat().st_size,
                "path_count": path_count(svg),
                "unique_fills": unique_fill_count(svg),
                "width": width,
                "height": height,
                "kwargs": preset.kwargs,
            }
            rows.append(row)
            print(
                f"{src.name} [{preset.name}] -> {dst.name} "
                f"({elapsed:.2f}s, {row['bytes']} bytes, {row['path_count']} paths)"
            )

    with summary_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "source_input",
                "source_path",
                "preset",
                "description",
                "svg_file",
                "seconds",
                "bytes",
                "path_count",
                "unique_fills",
                "width",
                "height",
                "kwargs",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSummary written to {summary_csv}")


if __name__ == "__main__":
    main()
