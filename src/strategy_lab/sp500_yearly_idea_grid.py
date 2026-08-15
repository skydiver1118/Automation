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
    kind: str
    max_positions: int = 2
    lookback_days: int = 126
    skip_days: int = 21
    leverage: float = 1.0
    spmo_weight: float = 0.0
    stock_weight: float = 1.0
    rebalance_frequency: str = "daily"
    weight_mode: str = "equal"
    sma_days: int | None = None
    vol_days: int = 126


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


def is_rebalance(index: int, dates: pd.DatetimeIndex, frequency: str, holdings: list[str]) -> bool:
    if frequency == "daily":
        return True
    next_index = min(index + 1, len(dates) - 1)
    if frequency == "weekly":
        return not holdings or index == len(dates) - 1 or dates[next_index].isocalendar().week != dates[index].isocalendar().week
    if frequency == "monthly":
        return not holdings or index == len(dates) - 1 or dates[next_index].month != dates[index].month
    if frequency == "quarterly":
        return not holdings or index == len(dates) - 1 or dates[next_index].quarter != dates[index].quarter
    raise ValueError(f"Unsupported rebalance frequency: {frequency}")


def stock_weights(close: pd.DataFrame, scores: pd.Series, index: int, variant: Variant) -> pd.Series:
    selected = scores.head(variant.max_positions)
    if selected.empty:
        return selected
    if variant.weight_mode == "equal":
        return pd.Series(1.0 / len(selected), index=selected.index)
    if variant.weight_mode == "score":
        weights = selected.clip(lower=0)
        if weights.sum() <= 0:
            return pd.Series(1.0 / len(selected), index=selected.index)
        return weights / weights.sum()
    if variant.weight_mode == "inverse_vol":
        returns = close.pct_change()
        if index < variant.vol_days:
            return pd.Series(1.0 / len(selected), index=selected.index)
        vol = returns.iloc[index - variant.vol_days + 1 : index + 1, :].std().reindex(selected.index)
        inv = (1.0 / vol).replace([math.inf, -math.inf], pd.NA).dropna()
        inv = inv.reindex(selected.index).fillna(0)
        if inv.sum() <= 0:
            return pd.Series(1.0 / len(selected), index=selected.index)
        return inv / inv.sum()
    raise ValueError(f"Unsupported weight mode: {variant.weight_mode}")


def risk_adjusted_scores(close: pd.DataFrame, index: int, lookback_days: int, skip_days: int, vol_days: int) -> pd.Series:
    raw = momentum_scores(close, index, lookback_days, score_mode="skip", skip_days=skip_days)
    if index - skip_days < vol_days:
        return pd.Series(dtype=float)
    returns = close.pct_change()
    score_index = index - skip_days
    vol = returns.iloc[score_index - vol_days + 1 : score_index + 1].std()
    score = raw / vol
    return score.replace([math.inf, -math.inf], pd.NA).dropna().sort_values(ascending=False)


def run_stock_variant(prices: pd.DataFrame, start: date, end: date, variant: Variant) -> dict[str, float | int]:
    close = prices["Close"].dropna(axis=1, thresh=variant.lookback_days + 2).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)

    holdings = pd.Series(dtype=float)
    pending: pd.Series | None = None
    equity = 1.0
    peak = 1.0
    max_drawdown = 0.0
    trades = 0

    for index in range(1, len(close)):
        current_date = close.index[index]
        if current_date.date() < start:
            continue
        if pending is not None:
            old = set(holdings.index)
            new = set(pending.index)
            trades += len(old - new) + len(new - old)
            holdings = pending.copy()
            pending = None

        returns = close.iloc[index] / open_prices.iloc[index] - 1.0
        daily = 0.0
        for ticker, weight in holdings.items():
            value = returns.get(ticker)
            if pd.notna(value):
                daily += float(weight) * float(value)
        equity *= 1.0 + variant.leverage * daily
        peak = max(peak, equity)
        max_drawdown = min(max_drawdown, equity / peak - 1.0)

        if not is_rebalance(index, close.index, variant.rebalance_frequency, list(holdings.index)):
            continue

        if variant.kind == "raw":
            scores = momentum_scores(close, index, variant.lookback_days, score_mode="raw", skip_days=0)
        elif variant.kind == "skip":
            scores = momentum_scores(close, index, variant.lookback_days, score_mode="skip", skip_days=variant.skip_days)
        elif variant.kind == "risk_adjusted":
            scores = risk_adjusted_scores(close, index, variant.lookback_days, variant.skip_days, variant.vol_days)
        else:
            raise ValueError(f"Unsupported stock variant kind: {variant.kind}")
        if variant.sma_days is not None:
            if index + 1 < variant.sma_days:
                scores = pd.Series(dtype=float)
            else:
                sma = close.iloc[index - variant.sma_days + 1 : index + 1].mean()
                current = close.iloc[index]
                scores = scores.loc[scores.index.intersection(current[current > sma].index)]
        pending = stock_weights(close, scores, index, variant)

    return {"return": equity - 1.0, "max_drawdown": max_drawdown, "trades": trades}


