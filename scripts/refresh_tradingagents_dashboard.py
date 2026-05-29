from __future__ import annotations

import argparse
import subprocess
from datetime import date
from pathlib import Path

from build_tradingagents_dashboard_data import (
    TRADINGAGENTS_REPORTS,
    merged_watchlist_rows,
)
from tradingagents_automation_support import python_command_for_tradingagents


WORKSPACE = Path(__file__).resolve().parents[1]
TRADINGAGENTS_ROOT = Path(r"C:\Users\skydiver1118\Documents\Stock Analysis\TradingAgents")
TRADINGAGENTS_PYTHON = TRADINGAGENTS_ROOT / ".venv" / "Scripts" / "python.exe"
GROUNDED_RUNNER = TRADINGAGENTS_ROOT / "scripts" / "run_grounded_tradingagents_pdf.py"
BUILD_DATA = WORKSPACE / "scripts" / "build_tradingagents_dashboard_data.py"
REPORT_PYTHON_CMD, REPORT_ENV, REPORT_PYTHON_LABEL = python_command_for_tradingagents(
    TRADINGAGENTS_PYTHON,
    TRADINGAGENTS_ROOT,
)


def symbols() -> list[str]:
    return [row["Symbol"].upper() for row in merged_watchlist_rows()]


def grounded_report_exists(symbol: str, report_date: str) -> bool:
    expected = (
        TRADINGAGENTS_REPORTS
        / f"{symbol}_{report_date}_grounded_full_report"
        / f"{symbol}_TradingAgents_Full_Report_{report_date}.md"
    )
    return expected.exists()


def run_grounded_report(symbol: str, report_date: str) -> int:
    cmd = [
        *REPORT_PYTHON_CMD,
        str(GROUNDED_RUNNER),
        "--symbol",
        symbol,
        "--date",
        report_date,
    ]
    print(f"Generating {symbol} grounded TradingAgents report with {REPORT_PYTHON_LABEL}...")
    completed = subprocess.run(cmd, cwd=TRADINGAGENTS_ROOT, env=REPORT_ENV)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh the TradingAgents dashboard data bundle.")
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help=(
            "TradingAgents/yfinance end date to request. yfinance treats this as an exclusive daily-bar end date, "
            "so the default morning run usually captures the prior completed market session."
        ),
    )
    parser.add_argument(
        "--reports",
        choices=["missing", "all", "none"],
        default="missing",
        help="Whether to generate missing reports, regenerate all reports, or only rebuild dashboard data.",
    )
    args = parser.parse_args()

    failures: list[str] = []
    for symbol in symbols():
        should_generate = args.reports == "all" or (
            args.reports == "missing" and not grounded_report_exists(symbol, args.date)
        )
        if should_generate:
            code = run_grounded_report(symbol, args.date)
            if code != 0:
                failures.append(symbol)

    build = subprocess.run([*REPORT_PYTHON_CMD, str(BUILD_DATA)], cwd=WORKSPACE, env=REPORT_ENV)
    if build.returncode != 0:
        return build.returncode

    if failures:
        print(f"Dashboard refreshed, but report generation failed for: {', '.join(failures)}")
        return 2

    print("Dashboard refresh complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
