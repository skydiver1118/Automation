from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_atr_exit_variants import (
    AtrExitVariant,
    add_atr,
    load_or_download_frames,
    run_backtest_atr_exit,
)
from scripts.cup_handle_rotation_backtest import benchmark_equity, markdown_table, plot_curves, summary_metrics
from scripts.cup_handle_trend_filter_variants import (
    add_indicators,
    build_entry_filter,
    download_market,
    flag_series,
    market_flag_series,
    prepare_signals,
)


def annual_return_drawdown(equity: pd.DataFrame, benchmark: pd.Series) -> pd.DataFrame:
    strategy = equity.set_index(pd.to_datetime(equity["Date"]))["Equity"].astype(float)
    bench = benchmark.reindex(strategy.index).ffill().dropna()
    strategy = strategy.reindex(bench.index).ffill()
    rows: list[dict[str, object]] = []
    for year, year_strategy in strategy.groupby(strategy.index.year):
        year_bench = bench[bench.index.year == year]
        if len(year_strategy) < 2 or len(year_bench) < 2:
            continue
        strategy_return = year_strategy.iloc[-1] / year_strategy.iloc[0] - 1.0
        benchmark_return = year_bench.iloc[-1] / year_bench.iloc[0] - 1.0
        strategy_dd = year_strategy / year_strategy.cummax() - 1.0
        benchmark_dd = year_bench / year_bench.cummax() - 1.0
        rows.append(
            {
                "Year": year,
                "StrategyReturnPct": round(strategy_return * 100.0, 2),
                "SP500ReturnPct": round(benchmark_return * 100.0, 2),
                "ExcessPct": round((strategy_return - benchmark_return) * 100.0, 2),
                "StrategyMaxDDPct": round(float(strategy_dd.min()) * 100.0, 2),
                "SP500MaxDDPct": round(float(benchmark_dd.min()) * 100.0, 2),
            }
        )
    return pd.DataFrame(rows)


