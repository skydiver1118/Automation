import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from investment_dashboard import compare_snapshot, build_payload, idea_state, TECH, FUND

def snapshot(date, scores, version='v2', fingerprint='same'):
    return pd.DataFrame([dict(ticker=t,as_of=date,buy_now_score=v,long_term_score=v,short_term_score=v,scoring_version=version,scoring_fingerprint=fingerprint,asset_type='Stock',price=100) for t,v in scores.items()])

class TrackerTest(unittest.TestCase):
    def test_full_universe_rank_and_ties(self):
        hist=pd.concat([snapshot('2026-09-03',{'A':60,'B':70,'C':50}),snapshot('2026-09-04',{'A':80,'B':70,'C':70})])
        changes,status=compare_snapshot(hist,'2026-09-04','2026-09-03','buy_now_score')
        self.assertEqual(status,'Comparable');self.assertEqual(changes['A'],{'delta':20.,'rank_delta':1})
        self.assertEqual(changes['C']['rank_delta'],1)
    def test_replaced_ticker_same_count_blocks_comparison(self):
        hist=pd.concat([snapshot('2026-09-03',{'A':60,'B':70}),snapshot('2026-09-04',{'A':80,'C':70})])
        self.assertEqual(compare_snapshot(hist,'2026-09-04','2026-09-03','buy_now_score')[1],'Method / universe reset')
    def test_fingerprint_change_blocks_comparison(self):
        hist=pd.concat([snapshot('2026-09-03',{'A':60},fingerprint='old'),snapshot('2026-09-04',{'A':80})])
        self.assertFalse(compare_snapshot(hist,'2026-09-04','2026-09-03','buy_now_score')[0])
    def test_missing_session_is_not_forward_filled(self):
        hist=pd.concat([snapshot('2026-09-02',{'A':60}),snapshot('2026-09-04',{'A':80})])
        payload=build_payload(hist,{'universe':['A']},{},{})
        self.assertEqual(payload['targets']['daily'],'2026-09-03')
        self.assertEqual(payload['comparison_status']['daily'],'Missing session')
        self.assertIsNone(payload['records'][0]['changes']['buy_now_score']['daily'])
    def test_holiday_calendar_and_stale_entry(self):
        hist=snapshot('2026-09-11',{'A':80})
        payload=build_payload(hist,{'universe':['A']},{'as_of':'2026-09-10'}, {'as_of':'2026-09-10','top3':[{'ticker':'A','entry_zone':[90,100]}]})
        self.assertEqual(payload['targets']['weekly'],'2026-09-03')
        self.assertEqual(payload['records'][0]['entry'],{})
    def test_initial_point_removed(self):
        hist=pd.concat([snapshot('2026-08-14',{'A':90}),snapshot('2026-08-17',{'A':70})])
        payload=build_payload(hist,{'universe':['A']},{},{})
        self.assertNotIn('2026-08-14',payload['dates'])
    def test_entry_timing_and_missing_data(self):
        row={f:1 for f in TECH+FUND};row.update(price=100,asset_type='Stock',long_term_score=70,short_term_score=75,rsi14=60,dist_50dma=.05,macd_hist=1)
        entry={'entry_zone':[95,101],'stop_reference':90}
        self.assertEqual(idea_state(row,entry),'In entry zone')
        self.assertEqual(idea_state(dict(row,price=110),entry),'Wait for pullback')
        self.assertEqual(idea_state(dict(row,short_term_score=50),entry),'In zone; timing weak')
        self.assertEqual(idea_state(dict(row,price=85),entry),'Setup broken')
        self.assertEqual(idea_state({'price':100},entry),'Check data')
        self.assertEqual(idea_state(row,{}),'Entry unavailable')

if __name__=='__main__': unittest.main()
