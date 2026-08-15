from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

from src.strategy_lab.sp500_top5 import load_or_fetch_prices, momentum_scores


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


def build_equity_curves(prices: pd.DataFrame, spmo: pd.DataFrame, start: date, end: date) -> pd.DataFrame:
    close = prices["Close"].dropna(axis=1, thresh=128).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)
    aligned_spmo = spmo.reindex(close.index).ffill()

    holdings: list[str] = []
    pending: list[str] | None = None
    pure_equity = 1.0
    fallback_equity = 1.0
    model_equity = 1.0
    model_peak = 1.0
    spmo_start_close = aligned_spmo.loc[aligned_spmo.index.date >= start, "Close"].dropna().iloc[0]
    active_fallback = False
    rows: list[dict[str, object]] = []

    for index in range(1, len(close)):
        current_date = close.index[index]
        if current_date.date() < start:
            continue
        if pending is not None:
            holdings = list(pending)
            pending = None

        stock_returns = close.iloc[index] / open_prices.iloc[index] - 1.0
        stock_daily = 0.0
        for ticker in holdings:
            value = stock_returns.get(ticker)
            if pd.notna(value):
                stock_daily += 0.5 * float(value)

        pure_equity *= 1.0 + stock_daily
        spmo_daily = aligned_spmo["Close"].iloc[index] / aligned_spmo["Open"].iloc[index] - 1.0
        spmo_daily = 0.0 if pd.isna(spmo_daily) else float(spmo_daily)
        spmo_equity = aligned_spmo["Close"].iloc[index] / spmo_start_close

        if active_fallback:
            fallback_equity *= 1.0 + spmo_daily
            sleeve = "SPMO"
        else:
            fallback_equity *= 1.0 + stock_daily
            sleeve = "Top2"

        model_equity *= 1.0 + stock_daily
        model_peak = max(model_peak, model_equity)
        model_drawdown = model_equity / model_peak - 1.0
        active_fallback = model_drawdown <= -0.05

        rows.append(
            {
                "date": current_date.date().isoformat(),
                "pure_top2_skip21": pure_equity,
                "fallback_5pct": fallback_equity,
                "spmo": spmo_equity,
                "fallback_sleeve": sleeve,
                "holdings": " ".join(holdings),
            }
        )

        scores = momentum_scores(close, index, 126, score_mode="skip", skip_days=21)
        selected = list(scores.head(2).index)
        next_holdings = [ticker for ticker in holdings if ticker in selected]
        for ticker in selected:
            if len(next_holdings) >= 2:
                break
            if ticker not in next_holdings:
                next_holdings.append(ticker)
        pending = next_holdings

    frame = pd.DataFrame(rows)
    frame["date"] = pd.to_datetime(frame["date"])
    return frame.set_index("date")


def main() -> None:
    start = date(2020, 1, 1)
    end = date(2026, 5, 15)
    data_start = date(2018, 12, 19)
    data_dir = Path("data/sp500_top5")
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    tickers = pd.read_csv(data_dir / "sp500_constituents.csv")["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(
        data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv",
        tickers,
        data_start,
        end,
        False,
    )
    spmo = load_spmo(data_start, end)
    curves = build_equity_curves(prices, spmo, start, end)

    csv_path = report_dir / "sp500_top2_skip21_equity_curve_2020_2026ytd.csv"
    png_path = report_dir / "sp500_top2_skip21_equity_curve_2020_2026ytd.png"
    curves.to_csv(csv_path)

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(curves.index, curves["pure_top2_skip21"], label="Pure top-2 skip21", linewidth=2)
    ax.plot(curves.index, curves["fallback_5pct"], label="5% SPMO fallback", linewidth=2.4)
    ax.plot(curves.index, curves["spmo"], label="SPMO", linewidth=2)
    ax.set_title("S&P 500 Top-2 Skip-Month Momentum Equity Curve")
    ax.set_ylabel("Growth of $1")
    ax.set_xlabel("")
    ax.legend(loc="upper left")
    ax.set_yscale("log")
    fig.tight_layout()
    fig.savefig(png_path, dpi=160)
    print(png_path)
    print(csv_path)


if __name__ == "__main__":
    main()
