from __future__ import annotations

import argparse
import csv
import json
import math
import os
import smtplib
import ssl
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

SYMBOLS = ["SOXL", "TQQQ"]
CONTEXT_SYMBOLS = ["SOXL", "TQQQ", "QQQ"]
DEFAULT_START = "2010-03-11"
OUTPUT_DIR = Path("reports")
DEFAULT_CSV = OUTPUT_DIR / "soxl_tqqq_cash_signal.csv"
DEFAULT_JSON = OUTPUT_DIR / "soxl_tqqq_cash_signal.json"
DEFAULT_STATUS_JSON = OUTPUT_DIR / "soxl_tqqq_cash_run_status.json"


@dataclass(frozen=True)
class StrategyConfig:
    start: str = DEFAULT_START
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
    data_source: str = "live"


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


def fetch_yahoo_daily_close(symbol: str, period1: int) -> dict[str, float]:
    params = {
        "period1": str(period1),
        "period2": str(int(time.time())),
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    last_exc: Exception | None = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            break
        except Exception as exc:
            last_exc = exc
            if attempt < 3:
                time.sleep(attempt)
    else:
        raise RuntimeError(f"Yahoo fetch failed for {symbol}: {last_exc}") from last_exc
    result = payload["chart"]["result"][0]
    ts = result.get("timestamp") or []
    quote = result["indicators"]["quote"][0]
    close = quote.get("close") or []
    adj = result["indicators"].get("adjclose", [{}])[0].get("adjclose", [])
    prices: dict[str, float] = {}
    for i, t in enumerate(ts):
        value = None
        if i < len(adj):
            value = adj[i]
        if value is None and i < len(close):
            value = close[i]
        if value is None:
            continue
        d = datetime.fromtimestamp(int(t), tz=timezone.utc).date().isoformat()
        prices[d] = float(value)
    return prices


def rolling_mean(values: list[float], window: int) -> list[float | None]:
    out: list[float | None] = [None] * len(values)
    if window <= 0:
        return out
    s = 0.0
    for i, v in enumerate(values):
        s += v
        if i >= window:
            s -= values[i - window]
        if i >= window - 1:
            out[i] = s / window
    return out


def pct_change(values: list[float]) -> list[float | None]:
    out: list[float | None] = [None]
    for i in range(1, len(values)):
        prev = values[i - 1]
        out.append((values[i] / prev - 1.0) if prev else None)
    return out


def shifted(values: list[float | None], n: int) -> list[float | None]:
    return [None] * n + values[:-n] if n > 0 else values[:]


def build_close_matrix(start: str) -> tuple[list[str], dict[str, list[float]]]:
    start_dt = datetime.strptime(start, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    period1 = int(start_dt.timestamp())
    raw = {s: fetch_yahoo_daily_close(s, period1) for s in CONTEXT_SYMBOLS}
    common_dates = sorted(set(raw["SOXL"]).intersection(raw["TQQQ"]).intersection(raw["QQQ"]))
    if not common_dates:
        raise RuntimeError("No overlapping Yahoo data for SOXL/TQQQ/QQQ.")
    matrix = {s: [raw[s][d] for d in common_dates] for s in CONTEXT_SYMBOLS}
    return common_dates, matrix


def compute_signal(dates: list[str], close: dict[str, list[float]], config: StrategyConfig, agent: str, positions: dict[str, AlpacaPosition] | None) -> SignalResult:
    soxl = close["SOXL"]
    tqqq = close["TQQQ"]
    qqq = close["QQQ"]
    n = len(dates)
    lb = config.rotation_lookback
    sk = config.rotation_skip

    ret_soxl = [None] * n
    ret_tqqq = [None] * n
    for i in range(n):
        a = i - sk
        b = i - (lb + sk)
        if b >= 0:
            ret_soxl[i] = soxl[a] / soxl[b] - 1.0
            ret_tqqq[i] = tqqq[a] / tqqq[b] - 1.0

    vol_window = max(lb, 10)
    dsoxl = shifted(pct_change(soxl), sk)
    dtqqq = shifted(pct_change(tqqq), sk)
    vol_soxl = [None] * n
    vol_tqqq = [None] * n
    for i in range(n):
        if i >= vol_window - 1:
            ws = [x for x in dsoxl[i - vol_window + 1 : i + 1] if x is not None]
            wt = [x for x in dtqqq[i - vol_window + 1 : i + 1] if x is not None]
            if len(ws) == vol_window:
                vol_soxl[i] = statistics.pstdev(ws) * math.sqrt(252.0)
            if len(wt) == vol_window:
                vol_tqqq[i] = statistics.pstdev(wt) * math.sqrt(252.0)

    score_soxl = [None if ret_soxl[i] is None or vol_soxl[i] is None else ret_soxl[i] - 0.5 * vol_soxl[i] for i in range(n)]
    score_tqqq = [None if ret_tqqq[i] is None or vol_tqqq[i] is None else ret_tqqq[i] - 0.5 * vol_tqqq[i] for i in range(n)]
    sma50_soxl = rolling_mean(soxl, config.rotation_trend_sma)
    sma50_tqqq = rolling_mean(tqqq, config.rotation_trend_sma)

    selected: list[str | None] = []
    current: str | None = None
    for i in range(n):
        if score_soxl[i] is None or score_tqqq[i] is None:
            selected.append(current)
            continue
        diff = score_soxl[i] - score_tqqq[i]
        choice = "SOXL" if diff >= 0 else "TQQQ"
        other = "TQQQ" if choice == "SOXL" else "SOXL"
        trend_choice = soxl[i] >= sma50_soxl[i] if choice == "SOXL" and sma50_soxl[i] is not None else tqqq[i] >= sma50_tqqq[i] if choice == "TQQQ" and sma50_tqqq[i] is not None else False
        trend_other = soxl[i] >= sma50_soxl[i] if other == "SOXL" and sma50_soxl[i] is not None else tqqq[i] >= sma50_tqqq[i] if other == "TQQQ" and sma50_tqqq[i] is not None else False
        adjusted = choice if (trend_choice or not trend_other) else other
        if current is None:
            current = adjusted
        elif adjusted != current and abs(diff) >= config.rotation_hysteresis:
            current = adjusted
        selected.append(current)

    monthly: list[str] = []
    last = "CASH"
    prev_month = ""
    for i, d in enumerate(dates):
        month = d[:7]
        sel = selected[i] if selected[i] is not None else last
        if month != prev_month and sel is not None:
            last = sel
            prev_month = month
        monthly.append(last)

    sma150_soxl = rolling_mean(soxl, config.cash_sma)
    sma150_tqqq = rolling_mean(tqqq, config.cash_sma)
    sma150_qqq = rolling_mean(qqq, config.cash_sma)
    targets: list[str] = []
    risk_on = True
    cur = "CASH"
    for i, sel in enumerate(monthly):
        if sel not in SYMBOLS:
            targets.append(cur)
            continue
        c_sel = soxl[i] if sel == "SOXL" else tqqq[i]
        s_sel = sma150_soxl[i] if sel == "SOXL" else sma150_tqqq[i]
        s_qqq = sma150_qqq[i]
        if s_sel is None or s_qqq is None:
            targets.append(cur)
            continue
        selected_exit = c_sel < s_sel * (1 - config.cash_exit_buffer)
        qqq_exit = qqq[i] < s_qqq * (1 - config.cash_exit_buffer)
        selected_reentry = c_sel >= s_sel * (1 + config.cash_reentry_buffer)
        qqq_reentry = qqq[i] >= s_qqq * (1 + config.cash_reentry_buffer)
        if risk_on and selected_exit and qqq_exit:
            cur = "CASH"
            risk_on = False
        elif not risk_on:
            if selected_reentry or qqq_reentry:
                cur = sel
                risk_on = True
            else:
                cur = "CASH"
        else:
            cur = sel
        targets.append(cur)

    if len(targets) < 2:
        raise RuntimeError("Not enough data after warmup.")
    target = targets[-1]
    previous_target = targets[-2]
    base_target = monthly[-1]
    current_positions = positions or {}
    held = [s for s, p in current_positions.items() if p.qty > 0]
    held_text = "; ".join(f"{s}:{p.qty:g}@{p.avg_entry_price:.4f}" for s, p in current_positions.items()) or "none"
    selected_close = None if target == "CASH" else (soxl[-1] if target == "SOXL" else tqqq[-1])
    selected_sma = None if target == "CASH" else (sma150_soxl[-1] if target == "SOXL" else sma150_tqqq[-1])
    qqq_sma = sma150_qqq[-1]
    selected_trend_ok = bool(selected_close is not None and selected_sma is not None and selected_close >= selected_sma)
    qqq_trend_ok = bool(qqq_sma is not None and qqq[-1] >= qqq_sma)

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
        date=dates[-1],
        target=target,
        previous_target=previous_target,
        base_rotation_target=base_target,
        signal=signal,
        action_summary=action_summary,
        soxl_close=round(soxl[-1], 4),
        tqqq_close=round(tqqq[-1], 4),
        qqq_close=round(qqq[-1], 4),
        selected_close=round(selected_close, 4) if selected_close is not None else None,
        selected_sma150=round(selected_sma, 4) if selected_sma is not None else None,
        qqq_sma150=round(qqq_sma, 4) if qqq_sma is not None else None,
        risk_on=(target != "CASH"),
        selected_trend_ok=selected_trend_ok,
        qqq_trend_ok=qqq_trend_ok,
        cash_rule="Risk-off only when selected ETF and QQQ are both below SMA150; re-enter when either is above SMA150 + 1%.",
        alpaca_positions=held_text,
        position_source="alpaca" if positions is not None else "signal_only",
        generated_at=datetime.now().astimezone().isoformat(timespec="seconds"),
    )


def alpaca_request(method: str, path: str, *, key: str, secret: str, paper: bool, payload: dict | None = None) -> dict:
    base = "https://paper-api.alpaca.markets" if paper else "https://api.alpaca.markets"
    data = None
    headers = {
        "APCA-API-KEY-ID": key,
        "APCA-API-SECRET-KEY": secret,
        "Content-Type": "application/json",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(base + path, data=data, method=method, headers=headers)
    ctx = ssl.create_default_context()
    last_exc: Exception | None = None
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            last_exc = exc
            if attempt < 3:
                time.sleep(attempt)
    raise RuntimeError(f"Alpaca request failed ({method} {path}): {last_exc}") from last_exc


def get_positions(key: str, secret: str, paper: bool) -> dict[str, AlpacaPosition]:
    out: dict[str, AlpacaPosition] = {}
    for symbol in SYMBOLS:
        try:
            row = alpaca_request("GET", f"/v2/positions/{symbol}", key=key, secret=secret, paper=paper)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                continue
            raise
        qty = float(row.get("qty", 0))
        if qty != 0:
            out[symbol] = AlpacaPosition(symbol=symbol, qty=qty, avg_entry_price=float(row.get("avg_entry_price", 0)))
    return out


def limit_price(close: float, side: str, offset_pct: float) -> float:
    offset = offset_pct / 100
    return round(close * (1 + offset), 2) if side == "buy" else round(close * (1 - offset), 2)


def submit_orders(signal: SignalResult, positions: dict[str, AlpacaPosition], *, qty: float, target_notional: float, extended_hours: bool, limit_offset_pct: float, key: str, secret: str, paper: bool) -> list[dict]:
    submitted: list[dict] = []
    close_by_symbol = {"SOXL": signal.soxl_close, "TQQQ": signal.tqqq_close}

    def post_order(symbol: str, side: str, order_qty: float) -> dict:
        payload: dict[str, object] = {
            "symbol": symbol,
            "qty": str(order_qty),
            "side": side,
            "time_in_force": "day",
        }
        if extended_hours:
            payload["type"] = "limit"
            payload["limit_price"] = str(limit_price(close_by_symbol[symbol], side, limit_offset_pct))
            payload["extended_hours"] = True
        else:
            payload["type"] = "market"
        return alpaca_request("POST", "/v2/orders", key=key, secret=secret, paper=paper, payload=payload)

    for symbol, pos in positions.items():
        if signal.target == symbol:
            continue
        submitted.append(post_order(symbol, "sell", abs(pos.qty)))
    if signal.target in SYMBOLS and signal.target not in positions:
        buy_qty = qty
        if target_notional > 0:
            buy_qty = max(target_notional / close_by_symbol[signal.target], 0.0001)
        submitted.append(post_order(signal.target, "buy", buy_qty))
    return submitted


def write_outputs(signal: SignalResult, csv_path: Path, json_path: Path) -> None:
    csv_path.parent.mkdir(exist_ok=True)
    json_path.parent.mkdir(exist_ok=True)
    row = asdict(signal)
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader()
        w.writerow(row)
    json_path.write_text(json.dumps(row, indent=2), encoding="utf-8")


def write_status(
    *,
    status_path: Path,
    signal: SignalResult,
    execute_requested: bool,
    executed_trade: bool,
    stale_reason: str,
    error: str,
) -> None:
    status_path.parent.mkdir(exist_ok=True)
    payload = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "mode": signal.data_source,
        "execute_requested": execute_requested,
        "executed_trade": executed_trade,
        "can_trade_live": signal.data_source == "live",
        "target": signal.target,
        "signal": signal.signal,
        "stale_reason": stale_reason,
        "error": error,
    }
    status_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def send_email_summary(signal: SignalResult, recipient: str, csv_path: Path, json_path: Path, submitted: list[dict]) -> None:
    smtp_host = os.environ.get("ALERT_SMTP_HOST")
    smtp_port_raw = os.environ.get("ALERT_SMTP_PORT", "587")
    smtp_user = os.environ.get("ALERT_SMTP_USER")
    smtp_password = os.environ.get("ALERT_SMTP_PASSWORD")
    sender = os.environ.get("ALERT_EMAIL_FROM", smtp_user or "")
    if not (smtp_host and smtp_user and smtp_password and sender):
        print("Email skipped: missing SMTP environment variables.")
        return
    smtp_port = int(smtp_port_raw)
    subject = f"{signal.agent} {signal.date}: target={signal.target} signal={signal.signal}"
    lines = [
        f"Agent: {signal.agent}",
        f"Date: {signal.date}",
        f"Target: {signal.target}",
        f"Previous target: {signal.previous_target}",
        f"Signal: {signal.signal}",
        f"Action summary: {signal.action_summary}",
        f"Alpaca positions: {signal.alpaca_positions}",
        "",
    ]
    if submitted:
        lines.append("Submitted orders:")
        for x in submitted:
            lines.append(f"- id={x.get('id')} symbol={x.get('symbol')} side={x.get('side')} qty={x.get('qty')} status={x.get('status')}")
    else:
        lines.append("Submitted orders: none")
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.set_content("\n".join(lines))
    for p in (csv_path, json_path):
        if p.exists():
            msg.add_attachment(p.read_bytes(), maintype="application", subtype="octet-stream", filename=p.name)
    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
    print(f"email_sent to={recipient} subject={subject}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Dependency-free SOXL/TQQQ rotation-with-cash scanner.")
    parser.add_argument("--agent", default="SOXL/TQQQ Rotation with cash")
    parser.add_argument("--start", default=DEFAULT_START)
    parser.add_argument("--csv", default=str(DEFAULT_CSV))
    parser.add_argument("--json", default=str(DEFAULT_JSON))
    parser.add_argument("--alpaca", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--extended-hours", action="store_true")
    parser.add_argument("--limit-offset-pct", type=float, default=0.0)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--qty", type=float, default=1.0)
    parser.add_argument("--target-notional", type=float, default=10000.0)
    parser.add_argument("--env-file", default=".env.alpaca")
    parser.add_argument("--email-to", default="")
    parser.add_argument("--status-json", default=str(DEFAULT_STATUS_JSON))
    parser.add_argument("--allow-stale-fallback", action="store_true", help="If live data fetch fails, reuse last signal file and emit a safe HOLD report.")
    args = parser.parse_args()

    load_env_file(Path(args.env_file))
    key = secret = ""
    positions: dict[str, AlpacaPosition] | None = None
    live_block_reason = ""
    if args.alpaca or args.execute:
        key = require_env("ALPACA_API_KEY")
        secret = require_env("ALPACA_SECRET_KEY")
        try:
            positions = get_positions(key, secret, paper=not args.live)
        except Exception as exc:
            if not args.allow_stale_fallback:
                raise
            live_block_reason = f"alpaca_positions_unavailable: {exc}"
            positions = None

    try:
        dates, close = build_close_matrix(args.start)
        signal = compute_signal(dates, close, StrategyConfig(start=args.start), args.agent, positions)
    except Exception as exc:
        if not args.allow_stale_fallback:
            raise
        prev_path = Path(args.json)
        if not prev_path.exists():
            raise RuntimeError(f"Live data unavailable and no fallback report exists at {prev_path}: {exc}") from exc
        prev = json.loads(prev_path.read_text(encoding="utf-8"))
        signal = SignalResult(
            agent=args.agent,
            date=prev.get("date", datetime.now().date().isoformat()),
            target=prev.get("target", "CASH"),
            previous_target=prev.get("previous_target", prev.get("target", "CASH")),
            base_rotation_target=prev.get("base_rotation_target", prev.get("target", "CASH")),
            signal="HOLD",
            action_summary=f"Live data unavailable; stale fallback used. No trade executed. cause={live_block_reason or exc}",
            soxl_close=float(prev.get("soxl_close", 0.0)),
            tqqq_close=float(prev.get("tqqq_close", 0.0)),
            qqq_close=float(prev.get("qqq_close", 0.0)),
            selected_close=prev.get("selected_close"),
            selected_sma150=prev.get("selected_sma150"),
            qqq_sma150=prev.get("qqq_sma150"),
            risk_on=bool(prev.get("risk_on", False)),
            selected_trend_ok=bool(prev.get("selected_trend_ok", False)),
            qqq_trend_ok=bool(prev.get("qqq_trend_ok", False)),
            cash_rule=str(prev.get("cash_rule", "")),
            alpaca_positions=prev.get("alpaca_positions", "unknown"),
            position_source="stale_fallback",
            generated_at=datetime.now().astimezone().isoformat(timespec="seconds"),
            data_source="stale_fallback",
        )
        print(f"warning stale_fallback_enabled cause={live_block_reason or exc}")
    write_outputs(signal, Path(args.csv), Path(args.json))
    print(json.dumps(asdict(signal), indent=2))
    print(f"wrote_csv={args.csv}")
    print(f"wrote_json={args.json}")

    submitted: list[dict] = []
    executed_trade = False
    if args.execute and signal.data_source == "live":
        submitted = submit_orders(signal, positions or {}, qty=args.qty, target_notional=args.target_notional, extended_hours=args.extended_hours, limit_offset_pct=args.limit_offset_pct, key=key, secret=secret, paper=not args.live)
        if submitted:
            executed_trade = True
            for row in submitted:
                print(f"submitted_order id={row.get('id')} symbol={row.get('symbol')} side={row.get('side')} qty={row.get('qty')} status={row.get('status')}")
        else:
            print("No Alpaca order needed; current SOXL/TQQQ positions already match target.")
    elif args.execute and signal.data_source != "live":
        print("Execution skipped because stale fallback mode is active.")
    else:
        print("Dry run: no Alpaca orders submitted. Add --execute to submit orders.")

    recipient = (args.email_to or os.environ.get("ALERT_EMAIL_TO", "")).strip()
    if recipient:
        try:
            send_email_summary(signal, recipient, Path(args.csv), Path(args.json), submitted)
        except Exception as exc:
            print(f"Email send failed: {exc}")

    write_status(
        status_path=Path(args.status_json),
        signal=signal,
        execute_requested=bool(args.execute),
        executed_trade=executed_trade,
        stale_reason=live_block_reason,
        error="",
    )
    print(f"wrote_status_json={args.status_json}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"scanner_failed error={exc}")
        try:
            DEFAULT_STATUS_JSON.parent.mkdir(exist_ok=True)
            DEFAULT_STATUS_JSON.write_text(
                json.dumps(
                    {
                        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                        "mode": "error",
                        "execute_requested": False,
                        "executed_trade": False,
                        "can_trade_live": False,
                        "target": None,
                        "signal": None,
                        "stale_reason": "",
                        "error": str(exc),
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
        except Exception:
            pass
        raise
