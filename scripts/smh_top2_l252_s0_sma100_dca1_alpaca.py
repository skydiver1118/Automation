from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from alpaca.trading.requests import ClosePositionRequest, GetCalendarRequest, LimitOrderRequest, MarketOrderRequest


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "smh_components"
REPORT_DIR = ROOT / "reports"
HOLDINGS_PATH = DATA_DIR / "smh_historical_holdings_sec.csv"
STATE_PATH = REPORT_DIR / "smh_top2_l252_s0_sma100_dca1_alpaca_state.json"
SIGNAL_JSON_PATH = REPORT_DIR / "smh_top2_l252_s0_sma100_dca1_alpaca_signal.json"
SIGNAL_CSV_PATH = REPORT_DIR / "smh_top2_l252_s0_sma100_dca1_alpaca_signal.csv"

STRATEGY_ID = "smh_top2_l252_s0_sma100_dca1"
TIMEZONE = ZoneInfo("America/New_York")
DEFAULT_TARGET_NOTIONAL_PER_SYMBOL = 10000.0


@dataclass
class StrategySignal:
    strategy_id: str
    as_of: str
    signal_date: str
    rebalance_month: str
    snapshot_filing_date: str
    snapshot_period_end: str
    snapshot_source_type: str
    raw_universe_size: int
    priced_universe_size: int
    smh_close: float | None
    smh_sma100: float | None
    risk_on: bool
    target_tickers: list[str]
    ranked_tickers: list[str]


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip().lstrip("\ufeff")
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def create_trading_client() -> TradingClient:
    return TradingClient(
        api_key=require_env("ALPACA_API_KEY"),
        secret_key=require_env("ALPACA_SECRET_KEY"),
        paper=True,
    )


def to_date(value: Any) -> date:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    return pd.Timestamp(value).date()


def get_calendar_dates(client: TradingClient, start: date, end: date) -> list[date]:
    calendar = client.get_calendar(GetCalendarRequest(start=start, end=end))
    return sorted(to_date(day.date) for day in calendar)


def trading_day_context(client: TradingClient, as_of: date) -> dict[str, Any]:
    month_start = as_of.replace(day=1)
    month_dates = get_calendar_dates(client, month_start, as_of)
    lookback_dates = get_calendar_dates(client, as_of - timedelta(days=21), as_of)
    prior_dates = [day for day in lookback_dates if day < as_of]
    is_trading_day = as_of in month_dates
    first_trading_day = month_dates[0] if month_dates else None
    return {
        "as_of": as_of,
        "is_trading_day": is_trading_day,
        "first_trading_day": first_trading_day,
        "is_first_trading_day_of_month": bool(is_trading_day and first_trading_day == as_of),
        "prior_trading_day": prior_dates[-1] if prior_dates else None,
    }


def maybe_refresh_holdings(enabled: bool) -> None:
    if not enabled:
        return
    subprocess.run(
        [sys.executable, str(ROOT / "src" / "strategy_lab" / "extract_smh_historical_holdings_sec.py")],
        cwd=ROOT,
        check=True,
    )


def load_historical_holdings() -> pd.DataFrame:
    if not HOLDINGS_PATH.exists():
        raise RuntimeError(f"Missing holdings file: {HOLDINGS_PATH}")
    holdings = pd.read_csv(HOLDINGS_PATH)
    holdings["filing_date"] = pd.to_datetime(holdings["filing_date"]).dt.date
    holdings["period_end"] = pd.to_datetime(holdings["period_end"]).dt.date
    holdings["ticker_guess"] = holdings["ticker_guess"].fillna("").astype(str).str.strip()
    holdings = holdings[holdings["ticker_guess"] != ""].copy()
    holdings["ticker"] = holdings["ticker_guess"].str.replace(".", "-", regex=False)
    return holdings.sort_values(["filing_date", "period_end", "ticker"])


def latest_snapshot(holdings: pd.DataFrame, signal_date: date) -> tuple[dict[str, Any], list[str]]:
    known = holdings[holdings["filing_date"] <= signal_date].copy()
    if known.empty:
        raise RuntimeError(f"No SMH holdings snapshot was public by signal date {signal_date}")

    group_cols = ["filing_date", "period_end", "source_type", "form", "accession", "source_url"]
    snapshots = []
    for keys, group in known.groupby(group_cols, sort=True):
        filing_date, period_end, source_type, form, accession, source_url = keys
        snapshots.append(
            {
                "filing_date": filing_date,
                "period_end": period_end,
                "source_type": source_type,
                "form": form,
                "accession": accession,
                "source_url": source_url,
                "tickers": sorted(set(group["ticker"])),
            }
        )
    snapshot = max(snapshots, key=lambda item: (item["filing_date"], item["period_end"]))
    return snapshot, list(snapshot["tickers"])


