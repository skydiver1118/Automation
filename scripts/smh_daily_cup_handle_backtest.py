from __future__ import annotations

import argparse
import json
import math
import pickle
import sys
import time
from dataclasses import asdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_atr_exit_variants import AtrExitVariant, add_atr, run_backtest_atr_exit  # noqa: E402
from scripts.cup_handle_daily_rotation_signals import find_daily_patterns_asof  # noqa: E402
from scripts.cup_handle_detection import local_pivots  # noqa: E402
from scripts.cup_handle_entry_window_test import override_expire_window  # noqa: E402
from scripts.cup_handle_rotation_backtest import markdown_table, normalize_download_frame, nth_trading_day, summary_metrics  # noqa: E402
from src.strategy_lab.smh_historical_components_momentum_is_oos import (  # noqa: E402
    HOLDINGS_PATH,
    load_historical_holdings,
    latest_known_snapshot,
    snapshot_tickers_by_public_date,
)


IS_START = "2010-01-01"
IS_END = "2020-01-01"
OOS_START = "2020-01-01"
OOS_END = "2026-05-30"
PRICE_START = "2008-12-01"
OUTPUT_DIR = Path("reports/smh_daily_cup_handle")
CACHE_PATH = Path("data/smh_components/historical_smh_daily_ohlcv_2008-12-01_2026-05-30.pkl")


