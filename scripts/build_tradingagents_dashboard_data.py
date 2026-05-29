from __future__ import annotations

import csv
import json
import os
import re
import site
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


WORKSPACE = Path(__file__).resolve().parents[1]
for vendor_dir in (".localdeps", ".deps", ".deps2"):
    candidate = WORKSPACE / vendor_dir
    if candidate.exists():
        site.addsitedir(str(candidate))

from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetCalendarRequest


ETRADE_CSV = Path(r"C:\Users\skydiver1118\Downloads\etrade_26May2026_2040.csv")
LOCAL_WATCHLIST = WORKSPACE / "tradingagents_dashboard" / "watchlist.local.json"
TRADINGAGENTS_REPORTS = Path(
    r"C:\Users\skydiver1118\Documents\Stock Analysis\TradingAgents\reports"
)
PORTFOLIO_SNAPSHOT_DIR = (
    TRADINGAGENTS_REPORTS / "portfolio_decision_snapshots_2026-05-26"
)
BATCH_DIR = (
    TRADINGAGENTS_REPORTS
    / "full_tradingagents_batch_2026-05-26"
    / "2026-05-22_ollama_qwen3_1.7b"
)
OWNED_SMA_STATE = WORKSPACE / "data" / "owned_stocks_sma50_state.json"
OUTPUT = WORKSPACE / "tradingagents_dashboard" / "data" / "dashboard-data.js"
ENV_FILES = (WORKSPACE / ".env.alpaca", WORKSPACE / ".env")
EASTERN = ZoneInfo("America/New_York")


MODULE_KEYS = {
    "market": ("Market Analyst", "market_report"),
    "sentiment": ("Sentiment Analyst", "sentiment_report"),
    "news": ("News Analyst", "news_report"),
    "fundamentals": ("Fundamentals Analyst", "fundamentals_report"),
    "research": ("Research Manager", "investment_plan"),
    "trader": ("Trader Proposal", "trader_investment_plan"),
    "risk": ("Risk Debate", "risk_debate_state"),
    "portfolio": ("Portfolio Manager", "final_trade_decision"),
}