def normalize_download(raw: pd.DataFrame, field: str) -> pd.DataFrame:
    if raw.empty:
        raise RuntimeError("No Yahoo Finance price data returned")

    if isinstance(raw.columns, pd.MultiIndex):
        if field in raw.columns.get_level_values(0):
            frame = raw[field]
        elif field in raw.columns.get_level_values(1):
            frame = raw.xs(field, axis=1, level=1)
        else:
            raise RuntimeError(f"Downloaded price data does not contain {field}")
    else:
        frame = raw[[field]].copy()
        frame.columns = [raw.attrs.get("symbol", field)]

    frame = frame.copy()
    frame.index = pd.to_datetime(frame.index).tz_localize(None)
    frame.columns = [str(col).replace(".", "-") for col in frame.columns]
    return frame.sort_index()


def fetch_close_prices(tickers: list[str], end_date: date) -> pd.DataFrame:
    start_date = end_date - timedelta(days=600)
    raw = yf.download(
        tickers=sorted(set(tickers)),
        start=start_date.isoformat(),
        end=(end_date + timedelta(days=1)).isoformat(),
        auto_adjust=True,
        progress=False,
        threads=True,
    )
    return normalize_download(raw, "Close")


def latest_reference_prices(tickers: list[str]) -> dict[str, float]:
    if not tickers:
        return {}
    raw = yf.download(
        tickers=sorted(set(tickers)),
        period="10d",
        auto_adjust=True,
        progress=False,
        threads=True,
    )
    close = normalize_download(raw, "Close")
    prices: dict[str, float] = {}
    for symbol in sorted(set(tickers)):
        if symbol not in close.columns:
            continue
        series = close[symbol].dropna()
        if not series.empty:
            prices[symbol] = float(series.iloc[-1])
    return prices


