from __future__ import annotations

from pathlib import Path
import sys

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
from scripts.cup_handle_entry_window_test import override_expire_window  # noqa: E402
from scripts.cup_handle_rotation_backtest import benchmark_equity, markdown_table, summary_metrics  # noqa: E402
from scripts.cup_handle_trend_filter_variants import (  # noqa: E402
    add_indicators,
    build_entry_filter,
    download_market,
    flag_series,
    market_flag_series,
    prepare_signals,
)


IS_START = "2010-01-01"
IS_END = "2020-01-01"
OOS_START = "2020-01-01"
END = "2026-05-30"
END_EXCLUSIVE = "2026-05-31"
INITIAL_CAPITAL = 100000.0


def annual_return_drawdown(
    equity: pd.DataFrame,
    trades: pd.DataFrame,
    segment: str,
    benchmark: pd.Series,
) -> pd.DataFrame:
    series = equity.set_index(pd.to_datetime(equity["Date"]))["Equity"].astype(float)
    rows: list[dict[str, object]] = []
    trade_year = pd.Series(dtype=int)
    if not trades.empty:
        trade_year = pd.to_datetime(trades["EntryDate"]).dt.year
    for year, values in series.groupby(series.index.year):
        if values.empty:
            continue
        annual_return = values.iloc[-1] / values.iloc[0] - 1.0
        drawdown = values / values.cummax() - 1.0
        year_trades = trades[trade_year == year] if not trades.empty else trades
        bench_values = benchmark[benchmark.index.year == year]
        if not bench_values.empty:
            bench_return = bench_values.iloc[-1] / bench_values.iloc[0] - 1.0
            bench_drawdown = bench_values / bench_values.cummax() - 1.0
            sp500_return_pct = round(float(bench_return) * 100.0, 2)
            sp500_drawdown_pct = round(float(bench_drawdown.min()) * 100.0, 2)
        else:
            sp500_return_pct = 0.0
            sp500_drawdown_pct = 0.0
        rows.append(
            {
                "Segment": segment,
                "Year": int(year),
                "StartDate": values.index[0].strftime("%Y-%m-%d"),
                "EndDate": values.index[-1].strftime("%Y-%m-%d"),
                "AnnualReturnPct": round(annual_return * 100.0, 2),
                "MaxDrawdownPct": round(float(drawdown.min()) * 100.0, 2),
                "SP500AnnualReturnPct": sp500_return_pct,
                "SP500MaxDrawdownPct": sp500_drawdown_pct,
                "Trades": int(len(year_trades)),
                "WinRatePct": round(float((year_trades["PnL"] > 0).mean()) * 100.0, 2) if not year_trades.empty else 0.0,
                "AvgTradeReturnPct": round(float(year_trades["ReturnPct"].mean()), 2) if not year_trades.empty else 0.0,
            }
        )
    return pd.DataFrame(rows)


