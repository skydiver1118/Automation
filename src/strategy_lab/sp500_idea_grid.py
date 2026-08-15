from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import load_or_fetch_prices, load_sp500_constituents, save_constituents


@dataclass(frozen=True)
class Variant:
    name: str
    max_positions: int
    score: str
    rebalance: str = "daily"
    positive_only: bool = False
    sma_days: int | None = None
    low_vol_quantile: float | None = None


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def format_pct(value: float) -> str:
    return f"{value:.2%}"


def load_series(symbol: str, start: date, end: date) -> pd.Series:
    data = yf.download(
        symbol,
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        auto_adjust=True,
        progress=False,
    )
    close = data["Close"].dropna()
    if hasattr(close, "columns"):
        close = close.iloc[:, 0].dropna()
    close.index = pd.to_datetime(close.index)
    return close.sort_index()


def annualized_vol(close: pd.DataFrame, index: int, days: int) -> pd.Series:
    if index < days:
        return pd.Series(dtype=float)
    returns = close.pct_change()
    vol = returns.iloc[index - days + 1 : index + 1].std() * math.sqrt(252)
    return vol.replace([math.inf, -math.inf], pd.NA).dropna()


def score_series(close: pd.DataFrame, spy: pd.Series, index: int, variant: Variant) -> pd.Series:
    current = close.iloc[index]
    if variant.score == "mom126":
        if index < 126:
            return pd.Series(dtype=float)
        score = current / close.iloc[index - 126] - 1.0
    elif variant.score == "mom126_skip21":
        if index < 126:
            return pd.Series(dtype=float)
        score = close.iloc[index - 21] / close.iloc[index - 126] - 1.0
    elif variant.score == "mom252_skip21":
        if index < 252:
            return pd.Series(dtype=float)
        score = close.iloc[index - 21] / close.iloc[index - 252] - 1.0
    elif variant.score == "combo_63_126_252_skip21":
        if index < 252:
            return pd.Series(dtype=float)
        score = (
            0.4 * (close.iloc[index - 21] / close.iloc[index - 63] - 1.0)
            + 0.4 * (close.iloc[index - 21] / close.iloc[index - 126] - 1.0)
            + 0.2 * (close.iloc[index - 21] / close.iloc[index - 252] - 1.0)
        )
    elif variant.score == "high52":
        if index < 252:
            return pd.Series(dtype=float)
        high = close.iloc[index - 251 : index + 1].max()
        score = current / high
    elif variant.score == "residual126_skip21":
        if index < 126:
            return pd.Series(dtype=float)
        stock_ret = close.iloc[index - 21] / close.iloc[index - 126] - 1.0
        aligned_spy = spy.reindex(close.index).ffill()
        spy_ret = aligned_spy.iloc[index - 21] / aligned_spy.iloc[index - 126] - 1.0
        daily = close.pct_change().iloc[index - 126 + 1 : index - 21 + 1]
        spy_daily = aligned_spy.pct_change().iloc[index - 126 + 1 : index - 21 + 1]
        variance = float(spy_daily.var())
        beta = daily.cov(spy_daily) / variance if variance else pd.Series(0.0, index=close.columns)
        score = stock_ret - beta * spy_ret
    else:
        raise ValueError(f"Unsupported score: {variant.score}")

    score = score.replace([math.inf, -math.inf], pd.NA).dropna()
    if variant.positive_only:
        score = score[score > 0]
    if variant.sma_days is not None:
        if index + 1 < variant.sma_days:
            return pd.Series(dtype=float)
        sma = close.iloc[index - variant.sma_days + 1 : index + 1].mean()
        score = score.loc[score.index.intersection(current[current > sma].index)]
    if variant.low_vol_quantile is not None:
        vol = annualized_vol(close, index, 126)
        if vol.empty:
            return pd.Series(dtype=float)
        cutoff = vol.quantile(variant.low_vol_quantile)
        score = score.loc[score.index.intersection(vol[vol <= cutoff].index)]
    return score.sort_values(ascending=False)


def default_variants() -> list[Variant]:
    return [
        Variant("top5 mom126 baseline", 5, "mom126"),
        Variant("top1 mom126 skip21", 1, "mom126_skip21"),
        Variant("top2 mom126 skip21", 2, "mom126_skip21"),
        Variant("top3 mom126 skip21", 3, "mom126_skip21"),
        Variant("top4 mom126 skip21", 4, "mom126_skip21"),
        Variant("top5 mom126 skip21 positive", 5, "mom126_skip21", positive_only=True),
        Variant("top5 mom126 skip21 SMA200", 5, "mom126_skip21", sma_days=200),
        Variant("top5 mom126 skip21 low-vol60", 5, "mom126_skip21", low_vol_quantile=0.60),
        Variant("top5 combo 3/6/12 skip21", 5, "combo_63_126_252_skip21"),
        Variant("top5 52-week high", 5, "high52"),
    ]


def is_rebalance_day(index: int, dates: pd.DatetimeIndex, frequency: str, holdings: list[str]) -> bool:
    if frequency == "daily":
        return True
    if frequency == "weekly":
        next_index = min(index + 1, len(dates) - 1)
        return not holdings or index == len(dates) - 1 or dates[next_index].isocalendar().week != dates[index].isocalendar().week
    if frequency == "monthly":
        next_index = min(index + 1, len(dates) - 1)
        return not holdings or index == len(dates) - 1 or dates[next_index].month != dates[index].month
    raise ValueError(f"Unsupported rebalance frequency: {frequency}")


