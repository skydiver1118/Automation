#!/usr/bin/env python3
"""Frozen MB25 research calibration, NOT a reproduction of archived official scores.
Inputs are primary-reconciled measurements and separately identified analyst grades.
This module is the only calculator for the displayed research comparison. No network.
"""
from __future__ import annotations
import math, copy
import numpy as np
FACTORS=['tam', 'growth', 'economics', 'balance', 'dilution', 'moat', 'execution', 'valuation']
WEIGHTS={'base': [15, 15, 10, 10, 10, 15, 10, 15], 'growth': [20, 25, 10, 5, 5, 15, 5, 15], 'quality': [10, 10, 15, 15, 15, 15, 10, 10]}
ANCHORS={'growth': ([-0.2, 0, 0.1, 0.2, 0.4, 0.6], [0, 25, 50, 70, 90, 100]), 'op': ([-0.5, -0.2, 0, 0.1, 0.2, 0.3], [0, 20, 50, 75, 90, 100]), 'fcfm': ([-1, -0.3, -0.1, 0, 0.1, 0.2, 0.3], [0, 15, 35, 50, 75, 90, 100]), 'leverage': ([-1, 0, 1, 2, 3, 4, 6, 8], [100, 90, 80, 65, 50, 35, 10, 0]), 'runway': ([0, 6, 12, 24, 36, 60], [0, 20, 40, 70, 85, 100]), 'dilution': ([-0.05, 0, 0.05, 0.1, 0.2, 0.4, 0.6], [100, 90, 70, 50, 25, 5, 0]), 'fwdgp': ([1, 3, 5, 10, 20, 40, 60], [100, 90, 80, 60, 35, 10, 0]), 'fcfy': ([-0.1, -0.02, 0, 0.02, 0.05, 0.08, 0.1], [0, 20, 40, 60, 80, 95, 100]), 'revision': ([-0.2, -0.1, 0, 0.1, 0.2], [0, 20, 50, 80, 100]), 'rsi': ([30, 50, 65, 80, 90], [0, 50, 100, 50, 0])}

def valid(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)

def clip(x): return max(0.0,min(100.0,float(x)))

def score(x,key):
    if not valid(x):return None
    return float(np.interp(x,*ANCHORS[key]))

def div(a,b):return a/b if valid(a) and valid(b) and b!=0 else None

def atomic(parts):
    usable=[(s,w) for s,w in parts if s is not None]
    cov=sum(w for s,w in usable)
    return (sum(s*w for s,w in usable)/cov if cov else None,cov)

def aggregate(factors,coverage,weights):
    den=sum(w*coverage[k] for k,w in zip(FACTORS,weights) if factors[k] is not None)
    num=sum(w*coverage[k]*factors[k] for k,w in zip(FACTORS,weights) if factors[k] is not None)
    return num/den if den else None,den/100,num/100,(num+100*(100-den))/100

def technical(t,bench):
    p=t['price'];a=t['atr14']
    trend=sum(w for n,w in [(20,30),(50,30),(200,40)] if p>t[f'ma{n}'])
    direction=np.sign(t['plus_di']-t['minus_di'])
    mom=.4*score(t['rsi14'],'rsi')+.4*clip(50+250*t['macd_hist']/a)+.2*clip(50+direction*min(t['adx14'],50))
    excess=np.mean([t['return_'+h]-(bench['QQQ']['return_'+h]+bench['SMH']['return_'+h])/2 for h in ['1m','3m']])
    vol=clip(50+25*(t['volume_ratio20']-1)*np.sign(p/t['ma20']-1))
    pos=clip(100*(p-t['low20'])/(t['high20']-t['low20']))
    factors={'trend':trend,'momentum':mom,'rs_volume':.75*clip(50+200*excess)+.25*vol,'support':.5*clip(100-25*abs(p-t['ma20'])/a)+.5*pos,'confirmation':.5*pos+.5*vol}
    total=sum(factors[k]*w for k,w in zip(factors,[.3,.2,.2,.2,.1]))
    return float(total),{k:float(v) for k,v in factors.items()}

