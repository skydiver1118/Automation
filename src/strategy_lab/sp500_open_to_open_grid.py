from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import load_or_fetch_prices, momentum_scores


@dataclass(frozen=True)
class Variant:
    name: str
    max_positions: int
    lookback_days: int = 126
    skip_days: int = 21
    rebalance_frequency: str = "daily"
    score_mode: str = "skip"
    weight_mode: str = "equal"
    vol_days: int = 126


def pct(value: float) -> str:
    return f"{value:.2%}"


def is_rebalance(signal_index: int, dates: pd.DatetimeIndex, frequency: str, holdings: pd.Series) -> bool:
    if frequency == "daily":
        return True
    next_index = min(signal_index + 1, len(dates) - 1)
    if frequency == "weekly":
        return holdings.empty or signal_index >= len(dates) - 2 or dates[next_index].isocalendar().week != dates[signal_index].isocalendar().week
    if frequency == "monthly":
        return holdings.empty or signal_index >= len(dates) - 2 or dates[next_index].month != dates[signal_index].month
    if frequency == "quarterly":
        return holdings.empty or signal_index >= len(dates) - 2 or dates[next_index].quarter != dates[signal_index].quarter
    raise ValueError(f"Unsupported frequency: {frequency}")


def risk_adjusted_scores(close: pd.DataFrame, signal_index: int, variant: Variant) -> pd.Series:
    raw = momentum_scores(
        close,
        signal_index,
        variant.lookback_days,
        score_mode="skip",
        skip_days=variant.skip_days,
    )
    score_index = signal_index - variant.skip_days
    if score_index < variant.vol_days:
        return pd.Series(dtype=float)
    returns = close.pct_change()
    vol = returns.iloc[score_index - variant.vol_days + 1 : score_index + 1].std()
    scores = raw / vol
    return scores.replace([math.inf, -math.inf], pd.NA).dropna().sort_values(ascending=False)


def weights(close: pd.DataFrame, scores: pd.Series, signal_index: int, variant: Variant) -> pd.Series:
    selected = scores.head(variant.max_positions)
    if selected.empty:
        return selected
    if variant.weight_mode == "equal":
        return pd.Series(1.0 / len(selected), index=selected.index)
    if variant.weight_mode == "inverse_vol":
        returns = close.pct_change()
        if signal_index < variant.vol_days:
            return pd.Series(1.0 / len(selected), index=selected.index)
        vol = returns.iloc[signal_index - variant.vol_days + 1 : signal_index + 1].std().reindex(selected.index)
        inv = (1.0 / vol).replace([math.inf, -math.inf], pd.NA).dropna().reindex(selected.index).fillna(0)
        if inv.sum() <= 0:
            return pd.Series(1.0 / len(selected), index=selected.index)
        return inv / inv.sum()
    raise ValueError(f"Unsupported weight mode: {variant.weight_mode}")


def run_variant(prices: pd.DataFrame, start: date, end: date, variant: Variant) -> dict[str, float | int | str]:
    close = prices["Close"].dropna(axis=1, thresh=variant.lookback_days + 2).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)

    holdings = pd.Series(dtype=float)
    equity = 1.0
    peak = 1.0
    max_drawdown = 0.0
    trades = 0

    for signal_index in range(variant.lookback_days, len(close) - 2):
        entry_index = signal_index + 1
        exit_index = signal_index + 2
        entry_date = close.index[entry_index].date()
        if entry_date < start or entry_date > end:
            continue

        if is_rebalance(signal_index, close.index, variant.rebalance_frequency, holdings):
            if variant.score_mode == "risk_adjusted":
                scores = risk_adjusted_scores(close, signal_index, variant)
            elif variant.score_mode == "raw":
                scores = momentum_scores(close, signal_index, variant.lookback_days, score_mode="raw", skip_days=0)
            else:
                scores = momentum_scores(
                    close,
                    signal_index,
                    variant.lookback_days,
                    score_mode="skip",
                    skip_days=variant.skip_days,
                )
            next_holdings = weights(close, scores, signal_index, variant)
            old = set(holdings.index)
            new = set(next_holdings.index)
            trades += len(old - new) + len(new - old)
            holdings = next_holdings

        period_returns = open_prices.iloc[exit_index] / open_prices.iloc[entry_index] - 1.0
        daily = 0.0
        for ticker, weight in holdings.items():
            value = period_returns.get(ticker)
            if pd.notna(value):
                daily += float(weight) * float(value)
        equity *= 1.0 + daily
        peak = max(peak, equity)
        max_drawdown = min(max_drawdown, equity / peak - 1.0)

    return {
        "return": equity - 1.0,
        "max_drawdown": max_drawdown,
        "trades": trades,
        "final_holdings": ", ".join(holdings.index),
    }


