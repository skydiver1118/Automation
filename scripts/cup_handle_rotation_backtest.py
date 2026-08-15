from __future__ import annotations

import argparse
import json
import math
import pickle
import sys
import time
from dataclasses import asdict, dataclass
from io import StringIO
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_detection import (  # noqa: E402
    PatternCandidate,
    local_pivots,
    score_candidate,
)


HISTORICAL_SP500_URL = "https://raw.githubusercontent.com/hanshof/sp500_constituents/main/sp_500_historical_components.csv"


@dataclass
class WatchCandidate:
    symbol: str
    signal_date: pd.Timestamp
    expire_date: pd.Timestamp
    candidate: PatternCandidate


@dataclass
class Position:
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


def yahoo_symbol(symbol: str) -> str:
    return symbol.replace(".", "-")


def normalize_symbol_for_membership(symbol: str) -> str:
    return yahoo_symbol(symbol.strip())


def load_historical_sp500(start: str, end: str) -> pd.DataFrame:
    df = pd.read_csv(HISTORICAL_SP500_URL)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    start_ts = pd.Timestamp(start) - pd.Timedelta(days=800)
    end_ts = pd.Timestamp(end) + pd.Timedelta(days=10)
    df = df[(df["date"] >= start_ts) & (df["date"] <= end_ts)].copy()
    return df


def constituent_set_on(history: pd.DataFrame, date: pd.Timestamp) -> set[str]:
    rows = history[history["date"] <= date]
    if rows.empty:
        return set()
    tickers = str(rows.iloc[-1]["tickers"]).split(",")
    return {normalize_symbol_for_membership(ticker) for ticker in tickers if ticker}


def unique_symbols(history: pd.DataFrame, start: str, end: str) -> list[str]:
    mask = (history["date"] >= pd.Timestamp(start)) & (history["date"] <= pd.Timestamp(end))
    symbols: set[str] = set()
    for value in history.loc[mask, "tickers"]:
        symbols.update(normalize_symbol_for_membership(ticker) for ticker in str(value).split(",") if ticker)
    return sorted(symbols)


def normalize_download_frame(raw: pd.DataFrame, ticker: str) -> pd.DataFrame:
    if raw.empty:
        return pd.DataFrame()
    if isinstance(raw.columns, pd.MultiIndex):
        if ticker in raw.columns.get_level_values(0):
            df = raw[ticker].copy()
        elif ticker in raw.columns.get_level_values(-1):
            df = raw.xs(ticker, axis=1, level=-1).copy()
        else:
            return pd.DataFrame()
    else:
        df = raw.copy()
    df = df.rename(columns=str.title)
    expected = ["Open", "High", "Low", "Close", "Volume"]
    missing = [column for column in expected if column not in df.columns]
    if missing:
        return pd.DataFrame()
    df = df[expected].dropna()
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df


def download_daily(symbols: list[str], start: str, end: str, batch_size: int, pause_seconds: float) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for batch_start in range(0, len(symbols), batch_size):
        batch = symbols[batch_start : batch_start + batch_size]
        print(f"Downloading daily adjusted OHLCV {batch_start + 1}-{batch_start + len(batch)} of {len(symbols)}...")
        raw = yf.download(
            batch,
            start=start,
            end=end,
            interval="1d",
            auto_adjust=True,
            group_by="ticker",
            threads=True,
            progress=False,
        )
        for symbol in batch:
            frame = normalize_download_frame(raw, symbol)
            if not frame.empty:
                frames[symbol] = frame
        if pause_seconds and batch_start + batch_size < len(symbols):
            time.sleep(pause_seconds)
    return frames


def load_or_download_daily(
    symbols: list[str],
    start: str,
    end: str,
    batch_size: int,
    pause_seconds: float,
    cache_path: Path | None,
) -> dict[str, pd.DataFrame]:
    if cache_path and cache_path.exists():
        with cache_path.open("rb") as fh:
            cached = pickle.load(fh)
        allowed = set(symbols)
        frames = {symbol: frame for symbol, frame in cached.items() if symbol in allowed}
        if frames:
            return frames
    frames = download_daily(symbols, start, end, batch_size, pause_seconds)
    if cache_path:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with cache_path.open("wb") as fh:
            pickle.dump(frames, fh, protocol=pickle.HIGHEST_PROTOCOL)
    return frames


