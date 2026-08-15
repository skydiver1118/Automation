from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest


SYMBOL = "SOXL"
DEFAULT_START = "2010-03-11"
OUTPUT_DIR = Path("reports")
DEFAULT_CSV = OUTPUT_DIR / "soxl_only_signal.csv"
DEFAULT_JSON = OUTPUT_DIR / "soxl_only_signal.json"
ENV_FILES = (Path(".env.alpaca"), Path(".env"))


@dataclass(frozen=True)
class StrategyConfig:
    symbol: str = SYMBOL
    fast_sma: int = 50
    slow_sma: int = 63
    stop_pct: float = 0.10
    start: str = DEFAULT_START
    interval: str = "1d"


@dataclass(frozen=True)
class AlpacaPosition:
    symbol: str
    qty: float
    avg_entry_price: float


@dataclass(frozen=True)
class SignalResult:
    agent: str
    symbol: str
    signal: str
    date: str
    close: float
    fast_sma: float
    slow_sma: float
    trend_on: bool
    previous_trend_on: bool
    has_position: bool
    position_source: str
    position_qty: float | None
    entry_price: float | None
    stop_price: float | None
    stop_hit: bool
    trend_exit: bool
    reason: str
    generated_at: str


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def load_env_files() -> None:
    for env_file in ENV_FILES:
        if not env_file.exists():
            continue
        for raw_line in env_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().lstrip("\ufeff")
            value = value.strip().strip("'").strip('"')
            if key and value and key not in os.environ:
                os.environ[key] = value


def create_trading_client(*, paper: bool) -> TradingClient:
    return TradingClient(
        api_key=require_env("ALPACA_API_KEY"),
        secret_key=require_env("ALPACA_SECRET_KEY"),
        paper=paper,
    )


def get_alpaca_position(client: TradingClient, symbol: str) -> AlpacaPosition | None:
    try:
        position = client.get_open_position(symbol)
    except Exception:
        return None

    qty = float(position.qty)
    return AlpacaPosition(
        symbol=symbol,
        qty=qty,
        avg_entry_price=float(position.avg_entry_price),
    )


