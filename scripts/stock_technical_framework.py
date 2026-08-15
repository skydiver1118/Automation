from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
import yfinance as yf


DEFAULT_TICKER = "NVDA"
DEFAULT_OUT_DIR = Path("reports") / "technical_framework"


@dataclass(frozen=True)
class EntryPlan:
    name: str
    zone_low: float
    zone_high: float
    trigger: str
    stop: float
    target_1: float
    target_2: float
    notes: str


def _flatten_yfinance_columns(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    if not isinstance(df.columns, pd.MultiIndex):
        return df

    ticker = ticker.upper()
    price_fields = {"OPEN", "HIGH", "LOW", "CLOSE", "ADJ CLOSE", "VOLUME"}
    for level in range(df.columns.nlevels):
        values = [str(item).upper() for item in df.columns.get_level_values(level)]
        unique_values = set(values)
        if ticker in unique_values and not unique_values.issubset(price_fields):
            return df.xs(ticker, axis=1, level=level, drop_level=True)

    df = df.copy()
    df.columns = [str(col[0]) for col in df.columns]
    return df


def fetch_daily_data(ticker: str, period: str) -> pd.DataFrame:
    df = yf.download(
        ticker,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=False,
    )
    df = _flatten_yfinance_columns(df, ticker)
    if df.empty:
        raise RuntimeError(f"No yfinance daily data returned for {ticker}.")

    expected = {"Open", "High", "Low", "Close", "Volume"}
    missing = expected.difference(df.columns)
    if missing:
        raise RuntimeError(f"Missing yfinance columns for {ticker}: {sorted(missing)}")

    df = df.loc[:, ["Open", "High", "Low", "Close", "Volume"]].dropna()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


def rsi(close: pd.Series, window: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def true_range(df: pd.DataFrame) -> pd.Series:
    prev_close = df["Close"].shift(1)
    ranges = pd.concat(
        [
            df["High"] - df["Low"],
            (df["High"] - prev_close).abs(),
            (df["Low"] - prev_close).abs(),
        ],
        axis=1,
    )
    return ranges.max(axis=1)


def adx(df: pd.DataFrame, window: int = 14) -> tuple[pd.Series, pd.Series, pd.Series]:
    high = df["High"]
    low = df["Low"]
    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = pd.Series(
        np.where((up_move > down_move) & (up_move > 0), up_move, 0.0), index=df.index
    )
    minus_dm = pd.Series(
        np.where((down_move > up_move) & (down_move > 0), down_move, 0.0),
        index=df.index,
    )

    atr_value = true_range(df).ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    plus_di = 100 * plus_dm.ewm(alpha=1 / window, adjust=False, min_periods=window).mean() / atr_value
    minus_di = 100 * minus_dm.ewm(alpha=1 / window, adjust=False, min_periods=window).mean() / atr_value
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    adx_value = dx.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    return adx_value, plus_di, minus_di


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["SMA20"] = out["Close"].rolling(20).mean()
    out["SMA50"] = out["Close"].rolling(50).mean()
    out["SMA200"] = out["Close"].rolling(200).mean()
    out["EMA8"] = out["Close"].ewm(span=8, adjust=False).mean()
    out["EMA21"] = out["Close"].ewm(span=21, adjust=False).mean()

    out["RSI14"] = rsi(out["Close"], 14)
    ema12 = out["Close"].ewm(span=12, adjust=False).mean()
    ema26 = out["Close"].ewm(span=26, adjust=False).mean()
    out["MACD"] = ema12 - ema26
    out["MACDSignal"] = out["MACD"].ewm(span=9, adjust=False).mean()
    out["MACDHist"] = out["MACD"] - out["MACDSignal"]

    out["BBMid"] = out["Close"].rolling(20).mean()
    bb_std = out["Close"].rolling(20).std()
    out["BBUpper"] = out["BBMid"] + 2 * bb_std
    out["BBLower"] = out["BBMid"] - 2 * bb_std

    out["ATR14"] = true_range(out).ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    out["ADX14"], out["PlusDI14"], out["MinusDI14"] = adx(out, 14)

    direction = np.sign(out["Close"].diff()).fillna(0.0)
    out["OBV"] = (direction * out["Volume"]).cumsum()
    out["OBV20"] = out["OBV"].rolling(20).mean()
    out["Volume20"] = out["Volume"].rolling(20).mean()
    out["ROC20"] = out["Close"].pct_change(20) * 100
    out["High63"] = out["High"].rolling(63).max()
    out["Low63"] = out["Low"].rolling(63).min()

    typical_price = (out["High"] + out["Low"] + out["Close"]) / 3
    pv = typical_price * out["Volume"]
    out["VWAP63"] = pv.rolling(63).sum() / out["Volume"].rolling(63).sum()
    return out


def _cluster_levels(levels: list[float], tolerance: float) -> list[float]:
    clean = sorted(level for level in levels if math.isfinite(level) and level > 0)
    if not clean:
        return []

    clusters: list[list[float]] = [[clean[0]]]
    for level in clean[1:]:
        group_mean = float(np.mean(clusters[-1]))
        if abs(level - group_mean) <= tolerance:
            clusters[-1].append(level)
        else:
            clusters.append([level])
    return [float(np.mean(group)) for group in clusters]


def support_resistance(df: pd.DataFrame, lookback: int = 126) -> tuple[list[float], list[float]]:
    recent = df.tail(lookback).copy()
    if recent.empty:
        return [], []

    current = float(recent["Close"].iloc[-1])
    atr_value = float(recent["ATR14"].iloc[-1])
    tolerance = max(current * 0.0125, atr_value * 0.6)

    lows = recent["Low"]
    highs = recent["High"]
    pivot_lows = lows[
        lows.eq(lows.rolling(7, center=True, min_periods=4).min())
    ].dropna()
    pivot_highs = highs[
        highs.eq(highs.rolling(7, center=True, min_periods=4).max())
    ].dropna()

    support_candidates = list(pivot_lows.values)
    resistance_candidates = list(pivot_highs.values)
    latest = recent.iloc[-1]
    support_candidates.extend(
        [
            float(latest["SMA20"]),
            float(latest["SMA50"]),
            float(latest["EMA21"]),
            float(latest["BBLower"]),
            float(latest["Low63"]),
        ]
    )
    resistance_candidates.extend(
        [
            float(latest["BBUpper"]),
            float(latest["High63"]),
            float(recent["High"].tail(20).max()),
        ]
    )

    supports = [level for level in _cluster_levels(support_candidates, tolerance) if level < current * 1.01]
    resistances = [
        level for level in _cluster_levels(resistance_candidates, tolerance) if level > current * 0.99
    ]
    return supports, resistances


def score_setup(df: pd.DataFrame) -> tuple[int, str, pd.DataFrame]:
    latest = df.dropna().iloc[-1]
    score_rows: list[dict[str, object]] = []

    def add(category: str, rule: str, points: int, max_points: int, evidence: str) -> None:
        score_rows.append(
            {
                "Category": category,
                "Rule": rule,
                "Points": points,
                "Max": max_points,
                "Evidence": evidence,
            }
        )

    close = float(latest["Close"])
    sma20 = float(latest["SMA20"])
    sma50 = float(latest["SMA50"])
    sma200 = float(latest["SMA200"])
    sma50_slope = float(df["SMA50"].diff(20).iloc[-1])

    add("Trend", "Close above SMA20", 6 if close > sma20 else 0, 6, f"{close:.2f} vs {sma20:.2f}")
    add("Trend", "Close above SMA50", 8 if close > sma50 else 0, 8, f"{close:.2f} vs {sma50:.2f}")
    add("Trend", "Close above SMA200", 8 if close > sma200 else 0, 8, f"{close:.2f} vs {sma200:.2f}")
    add("Trend", "SMA20 above SMA50", 6 if sma20 > sma50 else 0, 6, f"{sma20:.2f} vs {sma50:.2f}")
    add("Trend", "SMA50 above SMA200", 6 if sma50 > sma200 else 0, 6, f"{sma50:.2f} vs {sma200:.2f}")
    add("Trend", "SMA50 rising over 20 sessions", 6 if sma50_slope > 0 else 0, 6, f"{sma50_slope:.2f}")

    rsi14 = float(latest["RSI14"])
    if 45 <= rsi14 <= 70:
        rsi_points = 8
    elif 70 < rsi14 <= 78:
        rsi_points = 5
    elif 35 <= rsi14 < 45:
        rsi_points = 3
    else:
        rsi_points = 0
    add("Momentum", "RSI in constructive range", rsi_points, 8, f"RSI14 {rsi14:.1f}")

    macd = float(latest["MACD"])
    macd_signal = float(latest["MACDSignal"])
    macd_hist = float(latest["MACDHist"])
    macd_hist_slope = float(df["MACDHist"].diff(5).iloc[-1])
    roc20 = float(latest["ROC20"])
    add("Momentum", "MACD above signal", 7 if macd > macd_signal else 0, 7, f"{macd:.2f} vs {macd_signal:.2f}")
    add("Momentum", "MACD histogram improving", 5 if macd_hist_slope > 0 else 0, 5, f"5d change {macd_hist_slope:.2f}")
    add("Momentum", "20-day rate of change positive", 5 if roc20 > 0 else 0, 5, f"{roc20:.2f}%")

    volume = float(latest["Volume"])
    volume20 = float(latest["Volume20"])
    obv = float(latest["OBV"])
    obv20 = float(latest["OBV20"])
    recent = df.tail(20)
    up_volume = float(recent.loc[recent["Close"].diff() > 0, "Volume"].sum())
    down_volume = float(recent.loc[recent["Close"].diff() < 0, "Volume"].sum())
    up_down_ratio = up_volume / down_volume if down_volume else np.inf
    add("Confirmation", "Current volume above 20-day average", 5 if volume > volume20 else 0, 5, f"{volume / volume20:.2f}x")
    add("Confirmation", "OBV above 20-day average", 5 if obv > obv20 else 0, 5, f"{obv:.0f} vs {obv20:.0f}")
    add("Confirmation", "20-day up-volume beats down-volume", 5 if up_down_ratio > 1 else 0, 5, f"{up_down_ratio:.2f}x")

    adx14 = float(latest["ADX14"])
    plus_di = float(latest["PlusDI14"])
    minus_di = float(latest["MinusDI14"])
    atr_pct = float(latest["ATR14"] / close * 100)
    bb_upper = float(latest["BBUpper"])
    high63 = float(latest["High63"])
    add(
        "Risk/context",
        "ADX confirms bullish directional pressure",
        7 if adx14 > 20 and plus_di > minus_di else 0,
        7,
        f"ADX {adx14:.1f}, +DI {plus_di:.1f}, -DI {minus_di:.1f}",
    )
    not_overextended = close <= bb_upper * 1.02 and rsi14 <= 78
    add("Risk/context", "Not dangerously overextended", 4 if not_overextended else 0, 4, f"BB upper {bb_upper:.2f}")
    if atr_pct <= 6:
        atr_points = 4
    elif atr_pct <= 10:
        atr_points = 2
    else:
        atr_points = 0
    add("Risk/context", "ATR volatility is tradable", atr_points, 4, f"ATR14 {atr_pct:.2f}%")
    distance_from_high = (high63 - close) / high63 * 100
    add("Risk/context", "Close is within 8% of 63-day high", 5 if distance_from_high <= 8 else 0, 5, f"{distance_from_high:.2f}%")

    score_df = pd.DataFrame(score_rows)
    total = int(score_df["Points"].sum())
    if total >= 70 and close > sma50 and macd > macd_signal:
        label = "Bullish"
    elif total < 45 or (close < sma50 and macd < macd_signal):
        label = "Bearish"
    else:
        label = "Neutral"
    return total, label, score_df


def build_entry_plans(
    df: pd.DataFrame, supports: list[float], resistances: list[float], label: str
) -> list[EntryPlan]:
    latest = df.dropna().iloc[-1]
    close = float(latest["Close"])
    atr_value = float(latest["ATR14"])
    sma50 = float(latest["SMA50"])
    ema21 = float(latest["EMA21"])
    sma20 = float(latest["SMA20"])
    high63 = float(latest["High63"])

    below = [level for level in supports + [ema21, sma20, sma50] if math.isfinite(level) and level < close]
    above = [level for level in resistances + [high63] if math.isfinite(level) and level > close]
    nearest_support = max(below) if below else close - 1.5 * atr_value
    nearest_resistance = min(above) if above else close + 1.5 * atr_value

    pullback_ref = max([level for level in [nearest_support, ema21, sma20] if level < close], default=nearest_support)
    pullback_low = max(0.01, pullback_ref - 0.5 * atr_value)
    pullback_high = pullback_ref + 0.25 * atr_value
    pullback_stop = min(nearest_support, sma50) - 1.0 * atr_value
    pullback_entry = (pullback_low + pullback_high) / 2
    pullback_risk = max(pullback_entry - pullback_stop, atr_value)

    breakout_ref = nearest_resistance
    breakout_low = breakout_ref
    breakout_high = breakout_ref + 0.5 * atr_value
    breakout_stop = max(nearest_support, close - 2.0 * atr_value)
    breakout_entry = (breakout_low + breakout_high) / 2
    breakout_risk = max(breakout_entry - breakout_stop, atr_value)

    plans = [
        EntryPlan(
            name="Pullback entry",
            zone_low=pullback_low,
            zone_high=pullback_high,
            trigger="Buy only after price holds the zone and closes back above the prior day's high or EMA8.",
            stop=pullback_stop,
            target_1=max(nearest_resistance, pullback_entry + 2 * pullback_risk),
            target_2=pullback_entry + 3 * pullback_risk,
            notes="Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume.",
        ),
        EntryPlan(
            name="Breakout entry",
            zone_low=breakout_low,
            zone_high=breakout_high,
            trigger="Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive.",
            stop=breakout_stop,
            target_1=breakout_entry + 2 * breakout_risk,
            target_2=breakout_entry + 3 * breakout_risk,
            notes="Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.",
        ),
    ]

    if label == "Bearish":
        reclaim = max(float(latest["SMA20"]), float(latest["SMA50"]))
        plans.insert(
            0,
            EntryPlan(
                name="Reclaim entry",
                zone_low=reclaim,
                zone_high=reclaim + 0.5 * atr_value,
                trigger="Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.",
                stop=reclaim - 1.5 * atr_value,
                target_1=reclaim + 3 * atr_value,
                target_2=reclaim + 5 * atr_value,
                notes="The framework does not treat bearish charts as immediate buys; this is a repair trigger.",
            ),
        )
    return plans


def money(value: float) -> str:
    return f"${value:,.2f}"


def pct(value: float) -> str:
    return f"{value:,.2f}%"


def draw_candles(ax: plt.Axes, x: np.ndarray, plot_df: pd.DataFrame) -> None:
    price_span = max(float(plot_df["High"].max() - plot_df["Low"].min()), 0.01)
    min_body = max(price_span * 0.002, 0.01)
    width = 0.62

    for pos, (_, row) in zip(x, plot_df.iterrows()):
        open_price = float(row["Open"])
        high = float(row["High"])
        low = float(row["Low"])
        close = float(row["Close"])
        color = "#16a34a" if close >= open_price else "#dc2626"

        ax.vlines(pos, low, high, color=color, linewidth=1.0, alpha=0.95)
        body_bottom = min(open_price, close)
        body_height = abs(close - open_price)
        if body_height < min_body:
            body_bottom = ((open_price + close) / 2) - (min_body / 2)
            body_height = min_body
        ax.add_patch(
            Rectangle(
                (pos - width / 2, body_bottom),
                width,
                body_height,
                facecolor=color,
                edgecolor=color,
                linewidth=0.8,
                alpha=0.86,
            )
        )


def set_trading_day_ticks(ax: plt.Axes, dates: pd.DatetimeIndex, max_ticks: int = 8) -> None:
    if len(dates) == 0:
        return
    step = max(1, math.ceil(len(dates) / max_ticks))
    ticks = list(range(0, len(dates), step))
    if ticks[-1] != len(dates) - 1:
        ticks.append(len(dates) - 1)
    ax.set_xticks(ticks)
    ax.set_xticklabels(
        [dates[idx].strftime("%Y-%m-%d") for idx in ticks],
        rotation=30,
        ha="right",
    )


def chart_date_label(value: pd.Timestamp) -> str:
    stamp = pd.Timestamp(value)
    return f"{stamp.strftime('%b')} {stamp.day}, {stamp.year}"


def show_y_scale_on_both_sides(ax: plt.Axes) -> None:
    ax.tick_params(axis="y", which="both", left=True, right=True, labelleft=True, labelright=True)
    ax.yaxis.set_ticks_position("both")
    ax.spines["right"].set_visible(True)


def annotate_latest_value(
    ax: plt.Axes,
    x_pos: float,
    y_value: float,
    text: str,
    color: str,
    label_xy: tuple[float, float] = (0.54, 0.82),
) -> None:
    if not np.isfinite(y_value):
        return
    ax.scatter([x_pos], [y_value], color=color, s=20, zorder=5)
    ax.annotate(
        text,
        xy=(x_pos, y_value),
        xycoords="data",
        xytext=label_xy,
        textcoords="axes fraction",
        ha="center",
        va="center",
        fontsize=10,
        color="#0f172a",
        bbox={"boxstyle": "round,pad=0.36", "facecolor": "white", "alpha": 0.86, "edgecolor": color},
        arrowprops={"arrowstyle": "-", "color": color, "linewidth": 0.8, "alpha": 0.45, "shrinkA": 4, "shrinkB": 4},
        zorder=6,
    )


def write_chart(
    df: pd.DataFrame,
    ticker: str,
    score: int,
    label: str,
    supports: list[float],
    resistances: list[float],
    entries: list[EntryPlan],
    out_path: Path,
    months: int,
) -> None:
    last_date = df.index[-1]
    start_date = last_date - pd.DateOffset(months=months)
    plot_df = df.loc[df.index >= start_date].dropna().copy()
    if plot_df.empty:
        raise RuntimeError("No data available for chart window.")

    fig, axes = plt.subplots(
        4,
        1,
        figsize=(14, 11),
        sharex=True,
        gridspec_kw={"height_ratios": [3.2, 0.9, 1.0, 1.1]},
    )
    ax_price, ax_volume, ax_rsi, ax_macd = axes

    dates = pd.DatetimeIndex(plot_df.index)
    x = np.arange(len(plot_df))
    draw_candles(ax_price, x, plot_df)
    ax_price.plot([], [], color="#16a34a", linewidth=4, label="Candles")
    ax_price.plot(x, plot_df["EMA8"], color="#0ea5e9", linewidth=1.0, label="EMA8")
    ax_price.plot(x, plot_df["EMA21"], color="#2563eb", linewidth=1.0, label="EMA21")
    ax_price.plot(x, plot_df["SMA50"], color="#f97316", linewidth=1.2, label="SMA50")
    if plot_df["SMA200"].notna().any():
        ax_price.plot(x, plot_df["SMA200"], color="#7c3aed", linewidth=1.1, label="SMA200")
    ax_price.fill_between(
        x,
        plot_df["BBLower"].to_numpy(dtype=float),
        plot_df["BBUpper"].to_numpy(dtype=float),
        color="#94a3b8",
        alpha=0.16,
        label="Bollinger 20,2",
    )

    for idx, level in enumerate(supports[-3:]):
        ax_price.axhline(level, color="#16a34a", linestyle="--", linewidth=0.9, alpha=0.75, label="Support" if idx == 0 else None)
    for idx, level in enumerate(resistances[:3]):
        ax_price.axhline(level, color="#dc2626", linestyle="--", linewidth=0.9, alpha=0.75, label="Resistance" if idx == 0 else None)

    palette = ["#22c55e", "#f59e0b", "#06b6d4"]
    for idx, entry in enumerate(entries[:3]):
        ax_price.axhspan(entry.zone_low, entry.zone_high, color=palette[idx % len(palette)], alpha=0.12)
        ax_price.text(
            x[0],
            (entry.zone_low + entry.zone_high) / 2,
            entry.name,
            va="center",
            ha="left",
            fontsize=8,
            color="#111827",
            bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "alpha": 0.7, "edgecolor": "none"},
        )

    last = plot_df.iloc[-1]
    last_x = float(x[-1])
    latest_date_text = chart_date_label(dates[-1])
    ax_price.set_title(
        f"{ticker.upper()} technical framework - {label} ({score}/100) through {last_date.date()} | Close {money(float(last['Close']))}",
        loc="left",
        fontsize=13,
        fontweight="bold",
    )
    annotate_latest_value(
        ax_price,
        last_x,
        float(last["Close"]),
        f"Close {money(float(last['Close']))}\n{latest_date_text}",
        "#0f172a",
    )
    ax_price.set_ylabel("Price")
    ax_price.set_xlim(-0.8, len(x) - 0.2)
    ax_price.legend(loc="upper left", ncol=4, fontsize=8)
    ax_price.grid(True, alpha=0.25)

    colors = np.where(plot_df["Close"].diff().fillna(0) >= 0, "#16a34a", "#dc2626")
    ax_volume.bar(x, plot_df["Volume"], color=colors, alpha=0.55, width=0.8)
    ax_volume.plot(x, plot_df["Volume20"], color="#334155", linewidth=1.0, label="Volume20")
    ax_volume.set_ylabel("Volume")
    ax_volume.legend(loc="upper left", fontsize=8)
    ax_volume.grid(True, alpha=0.2)

    ax_rsi.plot(x, plot_df["RSI14"], color="#7c2d12", linewidth=1.2, label="RSI14")
    ax_rsi.axhline(70, color="#dc2626", linestyle="--", linewidth=0.8)
    ax_rsi.axhline(50, color="#64748b", linestyle=":", linewidth=0.8)
    ax_rsi.axhline(30, color="#16a34a", linestyle="--", linewidth=0.8)
    ax_rsi.set_ylim(0, 100)
    ax_rsi.set_ylabel("RSI")
    annotate_latest_value(
        ax_rsi,
        last_x,
        float(last["RSI14"]),
        f"RSI {float(last['RSI14']):.1f}\n{latest_date_text}",
        "#7c2d12",
    )
    ax_rsi.legend(loc="upper left", fontsize=8)
    ax_rsi.grid(True, alpha=0.2)

    hist_colors = np.where(plot_df["MACDHist"] >= 0, "#16a34a", "#dc2626")
    ax_macd.bar(x, plot_df["MACDHist"], color=hist_colors, alpha=0.45, width=0.8, label="Hist")
    ax_macd.plot(x, plot_df["MACD"], color="#0f172a", linewidth=1.1, label="MACD")
    ax_macd.plot(x, plot_df["MACDSignal"], color="#f97316", linewidth=1.0, label="Signal")
    ax_macd.axhline(0, color="#64748b", linewidth=0.8)
    ax_macd.set_ylabel("MACD")
    annotate_latest_value(
        ax_macd,
        last_x,
        float(last["MACD"]),
        f"MACD {float(last['MACD']):.2f}\nSignal {float(last['MACDSignal']):.2f}",
        "#0f172a",
    )
    ax_macd.legend(loc="upper left", fontsize=8)
    ax_macd.grid(True, alpha=0.2)

    for ax in axes:
        show_y_scale_on_both_sides(ax)

    set_trading_day_ticks(ax_macd, dates)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160)
    plt.close(fig)


