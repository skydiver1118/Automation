from __future__ import annotations

import argparse
import json
import math
import os
import site
import smtplib
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
for vendor_dir in (".localdeps", ".deps", ".deps2"):
    candidate = ROOT / vendor_dir
    if candidate.exists():
        site.addsitedir(str(candidate))

import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import GetCalendarRequest, LimitOrderRequest

sys.path.insert(0, str(ROOT))

from src.strategy_lab.momentum_is_oos_research import (
    PRICE_START,
    fetch_prices,
    load_nasdaq100_current_and_changes,
    nasdaq_members_on,
)


DEFAULT_OUTPUT_CSV = Path("reports/nasdaq100_top3_l126_s21_dca3_signal.csv")
DEFAULT_OUTPUT_JSON = Path("reports/nasdaq100_top3_l126_s21_dca3_signal.json")
DEFAULT_STATE_JSON = Path("reports/nasdaq100_top3_l126_s21_dca3_state.json")
DEFAULT_EXECUTION_JSON = Path("reports/nasdaq100_top3_l126_s21_dca3_execution.json")


@dataclass(frozen=True)
class SignalRow:
    strategy: str
    generated_for_date: str
    signal_month: str
    signal_date: str
    trade_date: str
    rank: int
    ticker: str
    score: float
    close_price_date: str
    close_price: float
    target_weight: float
    total_target_exposure: float
    rule: str


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


def create_trading_client() -> TradingClient:
    return TradingClient(
        api_key=require_env("ALPACA_API_KEY"),
        secret_key=require_env("ALPACA_SECRET_KEY"),
        paper=True,
    )


def latest_month_signal_dates(trading_days: pd.DatetimeIndex, as_of: pd.Timestamp) -> tuple[str, pd.Timestamp, pd.Timestamp]:
    eligible = trading_days[trading_days <= as_of]
    if eligible.empty:
        raise RuntimeError(f"No trading data available on or before {as_of.date()}")

    latest = eligible[-1]
    month_start = trading_days[(trading_days.year == latest.year) & (trading_days.month == latest.month)][0]
    prior = trading_days[trading_days < month_start]
    if prior.empty:
        raise RuntimeError("Not enough trading history to find prior month-end signal date.")

    return month_start.to_period("M").strftime("%Y-%m"), prior[-1], month_start


def dca3_exposure_months(close: pd.DataFrame, trade_date: pd.Timestamp) -> int:
    monthly_starts = []
    for period in close.index.to_series().dt.to_period("M").unique():
        days = close.index[close.index.to_period("M") == period]
        if len(days) and days[0] <= trade_date:
            monthly_starts.append(days[0])
    return len(monthly_starts)


