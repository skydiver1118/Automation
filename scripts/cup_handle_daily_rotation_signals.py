from __future__ import annotations

import argparse
import json
import pickle
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_daily_detection import score_daily_candidate  # noqa: E402
from scripts.cup_handle_detection import PatternCandidate, local_pivots  # noqa: E402
from scripts.cup_handle_rotation_backtest import (  # noqa: E402
    constituent_set_on,
    load_historical_sp500,
    next_trading_day,
    nth_trading_day,
    unique_symbols,
)


def load_cached_frames(cache_path: Path, symbols: list[str]) -> dict[str, pd.DataFrame]:
    with cache_path.open("rb") as fh:
        cached = pickle.load(fh)
    allowed = set(symbols)
    frames = {symbol: frame for symbol, frame in cached.items() if symbol in allowed}
    for symbol, frame in list(frames.items()):
        frame = frame.rename(columns=str.title)
        expected = ["Open", "High", "Low", "Close", "Volume"]
        if any(column not in frame.columns for column in expected):
            frames.pop(symbol, None)
            continue
        clean = frame[expected].dropna().copy()
        clean.index = pd.to_datetime(clean.index).tz_localize(None)
        frames[symbol] = clean
    return frames


def find_daily_patterns_asof(
    df: pd.DataFrame,
    last_idx: int,
    pivot_highs: np.ndarray,
    pivot_lows: np.ndarray,
    *,
    min_target_return_pct: float,
    min_score: float,
    max_right_rims: int = 3,
    max_left_rims: int = 3,
    max_cup_lows: int = 2,
) -> list[PatternCandidate]:
    candidates: list[PatternCandidate] = []
    high = df["High"].to_numpy()
    low = df["Low"].to_numpy()
    right_rims = pivot_highs[(last_idx - pivot_highs >= 3) & (last_idx - pivot_highs <= 30)]
    if right_rims.size > max_right_rims:
        right_rims = right_rims[np.argsort(high[right_rims])[-max_right_rims:]]
    for k in right_rims:
        left_rims = pivot_highs[(pivot_highs >= k - 180) & (pivot_highs <= k - 30)]
        if left_rims.size == 0:
            continue
        if left_rims.size > max_left_rims:
            left_rims = left_rims[np.argsort(high[left_rims])[-max_left_rims:]]
        cup_lows = pivot_lows[(pivot_lows > int(left_rims.min())) & (pivot_lows < k)]
        if cup_lows.size == 0:
            continue
        if cup_lows.size > max_cup_lows:
            cup_lows = cup_lows[np.argsort(low[cup_lows])[:max_cup_lows]]
        for j in cup_lows:
            valid_left_rims = left_rims[left_rims < j]
            for i in valid_left_rims:
                rim = max(float(high[i]), float(high[k]))
                cup_depth = rim - float(low[j])
                if cup_depth <= 0:
                    continue
                cup_width = int(k - i)
                bottom_pos = (int(j) - int(i)) / cup_width
                if bottom_pos < 0.25 or bottom_pos > 0.75:
                    continue
                cup_depth_pct = cup_depth / rim
                if cup_depth_pct < 0.12 or cup_depth_pct > 0.70:
                    continue
                if abs(float(high[k]) - float(high[i])) / cup_depth > 0.55:
                    continue
                handle_low = float(np.nanmin(low[int(k) : last_idx + 1]))
                handle_depth_pct = (float(high[k]) - handle_low) / cup_depth
                if handle_depth_pct > 0.60:
                    continue
                if handle_low < float(low[j]) + cup_depth * 0.45:
                    continue
                cup_vol = float(df["Volume"].iloc[int(i) : int(k) + 1].mean())
                handle_vol = float(df["Volume"].iloc[int(k) : last_idx + 1].mean())
                if cup_vol <= 0 or handle_vol / cup_vol > 1.05:
                    continue
                candidate = score_daily_candidate(df, int(i), int(j), int(k), last_idx, last_idx)
                if candidate is None:
                    continue
                target_return_pct = (candidate.projected_target / candidate.breakout_level - 1.0) * 100.0
                if target_return_pct <= min_target_return_pct:
                    continue
                if candidate.score < min_score:
                    continue
                if candidate.scanner_bucket != "Cup and Handle Pattern in Force":
                    continue
                candidates.append(candidate)
    candidates.sort(key=lambda item: item.score, reverse=True)
    return candidates


