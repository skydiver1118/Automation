from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import (
    calculate_summary,
    load_or_fetch_prices,
    run_top_n_backtest,
)


@dataclass(frozen=True)
class Variant:
    name: str
    lookback_days: int
    max_positions: int
    score_mode: str = "skip"
    skip_days: int = 21
    sma_filter_days: int | None = None
    sma_filter_mode: str = "top_n"
    confirm_days: int | None = None


def pct(value: float) -> str:
    return f"{value:.2%}"


def monthly_returns(result) -> list[tuple[str, float]]:
    equity = pd.Series(
        [snapshot.equity for snapshot in result.snapshots],
        index=pd.to_datetime([snapshot.date for snapshot in result.snapshots]),
    )
    rows: list[tuple[str, float]] = []
    previous = 1.0
    for period, group in equity.groupby(equity.index.to_period("M")):
        end_value = float(group.iloc[-1])
        rows.append((str(period), end_value / previous - 1.0))
        previous = end_value
    return rows


def ticker_contributions(result) -> list[tuple[str, float, int]]:
    contributions: dict[str, float] = {}
    days_held: dict[str, int] = {}
    for snapshot in result.snapshots:
        if not snapshot.holdings:
            continue
        share = snapshot.daily_return / len(snapshot.holdings)
        for ticker in snapshot.holdings:
            contributions[ticker] = contributions.get(ticker, 0.0) + share
            days_held[ticker] = days_held.get(ticker, 0) + 1
    return sorted(
        [(ticker, value, days_held[ticker]) for ticker, value in contributions.items()],
        key=lambda row: row[1],
    )


def apply_recent_confirmation(result, prices: pd.DataFrame, variant: Variant, start: date, end: date):
    if variant.confirm_days is None:
        return result

    from src.strategy_lab.sp500_top5 import run_top_n_backtest

    # Re-run with a temporary SMA-style universe by masking closes that fail recent confirmation.
    adjusted = prices.copy()
    close = adjusted["Close"].copy()
    open_prices = adjusted["Open"].copy()
    for index in range(variant.confirm_days, len(close)):
        recent_return = close.iloc[index] / close.iloc[index - variant.confirm_days] - 1.0
        failed = recent_return[recent_return <= 0].index
        close.loc[close.index[index], failed] = pd.NA
        open_prices.loc[open_prices.index[index], failed] = pd.NA
    masked = pd.concat({"Open": open_prices, "Close": close}, axis=1)
    return run_top_n_backtest(
        prices=masked,
        start=start,
        end=end,
        lookback_days=variant.lookback_days,
        max_positions=variant.max_positions,
        score_mode=variant.score_mode,
        skip_days=variant.skip_days,
        sma_filter_days=variant.sma_filter_days,
        sma_filter_mode=variant.sma_filter_mode,
    )


def run() -> None:
    start = date(2024, 1, 1)
    end = date(2024, 12, 31)
    data_dir = Path("data/sp500_top5")
    prices_path = data_dir / "adjusted_open_close_2018-12-19_2025-12-31.csv"
    tickers = pd.read_csv(data_dir / "sp500_constituents.csv")["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(prices_path, tickers, date(2018, 12, 19), date(2025, 12, 31), False)

    variants = [
        Variant("current top2 126 skip21", 126, 2),
        Variant("top3 126 skip21", 126, 3),
        Variant("top4 126 skip21", 126, 4),
        Variant("top5 126 skip21", 126, 5),
        Variant("top2 126 raw", 126, 2, score_mode="raw", skip_days=0),
        Variant("top1 126 raw", 126, 1, score_mode="raw", skip_days=0),
        Variant("top3 126 raw", 126, 3, score_mode="raw", skip_days=0),
        Variant("top4 126 raw", 126, 4, score_mode="raw", skip_days=0),
        Variant("top5 126 raw", 126, 5, score_mode="raw", skip_days=0),
        Variant("top2 63 skip21", 63, 2),
        Variant("top2 63 raw", 63, 2, score_mode="raw", skip_days=0),
        Variant("top2 252 skip21", 252, 2),
        Variant("top2 126 skip10", 126, 2, skip_days=10),
        Variant("top2 126 skip42", 126, 2, skip_days=42),
        Variant("top2 126 skip21 SMA50", 126, 2, sma_filter_days=50),
        Variant("top2 126 skip21 SMA200", 126, 2, sma_filter_days=200),
        Variant("top2 126 skip21 confirm21", 126, 2, confirm_days=21),
        Variant("top3 126 skip21 confirm21", 126, 3, confirm_days=21),
        Variant("top4 126 skip21 confirm21", 126, 4, confirm_days=21),
    ]

    _, _, spmo_return = benchmark_return("SPMO", start, end)
    rows = []
    results = {}
    for variant in variants:
        result = run_top_n_backtest(
            prices=prices,
            start=start,
            end=end,
            lookback_days=variant.lookback_days,
            max_positions=variant.max_positions,
            score_mode=variant.score_mode,
            skip_days=variant.skip_days,
            sma_filter_days=variant.sma_filter_days,
            sma_filter_mode=variant.sma_filter_mode,
        )
        result = apply_recent_confirmation(result, prices, variant, start, end)
        summary = calculate_summary(result)
        rows.append((variant.name, summary, float(summary["total_return"]) - spmo_return))
        results[variant.name] = result

    rows.sort(key=lambda row: float(row[1]["total_return"]), reverse=True)
    print(f"SPMO 2024: {pct(spmo_return)}")
    print("VARIANTS")
    for name, summary, excess in rows:
        print(
            f"{name}: return={pct(float(summary['total_return']))}, "
            f"excess={pct(excess)}, max_dd={pct(float(summary['max_drawdown']))}, "
            f"sharpe={float(summary['sharpe']):.2f}, final={summary['final_holdings']}"
        )

    current = results["current top2 126 skip21"]
    print("CURRENT_MONTHLY")
    for month, value in monthly_returns(current):
        print(f"{month},{pct(value)}")

    print("CURRENT_WORST_CONTRIBUTORS")
    for ticker, value, days in ticker_contributions(current)[:10]:
        print(f"{ticker},{pct(value)},{days}")

    print("CURRENT_BEST_CONTRIBUTORS")
    for ticker, value, days in ticker_contributions(current)[-10:]:
        print(f"{ticker},{pct(value)},{days}")


if __name__ == "__main__":
    run()
