from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_atr_exit_variants import (  # noqa: E402
    AtrExitVariant,
    add_atr,
    filter_top_candidates,
    load_or_download_frames,
    run_backtest_atr_exit,
)
from scripts.cup_handle_rotation_backtest import benchmark_equity, markdown_table, plot_curves, summary_metrics  # noqa: E402
from scripts.cup_handle_trend_filter_variants import (  # noqa: E402
    add_indicators,
    build_entry_filter,
    download_market,
    flag_series,
    market_flag_series,
    prepare_signals,
)


def trading_day(calendar: pd.DatetimeIndex, start_date: pd.Timestamp, n: int) -> pd.Timestamp | None:
    idx = calendar.searchsorted(start_date)
    target_idx = idx + n - 1
    if target_idx >= len(calendar):
        return None
    return pd.Timestamp(calendar[target_idx])


def override_expire_window(signals: pd.DataFrame, calendar: pd.DatetimeIndex, window_days: int) -> pd.DataFrame:
    frame = signals.copy()
    expire_dates: list[pd.Timestamp | None] = []
    for trade_start in pd.to_datetime(frame["TradeStartDate"]):
        expire_dates.append(trading_day(calendar, pd.Timestamp(trade_start), window_days))
    frame["ExpireTs"] = expire_dates
    frame = frame.dropna(subset=["ExpireTs"]).copy()
    frame["ExpireDate"] = pd.to_datetime(frame["ExpireTs"]).dt.strftime("%Y-%m-%d")
    return frame


