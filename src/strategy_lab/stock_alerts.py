from __future__ import annotations

import argparse
import json
import os
import smtplib
import ssl
import urllib.request
import urllib.parse
from base64 import b64encode
from dataclasses import dataclass
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf


SUPPORTED_CONDITIONS = {"below_sma", "above_sma", "cross_below_sma", "cross_above_sma"}


@dataclass(frozen=True)
class AlertRule:
    symbol: str
    condition: str
    window: int
    price_field: str = "Close"
    label: str | None = None
    notify_on: str = "enter"
    enabled: bool = True

    @property
    def state_key(self) -> str:
        return f"{self.symbol.upper()}:{self.price_field}:{self.condition}:{self.window}"

    @property
    def display_name(self) -> str:
        if self.label:
            return self.label
        return f"{self.symbol.upper()} {self.condition.replace('_', ' ')} {self.window}"


@dataclass(frozen=True)
class AlertEvaluation:
    rule: AlertRule
    triggered: bool
    should_notify: bool
    price: float
    sma: float
    bar_date: str
    reason: str


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)
    if not isinstance(config, dict):
        raise ValueError("Alert config must be a JSON object.")
    return config


def parse_rules(config: dict[str, Any]) -> list[AlertRule]:
    rules: list[AlertRule] = []
    for raw_rule in config.get("alerts", []):
        condition = str(raw_rule.get("condition", "")).lower()
        if condition not in SUPPORTED_CONDITIONS:
            raise ValueError(f"Unsupported condition {condition!r}. Choose one of {sorted(SUPPORTED_CONDITIONS)}.")
        window = int(raw_rule.get("window", 50))
        if window < 2:
            raise ValueError("SMA window must be at least 2.")
        rules.append(
            AlertRule(
                symbol=str(raw_rule["symbol"]).upper(),
                condition=condition,
                window=window,
                price_field=str(raw_rule.get("price_field", "Close")),
                label=raw_rule.get("label"),
                notify_on=str(raw_rule.get("notify_on", "enter")).lower(),
                enabled=bool(raw_rule.get("enabled", True)),
            )
        )
    return [rule for rule in rules if rule.enabled]


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"rules": {}}
    with path.open("r", encoding="utf-8") as handle:
        state = json.load(handle)
    if not isinstance(state, dict):
        return {"rules": {}}
    state.setdefault("rules", {})
    return state


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, sort_keys=True)
        handle.write("\n")


def fetch_symbol_history(symbol: str, period: str, interval: str) -> pd.DataFrame:
    data = yf.download(symbol, period=period, interval=interval, auto_adjust=True, progress=False)
    if data.empty:
        raise RuntimeError(f"No price data returned for {symbol}.")
    return data


def price_series(data: pd.DataFrame, field: str) -> pd.Series:
    if field not in data:
        raise ValueError(f"Downloaded data does not contain a {field!r} column.")
    series = data[field]
    if isinstance(series, pd.DataFrame):
        series = series.iloc[:, 0]
    return series.dropna().sort_index()


def evaluate_rule(rule: AlertRule, data: pd.DataFrame, state: dict[str, Any], repeat: bool = False) -> AlertEvaluation:
    prices = price_series(data, rule.price_field)
    if len(prices) < rule.window:
        raise RuntimeError(f"{rule.symbol} has only {len(prices)} bars, but SMA {rule.window} needs at least {rule.window}.")

    sma = prices.rolling(rule.window).mean().dropna()
    aligned = pd.DataFrame({"price": prices, "sma": sma}).dropna()
    if aligned.empty:
        raise RuntimeError(f"Could not calculate SMA {rule.window} for {rule.symbol}.")

    last = aligned.iloc[-1]
    previous = aligned.iloc[-2] if len(aligned) >= 2 else last
    price = float(last["price"])
    sma_value = float(last["sma"])
    prev_price = float(previous["price"])
    prev_sma = float(previous["sma"])

    triggered = {
        "below_sma": price < sma_value,
        "above_sma": price > sma_value,
        "cross_below_sma": prev_price >= prev_sma and price < sma_value,
        "cross_above_sma": prev_price <= prev_sma and price > sma_value,
    }[rule.condition]

    rule_state = state.setdefault("rules", {}).get(rule.state_key, {})
    was_active = bool(rule_state.get("active", False))
    last_bar_date = str(aligned.index[-1].date() if hasattr(aligned.index[-1], "date") else aligned.index[-1])

    if repeat or rule.notify_on == "always":
        should_notify = triggered
    elif rule.notify_on == "change":
        should_notify = triggered != was_active
    else:
        should_notify = triggered and not was_active

    reason = (
        f"{rule.symbol} close {price:.2f} is "
        f"{'below' if price < sma_value else 'above'} SMA{rule.window} {sma_value:.2f}"
    )

    state["rules"][rule.state_key] = {
        "active": triggered,
        "last_checked_at": datetime.now(timezone.utc).isoformat(),
        "last_bar_date": last_bar_date,
        "last_price": price,
        "last_sma": sma_value,
        "last_notified_at": datetime.now(timezone.utc).isoformat() if should_notify else rule_state.get("last_notified_at"),
    }

    return AlertEvaluation(
        rule=rule,
        triggered=triggered,
        should_notify=should_notify,
        price=price,
        sma=sma_value,
        bar_date=last_bar_date,
        reason=reason,
    )