def build_signal_table(
    frames: dict[str, pd.DataFrame],
    history: pd.DataFrame,
    calendar: pd.DatetimeIndex,
    *,
    start: str,
    end: str,
    min_score: float,
    min_target_return_pct: float,
    top_n_per_signal_date: int,
    max_symbols: int | None = None,
    pivot_window: int = 3,
    scan_step: int = 1,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    symbols = sorted(frames)
    if max_symbols:
        symbols = symbols[:max_symbols]
    scan_start = pd.Timestamp(start)
    scan_end = pd.Timestamp(end)
    membership_cache: dict[pd.Timestamp, set[str]] = {}
    for symbol_index, symbol in enumerate(symbols, start=1):
        if symbol_index == 1 or symbol_index % 25 == 0:
            print(f"Scanning daily patterns for {symbol_index}/{len(symbols)}: {symbol}", flush=True)
        daily = frames[symbol]
        if len(daily) < 240:
            continue
        pivot_highs_list, pivot_lows_list = local_pivots(daily, window=pivot_window)
        pivot_highs = np.asarray(pivot_highs_list, dtype=int)
        pivot_lows = np.asarray(pivot_lows_list, dtype=int)
        if pivot_highs.size == 0 or pivot_lows.size == 0:
            continue
        start_idx = max(220, int(daily.index.searchsorted(scan_start)))
        end_idx = min(len(daily) - 1, int(daily.index.searchsorted(scan_end, side="right")) - 1)
        for last_idx in range(start_idx, end_idx + 1, scan_step):
            signal_day = pd.Timestamp(daily.index[last_idx])
            if signal_day not in membership_cache:
                membership_cache[signal_day] = constituent_set_on(history, signal_day)
            if symbol not in membership_cache[signal_day]:
                continue
            trade_start = next_trading_day(calendar, signal_day)
            if trade_start is None:
                continue
            expire_date = nth_trading_day(calendar, trade_start, 3)
            if expire_date is None:
                continue
            candidates = find_daily_patterns_asof(
                daily,
                last_idx,
                pivot_highs,
                pivot_lows,
                min_target_return_pct=min_target_return_pct,
                min_score=min_score,
            )
            if not candidates:
                continue
            for candidate in candidates[: max(top_n_per_signal_date, 1)]:
                rows.append(
                    {
                        "Symbol": symbol,
                        "SignalDate": signal_day.strftime("%Y-%m-%d"),
                        "TradeStartDate": trade_start.strftime("%Y-%m-%d"),
                        "ExpireDate": expire_date.strftime("%Y-%m-%d"),
                        "Score": candidate.score,
                        "BreakoutLevel": candidate.breakout_level,
                        "Target": candidate.projected_target,
                        "TargetReturnPct": round((candidate.projected_target / candidate.breakout_level - 1.0) * 100.0, 2),
                        "Stop": candidate.handle_low_price,
                        "CupLowDate": candidate.bottom_date,
                        "LeftRimDate": candidate.left_rim_date,
                        "RightRimDate": candidate.right_rim_date,
                        "HandleLowDate": candidate.handle_low_date,
                        "CupDepthPct": candidate.cup_depth_pct,
                        "HandleDepthPctOfCup": candidate.handle_depth_pct_of_cup,
                        "CupWidthDays": candidate.cup_width_weeks,
                        "HandleWidthDays": candidate.handle_width_weeks,
                        "VolumeNote": candidate.volume_note,
                        "CandidateJson": json.dumps(asdict(candidate)),
                    }
                )
    signals = pd.DataFrame(rows)
    if signals.empty:
        return signals
    signals["SignalDateTs"] = pd.to_datetime(signals["SignalDate"])
    signals = signals.sort_values(["SignalDateTs", "Score", "TargetReturnPct"], ascending=[True, False, False])
    signals = signals.groupby("SignalDateTs", group_keys=False).head(top_n_per_signal_date)
    signals = signals.drop(columns=["SignalDateTs"]).reset_index(drop=True)
    return signals


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-path", default="data/cup_handle_signal_frames_2008_20260531.pkl")
    parser.add_argument("--output", default="reports/cup_handle_daily_rotation_backtest_volume_top10/cup_handle_daily_rotation_signals.csv")
    parser.add_argument("--download-start", default="2008-01-01")
    parser.add_argument("--start", default="2010-01-01")
    parser.add_argument("--end", default="2026-05-30")
    parser.add_argument("--min-score", type=float, default=45.0)
    parser.add_argument("--min-target-return-pct", type=float, default=30.0)
    parser.add_argument("--top-n-per-signal-date", type=int, default=10)
    parser.add_argument("--max-symbols", type=int, default=0)
    parser.add_argument("--scan-step", type=int, default=1)
    args = parser.parse_args()

    history = load_historical_sp500(args.download_start, args.end)
    symbols = unique_symbols(history, args.download_start, args.end)
    if args.max_symbols:
        symbols = symbols[: args.max_symbols]
    frames = load_cached_frames(Path(args.cache_path), symbols)
    calendar = pd.DatetimeIndex(sorted(set().union(*[set(frame.index) for frame in frames.values()])))
    signals = build_signal_table(
        frames,
        history,
        calendar,
        start=args.start,
        end=args.end,
        min_score=args.min_score,
        min_target_return_pct=args.min_target_return_pct,
        top_n_per_signal_date=args.top_n_per_signal_date,
        max_symbols=args.max_symbols or None,
        scan_step=args.scan_step,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    signals.to_csv(output, index=False)
    print(f"symbols={len(symbols)}")
    print(f"data_frames={len(frames)}")
    print(f"signals={len(signals)}")
    print(f"output={output}")


if __name__ == "__main__":
    main()
