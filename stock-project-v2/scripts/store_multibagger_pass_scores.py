#!/usr/bin/env python3
"""Validate, persist, and reconcile Multi Bagger six-pass snapshots."""
from __future__ import annotations

import argparse, csv, io, json, os, re, sys, tempfile
from datetime import date, datetime
from pathlib import Path

PASS_KEYS = (
    "pass_1_primary_source_inventory", "pass_2_financial_reconstruction",
    "pass_3_forward_expectations", "pass_4_risk_moat_sector_review",
    "pass_5_technical_review", "pass_6_adversarial_audit",
)
PASS_STATUSES = {"complete", "partial", "incomplete", "not_applicable", "legacy_not_captured", "legacy_score_only"}
CONFIDENCE = {"high", "medium_high", "medium", "low_medium", "low", "unknown"}
RUN_TYPES = {"regular_refresh", "research_rerun", "correction", "legacy_import"}
ENTRY_STATUSES = {"hit", "not_hit", "below", "above", "unknown", "no_zone"}
THESIS_STATUSES = {"strengthened", "intact", "intact_with_caveats", "weakened", "broken", "under_review", "legacy_note_only"}
TICKER_RE = re.compile(r"^[A-Z0-9.\-]{1,15}$")
HISTORY_COLUMNS = (
    "snapshot_id", "run_date", "snapshot_revision", "market_session_date", "run_type", "methodology_version",
    "ticker", "rank", "rank_delta", "market_cap_usd", "multi_bagger_score", "multi_bagger_score_delta",
    "expectation_valuation_score", "expectation_valuation_score_delta", "weekly_technical_score",
    "weekly_technical_score_delta", "pass_1_score", "pass_1_status", "pass_1_completion_pct",
    "pass_2_score", "pass_2_status", "pass_2_completion_pct", "pass_3_score", "pass_3_status",
    "pass_3_completion_pct", "pass_4_score", "pass_4_status", "pass_4_completion_pct", "pass_5_score",
    "pass_5_status", "pass_5_completion_pct", "pass_6_score", "pass_6_status", "pass_6_completion_pct",
    "probability_5x_pct", "data_confidence", "action", "thesis_status", "entry_zone_hit_status",
)

class ValidationError(ValueError): pass

def req(ok, msg):
    if not ok: raise ValidationError(msg)

def keys(obj, required, ctx):
    req(isinstance(obj, dict), f"{ctx}: object required")
    missing = [x for x in required if x not in obj]
    req(not missing, f"{ctx}: missing {missing}")

def iso_date(value, ctx):
    req(isinstance(value, str), f"{ctx}: YYYY-MM-DD required")
    try: parsed = date.fromisoformat(value)
    except ValueError as exc: raise ValidationError(f"{ctx}: invalid date {value!r}") from exc
    req(parsed.isoformat() == value, f"{ctx}: normalized YYYY-MM-DD required")

def iso_time(value, ctx):
    if value is None: return
    req(isinstance(value, str), f"{ctx}: ISO timestamp or null required")
    try: datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc: raise ValidationError(f"{ctx}: invalid timestamp") from exc

def number(value, ctx, low=None, high=None, integer=False, nullable=True):
    if value is None:
        req(nullable, f"{ctx}: null not allowed"); return
    good = isinstance(value, int) and not isinstance(value, bool) if integer else isinstance(value, (int, float)) and not isinstance(value, bool)
    req(good, f"{ctx}: {'integer' if integer else 'number'} required")
    if low is not None: req(value >= low, f"{ctx}: must be >= {low}")
    if high is not None: req(value <= high, f"{ctx}: must be <= {high}")

def string_list(value, ctx):
    req(isinstance(value, list), f"{ctx}: array required")
    req(all(isinstance(x, str) and x.strip() for x in value), f"{ctx}: non-empty strings required")
    req(len(value) == len(set(value)), f"{ctx}: duplicates not allowed")