def calculate(o,r,bench):
    f={};c={};sub={}
    ta,mo,ex,rat=o['analyst_grades']
    for k,v in [('tam',ta),('moat',mo),('execution',ex)]:f[k]=v;c[k]=1.
    o['analyst_rationale']=rat
    growthparts=[(score(o['current_growth'],'growth'),.5),(score(o['next_year_growth'],'growth'),.5)]
    f['growth'],c['growth']=atomic(growthparts)
    if o['revenue_ttm'] is not None and o['revenue_ttm']<25e6 and f['growth'] is not None:f['growth']=min(f['growth'],80.)
    o['operating_margin']=div(o['operating_income_ttm'],o['revenue_ttm']);o['fcf_margin']=div(o['fcf_ttm'],o['revenue_ttm']);o['gross_margin']=div(o['gross_profit_ttm'],o['revenue_ttm'])
    f['economics'],c['economics']=atomic([(score(o['operating_margin'],'op'),.5),(score(o['fcf_margin'],'fcfm'),.5)])
    ebitda=o['operating_income_ttm']+o['da_ttm'] if valid(o['operating_income_ttm']) and valid(o['da_ttm']) else None
    o['operating_ebitda_ttm']=ebitda
    o['net_debt_ebitda']=None;o['runway_months']=None
    if ebitda is not None and ebitda>0:
        o['net_debt_ebitda']=(o['debt']-o['cash'])/ebitda;f['balance']=score(o['net_debt_ebitda'],'leverage')
    elif valid(o['fcf_ttm']) and o['fcf_ttm']<0:
        o['runway_months']=o['cash']/(-o['fcf_ttm']/12);f['balance']=score(o['runway_months'],'runway')
    else:f['balance']=None
    c['balance']=1. if f['balance'] is not None else 0.
    f['dilution']=score(o['dilution_yoy'],'dilution');c['dilution']=float(f['dilution'] is not None)
    o['forward_gp']=o['next_year_revenue']*o['gross_margin'] if valid(o['next_year_revenue']) and valid(o['gross_margin']) else None
    o['ev_forward_gp']=div(o['enterprise_value'],o['forward_gp']) if valid(o['forward_gp']) and o['forward_gp']>0 else None
    o['fcf_yield']=div(o['fcf_ttm'],o['market_cap'])
    gp_score=score(o['ev_forward_gp'],'fwdgp') if o['enterprise_value']>0 else None
    if valid(o['gross_profit_ttm']) and o['gross_profit_ttm']<=0:gp_score=0.
    f['valuation'],c['valuation']=atomic([(gp_score,.6),(score(o['fcf_yield'],'fcfy'),.4)])
    rev=None
    if valid(o['eps_current']) and valid(o['eps_90days_ago']) and o['eps_90days_ago']>0:rev=o['eps_current']/o['eps_90days_ago']-1
    o['eps_revision90']=rev
    # Coverage propagates to the headline score at atomic component weights.
    evparts=[(f['valuation'],.7*c['valuation']),(score(rev,'revision'),.3)]
    ev,evcov=atomic(evparts)
    mb,cov,lb,ub=aggregate(f,c,WEIGHTS['base'])
    tech,techf=technical(r['technical'],bench)
    result={**o,'factor_scores':f,'factor_coverage':c,'research_mb_score':mb,'mb_input_weight_coverage':cov,'unknown_lower_bound':lb,'unknown_upper_bound':ub,
            'research_ev_score':ev,'ev_input_weight_coverage':evcov,'technical_score':tech,'technical_components':techf}
    for key in ['growth','quality']:result[key+'_weight_score']=aggregate(f,c,WEIGHTS[key])[0]
    for label,delta in [('analyst_low',-12.5),('analyst_high',12.5)]:
        ff=dict(f)
        for k in ['tam','moat','execution']:ff[k]=clip(ff[k]+delta)
        result[label]=aggregate(ff,c,WEIGHTS['base'])[0]
    result['numerical_coverage_sufficient']=cov>=.9
    result['comparison_caveat']=o['ticker'] in ['FIGR','SOUN','GRRR','POET']
    result['full_research_validation_complete']=False # Membership approval is not scoring-model validation.
    result['confidence']='Lower' if result['comparison_caveat'] or o['ticker']=='RZLV' else ('Medium' if o['ticker'] in ['AMPX','APLD','BKSY','WULF','TSSI','RR','SSII'] else 'Medium-high')
    return result

def compute_all(payload):
    rows=[calculate(copy.deepcopy(x['financial']), {'technical':x['technical']}, payload['benchmarks']) for x in payload['stocks']]
    rows.sort(key=lambda x:(-x['research_mb_score'],x['ticker']))
    for rank,row in enumerate(rows,1):row['research_rank']=rank
    for kind in ['growth','quality']:
        ordered=sorted(rows,key=lambda x:(-x[kind+'_weight_score'],x['ticker']))
        for rank,row in enumerate(ordered,1):row[kind+'_weight_rank']=rank
    for row in rows:
        rr=[row['research_rank'],row['growth_weight_rank'],row['quality_weight_rank']]
        row['weight_rank_low']=min(rr);row['weight_rank_high']=max(rr)
    return rows