def build_signal(as_of: date | None = None) -> pd.DataFrame:
    as_of_ts = pd.Timestamp(as_of or date.today())
    nasdaq_current, nasdaq_changes = load_nasdaq100_current_and_changes()
    prices = fetch_prices(sorted(set(nasdaq_current) | {"QQQ"}), PRICE_START, as_of_ts.date())
    close = prices["Close"].sort_index().dropna(axis=1, thresh=128)

    signal_month, signal_date, trade_date = latest_month_signal_dates(close.index, as_of_ts)
    members = nasdaq_members_on(nasdaq_current, nasdaq_changes, signal_date)
    missing_members = sorted(members - set(close.columns.astype(str)))
    if missing_members:
        prices = fetch_prices(sorted(members | {"QQQ"}), PRICE_START, as_of_ts.date())
        close = prices["Close"].sort_index().dropna(axis=1, thresh=128)
        signal_month, signal_date, trade_date = latest_month_signal_dates(close.index, as_of_ts)
        members = nasdaq_members_on(nasdaq_current, nasdaq_changes, signal_date)

    signal_index = close.index.get_loc(signal_date)
    score_index = signal_index - 21
    lookback_index = signal_index - 126
    if score_index < 0 or lookback_index < 0:
        raise RuntimeError("Not enough history for L126 S21 signal.")

    execution_price_date = close.index[close.index <= as_of_ts][-1]
    scores = (close.iloc[score_index] / close.iloc[lookback_index] - 1.0).replace([float("inf"), -float("inf")], pd.NA)
    eligible = [ticker for ticker in scores.dropna().index.astype(str) if ticker in members and ticker != "QQQ"]
    ranked = scores.loc[eligible].dropna().sort_values(ascending=False)
    selected = ranked.head(3)
    if len(selected) < 3:
        raise RuntimeError(f"Only {len(selected)} eligible tickers had valid scores.")

    total_exposure = min(1.0, dca3_exposure_months(close, trade_date) / 3.0)
    per_ticker_weight = total_exposure / 3.0
    rows = [
        SignalRow(
            strategy="NASDAQ100 Top3 L126 S21 none DCA3",
            generated_for_date=as_of_ts.date().isoformat(),
            signal_month=signal_month,
            signal_date=signal_date.date().isoformat(),
            trade_date=trade_date.date().isoformat(),
            rank=rank,
            ticker=str(ticker),
            score=round(float(score), 6),
            close_price_date=execution_price_date.date().isoformat(),
            close_price=round(float(close.loc[execution_price_date, ticker]), 4),
            target_weight=round(per_ticker_weight, 6),
            total_target_exposure=round(total_exposure, 6),
            rule="Rank Nasdaq-100 by 126-day momentum skipping 21 trading days; hold top 3; DCA3 exposure ramp.",
        )
        for rank, (ticker, score) in enumerate(selected.items(), start=1)
    ]
    return pd.DataFrame([asdict(row) for row in rows])


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def decimalish(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def account_equity(client: TradingClient) -> float:
    return decimalish(client.get_account().equity)


def alpaca_positions(client: TradingClient) -> dict[str, dict[str, float]]:
    positions: dict[str, dict[str, float]] = {}
    for position in client.get_all_positions():
        positions[str(position.symbol)] = {
            "qty": decimalish(position.qty),
            "market_value": decimalish(position.market_value),
        }
    return positions


def is_alpaca_trading_day(client: TradingClient, day: date) -> bool:
    calendar = client.get_calendar(GetCalendarRequest(start=day, end=day))
    return bool(calendar)


def get_calendar_dates(client: TradingClient, start: date, end: date) -> list[date]:
    calendar = client.get_calendar(GetCalendarRequest(start=start, end=end))
    return sorted(pd.Timestamp(day.date).date() for day in calendar)


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


def client_order_id(prefix: str, symbol: str) -> str:
    timestamp = datetime.now().astimezone().strftime("%Y%m%d%H%M%S")
    return f"nasdaq100-top3-dca3-{prefix}-{symbol}-{timestamp}"[:48]


def plan_rebalance(
    signal: pd.DataFrame,
    positions: dict[str, dict[str, float]],
    state: dict[str, Any],
    target_position_notional: float,
    tolerance_pct: float,
) -> list[dict[str, Any]]:
    target_symbols = set(signal["ticker"].astype(str))
    previous_symbols = set(state.get("last_target_symbols", []))
    managed_symbols = target_symbols | previous_symbols
    close_by_symbol = {str(row.ticker): float(row.close_price) for row in signal.itertuples()}
    total_exposure = float(signal["total_target_exposure"].iloc[0])
    per_symbol_notional = target_position_notional * total_exposure
    actions: list[dict[str, Any]] = []

    for symbol in sorted(managed_symbols):
        position = positions.get(symbol, {"qty": 0.0, "market_value": 0.0})
        qty = float(position["qty"])
        market_value = float(position["market_value"])

        if symbol not in target_symbols:
            if abs(qty) > 0.000001:
                actions.append(
                    {
                        "action": "sell",
                        "symbol": symbol,
                        "qty": round(abs(qty), 6),
                        "limit_price": close_by_symbol.get(symbol),
                        "reason": "not_in_target",
                    }
                )
            continue

        close_price = close_by_symbol[symbol]
        target_qty = math.floor(per_symbol_notional / close_price)
        qty_diff = target_qty - qty
        target_market_value = target_qty * close_price
        if target_market_value > 0 and abs((market_value - target_market_value) / target_market_value) <= tolerance_pct:
            actions.append(
                {
                    "action": "hold",
                    "symbol": symbol,
                    "current_qty": qty,
                    "target_qty": target_qty,
                    "limit_price": close_price,
                    "reason": "within_tolerance",
                }
            )
        elif qty_diff > 0:
            actions.append(
                {
                    "action": "buy",
                    "symbol": symbol,
                    "qty": round(qty_diff, 6),
                    "current_qty": qty,
                    "target_qty": target_qty,
                    "limit_price": close_price,
                    "reason": "below_target",
                }
            )
        elif qty_diff < 0:
            actions.append(
                {
                    "action": "sell",
                    "symbol": symbol,
                    "qty": round(abs(qty_diff), 6),
                    "current_qty": qty,
                    "target_qty": target_qty,
                    "limit_price": close_price,
                    "reason": "above_target",
                }
            )
        else:
            # Whole-share sizing can leave qty exactly on target even when the
            # mark-to-market value drifts outside the tolerance band.
            actions.append(
                {
                    "action": "hold",
                    "symbol": symbol,
                    "current_qty": qty,
                    "target_qty": target_qty,
                    "limit_price": close_price,
                    "reason": "at_target_qty",
                }
            )

    return actions


def submit_actions(
    client: TradingClient,
    actions: list[dict[str, Any]],
    *,
    extended_hours: bool,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for action in actions:
        if action["action"] == "hold":
            results.append({**action, "submitted": False, "status": "held"})
            continue
        if action.get("limit_price") is None:
            results.append({**action, "submitted": False, "status": "error", "error": "Missing close/limit price."})
            continue

        side = OrderSide.BUY if action["action"] == "buy" else OrderSide.SELL
        try:
            submitted = client.submit_order(
                LimitOrderRequest(
                    symbol=action["symbol"],
                    qty=float(action["qty"]),
                    side=side,
                    time_in_force=TimeInForce.DAY,
                    limit_price=round(float(action["limit_price"]), 2),
                    extended_hours=extended_hours,
                    client_order_id=client_order_id(action["action"], action["symbol"]),
                )
            )
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


def send_email_summary(
    signal: pd.DataFrame,
    *,
    execution_report: dict[str, Any] | None,
    csv_path: Path,
    json_path: Path,
    execution_path: Path,
    recipient: str,
) -> None:
    smtp_host = os.environ.get("ALERT_SMTP_HOST")
    smtp_port_raw = os.environ.get("ALERT_SMTP_PORT", "587")
    smtp_user = os.environ.get("ALERT_SMTP_USER")
    smtp_password = os.environ.get("ALERT_SMTP_PASSWORD")
    sender = os.environ.get("ALERT_EMAIL_FROM", smtp_user or "")
    if not (smtp_host and smtp_user and smtp_password and sender):
        print(
            "email_skipped=missing_smtp_env "
            "Set ALERT_SMTP_HOST/PORT/USER/PASSWORD and ALERT_EMAIL_FROM."
        )
        return

    try:
        smtp_port = int(smtp_port_raw)
    except ValueError:
        print(f"email_skipped=invalid_smtp_port ALERT_SMTP_PORT={smtp_port_raw!r}")
        return

    strategy = str(signal.loc[0, "strategy"])
    signal_date = str(signal.loc[0, "signal_date"])
    trade_date = str(signal.loc[0, "trade_date"])
    targets = ", ".join(f"{row.ticker}:{row.target_weight:.2%}" for row in signal.itertuples())
    execution_status = execution_report.get("status", "signal_only") if execution_report else "signal_only"
    subject = f"{strategy} {signal_date} trade {trade_date} status={execution_status}"

    lines = [
        f"Strategy: {strategy}",
        f"Generated for date: {signal.loc[0, 'generated_for_date']}",
        f"Signal date: {signal_date}",
        f"Trade date: {trade_date}",
        f"Total target exposure: {float(signal.loc[0, 'total_target_exposure']):.2%}",
        f"Targets: {targets}",
        "",
    ]

    if execution_report:
        lines.extend(
            [
                f"Execution status: {execution_status}",
                f"Paper account: {execution_report.get('paper')}",
                f"Target position notional: {execution_report.get('target_position_notional')}",
                f"Account equity: {execution_report.get('account_equity')}",
                "",
                "Actions:",
            ]
        )
        for action in execution_report.get("actions", []):
            details = [
                f"action={action.get('action')}",
                f"symbol={action.get('symbol')}",
                f"status={action.get('status')}",
                f"submitted={action.get('submitted')}",
            ]
            if action.get("qty") is not None:
                details.append(f"qty={action.get('qty')}")
            if action.get("current_qty") is not None:
                details.append(f"current_qty={action.get('current_qty')}")
            if action.get("target_qty") is not None:
                details.append(f"target_qty={action.get('target_qty')}")
            if action.get("limit_price") is not None:
                details.append(f"limit_price={action.get('limit_price')}")
            if action.get("order_id"):
                details.append(f"order_id={action.get('order_id')}")
            if action.get("client_order_id"):
                details.append(f"client_order_id={action.get('client_order_id')}")
            if action.get("reason"):
                details.append(f"reason={action.get('reason')}")
            if action.get("error"):
                details.append(f"error={action.get('error')}")
            lines.append("- " + " ".join(details))
    else:
        lines.append("Execution status: signal_only")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content("\n".join(lines))
    for path in (csv_path, json_path, execution_path):
        if path.exists():
            msg.add_attachment(
                path.read_bytes(),
                maintype="application",
                subtype="octet-stream",
                filename=path.name,
            )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
    print(f"email_sent to={recipient} subject={subject}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate signal for NASDAQ100 Top3 L126 S21 none DCA3.")
    parser.add_argument("--as-of", default=None, help="Optional YYYY-MM-DD date. Defaults to today.")
    parser.add_argument("--output-csv", default=str(DEFAULT_OUTPUT_CSV))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--state-json", default=str(DEFAULT_STATE_JSON))
    parser.add_argument("--execution-json", default=str(DEFAULT_EXECUTION_JSON))
    parser.add_argument("--env-file", default=str(ROOT / ".env.alpaca"), help="Path to Alpaca paper env file.")
    parser.add_argument("--alpaca", action="store_true", help="Read Alpaca paper account and current positions.")
    parser.add_argument("--execute", action="store_true", help="Submit Alpaca paper extended-hours limit orders.")
    parser.add_argument("--extended-hours", action="store_true", help="Allow Alpaca DAY limit orders outside regular market hours.")
    parser.add_argument("--force", action="store_true", help="Ignore first-trading-day and duplicate-state gates.")
    parser.add_argument("--target-position-notional", type=float, default=10000.0, help="Dollar target per position before the DCA3 exposure ramp is applied.")
    parser.add_argument("--tolerance-pct", type=float, default=0.02, help="Rebalance band around each target holding.")
    parser.add_argument("--email-to", default="", help="Optional recipient email for post-scan summary.")
    args = parser.parse_args()

    as_of = pd.Timestamp(args.as_of).date() if args.as_of else None
    as_of_date = as_of or date.today()
    csv_path = Path(args.output_csv)
    json_path = Path(args.output_json)
    execution_path = Path(args.execution_json)
    execution_report: dict[str, Any] | None = None

    if not args.alpaca and not args.execute:
        signal = build_signal(as_of_date)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        signal.to_csv(csv_path, index=False)
        json_path.write_text(json.dumps(signal.to_dict(orient="records"), indent=2), encoding="utf-8")

        print(f"strategy={signal.loc[0, 'strategy']}")
        print(f"signal_date={signal.loc[0, 'signal_date']}")
        print(f"trade_date={signal.loc[0, 'trade_date']}")
        print(f"total_target_exposure={signal.loc[0, 'total_target_exposure']:.2%}")
        print("targets=" + ", ".join(f"{row.ticker}:{row.target_weight:.2%}" for row in signal.itertuples()))
        print(f"csv={csv_path}")
        print(f"json={json_path}")
        print("Dry run: no Alpaca paper account read and no orders submitted.")
        recipient = (args.email_to or os.environ.get("ALERT_EMAIL_TO", "")).strip()
        if recipient:
            try:
                send_email_summary(
                    signal,
                    execution_report=None,
                    csv_path=csv_path,
                    json_path=json_path,
                    execution_path=execution_path,
                    recipient=recipient,
                )
            except Exception as exc:
                print(f"email_send_failed error={exc}")
        return

    load_env_file(Path(args.env_file))
    client = create_trading_client()
    context = trading_day_context(client, as_of_date)
    rebalance_month = as_of_date.strftime("%Y-%m")
    state_path = Path(args.state_json)
    state = load_state(state_path)

    if not args.force and not context["is_first_trading_day_of_month"]:
        execution_path.parent.mkdir(parents=True, exist_ok=True)
        execution_report = {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "paper": True,
            "strategy": "NASDAQ100 Top3 L126 S21 none DCA3",
            "status": "skipped_not_first_trading_day_of_month",
            "as_of": as_of_date.isoformat(),
            "calendar": {
                key: value.isoformat() if isinstance(value, date) else value
                for key, value in context.items()
                if key != "as_of"
            },
            "message": "Alpaca calendar shows this is not the first trading day of the month; no paper rebalance run.",
        }
        execution_path.write_text(json.dumps(execution_report, indent=2, sort_keys=True), encoding="utf-8")
        print(f"execution_status={execution_report['status']}")
        print(f"First trading day this month: {context['first_trading_day']}")
        print(f"execution_json={execution_path}")
        return

    if not args.force and state.get("last_rebalance_month") == rebalance_month:
        execution_path.parent.mkdir(parents=True, exist_ok=True)
        execution_report = {
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "paper": True,
            "strategy": "NASDAQ100 Top3 L126 S21 none DCA3",
            "status": "skipped_already_rebalanced_this_month",
            "as_of": as_of_date.isoformat(),
            "state": state,
            "message": f"State already shows a rebalance for {rebalance_month}; no duplicate paper rebalance run.",
        }
        execution_path.write_text(json.dumps(execution_report, indent=2, sort_keys=True), encoding="utf-8")
        print(f"execution_status={execution_report['status']}")
        print(execution_report["message"])
        print(f"execution_json={execution_path}")
        return

    if args.execute and not args.force and not args.extended_hours:
        clock = client.get_clock()
        if not bool(clock.is_open):
            execution_path.parent.mkdir(parents=True, exist_ok=True)
            execution_report = {
                "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                "paper": True,
                "strategy": "NASDAQ100 Top3 L126 S21 none DCA3",
                "status": "skipped_market_not_open",
                "as_of": as_of_date.isoformat(),
                "message": "Alpaca market is not open. Re-run after the open, or pass --extended-hours for DAY limit orders outside regular hours, or use --force for testing.",
            }
            execution_path.write_text(json.dumps(execution_report, indent=2, sort_keys=True), encoding="utf-8")
            print(f"execution_status={execution_report['status']}")
            print(execution_report["message"])
            print(f"execution_json={execution_path}")
            return

    signal = build_signal(as_of_date)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    signal.to_csv(csv_path, index=False)
    json_path.write_text(json.dumps(signal.to_dict(orient="records"), indent=2), encoding="utf-8")

    print(f"strategy={signal.loc[0, 'strategy']}")
    print(f"signal_date={signal.loc[0, 'signal_date']}")
    print(f"trade_date={signal.loc[0, 'trade_date']}")
    print(f"total_target_exposure={signal.loc[0, 'total_target_exposure']:.2%}")
    print("targets=" + ", ".join(f"{row.ticker}:{row.target_weight:.2%}" for row in signal.itertuples()))
    print(f"csv={csv_path}")
    print(f"json={json_path}")

    equity = account_equity(client)
    positions = alpaca_positions(client)
    actions = plan_rebalance(
        signal=signal,
        positions=positions,
        state=state,
        target_position_notional=args.target_position_notional,
        tolerance_pct=args.tolerance_pct,
    )
    execution_report = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "paper": True,
        "strategy": "NASDAQ100 Top3 L126 S21 none DCA3",
        "signal_date": str(signal.loc[0, "signal_date"]),
        "trade_date": str(signal.loc[0, "trade_date"]),
        "extended_hours": args.extended_hours,
        "target_position_notional": args.target_position_notional,
        "account_equity": equity,
        "targets": signal.to_dict(orient="records"),
        "actions": actions,
        "status": "planned",
    }

    if args.execute:
        execution_report["actions"] = submit_actions(client, actions, extended_hours=args.extended_hours)
        execution_report["status"] = (
            "submitted_with_errors"
            if any(action.get("status") == "error" for action in execution_report["actions"])
            else "submitted"
        )
        if execution_report["status"] == "submitted":
            save_state(
                state_path,
                {
                    "last_rebalance_month": rebalance_month,
                    "last_target_symbols": sorted(signal["ticker"].astype(str).tolist()),
                    "last_signal_date": str(signal.loc[0, "signal_date"]),
                    "last_trade_date": str(signal.loc[0, "trade_date"]),
                    "last_execution_at": execution_report["generated_at"],
                },
            )

    execution_path.parent.mkdir(parents=True, exist_ok=True)
    execution_path.write_text(json.dumps(execution_report, indent=2, sort_keys=True), encoding="utf-8")
    print(f"execution_status={execution_report['status']}")
    for action in execution_report["actions"]:
        print(action)
    print(f"execution_json={execution_path}")

    recipient = (args.email_to or os.environ.get("ALERT_EMAIL_TO", "")).strip()
    if recipient:
        try:
            send_email_summary(
                signal,
                execution_report=execution_report,
                csv_path=csv_path,
                json_path=json_path,
                execution_path=execution_path,
                recipient=recipient,
            )
        except Exception as exc:
            print(f"email_send_failed error={exc}")


if __name__ == "__main__":
    main()