def validate_pass(record, key, ticker):
    ctx = f"{ticker}.{key}"
    keys(record, ("status", "score", "completion_pct", "confidence", "source_ids", "findings", "missing_fields"), ctx)
    status, score, completion = record["status"], record["score"], record["completion_pct"]
    req(status in PASS_STATUSES, f"{ctx}.status: unsupported")
    number(score, f"{ctx}.score", 0, 100, True)
    number(completion, f"{ctx}.completion_pct", 0, 100, True)
    req(record["confidence"] is None or record["confidence"] in CONFIDENCE, f"{ctx}.confidence: unsupported")
    for field in ("source_ids", "findings", "missing_fields"): string_list(record[field], f"{ctx}.{field}")
    if status == "complete":
        req(score is not None and completion == 100, f"{ctx}: complete requires score and completion_pct=100")
    elif status == "partial":
        req(completion is not None and 0 < completion < 100 and record["missing_fields"], f"{ctx}: partial requires 1-99 completion and missing_fields")
    elif status == "legacy_score_only":
        req(score is not None and completion is None, f"{ctx}: legacy_score_only requires score and null completion")
    elif status in {"legacy_not_captured", "not_applicable"}:
        req(score is None and completion is None, f"{ctx}: status requires null score/completion")
    elif status == "incomplete":
        req(score is None and record["missing_fields"], f"{ctx}: incomplete requires null score and missing_fields")

def snapshot_id(snapshot):
    return snapshot["run_date"] if snapshot["snapshot_revision"] == 1 else f"{snapshot['run_date']}-r{snapshot['snapshot_revision']}"

def sort_key(snapshot): return date.fromisoformat(snapshot["run_date"]), snapshot["snapshot_revision"]

