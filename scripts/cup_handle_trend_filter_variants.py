from __future__ import annotations

import argparse
import pickle
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_rotation_backtest import (  # noqa: E402
    benchmark_equity,
    download_daily,
    markdown_table,
    plot_curves,
    run_backtest,
    summary_metrics,
)


def prepare_signals(path: Path) -> pd.DataFrame:
    signals = pd.read_csv(path)
    signals["SignalDateTs"] = pd.to_datetime(signals["SignalDate"])
    signals["TradeStartTs"] = pd.to_datetime(signals["TradeStartDate"])
    signals["ExpireTs"] = pd.to_datetime(signals["ExpireDate"])
    return signals


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
        return {symbol: frame for symbol, frame in frames.items() if symbol in set(symbols)}
    frames = download_daily(symbols, start, end, batch_size, pause_seconds)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with cache_path.open("wb") as fh:
        pickle.dump(frames, fh, protocol=pickle.HIGHEST_PROTOCOL)
    return frames


def add_indicators(frames: dict[str, pd.DataFrame]) -> None:
    for frame in frames.values():
        close = frame["Close"].astype(float)
        for length in (20, 50, 100, 150, 200):
            frame[f"SMA{length}"] = close.rolling(length).mean()
        frame["SMA50_RISING_20D"] = frame["SMA50"] > frame["SMA50"].shift(20)
        frame["SMA200_RISING_20D"] = frame["SMA200"] > frame["SMA200"].shift(20)
        frame["RET63"] = close.pct_change(63)


def download_market(start: str, end: str) -> pd.DataFrame:
    market = yf.download("^GSPC", start=start, end=end, interval="1d", auto_adjust=True, progress=False)
    if isinstance(market.columns, pd.MultiIndex):
        market.columns = [col[0] for col in market.columns]
    market = market.rename(columns=str.title).dropna()
    market.index = pd.to_datetime(market.index).tz_localize(None)
    close = market["Close"].astype(float)
    for length in (50, 100, 200):
        market[f"SMA{length}"] = close.rolling(length).mean()
    market["SMA200_RISING_20D"] = market["SMA200"] > market["SMA200"].shift(20)
    market["RET63"] = close.pct_change(63)
    return market


def flag_series(frame: pd.DataFrame, name: str, market: pd.DataFrame | None = None) -> pd.Series:
    close = frame["Close"].astype(float)
    if name == "stock_none":
        return pd.Series(True, index=frame.index)
    if name == "stock_close_gt_sma50":
        return close > frame["SMA50"]
    if name == "stock_close_gt_sma200":
        return close > frame["SMA200"]
    if name == "stock_close_gt_sma50_sma50_gt_sma200":
        return (close > frame["SMA50"]) & (frame["SMA50"] > frame["SMA200"])
    if name == "stock_close_gt_sma200_sma50_gt_sma200":
        return (close > frame["SMA200"]) & (frame["SMA50"] > frame["SMA200"])
    if name == "stock_close_gt_sma20_sma20_gt_sma50":
        return (close > frame["SMA20"]) & (frame["SMA20"] > frame["SMA50"])
    if name == "stock_close_gt_sma50_sma50_rising":
        return (close > frame["SMA50"]) & frame["SMA50_RISING_20D"]
    if name == "stock_close_gt_sma200_sma200_rising":
        return (close > frame["SMA200"]) & frame["SMA200_RISING_20D"]
    if name == "stock_close_gt_sma50_sma50_gt_sma150_gt_sma200":
        return (close > frame["SMA50"]) & (frame["SMA50"] > frame["SMA150"]) & (frame["SMA150"] > frame["SMA200"])
    if name == "stock_close_gt_sma50_rs63_gt_spx":
        if market is None:
            return pd.Series(False, index=frame.index)
        market_ret = market["RET63"].reindex(frame.index).ffill()
        return (close > frame["SMA50"]) & (frame["RET63"] > market_ret)
    raise ValueError(f"Unknown stock condition: {name}")


