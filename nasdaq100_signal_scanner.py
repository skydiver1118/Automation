import argparse
from dataclasses import dataclass
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf


NASDAQ_100_URL = "https://en.wikipedia.org/wiki/Nasdaq-100"
SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
OUTPUT_DIR = Path("reports")


@dataclass(frozen=True)
class SignalConfig:
    period: str = "1y"
    interval: str = "1d"
    stop_loss_pct: float = 0.08
    trailing_stop_pct: float = 0.10
    max_holding_bars: int = 20


def load_positions(path: str | None) -> dict[str, dict[str, object]]:
    if not path:
        return {}

    positions = pd.read_csv(path)
    required = {"symbol", "entry_date", "entry_price"}
    missing = required - set(positions.columns)
    if missing:
        raise RuntimeError(f"Position file is missing columns: {', '.join(sorted(missing))}")

    if "highest_close" not in positions.columns:
        positions["highest_close"] = pd.NA

    positions["symbol"] = positions["symbol"].astype(str).str.upper()
    return positions.set_index("symbol").to_dict(orient="index")


def read_html_tables(url: str) -> list[pd.DataFrame]:
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 nasdaq100-signal-scanner/1.0"},
        timeout=30,
    )
    response.raise_for_status()
    return pd.read_html(StringIO(response.text))


def load_nasdaq100_symbols(limit: int | None = None) -> list[str]:
    tables = read_html_tables(NASDAQ_100_URL)
    symbols: list[str] = []

    for table in tables:
        columns = {str(column).lower(): column for column in table.columns}
        ticker_column = columns.get("ticker")
        if ticker_column is None:
            continue
        symbols = table[ticker_column].astype(str).str.replace(".", "-", regex=False).tolist()
        break

    if not symbols:
        raise RuntimeError("Could not find Nasdaq-100 ticker table.")

    return symbols[:limit] if limit else symbols


def load_sp500_symbols(limit: int | None = None) -> list[str]:
    tables = read_html_tables(SP500_URL)
    symbols: list[str] = []

    for table in tables:
        columns = {str(column).lower(): column for column in table.columns}
        symbol_column = columns.get("symbol")
        if symbol_column is None:
            continue
        symbols = table[symbol_column].astype(str).str.replace(".", "-", regex=False).tolist()
        break

    if not symbols:
        raise RuntimeError("Could not find S&P 500 symbol table.")

    return symbols[:limit] if limit else symbols


def load_symbols(universe: str, limit: int | None = None) -> list[str]:
    if universe == "nasdaq100":
        return load_nasdaq100_symbols(limit=limit)
    if universe == "sp500":
        return load_sp500_symbols(limit=limit)
    raise ValueError(f"Unsupported universe: {universe}")


