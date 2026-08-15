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
    load_sp500_constituents,
    momentum_scores,
    save_constituents,
)


@dataclass(frozen=True)
class UniverseSpec:
    name: str
    data_dir: Path
    constituents_file: str


@dataclass(frozen=True)
class ResultRow:
    universe: str
    top_n: int
    strategy_return: float
    max_drawdown: float
    trades: int
    spmo_return: float
    vgt_return: float
    excess_vs_spmo: float
    excess_vs_vgt: float
    final_holdings: str


def pct(value: float) -> str:
    return f"{value:.2%}"


def is_month_end_signal(index: int, dates: pd.DatetimeIndex, holdings: pd.Series) -> bool:
    next_index = min(index + 1, len(dates) - 1)
    return (
        holdings.empty
        or index >= len(dates) - 2
        or dates[next_index].month != dates[index].month
        or dates[next_index].year != dates[index].year
    )


def load_universe(spec: UniverseSpec, data_start: date, end: date) -> pd.DataFrame:
    constituents_path = spec.data_dir / spec.constituents_file
    prices_path = spec.data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv"

    if constituents_path.exists():
        constituents = pd.read_csv(constituents_path)
    else:
        if spec.name == "S&P 500":
            constituents = load_sp500_constituents()
        elif spec.name == "Nasdaq-100":
            constituents = load_nasdaq100_constituents()
        else:
            raise ValueError(f"Unknown universe: {spec.name}")
        save_constituents(constituents, constituents_path)

    tickers = constituents["Yahoo Symbol"].dropna().astype(str).tolist()
    return load_or_fetch_prices(prices_path, tickers, data_start, end, False)


def run_topn_monthly_o2o(prices: pd.DataFrame, start: date, end: date, top_n: int) -> dict[str, object]:
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

    for signal_index in range(126, len(close) - 2):
        entry_index = signal_index + 1
        exit_index = signal_index + 2
        entry_date = close.index[entry_index].date()
        if entry_date < start or entry_date > end:
            continue

        if is_month_end_signal(signal_index, close.index, holdings):
            scores = momentum_scores(close, signal_index, 126, score_mode="skip", skip_days=21)
            selected = scores.head(top_n).index
            next_holdings = pd.Series(1.0 / top_n, index=selected, dtype=float)
            old = set(holdings.index)
            new = set(next_holdings.index)
            trades += len(old - new) + len(new - old)
            holdings = next_holdings

        one_day_returns = open_prices.iloc[exit_index] / open_prices.iloc[entry_index] - 1.0
        daily_return = 0.0
        for ticker, weight in holdings.items():
            value = one_day_returns.get(ticker)
            if pd.notna(value):
                daily_return += float(weight) * float(value)
        equity *= 1.0 + daily_return
        peak = max(peak, equity)
        max_drawdown = min(max_drawdown, equity / peak - 1.0)

    return {
        "strategy_return": equity - 1.0,
        "max_drawdown": max_drawdown,
        "trades": trades,
        "final_holdings": ", ".join(holdings.index),
    }


def load_benchmark(symbol: str, start: date, end: date) -> float:
    _, _, total_return = benchmark_return(symbol, start, end)
    return total_return


def main() -> None:
    start = date(2020, 1, 1)
    end = date(2026, 5, 17)
    data_start = date(2018, 12, 19)
    universes = [
        UniverseSpec("S&P 500", Path("data/sp500_top5"), "sp500_constituents.csv"),
        UniverseSpec("Nasdaq-100", Path("data/nasdaq100_topn_monthly"), "nasdaq100_constituents.csv"),
    ]

    spmo_return = load_benchmark("SPMO", start, end)
    vgt_return = load_benchmark("VGT", start, end)

    rows: list[ResultRow] = []
    for universe in universes:
        prices = load_universe(universe, data_start, end)
        for top_n in [1, 2, 3]:
            result = run_topn_monthly_o2o(prices, start, end, top_n)
            strategy_return = float(result["strategy_return"])
            rows.append(
                ResultRow(
                    universe=universe.name,
                    top_n=top_n,
                    strategy_return=strategy_return,
                    max_drawdown=float(result["max_drawdown"]),
                    trades=int(result["trades"]),
                    spmo_return=spmo_return,
                    vgt_return=vgt_return,
                    excess_vs_spmo=strategy_return - spmo_return,
                    excess_vs_vgt=strategy_return - vgt_return,
                    final_holdings=str(result["final_holdings"]),
                )
            )

    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    csv_path = report_dir / "top1_top2_top3_sp500_nasdaq100_vs_spmo_vgt_2020_2026ytd.csv"
    md_path = report_dir / "top1_top2_top3_sp500_nasdaq100_vs_spmo_vgt_2020_2026ytd.md"

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ResultRow.__dataclass_fields__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    lines = [
        "# Top 1/2/3 Monthly Skip-Momentum Comparison",
        "",
        f"Period: {start.isoformat()} to latest available trading data through {end.isoformat()}.",
        "Strategy: monthly rebalance, signal after month-end close, rank by 126-trading-day momentum excluding the latest 21 trading days, trade next open, hold open-to-open.",
        "",
        "| Universe | Top N | Strategy Return | Max DD | Trades | SPMO Return | VGT Return | Excess vs SPMO | Excess vs VGT | Final Holdings |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.universe} | {row.top_n} | {pct(row.strategy_return)} | "
            f"{pct(row.max_drawdown)} | {row.trades} | {pct(row.spmo_return)} | "
            f"{pct(row.vgt_return)} | {pct(row.excess_vs_spmo)} | "
            f"{pct(row.excess_vs_vgt)} | {row.final_holdings} |"
        )
    lines.extend(
        [
            "",
            "Benchmark returns use adjusted-close buy-and-hold.",
            "Important caveat: both universe tests use current constituents for past dates, so survivorship/index-membership bias remains.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(md_path)
    for row in rows:
        print(
            f"{row.universe} top{row.top_n}: return={pct(row.strategy_return)}, "
            f"max_dd={pct(row.max_drawdown)}, trades={row.trades}, "
            f"excess_vs_spmo={pct(row.excess_vs_spmo)}, excess_vs_vgt={pct(row.excess_vs_vgt)}"
        )


if __name__ == "__main__":
    main()