def market_flag_series(market: pd.DataFrame, name: str) -> pd.Series:
    close = market["Close"].astype(float)
    if name == "market_none":
        return pd.Series(True, index=market.index)
    if name == "market_spx_close_gt_sma200":
        return close > market["SMA200"]
    if name == "market_spx_sma50_gt_sma200":
        return market["SMA50"] > market["SMA200"]
    if name == "market_spx_close_gt_sma50_sma50_gt_sma200":
        return (close > market["SMA50"]) & (market["SMA50"] > market["SMA200"])
    if name == "market_spx_close_gt_sma100":
        return close > market["SMA100"]
    if name == "market_spx_sma200_rising":
        return market["SMA200_RISING_20D"]
    if name == "market_spx_close_gt_sma200_sma200_rising":
        return (close > market["SMA200"]) & market["SMA200_RISING_20D"]
    raise ValueError(f"Unknown market condition: {name}")


def build_entry_filter(
    stock_flags: dict[str, pd.Series],
    market_flags: pd.Series,
) -> callable:
    def allowed(symbol: str, day: pd.Timestamp) -> bool:
        stock = stock_flags.get(symbol)
        if stock is None or day not in stock.index or day not in market_flags.index:
            return False
        return bool(stock.loc[day]) and bool(market_flags.loc[day])

    return allowed


def metric_row(name: str, stock_condition: str, market_condition: str, metrics: dict[str, object]) -> dict[str, object]:
    return {
        "Variant": name,
        "StockCondition": stock_condition,
        "MarketCondition": market_condition,
        "TotalReturnPct": metrics.get("total_return_pct", np.nan),
        "CagrPct": metrics.get("cagr_pct", np.nan),
        "MaxDrawdownPct": metrics.get("max_drawdown_pct", np.nan),
        "Sharpe": metrics.get("sharpe", np.nan),
        "Trades": metrics.get("trade_count", 0),
        "WinRatePct": metrics.get("win_rate_pct", np.nan),
    }


def run_variant(
    frames: dict[str, pd.DataFrame],
    signals: pd.DataFrame,
    calendar: pd.DatetimeIndex,
    market_flags: pd.Series,
    stock_condition: str,
    market_condition: str,
    *,
    start: str,
    end: str,
    initial_capital: float,
    max_positions: int,
    max_hold_days: int,
    market: pd.DataFrame,
    require_entry_volume: bool = False,
    entry_volume_min_ratio: float = 1.4,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, object]]:
    stock_flags = {symbol: flag_series(frame, stock_condition, market) for symbol, frame in frames.items()}
    entry_filter = build_entry_filter(stock_flags, market_flags)
    equity, trades = run_backtest(
        frames,
        signals,
        calendar,
        start=start,
        end=end,
        initial_capital=initial_capital,
        max_positions=max_positions,
        max_hold_days=max_hold_days,
        entry_filter=entry_filter,
        require_entry_volume=require_entry_volume,
        entry_volume_min_ratio=entry_volume_min_ratio,
    )
    equity_series = equity.set_index(pd.to_datetime(equity["Date"]))["Equity"].astype(float)
    metrics = summary_metrics(equity_series, trades)
    variant_name = f"{stock_condition}__{market_condition}"
    return equity, trades, metric_row(variant_name, stock_condition, market_condition, metrics)


