from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "config.json").read_text())
LATEST = ROOT / "latest_scores.csv"
DASH = ROOT / "dashboard" / "index.html"


def main() -> int:
    if not DASH.exists() or not LATEST.exists():
        raise RuntimeError("Dashboard or latest_scores.csv missing")

    page = DASH.read_text(encoding="utf-8")
    latest = pd.read_csv(LATEST)
    present = set(latest.get("ticker", pd.Series(dtype=str)).astype(str))
    missing = [t for t in CONFIG["universe"] if t not in present]
    if not missing:
        print("All configured securities have a completed-session score.")
        return 0

    asset_types = CONFIG.get("asset_types", {})
    pending_rows = []
    for t in missing:
        typ = asset_types.get(t, "Stock")
        badge_cls = "etf" if typ == "ETF" else ""
        note = "Pending first completed-session ETF score" if typ == "ETF" else "Pending first completed-session stock score"
        pending_rows.append(
            f"<tr class='pending-security'><td class='rank'>—</td>"
            f"<td><span class='ticker'>{t}</span><small class='pending-note'>{note}</small></td>"
            f"<td><span class='badge {badge_cls}'>{typ}</span></td>"
            "<td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td>"
            "<td><span class='sentiment sent-mixed'>Pending</span></td></tr>"
        )

    # Add the pending securities at the bottom of Current ranking so the configured universe is always visible.
    marker = "</tbody></table>"
    if marker not in page:
        raise RuntimeError("Current ranking table not found")
    page = page.replace(marker, "".join(pending_rows) + marker, 1)

    css = """
<style id='pending-universe-css'>
.pending-security{opacity:.78;background:#0b1423}.pending-security td{border-bottom:1px dashed #29415e}.pending-note{display:block;color:#8fa4bf;font-size:10px;margin-top:3px;font-weight:500;white-space:normal;max-width:190px}.pending-security .ticker{color:#c4d2e4}
</style>
"""
    if "pending-universe-css" not in page:
        page = page.replace("</head>", css + "</head>")

    # Universe KPI should reflect configured securities, not only securities with an existing score row.
    page = re.sub(r"(<div class='label'>Universe</div><div class='value'>)\d+( securities</div>)", rf"\g<1>{len(CONFIG['universe'])}\g<2>", page, count=1)
    page = page.replace(
        "Sorted by Buy-Now score. ETF valuation/quality/growth fields are intentionally N/A.",
        "Sorted by Buy-Now score. Newly added securities without a completed-session score are shown at the bottom as Pending. ETF valuation/quality/growth fields are intentionally N/A.",
        1,
    )

    DASH.write_text(page, encoding="utf-8")
    print("Pending configured securities added to ranking:", ", ".join(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
