from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT_CSV = Path("reports/nasdaq100_top3_l126_s21_dca3_signal.csv")
DEFAULT_OUTPUT_JSON = Path("reports/nasdaq100_top3_l126_s21_dca3_signal.json")
DEFAULT_STATE_JSON = Path("reports/nasdaq100_top3_l126_s21_dca3_state.json")
DEFAULT_EXECUTION_JSON = Path("reports/nasdaq100_top3_l126_s21_dca3_execution.json")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Stale fallback writer for NASDAQ100 Top3 L126 S21 none DCA3.")
    parser.add_argument("--as-of", default=None, help="Optional YYYY-MM-DD date. Defaults to today.")
    parser.add_argument("--output-csv", default=str(DEFAULT_OUTPUT_CSV))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    parser.add_argument("--state-json", default=str(DEFAULT_STATE_JSON))
    parser.add_argument("--execution-json", default=str(DEFAULT_EXECUTION_JSON))
    parser.add_argument("--env-file", default=".env.alpaca")
    parser.add_argument("--alpaca", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--target-equity-pct", type=float, default=0.95)
    parser.add_argument("--tolerance-pct", type=float, default=0.02)
    parser.add_argument("--email-to", default="")
    parser.add_argument("--failure-reason", default="", help="Original heavy executor failure text.")
    args, _ = parser.parse_known_args()

    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    signal_rows = load_json(Path(args.output_json), [])
    state = load_json(Path(args.state_json), {})

    signal_date = signal_rows[0].get("signal_date") if signal_rows else state.get("last_signal_date")
    trade_date = signal_rows[0].get("trade_date") if signal_rows else state.get("last_trade_date")
    failure_reason = (args.failure_reason or "runtime unavailable").strip()
    message = f"Heavy NASDAQ executor unavailable; stale fallback used. No paper trades submitted. cause={failure_reason}"
    report = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "paper": True,
        "strategy": "NASDAQ100 Top3 L126 S21 none DCA3",
        "status": "stale_fallback_runtime_unavailable",
        "as_of": as_of.isoformat(),
        "signal_date": signal_date,
        "trade_date": trade_date,
        "target_equity_pct": args.target_equity_pct,
        "targets": signal_rows,
        "actions": [],
        "state": state,
        "stale_fallback": True,
        "execute_requested": bool(args.execute),
        "message": message,
        "error": failure_reason,
    }

    execution_path = Path(args.execution_json)
    execution_path.parent.mkdir(parents=True, exist_ok=True)
    execution_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    print(f"warning stale_fallback_enabled cause={failure_reason}")
    print(f"execution_status={report['status']}")
    print(message)
    print(f"execution_json={execution_path}")
    if signal_rows:
        targets = ", ".join(f"{row.get('ticker')}:{float(row.get('target_weight', 0.0)):.2%}" for row in signal_rows)
        print(f"targets={targets}")
    else:
        print("targets=unknown")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
