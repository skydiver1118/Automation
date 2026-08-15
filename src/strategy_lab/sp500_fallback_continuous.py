from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import calculate_summary, load_or_fetch_prices, momentum_scores, run_top_n_backtest


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


def run_fallback(prices: pd.DataFrame, spmo: pd.DataFrame, start: date, end: date, threshold: float = 0.05) -> dict[str, object]:
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
    trading_days = 0
    active_fallback = False

    for index in range(1, len(close)):
        current_date = close.index[index]
        if current_date.date() < start:
            continue
        trading_days += 1
        if pending is not None:
            holdings = list(pending)
            pending = None

        stock_returns = close.iloc[index] / open_prices.iloc[index] - 1.0
        stock_daily = 0.0
        for ticker in holdings:
            value = stock_returns.get(ticker)
            if pd.notna(value):
                stock_daily += 0.5 * float(value)

        if active_fallback:
            fallback_days += 1
            spmo_daily = aligned_spmo["Close"].iloc[index] / aligned_spmo["Open"].iloc[index] - 1.0
            portfolio_daily = 0.0 if pd.isna(spmo_daily) else float(spmo_daily)
        else:
            portfolio_daily = stock_daily

        model_equity *= 1.0 + stock_daily
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

    total_return = portfolio_equity - 1.0
    cagr = portfolio_equity ** (252 / trading_days) - 1.0
    return {
        "total_return": total_return,
        "cagr": cagr,
        "max_drawdown": max_drawdown,
        "fallback_days": fallback_days,
        "final_holdings": ", ".join(holdings),
    }


def main() -> None:
    start = date(2020, 1, 1)
    end = date(2026, 5, 15)
    data_start = date(2018, 12, 19)
    data_dir = Path("data/sp500_top5")
    tickers = pd.read_csv(data_dir / "sp500_constituents.csv")["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(
        data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv",
        tickers,
        data_start,
        end,
        False,
    )
    spmo = load_spmo(data_start, end)
    pure = run_top_n_backtest(
        prices=prices,
        start=start,
        end=end,
        lookback_days=126,
        max_positions=2,
        score_mode="skip",
        skip_days=21,
    )
    pure_summary = calculate_summary(pure)
    fallback = run_fallback(prices, spmo, start, end)
    spmo_start, spmo_end, spmo_return = benchmark_return("SPMO", start, end)

    report = Path("reports/sp500_top2_skip21_fallback5_continuous_2020_2026ytd.md")
    report.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Continuous Top-2 Skip-Month Momentum: Pure vs 5% SPMO Fallback",
        "",
        f"Period: {start.isoformat()} to {end.isoformat()} without annual reset.",
        "",
        "| Strategy | Total Return | CAGR | Max Drawdown | Fallback Days | Final Holdings |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
        f"| Pure top-2 skip21 | {pct(float(pure_summary['total_return']))} | {pct(float(pure_summary['cagr']))} | {pct(float(pure_summary['max_drawdown']))} | 0 | {pure_summary['final_holdings']} |",
        f"| 5% SPMO fallback | {pct(float(fallback['total_return']))} | {pct(float(fallback['cagr']))} | {pct(float(fallback['max_drawdown']))} | {fallback['fallback_days']} | {fallback['final_holdings']} |",
        f"| SPMO buy-and-hold | {pct(spmo_return)} |  |  |  | {spmo_start} to {spmo_end} |",
        "",
        "Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.",
        "",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report)
    print(
        f"pure_return={pct(float(pure_summary['total_return']))}, "
        f"pure_drawdown={pct(float(pure_summary['max_drawdown']))}"
    )
    print(
        f"fallback_return={pct(float(fallback['total_return']))}, "
        f"fallback_drawdown={pct(float(fallback['max_drawdown']))}, "
        f"fallback_days={fallback['fallback_days']}"
    )
    print(f"spmo_return={pct(spmo_return)}")


if __name__ == "__main__":
    main()
