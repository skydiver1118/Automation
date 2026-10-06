"""Offline completed-session download regressions; never call Yahoo."""
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("run_v2", ROOT / "run_v2.py")
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)
AS_OF = date(2026, 10, 1)


def bars(dates=("2026-09-30", "2026-10-01"), closes=(10., 11.)):
    return pd.DataFrame({"Open": closes, "High": closes, "Low": closes,
                         "Close": closes, "Volume": 100.}, index=pd.to_datetime(list(dates)))


def batch(**frames):
    return pd.concat(frames, axis=1)


class CompletedSessionTest(unittest.TestCase):
    def test_close_buffer_midnight_weekend_and_early_close(self):
        for now, expected in [
            ("2026-10-01T20:14:59Z", date(2026, 9, 30)),
            ("2026-10-01T20:15:00Z", AS_OF),
            ("2026-10-02T01:35:52Z", AS_OF),
            ("2026-10-02T13:30:00Z", AS_OF),
            ("2026-10-03T12:00:00Z", date(2026, 10, 2)),
            ("2026-11-27T18:14:59Z", date(2026, 11, 25)),
            ("2026-11-27T18:15:00Z", date(2026, 11, 27)),
        ]:
            with self.subTest(now=now):
                self.assertEqual(run.latest_completed_session(pd.Timestamp(now)), expected)


class PriceDownloadTest(unittest.TestCase):
    def download(self, responses):
        provider = Mock(side_effect=responses)
        log = io.StringIO()
        with patch.object(run.yf, "download", provider), contextlib.redirect_stdout(log):
            result = run.download_completed_prices(["NVDA", "QQQ"], AS_OF)
        return result, provider, log.getvalue()

    def test_fresh_batch_avoids_retry_and_preserves_values(self):
        frame = batch(NVDA=bars(), QQQ=bars())
        result, provider, log = self.download([frame])
        self.assertEqual(provider.call_count, 1)
        pd.testing.assert_frame_equal(result["NVDA"], frame["NVDA"])
        self.assertIn("NVDA", log)
        self.assertIn("latest_close=2026-10-01", log)

    def test_mixed_dates_retry_only_missing_symbol_with_explicit_history(self):
        stale = bars(("2026-09-29", "2026-09-30"))
        revised = bars(closes=(20., 21.))
        result, provider, log = self.download([batch(NVDA=stale, QQQ=bars()), batch(NVDA=revised)])
        self.assertEqual(provider.call_count, 2)
        args, kwargs = provider.call_args
        self.assertEqual(args[0], ["NVDA"])
        self.assertEqual(kwargs["start"], "2025-04-01")
        self.assertEqual(kwargs["end"], "2026-10-02")
        self.assertNotIn("period", kwargs)
        self.assertFalse(kwargs["threads"])
        self.assertTrue(kwargs["auto_adjust"])
        pd.testing.assert_frame_equal(result["NVDA"], revised)
        self.assertEqual(result["QQQ"].Close.iloc[-1], 11.)
        self.assertIn("latest_close=2026-09-30", log)
        self.assertIn("explicit", log)

    def test_missing_ticker_and_flat_single_ticker_response(self):
        result, provider, _ = self.download([batch(QQQ=bars()), bars()])
        self.assertEqual(provider.call_count, 2)
        self.assertEqual(result["NVDA"].Close.iloc[-1], 11.)

    def test_empty_batch_retries_each_symbol(self):
        result, provider, _ = self.download([pd.DataFrame(), bars(), bars()])
        self.assertEqual(set(result), {"NVDA", "QQQ"})
        self.assertEqual(provider.call_count, 3)

    def test_nan_or_infinite_close_does_not_pass_as_fresh(self):
        for value in (np.nan, np.inf, -np.inf):
            with self.subTest(value=value):
                broken = bars()
                broken.loc[pd.Timestamp(AS_OF), "Close"] = value
                result, provider, _ = self.download([batch(NVDA=broken, QQQ=bars()), bars()])
                self.assertEqual(provider.call_count, 2)
                self.assertEqual(result["NVDA"].Close.iloc[-1], 11.)

    def test_benchmark_needs_finite_close_too(self):
        broken = bars()
        broken.loc[pd.Timestamp(AS_OF), "Close"] = np.nan
        result, provider, _ = self.download([batch(NVDA=bars(), QQQ=broken), bars()])
        self.assertEqual(provider.call_args.args[0], ["QQQ"])
        self.assertTrue(np.isfinite(result["QQQ"].Close.iloc[-1]))

    def test_timezone_aware_daily_bars_are_market_dates(self):
        frame = bars()
        frame.index = pd.to_datetime(["2026-10-01T03:30:00Z", "2026-10-02T03:30:00Z"])
        result, provider, _ = self.download([batch(NVDA=frame, QQQ=frame)])
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(result["NVDA"].index.tolist(), list(pd.to_datetime(["2026-09-30", "2026-10-01"])))

    def test_naive_daily_labels_are_not_shifted_to_prior_day(self):
        result, _, _ = self.download([batch(NVDA=bars(), QQQ=bars())])
        self.assertEqual(result["NVDA"].index[-1].date(), AS_OF)

    def test_future_rows_do_not_change_current_price(self):
        frame = bars(("2026-09-30", "2026-10-01", "2026-10-02"), (10., 11., 999.))
        result, _, log = self.download([batch(NVDA=frame, QQQ=frame)])
        self.assertEqual(result["NVDA"].Close.iloc[-1], 11.)
        self.assertIn("latest_close=2026-10-02", log)
        self.assertIn("completed_close=2026-10-01", log)

    def test_no_stale_fallback_after_empty_stale_or_failed_retry(self):
        for retry in (pd.DataFrame(), bars(("2026-09-29", "2026-09-30")), RuntimeError("provider unavailable")):
            with self.subTest(retry=type(retry).__name__):
                provider = Mock(side_effect=[batch(QQQ=bars()), retry])
                with patch.object(run.yf, "download", provider), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaisesRegex(RuntimeError, "NVDA.*2026-10-01|2026-10-01.*NVDA"):
                        run.download_completed_prices(["NVDA", "QQQ"], AS_OF)
                self.assertEqual(provider.call_count, 3)  # diagnostic-only raw probe

    def test_missing_close_column_is_retried(self):
        result, provider, _ = self.download([batch(NVDA=bars().drop(columns="Close"), QQQ=bars()), bars()])
        self.assertEqual(provider.call_count, 2)
        self.assertEqual(result["NVDA"].Close.iloc[-1], 11.)

    def test_sort_daily_rows_without_synthesizing_prices(self):
        frame = bars().iloc[::-1]
        result, provider, _ = self.download([batch(NVDA=frame, QQQ=frame)])
        self.assertEqual(provider.call_count, 1)
        self.assertEqual(result["NVDA"].Close.tolist(), [10., 11.])