def run_window(
    window_days: int,
    *,
    frames: dict[str, pd.DataFrame],
    signals: pd.DataFrame,
    calendar: pd.DatetimeIndex,
    entry_filter,
    variant: AtrExitVariant,
    is_start: str,
    is_end: str,
    oos_start: str,
    end: str,
    initial_capital: float,
    require_entry_volume: bool,
    entry_volume_min_ratio: float,
) -> tuple[dict[str, object], pd.DataFrame, pd.DataFrame]:
    window_signals = override_expire_window(signals, calendar, window_days)
    is_equity, is_trades = run_backtest_atr_exit(
        frames,
        window_signals,
        calendar,
        start=is_start,
        end=(pd.Timestamp(is_end) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
        initial_capital=initial_capital,
        max_positions=3,
        variant=variant,
        atr_column="ATR14",
        entry_filter=entry_filter,
        require_entry_volume=require_entry_volume,
        entry_volume_min_ratio=entry_volume_min_ratio,
    )
    oos_equity, oos_trades = run_backtest_atr_exit(
        frames,
        window_signals,
        calendar,
        start=oos_start,
        end=end,
        initial_capital=initial_capital,
        max_positions=3,
        variant=variant,
        atr_column="ATR14",
        entry_filter=entry_filter,
        require_entry_volume=require_entry_volume,
        entry_volume_min_ratio=entry_volume_min_ratio,
    )
    is_metrics = summary_metrics(is_equity.set_index(pd.to_datetime(is_equity["Date"]))["Equity"].astype(float), is_trades)
    oos_metrics = summary_metrics(oos_equity.set_index(pd.to_datetime(oos_equity["Date"]))["Equity"].astype(float), oos_trades)
    row = {
        "EntryWindowTradingDays": window_days,
        "Signals": len(window_signals),
        "IS_TotalReturnPct": is_metrics.get("total_return_pct"),
        "IS_CagrPct": is_metrics.get("cagr_pct"),
        "IS_MaxDrawdownPct": is_metrics.get("max_drawdown_pct"),
        "IS_Sharpe": is_metrics.get("sharpe"),
        "IS_Trades": is_metrics.get("trade_count"),
        "IS_WinRatePct": is_metrics.get("win_rate_pct"),
        "OOS_TotalReturnPct": oos_metrics.get("total_return_pct"),
        "OOS_CagrPct": oos_metrics.get("cagr_pct"),
        "OOS_MaxDrawdownPct": oos_metrics.get("max_drawdown_pct"),
        "OOS_Sharpe": oos_metrics.get("sharpe"),
        "OOS_Trades": oos_metrics.get("trade_count"),
        "OOS_WinRatePct": oos_metrics.get("win_rate_pct"),
    }
    return row, oos_equity, oos_trades


def write_report(
    output: Path,
    results: pd.DataFrame,
    benchmark_is: dict[str, object],
    benchmark_oos: dict[str, object],
    *,
    best_is: pd.Series,
    best_oos: pd.Series,
    require_entry_volume: bool,
    entry_volume_min_ratio: float,
) -> None:
    lines = [
        "# Cup-And-Handle Entry Window Test",
        "",
        "This is technical strategy research, not investment advice.",
        "",
        "## Setup",
        "",
        "- Candidate pool: top 10 weekly candidates by score, after `TargetReturnPct > 30%`.",
        "- Entry stock filter: `Close > SMA50` and stock 63-day return greater than S&P 500 63-day return.",
        "- Entry market filter: `S&P 500 close > SMA100`.",
        "- Exit: `ATR14 3.5x initial stop`, no measured target, 60-trading-day time stop.",
        "- Portfolio: maximum 3 concurrent stocks.",
        f"- Entry volume condition: `{'enabled' if require_entry_volume else 'disabled'}`"
        + (f", breakout-day volume >= {entry_volume_min_ratio:.2f}x prior 50-day average." if require_entry_volume else "."),
        "- Test variable: breakout entry window from 3 to 10 trading days after trade-start date.",
        "",
        "## Benchmarks",
        "",
        "| Segment | S&P 500 Return % | CAGR % | Max DD % | Sharpe |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| IS | {benchmark_is.get('total_return_pct')} | {benchmark_is.get('cagr_pct')} | {benchmark_is.get('max_drawdown_pct')} | {benchmark_is.get('sharpe')} |",
        f"| OOS | {benchmark_oos.get('total_return_pct')} | {benchmark_oos.get('cagr_pct')} | {benchmark_oos.get('max_drawdown_pct')} | {benchmark_oos.get('sharpe')} |",
        "",
        "## Selection",
        "",
        f"- Best by IS return: `{int(best_is['EntryWindowTradingDays'])}` trading days.",
        f"- Best IS return: `{best_is['IS_TotalReturnPct']}%`; OOS return for that same window: `{best_is['OOS_TotalReturnPct']}%`.",
        f"- Best by OOS return: `{int(best_oos['EntryWindowTradingDays'])}` trading days with OOS `{best_oos['OOS_TotalReturnPct']}%`.",
        "",
        "## Results",
        "",
        markdown_table(results),
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--signals-csv", default="reports/cup_handle_rotation_backtest/cup_handle_rotation_signals.csv")
    parser.add_argument("--output-dir", default="reports/cup_handle_entry_window_test")
    parser.add_argument("--cache-path", default="data/cup_handle_signal_frames_2008_20260531.pkl")
    parser.add_argument("--download-start", default="2008-01-01")
    parser.add_argument("--end", default="2026-05-30")
    parser.add_argument("--is-start", default="2010-01-01")
    parser.add_argument("--is-end", default="2020-01-01")
    parser.add_argument("--oos-start", default="2020-01-01")
    parser.add_argument("--initial-capital", type=float, default=100000.0)
    parser.add_argument("--require-entry-volume", action="store_true")
    parser.add_argument("--entry-volume-min-ratio", type=float, default=1.4)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    signals = prepare_signals(Path(args.signals_csv))
    signals = filter_top_candidates(signals, 10, 30.0)
    symbols = sorted(signals["Symbol"].unique())
    end_exclusive = (pd.Timestamp(args.end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    frames = load_or_download_frames(symbols, args.download_start, end_exclusive, Path(args.cache_path), 60, 0.25)
    add_indicators(frames)
    add_atr(frames)
    calendar = pd.DatetimeIndex(sorted(set().union(*[set(frame.index) for frame in frames.values()])))
    market = download_market(args.download_start, end_exclusive)
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
    benchmark_is_series = benchmark_equity(args.is_start, args.is_end, args.initial_capital)
    benchmark_oos_series = benchmark_equity(args.oos_start, end_exclusive, args.initial_capital)
    benchmark_is = summary_metrics(benchmark_is_series, pd.DataFrame())
    benchmark_oos = summary_metrics(benchmark_oos_series, pd.DataFrame())

    rows: list[dict[str, object]] = []
    oos_equities: dict[int, pd.DataFrame] = {}
    oos_trades: dict[int, pd.DataFrame] = {}
    for window_days in range(3, 11):
        print(f"Testing entry window {window_days} trading days", flush=True)
        row, oos_equity, oos_trade = run_window(
            window_days,
            frames=frames,
            signals=signals,
            calendar=calendar,
            entry_filter=entry_filter,
            variant=variant,
            is_start=args.is_start,
            is_end=args.is_end,
            oos_start=args.oos_start,
            end=args.end,
            initial_capital=args.initial_capital,
            require_entry_volume=args.require_entry_volume,
            entry_volume_min_ratio=args.entry_volume_min_ratio,
        )
        rows.append(row)
        oos_equities[window_days] = oos_equity
        oos_trades[window_days] = oos_trade

    results = pd.DataFrame(rows)
    results.to_csv(output_dir / "entry_window_results.csv", index=False)
    best_is = results.sort_values(["IS_TotalReturnPct", "IS_Sharpe"], ascending=[False, False]).iloc[0]
    best_oos = results.sort_values(["OOS_TotalReturnPct", "OOS_Sharpe"], ascending=[False, False]).iloc[0]
    best_window = int(best_is["EntryWindowTradingDays"])
    oos_equities[best_window].to_csv(output_dir / "best_is_window_oos_equity.csv", index=False)
    oos_trades[best_window].to_csv(output_dir / "best_is_window_oos_trades.csv", index=False)
    plot_curves(oos_equities[best_window], benchmark_oos_series, output_dir / "best_is_window_oos_curves.png")
    write_report(
        output_dir / "entry_window_test_report.md",
        results,
        benchmark_is,
        benchmark_oos,
        best_is=best_is,
        best_oos=best_oos,
        require_entry_volume=args.require_entry_volume,
        entry_volume_min_ratio=args.entry_volume_min_ratio,
    )
    print(f"best_is_window={best_window}")
    print(f"best_is_return={best_is['IS_TotalReturnPct']}")
    print(f"best_is_oos_return={best_is['OOS_TotalReturnPct']}")
    print(f"best_oos_window={int(best_oos['EntryWindowTradingDays'])}")
    print(f"best_oos_return={best_oos['OOS_TotalReturnPct']}")
    print(f"report={output_dir / 'entry_window_test_report.md'}")


if __name__ == "__main__":
    main()
