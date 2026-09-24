import unittest
from feasibility_v22 import scenario, scenario_set

class TestFeasibilityV22(unittest.TestCase):
    def test_exact_five_x_maps_to_85_not_probability(self):
        # 100 revenue, 50% margin, 10x P/E => 500 value on 100 market cap.
        x=scenario(market_cap=100,revenue_ttm=100,revenue_cagr=0,net_margin=.5,terminal_pe=10)
        self.assertAlmostEqual(x["supportable_5y_multiple"],5)
        self.assertAlmostEqual(x["shadow_feasibility_score"],85)
        self.assertIsNone(x["calibrated_probability_5x"])

    def test_dilution_reduces_per_share_feasibility(self):
        a=scenario(market_cap=100,revenue_ttm=100,revenue_cagr=.2,net_margin=.2,terminal_pe=20,dilution_5y=0)
        b=scenario(market_cap=100,revenue_ttm=100,revenue_cagr=.2,net_margin=.2,terminal_pe=20,dilution_5y=.5)
        self.assertLess(b["supportable_5y_multiple"],a["supportable_5y_multiple"])

    def test_market_cap_is_hurdle_not_hard_exclusion(self):
        small=scenario(market_cap=10,revenue_ttm=10,revenue_cagr=.4,net_margin=.3,terminal_pe=25)
        large=scenario(market_cap=1000,revenue_ttm=1000,revenue_cagr=.4,net_margin=.3,terminal_pe=25)
        self.assertAlmostEqual(small["supportable_5y_multiple"],large["supportable_5y_multiple"])

    def test_scenario_set_never_changes_production_rank(self):
        s=scenario_set(market_cap=100,revenue_ttm=50,
            bear={"revenue_cagr":.05,"net_margin":.1,"terminal_pe":12},
            base={"revenue_cagr":.15,"net_margin":.15,"terminal_pe":18},
            bull={"revenue_cagr":.25,"net_margin":.2,"terminal_pe":22})
        self.assertFalse(s["production_rank_effect"])
        self.assertEqual(s["methodology"],"MB_5X_FEASIBILITY_SHADOW_V2_2")

if __name__=="__main__":
    unittest.main()