def load_or_download_ohlcv(symbols: list[str], start: str, end: str, cache_path: Path, batch_size: int = 30) -> dict[str, pd.DataFrame]:
    if cache_path.exists():
        with cache_path.open("rb") as fh:
            cached = pickle.load(fh)
        allowed = set(symbols)
        return {symbol: frame for symbol, frame in cached.items() if symbol in allowed and not frame.empty}

    frames: dict[str, pd.DataFrame] = {}
    end_exclusive = (pd.Timestamp(end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    for offset in range(0, len(symbols), batch_size):
        batch = sorted(symbols[offset : offset + batch_size])
        print(f"Downloading SMH OHLCV {offset + 1}-{offset + len(batch)} of {len(symbols)}", flush=True)
        raw = yf.download(
            batch,
            start=start,
            end=end_exclusive,
            interval="1d",
            auto_adjust=True,
            group_by="ticker",
            threads=True,
            progress=False,
        )
        for symbol in batch:
            frame = normalize_download_frame(raw, symbol)
            if not frame.empty and len(frame) >= 260:
                frames[symbol] = frame
        if offset + batch_size < len(symbols):
            time.sleep(0.25)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with cache_path.open("wb") as fh:
        pickle.dump(frames, fh, protocol=pickle.HIGHEST_PROTOCOL)
    return frames


def add_indicators(frames: dict[str, pd.DataFrame]) -> None:
    smh = frames["SMH"]
    smh_close = smh["Close"].astype(float)
    smh["SMA100"] = smh_close.rolling(100).mean()
    smh["RET63"] = smh_close.pct_change(63)
    for frame in frames.values():
        close = frame["Close"].astype(float)
        frame["SMA50"] = close.rolling(50).mean()
        frame["RET63"] = close.pct_change(63)
    add_atr(frames)


def smh_entry_filter(frames: dict[str, pd.DataFrame]):
    smh = frames["SMH"]

    def allowed(symbol: str, day: pd.Timestamp) -> bool:
        frame = frames.get(symbol)
        if frame is None or day not in frame.index or day not in smh.index:
            return False
        row = frame.loc[day]
        smh_row = smh.loc[day]
        checks = [row.get("Close"), row.get("SMA50"), row.get("RET63"), smh_row.get("Close"), smh_row.get("SMA100"), smh_row.get("RET63")]
        if any(pd.isna(value) for value in checks):
            return False
        return bool(float(row["Close"]) > float(row["SMA50"]) and float(row["RET63"]) > float(smh_row["RET63"]) and float(smh_row["Close"]) > float(smh_row["SMA100"]))

    return allowed


def build_daily_signals(
    frames: dict[str, pd.DataFrame],
    snapshots: list[dict[str, object]],
    available_tickers: set[str],
    *,
    start: str,
    end: str,
    scan_step: int,
    top_n: int,
    min_score: float,
    min_target_return_pct: float,
) -> pd.DataFrame:
    smh_calendar = frames["SMH"].index
    membership_cache: dict[pd.Timestamp, set[str]] = {}
    rows: list[dict[str, object]] = []
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    symbols = sorted(available_tickers - {"SMH"})

    for idx, symbol in enumerate(symbols, start=1):
        if idx == 1 or idx % 10 == 0:
            print(f"Scanning SMH daily cup/handle {idx}/{len(symbols)}: {symbol}", flush=True)
        frame = frames.get(symbol)
        if frame is None or len(frame) < 260:
            continue
        pivot_highs, pivot_lows = local_pivots(frame, window=3)
        pivot_highs_arr = np.asarray(pivot_highs, dtype=int)
        pivot_lows_arr = np.asarray(pivot_lows, dtype=int)
        first_idx = max(220, int(frame.index.searchsorted(start_ts)))
        last_possible_idx = min(len(frame) - 1, int(frame.index.searchsorted(end_ts, side="right")) - 1)
        for last_idx in range(first_idx, last_possible_idx + 1, scan_step):
            signal_day = pd.Timestamp(frame.index[last_idx])
            if signal_day not in membership_cache:
                snapshot = latest_known_snapshot(snapshots, signal_day)
                membership_cache[signal_day] = set(snapshot["tickers"]) if snapshot else set()
            if symbol not in membership_cache[signal_day]:
                continue
            trade_start_idx = smh_calendar.searchsorted(signal_day + pd.Timedelta(days=1))
            if trade_start_idx >= len(smh_calendar):
                continue
            trade_start = pd.Timestamp(smh_calendar[trade_start_idx])
            expire_date = nth_trading_day(smh_calendar, trade_start, 3)
            if expire_date is None:
                continue
            candidates = find_daily_patterns_asof(
                frame,
                last_idx,
                pivot_highs_arr,
                pivot_lows_arr,
                min_target_return_pct=min_target_return_pct,
                min_score=min_score,
            )
            if not candidates:
                continue
            candidate = candidates[0]
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
    signals = signals.groupby("SignalDateTs", group_keys=False).head(top_n)
    return signals.drop(columns=["SignalDateTs"]).reset_index(drop=True)


def benchmark_equity_from_frame(frame: pd.DataFrame, start: str, end: str, initial_capital: float) -> pd.Series:
    close = frame["Close"].astype(float)
    values = close[(close.index >= pd.Timestamp(start)) & (close.index <= pd.Timestamp(end))].dropna()
    return initial_capital * values / values.iloc[0]


def annual_return_drawdown(equity: pd.Series, trades: pd.DataFrame, label: str) -> pd.DataFrame:
    rows = []
    trade_year = pd.to_datetime(trades["EntryDate"]).dt.year if not trades.empty else pd.Series(dtype=int)
    for year, values in equity.groupby(equity.index.year):
        dd = values / values.cummax() - 1.0
        year_trades = trades[trade_year == year] if not trades.empty else trades
        rows.append(
            {
                "Strategy": label,
                "Year": int(year),
                "AnnualReturnPct": round((values.iloc[-1] / values.iloc[0] - 1.0) * 100.0, 2),
                "MaxDrawdownPct": round(float(dd.min()) * 100.0, 2),
                "Trades": int(len(year_trades)),
            }
        )
    return pd.DataFrame(rows)


def plot_equity(strategy: pd.Series, benchmark: pd.Series, output: Path) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), dpi=150, sharex=True)
    axes[0].plot(strategy.index, strategy.values, label="SMH component cup/handle", linewidth=1.6)
    axes[0].plot(benchmark.index, benchmark.values, label="SMH buy-and-hold", linewidth=1.4)
    axes[0].set_title("OOS Equity")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend()
    axes[1].plot((strategy / strategy.cummax() - 1.0).index, (strategy / strategy.cummax() - 1.0).values * 100.0, label="Strategy DD")
    axes[1].plot((benchmark / benchmark.cummax() - 1.0).index, (benchmark / benchmark.cummax() - 1.0).values * 100.0, label="SMH DD")
    axes[1].set_title("OOS Drawdown")
    axes[1].set_ylabel("Drawdown %")
    axes[1].grid(True, alpha=0.25)
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)