def daily_to_weekly(daily: pd.DataFrame) -> pd.DataFrame:
    weekly = pd.DataFrame(
        {
            "Open": daily["Open"].resample("W-FRI").first(),
            "High": daily["High"].resample("W-FRI").max(),
            "Low": daily["Low"].resample("W-FRI").min(),
            "Close": daily["Close"].resample("W-FRI").last(),
            "Volume": daily["Volume"].resample("W-FRI").sum(),
        }
    ).dropna()
    return weekly


def next_trading_day(calendar: pd.DatetimeIndex, date: pd.Timestamp) -> pd.Timestamp | None:
    idx = calendar.searchsorted(date + pd.Timedelta(days=1))
    if idx >= len(calendar):
        return None
    return pd.Timestamp(calendar[idx])


def nth_trading_day(calendar: pd.DatetimeIndex, start_date: pd.Timestamp, n: int) -> pd.Timestamp | None:
    idx = calendar.searchsorted(start_date)
    target_idx = idx + n - 1
    if target_idx >= len(calendar):
        return None
    return pd.Timestamp(calendar[target_idx])


def entry_volume_pass(frame: pd.DataFrame, day: pd.Timestamp, min_ratio: float = 1.4, lookback_days: int = 50) -> bool:
    if day not in frame.index or "Volume" not in frame.columns:
        return False
    idx = int(frame.index.get_loc(day))
    if idx < lookback_days:
        return False
    prior_avg = float(frame["Volume"].iloc[idx - lookback_days : idx].mean())
    if not math.isfinite(prior_avg) or prior_avg <= 0:
        return False
    return float(frame.loc[day, "Volume"]) >= prior_avg * min_ratio


def find_patterns_asof(
    df: pd.DataFrame,
    last_idx: int,
    pivot_highs: list[int],
    pivot_lows: list[int],
    *,
    min_target_return_pct: float,
    min_score: float,
) -> list[PatternCandidate]:
    candidates: list[PatternCandidate] = []
    highs = np.asarray(pivot_highs, dtype=int)
    lows = np.asarray(pivot_lows, dtype=int)
    if highs.size == 0 or lows.size == 0:
        return candidates

    right_rims = highs[(last_idx - highs >= 2) & (last_idx - highs <= 10)]
    for k in right_rims:
        left_rims = highs[(highs >= k - 70) & (highs <= k - 20)]
        if left_rims.size == 0:
            continue
        cup_lows = lows[(lows > int(left_rims.min())) & (lows < k)]
        if cup_lows.size == 0:
            continue
        for j in cup_lows:
            for i in left_rims[left_rims < j]:
                candidate = score_candidate(df, int(i), int(j), int(k), last_idx)
                if not candidate:
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
    max_symbols: int | None = None,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    symbols = list(frames.keys())
    if max_symbols:
        symbols = symbols[:max_symbols]
    scan_start = pd.Timestamp(start)
    scan_end = pd.Timestamp(end)
    membership_cache: dict[pd.Timestamp, set[str]] = {}
    for symbol_index, symbol in enumerate(symbols, start=1):
        if symbol_index % 25 == 0 or symbol_index == 1:
            print(f"Scanning patterns for {symbol_index}/{len(symbols)}: {symbol}", flush=True)
        daily = frames[symbol]
        weekly = daily_to_weekly(daily)
        if len(weekly) < 90:
            continue
        pivot_highs, pivot_lows = local_pivots(weekly, window=2)
        for last_idx in range(75, len(weekly)):
            signal_week = pd.Timestamp(weekly.index[last_idx])
            if signal_week < scan_start or signal_week > scan_end:
                continue
            if signal_week not in membership_cache:
                membership_cache[signal_week] = constituent_set_on(history, signal_week)
            members = membership_cache[signal_week]
            if symbol not in members:
                continue
            trade_start = next_trading_day(calendar, signal_week)
            if trade_start is None:
                continue
            expire_date = nth_trading_day(calendar, trade_start, 3)
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
                }
            )
    signals = pd.DataFrame(rows)
    if not signals.empty:
        signals = signals.sort_values(["SignalDate", "Score"], ascending=[True, False]).reset_index(drop=True)
    return signals


