import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


OUT_DIR = Path("backtest_results")
DAILY_START = "2010-03-11"
DAILY_END_EXCLUSIVE = "2026-05-21"
DAILY_END_LABEL = "2026-05-20"
SYMBOLS = ["SOXL", "SMH"]


@dataclass
class Result:
    family: str
    variant: str
    symbol: str
    timeframe: str
    requested_range: str
    actual_range: str
    net_perf_pct: float
    asset_symbol: str
    asset_perf_pct: float
    excess_vs_asset_pct: float
    beat_asset: bool
    strategy_max_drawdown_pct: float
    asset_max_drawdown_pct: float
    positions: int
    win_rate_pct: float | None
    notes: str


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    return df


def fetch_single(symbol: str, *, start=None, end=None, period=None, interval="1d") -> pd.DataFrame:
    df = yf.download(
        symbol,
        start=start,
        end=end,
        period=period,
        interval=interval,
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    df = flatten_columns(df)
    if df.empty:
        return df
    return df.dropna(subset=["Close"])


def fetch_multi(symbols: list[str], *, start=None, end=None, interval="1d") -> pd.DataFrame:
    return yf.download(
        symbols,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )


def regular_hours(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy()
    if out.index.tz is None:
        out.index = out.index.tz_localize("UTC")
    out = out.tz_convert("America/New_York")
    return out.between_time("09:30", "16:00")


def rsi(series: pd.Series, length: int) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(length).mean()
    loss = (-delta.clip(upper=0)).rolling(length).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    dd = equity / equity.cummax() - 1
    return float(dd.min() * 100)


def perf_pct(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    return (float(equity.iloc[-1]) - 1) * 100


def price_equity(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=float)
    return df["Close"] / df["Close"].iloc[0]


def actual_range(df: pd.DataFrame) -> str:
    if df.empty:
        return "data not available"
    return f"{df.index.min()} to {df.index.max()}"


def win_rate(trades: list[float]) -> float | None:
    if not trades:
        return None
    return len([trade for trade in trades if trade > 0]) / len(trades) * 100


def summarize(
    *,
    family: str,
    variant: str,
    symbol: str,
    timeframe: str,
    requested_range: str,
    df: pd.DataFrame,
    equity: pd.Series,
    trades: list[float],
    notes: str,
    asset_symbol: str | None = None,
    asset_equity: pd.Series | None = None,
) -> Result:
    bench_symbol = asset_symbol or symbol
    benchmark = price_equity(df) if asset_equity is None else asset_equity
    net = perf_pct(equity)
    asset = perf_pct(benchmark)
    excess = net - asset
    return Result(
        family=family,
        variant=variant,
        symbol=symbol,
        timeframe=timeframe,
        requested_range=requested_range,
        actual_range=actual_range(df),
        net_perf_pct=round(net, 2),
        asset_symbol=bench_symbol,
        asset_perf_pct=round(asset, 2),
        excess_vs_asset_pct=round(excess, 2),
        beat_asset=bool(excess > 0),
        strategy_max_drawdown_pct=round(max_drawdown(equity), 2),
        asset_max_drawdown_pct=round(max_drawdown(benchmark), 2),
        positions=len(trades),
        win_rate_pct=round(win_rate(trades), 2) if win_rate(trades) is not None else None,
        notes=notes,
    )


def daily_long_only_backtest(
    df: pd.DataFrame,
    entry_signal: pd.Series,
    exit_signal: pd.Series,
    *,
    stop_loss_pct: float | None = None,
) -> tuple[pd.Series, list[float]]:
    capital = 1.0
    entry = np.nan
    pos = 0
    equity_values = []
    trades: list[float] = []
    closes = df["Close"].to_numpy(dtype=float)
    entries = entry_signal.reindex(df.index).fillna(False).to_numpy(dtype=bool)
    exits = exit_signal.reindex(df.index).fillna(False).to_numpy(dtype=bool)
    for i, close in enumerate(closes):
        if pos == 0 and entries[i]:
            pos = 1
            entry = close
        mark = capital if pos == 0 else capital * (close / entry)
        equity_values.append(mark)
        stop_hit = stop_loss_pct is not None and pos == 1 and close <= entry * (1 - stop_loss_pct)
        if pos == 1 and (exits[i] or stop_hit):
            trade = close / entry - 1
            trades.append(trade)
            capital *= 1 + trade
            pos = 0
            entry = np.nan
            equity_values[-1] = capital
    if pos == 1:
        close = float(df["Close"].iloc[-1])
        trade = close / entry - 1
        trades.append(trade)
        equity_values[-1] = capital * (1 + trade)
    return pd.Series(equity_values, index=df.index), trades


def search_ma(symbol: str, df: pd.DataFrame) -> list[Result]:
    results: list[Result] = []
    fast_windows = [2, 3, 5, 8, 10, 13, 20, 21, 30, 40, 50, 63, 100, 126]
    slow_windows = [20, 30, 40, 50, 63, 100, 126, 150, 200, 252, 300]
    stop_losses = [None, 0.10, 0.20, 0.30]
    for fast in fast_windows:
        for slow in slow_windows:
            if fast >= slow:
                continue
            fast_ma = df["Close"].rolling(fast).mean()
            slow_ma = df["Close"].rolling(slow).mean()
            for mode in ["cross", "state"]:
                if mode == "cross":
                    entry = (fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))
                    exit_ = (fast_ma < slow_ma) & (fast_ma.shift(1) >= slow_ma.shift(1))
                else:
                    condition = fast_ma > slow_ma
                    entry = condition & (~condition.shift(1).fillna(False))
                    exit_ = ~condition
                for stop_loss in stop_losses:
                    eq, trades = daily_long_only_backtest(df, entry.fillna(False), exit_.fillna(False), stop_loss_pct=stop_loss)
                    stop_label = "no stop" if stop_loss is None else f"{int(stop_loss * 100)}% stop"
                    results.append(
                        summarize(
                            family="Moving-average trend",
                            variant=f"SMA{fast}/SMA{slow} {mode}, {stop_label}",
                            symbol=symbol,
                            timeframe="1d",
                            requested_range=f"{DAILY_START} to {DAILY_END_LABEL}",
                            df=df,
                            equity=eq,
                            trades=trades,
                            notes="Daily MA parameter search; optimized in-sample; no costs/slippage.",
                        )
                    )
    return results


def search_abs_momentum(symbol: str, df: pd.DataFrame) -> list[Result]:
    results: list[Result] = []
    lookbacks = [10, 21, 42, 63, 84, 126, 168, 189, 252, 300]
    trend_windows = [0, 20, 50, 100, 150, 200, 252]
    stop_losses = [None, 0.10, 0.20, 0.30]
    for lookback in lookbacks:
        positive = df["Close"] > df["Close"].shift(lookback)
        for trend_window in trend_windows:
            if trend_window == 0:
                condition = positive
                trend_label = "no trend SMA"
            else:
                condition = positive & (df["Close"] > df["Close"].rolling(trend_window).mean())
                trend_label = f"above SMA{trend_window}"
            entry = condition & (~condition.shift(1).fillna(False))
            exit_ = ~condition
            for stop_loss in stop_losses:
                eq, trades = daily_long_only_backtest(df, entry.fillna(False), exit_.fillna(False), stop_loss_pct=stop_loss)
                stop_label = "no stop" if stop_loss is None else f"{int(stop_loss * 100)}% stop"
                results.append(
                    summarize(
                        family="Absolute momentum",
                        variant=f"{lookback}-day positive return, {trend_label}, {stop_label}",
                        symbol=symbol,
                        timeframe="1d",
                        requested_range=f"{DAILY_START} to {DAILY_END_LABEL}",
                        df=df,
                        equity=eq,
                        trades=trades,
                        notes="Daily absolute momentum parameter search; optimized in-sample; no costs/slippage.",
                    )
                )
    return results


def search_rsi_pullback(symbol: str, df: pd.DataFrame) -> list[Result]:
    results: list[Result] = []
    rsi_lengths = [2, 3, 4, 5]
    thresholds = [3, 5, 10, 15, 20, 25]
    trend_windows = [20, 50, 100, 150, 200]
    exit_windows = [2, 3, 5, 10, 20, 50]
    stop_losses = [None, 0.05, 0.10, 0.20]
    for rsi_len in rsi_lengths:
        rsi_value = rsi(df["Close"], rsi_len)
        for threshold in thresholds:
            for trend_window in trend_windows:
                trend_ma = df["Close"].rolling(trend_window).mean()
                for exit_window in exit_windows:
                    exit_ma = df["Close"].rolling(exit_window).mean()
                    entry = (df["Close"] > trend_ma) & (rsi_value <= threshold)
                    exit_ = (df["Close"] > exit_ma) | (df["Close"] < trend_ma)
                    for stop_loss in stop_losses:
                        eq, trades = daily_long_only_backtest(df, entry.fillna(False), exit_.fillna(False), stop_loss_pct=stop_loss)
                        stop_label = "no stop" if stop_loss is None else f"{int(stop_loss * 100)}% stop"
                        results.append(
                            summarize(
                                family="RSI pullback",
                                variant=f"RSI{rsi_len}<={threshold}, above SMA{trend_window}, exit above SMA{exit_window}, {stop_label}",
                                symbol=symbol,
                                timeframe="1d",
                                requested_range=f"{DAILY_START} to {DAILY_END_LABEL}",
                                df=df,
                                equity=eq,
                                trades=trades,
                                notes="Daily RSI pullback parameter search; optimized in-sample; no costs/slippage.",
                            )
                        )
    return results


def intraday_vwap_variant(
    df: pd.DataFrame,
    *,
    allow_short: bool,
    min_bars: int,
    entry_mode: str,
    target_pct: float | None,
    stop_pct: float | None,
) -> tuple[pd.Series, list[float]]:
    if df.empty:
        return pd.Series(dtype=float), []
    capital = 1.0
    trades: list[float] = []
    equity_values = []
    equity_index = []
    for _, day_df in df.groupby(df.index.date, sort=False):
        if len(day_df) <= min_bars:
            continue
        tp = (day_df["High"] + day_df["Low"] + day_df["Close"]) / 3
        vwap = (tp * day_df["Volume"]).cumsum() / day_df["Volume"].replace(0, np.nan).cumsum()
        pos = 0
        entry = np.nan
        closes = day_df["Close"].to_numpy(dtype=float)
        highs = day_df["High"].to_numpy(dtype=float)
        lows = day_df["Low"].to_numpy(dtype=float)
        vwap_values = vwap.to_numpy(dtype=float)
        index_values = day_df.index.to_numpy()
        for bar_index, close in enumerate(closes):
            ts = index_values[bar_index]
            mark = capital if pos == 0 else capital * (1 + pos * (close / entry - 1))
            equity_values.append(mark)
            equity_index.append(ts)
            if bar_index < min_bars:
                continue
            is_last = bar_index == len(closes) - 1
            prev_close = closes[bar_index - 1]
            prev_vwap = vwap_values[bar_index - 1]
            cur_vwap = vwap_values[bar_index]
            if entry_mode == "state":
                long_entry = close > cur_vwap
                short_entry = close < cur_vwap
            elif entry_mode == "reclaim":
                long_entry = prev_close <= prev_vwap and close > cur_vwap
                short_entry = prev_close >= prev_vwap and close < cur_vwap
            else:
                long_entry = close > cur_vwap and lows[bar_index] <= cur_vwap
                short_entry = close < cur_vwap and highs[bar_index] >= cur_vwap
            if pos == 0 and long_entry:
                pos = 1
                entry = close
            elif pos == 0 and allow_short and short_entry:
                pos = -1
                entry = close
            elif pos != 0:
                trade = pos * (close / entry - 1)
                stop_hit = stop_pct is not None and trade <= -stop_pct
                target_hit = target_pct is not None and trade >= target_pct
                vwap_exit = (pos == 1 and close < cur_vwap) or (pos == -1 and close > cur_vwap)
                if stop_hit or target_hit or vwap_exit or is_last:
                    trades.append(trade)
                    capital *= 1 + trade
                    pos = 0
                    entry = np.nan
                    equity_values[-1] = capital
    return pd.Series(equity_values, index=equity_index), trades


def intraday_orb_variant(
    df: pd.DataFrame,
    *,
    allow_short: bool,
    opening_bars: int,
    volume_mult: float,
    target_rr: float | None,
) -> tuple[pd.Series, list[float]]:
    if df.empty:
        return pd.Series(dtype=float), []
    capital = 1.0
    trades: list[float] = []
    equity_values = []
    equity_index = []
    volume_sma = df["Volume"].rolling(20).mean()
    for _, day_df in df.groupby(df.index.date, sort=False):
        if len(day_df) <= opening_bars:
            continue
        opening = day_df.iloc[:opening_bars]
        range_high = float(opening["High"].max())
        range_low = float(opening["Low"].min())
        range_size = max(range_high - range_low, 0.01)
        pos = 0
        entry = np.nan
        stop = np.nan
        target = np.nan
        closes = day_df["Close"].to_numpy(dtype=float)
        volumes = day_df["Volume"].to_numpy(dtype=float)
        vol_refs = volume_sma.reindex(day_df.index).to_numpy(dtype=float)
        index_values = day_df.index.to_numpy()
        for bar_index, close in enumerate(closes):
            ts = index_values[bar_index]
            mark = capital if pos == 0 else capital * (1 + pos * (close / entry - 1))
            equity_values.append(mark)
            equity_index.append(ts)
            if bar_index < opening_bars:
                continue
            is_last = bar_index == len(closes) - 1
            vol_ref = vol_refs[bar_index]
            vol_ok = volume_mult == 0 or (not np.isnan(vol_ref) and volumes[bar_index] >= volume_mult * float(vol_ref))
            if pos == 0 and vol_ok and close > range_high:
                pos = 1
                entry = close
                stop = min(range_low, entry - range_size)
                target = np.nan if target_rr is None else entry + target_rr * (entry - stop)
            elif pos == 0 and allow_short and vol_ok and close < range_low:
                pos = -1
                entry = close
                stop = max(range_high, entry + range_size)
                target = np.nan if target_rr is None else entry - target_rr * (stop - entry)
            elif pos != 0:
                stop_hit = (pos == 1 and close <= stop) or (pos == -1 and close >= stop)
                target_hit = target_rr is not None and ((pos == 1 and close >= target) or (pos == -1 and close <= target))
                opposite_hit = (pos == 1 and close < range_low) or (pos == -1 and close > range_high)
                if stop_hit or target_hit or opposite_hit or is_last:
                    trade = pos * (close / entry - 1)
                    trades.append(trade)
                    capital *= 1 + trade
                    pos = 0
                    entry = np.nan
                    stop = np.nan
                    target = np.nan
                    equity_values[-1] = capital
    return pd.Series(equity_values, index=equity_index), trades


def search_intraday(symbol: str, timeframe: str, period: str, df: pd.DataFrame) -> list[Result]:
    results: list[Result] = []
    rh_df = regular_hours(df)
    requested = f"period={period}; interval={timeframe}"
    min_bars_by_timeframe = [1, 3, 6] if timeframe in {"5m", "15m"} else [1, 2]
    for allow_short in [False, True]:
        direction = "long+short" if allow_short else "long-only"
        for entry_mode in ["state", "reclaim", "pullback"]:
            for min_bars in min_bars_by_timeframe:
                for target_pct in [None, 0.01, 0.02]:
                    for stop_pct in [None, 0.01]:
                        eq, trades = intraday_vwap_variant(
                            rh_df,
                            allow_short=allow_short,
                            min_bars=min_bars,
                            entry_mode=entry_mode,
                            target_pct=target_pct,
                            stop_pct=stop_pct,
                        )
                        target_label = "no target" if target_pct is None else f"{target_pct * 100:.1f}% target"
                        stop_label = "no stop" if stop_pct is None else f"{stop_pct * 100:.1f}% stop"
                        results.append(
                            summarize(
                                family="VWAP intraday",
                                variant=f"{direction} {entry_mode}, after {min_bars} bars, {target_label}, {stop_label}",
                                symbol=symbol,
                                timeframe=timeframe,
                                requested_range=requested,
                                df=rh_df,
                                equity=eq,
                                trades=trades,
                                notes="Intraday VWAP parameter search; no costs/slippage.",
                            )
                        )
    opening_bars_by_timeframe = [1, 3, 6, 12] if timeframe in {"5m", "15m"} else [1, 2]
    for allow_short in [False, True]:
        direction = "long+short" if allow_short else "long-only"
        for opening_bars in opening_bars_by_timeframe:
            for volume_mult in [0, 1.0, 1.5, 2.0]:
                for target_rr in [None, 1.0, 2.0, 3.0]:
                    eq, trades = intraday_orb_variant(
                        rh_df,
                        allow_short=allow_short,
                        opening_bars=opening_bars,
                        volume_mult=volume_mult,
                        target_rr=target_rr,
                    )
                    vol_label = "no volume filter" if volume_mult == 0 else f"volume >= {volume_mult:.1f}x SMA20"
                    target_label = "no target" if target_rr is None else f"{target_rr:.1f}R target"
                    results.append(
                        summarize(
                            family="ORB intraday",
                            variant=f"{direction}, {opening_bars}-bar ORB, {vol_label}, {target_label}",
                            symbol=symbol,
                            timeframe=timeframe,
                            requested_range=requested,
                            df=rh_df,
                            equity=eq,
                            trades=trades,
                            notes="Intraday opening-range parameter search; no costs/slippage.",
                        )
                    )
    return results


def monthly_rotation_backtest(close: pd.DataFrame, risky: list[str], defensive: str, lookback_months: int) -> tuple[pd.Series, list[float], pd.Series]:
    monthly = close.resample("ME").last()
    returns = monthly[risky].pct_change(lookback_months)
    choices = []
    for ts, row in returns.iterrows():
        if row.isna().all():
            choices.append((ts, defensive))
            continue
        best = row.idxmax()
        choices.append((ts, best if row[best] > 0 else defensive))
    monthly_alloc = pd.Series({ts: symbol for ts, symbol in choices})
    daily_alloc = monthly_alloc.reindex(close.index, method="ffill").shift(1).fillna(defensive)
    daily_returns = close.pct_change().fillna(0)
    strategy_returns = pd.Series([daily_returns.loc[ts, daily_alloc.loc[ts]] for ts in close.index], index=close.index)
    equity = (1 + strategy_returns).cumprod()
    trades: list[float] = []
    current_symbol = daily_alloc.iloc[0]
    entry_price = close.iloc[0][current_symbol]
    for ts, symbol in daily_alloc.iloc[1:].items():
        if symbol != current_symbol:
            trades.append(float(close.loc[ts, current_symbol] / entry_price - 1))
            current_symbol = symbol
            entry_price = close.loc[ts, symbol]
    trades.append(float(close.iloc[-1][current_symbol] / entry_price - 1))
    return equity, trades, daily_alloc


def search_rotation(close: pd.DataFrame) -> list[Result]:
    results: list[Result] = []
    close = close.dropna(how="all").ffill().dropna()
    if not {"SOXL", "SMH", "BIL", "AGG"}.issubset(close.columns):
        return results
    risky = ["SMH", "SOXL"]
    for defensive in ["BIL", "AGG"]:
        for benchmark in ["SMH", "SOXL"]:
            for lookback in [1, 2, 3, 6, 9, 12]:
                eq, trades, _ = monthly_rotation_backtest(close, risky, defensive, lookback)
                benchmark_equity = close[benchmark] / close[benchmark].iloc[0]
                results.append(
                    summarize(
                        family="SMH/SOXL relative-strength rotation",
                        variant=f"Choose stronger of SMH/SOXL by {lookback}-month return if positive, else {defensive}",
                        symbol=f"SMH/SOXL/{defensive}",
                        timeframe="Daily signal, monthly rebalance",
                        requested_range=f"{DAILY_START} to {DAILY_END_LABEL}",
                        df=pd.DataFrame({"Close": close[benchmark]}),
                        equity=eq,
                        trades=trades,
                        asset_symbol=benchmark,
                        asset_equity=benchmark_equity,
                        notes="Monthly ETF rotation parameter search; benchmark listed in asset_symbol.",
                    )
                )
    return results


def run() -> list[Result]:
    results: list[Result] = []
    daily_data: dict[str, pd.DataFrame] = {}
    for symbol in SYMBOLS:
        df = fetch_single(symbol, start=DAILY_START, end=DAILY_END_EXCLUSIVE, interval="1d")
        daily_data[symbol] = df
        if df.empty:
            continue
        results.extend(search_ma(symbol, df))
        results.extend(search_abs_momentum(symbol, df))
        results.extend(search_rsi_pullback(symbol, df))
    intraday_cases = [("5m", "60d"), ("15m", "60d"), ("30m", "60d"), ("60m", "730d")]
    for symbol in SYMBOLS:
        for timeframe, period in intraday_cases:
            df = fetch_single(symbol, period=period, interval=timeframe)
            if df.empty:
                continue
            results.extend(search_intraday(symbol, timeframe, period, df))
    multi = fetch_multi(["SMH", "SOXL", "BIL", "AGG"], start=DAILY_START, end=DAILY_END_EXCLUSIVE, interval="1d")
    if not multi.empty and "Close" in multi:
        results.extend(search_rotation(multi["Close"]))
    return results


def write_outputs(results: list[Result]) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    rows = [asdict(result) for result in results]
    all_df = pd.DataFrame(rows)
    all_df = all_df.sort_values(["beat_asset", "excess_vs_asset_pct", "net_perf_pct"], ascending=[False, False, False])
    all_df.to_csv(OUT_DIR / "soxl_smh_variant_search_all.csv", index=False)
    (OUT_DIR / "soxl_smh_variant_search_all.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    best_by_family_symbol = (
        all_df.sort_values(["symbol", "family", "beat_asset", "excess_vs_asset_pct", "net_perf_pct"], ascending=[True, True, False, False, False])
        .groupby(["symbol", "family"], as_index=False)
        .head(1)
        .sort_values(["beat_asset", "excess_vs_asset_pct", "net_perf_pct"], ascending=[False, False, False])
    )
    best_by_family_symbol.to_csv(OUT_DIR / "soxl_smh_variant_search_best_by_family_symbol.csv", index=False)
    beating = all_df[all_df["beat_asset"]]
    beating.to_csv(OUT_DIR / "soxl_smh_variant_search_beating_asset.csv", index=False)
    print("Total variants:", len(all_df))
    print()
    print("Best by symbol/family:")
    print(best_by_family_symbol.to_string(index=False))
    print()
    print("Top 25 beating asset:")
    print(beating.head(25).to_string(index=False))


def main() -> None:
    results = run()
    write_outputs(results)


if __name__ == "__main__":
    main()