def run_blend(prices: pd.DataFrame, etf: pd.DataFrame, start: date, end: date, variant: Variant) -> dict[str, float | int]:
    # Approximate blend by running the stock sleeve and ETF sleeve independently day by day.
    # This avoids lookahead; both sleeves use open-to-close returns after prior close signals.
    close = prices["Close"].dropna(axis=1, thresh=variant.lookback_days + 2).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)
    aligned_etf = etf.reindex(close.index).ffill()

    holdings = pd.Series(dtype=float)
    pending: pd.Series | None = None
    equity = 1.0
    peak = 1.0
    max_drawdown = 0.0
    trades = 0

    for index in range(1, len(close)):
        current_date = close.index[index]
        if current_date.date() < start:
            continue
        if pending is not None:
            old = set(holdings.index)
            new = set(pending.index)
            trades += len(old - new) + len(new - old)
            holdings = pending.copy()
            pending = None
        returns = close.iloc[index] / open_prices.iloc[index] - 1.0
        stock_daily = 0.0
        for ticker, weight in holdings.items():
            value = returns.get(ticker)
            if pd.notna(value):
                stock_daily += float(weight) * float(value)
        etf_daily = aligned_etf["Close"].iloc[index] / aligned_etf["Open"].iloc[index] - 1.0
        etf_daily = 0.0 if pd.isna(etf_daily) else float(etf_daily)
        daily = variant.stock_weight * stock_daily + variant.spmo_weight * etf_daily
        equity *= 1.0 + daily
        peak = max(peak, equity)
        max_drawdown = min(max_drawdown, equity / peak - 1.0)
        if not is_rebalance(index, close.index, variant.rebalance_frequency, list(holdings.index)):
            continue
        scores = momentum_scores(close, index, variant.lookback_days, score_mode="skip", skip_days=variant.skip_days)
        pending = stock_weights(close, scores, index, variant)
    return {"return": equity - 1.0, "max_drawdown": max_drawdown, "trades": trades}


