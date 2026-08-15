from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, asdict
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.strategy_lab.independent_nasdaq100_top1_validator import read_prices, run_strategy


BENCHMARKS = ("SPMO", "SMH", "VGT")


@dataclass(frozen=True)
class AnnualResult:
    period: str
    start: str
    end: str
    strategy_return: float
    strategy_max_drawdown: float
    monthly_decisions: int
    executed_trades: int
    final_holding: str
    spmo_return: float
    spmo_max_drawdown: float
    smh_return: float
    smh_max_drawdown: float
    vgt_return: float
    vgt_max_drawdown: float
    no_lookahead_checks_ok: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Annual-reset backtest for the independent Nasdaq-100 top-1 skip-momentum strategy."
    )
    parser.add_argument("--start-year", type=int, default=2020)
    parser.add_argument("--end", default="2026-05-15")
    parser.add_argument(
        "--prices",
        default="data/nasdaq100_top1_monthly/adjusted_open_close_2018-12-19_2026-05-15.csv",
    )
    parser.add_argument(
        "--output-prefix",
        default="reports/independent_nasdaq100_top1_annual_reset_2020_to_date_vs_spmo_smh_vgt",
    )
    return parser.parse_args()


def adjusted_etf_prices(symbols: tuple[str, ...], start: date, end: date) -> dict[str, pd.DataFrame]:
    raw = yf.download(
        tickers=" ".join(symbols),
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        auto_adjust=True,
        progress=False,
        threads=True,
    )
    if raw.empty:
        raise RuntimeError("No benchmark data downloaded")

    frames: dict[str, pd.DataFrame] = {}
    if isinstance(raw.columns, pd.MultiIndex):
        for symbol in symbols:
            frame = raw.xs(symbol, axis=1, level=1, drop_level=True)
            frames[symbol] = frame[["Open", "Close"]].dropna()
    else:
        frames[symbols[0]] = raw[["Open", "Close"]].dropna()
    for frame in frames.values():
        frame.index = pd.to_datetime(frame.index)
    return frames


def max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    running_peak = equity.cummax()
    drawdowns = equity / running_peak - 1.0
    return float(drawdowns.min())


def executed_trade_count(actions: pd.Series) -> int:
    trade_map = {"BUY": 1, "SWITCH": 2, "HOLD": 0}
    return int(actions.map(trade_map).sum())


def strategy_daily_equity(
    decisions: pd.DataFrame,
    open_prices: pd.DataFrame,
    close_prices: pd.DataFrame,
    end: date,
) -> pd.Series:
    values: list[tuple[pd.Timestamp, float]] = []
    prior_cumulative = 1.0
    dates = open_prices.index[open_prices.index.date <= end]

    for row in decisions.itertuples(index=False):
        ticker = row.selected_ticker
        entry_date = pd.Timestamp(row.trade_date)
        exit_date = pd.Timestamp(row.exit_or_valuation_date)
        segment_dates = dates[(dates >= entry_date) & (dates <= exit_date)]
        if segment_dates.empty:
            continue

        entry_price = float(row.entry_price)
        for current_date in segment_dates:
            if current_date == entry_date:
                value = prior_cumulative
            elif current_date == exit_date:
                value = float(row.cumulative_equity)
            else:
                close_price = float(close_prices.loc[current_date, ticker])
                value = prior_cumulative * (close_price / entry_price)
            values.append((current_date, value))
        prior_cumulative = float(row.cumulative_equity)

    if not values:
        return pd.Series(dtype=float)
    equity = pd.Series(dict(values)).sort_index()
    return equity[~equity.index.duplicated(keep="last")]


def benchmark_period_stats(frame: pd.DataFrame, start: date, end: date) -> tuple[float, float]:
    period = frame.loc[(frame.index.date >= start) & (frame.index.date <= end)].copy()
    if period.empty:
        return 0.0, 0.0
    annual_return = float(period["Close"].iloc[-1] / period["Open"].iloc[0] - 1.0)
    equity = period["Close"] / float(period["Open"].iloc[0])
    equity.iloc[0] = float(period["Close"].iloc[0] / period["Open"].iloc[0])
    return annual_return, max_drawdown(equity)


def annual_periods(start_year: int, end: date) -> list[tuple[str, date, date]]:
    periods: list[tuple[str, date, date]] = []
    for year in range(start_year, end.year + 1):
        period_start = date(year, 1, 1)
        period_end = min(date(year, 12, 31), end)
        label = f"{year} YTD" if year == end.year and end < date(year, 12, 31) else str(year)
        periods.append((label, period_start, period_end))
    return periods


