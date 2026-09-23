"""Regression tests for normalization and ETF scoring policy; no network access."""
import ast
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "run_v2.py"
tree = ast.parse(SOURCE.read_text())
CONFIG = json.loads((ROOT / "config.json").read_text())
namespace = {"np": np, "pd": pd, "CONFIG": CONFIG}
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {"pct_rank", "weighted_mean", "score"}]
exec(compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), "exec"), namespace)
pct_rank = namespace["pct_rank"]
score = namespace["score"]

class NormalizationTest(unittest.TestCase):
    def test_inverse_and_missing_values(self):
        x = pd.Series([1., 2., 3., np.nan])
        np.testing.assert_allclose((pct_rank(x) + pct_rank(x, False))[:3], 100)
        padded = pd.concat([x, pd.Series([np.nan])], ignore_index=True)
        np.testing.assert_allclose(pct_rank(padded)[:3], pct_rank(x)[:3])
        self.assertEqual(pct_rank(x, False)[0], 100)
        self.assertEqual(pct_rank(x, False)[2], 0)

    def test_ties_and_no_dispersion(self):
        self.assertTrue(pct_rank(pd.Series([2., 2., np.nan])).eq(50).all())
        ranks = pct_rank(pd.Series([1., 1., 2.]))
        self.assertEqual(ranks[0], ranks[1])

class EtfLeveragePolicyTest(unittest.TestCase):
    @staticmethod
    def fixture():
        # Identical market inputs isolate the effect of asset metadata.
        fields = ["rs_1m", "rs_3m", "rs_6m", "rs_12m", "macd_hist", "adx14",
                  "volume_ratio_20d", "dist_20dma", "dist_50dma", "dist_200dma",
                  "rsi14", "forward_revenue_growth", "forward_eps_growth",
                  "eps_revision_signal", "fcf_yield", "fcf_margin", "roic_proxy",
                  "gross_margin", "operating_margin", "forward_pe", "ev_sales",
                  "ev_ebitda", "debt_to_equity"]
        rows = []
        for ticker, asset_type in [("SOXL", "ETF"), ("QTUM", "ETF"), ("NVDA", "Stock")]:
            row = dict.fromkeys(fields, 1.0)
            row.update(ticker=ticker, asset_type=asset_type, price=100.0)
            rows.append(row)
        return pd.DataFrame(rows)

    def test_production_penalty_is_zero_and_leverage_metadata_retained(self):
        self.assertEqual(CONFIG["etf_scoring"]["leveraged_long_term_penalty"], 0)
        self.assertTrue(CONFIG["etf_metadata"]["SOXL"]["leveraged"])
        self.assertEqual(CONFIG["etf_metadata"]["SOXL"]["leverage"], 3)

    def test_identical_etfs_receive_identical_scores_regardless_of_leverage(self):
        result = score(self.fixture()).set_index("ticker")
        for column in ["long_term_score", "short_term_score", "buy_now_score"]:
            self.assertEqual(result.at["SOXL", column], result.at["QTUM", column])
        self.assertEqual(result.at["SOXL", "long_term_score"], 50.0)

    def test_only_the_fixed_long_term_deduction_is_removed(self):
        current = score(self.fixture()).set_index("ticker")
        old_config = json.loads(json.dumps(CONFIG))
        old_config["etf_scoring"]["leveraged_long_term_penalty"] = 15
        with patch.dict(namespace, {"CONFIG": old_config}):
            previous = score(self.fixture()).set_index("ticker")
        self.assertEqual(current.at["SOXL", "long_term_score"] - previous.at["SOXL", "long_term_score"], 15.0)
        self.assertEqual(current.at["SOXL", "short_term_score"], previous.at["SOXL", "short_term_score"])
        for ticker in ["QTUM", "NVDA"]:
            for column in ["long_term_score", "short_term_score", "buy_now_score"]:
                self.assertEqual(current.at[ticker, column], previous.at[ticker, column])

if __name__ == "__main__":
    unittest.main()
