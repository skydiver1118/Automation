from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any


DEFAULT_STATE_JSON = Path("reports/nasdaq100_top3_l126_s21_dca3_state.json")
DEFAULT_EXECUTION_JSON = Path("reports/nasdaq100_top3_l126_s21_dca3_execution.json")


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_skip_execution(path: Path, *, as_of: date, state: dict[str, Any]) -> None:
    execution_report = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "paper": True,
        "strategy": "NASDAQ100 Top3 L126 S21 none DCA3",
        "status": "skipped_already_rebalanced_this_month",
        "as_of": as_of.isoformat(),
        "state": state,
        "message": f"State already shows a rebalance for {as_of.strftime('%Y-%m')}; no duplicate paper rebalance run.",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(execution_report, indent=2, sort_keys=True), encoding="utf-8")
    print(f"execution_status={execution_report['status']}")
    print(execution_report["message"])
    print(f"execution_json={path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight skip checks for NASDAQ100 Top3 L126 S21 none DCA3.")
    parser.add_argument("--as-of", default=None, help="Optional YYYY-MM-DD date. Defaults to today.")
    parser.add_argument("--state-json", default=str(DEFAULT_STATE_JSON))
    parser.add_argument("--execution-json", default=str(DEFAULT_EXECUTION_JSON))
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--force", action="store_true")
    args, _ = parser.parse_known_args()

    if not args.execute or args.force:
        return 10

    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    state = load_state(Path(args.state_json))
    if state.get("last_rebalance_month") != as_of.strftime("%Y-%m"):
        return 10

    write_skip_execution(Path(args.execution_json), as_of=as_of, state=state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
