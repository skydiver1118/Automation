from __future__ import annotations

import argparse
import json
import math
import os
import pickle
import sys
import time
from dataclasses import asdict
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Any
import urllib.request

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_daily_rotation_signals import find_daily_patterns_asof  # noqa: E402
from scripts.cup_handle_detection import local_pivots  # noqa: E402
from scripts.cup_handle_rotation_backtest import entry_volume_pass, load_historical_sp500, normalize_download_frame  # noqa: E402


REPORT_DIR = Path("reports/cup_handle_daily_alpaca")
STATE_PATH = REPORT_DIR / "cup_handle_daily_alpaca_state.json"
SIGNAL_CSV = REPORT_DIR / "cup_handle_daily_candidates.csv"
RUN_JSON = REPORT_DIR / "cup_handle_daily_run.json"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().lstrip("\ufeff")
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_state() -> dict[str, Any]:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"positions": {}, "last_run": None}


def save_state(state: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def sp500_symbols() -> list[str]:
    try:
        req = urllib.request.Request(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
            headers={"User-Agent": "Mozilla/5.0 cup-handle-daily-scanner/1.0"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8")
        tables = pd.read_html(StringIO(html))
        symbols = tables[0]["Symbol"].astype(str).str.replace(".", "-", regex=False).to_list()
    except Exception:
        history = load_historical_sp500("2025-01-01", datetime.now().strftime("%Y-%m-%d"))
        latest = str(history.iloc[-1]["tickers"]).split(",")
        symbols = [symbol.strip().replace(".", "-") for symbol in latest if symbol.strip()]
    return sorted(set(symbols))


def load_cached_frames(cache_path: Path, symbols: list[str]) -> dict[str, pd.DataFrame]:
    if not cache_path.exists():
        return {}
    with cache_path.open("rb") as fh:
        cached = pickle.load(fh)
    allowed = set(symbols)
    return {symbol: frame for symbol, frame in cached.items() if symbol in allowed and len(frame) >= 260}


def download_frames(symbols: list[str], period: str, batch_size: int, pause_seconds: float) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for start in range(0, len(symbols), batch_size):
        batch = symbols[start : start + batch_size]
        raw = yf.download(
            batch,
            period=period,
            interval="1d",
            auto_adjust=True,
            group_by="ticker",
            threads=True,
            progress=False,
        )
        for symbol in batch:
            frame = normalize_download_frame(raw, symbol)
            if len(frame) >= 260:
                frames[symbol] = frame
        if pause_seconds and start + batch_size < len(symbols):
            time.sleep(pause_seconds)
    return frames


def add_indicators(frame: pd.DataFrame, spx: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    close = out["Close"].astype(float)
    out["SMA50"] = close.rolling(50).mean()
    out["ATR14"] = true_range(out).rolling(14).mean()
    out["RET63"] = close.pct_change(63)
    spx_ret63 = spx["Close"].astype(float).pct_change(63).reindex(out.index).ffill()
    out["SPX_RET63"] = spx_ret63
    return out


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


def latest_spx(period: str) -> pd.DataFrame:
    spx = yf.download("^GSPC", period=period, interval="1d", auto_adjust=True, progress=False)
    if isinstance(spx.columns, pd.MultiIndex):
        spx.columns = [col[0] for col in spx.columns]
    spx = spx.rename(columns=str.title).dropna()
    spx.index = pd.to_datetime(spx.index).tz_localize(None)
    spx["SMA100"] = spx["Close"].astype(float).rolling(100).mean()
    return spx


def market_ok(spx: pd.DataFrame) -> bool:
    if spx.empty:
        return False
    latest = spx.iloc[-1]
    return bool(float(latest["Close"]) > float(latest["SMA100"]))


def stock_ok(frame: pd.DataFrame) -> bool:
    latest = frame.iloc[-1]
    values = [latest.get("Close"), latest.get("SMA50"), latest.get("RET63"), latest.get("SPX_RET63")]
    if any(pd.isna(value) for value in values):
        return False
    return bool(float(latest["Close"]) > float(latest["SMA50"]) and float(latest["RET63"]) > float(latest["SPX_RET63"]))


def scan_candidates(frames: dict[str, pd.DataFrame], spx: pd.DataFrame, min_score: float, min_target_return_pct: float, top_n: int) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for symbol, raw_frame in frames.items():
        frame = add_indicators(raw_frame, spx)
        pivot_highs, pivot_lows = local_pivots(frame, window=3)
        patterns = find_daily_patterns_asof(
            frame,
            len(frame) - 1,
            np.asarray(pivot_highs, dtype=int),
            np.asarray(pivot_lows, dtype=int),
            min_target_return_pct=min_target_return_pct,
            min_score=min_score,
        )
        if not patterns:
            continue
        candidate = patterns[0]
        target_return_pct = (candidate.projected_target / candidate.breakout_level - 1.0) * 100.0
        latest_day = pd.Timestamp(frame.index[-1])
        entry_vol_ok = entry_volume_pass(frame, latest_day, min_ratio=1.4)
        close_confirmed = float(frame["Close"].iloc[-1]) >= candidate.breakout_level
        atr14 = float(frame["ATR14"].iloc[-1]) if not pd.isna(frame["ATR14"].iloc[-1]) else math.nan
        rows.append(
            {
                "Symbol": symbol,
                "Date": latest_day.strftime("%Y-%m-%d"),
                "Score": candidate.score,
                "Status": candidate.status,
                "Close": round(float(frame["Close"].iloc[-1]), 4),
                "BreakoutLevel": candidate.breakout_level,
                "TargetReturnPct": round(target_return_pct, 2),
                "CupLowDate": candidate.bottom_date,
                "RightRimDate": candidate.right_rim_date,
                "HandleLowDate": candidate.handle_low_date,
                "StopPrice": round(float(frame["Close"].iloc[-1]) - 3.5 * atr14, 4) if math.isfinite(atr14) else math.nan,
                "StockFilterOK": stock_ok(frame),
                "MarketFilterOK": market_ok(spx),
                "EntryVolumeOK": entry_vol_ok,
                "CloseConfirmed": close_confirmed,
                "VolumeNote": candidate.volume_note,
                "CandidateJson": json.dumps(asdict(candidate)),
            }
        )
    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows)
    return out.sort_values(["Score", "TargetReturnPct"], ascending=[False, False]).head(top_n).reset_index(drop=True)


def trading_client(paper: bool):
    from alpaca.trading.client import TradingClient

    return TradingClient(
        api_key=require_env("ALPACA_API_KEY"),
        secret_key=require_env("ALPACA_SECRET_KEY"),
        paper=paper,
    )


def alpaca_positions(client) -> dict[str, Any]:
    positions = {}
    for pos in client.get_all_positions():
        positions[str(pos.symbol).upper()] = pos
    return positions


def submit_order(client, *, symbol: str, side: str, qty: int, limit_price: float, extended_hours: bool, client_order_id: str):
    from alpaca.trading.enums import OrderSide, TimeInForce
    from alpaca.trading.requests import LimitOrderRequest

    side_value = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL
    request = LimitOrderRequest(
        symbol=symbol,
        qty=qty,
        side=side_value,
        time_in_force=TimeInForce.DAY,
        limit_price=round(limit_price, 2),
        extended_hours=extended_hours,
        client_order_id=client_order_id[:48],
    )
    return client.submit_order(request)


def trading_days_after(index: pd.DatetimeIndex, start_day: pd.Timestamp, days: int) -> str:
    idx = index.searchsorted(start_day)
    target = min(idx + days, len(index) - 1)
    return pd.Timestamp(index[target]).strftime("%Y-%m-%d")


def build_actions(candidates: pd.DataFrame, frames: dict[str, pd.DataFrame], state: dict[str, Any], positions: dict[str, Any], account_equity: float, max_positions: int, target_equity_pct: float) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    managed = state.setdefault("positions", {})
    today = pd.Timestamp(datetime.now().date())

    for symbol, position_state in list(managed.items()):
        frame = frames.get(symbol)
        if frame is None or frame.empty:
            continue
        latest = frame.iloc[-1]
        close = float(latest["Close"])
        stop = float(position_state.get("stop", 0))
        max_exit_date = pd.Timestamp(position_state.get("max_exit_date"))
        if close <= stop or pd.Timestamp(frame.index[-1]) >= max_exit_date:
            pos = positions.get(symbol)
            qty = int(float(getattr(pos, "qty", position_state.get("qty", 0)))) if pos is not None else int(position_state.get("qty", 0))
            if qty > 0:
                actions.append({"action": "sell", "symbol": symbol, "qty": qty, "limit_price": close, "reason": "stop_or_time_exit"})

    open_symbols = set(managed) | set(positions)
    open_count = len(managed)
    slots = max(0, max_positions - open_count)
    if slots <= 0 or candidates.empty:
        return actions

    slot_value = account_equity * target_equity_pct / max_positions
    eligible = candidates[
        candidates["StockFilterOK"]
        & candidates["MarketFilterOK"]
        & candidates["EntryVolumeOK"]
        & candidates["CloseConfirmed"]
        & ~candidates["Symbol"].isin(open_symbols)
    ]
    for _, row in eligible.head(slots).iterrows():
        symbol = str(row["Symbol"])
        price = float(row["Close"])
        qty = int(slot_value // price)
        if qty <= 0:
            continue
        frame = frames[symbol]
        actions.append(
            {
                "action": "buy",
                "symbol": symbol,
                "qty": qty,
                "limit_price": price,
                "reason": "daily_close_breakout_volume_confirmed",
                "stop": float(row["StopPrice"]),
                "max_exit_date": trading_days_after(frame.index, pd.Timestamp(frame.index[-1]), 60),
                "signal": row.to_dict(),
            }
        )
    return actions


def main() -> None:
    parser = argparse.ArgumentParser(description="Cup & Handle Daily Alpaca paper scanner.")
    parser.add_argument("--env-file", default=".env.alpaca")
    parser.add_argument("--period", default="2y")
    parser.add_argument("--cache-path", default="data/cup_handle_signal_frames_2008_20260531.pkl")
    parser.add_argument("--live-download", action="store_true", help="Download fresh Yahoo data instead of using the local cached OHLCV file.")
    parser.add_argument("--batch-size", type=int, default=80)
    parser.add_argument("--pause-seconds", type=float, default=0.25)
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--min-score", type=float, default=45.0)
    parser.add_argument("--min-target-return-pct", type=float, default=30.0)
    parser.add_argument("--max-positions", type=int, default=3)
    parser.add_argument("--target-equity-pct", type=float, default=0.95)
    parser.add_argument("--limit-offset-pct", type=float, default=0.0)
    parser.add_argument("--extended-hours", action="store_true")
    parser.add_argument("--alpaca", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    load_env_file(Path(args.env_file))
    symbols = sp500_symbols()
    spx = latest_spx(args.period)
    frames = download_frames(symbols, args.period, args.batch_size, args.pause_seconds) if args.live_download else load_cached_frames(Path(args.cache_path), symbols)
    candidates = scan_candidates(frames, spx, args.min_score, args.min_target_return_pct, args.top_n)
    candidates.to_csv(SIGNAL_CSV, index=False)

    state = load_state()
    client = trading_client(paper=not args.live) if args.alpaca or args.execute else None
    positions = alpaca_positions(client) if client is not None else {}
    account_equity = float(getattr(client.get_account(), "equity", 100000.0)) if client is not None else 100000.0
    actions = build_actions(candidates, frames, state, positions, account_equity, args.max_positions, args.target_equity_pct)

    submitted: list[dict[str, Any]] = []
    if args.execute and client is not None:
        stamp = datetime.now().strftime("%Y%m%d")
        for action in actions:
            limit_price = float(action["limit_price"])
            if action["action"] == "buy":
                limit_price *= 1.0 + args.limit_offset_pct / 100.0
            else:
                limit_price *= 1.0 - args.limit_offset_pct / 100.0
            order = submit_order(
                client,
                symbol=action["symbol"],
                side=action["action"],
                qty=int(action["qty"]),
                limit_price=limit_price,
                extended_hours=args.extended_hours,
                client_order_id=f"cuphdl-{stamp}-{action['action']}-{action['symbol']}",
            )
            submitted.append({"symbol": action["symbol"], "action": action["action"], "qty": action["qty"], "order_id": str(order.id), "status": str(order.status)})
            if action["action"] == "buy":
                signal = action.get("signal", {})
                state["positions"][action["symbol"]] = {
                    "entry_date": signal.get("Date", datetime.now().strftime("%Y-%m-%d")),
                    "entry_price": round(float(action["limit_price"]), 4),
                    "qty": int(action["qty"]),
                    "stop": round(float(action["stop"]), 4),
                    "max_exit_date": action["max_exit_date"],
                    "signal": signal,
                }
            elif action["action"] == "sell":
                state["positions"].pop(action["symbol"], None)

    state["last_run"] = datetime.now().isoformat(timespec="seconds")
    save_state(state)
    run = {
        "name": "Cup & Handle Daily",
        "generated_at": state["last_run"],
        "paper": not args.live,
        "execute": args.execute,
        "symbols": len(symbols),
        "frames": len(frames),
        "candidates": 0 if candidates.empty else len(candidates),
        "actions": actions,
        "submitted": submitted,
        "signal_csv": str(SIGNAL_CSV),
    }
    RUN_JSON.write_text(json.dumps(run, indent=2, default=str), encoding="utf-8")
    print(json.dumps(run, indent=2, default=str))


if __name__ == "__main__":
    main()
