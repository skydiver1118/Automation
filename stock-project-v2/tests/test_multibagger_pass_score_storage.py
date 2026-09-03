from __future__ import annotations

import copy
import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "store_multibagger_pass_scores.py"
SPEC = importlib.util.spec_from_file_location("multibagger_store", SCRIPT_PATH)
assert SPEC and SPEC.loader
store = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = store
SPEC.loader.exec_module(store)


def complete_pass(score: int, source_id: str = "source-1") -> dict:
    return {
        "status": "complete",
        "score": score,
        "completion_pct": 100,
        "confidence": "high",
        "source_ids": [source_id],
        "findings": ["Validated finding."],
        "missing_fields": [],
    }


def build_snapshot(run_date: str = "2026-09-03", revision: int = 1) -> dict:
    passes = {
        store.PASS_KEYS[0]: complete_pass(90),
        store.PASS_KEYS[1]: complete_pass(82),
        store.PASS_KEYS[2]: complete_pass(78),
        store.PASS_KEYS[3]: complete_pass(75),
        store.PASS_KEYS[4]: complete_pass(67),
        store.PASS_KEYS[5]: complete_pass(72),
    }
    return {
        "$schema": "../schemas/pass_scores.schema.json",
        "schema_version": "1.0.0",
        "methodology_version": "multi-bagger-v2.1",
        "run_date": run_date,
        "snapshot_revision": revision,
        "market_session_date": "2026-09-02",
        "run_type": "regular_refresh",
        "generated_at": "2026-09-03T12:00:00-04:00",
        "recorded_at": "2026-09-03T16:01:00Z",
        "source_time_precision": "exact",
        "price_basis": "2026-09-02 regular-session close",
        "universe_size": 1,
        "changes": {
            "top20_additions": [],
            "top20_removals": [],
            "index_etf_changes": [],
            "entry_zone_hits": [],
            "notes": [],
        },
        "corrections": [],
        "record_limitations": [],
        "stocks": [
            {
                "ticker": "TEST",
                "rank": 1,
                "rank_delta": 0,
                "market_cap_usd": 1_000_000_000,
                "market_cap_display": "~$1.00B",
                "multi_bagger_score": 85,
                "multi_bagger_score_delta": 1,
                "expectation_valuation_score": 78,
                "expectation_valuation_score_delta": 2,
                "weekly_technical_score": 67,
                "weekly_technical_score_delta": 3,
                "probability_5x_pct": 25,
                "data_confidence": "high",
                "action": "WAIT",
                "thesis_status": "intact",
                "thesis_note": "Test thesis remains intact.",
                "entry_zone": {
                    "display": "$8-10",
                    "low": 8.0,
                    "high": 10.0,
                    "qualifier": None,
                    "hit_status": "not_hit",
                },
                "passes": passes,
            }
        ],
    }


def build_evidence(snapshot: dict) -> dict:
    return {
        "$schema": "../schemas/evidence_manifest.schema.json",
        "schema_version": "1.0.0",
        "run_date": snapshot["run_date"],
        "snapshot_revision": snapshot["snapshot_revision"],
        "sources": [
            {
                "source_id": "source-1",
                "source_type": "10-Q",
                "title": "Test filing",
                "source_date": "2026-08-01",
                "retrieved_at": "2026-09-03T15:00:00Z",
                "locator": "SEC accession test",
                "content_sha256": "a" * 64,
                "notes": "Test source.",
            }
        ],
        "limitations": [],
    }


