from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import (
    load_nasdaq100_constituents,
    load_or_fetch_prices,
    momentum_scores,
    save_constituents,
)


@dataclass(frozen=True)
class PeriodResult:
    period: str
    start: date
    end: date
    actual_start: str
    actual_end: str
    strategy_return: float
    strategy_max_drawdown: float
    trades: int
    benchmark_close_return: float
    benchmark_open_to_open_return: float
    excess_vs_benchmark_close: float
    excess_vs_benchmark_o2o: float
    final_holdings: str


def pct(value: float) -> str:
    return f"{value:.2%}"


def load_etf(symbol: str, start: date, end: date) -> pd.DataFrame:
    data = yf.download(
        symbol,
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        auto_adjust=True,
        progress=False,
    )
    if isinstance(data.columns, pd.MultiIndex):
        data = data.droplevel(1, axis=1)
    data.index = pd.to_datetime(data.index)
    return data[["Open", "Close"]].dropna()


def is_month_end_signal(index: int, dates: pd.DatetimeIndex, holdings: pd.Series) -> bool:
    next_index = min(index + 1, len(dates) - 1)
    return (
        holdings.empty
        or index >= len(dates) - 2
        or dates[next_index].month != dates[index].month
        or dates[next_index].year != dates[index].year
    )


def run_top2_monthly_o2o(prices: pd.DataFrame, start: date, end: date) -> dict[str, object]:
    close = prices["Close"].dropna(axis=1, thresh=128).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)

    holdings = pd.Series(dtype=float)
    equity = 1.0
    peak = 1.0
    max_drawdown = 0.0
    trades = 0
    first_entry_date = None
    last_exit_date = None

    for signal_index in range(126, len(close) - 2):
        entry_index = signal_index + 1
        exit_index = signal_index + 2
        entry_date = close.index[entry_index].date()
        exit_date = close.index[exit_index].date()
        if entry_date < start or entry_date > end:
            continue

        if is_month_end_signal(signal_index, close.index, holdings):
            scores = momentum_scores(close, signal_index, 126, score_mode="skip", skip_days=21)
            selected = scores.head(2).index
            next_holdings = pd.Series(0.5, index=selected, dtype=float)
            old = set(holdings.index)
            new = set(next_holdings.index)
            trades += len(old - new) + len(new - old)
            holdings = next_holdings
            if first_entry_date is None and not holdings.empty:
                first_entry_date = entry_date

        one_day_returns = open_prices.iloc[exit_index] / open_prices.iloc[entry_index] - 1.0
        daily_return = 0.0
        for ticker, weight in holdings.items():
            value = one_day_returns.get(ticker)
            if pd.notna(value):
                daily_return += float(weight) * float(value)
        equity *= 1.0 + daily_return
        peak = max(peak, equity)
        max_drawdown = min(max_drawdown, equity / peak - 1.0)
        last_exit_date = exit_date

    return {
        "return": equity - 1.0,
        "max_drawdown": max_drawdown,
        "trades": trades,
        "actual_start": "" if first_entry_date is None else first_entry_date.isoformat(),
        "actual_end": "" if last_exit_date is None else last_exit_date.isoformat(),
        "final_holdings": ", ".join(holdings.index),
    }


def etf_open_to_open_return(etf: pd.DataFrame, start: date, end: date) -> float:
    frame = etf.loc[(etf.index.date >= start) & (etf.index.date <= end)]
    if frame.empty:
        return 0.0
    return float(frame["Open"].iloc[-1] / frame["Open"].iloc[0] - 1.0)


