from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG_DIR = ROOT / "output" / "omnisvg" / "logs"
DEFAULT_EXPERIMENT_DIR = ROOT / "output" / "omnisvg" / "experiments"
DEFAULT_SUMMARY = DEFAULT_EXPERIMENT_DIR / "attempt_summary.csv"
DEFAULT_REPORT = DEFAULT_EXPERIMENT_DIR / "report.md"

FIELD_PATTERNS = {
    "task": re.compile(r"^Task:\s*(.+)$", re.MULTILINE),
    "model_size": re.compile(r"^Model Size:\s*(.+)$", re.MULTILINE),
    "input_path": re.compile(r"^Input:\s*(.+)$", re.MULTILINE),
    "output_dir": re.compile(r"^Output:\s*(.+)$", re.MULTILINE),
    "num_candidates": re.compile(r"^Num Candidates:\s*(.+)$", re.MULTILINE),
    "max_length": re.compile(r"^Max Length:\s*(.+)$", re.MULTILINE),
    "success_count": re.compile(r"Success:\s*(\d+)\s*/\s*(\d+)"),
    "failed_count": re.compile(r"Failed:\s*(\d+)\s*/\s*(\d+)"),
}

FAIL_SECONDS_RE = re.compile(r"Failed to generate valid SVG \(([\d.]+)s\)")
SUCCESS_SECONDS_RE = re.compile(r"Generated valid SVG.*?\(([\d.]+)s\)")
NO_TOKEN_RE = re.compile(r"Candidate \d+ yielded no SVG token groups")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local OmniSVG attempt report from run logs.")
    parser.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR), help="Directory containing OmniSVG log files.")
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY), help="Output CSV summary path.")
    parser.add_argument("--output", default=str(DEFAULT_REPORT), help="Output Markdown report path.")
    return parser.parse_args()


def first_match(text: str, pattern: re.Pattern[str]) -> str:
    match = pattern.search(text)
    if not match:
        return ""
    if len(match.groups()) == 1:
        return match.group(1).strip()
    return "|".join(group.strip() for group in match.groups())


def classify_error(text: str, success_count: int) -> str:
    if success_count > 0:
        return "success"
    if "No chat template is set" in text:
        return "chat_template_missing"
    if "Trying to set a tensor of shape" in text:
        return "generation_shape_mismatch"
    if "Candidate 0 yielded no SVG token groups" in text or NO_TOKEN_RE.search(text):
        return "no_svg_token_groups"
    if "Failed to generate valid SVG" in text:
        return "no_valid_svg"
    if "Traceback" in text:
        return "runtime_error"
    return "unknown"


