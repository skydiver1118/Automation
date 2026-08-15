from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_atr_exit_variants import (  # noqa: E402
    AtrExitVariant,
    add_atr,
    run_backtest_atr_exit,
)
from scripts.cup_handle_detection import local_pivots  # noqa: E402
from scripts.cup_handle_rotation_backtest import (  # noqa: E402
    benchmark_equity,
    daily_to_weekly,
    download_daily,
    find_patterns_asof,
    markdown_table,
    next_trading_day,
    plot_curves,
    summary_metrics,
)
from scripts.cup_handle_revision_diagnostics import (  # noqa: E402
    annual_return_drawdown,
    exit_summary,
    exposure_by_year,
    trade_by_year,
)
from scripts.cup_handle_trend_filter_variants import (  # noqa: E402
    add_indicators,
    build_entry_filter,
    download_market,
    flag_series,
    market_flag_series,
)


def nth_trading_day(calendar: pd.DatetimeIndex, start_date: pd.Timestamp, n: int) -> pd.Timestamp | None:
    idx = calendar.searchsorted(start_date)
    target_idx = idx + n - 1
    if target_idx >= len(calendar):
        return None
    return pd.Timestamp(calendar[target_idx])


def build_custom_signal_table(
    frames: dict[str, pd.DataFrame],
    calendar: pd.DatetimeIndex,
    *,
    start: str,
    end: str,
    entry_window_days: int,
    min_score: float,
    min_target_return_pct: float,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    scan_start = pd.Timestamp(start)
    scan_end = pd.Timestamp(end)
    for symbol, daily in frames.items():
        weekly = daily_to_weekly(daily)
        if len(weekly) < 90:
            continue
        pivot_highs, pivot_lows = local_pivots(weekly, window=2)
        for last_idx in range(75, len(weekly)):
            signal_week = pd.Timestamp(weekly.index[last_idx])
            if signal_week < scan_start or signal_week > scan_end:
                continue
            trade_start = next_trading_day(calendar, signal_week)
            if trade_start is None:
                continue
            expire_date = nth_trading_day(calendar, trade_start, entry_window_days)
            if expire_date is None:
                continue
            candidates = find_patterns_asof(
                weekly,
                last_idx,
                pivot_highs,
                pivot_lows,
                min_target_return_pct=min_target_return_pct,
                min_score=min_score,
            )
            if not candidates:
                continue
            candidate = candidates[0]
            rows.append(
                {
                    "Symbol": symbol,
                    "SignalDate": signal_week.strftime("%Y-%m-%d"),
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
                    "CandidateJson": json.dumps(asdict(candidate)),
                    "SignalDateTs": signal_week,
                    "TradeStartTs": trade_start,
                    "ExpireTs": expire_date,
                }
            )
    signals = pd.DataFrame(rows)
    if not signals.empty:
        signals = signals.sort_values(["SignalDateTs", "Score"], ascending=[True, False]).reset_index(drop=True)
    return signals


def write_report(
    output: Path,
    *,
    signals: pd.DataFrame,
    trades: pd.DataFrame,
    equity: pd.DataFrame,
    benchmark: pd.Series,
    is_metrics: dict[str, object],
    oos_metrics: dict[str, object],
    benchmark_is: dict[str, object],
    benchmark_oos: dict[str, object],
    annual: pd.DataFrame,
    trade_year: pd.DataFrame,
    exits: pd.DataFrame,
    exposure: pd.DataFrame,
    symbols: list[str],
) -> None:
    last_trades = trades.tail(20) if not trades.empty else pd.DataFrame()
    last_cols = ["Symbol", "EntryDate", "ExitDate", "EntryPrice", "ExitPrice", "ReturnPct", "ExitReason", "Score"]
    lines = [
        "# SOXL/TQQQ Cup-And-Handle Test",
        "",
        "This is technical strategy research, not investment advice.",
        "",
        "## Setup",
        "",
        f"- Universe: `{', '.join(symbols)}`",
        "- Pattern data: weekly OHLCV.",
        "- Execution data: daily OHLCV.",
        "- Candidate filter: `TargetReturnPct > 30%`.",
        "- Breakout fill window: 3 trading days.",
        "- Entry filter: `Close > SMA50`, ETF 63-day return greater than S&P 500 63-day return, and S&P 500 close > SMA100.",
        "- Exit: `ATR14 3.5x initial stop`, no measured target, 60-trading-day time stop.",
        "- Max concurrent positions: 2, because the universe has only two symbols.",
        "",
        "## Summary",
        "",
        "| Segment | Strategy Return % | S&P 500 Return % | Strategy Max DD % | Sharpe | Trades |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        f"| IS | {is_metrics.get('total_return_pct')} | {benchmark_is.get('total_return_pct')} | {is_metrics.get('max_drawdown_pct')} | {is_metrics.get('sharpe')} | {is_metrics.get('trade_count')} |",
        f"| OOS | {oos_metrics.get('total_return_pct')} | {benchmark_oos.get('total_return_pct')} | {oos_metrics.get('max_drawdown_pct')} | {oos_metrics.get('sharpe')} | {oos_metrics.get('trade_count')} |",
        "",
        "## Data Audit",
        "",
        f"- Signals generated: `{len(signals)}`",
        f"- Trades executed: `{len(trades)}`",
        "",
        "## OOS Annual Return/Drawdown",
        "",
        markdown_table(annual),
        "",
        "## OOS Trade By Year",
        "",
        markdown_table(trade_year),
        "",
        "## OOS Exit Summary",
        "",
        markdown_table(exits),
        "",
        "## OOS Exposure By Year",
        "",
        markdown_table(exposure),
        "",
        "## Last 20 Trades",
        "",
        markdown_table(last_trades[last_cols]) if not last_trades.empty else "No trades.",
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbols", default="SOXL,TQQQ")
    parser.add_argument("--output-dir", default="reports/cup_handle_soxl_tqqq_test")
    parser.add_argument("--download-start", default="2008-01-01")
    parser.add_argument("--is-start", default="2010-01-01")
    parser.add_argument("--is-end", default="2020-01-01")
    parser.add_argument("--oos-start", default="2020-01-01")
    parser.add_argument("--end", default="2026-05-30")
    parser.add_argument("--initial-capital", type=float, default=100000.0)
    parser.add_argument("--min-score", type=float, default=45.0)
    parser.add_argument("--min-target-return-pct", type=float, default=30.0)
    args = parser.parse_args()

    symbols = [symbol.strip().upper() for symbol in args.symbols.split(",") if symbol.strip()]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    end_exclusive = (pd.Timestamp(args.end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    frames = download_daily(symbols, args.download_start, end_exclusive, batch_size=len(symbols), pause_seconds=0.0)
    add_indicators(frames)
    add_atr(frames)
    calendar = pd.DatetimeIndex(sorted(set().union(*[set(frame.index) for frame in frames.values()])))
    market = download_market(args.download_start, end_exclusive)
    signals = build_custom_signal_table(
        frames,
        calendar,
        start=args.is_start,
        end=args.end,
        entry_window_days=3,
        min_score=args.min_score,
        min_target_return_pct=args.min_target_return_pct,
    )
    if signals.empty:
        raise RuntimeError("No SOXL/TQQQ cup-and-handle signals found with the configured filters.")
    stock_flags = {symbol: flag_series(frame, "stock_close_gt_sma50_rs63_gt_spx", market) for symbol, frame in frames.items()}
    market_flags = market_flag_series(market, "market_spx_close_gt_sma100")
    entry_filter = build_entry_filter(stock_flags, market_flags)
    variant = AtrExitVariant(
        name="atr_3.5x_no_target_60d",
        stop_mode="atr",
        atr_mult=3.5,
        use_target=False,
        trail_mode="none",
        time_stop_days=60,
    )
    is_equity, is_trades = run_backtest_atr_exit(
        frames,
        signals,
        calendar,
        start=args.is_start,
        end=(pd.Timestamp(args.is_end) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
        initial_capital=args.initial_capital,
        max_positions=min(2, len(symbols)),
        variant=variant,
        atr_column="ATR14",
        entry_filter=entry_filter,
    )
    oos_equity, oos_trades = run_backtest_atr_exit(
        frames,
        signals,
        calendar,
        start=args.oos_start,
        end=args.end,
        initial_capital=args.initial_capital,
        max_positions=min(2, len(symbols)),
        variant=variant,
        atr_column="ATR14",
        entry_filter=entry_filter,
    )
    benchmark_is_series = benchmark_equity(args.is_start, args.is_end, args.initial_capital)
    benchmark_oos_series = benchmark_equity(args.oos_start, end_exclusive, args.initial_capital)
    is_metrics = summary_metrics(is_equity.set_index(pd.to_datetime(is_equity["Date"]))["Equity"].astype(float), is_trades)
    oos_metrics = summary_metrics(oos_equity.set_index(pd.to_datetime(oos_equity["Date"]))["Equity"].astype(float), oos_trades)
    benchmark_is = summary_metrics(benchmark_is_series, pd.DataFrame())
    benchmark_oos = summary_metrics(benchmark_oos_series, pd.DataFrame())
    annual = annual_return_drawdown(oos_equity, benchmark_oos_series)
    trade_year = trade_by_year(oos_trades)
    exits = exit_summary(oos_trades)
    exposure = exposure_by_year(oos_equity)

    signals.to_csv(output_dir / "soxl_tqqq_cup_handle_signals.csv", index=False)
    is_equity.to_csv(output_dir / "soxl_tqqq_is_equity.csv", index=False)
    is_trades.to_csv(output_dir / "soxl_tqqq_is_trades.csv", index=False)
    oos_equity.to_csv(output_dir / "soxl_tqqq_oos_equity.csv", index=False)
    oos_trades.to_csv(output_dir / "soxl_tqqq_oos_trades.csv", index=False)
    annual.to_csv(output_dir / "soxl_tqqq_oos_annual_return_drawdown.csv", index=False)
    plot_curves(oos_equity, benchmark_oos_series, output_dir / "soxl_tqqq_oos_curves.png")
    write_report(
        output_dir / "soxl_tqqq_cup_handle_report.md",
        signals=signals,
        trades=pd.concat([is_trades, oos_trades], ignore_index=True),
        equity=oos_equity,
        benchmark=benchmark_oos_series,
        is_metrics=is_metrics,
        oos_metrics=oos_metrics,
        benchmark_is=benchmark_is,
        benchmark_oos=benchmark_oos,
        annual=annual,
        trade_year=trade_year,
        exits=exits,
        exposure=exposure,
        symbols=symbols,
    )
    print(f"signals={len(signals)}")
    print(f"is_trades={len(is_trades)}")
    print(f"oos_trades={len(oos_trades)}")
    print(f"is_return={is_metrics.get('total_return_pct')}")
    print(f"oos_return={oos_metrics.get('total_return_pct')}")
    print(f"oos_sharpe={oos_metrics.get('sharpe')}")
    print(f"report={output_dir / 'soxl_tqqq_cup_handle_report.md'}")


if __name__ == "__main__":
    main()
