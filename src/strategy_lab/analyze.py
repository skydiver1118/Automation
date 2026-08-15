from __future__ import annotations

import argparse
from pathlib import Path

from src.strategy_lab.metrics import BacktestMetrics, calculate_metrics
from src.strategy_lab.reporting import analyze_run, format_metrics, write_comparison_csv, write_markdown_report
from src.strategy_lab.trendspider import find_pnl_column, load_backtest_run, load_trade_pnls


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze one or more TrendSpider trade-level backtest CSV exports.")
    parser.add_argument("csv_paths", nargs="+", type=Path, help="Path(s) to TrendSpider export CSV files")
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports"),
        help="Folder for generated comparison reports",
    )
    args = parser.parse_args()

    analyzed_runs = [analyze_run(load_backtest_run(path)) for path in args.csv_paths]
    for analyzed in analyzed_runs:
        print(f"\n== {analyzed.run.label} ==")
        print(format_metrics(analyzed.metrics))

    if len(analyzed_runs) > 1:
        write_comparison_csv(analyzed_runs, args.report_dir / "backtest_comparison.csv")
        write_markdown_report(analyzed_runs, args.report_dir / "backtest_comparison.md")
        print(f"\nWrote comparison reports to {args.report_dir}")


if __name__ == "__main__":
    main()