def rsi(close: pd.Series, length: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    avg_loss = loss.ewm(alpha=1 / length, adjust=False, min_periods=length).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    return 100 - (100 / (1 + rs))


def add_indicators(bars: pd.DataFrame) -> pd.DataFrame:
    bars = bars.copy()
    close = bars["Close"]
    bars["ema_9"] = close.ewm(span=9, adjust=False).mean()
    bars["ema_21"] = close.ewm(span=21, adjust=False).mean()
    bars["ema_200"] = close.ewm(span=200, adjust=False).mean()
    bars["rsi_14"] = rsi(close)
    bars["volume_ma20"] = bars["Volume"].rolling(20).mean()
    return bars


def evaluate_symbol(symbol: str, config: SignalConfig, position: dict[str, object] | None = None) -> dict[str, object]:
    bars = yf.Ticker(symbol).history(period=config.period, interval=config.interval, auto_adjust=False)
    if len(bars) < 220:
        return {
            "symbol": symbol,
            "signal": "SKIP",
            "reason": f"not enough bars: {len(bars)}",
        }

    bars = add_indicators(bars).dropna()
    if len(bars) < 2:
        return {"symbol": symbol, "signal": "SKIP", "reason": "not enough indicator bars"}

    prev = bars.iloc[-2]
    last = bars.iloc[-1]

    ema_cross_up = prev["ema_9"] <= prev["ema_21"] and last["ema_9"] > last["ema_21"]
    ema_cross_down = prev["ema_9"] >= prev["ema_21"] and last["ema_9"] < last["ema_21"]
    price_above_200 = last["Close"] > last["ema_200"]
    rsi_buy_zone = 50 <= last["rsi_14"] <= 70
    volume_confirmed = last["Volume"] > last["volume_ma20"]
    rsi_reversal = prev["rsi_14"] >= 70 and last["rsi_14"] < 70
    price_reversal = last["Close"] < last["ema_21"] and last["rsi_14"] < prev["rsi_14"]
    stop_loss_hit = False
    trailing_stop_hit = False
    max_holding_hit = False
    holding_bars = pd.NA

    if position:
        entry_date = pd.Timestamp(position["entry_date"])
        entry_price = float(position["entry_price"])
        held_bars = bars[bars.index >= entry_date]
        holding_bars = len(held_bars)
        observed_highest_close = held_bars["Close"].max() if not held_bars.empty else last["Close"]
        saved_highest_close = position.get("highest_close")
        if pd.notna(saved_highest_close):
            highest_close = max(float(saved_highest_close), float(observed_highest_close))
        else:
            highest_close = float(observed_highest_close)

        stop_loss_hit = last["Close"] <= entry_price * (1 - config.stop_loss_pct)
        trailing_stop_hit = last["Close"] <= highest_close * (1 - config.trailing_stop_pct)
        max_holding_hit = holding_bars >= config.max_holding_bars

    buy = ema_cross_up and price_above_200 and rsi_buy_zone and volume_confirmed
    sell = ema_cross_down or rsi_reversal or price_reversal or stop_loss_hit or trailing_stop_hit or max_holding_hit

    reasons: list[str] = []
    if buy:
        signal = "BUY"
        reasons = [
            "close > ema_200",
            "ema_9 crossed above ema_21",
            "rsi_14 between 50 and 70",
            "volume > volume_ma20",
        ]
    elif sell:
        signal = "SELL"
        if ema_cross_down:
            reasons.append("ema_9 crossed below ema_21")
        if rsi_reversal:
            reasons.append("rsi_14 reversed below 70")
        if price_reversal:
            reasons.append("close < ema_21 with falling rsi_14")
        if stop_loss_hit:
            reasons.append(f"{config.stop_loss_pct:.0%} stop loss hit")
        if trailing_stop_hit:
            reasons.append(f"{config.trailing_stop_pct:.0%} trailing stop hit")
        if max_holding_hit:
            reasons.append(f"max holding bars hit: {holding_bars}")
    else:
        signal = "HOLD"
        reasons.append("no trigger")

    return {
        "symbol": symbol,
        "signal": signal,
        "reason": "; ".join(reasons),
        "date": bars.index[-1].date().isoformat(),
        "close": round(float(last["Close"]), 2),
        "ema_9": round(float(last["ema_9"]), 2),
        "ema_21": round(float(last["ema_21"]), 2),
        "ema_200": round(float(last["ema_200"]), 2),
        "rsi_14": round(float(last["rsi_14"]), 2),
        "volume": int(last["Volume"]),
        "volume_ma20": int(last["volume_ma20"]),
        "has_position": bool(position),
        "holding_bars": holding_bars,
        "buy_setup_score": int(price_above_200) + int(last["ema_9"] > last["ema_21"]) + int(rsi_buy_zone) + int(volume_confirmed),
        "ema_9_above_21": bool(last["ema_9"] > last["ema_21"]),
        "price_above_200": bool(price_above_200),
        "rsi_buy_zone": bool(rsi_buy_zone),
        "volume_confirmed": bool(volume_confirmed),
    }


def scan(
    config: SignalConfig,
    universe: str = "nasdaq100",
    limit: int | None = None,
    positions_path: str | None = None,
) -> pd.DataFrame:
    symbols = load_symbols(universe=universe, limit=limit)
    positions = load_positions(positions_path)
    rows = []

    for index, symbol in enumerate(symbols, start=1):
        print(f"[{index:03d}/{len(symbols):03d}] scanning {symbol}")
        try:
            rows.append(evaluate_symbol(symbol, config, position=positions.get(symbol)))
        except Exception as exc:
            rows.append({"symbol": symbol, "signal": "ERROR", "reason": str(exc)})

    signal_order = {"BUY": 0, "SELL": 1, "HOLD": 2, "SKIP": 3, "ERROR": 4}
    result = pd.DataFrame(rows)
    return result.sort_values(
        by=["signal", "symbol"],
        key=lambda column: column.map(signal_order).fillna(99) if column.name == "signal" else column,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan stocks for EMA/RSI/volume signals.")
    parser.add_argument("--universe", choices=["nasdaq100", "sp500"], default="nasdaq100")
    parser.add_argument("--limit", type=int, default=None, help="Scan only the first N symbols for a quick test.")
    parser.add_argument("--period", default="1y", help="yfinance history period, for example 1y or 2y.")
    parser.add_argument("--interval", default="1d", help="yfinance bar interval, for example 1d or 1h.")
    parser.add_argument("--output", default=None, help="Optional CSV output path.")
    parser.add_argument(
        "--positions",
        default=None,
        help="Optional CSV with symbol,entry_date,entry_price,highest_close for stop/trailing/max-hold exits.",
    )
    args = parser.parse_args()

    config = SignalConfig(period=args.period, interval=args.interval)
    results = scan(config=config, universe=args.universe, limit=args.limit, positions_path=args.positions)

    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = Path(args.output) if args.output else OUTPUT_DIR / f"{args.universe}_signals.csv"
    results.to_csv(output_path, index=False)

    print("\nSignal summary:")
    print(results["signal"].value_counts().to_string())
    print(f"\nSaved: {output_path}")
    print("\nTop signals:")
    print(results.head(20).to_string(index=False))
    print("\nClosest buy setups:")
    watchlist_columns = [
        "symbol",
        "signal",
        "buy_setup_score",
        "close",
        "ema_9",
        "ema_21",
        "ema_200",
        "rsi_14",
        "volume",
        "volume_ma20",
        "reason",
    ]
    watchlist = results.sort_values(["buy_setup_score", "rsi_14"], ascending=[False, False])
    print(watchlist[watchlist_columns].head(20).to_string(index=False))


if __name__ == "__main__":
    main()