def choose_candidates_for_day(
    signals: pd.DataFrame,
    day: pd.Timestamp,
    excluded_symbols: set[str],
    consumed_signal_keys: set[tuple[str, str]],
    n: int,
) -> list[WatchCandidate]:
    if signals.empty or n <= 0:
        return []
    trade_start = signals["TradeStartTs"] if "TradeStartTs" in signals.columns else pd.to_datetime(signals["TradeStartDate"])
    expire = signals["ExpireTs"] if "ExpireTs" in signals.columns else pd.to_datetime(signals["ExpireDate"])
    eligible = signals[(trade_start <= day) & (expire >= day)].copy()
    eligible = eligible[~eligible["Symbol"].isin(excluded_symbols)]
    if eligible.empty:
        return []
    eligible = eligible.sort_values(["Score", "TargetReturnPct"], ascending=[False, False])
    selected: list[WatchCandidate] = []
    seen: set[str] = set()
    for _, row in eligible.iterrows():
        symbol = row["Symbol"]
        if symbol in seen:
            continue
        signal_date_value = row["SignalDateTs"] if "SignalDateTs" in eligible.columns else row["SignalDate"]
        signal_date_str = pd.Timestamp(signal_date_value).strftime("%Y-%m-%d")
        if (symbol, signal_date_str) in consumed_signal_keys:
            continue
        candidate = PatternCandidate(**json.loads(row["CandidateJson"]))
        selected.append(
            WatchCandidate(
                symbol=symbol,
                signal_date=pd.Timestamp(signal_date_value),
                expire_date=pd.Timestamp(row["ExpireDate"]),
                candidate=candidate,
            )
        )
        seen.add(symbol)
        if len(selected) >= n:
            break
    return selected


def run_backtest(
    frames: dict[str, pd.DataFrame],
    signals: pd.DataFrame,
    calendar: pd.DatetimeIndex,
    *,
    start: str,
    end: str,
    initial_capital: float,
    max_positions: int,
    max_hold_days: int,
    entry_filter: Callable[[str, pd.Timestamp], bool] | None = None,
    require_entry_volume: bool = False,
    entry_volume_min_ratio: float = 1.4,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    cash = initial_capital
    positions: list[Position] = []
    watches: list[WatchCandidate] = []
    consumed_signal_keys: set[tuple[str, str]] = set()
    trades: list[dict[str, object]] = []
    equity_rows: list[dict[str, object]] = []

    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)
    days = [pd.Timestamp(day) for day in calendar if start_ts <= day <= end_ts]
    for day in days:
        # Expire unfilled watch candidates.
        watches = [watch for watch in watches if watch.expire_date >= day]

        # Conservative same-day exit handling: stop before target if both touched.
        survivors: list[Position] = []
        for pos in positions:
            frame = frames.get(pos.symbol)
            if frame is None or day not in frame.index:
                survivors.append(pos)
                continue
            row = frame.loc[day]
            exit_price = None
            exit_reason = None
            if float(row["Low"]) <= pos.stop:
                exit_price = pos.stop
                exit_reason = "stop"
            elif float(row["High"]) >= pos.target:
                exit_price = pos.target
                exit_reason = "target"
            elif day >= pos.max_exit_date:
                exit_price = float(row["Close"])
                exit_reason = "time_stop"

            if exit_price is None:
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
                    "Stop": pos.stop,
                    "HoldingDays": int((day - pos.entry_date).days),
                }
            )
        positions = survivors

        excluded = {pos.symbol for pos in positions} | {watch.symbol for watch in watches}
        needed = max_positions - len(positions) - len(watches)
        watches.extend(choose_candidates_for_day(signals, day, excluded, consumed_signal_keys, needed))

        # Buy at breakout stop if touched within the three-trading-day watch window.
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
            if entry_filter is not None and not entry_filter(watch.symbol, day):
                remaining_watches.append(watch)
                continue
            if require_entry_volume and not entry_volume_pass(frame, day, entry_volume_min_ratio):
                remaining_watches.append(watch)
                continue
            slot_value = (cash + sum(mark_position(pos, frames, day) for pos in positions)) / max_positions
            spend = min(cash, slot_value)
            if spend <= 0:
                remaining_watches.append(watch)
                continue
            shares = spend / breakout
            cash -= spend
            max_exit_date = nth_trading_day(calendar, day, max_hold_days) or end_ts
            consumed_signal_keys.add((watch.symbol, watch.signal_date.strftime("%Y-%m-%d")))
            positions.append(
                Position(
                    symbol=watch.symbol,
                    entry_date=day,
                    entry_price=breakout,
                    shares=shares,
                    target=watch.candidate.projected_target,
                    stop=watch.candidate.handle_low_price,
                    score=watch.candidate.score,
                    signal_date=watch.signal_date,
                    breakout_level=breakout,
                    max_exit_date=max_exit_date,
                )
            )
        watches = remaining_watches

        position_value = sum(mark_position(pos, frames, day) for pos in positions)
        equity = cash + position_value
        equity_rows.append(
            {
                "Date": day.strftime("%Y-%m-%d"),
                "Equity": equity,
                "Cash": cash,
                "PositionValue": position_value,
                "OpenPositions": len(positions),
                "OpenWatches": len(watches),
            }
        )

    return pd.DataFrame(equity_rows), pd.DataFrame(trades)


