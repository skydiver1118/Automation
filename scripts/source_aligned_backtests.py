import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


RUN_DATE = "2026-05-19"
OUT_DIR = Path("backtest_results")


@dataclass
class Result:
    strategy: str
    variant: str
    symbol: str
    timeframe: str
    requested_range: str
    actual_range: str
    net_perf_pct: float
    asset_perf_pct: float | None
    max_drawdown_pct: float
    positions: int
    win_rate_pct: float | None
    notes: str


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    return df


def fetch(symbols, *, start=None, end=None, period=None, interval="1d") -> pd.DataFrame:
    df = yf.download(
        tickers=symbols,
        start=start,
        end=end,
        period=period,
        interval=interval,
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    return df


def single_symbol(symbol: str, *, start=None, end=None, period=None, interval="1d") -> pd.DataFrame:
    df = fetch(symbol, start=start, end=end, period=period, interval=interval)
    df = flatten_columns(df)
    df = df.dropna(subset=["Close"])
    return df


def rsi(series: pd.Series, length: int) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(length).mean()
    loss = (-delta.clip(upper=0)).rolling(length).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    peak = equity.cummax()
    dd = equity / peak - 1
    return float(dd.min() * 100)


def summarize(
    strategy: str,
    variant: str,
    symbol: str,
    timeframe: str,
    requested_range: str,
    df: pd.DataFrame,
    equity: pd.Series,
    trades: list[float],
    notes: str,
) -> Result:
    actual_range = "data not available"
    asset_perf = None
    if not df.empty:
        actual_range = f"{df.index.min()} to {df.index.max()}"
        asset_perf = (float(df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1) * 100
    net_perf = (float(equity.iloc[-1]) - 1) * 100 if not equity.empty else 0.0
    wins = [x for x in trades if x > 0]
    win_rate = (len(wins) / len(trades) * 100) if trades else None
    return Result(
        strategy=strategy,
        variant=variant,
        symbol=symbol,
        timeframe=timeframe,
        requested_range=requested_range,
        actual_range=actual_range,
        net_perf_pct=round(net_perf, 2),
        asset_perf_pct=round(asset_perf, 2) if asset_perf is not None else None,
        max_drawdown_pct=round(max_drawdown(equity), 2),
        positions=len(trades),
        win_rate_pct=round(win_rate, 2) if win_rate is not None else None,
        notes=notes,
    )


def regular_hours(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    if out.index.tz is None:
        out.index = out.index.tz_localize("UTC")
    out = out.tz_convert("America/New_York")
    return out.between_time("09:30", "16:00")


def intraday_vwap(df: pd.DataFrame, allow_short: bool) -> tuple[pd.Series, list[float]]:
    df = regular_hours(df)
    if df.empty:
        return pd.Series(dtype=float), []
    equity_values = []
    equity_index = []
    capital = 1.0
    pos = 0
    entry = np.nan
    trades: list[float] = []
    for day, day_df in df.groupby(df.index.date):
        if day_df.empty:
            continue
        tp = (day_df["High"] + day_df["Low"] + day_df["Close"]) / 3
        vwap = (tp * day_df["Volume"]).cumsum() / day_df["Volume"].replace(0, np.nan).cumsum()
        first_idx = day_df.index[0]
        first_close = float(day_df.loc[first_idx, "Close"])
        first_vwap = float(vwap.iloc[0])
        if first_close > first_vwap:
            pos = 1
            entry = first_close
        elif allow_short and first_close < first_vwap:
            pos = -1
            entry = first_close
        else:
            pos = 0
            entry = np.nan
        for ts, row in day_df.iterrows():
            close = float(row["Close"])
            mark = capital if pos == 0 else capital * (1 + pos * (close / entry - 1))
            equity_values.append(mark)
            equity_index.append(ts)
            is_last = ts == day_df.index[-1]
            cross_exit = (pos == 1 and close < float(vwap.loc[ts])) or (pos == -1 and close > float(vwap.loc[ts]))
            if pos != 0 and (cross_exit or is_last):
                ret = pos * (close / entry - 1)
                trades.append(ret)
                capital *= 1 + ret
                pos = 0
                entry = np.nan
                equity_values[-1] = capital
    return pd.Series(equity_values, index=equity_index), trades


def intraday_orb(df: pd.DataFrame, allow_short: bool) -> tuple[pd.Series, list[float]]:
    df = regular_hours(df)
    if df.empty:
        return pd.Series(dtype=float), []
    equity_values = []
    equity_index = []
    capital = 1.0
    trades: list[float] = []
    volume_sma = df["Volume"].rolling(20).mean()
    for day, day_df in df.groupby(df.index.date):
        if len(day_df) < 2:
            continue
        first_high = float(day_df["High"].iloc[0])
        first_low = float(day_df["Low"].iloc[0])
        pos = 0
        entry = np.nan
        for ts, row in day_df.iterrows():
            close = float(row["Close"])
            mark = capital if pos == 0 else capital * (1 + pos * (close / entry - 1))
            equity_values.append(mark)
            equity_index.append(ts)
            if ts == day_df.index[0]:
                continue
            is_last = ts == day_df.index[-1]
            vol_ok = not np.isnan(volume_sma.loc[ts]) and row["Volume"] > volume_sma.loc[ts]
            if pos == 0 and vol_ok and close > first_high:
                pos = 1
                entry = close
            elif pos == 0 and allow_short and vol_ok and close < first_low:
                pos = -1
                entry = close
            elif pos == 1 and (close < first_low or is_last):
                ret = close / entry - 1
                trades.append(ret)
                capital *= 1 + ret
                pos = 0
                entry = np.nan
                equity_values[-1] = capital
            elif pos == -1 and (close > first_high or is_last):
                ret = -(close / entry - 1)
                trades.append(ret)
                capital *= 1 + ret
                pos = 0
                entry = np.nan
                equity_values[-1] = capital
    return pd.Series(equity_values, index=equity_index), trades


def daily_signal_backtest(df: pd.DataFrame, entry_signal: pd.Series, exit_signal: pd.Series) -> tuple[pd.Series, list[float]]:
    capital = 1.0
    pos = 0
    entry = np.nan
    equity_values = []
    trades: list[float] = []
    for ts, row in df.iterrows():
        close = float(row["Close"])
        if pos == 0 and bool(entry_signal.loc[ts]):
            pos = 1
            entry = close
        mark = capital if pos == 0 else capital * (close / entry)
        equity_values.append(mark)
        if pos == 1 and bool(exit_signal.loc[ts]):
            ret = close / entry - 1
            trades.append(ret)
            capital *= 1 + ret
            pos = 0
            entry = np.nan
            equity_values[-1] = capital
    if pos == 1:
        close = float(df["Close"].iloc[-1])
        trades.append(close / entry - 1)
        equity_values[-1] = capital * (1 + trades[-1])
    return pd.Series(equity_values, index=df.index), trades


def ma_cross(df: pd.DataFrame) -> tuple[pd.Series, list[float]]:
    sma50 = df["Close"].rolling(50).mean()
    sma200 = df["Close"].rolling(200).mean()
    entry = (sma50 > sma200) & (sma50.shift(1) <= sma200.shift(1))
    exit_ = (sma50 < sma200) & (sma50.shift(1) >= sma200.shift(1))
    return daily_signal_backtest(df, entry.fillna(False), exit_.fillna(False))


def abs_momentum_252(df: pd.DataFrame) -> tuple[pd.Series, list[float]]:
    sma200 = df["Close"].rolling(200).mean()
    cond = (df["Close"] > sma200) & (df["Close"] > df["Close"].shift(252))
    entry = cond & (~cond.shift(1).fillna(False))
    exit_ = ~cond
    return daily_signal_backtest(df, entry.fillna(False), exit_.fillna(False))


def connors_rsi2(df: pd.DataFrame) -> tuple[pd.Series, list[float]]:
    sma5 = df["Close"].rolling(5).mean()
    sma200 = df["Close"].rolling(200).mean()
    rsi2 = rsi(df["Close"], 2)
    entry = (df["Close"] > sma200) & (rsi2 <= 5)
    exit_ = (df["Close"] > sma5) | (df["Close"] < sma200)
    return daily_signal_backtest(df, entry.fillna(False), exit_.fillna(False))


def gem_rotation() -> Result:
    tickers = ["SPY", "VEU", "AGG", "BIL"]
    raw = fetch(tickers, start="2018-01-02", end="2026-05-20", interval="1d")
    close = raw["Close"].dropna(how="all").ffill()
    close = close.dropna()
    if close.empty:
        return Result("Momentum / relative strength", "GEM ETF rotation", "SPY/VEU/AGG/BIL", "Daily/monthly rebalance", "2018-01-02 to 2026-05-19", "data not available", 0, None, 0, 0, None, "Data not available")
    monthly = close.resample("ME").last()
    ret12 = monthly[["SPY", "VEU"]].pct_change(12)
    chosen = []
    for ts, row in ret12.iterrows():
        if row.isna().any():
            chosen.append((ts, "BIL"))
        else:
            best = row.idxmax()
            chosen.append((ts, best if row[best] > 0 else "AGG"))
    alloc = pd.Series({ts: sym for ts, sym in chosen})
    daily_alloc = alloc.reindex(close.index, method="ffill").shift(1).fillna("BIL")
    daily_ret = close.pct_change().fillna(0)
    strat_ret = []
    for ts in close.index:
        sym = daily_alloc.loc[ts]
        strat_ret.append(daily_ret.loc[ts, sym])
    equity = (1 + pd.Series(strat_ret, index=close.index)).cumprod()
    trades = []
    prev_sym = daily_alloc.iloc[0]
    entry_px = close.iloc[0][prev_sym]
    for ts, sym in daily_alloc.iloc[1:].items():
        if sym != prev_sym:
            exit_px = close.loc[ts, prev_sym]
            trades.append(float(exit_px / entry_px - 1))
            prev_sym = sym
            entry_px = close.loc[ts, sym]
    trades.append(float(close.iloc[-1][prev_sym] / entry_px - 1))
    asset_perf = (float(close["SPY"].iloc[-1] / close["SPY"].iloc[0]) - 1) * 100
    return Result(
        strategy="Momentum / relative strength",
        variant="GEM ETF rotation: choose stronger of SPY/VEU if positive, else AGG",
        symbol="SPY/VEU/AGG/BIL",
        timeframe="Daily signal, monthly rebalance",
        requested_range="2018-01-02 to 2026-05-19",
        actual_range=f"{close.index.min()} to {close.index.max()}",
        net_perf_pct=round((float(equity.iloc[-1]) - 1) * 100, 2),
        asset_perf_pct=round(asset_perf, 2),
        max_drawdown_pct=round(max_drawdown(equity), 2),
        positions=len(trades),
        win_rate_pct=round(len([t for t in trades if t > 0]) / len(trades) * 100, 2) if trades else None,
        notes="Source-aligned multi-ETF rotation; not a single-symbol TrendSpider proxy.",
    )


def run() -> list[Result]:
    results: list[Result] = []
    intraday_cases = [
        ("5m", "60d", "5-minute Yahoo intraday limit"),
        ("60m", "730d", "1-hour Yahoo intraday limit"),
    ]
    for symbol in ["QQQ", "TQQQ"]:
        for interval, period, note in intraday_cases:
            df = single_symbol(symbol, period=period, interval=interval)
            requested = f"period={period}; interval={interval}"
            for allow_short in [False, True]:
                eq, trades = intraday_vwap(df, allow_short)
                results.append(
                    summarize(
                        "VWAP trend / reclaim",
                        "Long+short first-bar VWAP" if allow_short else "Long-only first-bar VWAP",
                        symbol,
                        interval,
                        requested,
                        regular_hours(df),
                        eq,
                        trades,
                        f"Original research uses QQQ/TQQQ 1-minute; {note}; no costs/slippage.",
                    )
                )
                eq, trades = intraday_orb(df, allow_short)
                results.append(
                    summarize(
                        "Opening range breakout",
                        "Long+short first-bar ORB with volume filter" if allow_short else "Long-only first-bar ORB with volume filter",
                        symbol,
                        interval,
                        requested,
                        regular_hours(df),
                        eq,
                        trades,
                        f"ETF proxy for stocks-in-play ORB source; {note}; no costs/slippage.",
                    )
                )
    for symbol in ["SPY", "QQQ", "TQQQ", "SPYM"]:
        df = single_symbol(symbol, start="2018-01-02", end="2026-05-20", interval="1d")
        if df.empty:
            continue
        for name, fn, variant in [
            ("Moving-average crossover", ma_cross, "Daily SMA50/SMA200 crossover"),
            ("Relative strength / absolute momentum", abs_momentum_252, "Daily close > SMA200 and > 252 bars ago"),
            ("RSI(2) / mean reversion", connors_rsi2, "Daily Connors-style RSI(2)<=5 above SMA200, exit above SMA5"),
        ]:
            eq, trades = fn(df)
            results.append(
                summarize(
                    name,
                    variant,
                    symbol,
                    "1d",
                    "2018-01-02 to 2026-05-19",
                    df,
                    eq,
                    trades,
                    "Daily ETF proxy; no costs/slippage.",
                )
            )
    results.append(gem_rotation())
    return results


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    results = run()
    rows = [asdict(r) for r in results]
    pd.DataFrame(rows).to_csv(OUT_DIR / "source_aligned_backtests.csv", index=False)
    (OUT_DIR / "source_aligned_backtests.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
