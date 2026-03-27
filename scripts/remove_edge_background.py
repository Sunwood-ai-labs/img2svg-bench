from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "output" / "preprocessed"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove bright border-connected background regions and save transparent PNGs."
    )
    parser.add_argument("--inputs", nargs="+", required=True, help="Input image files.")
    parser.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Directory for background-removed PNG outputs.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=45,
        help="RGB distance threshold for flood-filling the bright edge background.",
    )
    parser.add_argument(
        "--min-brightness",
        type=int,
        default=220,
        help="Minimum average brightness used to classify background samples.",
    )
    return parser.parse_args()


def remove_background(src: Path, out_dir: Path, threshold: int, min_brightness: int) -> None:
    img = Image.open(src).convert("RGB")
    w, h = img.size
    px = img.load()

    sample_coords = [
        (0, 0),
        (w - 1, 0),
        (0, h - 1),
        (w - 1, h - 1),
        (w // 2, 0),
        (0, h // 2),
        (w - 1, h // 2),
    ]
    samples = [px[x, y] for x, y in sample_coords]
    bright = [color for color in samples if sum(color) / 3 >= min_brightness]
    if not bright:
        bright = samples
    bg = tuple(round(sum(color[i] for color in bright) / len(bright)) for i in range(3))

    def close_to_bg(rgb: tuple[int, int, int]) -> bool:
        return sum(abs(rgb[i] - bg[i]) for i in range(3)) <= threshold and (sum(rgb) / 3) >= (
            min_brightness - 10
        )

    visited = bytearray(w * h)
    queue: deque[tuple[int, int]] = deque()

    def push(x: int, y: int) -> None:
        idx = y * w + x
        if not visited[idx] and close_to_bg(px[x, y]):
            visited[idx] = 1
            queue.append((x, y))

    for x in range(w):
        push(x, 0)
        push(x, h - 1)
    for y in range(h):
        push(0, y)
        push(w - 1, y)

    while queue:
        x, y = queue.popleft()
        if x > 0:
            idx = y * w + (x - 1)
            if not visited[idx] and close_to_bg(px[x - 1, y]):
                visited[idx] = 1
                queue.append((x - 1, y))
        if x < w - 1:
            idx = y * w + (x + 1)
            if not visited[idx] and close_to_bg(px[x + 1, y]):
                visited[idx] = 1
                queue.append((x + 1, y))
        if y > 0:
            idx = (y - 1) * w + x
            if not visited[idx] and close_to_bg(px[x, y - 1]):
                visited[idx] = 1
                queue.append((x, y - 1))
        if y < h - 1:
            idx = (y + 1) * w + x
            if not visited[idx] and close_to_bg(px[x, y + 1]):
                visited[idx] = 1
                queue.append((x, y + 1))

    rgba = Image.new("RGBA", (w, h))
    out_px = rgba.load()
    removed = 0
    for y in range(h):
        row = y * w
        for x in range(w):
            r, g, b = px[x, y]
            if visited[row + x]:
                out_px[x, y] = (r, g, b, 0)
                removed += 1
            else:
                out_px[x, y] = (r, g, b, 255)

    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / f"{src.stem}.nobg.png"
    rgba.save(dst)
    print(
        f"{src.name} -> {dst.name} "
        f"(removed {removed}/{w * h} pixels, {removed / (w * h):.2%}, bg={bg})"
    )


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    for input_arg in args.inputs:
        src = Path(input_arg)
        if not src.exists():
            raise FileNotFoundError(f"Missing input: {src}")
        remove_background(src, out_dir, args.threshold, args.min_brightness)


if __name__ == "__main__":
    main()