def load_row(log_path: Path) -> dict[str, str]:
    raw = log_path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    if text.count("\x00") > max(8, len(text) // 8):
        text = raw.decode("utf-16", errors="replace")

    row: dict[str, str] = {"log_file": log_path.name}
    for key, pattern in FIELD_PATTERNS.items():
        row[key] = first_match(text, pattern)

    success_count = 0
    if row["success_count"]:
        success_count = int(row["success_count"].split("|")[0])

    failed_count = 0
    if row["failed_count"]:
        failed_count = int(row["failed_count"].split("|")[0])

    row["loaded_model"] = "yes" if "models loaded successfully" in text else "no"
    row["run_finished"] = "yes" if "Done!" in text else "no"
    row["error_kind"] = classify_error(text, success_count)
    row["no_svg_token_groups"] = str(len(NO_TOKEN_RE.findall(text)))

    seconds = first_match(text, SUCCESS_SECONDS_RE) or first_match(text, FAIL_SECONDS_RE)
    row["seconds"] = seconds or ""

    output_dir = Path(row["output_dir"]) if row["output_dir"] else None
    output_svg_count = 0
    if output_dir and output_dir.exists():
        output_svg_count = len(list(output_dir.glob("*.svg")))
    row["output_svg_count"] = str(output_svg_count)

    input_name = Path(row["input_path"]).name if row["input_path"] else ""
    row["input_name"] = input_name

    if success_count > 0 and output_svg_count > 0:
        status = "success"
    elif failed_count > 0:
        status = "failed"
    elif row["run_finished"] == "yes":
        status = "completed_without_outputs"
    else:
        status = "incomplete"
    row["status"] = status

    return row


def load_rows(log_dir: Path) -> list[dict[str, str]]:
    rows = [load_row(path) for path in sorted(log_dir.glob("*.log"))]
    rows.sort(key=lambda row: (row["model_size"], row["input_name"], row["log_file"]))
    return rows


def write_summary(rows: list[dict[str, str]], summary_path: Path) -> None:
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "log_file",
        "status",
        "error_kind",
        "model_size",
        "task",
        "input_name",
        "input_path",
        "output_dir",
        "num_candidates",
        "max_length",
        "seconds",
        "loaded_model",
        "run_finished",
        "success_count",
        "failed_count",
        "no_svg_token_groups",
        "output_svg_count",
    ]
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def report_table(rows: list[dict[str, str]]) -> str:
    lines = [
        "| Log | Model | Input | Status | Error | Max tokens | Candidates | Time | SVGs |",
        "| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| [link](../logs/{row['log_file']}) | `{row['model_size']}` | `{row['input_name']}` | "
            f"`{row['status']}` | `{row['error_kind']}` | {row['max_length'] or '-'} | "
            f"{row['num_candidates'] or '-'} | {row['seconds'] or '-'} | {row['output_svg_count']} |"
        )
    return "\n".join(lines)


def quick_take(rows: list[dict[str, str]]) -> list[str]:
    lines: list[str] = []
    if any(row["model_size"] == "4B" and row["loaded_model"] == "yes" for row in rows):
        lines.append("- `4B` loaded successfully on this machine under a non-standard local setup.")
    if any(row["error_kind"] == "no_svg_token_groups" for row in rows):
        lines.append("- The tested `4B` runs produced no decodable SVG token groups, including one official example image.")
    if any(row["model_size"] == "8B" and row["loaded_model"] == "yes" for row in rows):
        lines.append("- `8B` also loaded under offload, but generation failed with a tensor shape mismatch before any SVG was saved.")
    if any(row["error_kind"] == "chat_template_missing" for row in rows):
        lines.append("- The first `4B` run hit a `processor.chat_template` compatibility issue and required a local fallback patch.")
    return lines


def build_report(rows: list[dict[str, str]], summary_name: str) -> str:
    parts = [
        "# OmniSVG Attempt Report",
        "",
        "This report summarizes local OmniSVG 1.1 smoke tests captured from raw logs.",
        "",
        "## Scope",
        "",
        "- Runner: local clone of `OmniSVG/OmniSVG` under `.tmp/OmniSVG`.",
        "- Python env: `UV`-managed `.venv-omnisvg310` on Windows.",
        "- Inputs: local `kiyoka` images plus one official example image.",
        "- Goal: determine whether `4B` and `8B` can be loaded and produce valid SVG outputs on this machine.",
        "",
        "## Quick Take",
        "",
        *quick_take(rows),
        "",
        f"- [summary CSV](./{summary_name})",
        "",
        "## Attempt Matrix",
        "",
        report_table(rows),
        "",
        "## Notes",
        "",
        "- These runs were non-standard local experiments, not an official benchmark reproduction.",
        "- The local OmniSVG clone used compatibility patches for Windows rendering and chat-template fallback.",
        "- `8B` required an additional local patch to bypass `mean_resizing` with meta-device offload.",
        "- No OmniSVG SVG outputs were successfully saved in these smoke tests.",
        "",
    ]
    return "\n".join(parts)


def main() -> None:
    args = parse_args()
    log_dir = Path(args.log_dir)
    summary_path = Path(args.summary)
    output_path = Path(args.output)
    rows = load_rows(log_dir)
    write_summary(rows, summary_path)
    report = build_report(rows, summary_path.name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote {summary_path}")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
