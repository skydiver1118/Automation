from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_detection import (  # noqa: E402
    PatternCandidate,
    find_patterns,
    score_interpretation,
    select_primary,
)


SP500_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def yahoo_symbol(symbol: str) -> str:
    return symbol.replace(".", "-")


def load_sp500_universe() -> pd.DataFrame:
    response = requests.get(
        SP500_WIKI_URL,
        headers={"User-Agent": "Mozilla/5.0 cup-handle-scanner/1.0"},
        timeout=30,
    )
    response.raise_for_status()
    tables = pd.read_html(StringIO(response.text))
    if not tables:
        raise RuntimeError("Could not read S&P 500 constituent table")
    df = tables[0].copy()
    required = {"Symbol", "Security", "GICS Sector", "GICS Sub-Industry"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"S&P 500 table missing expected columns: {sorted(missing)}")
    df["YahooSymbol"] = df["Symbol"].map(yahoo_symbol)
    return df[["Symbol", "YahooSymbol", "Security", "GICS Sector", "GICS Sub-Industry"]]


def normalize_download_frame(raw: pd.DataFrame, ticker: str) -> pd.DataFrame:
    if raw.empty:
        return raw

    if isinstance(raw.columns, pd.MultiIndex):
        if ticker in raw.columns.get_level_values(0):
            df = raw[ticker].copy()
        elif ticker in raw.columns.get_level_values(-1):
            df = raw.xs(ticker, axis=1, level=-1).copy()
        else:
            return pd.DataFrame()
    else:
        df = raw.copy()

    df = df.rename(columns=str.title)
    expected = ["Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in expected if col not in df.columns]
    if missing:
        return pd.DataFrame()

    df = df[expected].dropna()
    df.index = pd.to_datetime(df.index)
    return df


def download_weekly_batches(tickers: list[str], period: str, batch_size: int, pause_seconds: float) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    total = len(tickers)
    for start in range(0, total, batch_size):
        batch = tickers[start : start + batch_size]
        print(f"Downloading weekly OHLCV {start + 1}-{start + len(batch)} of {total}...")
        raw = yf.download(
            batch,
            period=period,
            interval="1wk",
            auto_adjust=False,
            group_by="ticker",
            threads=True,
            progress=False,
        )
        for ticker in batch:
            frame = normalize_download_frame(raw, ticker)
            if not frame.empty:
                frames[ticker] = frame
        if pause_seconds and start + batch_size < total:
            time.sleep(pause_seconds)
    return frames


def latest_market_close_date() -> str:
    try:
        spy = yf.download("SPY", period="10d", interval="1d", auto_adjust=False, progress=False)
        if spy.empty:
            return "n/a"
        return pd.to_datetime(spy.index[-1]).strftime("%Y-%m-%d")
    except Exception:
        return "n/a"


def candidate_to_row(meta: pd.Series, candidate: PatternCandidate) -> dict[str, object]:
    score_label, score_meaning = score_interpretation(candidate.score)
    breakout_gain_pct = (candidate.breakout_level / candidate.last_close - 1.0) * 100.0
    target_gain_pct = (candidate.projected_target / candidate.last_close - 1.0) * 100.0
    target_return_from_breakout_pct = (candidate.projected_target / candidate.breakout_level - 1.0) * 100.0
    handle_risk_pct = (candidate.handle_low_price / candidate.last_close - 1.0) * 100.0
    return {
        "Symbol": meta["Symbol"],
        "YahooSymbol": meta["YahooSymbol"],
        "Company": meta["Security"],
        "Sector": meta["GICS Sector"],
        "Industry": meta["GICS Sub-Industry"],
        "Score": candidate.score,
        "ScoreBand": score_label,
        "ScoreMeaning": score_meaning,
        "Bucket": candidate.scanner_bucket,
        "Status": candidate.status,
        "LatestDate": candidate.last_date,
        "LatestClose": candidate.last_close,
        "BreakoutLevel": candidate.breakout_level,
        "BreakoutGainPct": round(breakout_gain_pct, 2),
        "MeasuredTarget": candidate.projected_target,
        "TargetGainPct": round(target_gain_pct, 2),
        "TargetReturnPct": round(target_return_from_breakout_pct, 2),
        "HandleLow": candidate.handle_low_price,
        "HandleRiskPct": round(handle_risk_pct, 2),
        "LeftRimDate": candidate.left_rim_date,
        "LeftRimPrice": candidate.left_rim_price,
        "CupLowDate": candidate.bottom_date,
        "CupLowPrice": candidate.bottom_price,
        "RightRimDate": candidate.right_rim_date,
        "RightRimPrice": candidate.right_rim_price,
        "HandleLowDate": candidate.handle_low_date,
        "CupDepthPct": candidate.cup_depth_pct,
        "HandleDepthPctOfCup": candidate.handle_depth_pct_of_cup,
        "RimGapPct": candidate.right_rim_gap_pct,
        "CupWidthWeeks": candidate.cup_width_weeks,
        "HandleWidthWeeks": candidate.handle_width_weeks,
        "VolumeNote": candidate.volume_note,
        "Notes": "; ".join(candidate.notes),
    }


def scan_universe(universe: pd.DataFrame, frames: dict[str, pd.DataFrame], min_score: float) -> tuple[pd.DataFrame, list[dict[str, object]]]:
    selected_rows: list[dict[str, object]] = []
    audit_rows: list[dict[str, object]] = []

    for _, meta in universe.iterrows():
        yahoo = meta["YahooSymbol"]
        frame = frames.get(yahoo)
        if frame is None or frame.empty:
            audit_rows.append({"Symbol": meta["Symbol"], "Company": meta["Security"], "Status": "no data"})
            continue
        try:
            patterns = find_patterns(frame)
            primary = select_primary(patterns)
        except Exception as exc:  # defensive: keep the full scan moving
            audit_rows.append({"Symbol": meta["Symbol"], "Company": meta["Security"], "Status": f"scan error: {exc}"})
            continue

        if not primary:
            audit_rows.append({"Symbol": meta["Symbol"], "Company": meta["Security"], "Status": "no pattern"})
            continue

        audit_rows.append(
            {
                "Symbol": meta["Symbol"],
                "Company": meta["Security"],
                "Status": primary.status,
                "Score": primary.score,
                "Bucket": primary.scanner_bucket,
            }
        )
        if primary.scanner_bucket == "Cup and Handle Pattern in Force" and primary.score >= min_score:
            selected_rows.append(candidate_to_row(meta, primary))

    selected = pd.DataFrame(selected_rows)
    if not selected.empty:
        selected = selected.sort_values(["Score", "TargetGainPct"], ascending=[False, False]).reset_index(drop=True)
    return selected, audit_rows


def write_markdown_report(
    selected: pd.DataFrame,
    audit_rows: list[dict[str, object]],
    output: Path,
    *,
    universe_count: int,
    data_count: int,
    latest_weekly_bar: str,
    market_close_date: str,
    min_score: float,
    period: str,
    top_n: int,
    total_selected_before_top_n: int,
) -> None:
    def markdown_table(frame: pd.DataFrame) -> str:
        if frame.empty:
            return ""
        headers = [str(col) for col in frame.columns]
        rows = []
        for _, row in frame.iterrows():
            rows.append([str(row[col]).replace("|", "\\|") for col in frame.columns])
        output_lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        output_lines.extend("| " + " | ".join(row) + " |" for row in rows)
        return "\n".join(output_lines)

    lines = [
        "# S&P 500 Cup-And-Handle Pattern In Force Scan",
        "",
        f"Generated from weekly OHLCV data through latest available weekly bar `{latest_weekly_bar}`.",
        f"Latest broad-market daily close check: SPY close date `{market_close_date}`.",
        f"Universe source: `{SP500_WIKI_URL}`.",
        f"Universe size: {universe_count}; tickers with usable yfinance weekly data: {data_count}.",
        f"Lookback: `{period}`. Minimum selected score: `{min_score}`. Kept top `{top_n}` scores only.",
        "",
        "This is technical-pattern research, not investment advice.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Pattern in Force selections before top-N filter | {total_selected_before_top_n} |",
        f"| Pattern in Force selections kept | {len(selected)} |",
        f"| Scanned tickers with data | {data_count} |",
        f"| Failed/no-data tickers | {sum(1 for row in audit_rows if row.get('Status') == 'no data')} |",
        "",
        "## Score Meaning",
        "",
        "| Score band | Meaning |",
        "| --- | --- |",
        "| 75-100 | Strong: clean geometry and stronger confirmation traits. |",
        "| 60-74 | Good watchlist: pattern is usable but still needs confirmation. |",
        "| 45-59 | Speculative watchlist: recognizable shape, but quality issues remain. |",
        "| Below 45 | Weak: too many geometry/confirmation problems. |",
        "",
        "Score is pattern quality, not a probability forecast. It rewards cup symmetry, reasonable depth, rim alignment, handle quality, proximity to breakout, and healthier volume behavior.",
        "",
        "## Refined Textbook Filters Used",
        "",
        "- Minimum cup width is 20 weekly bars, matching TradingView's documented auto-pattern minimum.",
        "- Cup low must sit near the middle of the cup, and the cup must pass a rounded U-shape fit check.",
        "- Cup depth must be moderate: 12%-45% in this scanner, with higher scores near the 20%-30% textbook zone.",
        "- Cup rims must be close: rim deviation is measured against cup height, not only raw price percentage.",
        "- Handle must be shorter than the cup, stay in the upper half, and retrace no more than 45% of cup depth.",
        "- Pattern bucket is kept as `Cup and Handle Pattern in Force`, meaning active/formed and waiting for breakout.",
        "- Rule references used: TradingView Cup and Handle auto-pattern docs, TrendSpider chart-pattern recognition docs, and classic O'Neil-style guidance on U-shaped cups and upper-half handles.",
        "",
        "## Ranked Pattern In Force Selections",
        "",
    ]

    if selected.empty:
        lines.append("No S&P 500 stocks passed the Pattern in Force filter.")
    else:
        table_cols = [
            "Symbol",
            "Company",
            "Sector",
            "Score",
            "ScoreBand",
            "LatestClose",
            "BreakoutLevel",
            "BreakoutGainPct",
            "MeasuredTarget",
            "TargetGainPct",
            "TargetReturnPct",
            "HandleLow",
            "HandleRiskPct",
            "CupDepthPct",
            "HandleDepthPctOfCup",
            "CupWidthWeeks",
            "HandleWidthWeeks",
        ]
        table = selected[table_cols].copy()
        table.insert(0, "Rank", range(1, len(table) + 1))
        lines.append(markdown_table(table))
        lines += [
            "",
            "## Pattern Dates",
            "",
        ]
        date_cols = [
            "Symbol",
            "LeftRimDate",
            "LeftRimPrice",
            "CupLowDate",
            "CupLowPrice",
            "RightRimDate",
            "RightRimPrice",
            "HandleLowDate",
            "LatestDate",
        ]
        lines.append(markdown_table(selected[date_cols]))
        lines += [
            "",
            "## Notes By Ticker",
            "",
        ]
        for _, row in selected.iterrows():
            lines.append(
                f"- **{row['Symbol']} ({row['Company']})**: {row['Bucket']}; {row['Status']}; "
                f"breakout `{row['BreakoutLevel']}`, target `{row['MeasuredTarget']}`. {row['Notes']}"
            )

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--period", default="2y")
    parser.add_argument("--batch-size", type=int, default=80)
    parser.add_argument("--pause-seconds", type=float, default=1.0)
    parser.add_argument("--min-score", type=float, default=45.0)
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--output-dir", default="reports/cup_handle_sp500")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    universe = load_sp500_universe()
    frames = download_weekly_batches(universe["YahooSymbol"].tolist(), args.period, args.batch_size, args.pause_seconds)
    selected, audit_rows = scan_universe(universe, frames, args.min_score)
    total_selected = len(selected)
    if args.top_n > 0 and not selected.empty:
        selected = selected.head(args.top_n).copy()

    latest_dates = [frame.index[-1].strftime("%Y-%m-%d") for frame in frames.values() if not frame.empty]
    latest_weekly_bar = max(latest_dates) if latest_dates else "n/a"
    market_close_date = latest_market_close_date()

    csv_path = output_dir / "sp500_cup_handle_pattern_in_force.csv"
    md_path = output_dir / "sp500_cup_handle_pattern_in_force.md"
    audit_path = output_dir / "sp500_cup_handle_scan_audit.json"

    selected.to_csv(csv_path, index=False)
    audit_path.write_text(json.dumps(audit_rows, indent=2), encoding="utf-8")
    write_markdown_report(
        selected,
        audit_rows,
        md_path,
        universe_count=len(universe),
        data_count=len(frames),
        latest_weekly_bar=latest_weekly_bar,
        market_close_date=market_close_date,
        min_score=args.min_score,
        period=args.period,
        top_n=args.top_n,
        total_selected_before_top_n=total_selected,
    )

    print(f"universe={len(universe)}")
    print(f"data_frames={len(frames)}")
    print(f"selected_before_top_n={total_selected}")
    print(f"selected_kept={len(selected)}")
    print(f"latest_weekly_bar={latest_weekly_bar}")
    print(f"market_close_date={market_close_date}")
    print(f"csv={csv_path}")
    print(f"report={md_path}")
    print(f"audit={audit_path}")
    if not selected.empty:
        print(selected[["Symbol", "Company", "Score", "BreakoutLevel", "MeasuredTarget"]].head(20).to_string(index=False))


if __name__ == "__main__":
    main()