def existing_smh_top2_metrics() -> dict[str, object]:
    path = Path("reports/smh_historical_components_momentum_is2010_2019_oos2020_2026ytd.csv")
    if not path.exists():
        return {}
    rows = pd.read_csv(path)
    row = rows[rows["strategy"] == "SMH_HIST_PIT Top2 L252 S0 smh_sma100 DCA1"]
    if row.empty:
        return {}
    item = row.iloc[0]
    return {
        "is_return_pct": round(float(item["is_return"]) * 100.0, 2),
        "is_sharpe": round(float(item["is_sharpe"]), 3),
        "is_max_drawdown_pct": round(float(item["is_max_drawdown"]) * 100.0, 2),
        "oos_return_pct": round(float(item["oos_return"]) * 100.0, 2),
        "oos_sharpe": round(float(item["oos_sharpe"]), 3),
        "oos_max_drawdown_pct": round(float(item["oos_max_drawdown"]) * 100.0, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    parser.add_argument("--scan-step", type=int, default=5)
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--min-score", type=float, default=45.0)
    parser.add_argument("--min-target-return-pct", type=float, default=30.0)
    parser.add_argument("--initial-capital", type=float, default=100000.0)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    holdings = load_historical_holdings()
    snapshots = snapshot_tickers_by_public_date(holdings)
    historical_tickers = sorted(set(holdings["ticker"]) | {"SMH"})
    frames = load_or_download_ohlcv(historical_tickers, PRICE_START, OOS_END, CACHE_PATH)
    available_tickers = {ticker for ticker, frame in frames.items() if len(frame) >= 260}
    add_indicators(frames)

    signals = build_daily_signals(
        frames,
        snapshots,
        available_tickers,
        start=IS_START,
        end=OOS_END,
        scan_step=args.scan_step,
        top_n=args.top_n,
        min_score=args.min_score,
        min_target_return_pct=args.min_target_return_pct,
    )
    signals_path = output_dir / "smh_daily_cup_handle_signals.csv"
    signals.to_csv(signals_path, index=False)
    signals_prepared = signals.copy()
    signals_prepared["SignalDateTs"] = pd.to_datetime(signals_prepared["SignalDate"])
    signals_prepared["TradeStartTs"] = pd.to_datetime(signals_prepared["TradeStartDate"])
    signals_prepared["ExpireTs"] = pd.to_datetime(signals_prepared["ExpireDate"])
    smh_calendar = frames["SMH"].index
    signals_window = override_expire_window(signals_prepared, smh_calendar, 7)

    entry_filter = smh_entry_filter(frames)
    variant = AtrExitVariant("atr_3.5x_no_target_60d_entry7", "atr", 3.5, False, "none", 60)
    is_equity, is_trades = run_backtest_atr_exit(
        frames,
        signals_window,
        smh_calendar,
        start=IS_START,
        end=(pd.Timestamp(IS_END) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
        initial_capital=args.initial_capital,
        max_positions=3,
        variant=variant,
        atr_column="ATR14",
        entry_filter=entry_filter,
        require_entry_volume=True,
        entry_volume_min_ratio=1.4,
    )
    oos_equity, oos_trades = run_backtest_atr_exit(
        frames,
        signals_window,
        smh_calendar,
        start=OOS_START,
        end=OOS_END,
        initial_capital=args.initial_capital,
        max_positions=3,
        variant=variant,
        atr_column="ATR14",
        entry_filter=entry_filter,
        require_entry_volume=True,
        entry_volume_min_ratio=1.4,
    )

    is_series = is_equity.set_index(pd.to_datetime(is_equity["Date"]))["Equity"].astype(float)
    oos_series = oos_equity.set_index(pd.to_datetime(oos_equity["Date"]))["Equity"].astype(float)
    smh_is = benchmark_equity_from_frame(frames["SMH"], IS_START, (pd.Timestamp(IS_END) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"), args.initial_capital)
    smh_oos = benchmark_equity_from_frame(frames["SMH"], OOS_START, OOS_END, args.initial_capital)
    is_metrics = summary_metrics(is_series, is_trades)
    oos_metrics = summary_metrics(oos_series, oos_trades)
    smh_is_metrics = summary_metrics(smh_is, pd.DataFrame())
    smh_oos_metrics = summary_metrics(smh_oos, pd.DataFrame())
    top2 = existing_smh_top2_metrics()

    is_equity.to_csv(output_dir / "smh_daily_cup_handle_is_equity.csv", index=False)
    oos_equity.to_csv(output_dir / "smh_daily_cup_handle_oos_equity.csv", index=False)
    is_trades.to_csv(output_dir / "smh_daily_cup_handle_is_trades.csv", index=False)
    oos_trades.to_csv(output_dir / "smh_daily_cup_handle_oos_trades.csv", index=False)
    annual = pd.concat(
        [
            annual_return_drawdown(is_series, is_trades, "CupHandle IS"),
            annual_return_drawdown(oos_series, oos_trades, "CupHandle OOS"),
            annual_return_drawdown(smh_is, pd.DataFrame(), "SMH IS"),
            annual_return_drawdown(smh_oos, pd.DataFrame(), "SMH OOS"),
        ],
        ignore_index=True,
    )
    annual.to_csv(output_dir / "smh_daily_cup_handle_annual_return_drawdown.csv", index=False)
    plot_equity(oos_series, smh_oos, output_dir / "smh_daily_cup_handle_oos_curves.png")

    comparison_rows = [
        {
            "Strategy": "SMH component daily cup/handle",
            "IS_ReturnPct": is_metrics["total_return_pct"],
            "IS_MaxDrawdownPct": is_metrics["max_drawdown_pct"],
            "IS_Sharpe": is_metrics["sharpe"],
            "IS_Trades": is_metrics["trade_count"],
            "OOS_ReturnPct": oos_metrics["total_return_pct"],
            "OOS_MaxDrawdownPct": oos_metrics["max_drawdown_pct"],
            "OOS_Sharpe": oos_metrics["sharpe"],
            "OOS_Trades": oos_metrics["trade_count"],
        },
        {
            "Strategy": "SMH buy-and-hold",
            "IS_ReturnPct": smh_is_metrics["total_return_pct"],
            "IS_MaxDrawdownPct": smh_is_metrics["max_drawdown_pct"],
            "IS_Sharpe": smh_is_metrics["sharpe"],
            "IS_Trades": "",
            "OOS_ReturnPct": smh_oos_metrics["total_return_pct"],
            "OOS_MaxDrawdownPct": smh_oos_metrics["max_drawdown_pct"],
            "OOS_Sharpe": smh_oos_metrics["sharpe"],
            "OOS_Trades": "",
        },
    ]
    if top2:
        comparison_rows.append(
            {
                "Strategy": "SMH Top2 L252 S0 SMA100 DCA1",
                "IS_ReturnPct": top2["is_return_pct"],
                "IS_MaxDrawdownPct": top2["is_max_drawdown_pct"],
                "IS_Sharpe": top2["is_sharpe"],
                "IS_Trades": "",
                "OOS_ReturnPct": top2["oos_return_pct"],
                "OOS_MaxDrawdownPct": top2["oos_max_drawdown_pct"],
                "OOS_Sharpe": top2["oos_sharpe"],
                "OOS_Trades": "",
            }
        )
    comparison = pd.DataFrame(comparison_rows)
    comparison.to_csv(output_dir / "smh_daily_cup_handle_comparison.csv", index=False)

    lines = [
        "# SMH Historical Components Daily Cup-And-Handle Backtest",
        "",
        "This is technical strategy research, not investment advice.",
        "",
        "## Setup",
        "",
        f"- Holdings source: `{HOLDINGS_PATH}`.",
        "- Universe logic: latest SMH/legacy Semiconductor HOLDRS holdings snapshot whose SEC filing date was public on or before the signal date.",
        "- Pattern timeframe: daily cup-and-handle, scanned every 5 trading days.",
        "- Candidate pool: top 10 by score after `TargetReturnPct > 30%`.",
        "- Entry window: 7 trading days.",
        "- Entry filters: stock close > SMA50, stock 63-day return > SMH 63-day return, and SMH close > SMA100.",
        "- Entry volume: breakout-day volume >= 1.40x prior 50-day average.",
        "- Exit: ATR14 3.5x stop, no target, 60-trading-day time stop.",
        "- Portfolio: max 3 concurrent stocks.",
        "",
        "## Data Audit",
        "",
        f"- Historical SMH tickers in SEC holdings file: `{len(historical_tickers) - 1}`",
        f"- Price-available tickers including SMH: `{len(available_tickers)}`",
        f"- Signals generated: `{len(signals)}`",
        f"- IS trades: `{len(is_trades)}`",
        f"- OOS trades: `{len(oos_trades)}`",
        "",
        "## IS/OOS Comparison",
        "",
        markdown_table(comparison),
        "",
        "## Annual Return / Drawdown",
        "",
        markdown_table(annual),
        "",
        "## Outputs",
        "",
        f"- Signals: `{signals_path}`",
        f"- Comparison CSV: `{output_dir / 'smh_daily_cup_handle_comparison.csv'}`",
        f"- Annual CSV: `{output_dir / 'smh_daily_cup_handle_annual_return_drawdown.csv'}`",
        f"- OOS curve: `{output_dir / 'smh_daily_cup_handle_oos_curves.png'}`",
    ]
    report_path = output_dir / "smh_daily_cup_handle_report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"signals={len(signals)}")
    print(f"is_return={is_metrics['total_return_pct']}")
    print(f"oos_return={oos_metrics['total_return_pct']}")
    print(f"smh_oos_return={smh_oos_metrics['total_return_pct']}")
    print(f"report={report_path}")


if __name__ == "__main__":
    main()