def validate_snapshot(snapshot, require_complete=False):
    required = ("schema_version", "methodology_version", "run_date", "snapshot_revision", "market_session_date", "run_type",
        "generated_at", "recorded_at", "source_time_precision", "price_basis", "universe_size", "changes", "corrections",
        "record_limitations", "stocks")
    keys(snapshot, required, "snapshot")
    req(snapshot["schema_version"] == "1.0.0", "schema_version must be 1.0.0")
    req(isinstance(snapshot["methodology_version"], str) and snapshot["methodology_version"].strip(), "methodology_version required")
    iso_date(snapshot["run_date"], "run_date"); iso_date(snapshot["market_session_date"], "market_session_date")
    req(date.fromisoformat(snapshot["market_session_date"]) <= date.fromisoformat(snapshot["run_date"]), "market_session_date after run_date")
    number(snapshot["snapshot_revision"], "snapshot_revision", 1, integer=True, nullable=False)
    req(snapshot["run_type"] in RUN_TYPES, "unsupported run_type")
    iso_time(snapshot["generated_at"], "generated_at"); iso_time(snapshot["recorded_at"], "recorded_at")
    req(snapshot["source_time_precision"] in {"exact", "date_only", "legacy_unknown"}, "unsupported source_time_precision")
    if snapshot["source_time_precision"] == "exact": req(snapshot["generated_at"] is not None, "exact source time requires generated_at")
    req(isinstance(snapshot["price_basis"], str) and snapshot["price_basis"].strip(), "price_basis required")
    number(snapshot["universe_size"], "universe_size", 1, integer=True, nullable=False)
    keys(snapshot["changes"], ("top20_additions", "top20_removals", "index_etf_changes", "entry_zone_hits", "notes"), "changes")
    for field in ("top20_additions", "top20_removals", "index_etf_changes", "entry_zone_hits", "notes"): string_list(snapshot["changes"][field], f"changes.{field}")
    req(isinstance(snapshot["corrections"], list), "corrections: array required")
    for i, correction in enumerate(snapshot["corrections"]):
        keys(correction, ("ticker", "field", "prior_value", "corrected_value", "reason"), f"corrections[{i}]")
        req(correction["ticker"] is None or (isinstance(correction["ticker"], str) and TICKER_RE.fullmatch(correction["ticker"])), f"corrections[{i}].ticker invalid")
        req(isinstance(correction["field"], str) and correction["field"].strip(), f"corrections[{i}].field required")
        req(isinstance(correction["reason"], str) and correction["reason"].strip(), f"corrections[{i}].reason required")
    if snapshot["run_type"] == "correction": req(snapshot["corrections"], "correction run requires correction record")
    string_list(snapshot["record_limitations"], "record_limitations")
    req(isinstance(snapshot["stocks"], list) and len(snapshot["stocks"]) == snapshot["universe_size"], "stocks/universe_size mismatch")
    tickers, ranks = set(), set()
    stock_required = ("ticker", "rank", "rank_delta", "market_cap_usd", "market_cap_display", "multi_bagger_score",
        "multi_bagger_score_delta", "expectation_valuation_score", "expectation_valuation_score_delta", "weekly_technical_score",
        "weekly_technical_score_delta", "probability_5x_pct", "data_confidence", "action", "thesis_status", "thesis_note", "entry_zone", "passes")
    for stock in snapshot["stocks"]:
        keys(stock, stock_required, "stock")
        ticker = stock["ticker"]
        req(isinstance(ticker, str) and TICKER_RE.fullmatch(ticker) and ticker not in tickers, f"invalid/duplicate ticker {ticker}"); tickers.add(ticker)
        number(stock["rank"], f"{ticker}.rank", 1, integer=True, nullable=False); req(stock["rank"] not in ranks, f"duplicate rank {stock['rank']}"); ranks.add(stock["rank"])
        number(stock["rank_delta"], f"{ticker}.rank_delta", integer=True); number(stock["market_cap_usd"], f"{ticker}.market_cap_usd", 0, integer=True)
        req(isinstance(stock["market_cap_display"], str), f"{ticker}.market_cap_display required")
        for field in ("multi_bagger_score", "expectation_valuation_score", "weekly_technical_score", "probability_5x_pct"): number(stock[field], f"{ticker}.{field}", 0, 100, True)
        for field in ("multi_bagger_score_delta", "expectation_valuation_score_delta", "weekly_technical_score_delta"): number(stock[field], f"{ticker}.{field}", integer=True)
        req(stock["data_confidence"] in CONFIDENCE and isinstance(stock["action"], str) and stock["action"].strip(), f"{ticker}: confidence/action invalid")
        req(stock["thesis_status"] in THESIS_STATUSES and isinstance(stock["thesis_note"], str), f"{ticker}: thesis invalid")
        zone = stock["entry_zone"]; keys(zone, ("display", "low", "high", "qualifier", "hit_status"), f"{ticker}.entry_zone")
        req(isinstance(zone["display"], str) and zone["hit_status"] in ENTRY_STATUSES, f"{ticker}: entry zone invalid")
        number(zone["low"], f"{ticker}.entry_zone.low", 0); number(zone["high"], f"{ticker}.entry_zone.high", 0)
        if zone["low"] is not None and zone["high"] is not None: req(zone["low"] <= zone["high"], f"{ticker}: entry low > high")
        req(zone["qualifier"] is None or isinstance(zone["qualifier"], str), f"{ticker}: entry qualifier invalid")
        req(isinstance(stock["passes"], dict) and set(stock["passes"]) == set(PASS_KEYS), f"{ticker}: exactly six passes required")
        for key in PASS_KEYS: validate_pass(stock["passes"][key], key, ticker)
        p5 = stock["passes"][PASS_KEYS[4]]["score"]
        if p5 is not None and stock["weekly_technical_score"] is not None: req(p5 == stock["weekly_technical_score"], f"{ticker}: P5 != weekly technical")
        if snapshot["run_type"] == "regular_refresh": req(not any(stock["passes"][k]["status"].startswith("legacy_") for k in PASS_KEYS), f"{ticker}: regular refresh has legacy pass")
        if require_complete:
            for key in PASS_KEYS:
                record = stock["passes"][key]
                req(record["status"] == "complete" and record["completion_pct"] == 100 and record["source_ids"] and record["findings"], f"{ticker}.{key}: complete sourced pass required")
    req(ranks == set(range(1, len(snapshot["stocks"]) + 1)), "ranks must be contiguous from 1")
    if require_complete: req(snapshot["generated_at"] and snapshot["recorded_at"], "complete run requires timestamps")

