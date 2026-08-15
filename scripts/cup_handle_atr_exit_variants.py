from __future__ import annotations

import argparse
import pickle
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_detection import PatternCandidate  # noqa: E402
from scripts.cup_handle_rotation_backtest import (  # noqa: E402
    WatchCandidate,
    benchmark_equity,
    choose_candidates_for_day,
    download_daily,
    entry_volume_pass,
    markdown_table,
    mark_position,
    plot_curves,
    summary_metrics,
)
from scripts.cup_handle_trend_filter_variants import (  # noqa: E402
    add_indicators,
    build_entry_filter,
    download_market,
    flag_series,
    market_flag_series,
    prepare_signals,
)


def filter_top_candidates(signals: pd.DataFrame, top_n: int, min_target_return_pct: float) -> pd.DataFrame:
    filtered = signals[signals["TargetReturnPct"].astype(float) > min_target_return_pct].copy()
    if top_n <= 0 or filtered.empty:
        return filtered.reset_index(drop=True)
    filtered = filtered.sort_values(["SignalDateTs", "Score", "TargetReturnPct"], ascending=[True, False, False])
    filtered = filtered.groupby("SignalDateTs", group_keys=False).head(top_n)
    return filtered.sort_values(["SignalDateTs", "Score"], ascending=[True, False]).reset_index(drop=True)


@dataclass
class AtrExitVariant:
    name: str
    stop_mode: str
    atr_mult: float
    use_target: bool
    trail_mode: str
    time_stop_days: int


@dataclass
class AtrPosition:
    symbol: str
    entry_date: pd.Timestamp
    entry_price: float
    shares: float
    target: float
    stop: float
    score: float
    signal_date: pd.Timestamp
    breakout_level: float
    max_exit_date: pd.Timestamp
    atr_mult: float
    trail_mode: str
    use_target: bool
    highest_high: float


def true_range(frame: pd.DataFrame) -> pd.Series:
    prev_close = frame["Close"].shift(1)
    ranges = pd.concat(
        [
            frame["High"] - frame["Low"],
            (frame["High"] - prev_close).abs(),
            (frame["Low"] - prev_close).abs(),
        ],
        axis=1,
    )
    return ranges.max(axis=1)


def add_atr(frames: dict[str, pd.DataFrame], lengths: tuple[int, ...] = (14, 20)) -> None:
    for frame in frames.values():
        tr = true_range(frame)
        for length in lengths:
            frame[f"ATR{length}"] = tr.rolling(length).mean()


def load_or_download_frames(
    symbols: list[str],
    start: str,
    end: str,
    cache_path: Path,
    batch_size: int,
    pause_seconds: float,
) -> dict[str, pd.DataFrame]:
    if cache_path.exists():
        with cache_path.open("rb") as fh:
            frames = pickle.load(fh)
        allowed = set(symbols)
        return {symbol: frame for symbol, frame in frames.items() if symbol in allowed}
    frames = download_daily(symbols, start, end, batch_size, pause_seconds)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with cache_path.open("wb") as fh:
        pickle.dump(frames, fh, protocol=pickle.HIGHEST_PROTOCOL)
    return frames


def trading_day(calendar: pd.DatetimeIndex, start_date: pd.Timestamp, n: int) -> pd.Timestamp | None:
    idx = calendar.searchsorted(start_date)
    target_idx = idx + n - 1
    if target_idx >= len(calendar):
        return None
    return pd.Timestamp(calendar[target_idx])


def entry_atr(frame: pd.DataFrame, day: pd.Timestamp, atr_column: str) -> float | None:
    if day not in frame.index or atr_column not in frame.columns:
        return None
    value = float(frame.loc[day, atr_column])
    if not np.isfinite(value) or value <= 0:
        return None
    return value


def variant_stop(candidate: PatternCandidate, breakout: float, atr_value: float, variant: AtrExitVariant) -> float:
    atr_stop = breakout - variant.atr_mult * atr_value
    if variant.stop_mode == "handle":
        return candidate.handle_low_price
    if variant.stop_mode == "atr":
        return atr_stop
    if variant.stop_mode == "tighter":
        return max(candidate.handle_low_price, atr_stop)
    if variant.stop_mode == "wider":
        return min(candidate.handle_low_price, atr_stop)
    raise ValueError(f"Unknown stop_mode: {variant.stop_mode}")


def update_trailing_stop(pos: AtrPosition, row: pd.Series, atr_value: float) -> float:
    if pos.trail_mode == "none":
        return pos.stop
    pos.highest_high = max(pos.highest_high, float(row["High"]))
    trail = pos.highest_high - pos.atr_mult * atr_value
    if pos.trail_mode == "atr_trail":
        return max(pos.stop, trail)
    raise ValueError(f"Unknown trail_mode: {pos.trail_mode}")


