from __future__ import annotations

import argparse
import subprocess
from datetime import date
from pathlib import Path

import build_tradingagents_dashboard_data as dashboard_builder
from tradingagents_automation_support import python_command_for_tradingagents


WORKSPACE = Path(__file__).resolve().parents[1]
TRADINGAGENTS_ROOT = Path(r"C:\Users\skydiver1118\Documents\Stock Analysis\TradingAgents")
TRADINGAGENTS_PYTHON = TRADINGAGENTS_ROOT / ".venv" / "Scripts" / "python.exe"
GROUNDED_RUNNER = TRADINGAGENTS_ROOT / "scripts" / "run_grounded_tradingagents_pdf.py"
REPORT_PYTHON_CMD, REPORT_ENV, REPORT_PYTHON_LABEL = python_command_for_tradingagents(
    TRADINGAGENTS_PYTHON,
    TRADINGAGENTS_ROOT,
)


def newest_path(paths: list[Path]) -> Path | None:
    existing = [path for path in paths if path.exists()]
    if not existing:
        return None
    return max(existing, key=lambda path: path.stat().st_mtime)


def configure_latest_sources() -> None:
    """Replace stale hard-coded May 2026 inputs with the newest local artifacts available."""
    downloads = Path.home() / "Downloads"
    newest_etrade = newest_path(list(downloads.glob("etrade_*.csv")))
    if newest_etrade:
        dashboard_builder.ETRADE_CSV = newest_etrade

    reports_root = dashboard_builder.TRADINGAGENTS_REPORTS
    newest_snapshot = newest_path(
        [path for path in reports_root.glob("portfolio_decision_snapshots_*") if path.is_dir()]
    )
    if newest_snapshot:
        dashboard_builder.PORTFOLIO_SNAPSHOT_DIR = newest_snapshot

    batch_roots = [path for path in reports_root.glob("full_tradingagents_batch_*") if path.is_dir()]
    newest_batch_root = newest_path(batch_roots)
    if newest_batch_root:
        batch_children = [path for path in newest_batch_root.iterdir() if path.is_dir()]
        dashboard_builder.BATCH_DIR = newest_path(batch_children) or newest_batch_root

    print(f"E*TRADE source: {dashboard_builder.ETRADE_CSV}")
    print(f"Portfolio snapshot: {dashboard_builder.PORTFOLIO_SNAPSHOT_DIR}")
    print(f"Legacy batch fallback: {dashboard_builder.BATCH_DIR}")
    print("Stock-price source: Alpaca Market Data, IEX feed (completed daily bars).")


def symbols() -> list[str]:
    configure_latest_sources()
    return [row["Symbol"].upper() for row in dashboard_builder.merged_watchlist_rows()]


def grounded_report_exists(symbol: str, report_date: str) -> bool:
    expected = (
        dashboard_builder.TRADINGAGENTS_REPORTS
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

    configure_latest_sources()
    failures: list[str] = []
    for symbol in [row["Symbol"].upper() for row in dashboard_builder.merged_watchlist_rows()]:
        should_generate = args.reports == "all" or (
            args.reports == "missing" and not grounded_report_exists(symbol, args.date)
        )
        if should_generate:
            code = run_grounded_report(symbol, args.date)
            if code != 0:
                failures.append(symbol)

    # Build in-process so the dynamically selected latest source paths above are preserved.
    dashboard_builder.main()

    if failures:
        print(f"Dashboard refreshed, but report generation failed for: {', '.join(failures)}")
        return 2

    print("Dashboard refresh complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
