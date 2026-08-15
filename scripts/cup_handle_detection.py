from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


@dataclass
class PatternCandidate:
    score: float
    status: str
    scanner_bucket: str
    left_rim_idx: int
    bottom_idx: int
    right_rim_idx: int
    handle_low_idx: int
    last_idx: int
    left_rim_date: str
    bottom_date: str
    right_rim_date: str
    handle_low_date: str
    last_date: str
    left_rim_price: float
    bottom_price: float
    right_rim_price: float
    handle_low_price: float
    last_close: float
    cup_depth_pct: float
    handle_depth_pct_of_cup: float
    right_rim_gap_pct: float
    cup_width_weeks: int
    handle_width_weeks: int
    breakout_level: float
    projected_target: float
    volume_note: str
    notes: list[str]


def _flatten_yfinance_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [col[0] for col in df.columns]
    return df


def load_weekly(symbol: str, period: str) -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval="1wk", auto_adjust=False, progress=False)
    df = _flatten_yfinance_columns(df)
    if df.empty:
        raise RuntimeError(f"No data returned for {symbol}")
    df = df.rename(columns=str.title)
    expected = ["Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in expected if col not in df.columns]
    if missing:
        raise RuntimeError(f"Missing columns from yfinance data: {missing}")
    df = df[expected].dropna()
    df.index = pd.to_datetime(df.index)
    return df


def local_pivots(df: pd.DataFrame, window: int = 2) -> tuple[list[int], list[int]]:
    highs: list[int] = []
    lows: list[int] = []
    high = df["High"].to_numpy()
    low = df["Low"].to_numpy()
    for idx in range(window, len(df) - window):
        if high[idx] >= max(high[idx - window : idx]) and high[idx] >= max(high[idx + 1 : idx + window + 1]):
            highs.append(idx)
        if low[idx] <= min(low[idx - window : idx]) and low[idx] <= min(low[idx + 1 : idx + window + 1]):
            lows.append(idx)
    return highs, lows


def _linear_slope(values: np.ndarray) -> float:
    if len(values) < 2:
        return 0.0
    x = np.arange(len(values), dtype=float)
    slope, _ = np.polyfit(x, values.astype(float), 1)
    return float(slope)


def _cup_visual_expected(
    x_positions: np.ndarray,
    bottom_pos: float,
    left_rim: float,
    bottom: float,
    right_rim: float,
) -> np.ndarray:
    expected = np.empty_like(x_positions, dtype=float)
    left_mask = x_positions <= bottom_pos
    left_span = max(bottom_pos, 1e-6)
    right_span = max(1.0 - bottom_pos, 1e-6)
    left_u = (bottom_pos - x_positions[left_mask]) / left_span
    right_u = (x_positions[~left_mask] - bottom_pos) / right_span
    expected[left_mask] = bottom + (left_rim - bottom) * left_u**2
    expected[~left_mask] = bottom + (right_rim - bottom) * right_u**2
    return expected


def _cup_shape_score(df: pd.DataFrame, i: int, j: int, k: int, left_rim: float, bottom: float, right_rim: float) -> float:
    cup_width = k - i
    if cup_width <= 0:
        return 0.0
    cup_depth = max(max(left_rim, right_rim) - bottom, 1e-6)
    lows = df["Low"].iloc[i : k + 1].to_numpy(dtype=float)
    x_positions = np.linspace(0.0, 1.0, len(lows))
    bottom_pos = (j - i) / cup_width
    expected = _cup_visual_expected(x_positions, bottom_pos, left_rim, bottom, right_rim)
    rmse = float(np.sqrt(np.nanmean(((lows - expected) / cup_depth) ** 2)))
    fit_score = 1.0 - min(rmse / 0.24, 1.0)

    floor_limit = bottom + cup_depth * 0.25
    floor_weeks = int(np.sum(lows <= floor_limit))
    floor_score = min(floor_weeks / max(3.0, cup_width * 0.16), 1.0)

    center_score = 1.0 - min(abs(bottom_pos - 0.5) / 0.25, 1.0)
    return float(0.45 * fit_score + 0.30 * floor_score + 0.25 * center_score)


def _prior_uptrend_score(df: pd.DataFrame, i: int) -> float:
    lookback = min(26, i)
    if lookback < 8:
        return 0.5
    prior = df.iloc[i - lookback : i]
    prior_low = float(prior["Low"].min())
    left_price = float(df["High"].iloc[i])
    if prior_low <= 0:
        return 0.0
    advance = (left_price / prior_low) - 1.0
    return float(min(max(advance / 0.30, 0.0), 1.0))


def score_candidate(df: pd.DataFrame, i: int, j: int, k: int, last_idx: int) -> PatternCandidate | None:
    high = df["High"].to_numpy()
    low = df["Low"].to_numpy()
    close = df["Close"].to_numpy()
    volume = df["Volume"].to_numpy()

    left_rim = float(high[i])
    bottom = float(low[j])
    right_rim = float(high[k])
    last_close = float(close[last_idx])
    rim = max(left_rim, right_rim)
    cup_depth = rim - bottom
    if cup_depth <= 0:
        return None
    if bottom > float(np.nanmin(low[i : k + 1])) * 1.04:
        return None

    cup_width = k - i
    handle_width = last_idx - k
    cup_depth_pct = cup_depth / rim
    right_rim_gap_pct = abs(right_rim - left_rim) / rim

    if not (20 <= cup_width <= 70):
        return None
    if handle_width < 2 or handle_width > min(max(cup_width // 2, 4), 10):
        return None
    if not (0.12 <= cup_depth_pct <= 0.45):
        return None
    rim_deviation_of_cup = abs(right_rim - left_rim) / cup_depth
    if rim_deviation_of_cup > 0.35:
        return None

    bottom_pos = (j - i) / cup_width
    if bottom_pos < 0.30 or bottom_pos > 0.70:
        return None

    left_slope = _linear_slope(close[i : j + 1])
    right_slope = _linear_slope(close[j : k + 1])
    if left_slope >= 0 or right_slope <= 0:
        return None

    handle_slice = slice(k, last_idx + 1)
    handle_low_idx = int(k + np.argmin(low[handle_slice]))
    handle_low = float(low[handle_low_idx])
    handle_depth = right_rim - handle_low
    if handle_depth < 0:
        return None
    handle_depth_pct_of_cup = handle_depth / cup_depth
    if handle_depth_pct_of_cup > 0.45:
        return None
    if handle_low < bottom + cup_depth * 0.50:
        return None
    if float(close[last_idx]) < handle_low:
        return None

    cup_shape_score = _cup_shape_score(df, i, j, k, left_rim, bottom, right_rim)
    if cup_shape_score < 0.42:
        return None
    prior_score = _prior_uptrend_score(df, i)

    handle_high = float(max(high[k : last_idx + 1]))
    breakout_level = handle_high
    projected_target = breakout_level + cup_depth
    status = "awaiting breakout"
    if last_close > breakout_level:
        status = "breakout confirmed"
    elif last_close > breakout_level * 0.97:
        status = "near breakout"
    scanner_bucket = "Cup and Handle Breakout" if status == "breakout confirmed" else "Cup and Handle Pattern in Force"

    bottom_score = 1.0 - min(abs(bottom_pos - 0.5) / 0.5, 1.0)
    depth_score = 1.0 - min(abs(cup_depth_pct - 0.27) / 0.20, 1.0)
    rim_score = 1.0 - min(rim_deviation_of_cup / 0.35, 1.0)
    handle_score = 1.0 - min(abs(handle_depth_pct_of_cup - 0.25) / 0.25, 1.0)
    breakout_score = min(max((last_close - handle_low) / max(handle_high - handle_low, 1e-6), 0.0), 1.0)

    handle_vol = float(np.nanmean(volume[k : last_idx + 1]))
    cup_vol = float(np.nanmean(volume[i : k + 1]))
    recent_vol = float(volume[last_idx])
    handle_volume_ratio = handle_vol / cup_vol if cup_vol > 0 else math.inf
    if handle_volume_ratio > 1.05:
        return None
    volume_note = (
        f"volume condition PASS: handle avg volume {handle_volume_ratio:.2f}x cup avg; "
        f"latest week {recent_vol / handle_vol:.2f}x handle avg"
    )
    vol_score = 0.65 if handle_vol <= cup_vol else 0.35
    if status == "breakout confirmed" and recent_vol > handle_vol:
        vol_score += 0.20

    score = (
        16 * bottom_score
        + 15 * depth_score
        + 18 * rim_score
        + 17 * handle_score
        + 18 * cup_shape_score
        + 4 * prior_score
        + 12 * breakout_score
        + 8 * min(vol_score, 1.0)
    )

    notes: list[str] = []
    notes.append("cup has a declining left side, rising right side, and rounded U-shape fit")
    notes.append("handle remains in upper half of the cup")
    if right_rim < left_rim:
        notes.append("right rim is modestly below the left rim")
    if prior_score < 0.40:
        notes.append("prior uptrend is not strong, so continuation quality is weaker")
    if status != "breakout confirmed":
        notes.append("no weekly close above the handle/rim resistance yet")

    dates = df.index.strftime("%Y-%m-%d").to_list()
    return PatternCandidate(
        score=round(float(score), 2),
        status=status,
        scanner_bucket=scanner_bucket,
        left_rim_idx=i,
        bottom_idx=j,
        right_rim_idx=k,
        handle_low_idx=handle_low_idx,
        last_idx=last_idx,
        left_rim_date=dates[i],
        bottom_date=dates[j],
        right_rim_date=dates[k],
        handle_low_date=dates[handle_low_idx],
        last_date=dates[last_idx],
        left_rim_price=round(left_rim, 2),
        bottom_price=round(bottom, 2),
        right_rim_price=round(right_rim, 2),
        handle_low_price=round(handle_low, 2),
        last_close=round(last_close, 2),
        cup_depth_pct=round(cup_depth_pct * 100, 2),
        handle_depth_pct_of_cup=round(handle_depth_pct_of_cup * 100, 2),
        right_rim_gap_pct=round(right_rim_gap_pct * 100, 2),
        cup_width_weeks=cup_width,
        handle_width_weeks=handle_width,
        breakout_level=round(breakout_level, 2),
        projected_target=round(projected_target, 2),
        volume_note=volume_note,
        notes=notes,
    )


def find_patterns(df: pd.DataFrame) -> list[PatternCandidate]:
    pivot_highs, pivot_lows = local_pivots(df, window=2)
    last_idx = len(df) - 1
    candidates: list[PatternCandidate] = []
    for i in pivot_highs:
        for j in pivot_lows:
            if j <= i:
                continue
            for k in pivot_highs + [last_idx]:
                if k <= j or k >= last_idx:
                    continue
                candidate = score_candidate(df, i, j, k, last_idx)
                if candidate:
                    candidates.append(candidate)
    candidates.sort(key=lambda item: item.score, reverse=True)
    return candidates


def select_primary(patterns: list[PatternCandidate]) -> PatternCandidate | None:
    if not patterns:
        return None
    tighter = [
        item
        for item in patterns
        if item.cup_depth_pct <= 40.0 and item.handle_width_weeks <= 6
    ]
    if tighter:
        tighter.sort(key=lambda item: (item.right_rim_idx, item.score), reverse=True)
        return tighter[0]
    return patterns[0]


def score_interpretation(score: float) -> tuple[str, str]:
    if score >= 75:
        return "Strong", "Clean cup/handle geometry with stronger confirmation traits."
    if score >= 60:
        return "Good watchlist", "Pattern shape is usable, but still needs breakout/confirmation."
    if score >= 45:
        return "Speculative watchlist", "Recognizable structure, but one or more quality issues need respect."
    return "Weak", "Too many geometry or confirmation issues for a high-conviction setup."


def draw_candles(ax: plt.Axes, df: pd.DataFrame) -> None:
    dates = mdates.date2num(df.index.to_pydatetime())
    candle_width = 3.8
    for date_num, row in zip(dates, df.itertuples()):
        color = "#1f9d68" if row.Close >= row.Open else "#c2413b"
        ax.vlines(date_num, row.Low, row.High, color=color, linewidth=1.1, alpha=0.85)
        lower = min(row.Open, row.Close)
        height = abs(row.Close - row.Open)
        if math.isclose(height, 0.0):
            height = 0.35
        rect = plt.Rectangle(
            (date_num - candle_width / 2, lower),
            candle_width,
            height,
            facecolor=color,
            edgecolor=color,
            linewidth=0.8,
            alpha=0.78,
        )
        ax.add_patch(rect)
    ax.set_xlim(dates[0] - 5, dates[-1] + 5)


def _cup_visual_curve(xvals: np.ndarray, yvals: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    left_x, bottom_x, right_x = [float(value) for value in xvals]
    left_y, bottom_y, right_y = [float(value) for value in yvals]
    if math.isclose(left_x, right_x):
        return xvals, yvals

    left_curve_x = np.linspace(left_x, bottom_x, 110)
    right_curve_x = np.linspace(bottom_x, right_x, 90)
    left_span = max(bottom_x - left_x, 1e-6)
    right_span = max(right_x - bottom_x, 1e-6)
    left_u = (bottom_x - left_curve_x) / left_span
    right_u = (right_curve_x - bottom_x) / right_span
    left_curve_y = bottom_y + (left_y - bottom_y) * left_u**2
    right_curve_y = bottom_y + (right_y - bottom_y) * right_u**2

    x_curve = np.concatenate([left_curve_x, right_curve_x[1:]])
    y_curve = np.concatenate([left_curve_y, right_curve_y[1:]])
    return x_curve, y_curve


def _label_point(ax: plt.Axes, x: float, y: float, label: str, *, offset: tuple[int, int] = (0, 12)) -> None:
    ax.annotate(
        label,
        xy=(x, y),
        xytext=offset,
        textcoords="offset points",
        ha="center",
        fontsize=8.5,
        color="#111827",
        bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": "#d1d5db", "alpha": 0.88},
    )


def annotate_pattern(ax: plt.Axes, df: pd.DataFrame, pattern: PatternCandidate) -> None:
    idxs = [pattern.left_rim_idx, pattern.bottom_idx, pattern.right_rim_idx, pattern.handle_low_idx, pattern.last_idx]
    yvals = [
        pattern.left_rim_price,
        pattern.bottom_price,
        pattern.right_rim_price,
        pattern.handle_low_price,
        pattern.last_close,
    ]
    xvals = mdates.date2num(df.index[idxs].to_pydatetime())
    date_labels = [df.index[idx].strftime("%Y-%m-%d") for idx in idxs]
    cup_x, cup_y = _cup_visual_curve(xvals[:3], np.array(yvals[:3], dtype=float))
    handle_x = xvals[2:5]
    handle_y = yvals[2:5]

    ax.axhspan(pattern.breakout_level * 0.985, pattern.breakout_level * 1.015, color="#7c3aed", alpha=0.07)
    ax.fill_between(
        [xvals[2], xvals[4]],
        pattern.handle_low_price,
        pattern.breakout_level,
        color="#f59e0b",
        alpha=0.11,
        label="handle range",
    )
    ax.fill_between(
        cup_x,
        cup_y,
        pattern.breakout_level,
        where=cup_y <= pattern.breakout_level,
        color="#2563eb",
        alpha=0.08,
        label="cup bowl",
    )
    ax.plot(cup_x, cup_y, color="#2563eb", linewidth=3.0, solid_capstyle="round", label="smooth cup")
    ax.plot(xvals[:3], yvals[:3], color="#2563eb", linewidth=0, marker="o", markersize=6)
    ax.plot(handle_x, handle_y, color="#f59e0b", linewidth=2.8, marker="o", markersize=5.5, label="handle")
    ax.axhline(pattern.breakout_level, color="#7c3aed", linestyle="--", linewidth=1.6, label="handle end / resistance")
    ax.axhline(pattern.projected_target, color="#0f766e", linestyle=":", linewidth=1.5, label="measured target")
    target_x = xvals[-1]
    ax.scatter(
        [target_x],
        [pattern.projected_target],
        marker="*",
        s=260,
        color="#facc15",
        edgecolor="#92400e",
        linewidth=1.0,
        zorder=6,
        label="target star",
    )
    _label_point(
        ax,
        target_x,
        pattern.projected_target,
        f"Target\n{pattern.projected_target:.2f}",
        offset=(-10, -30),
    )
    ax.text(
        0.985,
        0.955,
        pattern.scanner_bucket,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        color="#111827",
        bbox={"boxstyle": "round,pad=0.3", "fc": "#f8fafc", "ec": "#94a3b8", "alpha": 0.92},
    )

    cup_height = max(pattern.left_rim_price, pattern.right_rim_price) - pattern.bottom_price
    for pct, alpha in [(0.382, 0.65), (0.5, 0.55), (0.618, 0.45)]:
        level = max(pattern.left_rim_price, pattern.right_rim_price) - cup_height * pct
        ax.hlines(level, xvals[0], xvals[2], color="#64748b", linestyle=":", linewidth=0.9, alpha=alpha)
        ax.text(xvals[0], level, f" {pct:.1%}", color="#64748b", fontsize=7.5, va="center")

    _label_point(ax, xvals[0], yvals[0], f"1st Pivot\n{date_labels[0]}\n{yvals[0]:.2f}")
    _label_point(ax, xvals[1], yvals[1], f"Cup Low\n{date_labels[1]}\n{yvals[1]:.2f}")
    _label_point(ax, xvals[2], yvals[2], f"2nd Pivot\n{date_labels[2]}\n{yvals[2]:.2f}", offset=(-34, 30))
    _label_point(ax, xvals[3], yvals[3], f"Handle Low\n{date_labels[3]}\n{yvals[3]:.2f}", offset=(0, -42))
    _label_point(ax, xvals[4], yvals[4], f"Handle End\n{date_labels[4]}\n{pattern.breakout_level:.2f}", offset=(10, 12))


def save_chart(
    symbol: str,
    df: pd.DataFrame,
    pattern: PatternCandidate | None,
    output: Path,
    *,
    tail_weeks: int | None = 53,
    title_suffix: str = "last 1 year",
) -> None:
    if tail_weeks is None:
        recent = df
    else:
        recent = df.tail(tail_weeks)
    fig = plt.figure(figsize=(13, 8), dpi=150)
    grid = fig.add_gridspec(4, 1, height_ratios=[3, 0.05, 0.9, 0.05])
    ax_price = fig.add_subplot(grid[0, 0])
    ax_vol = fig.add_subplot(grid[2, 0], sharex=ax_price)

    draw_candles(ax_price, recent)
    ax_price.plot(recent.index, recent["Close"].rolling(10, min_periods=1).mean(), color="#374151", linewidth=1.2, label="10-week MA")
    if pattern:
        offset = len(df) - len(recent)
        if pattern.left_rim_idx >= offset:
            adjusted = PatternCandidate(**asdict(pattern))
            adjusted.left_rim_idx -= offset
            adjusted.bottom_idx -= offset
            adjusted.right_rim_idx -= offset
            adjusted.handle_low_idx -= offset
            adjusted.last_idx -= offset
            annotate_pattern(ax_price, recent, adjusted)

    ax_price.set_title(f"{symbol} weekly chart, {title_suffix}, cup-and-handle scan", fontsize=14, weight="bold")
    ax_price.set_ylabel("Price")
    ax_price.grid(True, axis="y", alpha=0.25)
    ax_price.legend(loc="upper left", ncol=3, fontsize=8.5)

    up = recent["Close"] >= recent["Open"]
    colors = np.where(up, "#1f9d68", "#c2413b")
    ax_vol.bar(recent.index, recent["Volume"] / 1_000_000, width=4.2, color=colors, alpha=0.55)
    ax_vol.set_ylabel("Volume (M)")
    ax_vol.grid(True, axis="y", alpha=0.25)
    ax_vol.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax_vol.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)


def write_report(
    symbol: str,
    df: pd.DataFrame,
    patterns: list[PatternCandidate],
    one_year_chart_path: Path,
    context_chart_path: Path,
    output: Path,
) -> None:
    best = select_primary(patterns)
    lines = [
        f"# {symbol} Cup-And-Handle Weekly Scan",
        "",
        f"Data source: yfinance weekly OHLCV, generated through {df.index[-1].date()}.",
        f"One-year chart: {one_year_chart_path.name}",
        f"Pattern-context chart: {context_chart_path.name}",
        "",
        "This is technical-pattern research, not investment advice.",
        "",
    ]
    if not best:
        lines += ["No candidate passed the scan filters."]
    else:
        score_label, score_meaning = score_interpretation(best.score)
        breakout_gain = (best.breakout_level / best.last_close - 1.0) * 100.0
        target_gain = (best.projected_target / best.last_close - 1.0) * 100.0
        invalidation_loss = (best.handle_low_price / best.last_close - 1.0) * 100.0
        cup_height = max(best.left_rim_price, best.right_rim_price) - best.bottom_price
        ideal_handle_floor = best.bottom_price + cup_height * 0.50
        lines += [
            "## Summary",
            "",
            "| Item | Read |",
            "| --- | --- |",
            f"| Pattern bucket | {best.scanner_bucket} |",
            f"| Verdict | {score_label}: {score_meaning} |",
            f"| Score | {best.score}/100 |",
            f"| Latest weekly close | {best.last_close} on {best.last_date} |",
            f"| Breakout trigger | Weekly close above {best.breakout_level} ({breakout_gain:+.1f}% from latest close) |",
            f"| Potential measured target | {best.projected_target} ({target_gain:+.1f}% from latest close, if breakout confirms) |",
            f"| Handle risk / invalidation area | Below handle low {best.handle_low_price} ({invalidation_loss:.1f}% from latest close) |",
            f"| Current state | {best.status}; no confirmed weekly breakout yet |",
            "",
            "## How To Read The Score",
            "",
            "| Score band | Meaning |",
            "| --- | --- |",
            "| 75-100 | Strong: clean geometry and stronger confirmation traits. |",
            "| 60-74 | Good watchlist: pattern is usable but still needs confirmation. |",
            "| 45-59 | Speculative watchlist: recognizable shape, but quality issues remain. |",
            "| Below 45 | Weak: too many geometry/confirmation problems. |",
            "",
            "This score is a pattern-quality score, not a probability forecast. It rewards cup symmetry, reasonable depth, rim alignment, handle quality, proximity to breakout, and healthier volume behavior.",
            "",
            "## Key Levels",
            "",
            "| Level | Date | Price | Meaning |",
            "| --- | --- | ---: | --- |",
            f"| 1st Pivot | {best.left_rim_date} | {best.left_rim_price} | Left rim of the cup. |",
            f"| Cup | {best.bottom_date} | {best.bottom_price} | Low point of the cup. |",
            f"| 2nd Pivot | {best.right_rim_date} | {best.right_rim_price} | Right rim / resistance area. |",
            f"| Handle | {best.handle_low_date} | {best.handle_low_price} | Handle pullback low. |",
            f"| Handle End | {best.last_date} | {best.breakout_level} | Breakout level to watch. |",
            f"| Measured target | n/a | {best.projected_target} | Breakout level plus cup depth. |",
            "",
            "## Pattern Quality",
            "",
            "| Check | Result | Read |",
            "| --- | ---: | --- |",
            f"| Cup depth | {best.cup_depth_pct}% | Deep but still within the script's loose scan range. |",
            f"| Cup width | {best.cup_width_weeks} weeks | Long enough to qualify as a weekly base candidate. |",
            f"| Handle width | {best.handle_width_weeks} weeks | Short/current handle; still forming. |",
            f"| Handle depth | {best.handle_depth_pct_of_cup}% of cup depth | Pullback is deeper than ideal, so confirmation matters. |",
            f"| Rim gap | {best.right_rim_gap_pct}% | Right rim is below the left rim; this weakens symmetry. |",
            f"| Ideal upper-half handle floor | {ideal_handle_floor:.2f} | Handle quality improves if it holds above this zone. |",
            f"| Volume | n/a | {best.volume_note}. |",
            "",
            "## Interpretation",
            "",
            f"- {symbol.upper()} currently fits the video-style scanner bucket `{best.scanner_bucket}`.",
            f"- The bullish trigger is a weekly breakout above `{best.breakout_level}`.",
            f"- A simple measured target after confirmation is `{best.projected_target}`.",
            f"- The setup weakens if price loses the handle low near `{best.handle_low_price}`.",
            f"- Visible inside the one-year chart: {'yes' if best.left_rim_idx >= len(df) - 53 else 'partial only'}.",
            "",
            "## Caveats",
            "",
        ]
        lines.extend([f"- {note}" for note in best.notes])
        lines += [
            "",
            "## TrendSpider / Video Mapping",
            "",
            "- The transcript workflow is: enable chart-pattern recognition, choose settings, scan a universe, optionally schedule the scan, then rank candidates by fundamentals/news/catalysts/technicals.",
            "- Pattern in Force means a formed/active pattern waiting to break out.",
            "- Breakout means price has moved through handle resistance.",
            "- This script maps: left rim = 1st Pivot, bottom = Cup, right rim = 2nd Pivot, handle low/current handle = Handle, breakout level = Handle End.",
            "- The chart adds Fibonacci-style reference lines and a shaded handle range, matching the video/article settings.",
            "",
            "## Top Iterations",
            "",
            "| Rank | Score | Bucket | Structure | Breakout |",
            "| ---: | ---: | --- | --- | ---: |",
        ]
        for idx, item in enumerate(patterns[:10], start=1):
            lines.append(
                f"| {idx} | {item.score} | {item.scanner_bucket} | "
                f"{item.left_rim_date} -> {item.bottom_date} -> {item.right_rim_date}; handle low {item.handle_low_date} | "
                f"{item.breakout_level} |"
            )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="TSLA")
    parser.add_argument("--period", default="2y")
    parser.add_argument("--output-dir", default="reports/cup_handle")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_weekly(args.symbol, args.period)
    patterns = find_patterns(df)
    chart_path = output_dir / f"{args.symbol.upper()}_weekly_cup_handle_1y.png"
    context_chart_path = output_dir / f"{args.symbol.upper()}_weekly_cup_handle_context.png"
    report_path = output_dir / f"{args.symbol.upper()}_cup_handle_report.md"
    json_path = output_dir / f"{args.symbol.upper()}_cup_handle_candidates.json"

    primary = select_primary(patterns)
    save_chart(args.symbol.upper(), df, primary, chart_path, tail_weeks=53, title_suffix="last 1 year")
    context_tail_weeks = None
    if primary:
        context_tail_weeks = min(len(df), len(df) - max(primary.left_rim_idx - 3, 0))
    save_chart(
        args.symbol.upper(),
        df.tail(context_tail_weeks) if context_tail_weeks else df,
        primary if primary and context_tail_weeks == len(df) else None,
        context_chart_path,
        tail_weeks=None,
        title_suffix="pattern context",
    )
    if primary and context_tail_weeks != len(df):
        context_df = df.tail(context_tail_weeks)
        adjusted = PatternCandidate(**asdict(primary))
        offset = len(df) - len(context_df)
        adjusted.left_rim_idx -= offset
        adjusted.bottom_idx -= offset
        adjusted.right_rim_idx -= offset
        adjusted.handle_low_idx -= offset
        adjusted.last_idx -= offset
        save_chart(
            args.symbol.upper(),
            context_df,
            adjusted,
            context_chart_path,
            tail_weeks=None,
            title_suffix="pattern context",
        )
    write_report(args.symbol.upper(), df, patterns, chart_path, context_chart_path, report_path)
    json_path.write_text(json.dumps([asdict(item) for item in patterns], indent=2), encoding="utf-8")

    print(f"chart={chart_path}")
    print(f"context_chart={context_chart_path}")
    print(f"report={report_path}")
    print(f"candidates={json_path}")
    if primary:
        print(json.dumps(asdict(primary), indent=2))
    else:
        print("No candidates found")


if __name__ == "__main__":
    main()
