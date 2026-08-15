#!/usr/bin/env python3
"""
Backtest Magnificent 7 stocks on a 200-week EMA touch entry rule with ATR/5%-below-EMA exit.

Rules:
- Download adjusted daily data from yfinance.
- Build a 200-week EMA from weekly close prices and forward-fill to daily bars.
- Enter long when the day range touches the 200-week EMA.
- Exit when close falls below the easier of:
  - 5% below EMA200_weekly
  - EMA200_weekly minus ATR_multiplier * ATR(14)
- Compare strategy equity vs buy-and-hold on in-sample and out-of-sample windows.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math

import pandas as pd
import yfinance as yf


SYMBOLS = ["AAPL", "AMZN", "GOOGL", "META", "MSFT", "NVDA", "TSLA"]
ATR_WINDOW = 14
EMA_WINDOW = 200
ATR_MULTIPLIER = 2.5
START_DATE = "2010-01-01"
IS_START = "2010-01-04"
IS_END = "2020-12-31"
OOS_START = "2020-12-31"
OOS_END = "2026-06-01"
OUTPUT_DIR = Path("reports")


@dataclass
class BacktestResult:
    cumulative_return_pct: float
    max_drawdown_pct: float
    final_equity: float
    start_equity: float
    trades: int
    sharpe: float
    sortino: float


def download_data(symbol: str, start_date: str) -> pd.DataFrame:
    df = yf.download(symbol, start=start_date, progress=False, auto_adjust=False)
    if df.empty:
        raise RuntimeError(f"No data returned for {symbol}.")
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs(symbol, axis=1, level=1)
    return df[["Open", "High", "Low", "Close", "Adj Close"]].copy()


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy().sort_index()
    frame["PrevClose"] = frame["Close"].shift(1)
    true_range = pd.concat(
        [
            frame["High"] - frame["Low"],
            (frame["High"] - frame["PrevClose"]).abs(),
            (frame["Low"] - frame["PrevClose"]).abs(),
        ],
        axis=1,
    ).max(axis=1)
    frame["ATR14"] = true_range.rolling(window=ATR_WINDOW, min_periods=ATR_WINDOW).mean()

    weekly_close = frame["Close"].resample("W-FRI").last().to_frame("Close")
    frame["EMA200_weekly"] = (
        weekly_close["Close"].ewm(span=EMA_WINDOW, adjust=False).mean().reindex(frame.index, method="ffill")
    )
    return frame


def split_by_dates(df: pd.DataFrame, is_start: str, is_end: str, oos_start: str, oos_end: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    in_sample = df.loc[is_start:is_end].copy()
    out_sample = df.loc[oos_start:oos_end].copy()
    return in_sample, out_sample


def compute_sharpe_sortino(equity: pd.Series, risk_free_annual: float = 0.0, periods: int = 252) -> tuple[float, float]:
    returns = equity.pct_change().dropna()
    if returns.empty:
        return float("nan"), float("nan")

    risk_free_daily = risk_free_annual / periods
    excess = returns - risk_free_daily
    if excess.std(ddof=0) == 0:
        sharpe = float("nan")
    else:
        sharpe = float(excess.mean() / excess.std(ddof=0) * (periods ** 0.5))

    downside = excess[excess < 0.0]
    if len(downside) == 0:
        sortino = math.inf
    else:
        downside_std = downside.std(ddof=0)
        sortino = float(excess.mean() / downside_std * (periods ** 0.5)) if downside_std != 0 else float("nan")

    return sharpe, sortino


def run_backtest(df: pd.DataFrame, symbol: str) -> tuple[pd.DataFrame, BacktestResult]:
    cash = 1.0
    shares = 0.0
    entry_price = None
    rows = []
    trades = 0

    for current in df.itertuples():
        close = float(current.Close)
        date = current.Index
        ema = current.EMA200_weekly
        atr = current.ATR14
        low = current.Low
        high = current.High

        if pd.isna(ema) or pd.isna(close):
            equity = cash + shares * close
            rows.append((date, close, ema, atr, equity, 1 if shares > 0 else 0))
            continue

        touch = (low <= ema) and (high >= ema)
        if shares == 0 and touch:
            shares = cash / close
            cash = 0.0
            entry_price = close
            trades += 1
        elif shares > 0:
            atr_floor = ema - ATR_MULTIPLIER * (atr if pd.notna(atr) else 0.0)
            exit_floor = max(0.95 * ema, atr_floor)
            if close <= exit_floor:
                cash = shares * close
                shares = 0.0
                entry_price = None

        equity = cash + shares * close
        rows.append((date, close, ema, atr, equity, 1 if shares > 0 else 0))

    equity_series = pd.DataFrame(rows, columns=[
        "Date",
        "Close",
        "EMA200_weekly",
        "ATR14",
        "Equity",
        "InPosition",
    ]).set_index("Date")

    if shares > 0:
        final_close = float(df.iloc[-1]["Close"])
        cash = shares * final_close
        shares = 0.0
        equity_series.loc[df.index[-1], "Equity"] = cash
        equity_series.loc[df.index[-1], "InPosition"] = 0

    start_equity = float(equity_series["Equity"].iloc[0])
    final_equity = float(equity_series["Equity"].iloc[-1])
    cumulative_return = (final_equity / start_equity - 1.0) * 100.0 if start_equity > 0 else float("nan")
    max_dd = (equity_series["Equity"] / equity_series["Equity"].cummax() - 1.0).min() * 100.0
    sharpe, sortino = compute_sharpe_sortino(equity_series["Equity"])

    return equity_series, BacktestResult(
        cumulative_return_pct=cumulative_return,
        max_drawdown_pct=max_dd,
        final_equity=final_equity,
        start_equity=start_equity,
        trades=trades,
        sharpe=sharpe,
        sortino=sortino,
    )


def buy_and_hold_result(df: pd.DataFrame, label: str) -> BacktestResult:
    if df.empty:
        raise ValueError(f"{label} dataframe is empty.")

    if df["Close"].isna().all():
        raise ValueError(f"{label} contains only NaN close values.")

    close = df["Close"].dropna()
    if len(close) < 2:
        raise ValueError(f"{label} does not have enough close observations.")

    start_idx = close.index[0]
    end_idx = close.index[-1]
    start_price = float(close.iloc[0])
    end_price = float(close.iloc[-1])
    final_equity = 1.0 * (end_price / start_price)
    returns = (final_equity - 1.0) * 100.0
    equity = (close / start_price).reindex(df.index).ffill()
    max_dd = (equity / equity.cummax() - 1.0).min() * 100.0
    sharpe, sortino = compute_sharpe_sortino(equity)

    # no trade counting for buy and hold
    return BacktestResult(
        cumulative_return_pct=returns,
        max_drawdown_pct=max_dd,
        final_equity=final_equity,
        start_equity=1.0,
        trades=1,
        sharpe=sharpe,
        sortino=sortino,
    )


def build_row(symbol: str, name: str, res: BacktestResult, bh: BacktestResult) -> dict[str, float | str]:
    return {
        "Symbol": symbol,
        "Segment": name,
        "Strategy_Return_%": round(res.cumulative_return_pct, 4),
        "Strategy_MaxDD_%": round(res.max_drawdown_pct, 4),
        "Strategy_Trades": res.trades,
        "BuyHold_Return_%": round(bh.cumulative_return_pct, 4),
        "BuyHold_MaxDD_%": round(bh.max_drawdown_pct, 4),
        "Strategy_Sharpe": round(res.sharpe, 4) if pd.notna(res.sharpe) else res.sharpe,
        "Strategy_Sortino": round(res.sortino, 4) if pd.notna(res.sortino) else res.sortino,
        "BuyHold_Sharpe": round(bh.sharpe, 4) if pd.notna(bh.sharpe) else bh.sharpe,
        "BuyHold_Sortino": round(bh.sortino, 4) if pd.notna(bh.sortino) else bh.sortino,
    }


def backtest_symbol(symbol: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    raw = download_data(symbol, START_DATE)
    framed = add_indicators(raw)
    in_sample, out_sample = split_by_dates(framed, IS_START, IS_END, OOS_START, OOS_END)

    if in_sample.empty or out_sample.empty:
        raise RuntimeError(f"{symbol} has insufficient data for the requested split.")

    in_equity, in_res = run_backtest(in_sample, symbol)
    oos_equity, oos_res = run_backtest(out_sample, symbol)

    in_bh = buy_and_hold_result(in_sample, "In-Sample")
    oos_bh = buy_and_hold_result(out_sample, "Out-of-Sample")

    rows = [
        build_row(symbol, "In-Sample", in_res, in_bh),
        build_row(symbol, "Out-of-Sample", oos_res, oos_bh),
    ]
    summary = pd.DataFrame(rows)
    return summary, in_equity, oos_equity


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_rows = []

    for symbol in SYMBOLS:
        summary, in_equity, oos_equity = backtest_symbol(symbol)
        all_rows.append(summary)
        in_equity_path = OUTPUT_DIR / f"{symbol}_EMA200_InSample_Equity.csv"
        oos_equity_path = OUTPUT_DIR / f"{symbol}_EMA200_OOS_Equity.csv"
        in_equity.to_csv(in_equity_path)
        oos_equity.to_csv(oos_equity_path)
        print(f"Completed {symbol}")

    combined = pd.concat(all_rows, ignore_index=True)
    out_csv = OUTPUT_DIR / "magnificent7_ema200_Weekly_ExitStrategy_InOut.csv"
    combined.to_csv(out_csv, index=False)

    oos = combined[combined["Segment"] == "Out-of-Sample"].copy()
    oos["OOS_Excess_Return_%"] = oos["Strategy_Return_%"] - oos["BuyHold_Return_%"]
    oos_by_sharpe = oos.sort_values("Strategy_Sharpe", ascending=False)
    oos_by_sortino = oos.sort_values("Strategy_Sortino", ascending=False)
    oos_by_excess = oos.sort_values("OOS_Excess_Return_%", ascending=False)

    oos_sharpe_path = OUTPUT_DIR / "magnificent7_ema200_oos_rank_by_sharpe.csv"
    oos_sortino_path = OUTPUT_DIR / "magnificent7_ema200_oos_rank_by_sortino.csv"
    oos_excess_path = OUTPUT_DIR / "magnificent7_ema200_oos_rank_by_excess_return.csv"
    oos_by_sharpe.to_csv(oos_sharpe_path, index=False)
    oos_by_sortino.to_csv(oos_sortino_path, index=False)
    oos_by_excess.to_csv(oos_excess_path, index=False)

    print("Magnificent 7: 200-week EMA touch strategy vs buy-and-hold")
    print(f"ATR window: {ATR_WINDOW}, ATR multiplier: {ATR_MULTIPLIER}, EMA window: {EMA_WINDOW}")
    print(f"In-sample period: {IS_START} to {IS_END}")
    print(f"Out-sample period: {OOS_START} to {OOS_END}")
    print("\nSummary")
    print(combined.to_string(index=False))
    print("\nOut-of-sample ranking: by Strategy Sharpe (best to worst)")
    print(oos_by_sharpe[["Symbol", "Strategy_Return_%", "BuyHold_Return_%", "Strategy_Sharpe", "Strategy_Sortino"]].to_string(index=False))
    print("\nOut-of-sample ranking: by Strategy Sortino (best to worst)")
    print(oos_by_sortino[["Symbol", "Strategy_Return_%", "BuyHold_Return_%", "Strategy_Sharpe", "Strategy_Sortino"]].to_string(index=False))
    print("\nOut-of-sample ranking: by excess return (Strategy - Buy&Hold, best to worst)")
    print(oos_by_excess[["Symbol", "Strategy_Return_%", "BuyHold_Return_%", "OOS_Excess_Return_%"]].to_string(index=False))
    print(f"\nSaved summary: {out_csv}")
    print(f"Saved ranking (Sharpe): {oos_sharpe_path}")
    print(f"Saved ranking (Sortino): {oos_sortino_path}")
    print(f"Saved ranking (Excess Return): {oos_excess_path}")


if __name__ == "__main__":
    main()
