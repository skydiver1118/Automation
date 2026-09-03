#!/usr/bin/env python3
"""Build a dated stock-price layer for the standalone Multi Bagger dashboard.

The six-pass research archive remains the system of record for rankings and scores.
This script writes a separate, reproducible market-data file containing the regular-
session closing price on (or, defensively, immediately before) the snapshot's
``market_session_date``.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from datetime import date, datetime, time as dt_time, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

HOSTS = ("query1.finance.yahoo.com", "query2.finance.yahoo.com")
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
)


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


def _epoch_start(day: date) -> int:
    return int(datetime.combine(day, dt_time.min, tzinfo=timezone.utc).timestamp())


def _session_date(timestamp: int, timezone_name: str | None) -> date:
    try:
        market_tz = ZoneInfo(timezone_name or "America/New_York")
    except ZoneInfoNotFoundError:
        market_tz = ZoneInfo("America/New_York")
    return datetime.fromtimestamp(timestamp, timezone.utc).astimezone(market_tz).date()


def _fetch_price(ticker: str, target: date, lookback_days: int) -> dict[str, Any]:
    start = target - timedelta(days=max(lookback_days, 7))
    end = target + timedelta(days=2)
    params = urlencode(
        {
            "period1": _epoch_start(start),
            "period2": _epoch_start(end),
            "interval": "1d",
            "events": "history",
            "includeAdjustedClose": "true",
        }
    )
    errors: list[str] = []

    for host in HOSTS:
        url = f"https://{host}/v8/finance/chart/{quote(ticker)}?{params}"
        request = Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json,text/plain,*/*",
                "Referer": f"https://finance.yahoo.com/quote/{quote(ticker)}/history/",
            },
        )
        try:
            with urlopen(request, timeout=25) as response:
                payload = json.load(response)
            chart = payload.get("chart") or {}
            if chart.get("error"):
                raise ValueError(str(chart["error"]))
            results = chart.get("result") or []
            if not results:
                raise ValueError("chart.result is empty")

            result = results[0]
            meta = result.get("meta") or {}
            timestamps = result.get("timestamp") or []
            quotes = ((result.get("indicators") or {}).get("quote") or [{}])[0]
            closes = quotes.get("close") or []
            timezone_name = meta.get("exchangeTimezoneName")

            candidates: list[tuple[date, float]] = []
            for timestamp, close_value in zip(timestamps, closes):
                if close_value is None:
                    continue
                price = float(close_value)
                if not math.isfinite(price) or price <= 0:
                    continue
                trading_date = _session_date(int(timestamp), timezone_name)
                if trading_date <= target:
                    candidates.append((trading_date, price))

            if not candidates:
                raise ValueError(f"No valid close on or before {target.isoformat()}")

            as_of, price = max(candidates, key=lambda item: item[0])
            return {
                "ticker": ticker,
                "price_usd": round(price, 4),
                "as_of": as_of.isoformat(),
                "currency": str(meta.get("currency") or "USD"),
                "basis": "regular_session_close",
                "status": "ok" if as_of == target else "prior_session_fallback",
                "source": "Yahoo Finance chart endpoint",
            }
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"{host}: {type(exc).__name__}: {exc}")
            time.sleep(0.25)

    return {
        "ticker": ticker,
        "price_usd": None,
        "as_of": None,
        "currency": "USD",
        "basis": "regular_session_close",
        "status": "unavailable",
        "source": "Yahoo Finance chart endpoint",
        "error": " | ".join(errors)[-600:],
    }


def build(snapshot_path: Path, output_path: Path, lookback_days: int, minimum_coverage: float) -> dict[str, Any]:
    snapshot = _load_snapshot(snapshot_path)
    target = date.fromisoformat(str(snapshot["market_session_date"]))
    tickers = [str(row["ticker"]).strip().upper() for row in snapshot["stocks"]]

    records: dict[str, dict[str, Any]] = {}
    for index, ticker in enumerate(tickers, start=1):
        record = _fetch_price(ticker, target, lookback_days)
        records[ticker] = record
        status = record["status"]
        price = record["price_usd"]
        print(f"[{index:02d}/{len(tickers):02d}] {ticker}: {status} {price if price is not None else ''}".rstrip())
        time.sleep(0.10)

    available = [ticker for ticker, record in records.items() if record["price_usd"] is not None]
    missing = [ticker for ticker in tickers if ticker not in available]
    coverage = len(available) / len(tickers)

    output = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "run_date": snapshot.get("run_date"),
        "market_session_date": target.isoformat(),
        "price_basis": "regular-session closing price for the Multi Bagger snapshot market session",
        "source": "Yahoo Finance chart endpoint",
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
