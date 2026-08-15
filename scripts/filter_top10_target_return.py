from __future__ import annotations

import argparse
import csv
from pathlib import Path


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row.get(col, "") for col in columns) + " |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", default="reports/cup_handle_sp500_strict/sp500_cup_handle_pattern_in_force.csv")
    parser.add_argument("--output-dir", default="reports/cup_handle_sp500_strict")
    parser.add_argument("--threshold", type=float, default=30.0)
    args = parser.parse_args()

    input_csv = Path(args.input_csv)
    output_dir = Path(args.output_dir)
    rows = list(csv.DictReader(input_csv.open(newline="", encoding="utf-8")))
    keepers = [row for row in rows if float(row["TargetReturnPct"]) > args.threshold]

    filtered_csv = output_dir / "sp500_cup_handle_top10_target_return_gt30.csv"
    if keepers:
        with filtered_csv.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(keepers[0].keys()))
            writer.writeheader()
            writer.writerows(keepers)
    else:
        filtered_csv.write_text("", encoding="utf-8")

    columns = [
        "Symbol",
        "Company",
        "Score",
        "LatestClose",
        "BreakoutLevel",
        "MeasuredTarget",
        "TargetReturnPct",
        "HandleLow",
        "CupDepthPct",
        "HandleDepthPctOfCup",
    ]
    report_lines = [
        "# Top-10 Cup-And-Handle Candidates With Target Return > 30%",
        "",
        f"Filter: `TargetReturnPct > {args.threshold}%`, where `TargetReturnPct = MeasuredTarget / BreakoutLevel - 1`.",
        f"Source file: `{input_csv.name}`.",
        f"Kept: `{len(keepers)}` of `{len(rows)}` top-10 candidates.",
        "",
    ]
    if keepers:
        report_lines.append(markdown_table(keepers, columns))
        report_lines += ["", "## Charts", ""]
        for idx, row in enumerate(keepers, start=1):
            symbol = row["YahooSymbol"] or row["Symbol"]
            report_lines += [
                f"## {idx}. {row['Symbol']} - {row['Company']}",
                "",
                f"Score: `{row['Score']}`. Breakout: `{row['BreakoutLevel']}`. Target: `{row['MeasuredTarget']}`. Target return: `{float(row['TargetReturnPct']):.2f}%`.",
                "",
                f"![{row['Symbol']} cup and handle](C:/Users/skydiver1118/Documents/New%20project/reports/cup_handle_sp500_strict/charts/{symbol}_weekly_cup_handle_context.png)",
                "",
            ]
    else:
        report_lines.append("No candidates passed the filter.")

    filtered_report = output_dir / "sp500_cup_handle_top10_target_return_gt30.md"
    filtered_gallery = output_dir / "top10_target_return_gt30_chart_gallery.md"
    text = "\n".join(report_lines) + "\n"
    filtered_report.write_text(text, encoding="utf-8")
    filtered_gallery.write_text(text, encoding="utf-8")

    print(f"input_rows={len(rows)}")
    print(f"kept={len(keepers)}")
    print(f"csv={filtered_csv}")
    print(f"report={filtered_report}")
    print(f"gallery={filtered_gallery}")
    if keepers:
        print([(row["Symbol"], row["TargetReturnPct"]) for row in keepers])


if __name__ == "__main__":
    main()