def validate_evidence(evidence, snapshot):
    keys(evidence, ("schema_version", "run_date", "snapshot_revision", "sources", "limitations"), "evidence")
    req(evidence["schema_version"] == "1.0.0" and evidence["run_date"] == snapshot["run_date"] and evidence["snapshot_revision"] == snapshot["snapshot_revision"], "evidence identity mismatch")
    req(isinstance(evidence["sources"], list), "evidence.sources: array required"); string_list(evidence["limitations"], "evidence.limitations")
    ids = set()
    for i, source in enumerate(evidence["sources"]):
        keys(source, ("source_id", "source_type", "title", "source_date", "retrieved_at", "locator", "content_sha256", "notes"), f"source[{i}]")
        sid = source["source_id"]; req(isinstance(sid, str) and sid.strip() and sid not in ids, f"source[{i}].source_id invalid"); ids.add(sid)
        req(isinstance(source["source_type"], str) and source["source_type"].strip() and isinstance(source["title"], str) and source["title"].strip(), f"source[{i}] type/title invalid")
        if source["source_date"] is not None: iso_date(source["source_date"], f"source[{i}].source_date")
        iso_time(source["retrieved_at"], f"source[{i}].retrieved_at")
        req(source["locator"] is None or isinstance(source["locator"], str), f"source[{i}].locator invalid")
        req(source["content_sha256"] is None or re.fullmatch(r"[0-9a-f]{64}", source["content_sha256"]), f"source[{i}].content_sha256 invalid")
        req(isinstance(source["notes"], str), f"source[{i}].notes invalid")
    referenced = {sid for stock in snapshot["stocks"] for key in PASS_KEYS for sid in stock["passes"][key]["source_ids"]}
    req(referenced <= ids, f"missing evidence source_ids {sorted(referenced - ids)}")

def canonical_json(data): return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
def csv_value(value): return "" if value is None else str(value).lower() if isinstance(value, bool) else str(value)

def history_rows(snapshot):
    result=[]
    for stock in sorted(snapshot["stocks"], key=lambda x: x["rank"]):
        row={"snapshot_id":snapshot_id(snapshot), "run_date":snapshot["run_date"], "snapshot_revision":snapshot["snapshot_revision"],
            "market_session_date":snapshot["market_session_date"], "run_type":snapshot["run_type"], "methodology_version":snapshot["methodology_version"],
            "ticker":stock["ticker"], "rank":stock["rank"], "rank_delta":stock["rank_delta"], "market_cap_usd":stock["market_cap_usd"],
            "multi_bagger_score":stock["multi_bagger_score"], "multi_bagger_score_delta":stock["multi_bagger_score_delta"],
            "expectation_valuation_score":stock["expectation_valuation_score"], "expectation_valuation_score_delta":stock["expectation_valuation_score_delta"],
            "weekly_technical_score":stock["weekly_technical_score"], "weekly_technical_score_delta":stock["weekly_technical_score_delta"],
            "probability_5x_pct":stock["probability_5x_pct"], "data_confidence":stock["data_confidence"], "action":stock["action"],
            "thesis_status":stock["thesis_status"], "entry_zone_hit_status":stock["entry_zone"]["hit_status"]}
        for i,key in enumerate(PASS_KEYS,1):
            record=stock["passes"][key]; row[f"pass_{i}_score"]=record["score"]; row[f"pass_{i}_status"]=record["status"]; row[f"pass_{i}_completion_pct"]=record["completion_pct"]
        result.append({column:csv_value(row.get(column)) for column in HISTORY_COLUMNS})
    return result

def read_history(path):
    if not path.exists(): return []
    with path.open(encoding="utf-8", newline="") as handle:
        reader=csv.DictReader(handle); req(tuple(reader.fieldnames or ()) == HISTORY_COLUMNS, f"{path}: CSV schema mismatch"); return list(reader)

def render_history(existing, new):
    rows=[]; seen={}
    for raw in [*existing, *new]:
        row={column:raw.get(column,"") for column in HISTORY_COLUMNS}; key=(row["snapshot_id"],row["ticker"])
        if key in seen: req(seen[key] == row, f"history conflict {key}"); continue
        seen[key]=row; rows.append(row)
    out=io.StringIO(newline=""); writer=csv.DictWriter(out, fieldnames=HISTORY_COLUMNS, lineterminator="\n"); writer.writeheader(); writer.writerows(rows); return out.getvalue()