def variants() -> list[Variant]:
    return [
        Variant("Top2 skip21 daily O2O", 2),
        Variant("Top2 skip21 weekly O2O", 2, rebalance_frequency="weekly"),
        Variant("Top2 skip21 monthly O2O", 2, rebalance_frequency="monthly"),
        Variant("Top3 skip21 daily O2O", 3),
        Variant("Top4 skip21 daily O2O", 4),
        Variant("Top2 raw daily O2O", 2, skip_days=0, score_mode="raw"),
        Variant("Top20 risk-adj inv-vol monthly O2O", 20, lookback_days=252, skip_days=21, score_mode="risk_adjusted", rebalance_frequency="monthly", weight_mode="inverse_vol", vol_days=252),
        Variant("Top50 risk-adj inv-vol monthly O2O", 50, lookback_days=252, skip_days=21, score_mode="risk_adjusted", rebalance_frequency="monthly", weight_mode="inverse_vol", vol_days=252),
        Variant("Top100 risk-adj inv-vol monthly O2O", 100, lookback_days=252, skip_days=21, score_mode="risk_adjusted", rebalance_frequency="monthly", weight_mode="inverse_vol", vol_days=252),
    ]


def main() -> None:
    data_start = date(2018, 12, 19)
    end = date(2026, 5, 15)
    data_dir = Path("data/sp500_top5")
    tickers = pd.read_csv(data_dir / "sp500_constituents.csv")["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(
        data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv",
        tickers,
        data_start,
        end,
        False,
    )
    periods = [(str(year), date(year, 1, 1), date(year, 12, 31)) for year in range(2020, 2026)]
    periods.append(("2026 YTD", date(2026, 1, 1), end))

    rows = []
    for variant in variants():
        wins = 0
        compound = 1.0
        worst_excess = 1.0
        values = {}
        for period, start, stop in periods:
            result = run_variant(prices, start, stop, variant)
            _, _, spmo_return = benchmark_return("SPMO", start, stop)
            total_return = float(result["return"])
            excess = total_return - spmo_return
            wins += int(excess > 0)
            compound *= 1.0 + total_return
            worst_excess = min(worst_excess, excess)
            values[f"{period}_return"] = total_return
            values[f"{period}_excess"] = excess
            values[f"{period}_drawdown"] = result["max_drawdown"]
            values[f"{period}_trades"] = result["trades"]
        rows.append({"variant": variant.name, "wins": wins, "compound": compound - 1.0, "worst_excess": worst_excess, **values})
        print(f"{variant.name}: wins={wins}/7, compound={pct(compound - 1.0)}, worst_excess={pct(worst_excess)}")

    rows.sort(key=lambda row: (int(row["wins"]), float(row["compound"])), reverse=True)
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    csv_path = report_dir / "sp500_open_to_open_yearly_grid_vs_spmo.csv"
    md_path = report_dir / "sp500_open_to_open_yearly_grid_vs_spmo.md"
    fields = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# S&P 500 Open-to-Open Yearly Grid vs SPMO",
        "",
        "Execution model: signal after close, trade at next open, hold until the following open. Each year/YTD period is reset independently.",
        "",
        "| Rank | Variant | Wins | Compound Reset Return | Worst Excess | 2024 Return | 2024 Excess | 2026 YTD Return | 2026 YTD Excess |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for rank, row in enumerate(rows, start=1):
        lines.append(
            "| "
            f"{rank} | {row['variant']} | {row['wins']}/7 | {pct(float(row['compound']))} | "
            f"{pct(float(row['worst_excess']))} | {pct(float(row['2024_return']))} | "
            f"{pct(float(row['2024_excess']))} | {pct(float(row['2026 YTD_return']))} | "
            f"{pct(float(row['2026 YTD_excess']))} |"
        )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(md_path)


if __name__ == "__main__":
    main()
