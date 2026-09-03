#!/usr/bin/env python3
"""Build a dated price layer for the standalone Multi Bagger dashboard.

The six-pass archive remains the system of record for rankings and scores. This
script writes a separate market-data file containing the regular-session close
on the snapshot's ``market_session_date``. It deliberately reuses the same
Yahoo Finance/yfinance data path already used by Stock Project V2, while keeping
the two dashboards and their stored outputs separate.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf


def _load_snapshot(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    stocks = payload.get("stocks")
    if not isinstance(stocks, list) or not stocks:
        raise ValueError("Snapshot must contain a non-empty stocks array")
    if not payload.get("market_session_date"):
        raise ValueError("Snapshot is missing market_session_date")

    tickers = [str(row.get("ticker", "")).strip().upper() for row in stocks]
    if any(not ticker for ticker in tickers):
        raise ValueError("Every stock must have a non-empty ticker")
    if len(tickers) != len(set(tickers)):
        raise ValueError("Snapshot contains duplicate tickers")
    return payload


def _ticker_frame(raw: pd.DataFrame, ticker: str) -> pd.DataFrame:
    if raw is None or raw.empty:
        return pd.DataFrame()
    if not isinstance(raw.columns, pd.MultiIndex):
        return raw.copy()

    level0 = raw.columns.get_level_values(0)
    level1 = raw.columns.get_level_values(1)
    if ticker in level0:
        return raw[ticker].copy()
    if ticker in level1:
        return raw.xs(ticker, axis=1, level=1).copy()
    return pd.DataFrame()


def _extract_close(frame: pd.DataFrame, target: date) -> tuple[date, float] | None:
    if frame is None or frame.empty or "Close" not in frame.columns:
        return None
    close = frame["Close"]
    if isinstance(close, pd.DataFrame):
        if close.empty:
            return None
        close = close.iloc[:, 0]
    close = pd.to_numeric(close, errors="coerce").dropna()
    if close.empty:
        return None

    dates = pd.to_datetime(close.index, errors="coerce")
    candidates: list[tuple[date, float]] = []
    for timestamp, value in zip(dates, close.to_numpy()):
        if pd.isna(timestamp):
            continue
        trading_date = timestamp.date()
        price = float(value)
        if trading_date <= target and math.isfinite(price) and price > 0:
            candidates.append((trading_date, price))
    return max(candidates, key=lambda item: item[0]) if candidates else None


def _download_prices(tickers: list[str], target: date, lookback_days: int) -> tuple[pd.DataFrame, str, str]:
    start = (target - timedelta(days=max(lookback_days, 7))).isoformat()
    end = (target + timedelta(days=2)).isoformat()
    raw = yf.download(
        tickers,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=False,
        group_by="ticker",
        threads=True,
        progress=False,
    )
    return raw, start, end


def _fallback_one(ticker: str, start: str, end: str) -> pd.DataFrame:
    try:
        return yf.download(
            ticker,
            start=start,
            end=end,
            interval="1d",
            auto_adjust=False,
            group_by="column",
            threads=False,
            progress=False,
        )
    except Exception:  # noqa: BLE001 - individual failures are recorded in output
        return pd.DataFrame()


def build(snapshot_path: Path, output_path: Path, lookback_days: int, minimum_coverage: float) -> dict[str, Any]:
    snapshot = _load_snapshot(snapshot_path)
    target = date.fromisoformat(str(snapshot["market_session_date"]))
    tickers = [str(row["ticker"]).strip().upper() for row in snapshot["stocks"]]
    raw, start, end = _download_prices(tickers, target, lookback_days)

    records: dict[str, dict[str, Any]] = {}
    for index, ticker in enumerate(tickers, start=1):
        result = _extract_close(_ticker_frame(raw, ticker), target)
        if result is None:
            result = _extract_close(_fallback_one(ticker, start, end), target)

        if result is None:
            record = {
                "ticker": ticker,
                "price_usd": None,
                "as_of": None,
                "currency": "USD",
                "basis": "regular_session_close",
                "status": "unavailable",
                "source": "Yahoo Finance via yfinance",
            }
        else:
            as_of, price = result
            record = {
                "ticker": ticker,
                "price_usd": round(price, 4),
                "as_of": as_of.isoformat(),
                "currency": "USD",
                "basis": "regular_session_close",
                "status": "ok" if as_of == target else "prior_session_fallback",
                "source": "Yahoo Finance via yfinance",
            }
        records[ticker] = record
        value = "" if record["price_usd"] is None else record["price_usd"]
        print(f"[{index:02d}/{len(tickers):02d}] {ticker}: {record['status']} {value}".rstrip())

    available = [ticker for ticker, record in records.items() if record["price_usd"] is not None]
    missing = [ticker for ticker in tickers if ticker not in available]
    coverage = len(available) / len(tickers)

    output = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "run_date": snapshot.get("run_date"),
        "market_session_date": target.isoformat(),
        "price_basis": "regular-session closing price for the Multi Bagger snapshot market session",
        "source": "Yahoo Finance via yfinance",
        "coverage": {
            "requested": len(tickers),
            "available": len(available),
            "coverage_pct": round(coverage * 100, 1),
            "missing": missing,
        },
        "prices": records,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if coverage < minimum_coverage:
        raise RuntimeError(
            f"Price coverage {coverage:.1%} is below the required {minimum_coverage:.1%}; missing={missing}"
        )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True, help="Canonical Multi Bagger latest.json")
    parser.add_argument("--output", type=Path, required=True, help="Destination price JSON")
    parser.add_argument("--lookback-days", type=int, default=12)
    parser.add_argument("--minimum-coverage", type=float, default=0.75)
    args = parser.parse_args()

    if not 0 <= args.minimum_coverage <= 1:
        parser.error("--minimum-coverage must be between 0 and 1")
    try:
        result = build(args.snapshot, args.output, args.lookback_days, args.minimum_coverage)
    except Exception as exc:  # noqa: BLE001 - CLI must report a concise deployment failure
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    coverage = result["coverage"]
    print(
        "Wrote price snapshot: "
        f"{coverage['available']}/{coverage['requested']} prices "
        f"for {result['market_session_date']} -> {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