def mark_position(pos: Position, frames: dict[str, pd.DataFrame], day: pd.Timestamp) -> float:
    frame = frames.get(pos.symbol)
    if frame is None or frame.empty:
        return pos.shares * pos.entry_price
    idx = frame.index.searchsorted(day, side="right") - 1
    if idx < 0:
        return pos.shares * pos.entry_price
    return pos.shares * float(frame.iloc[idx]["Close"])


def summary_metrics(equity: pd.Series, trades: pd.DataFrame) -> dict[str, float | int]:
    if equity.empty:
        return {}
    values = equity.astype(float)
    total_return = values.iloc[-1] / values.iloc[0] - 1.0
    years = max((values.index[-1] - values.index[0]).days / 365.25, 1e-9)
    cagr = (values.iloc[-1] / values.iloc[0]) ** (1.0 / years) - 1.0
    running_max = values.cummax()
    drawdown = values / running_max - 1.0
    daily_returns = values.pct_change().dropna()
    sharpe = math.nan
    if daily_returns.std(ddof=0) > 0:
        sharpe = float(daily_returns.mean() / daily_returns.std(ddof=0) * math.sqrt(252))
    win_rate = math.nan
    if not trades.empty:
        win_rate = float((trades["PnL"] > 0).mean())
    return {
        "total_return_pct": round(total_return * 100.0, 2),
        "cagr_pct": round(cagr * 100.0, 2),
        "max_drawdown_pct": round(float(drawdown.min()) * 100.0, 2),
        "sharpe": round(sharpe, 3) if not math.isnan(sharpe) else math.nan,
        "trade_count": int(len(trades)),
        "win_rate_pct": round(win_rate * 100.0, 2) if not math.isnan(win_rate) else math.nan,
    }


def benchmark_equity(start: str, end: str, initial_capital: float) -> pd.Series:
    bench = yf.download("^GSPC", start=start, end=end, interval="1d", auto_adjust=True, progress=False)
    if bench.empty:
        return pd.Series(dtype=float)
    close = bench["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return initial_capital * close / close.iloc[0]


def plot_curves(equity: pd.DataFrame, benchmark: pd.Series, output: Path) -> None:
    if equity.empty:
        return
    strategy = equity.set_index(pd.to_datetime(equity["Date"]))["Equity"].astype(float)
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), dpi=150, sharex=True)
    axes[0].plot(strategy.index, strategy.values, label="Cup/Handle rotation", linewidth=1.6)
    if not benchmark.empty:
        axes[0].plot(benchmark.index, benchmark.values, label="S&P 500 index", linewidth=1.4)
    axes[0].set_title("Equity Curve")
    axes[0].set_ylabel("Equity")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend()

    strategy_dd = strategy / strategy.cummax() - 1.0
    axes[1].plot(strategy_dd.index, strategy_dd.values * 100.0, label="Strategy DD", linewidth=1.4)
    if not benchmark.empty:
        bench_dd = benchmark / benchmark.cummax() - 1.0
        axes[1].plot(bench_dd.index, bench_dd.values * 100.0, label="S&P 500 DD", linewidth=1.2)
    axes[1].set_title("Drawdown")
    axes[1].set_ylabel("Drawdown %")
    axes[1].grid(True, alpha=0.25)
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)


