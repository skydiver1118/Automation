from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from build_tradingagents_dashboard_data import build, build_on_demand_stock


WORKSPACE = Path(__file__).resolve().parents[1]
LOCAL_WATCHLIST = WORKSPACE / "tradingagents_dashboard" / "watchlist.local.json"
TRADINGAGENTS_ROOT = Path(r"C:\Users\skydiver1118\Documents\Stock Analysis\TradingAgents")
TRADINGAGENTS_PYTHON = TRADINGAGENTS_ROOT / ".venv" / "Scripts" / "python.exe"
GROUNDED_RUNNER = TRADINGAGENTS_ROOT / "scripts" / "run_grounded_tradingagents_pdf.py"
BUILD_DATA = WORKSPACE / "scripts" / "build_tradingagents_dashboard_data.py"
PAGES_URL = "https://skydiver1118.github.io/my_yolo_test/"
SYMBOL_RE = re.compile(r"^[A-Z0-9][A-Z0-9.\-]{0,14}$")


def run_command(cmd: list[str], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


def persist_symbol(symbol: str, asset_type: str = "", note: str = "Added from dashboard watchlist button.") -> bool:
    if LOCAL_WATCHLIST.exists():
        data = json.loads(LOCAL_WATCHLIST.read_text(encoding="utf-8"))
    else:
        data = {"symbols": []}
    symbols = data.setdefault("symbols", [])
    if any(str(item.get("symbol", "")).upper() == symbol for item in symbols):
        return False
    symbols.append(
        {
            "symbol": symbol,
            "assetType": asset_type,
            "note": note,
        }
    )
    LOCAL_WATCHLIST.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return True


def rebuild_dashboard(timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return run_command([sys.executable, str(BUILD_DATA)], WORKSPACE, timeout)


def current_dashboard_stock(symbol: str) -> dict | None:
    current = build()
    return next((stock for stock in current["stocks"] if stock["symbol"] == symbol), None)


def run_report(symbol: str, report_date: str, timeout: int, persist_to_watchlist: bool = False) -> dict:
    started = time.time()
    report = run_command(
        [
            str(TRADINGAGENTS_PYTHON),
            str(GROUNDED_RUNNER),
            "--symbol",
            symbol,
            "--date",
            report_date,
        ],
        TRADINGAGENTS_ROOT,
        timeout,
    )
    added = False
    if report.returncode == 0 and persist_to_watchlist:
        added = persist_symbol(symbol)
    build = rebuild_dashboard()
    stock = build_on_demand_stock(symbol)
    ok = report.returncode == 0 and build.returncode == 0 and stock["fullReport"]["available"]
    message = None
    if persist_to_watchlist:
        message = "Ticker added to local watchlist." if added else "Ticker already exists in local watchlist."
    return {
        "ok": ok,
        "symbol": symbol,
        "date": report_date,
        "elapsedSeconds": round(time.time() - started, 2),
        "stock": stock,
        "reportReturnCode": report.returncode,
        "buildReturnCode": build.returncode,
        "log": "\n".join(
            [
                "TradingAgents report:",
                report.stdout[-6000:] if report.stdout else "",
                "Dashboard rebuild:",
                build.stdout[-2000:] if build.stdout else "",
            ]
        ).strip(),
        "dashboardUrl": PAGES_URL,
        "message": message,
        "addedToWatchlist": added if persist_to_watchlist else None,
    }


def add_symbol_to_watchlist(symbol: str, asset_type: str = "", note: str = "") -> dict:
    added = persist_symbol(
        symbol,
        asset_type=asset_type.strip(),
        note=(note or "Added from dashboard watchlist button.").strip(),
    )
    build_result = rebuild_dashboard()
    stock = current_dashboard_stock(symbol)
    ok = build_result.returncode == 0 and stock is not None
    return {
        "ok": ok,
        "symbol": symbol,
        "added": added,
        "stock": stock,
        "buildReturnCode": build_result.returncode,
        "dashboardUrl": PAGES_URL,
        "localWatchlistPath": str(LOCAL_WATCHLIST),
        "message": "Ticker added to local watchlist." if added else "Ticker already exists in local watchlist.",
        "log": build_result.stdout[-2000:] if build_result.stdout else "",
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "TradingAgentsBackend/1.0"

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
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
                    "service": "TradingAgents on-demand backend",
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
            report_date = str(request.get("date") or date.today().isoformat())
            timeout = int(request.get("timeoutSeconds") or 900)
            persist_to_watchlist = bool(request.get("persistToWatchlist"))
            if not SYMBOL_RE.match(symbol):
                self._json(400, {"ok": False, "error": "Enter a valid ticker symbol."})
                return
            if path == "/watchlist":
                asset_type = str(request.get("assetType") or "")
                note = str(request.get("note") or "")
                self._json(200, add_symbol_to_watchlist(symbol, asset_type=asset_type, note=note))
                return
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", report_date):
                self._json(400, {"ok": False, "error": "Date must use YYYY-MM-DD."})
                return
            self._json(200, run_report(symbol, report_date, timeout, persist_to_watchlist=persist_to_watchlist))
        except subprocess.TimeoutExpired as exc:
            self._json(504, {"ok": False, "error": f"TradingAgents timed out after {exc.timeout} seconds."})
        except Exception as exc:
            self._json(500, {"ok": False, "error": f"{type(exc).__name__}: {exc}"})

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the local TradingAgents on-demand dashboard backend.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8790)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"TradingAgents backend listening at http://{args.host}:{args.port}")
    print(f"Open {PAGES_URL} and use the Run TradingAgents ticker box.")
    server.serve_forever()


if __name__ == "__main__":
    main()
