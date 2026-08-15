from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf

from src.strategy_lab.stock_alerts import load_config, send_email


@dataclass(frozen=True)
class SmaStatus:
    symbol: str
    price: float
    sma50: float
    below_sma50: bool
    bar_date: str


def load_symbols(config: dict[str, Any]) -> list[str]:
    symbols = [str(symbol).strip().upper() for symbol in config.get("symbols", []) if str(symbol).strip()]
    if not symbols:
        raise RuntimeError("No owned stock symbols configured. Add tickers to configs/owned_stocks_sma50.json.")
    return sorted(set(symbols))


def fetch_close_series(symbol: str, period: str = "6mo", interval: str = "1d") -> pd.Series:
    data = yf.download(symbol, period=period, interval=interval, auto_adjust=True, progress=False)
    if data.empty or "Close" not in data:
        raise RuntimeError(f"No close data returned for {symbol}.")
    close = data["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    close = close.dropna().sort_index()
    if len(close) < 50:
        raise RuntimeError(f"{symbol} has only {len(close)} close bars; SMA50 needs at least 50.")
    return close


def evaluate_symbol(symbol: str, period: str = "6mo", interval: str = "1d") -> SmaStatus:
    close = fetch_close_series(symbol, period=period, interval=interval)
    sma50 = close.rolling(50).mean().dropna()
    aligned = pd.DataFrame({"price": close, "sma50": sma50}).dropna()
    if aligned.empty:
        raise RuntimeError(f"Could not calculate SMA50 for {symbol}.")
    last = aligned.iloc[-1]
    bar = aligned.index[-1]
    bar_date = str(bar.date() if hasattr(bar, "date") else bar)
    price = float(last["price"])
    sma = float(last["sma50"])
    return SmaStatus(symbol=symbol, price=price, sma50=sma, below_sma50=price < sma, bar_date=bar_date)


def load_previous_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"below_sma50": []}
    with path.open("r", encoding="utf-8") as handle:
        state = json.load(handle)
    if not isinstance(state, dict):
        return {"below_sma50": []}
    state.setdefault("below_sma50", [])
    return state