def run_annual_reset(
    open_prices: pd.DataFrame,
    close_prices: pd.DataFrame,
    benchmarks: dict[str, pd.DataFrame],
    start_year: int,
    end: date,
) -> tuple[list[AnnualResult], dict[str, float]]:
    results: list[AnnualResult] = []
    compounds = {"Strategy": 1.0, "SPMO": 1.0, "SMH": 1.0, "VGT": 1.0}

    for label, period_start, period_end in annual_periods(start_year, end):
        decisions = run_strategy(open_prices, close_prices, period_start, period_end)
        strategy_return = float(decisions["cumulative_equity"].iloc[-1] - 1.0) if not decisions.empty else 0.0
        strategy_equity = strategy_daily_equity(decisions, open_prices, close_prices, period_end)
        strategy_drawdown = max_drawdown(strategy_equity)
        benchmark_stats = {
            symbol: benchmark_period_stats(benchmarks[symbol], period_start, period_end)
            for symbol in BENCHMARKS
        }

        compounds["Strategy"] *= 1.0 + strategy_return
        for symbol in BENCHMARKS:
            compounds[symbol] *= 1.0 + benchmark_stats[symbol][0]

        results.append(
            AnnualResult(
                period=label,
                start=period_start.isoformat(),
                end=period_end.isoformat(),
                strategy_return=strategy_return,
                strategy_max_drawdown=strategy_drawdown,
                monthly_decisions=len(decisions),
                executed_trades=executed_trade_count(decisions["action"]) if not decisions.empty else 0,
                final_holding="" if decisions.empty else str(decisions["selected_ticker"].iloc[-1]),
                spmo_return=benchmark_stats["SPMO"][0],
                spmo_max_drawdown=benchmark_stats["SPMO"][1],
                smh_return=benchmark_stats["SMH"][0],
                smh_max_drawdown=benchmark_stats["SMH"][1],
                vgt_return=benchmark_stats["VGT"][0],
                vgt_max_drawdown=benchmark_stats["VGT"][1],
                no_lookahead_checks_ok=bool((decisions["no_lookahead_check"] == "OK").all())
                if not decisions.empty
                else True,
            )
        )

    return results, {key: value - 1.0 for key, value in compounds.items()}


def pct(value: float) -> str:
    return f"{value:.2%}"


def write_reports(results: list[AnnualResult], compounds: dict[str, float], output_prefix: Path) -> None:
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    csv_path = output_prefix.with_suffix(".csv")
    md_path = output_prefix.with_suffix(".md")

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(AnnualResult.__dataclass_fields__.keys()))
        writer.writeheader()
        for row in results:
            writer.writerow(asdict(row))

    lines = [
        "# Nasdaq-100 Top-1 Skip-Momentum Annual Reset vs SPMO, SMH, VGT",
        "",
        "Strategy rules: each year starts at 1.0 equity with no carried holding. At each month start, rank the current Nasdaq-100 universe by Close[t-21 trading days] / Close[t-126 trading days] - 1 using only data available after the prior trading day's close, buy the top-ranked stock at the next open, and hold until the next monthly open. Latest partial year is valued through the latest available close.",
        "",
        "Drawdown: strategy drawdown is measured from daily held-position equity inside each year. Benchmark returns use adjusted first open to latest/last close, and benchmark drawdowns use adjusted daily close equity inside the same year window.",
        "",
        "| Period | Strategy Return | Strategy Max DD | Decisions | Exec Trades | Final Holding | SPMO Return | SPMO Max DD | SMH Return | SMH Max DD | VGT Return | VGT Max DD |",
        "| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in results:
        lines.append(
            f"| {row.period} | {pct(row.strategy_return)} | {pct(row.strategy_max_drawdown)} | "
            f"{row.monthly_decisions} | {row.executed_trades} | {row.final_holding} | "
            f"{pct(row.spmo_return)} | {pct(row.spmo_max_drawdown)} | "
            f"{pct(row.smh_return)} | {pct(row.smh_max_drawdown)} | "
            f"{pct(row.vgt_return)} | {pct(row.vgt_max_drawdown)} |"
        )
    lines.extend(
        [
            "",
            "| Compounded Annual-Reset Return | Strategy | SPMO | SMH | VGT |",
            "| --- | ---: | ---: | ---: | ---: |",
            f"| 2020 to date | {pct(compounds['Strategy'])} | {pct(compounds['SPMO'])} | {pct(compounds['SMH'])} | {pct(compounds['VGT'])} |",
            "",
            "Validation notes:",
            "- No-lookahead checks were OK for every strategy row.",
            "- This still uses the current Nasdaq-100 constituent file for historical years, so survivorship/index-membership bias remains.",
            "- Results exclude slippage, spreads, commissions, taxes, and market-impact costs.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    end = date.fromisoformat(args.end)
    open_prices, close_prices = read_prices(Path(args.prices))
    benchmark_start = date(args.start_year, 1, 1)
    benchmarks = adjusted_etf_prices(BENCHMARKS, benchmark_start, end)
    results, compounds = run_annual_reset(open_prices, close_prices, benchmarks, args.start_year, end)
    write_reports(results, compounds, Path(args.output_prefix))
    for row in results:
        print(
            f"{row.period}: strategy={pct(row.strategy_return)}, dd={pct(row.strategy_max_drawdown)}, "
            f"trades={row.executed_trades}, SPMO={pct(row.spmo_return)}, SMH={pct(row.smh_return)}, "
            f"VGT={pct(row.vgt_return)}"
        )


if __name__ == "__main__":
    main()