def markdown_table(df: pd.DataFrame) -> str:
    text_df = df.fillna("").astype(str)
    headers = list(text_df.columns)
    rows = text_df.values.tolist()
    widths = [
        max(len(header), *(len(row[idx]) for row in rows)) if rows else len(header)
        for idx, header in enumerate(headers)
    ]

    def fmt_row(values: list[str]) -> str:
        cells = [value.ljust(widths[idx]) for idx, value in enumerate(values)]
        return "| " + " | ".join(cells) + " |"

    separator = "| " + " | ".join("-" * width for width in widths) + " |"
    return "\n".join([fmt_row(headers), separator, *(fmt_row(row) for row in rows)])


def write_report(
    df: pd.DataFrame,
    ticker: str,
    score: int,
    label: str,
    score_df: pd.DataFrame,
    supports: list[float],
    resistances: list[float],
    entries: list[EntryPlan],
    chart_path: Path,
    out_path: Path,
) -> None:
    latest = df.dropna().iloc[-1]
    last_date = df.index[-1].date()
    gate_notes: list[str] = []
    if float(latest["Close"]) <= float(latest["SMA50"]):
        gate_notes.append("close is not above SMA50")
    if float(latest["MACD"]) <= float(latest["MACDSignal"]):
        gate_notes.append("MACD is not above signal")
    if float(latest["Close"]) <= float(latest["SMA20"]):
        gate_notes.append("close is below SMA20, showing near-term pullback pressure")

    if label == "Bullish":
        decision_note = "Bullish under the framework, but still buy only at a defined pullback or breakout trigger."
    elif label == "Neutral":
        reason = "; ".join(gate_notes) if gate_notes else "confirmation is mixed"
        decision_note = f"Not bullish yet under the framework; classify as Neutral because {reason}."
    else:
        reason = "; ".join(gate_notes) if gate_notes else "trend and momentum confirmation are weak"
        decision_note = f"Not bullish under the framework; classify as Bearish because {reason}."

    key = pd.DataFrame(
        [
            ("Close", money(float(latest["Close"]))),
            ("SMA20", money(float(latest["SMA20"]))),
            ("SMA50", money(float(latest["SMA50"]))),
            ("SMA200", money(float(latest["SMA200"]))),
            ("RSI14", f"{float(latest['RSI14']):.1f}"),
            ("MACD / Signal", f"{float(latest['MACD']):.2f} / {float(latest['MACDSignal']):.2f}"),
            ("ADX14 / +DI / -DI", f"{float(latest['ADX14']):.1f} / {float(latest['PlusDI14']):.1f} / {float(latest['MinusDI14']):.1f}"),
            ("ATR14", f"{money(float(latest['ATR14']))} ({pct(float(latest['ATR14'] / latest['Close'] * 100))})"),
            ("63-day range", f"{money(float(latest['Low63']))} - {money(float(latest['High63']))}"),
        ],
        columns=["Metric", "Value"],
    )
    entry_df = pd.DataFrame(
        [
            {
                "Plan": entry.name,
                "Entry zone": f"{money(entry.zone_low)} - {money(entry.zone_high)}",
                "Trigger": entry.trigger,
                "Stop": money(entry.stop),
                "Target 1": money(entry.target_1),
                "Target 2": money(entry.target_2),
                "Notes": entry.notes,
            }
            for entry in entries
        ]
    )

    source_lines = [
        "- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.",
        "- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.",
        "- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.",
        "- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.",
    ]

    report = f"""# {ticker.upper()} Technical Analysis Sample

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Data source: yfinance adjusted daily OHLCV through {last_date}.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: {label} ({score}/100).**

{decision_note}

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [{chart_path.name}]({chart_path.as_posix()})

## Key Indicators

{markdown_table(key)}

## Score Breakdown

{markdown_table(score_df)}

## Support And Resistance

- Support levels: {", ".join(money(level) for level in supports[-5:]) if supports else "None detected"}
- Resistance levels: {", ".join(money(level) for level in resistances[:5]) if resistances else "None detected"}

## Entry Plans

{markdown_table(entry_df)}

## Source Research Used

{chr(10).join(source_lines)}
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")


def run(ticker: str, out_dir: Path, period: str, chart_months: int) -> tuple[Path, Path, int, str]:
    ticker = ticker.upper()
    df = add_indicators(fetch_daily_data(ticker, period))
    ready = df.dropna()
    if len(ready) < 30:
        raise RuntimeError(f"Not enough indicator-ready rows for {ticker}; got {len(ready)}.")

    score, label, score_df = score_setup(df)
    supports, resistances = support_resistance(df)
    entries = build_entry_plans(df, supports, resistances, label)

    stamp = df.index[-1].strftime("%Y%m%d")
    chart_path = out_dir / f"{ticker}_technical_chart_{stamp}.png"
    report_path = out_dir / f"{ticker}_technical_report_{stamp}.md"
    write_chart(df, ticker, score, label, supports, resistances, entries, chart_path, chart_months)
    write_report(df, ticker, score, label, score_df, supports, resistances, entries, chart_path, report_path)
    return chart_path, report_path, score, label


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a stock technical-analysis framework chart and sample report.")
    parser.add_argument("--ticker", default=DEFAULT_TICKER, help=f"Ticker to analyze. Default: {DEFAULT_TICKER}.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Directory for chart and report outputs.")
    parser.add_argument("--period", default="2y", help="yfinance history period used for indicator warmup. Default: 2y.")
    parser.add_argument("--chart-months", type=int, default=3, help="Months of daily data to show on the chart. Default: 3.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chart_path, report_path, score, label = run(
        ticker=args.ticker,
        out_dir=Path(args.out_dir),
        period=args.period,
        chart_months=args.chart_months,
    )
    print(f"{args.ticker.upper()}: {label} ({score}/100)")
    print(f"Chart: {chart_path}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
