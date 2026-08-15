from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import load_or_fetch_prices, momentum_scores


@dataclass(frozen=True)
class Row:
    year: int
    threshold: float
    strategy_return: float
    spmo_return: float
    excess: float
    max_drawdown: float
    fallback_days: int


def pct(value: float) -> str:
    return f"{value:.2%}"


def load_spmo(start: date, end: date) -> pd.DataFrame:
    data = yf.download("SPMO", start=start.isoformat(), end=end.isoformat(), auto_adjust=True, progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        data = data.droplevel(1, axis=1)
    data.index = pd.to_datetime(data.index)
    return data[["Open", "Close"]].dropna()


def run_year(prices: pd.DataFrame, spmo: pd.DataFrame, year: int, threshold: float) -> Row:
    start = date(year, 1, 1)
    end = date(year, 12, 31)
    close = prices["Close"].dropna(axis=1, thresh=128).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)
    aligned_spmo = spmo.reindex(close.index).ffill()

    holdings: list[str] = []
    pending: list[str] | None = None
    model_equity = 1.0
    model_peak = 1.0
    portfolio_equity = 1.0
    portfolio_peak = 1.0
    max_drawdown = 0.0
    fallback_days = 0
    active_fallback = False

    for index in range(1, len(close)):
        current_date = close.index[index]
        if current_date.date() < start:
            continue
        if pending is not None:
            holdings = list(pending)
            pending = None

        stock_returns = close.iloc[index] / open_prices.iloc[index] - 1.0
        strategy_daily = 0.0
        for ticker in holdings:
            value = stock_returns.get(ticker)
            if pd.notna(value):
                strategy_daily += 0.5 * float(value)
        if active_fallback:
            fallback_days += 1
            spmo_daily = aligned_spmo["Close"].iloc[index] / aligned_spmo["Open"].iloc[index] - 1.0
            portfolio_daily = 0.0 if pd.isna(spmo_daily) else float(spmo_daily)
        else:
            portfolio_daily = strategy_daily

        model_equity *= 1.0 + strategy_daily
        model_peak = max(model_peak, model_equity)
        model_drawdown = model_equity / model_peak - 1.0
        active_fallback = model_drawdown <= -threshold

        portfolio_equity *= 1.0 + portfolio_daily
        portfolio_peak = max(portfolio_peak, portfolio_equity)
        max_drawdown = min(max_drawdown, portfolio_equity / portfolio_peak - 1.0)

        scores = momentum_scores(close, index, 126, score_mode="skip", skip_days=21)
        selected = list(scores.head(2).index)
        next_holdings = [ticker for ticker in holdings if ticker in selected]
        for ticker in selected:
            if len(next_holdings) >= 2:
                break
            if ticker not in next_holdings:
                next_holdings.append(ticker)
        pending = next_holdings

    _, _, spmo_return = benchmark_return("SPMO", start, end)
    strategy_return = portfolio_equity - 1.0
    return Row(
        year=year,
        threshold=threshold,
        strategy_return=strategy_return,
        spmo_return=spmo_return,
        excess=strategy_return - spmo_return,
        max_drawdown=max_drawdown,
        fallback_days=fallback_days,
    )


def run() -> None:
    data_dir = Path("data/sp500_top5")
    tickers = pd.read_csv(data_dir / "sp500_constituents.csv")["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(
        data_dir / "adjusted_open_close_2018-12-19_2025-12-31.csv",
        tickers,
        date(2018, 12, 19),
        date(2025, 12, 31),
        False,
    )
    spmo = load_spmo(date(2018, 12, 19), date(2026, 1, 1))
    rows = []
    for threshold in [0.05, 0.10, 0.15, 0.20, 0.25]:
        for year in range(2020, 2026):
            rows.append(run_year(prices, spmo, year, threshold))

    for threshold in [0.05, 0.10, 0.15, 0.20, 0.25]:
        subset = [row for row in rows if row.threshold == threshold]
        strategy_compound = 1.0
        spmo_compound = 1.0
        print(f"THRESHOLD {pct(threshold)}")
        for row in subset:
            strategy_compound *= 1.0 + row.strategy_return
            spmo_compound *= 1.0 + row.spmo_return
            print(
                f"{row.year}: strategy={pct(row.strategy_return)}, spmo={pct(row.spmo_return)}, "
                f"excess={pct(row.excess)}, max_dd={pct(row.max_drawdown)}, fallback_days={row.fallback_days}"
            )
        print(
            f"compound: strategy={pct(strategy_compound - 1.0)}, "
            f"spmo={pct(spmo_compound - 1.0)}, excess={pct((strategy_compound - 1.0) - (spmo_compound - 1.0))}"
        )


if __name__ == "__main__":
    run()