def compute_signal(as_of: date, signal_date: date) -> StrategySignal:
    holdings = load_historical_holdings()
    snapshot, raw_universe = latest_snapshot(holdings, signal_date)
    tickers = sorted(set(raw_universe) | {"SMH"})
    close = fetch_close_prices(tickers, signal_date)

    signal_ts = pd.Timestamp(signal_date)
    valid_dates = close.index[close.index <= signal_ts]
    if valid_dates.empty:
        raise RuntimeError(f"No close prices available on or before signal date {signal_date}")
    signal_ts = valid_dates[-1]
    signal_index = close.index.get_loc(signal_ts)
    if signal_index < 252:
        raise RuntimeError(f"Need 252 trading days before {signal_ts.date()} to rank momentum")
    if signal_index < 99:
        raise RuntimeError(f"Need 100 trading days before {signal_ts.date()} to calculate SMH SMA100")

    smh_close = close.loc[signal_ts, "SMH"] if "SMH" in close.columns else float("nan")
    smh_sma100 = close["SMH"].iloc[signal_index - 99 : signal_index + 1].mean() if "SMH" in close.columns else float("nan")
    risk_on = bool(pd.notna(smh_close) and pd.notna(smh_sma100) and smh_close > smh_sma100)

    lookback_ts = close.index[signal_index - 252]
    scores = (close.loc[signal_ts] / close.loc[lookback_ts] - 1.0).replace([float("inf"), -float("inf")], pd.NA)
    eligible = [ticker for ticker in raw_universe if ticker in scores.index and pd.notna(scores.get(ticker))]
    ranked = scores.loc[eligible].sort_values(ascending=False)
    ranked_tickers = [str(ticker) for ticker in ranked.index]
    target_tickers = ranked_tickers[:2] if risk_on else []

    return StrategySignal(
        strategy_id=STRATEGY_ID,
        as_of=as_of.isoformat(),
        signal_date=signal_ts.date().isoformat(),
        rebalance_month=as_of.strftime("%Y-%m"),
        snapshot_filing_date=snapshot["filing_date"].isoformat(),
        snapshot_period_end=snapshot["period_end"].isoformat(),
        snapshot_source_type=str(snapshot["source_type"]),
        raw_universe_size=len(raw_universe),
        priced_universe_size=len(eligible),
        smh_close=float(smh_close) if pd.notna(smh_close) else None,
        smh_sma100=float(smh_sma100) if pd.notna(smh_sma100) else None,
        risk_on=risk_on,
        target_tickers=target_tickers,
        ranked_tickers=ranked_tickers[:10],
    )


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def decimalish(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def position_rows(client: TradingClient) -> dict[str, dict[str, float]]:
    rows: dict[str, dict[str, float]] = {}
    for position in client.get_all_positions():
        rows[str(position.symbol)] = {
            "qty": decimalish(position.qty),
            "market_value": decimalish(position.market_value),
        }
    return rows


def order_id(prefix: str, symbol: str, rebalance_month: str) -> str:
    timestamp = datetime.now(TIMEZONE).strftime("%Y%m%d%H%M%S")
    return f"{STRATEGY_ID}-{rebalance_month}-{prefix}-{symbol}-{timestamp}"[:48]


def plan_rebalance(
    client: TradingClient,
    signal: StrategySignal,
    target_notional_per_symbol: float,
    tolerance_pct: float,
    manage_all_smh_positions: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    account = client.get_account()
    equity = decimalish(account.equity)
    target_symbols = set(signal.target_tickers)
    state = load_state()
    previous_symbols = set(state.get("last_target_symbols", []))
    positions = position_rows(client)
    managed_symbols = set(previous_symbols) | target_symbols

    if manage_all_smh_positions:
        holdings = load_historical_holdings()
        _, raw_universe = latest_snapshot(holdings, date.fromisoformat(signal.signal_date))
        managed_symbols |= set(raw_universe)

    target_notional = target_notional_per_symbol if target_symbols else 0.0
    actions: list[dict[str, Any]] = []

    for symbol in sorted(managed_symbols):
        pos = positions.get(symbol, {"qty": 0.0, "market_value": 0.0})
        qty = pos["qty"]
        market_value = pos["market_value"]

        if symbol not in target_symbols:
            if abs(qty) > 0.000001:
                actions.append({"action": "close", "symbol": symbol, "qty": qty, "market_value": market_value})
            continue

        diff = target_notional - market_value
        if target_notional > 0 and abs(diff) / target_notional <= tolerance_pct:
            actions.append(
                {
                    "action": "hold",
                    "symbol": symbol,
                    "current_market_value": market_value,
                    "target_notional": target_notional,
                    "reason": "within_tolerance",
                }
            )
        elif diff > 0:
            actions.append(
                {
                    "action": "buy_notional",
                    "symbol": symbol,
                    "notional": round(diff, 2),
                    "current_market_value": market_value,
                    "target_notional": target_notional,
                }
            )
        elif qty > 0 and market_value > 0:
            estimated_price = abs(market_value / qty)
            sell_qty = min(qty, abs(diff) / estimated_price)
            actions.append(
                {
                    "action": "sell_qty",
                    "symbol": symbol,
                    "qty": round(sell_qty, 6),
                    "current_market_value": market_value,
                    "target_notional": target_notional,
                }
            )

    unmanaged_smh_positions: list[str] = []
    try:
        holdings = load_historical_holdings()
        _, raw_universe = latest_snapshot(holdings, date.fromisoformat(signal.signal_date))
        smh_symbols = set(raw_universe) | {"SMH"}
        unmanaged_smh_positions = sorted((set(positions) & smh_symbols) - managed_symbols)
    except Exception:
        unmanaged_smh_positions = []

    context = {
        "account_equity": equity,
        "configured_target_notional_per_symbol": target_notional_per_symbol,
        "target_notional_per_symbol": target_notional,
        "positions": positions,
        "managed_symbols": sorted(managed_symbols),
        "unmanaged_smh_positions": unmanaged_smh_positions,
    }
    return actions, context


def submit_actions(
    client: TradingClient,
    actions: list[dict[str, Any]],
    rebalance_month: str,
    extended_hours: bool,
    limit_offset_pct: float,
) -> list[dict[str, Any]]:
    ref_prices = latest_reference_prices(
        [
            str(action.get("symbol", ""))
            for action in actions
            if action.get("action") in {"close", "buy_notional", "sell_qty"} and action.get("symbol")
        ]
    )
    results: list[dict[str, Any]] = []
    for action in actions:
        if action["action"] == "hold":
            results.append({**action, "submitted": False, "status": "held"})
            continue
        symbol = action["symbol"]
        try:
            ref_price = ref_prices.get(symbol)
            if extended_hours and (ref_price is None or ref_price <= 0):
                raise RuntimeError(f"Missing valid reference price for extended-hours limit order: {symbol}")
            if action["action"] == "close":
                if extended_hours:
                    qty = abs(float(action.get("qty", 0.0)))
                    if qty <= 0:
                        raise RuntimeError(f"Invalid close qty for {symbol}: {qty}")
                    limit_price = round(ref_price * (1.0 - limit_offset_pct / 100.0), 2)
                    submitted = client.submit_order(
                        LimitOrderRequest(
                            symbol=symbol,
                            qty=qty,
                            side=OrderSide.SELL,
                            time_in_force=TimeInForce.DAY,
                            limit_price=limit_price,
                            extended_hours=True,
                            client_order_id=order_id("close", symbol, rebalance_month),
                        )
                    )
                else:
                    submitted = client.close_position(symbol, ClosePositionRequest(percentage="100"))
            elif action["action"] == "buy_notional":
                if extended_hours:
                    notional = float(action["notional"])
                    limit_price = round(ref_price * (1.0 + limit_offset_pct / 100.0), 2)
                    qty = round(notional / limit_price, 6) if limit_price > 0 else 0.0
                    if qty <= 0:
                        raise RuntimeError(f"Computed buy qty is zero for {symbol} from notional={notional} price={limit_price}")
                    submitted = client.submit_order(
                        LimitOrderRequest(
                            symbol=symbol,
                            qty=qty,
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.DAY,
                            limit_price=limit_price,
                            extended_hours=True,
                            client_order_id=order_id("buy", symbol, rebalance_month),
                        )
                    )
                else:
                    submitted = client.submit_order(
                        MarketOrderRequest(
                            symbol=symbol,
                            notional=float(action["notional"]),
                            side=OrderSide.BUY,
                            type=OrderType.MARKET,
                            time_in_force=TimeInForce.DAY,
                            client_order_id=order_id("buy", symbol, rebalance_month),
                        )
                    )
            elif action["action"] == "sell_qty":
                if extended_hours:
                    limit_price = round(ref_price * (1.0 - limit_offset_pct / 100.0), 2)
                    submitted = client.submit_order(
                        LimitOrderRequest(
                            symbol=symbol,
                            qty=float(action["qty"]),
                            side=OrderSide.SELL,
                            time_in_force=TimeInForce.DAY,
                            limit_price=limit_price,
                            extended_hours=True,
                            client_order_id=order_id("sell", symbol, rebalance_month),
                        )
                    )
                else:
                    submitted = client.submit_order(
                        MarketOrderRequest(
                            symbol=symbol,
                            qty=float(action["qty"]),
                            side=OrderSide.SELL,
                            type=OrderType.MARKET,
                            time_in_force=TimeInForce.DAY,
                            client_order_id=order_id("sell", symbol, rebalance_month),
                        )
                    )
            else:
                results.append({**action, "submitted": False, "status": "unknown_action"})
                continue
            results.append(
                {
                    **action,
                    "submitted": True,
                    "status": str(getattr(submitted, "status", "")),
                    "order_id": str(getattr(submitted, "id", "")),
                    "client_order_id": str(getattr(submitted, "client_order_id", "")),
                }
            )
        except Exception as exc:
            results.append({**action, "submitted": False, "status": "error", "error": str(exc)})
    return results


def write_report(report: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    SIGNAL_JSON_PATH.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    rows = []
    for action in report.get("actions", []):
        rows.append(
            {
                "generated_at": report["generated_at"],
                "as_of": report["as_of"],
                "signal_date": report.get("signal", {}).get("signal_date", ""),
                "risk_on": report.get("signal", {}).get("risk_on", ""),
                "target_tickers": ", ".join(report.get("signal", {}).get("target_tickers", [])),
                **action,
            }
        )
    if not rows:
        rows.append(
            {
                "generated_at": report["generated_at"],
                "as_of": report["as_of"],
                "signal_date": report.get("signal", {}).get("signal_date", ""),
                "risk_on": report.get("signal", {}).get("risk_on", ""),
                "target_tickers": ", ".join(report.get("signal", {}).get("target_tickers", [])),
                "action": report.get("status", "no_action"),
            }
        )
    pd.DataFrame(rows).to_csv(SIGNAL_CSV_PATH, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Paper trade SMH Top2 L252 S0 SMA100 DCA1 in Alpaca.")
    parser.add_argument("--env-file", default=str(ROOT / ".env.alpaca"), help="Path to Alpaca paper env file.")
    parser.add_argument("--execute", action="store_true", help="Submit Alpaca paper orders. Default is dry-run.")
    parser.add_argument("--force", action="store_true", help="Ignore first-trading-day and duplicate-state gates.")
    parser.add_argument("--as-of", help="Override current ET date, YYYY-MM-DD. For testing only.")
    parser.add_argument("--refresh-holdings", action="store_true", help="Refresh SEC SMH holdings before a rebalance.")
    parser.add_argument("--extended-hours", action="store_true", help="Allow Alpaca DAY limit orders outside regular market hours.")
    parser.add_argument("--limit-offset-pct", type=float, default=0.0, help="Limit offset percent from last close when using --extended-hours.")
    parser.add_argument(
        "--target-notional-per-symbol",
        type=float,
        default=DEFAULT_TARGET_NOTIONAL_PER_SYMBOL,
        help="Dollar notional to target for each selected equity.",
    )
    parser.add_argument("--tolerance-pct", type=float, default=0.02, help="Rebalance band around each target notional.")
    parser.add_argument(
        "--manage-all-smh-positions",
        action="store_true",
        help="Also close/rebalance any current Alpaca position in the current SMH holdings universe.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_env_file(Path(args.env_file))
    client = create_trading_client()
    as_of = date.fromisoformat(args.as_of) if args.as_of else datetime.now(TIMEZONE).date()
    generated_at = datetime.now(TIMEZONE).isoformat()

    context = trading_day_context(client, as_of)
    report: dict[str, Any] = {
        "generated_at": generated_at,
        "strategy_id": STRATEGY_ID,
        "as_of": as_of.isoformat(),
        "paper": True,
        "calendar": {
            key: value.isoformat() if isinstance(value, date) else value
            for key, value in context.items()
            if key != "as_of"
        },
        "status": "created",
        "actions": [],
    }

    rebalance_key = as_of.strftime("%Y-%m")
    state = load_state()

    if not args.force and not context["is_first_trading_day_of_month"]:
        report["status"] = "skipped_not_first_trading_day_of_month"
        write_report(report)
        print(f"Skipped: {as_of} is not the first Alpaca trading day of the month.")
        print(f"First trading day this month: {context['first_trading_day']}")
        print(f"Report: {SIGNAL_JSON_PATH}")
        return 0

    if not args.force and state.get("last_rebalance_month") == rebalance_key:
        report["status"] = "skipped_already_rebalanced_this_month"
        report["state"] = state
        write_report(report)
        print(f"Skipped: state already shows rebalance for {rebalance_key}.")
        print(f"Report: {SIGNAL_JSON_PATH}")
        return 0

    if args.execute and not args.force and not args.extended_hours:
        clock = client.get_clock()
        if not bool(clock.is_open):
            report["status"] = "skipped_market_not_open"
            write_report(report)
            print("Skipped: Alpaca market is not open. Re-run after open, or pass --extended-hours for DAY limit orders.")
            print(f"Report: {SIGNAL_JSON_PATH}")
            return 0

    maybe_refresh_holdings(args.refresh_holdings)
    signal_date = context["prior_trading_day"] or (as_of - timedelta(days=1))
    signal = compute_signal(as_of, signal_date)
    actions, account_context = plan_rebalance(
        client=client,
        signal=signal,
        target_notional_per_symbol=args.target_notional_per_symbol,
        tolerance_pct=args.tolerance_pct,
        manage_all_smh_positions=args.manage_all_smh_positions,
    )

    report["signal"] = asdict(signal)
    report["account_context"] = account_context
    report["extended_hours"] = bool(args.extended_hours)
    report["limit_offset_pct"] = float(args.limit_offset_pct)
    report["actions"] = actions
    report["status"] = "planned"

    if args.execute:
        results = submit_actions(
            client,
            actions,
            rebalance_key,
            extended_hours=bool(args.extended_hours),
            limit_offset_pct=float(args.limit_offset_pct),
        )
        report["actions"] = results
        had_errors = any(action.get("status") == "error" for action in results)
        report["status"] = "submitted_with_errors" if had_errors else "submitted"
        if not had_errors:
            save_state(
                {
                    "last_rebalance_month": rebalance_key,
                    "last_rebalance_at": generated_at,
                    "last_signal_date": signal.signal_date,
                    "last_target_symbols": signal.target_tickers,
                    "last_risk_on": signal.risk_on,
                }
            )
    else:
        report["status"] = "dry_run_planned"

    write_report(report)

    print(f"Strategy: {STRATEGY_ID}")
    print(f"As of: {as_of} | signal date: {signal.signal_date}")
    print(f"Risk on: {signal.risk_on} | target: {', '.join(signal.target_tickers) if signal.target_tickers else 'CASH'}")
    print(f"Ranked top 10: {', '.join(signal.ranked_tickers)}")
    print(f"Status: {report['status']} | execute={args.execute}")
    print(f"Actions: {len(report['actions'])}")
    for action in report["actions"]:
        print(json.dumps(action, sort_keys=True))
    if account_context.get("unmanaged_smh_positions"):
        print("Warning: unmanaged SMH-universe positions not touched:", ", ".join(account_context["unmanaged_smh_positions"]))
    print(f"Report: {SIGNAL_JSON_PATH}")
    print(f"CSV: {SIGNAL_CSV_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