GROUND_SECTION_MAP = {
    "market": ["Market Analyst Report"],
    "sentiment": ["Sentiment Analyst Report"],
    "news": ["News Analyst Report"],
    "fundamentals": ["Fundamentals Analyst Report", "Earnings And Data Availability"],
    "research": ["Executive Summary", "Bull Case", "Bear Case"],
    "trader": ["Trader Transaction Proposal"],
    "risk": ["Risk Management Debate"],
    "portfolio": ["Portfolio-Level Final Decision", "Verification Notes"],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def clean_report_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if item in (None, "", [], {}):
                continue
            title = str(key).replace("_", " ").title()
            lines.append(f"### {title}")
            lines.append(clean_report_text(item))
        text = "\n\n".join(lines)
    elif isinstance(value, list):
        text = "\n\n".join(clean_report_text(item) for item in value)
    else:
        text = str(value)

    text = re.sub(r"<think>.*?</think>", "", text, flags=re.I | re.S)
    text = re.sub(r"</?think>", "", text, flags=re.I)
    text = text.replace("\ufeff", "").replace("\u00c2", "")
    text = text.replace("\u00b1", "+/-")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_json(path: Path) -> dict:
    return json.loads(read_text(path))


def load_env_files() -> None:
    for env_file in ENV_FILES:
        if not env_file.exists():
            continue
        for raw_line in env_file.read_text(encoding="utf-8-sig").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().lstrip("\ufeff")
            value = value.strip().strip('"').strip("'")
            if key and value and key not in os.environ:
                os.environ[key] = value


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def create_alpaca_clients() -> tuple[TradingClient, StockHistoricalDataClient]:
    load_env_files()
    key = require_env("ALPACA_API_KEY")
    secret = require_env("ALPACA_SECRET_KEY")
    return (
        TradingClient(api_key=key, secret_key=secret, paper=True),
        StockHistoricalDataClient(api_key=key, secret_key=secret),
    )


def latest_completed_market_day(trading_client: TradingClient) -> date:
    now_et = datetime.now(EASTERN)
    window_start = now_et.date() - timedelta(days=14)
    calendar = sorted(
        trading_client.get_calendar(GetCalendarRequest(start=window_start, end=now_et.date())),
        key=lambda row: row.date,
    )
    if not calendar:
        raise RuntimeError("Alpaca calendar returned no recent trading days.")

    today_session = next((row for row in calendar if row.date == now_et.date()), None)
    if today_session:
        close_value = today_session.close
        close_time = close_value if isinstance(close_value, time) else close_value.timetz().replace(tzinfo=None)
        close_dt = datetime.combine(today_session.date, close_time, tzinfo=EASTERN)
        if now_et < close_dt + timedelta(minutes=15):
            prior = [row.date for row in calendar if row.date < today_session.date]
            if prior:
                return prior[-1]
    return calendar[-1].date


def fetch_alpaca_market_snapshot(symbols: list[str]) -> dict:
    try:
        trading_client, data_client = create_alpaca_clients()
        latest_day = latest_completed_market_day(trading_client)
        request = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=TimeFrame.Day,
            start=latest_day - timedelta(days=10),
            end=latest_day + timedelta(days=1),
            feed="iex",
        )
        bars_response = data_client.get_stock_bars(request)
        by_symbol: dict[str, dict[str, float | str | None]] = {}
        for symbol in symbols:
            rows = sorted(
                bars_response.data.get(symbol, []),
                key=lambda row: row.timestamp,
            )
            completed = [
                row for row in rows if row.timestamp.astimezone(EASTERN).date() <= latest_day
            ]
            if not completed:
                continue
            latest = completed[-1]
            prior = completed[-2] if len(completed) > 1 else None
            prev_close = float(prior.close) if prior else None
            close = float(latest.close)
            chg_pct = None
            if prev_close not in (None, 0):
                chg_pct = round(((close / prev_close) - 1.0) * 100.0, 2)
            by_symbol[symbol] = {
                "close": close,
                "prevClose": prev_close,
                "chgPct": chg_pct,
                "barDate": latest.timestamp.astimezone(EASTERN).date().isoformat(),
            }
        return {
            "ok": True,
            "latestDay": latest_day.isoformat(),
            "barsBySymbol": by_symbol,
            "vendor": "alpaca-iex",
        }
    except Exception as exc:
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "barsBySymbol": {},
            "vendor": "alpaca-iex",
        }


def local_watchlist_rows() -> list[dict[str, str]]:
    if not LOCAL_WATCHLIST.exists():
        return []
    data = read_json(LOCAL_WATCHLIST)
    rows = []
    for item in data.get("symbols", []):
        symbol = str(item.get("symbol", "")).upper().strip()
        if not symbol:
            continue
        rows.append(
            {
                "Symbol": symbol,
                "Last": "",
                "Chg%": "",
                "Color": "",
                "Source": "local",
                "Asset Type": item.get("assetType", ""),
                "Note": item.get("note", ""),
            }
        )
    return rows


def merged_watchlist_rows() -> list[dict[str, str]]:
    rows = []
    seen = set()
    if ETRADE_CSV.exists():
        for row in read_csv(ETRADE_CSV):
            symbol = str(row.get("Symbol", "")).upper().strip()
            if not symbol:
                continue
            row = dict(row)
            row["Symbol"] = symbol
            row.setdefault("Source", "etrade")
            row["Source"] = row.get("Source") or "etrade"
            rows.append(row)
            seen.add(symbol)
    for row in local_watchlist_rows():
        if row["Symbol"] not in seen:
            rows.append(row)
            seen.add(row["Symbol"])
    return rows


def parse_float(value: object) -> float | None:
    if value in (None, ""):
        return None
    cleaned = re.sub(r"[^0-9.\-]", "", str(value))
    if cleaned in ("", "-", "."):
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def normalize_flag(value: str | None) -> str:
    text = (value or "").upper()
    if "SELL" in text or "AVOID" in text:
        return "SELL"
    if "BUY" in text or "LONG" in text or "ACCUMULATE" in text:
        return "BUY"
    return "HOLD"


def derive_fallback_flag(chg_pct: float | None, below_sma50: bool | None) -> str:
    if below_sma50 is True:
        return "SELL"
    if below_sma50 is False and chg_pct is not None and chg_pct >= 2:
        return "BUY"
    return "HOLD"