def render_research_report(snapshot):
    def fmt(v):return '—' if v is None else f'{v:.1f}'
    def pct(v):return '—' if v is None else f'{100*v:.1f}%'
    lines=[f"# Multi Bagger Final {snapshot['universe_size']} — {snapshot_id(snapshot)}",'',
      f"Market session: {snapshot['market_session_date']} regular-session close. Data collected: {snapshot['generated_at']}. Watchlist publication prepared: {snapshot['recorded_at']}.",'',
      '**Research calibration, not reproduced official scores.** All five new names were added; all prior 20 retained. No Stock Project V2 data or scoring changes. No P(5x) probability model has been calibrated.','',
      '| Rank | Ticker | Price | Market cap | MB research | E&V research | Technical research | MB coverage | E&V coverage | New |',
      '|---:|---|---:|---:|---:|---:|---:|---:|---:|---|']
    for s in snapshot['stocks']:
        r=s['metadata']['research']
        lines.append(f"| {s['rank']} | {s['ticker']} | ${r['price']:,.2f} | {s['market_cap_display']} | {fmt(r['research_mb_score'])} | {fmt(r['research_ev_score'])} | {fmt(r['technical_score'])} | {pct(r['mb_input_weight_coverage'])} | {pct(r['ev_input_weight_coverage'])} | {'Yes' if s['metadata']['new_member'] else ''} |")
    lines+=['','E&V with 70% input coverage is valuation-only, not a complete E&V comparison. Coverage is input weight, NOT completion of the six research passes.','', '## Changes', '', 'Additions: '+', '.join(snapshot['changes']['top20_additions'])+'. Removals: none.','Score and rank deltas against the older calibration: not comparable (not zero).','Legacy preferred-entry ranges hit at the September 4 close: '+', '.join(snapshot['changes']['entry_zone_hits'])+'.']
    for s in snapshot['stocks']:
        m=s['metadata'];r=m['research'];t=m['technical'];zone=s['entry_zone'];prior=m.get('prior_archive')
        lines+=['',f"## {s['ticker']} — {m['company']['name']}",'',f"**{s['action']}**. Thesis: {s['thesis_status']}. Data confidence: {s['data_confidence']}. Final watchlist member: yes.",
         f"Sector: {m['sector']}; sector trend: {m['sector_trend']} (analyst judgment). {m['sector_drivers_risks']}",'',s['thesis_note'],'',
         f"Preferred entry: {zone['display']} ({zone['hit_status']}). {zone.get('qualifier') or ''}",
         f"Chart references only: 20-day low ${t['low20']:.2f}; 20-day high ${t['high20']:.2f}; 20/50/200-day averages ${t['ma20']:.2f}/${t['ma50']:.2f}/${t['ma200']:.2f}. RSI14 {t['rsi14']:.1f}, MACD histogram {t['macd_hist']:.4f}, ADX14 {t['adx14']:.1f}.",
         f"Sensitivity rank: {r['weight_rank_low']}–{r['weight_rank_high']}. Missing-input score bounds: {fmt(r['unknown_lower_bound'])}–{fmt(r['unknown_upper_bound'])}. These are not statistical confidence intervals.",'',
         '### Financial and expectation inputs','', '| Metric | Value |','|---|---:|']
        for k in ['financial_period_end','revenue_ttm','gross_profit_ttm','operating_income_ttm','cfo_ttm','capex_ttm','fcf_ttm','cash','debt','current_growth','current_growth_basis','next_year_growth','next_year_revenue','eps_revision90','dilution_yoy','dilution_basis','ev_forward_gp','fcf_yield']:
            v=r.get(k);lines.append(f"| {k} | {'—' if v is None else v} |")
        lines+=['','### ETF / index evidence','',m['membership_confidence']]
        for h in m['etf_holdings']:lines.append(f"- {h['fund']}: {h['weight_pct']}%; {h['as_of']}; benchmark {h['benchmark']}. [Primary holdings]({h['source']})")
        lines+=['','### Audit findings','']+['- '+x for x in r['issues']]
        lines+=['','### Six-pass scope','']
        for key,p in s['passes'].items():lines.append(f"- {key}: {p['status']}. {' '.join(p['findings'])} Remaining: {', '.join(p['missing_fields']) or 'None for the research technical calculation.'}")
        if prior:lines+=['',f"Prior archive ({prior['run_date']}, different calibration): rank {prior['rank']}, MB {prior['mb']}, E&V {prior['ev']}, technical {prior['technical']}. Not comparable with this run's research scores."]
        lines+=['','### Sources','']+[f"- [{x['source_kind']}]({x['locator']})" for x in m['sources']]
    lines+=['','## Limitations','']+['- '+x for x in snapshot['record_limitations']]
    return '\n'.join(lines)+'\n'

