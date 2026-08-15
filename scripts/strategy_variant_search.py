import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


OUT_DIR = Path("backtest_results")
DAILY_START = "2018-01-02"
DAILY_END = "2026-05-20"


@dataclass
class SearchResult:
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
    max_drawdown_pct: float
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
    drawdown = equity / equity.cummax() - 1
    return float(drawdown.min() * 100)


def asset_return(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    return (float(df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1) * 100


def win_rate(trades: list[float]) -> float | None:
    if not trades:
        return None
    return len([trade for trade in trades if trade > 0]) / len(trades) * 100


def actual_range(df: pd.DataFrame) -> str:
    if df.empty:
        return "data not available"
    return f"{df.index.min()} to {df.index.max()}"


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
    asset_perf: float | None = None,
) -> SearchResult:
    net_perf = (float(equity.iloc[-1]) - 1) * 100 if not equity.empty else 0.0
    bench_symbol = asset_symbol or symbol
    bench_perf = asset_return(df) if asset_perf is None else asset_perf
    excess = net_perf - bench_perf
    return SearchResult(
        family=family,
        variant=variant,
        symbol=symbol,
        timeframe=timeframe,
        requested_range=requested_range,
        actual_range=actual_range(df),
        net_perf_pct=round(net_perf, 2),
        asset_symbol=bench_symbol,
        asset_perf_pct=round(bench_perf, 2),
        excess_vs_asset_pct=round(excess, 2),
        beat_asset=bool(excess > 0),
        max_drawdown_pct=round(max_drawdown(equity), 2),
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


def search_ma_variants(symbol: str, df: pd.DataFrame) -> list[SearchResult]:
    results: list[SearchResult] = []
    fast_windows = [3, 5, 8, 10, 13, 20, 21, 30, 40, 50, 63, 100]
    slow_windows = [20, 30, 40, 50, 63, 100, 126, 150, 200, 252]
    stop_losses = [None, 0.20]
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
                    equity, trades = daily_long_only_backtest(
                        df,
                        entry.fillna(False),
                        exit_.fillna(False),
                        stop_loss_pct=stop_loss,
                    )
                    stop_label = "no stop" if stop_loss is None else f"{int(stop_loss * 100)}% stop"
                    results.append(
                        summarize(
                            family="Moving-average crossover / trend following",
                            variant=f"SMA{fast}/SMA{slow} {mode}, {stop_label}",
                            symbol=symbol,
                            timeframe="1d",
                            requested_range=f"{DAILY_START} to 2026-05-19",
                            df=df,
                            equity=equity,
                            trades=trades,
                            notes="Daily ETF parameter search; optimized in-sample; no costs/slippage.",
                        )
                    )
    return results


def search_abs_momentum_variants(symbol: str, df: pd.DataFrame) -> list[SearchResult]:
    results: list[SearchResult] = []
    lookbacks = [21, 42, 63, 84, 126, 168, 189, 252]
    trend_windows = [0, 20, 50, 100, 150, 200]
    stop_losses = [None, 0.20]
    for lookback in lookbacks:
        positive_momentum = df["Close"] > df["Close"].shift(lookback)
        for trend_window in trend_windows:
            if trend_window == 0:
                condition = positive_momentum
                trend_label = "no trend SMA"
            else:
                condition = positive_momentum & (df["Close"] > df["Close"].rolling(trend_window).mean())
                trend_label = f"above SMA{trend_window}"
            entry = condition & (~condition.shift(1).fillna(False))
            exit_ = ~condition
            for stop_loss in stop_losses:
                equity, trades = daily_long_only_backtest(
                    df,
                    entry.fillna(False),
                    exit_.fillna(False),
                    stop_loss_pct=stop_loss,
                )
                stop_label = "no stop" if stop_loss is None else f"{int(stop_loss * 100)}% stop"
                results.append(
                    summarize(
                        family="Relative strength / absolute momentum",
                        variant=f"{lookback}-day positive return, {trend_label}, {stop_label}",
                        symbol=symbol,
                        timeframe="1d",
                        requested_range=f"{DAILY_START} to 2026-05-19",
                        df=df,
                        equity=equity,
                        trades=trades,
                        notes="Daily ETF absolute momentum parameter search; optimized in-sample; no costs/slippage.",
                    )
                )
    return results


def search_rsi2_variants(symbol: str, df: pd.DataFrame) -> list[SearchResult]:
    results: list[SearchResult] = []
    rsi_lengths = [2, 3, 4]
    thresholds = [3, 5, 10, 15]
    trend_windows = [50, 100, 150, 200]
    exit_windows = [3, 5, 10, 20]
    stop_losses = [None, 0.10]
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
                        equity, trades = daily_long_only_backtest(
                            df,
                            entry.fillna(False),
                            exit_.fillna(False),
                            stop_loss_pct=stop_loss,
                        )
                        stop_label = "no stop" if stop_loss is None else f"{int(stop_loss * 100)}% stop"
                        results.append(
                            summarize(
                                family="RSI(2) / mean reversion",
                                variant=(
                                    f"RSI{rsi_len}<={threshold}, above SMA{trend_window}, "
                                    f"exit above SMA{exit_window}, {stop_label}"
                                ),
                                symbol=symbol,
                                timeframe="1d",
                                requested_range=f"{DAILY_START} to 2026-05-19",
                                df=df,
                                equity=equity,
                                trades=trades,
                                notes="Daily ETF RSI pullback parameter search; optimized in-sample; no costs/slippage.",
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
            long_entry = False
            short_entry = False
            if entry_mode == "state":
                long_entry = close > cur_vwap
                short_entry = close < cur_vwap
            elif entry_mode == "reclaim":
                long_entry = prev_close <= prev_vwap and close > cur_vwap
                short_entry = prev_close >= prev_vwap and close < cur_vwap
            elif entry_mode == "pullback":
                long_entry = close > cur_vwap and lows[bar_index] <= cur_vwap
                short_entry = close < cur_vwap and highs[bar_index] >= cur_vwap
            if pos == 0 and long_entry:
                pos = 1
                entry = close
            elif pos == 0 and allow_short and short_entry:
                pos = -1
                entry = close
            elif pos != 0:
                ret = pos * (close / entry - 1)
                stop_hit = stop_pct is not None and ret <= -stop_pct
                target_hit = target_pct is not None and ret >= target_pct
                vwap_exit = (pos == 1 and close < cur_vwap) or (pos == -1 and close > cur_vwap)
                if stop_hit or target_hit or vwap_exit or is_last:
                    trades.append(ret)
                    capital *= 1 + ret
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


def search_intraday_variants(symbol: str, timeframe: str, period: str, df: pd.DataFrame) -> list[SearchResult]:
    results: list[SearchResult] = []
    rh_df = regular_hours(df)
    requested = f"period={period}; interval={timeframe}"
    min_bars_by_timeframe = [1, 3, 6] if timeframe == "5m" else [1, 2]
    for allow_short in [False, True]:
        direction = "long+short" if allow_short else "long-only"
        for entry_mode in ["state", "reclaim", "pullback"]:
            for min_bars in min_bars_by_timeframe:
                for target_pct in [None, 0.01, 0.02]:
                    for stop_pct in [None, 0.01]:
                        equity, trades = intraday_vwap_variant(
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
                                family="VWAP trend / reclaim",
                                variant=f"{direction} {entry_mode}, after {min_bars} bars, {target_label}, {stop_label}",
                                symbol=symbol,
                                timeframe=timeframe,
                                requested_range=requested,
                                df=rh_df,
                                equity=equity,
                                trades=trades,
                                notes="Intraday VWAP parameter search; source proxy only; no costs/slippage.",
                            )
                        )
    opening_bars_by_timeframe = [1, 3, 6, 12] if timeframe == "5m" else [1, 2]
    for allow_short in [False, True]:
        direction = "long+short" if allow_short else "long-only"
        for opening_bars in opening_bars_by_timeframe:
            for volume_mult in [0, 1.0, 1.5, 2.0]:
                for target_rr in [None, 1.0, 2.0, 3.0]:
                    equity, trades = intraday_orb_variant(
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
                            family="Opening range breakout",
                            variant=f"{direction}, {opening_bars}-bar ORB, {vol_label}, {target_label}",
                            symbol=symbol,
                            timeframe=timeframe,
                            requested_range=requested,
                            df=rh_df,
                            equity=equity,
                            trades=trades,
                            notes="Intraday ORB parameter search; ETF proxy for stocks-in-play; no costs/slippage.",
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


def search_rotation_variants(close: pd.DataFrame) -> list[SearchResult]:
    results: list[SearchResult] = []
    close = close.dropna(how="all").ffill().dropna()
    risky_sets = [
        ("classic GEM", ["SPY", "VEU"], "SPY"),
        ("QQQ/SPY rotation", ["SPY", "QQQ"], "SPY"),
        ("QQQ/TQQQ rotation", ["QQQ", "TQQQ"], "QQQ"),
        ("SPY/QQQ/TQQQ rotation", ["SPY", "QQQ", "TQQQ"], "SPY"),
    ]
    for label, risky, benchmark in risky_sets:
        for defensive in ["BIL", "AGG"]:
            needed = set(risky + [defensive, benchmark])
            if not needed.issubset(close.columns):
                continue
            for lookback in [1, 3, 6, 9, 12]:
                equity, trades, _ = monthly_rotation_backtest(close, risky, defensive, lookback)
                benchmark_perf = (float(close[benchmark].iloc[-1] / close[benchmark].iloc[0]) - 1) * 100
                results.append(
                    summarize(
                        family="Momentum / relative strength rotation",
                        variant=f"{label}, {lookback}-month lookback, defensive {defensive}",
                        symbol="/".join(risky + [defensive]),
                        timeframe="Daily signal, monthly rebalance",
                        requested_range=f"{DAILY_START} to 2026-05-19",
                        df=pd.DataFrame({"Close": close[benchmark]}),
                        equity=equity,
                        trades=trades,
                        asset_symbol=benchmark,
                        asset_perf=benchmark_perf,
                        notes="GEM-style monthly ETF rotation parameter search; benchmark is listed in asset_symbol.",
                    )
                )
    return results


def run_search() -> list[SearchResult]:
    results: list[SearchResult] = []
    intraday_cases = [("5m", "60d"), ("60m", "730d")]
    for symbol in ["QQQ", "TQQQ"]:
        for timeframe, period in intraday_cases:
            df = fetch_single(symbol, period=period, interval=timeframe)
            results.extend(search_intraday_variants(symbol, timeframe, period, df))
    daily_data = {
        symbol: fetch_single(symbol, start=DAILY_START, end=DAILY_END, interval="1d")
        for symbol in ["SPY", "QQQ", "TQQQ"]
    }
    for symbol, df in daily_data.items():
        if df.empty:
            continue
        results.extend(search_ma_variants(symbol, df))
        results.extend(search_abs_momentum_variants(symbol, df))
        results.extend(search_rsi2_variants(symbol, df))
    multi = fetch_multi(["SPY", "QQQ", "TQQQ", "VEU", "AGG", "BIL"], start=DAILY_START, end=DAILY_END, interval="1d")
    if not multi.empty and "Close" in multi:
        results.extend(search_rotation_variants(multi["Close"]))
    return results


def write_outputs(results: list[SearchResult]) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    rows = [asdict(result) for result in results]
    all_df = pd.DataFrame(rows)
    all_df = all_df.sort_values(["beat_asset", "excess_vs_asset_pct", "net_perf_pct"], ascending=[False, False, False])
    all_df.to_csv(OUT_DIR / "strategy_variant_search_all.csv", index=False)
    (OUT_DIR / "strategy_variant_search_all.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    best_by_family = (
        all_df.sort_values(["family", "beat_asset", "excess_vs_asset_pct", "net_perf_pct"], ascending=[True, False, False, False])
        .groupby("family", as_index=False)
        .head(1)
        .sort_values(["beat_asset", "excess_vs_asset_pct", "net_perf_pct"], ascending=[False, False, False])
    )
    best_by_family.to_csv(OUT_DIR / "strategy_variant_search_best_by_family.csv", index=False)
    all_df[all_df["beat_asset"]].to_csv(OUT_DIR / "strategy_variant_search_beating_asset.csv", index=False)
    print("Best by family:")
    print(best_by_family.to_string(index=False))
    print()
    print("Top 20 beating asset:")
    print(all_df[all_df["beat_asset"]].head(20).to_string(index=False))


def main() -> None:
    results = run_search()
    write_outputs(results)


if __name__ == "__main__":
    main()