def module_summary(text: str, max_chars: int = 280) -> str:
    plain = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    plain = re.sub(r"[*_#`>|-]", " ", plain)
    plain = re.sub(r"\s+", " ", plain).strip()
    if len(plain) <= max_chars:
        return plain
    return plain[: max_chars - 1].rstrip() + "..."


def markdown_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "Overview"
    sections[current] = []
    for line in markdown.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            current = match.group(1).strip()
            sections.setdefault(current, [])
            continue
        if line.startswith("# "):
            continue
        sections.setdefault(current, []).append(line)
    return {key: clean_report_text("\n".join(value)) for key, value in sections.items()}


def first_report_stance(markdown: str) -> str | None:
    patterns = [
        r"Final stance:\s*(BUY|HOLD|SELL)",
        r"Processed portfolio rating:\s*(BUY|HOLD|SELL)",
        r"Rating:\s*(BUY|HOLD|SELL)",
        r"^#\s+.+?\b(BUY|HOLD|SELL)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, markdown, flags=re.I | re.M)
        if match:
            return match.group(1).upper()
    return None


def first_sentence(markdown: str, max_chars: int = 260) -> str:
    plain = module_summary(markdown, max_chars * 2)
    parts = re.split(r"(?<=[.!?])\s+", plain, maxsplit=2)
    sentence = parts[0]
    if sentence.lower().startswith("final stance:") and len(parts) > 1:
        sentence = f"{parts[0]} {parts[1]}"
    if len(sentence) > max_chars:
        return sentence[: max_chars - 1].rstrip() + "..."
    return sentence


def load_grounded_facts(md_path: Path) -> dict:
    facts_path = md_path.parent / "facts.json"
    if facts_path.exists():
        return read_json(facts_path)
    return {}


def derive_grounded_scores(facts: dict) -> dict[str, float | None]:
    latest = facts.get("latest_ohlcv", {})
    ind = facts.get("latest_indicators", {})
    validity = facts.get("indicator_validity", {})
    close = parse_float(latest.get("close"))
    sma50 = parse_float(ind.get("close_50_sma"))
    sma200 = parse_float(ind.get("close_200_sma"))
    macd = parse_float(ind.get("macd"))
    macds = parse_float(ind.get("macds"))
    rsi = parse_float(ind.get("rsi"))
    window_return = parse_float(facts.get("window_return_pct"))

    if close is None:
        return {"trading": None, "investment": None, "nearTerm": None}

    trading = 50.0
    if validity.get("close_50_sma", True) and sma50 and close > sma50:
        trading += 12
    if validity.get("close_200_sma", True) and sma200 and close > sma200:
        trading += 10
    if macd is not None and macds is not None and macd > macds:
        trading += 8
    if rsi is not None and rsi > 75:
        trading -= 10
    elif rsi is not None and 45 <= rsi <= 68:
        trading += 5
    if window_return is not None:
        trading += max(-10, min(10, window_return / 2))

    investment = 55.0
    fundamentals = str(facts.get("fundamentals_text", ""))
    pe = parse_float(re.search(r"PE Ratio \(TTM\):\s*([^\n]+)", fundamentals).group(1)) if re.search(r"PE Ratio \(TTM\):\s*([^\n]+)", fundamentals) else None
    margin = parse_float(re.search(r"Profit Margin:\s*([^\n]+)", fundamentals).group(1)) if re.search(r"Profit Margin:\s*([^\n]+)", fundamentals) else None
    debt = parse_float(re.search(r"Debt to Equity:\s*([^\n]+)", fundamentals).group(1)) if re.search(r"Debt to Equity:\s*([^\n]+)", fundamentals) else None
    if margin is not None and margin > 0.15:
        investment += 15
    elif margin is not None and margin < 0:
        investment -= 14
    if pe is not None and 0 < pe < 35:
        investment += 8
    elif pe is not None and pe > 80:
        investment -= 10
    if debt is not None and debt > 200:
        investment -= 6

    near_term = (trading * 0.72) + (investment * 0.28)
    clamp = lambda value: round(max(0, min(100, value)), 1)
    return {
        "trading": clamp(trading),
        "investment": clamp(investment),
        "nearTerm": clamp(near_term),
    }


def derive_grounded_risk(facts: dict) -> str:
    latest = facts.get("latest_ohlcv", {})
    ind = facts.get("latest_indicators", {})
    validity = facts.get("indicator_validity", {})
    close = parse_float(latest.get("close"))
    atr = parse_float(ind.get("atr"))
    rsi = parse_float(ind.get("rsi"))
    if close and atr and atr / close > 0.07:
        return "High"
    if validity and not validity.get("close_50_sma", True):
        return "Medium-high"
    if rsi and (rsi > 75 or rsi < 30):
        return "Medium-high"
    return "Medium"


def load_sma_statuses() -> dict[str, dict]:
    if not OWNED_SMA_STATE.exists():
        return {}
    state = read_json(OWNED_SMA_STATE)
    return {row["symbol"].upper(): row for row in state.get("statuses", [])}


def load_snapshot() -> tuple[dict, dict[str, dict]]:
    json_path = PORTFOLIO_SNAPSHOT_DIR / "portfolio_decision_snapshots.json"
    csv_path = PORTFOLIO_SNAPSHOT_DIR / "portfolio_decision_snapshots.csv"
    snapshot = read_json(json_path) if json_path.exists() else {}
    rows = read_csv(csv_path) if csv_path.exists() else []
    by_symbol = {row["Symbol"].upper(): row for row in rows if row.get("Symbol")}
    return snapshot, by_symbol


def compose_data_note(snapshot: dict, market_snapshot: dict) -> str:
    snapshot_date = snapshot.get("generated_on") or snapshot.get("report_date") or "unknown snapshot date"
    if market_snapshot.get("ok"):
        latest_day = market_snapshot.get("latestDay", "unknown")
        return (
            f"Latest completed daily price bars come from Alpaca ({market_snapshot.get('vendor')}) "
            f"through {latest_day}. TradingAgents full reports, indicators, fundamentals, and news "
            f"remain yfinance-backed, and the watchlist-level stance/ranking still comes from the "
            f"portfolio snapshot generated on {snapshot_date}."
        )
    return (
        f"TradingAgents full reports, indicators, fundamentals, and news remain yfinance-backed, and "
        f"the watchlist-level stance/ranking comes from the portfolio snapshot generated on "
        f"{snapshot_date}. Alpaca market-data refresh was unavailable for this build "
        f"({market_snapshot.get('error', 'unknown error')})."
    )


def report_paths_for(symbol: str) -> tuple[Path | None, Path | None]:
    folder = BATCH_DIR / symbol
    md_path = folder / "full_tradingagents_output.md"
    json_path = folder / "full_tradingagents_output.json"
    if md_path.exists() and json_path.exists():
        return md_path, json_path
    candidates = list(TRADINGAGENTS_REPORTS.rglob(f"{symbol}_TradingAgents_Full_Report_*.md"))
    if candidates:
        newest = max(candidates, key=lambda p: p.stat().st_mtime)
        return newest, None
    return None, None


def load_full_report(symbol: str) -> dict:
    md_path, json_path = report_paths_for(symbol)
    if not md_path:
        return {
            "available": False,
            "path": None,
            "provider": None,
            "tradeDate": None,
            "processedRating": None,
            "derivedScores": {"trading": None, "investment": None, "nearTerm": None},
            "decisionSummary": "",
            "riskLabel": None,
            "modules": {},
            "fullMarkdown": "",
        }

    state = {}
    metadata = {}
    if json_path and json_path.exists():
        raw = read_json(json_path)
        state = raw.get("state", {})
        metadata = {
            "provider": raw.get("provider"),
            "quickModel": raw.get("quick_model"),
            "deepModel": raw.get("deep_model"),
            "tradeDate": raw.get("trade_date"),
            "processedRating": raw.get("processed_rating"),
        }

    full_markdown = clean_report_text(read_text(md_path))
    facts = load_grounded_facts(md_path)
    sections = markdown_sections(full_markdown)

    modules = {}
    for module_key, (label, state_key) in MODULE_KEYS.items():
        text = clean_report_text(state.get(state_key))
        if not text:
            parts = [
                sections[section_name]
                for section_name in GROUND_SECTION_MAP.get(module_key, [])
                if sections.get(section_name)
            ]
            text = "\n\n".join(parts)
        modules[module_key] = {
            "label": label,
            "text": text,
            "summary": module_summary(text) if text else "No module text found in this artifact.",
        }

    processed_rating = metadata.get("processedRating") or first_report_stance(full_markdown)
    decision_summary = first_sentence(
        modules.get("research", {}).get("text")
        or modules.get("portfolio", {}).get("text")
        or full_markdown
    )
    return {
        "available": True,
        "path": str(md_path),
        "provider": metadata.get("provider") or ("grounded-tools" if facts else None),
        "quickModel": metadata.get("quickModel"),
        "deepModel": metadata.get("deepModel"),
        "tradeDate": metadata.get("tradeDate") or facts.get("latest_data_date"),
        "processedRating": processed_rating,
        "derivedScores": derive_grounded_scores(facts) if facts else {"trading": None, "investment": None, "nearTerm": None},
        "decisionSummary": decision_summary,
        "riskLabel": derive_grounded_risk(facts) if facts else None,
        "latestClose": parse_float(facts.get("latest_ohlcv", {}).get("close")) if facts else None,
        "oneDayReturnPct": parse_float(facts.get("one_day_return_pct")) if facts else None,
        "modules": modules,
        "fullMarkdown": full_markdown,
    }


def build_on_demand_stock(symbol: str) -> dict:
    symbol = symbol.upper().strip()
    full_report = load_full_report(symbol)
    ta_rating = full_report.get("processedRating")
    flag = normalize_flag(ta_rating) if ta_rating else "HOLD"
    scores = full_report.get("derivedScores") or {
        "trading": None,
        "investment": None,
        "nearTerm": None,
    }
    if full_report.get("available"):
        decision = (
            full_report.get("decisionSummary")
            or "Grounded TradingAgents report is available; review the report and module tabs for the full decision trail."
        )
        risk = full_report.get("riskLabel") or "Review report"
        horizon = full_report.get("tradeDate") or "Grounded report"
        action = "On-demand grounded full report"
    else:
        decision = "TradingAgents report generation did not create a readable full report artifact."
        risk = "Needs review"
        horizon = "Not scored"
        action = "On-demand report pending"

    return {
        "symbol": symbol,
        "last": full_report.get("latestClose"),
        "lastDisplay": "",
        "chgPct": full_report.get("oneDayReturnPct"),
        "color": "",
        "source": "on-demand",
        "assetType": "",
        "note": "Generated from the dashboard ticker runner.",
        "flag": flag,
        "flagSource": "TradingAgents on-demand" if ta_rating else "On-demand backend",
        "scores": scores,
        "decision": decision,
        "risk": risk,
        "horizon": horizon,
        "action": action,
        "snapshot": None,
        "sma": None,
        "fullReport": full_report,
    }


def build() -> dict:
    etrade_rows = merged_watchlist_rows()
    sma = load_sma_statuses()
    snapshot, snapshot_by_symbol = load_snapshot()
    market_snapshot = fetch_alpaca_market_snapshot([row["Symbol"].upper() for row in etrade_rows])
    alpaca_bars = market_snapshot.get("barsBySymbol", {})

    stocks = []
    for row in etrade_rows:
        symbol = row["Symbol"].upper()
        chg_pct = parse_float(row.get("Chg%"))
        last = parse_float(row.get("Last"))
        snapshot_row = snapshot_by_symbol.get(symbol)
        sma_row = sma.get(symbol)
        full_report = load_full_report(symbol)
        alpaca_bar = alpaca_bars.get(symbol)
        if alpaca_bar:
            last = parse_float(alpaca_bar.get("close"))
            chg_pct = parse_float(alpaca_bar.get("chgPct"))
        if last is None and snapshot_row:
            last = parse_float(snapshot_row.get("Last Close"))
        if last is None and full_report.get("latestClose") is not None:
            last = full_report.get("latestClose")
        if chg_pct is None and full_report.get("oneDayReturnPct") is not None:
            chg_pct = full_report.get("oneDayReturnPct")

        ta_rating = None
        if full_report.get("processedRating"):
            ta_rating = full_report["processedRating"]
        elif snapshot_row:
            ta_rating = snapshot_row.get("Final Portfolio Rating")

        if ta_rating:
            flag = normalize_flag(ta_rating)
            flag_source = "TradingAgents"
        else:
            flag = derive_fallback_flag(chg_pct, sma_row.get("below_sma50") if sma_row else None)
            flag_source = "SMA50 + E*TRADE fallback"

        if snapshot_row:
            scores = {
                "trading": parse_float(snapshot_row.get("Trading Score")),
                "investment": parse_float(snapshot_row.get("Investment Score")),
                "nearTerm": parse_float(snapshot_row.get("Near-Term Trade Score")),
            }
            decision = snapshot_row.get("Decision Snapshot") or ""
            risk = snapshot_row.get("Risk") or "Unknown"
            horizon = snapshot_row.get("Time Horizon") or "Watchlist"
            action = snapshot_row.get("Near-Term Action") or ""
        else:
            scores = full_report.get("derivedScores") or {
                "trading": None,
                "investment": None,
                "nearTerm": None,
            }
            if full_report.get("available"):
                decision = (
                    full_report.get("decisionSummary")
                    or "Grounded TradingAgents report is available; review the top panel and module tabs for the full decision trail."
                )
                risk = full_report.get("riskLabel") or "Review report"
                horizon = full_report.get("tradeDate") or "Grounded report"
                action = "Grounded full report"
            else:
                decision = (
                    "No portfolio snapshot row was found for this E*TRADE symbol. "
                    "The dashboard keeps it selectable and shows the uploaded price/SMA context."
                )
                risk = "Needs TradingAgents run"
                horizon = "Not scored"
                action = "Coverage pending"

        stocks.append(
            {
                "symbol": symbol,
                "last": last,
                "lastDisplay": row.get("Last", ""),
                "chgPct": chg_pct,
                "color": row.get("Color", ""),
                "source": row.get("Source", "etrade"),
                "assetType": row.get("Asset Type") or (snapshot_row or {}).get("Asset Type") or "",
                "note": row.get("Note", ""),
                "flag": flag,
                "flagSource": flag_source,
                "scores": scores,
                "decision": decision,
                "risk": risk,
                "horizon": alpaca_bar.get("barDate") if alpaca_bar and row.get("Source", "etrade") != "on-demand" else horizon,
                "action": action,
                "snapshot": snapshot_row,
                "sma": sma_row,
                "marketData": alpaca_bar,
                "fullReport": full_report,
            }
        )

    coverage = sum(1 for stock in stocks if stock["fullReport"]["available"])
    snapshot_symbols = set(snapshot_by_symbol)
    overlap = [stock["symbol"] for stock in stocks if stock["symbol"] in snapshot_symbols]

    return {
        "generatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "sources": {
            "etradeCsv": str(ETRADE_CSV),
            "localWatchlist": str(LOCAL_WATCHLIST),
            "portfolioSnapshot": str(PORTFOLIO_SNAPSHOT_DIR),
            "fullReports": str(BATCH_DIR),
            "smaState": str(OWNED_SMA_STATE),
            "marketData": market_snapshot.get("vendor"),
        },
        "portfolio": {
            "rating": snapshot.get("portfolio_rating", "Not available"),
            "decision": snapshot.get("portfolio_decision", ""),
            "dataNote": compose_data_note(snapshot, market_snapshot),
            "averageTradingScore": snapshot.get("average_trading_score"),
            "averageInvestmentScore": snapshot.get("average_investment_score"),
            "top5Symbols": snapshot.get("top5_symbols", []),
            "resultCount": snapshot.get("result_count", 0),
            "coverageCount": coverage,
            "watchlistCount": len(stocks),
            "snapshotOverlap": overlap,
            "latestMarketDate": market_snapshot.get("latestDay"),
        },
        "stocks": stocks,
    }


def main() -> None:
    data = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    OUTPUT.write_text(f"window.TRADING_AGENTS_DASHBOARD_DATA = {payload};\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(
        f"Stocks: {len(data['stocks'])}; full reports: "
        f"{data['portfolio']['coverageCount']}; snapshot overlap: "
        f"{len(data['portfolio']['snapshotOverlap'])}"
    )


if __name__ == "__main__":
    main()