def write_report(
    output: Path,
    *,
    signals: pd.DataFrame,
    trades: pd.DataFrame,
    equity: pd.DataFrame,
    benchmark: pd.Series,
    is_start: str,
    is_end: str,
    oos_start: str,
    oos_end: str,
    universe_count: int,
    data_count: int,
    membership_start: str,
    membership_end: str,
    require_entry_volume: bool,
    entry_volume_min_ratio: float,
) -> None:
    equity_series = equity.set_index(pd.to_datetime(equity["Date"]))["Equity"].astype(float)
    is_equity = equity_series[(equity_series.index >= pd.Timestamp(is_start)) & (equity_series.index < pd.Timestamp(is_end))]
    oos_equity = equity_series[(equity_series.index >= pd.Timestamp(oos_start)) & (equity_series.index <= pd.Timestamp(oos_end))]
    is_trades = trades[(pd.to_datetime(trades["EntryDate"]) >= pd.Timestamp(is_start)) & (pd.to_datetime(trades["EntryDate"]) < pd.Timestamp(is_end))] if not trades.empty else trades
    oos_trades = trades[(pd.to_datetime(trades["EntryDate"]) >= pd.Timestamp(oos_start)) & (pd.to_datetime(trades["EntryDate"]) <= pd.Timestamp(oos_end))] if not trades.empty else trades
    bench_is = benchmark[(benchmark.index >= pd.Timestamp(is_start)) & (benchmark.index < pd.Timestamp(is_end))]
    bench_oos = benchmark[(benchmark.index >= pd.Timestamp(oos_start)) & (benchmark.index <= pd.Timestamp(oos_end))]

    is_metrics = summary_metrics(is_equity, is_trades)
    oos_metrics = summary_metrics(oos_equity, oos_trades)
    bench_is_metrics = summary_metrics(bench_is, pd.DataFrame())
    bench_oos_metrics = summary_metrics(bench_oos, pd.DataFrame())

    def row(label: str, metrics: dict[str, object]) -> str:
        return (
            f"| {label} | {metrics.get('total_return_pct', 'n/a')} | {metrics.get('cagr_pct', 'n/a')} | "
            f"{metrics.get('max_drawdown_pct', 'n/a')} | {metrics.get('sharpe', 'n/a')} | "
            f"{metrics.get('trade_count', 'n/a')} | {metrics.get('win_rate_pct', 'n/a')} |"
        )

    lines = [
        "# Cup-And-Handle Rotation Strategy Backtest",
        "",
        "This is technical strategy research, not investment advice.",
        "",
        "## Strategy Rules",
        "",
        "- Point-in-time S&P 500 membership comes from the public `hanshof/sp500_constituents` historical constituents file.",
        "- Dates after the membership file's latest row use the last available constituent snapshot.",
        "- Weekly cup-and-handle patterns are scanned after each completed week.",
        "- Weekly signal volume gate: handle average volume must be <= 1.05x cup average volume.",
        "- Candidates must score above the configured threshold and have target return greater than 30%, where target return is `target / breakout - 1`.",
        "- Portfolio can hold up to three concurrent stocks.",
        "- Buy uses a breakout stop: enter if the stock trades at or above the breakout level within the next three trading days.",
        f"- Entry volume condition: `{'enabled' if require_entry_volume else 'disabled'}`"
        + (f", breakout-day volume >= {entry_volume_min_ratio:.2f}x prior 50-day average." if require_entry_volume else "."),
        "- If no breakout fill occurs within three trading days, the candidate expires and the tester rotates to another qualified candidate.",
        "- Exit at measured target, stop out at handle low, or use a 60-trading-day time stop so capital is not trapped indefinitely.",
        "- If stop and target are both touched on the same day, the stop is assumed first.",
        "",
        "## Data Audit",
        "",
        f"- Historical universe symbols considered: `{universe_count}`",
        f"- Historical membership file coverage used: `{membership_start}` to `{membership_end}`",
        f"- Symbols with usable Yahoo adjusted daily OHLCV: `{data_count}`",
        f"- Signals generated: `{len(signals)}`",
        f"- Trades executed: `{len(trades)}`",
        "",
        "## Performance Summary",
        "",
        "| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe | Trades | Win Rate % |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        row(f"Strategy IS {is_start} to {is_end}", is_metrics),
        row(f"S&P 500 IS {is_start} to {is_end}", bench_is_metrics),
        row(f"Strategy OOS {oos_start} to {oos_end}", oos_metrics),
        row(f"S&P 500 OOS {oos_start} to {oos_end}", bench_oos_metrics),
        "",
        "## Exit Reason Counts",
        "",
    ]
    if trades.empty:
        lines.append("No trades executed.")
    else:
        counts = trades["ExitReason"].value_counts()
        for reason, count in counts.items():
            lines.append(f"- `{reason}`: {count}")
        lines += ["", "## Last 20 Trades", ""]
        cols = ["Symbol", "EntryDate", "ExitDate", "EntryPrice", "ExitPrice", "ReturnPct", "ExitReason", "Score"]
        last = trades.tail(20)[cols].copy()
        lines.append(markdown_table(last))
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--is-start", default="2010-01-01")
    parser.add_argument("--is-end", default="2020-01-01")
    parser.add_argument("--oos-start", default="2020-01-01")
    parser.add_argument("--oos-end", default="2026-05-30")
    parser.add_argument("--download-start", default="2008-01-01")
    parser.add_argument("--initial-capital", type=float, default=100000.0)
    parser.add_argument("--max-positions", type=int, default=3)
    parser.add_argument("--max-hold-days", type=int, default=60)
    parser.add_argument("--min-score", type=float, default=45.0)
    parser.add_argument("--min-target-return-pct", type=float, default=30.0)
    parser.add_argument("--batch-size", type=int, default=60)
    parser.add_argument("--pause-seconds", type=float, default=1.0)
    parser.add_argument("--max-symbols", type=int, default=0)
    parser.add_argument("--signals-csv", default="")
    parser.add_argument("--output-dir", default="reports/cup_handle_rotation_backtest")
    parser.add_argument("--cache-path", default="")
    parser.add_argument("--require-entry-volume", action="store_true")
    parser.add_argument("--entry-volume-min-ratio", type=float, default=1.4)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    end_exclusive = (pd.Timestamp(args.oos_end) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    history = load_historical_sp500(args.download_start, args.oos_end)
    symbols = unique_symbols(history, args.download_start, args.oos_end)
    if args.max_symbols:
        symbols = symbols[: args.max_symbols]
    cache_path = Path(args.cache_path) if args.cache_path else None
    frames = load_or_download_daily(symbols, args.download_start, end_exclusive, args.batch_size, args.pause_seconds, cache_path)
    calendar = sorted(set().union(*[set(frame.index) for frame in frames.values()])) if frames else []
    calendar_idx = pd.DatetimeIndex(calendar)

    if args.signals_csv:
        signals = pd.read_csv(args.signals_csv)
    else:
        signals = build_signal_table(
            frames,
            history,
            calendar_idx,
            start=args.is_start,
            end=args.oos_end,
            min_score=args.min_score,
            min_target_return_pct=args.min_target_return_pct,
            max_symbols=args.max_symbols or None,
        )
    equity, trades = run_backtest(
        frames,
        signals,
        calendar_idx,
        start=args.is_start,
        end=args.oos_end,
        initial_capital=args.initial_capital,
        max_positions=args.max_positions,
        max_hold_days=args.max_hold_days,
        require_entry_volume=args.require_entry_volume,
        entry_volume_min_ratio=args.entry_volume_min_ratio,
    )
    benchmark = benchmark_equity(args.is_start, end_exclusive, args.initial_capital)

    signals_path = output_dir / "cup_handle_rotation_signals.csv"
    trades_path = output_dir / "cup_handle_rotation_trades.csv"
    equity_path = output_dir / "cup_handle_rotation_equity.csv"
    bench_path = output_dir / "sp500_benchmark_equity.csv"
    report_path = output_dir / "cup_handle_rotation_backtest_report.md"
    curves_path = output_dir / "cup_handle_rotation_curves.png"

    signals.to_csv(signals_path, index=False)
    trades.to_csv(trades_path, index=False)
    equity.to_csv(equity_path, index=False)
    benchmark.rename("BenchmarkEquity").to_csv(bench_path, index_label="Date")
    plot_curves(equity, benchmark, curves_path)
    write_report(
        report_path,
        signals=signals,
        trades=trades,
        equity=equity,
        benchmark=benchmark,
        is_start=args.is_start,
        is_end=args.is_end,
        oos_start=args.oos_start,
        oos_end=args.oos_end,
        universe_count=len(symbols),
        data_count=len(frames),
        membership_start=history["date"].min().strftime("%Y-%m-%d") if not history.empty else "n/a",
        membership_end=history["date"].max().strftime("%Y-%m-%d") if not history.empty else "n/a",
        require_entry_volume=args.require_entry_volume,
        entry_volume_min_ratio=args.entry_volume_min_ratio,
    )

    print(f"symbols={len(symbols)}")
    print(f"data_frames={len(frames)}")
    print(f"signals={len(signals)}")
    print(f"trades={len(trades)}")
    print(f"report={report_path}")
    print(f"signals_csv={signals_path}")
    print(f"trades_csv={trades_path}")
    print(f"equity_csv={equity_path}")
    print(f"curves={curves_path}")


if __name__ == "__main__":
    main()
