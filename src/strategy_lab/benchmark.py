from __future__ import annotations

import argparse
from datetime import datetime, date, timedelta

import yfinance as yf


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def benchmark_return(symbol: str, start: date, end: date) -> tuple[str, str, float]:
    data = yf.download(
        symbol,
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        auto_adjust=True,
        progress=False,
    )
    close = data["Close"].dropna()
    if hasattr(close, "columns"):
        close = close.iloc[:, 0].dropna()
    if close.empty:
        raise RuntimeError(f"No benchmark data downloaded for {symbol}")
    return close.index[0].date().isoformat(), close.index[-1].date().isoformat(), float(close.iloc[-1] / close.iloc[0] - 1.0)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch adjusted benchmark return from Yahoo Finance.")
    parser.add_argument("symbols", nargs="+")
    parser.add_argument("--start", type=parse_date, required=True)
    parser.add_argument("--end", type=parse_date, required=True)
    args = parser.parse_args()

    for symbol in args.symbols:
        start, end, total_return = benchmark_return(symbol, args.start, args.end)
        print(f"{symbol},{start},{end},{total_return:.10f}")


if __name__ == "__main__":
    main()
