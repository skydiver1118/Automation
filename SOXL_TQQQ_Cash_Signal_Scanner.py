from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest


SYMBOLS = ["SOXL", "TQQQ"]
CONTEXT_SYMBOLS = ["SOXL", "TQQQ", "QQQ"]
DEFAULT_START = "2010-03-11"
OUTPUT_DIR = Path("reports")
DEFAULT_CSV = OUTPUT_DIR / "soxl_tqqq_cash_signal.csv"
DEFAULT_JSON = OUTPUT_DIR / "soxl_tqqq_cash_signal.json"


@dataclass(frozen=True)
class StrategyConfig:
    start: str = DEFAULT_START
    interval: str = "1d"
    rotation_lookback: int = 63
    rotation_skip: int = 10
    rotation_trend_sma: int = 50
    rotation_hysteresis: float = 0.05
    cash_sma: int = 150
    cash_exit_buffer: float = 0.00
    cash_reentry_buffer: float = 0.01


@dataclass(frozen=True)
class AlpacaPosition:
    symbol: str
    qty: float
    avg_entry_price: float


@dataclass(frozen=True)
class SignalResult:
    agent: str
    date: str
    target: str
    previous_target: str
    base_rotation_target: str
    signal: str
    action_summary: str
    soxl_close: float
    tqqq_close: float
    qqq_close: float
    selected_close: float | None
    selected_sma150: float | None
    qqq_sma150: float | None
    risk_on: bool
    selected_trend_ok: bool
    qqq_trend_ok: bool
    cash_rule: str
    alpaca_positions: str
    position_source: str
    generated_at: str


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


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


def create_trading_client(*, paper: bool) -> TradingClient:
    return TradingClient(
        api_key=require_env("ALPACA_API_KEY"),
        secret_key=require_env("ALPACA_SECRET_KEY"),
        paper=paper,
    )


def get_positions(client: TradingClient) -> dict[str, AlpacaPosition]:
    positions: dict[str, AlpacaPosition] = {}
    for symbol in SYMBOLS:
        try:
            position = client.get_open_position(symbol)
        except Exception:
            continue
        qty = float(position.qty)
        if qty != 0:
            positions[symbol] = AlpacaPosition(
                symbol=symbol,
                qty=qty,
                avg_entry_price=float(position.avg_entry_price),
            )
    return positions


