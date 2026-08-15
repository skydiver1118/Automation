from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd


HANDLE_VOLUME_RE = re.compile(r"handle avg volume ([0-9.]+)x cup avg")


def handle_volume_ratio(candidate_json: str) -> float | None:
    candidate = json.loads(candidate_json)
    note = str(candidate.get("volume_note", ""))
    match = HANDLE_VOLUME_RE.search(note)
    if not match:
        return None
    return float(match.group(1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="reports/cup_handle_rotation_backtest/cup_handle_rotation_signals.csv")
    parser.add_argument("--output", default="reports/cup_handle_rotation_backtest_volume/cup_handle_rotation_signals.csv")
    parser.add_argument("--max-handle-cup-volume-ratio", type=float, default=1.05)
    args = parser.parse_args()

    source = Path(args.input)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    signals = pd.read_csv(source)
    signals["HandleCupVolumeRatio"] = signals["CandidateJson"].map(handle_volume_ratio)
    filtered = signals[signals["HandleCupVolumeRatio"].le(args.max_handle_cup_volume_ratio)].copy()
    filtered["WeeklyVolumeCondition"] = (
        "PASS: handle avg volume <= "
        + f"{args.max_handle_cup_volume_ratio:.2f}x cup avg"
    )
    filtered.to_csv(output, index=False)

    print(f"input_signals={len(signals)}")
    print(f"output_signals={len(filtered)}")
    print(f"removed={len(signals) - len(filtered)}")
    print(f"output={output}")


if __name__ == "__main__":
    main()