def render_report(snapshot):
    if snapshot.get("metadata", {}).get("display_mode") == "common_calibration_research":
        return render_research_report(snapshot)
    lines=[f"# Multi Bagger Pass-Score Snapshot — {snapshot_id(snapshot)}", "", f"- Run date: `{snapshot['run_date']}`", f"- Market session used: `{snapshot['market_session_date']}`",
        f"- Methodology: `{snapshot['methodology_version']}`", f"- Run type: `{snapshot['run_type']}`", f"- Price basis: {snapshot['price_basis']}", "", "## Rankings and pass scores", "",
        "| Rank | Ticker | Market cap | MB | E&V | P1 | P2 | P3 | P4 | P5 | P6 | P(5×) | Action | Confidence |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for stock in sorted(snapshot["stocks"], key=lambda x:x["rank"]):
        cells=[]
        for key in PASS_KEYS:
            record=stock["passes"][key]; value="—" if record["score"] is None else str(record["score"])
            cells.append(value if record["status"] == "complete" else f"{value} ({record['status']})")
        lines.append(f"| {stock['rank']} | {stock['ticker']} | {stock['market_cap_display']} | {stock['multi_bagger_score']} | {stock['expectation_valuation_score']} | {' | '.join(cells)} | {stock['probability_5x_pct']}% | {stock['action'].replace('|','\\|')} | {stock['data_confidence']} |")
    lines += ["", "## Thesis and correction notes", ""]
    lines += [f"- **{s['ticker']} — {s['thesis_status']}:** {s['thesis_note'].strip() or 'No note recorded.'}" for s in sorted(snapshot["stocks"], key=lambda x:x["rank"])]
    if snapshot["corrections"]:
        lines += ["", "## Corrections", ""] + [f"- **{c.get('ticker') or 'Portfolio'} / {c.get('field','unspecified field')}:** {c.get('reason','No reason recorded.')}" for c in snapshot["corrections"]]
    if snapshot["record_limitations"]: lines += ["", "## Record limitations", ""] + [f"- {x}" for x in snapshot["record_limitations"]]
    return "\n".join(lines)+"\n"

def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True); fd,tmp=tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    try:
        with os.fdopen(fd,"w",encoding="utf-8",newline="") as handle: handle.write(content); handle.flush(); os.fsync(handle.fileno())
        os.replace(tmp,path)
    except Exception:
        try: os.unlink(tmp)
        except FileNotFoundError: pass
        raise

def immutable(path, content):
    if path.exists(): req(path.read_text(encoding="utf-8") == content, f"immutable artifact conflict: {path}")
def artifact(snapshot,suffix): return f"{snapshot_id(snapshot)}{suffix}"
def load_json(path):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc: raise ValidationError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc: raise ValidationError(f"invalid JSON in {path}: {exc}") from exc

