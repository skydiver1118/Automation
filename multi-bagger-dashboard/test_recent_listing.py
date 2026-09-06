"""Recent IPOs need 200 real sessions, not a fabricated one-year history."""
import unittest
import numpy as np
import pandas as pd
from watchlist_runtime import technical
class RecentListingTests(unittest.TestCase):
    def test_recent_listing_without_12_month_return(self):
        x=np.arange(215);c=50+.04*x+np.sin(x/3)
        f=pd.DataFrame({'Close':c,'Adj Close':c,'High':c+1,'Low':c-1,'Volume':1000000+x*100},index=pd.bdate_range(end='2026-09-04',periods=215))
        t=technical(f,'2026-09-04')
        self.assertIsNone(t['return_12m'])
        self.assertTrue(np.isfinite(t['ma200']))
        self.assertTrue(np.isfinite(t['return_3m']))
        with self.assertRaises(ValueError):technical(f.tail(199),'2026-09-04')