def run_backtest_atr_exit(
    frames: dict[str, pd.DataFrame],
    signals: pd.DataFrame,
    calendar: pd.DatetimeIndex,
    *,
    start: str,
    end: str,
    initial_capital: float,
    max_positions: int,
    variant: AtrExitVariant,
    atr_column: str,
    entry_filter,
    require_entry_volume: bool = False,
    entry_volume_min_ratio: float = 1.4,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    cash = initial_capital
    positions: list[AtrPosition] = []
    watches: list[WatchCandidate] = []
    consumed_signal_keys: set[tuple[str, str]] = set()
    trades: list[dict[str, object]] = []
    equity_rows: list[dict[str, object]] = []
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    days = [pd.Timestamp(day) for day in calendar if start_ts <= day <= end_ts]

    for day in days:
        watches = [watch for watch in watches if watch.expire_date >= day]

        survivors: list[AtrPosition] = []
        for pos in positions:
            frame = frames.get(pos.symbol)
            if frame is None or day not in frame.index:
                survivors.append(pos)
                continue
            row = frame.loc[day]
            atr_value = entry_atr(frame, day, atr_column)
            if atr_value is None:
                atr_value = max((pos.entry_price - pos.stop) / max(pos.atr_mult, 1e-9), 0.01)
            effective_stop = update_trailing_stop(pos, row, atr_value)
            exit_price = None
            exit_reason = None
            if float(row["Low"]) <= effective_stop:
                exit_price = effective_stop
                exit_reason = "atr_stop" if pos.trail_mode != "none" else "stop"
            elif pos.use_target and float(row["High"]) >= pos.target:
                exit_price = pos.target
                exit_reason = "target"
            elif day >= pos.max_exit_date:
                exit_price = float(row["Close"])
                exit_reason = "time_stop"

            if exit_price is None:
                pos.stop = effective_stop
                survivors.append(pos)
                continue

            proceeds = pos.shares * exit_price
            cash += proceeds
            trades.append(
                {
                    "Symbol": pos.symbol,
                    "SignalDate": pos.signal_date.strftime("%Y-%m-%d"),
                    "EntryDate": pos.entry_date.strftime("%Y-%m-%d"),
                    "ExitDate": day.strftime("%Y-%m-%d"),
                    "EntryPrice": round(pos.entry_price, 4),
                    "ExitPrice": round(exit_price, 4),
                    "Shares": round(pos.shares, 6),
                    "PnL": round(proceeds - pos.shares * pos.entry_price, 2),
                    "ReturnPct": round((exit_price / pos.entry_price - 1.0) * 100.0, 2),
                    "ExitReason": exit_reason,
                    "Score": pos.score,
                    "BreakoutLevel": pos.breakout_level,
                    "Target": pos.target,
                    "Stop": round(effective_stop, 4),
                    "HoldingDays": int((day - pos.entry_date).days),
                }
            )
        positions = survivors

        excluded = {pos.symbol for pos in positions} | {watch.symbol for watch in watches}
        needed = max_positions - len(positions) - len(watches)
        watches.extend(choose_candidates_for_day(signals, day, excluded, consumed_signal_keys, needed))

        remaining_watches: list[WatchCandidate] = []
        for watch in watches:
            if len(positions) >= max_positions:
                remaining_watches.append(watch)
                continue
            frame = frames.get(watch.symbol)
            if frame is None or day not in frame.index:
                remaining_watches.append(watch)
                continue
            row = frame.loc[day]
            breakout = watch.candidate.breakout_level
            if float(row["High"]) < breakout:
                remaining_watches.append(watch)
                continue
            if not entry_filter(watch.symbol, day):
                remaining_watches.append(watch)
                continue
            if require_entry_volume and not entry_volume_pass(frame, day, entry_volume_min_ratio):
                remaining_watches.append(watch)
                continue
            atr_value = entry_atr(frame, day, atr_column)
            if atr_value is None:
                remaining_watches.append(watch)
                continue
            slot_value = (cash + sum(mark_position(pos, frames, day) for pos in positions)) / max_positions
            spend = min(cash, slot_value)
            if spend <= 0:
                remaining_watches.append(watch)
                continue
            initial_stop = variant_stop(watch.candidate, breakout, atr_value, variant)
            if initial_stop >= breakout:
                initial_stop = breakout - variant.atr_mult * atr_value
            shares = spend / breakout
            cash -= spend
            max_exit_date = trading_day(calendar, day, variant.time_stop_days) or end_ts
            consumed_signal_keys.add((watch.symbol, watch.signal_date.strftime("%Y-%m-%d")))
            positions.append(
                AtrPosition(
                    symbol=watch.symbol,
                    entry_date=day,
                    entry_price=breakout,
                    shares=shares,
                    target=watch.candidate.projected_target,
                    stop=initial_stop,
                    score=watch.candidate.score,
                    signal_date=watch.signal_date,
                    breakout_level=breakout,
                    max_exit_date=max_exit_date,
                    atr_mult=variant.atr_mult,
                    trail_mode=variant.trail_mode,
                    use_target=variant.use_target,
                    highest_high=float(row["High"]),
                )
            )
        watches = remaining_watches

        position_value = sum(mark_position(pos, frames, day) for pos in positions)
        equity_rows.append(
            {
                "Date": day.strftime("%Y-%m-%d"),
                "Equity": cash + position_value,
                "Cash": cash,
                "PositionValue": position_value,
                "OpenPositions": len(positions),
                "OpenWatches": len(watches),
            }
        )

    return pd.DataFrame(equity_rows), pd.DataFrame(trades)


def metric_row(variant: AtrExitVariant, metrics: dict[str, object], suffix: str = "") -> dict[str, object]:
    return {
        f"Variant{suffix}": variant.name,
        f"StopMode{suffix}": variant.stop_mode,
        f"AtrMult{suffix}": variant.atr_mult,
        f"UseTarget{suffix}": variant.use_target,
        f"TrailMode{suffix}": variant.trail_mode,
        f"TimeStopDays{suffix}": variant.time_stop_days,
        f"TotalReturnPct{suffix}": metrics.get("total_return_pct", np.nan),
        f"CagrPct{suffix}": metrics.get("cagr_pct", np.nan),
        f"MaxDrawdownPct{suffix}": metrics.get("max_drawdown_pct", np.nan),
        f"Sharpe{suffix}": metrics.get("sharpe", np.nan),
        f"Trades{suffix}": metrics.get("trade_count", 0),
        f"WinRatePct{suffix}": metrics.get("win_rate_pct", np.nan),
    }


def build_variants() -> list[AtrExitVariant]:
    variants: list[AtrExitVariant] = []
    for stop_mode in ("atr", "tighter", "wider"):
        for atr_mult in (1.5, 2.0, 2.5, 3.0, 3.5):
            for use_target in (True, False):
                variants.append(
                    AtrExitVariant(
                        name=f"{stop_mode}_{atr_mult:g}x_{'target' if use_target else 'no_target'}_60d",
                        stop_mode=stop_mode,
                        atr_mult=atr_mult,
                        use_target=use_target,
                        trail_mode="none",
                        time_stop_days=60,
                    )
                )
                variants.append(
                    AtrExitVariant(
                        name=f"{stop_mode}_{atr_mult:g}x_atrtrail_{'target' if use_target else 'no_target'}_60d",
                        stop_mode=stop_mode,
                        atr_mult=atr_mult,
                        use_target=use_target,
                        trail_mode="atr_trail",
                        time_stop_days=60,
                    )
                )
    for atr_mult in (2.0, 3.0):
        variants.append(
            AtrExitVariant(
                name=f"handle_{atr_mult:g}x_atrtrail_target_60d",
                stop_mode="handle",
                atr_mult=atr_mult,
                use_target=True,
                trail_mode="atr_trail",
                time_stop_days=60,
            )
        )
    return variants


def write_report(
    output: Path,
    rankings: pd.DataFrame,
    best: pd.Series,
    benchmark_is: dict[str, object],
    benchmark_oos: dict[str, object],
    *,
    entry_stock_condition: str,
    entry_market_condition: str,
    signals_count: int,
    symbols_count: int,
    require_entry_volume: bool,
    entry_volume_min_ratio: float,
) -> None:
    top_cols = [
        "Variant",
        "TotalReturnPct_IS",
        "CagrPct_IS",
        "MaxDrawdownPct_IS",
        "Sharpe_IS",
        "Trades_IS",
        "TotalReturnPct_OOS",
        "CagrPct_OOS",
        "MaxDrawdownPct_OOS",
        "Sharpe_OOS",
        "Trades_OOS",
    ]
    top_is = rankings.head(15)[top_cols].copy()
    top_oos = rankings.sort_values("TotalReturnPct_OOS", ascending=False).head(10)[top_cols].copy()
    lines = [
        "# Cup-And-Handle ATR Exit Variant Search",
        "",
        "This is technical strategy research, not investment advice.",
        "",
        "## Setup",
        "",
        f"- Saved cup-and-handle signals tested: `{signals_count}`",
        f"- Symbols with usable cached data: `{symbols_count}`",
        f"- Entry stock condition: `{entry_stock_condition}`",
        f"- Entry market condition: `{entry_market_condition}`",
        f"- Entry volume condition: `{'enabled' if require_entry_volume else 'disabled'}`"
        + (f", breakout-day volume >= {entry_volume_min_ratio:.2f}x prior 50-day average." if require_entry_volume else "."),
        "- Exit variants tested: initial ATR stops, handle/ATR tighter or wider stops, ATR trailing stops, target on/off.",
        "- Selection rule: rank by IS total return; evaluate the IS winner OOS.",
        "",
        "## Benchmark",
        "",
        "| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| S&P 500 IS | {benchmark_is.get('total_return_pct')} | {benchmark_is.get('cagr_pct')} | {benchmark_is.get('max_drawdown_pct')} | {benchmark_is.get('sharpe')} |",
        f"| S&P 500 OOS | {benchmark_oos.get('total_return_pct')} | {benchmark_oos.get('cagr_pct')} | {benchmark_oos.get('max_drawdown_pct')} | {benchmark_oos.get('sharpe')} |",
        "",
        "## Selected IS Winner",
        "",
        f"- Variant: `{best['Variant']}`",
        f"- IS return: `{best['TotalReturnPct_IS']}%` versus S&P 500 `{benchmark_is.get('total_return_pct')}%`",
        f"- OOS return: `{best['TotalReturnPct_OOS']}%` versus S&P 500 `{benchmark_oos.get('total_return_pct')}%`",
        f"- OOS max drawdown: `{best['MaxDrawdownPct_OOS']}%`",
        f"- ATR variants beating S&P 500 IS: `{int(rankings['BeatsSP500_IS'].sum())}`",
        f"- ATR variants beating S&P 500 OOS: `{int((rankings['TotalReturnPct_OOS'] > benchmark_oos.get('total_return_pct', np.inf)).sum())}`",
        "",
        "## Top 15 By IS Return",
        "",
        markdown_table(top_is),
        "",
        "## Top 10 By OOS Return",
        "",
        markdown_table(top_oos),
        "",
    ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--signals-csv", default="reports/cup_handle_rotation_backtest/cup_handle_rotation_signals.csv")
    parser.add_argument("--output-dir", default="reports/cup_handle_atr_exit_variants")
    parser.add_argument("--cache-path", default="data/cup_handle_signal_frames_2008_20260531.pkl")
    parser.add_argument("--download-start", default="2008-01-01")
    parser.add_argument("--end", default="2026-05-30")
    parser.add_argument("--is-start", default="2010-01-01")
    parser.add_argument("--is-end", default="2020-01-01")
    parser.add_argument("--oos-start", default="2020-01-01")
    parser.add_argument("--initial-capital", type=float, default=100000.0)
    parser.add_argument("--max-positions", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=60)
    parser.add_argument("--pause-seconds", type=float, default=0.25)
    parser.add_argument("--entry-stock-condition", default="stock_close_gt_sma200_sma200_rising")
    parser.add_argument("--entry-market-condition", default="market_spx_close_gt_sma200_sma200_rising")
    parser.add_argument("--top-n-per-signal-date", type=int, default=0)
    parser.add_argument("--min-target-return-pct", type=float, default=30.0)
    parser.add_argument("--require-entry-volume", action="store_true")
    parser.add_argument("--entry-volume-min-ratio", type=float, default=1.4)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    signals = prepare_signals(Path(args.signals_csv))
    signals = filter_top_candidates(signals, args.top_n_per_signal_date, args.min_target_return_pct)
    symbols = sorted(signals["Symbol"].unique())
    end_exclusive = (pd.Timestamp(args.end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    frames = load_or_download_frames(
        symbols,
        args.download_start,
        end_exclusive,
        Path(args.cache_path),
        args.batch_size,
        args.pause_seconds,
    )
    add_indicators(frames)
    add_atr(frames)
    calendar = pd.DatetimeIndex(sorted(set().union(*[set(frame.index) for frame in frames.values()])))
    market = download_market(args.download_start, end_exclusive)
    market_flags = market_flag_series(market, args.entry_market_condition)
    stock_flags = {symbol: flag_series(frame, args.entry_stock_condition, market) for symbol, frame in frames.items()}
    entry_filter = build_entry_filter(stock_flags, market_flags)

    benchmark_is_series = benchmark_equity(args.is_start, args.is_end, args.initial_capital)
    benchmark_oos_series = benchmark_equity(args.oos_start, end_exclusive, args.initial_capital)
    benchmark_is = summary_metrics(benchmark_is_series, pd.DataFrame())
    benchmark_oos = summary_metrics(benchmark_oos_series, pd.DataFrame())

    variants = build_variants()
    is_rows: list[dict[str, object]] = []
    oos_rows: list[dict[str, object]] = []
    for idx, variant in enumerate(variants, start=1):
        print(f"Running ATR exit variant {idx}/{len(variants)}: {variant.name}", flush=True)
        is_equity, is_trades = run_backtest_atr_exit(
            frames,
            signals,
            calendar,
            start=args.is_start,
            end=(pd.Timestamp(args.is_end) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
            initial_capital=args.initial_capital,
            max_positions=args.max_positions,
            variant=variant,
            atr_column="ATR14",
            entry_filter=entry_filter,
            require_entry_volume=args.require_entry_volume,
            entry_volume_min_ratio=args.entry_volume_min_ratio,
        )
        is_metrics = summary_metrics(is_equity.set_index(pd.to_datetime(is_equity["Date"]))["Equity"].astype(float), is_trades)
        is_rows.append(metric_row(variant, is_metrics, "_IS"))

        oos_equity, oos_trades = run_backtest_atr_exit(
            frames,
            signals,
            calendar,
            start=args.oos_start,
            end=args.end,
            initial_capital=args.initial_capital,
            max_positions=args.max_positions,
            variant=variant,
            atr_column="ATR14",
            entry_filter=entry_filter,
            require_entry_volume=args.require_entry_volume,
            entry_volume_min_ratio=args.entry_volume_min_ratio,
        )
        oos_metrics = summary_metrics(oos_equity.set_index(pd.to_datetime(oos_equity["Date"]))["Equity"].astype(float), oos_trades)
        oos_rows.append(metric_row(variant, oos_metrics, "_OOS"))

    is_df = pd.DataFrame(is_rows).rename(columns={"Variant_IS": "Variant"})
    oos_df = pd.DataFrame(oos_rows).rename(columns={"Variant_OOS": "Variant"})
    rankings = is_df.merge(oos_df, on="Variant")
    rankings = rankings.sort_values(["TotalReturnPct_IS", "Sharpe_IS"], ascending=[False, False]).reset_index(drop=True)
    rankings["BeatsSP500_IS"] = rankings["TotalReturnPct_IS"] > benchmark_is.get("total_return_pct", np.inf)
    rankings.to_csv(output_dir / "cup_handle_atr_exit_variant_rankings.csv", index=False)

    best_row = rankings.iloc[0]
    best_variant = next(variant for variant in variants if variant.name == best_row["Variant"])
    best_oos_equity, best_oos_trades = run_backtest_atr_exit(
        frames,
        signals,
        calendar,
        start=args.oos_start,
        end=args.end,
        initial_capital=args.initial_capital,
        max_positions=args.max_positions,
        variant=best_variant,
        atr_column="ATR14",
        entry_filter=entry_filter,
        require_entry_volume=args.require_entry_volume,
        entry_volume_min_ratio=args.entry_volume_min_ratio,
    )
    best_oos_equity.to_csv(output_dir / "best_is_atr_exit_oos_equity.csv", index=False)
    best_oos_trades.to_csv(output_dir / "best_is_atr_exit_oos_trades.csv", index=False)
    plot_curves(best_oos_equity, benchmark_oos_series, output_dir / "best_is_atr_exit_oos_curves.png")
    write_report(
        output_dir / "cup_handle_atr_exit_variant_report.md",
        rankings,
        best_row,
        benchmark_is,
        benchmark_oos,
        entry_stock_condition=args.entry_stock_condition,
        entry_market_condition=args.entry_market_condition,
        signals_count=len(signals),
        symbols_count=len(frames),
        require_entry_volume=args.require_entry_volume,
        entry_volume_min_ratio=args.entry_volume_min_ratio,
    )

    print(f"variants={len(rankings)}")
    print(f"is_sp500_return={benchmark_is.get('total_return_pct')}")
    print(f"best_variant={best_row['Variant']}")
    print(f"best_is_return={best_row['TotalReturnPct_IS']}")
    print(f"best_oos_return={best_row['TotalReturnPct_OOS']}")
    print(f"report={output_dir / 'cup_handle_atr_exit_variant_report.md'}")


if __name__ == "__main__":
    main()
