"""Audited, network-free scoring replay of the latest completed-session inputs.

This is an explicit methodology migration, not a market-data fallback. The
normal live-data workflow and its completed-session guards remain unchanged.
"""
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import pandas_market_calendars as mcal

import run_v2 as engine
from materialize_decisions import apply_fields, write_json

ROOT = Path(__file__).resolve().parent
SCORE_COLUMNS = ["long_term_score", "short_term_score", "buy_now_score"]


def archive(path: Path, folder: Path) -> str:
    content = path.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    destination = folder / f"{path.stem}-{digest[:12]}{path.suffix}"
    folder.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_bytes(content)
    return digest


def main() -> int:
    now = datetime.now(engine.TZ)
    schedule = mcal.get_calendar("NYSE").schedule(
        start_date=now.date() - timedelta(days=14), end_date=now.date()
    )
    completed = schedule[schedule.market_close + pd.Timedelta(minutes=15) <= pd.Timestamp(now)]
    if completed.empty:
        raise RuntimeError("No completed NYSE session")
    required_date = completed.index[-1].date().isoformat()
    path = ROOT / "latest_scores.csv"
    before = pd.read_csv(path)
    config = engine.CONFIG
    if config.get("scoring_version") != "2.3-no-leverage-penalty":
        raise RuntimeError("This audited replay is limited to the no-leverage-penalty migration")
    if config["etf_scoring"]["leveraged_long_term_penalty"] != 0:
        raise RuntimeError("The requested zero-penalty policy is not active")
    expected = set(config["universe"])
    if before.ticker.duplicated().any() or set(before.ticker) != expected:
        raise RuntimeError("Saved inputs do not match the complete configured universe")
    if not before.as_of.astype(str).eq(required_date).all():
        raise RuntimeError(f"Saved inputs must be from latest completed session {required_date}")
    if not np.isfinite(pd.to_numeric(before.price, errors="coerce")).all():
        raise RuntimeError("Saved inputs contain invalid prices")
    required = {"data_retrieved_at", "scoring_version", "scoring_fingerprint"}
    if not required.issubset(before.columns):
        raise RuntimeError("Saved input provenance is incomplete")

    canonical_path = ROOT / "canonical_market.json"
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    if canonical.get("as_of") != required_date or set(canonical.get("stocks", {})) != expected:
        raise RuntimeError("Canonical technical snapshot does not match the saved session/universe")
    for ticker, record in canonical["stocks"].items():
        if record.get("as_of") != required_date:
            raise RuntimeError(f"Mismatched canonical input date for {ticker}")

    fingerprint = engine.scoring_fingerprint()
    old_config = copy.deepcopy(config)
    old_config["scoring_version"] = "2.2-universe-normalization"
    old_config["etf_scoring"]["leveraged_long_term_penalty"] = 15
    engine.CONFIG = old_config
    try:
        old_fingerprint = engine.scoring_fingerprint()
        old_replay = engine.score(before).set_index("ticker")
    finally:
        engine.CONFIG = config
    versions = set(before.scoring_fingerprint.astype(str))
    if versions not in ({old_fingerprint}, {fingerprint}):
        raise RuntimeError("Saved inputs were produced by an unexpected scoring engine/configuration")

    recalculated = engine.score(before)
    actual = recalculated.set_index("ticker")
    saved = before.set_index("ticker")
    comparison = old_replay if versions == {old_fingerprint} else actual
    for column in SCORE_COLUMNS:
        np.testing.assert_allclose(
            saved[column], comparison.loc[saved.index, column], atol=0.100001,
            rtol=0, equal_nan=True, err_msg=f"Saved score cannot be reproduced: {column}"
        )
    # Validate the causal effect using identical inputs and the production scorer.
    for ticker in saved.index:
        leveraged = bool(config.get("etf_metadata", {}).get(ticker, {}).get("leveraged", False))
        delta = actual.at[ticker, "long_term_score"] - old_replay.at[ticker, "long_term_score"]
        expected_delta = min(15.0, actual.at[ticker, "long_term_score"]) if leveraged else 0.0
        if abs(delta - expected_delta) > 0.100001:
            raise RuntimeError(f"Unexpected policy effect on {ticker}: {delta}")
        if actual.at[ticker, "short_term_score"] != old_replay.at[ticker, "short_term_score"]:
            raise RuntimeError(f"Short-term formula unexpectedly changed for {ticker}")

    columns = list(before.columns)
    out = recalculated[columns].copy()
    out["scoring_version"] = config["scoring_version"]
    out["scoring_fingerprint"] = fingerprint
    out["scores_recomputed_at"] = now.isoformat()
    out["score_input_mode"] = "Saved latest-completed-session factor replay; no new price download"
    out = apply_fields(out).sort_values(["buy_now_score", "long_term_score"], ascending=False).reset_index(drop=True)
    out["rank"] = np.arange(1, len(out) + 1)
    # The original data_retrieved_at and as_of are deliberately retained.
    revision_folder = ROOT / "history" / "revisions" / f"{required_date}-no-leverage-penalty"
    input_sha = archive(path, revision_folder)
    archive(canonical_path, revision_folder)
    history_path = ROOT / "history" / f"{required_date}.csv"
    if history_path.exists():
        archive(history_path, revision_folder)
    out.to_csv(path, index=False)
    out.to_csv(history_path, index=False)
    write_json(out, ROOT / "latest_scores.json")

    for _, row in out.iterrows():
        target = canonical["stocks"][row.ticker]
        target.update(
            long_term_score=float(row.long_term_score),
            long_term_rating=str(row.long_term_rating),
            entry_score=float(row.entry_score),
            entry_quality=str(row.entry_quality),
            composite_score=float(row.buy_now_score),
            short_put_eligible=bool(row.short_put_eligible),
        )
    canonical["scoring_version"] = config["scoring_version"]
    canonical["scoring_fingerprint"] = fingerprint
    canonical["scores_recomputed_at"] = now.isoformat()
    canonical["score_input_mode"] = "Saved latest-completed-session factor replay; original technical snapshot retained"
    canonical_path.write_text(json.dumps(canonical, indent=2), encoding="utf-8")

    audit = {
        "as_of": required_date,
        "recomputed_at": now.isoformat(),
        "input_sha256": input_sha,
        "input_mode": "saved completed-session factors",
        "old_fingerprint": old_fingerprint,
        "new_fingerprint": fingerprint,
        "universe_size": len(out),
        "configured_leverage_penalty": 0,
        "changed": [
            {"ticker": t, "old_long_term_score": float(saved.at[t, "long_term_score"]),
             "new_long_term_score": float(actual.at[t, "long_term_score"])}
            for t in saved.index if actual.at[t, "long_term_score"] != saved.at[t, "long_term_score"]
        ],
    }
    (revision_folder / f"audit-{input_sha[:12]}.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(out[["ticker", "long_term_score", "long_term_rating", "entry_score", "short_put_eligible"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