def write_variant_report(
    output: Path,
    rankings: pd.DataFrame,
    best_is: pd.Series,
    best_oos: pd.Series,
    benchmark_is: dict[str, object],
    benchmark_oos: dict[str, object],
    *,
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
    top = rankings.head(15)[top_cols].copy()
    top_oos = rankings.sort_values("TotalReturnPct_OOS", ascending=False).head(10)[top_cols].copy()
    oos_beats = int((rankings["TotalReturnPct_OOS"] > benchmark_oos.get("total_return_pct", np.inf)).sum())
    lines = [
        "# Cup-And-Handle Trend Filter Variant Search",
        "",
        "This is technical strategy research, not investment advice.",
        "",
        "## Summary",
        "",
        f"- Saved cup-and-handle signals tested: `{signals_count}`",
        f"- Symbols with signals/data requested: `{symbols_count}`",
        "- Variant selection rule: rank by in-sample total return only, then evaluate the selected winner out of sample.",
        "- Entry filter timing: stock and market trend conditions are checked only when the breakout buy stop is touched.",
        f"- Entry volume condition: `{'enabled' if require_entry_volume else 'disabled'}`"
        + (f", breakout-day volume >= {entry_volume_min_ratio:.2f}x prior 50-day average." if require_entry_volume else "."),
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
        f"- Variant: `{best_is['Variant']}`",
        f"- IS return: `{best_is['TotalReturnPct_IS']}%` versus S&P 500 `{benchmark_is.get('total_return_pct')}%`",
        f"- OOS return: `{best_oos['TotalReturnPct_OOS']}%` versus S&P 500 `{benchmark_oos.get('total_return_pct')}%`",
        f"- OOS max drawdown: `{best_oos['MaxDrawdownPct_OOS']}%`",
        f"- Variants beating S&P 500 OOS: `{oos_beats}`",
        "",
        "## Top 15 By IS Return",
        "",
        markdown_table(top),
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
    parser.add_argument("--output-dir", default="reports/cup_handle_trend_filter_variants")
    parser.add_argument("--cache-path", default="data/cup_handle_signal_frames_2008_20260531.pkl")
    parser.add_argument("--download-start", default="2008-01-01")
    parser.add_argument("--end", default="2026-05-30")
    parser.add_argument("--is-start", default="2010-01-01")
    parser.add_argument("--is-end", default="2020-01-01")
    parser.add_argument("--oos-start", default="2020-01-01")
    parser.add_argument("--initial-capital", type=float, default=100000.0)
    parser.add_argument("--max-positions", type=int, default=3)
    parser.add_argument("--max-hold-days", type=int, default=60)
    parser.add_argument("--batch-size", type=int, default=60)
    parser.add_argument("--pause-seconds", type=float, default=0.25)
    parser.add_argument("--require-entry-volume", action="store_true")
    parser.add_argument("--entry-volume-min-ratio", type=float, default=1.4)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    signals = prepare_signals(Path(args.signals_csv))
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
    calendar = pd.DatetimeIndex(sorted(set().union(*[set(frame.index) for frame in frames.values()])))
    market = download_market(args.download_start, end_exclusive)

    stock_conditions = [
        "stock_none",
        "stock_close_gt_sma50",
        "stock_close_gt_sma200",
        "stock_close_gt_sma50_sma50_gt_sma200",
        "stock_close_gt_sma200_sma50_gt_sma200",
        "stock_close_gt_sma20_sma20_gt_sma50",
        "stock_close_gt_sma50_sma50_rising",
        "stock_close_gt_sma200_sma200_rising",
        "stock_close_gt_sma50_sma50_gt_sma150_gt_sma200",
        "stock_close_gt_sma50_rs63_gt_spx",
    ]
    market_conditions = [
        "market_none",
        "market_spx_close_gt_sma200",
        "market_spx_sma50_gt_sma200",
        "market_spx_close_gt_sma50_sma50_gt_sma200",
        "market_spx_close_gt_sma100",
        "market_spx_sma200_rising",
        "market_spx_close_gt_sma200_sma200_rising",
    ]

    benchmark_is_series = benchmark_equity(args.is_start, args.is_end, args.initial_capital)
    benchmark_oos_series = benchmark_equity(args.oos_start, end_exclusive, args.initial_capital)
    benchmark_is = summary_metrics(benchmark_is_series, pd.DataFrame())
    benchmark_oos = summary_metrics(benchmark_oos_series, pd.DataFrame())

    is_rows: list[dict[str, object]] = []
    oos_rows: list[dict[str, object]] = []
    best_equity = pd.DataFrame()
    best_trades = pd.DataFrame()
    total_variants = len(stock_conditions) * len(market_conditions)
    current = 0
    for stock_condition in stock_conditions:
        stock_flags = {symbol: flag_series(frame, stock_condition, market) for symbol, frame in frames.items()}
        for market_condition in market_conditions:
            current += 1
            print(f"Running variant {current}/{total_variants}: {stock_condition} + {market_condition}", flush=True)
            market_flags = market_flag_series(market, market_condition)
            entry_filter = build_entry_filter(stock_flags, market_flags)
            is_equity, is_trades = run_backtest(
                frames,
                signals,
                calendar,
                start=args.is_start,
                end=(pd.Timestamp(args.is_end) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
                initial_capital=args.initial_capital,
                max_positions=args.max_positions,
                max_hold_days=args.max_hold_days,
                entry_filter=entry_filter,
                require_entry_volume=args.require_entry_volume,
                entry_volume_min_ratio=args.entry_volume_min_ratio,
            )
            is_metrics = summary_metrics(is_equity.set_index(pd.to_datetime(is_equity["Date"]))["Equity"].astype(float), is_trades)
            variant_name = f"{stock_condition}__{market_condition}"
            is_rows.append(metric_row(variant_name, stock_condition, market_condition, is_metrics))

            oos_equity, oos_trades = run_backtest(
                frames,
                signals,
                calendar,
                start=args.oos_start,
                end=args.end,
                initial_capital=args.initial_capital,
                max_positions=args.max_positions,
                max_hold_days=args.max_hold_days,
                entry_filter=entry_filter,
                require_entry_volume=args.require_entry_volume,
                entry_volume_min_ratio=args.entry_volume_min_ratio,
            )
            oos_metrics = summary_metrics(oos_equity.set_index(pd.to_datetime(oos_equity["Date"]))["Equity"].astype(float), oos_trades)
            oos_rows.append(metric_row(variant_name, stock_condition, market_condition, oos_metrics))

    is_df = pd.DataFrame(is_rows).sort_values(["TotalReturnPct", "Sharpe"], ascending=[False, False]).reset_index(drop=True)
    oos_df = pd.DataFrame(oos_rows)
    rankings = is_df.merge(oos_df, on=["Variant", "StockCondition", "MarketCondition"], suffixes=("_IS", "_OOS"))
    rankings["BeatsSP500_IS"] = rankings["TotalReturnPct_IS"] > benchmark_is.get("total_return_pct", np.inf)
    rankings.to_csv(output_dir / "cup_handle_trend_filter_variant_rankings.csv", index=False)

    best = rankings.iloc[0]
    best_stock = str(best["StockCondition"])
    best_market = str(best["MarketCondition"])
    best_stock_flags = {symbol: flag_series(frame, best_stock, market) for symbol, frame in frames.items()}
    best_market_flags = market_flag_series(market, best_market)
    best_filter = build_entry_filter(best_stock_flags, best_market_flags)
    best_equity, best_trades = run_backtest(
        frames,
        signals,
        calendar,
        start=args.oos_start,
        end=args.end,
        initial_capital=args.initial_capital,
        max_positions=args.max_positions,
        max_hold_days=args.max_hold_days,
        entry_filter=best_filter,
        require_entry_volume=args.require_entry_volume,
        entry_volume_min_ratio=args.entry_volume_min_ratio,
    )
    best_equity.to_csv(output_dir / "best_is_variant_oos_equity.csv", index=False)
    best_trades.to_csv(output_dir / "best_is_variant_oos_trades.csv", index=False)
    plot_curves(best_equity, benchmark_oos_series, output_dir / "best_is_variant_oos_curves.png")

    best_oos = rankings[rankings["Variant"] == best["Variant"]].iloc[0]
    write_variant_report(
        output_dir / "cup_handle_trend_filter_variant_report.md",
        rankings,
        best,
        best_oos,
        benchmark_is,
        benchmark_oos,
        signals_count=len(signals),
        symbols_count=len(frames),
        require_entry_volume=args.require_entry_volume,
        entry_volume_min_ratio=args.entry_volume_min_ratio,
    )

    print(f"variants={len(rankings)}")
    print(f"is_sp500_return={benchmark_is.get('total_return_pct')}")
    print(f"best_variant={best['Variant']}")
    print(f"best_is_return={best['TotalReturnPct_IS']}")
    print(f"best_oos_return={best_oos['TotalReturnPct_OOS']}")
    print(f"report={output_dir / 'cup_handle_trend_filter_variant_report.md'}")


if __name__ == "__main__":
    main()