def persist_snapshot(snapshot, project_root, evidence=None, dry_run=False, require_complete=False):
    validate_snapshot(snapshot, require_complete)
    if evidence is not None: validate_evidence(evidence,snapshot)
    else: req(not {sid for stock in snapshot["stocks"] for key in PASS_KEYS for sid in stock["passes"][key]["source_ids"]}, "evidence manifest required")
    base=project_root/"data"/"multi_bagger"; snap=base/"pass_scores"/artifact(snapshot,".json"); latest=base/"pass_scores"/"latest.json"
    evid=base/"evidence"/artifact(snapshot,".json"); hist=base/"history"/"pass_score_history.csv"; report=project_root/"reports"/"multi_bagger"/artifact(snapshot,".md")
    snap_text=canonical_json(snapshot); evid_text=canonical_json(evidence) if evidence is not None else None; report_text=render_report(snapshot); hist_text=render_history(read_history(hist),history_rows(snapshot))
    immutable(snap,snap_text); immutable(report,report_text)
    if evid_text is not None: immutable(evid,evid_text)
    update_latest=True
    if latest.exists(): current=load_json(latest); validate_snapshot(current); update_latest=sort_key(snapshot) >= sort_key(current)
    planned=[snap,hist,report]+([evid] if evid_text is not None else [])+([latest] if update_latest else [])
    if dry_run: return planned
    atomic_write(snap,snap_text)
    if evid_text is not None: atomic_write(evid,evid_text)
    atomic_write(report,report_text); atomic_write(hist,hist_text)
    if update_latest: atomic_write(latest,snap_text)
    return planned

def verify_repository(project_root, require_complete=False):
    base=project_root/"data"/"multi_bagger"; pass_dir=base/"pass_scores"; paths=sorted(p for p in pass_dir.glob("*.json") if p.name != "latest.json"); req(paths, f"no snapshots under {pass_dir}")
    snapshots=[]; expected={}
    for path in paths:
        snapshot=load_json(path); validate_snapshot(snapshot,require_complete); req(path.name == artifact(snapshot,".json"), f"bad snapshot filename {path.name}")
        for row in history_rows(snapshot):
            key=(row["snapshot_id"],row["ticker"]); req(key not in expected, f"duplicate snapshot row {key}"); expected[key]=row
        referenced={sid for stock in snapshot["stocks"] for pkey in PASS_KEYS for sid in stock["passes"][pkey]["source_ids"]}
        if referenced: validate_evidence(load_json(base/"evidence"/artifact(snapshot,".json")),snapshot)
        report=project_root/"reports"/"multi_bagger"/artifact(snapshot,".md"); req(report.exists() and report.read_text(encoding="utf-8") == render_report(snapshot), f"missing/stale report {report}")
        snapshots.append(snapshot)
    actual={}
    for row in read_history(base/"history"/"pass_score_history.csv"):
        key=(row["snapshot_id"],row["ticker"]); req(key not in actual, f"duplicate CSV row {key}"); actual[key]=row
    req(actual == expected, "CSV does not match canonical snapshots")
    latest=load_json(pass_dir/"latest.json"); validate_snapshot(latest); req(canonical_json(latest) == canonical_json(max(snapshots,key=sort_key)), "latest.json mismatch")
    return {"snapshots":len(snapshots),"history_rows":len(actual),"stocks_in_latest":len(latest["stocks"])}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("snapshot",nargs="?",type=Path); parser.add_argument("--evidence",type=Path)
    parser.add_argument("--project-root",type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument("--dry-run",action="store_true")
    parser.add_argument("--verify-repository",action="store_true"); parser.add_argument("--require-complete",action="store_true"); args=parser.parse_args(argv)
    try:
        root=args.project_root.resolve()
        if args.verify_repository:
            req(args.snapshot is None,"snapshot not used with --verify-repository"); result=verify_repository(root,args.require_complete)
            print(f"Verified Multi Bagger repository: {result['snapshots']} snapshot(s), {result['history_rows']} history row(s), {result['stocks_in_latest']} stock(s) in latest."); return 0
        req(args.snapshot is not None,"snapshot JSON required"); snapshot=load_json(args.snapshot.resolve()); evidence=load_json(args.evidence.resolve()) if args.evidence else None
        paths=persist_snapshot(snapshot,root,evidence,args.dry_run,args.require_complete); print(f"{'Validated' if args.dry_run else 'Persisted'} Multi Bagger snapshot {snapshot_id(snapshot)}:")
        for path in paths: print(f"- {path.relative_to(root)}")
        return 0
    except ValidationError as exc: print(f"ERROR: {exc}",file=sys.stderr); return 2

if __name__ == "__main__": raise SystemExit(main())
