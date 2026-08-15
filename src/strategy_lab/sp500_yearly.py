from __future__ import annotations

import argparse
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
class YearlyRun:
    year: int
    start: date
    end: date
    summary: dict[str, str | int | float]


def format_pct(value: object) -> str:
    return f"{float(value):.2%}"


def run_yearly_backtests(
    start_year: int,
    end_year: int,
    lookback_days: int,
    max_positions: int,
    transaction_cost_bps: float,
    sma_filter_days: int | None,
    sma_filter_mode: str,
    score_mode: str,
    skip_days: int,
    volatility_days: int | None,
    confirm_recent_days: int | None,
    data_dir: Path,
    refresh: bool,
) -> list[YearlyRun]:
    first_start = date(start_year, 1, 1)
    final_end = date(end_year, 12, 31)
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

    runs: list[YearlyRun] = []
    for year in range(start_year, end_year + 1):
        start = date(year, 1, 1)
        end = date(year, 12, 31)
        result = run_top_n_backtest(
            prices=prices,
            start=start,
            end=end,
            lookback_days=lookback_days,
            max_positions=max_positions,
            transaction_cost_bps=transaction_cost_bps,
            sma_filter_days=sma_filter_days,
            sma_filter_mode=sma_filter_mode,
            score_mode=score_mode,
            skip_days=skip_days,
            volatility_days=volatility_days,
            confirm_recent_days=confirm_recent_days,
        )
        runs.append(
            YearlyRun(
                year=year,
                start=start,
                end=end,
                summary=calculate_summary(result),
            )
        )
    return runs


def write_yearly_csv(runs: list[YearlyRun], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "year",
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
                "year": run.year,
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


def write_yearly_markdown(
    runs: list[YearlyRun],
    path: Path,
    lookback_days: int,
    sma_filter_days: int | None,
    sma_filter_mode: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sma_text = "none"
    if sma_filter_days is not None:
        sma_text = f"SMA{sma_filter_days} ({sma_filter_mode})"
    lines = [
        "# Annual S&P 500 Top-5 Momentum Backtests",
        "",
        f"Rules: rank after each close by {lookback_days}-trading-day adjusted-close momentum, SMA filter: {sma_text}, execute exits/entries at the next trading day's open, hold at most five 20% slots.",
        "",
        "| Year | Actual Trading Period | Return | Max DD | Sharpe | Buys | Sells | Final Holdings |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for run in runs:
        sharpe = run.summary["sharpe"]
        sharpe_text = "" if sharpe == "" else f"{float(sharpe):.2f}"
        lines.append(
            "| "
            f"{run.year} | "
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
            "Each row is a standalone full-year backtest that starts fresh at the beginning of that year.",
            "This uses current S&P 500 constituents, not point-in-time index membership, so long-horizon results may contain survivorship bias.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run S&P 500 top-5 momentum backtests by full calendar year.")
    parser.add_argument("--start-year", type=int, default=2020)
    parser.add_argument("--end-year", type=int, default=2025)
    parser.add_argument("--lookback-days", type=int, default=126)
    parser.add_argument("--max-positions", type=int, default=5)
    parser.add_argument("--transaction-cost-bps", type=float, default=0.0)
    parser.add_argument("--sma-filter-days", type=int, default=None)
    parser.add_argument("--sma-filter-mode", choices=["universe", "top_n"], default="universe")
    parser.add_argument(
        "--score-mode",
        choices=["raw", "skip", "risk_adjusted", "risk_adjusted_skip"],
        default="raw",
    )
    parser.add_argument("--skip-days", type=int, default=0)
    parser.add_argument("--volatility-days", type=int, default=None)
    parser.add_argument("--confirm-recent-days", type=int, default=None)
    parser.add_argument("--data-dir", type=Path, default=Path("data/sp500_top5"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    runs = run_yearly_backtests(
        start_year=args.start_year,
        end_year=args.end_year,
        lookback_days=args.lookback_days,
        max_positions=args.max_positions,
        transaction_cost_bps=args.transaction_cost_bps,
        sma_filter_days=args.sma_filter_days,
        sma_filter_mode=args.sma_filter_mode,
        score_mode=args.score_mode,
        skip_days=args.skip_days,
        volatility_days=args.volatility_days,
        confirm_recent_days=args.confirm_recent_days,
        data_dir=args.data_dir,
        refresh=args.refresh,
    )
    output_stem = f"sp500_top5_yearly_{args.start_year}_{args.end_year}"
    write_yearly_csv(runs, args.report_dir / f"{output_stem}.csv")
    write_yearly_markdown(
        runs,
        args.report_dir / f"{output_stem}.md",
        args.lookback_days,
        args.sma_filter_days,
        args.sma_filter_mode,
    )

    for run in runs:
        sharpe = run.summary["sharpe"]
        sharpe_text = "" if sharpe == "" else f"{float(sharpe):.2f}"
        print(
            f"{run.year}: return={format_pct(run.summary['total_return'])}, "
            f"max_dd={format_pct(run.summary['max_drawdown'])}, "
            f"sharpe={sharpe_text}, "
            f"buys={run.summary['buy_trades']}, sells={run.summary['sell_trades']}, "
            f"final={run.summary['final_holdings']}"
        )


if __name__ == "__main__":
    main()
