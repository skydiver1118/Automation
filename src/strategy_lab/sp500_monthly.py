from __future__ import annotations

import argparse
import calendar
import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from src.strategy_lab.sp500_top5 import (
    calculate_summary,
    load_or_fetch_prices,
    load_sp500_constituents,
    run_top_n_backtest,
    save_constituents,
)


@dataclass(frozen=True)
class MonthlyRun:
    month: str
    start: date
    end: date
    summary: dict[str, str | int | float]


def month_bounds(year: int, month: int) -> tuple[date, date]:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)


def format_pct(value: object) -> str:
    return f"{float(value):.2%}"


def run_monthly_backtests(
    year: int,
    through_month: int,
    lookback_days: int,
    max_positions: int,
    transaction_cost_bps: float,
    data_dir: Path,
    refresh: bool,
) -> list[MonthlyRun]:
    first_start, _ = month_bounds(year, 1)
    _, final_end = month_bounds(year, through_month)
    fetch_start = first_start - timedelta(days=max(lookback_days * 3, 260))

    constituents_path = data_dir / "sp500_constituents.csv"
    prices_path = data_dir / f"adjusted_open_close_{fetch_start.isoformat()}_{final_end.isoformat()}.csv"

    if constituents_path.exists() and not refresh:
        constituents = pd.read_csv(constituents_path)
    else:
        constituents = load_sp500_constituents()
        save_constituents(constituents, constituents_path)

    tickers = constituents["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(prices_path, tickers, fetch_start, final_end, refresh)

    runs: list[MonthlyRun] = []
    for month in range(1, through_month + 1):
        start, end = month_bounds(year, month)
        result = run_top_n_backtest(
            prices=prices,
            start=start,
            end=end,
            lookback_days=lookback_days,
            max_positions=max_positions,
            transaction_cost_bps=transaction_cost_bps,
        )
        runs.append(
            MonthlyRun(
                month=f"{year}-{month:02d}",
                start=start,
                end=end,
                summary=calculate_summary(result),
            )
        )
    return runs


def write_monthly_csv(runs: list[MonthlyRun], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "month",
        "requested_start",
        "requested_end",
        "actual_start",
        "actual_end",
        "trading_days",
        "total_return",
        "cagr",
        "max_drawdown",
        "sharpe",
        "buy_trades",
        "sell_trades",
        "final_holdings",
        "ticker_count",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for run in runs:
            row = {
                "month": run.month,
                "requested_start": run.start.isoformat(),
                "requested_end": run.end.isoformat(),
                "actual_start": run.summary["start"],
                "actual_end": run.summary["end"],
                "trading_days": run.summary["trading_days"],
                "total_return": run.summary["total_return"],
                "cagr": run.summary["cagr"],
                "max_drawdown": run.summary["max_drawdown"],
                "sharpe": run.summary["sharpe"],
                "buy_trades": run.summary["buy_trades"],
                "sell_trades": run.summary["sell_trades"],
                "final_holdings": run.summary["final_holdings"],
                "ticker_count": run.summary["ticker_count"],
            }
            writer.writerow(row)


def write_monthly_markdown(runs: list[MonthlyRun], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 2026 Monthly S&P 500 Top-5 Momentum Backtests",
        "",
        "Rules: rank after each close by 126-trading-day adjusted-close momentum, execute exits/entries at the next trading day's open, hold at most five 20% slots.",
        "",
        "| Month | Requested Period | Actual Trading Period | Return | Max DD | Sharpe | Buys | Sells | Final Holdings |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for run in runs:
        sharpe = run.summary["sharpe"]
        sharpe_text = "" if sharpe == "" else f"{float(sharpe):.2f}"
        lines.append(
            "| "
            f"{run.month} | "
            f"{run.start.isoformat()} to {run.end.isoformat()} | "
            f"{run.summary['start']} to {run.summary['end']} | "
            f"{format_pct(run.summary['total_return'])} | "
            f"{format_pct(run.summary['max_drawdown'])} | "
            f"{sharpe_text} | "
            f"{run.summary['buy_trades']} | "
            f"{run.summary['sell_trades']} | "
            f"{run.summary['final_holdings']} |"
        )
    lines.extend(
        [
            "",
            "Note: CAGR is intentionally omitted from this table because one-month annualization is noisy and easy to overread.",
            "This uses current S&P 500 constituents, which is fine for a 2026 smoke test but not a point-in-time constituent backtest.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run S&P 500 top-5 momentum backtests by calendar month.")
    parser.add_argument("--year", type=int, default=2026)
    parser.add_argument("--through-month", type=int, default=date.today().month)
    parser.add_argument("--lookback-days", type=int, default=126)
    parser.add_argument("--max-positions", type=int, default=5)
    parser.add_argument("--transaction-cost-bps", type=float, default=0.0)
    parser.add_argument("--data-dir", type=Path, default=Path("data/sp500_top5"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    runs = run_monthly_backtests(
        year=args.year,
        through_month=args.through_month,
        lookback_days=args.lookback_days,
        max_positions=args.max_positions,
        transaction_cost_bps=args.transaction_cost_bps,
        data_dir=args.data_dir,
        refresh=args.refresh,
    )
    write_monthly_csv(runs, args.report_dir / f"sp500_top5_monthly_{args.year}.csv")
    write_monthly_markdown(runs, args.report_dir / f"sp500_top5_monthly_{args.year}.md")

    for run in runs:
        print(
            f"{run.month}: return={format_pct(run.summary['total_return'])}, "
            f"max_dd={format_pct(run.summary['max_drawdown'])}, "
            f"buys={run.summary['buy_trades']}, sells={run.summary['sell_trades']}, "
            f"final={run.summary['final_holdings']}"
        )


if __name__ == "__main__":
    main()
