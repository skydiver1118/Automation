from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from signal_policy import entry_quality, long_term_rating, short_put_eligible

ROOT = Path(__file__).resolve().parent
LATEST_CSV = ROOT / "latest_scores.csv"
LATEST_JSON = ROOT / "latest_scores.json"
HISTORY = ROOT / "history"


def apply_fields(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["long_term_rating"] = out.get("long_term_score", pd.Series(index=out.index, dtype=float)).map(long_term_rating)
    out["entry_score"] = pd.to_numeric(out.get("short_term_score"), errors="coerce").round(1)
    out["entry_quality"] = out["entry_score"].map(entry_quality)
    out["short_put_eligible"] = out["long_term_rating"].map(short_put_eligible)
    return out


def write_json(df: pd.DataFrame, path: Path) -> None:
    records = json.loads(df.replace({np.nan: None}).to_json(orient="records"))
    path.write_text(json.dumps(records, indent=2), encoding="utf-8")


def main() -> int:
    df = apply_fields(pd.read_csv(LATEST_CSV))
    df.to_csv(LATEST_CSV, index=False)
    write_json(df, LATEST_JSON)

    if "as_of" in df.columns and not df.empty:
        as_of = str(df["as_of"].iloc[0])
        hist = HISTORY / f"{as_of}.csv"
        if hist.exists():
            apply_fields(pd.read_csv(hist)).to_csv(hist, index=False)

    cols = ["ticker", "long_term_score", "long_term_rating", "entry_score", "entry_quality", "short_put_eligible"]
    print(df[[c for c in cols if c in df.columns]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