def main() -> None:
    data_start = date(2018, 12, 19)
    end = date(2026, 5, 16)
    benchmark = "QQQ"
    data_dir = Path("data/nasdaq100_top2_monthly")
    constituents_path = data_dir / "nasdaq100_constituents.csv"
    prices_path = data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv"

    if constituents_path.exists():
        constituents = pd.read_csv(constituents_path)
    else:
        constituents = load_nasdaq100_constituents()
        save_constituents(constituents, constituents_path)

    tickers = constituents["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(prices_path, tickers, data_start, end, False)
    etf = load_etf(benchmark, data_start, end)

    periods = [(str(year), date(year, 1, 1), date(year, 12, 31)) for year in range(2020, 2026)]
    periods.append(("2026 YTD", date(2026, 1, 1), end))

    rows: list[PeriodResult] = []
    for period, start, stop in periods:
        result = run_top2_monthly_o2o(prices, start, stop)
        _, _, benchmark_close = benchmark_return(benchmark, start, stop)
        benchmark_o2o = etf_open_to_open_return(etf, start, stop)
        rows.append(
            PeriodResult(
                period=period,
                start=start,
                end=stop,
                actual_start=str(result["actual_start"]),
                actual_end=str(result["actual_end"]),
                strategy_return=float(result["return"]),
                strategy_max_drawdown=float(result["max_drawdown"]),
                trades=int(result["trades"]),
                benchmark_close_return=benchmark_close,
                benchmark_open_to_open_return=benchmark_o2o,
                excess_vs_benchmark_close=float(result["return"]) - benchmark_close,
                excess_vs_benchmark_o2o=float(result["return"]) - benchmark_o2o,
                final_holdings=str(result["final_holdings"]),
            )
        )

    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    csv_path = report_dir / "nasdaq100_top2_skip21_monthly_o2o_validation_2020_2026ytd.csv"
    md_path = report_dir / "nasdaq100_top2_skip21_monthly_o2o_validation_2020_2026ytd.md"

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(PeriodResult.__dataclass_fields__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    strategy_compound = 1.0
    benchmark_close_compound = 1.0
    benchmark_o2o_compound = 1.0
    lines = [
        f"# Nasdaq-100 Top-2 Skip21 Monthly Open-to-Open vs {benchmark}",
        "",
        "Rules: current Nasdaq-100 universe, signal after the last close of each month, rank by 126-trading-day momentum excluding the most recent 21 trading days, buy the top 2 equal-weight at the next open, and hold open-to-open until the next rebalance. Each year/YTD period resets independently.",
        "",
        f"| Period | Strategy | Max DD | Trades | {benchmark} Close | {benchmark} O2O | Excess vs {benchmark} Close | Excess vs {benchmark} O2O | Final Holdings |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        strategy_compound *= 1.0 + row.strategy_return
        benchmark_close_compound *= 1.0 + row.benchmark_close_return
        benchmark_o2o_compound *= 1.0 + row.benchmark_open_to_open_return
        lines.append(
            "| "
            f"{row.period} | {pct(row.strategy_return)} | {pct(row.strategy_max_drawdown)} | "
            f"{row.trades} | {pct(row.benchmark_close_return)} | {pct(row.benchmark_open_to_open_return)} | "
            f"{pct(row.excess_vs_benchmark_close)} | {pct(row.excess_vs_benchmark_o2o)} | "
            f"{row.final_holdings} |"
        )
    lines.extend(
        [
            "",
            f"| Compounded Reset Return | Strategy | {benchmark} Close | {benchmark} O2O |",
            "| --- | ---: | ---: | ---: |",
            f"| 2020-2026 YTD | {pct(strategy_compound - 1.0)} | {pct(benchmark_close_compound - 1.0)} | {pct(benchmark_o2o_compound - 1.0)} |",
            "",
            "Validation notes:",
            "- No same-day lookahead: month-end close signals are used for the next trading day's open.",
            "- Major remaining flaw: this uses the current Nasdaq-100 constituent list for past years, so survivorship/index-membership bias remains.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(md_path)
    for row in rows:
        print(
            f"{row.period}: strategy={pct(row.strategy_return)}, "
            f"{benchmark}_close={pct(row.benchmark_close_return)}, "
            f"{benchmark}_o2o={pct(row.benchmark_open_to_open_return)}, "
            f"trades={row.trades}, max_dd={pct(row.strategy_max_drawdown)}, "
            f"final={row.final_holdings}"
        )


if __name__ == "__main__":
    main()