def run_variant(
    prices: pd.DataFrame,
    spy: pd.Series,
    start: date,
    end: date,
    variant: Variant,
) -> dict[str, object]:
    close = prices["Close"].dropna(axis=1, thresh=260).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)

    holdings: list[str] = []
    pending: list[str] | None = None
    equity = 1.0
    peak = 1.0
    max_drawdown = 0.0
    daily_returns: list[float] = []
    buys = 0
    sells = 0

    for index in range(1, len(close)):
        current_date = close.index[index]
        if current_date.date() < start:
            continue
        if pending is not None:
            previous = set(holdings)
            next_holdings = set(pending)
            sells += len([ticker for ticker in holdings if ticker not in next_holdings])
            buys += len([ticker for ticker in pending if ticker not in previous])
            holdings = list(pending)
            pending = None

        returns = close.iloc[index] / open_prices.iloc[index] - 1.0
        daily_return = 0.0
        for ticker in holdings:
            value = returns.get(ticker)
            if pd.notna(value):
                daily_return += (1.0 / variant.max_positions) * float(value)
        equity *= 1.0 + daily_return
        daily_returns.append(daily_return)
        peak = max(peak, equity)
        max_drawdown = min(max_drawdown, equity / peak - 1.0)

        if not is_rebalance_day(index, close.index, variant.rebalance, holdings):
            continue

        scores = score_series(close, spy, index, variant)
        selected = list(scores.head(variant.max_positions).index)
        next_holdings = [ticker for ticker in holdings if ticker in selected]
        for ticker in selected:
            if len(next_holdings) >= variant.max_positions:
                break
            if ticker not in next_holdings:
                next_holdings.append(ticker)
        pending = next_holdings

    trading_days = len(daily_returns)
    total_return = equity - 1.0
    cagr = equity ** (252 / trading_days) - 1.0 if trading_days else 0.0
    series = pd.Series(daily_returns)
    sharpe = math.sqrt(252) * float(series.mean()) / float(series.std()) if len(series) > 1 and series.std() else ""
    return {
        "variant": variant.name,
        "total_return": total_return,
        "cagr": cagr,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "buy_trades": buys,
        "sell_trades": sells,
        "final_holdings": ", ".join(holdings),
    }


def write_reports(rows: list[dict[str, object]], spmo_return: float, report_dir: Path, start: date, end: date) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    stem = f"sp500_idea_grid_{start.isoformat()}_{end.isoformat()}"
    csv_path = report_dir / f"{stem}.csv"
    md_path = report_dir / f"{stem}.md"
    fieldnames = ["variant", "total_return", "excess_vs_spmo", "cagr", "max_drawdown", "sharpe", "buy_trades", "sell_trades", "final_holdings"]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# S&P 500 Momentum Idea Grid",
        "",
        f"Benchmark: SPMO total return = {format_pct(spmo_return)}.",
        "",
        "| Rank | Variant | Return | Excess vs SPMO | CAGR | Max DD | Sharpe | Buys | Final Holdings |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for rank, row in enumerate(rows, start=1):
        sharpe = row["sharpe"]
        sharpe_text = "" if sharpe == "" else f"{float(sharpe):.2f}"
        lines.append(
            "| "
            f"{rank} | "
            f"{row['variant']} | "
            f"{format_pct(float(row['total_return']))} | "
            f"{format_pct(float(row['excess_vs_spmo']))} | "
            f"{format_pct(float(row['cagr']))} | "
            f"{format_pct(float(row['max_drawdown']))} | "
            f"{sharpe_text} | "
            f"{row['buy_trades']} | "
            f"{row['final_holdings']} |"
        )
    lines.extend(
        [
            "",
            "Ideas tested: skip-month cross-sectional momentum, positive absolute momentum, stock SMA200 filters, low-volatility prefilters, 3/6/12-month composite momentum, 52-week-high momentum, and residual/market-adjusted momentum.",
            "Data note: this uses the current S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved reports: {md_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Backtest S&P 500 momentum idea grid against SPMO.")
    parser.add_argument("--start", type=parse_date, default=date(2020, 1, 1))
    parser.add_argument("--end", type=parse_date, default=date(2025, 12, 31))
    parser.add_argument("--data-start", type=parse_date, default=date(2018, 12, 19))
    parser.add_argument("--data-dir", type=Path, default=Path("data/sp500_top5"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    constituents_path = args.data_dir / "sp500_constituents.csv"
    prices_path = args.data_dir / f"adjusted_open_close_{args.data_start.isoformat()}_{args.end.isoformat()}.csv"
    if constituents_path.exists() and not args.refresh:
        constituents = pd.read_csv(constituents_path)
    else:
        constituents = load_sp500_constituents()
        save_constituents(constituents, constituents_path)
    tickers = constituents["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(prices_path, tickers, args.data_start, args.end, args.refresh)
    spy = load_series("SPY", args.data_start, args.end)
    _, _, spmo_return = benchmark_return("SPMO", args.start, args.end)

    rows: list[dict[str, object]] = []
    for variant in default_variants():
        row = run_variant(prices, spy, args.start, args.end, variant)
        row["excess_vs_spmo"] = float(row["total_return"]) - spmo_return
        rows.append(row)
        print(
            f"{variant.name}: return={format_pct(float(row['total_return']))}, "
            f"excess={format_pct(float(row['excess_vs_spmo']))}, "
            f"max_dd={format_pct(float(row['max_drawdown']))}"
        )
    rows.sort(key=lambda row: float(row["total_return"]), reverse=True)
    print(f"SPMO: return={format_pct(spmo_return)}")
    write_reports(rows, spmo_return, args.report_dir, args.start, args.end)


if __name__ == "__main__":
    main()