def fetch_bars(config: StrategyConfig) -> pd.DataFrame:
    bars = yf.download(
        CONTEXT_SYMBOLS,
        start=config.start,
        interval=config.interval,
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if bars.empty:
        raise RuntimeError("No price data returned by yfinance.")
    close = bars["Close"] if isinstance(bars.columns, pd.MultiIndex) else bars[["Close"]]
    close = close[CONTEXT_SYMBOLS].dropna().copy()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


def relative_momentum_score(close: pd.DataFrame, config: StrategyConfig) -> pd.DataFrame:
    prices = close[SYMBOLS]
    lookback = config.rotation_lookback
    skip = config.rotation_skip
    score_return = prices.shift(skip) / prices.shift(lookback + skip) - 1
    daily_returns = prices.pct_change().shift(skip)
    vol = daily_returns.rolling(max(lookback, 10)).std() * np.sqrt(252)
    return score_return - 0.5 * vol


def apply_hysteresis(raw: pd.Series, diff: pd.Series, threshold: float) -> pd.Series:
    current: str | None = None
    values: list[str | None] = []
    for ts, choice in raw.items():
        if pd.isna(choice):
            values.append(current)
            continue
        choice = str(choice)
        if current is None:
            current = choice
        elif choice != current and abs(float(diff.loc[ts])) >= threshold:
            current = choice
        values.append(current)
    return pd.Series(values, index=raw.index).ffill()


def build_base_rotation(close: pd.DataFrame, config: StrategyConfig) -> pd.Series:
    score = relative_momentum_score(close, config)
    diff = score["SOXL"] - score["TQQQ"]
    raw = pd.Series(np.where(diff >= 0, "SOXL", "TQQQ"), index=close.index)
    raw[~np.isfinite(diff)] = None

    trend = close[SYMBOLS] > close[SYMBOLS].rolling(config.rotation_trend_sma).mean()
    adjusted: list[str | None] = []
    for ts, choice in raw.items():
        if choice is None or pd.isna(choice):
            adjusted.append(None)
            continue
        choice = str(choice)
        other = "TQQQ" if choice == "SOXL" else "SOXL"
        if bool(trend.loc[ts, choice]) or not bool(trend.loc[ts, other]):
            adjusted.append(choice)
        else:
            adjusted.append(other)
    selected = apply_hysteresis(pd.Series(adjusted, index=close.index), diff.fillna(0), config.rotation_hysteresis)

    month = pd.Series(close.index.to_period("M"), index=close.index)
    rebalance = month.ne(month.shift(1))
    monthly = selected.where(rebalance).ffill()
    return monthly.ffill()


def cash_filtered_targets(close: pd.DataFrame, base_target: pd.Series, config: StrategyConfig) -> pd.Series:
    sma_assets = close[SYMBOLS].rolling(config.cash_sma).mean()
    qqq_sma = close["QQQ"].rolling(config.cash_sma).mean()
    targets: list[str] = []
    risk_on = True
    current = "CASH"
    for ts, selected in base_target.items():
        if pd.isna(selected):
            targets.append(current)
            continue
        selected = str(selected)
        selected_exit = close.loc[ts, selected] < sma_assets.loc[ts, selected] * (1 - config.cash_exit_buffer)
        qqq_exit = close.loc[ts, "QQQ"] < qqq_sma.loc[ts] * (1 - config.cash_exit_buffer)
        selected_reentry = close.loc[ts, selected] >= sma_assets.loc[ts, selected] * (1 + config.cash_reentry_buffer)
        qqq_reentry = close.loc[ts, "QQQ"] >= qqq_sma.loc[ts] * (1 + config.cash_reentry_buffer)

        if risk_on and selected_exit and qqq_exit:
            current = "CASH"
            risk_on = False
        elif not risk_on:
            if selected_reentry or qqq_reentry:
                current = selected
                risk_on = True
            else:
                current = "CASH"
        else:
            current = selected
        targets.append(current)
    return pd.Series(targets, index=close.index).ffill().fillna("CASH")


def build_signal(
    close: pd.DataFrame,
    config: StrategyConfig,
    *,
    agent: str,
    alpaca_positions: dict[str, AlpacaPosition] | None = None,
) -> SignalResult:
    base = build_base_rotation(close, config)
    targets = cash_filtered_targets(close, base, config)
    if len(targets.dropna()) < 2:
        raise RuntimeError("Not enough data after indicator warmup.")

    last_ts = targets.index[-1]
    prev_ts = targets.index[-2]
    target = str(targets.loc[last_ts])
    previous_target = str(targets.loc[prev_ts])
    base_target = str(base.loc[last_ts])
    current_positions = alpaca_positions or {}
    held = [symbol for symbol, pos in current_positions.items() if pos.qty > 0]
    held_text = "; ".join(f"{symbol}:{pos.qty:g}@{pos.avg_entry_price:.4f}" for symbol, pos in current_positions.items()) or "none"

    selected_close = None if target == "CASH" else float(close.loc[last_ts, target])
    selected_sma = None if target == "CASH" else float(close[target].rolling(config.cash_sma).mean().loc[last_ts])
    qqq_sma = float(close["QQQ"].rolling(config.cash_sma).mean().loc[last_ts])
    selected_trend_ok = False if target == "CASH" else bool(selected_close is not None and selected_sma is not None and selected_close >= selected_sma)
    qqq_trend_ok = bool(float(close.loc[last_ts, "QQQ"]) >= qqq_sma)

    if target == "CASH":
        signal = "SELL" if held else "HOLD"
        action_summary = "Target is CASH; sell SOXL/TQQQ positions." if held else "Target is CASH; no SOXL/TQQQ position detected."
    elif target in held and len(held) == 1:
        signal = "HOLD"
        action_summary = f"Already aligned with target {target}."
    else:
        signal = "BUY" if not held else "ROTATE"
        action_summary = f"Target is {target}; sell non-target SOXL/TQQQ positions and buy {target}."

    return SignalResult(
        agent=agent,
        date=pd.Timestamp(last_ts).date().isoformat(),
        target=target,
        previous_target=previous_target,
        base_rotation_target=base_target,
        signal=signal,
        action_summary=action_summary,
        soxl_close=round(float(close.loc[last_ts, "SOXL"]), 4),
        tqqq_close=round(float(close.loc[last_ts, "TQQQ"]), 4),
        qqq_close=round(float(close.loc[last_ts, "QQQ"]), 4),
        selected_close=round(selected_close, 4) if selected_close is not None else None,
        selected_sma150=round(selected_sma, 4) if selected_sma is not None else None,
        qqq_sma150=round(qqq_sma, 4),
        risk_on=target != "CASH",
        selected_trend_ok=selected_trend_ok,
        qqq_trend_ok=qqq_trend_ok,
        cash_rule="Risk-off only when selected ETF and QQQ are both below SMA150; re-enter when either is above SMA150 + 1%.",
        alpaca_positions=held_text,
        position_source="alpaca" if alpaca_positions is not None else "signal_only",
        generated_at=datetime.now().astimezone().isoformat(timespec="seconds"),
    )


def limit_price(close: float, side: OrderSide, offset_pct: float) -> float:
    offset = offset_pct / 100
    if side == OrderSide.BUY:
        return round(close * (1 + offset), 2)
    return round(close * (1 - offset), 2)


def submit_orders(
    client: TradingClient,
    signal: SignalResult,
    positions: dict[str, AlpacaPosition],
    *,
    qty: float,
    extended_hours: bool,
    limit_offset_pct: float,
) -> list[Any]:
    submitted = []

    def order(symbol: str, side: OrderSide, order_qty: float, close_price: float):
        if extended_hours:
            return LimitOrderRequest(
                symbol=symbol,
                qty=order_qty,
                side=side,
                time_in_force=TimeInForce.DAY,
                limit_price=limit_price(close_price, side, limit_offset_pct),
                extended_hours=True,
            )
        return MarketOrderRequest(
            symbol=symbol,
            qty=order_qty,
            side=side,
            time_in_force=TimeInForce.DAY,
        )

    close_by_symbol = {"SOXL": signal.soxl_close, "TQQQ": signal.tqqq_close}
    for symbol, position in positions.items():
        if signal.target == symbol:
            continue
        submitted.append(client.submit_order(order(symbol, OrderSide.SELL, abs(position.qty), close_by_symbol[symbol])))

    if signal.target in SYMBOLS and signal.target not in positions:
        submitted.append(client.submit_order(order(signal.target, OrderSide.BUY, qty, close_by_symbol[signal.target])))

    return submitted


def write_outputs(signal: SignalResult, csv_path: Path, json_path: Path) -> None:
    csv_path.parent.mkdir(exist_ok=True)
    json_path.parent.mkdir(exist_ok=True)
    row = asdict(signal)
    pd.DataFrame([row]).to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(row, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily SOXL/TQQQ rotation-with-cash signal scanner.")
    parser.add_argument("--agent", default="SOXL/TQQQ Rotation with cash", help="Agent name to stamp into output files.")
    parser.add_argument("--start", default=DEFAULT_START, help="Start date for yfinance history.")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Signal CSV output path.")
    parser.add_argument("--json", default=str(DEFAULT_JSON), help="Signal JSON output path.")
    parser.add_argument("--alpaca", action="store_true", help="Read current SOXL/TQQQ positions from Alpaca.")
    parser.add_argument("--execute", action="store_true", help="Submit required BUY/SELL orders to Alpaca.")
    parser.add_argument("--extended-hours", action="store_true", help="Use Alpaca DAY limit orders with extended_hours=True.")
    parser.add_argument("--limit-offset-pct", type=float, default=0.0, help="Limit offset from latest close for extended-hours orders.")
    parser.add_argument("--live", action="store_true", help="Use Alpaca live trading. Default is paper trading.")
    parser.add_argument("--qty", type=float, default=1.0, help="Target shares to buy when target is SOXL or TQQQ.")
    parser.add_argument("--env-file", default=".env.alpaca", help="Optional env file containing ALPACA_API_KEY and ALPACA_SECRET_KEY.")
    args = parser.parse_args()

    config = StrategyConfig(start=args.start)
    load_env_file(Path(args.env_file))
    client: TradingClient | None = None
    positions: dict[str, AlpacaPosition] | None = None
    if args.alpaca or args.execute:
        client = create_trading_client(paper=not args.live)
        positions = get_positions(client)

    signal = build_signal(fetch_bars(config), config, agent=args.agent, alpaca_positions=positions)
    write_outputs(signal, Path(args.csv), Path(args.json))

    print(pd.DataFrame([asdict(signal)]).to_string(index=False))
    print(f"\nwrote_csv={Path(args.csv)}")
    print(f"wrote_json={Path(args.json)}")

    if not args.execute:
        print("\nDry run: no Alpaca orders submitted. Add --execute to submit target-alignment orders.")
        return

    assert client is not None
    submitted = submit_orders(
        client,
        signal,
        positions or {},
        qty=args.qty,
        extended_hours=args.extended_hours,
        limit_offset_pct=args.limit_offset_pct,
    )
    if not submitted:
        print("\nNo Alpaca order needed; current SOXL/TQQQ positions already match target.")
        return
    for order_result in submitted:
        print(
            "\nsubmitted_order "
            f"id={order_result.id} "
            f"symbol={order_result.symbol} "
            f"side={order_result.side} "
            f"qty={order_result.qty} "
            f"limit_price={getattr(order_result, 'limit_price', None)} "
            f"extended_hours={getattr(order_result, 'extended_hours', None)} "
            f"status={order_result.status}"
        )


if __name__ == "__main__":
    main()