def fetch_bars(config: StrategyConfig) -> pd.DataFrame:
    bars = yf.download(
        config.symbol,
        start=config.start,
        interval=config.interval,
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if isinstance(bars.columns, pd.MultiIndex):
        bars.columns = [column[0] for column in bars.columns]
    bars = bars.dropna(subset=["Close"]).copy()
    bars.index = pd.to_datetime(bars.index).tz_localize(None)
    return bars


def add_strategy_columns(bars: pd.DataFrame, config: StrategyConfig) -> pd.DataFrame:
    out = bars.copy()
    close = out["Close"]
    out["fast_sma"] = close.rolling(config.fast_sma).mean()
    out["slow_sma"] = close.rolling(config.slow_sma).mean()
    out["trend_on"] = out["fast_sma"] > out["slow_sma"]
    return out.dropna(subset=["fast_sma", "slow_sma"])


def reconstruct_local_position(bars: pd.DataFrame, config: StrategyConfig) -> tuple[bool, float | None, pd.Timestamp | None]:
    in_position = False
    entry_price: float | None = None
    entry_date: pd.Timestamp | None = None

    for ts, row in bars.iterrows():
        close = float(row["Close"])
        trend_on = bool(row["trend_on"])

        if not in_position and trend_on:
            in_position = True
            entry_price = close
            entry_date = ts

        if in_position and entry_price is not None:
            stop_hit = close <= entry_price * (1 - config.stop_pct)
            trend_exit = not trend_on
            if stop_hit or trend_exit:
                in_position = False
                entry_price = None
                entry_date = None

    return in_position, entry_price, entry_date


def build_signal(
    bars: pd.DataFrame,
    config: StrategyConfig,
    *,
    agent: str,
    alpaca_position: AlpacaPosition | None = None,
) -> SignalResult:
    if len(bars) < 2:
        raise RuntimeError("Not enough bars after SMA warmup.")

    last = bars.iloc[-1]
    previous = bars.iloc[-2]
    close = float(last["Close"])
    trend_on = bool(last["trend_on"])
    previous_trend_on = bool(previous["trend_on"])

    local_has_position, local_entry_price, _ = reconstruct_local_position(bars.iloc[:-1], config)

    if alpaca_position is not None and alpaca_position.qty > 0:
        has_position = True
        entry_price = alpaca_position.avg_entry_price
        position_qty = alpaca_position.qty
        position_source = "alpaca"
    else:
        has_position = local_has_position
        entry_price = local_entry_price
        position_qty = None
        position_source = "local_reconstruction"

    stop_price = entry_price * (1 - config.stop_pct) if entry_price is not None else None
    stop_hit = has_position and stop_price is not None and close <= stop_price
    trend_exit = has_position and not trend_on

    if trend_exit or stop_hit:
        signal = "SELL"
        reasons = []
        if trend_exit:
            reasons.append(f"SMA{config.fast_sma} <= SMA{config.slow_sma}")
        if stop_hit:
            reasons.append(f"close <= {config.stop_pct:.0%} stop")
        reason = "; ".join(reasons)
    elif not has_position and trend_on:
        signal = "BUY"
        reason = f"SMA{config.fast_sma} > SMA{config.slow_sma}; strategy state is long"
    else:
        signal = "HOLD"
        reason = "already aligned with strategy state" if has_position else "strategy state is flat"

    return SignalResult(
        agent=agent,
        symbol=config.symbol,
        signal=signal,
        date=pd.Timestamp(bars.index[-1]).date().isoformat(),
        close=round(close, 4),
        fast_sma=round(float(last["fast_sma"]), 4),
        slow_sma=round(float(last["slow_sma"]), 4),
        trend_on=trend_on,
        previous_trend_on=previous_trend_on,
        has_position=has_position,
        position_source=position_source,
        position_qty=position_qty,
        entry_price=round(entry_price, 4) if entry_price is not None else None,
        stop_price=round(stop_price, 4) if stop_price is not None else None,
        stop_hit=bool(stop_hit),
        trend_exit=bool(trend_exit),
        reason=reason,
        generated_at=datetime.now().astimezone().isoformat(timespec="seconds"),
    )


def submit_alpaca_order(
    client: TradingClient,
    signal: SignalResult,
    *,
    qty: float,
    current_position: AlpacaPosition | None,
    extended_hours: bool,
    limit_offset_pct: float,
    execute_buy_only: bool,
) -> Any | None:
    def limit_price_for(side: OrderSide) -> float:
        offset = limit_offset_pct / 100
        if side == OrderSide.BUY:
            return round(signal.close * (1 + offset), 2)
        return round(signal.close * (1 - offset), 2)

    def build_order(side: OrderSide, order_qty: float):
        if extended_hours:
            return LimitOrderRequest(
                symbol=signal.symbol,
                qty=order_qty,
                side=side,
                time_in_force=TimeInForce.DAY,
                limit_price=limit_price_for(side),
                extended_hours=True,
            )

        return MarketOrderRequest(
            symbol=signal.symbol,
            qty=order_qty,
            side=side,
            time_in_force=TimeInForce.DAY,
        )

    if signal.signal == "BUY":
        if current_position is not None and current_position.qty > 0:
            return None
        return client.submit_order(build_order(OrderSide.BUY, qty))

    if signal.signal == "SELL":
        if execute_buy_only:
            return None
        if current_position is None or current_position.qty <= 0:
            return None
        return client.submit_order(build_order(OrderSide.SELL, abs(current_position.qty)))

    return None


def write_outputs(signal: SignalResult, csv_path: Path, json_path: Path) -> None:
    csv_path.parent.mkdir(exist_ok=True)
    json_path.parent.mkdir(exist_ok=True)

    row = asdict(signal)
    pd.DataFrame([row]).to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(row, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily SOXL-only SMA50/SMA63 + 10% stop signal scanner.")
    parser.add_argument("--agent", default="SOXL only", help="Agent name to stamp into output files.")
    parser.add_argument("--start", default=DEFAULT_START, help="Start date for yfinance history.")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Signal CSV output path.")
    parser.add_argument("--json", default=str(DEFAULT_JSON), help="Signal JSON output path.")
    parser.add_argument("--alpaca", action="store_true", help="Read the current SOXL position from Alpaca.")
    parser.add_argument("--execute", action="store_true", help="Submit the generated BUY/SELL order to Alpaca.")
    parser.add_argument(
        "--execute-buy-only",
        action="store_true",
        help="When used with --execute, submit only BUY orders and never submit SELL orders.",
    )
    parser.add_argument(
        "--extended-hours",
        action="store_true",
        help="Use an Alpaca extended-hours DAY limit order instead of a regular market order.",
    )
    parser.add_argument(
        "--limit-offset-pct",
        type=float,
        default=0.0,
        help=(
            "Limit offset from latest close for extended-hours orders. "
            "Buy limit = close * (1 + offset); sell limit = close * (1 - offset)."
        ),
    )
    parser.add_argument("--live", action="store_true", help="Use Alpaca live trading. Default is paper trading.")
    parser.add_argument("--qty", type=float, default=1.0, help="SOXL shares to buy on BUY signals.")
    args = parser.parse_args()
    load_env_files()

    config = StrategyConfig(start=args.start)
    bars = add_strategy_columns(fetch_bars(config), config)

    client: TradingClient | None = None
    alpaca_position: AlpacaPosition | None = None
    if args.alpaca or args.execute:
        client = create_trading_client(paper=not args.live)
        alpaca_position = get_alpaca_position(client, config.symbol)

    signal = build_signal(
        bars,
        config,
        agent=args.agent,
        alpaca_position=alpaca_position,
    )
    write_outputs(signal, Path(args.csv), Path(args.json))

    print(pd.DataFrame([asdict(signal)]).to_string(index=False))
    print(f"\nwrote_csv={Path(args.csv)}")
    print(f"wrote_json={Path(args.json)}")

    if not args.execute:
        print("\nDry run: no Alpaca order submitted. Add --execute to submit BUY/SELL orders.")
        return

    assert client is not None
    submitted = submit_alpaca_order(
        client,
        signal,
        qty=args.qty,
        current_position=alpaca_position,
        extended_hours=args.extended_hours,
        limit_offset_pct=args.limit_offset_pct,
        execute_buy_only=args.execute_buy_only,
    )
    if submitted is None:
        print(f"\nNo Alpaca order needed for signal={signal.signal}.")
        return

    print(
        "\nsubmitted_order "
        f"id={submitted.id} "
        f"symbol={submitted.symbol} "
        f"side={submitted.side} "
        f"qty={submitted.qty} "
        f"limit_price={getattr(submitted, 'limit_price', None)} "
        f"extended_hours={getattr(submitted, 'extended_hours', None)} "
        f"status={submitted.status}"
    )


if __name__ == "__main__":
    main()