class MainGuardTest(unittest.TestCase):
    def test_incomplete_universe_never_scores_or_overwrites_saved_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "latest_scores.csv"
            saved.write_text("previous verified snapshot")
            cfg = dict(run.CONFIG, universe=["NVDA"], benchmarks={"QQQ": 1.})
            provider = Mock(side_effect=[batch(NVDA=bars(("2026-09-29", "2026-09-30")), QQQ=bars()), pd.DataFrame(), bars()])
            with patch.object(run, "ROOT", root), patch.object(run, "CONFIG", cfg), patch.object(run, "latest_completed_session", return_value=AS_OF), patch.object(run.yf, "download", provider), patch.object(run, "scoring_fingerprint", return_value="unchanged"), patch.object(run, "score") as score, patch.object(sys, "argv", ["run_v2.py", "--latest-completed"]), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(RuntimeError):
                    run.main()
            score.assert_not_called()
            self.assertEqual(saved.read_text(), "previous verified snapshot")
            self.assertFalse((root / "history").exists())


class PriceDiagnosticTest(unittest.TestCase):
    def test_diagnostics_identify_invalid_input_without_mutating_it(self):
        frame = bars()
        frame.loc[pd.Timestamp(AS_OF), "Close"] = np.inf
        before = frame.copy(deep=True)
        log = io.StringIO()
        with contextlib.redirect_stdout(log):
            run.completed_prices(frame, "NVDA", AS_OF, "explicit", single=True)
        records = [json.loads(line.split(" ", 1)[1])
                   for line in log.getvalue().splitlines() if line.startswith("PRICE_DIAG ")]
        self.assertTrue(records, "missing structured price diagnostics")
        self.assertEqual([r["boundary"] for r in records], ["received", "normalized", "accepted"])
        self.assertEqual(records[0]["tail"][-1]["Close"], "Infinity")
        self.assertEqual(records[-1]["tail"][-1]["date"], "2026-09-30T00:00:00")
        pd.testing.assert_frame_equal(frame, before)

    def test_raw_probe_cannot_rescue_invalid_adjusted_data(self):
        stale = bars(("2026-09-29", "2026-09-30"))
        raw = bars()
        raw["Adj Close"] = raw.Close / 2
        provider = Mock(side_effect=[batch(NVDA=stale), stale, raw])
        log = io.StringIO()
        with patch.object(run.yf, "download", provider), contextlib.redirect_stdout(log):
            with self.assertRaisesRegex(RuntimeError, "refusing mixed/stale"):
                run.download_completed_prices(["NVDA"], AS_OF)
        self.assertEqual(provider.call_count, 3)
        self.assertFalse(provider.call_args.kwargs["auto_adjust"])
        self.assertIn('"Adj Close": 5.5', log.getvalue())
        self.assertIn('"boundary": "raw_probe"', log.getvalue())

    def test_probe_is_bounded_and_errors_do_not_replace_guard_failure(self):
        symbols = ["NVDA", "MU", "AVGO", "SMH", "QQQ"]
        provider = Mock(side_effect=RuntimeError("request failed: private cookie text"))
        log = io.StringIO()
        with patch.object(run.yf, "download", provider), contextlib.redirect_stdout(log):
            with self.assertRaisesRegex(RuntimeError, "Incomplete universe/benchmarks"):
                run.download_completed_prices(symbols, AS_OF)
        probes = [c for c in provider.call_args_list if c.kwargs["auto_adjust"] is False]
        self.assertEqual([c.args[0] for c in probes], [["NVDA"], ["SMH"], ["QQQ"]])
        self.assertNotIn("private cookie text", log.getvalue())


if __name__ == "__main__":
    unittest.main()