class MultiBaggerPassScoreStorageTests(unittest.TestCase):
    def test_persist_and_verify_complete_snapshot(self) -> None:
        snapshot = build_snapshot()
        evidence = build_evidence(snapshot)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = store.persist_snapshot(snapshot, root, evidence=evidence, require_complete=True)
            self.assertTrue(all(path.exists() for path in paths))
            result = store.verify_repository(root, require_complete=True)
            self.assertEqual(result, {"snapshots": 1, "history_rows": 1, "stocks_in_latest": 1})

            with (root / "data/multi_bagger/history/pass_score_history.csv").open(
                "r", encoding="utf-8", newline=""
            ) as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["pass_5_score"], "67")
            self.assertEqual(rows[0]["pass_5_status"], "complete")

    def test_idempotent_replay_does_not_duplicate_history(self) -> None:
        snapshot = build_snapshot()
        evidence = build_evidence(snapshot)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store.persist_snapshot(snapshot, root, evidence=evidence)
            store.persist_snapshot(snapshot, root, evidence=evidence)
            with (root / "data/multi_bagger/history/pass_score_history.csv").open(
                "r", encoding="utf-8", newline=""
            ) as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)

    def test_conflicting_same_revision_is_rejected(self) -> None:
        snapshot = build_snapshot()
        evidence = build_evidence(snapshot)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store.persist_snapshot(snapshot, root, evidence=evidence)
            changed = copy.deepcopy(snapshot)
            changed["stocks"][0]["multi_bagger_score"] = 84
            with self.assertRaises(store.ValidationError):
                store.persist_snapshot(changed, root, evidence=evidence)

    def test_revision_two_preserves_revision_one_and_updates_latest(self) -> None:
        first = build_snapshot()
        second = build_snapshot(revision=2)
        second["run_type"] = "correction"
        second["stocks"][0]["multi_bagger_score"] = 84
        second["corrections"] = [
            {
                "ticker": "TEST",
                "field": "multi_bagger_score",
                "prior_value": 85,
                "corrected_value": 84,
                "reason": "Test correction.",
            }
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            store.persist_snapshot(first, root, evidence=build_evidence(first))
            store.persist_snapshot(second, root, evidence=build_evidence(second))
            self.assertTrue((root / "data/multi_bagger/pass_scores/2026-09-03.json").exists())
            self.assertTrue((root / "data/multi_bagger/pass_scores/2026-09-03-r2.json").exists())
            latest = json.loads((root / "data/multi_bagger/pass_scores/latest.json").read_text())
            self.assertEqual(latest["snapshot_revision"], 2)
            self.assertEqual(store.verify_repository(root)["history_rows"], 2)

    def test_duplicate_ticker_is_rejected(self) -> None:
        snapshot = build_snapshot()
        duplicate = copy.deepcopy(snapshot["stocks"][0])
        duplicate["rank"] = 2
        snapshot["stocks"].append(duplicate)
        snapshot["universe_size"] = 2
        with self.assertRaises(store.ValidationError):
            store.validate_snapshot(snapshot)

    def test_legacy_score_only_is_preserved_but_fails_strict_mode(self) -> None:
        snapshot = build_snapshot()
        snapshot["run_type"] = "legacy_import"
        for pass_key in store.PASS_KEYS:
            snapshot["stocks"][0]["passes"][pass_key] = {
                "status": "legacy_not_captured",
                "score": None,
                "completion_pct": None,
                "confidence": None,
                "source_ids": [],
                "findings": [],
                "missing_fields": ["structured_pass_record"],
            }
        snapshot["stocks"][0]["passes"][store.PASS_KEYS[4]] = {
            "status": "legacy_score_only",
            "score": 67,
            "completion_pct": None,
            "confidence": None,
            "source_ids": ["source-1"],
            "findings": ["Only the final technical score was preserved."],
            "missing_fields": ["technical_components"],
        }
        store.validate_snapshot(snapshot)
        with self.assertRaises(store.ValidationError):
            store.validate_snapshot(snapshot, require_complete=True)

    def test_pass_five_must_equal_weekly_technical_score(self) -> None:
        snapshot = build_snapshot()
        snapshot["stocks"][0]["passes"][store.PASS_KEYS[4]]["score"] = 66
        with self.assertRaises(store.ValidationError):
            store.validate_snapshot(snapshot)


if __name__ == "__main__":
    unittest.main()