def trade_by_year(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    frame = trades.copy()
    frame["EntryDate"] = pd.to_datetime(frame["EntryDate"])
    frame["Year"] = frame["EntryDate"].dt.year
    grouped = frame.groupby("Year")
    return grouped.agg(
        Trades=("Symbol", "size"),
        AvgReturnPct=("ReturnPct", "mean"),
        MedianReturnPct=("ReturnPct", "median"),
        WinRatePct=("ReturnPct", lambda values: (values > 0).mean() * 100.0),
        Stops=("ExitReason", lambda values: (values == "stop").sum()),
        AtrStops=("ExitReason", lambda values: (values == "atr_stop").sum()),
        Targets=("ExitReason", lambda values: (values == "target").sum()),
        TimeStops=("ExitReason", lambda values: (values == "time_stop").sum()),
    ).round(2).reset_index()


def exit_summary(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    grouped = trades.groupby("ExitReason")
    return grouped.agg(
        Trades=("Symbol", "size"),
        AvgReturnPct=("ReturnPct", "mean"),
        MedianReturnPct=("ReturnPct", "median"),
        WinRatePct=("ReturnPct", lambda values: (values > 0).mean() * 100.0),
    ).round(2).reset_index()


def exposure_by_year(equity: pd.DataFrame) -> pd.DataFrame:
    frame = equity.copy()
    frame["Date"] = pd.to_datetime(frame["Date"])
    frame["ExposurePct"] = frame["PositionValue"] / frame["Equity"] * 100.0
    return frame.groupby(frame["Date"].dt.year).agg(
        AvgExposurePct=("ExposurePct", "mean"),
        MedianExposurePct=("ExposurePct", "median"),
        AvgOpenPositions=("OpenPositions", "mean"),
        Days=("Date", "size"),
    ).round(2).reset_index(names="Year")


def write_report(
    output: Path,
    *,
    original_annual: pd.DataFrame,
    revised_annual: pd.DataFrame,
    original_trade_year: pd.DataFrame,
    revised_trade_year: pd.DataFrame,
    original_exit_summary: pd.DataFrame,
    revised_exit_summary: pd.DataFrame,
    original_exposure: pd.DataFrame,
    revised_exposure: pd.DataFrame,
    revised_is_metrics: dict[str, object],
    revised_oos_metrics: dict[str, object],
    benchmark_is: dict[str, object],
    benchmark_oos: dict[str, object],
) -> None:
    lines = [
        "# Cup-And-Handle OOS Diagnosis And Revised 3-Stock Rule",
        "",
        "This is technical strategy research, not investment advice.",
        "",
        "## Diagnosis",
        "",
        "- The original 3-stock IS winner did not mainly fail during the 2022 bear market; it underperformed most in bull years.",
        "- Original OOS annual underperformance was largest in 2021, 2023, 2024, and 2025.",
        "- Stop exits had poor expectancy, while time-stop exits were usually profitable. Tightening stops alone was not the fix.",
        "- The stronger fix was entry quality: require stock relative strength versus S&P 500 and use a faster market filter.",
        "",
        "## Revised Rule",
        "",
        "- Entry stock filter: `Close > SMA50` and 63-day stock return greater than S&P 500 63-day return.",
        "- Entry market filter: `S&P 500 close > SMA100`.",
        "- Exit: `ATR14 3.5x initial stop`, no measured target, 60-trading-day time stop.",
        "- Portfolio: maximum 3 concurrent stocks.",
        "",
        "## Summary",
        "",
        "| Segment | Revised Strategy Return % | S&P 500 Return % | Strategy Max DD % | Sharpe |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| IS | {revised_is_metrics.get('total_return_pct')} | {benchmark_is.get('total_return_pct')} | {revised_is_metrics.get('max_drawdown_pct')} | {revised_is_metrics.get('sharpe')} |",
        f"| OOS | {revised_oos_metrics.get('total_return_pct')} | {benchmark_oos.get('total_return_pct')} | {revised_oos_metrics.get('max_drawdown_pct')} | {revised_oos_metrics.get('sharpe')} |",
        "",
        "## Original OOS Annual Return/Drawdown",
        "",
        markdown_table(original_annual),
        "",
        "## Revised OOS Annual Return/Drawdown",
        "",
        markdown_table(revised_annual),
        "",
        "## Original OOS Trade By Year",
        "",
        markdown_table(original_trade_year),
        "",
        "## Revised OOS Trade By Year",
        "",
        markdown_table(revised_trade_year),
        "",
        "## Original OOS Exit Summary",
        "",
        markdown_table(original_exit_summary),
        "",
        "## Revised OOS Exit Summary",
        "",
        markdown_table(revised_exit_summary),
        "",
        "## Original OOS Exposure By Year",
        "",
        markdown_table(original_exposure),
        "",
        "## Revised OOS Exposure By Year",
        "",
        markdown_table(revised_exposure),
        "",
    ]
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="reports/cup_handle_revision_diagnosis")
    parser.add_argument("--signals-csv", default="reports/cup_handle_rotation_backtest/cup_handle_rotation_signals.csv")
    parser.add_argument("--cache-path", default="data/cup_handle_signal_frames_2008_20260531.pkl")
    parser.add_argument("--is-start", default="2010-01-01")
    parser.add_argument("--is-end", default="2020-01-01")
    parser.add_argument("--oos-start", default="2020-01-01")
    parser.add_argument("--end", default="2026-05-30")
    parser.add_argument("--download-start", default="2008-01-01")
    parser.add_argument("--initial-capital", type=float, default=100000.0)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    signals = prepare_signals(Path(args.signals_csv))
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
    revised_variant = AtrExitVariant(
        name="atr_3.5x_no_target_60d",
        stop_mode="atr",
        atr_mult=3.5,
        use_target=False,
        trail_mode="none",
        time_stop_days=60,
    )
    revised_is_equity, revised_is_trades = run_backtest_atr_exit(
        frames,
        signals,
        calendar,
        start=args.is_start,
        end=(pd.Timestamp(args.is_end) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
        initial_capital=args.initial_capital,
        max_positions=3,
        variant=revised_variant,
        atr_column="ATR14",
        entry_filter=entry_filter,
    )
    revised_oos_equity, revised_oos_trades = run_backtest_atr_exit(
        frames,
        signals,
        calendar,
        start=args.oos_start,
        end=args.end,
        initial_capital=args.initial_capital,
        max_positions=3,
        variant=revised_variant,
        atr_column="ATR14",
        entry_filter=entry_filter,
    )
    benchmark_is = benchmark_equity(args.is_start, args.is_end, args.initial_capital)
    benchmark_oos = benchmark_equity(args.oos_start, end_exclusive, args.initial_capital)

    original_oos_equity = pd.read_csv("reports/cup_handle_atr_exit_variants/best_is_atr_exit_oos_equity.csv")
    original_oos_trades = pd.read_csv("reports/cup_handle_atr_exit_variants/best_is_atr_exit_oos_trades.csv")

    revised_is_metrics = summary_metrics(
        revised_is_equity.set_index(pd.to_datetime(revised_is_equity["Date"]))["Equity"].astype(float),
        revised_is_trades,
    )
    revised_oos_metrics = summary_metrics(
        revised_oos_equity.set_index(pd.to_datetime(revised_oos_equity["Date"]))["Equity"].astype(float),
        revised_oos_trades,
    )
    benchmark_is_metrics = summary_metrics(benchmark_is, pd.DataFrame())
    benchmark_oos_metrics = summary_metrics(benchmark_oos, pd.DataFrame())

    original_annual = annual_return_drawdown(original_oos_equity, benchmark_oos)
    revised_annual = annual_return_drawdown(revised_oos_equity, benchmark_oos)
    original_trade_year = trade_by_year(original_oos_trades)
    revised_trade_year = trade_by_year(revised_oos_trades)
    original_exit = exit_summary(original_oos_trades)
    revised_exit = exit_summary(revised_oos_trades)
    original_exposure = exposure_by_year(original_oos_equity)
    revised_exposure = exposure_by_year(revised_oos_equity)

    revised_is_equity.to_csv(output_dir / "revised_is_equity.csv", index=False)
    revised_is_trades.to_csv(output_dir / "revised_is_trades.csv", index=False)
    revised_oos_equity.to_csv(output_dir / "revised_oos_equity.csv", index=False)
    revised_oos_trades.to_csv(output_dir / "revised_oos_trades.csv", index=False)
    original_annual.to_csv(output_dir / "original_oos_annual_return_drawdown.csv", index=False)
    revised_annual.to_csv(output_dir / "revised_oos_annual_return_drawdown.csv", index=False)
    original_trade_year.to_csv(output_dir / "original_oos_trade_by_year.csv", index=False)
    revised_trade_year.to_csv(output_dir / "revised_oos_trade_by_year.csv", index=False)
    plot_curves(revised_oos_equity, benchmark_oos, output_dir / "revised_oos_curves.png")

    write_report(
        output_dir / "cup_handle_revision_diagnosis_report.md",
        original_annual=original_annual,
        revised_annual=revised_annual,
        original_trade_year=original_trade_year,
        revised_trade_year=revised_trade_year,
        original_exit_summary=original_exit,
        revised_exit_summary=revised_exit,
        original_exposure=original_exposure,
        revised_exposure=revised_exposure,
        revised_is_metrics=revised_is_metrics,
        revised_oos_metrics=revised_oos_metrics,
        benchmark_is=benchmark_is_metrics,
        benchmark_oos=benchmark_oos_metrics,
    )

    print(f"revised_is_return={revised_is_metrics.get('total_return_pct')}")
    print(f"revised_oos_return={revised_oos_metrics.get('total_return_pct')}")
    print(f"report={output_dir / 'cup_handle_revision_diagnosis_report.md'}")


if __name__ == "__main__":
    main()
