from __future__ import annotations

import argparse
import base64
import json
import math
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from score_tradingagents_watchlist import investment_view, score_symbol
from stock_technical_framework import run as run_technical_report


WORKSPACE = Path(__file__).resolve().parents[1]
REPORTS_DIR = WORKSPACE / "reports" / "technical_framework"
LOCAL_WATCHLIST = WORKSPACE / "tradingagents_dashboard" / "watchlist.local.json"
PAGES_URL = "https://skydiver1118.github.io/my_yolo_test/technical-analysis/"
SYMBOL_RE = re.compile(r"^[A-Z0-9][A-Z0-9.\-]{0,14}$")


def as_float(value: object) -> float | None:
    if value in (None, ""):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def chart_data_url(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def parse_zone(text: str) -> tuple[float | None, float | None]:
    if "-" not in text:
        return None, None
    left, right = text.split("-", 1)
    return as_float(left), as_float(right)


def persist_symbol(symbol: str, asset_type: str = "Stock", note: str = "Added from technical-analysis dashboard.") -> bool:
    if LOCAL_WATCHLIST.exists():
        data = json.loads(LOCAL_WATCHLIST.read_text(encoding="utf-8"))
    else:
        data = {"symbols": []}

    symbols = data.setdefault("symbols", [])
    if any(str(item.get("symbol", "")).upper() == symbol for item in symbols):
        return False

    symbols.append({"symbol": symbol, "assetType": asset_type, "note": note})
    LOCAL_WATCHLIST.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return True


def build_stock(symbol: str, period: str = "2y") -> dict:
    scored = score_symbol(symbol, period)
    chart_path, report_path, _score, _label = run_technical_report(
        ticker=symbol,
        out_dir=REPORTS_DIR,
        period=period,
        chart_months=3,
    )
    low, high = parse_zone(str(scored.get("entry_zone") or ""))
    return {
        "symbol": symbol,
        "watchlistSource": "on-demand",
        "assetType": "Stock",
        "note": "Generated manually from technical-analysis dashboard.",
        "latestDate": scored.get("latest_date", ""),
        "last": as_float(scored.get("last")),
        "chgPct": as_float(scored.get("chg_pct")),
        "tradingScore": as_float(scored.get("technical_score")),
        "tradingView": scored.get("trading_view", ""),
        "technicalLabel": scored.get("technical_label", ""),
        "investmentScore": None,
        "investmentView": investment_view(None),
        "dashboardTradingScore": None,
        "dashboardNearTermScore": None,
        "dashboardFlag": "",
        "dashboardRisk": "",
        "nextEarnings": "",
        "indicators": {
            "rsi14": as_float(scored.get("rsi14")),
            "macd": as_float(scored.get("macd")),
            "macdSignal": as_float(scored.get("macd_signal")),
            "adx14": as_float(scored.get("adx14")),
            "atrPct": as_float(scored.get("atr_pct")),
            "ema8": as_float(scored.get("ema8")),
            "sma20": as_float(scored.get("sma20")),
            "sma50": as_float(scored.get("sma50")),
            "sma200": as_float(scored.get("sma200")),
        },
        "levels": {
            "nearestSupport": as_float(scored.get("support")),
            "nearestResistance": as_float(scored.get("resistance")),
        },
        "entry": {
            "plan": scored.get("entry_plan", ""),
            "zone": scored.get("entry_zone", ""),
            "zoneLow": low,
            "zoneHigh": high,
            "trigger": scored.get("entry_trigger", ""),
            "stop": as_float(scored.get("stop")),
            "target1": as_float(scored.get("target_1")),
            "target2": as_float(scored.get("target_2")),
        },
        "scoreError": "",
        "investmentNote": "",
        "chartPath": chart_data_url(chart_path),
        "reportMarkdown": report_path.read_text(encoding="utf-8"),
    }


def analyze_symbol(symbol: str, persist_to_watchlist: bool, period: str = "2y") -> dict:
    started = time.time()
    stock = build_stock(symbol, period=period)
    added = persist_symbol(symbol) if persist_to_watchlist else None
    message = None
    if persist_to_watchlist:
        message = "Ticker added to local watchlist." if added else "Ticker already exists in local watchlist."
    return {
        "ok": True,
        "symbol": symbol,
        "stock": stock,
        "addedToWatchlist": added,
        "message": message,
        "elapsedSeconds": round(time.time() - started, 2),
        "dashboardUrl": PAGES_URL,
        "localWatchlistPath": str(LOCAL_WATCHLIST),
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "TechnicalAnalysisBackend/1.0"

    def _cors(self) -> None:
        origin = self.headers.get("Origin") or "*"
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Cache-Control", "no-store")

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/health":
            self._json(
                200,
                {
                    "ok": True,
                    "service": "Technical-analysis on-demand backend",
                    "dashboardUrl": PAGES_URL,
                },
            )
            return
        self._json(404, {"ok": False, "error": "Unknown endpoint."})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path not in {"/analyze", "/watchlist"}:
            self._json(404, {"ok": False, "error": "Unknown endpoint."})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            request = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            symbol = str(request.get("symbol", "")).upper().strip()
            period = str(request.get("period") or "2y")
            if not SYMBOL_RE.match(symbol):
                self._json(400, {"ok": False, "error": "Enter a valid ticker symbol."})
                return
            if path == "/watchlist":
                response = analyze_symbol(symbol, persist_to_watchlist=True, period=period)
            else:
                response = analyze_symbol(
                    symbol,
                    persist_to_watchlist=bool(request.get("persistToWatchlist")),
                    period=period,
                )
            self._json(200, response)
        except Exception as exc:
            self._json(500, {"ok": False, "error": f"{type(exc).__name__}: {exc}"})

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve local on-demand technical-analysis dashboard reports.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8791)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Technical-analysis backend listening at http://{args.host}:{args.port}")
    print(f"Open {PAGES_URL} and use the Run ticker box.")
    server.serve_forever()


if __name__ == "__main__":
    main()
