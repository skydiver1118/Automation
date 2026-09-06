"""Regression tests for cross-universe normalization; no network access."""
import ast
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1] / "run_v2.py"
tree = ast.parse(SOURCE.read_text())
namespace = {"np": np, "pd": pd}
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "pct_rank"]
exec(compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), "exec"), namespace)
pct_rank = namespace["pct_rank"]

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

if __name__ == "__main__":
    unittest.main()