def run_segment(
    segment: str,
    start: str,
    end: str,
    frames: dict[str, pd.DataFrame],
    signals: pd.DataFrame,
    calendar: pd.DatetimeIndex,
    entry_filter,
    variant: AtrExitVariant,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, object], pd.Series, dict[str, object]]:
    equity, trades = run_backtest_atr_exit(
        frames,
        signals,
        calendar,
        start=start,
        end=end,
        initial_capital=INITIAL_CAPITAL,
        max_positions=3,
        variant=variant,
        atr_column="ATR14",
        entry_filter=entry_filter,
        require_entry_volume=True,
        entry_volume_min_ratio=1.4,
    )
    equity_series = equity.set_index(pd.to_datetime(equity["Date"]))["Equity"].astype(float)
    metrics = summary_metrics(equity_series, trades)
    benchmark = benchmark_equity(start, (pd.Timestamp(end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d"), INITIAL_CAPITAL)
    benchmark_metrics = summary_metrics(benchmark, pd.DataFrame())
    print(f"{segment}_return={metrics.get('total_return_pct')}")
    print(f"{segment}_sharpe={metrics.get('sharpe')}")
    print(f"{segment}_trades={metrics.get('trade_count')}")
    return equity, trades, metrics, benchmark, benchmark_metrics


def main() -> None:
    output_dir = Path("reports/cup_handle_daily_volume_annual_breakdown")
    output_dir.mkdir(parents=True, exist_ok=True)

    signals = prepare_signals(Path("reports/cup_handle_daily_rotation_backtest_volume_top10/cup_handle_daily_rotation_signals.csv"))
    signals = filter_top_candidates(signals, 10, 30.0)
    symbols = sorted(signals["Symbol"].unique())
    frames = load_or_download_frames(
        symbols,
        "2008-01-01",
        END_EXCLUSIVE,
        Path("data/cup_handle_signal_frames_2008_20260531.pkl"),
        60,
        0.0,
    )
    add_indicators(frames)
    add_atr(frames)
    calendar = pd.DatetimeIndex(sorted(set().union(*[set(frame.index) for frame in frames.values()])))
    window_signals = override_expire_window(signals, calendar, 7)

    market = download_market("2008-01-01", END_EXCLUSIVE)
    stock_flags = {symbol: flag_series(frame, "stock_close_gt_sma50_rs63_gt_spx", market) for symbol, frame in frames.items()}
    market_flags = market_flag_series(market, "market_spx_close_gt_sma100")
    entry_filter = build_entry_filter(stock_flags, market_flags)
    variant = AtrExitVariant(
        name="atr_3.5x_no_target_60d_entry_window_7d",
        stop_mode="atr",
        atr_mult=3.5,
        use_target=False,
        trail_mode="none",
        time_stop_days=60,
    )

    is_equity, is_trades, is_metrics, is_benchmark_series, is_benchmark = run_segment(
        "IS",
        IS_START,
        (pd.Timestamp(IS_END) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
        frames,
        window_signals,
        calendar,
        entry_filter,
        variant,
    )
    oos_equity, oos_trades, oos_metrics, oos_benchmark_series, oos_benchmark = run_segment(
        "OOS",
        OOS_START,
        END,
        frames,
        window_signals,
        calendar,
        entry_filter,
        variant,
    )

    is_equity.to_csv(output_dir / "daily_entry7_is_equity.csv", index=False)
    is_trades.to_csv(output_dir / "daily_entry7_is_trades.csv", index=False)
    oos_equity.to_csv(output_dir / "daily_entry7_oos_equity.csv", index=False)
    oos_trades.to_csv(output_dir / "daily_entry7_oos_trades.csv", index=False)

    annual = pd.concat(
        [
            annual_return_drawdown(is_equity, is_trades, "IS", is_benchmark_series),
            annual_return_drawdown(oos_equity, oos_trades, "OOS", oos_benchmark_series),
        ],
        ignore_index=True,
    )
    annual.to_csv(output_dir / "daily_entry7_annual_return_drawdown_trades.csv", index=False)

    lines = [
        "# Daily Cup-And-Handle Entry-Window 7 Annual Breakdown",
        "",
        "This is technical strategy research, not investment advice.",
        "",
        "## Rule",
        "",
        "- Daily cup-and-handle signals with volume gates.",
        "- Candidate pool: top 10 per scan date, `TargetReturnPct > 30%`.",
        "- Entry window: `7 trading days`.",
        "- Entry filters: `Close > SMA50`, stock 63-day return > S&P 500 63-day return, and `S&P 500 close > SMA100`.",
        "- Entry volume: breakout-day volume >= `1.40x` prior 50-day average.",
        "- Exit: ATR14 `3.5x` initial stop, no target, 60-trading-day time stop.",
        "- Portfolio: max 3 concurrent stocks.",
        "",
        "## Segment Summary",
        "",
        "| Segment | Strategy Return % | Strategy Sharpe | Strategy Max DD % | Trades | S&P 500 Return % | S&P 500 Sharpe |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        f"| IS | {is_metrics.get('total_return_pct')} | {is_metrics.get('sharpe')} | {is_metrics.get('max_drawdown_pct')} | {is_metrics.get('trade_count')} | {is_benchmark.get('total_return_pct')} | {is_benchmark.get('sharpe')} |",
        f"| OOS | {oos_metrics.get('total_return_pct')} | {oos_metrics.get('sharpe')} | {oos_metrics.get('max_drawdown_pct')} | {oos_metrics.get('trade_count')} | {oos_benchmark.get('total_return_pct')} | {oos_benchmark.get('sharpe')} |",
        "",
        "## Annual Return, Drawdown, Trades",
        "",
        markdown_table(annual),
        "",
    ]
    (output_dir / "daily_entry7_annual_breakdown.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"annual={output_dir / 'daily_entry7_annual_return_drawdown_trades.csv'}")
    print(f"report={output_dir / 'daily_entry7_annual_breakdown.md'}")


if __name__ == "__main__":
    main()
