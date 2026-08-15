from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import calculate_summary, load_or_fetch_prices, momentum_scores, run_top_n_backtest


@dataclass(frozen=True)
class Row:
    period: str
    reset: str
    pure_return: float
    pure_max_drawdown: float
    pure_trades: int
    fallback_return: float
    fallback_max_drawdown: float
    fallback_stock_trades: int
    fallback_days: int
    spmo_return: float


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


def run_fallback(prices: pd.DataFrame, spmo: pd.DataFrame, start: date, end: date, threshold: float = 0.05) -> dict[str, float | int]:
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
    stock_trades = 0
    active_fallback = False

    for index in range(1, len(close)):
        current_date = close.index[index]
        if current_date.date() < start:
            continue
        if pending is not None:
            previous = set(holdings)
            next_holdings = set(pending)
            stock_trades += len([ticker for ticker in holdings if ticker not in next_holdings])
            stock_trades += len([ticker for ticker in pending if ticker not in previous])
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

    return {
        "return": portfolio_equity - 1.0,
        "max_drawdown": max_drawdown,
        "fallback_days": fallback_days,
        "stock_trades": stock_trades,
    }


def build_row(prices: pd.DataFrame, spmo: pd.DataFrame, period: str, reset: str, start: date, end: date) -> Row:
    pure_result = run_top_n_backtest(
        prices=prices,
        start=start,
        end=end,
        lookback_days=126,
        max_positions=2,
        score_mode="skip",
        skip_days=21,
    )
    pure = calculate_summary(pure_result)
    fallback = run_fallback(prices, spmo, start, end)
    _, _, spmo_return = benchmark_return("SPMO", start, end)
    return Row(
        period=period,
        reset=reset,
        pure_return=float(pure["total_return"]),
        pure_max_drawdown=float(pure["max_drawdown"]),
        pure_trades=int(pure["buy_trades"]) + int(pure["sell_trades"]),
        fallback_return=float(fallback["return"]),
        fallback_max_drawdown=float(fallback["max_drawdown"]),
        fallback_stock_trades=int(fallback["stock_trades"]),
        fallback_days=int(fallback["fallback_days"]),
        spmo_return=spmo_return,
    )


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
    spmo = load_spmo(data_start, end)
    periods = [(str(year), "Annual", date(year, 1, 1), date(year, 12, 31)) for year in range(2020, 2026)]
    periods.append(("2026 YTD", "YTD", date(2026, 1, 1), end))
    periods.append(("2020-2026 YTD", "No reset", date(2020, 1, 1), end))
    rows = [build_row(prices, spmo, period, reset, start, stop) for period, reset, start, stop in periods]

    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    csv_path = report_dir / "sp500_top2_skip21_combined_annual_continuous_trades.csv"
    md_path = report_dir / "sp500_top2_skip21_combined_annual_continuous_trades.md"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(Row.__dataclass_fields__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)

    lines = [
        "# Top-2 Skip-Month Momentum: Annual and Continuous Summary",
        "",
        "Pure strategy: S&P 500 top 2 by 126-trading-day momentum excluding the most recent 21 trading days.",
        "Fallback strategy: same stock sleeve, but use SPMO whenever the pure stock sleeve model drawdown is at or below -5%.",
        "",
        "| Period | Reset | Pure Return | Pure Max DD | Pure Trades | 5% Fallback Return | Fallback Max DD | Fallback Stock Trades | Fallback Days | SPMO Return |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.period} | "
            f"{row.reset} | "
            f"{pct(row.pure_return)} | "
            f"{pct(row.pure_max_drawdown)} | "
            f"{row.pure_trades} | "
            f"{pct(row.fallback_return)} | "
            f"{pct(row.fallback_max_drawdown)} | "
            f"{row.fallback_stock_trades} | "
            f"{row.fallback_days} | "
            f"{pct(row.spmo_return)} |"
        )
    lines.extend(
        [
            "",
            "Trade count is stock-sleeve buys plus sells. Fallback Days counts trading days where the fallback sleeve used SPMO.",
            "Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(md_path)


if __name__ == "__main__":
    main()