def build_alert_message(evaluations: list[AlertEvaluation]) -> str:
    lines = [
        "Stock alert triggered",
        "",
        *[
            f"- {item.rule.display_name}: {item.reason} on {item.bar_date}"
            for item in evaluations
            if item.should_notify
        ],
    ]
    return "\n".join(lines)


def send_email(config: dict[str, Any], subject: str, body: str, html_body: str | None = None) -> None:
    email_config = config.get("notifications", {}).get("email", {})
    if not email_config.get("enabled", False):
        return

    host = os.environ.get("ALERT_SMTP_HOST", email_config.get("smtp_host", "smtp.gmail.com"))
    port = int(os.environ.get("ALERT_SMTP_PORT", email_config.get("smtp_port", 587)))
    username = os.environ.get("ALERT_SMTP_USER", "")
    password = os.environ.get("ALERT_SMTP_PASSWORD", "")
    sender = os.environ.get("ALERT_EMAIL_FROM", email_config.get("from", username))
    recipients = os.environ.get("ALERT_EMAIL_TO", "") or email_config.get("to", [])

    if isinstance(recipients, str):
        recipients = [item.strip() for item in recipients.split(",") if item.strip()]
    if not username or not password or not sender or not recipients:
        raise RuntimeError("Email alerts need ALERT_SMTP_USER, ALERT_SMTP_PASSWORD, ALERT_EMAIL_FROM, and recipients.")

    message = EmailMessage()
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(body)
    if html_body:
        message.add_alternative(html_body, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls(context=context)
        smtp.login(username, password)
        smtp.send_message(message)


def post_webhooks(config: dict[str, Any], body: str) -> None:
    for webhook in config.get("notifications", {}).get("webhooks", []):
        if not webhook.get("enabled", False):
            continue
        url = webhook.get("url") or os.environ.get(str(webhook.get("url_env", "")))
        if not url:
            raise RuntimeError(f"Webhook {webhook.get('name', '<unnamed>')} is enabled but has no URL.")
        payload = json.dumps({"content": body}).encode("utf-8")
        request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status >= 400:
                raise RuntimeError(f"Webhook {webhook.get('name', '<unnamed>')} returned HTTP {response.status}.")


def send_twilio_sms(config: dict[str, Any], body: str) -> None:
    sms_config = config.get("notifications", {}).get("twilio_sms", {})
    if not sms_config.get("enabled", False):
        return

    account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "")
    from_number = os.environ.get("TWILIO_FROM_NUMBER", sms_config.get("from", ""))
    to_number = os.environ.get("TWILIO_TO_NUMBER", sms_config.get("to", ""))
    if not account_sid or not auth_token or not from_number or not to_number:
        raise RuntimeError("Twilio SMS needs TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, and TWILIO_TO_NUMBER.")

    payload = urllib.parse.urlencode(
        {
            "From": from_number,
            "To": to_number,
            "Body": body[:1500],
        }
    ).encode("utf-8")
    credentials = b64encode(f"{account_sid}:{auth_token}".encode("utf-8")).decode("ascii")
    request = urllib.request.Request(
        f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json",
        data=payload,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.status >= 400:
            raise RuntimeError(f"Twilio SMS returned HTTP {response.status}.")


def run_alerts(config_path: Path, state_path: Path, dry_run: bool = False, repeat: bool = False) -> list[AlertEvaluation]:
    config = load_config(config_path)
    rules = parse_rules(config)
    if not rules:
        raise RuntimeError("No enabled alert rules found.")

    data_config = config.get("data", {})
    period = str(data_config.get("period", "6mo"))
    interval = str(data_config.get("interval", "1d"))
    state = load_state(state_path)

    evaluations: list[AlertEvaluation] = []
    for rule in rules:
        data = fetch_symbol_history(rule.symbol, period=period, interval=interval)
        evaluations.append(evaluate_rule(rule, data, state, repeat=repeat))

    notifying = [item for item in evaluations if item.should_notify]
    if notifying:
        subject_prefix = config.get("notifications", {}).get("subject_prefix", "[Stock Alert]")
        subject = f"{subject_prefix} {len(notifying)} condition{'s' if len(notifying) != 1 else ''} triggered"
        body = build_alert_message(notifying)
        if dry_run:
            print(body)
        else:
            send_email(config, subject, body)
            post_webhooks(config, body)
            send_twilio_sms(config, body)

    save_state(state_path, state)
    return evaluations


def main() -> None:
    parser = argparse.ArgumentParser(description="Run stock condition alerts from a JSON config.")
    parser.add_argument("--config", type=Path, default=Path("configs/stock_alerts.example.json"))
    parser.add_argument("--state", type=Path, default=Path("data/stock_alerts_state.json"))
    parser.add_argument("--dry-run", action="store_true", help="Print alerts instead of sending notifications.")
    parser.add_argument("--repeat", action="store_true", help="Notify on every run while a condition remains true.")
    parser.add_argument("--test-email", action="store_true", help="Send a Gmail SMTP test email without checking stock data.")
    args = parser.parse_args()

    if args.test_email:
        config = load_config(args.config)
        send_email(config, "[Stock Alert] Gmail test", "Gmail SMTP stock-alert test message.")
        print("Sent Gmail SMTP test email.")
        return

    evaluations = run_alerts(args.config, args.state, dry_run=args.dry_run, repeat=args.repeat)
    for item in evaluations:
        status = "NOTIFY" if item.should_notify else "ok"
        print(f"{status}: {item.rule.display_name} | triggered={item.triggered} | {item.reason} | {item.bar_date}")


if __name__ == "__main__":
    main()
