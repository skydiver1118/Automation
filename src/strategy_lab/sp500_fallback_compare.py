from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import (
    calculate_summary,
    load_or_fetch_prices,
    momentum_scores,
    run_top_n_backtest,
)


@dataclass(frozen=True)
class ComparisonRow:
    period: str
    start: date
    end: date
    pure_return: float
    fallback_return: float
    spmo_return: float
    fallback_vs_pure: float
    pure_vs_spmo: float
    fallback_vs_spmo: float
    pure_max_drawdown: float
    fallback_max_drawdown: float
    fallback_days: int
    fallback_final_holdings: str


def pct(value: float) -> str:
    return f"{value:.2%}"


def load_spmo(start: date, end: date) -> pd.DataFrame:
    data = yf.download(
        "SPMO",
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        auto_adjust=True,
        progress=False,
    )
    if isinstance(data.columns, pd.MultiIndex):
        data = data.droplevel(1, axis=1)
    data.index = pd.to_datetime(data.index)
    return data[["Open", "Close"]].dropna()


def run_fallback_period(
    prices: pd.DataFrame,
    spmo: pd.DataFrame,
    start: date,
    end: date,
    threshold: float = 0.05,
) -> tuple[float, float, int, str]:
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

    return portfolio_equity - 1.0, max_drawdown, fallback_days, ", ".join(holdings)


def run_period(prices: pd.DataFrame, spmo: pd.DataFrame, period: str, start: date, end: date) -> ComparisonRow:
    pure_result = run_top_n_backtest(
        prices=prices,
        start=start,
        end=end,
        lookback_days=126,
        max_positions=2,
        score_mode="skip",
        skip_days=21,
    )
    pure_summary = calculate_summary(pure_result)
    fallback_return, fallback_drawdown, fallback_days, final_holdings = run_fallback_period(prices, spmo, start, end)
    _, _, spmo_return = benchmark_return("SPMO", start, end)

    pure_return = float(pure_summary["total_return"])
    return ComparisonRow(
        period=period,
        start=start,
        end=end,
        pure_return=pure_return,
        fallback_return=fallback_return,
        spmo_return=spmo_return,
        fallback_vs_pure=fallback_return - pure_return,
        pure_vs_spmo=pure_return - spmo_return,
        fallback_vs_spmo=fallback_return - spmo_return,
        pure_max_drawdown=float(pure_summary["max_drawdown"]),
        fallback_max_drawdown=fallback_drawdown,
        fallback_days=fallback_days,
        fallback_final_holdings=final_holdings,
    )


def write_reports(rows: list[ComparisonRow], report_dir: Path) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    csv_path = report_dir / "sp500_top2_skip21_fallback5_vs_pure_vs_spmo_2020_2026ytd.csv"
    md_path = report_dir / "sp500_top2_skip21_fallback5_vs_pure_vs_spmo_2020_2026ytd.md"

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ComparisonRow.__dataclass_fields__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    pure_compound = 1.0
    fallback_compound = 1.0
    spmo_compound = 1.0
    lines = [
        "# Top-2 Skip-Month Momentum: Pure vs 5% SPMO Fallback vs SPMO",
        "",
        "Strategy: S&P 500 top 2 by 126-trading-day momentum excluding the most recent 21 trading days. The fallback version uses SPMO whenever the pure stock sleeve's model drawdown is at or below -5%. Each row resets at the period start.",
        "",
        "| Period | Pure Strategy | 5% Fallback | SPMO | Fallback - Pure | Pure - SPMO | Fallback - SPMO | Pure Max DD | Fallback Max DD | Fallback Days |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        pure_compound *= 1.0 + row.pure_return
        fallback_compound *= 1.0 + row.fallback_return
        spmo_compound *= 1.0 + row.spmo_return
        lines.append(
            "| "
            f"{row.period} | "
            f"{pct(row.pure_return)} | "
            f"{pct(row.fallback_return)} | "
            f"{pct(row.spmo_return)} | "
            f"{pct(row.fallback_vs_pure)} | "
            f"{pct(row.pure_vs_spmo)} | "
            f"{pct(row.fallback_vs_spmo)} | "
            f"{pct(row.pure_max_drawdown)} | "
            f"{pct(row.fallback_max_drawdown)} | "
            f"{row.fallback_days} |"
        )

    pure_total = pure_compound - 1.0
    fallback_total = fallback_compound - 1.0
    spmo_total = spmo_compound - 1.0
    lines.extend(
        [
            "",
            "| Compounded Reset-Period Return | Pure Strategy | 5% Fallback | SPMO |",
            "| --- | ---: | ---: | ---: |",
            f"| 2020-2026 YTD | {pct(pure_total)} | {pct(fallback_total)} | {pct(spmo_total)} |",
            "",
            "Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(md_path)


def main() -> None:
    end_2026 = date(2026, 5, 15)
    data_dir = Path("data/sp500_top5")
    data_start = date(2018, 12, 19)
    tickers = pd.read_csv(data_dir / "sp500_constituents.csv")["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(
        data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end_2026.isoformat()}.csv",
        tickers,
        data_start,
        end_2026,
        False,
    )
    spmo = load_spmo(data_start, end_2026)

    periods = [(str(year), date(year, 1, 1), date(year, 12, 31)) for year in range(2020, 2026)]
    periods.append(("2026 YTD", date(2026, 1, 1), end_2026))
    rows = [run_period(prices, spmo, period, start, end) for period, start, end in periods]
    write_reports(rows, Path("reports"))
    for row in rows:
        print(
            f"{row.period}: pure={pct(row.pure_return)}, fallback={pct(row.fallback_return)}, "
            f"SPMO={pct(row.spmo_return)}, fallback_vs_pure={pct(row.fallback_vs_pure)}, "
            f"fallback_vs_spmo={pct(row.fallback_vs_spmo)}"
        )


if __name__ == "__main__":
    main()