def variants() -> list[Variant]:
    return [
        Variant("Top2 skip21 daily", "skip", max_positions=2),
        Variant("Top3 skip21 daily", "skip", max_positions=3),
        Variant("Top4 skip21 daily", "skip", max_positions=4),
        Variant("Top2 raw daily", "raw", max_positions=2, skip_days=0),
        Variant("Top2 skip21 weekly", "skip", max_positions=2, rebalance_frequency="weekly"),
        Variant("Top2 skip21 monthly", "skip", max_positions=2, rebalance_frequency="monthly"),
        Variant("Top2 skip21 SMA50", "skip", max_positions=2, sma_days=50),
        Variant("Top2 skip21 SMA200", "skip", max_positions=2, sma_days=200),
        Variant("Top100 risk-adj inv-vol monthly", "risk_adjusted", max_positions=100, rebalance_frequency="monthly", weight_mode="inverse_vol", lookback_days=252, skip_days=21, vol_days=252),
        Variant("Top100 risk-adj inv-vol quarterly", "risk_adjusted", max_positions=100, rebalance_frequency="quarterly", weight_mode="inverse_vol", lookback_days=252, skip_days=21, vol_days=252),
        Variant("Top50 risk-adj inv-vol monthly", "risk_adjusted", max_positions=50, rebalance_frequency="monthly", weight_mode="inverse_vol", lookback_days=252, skip_days=21, vol_days=252),
        Variant("Top20 risk-adj inv-vol monthly", "risk_adjusted", max_positions=20, rebalance_frequency="monthly", weight_mode="inverse_vol", lookback_days=252, skip_days=21, vol_days=252),
        Variant("50% SPMO + 50% Top2", "blend", max_positions=2, spmo_weight=0.5, stock_weight=0.5),
        Variant("75% SPMO + 25% Top2", "blend", max_positions=2, spmo_weight=0.75, stock_weight=0.25),
        Variant("90% SPMO + 10% Top2", "blend", max_positions=2, spmo_weight=0.9, stock_weight=0.1),
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
    spmo = load_etf("SPMO", data_start, end)
    periods = [(str(year), date(year, 1, 1), date(year, 12, 31)) for year in range(2020, 2026)]
    periods.append(("2026 YTD", date(2026, 1, 1), end))

    rows = []
    for variant in variants():
        wins = 0
        worst_excess = 1.0
        compound = 1.0
        spmo_compound = 1.0
        year_returns: dict[str, float] = {}
        year_excess: dict[str, float] = {}
        year_drawdowns: dict[str, float] = {}
        for period, start, stop in periods:
            if variant.kind == "blend":
                result = run_blend(prices, spmo, start, stop, variant)
            else:
                result = run_stock_variant(prices, start, stop, variant)
            _, _, spmo_return = benchmark_return("SPMO", start, stop)
            total_return = float(result["return"])
            excess = total_return - spmo_return
            wins += int(excess > 0)
            worst_excess = min(worst_excess, excess)
            compound *= 1.0 + total_return
            spmo_compound *= 1.0 + spmo_return
            year_returns[period] = total_return
            year_excess[period] = excess
            year_drawdowns[period] = float(result["max_drawdown"])
        rows.append(
            {
                "variant": variant.name,
                "wins": wins,
                "worst_excess": worst_excess,
                "compound": compound - 1.0,
                "spmo_compound": spmo_compound - 1.0,
                "returns": year_returns,
                "excess": year_excess,
                "drawdowns": year_drawdowns,
            }
        )
        print(f"{variant.name}: wins={wins}/7, compound={pct(compound - 1.0)}, worst_excess={pct(worst_excess)}")

    rows.sort(key=lambda row: (int(row["wins"]), float(row["compound"])), reverse=True)
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    md_path = report_dir / "sp500_yearly_idea_grid_vs_spmo.md"
    csv_path = report_dir / "sp500_yearly_idea_grid_vs_spmo.csv"

    fields = ["variant", "wins", "compound", "worst_excess"] + [f"{period}_return" for period, _, _ in periods] + [f"{period}_excess" for period, _, _ in periods]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            out = {
                "variant": row["variant"],
                "wins": row["wins"],
                "compound": row["compound"],
                "worst_excess": row["worst_excess"],
            }
            for period, _, _ in periods:
                out[f"{period}_return"] = row["returns"][period]
                out[f"{period}_excess"] = row["excess"][period]
            writer.writerow(out)

    lines = [
        "# S&P 500 Yearly Idea Grid vs SPMO",
        "",
        "Each period is reset independently. Returns execute stock sleeves at next-day open using signals known after the prior close.",
        "",
        "| Rank | Variant | Wins vs SPMO | Compounded Reset Return | Worst Excess | 2024 Return | 2024 Excess | 2026 YTD Return | 2026 YTD Excess |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for rank, row in enumerate(rows, start=1):
        lines.append(
            "| "
            f"{rank} | {row['variant']} | {row['wins']}/7 | {pct(float(row['compound']))} | "
            f"{pct(float(row['worst_excess']))} | {pct(float(row['returns']['2024']))} | "
            f"{pct(float(row['excess']['2024']))} | {pct(float(row['returns']['2026 YTD']))} | "
            f"{pct(float(row['excess']['2026 YTD']))} |"
        )
    lines.extend(
        [
            "",
            "Research notes: SPMO-like broad risk-adjusted/inverse-volatility portfolios improved 2024 robustness but did not beat SPMO in every year. Concentrated top-2 variants keep the strongest compounded return but fail individual years like 2021, 2022 and 2024.",
            "Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(md_path)


if __name__ == "__main__":
    main()
