from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_detection import (
    PatternCandidate,
    _cup_shape_score,
    _linear_slope,
    _prior_uptrend_score,
    annotate_pattern,
    local_pivots,
    score_interpretation,
)


def _flatten_yfinance_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [col[0] for col in df.columns]
    return df


def load_daily(symbol: str, period: str) -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval="1d", auto_adjust=False, progress=False)
    df = _flatten_yfinance_columns(df)
    if df.empty:
        raise RuntimeError(f"No daily data returned for {symbol}")
    df = df.rename(columns=str.title)
    expected = ["Open", "High", "Low", "Close", "Volume"]
    missing = [column for column in expected if column not in df.columns]
    if missing:
        raise RuntimeError(f"Missing columns from yfinance data: {missing}")
    df = df[expected].dropna()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


def score_daily_candidate(
    df: pd.DataFrame,
    i: int,
    j: int,
    k: int,
    handle_end_idx: int,
    scan_idx: int | None = None,
) -> PatternCandidate | None:
    if scan_idx is None:
        scan_idx = handle_end_idx
    high = df["High"].to_numpy()
    low = df["Low"].to_numpy()
    close = df["Close"].to_numpy()
    volume = df["Volume"].to_numpy()

    left_rim = float(high[i])
    bottom = float(low[j])
    right_rim = float(high[k])
    handle_end_close = float(close[handle_end_idx])
    latest_close = float(close[scan_idx])
    rim = max(left_rim, right_rim)
    cup_depth = rim - bottom
    if cup_depth <= 0:
        return None
    if bottom > float(np.nanmin(low[i : k + 1])) * 1.04:
        return None

    cup_width = k - i
    handle_width = handle_end_idx - k
    cup_depth_pct = cup_depth / rim
    right_rim_gap_pct = abs(right_rim - left_rim) / rim

    # Daily mode: wider than weekly in bar count, but still intended to find bases, not intraday noise.
    if not (30 <= cup_width <= 180):
        return None
    if handle_width < 3 or handle_width > min(max(cup_width // 2, 8), 30):
        return None
    if not (0.12 <= cup_depth_pct <= 0.70):
        return None
    rim_deviation_of_cup = abs(right_rim - left_rim) / cup_depth
    if rim_deviation_of_cup > 0.55:
        return None

    bottom_pos = (j - i) / cup_width
    if bottom_pos < 0.25 or bottom_pos > 0.75:
        return None

    left_slope = _linear_slope(close[i : j + 1])
    right_slope = _linear_slope(close[j : k + 1])
    if left_slope >= 0 or right_slope <= 0:
        return None

    handle_slice = slice(k, handle_end_idx + 1)
    handle_low_idx = int(k + np.argmin(low[handle_slice]))
    handle_low = float(low[handle_low_idx])
    handle_depth = right_rim - handle_low
    if handle_depth < 0:
        return None
    handle_depth_pct_of_cup = handle_depth / cup_depth
    if handle_depth_pct_of_cup > 0.60:
        return None
    if handle_low < bottom + cup_depth * 0.45:
        return None
    if float(close[handle_end_idx]) < handle_low:
        return None

    cup_shape_score = _cup_shape_score(df, i, j, k, left_rim, bottom, right_rim)
    if cup_shape_score < 0.36:
        return None
    prior_score = _prior_uptrend_score(df, i)

    handle_high = float(max(high[k : handle_end_idx + 1]))
    breakout_level = handle_high
    projected_target = breakout_level + cup_depth
    status = "awaiting breakout"
    post_handle_close_max = float(np.nanmax(close[handle_end_idx : scan_idx + 1]))
    if latest_close > breakout_level:
        status = "breakout confirmed"
    elif post_handle_close_max > breakout_level:
        status = "breakout attempt, back below resistance"
    elif latest_close > breakout_level * 0.97:
        status = "near breakout"
    scanner_bucket = "Cup and Handle Breakout" if status == "breakout confirmed" else "Cup and Handle Pattern in Force"

    bottom_score = 1.0 - min(abs(bottom_pos - 0.5) / 0.5, 1.0)
    depth_score = 1.0 - min(abs(cup_depth_pct - 0.32) / 0.28, 1.0)
    rim_score = 1.0 - min(rim_deviation_of_cup / 0.55, 1.0)
    handle_score = 1.0 - min(abs(handle_depth_pct_of_cup - 0.28) / 0.32, 1.0)
    breakout_score = min(max((latest_close - handle_low) / max(handle_high - handle_low, 1e-6), 0.0), 1.0)

    handle_vol = float(np.nanmean(volume[k : handle_end_idx + 1]))
    cup_vol = float(np.nanmean(volume[i : k + 1]))
    recent_vol = float(volume[scan_idx])
    breakout_close_indexes = np.where(close[handle_end_idx : scan_idx + 1] > breakout_level)[0] + handle_end_idx
    breakout_day_idx: int | None = int(breakout_close_indexes[0]) if len(breakout_close_indexes) else None
    breakout_volume_ratio: float | None = None
    if breakout_day_idx is not None:
        avg_start = max(0, breakout_day_idx - 50)
        prior_avg_vol = float(np.nanmean(volume[avg_start:breakout_day_idx]))
        if prior_avg_vol > 0:
            breakout_volume_ratio = float(volume[breakout_day_idx] / prior_avg_vol)

    handle_volume_ratio = handle_vol / cup_vol if cup_vol > 0 else math.inf
    quiet_handle_pass = handle_volume_ratio <= 1.05
    breakout_volume_pass = breakout_volume_ratio is not None and breakout_volume_ratio >= 1.40
    volume_condition_pass = breakout_volume_pass if breakout_day_idx is not None else quiet_handle_pass
    if not volume_condition_pass:
        return None

    volume_condition = "PASS"
    if breakout_day_idx is not None:
        volume_condition_detail = (
            f"breakout-day volume {breakout_volume_ratio:.2f}x prior 50-day avg "
            f"on {df.index[breakout_day_idx].strftime('%Y-%m-%d')}"
        )
    else:
        volume_condition_detail = f"handle avg volume {handle_volume_ratio:.2f}x cup avg"

    volume_note = (
        f"volume condition {volume_condition}: {volume_condition_detail}; "
        f"handle avg {handle_volume_ratio:.2f}x cup avg; latest day {recent_vol / handle_vol:.2f}x handle avg"
    )
    vol_score = 0.65 if quiet_handle_pass else 0.45
    if breakout_volume_pass:
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

    notes: list[str] = [
        "daily cup has a declining left side, rising right side, and rounded U-shape fit",
        "daily handle remains in the upper half of the cup",
    ]
    if right_rim < left_rim:
        notes.append("right rim is below the left rim")
    if prior_score < 0.40:
        notes.append("prior uptrend is not strong, so continuation quality is weaker")
    notes.append(volume_condition_detail)
    if status == "breakout confirmed":
        notes.append(f"latest daily close is above resistance as of {df.index[scan_idx].strftime('%Y-%m-%d')}")
    elif status == "breakout attempt, back below resistance":
        notes.append("price closed above resistance after the handle, but the latest close is back below it")
    else:
        notes.append("no daily close above the handle/rim resistance yet")

    dates = df.index.strftime("%Y-%m-%d").to_list()
    return PatternCandidate(
        score=round(float(score), 2),
        status=status,
        scanner_bucket=scanner_bucket,
        left_rim_idx=i,
        bottom_idx=j,
        right_rim_idx=k,
        handle_low_idx=handle_low_idx,
        last_idx=handle_end_idx,
        left_rim_date=dates[i],
        bottom_date=dates[j],
        right_rim_date=dates[k],
        handle_low_date=dates[handle_low_idx],
        last_date=dates[handle_end_idx],
        left_rim_price=round(left_rim, 2),
        bottom_price=round(bottom, 2),
        right_rim_price=round(right_rim, 2),
        handle_low_price=round(handle_low, 2),
        last_close=round(handle_end_close, 2),
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


def find_daily_patterns(df: pd.DataFrame, pivot_window: int = 3, recent_endpoints: int = 40) -> list[PatternCandidate]:
    pivot_highs, pivot_lows = local_pivots(df, window=pivot_window)
    scan_idx = len(df) - 1
    endpoint_indexes = list(range(max(0, scan_idx - recent_endpoints), scan_idx + 1))
    candidates: list[PatternCandidate] = []
    for handle_end_idx in endpoint_indexes:
        for k in pivot_highs:
            if k >= handle_end_idx:
                continue
            handle_width = handle_end_idx - k
            if handle_width < 3 or handle_width > 30:
                continue
            for j in pivot_lows:
                if j <= 0 or j >= k:
                    continue
                for i in pivot_highs:
                    if i >= j:
                        continue
                    candidate = score_daily_candidate(df, i, j, k, handle_end_idx, scan_idx)
                    if candidate:
                        candidates.append(candidate)
    candidates.sort(key=lambda item: item.score, reverse=True)
    return candidates


def select_daily_primary(patterns: list[PatternCandidate]) -> PatternCandidate | None:
    if not patterns:
        return None
    cleaner = [
        item
        for item in patterns
        if item.cup_depth_pct <= 55.0
        and 3 <= item.handle_width_weeks <= 20
        and item.handle_depth_pct_of_cup <= 45.0
    ]
    status_rank = {"breakout confirmed": 3, "near breakout": 2, "breakout attempt, back below resistance": 1, "awaiting breakout": 0}
    if cleaner:
        cleaner.sort(key=lambda item: (status_rank.get(item.status, 0), item.last_idx, item.right_rim_idx, item.score), reverse=True)
        return cleaner[0]
    return sorted(patterns, key=lambda item: (status_rank.get(item.status, 0), item.last_idx, item.score), reverse=True)[0]


def draw_daily_candles(ax: plt.Axes, df: pd.DataFrame) -> None:
    dates = mdates.date2num(df.index.to_pydatetime())
    candle_width = 0.65
    for date_num, row in zip(dates, df.itertuples()):
        color = "#1f9d68" if row.Close >= row.Open else "#c2413b"
        ax.vlines(date_num, row.Low, row.High, color=color, linewidth=0.9, alpha=0.85)
        lower = min(row.Open, row.Close)
        height = abs(row.Close - row.Open) or 0.02
        ax.add_patch(
            plt.Rectangle(
                (date_num - candle_width / 2, lower),
                candle_width,
                height,
                facecolor=color,
                edgecolor=color,
                linewidth=0.6,
                alpha=0.78,
            )
        )
    ax.set_xlim(dates[0] - 2, dates[-1] + 2)


def save_daily_chart(symbol: str, df: pd.DataFrame, pattern: PatternCandidate | None, output: Path, tail_days: int = 220) -> None:
    recent = df.tail(tail_days)
    fig = plt.figure(figsize=(13, 8), dpi=150)
    grid = fig.add_gridspec(4, 1, height_ratios=[3, 0.05, 0.9, 0.05])
    ax_price = fig.add_subplot(grid[0, 0])
    ax_vol = fig.add_subplot(grid[2, 0], sharex=ax_price)

    draw_daily_candles(ax_price, recent)
    ax_price.plot(recent.index, recent["Close"].rolling(20, min_periods=1).mean(), color="#374151", linewidth=1.1, label="20-day MA")
    ax_price.plot(recent.index, recent["Close"].rolling(50, min_periods=1).mean(), color="#0f766e", linewidth=1.0, label="50-day MA")
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

    ax_price.set_title(f"{symbol} daily chart, cup-and-handle scan", fontsize=14, weight="bold")
    ax_price.set_ylabel("Price")
    ax_price.grid(True, axis="y", alpha=0.25)
    ax_price.legend(loc="upper left", ncol=3, fontsize=8.5)

    up = recent["Close"] >= recent["Open"]
    colors = np.where(up, "#1f9d68", "#c2413b")
    ax_vol.bar(recent.index, recent["Volume"] / 1_000_000, width=0.8, color=colors, alpha=0.55)
    vol_ma50 = recent["Volume"].rolling(50, min_periods=10).mean() / 1_000_000
    ax_vol.plot(recent.index, vol_ma50, color="#7c3aed", linewidth=1.0, alpha=0.9, label="50-day avg volume")
    if pattern:
        breakout_window = df.iloc[pattern.last_idx :].copy()
        breakout_rows = breakout_window[breakout_window["Close"] > pattern.breakout_level]
        if not breakout_rows.empty:
            breakout_date = breakout_rows.index[0]
            avg_start = max(0, df.index.get_loc(breakout_date) - 50)
            breakout_idx = df.index.get_loc(breakout_date)
            prior_avg_vol = float(df["Volume"].iloc[avg_start:breakout_idx].mean())
            breakout_vol = float(df.loc[breakout_date, "Volume"])
            if breakout_date in recent.index and prior_avg_vol > 0:
                breakout_vol_m = breakout_vol / 1_000_000
                ratio = breakout_vol / prior_avg_vol
                ax_vol.axvline(breakout_date, color="#f59e0b", linestyle="--", linewidth=1.2, alpha=0.9)
                ax_vol.scatter(
                    [breakout_date],
                    [breakout_vol_m],
                    marker="*",
                    s=130,
                    color="#facc15",
                    edgecolor="#92400e",
                    linewidth=0.9,
                    zorder=5,
                )
                ax_vol.annotate(
                    f"Volume confirm\n{ratio:.2f}x 50D avg",
                    xy=(breakout_date, breakout_vol_m),
                    xytext=(12, 14),
                    textcoords="offset points",
                    fontsize=8,
                    color="#111827",
                    bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": "#d1d5db", "alpha": 0.88},
                )
    ax_vol.set_ylabel("Volume (M)")
    ax_vol.grid(True, axis="y", alpha=0.25)
    ax_vol.legend(loc="upper left", fontsize=8)
    ax_vol.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax_vol.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))

    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)


def markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return ""
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in frame.columns) + " |")
    return "\n".join(lines)


def write_daily_report(symbol: str, df: pd.DataFrame, patterns: list[PatternCandidate], chart_path: Path, output: Path) -> None:
    best = select_daily_primary(patterns)
    current_date = df.index[-1].strftime("%Y-%m-%d")
    current_close = float(df["Close"].iloc[-1])
    lines = [
        f"# {symbol} Daily Cup-And-Handle Scan",
        "",
        f"Data source: yfinance daily OHLCV through `{current_date}`.",
        f"Chart: `{chart_path.name}`",
        "",
        "This is technical-pattern research, not investment advice.",
        "",
        "## Volume Rule Used",
        "",
        "Daily candidates now must pass one volume gate: either the handle is quiet before breakout "
        "(`handle average volume <= 1.05x cup average volume`), or a breakout/attempt closes above resistance "
        "on at least `1.40x` the prior 50-day average volume.",
        "",
    ]
    if not best:
        lines += [
            "## Summary",
            "",
            "No daily cup-and-handle candidate passed the configured geometry filters.",
            "",
        ]
    else:
        score_label, score_meaning = score_interpretation(best.score)
        target_return = (best.projected_target / best.breakout_level - 1.0) * 100.0
        latest_to_breakout = (best.breakout_level / current_close - 1.0) * 100.0
        lines += [
            "## Summary",
            "",
            "| Item | Read |",
            "| --- | --- |",
            f"| Pattern bucket | {best.scanner_bucket} |",
            f"| Current status | {best.status} |",
            f"| Score | {best.score}/100 ({score_label}: {score_meaning}) |",
            f"| Latest close | {current_close:.2f} on {current_date} |",
            f"| Pattern handle end | {best.last_close} on {best.last_date} |",
            f"| Breakout trigger | Daily close above {best.breakout_level} ({latest_to_breakout:+.1f}% from latest close) |",
            f"| Measured target | {best.projected_target} ({target_return:.1f}% from breakout) |",
            f"| Invalidation / stop area | Below handle low {best.handle_low_price} |",
            "",
            "## Key Levels",
            "",
            "| Level | Date | Price |",
            "| --- | --- | ---: |",
            f"| Left rim | {best.left_rim_date} | {best.left_rim_price} |",
            f"| Cup low | {best.bottom_date} | {best.bottom_price} |",
            f"| Right rim | {best.right_rim_date} | {best.right_rim_price} |",
            f"| Handle low | {best.handle_low_date} | {best.handle_low_price} |",
            f"| Handle end / resistance | {best.last_date} | {best.breakout_level} |",
            f"| Measured target | n/a | {best.projected_target} |",
            "",
            "## Pattern Quality",
            "",
            "| Check | Result |",
            "| --- | ---: |",
            f"| Cup depth | {best.cup_depth_pct}% |",
            f"| Cup width | {best.cup_width_weeks} daily bars |",
            f"| Handle width | {best.handle_width_weeks} daily bars |",
            f"| Handle depth | {best.handle_depth_pct_of_cup}% of cup depth |",
            f"| Rim gap | {best.right_rim_gap_pct}% |",
            f"| Volume | {best.volume_note} |",
            "",
        ]
    display_patterns = patterns
    if best:
        display_patterns = [best] + [pattern for pattern in patterns if pattern != best]

    rows = []
    for rank, pattern in enumerate(display_patterns[:10], start=1):
        rows.append(
            {
                "Rank": rank,
                "Score": pattern.score,
                "Status": pattern.status,
                "Bucket": pattern.scanner_bucket,
                "HandleEnd": pattern.last_date,
                "LeftRim": pattern.left_rim_date,
                "CupLow": pattern.bottom_date,
                "RightRim": pattern.right_rim_date,
                "HandleLow": pattern.handle_low_date,
                "Breakout": pattern.breakout_level,
                "Target": pattern.projected_target,
            }
        )
    lines += [
        "## Top Daily Iterations",
        "",
        markdown_table(pd.DataFrame(rows)) if rows else "No candidates.",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="IREN")
    parser.add_argument("--period", default="2y")
    parser.add_argument("--output-dir", default="reports/cup_handle_daily_iren")
    parser.add_argument("--tail-days", type=int, default=220)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    symbol = args.symbol.upper()
    df = load_daily(symbol, args.period)
    patterns = find_daily_patterns(df)
    best = select_daily_primary(patterns)
    chart_path = output_dir / f"{symbol}_daily_cup_handle.png"
    report_path = output_dir / f"{symbol}_daily_cup_handle_report.md"
    candidates_path = output_dir / f"{symbol}_daily_cup_handle_candidates.json"
    save_daily_chart(symbol, df, best, chart_path, tail_days=args.tail_days)
    write_daily_report(symbol, df, patterns, chart_path, report_path)
    export_patterns = patterns
    if best:
        export_patterns = [best] + [pattern for pattern in patterns if pattern != best]
    candidates_path.write_text(json.dumps([asdict(pattern) for pattern in export_patterns[:25]], indent=2), encoding="utf-8")

    print(f"symbol={symbol}")
    print(f"daily_bars={len(df)}")
    print(f"patterns={len(patterns)}")
    if best:
        print(f"best_score={best.score}")
        print(f"best_bucket={best.scanner_bucket}")
        print(f"breakout={best.breakout_level}")
        print(f"target={best.projected_target}")
    print(f"chart={chart_path}")
    print(f"report={report_path}")


if __name__ == "__main__":
    main()
