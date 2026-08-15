from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import (
    calculate_summary,
    load_nasdaq100_constituents,
    load_or_fetch_prices,
    run_top_n_backtest,
    save_constituents,
)


@dataclass(frozen=True)
class ComparisonRow:
    year: int
    strategy_return: float
    benchmark_return: float
    excess_return: float
    max_drawdown: float
    sharpe: float | str
    buy_trades: int
    sell_trades: int
    final_holdings: str


def format_pct(value: object) -> str:
    return f"{float(value):.2%}"


def run_comparison(
    start_year: int,
    end_year: int,
    lookback_days: int,
    max_positions: int,
    score_mode: str,
    skip_days: int,
    benchmark_symbol: str,
    data_dir: Path,
    refresh: bool,
) -> list[ComparisonRow]:
    first_start = date(start_year, 1, 1)
    final_end = date(end_year, 12, 31)
    fetch_start = first_start - timedelta(days=max(lookback_days * 3, 260))

    constituents_path = data_dir / "nasdaq100_constituents.csv"
    prices_path = data_dir / f"adjusted_open_close_{fetch_start.isoformat()}_{final_end.isoformat()}.csv"

    if constituents_path.exists() and not refresh:
        constituents = pd.read_csv(constituents_path)
    else:
        constituents = load_nasdaq100_constituents()
        save_constituents(constituents, constituents_path)

    tickers = constituents["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(prices_path, tickers, fetch_start, final_end, refresh)

    rows: list[ComparisonRow] = []
    for year in range(start_year, end_year + 1):
        start = date(year, 1, 1)
        end = date(year, 12, 31)
        result = run_top_n_backtest(
            prices=prices,
            start=start,
            end=end,
            lookback_days=lookback_days,
            max_positions=max_positions,
            score_mode=score_mode,
            skip_days=skip_days,
        )
        summary = calculate_summary(result)
        _, _, benchmark_total_return = benchmark_return(benchmark_symbol, start, end)
        rows.append(
            ComparisonRow(
                year=year,
                strategy_return=float(summary["total_return"]),
                benchmark_return=benchmark_total_return,
                excess_return=float(summary["total_return"]) - benchmark_total_return,
                max_drawdown=float(summary["max_drawdown"]),
                sharpe=summary["sharpe"],
                buy_trades=int(summary["buy_trades"]),
                sell_trades=int(summary["sell_trades"]),
                final_holdings=str(summary["final_holdings"]),
            )
        )
    return rows


def write_csv(rows: list[ComparisonRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "year",
                "strategy_return",
                "benchmark_return",
                "excess_return",
                "max_drawdown",
                "sharpe",
                "buy_trades",
                "sell_trades",
                "final_holdings",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def write_markdown(
    rows: list[ComparisonRow],
    path: Path,
    benchmark_symbol: str,
    lookback_days: int,
    max_positions: int,
    skip_days: int,
) -> None:
    strategy_compound = 1.0
    benchmark_compound = 1.0
    lines = [
        f"# Nasdaq-100 Top-{max_positions} Momentum vs {benchmark_symbol}",
        "",
        f"Strategy: current Nasdaq-100 universe, rank by {lookback_days}-trading-day momentum excluding the most recent {skip_days} trading days, hold top {max_positions} equal-weight positions, execute at next trading day's open, reset each calendar year.",
        "",
        "| Year | Strategy Return | Benchmark Return | Excess | Max DD | Sharpe | Buys | Final Holdings |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        strategy_compound *= 1.0 + row.strategy_return
        benchmark_compound *= 1.0 + row.benchmark_return
        sharpe_text = "" if row.sharpe == "" else f"{float(row.sharpe):.2f}"
        lines.append(
            "| "
            f"{row.year} | "
            f"{format_pct(row.strategy_return)} | "
            f"{format_pct(row.benchmark_return)} | "
            f"{format_pct(row.excess_return)} | "
            f"{format_pct(row.max_drawdown)} | "
            f"{sharpe_text} | "
            f"{row.buy_trades} | "
            f"{row.final_holdings} |"
        )
    strategy_total = strategy_compound - 1.0
    benchmark_total = benchmark_compound - 1.0
    lines.extend(
        [
            "",
            "| Compounded Reset-Year Return | Strategy | Benchmark | Excess |",
            "| --- | ---: | ---: | ---: |",
            f"| {rows[0].year}-{rows[-1].year} | {format_pct(strategy_total)} | {format_pct(benchmark_total)} | {format_pct(strategy_total - benchmark_total)} |",
            "",
            "Data note: this uses the current Nasdaq-100 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Nasdaq-100 annual reset momentum backtests.")
    parser.add_argument("--start-year", type=int, default=2020)
    parser.add_argument("--end-year", type=int, default=2025)
    parser.add_argument("--lookback-days", type=int, default=126)
    parser.add_argument("--max-positions", type=int, default=3)
    parser.add_argument("--score-mode", choices=["raw", "skip", "risk_adjusted", "risk_adjusted_skip"], default="skip")
    parser.add_argument("--skip-days", type=int, default=21)
    parser.add_argument("--benchmark-symbol", default="VGT")
    parser.add_argument("--data-dir", type=Path, default=Path("data/nasdaq100_top3"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    rows = run_comparison(
        start_year=args.start_year,
        end_year=args.end_year,
        lookback_days=args.lookback_days,
        max_positions=args.max_positions,
        score_mode=args.score_mode,
        skip_days=args.skip_days,
        benchmark_symbol=args.benchmark_symbol,
        data_dir=args.data_dir,
        refresh=args.refresh,
    )
    output_stem = f"nasdaq100_top{args.max_positions}_skip{args.skip_days}_vs_{args.benchmark_symbol.lower()}_{args.start_year}_{args.end_year}"
    write_csv(rows, args.report_dir / f"{output_stem}.csv")
    write_markdown(
        rows,
        args.report_dir / f"{output_stem}.md",
        args.benchmark_symbol,
        args.lookback_days,
        args.max_positions,
        args.skip_days,
    )
    for row in rows:
        print(
            f"{row.year}: strategy={format_pct(row.strategy_return)}, "
            f"{args.benchmark_symbol}={format_pct(row.benchmark_return)}, "
            f"excess={format_pct(row.excess_return)}, "
            f"max_dd={format_pct(row.max_drawdown)}, final={row.final_holdings}"
        )


if __name__ == "__main__":
    main()