def save_state(path: Path, below_symbols: set[str], statuses: list[SmaStatus]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "last_run_at": datetime.now().isoformat(timespec="seconds"),
        "below_sma50": sorted(below_symbols),
        "statuses": [
            {
                "symbol": item.symbol,
                "price": item.price,
                "sma50": item.sma50,
                "below_sma50": item.below_sma50,
                "bar_date": item.bar_date,
            }
            for item in sorted(statuses, key=lambda status: status.symbol)
        ],
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def style_symbol(symbol: str, added: set[str], removed: set[str]) -> str:
    safe = escape(symbol)
    if symbol in added:
        return f'<span style="color:#1d4ed8;background:#dbeafe;font-weight:700;padding:2px 6px;border-radius:4px;">{safe}</span>'
    if symbol in removed:
        return f'<span style="color:#b91c1c;text-decoration:line-through;font-weight:700;">{safe}</span>'
    return f"<span>{safe}</span>"


def build_email(statuses: list[SmaStatus], previous_below: set[str]) -> tuple[str, str]:
    current_below = {item.symbol for item in statuses if item.below_sma50}
    added = current_below - previous_below
    removed = previous_below - current_below
    bar_date = max((item.bar_date for item in statuses), default="n/a")

    below_rows = []
    for symbol in sorted(current_below | removed):
        status = next((item for item in statuses if item.symbol == symbol), None)
        price = "" if status is None else f"{status.price:.2f}"
        sma = "" if status is None else f"{status.sma50:.2f}"
        below_rows.append(
            "<tr>"
            f"<td>{style_symbol(symbol, added, removed)}</td>"
            f"<td style=\"text-align:right;\">{price}</td>"
            f"<td style=\"text-align:right;\">{sma}</td>"
            f"<td>{'New below SMA50' if symbol in added else 'Removed from below list' if symbol in removed else 'Still below SMA50'}</td>"
            "</tr>"
        )

    all_rows = []
    for item in sorted(statuses, key=lambda status: status.symbol):
        status_text = "Below SMA50" if item.below_sma50 else "Above SMA50"
        all_rows.append(
            "<tr>"
            f"<td>{escape(item.symbol)}</td>"
            f"<td style=\"text-align:right;\">{item.price:.2f}</td>"
            f"<td style=\"text-align:right;\">{item.sma50:.2f}</td>"
            f"<td>{status_text}</td>"
            "</tr>"
        )

    plain_lines = [
        f"Owned stocks below SMA50 scan for {bar_date}",
        "",
        f"Current below SMA50: {', '.join(sorted(current_below)) if current_below else 'None'}",
        f"New below SMA50: {', '.join(sorted(added)) if added else 'None'}",
        f"Removed from below SMA50: {', '.join(sorted(removed)) if removed else 'None'}",
        "",
        "All statuses:",
    ]
    plain_lines.extend(
        f"- {item.symbol}: close {item.price:.2f}, SMA50 {item.sma50:.2f}, {'below' if item.below_sma50 else 'above'}"
        for item in sorted(statuses, key=lambda status: status.symbol)
    )

    summary = (
        "".join(below_rows)
        if below_rows
        else '<tr><td colspan="4" style="color:#166534;">No owned stocks are below SMA50.</td></tr>'
    )
    html = f"""\
<!doctype html>
<html>
  <body style="font-family:Arial, sans-serif;color:#111827;">
    <h2 style="margin-bottom:4px;">Owned Stocks Below SMA50</h2>
    <p style="margin-top:0;color:#4b5563;">Scan date: {escape(bar_date)}</p>
    <p><strong>Blue highlight</strong> = newly below SMA50. <strong style="color:#b91c1c;">Red strikethrough</strong> = removed from yesterday's below-SMA50 list.</p>
    <table style="border-collapse:collapse;min-width:520px;" border="1" cellpadding="8">
      <thead style="background:#f3f4f6;">
        <tr><th>Symbol</th><th>Close</th><th>SMA50</th><th>Change</th></tr>
      </thead>
      <tbody>{summary}</tbody>
    </table>
    <h3>All Owned Stocks</h3>
    <table style="border-collapse:collapse;min-width:520px;" border="1" cellpadding="8">
      <thead style="background:#f3f4f6;">
        <tr><th>Symbol</th><th>Close</th><th>SMA50</th><th>Status</th></tr>
      </thead>
      <tbody>{''.join(all_rows)}</tbody>
    </table>
  </body>
</html>
"""
    return "\n".join(plain_lines), html


def run_scan(config_path: Path, state_path: Path, dry_run: bool = False) -> list[SmaStatus]:
    config = load_config(config_path)
    symbols = load_symbols(config)
    data_config = config.get("data", {})
    period = str(data_config.get("period", "6mo"))
    interval = str(data_config.get("interval", "1d"))
    previous_state = load_previous_state(state_path)
    previous_below = {str(symbol).upper() for symbol in previous_state.get("below_sma50", [])}

    statuses = [evaluate_symbol(symbol, period=period, interval=interval) for symbol in symbols]
    current_below = {item.symbol for item in statuses if item.below_sma50}
    plain, html = build_email(statuses, previous_below)
    subject = config.get("notifications", {}).get("subject", "[Stock Alert] Owned stocks below SMA50")

    if dry_run:
        print(plain)
    else:
        send_email(config, str(subject), plain, html_body=html)
    save_state(state_path, current_below, statuses)
    return statuses


def main() -> None:
    parser = argparse.ArgumentParser(description="Email owned stocks that are below SMA50 with day-over-day HTML diff.")
    parser.add_argument("--config", type=Path, default=Path("configs/owned_stocks_sma50.json"))
    parser.add_argument("--state", type=Path, default=Path("data/owned_stocks_sma50_state.json"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    statuses = run_scan(args.config, args.state, dry_run=args.dry_run)
    below = [item.symbol for item in statuses if item.below_sma50]
    print(f"Scanned {len(statuses)} symbols. Below SMA50: {', '.join(below) if below else 'None'}")


if __name__ == "__main__":
    main()
